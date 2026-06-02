"""eskiz.uz SMS backend.

Auth token is obtained from ``/auth/login`` (email + password) and cached in
Redis (~25 days; eskiz tokens last ~30). On a 401 the token is refreshed once.

Note: eskiz requires SMS text to match a pre-approved template for production
sending — coordinate the OTP message wording with the eskiz dashboard.
"""
import logging
import re

import httpx

from ssmarttv.core.config import settings
from ssmarttv.redis.client import redis_client

logger = logging.getLogger("ssmarttv.sms.eskiz")

_TOKEN_KEY = "eskiz:token"
_TOKEN_TTL = 60 * 60 * 24 * 25


class EskizSmsSender:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=settings.ESKIZ_BASE_URL, timeout=20.0)

    async def _login(self) -> str:
        resp = await self._client.post(
            "/auth/login",
            data={"email": settings.ESKIZ_EMAIL, "password": settings.ESKIZ_PASSWORD},
        )
        resp.raise_for_status()
        token = resp.json()["data"]["token"]
        await redis_client.set(_TOKEN_KEY, token, ex=_TOKEN_TTL)
        return token

    async def _token(self) -> str:
        cached = await redis_client.get(_TOKEN_KEY)
        return cached if cached else await self._login()

    async def send(self, phone: str, message: str) -> None:
        mobile = re.sub(r"\D", "", phone)
        token = await self._token()
        payload = {"mobile_phone": mobile, "message": message, "from": settings.ESKIZ_FROM}
        resp = await self._client.post(
            "/message/sms/send",
            data=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code == httpx.codes.UNAUTHORIZED:
            token = await self._login()
            resp = await self._client.post(
                "/message/sms/send",
                data=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
        resp.raise_for_status()
        logger.info("SMS (eskiz) sent to %s", phone)
