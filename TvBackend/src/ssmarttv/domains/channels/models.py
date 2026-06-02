"""Live TV channel model (manually managed: name, logo, stream URL, status)."""
from __future__ import annotations

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ssmarttv.db.base import Base, TimestampMixin
from ssmarttv.domains.catalog.models import ACCESS_FREE, ACCESS_PREMIUM, Country, Genre


class Channel(Base, TimestampMixin):
    __tablename__ = "channels"
    __table_args__ = (
        CheckConstraint(
            f"access_level IN ('{ACCESS_FREE}', '{ACCESS_PREMIUM}')",
            name="access_level",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    logo: Mapped[str | None] = mapped_column(Text)
    image: Mapped[str | None] = mapped_column(Text)
    stream_url: Mapped[str | None] = mapped_column(Text)  # upstream HLS (m3u8)
    # Extra HTTP headers the proxy must send when fetching this channel's
    # upstream (e.g. {"Referer": ..., "User-Agent": ...}). Some CDNs reject
    # requests without them (HTTP 403). Resolved by host in the streaming proxy.
    stream_headers: Mapped[dict[str, str] | None] = mapped_column(
        JSONB(none_as_null=True)
    )

    access_level: Mapped[str] = mapped_column(
        String(10), default=ACCESS_FREE, server_default=ACCESS_FREE, index=True
    )
    country_id: Mapped[int | None] = mapped_column(
        ForeignKey("countries.id", ondelete="SET NULL"), index=True
    )
    genre_id: Mapped[int | None] = mapped_column(
        ForeignKey("genres.id", ondelete="SET NULL"), index=True
    )

    current_show: Mapped[str | None] = mapped_column(String(255))
    time: Mapped[str | None] = mapped_column(String(50))
    is_live: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    country: Mapped[Country | None] = relationship(lazy="joined")
    genre: Mapped[Genre | None] = relationship(lazy="joined")
