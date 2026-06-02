"""Single shared async Redis client (sessions, OTP, rate limiting)."""
import redis.asyncio as aioredis

from ssmarttv.core.config import settings

redis_client: aioredis.Redis = aioredis.from_url(
    settings.REDIS_URL, encoding="utf-8", decode_responses=True
)


async def ping() -> bool:
    """Readiness check helper."""
    return bool(await redis_client.ping())
