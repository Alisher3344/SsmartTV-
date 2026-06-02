"""Carousel slide business logic (async CRUD)."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.exceptions import NotFoundError
from ssmarttv.domains.carousel.models import CarouselSlide
from ssmarttv.domains.carousel.schemas import SlideIn, SlideUpdate


async def list_slides(db: AsyncSession, *, active_only: bool = False) -> list[CarouselSlide]:
    stmt = select(CarouselSlide)
    if active_only:
        stmt = stmt.where(CarouselSlide.is_active.is_(True))
    stmt = stmt.order_by(CarouselSlide.sort_order, CarouselSlide.id)
    return list((await db.scalars(stmt)).all())


async def get_slide(db: AsyncSession, slide_id: int) -> CarouselSlide:
    slide = await db.get(CarouselSlide, slide_id)
    if slide is None:
        raise NotFoundError("Slide not found")
    return slide


async def create_slide(db: AsyncSession, data: SlideIn) -> CarouselSlide:
    slide = CarouselSlide(**data.model_dump())
    db.add(slide)
    await db.commit()
    await db.refresh(slide)
    return slide


async def update_slide(db: AsyncSession, slide_id: int, data: SlideUpdate) -> CarouselSlide:
    slide = await get_slide(db, slide_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(slide, field, value)
    await db.commit()
    await db.refresh(slide)
    return slide


async def delete_slide(db: AsyncSession, slide_id: int) -> None:
    slide = await get_slide(db, slide_id)
    await db.delete(slide)
    await db.commit()
