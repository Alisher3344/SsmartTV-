from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieOut

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("", response_model=list[MovieOut])
async def list_movies(kind: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Movie)
    if kind:
        stmt = stmt.where(Movie.kind == kind)
    stmt = stmt.order_by(Movie.sort_order, Movie.id)
    result = await db.scalars(stmt)
    return list(result)


@router.get("/{slug}", response_model=MovieOut)
async def get_movie(slug: str, db: AsyncSession = Depends(get_db)):
    movie = await db.scalar(select(Movie).where(Movie.slug == slug))
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
