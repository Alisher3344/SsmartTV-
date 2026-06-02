"""Premium subscription model (payment-less placeholder).

Until billing is wired up, a subscription is granted manually by a superuser.
``User.is_premium`` is the simple superuser-toggled flag; a ``Subscription`` row
is the richer, time-bounded mechanism future payments will populate. Either one
satisfies the premium access gate.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ssmarttv.db.base import Base, TimestampMixin

SUB_ACTIVE = "active"
SUB_EXPIRED = "expired"
SUB_CANCELLED = "cancelled"


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(20), default=SUB_ACTIVE, index=True)
    plan: Mapped[str | None] = mapped_column(String(40))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
