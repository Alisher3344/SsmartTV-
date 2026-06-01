"""HLS proxy ported from proxy-server.cjs.

Fetches an upstream .m3u8 playlist, rewrites every non-comment line to route
through /api/segment so the browser only ever talks to our origin (solving CORS
for external CDN streams). Segments are streamed back without buffering.
"""
import re
from urllib.parse import quote

import httpx

# Shared client; created/closed in the FastAPI lifespan (see app.main).
_client: httpx.AsyncClient | None = None

_NON_COMMENT_LINE = re.compile(r"^(?![#\s])(.+)$", re.MULTILINE)


def set_client(client: httpx.AsyncClient) -> None:
    global _client
    _client = client


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("httpx client not initialised")
    return _client


def rewrite_manifest(text: str, playlist_url: str) -> str:
    """Rewrite media/segment URLs in an m3u8 to /api/segment?url=<absolute>."""
    base_url = playlist_url[: playlist_url.rfind("/") + 1]

    def _replace(match: re.Match) -> str:
        line = match.group(1).strip()
        if not line:
            return match.group(1)
        absolute = line if line.startswith("http") else base_url + line
        return f"/api/segment?url={quote(absolute, safe='')}"

    return _NON_COMMENT_LINE.sub(_replace, text)


async def fetch_manifest(upstream_url: str) -> str:
    resp = await get_client().get(upstream_url, follow_redirects=True)
    resp.raise_for_status()
    return rewrite_manifest(resp.text, str(resp.url))
