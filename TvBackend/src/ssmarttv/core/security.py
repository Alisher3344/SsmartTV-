"""Password hashing (Argon2, staff accounts) and opaque token generation.

Regular users authenticate via phone + OTP and have no password; only
staff/admin/superuser accounts carry an Argon2 ``password_hash``.
"""
import hashlib
import hmac
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from ssmarttv.core.config import settings

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Return an Argon2id hash for a staff password."""
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Verify a password against a stored Argon2 hash. Never raises."""
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash: str) -> bool:
    """True if the hash uses outdated Argon2 parameters."""
    try:
        return _hasher.check_needs_rehash(password_hash)
    except InvalidHashError:
        return True


def new_token(nbytes: int = 32) -> str:
    """Cryptographically secure, URL-safe opaque token (session ids, etc.)."""
    return secrets.token_urlsafe(nbytes)


def hash_otp(code: str, phone: str) -> str:
    """Keyed HMAC of an OTP code so plaintext codes never touch Redis."""
    msg = f"{phone}:{code}".encode()
    return hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()


def verify_otp(code: str, phone: str, stored_hash: str) -> bool:
    return hmac.compare_digest(hash_otp(code, phone), stored_hash)
