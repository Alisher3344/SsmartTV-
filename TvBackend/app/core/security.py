"""Password hashing (Argon2) and session-id generation."""
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Return an Argon2id hash ($argon2id$...) for the given password."""
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Verify a password against a stored Argon2 hash. Never raises."""
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash: str) -> bool:
    """True if the hash was created with outdated parameters."""
    try:
        return _hasher.check_needs_rehash(password_hash)
    except InvalidHashError:
        return True


def new_session_id() -> str:
    """Cryptographically secure, URL-safe opaque session id."""
    return secrets.token_urlsafe(32)
