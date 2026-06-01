from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel import Channel


async def list_channels(
    db: AsyncSession,
    category: str | None = None,
    q: str | None = None,
    live_only: bool = False,
) -> list[Channel]:
    stmt = select(Channel)
    if category and category != "barcasi":
        stmt = stmt.where(Channel.category == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Channel.name.ilike(like)))
    if live_only:
        stmt = stmt.where(Channel.is_live.is_(True))
    stmt = stmt.order_by(Channel.sort_order, Channel.id)
    result = await db.scalars(stmt)
    return list(result)


async def get_channel(db: AsyncSession, slug: str) -> Channel | None:
    return await db.scalar(select(Channel).where(Channel.slug == slug))
