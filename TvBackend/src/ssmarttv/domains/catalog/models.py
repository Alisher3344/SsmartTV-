"""Fully-normalized catalog domain.

``Content`` is a joined-table-inheritance base shared by ``Movie`` and
``Series`` so genres, ratings, cast, trailers and translations attach once and
work for both. Series own Seasons → Episodes. Localized text lives in dedicated
translation tables (one row per language).
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ssmarttv.db.base import Base, TimestampMixin

# Access tiers — free content is watchable anonymously; premium needs auth +
# an active subscription (enforced in the streaming/premium gate).
ACCESS_FREE = "free"
ACCESS_PREMIUM = "premium"
ACCESS_LEVELS = (ACCESS_FREE, ACCESS_PREMIUM)

CONTENT_MOVIE = "movie"
CONTENT_SERIES = "series"

COLLECTION_HERO = "hero"
COLLECTION_SHELF = "shelf"

LANGS = ("uz", "ru", "en")


# --- Reference vocabularies ---------------------------------------------
class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True, index=True)  # uz, ru, by
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name_uz: Mapped[str] = mapped_column(String(80))
    name_ru: Mapped[str | None] = mapped_column(String(80))
    name_en: Mapped[str | None] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name_uz: Mapped[str] = mapped_column(String(80))
    name_ru: Mapped[str | None] = mapped_column(String(80))
    name_en: Mapped[str | None] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")


class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    photo: Mapped[str | None] = mapped_column(Text)


content_genres = Table(
    "content_genres",
    Base.metadata,
    Column("content_id", ForeignKey("contents.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


# --- Content (polymorphic base) -----------------------------------------
class Content(Base, TimestampMixin):
    __tablename__ = "contents"
    __table_args__ = (
        CheckConstraint(
            f"access_level IN ('{ACCESS_FREE}', '{ACCESS_PREMIUM}')",
            name="access_level",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20), index=True)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True)
    access_level: Mapped[str] = mapped_column(
        String(10), default=ACCESS_FREE, server_default=ACCESS_FREE, index=True
    )

    country_id: Mapped[int | None] = mapped_column(
        ForeignKey("countries.id", ondelete="SET NULL"), index=True
    )
    year: Mapped[int | None] = mapped_column(Integer, index=True)
    age_rating: Mapped[str | None] = mapped_column(String(10))

    poster: Mapped[str | None] = mapped_column(Text)
    background: Mapped[str | None] = mapped_column(Text)
    image: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(String(20))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    country: Mapped[Country | None] = relationship(lazy="joined")
    genres: Mapped[list[Genre]] = relationship(
        secondary=content_genres, lazy="selectin", order_by=Genre.sort_order
    )
    ratings: Mapped[list[Rating]] = relationship(
        back_populates="content", cascade="all, delete-orphan", lazy="selectin"
    )
    trailers: Mapped[list[Trailer]] = relationship(
        back_populates="content",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Trailer.sort_order",
    )
    cast: Mapped[list[ContentCast]] = relationship(
        back_populates="content",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="ContentCast.sort_order",
    )
    translations: Mapped[list[ContentTranslation]] = relationship(
        back_populates="content", cascade="all, delete-orphan", lazy="selectin"
    )

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "content"}


class Movie(Content):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), primary_key=True
    )
    video_url: Mapped[str | None] = mapped_column(Text)
    duration_sec: Mapped[int | None] = mapped_column(Integer)

    __mapper_args__ = {"polymorphic_identity": CONTENT_MOVIE}


class Series(Content):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), primary_key=True
    )

    seasons: Mapped[list[Season]] = relationship(
        back_populates="series",
        cascade="all, delete-orphan",
        order_by="Season.number",
    )

    __mapper_args__ = {"polymorphic_identity": CONTENT_SERIES}


class Season(Base):
    __tablename__ = "seasons"
    __table_args__ = (UniqueConstraint("series_id", "number", name="series_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    series_id: Mapped[int] = mapped_column(
        ForeignKey("series.id", ondelete="CASCADE"), index=True
    )
    number: Mapped[int] = mapped_column(Integer)

    series: Mapped[Series] = relationship(back_populates="seasons")
    episodes: Mapped[list[Episode]] = relationship(
        back_populates="season",
        cascade="all, delete-orphan",
        order_by="Episode.number",
    )


class Episode(Base):
    __tablename__ = "episodes"
    __table_args__ = (
        CheckConstraint(
            f"access_level IN ('{ACCESS_FREE}', '{ACCESS_PREMIUM}')",
            name="access_level",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"), index=True
    )
    number: Mapped[int] = mapped_column(Integer)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    access_level: Mapped[str] = mapped_column(
        String(10), default=ACCESS_FREE, server_default=ACCESS_FREE
    )
    video_url: Mapped[str | None] = mapped_column(Text)
    duration_sec: Mapped[int | None] = mapped_column(Integer)
    air_date: Mapped[date | None] = mapped_column(Date)

    season: Mapped[Season] = relationship(back_populates="episodes")
    translations: Mapped[list[EpisodeTranslation]] = relationship(
        back_populates="episode", cascade="all, delete-orphan", lazy="selectin"
    )


# --- Attached records ----------------------------------------------------
class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("content_id", "source", name="content_source"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    source: Mapped[str] = mapped_column(String(30))  # imdb, kinopoisk, ntv, ...
    value: Mapped[float] = mapped_column(Float)

    content: Mapped[Content] = relationship(back_populates="ratings")


class Trailer(Base):
    __tablename__ = "trailers"

    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    url: Mapped[str] = mapped_column(Text)
    title: Mapped[str | None] = mapped_column(String(160))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    content: Mapped[Content] = relationship(back_populates="trailers")


class ContentCast(Base):
    __tablename__ = "content_cast"

    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), primary_key=True
    )
    actor_id: Mapped[int] = mapped_column(
        ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True
    )
    character: Mapped[str | None] = mapped_column(String(160))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    content: Mapped[Content] = relationship(back_populates="cast")
    actor: Mapped[Actor] = relationship(lazy="joined")


class ContentTranslation(Base):
    __tablename__ = "content_translations"
    __table_args__ = (UniqueConstraint("content_id", "lang", name="content_lang"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    lang: Mapped[str] = mapped_column(String(2))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)

    content: Mapped[Content] = relationship(back_populates="translations")


class EpisodeTranslation(Base):
    __tablename__ = "episode_translations"
    __table_args__ = (UniqueConstraint("episode_id", "lang", name="episode_lang"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    episode_id: Mapped[int] = mapped_column(
        ForeignKey("episodes.id", ondelete="CASCADE"), index=True
    )
    lang: Mapped[str] = mapped_column(String(2))
    title: Mapped[str] = mapped_column(String(255))

    episode: Mapped[Episode] = relationship(back_populates="translations")


# --- Curation (home page rows) ------------------------------------------
class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    type: Mapped[str] = mapped_column(String(20), default=COLLECTION_SHELF)
    name_uz: Mapped[str] = mapped_column(String(120))
    name_ru: Mapped[str | None] = mapped_column(String(120))
    name_en: Mapped[str | None] = mapped_column(String(120))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    items: Mapped[list[CollectionItem]] = relationship(
        back_populates="collection",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="CollectionItem.sort_order",
    )


class CollectionItem(Base):
    __tablename__ = "collection_items"
    __table_args__ = (
        UniqueConstraint("collection_id", "content_id", name="collection_content"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collections.id", ondelete="CASCADE"), index=True
    )
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    collection: Mapped[Collection] = relationship(back_populates="items")
    content: Mapped[Content] = relationship(lazy="joined")
