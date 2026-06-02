"""HLS proxy endpoints: manifest (premium-gated) and segment (SSRF-guarded)."""
from urllib.parse import unquote

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.exceptions import AppError
from ssmarttv.core.ratelimit import RateLimit, hit
from ssmarttv.db.session import get_db
from ssmarttv.domains.auth.dependencies import get_optional_user
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.channels import service as channel_service
from ssmarttv.domains.streaming import service, ssrf
from ssmarttv.domains.subscriptions.service import ensure_can_watch

router = APIRouter(tags=["streaming"])

_CORS = {"Access-Control-Allow-Origin": "*"}
_M3U8 = "application/vnd.apple.mpegurl"
_SEGMENT_LIMIT = RateLimit(300, 60)  # per client ip, per minute


@router.get("/stream/{slug}")
async def stream_manifest(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> Response:
    channel = await channel_service.get_channel(db, slug)
    if not channel.stream_url:
        raise AppError("Channel has no stream", code="not_found")
    # Premium channels require auth + entitlement.
    await ensure_can_watch(db, channel.access_level, user)
    await ssrf.validate_target(
        channel.stream_url, allowed_hosts=await service.get_allowed_hosts(db)
    )
    # Prefer channel-specific headers; otherwise reuse headers configured for
    # another channel on the same host (some playlists only set Referer/UA on a
    # few entries of the same provider).
    host_headers = await service.get_host_headers(db)
    headers = channel.stream_headers or service.headers_for(
        channel.stream_url, host_headers
    )
    try:
        manifest = await service.fetch_manifest(channel.stream_url, headers=headers)
    except httpx.HTTPError as exc:
        raise AppError(
            "Upstream stream unavailable", code="upstream_error",
        ) from exc
    return Response(content=manifest, media_type=_M3U8, headers=_CORS)


@router.get("/segment")
async def stream_segment(
    request: Request,
    request_url: str = Query(alias="url"),
    db: AsyncSession = Depends(get_db),
) -> Response:
    target = unquote(request_url)
    allowed = await service.get_allowed_hosts(db)
    await ssrf.validate_target(target, allowed_hosts=allowed)

    client_host = request.client.host if request.client else "anon"
    await hit("segment", client_host, _SEGMENT_LIMIT)

    # Some upstreams require Referer/User-Agent on every request (manifest and
    # segments alike); resolve them by host so this stateless endpoint matches.
    host_headers = await service.get_host_headers(db)
    upstream_headers = service.headers_for(target, host_headers)

    # Nested playlist (master -> variant .m3u8): rewrite recursively so its
    # segments are proxied too, instead of returned as raw bytes.
    if target.split("?", 1)[0].endswith(".m3u8"):
        try:
            manifest = await service.fetch_manifest(target, headers=upstream_headers)
        except httpx.HTTPError as exc:
            raise AppError("Variant fetch failed", code="upstream_error") from exc
        return Response(content=manifest, media_type=_M3U8, headers=_CORS)

    client = service.get_client()
    upstream = await client.send(
        client.build_request("GET", target, headers=upstream_headers), stream=True
    )
    if upstream.status_code >= 400:
        await upstream.aclose()
        raise AppError("Segment fetch failed", code="upstream_error")

    media_type = upstream.headers.get("content-type", "application/octet-stream")

    async def _iter():  # type: ignore[no-untyped-def]
        try:
            async for chunk in upstream.aiter_bytes():
                yield chunk
        finally:
            await upstream.aclose()

    return StreamingResponse(_iter(), media_type=media_type, headers=_CORS)
