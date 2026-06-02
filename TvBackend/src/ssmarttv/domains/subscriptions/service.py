"""Premium access checks and (placeholder) subscription granting."""
from datetime import UTC, datetime, timedelta

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.exceptions import (
    AuthenticationError,
    NotFoundError,
    SubscriptionRequiredError,
)
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.catalog.models import ACCESS_PREMIUM
from ssmarttv.domains.subscriptions.models import SUB_ACTIVE, Subscription


async def has_active_subscription(db: AsyncSession, user_id: int) -> bool:
    now = datetime.now(UTC)
    sub = await db.scalar(
        select(Subscription.id).where(
            Subscription.user_id == user_id,
            Subscription.status == SUB_ACTIVE,
            or_(Subscription.expires_at.is_(None), Subscription.expires_at > now),
        )
    )
    return sub is not None


async def can_watch_premium(db: AsyncSession, user: User | None) -> bool:
    """True if the user may access premium content.

    Staff/superuser can always preview; regular users need the superuser-set
    ``is_premium`` flag or an active subscription.
    """
    if user is None:
        return False
    if user.is_staff or user.is_premium:
        return True
    return await has_active_subscription(db, user.id)


async def ensure_can_watch(db: AsyncSession, access_level: str, user: User | None) -> None:
    """Gate playback. Free is open; premium needs auth + entitlement (402)."""
    if access_level != ACCESS_PREMIUM:
        return
    if user is None:
        raise AuthenticationError("Sign in to watch premium content")
    if not await can_watch_premium(db, user):
        raise SubscriptionRequiredError()


async def grant(
    db: AsyncSession, user_id: int, *, days: int | None, plan: str | None
) -> Subscription:
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found")
    now = datetime.now(UTC)
    sub = Subscription(
        user_id=user_id,
        status=SUB_ACTIVE,
        plan=plan,
        started_at=now,
        expires_at=now + timedelta(days=days) if days else None,
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub
