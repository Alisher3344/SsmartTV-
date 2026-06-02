"""Auth orchestration: OTP login, staff password login, sessions, accounts."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.config import settings
from ssmarttv.core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
)
from ssmarttv.core.phone import normalize_phone
from ssmarttv.core.ratelimit import RateLimit, hit
from ssmarttv.core.security import hash_password, needs_rehash, verify_password
from ssmarttv.domains.auth import otp, sessions
from ssmarttv.domains.auth.models import (
    ROLE_SUPERUSER,
    ROLE_USER,
    STAFF_ROLES,
    Role,
    User,
)


async def _role(db: AsyncSession, slug: str) -> Role:
    role = await db.scalar(select(Role).where(Role.slug == slug))
    if role is None:
        raise NotFoundError(f"Role '{slug}' not found — seed reference data")
    return role


# --- Regular users: phone + OTP -----------------------------------------
async def request_login_otp(phone: str) -> str:
    normalized = normalize_phone(phone)
    await otp.request_code(normalized)
    return normalized


async def verify_login_otp(
    db: AsyncSession,
    phone: str,
    code: str,
    *,
    device: str | None = None,
    ip: str | None = None,
    user_agent: str | None = None,
) -> tuple[User, str]:
    normalized = normalize_phone(phone)
    await otp.verify_code(normalized, code)

    user = await db.scalar(select(User).where(User.phone == normalized))
    if user is None:
        user = User(phone=normalized, role=await _role(db, ROLE_USER))
        db.add(user)
        await db.commit()
        await db.refresh(user)
    elif user.is_staff:
        # Staff/admin/superuser must authenticate with username + password.
        raise PermissionDeniedError("This number belongs to a staff account")
    elif not user.is_active:
        raise PermissionDeniedError("Account is disabled")

    sid = await sessions.create(
        user.id,
        settings.SESSION_TTL_SECONDS,
        device=device,
        ip=ip,
        user_agent=user_agent,
    )
    return user, sid


# --- Staff: username + password -----------------------------------------
async def staff_login(
    db: AsyncSession,
    username: str,
    password: str,
    *,
    device: str | None = None,
    ip: str | None = None,
    user_agent: str | None = None,
) -> tuple[User, str]:
    await hit("staff_login", username, RateLimit(10, 300))
    user = await db.scalar(select(User).where(User.username == username))
    if user is None or not user.password_hash or not user.is_staff:
        raise AuthenticationError("Invalid credentials")
    if not verify_password(user.password_hash, password):
        raise AuthenticationError("Invalid credentials")
    if not user.is_active:
        raise PermissionDeniedError("Account is disabled")
    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)
        await db.commit()

    sid = await sessions.create(
        user.id,
        settings.STAFF_SESSION_TTL_SECONDS,
        device=device,
        ip=ip,
        user_agent=user_agent,
    )
    return user, sid


# --- Sessions / devices --------------------------------------------------
async def logout(sid: str) -> None:
    await sessions.delete(sid)


async def logout_all(user_id: int) -> int:
    return await sessions.delete_all_for_user(user_id)


async def list_sessions(user_id: int) -> list[sessions.SessionInfo]:
    return await sessions.list_for_user(user_id)


async def revoke_session(user_id: int, sid: str) -> None:
    data = await sessions.get(sid)
    if data is None or data["user_id"] != user_id:
        raise NotFoundError("Session not found")
    await sessions.delete(sid)


# --- Account management (superuser-only; enforced by router deps) ---------
async def create_staff_account(
    db: AsyncSession,
    *,
    username: str,
    password: str,
    role_slug: str,
    full_name: str | None,
) -> User:
    if role_slug == ROLE_SUPERUSER or role_slug not in STAFF_ROLES:
        raise PermissionDeniedError("Only 'admin' and 'staff' accounts can be created")
    if await db.scalar(select(User).where(User.username == username)):
        raise ConflictError("Username already taken")
    user = User(
        username=username,
        password_hash=hash_password(password),
        full_name=full_name,
        role=await _role(db, role_slug),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_staff_account(db: AsyncSession, target_id: int) -> None:
    user = await db.get(User, target_id)
    if user is None:
        raise NotFoundError("Account not found")
    if user.is_superuser:
        raise PermissionDeniedError("Superuser accounts cannot be deleted")
    if not user.is_staff:
        raise PermissionDeniedError("Not a staff account")
    await sessions.delete_all_for_user(user.id)
    await db.delete(user)
    await db.commit()


async def update_staff_account(
    db: AsyncSession,
    target_id: int,
    *,
    username: str | None = None,
    password: str | None = None,
    role_slug: str | None = None,
    full_name: str | None = None,
) -> User:
    """Tahrirlash — faqat berilgan (not-None) maydonlar o'zgaradi. Superuser
    hisoblari bu yo'l orqali tahrirlanmaydi. Parol o'zgarsa eski sessiyalar
    bekor qilinadi (yangi parol bilan qayta kirish kerak)."""
    user = await db.get(User, target_id)
    if user is None:
        raise NotFoundError("Account not found")
    if user.is_superuser:
        raise PermissionDeniedError("Superuser accounts cannot be edited")
    if not user.is_staff:
        raise PermissionDeniedError("Not a staff account")

    if username is not None and username != user.username:
        clash = await db.scalar(select(User).where(User.username == username))
        if clash is not None and clash.id != user.id:
            raise ConflictError("Username already taken")
        user.username = username
    if role_slug is not None:
        if role_slug == ROLE_SUPERUSER or role_slug not in STAFF_ROLES:
            raise PermissionDeniedError("Role must be 'admin' or 'staff'")
        user.role = await _role(db, role_slug)
    if full_name is not None:
        user.full_name = full_name or None
    if password is not None:
        user.password_hash = hash_password(password)
        await sessions.delete_all_for_user(user.id)

    await db.commit()
    await db.refresh(user)
    return user


async def set_premium(db: AsyncSession, user_id: int, is_premium: bool) -> User:
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found")
    user.is_premium = is_premium
    await db.commit()
    await db.refresh(user)
    return user
