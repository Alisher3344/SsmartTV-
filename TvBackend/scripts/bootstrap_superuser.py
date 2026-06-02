"""Create (or update) the bootstrap superuser — the only way a superuser exists.

Superusers cannot be created or deleted through the API; this CLI is the sole
entry point. Staff/admin/superuser authenticate with username + password.

Usage:
    python scripts/bootstrap_superuser.py --username admin --password 'secret'
    python scripts/bootstrap_superuser.py --username admin --password 'secret' --phone +998901234567
"""
import argparse
import asyncio

from sqlalchemy import select

from ssmarttv.core.security import hash_password
from ssmarttv.db.session import async_session_maker
from ssmarttv.domains.auth.models import ROLE_SUPERUSER, Role, User


async def bootstrap(username: str, password: str, phone: str | None) -> str:
    async with async_session_maker() as session:
        role = await session.scalar(select(Role).where(Role.slug == ROLE_SUPERUSER))
        if role is None:
            raise SystemExit(
                "Superuser role not found — run scripts/seed_reference.py first."
            )
        user = await session.scalar(select(User).where(User.username == username))
        if user is None:
            user = User(username=username, role=role)
            session.add(user)
            action = "created"
        else:
            action = "updated"
        user.password_hash = hash_password(password)
        user.role = role
        user.is_active = True
        if phone:
            user.phone = phone
        await session.commit()
    return action


def main() -> None:
    parser = argparse.ArgumentParser(description="Create/update the superuser account")
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--phone", default=None)
    args = parser.parse_args()
    action = asyncio.run(bootstrap(args.username, args.password, args.phone))
    print(f"Superuser '{args.username}' {action}.")


if __name__ == "__main__":
    main()
