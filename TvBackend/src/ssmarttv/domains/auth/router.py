"""Auth HTTP endpoints: OTP login, staff login, sessions, account management."""
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.config import settings
from ssmarttv.db.session import get_db
from ssmarttv.domains.auth import service
from ssmarttv.domains.auth.dependencies import (
    AuthContext,
    get_auth_context,
    get_current_user,
    require_permission,
)
from ssmarttv.domains.auth.models import STAFF_ROLES, User
from ssmarttv.domains.auth.permissions import ACCOUNT_MANAGE, USER_SET_PREMIUM
from ssmarttv.domains.auth.schemas import (
    AccountCreateIn,
    MessageOut,
    OtpRequestIn,
    OtpVerifyIn,
    PremiumIn,
    SessionOut,
    StaffLoginIn,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])
accounts_router = APIRouter(tags=["accounts"])


def _device_meta(request: Request) -> tuple[str | None, str | None, str | None]:
    ua = request.headers.get("user-agent")
    ip = request.client.host if request.client else None
    device = (ua.split(")")[0].split("(")[-1].strip() if ua and "(" in ua else ua) or None
    if device:
        device = device[:80]
    return device, ip, ua


def _set_cookie(response: Response, sid: str, max_age: int) -> None:
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=sid,
        max_age=max_age,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAMESITE,
        path="/",
    )


# --- Phone + OTP login ---------------------------------------------------
@router.post("/otp/request", response_model=MessageOut)
async def otp_request(data: OtpRequestIn) -> MessageOut:
    await service.request_login_otp(data.phone)
    return MessageOut(detail="Code sent")


@router.post("/otp/verify", response_model=UserOut)
async def otp_verify(
    data: OtpVerifyIn,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    device, ip, ua = _device_meta(request)
    user, sid = await service.verify_login_otp(
        db, data.phone, data.code, device=device, ip=ip, user_agent=ua
    )
    _set_cookie(response, sid, settings.SESSION_TTL_SECONDS)
    return UserOut.of(user)


# --- Staff username + password login -------------------------------------
@router.post("/staff/login", response_model=UserOut)
async def staff_login(
    data: StaffLoginIn,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    device, ip, ua = _device_meta(request)
    user, sid = await service.staff_login(
        db, data.username, data.password, device=device, ip=ip, user_agent=ua
    )
    _set_cookie(response, sid, settings.STAFF_SESSION_TTL_SECONDS)
    return UserOut.of(user)


# --- Sessions / devices --------------------------------------------------
@router.post("/logout", response_model=MessageOut)
async def logout(
    response: Response, ctx: AuthContext = Depends(get_auth_context)
) -> MessageOut:
    await service.logout(ctx.sid)
    response.delete_cookie(settings.SESSION_COOKIE_NAME, path="/")
    return MessageOut(detail="Logged out")


@router.post("/logout-all", response_model=MessageOut)
async def logout_all(
    response: Response, ctx: AuthContext = Depends(get_auth_context)
) -> MessageOut:
    count = await service.logout_all(ctx.user.id)
    response.delete_cookie(settings.SESSION_COOKIE_NAME, path="/")
    return MessageOut(detail=f"Logged out of {count} device(s)")


@router.get("/sessions", response_model=list[SessionOut])
async def list_sessions(ctx: AuthContext = Depends(get_auth_context)) -> list[SessionOut]:
    items = await service.list_sessions(ctx.user.id)
    return [
        SessionOut(
            sid=s.sid,
            created_at=s.created_at,
            last_seen=s.last_seen,
            device=s.device,
            ip=s.ip,
            user_agent=s.user_agent,
            current=s.sid == ctx.sid,
        )
        for s in items
    ]


@router.delete("/sessions/{sid}", response_model=MessageOut)
async def revoke_session(
    sid: str, ctx: AuthContext = Depends(get_auth_context)
) -> MessageOut:
    await service.revoke_session(ctx.user.id, sid)
    return MessageOut(detail="Session revoked")


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.of(user)


# --- Account management (superuser-only via ACCOUNT_MANAGE permission) ----
@accounts_router.post(
    "/staff/accounts", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def create_account(
    data: AccountCreateIn,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_permission(ACCOUNT_MANAGE)),
) -> UserOut:
    user = await service.create_staff_account(
        db,
        username=data.username,
        password=data.password,
        role_slug=data.role,
        full_name=data.full_name,
    )
    return UserOut.of(user)


@accounts_router.get("/staff/accounts", response_model=list[UserOut])
async def list_accounts(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_permission(ACCOUNT_MANAGE)),
) -> list[UserOut]:
    # Staff accounts have a username; filter to staff roles defensively.
    stmt = select(User).where(User.username.is_not(None)).order_by(User.id)
    users = (await db.scalars(stmt)).all()
    return [UserOut.of(u) for u in users if u.role.slug in STAFF_ROLES]


@accounts_router.delete("/staff/accounts/{user_id}", response_model=MessageOut)
async def delete_account(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_permission(ACCOUNT_MANAGE)),
) -> MessageOut:
    await service.delete_staff_account(db, user_id)
    return MessageOut(detail="Account deleted")


@accounts_router.post("/users/{user_id}/premium", response_model=UserOut)
async def set_premium(
    user_id: int,
    data: PremiumIn,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_permission(USER_SET_PREMIUM)),
) -> UserOut:
    user = await service.set_premium(db, user_id, data.is_premium)
    return UserOut.of(user)
