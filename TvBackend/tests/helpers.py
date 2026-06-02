"""Shared test helpers."""
import re

from ssmarttv.core.sms import get_sms_sender


def latest_otp() -> str:
    """The 6-digit code from the most recent console SMS."""
    sender = get_sms_sender()
    return re.search(r"(\d{6})", sender.outbox[-1][1]).group(1)  # type: ignore[union-attr]
