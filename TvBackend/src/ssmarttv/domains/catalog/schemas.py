"""Catalog request/response schemas."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ssmarttv.domains.catalog import models as m

Lang = Literal["uz", "ru", "en"]
AccessLevel = Literal["free", "premium"]


# --- Reference -----------------------------------------------------------
class GenreIn(BaseModel):
    slug: str | None = None
    name_uz: str
    name_ru: str | None = None
    name_en: str | None = None
    sort_order: int = 0


class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slug: str
    name_uz: str
    name_ru: str | None = None
    name_en: str | None = None
    sort_order: int


class CountryIn(BaseModel):
    code: str
    slug: str | None = None
    name_uz: str
    name_ru: str | None = None
    name_en: str | None = None
    sort_order: int = 0


class CountryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    slug: str
    name_uz: str
    name_ru: str | None = None
    name_en: str | None = None
    sort_order: int


class ActorIn(BaseModel):
    slug: str | None = None
    name: str
    photo: str | None = None


class ActorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slug: str
    name: str
    photo: str | None = None


# --- Nested value objects ------------------------------------------------
class TranslationIn(BaseModel):
    lang: Lang
    title: str
    description: str | None = None


class TranslationOut(BaseModel):
    lang: str
    title: str
    description: str | None = None


class RatingIn(BaseModel):
    source: str
    value: float


class RatingOut(BaseModel):
    source: str
    value: float


class CastIn(BaseModel):
    actor_id: int
    character: str | None = None
    sort_order: int = 0


class CastMemberOut(BaseModel):
    actor: ActorOut
    character: str | None = None
    sort_order: int


class TrailerIn(BaseModel):
    url: str
    title: str | None = None
    sort_order: int = 0


class TrailerOut(BaseModel):
    id: int
    url: str
    title: str | None = None
    sort_order: int


# --- Content (movie / series) -------------------------------------------
class _ContentBaseIn(BaseModel):
    slug: str | None = None
    access_level: AccessLevel = "free"
    country_id: int | None = None
    year: int | None = None
    age_rating: str | None = None
    poster: str | None = None
    background: str | None = None
    image: str | None = None
    color: str | None = None
    sort_order: int = 0
    translations: list[TranslationIn] = Field(min_length=1)
    genre_ids: list[int] = Field(default_factory=list)
    ratings: list[RatingIn] = Field(default_factory=list)
    cast: list[CastIn] = Field(default_factory=list)
    trailers: list[TrailerIn] = Field(default_factory=list)


class MovieCreateIn(_ContentBaseIn):
    video_url: str | None = None
    duration_sec: int | None = None


class MovieUpdateIn(MovieCreateIn):
    translations: list[TranslationIn] | None = None  # type: ignore[assignment]


class SeriesCreateIn(_ContentBaseIn):
    pass


class SeriesUpdateIn(SeriesCreateIn):
    translations: list[TranslationIn] | None = None  # type: ignore[assignment]


class _ContentOut(BaseModel):
    id: int
    type: str
    slug: str
    access_level: str
    country: CountryOut | None = None
    year: int | None = None
    age_rating: str | None = None
    poster: str | None = None
    background: str | None = None
    image: str | None = None
    color: str | None = None
    sort_order: int
    genres: list[GenreOut]
    ratings: list[RatingOut]
    cast: list[CastMemberOut]
    trailers: list[TrailerOut]
    translations: list[TranslationOut]
    created_at: datetime

    @staticmethod
    def _common(c: m.Content) -> dict:
        return {
            "id": c.id,
            "type": c.type,
            "slug": c.slug,
            "access_level": c.access_level,
            "country": CountryOut.model_validate(c.country) if c.country else None,
            "year": c.year,
            "age_rating": c.age_rating,
            "poster": c.poster,
            "background": c.background,
            "image": c.image,
            "color": c.color,
            "sort_order": c.sort_order,
            "genres": [GenreOut.model_validate(g) for g in c.genres],
            "ratings": [RatingOut(source=r.source, value=r.value) for r in c.ratings],
            "cast": [
                CastMemberOut(
                    actor=ActorOut.model_validate(cc.actor),
                    character=cc.character,
                    sort_order=cc.sort_order,
                )
                for cc in c.cast
            ],
            "trailers": [
                TrailerOut(id=t.id, url=t.url, title=t.title, sort_order=t.sort_order)
                for t in c.trailers
            ],
            "translations": [
                TranslationOut(lang=t.lang, title=t.title, description=t.description)
                for t in c.translations
            ],
            "created_at": c.created_at,
        }


def _reveal(access_level: str, video_url: str | None, can_watch: bool) -> str | None:
    """Hide premium playback URLs from users who cannot watch them."""
    if access_level == m.ACCESS_PREMIUM and not can_watch:
        return None
    return video_url


class MovieOut(_ContentOut):
    video_url: str | None = None
    duration_sec: int | None = None
    # True when the requester may actually play this (free, or premium + entitled).
    playable: bool = True

    @classmethod
    def of(cls, movie: m.Movie, *, can_watch: bool = True) -> "MovieOut":
        playable = movie.access_level != m.ACCESS_PREMIUM or can_watch
        return cls(
            **cls._common(movie),
            video_url=_reveal(movie.access_level, movie.video_url, can_watch),
            duration_sec=movie.duration_sec,
            playable=playable,
        )


class EpisodeOut(BaseModel):
    id: int
    number: int
    slug: str
    access_level: str
    video_url: str | None = None
    duration_sec: int | None = None
    air_date: date | None = None
    playable: bool = True
    translations: list[TranslationOut]

    @classmethod
    def of(cls, ep: m.Episode, *, can_watch: bool = True) -> "EpisodeOut":
        playable = ep.access_level != m.ACCESS_PREMIUM or can_watch
        return cls(
            id=ep.id,
            number=ep.number,
            slug=ep.slug,
            access_level=ep.access_level,
            video_url=_reveal(ep.access_level, ep.video_url, can_watch),
            duration_sec=ep.duration_sec,
            air_date=ep.air_date,
            playable=playable,
            translations=[
                TranslationOut(lang=t.lang, title=t.title) for t in ep.translations
            ],
        )


class SeasonOut(BaseModel):
    id: int
    number: int
    episodes: list[EpisodeOut]

    @classmethod
    def of(cls, season: m.Season, *, can_watch: bool = True) -> "SeasonOut":
        return cls(
            id=season.id,
            number=season.number,
            episodes=[EpisodeOut.of(e, can_watch=can_watch) for e in season.episodes],
        )


class SeriesOut(_ContentOut):
    @classmethod
    def of(cls, series: m.Series) -> "SeriesOut":
        return cls(**cls._common(series))


class SeriesDetailOut(SeriesOut):
    seasons: list[SeasonOut] = Field(default_factory=list)

    @classmethod
    def of(cls, series: m.Series, *, can_watch: bool = True) -> "SeriesDetailOut":
        return cls(
            **cls._common(series),
            seasons=[SeasonOut.of(s, can_watch=can_watch) for s in series.seasons],
        )


# --- Seasons / episodes input -------------------------------------------
class SeasonIn(BaseModel):
    number: int


class EpisodeIn(BaseModel):
    number: int
    slug: str | None = None
    access_level: AccessLevel = "free"
    video_url: str | None = None
    duration_sec: int | None = None
    air_date: date | None = None
    translations: list[TranslationIn] = Field(min_length=1)


# --- Collections ---------------------------------------------------------
class CollectionIn(BaseModel):
    slug: str | None = None
    type: Literal["hero", "shelf"] = "shelf"
    name_uz: str
    name_ru: str | None = None
    name_en: str | None = None
    sort_order: int = 0


class CollectionItemIn(BaseModel):
    content_id: int
    sort_order: int = 0


class CollectionItemOut(BaseModel):
    id: int
    content_id: int
    sort_order: int
    slug: str
    type: str

    @classmethod
    def of(cls, item: m.CollectionItem) -> "CollectionItemOut":
        return cls(
            id=item.id,
            content_id=item.content_id,
            sort_order=item.sort_order,
            slug=item.content.slug,
            type=item.content.type,
        )


class CollectionOut(BaseModel):
    id: int
    slug: str
    type: str
    name_uz: str
    name_ru: str | None = None
    name_en: str | None = None
    sort_order: int
    items: list[CollectionItemOut]

    @classmethod
    def of(cls, col: m.Collection) -> "CollectionOut":
        return cls(
            id=col.id,
            slug=col.slug,
            type=col.type,
            name_uz=col.name_uz,
            name_ru=col.name_ru,
            name_en=col.name_en,
            sort_order=col.sort_order,
            items=[CollectionItemOut.of(i) for i in col.items],
        )
