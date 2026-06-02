"""Catalog business logic: CRUD + filtered listing for movies/series/taxonomy."""
from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ssmarttv.core.exceptions import ConflictError, NotFoundError
from ssmarttv.core.pagination import PageParams
from ssmarttv.core.text import slugify
from ssmarttv.domains.catalog import models as m
from ssmarttv.domains.catalog import schemas as s


# --- shared helpers ------------------------------------------------------
def _primary_title(translations: Sequence[s.TranslationIn]) -> str:
    for t in translations:
        if t.lang == "uz":
            return t.title
    return translations[0].title


async def _unique_slug(
    db: AsyncSession, model: type[Any], slug: str, *, exclude_id: int | None = None
) -> None:
    stmt = select(model.id).where(model.slug == slug)
    if exclude_id is not None:
        stmt = stmt.where(model.id != exclude_id)
    if await db.scalar(stmt):
        raise ConflictError(f"Slug '{slug}' already exists")


async def _load_genres(db: AsyncSession, ids: list[int]) -> list[m.Genre]:
    if not ids:
        return []
    genres = (await db.scalars(select(m.Genre).where(m.Genre.id.in_(ids)))).all()
    if len(genres) != len(set(ids)):
        raise NotFoundError("One or more genres not found")
    return list(genres)


def _apply_translations(content: m.Content, translations: list[s.TranslationIn]) -> None:
    content.translations = [
        m.ContentTranslation(lang=t.lang, title=t.title, description=t.description)
        for t in translations
    ]


def _apply_ratings(content: m.Content, ratings: list[s.RatingIn]) -> None:
    content.ratings = [m.Rating(source=r.source, value=r.value) for r in ratings]


def _apply_cast(content: m.Content, cast: list[s.CastIn]) -> None:
    content.cast = [
        m.ContentCast(actor_id=c.actor_id, character=c.character, sort_order=c.sort_order)
        for c in cast
    ]


def _apply_trailers(content: m.Content, trailers: list[s.TrailerIn]) -> None:
    content.trailers = [
        m.Trailer(url=t.url, title=t.title, sort_order=t.sort_order) for t in trailers
    ]


def _apply_scalars(content: m.Content, fields: dict) -> None:
    for key in (
        "access_level", "country_id", "year", "age_rating",
        "poster", "background", "image", "color", "sort_order",
    ):
        if key in fields:
            setattr(content, key, fields[key])


# --- generic content filters --------------------------------------------
def _apply_filters(
    stmt: Select,
    model: type[m.Content],
    *,
    q: str | None,
    genre: str | None,
    country_id: int | None,
    year: int | None,
    access_level: str | None,
) -> Select:
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            model.id.in_(
                select(m.ContentTranslation.content_id).where(
                    m.ContentTranslation.title.ilike(like)
                )
            )
        )
    if genre:
        stmt = stmt.where(model.genres.any(m.Genre.slug == genre))
    if country_id is not None:
        stmt = stmt.where(model.country_id == country_id)
    if year is not None:
        stmt = stmt.where(model.year == year)
    if access_level:
        stmt = stmt.where(model.access_level == access_level)
    return stmt


# --- MOVIES --------------------------------------------------------------
async def list_movies(
    db: AsyncSession,
    params: PageParams,
    *,
    q: str | None = None,
    genre: str | None = None,
    country_id: int | None = None,
    year: int | None = None,
    access_level: str | None = None,
) -> tuple[list[m.Movie], int]:
    base = _apply_filters(
        select(m.Movie), m.Movie,
        q=q, genre=genre, country_id=country_id, year=year, access_level=access_level,
    )
    total = await db.scalar(select(func.count()).select_from(base.subquery())) or 0
    stmt = base.order_by(m.Movie.sort_order, m.Movie.id).limit(params.limit).offset(params.offset)
    movies = (await db.scalars(stmt)).all()
    return list(movies), total


