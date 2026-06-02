"""Identity & RBAC models: User, Role, Permission.

Two authentication tracks share one ``users`` table:
- regular users (role ``user``) sign in with phone + OTP — no password;
- staff/admin/superuser sign in with username + Argon2 password.

The ``ck_users_login_identifier`` constraint guarantees every row has at least
one of (phone, username).
"""
from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ssmarttv.db.base import Base, TimestampMixin

# Role slugs are a fixed, code-referenced vocabulary.
ROLE_SUPERUSER = "superuser"
ROLE_ADMIN = "admin"
ROLE_STAFF = "staff"
ROLE_USER = "user"
STAFF_ROLES = frozenset({ROLE_SUPERUSER, ROLE_ADMIN, ROLE_STAFF})


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permissions, lazy="selectin"
    )
    users: Mapped[list[User]] = relationship(back_populates="role")

    @property
    def permission_slugs(self) -> set[str]:
        return {p.slug for p in self.permissions}


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "phone IS NOT NULL OR username IS NOT NULL",
            name="login_identifier",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # Regular users: phone (E.164). Staff: username. Either may be null.
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))  # staff only

    full_name: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(255))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    is_premium: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    role: Mapped[Role] = relationship(back_populates="users", lazy="joined")

    @property
    def is_staff(self) -> bool:
        return self.role.slug in STAFF_ROLES

    @property
    def is_superuser(self) -> bool:
        return self.role.slug == ROLE_SUPERUSER

    def has_permission(self, slug: str) -> bool:
        return self.role.slug == ROLE_SUPERUSER or slug in self.role.permission_slugs
