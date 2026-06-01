from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://ssmart:ssmart@localhost:5432/ssmarttv"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security / sessions
    SECRET_KEY: str = "change-me"
    SESSION_COOKIE_NAME: str = "ssmart_session"
    SESSION_TTL_SECONDS: int = 60 * 60 * 24 * 14  # 14 days
    SESSION_COOKIE_SECURE: bool = False

    # CORS (comma-separated string in env; parsed to a list below)
    CORS_ORIGINS: Annotated[list[str], NoDecode] = ["http://localhost:5173"]
    # Optional regex to allow any matching origin (handy in dev when Vite
    # picks a different port, e.g. 5174). Takes precedence over the list.
    CORS_ORIGIN_REGEX: str | None = r"http://(localhost|127\.0\.0\.1):\d+"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
