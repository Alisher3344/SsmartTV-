"""Pytest fixtures: isolated test DB, clean Redis, and HTTP client helpers.

Tests run against a dedicated ``ssmarttv_test`` Postgres database and a real
Redis (flushed between tests). The schema is created from the models once; every
test starts from a truncated DB re-seeded with reference data + a superuser.
"""
import os

# Configure the environment BEFORE importing the app/settings singleton.
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://ssmart:ssmart@localhost:5432/ssmarttv_test"
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/15")
os.environ.setdefault("SMS_BACKEND", "console")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import asyncpg
import httpx
import pytest_asyncio
from sqlalchemy import text

import ssmarttv.db.all_models  # noqa: F401  (register all tables)
from ssmarttv.core.config import settings
from ssmarttv.core.security import hash_password
from ssmarttv.db.base import Base
from ssmarttv.db.session import async_session_maker, engine
from ssmarttv.domains.auth.models import ROLE_SUPERUSER, Permission, Role, User
from ssmarttv.domains.auth.permissions import (
    ALL_PERMISSIONS,
    ROLE_NAMES,
    ROLE_PERMISSIONS,
)
from ssmarttv.domains.catalog.models import Country, Genre
from ssmarttv.domains.streaming import service as stream_service
from ssmarttv.main import app
from ssmarttv.redis.client import redis_client
from tests.helpers import latest_otp

SUPERUSER = {"username": "root", "password": "rootpass123"}
TEST_GENRES = [("kino", "Kino"), ("sport", "Sport"), ("komediya", "Komediya")]
TEST_COUNTRY = ("uz", "ozbekiston", "O'zbekiston")


async def _ensure_database() -> None:
    """Create the test database if it does not exist yet."""
    url = settings.DATABASE_URL
    dbname = url.rsplit("/", 1)[1]
    admin_dsn = "postgresql://ssmart:ssmart@localhost:5432/postgres"
    conn = await asyncpg.connect(admin_dsn)
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", dbname)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{dbname}"')
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _schema():
    await _ensure_database()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


async def _seed(session) -> None:
    perms = {p: Permission(slug=p, name=n) for p, n in ALL_PERMISSIONS.items()}
    session.add_all(perms.values())
    await session.flush()
    for order, (slug, pslugs) in enumerate(ROLE_PERMISSIONS.items()):
        session.add(
            Role(
                slug=slug,
                name=ROLE_NAMES[slug],
                sort_order=order,
                permissions=[perms[p] for p in pslugs],
            )
        )
    await session.flush()
    for order, (slug, name) in enumerate(TEST_GENRES):
        session.add(Genre(slug=slug, name_uz=name, sort_order=order))
    session.add(
        Country(code=TEST_COUNTRY[0], slug=TEST_COUNTRY[1], name_uz=TEST_COUNTRY[2])
    )
    su_role = await session.scalar(
        text("SELECT id FROM roles WHERE slug = :s").bindparams(s=ROLE_SUPERUSER)
    )
    session.add(
        User(
            username=SUPERUSER["username"],
            password_hash=hash_password(SUPERUSER["password"]),
            role_id=su_role,
        )
    )


@pytest_asyncio.fixture(autouse=True)
async def clean_state():
    """Truncate all tables, re-seed reference data, flush Redis (per test)."""
    tables = ", ".join(t.name for t in reversed(Base.metadata.sorted_tables))
    async with async_session_maker() as session:
        await session.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
        await _seed(session)
        await session.commit()
    await redis_client.flushdb()
    # The HLS proxy needs an httpx client (lifespan does not run under ASGITransport).
    client = httpx.AsyncClient()
    stream_service.set_client(client)
    yield
    await client.aclose()


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def superuser_client():
    """Logged-in superuser on its own client (separate cookie jar from `client`)."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post("/api/v1/auth/staff/login", json=SUPERUSER)
        yield c


@pytest_asyncio.fixture
async def user_client(client):
    """A logged-in regular (phone/OTP) user on a fresh client."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post("/api/v1/auth/otp/request", json={"phone": "+998901234567"})
        await c.post(
            "/api/v1/auth/otp/verify",
            json={"phone": "+998901234567", "code": latest_otp()},
        )
        yield c