async def get_movie(db: AsyncSession, slug: str) -> m.Movie:
    movie = await db.scalar(select(m.Movie).where(m.Movie.slug == slug))
    if movie is None:
        raise NotFoundError("Movie not found")
    return movie


async def create_movie(db: AsyncSession, data: s.MovieCreateIn) -> m.Movie:
    slug = data.slug or slugify(_primary_title(data.translations))
    await _unique_slug(db, m.Content, slug)
    movie = m.Movie(
        slug=slug,
        access_level=data.access_level,
        country_id=data.country_id,
        year=data.year,
        age_rating=data.age_rating,
        poster=data.poster,
        background=data.background,
        image=data.image,
        color=data.color,
        sort_order=data.sort_order,
        video_url=data.video_url,
        duration_sec=data.duration_sec,
    )
    _apply_translations(movie, data.translations)
    _apply_ratings(movie, data.ratings)
    _apply_cast(movie, data.cast)
    _apply_trailers(movie, data.trailers)
    movie.genres = await _load_genres(db, data.genre_ids)
    db.add(movie)
    await db.commit()
    return await get_movie(db, slug)


async def update_movie(db: AsyncSession, slug: str, data: s.MovieUpdateIn) -> m.Movie:
    movie = await get_movie(db, slug)
    fields = data.model_dump(exclude_unset=True)
    if fields.get("slug"):
        await _unique_slug(db, m.Content, fields["slug"], exclude_id=movie.id)
        movie.slug = fields["slug"]
    _apply_scalars(movie, fields)
    if "video_url" in fields:
        movie.video_url = fields["video_url"]
    if "duration_sec" in fields:
        movie.duration_sec = fields["duration_sec"]
    if data.translations is not None:
        _apply_translations(movie, data.translations)
    if "ratings" in fields:
        _apply_ratings(movie, data.ratings)
    if "cast" in fields:
        _apply_cast(movie, data.cast)
    if "trailers" in fields:
        _apply_trailers(movie, data.trailers)
    if "genre_ids" in fields:
        movie.genres = await _load_genres(db, data.genre_ids)
    await db.commit()
    return await get_movie(db, movie.slug)


async def delete_movie(db: AsyncSession, slug: str) -> None:
    movie = await get_movie(db, slug)
    await db.delete(movie)
    await db.commit()


# --- SERIES --------------------------------------------------------------
_SERIES_DETAIL = (
    selectinload(m.Series.seasons)
    .selectinload(m.Season.episodes)
    .selectinload(m.Episode.translations),
)


async def list_series(
    db: AsyncSession,
    params: PageParams,
    *,
    q: str | None = None,
    genre: str | None = None,
    country_id: int | None = None,
    year: int | None = None,
    access_level: str | None = None,
) -> tuple[list[m.Series], int]:
    base = _apply_filters(
        select(m.Series), m.Series,
        q=q, genre=genre, country_id=country_id, year=year, access_level=access_level,
    )
    total = await db.scalar(select(func.count()).select_from(base.subquery())) or 0
    stmt = base.order_by(m.Series.sort_order, m.Series.id).limit(params.limit).offset(params.offset)
    return list((await db.scalars(stmt)).all()), total


async def get_series(db: AsyncSession, slug: str, *, with_seasons: bool = False) -> m.Series:
    stmt = select(m.Series).where(m.Series.slug == slug)
    if with_seasons:
        stmt = stmt.options(*_SERIES_DETAIL)
    series = await db.scalar(stmt)
    if series is None:
        raise NotFoundError("Series not found")
    return series


