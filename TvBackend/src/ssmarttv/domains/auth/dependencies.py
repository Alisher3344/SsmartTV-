"""FastAPI auth dependencies: session resolution and RBAC guards."""
import hmac
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from fastapi import Cookie, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.config import settings
from ssmarttv.core.exceptions import AuthenticationError, PermissionDeniedError
from ssmarttv.db.session import get_db
from ssmarttv.domains.auth import sessions
from ssmarttv.domains.auth.models import User

_CookieDep = Cookie(default=None, alias=settings.SESSION_COOKIE_NAME)


@dataclass
class AuthContext:
    user: User
    sid: str


async def _resolve(session_id: str | None, db: AsyncSession) -> AuthContext | None:
    if not session_id:
        return None
    data = await sessions.get(session_id)
    if data is None:
        return None
    user = await db.get(User, data["user_id"])
    if user is None or not user.is_active:
        return None
    # Sliding expiration: regular users 60d, staff 7d.
    ttl = settings.STAFF_SESSION_TTL_SECONDS if user.is_staff else settings.SESSION_TTL_SECONDS
    await sessions.get(session_id, touch_ttl=ttl)
    return AuthContext(user=user, sid=session_id)


async def get_auth_context(
    db: AsyncSession = Depends(get_db),
    session_id: str | None = _CookieDep,
) -> AuthContext:
    ctx = await _resolve(session_id, db)
    if ctx is None:
        raise AuthenticationError()
    return ctx


async def get_current_user(ctx: AuthContext = Depends(get_auth_context)) -> User:
    return ctx.user


async def get_optional_user(
    db: AsyncSession = Depends(get_db),
    session_id: str | None = _CookieDep,
) -> User | None:
    ctx = await _resolve(session_id, db)
    return ctx.user if ctx else None


def require_role(*roles: str) -> Callable[[User], Awaitable[User]]:
    allowed = set(roles)

    async def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role.slug not in allowed and not user.is_superuser:
            raise PermissionDeniedError()
        return user

    return _dep


def require_permission(slug: str) -> Callable[[User], Awaitable[User]]:
    async def _dep(user: User = Depends(get_current_user)) -> User:
        if not user.has_permission(slug):
            raise PermissionDeniedError()
        return user

    return _dep


async def require_internal_service(
    x_internal_secret: str | None = Header(default=None, alias="X-Internal-Secret"),
) -> None:
    """Guard for trusted server-to-server endpoints (e.g. SsmartShop provisioning
    TV admins). Requires a configured INTERNAL_API_SECRET and a matching header,
    compared in constant time. No user session involved."""
    secret = settings.INTERNAL_API_SECRET
    if not secret or not x_internal_secret or not hmac.compare_digest(
        x_internal_secret, secret
    ):
        raise PermissionDeniedError()
