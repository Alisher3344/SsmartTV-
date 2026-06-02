"""SMS delivery abstraction with a console (dev) and eskiz.uz (prod) backend."""
import logging
from functools import lru_cache
from typing import Protocol

from ssmarttv.core.config import settings

logger = logging.getLogger("ssmarttv.sms")


class SmsSender(Protocol):
    async def send(self, phone: str, message: str) -> None: ...


class ConsoleSmsSender:
    """Logs messages instead of sending; keeps an in-memory outbox for dev/tests."""

    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    async def send(self, phone: str, message: str) -> None:
        self.outbox.append((phone, message))
        logger.info("SMS (console) to %s: %s", phone, message)


@lru_cache
def get_sms_sender() -> SmsSender:
    if settings.SMS_BACKEND == "eskiz":
        from ssmarttv.core.sms.eskiz import EskizSmsSender

        return EskizSmsSender()
    return ConsoleSmsSender()
