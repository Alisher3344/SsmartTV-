from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    username: str | None = Field(default=None, max_length=100)


class LoginIn(BaseModel):
    # May be an email OR a username — authenticate() matches either. The field
    # name stays "email" to keep the existing frontend contract unchanged.
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str | None
    is_admin: bool
    created_at: datetime
