"""Phone OTP: generation, delivery and verification (Redis-backed)."""
import json
import secrets

from ssmarttv.core.config import settings
from ssmarttv.core.exceptions import AppError
from ssmarttv.core.ratelimit import RateLimit, hit
from ssmarttv.core.security import hash_otp, verify_otp
from ssmarttv.core.sms import get_sms_sender
from ssmarttv.redis.client import redis_client


def _key(phone: str) -> str:
    return f"otp:code:{phone}"


def _cooldown_key(phone: str) -> str:
    return f"otp:cooldown:{phone}"


def _generate_code() -> str:
    upper = 10**settings.OTP_LENGTH
    return str(secrets.randbelow(upper)).zfill(settings.OTP_LENGTH)


async def request_code(phone: str) -> None:
    """Issue and send an OTP, enforcing resend cooldown and hourly cap."""
    if await redis_client.exists(_cooldown_key(phone)):
        ttl = await redis_client.ttl(_cooldown_key(phone))
        raise AppError(
            f"Please wait {max(ttl, 1)}s before requesting another code",
            code="otp_cooldown",
            details={"retry_after": max(ttl, 1)},
        )
    await hit("otp_request", phone, RateLimit(settings.OTP_MAX_PER_HOUR, 3600))

    code = _generate_code()
    payload = {"hash": hash_otp(code, phone), "attempts": 0}
    await redis_client.set(_key(phone), json.dumps(payload), ex=settings.OTP_TTL_SECONDS)
    await redis_client.set(_cooldown_key(phone), "1", ex=settings.OTP_RESEND_COOLDOWN_SECONDS)

    await get_sms_sender().send(phone, f"SsmartTv kirish kodi: {code}")


async def verify_code(phone: str, code: str) -> None:
    """Validate an OTP. Raises :class:`AppError` on any failure."""
    raw = await redis_client.get(_key(phone))
    if raw is None:
        raise AppError("Code expired or not requested", code="otp_expired")
    data = json.loads(raw)

    if data["attempts"] >= settings.OTP_MAX_ATTEMPTS:
        await redis_client.delete(_key(phone))
        raise AppError("Too many attempts, request a new code", code="otp_attempts")

    if not verify_otp(code, phone, data["hash"]):
        data["attempts"] += 1
        ttl = await redis_client.ttl(_key(phone))
        await redis_client.set(_key(phone), json.dumps(data), ex=max(ttl, 1))
        raise AppError("Invalid code", code="otp_invalid")

    await redis_client.delete(_key(phone))
    await redis_client.delete(_cooldown_key(phone))
