"""Premium access gating for movies and channels."""
import httpx
import pytest

from tests.helpers import latest_otp

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def _genre_ids(c: httpx.AsyncClient) -> list[int]:
    return [g["id"] for g in (await c.get("/api/v1/genres")).json()]


async def _login_user(c: httpx.AsyncClient, phone: str) -> dict:
    await c.post("/api/v1/auth/otp/request", json={"phone": phone})
    return (
        await c.post("/api/v1/auth/otp/verify", json={"phone": phone, "code": latest_otp()})
    ).json()


async def _premium_movie(superuser_client) -> str:
    gids = await _genre_ids(superuser_client)
    r = await superuser_client.post(
        "/api/v1/movies",
        json={
            "translations": [{"lang": "uz", "title": "Premium"}],
            "genre_ids": gids[:1],
            "access_level": "premium",
            "video_url": "https://cdn/secret.m3u8",
        },
    )
    return r.json()["slug"]


async def test_premium_video_url_hidden_from_anonymous(superuser_client, client):
    slug = await _premium_movie(superuser_client)
    body = (await client.get(f"/api/v1/movies/{slug}")).json()
    assert body["video_url"] is None and body["playable"] is False


async def test_premium_revealed_after_grant(superuser_client, client):
    slug = await _premium_movie(superuser_client)
    user = await _login_user(client, "+998901112233")
    assert (await client.get(f"/api/v1/movies/{slug}")).json()["video_url"] is None
    await superuser_client.post(
        f"/api/v1/users/{user['id']}/premium", json={"is_premium": True}
    )
    body = (await client.get(f"/api/v1/movies/{slug}")).json()
    assert body["video_url"] == "https://cdn/secret.m3u8" and body["playable"] is True


async def test_subscription_grant_enables_premium(superuser_client, client):
    slug = await _premium_movie(superuser_client)
    user = await _login_user(client, "+998901114455")
    await superuser_client.post(
        f"/api/v1/users/{user['id']}/subscription", json={"days": 30, "plan": "monthly"}
    )
    sub = (await client.get("/api/v1/me/subscription")).json()
    assert sub["can_watch_premium"] is True
    assert (await client.get(f"/api/v1/movies/{slug}")).json()["video_url"] is not None


async def test_premium_channel_stream_requires_auth(superuser_client, client):
    await superuser_client.post(
        "/api/v1/channels",
        json={
            "name": "Prem",
            "slug": "prem",
            "stream_url": "https://8.8.8.8/live.m3u8",
            "access_level": "premium",
            "is_live": True,
        },
    )
    # Anonymous -> must sign in (401).
    assert (await client.get("/api/v1/stream/prem")).status_code == 401


async def test_free_movie_visible_to_anonymous(superuser_client, client):
    gids = await _genre_ids(superuser_client)
    r = await superuser_client.post(
        "/api/v1/movies",
        json={
            "translations": [{"lang": "uz", "title": "Free"}],
            "genre_ids": gids[:1],
            "access_level": "free",
            "video_url": "https://cdn/free.m3u8",
        },
    )
    body = (await client.get(f"/api/v1/movies/{r.json()['slug']}")).json()
    assert body["video_url"] == "https://cdn/free.m3u8" and body["playable"] is True
