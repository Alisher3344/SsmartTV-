"""Channel request/response schemas."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from ssmarttv.domains.catalog.schemas import CountryOut, GenreOut

AccessLevel = Literal["free", "premium"]


class ChannelIn(BaseModel):
    slug: str | None = None
    name: str
    logo: str | None = None
    image: str | None = None
    stream_url: str | None = None
    stream_headers: dict[str, str] | None = None
    access_level: AccessLevel = "free"
    country_id: int | None = None
    genre_id: int | None = None
    current_show: str | None = None
    time: str | None = None
    is_live: bool = False
    sort_order: int = 0


class ChannelUpdate(BaseModel):
    name: str | None = None
    logo: str | None = None
    image: str | None = None
    stream_url: str | None = None
    stream_headers: dict[str, str] | None = None
    access_level: AccessLevel | None = None
    country_id: int | None = None
    genre_id: int | None = None
    current_show: str | None = None
    time: str | None = None
    is_live: bool | None = None
    sort_order: int | None = None


class ChannelOut(BaseModel):
    id: int
    slug: str
    name: str
    logo: str | None = None
    image: str | None = None
    access_level: str
    is_live: bool
    current_show: str | None = None
    time: str | None = None
    country: CountryOut | None = None
    genre: GenreOut | None = None
    sort_order: int
    # Proxy playback URL clients should load (null for non-live channels).
    playback_url: str | None = None
    # Raw upstream URL — only populated for privileged (channel:write) requests.
    stream_url: str | None = None
    # Upstream request headers — privileged only (internal config).
    stream_headers: dict[str, str] | None = None
    created_at: datetime
