"""HLS proxy: fetch upstream m3u8, rewrite media lines through our origin.

Rewriting every segment/variant URL to ``/api/v1/segment?url=`` means the
browser only ever talks to our origin, solving CORS for external CDN streams
(this replaces the old Node ``proxy-server.cjs``).
"""
import json
import re
from urllib.parse import quote, urlsplit

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.config import settings
from ssmarttv.domains.channels.models import Channel
from ssmarttv.redis.client import redis_client

_client: httpx.AsyncClient | None = None
_NON_COMMENT_LINE = re.compile(r"^(?![#\s])(.+)$", re.MULTILINE)
_ALLOWED_HOSTS_KEY = "streaming:allowed_hosts"
_ALLOWED_HOSTS_TTL = 300
_HOST_HEADERS_KEY = "streaming:host_headers"
_HOST_HEADERS_TTL = 300


def set_client(client: httpx.AsyncClient) -> None:
    global _client
    _client = client


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("HLS proxy httpx client not initialised")
    return _client


def rewrite_manifest(text: str, playlist_url: str) -> str:
    """Rewrite media/segment URLs in an m3u8 to /api/v1/segment?url=<absolute>."""
    base_url = playlist_url[: playlist_url.rfind("/") + 1]

    def _replace(match: re.Match) -> str:
        line = match.group(1).strip()
        if not line:
            return match.group(1)
        absolute = line if line.startswith("http") else base_url + line
        return f"/api/v1/segment?url={quote(absolute, safe='')}"

    return _NON_COMMENT_LINE.sub(_replace, text)


async def fetch_manifest(
    upstream_url: str, headers: dict[str, str] | None = None
) -> str:
    resp = await get_client().get(
        upstream_url, headers=headers or None, follow_redirects=True
    )
    resp.raise_for_status()
    return rewrite_manifest(resp.text, str(resp.url))


async def get_host_headers(db: AsyncSession) -> dict[str, dict[str, str]]:
    """Map upstream host -> extra request headers (Referer/User-Agent/...).

    Some CDNs reject server-side fetches that lack a Referer or browser
    User-Agent. Headers are configured per channel; we key them by host so the
    stateless ``/segment`` endpoint can apply them too. Cached in Redis.
    """
    cached = await redis_client.get(_HOST_HEADERS_KEY)
    if cached:
        return json.loads(cached)

    mapping: dict[str, dict[str, str]] = {}
    stmt = select(Channel.stream_url, Channel.stream_headers).where(
        Channel.stream_headers.is_not(None)
    )
    for url, headers in (await db.execute(stmt)).all():
        host = urlsplit(str(url)).hostname
        if host and headers:
            mapping[host] = headers
    await redis_client.set(_HOST_HEADERS_KEY, json.dumps(mapping), ex=_HOST_HEADERS_TTL)
    return mapping


def headers_for(url: str, host_headers: dict[str, dict[str, str]]) -> dict[str, str] | None:
    host = urlsplit(url).hostname
    return host_headers.get(host) if host else None


async def get_allowed_hosts(db: AsyncSession) -> set[str]:
    """Hosts the proxy may fetch: channel stream hosts + configured extras.

    Cached in Redis (short TTL) to avoid a DB scan on every segment request.
    """
    cached = await redis_client.smembers(_ALLOWED_HOSTS_KEY)  # type: ignore[misc]
    if cached:
        return set(cached)

    hosts: set[str] = set(settings.STREAM_ALLOWED_HOSTS)
    stmt = select(Channel.stream_url).where(Channel.stream_url.is_not(None))
    urls = (await db.scalars(stmt)).all()
    for url in urls:
        host = urlsplit(str(url)).hostname
        if host:
            hosts.add(host)
    if hosts:
        await redis_client.sadd(_ALLOWED_HOSTS_KEY, *hosts)  # type: ignore[misc]
        await redis_client.expire(_ALLOWED_HOSTS_KEY, _ALLOWED_HOSTS_TTL)
    return hosts
