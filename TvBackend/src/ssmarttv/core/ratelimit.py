"""Redis fixed-window rate limiter (OTP requests, staff login, segment proxy)."""
from dataclasses import dataclass

from ssmarttv.core.exceptions import RateLimitError
from ssmarttv.redis.client import redis_client

_PREFIX = "ratelimit:"


@dataclass(frozen=True)
class RateLimit:
    limit: int
    window_seconds: int


async def hit(scope: str, identifier: str, rule: RateLimit) -> int:
    """Register one hit; return the remaining allowance.

    Uses INCR + EXPIRE on a window-bucketed key. Raises :class:`RateLimitError`
    when the limit is exceeded.
    """
    key = f"{_PREFIX}{scope}:{identifier}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, rule.window_seconds)
    if count > rule.limit:
        ttl = await redis_client.ttl(key)
        raise RateLimitError(
            f"Rate limit exceeded, retry in {max(ttl, 1)}s",
            details={"retry_after": max(ttl, 1)},
        )
    return rule.limit - count


async def reset(scope: str, identifier: str) -> None:
    await redis_client.delete(f"{_PREFIX}{scope}:{identifier}")
