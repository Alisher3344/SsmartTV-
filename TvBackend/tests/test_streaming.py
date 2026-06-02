"""HLS proxy: SSRF protection and manifest rewriting."""
import pytest

from ssmarttv.core.exceptions import AppError, PermissionDeniedError
from ssmarttv.domains.streaming import service, ssrf

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_manifest_rewrite_routes_through_proxy():
    src = "#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=1\nchunk0.ts\nhttps://cdn.example/v.m3u8\n"
    out = service.rewrite_manifest(src, "https://cdn.example/dir/master.m3u8")
    assert "/api/v1/segment?url=" in out
    assert "#EXT-X-STREAM-INF" in out  # comments preserved


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1/x",
        "http://169.254.169.254/latest/meta-data",  # cloud metadata
        "http://10.0.0.5/x",
        "http://192.168.1.1/x",
    ],
)
async def test_ssrf_blocks_internal_addresses(url):
    with pytest.raises(PermissionDeniedError):
        await ssrf.validate_target(url)


async def test_ssrf_rejects_non_http_scheme():
    with pytest.raises(AppError):
        await ssrf.validate_target("file:///etc/passwd")


async def test_ssrf_allows_public_ip():
    assert await ssrf.validate_target("https://8.8.8.8/playlist.m3u8")


async def test_segment_endpoint_blocks_internal(client):
    r = await client.get("/api/v1/segment", params={"url": "http://127.0.0.1/x"})
    assert r.status_code == 403


async def test_free_channel_stream_resolves(superuser_client, client):
    # Free channel: no auth needed; upstream unreachable -> upstream_error, not a
    # permission error (proves the gate + SSRF allowed the public host).
    await superuser_client.post(
        "/api/v1/channels",
        json={
            "name": "Free",
            "slug": "free",
            "stream_url": "https://8.8.8.8/live.m3u8",
            "access_level": "free",
            "is_live": True,
        },
    )
    r = await client.get("/api/v1/stream/free")
    assert r.status_code in (200, 400, 502)
    assert r.json().get("error", {}).get("code") != "permission_denied"
