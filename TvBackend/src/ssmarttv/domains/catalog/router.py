"""Catalog HTTP endpoints. Public GETs; writes gated by RBAC permissions."""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.pagination import Page, PageParams, page_params
from ssmarttv.core.schemas import MessageOut
from ssmarttv.db.session import get_db
from ssmarttv.domains.auth.dependencies import get_optional_user, require_permission
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.auth.permissions import CATALOG_DELETE, CATALOG_WRITE
from ssmarttv.domains.catalog import schemas as s
from ssmarttv.domains.catalog import service
from ssmarttv.domains.subscriptions import service as sub_service

router = APIRouter(tags=["catalog"])

_write = Depends(require_permission(CATALOG_WRITE))
_delete = Depends(require_permission(CATALOG_DELETE))
_AccessQuery = Query(default=None, pattern="^(free|premium)$")


# --- Movies --------------------------------------------------------------
@router.get("/movies", response_model=Page[s.MovieOut])
async def list_movies(
    params: PageParams = Depends(page_params),
    q: str | None = None,
    genre: str | None = None,
    country_id: int | None = None,
    year: int | None = None,
    access_level: str | None = _AccessQuery,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> Page[s.MovieOut]:
    items, total = await service.list_movies(
        db, params, q=q, genre=genre, country_id=country_id,
        year=year, access_level=access_level,
    )
    can = await sub_service.can_watch_premium(db, user)
    return Page.create([s.MovieOut.of(mv, can_watch=can) for mv in items], total, params)


@router.get("/movies/{slug}", response_model=s.MovieOut)
async def get_movie(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> s.MovieOut:
    movie = await service.get_movie(db, slug)
    return s.MovieOut.of(movie, can_watch=await sub_service.can_watch_premium(db, user))


@router.post("/movies", response_model=s.MovieOut, status_code=status.HTTP_201_CREATED)
async def create_movie(
    data: s.MovieCreateIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.MovieOut:
    return s.MovieOut.of(await service.create_movie(db, data))


@router.put("/movies/{slug}", response_model=s.MovieOut)
async def update_movie(
    slug: str, data: s.MovieUpdateIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.MovieOut:
    return s.MovieOut.of(await service.update_movie(db, slug, data))


@router.delete("/movies/{slug}", response_model=MessageOut)
async def delete_movie(
    slug: str, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_movie(db, slug)
    return MessageOut(detail="Movie deleted")


# --- Series / seasons / episodes ----------------------------------------
@router.get("/series", response_model=Page[s.SeriesOut])
async def list_series(
    params: PageParams = Depends(page_params),
    q: str | None = None,
    genre: str | None = None,
    country_id: int | None = None,
    year: int | None = None,
    access_level: str | None = _AccessQuery,
    db: AsyncSession = Depends(get_db),
) -> Page[s.SeriesOut]:
    items, total = await service.list_series(
        db, params, q=q, genre=genre, country_id=country_id,
        year=year, access_level=access_level,
    )
    return Page.create([s.SeriesOut.of(sr) for sr in items], total, params)


@router.get("/series/{slug}", response_model=s.SeriesDetailOut)
async def get_series(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> s.SeriesDetailOut:
    series = await service.get_series(db, slug, with_seasons=True)
    can = await sub_service.can_watch_premium(db, user)
    return s.SeriesDetailOut.of(series, can_watch=can)


@router.post("/series", response_model=s.SeriesDetailOut, status_code=status.HTTP_201_CREATED)
async def create_series(
    data: s.SeriesCreateIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.SeriesDetailOut:
    return s.SeriesDetailOut.of(await service.create_series(db, data))


@router.put("/series/{slug}", response_model=s.SeriesDetailOut)
async def update_series(
    slug: str, data: s.SeriesUpdateIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.SeriesDetailOut:
    return s.SeriesDetailOut.of(await service.update_series(db, slug, data))


@router.delete("/series/{slug}", response_model=MessageOut)
async def delete_series(
    slug: str, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_series(db, slug)
    return MessageOut(detail="Series deleted")


@router.post("/series/{slug}/seasons", response_model=s.SeriesDetailOut)
async def add_season(
    slug: str, data: s.SeasonIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.SeriesDetailOut:
    return s.SeriesDetailOut.of(await service.add_season(db, slug, data))


@router.delete("/seasons/{season_id}", response_model=MessageOut)
async def delete_season(
    season_id: int, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_season(db, season_id)
    return MessageOut(detail="Season deleted")


@router.post("/seasons/{season_id}/episodes", response_model=s.EpisodeOut, status_code=201)
async def add_episode(
    season_id: int, data: s.EpisodeIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.EpisodeOut:
    return s.EpisodeOut.of(await service.add_episode(db, season_id, data))


@router.delete("/episodes/{episode_id}", response_model=MessageOut)
async def delete_episode(
    episode_id: int, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_episode(db, episode_id)
    return MessageOut(detail="Episode deleted")


# --- Genres --------------------------------------------------------------
@router.get("/genres", response_model=list[s.GenreOut])
async def list_genres(db: AsyncSession = Depends(get_db)) -> list[s.GenreOut]:
    return [s.GenreOut.model_validate(g) for g in await service.list_genres(db)]


@router.post("/genres", response_model=s.GenreOut, status_code=status.HTTP_201_CREATED)
async def create_genre(
    data: s.GenreIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.GenreOut:
    return s.GenreOut.model_validate(await service.create_genre(db, data))


@router.delete("/genres/{genre_id}", response_model=MessageOut)
async def delete_genre(
    genre_id: int, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_genre(db, genre_id)
    return MessageOut(detail="Genre deleted")


# --- Countries -----------------------------------------------------------
@router.get("/countries", response_model=list[s.CountryOut])
async def list_countries(db: AsyncSession = Depends(get_db)) -> list[s.CountryOut]:
    return [s.CountryOut.model_validate(c) for c in await service.list_countries(db)]


@router.post("/countries", response_model=s.CountryOut, status_code=status.HTTP_201_CREATED)
async def create_country(
    data: s.CountryIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.CountryOut:
    return s.CountryOut.model_validate(await service.create_country(db, data))


@router.delete("/countries/{country_id}", response_model=MessageOut)
async def delete_country(
    country_id: int, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_country(db, country_id)
    return MessageOut(detail="Country deleted")


# --- Actors --------------------------------------------------------------
@router.get("/actors", response_model=list[s.ActorOut])
async def list_actors(
    q: str | None = None, db: AsyncSession = Depends(get_db)
) -> list[s.ActorOut]:
    return [s.ActorOut.model_validate(a) for a in await service.list_actors(db, q)]


@router.post("/actors", response_model=s.ActorOut, status_code=status.HTTP_201_CREATED)
async def create_actor(
    data: s.ActorIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.ActorOut:
    return s.ActorOut.model_validate(await service.create_actor(db, data))


@router.delete("/actors/{actor_id}", response_model=MessageOut)
async def delete_actor(
    actor_id: int, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_actor(db, actor_id)
    return MessageOut(detail="Actor deleted")


# --- Collections ---------------------------------------------------------
@router.get("/collections", response_model=list[s.CollectionOut])
async def list_collections(db: AsyncSession = Depends(get_db)) -> list[s.CollectionOut]:
    return [s.CollectionOut.of(c) for c in await service.list_collections(db)]


@router.get("/collections/{slug}", response_model=s.CollectionOut)
async def get_collection(slug: str, db: AsyncSession = Depends(get_db)) -> s.CollectionOut:
    return s.CollectionOut.of(await service.get_collection(db, slug))


@router.post("/collections", response_model=s.CollectionOut, status_code=status.HTTP_201_CREATED)
async def create_collection(
    data: s.CollectionIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> s.CollectionOut:
    return s.CollectionOut.of(await service.create_collection(db, data))


@router.put("/collections/{slug}/items", response_model=s.CollectionOut)
async def set_collection_items(
    slug: str,
    items: list[s.CollectionItemIn],
    db: AsyncSession = Depends(get_db),
    _: object = _write,
) -> s.CollectionOut:
    return s.CollectionOut.of(await service.set_collection_items(db, slug, items))


@router.delete("/collections/{slug}", response_model=MessageOut)
async def delete_collection(
    slug: str, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_collection(db, slug)
    return MessageOut(detail="Collection deleted")
