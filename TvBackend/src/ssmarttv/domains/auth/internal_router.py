"""Trusted server-to-server endpoints for provisioning TV admin accounts.

Authenticated by a shared secret (X-Internal-Secret header), NOT a user session.
Used by the SsmartShop super-admin dashboard to create/list/delete SsmartTV
admin accounts. Reuses the same service functions as the session-based
account-management endpoints in router.py. Must never be exposed publicly
(nginx blocks /api/v1/internal/ on the tv host; reachable only via the docker
network).
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.db.session import get_db
from ssmarttv.domains.auth import service
from ssmarttv.domains.auth.dependencies import require_internal_service
from ssmarttv.domains.auth.models import STAFF_ROLES, User
from ssmarttv.domains.auth.schemas import (
    AccountCreateIn,
    AccountUpdateIn,
    MessageOut,
    UserOut,
)

internal_router = APIRouter(
    prefix="/internal/tv-admins",
    tags=["internal"],
    dependencies=[Depends(require_internal_service)],
)


@internal_router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_tv_admin(
    data: AccountCreateIn,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await service.create_staff_account(
        db,
        username=data.username,
        password=data.password,
        role_slug=data.role,
        full_name=data.full_name,
    )
    return UserOut.of(user)


@internal_router.get("", response_model=list[UserOut])
async def list_tv_admins(db: AsyncSession = Depends(get_db)) -> list[UserOut]:
    stmt = select(User).where(User.username.is_not(None)).order_by(User.id)
    users = (await db.scalars(stmt)).all()
    return [UserOut.of(u) for u in users if u.role.slug in STAFF_ROLES]


@internal_router.put("/{user_id}", response_model=UserOut)
async def update_tv_admin(
    user_id: int,
    data: AccountUpdateIn,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await service.update_staff_account(
        db,
        user_id,
        username=data.username,
        password=data.password,
        role_slug=data.role,
        full_name=data.full_name,
    )
    return UserOut.of(user)


@internal_router.delete("/{user_id}", response_model=MessageOut)
async def delete_tv_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> MessageOut:
    await service.delete_staff_account(db, user_id)
    return MessageOut(detail="Account deleted")
