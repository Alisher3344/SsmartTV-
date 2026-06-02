"""Channel HTTP endpoints. Public GETs; writes gated by RBAC permissions."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.pagination import Page, PageParams, page_params
from ssmarttv.core.schemas import MessageOut
from ssmarttv.db.session import get_db
from ssmarttv.domains.auth.dependencies import get_optional_user, require_permission
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.auth.permissions import CHANNEL_DELETE, CHANNEL_WRITE
from ssmarttv.domains.catalog.schemas import CountryOut, GenreOut
from ssmarttv.domains.channels import service
from ssmarttv.domains.channels.models import Channel
from ssmarttv.domains.channels.schemas import ChannelIn, ChannelOut, ChannelUpdate

router = APIRouter(prefix="/channels", tags=["channels"])

_write = Depends(require_permission(CHANNEL_WRITE))
_delete = Depends(require_permission(CHANNEL_DELETE))
_AccessQuery = Query(default=None, pattern="^(free|premium)$")


def _to_out(channel: Channel, *, reveal_upstream: bool) -> ChannelOut:
    playback = (
        f"/api/v1/stream/{channel.slug}"
        if channel.is_live and channel.stream_url
        else None
    )
    return ChannelOut(
        id=channel.id,
        slug=channel.slug,
        name=channel.name,
        logo=channel.logo,
        image=channel.image,
        access_level=channel.access_level,
        is_live=channel.is_live,
        current_show=channel.current_show,
        time=channel.time,
        country=CountryOut.model_validate(channel.country) if channel.country else None,
        genre=GenreOut.model_validate(channel.genre) if channel.genre else None,
        sort_order=channel.sort_order,
        playback_url=playback,
        stream_url=channel.stream_url if reveal_upstream else None,
        stream_headers=channel.stream_headers if reveal_upstream else None,
        created_at=channel.created_at,
    )


def _can_write(user: User | None) -> bool:
    return user is not None and user.has_permission(CHANNEL_WRITE)


@router.get("", response_model=Page[ChannelOut])
async def list_channels(
    params: PageParams = Depends(page_params),
    q: str | None = None,
    country_id: int | None = None,
    genre: str | None = None,
    live_only: bool = False,
    access_level: str | None = _AccessQuery,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> Page[ChannelOut]:
    items, total = await service.list_channels(
        db, params, q=q, country_id=country_id, genre=genre,
        live_only=live_only, access_level=access_level,
    )
    reveal = _can_write(user)
    return Page.create([_to_out(c, reveal_upstream=reveal) for c in items], total, params)


@router.get("/{slug}", response_model=ChannelOut)
async def get_channel(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> ChannelOut:
    channel = await service.get_channel(db, slug)
    return _to_out(channel, reveal_upstream=_can_write(user))


@router.post("", response_model=ChannelOut, status_code=201)
async def create_channel(
    data: ChannelIn, db: AsyncSession = Depends(get_db), _: object = _write
) -> ChannelOut:
    channel = await service.create_channel(db, data)
    return _to_out(channel, reveal_upstream=True)


@router.put("/{slug}", response_model=ChannelOut)
async def update_channel(
    slug: str, data: ChannelUpdate, db: AsyncSession = Depends(get_db), _: object = _write
) -> ChannelOut:
    channel = await service.update_channel(db, slug, data)
    return _to_out(channel, reveal_upstream=True)


@router.delete("/{slug}", response_model=MessageOut)
async def delete_channel(
    slug: str, db: AsyncSession = Depends(get_db), _: object = _delete
) -> MessageOut:
    await service.delete_channel(db, slug)
    return MessageOut(detail="Channel deleted")
