"""Channel business logic: filtered listing and CRUD."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.exceptions import ConflictError, NotFoundError
from ssmarttv.core.pagination import PageParams
from ssmarttv.core.text import slugify
from ssmarttv.domains.catalog.models import Genre
from ssmarttv.domains.channels.models import Channel
from ssmarttv.domains.channels.schemas import ChannelIn, ChannelUpdate


async def list_channels(
    db: AsyncSession,
    params: PageParams,
    *,
    q: str | None = None,
    country_id: int | None = None,
    genre: str | None = None,
    live_only: bool = False,
    access_level: str | None = None,
) -> tuple[list[Channel], int]:
    stmt = select(Channel)
    if q:
        stmt = stmt.where(Channel.name.ilike(f"%{q}%"))
    if country_id is not None:
        stmt = stmt.where(Channel.country_id == country_id)
    if genre:
        stmt = stmt.where(Channel.genre.has(Genre.slug == genre))
    if live_only:
        stmt = stmt.where(Channel.is_live.is_(True))
    if access_level:
        stmt = stmt.where(Channel.access_level == access_level)

    total = await db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    stmt = stmt.order_by(Channel.sort_order, Channel.id).limit(params.limit).offset(params.offset)
    return list((await db.scalars(stmt)).all()), total


async def get_channel(db: AsyncSession, slug: str) -> Channel:
    channel = await db.scalar(select(Channel).where(Channel.slug == slug))
    if channel is None:
        raise NotFoundError("Channel not found")
    return channel


async def create_channel(db: AsyncSession, data: ChannelIn) -> Channel:
    slug = data.slug or slugify(data.name)
    if await db.scalar(select(Channel.id).where(Channel.slug == slug)):
        raise ConflictError(f"Slug '{slug}' already exists")
    channel = Channel(**data.model_dump(exclude={"slug"}), slug=slug)
    db.add(channel)
    await db.commit()
    return await get_channel(db, slug)


async def update_channel(db: AsyncSession, slug: str, data: ChannelUpdate) -> Channel:
    channel = await get_channel(db, slug)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(channel, field, value)
    await db.commit()
    return await get_channel(db, slug)


async def delete_channel(db: AsyncSession, slug: str) -> None:
    channel = await get_channel(db, slug)
    await db.delete(channel)
    await db.commit()
