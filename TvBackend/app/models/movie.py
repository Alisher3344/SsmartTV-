from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    # hero | featured | premiere | cinema | movie | series
    kind: Mapped[str] = mapped_column(String(30), index=True, default="movie")

    title_uz: Mapped[str] = mapped_column(String(255))
    title_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    description_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    genre_uz: Mapped[str | None] = mapped_column(String(120), nullable=True)
    genre_ru: Mapped[str | None] = mapped_column(String(120), nullable=True)

    age: Mapped[str | None] = mapped_column(String(10), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    image: Mapped[str | None] = mapped_column(Text, nullable=True)
    poster: Mapped[str | None] = mapped_column(Text, nullable=True)
    background: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    video_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    rating_imdb: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating_kinopoisk: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating_ntv: Mapped[float | None] = mapped_column(Float, nullable=True)

    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
