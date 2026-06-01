"""Redis-backed session store.

Sessions are opaque ids (see core.security.new_session_id) mapped to a small
JSON payload with the user id. Keys expire after SESSION_TTL_SECONDS.
"""
import json

import redis.asyncio as aioredis

from app.core.config import settings

_SESSION_PREFIX = "session:"

# Single shared connection pool for the app lifetime.
redis_client: aioredis.Redis = aioredis.from_url(
    settings.REDIS_URL, encoding="utf-8", decode_responses=True
)


def _key(session_id: str) -> str:
    return f"{_SESSION_PREFIX}{session_id}"


async def create_session(session_id: str, user_id: int, **meta) -> None:
    payload = {"user_id": user_id, **meta}
    await redis_client.set(
        _key(session_id), json.dumps(payload), ex=settings.SESSION_TTL_SECONDS
    )


async def get_session(session_id: str) -> dict | None:
    raw = await redis_client.get(_key(session_id))
    if raw is None:
        return None
    return json.loads(raw)


async def delete_session(session_id: str) -> None:
    await redis_client.delete(_key(session_id))
