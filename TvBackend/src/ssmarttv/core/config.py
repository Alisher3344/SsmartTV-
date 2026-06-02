"""Application settings (pydantic-settings) with environment-aware guards."""
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

Environment = Literal["development", "test", "production"]
SmsBackend = Literal["console", "eskiz"]

_INSECURE_SECRET = "change-me"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ENVIRONMENT: Environment = "development"

    # --- Infrastructure ---------------------------------------------------
    DATABASE_URL: str = "postgresql+asyncpg://ssmart:ssmart@localhost:5432/ssmarttv"
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Security / sessions ---------------------------------------------
    SECRET_KEY: str = _INSECURE_SECRET
    SESSION_COOKIE_NAME: str = "ssmart_session"
    SESSION_TTL_SECONDS: int = 60 * 60 * 24 * 60  # 60 days (regular phone/OTP users)
    STAFF_SESSION_TTL_SECONDS: int = 60 * 60 * 24 * 7  # 7 days (password staff/admin)
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"

    # Shared secret for trusted server-to-server calls (e.g. SsmartShop super-admin
    # provisioning TV admin accounts). When set, the /internal/* endpoints accept
    # an X-Internal-Secret header instead of a session cookie.
    INTERNAL_API_SECRET: str | None = None

    # --- OTP --------------------------------------------------------------
    OTP_LENGTH: int = 6
    OTP_TTL_SECONDS: int = 300  # 5 minutes
    OTP_MAX_ATTEMPTS: int = 5
    OTP_RESEND_COOLDOWN_SECONDS: int = 60
    OTP_MAX_PER_HOUR: int = 5

    # --- SMS provider (eskiz.uz) -----------------------------------------
    SMS_BACKEND: SmsBackend = "console"
    ESKIZ_BASE_URL: str = "https://notify.eskiz.uz/api"
    ESKIZ_EMAIL: str | None = None
    ESKIZ_PASSWORD: str | None = None
    ESKIZ_FROM: str = "4546"

    # --- Streaming / SSRF -------------------------------------------------
    # Extra hosts the HLS proxy may fetch from, beyond channels in the DB.
    STREAM_ALLOWED_HOSTS: Annotated[list[str], NoDecode] = Field(default_factory=list)
    # When true, the proxy only fetches hosts in the allowlist (channel hosts +
    # STREAM_ALLOWED_HOSTS). Private/loopback/metadata IPs are always blocked.
    STREAM_ENFORCE_ALLOWLIST: bool = False

    # --- CORS -------------------------------------------------------------
    CORS_ORIGINS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )
    CORS_ORIGIN_REGEX: str | None = r"http://(localhost|127\.0\.0\.1):\d+"

    # --- Observability ----------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = True

    @model_validator(mode="before")
    @classmethod
    def _split_csv(cls, data: dict) -> dict:
        if isinstance(data, dict):
            for key in ("CORS_ORIGINS", "STREAM_ALLOWED_HOSTS"):
                value = data.get(key)
                if isinstance(value, str):
                    data[key] = [v.strip() for v in value.split(",") if v.strip()]
        return data

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @model_validator(mode="after")
    def _production_guards(self) -> "Settings":
        if not self.is_production:
            return self
        errors: list[str] = []
        if self.SECRET_KEY == _INSECURE_SECRET or len(self.SECRET_KEY) < 32:
            errors.append("SECRET_KEY must be a strong, non-default value in production")
        if not self.SESSION_COOKIE_SECURE:
            errors.append("SESSION_COOKIE_SECURE must be true in production")
        if "*" in self.CORS_ORIGINS:
            errors.append("CORS_ORIGINS must not contain '*' in production")
        if self.SMS_BACKEND == "eskiz" and not (self.ESKIZ_EMAIL and self.ESKIZ_PASSWORD):
            errors.append("ESKIZ_EMAIL and ESKIZ_PASSWORD are required for the eskiz backend")
        if self.INTERNAL_API_SECRET is not None and len(self.INTERNAL_API_SECRET) < 32:
            errors.append("INTERNAL_API_SECRET must be at least 32 chars when set")
        if errors:
            raise ValueError("Insecure production configuration: " + "; ".join(errors))
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
