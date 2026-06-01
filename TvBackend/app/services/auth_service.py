from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.models.user import User
from app.redis import client as session_store
from app.schemas.auth import LoginIn, RegisterIn


async def register_user(db: AsyncSession, data: RegisterIn) -> User:
    existing = await db.scalar(select(User).where(User.email == data.email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    if data.username:
        dup = await db.scalar(select(User).where(User.username == data.username))
        if dup:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
            )

    user = User(
        email=data.email,
        username=data.username,
        password_hash=security.hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate(db: AsyncSession, data: LoginIn) -> User:
    # data.email may be an email or a username (e.g. the admin logs in as "admin123").
    user = await db.scalar(
        select(User).where(
            or_(User.email == data.email, User.username == data.email)
        )
    )
    if user is None or not security.verify_password(user.password_hash, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled"
        )

    # Transparently upgrade hash params if argon2 defaults changed.
    if security.needs_rehash(user.password_hash):
        user.password_hash = security.hash_password(data.password)
        await db.commit()
    return user


async def start_session(user_id: int, **meta) -> str:
    session_id = security.new_session_id()
    await session_store.create_session(session_id, user_id, **meta)
    return session_id


async def end_session(session_id: str) -> None:
    await session_store.delete_session(session_id)