async def create_series(db: AsyncSession, data: s.SeriesCreateIn) -> m.Series:
    slug = data.slug or slugify(_primary_title(data.translations))
    await _unique_slug(db, m.Content, slug)
    series = m.Series(
        slug=slug,
        access_level=data.access_level,
        country_id=data.country_id,
        year=data.year,
        age_rating=data.age_rating,
        poster=data.poster,
        background=data.background,
        image=data.image,
        color=data.color,
        sort_order=data.sort_order,
    )
    _apply_translations(series, data.translations)
    _apply_ratings(series, data.ratings)
    _apply_cast(series, data.cast)
    _apply_trailers(series, data.trailers)
    series.genres = await _load_genres(db, data.genre_ids)
    db.add(series)
    await db.commit()
    return await get_series(db, slug, with_seasons=True)


async def update_series(db: AsyncSession, slug: str, data: s.SeriesUpdateIn) -> m.Series:
    series = await get_series(db, slug)
    fields = data.model_dump(exclude_unset=True)
    if fields.get("slug"):
        await _unique_slug(db, m.Content, fields["slug"], exclude_id=series.id)
        series.slug = fields["slug"]
    _apply_scalars(series, fields)
    if data.translations is not None:
        _apply_translations(series, data.translations)
    if "ratings" in fields:
        _apply_ratings(series, data.ratings)
    if "cast" in fields:
        _apply_cast(series, data.cast)
    if "trailers" in fields:
        _apply_trailers(series, data.trailers)
    if "genre_ids" in fields:
        series.genres = await _load_genres(db, data.genre_ids)
    await db.commit()
    return await get_series(db, series.slug, with_seasons=True)


async def delete_series(db: AsyncSession, slug: str) -> None:
    series = await get_series(db, slug)
    await db.delete(series)
    await db.commit()


# --- SEASONS / EPISODES --------------------------------------------------
async def add_season(db: AsyncSession, series_slug: str, data: s.SeasonIn) -> m.Series:
    series = await get_series(db, series_slug)
    exists = await db.scalar(
        select(m.Season.id).where(
            m.Season.series_id == series.id, m.Season.number == data.number
        )
    )
    if exists:
        raise ConflictError(f"Season {data.number} already exists")
    db.add(m.Season(series_id=series.id, number=data.number))
    await db.commit()
    return await get_series(db, series_slug, with_seasons=True)


async def delete_season(db: AsyncSession, season_id: int) -> None:
    season = await db.get(m.Season, season_id)
    if season is None:
        raise NotFoundError("Season not found")
    await db.delete(season)
    await db.commit()


async def add_episode(db: AsyncSession, season_id: int, data: s.EpisodeIn) -> m.Episode:
    season = await db.get(m.Season, season_id)
    if season is None:
        raise NotFoundError("Season not found")
    slug = data.slug or slugify(_primary_title(data.translations))
    await _unique_slug(db, m.Episode, slug)
    episode = m.Episode(
        season_id=season_id,
        number=data.number,
        slug=slug,
        access_level=data.access_level,
        video_url=data.video_url,
        duration_sec=data.duration_sec,
        air_date=data.air_date,
        translations=[
            m.EpisodeTranslation(lang=t.lang, title=t.title) for t in data.translations
        ],
    )
    db.add(episode)
    await db.commit()
    await db.refresh(episode, ["translations"])
    return episode


async def delete_episode(db: AsyncSession, episode_id: int) -> None:
    episode = await db.get(m.Episode, episode_id)
    if episode is None:
        raise NotFoundError("Episode not found")
    await db.delete(episode)
    await db.commit()


# --- TAXONOMY (genres / countries / actors) ------------------------------
async def list_genres(db: AsyncSession) -> list[m.Genre]:
    return list((await db.scalars(select(m.Genre).order_by(m.Genre.sort_order, m.Genre.id))).all())


async def create_genre(db: AsyncSession, data: s.GenreIn) -> m.Genre:
    slug = data.slug or slugify(data.name_uz)
    await _unique_slug(db, m.Genre, slug)
    genre = m.Genre(
        slug=slug, name_uz=data.name_uz, name_ru=data.name_ru,
        name_en=data.name_en, sort_order=data.sort_order,
    )
    db.add(genre)
    await db.commit()
    await db.refresh(genre)
    return genre


