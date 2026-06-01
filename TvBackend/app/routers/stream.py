from urllib.parse import unquote

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import channel_service, stream_service

router = APIRouter(tags=["stream"])

_CORS = {"Access-Control-Allow-Origin": "*"}
_M3U8 = "application/vnd.apple.mpegurl"


@router.get("/api/stream/{slug}")
async def stream_manifest(slug: str, db: AsyncSession = Depends(get_db)):
    channel = await channel_service.get_channel(db, slug)
    if channel is None or not channel.video_url:
        raise HTTPException(status_code=404, detail="Stream not found")
    try:
        manifest = await stream_service.fetch_manifest(channel.video_url)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502, detail=f"Upstream stream unavailable: {exc}"
        ) from exc
    return Response(content=manifest, media_type=_M3U8, headers=_CORS)


@router.get("/api/segment")
async def stream_segment(url: str = Query(...)):
    target = unquote(url)
    client = stream_service.get_client()

    # Nested playlist (master -> variant .m3u8): rewrite recursively so its
    # segments are also proxied, instead of returning it as raw bytes.
    if target.split("?", 1)[0].endswith(".m3u8"):
        try:
            manifest = await stream_service.fetch_manifest(target)
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail="Variant fetch failed") from exc
        return Response(content=manifest, media_type=_M3U8, headers=_CORS)

    upstream = await client.send(
        client.build_request("GET", target), stream=True
    )
    if upstream.status_code >= 400:
        await upstream.aclose()
        raise HTTPException(status_code=502, detail="Segment fetch failed")

    media_type = upstream.headers.get("content-type", "application/octet-stream")

    async def _iter():
        try:
            async for chunk in upstream.aiter_bytes():
                yield chunk
        finally:
            await upstream.aclose()

    return StreamingResponse(_iter(), media_type=media_type, headers=_CORS)


@router.get("/health")
async def health():
    return {
        "status": "OK",
        "service": "SSMART TV Backend",
        "endpoints": {
            "stream": "/api/stream/{slug}",
            "segment": "/api/segment?url=...",
            "channels": "/api/channels",
            "movies": "/api/movies",
            "auth": "/api/auth/{register,login,logout,me}",
        },
    }
