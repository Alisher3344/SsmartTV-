from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    logo: Mapped[str | None] = mapped_column(Text, nullable=True)  # data-URI / path / URL
    current_show: Mapped[str | None] = mapped_column(String(255), nullable=True)
    time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Primary grouping = country (e.g. "ozbekiston", "rossiya", "belarus").
    category: Mapped[str] = mapped_column(String(50), index=True, default="barcasi")
    # Secondary grouping = genre (e.g. "yangiliklar", "sport", "kino"); optional.
    subcategory: Mapped[str | None] = mapped_column(
        String(50), index=True, nullable=True
    )
    # Upstream CDN m3u8 URL; clients receive a computed /api/stream/{slug} proxy URL.
    video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
