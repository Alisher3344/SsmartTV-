"""Auth request/response schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ssmarttv.domains.auth.models import ROLE_ADMIN, ROLE_STAFF


class OtpRequestIn(BaseModel):
    phone: str = Field(min_length=5, max_length=20)


class OtpVerifyIn(BaseModel):
    phone: str = Field(min_length=5, max_length=20)
    code: str = Field(min_length=4, max_length=8)


class StaffLoginIn(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)


class AccountCreateIn(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(description=f"'{ROLE_ADMIN}' or '{ROLE_STAFF}'")
    full_name: str | None = Field(default=None, max_length=120)


class AccountUpdateIn(BaseModel):
    """Partial update — faqat berilgan maydonlar o'zgaradi.
    Parol berilsa qayta-hash qilinadi va eski sessiyalar bekor qilinadi."""
    username: str | None = Field(default=None, min_length=3, max_length=64)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: str | None = Field(default=None, description=f"'{ROLE_ADMIN}' or '{ROLE_STAFF}'")
    full_name: str | None = Field(default=None, max_length=120)


class PremiumIn(BaseModel):
    is_premium: bool


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone: str | None
    username: str | None
    full_name: str | None
    is_active: bool
    is_premium: bool
    role: str
    permissions: list[str]
    created_at: datetime

    @classmethod
    def of(cls, user) -> "UserOut":  # type: ignore[no-untyped-def]
        return cls(
            id=user.id,
            phone=user.phone,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_premium=user.is_premium,
            role=user.role.slug,
            permissions=sorted(
                user.role.permission_slugs if not user.is_superuser else ["*"]
            ),
            created_at=user.created_at,
        )


class SessionOut(BaseModel):
    sid: str
    created_at: str
    last_seen: str
    device: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    current: bool = False


class MessageOut(BaseModel):
    detail: str
