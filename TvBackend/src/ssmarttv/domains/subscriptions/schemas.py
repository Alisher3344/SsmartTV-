"""Subscription request/response schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubscriptionGrantIn(BaseModel):
    days: int | None = Field(default=None, ge=1, description="null = no expiry")
    plan: str | None = None


class SubscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    plan: str | None = None
    started_at: datetime
    expires_at: datetime | None = None


class MySubscriptionOut(BaseModel):
    is_premium: bool
    can_watch_premium: bool
    subscription: SubscriptionOut | None = None
