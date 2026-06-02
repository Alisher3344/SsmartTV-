"""Phone number normalization to E.164 (default region: Uzbekistan)."""
import phonenumbers

from ssmarttv.core.exceptions import AppError

_DEFAULT_REGION = "UZ"


def normalize_phone(raw: str) -> str:
    """Parse and validate a phone number, returning E.164 (e.g. +998901234567).

    Raises :class:`AppError` (400) for malformed/invalid numbers.
    """
    try:
        parsed = phonenumbers.parse(raw, _DEFAULT_REGION)
    except phonenumbers.NumberParseException as exc:
        raise AppError("Invalid phone number", code="invalid_phone") from exc
    if not phonenumbers.is_valid_number(parsed):
        raise AppError("Invalid phone number", code="invalid_phone")
    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
