from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps.auth import require_admin
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelOut, ChannelUpdate
from app.services import channel_service

router = APIRouter(prefix="/api/channels", tags=["channels"])


def _to_out(channel: Channel) -> ChannelOut:
    out = ChannelOut.model_validate(channel)
    out.stream_url = f"/api/stream/{channel.slug}" if channel.is_live else None
    return out


@router.get("", response_model=list[ChannelOut])
async def list_channels(
    category: str | None = None,
    q: str | None = None,
    live_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    channels = await channel_service.list_channels(db, category, q, live_only)
    return [_to_out(c) for c in channels]


@router.get("/{slug}", response_model=ChannelOut)
async def get_channel(slug: str, db: AsyncSession = Depends(get_db)):
    channel = await channel_service.get_channel(db, slug)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return _to_out(channel)


@router.post("", response_model=ChannelOut, status_code=status.HTTP_201_CREATED)
async def create_channel(
    data: ChannelCreate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    if await channel_service.get_channel(db, data.slug):
        raise HTTPException(status_code=409, detail="Slug already exists")
    channel = Channel(**data.model_dump())
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return _to_out(channel)


@router.put("/{slug}", response_model=ChannelOut)
async def update_channel(
    slug: str,
    data: ChannelUpdate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    channel = await channel_service.get_channel(db, slug)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(channel, field, value)
    await db.commit()
    await db.refresh(channel)
    return _to_out(channel)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    slug: str,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),
):
    channel = await channel_service.get_channel(db, slug)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    await db.delete(channel)
    await db.commit()
