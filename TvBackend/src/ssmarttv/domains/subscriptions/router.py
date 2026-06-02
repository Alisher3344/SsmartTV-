"""Subscription endpoints: superuser grant + the caller's own status."""
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.db.session import get_db
from ssmarttv.domains.auth.dependencies import get_current_user, require_permission
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.auth.permissions import USER_SET_PREMIUM
from ssmarttv.domains.subscriptions import service
from ssmarttv.domains.subscriptions.models import Subscription
from ssmarttv.domains.subscriptions.schemas import (
    MySubscriptionOut,
    SubscriptionGrantIn,
    SubscriptionOut,
)

router = APIRouter(tags=["subscriptions"])


@router.post(
    "/users/{user_id}/subscription",
    response_model=SubscriptionOut,
    status_code=201,
)
async def grant_subscription(
    user_id: int,
    data: SubscriptionGrantIn,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_permission(USER_SET_PREMIUM)),
) -> SubscriptionOut:
    sub = await service.grant(db, user_id, days=data.days, plan=data.plan)
    return SubscriptionOut.model_validate(sub)


@router.get("/me/subscription", response_model=MySubscriptionOut)
async def my_subscription(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MySubscriptionOut:
    sub = await db.scalar(
        select(Subscription)
        .where(Subscription.user_id == user.id)
        .order_by(desc(Subscription.created_at))
        .limit(1)
    )
    return MySubscriptionOut(
        is_premium=user.is_premium,
        can_watch_premium=await service.can_watch_premium(db, user),
        subscription=SubscriptionOut.model_validate(sub) if sub else None,
    )