async def delete_genre(db: AsyncSession, genre_id: int) -> None:
    genre = await db.get(m.Genre, genre_id)
    if genre is None:
        raise NotFoundError("Genre not found")
    await db.delete(genre)
    await db.commit()


async def list_countries(db: AsyncSession) -> list[m.Country]:
    return list(
        (await db.scalars(select(m.Country).order_by(m.Country.sort_order, m.Country.id))).all()
    )


async def create_country(db: AsyncSession, data: s.CountryIn) -> m.Country:
    slug = data.slug or slugify(data.name_uz)
    await _unique_slug(db, m.Country, slug)
    if await db.scalar(select(m.Country.id).where(m.Country.code == data.code)):
        raise ConflictError(f"Country code '{data.code}' already exists")
    country = m.Country(
        code=data.code, slug=slug, name_uz=data.name_uz,
        name_ru=data.name_ru, name_en=data.name_en, sort_order=data.sort_order,
    )
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country


async def delete_country(db: AsyncSession, country_id: int) -> None:
    country = await db.get(m.Country, country_id)
    if country is None:
        raise NotFoundError("Country not found")
    await db.delete(country)
    await db.commit()


async def list_actors(db: AsyncSession, q: str | None = None) -> list[m.Actor]:
    stmt = select(m.Actor).order_by(m.Actor.name)
    if q:
        stmt = stmt.where(m.Actor.name.ilike(f"%{q}%"))
    return list((await db.scalars(stmt)).all())


async def create_actor(db: AsyncSession, data: s.ActorIn) -> m.Actor:
    slug = data.slug or slugify(data.name)
    await _unique_slug(db, m.Actor, slug)
    actor = m.Actor(slug=slug, name=data.name, photo=data.photo)
    db.add(actor)
    await db.commit()
    await db.refresh(actor)
    return actor


async def delete_actor(db: AsyncSession, actor_id: int) -> None:
    actor = await db.get(m.Actor, actor_id)
    if actor is None:
        raise NotFoundError("Actor not found")
    await db.delete(actor)
    await db.commit()


# --- COLLECTIONS ---------------------------------------------------------
async def list_collections(db: AsyncSession) -> list[m.Collection]:
    return list(
        (await db.scalars(
            select(m.Collection).order_by(m.Collection.sort_order, m.Collection.id)
        )).all()
    )


async def get_collection(db: AsyncSession, slug: str) -> m.Collection:
    col = await db.scalar(select(m.Collection).where(m.Collection.slug == slug))
    if col is None:
        raise NotFoundError("Collection not found")
    return col


async def create_collection(db: AsyncSession, data: s.CollectionIn) -> m.Collection:
    slug = data.slug or slugify(data.name_uz)
    await _unique_slug(db, m.Collection, slug)
    col = m.Collection(
        slug=slug, type=data.type, name_uz=data.name_uz,
        name_ru=data.name_ru, name_en=data.name_en, sort_order=data.sort_order,
    )
    db.add(col)
    await db.commit()
    return await get_collection(db, slug)


async def delete_collection(db: AsyncSession, slug: str) -> None:
    col = await get_collection(db, slug)
    await db.delete(col)
    await db.commit()


async def set_collection_items(
    db: AsyncSession, slug: str, items: list[s.CollectionItemIn]
) -> m.Collection:
    col = await get_collection(db, slug)
    ids = [i.content_id for i in items]
    if ids:
        found = (await db.scalars(select(m.Content.id).where(m.Content.id.in_(ids)))).all()
        if len(set(found)) != len(set(ids)):
            raise NotFoundError("One or more content items not found")
    col.items = [
        m.CollectionItem(content_id=i.content_id, sort_order=i.sort_order) for i in items
    ]
    await db.commit()
    return await get_collection(db, slug)
