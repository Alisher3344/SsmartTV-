"""Catalog CRUD, pagination/filter and RBAC gating."""
import httpx
import pytest

from ssmarttv.main import app

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def _genre_ids(c: httpx.AsyncClient) -> list[int]:
    return [g["id"] for g in (await c.get("/api/v1/genres")).json()]


def _movie(title: str, genre_ids: list[int], **extra) -> dict:
    return {
        "translations": [{"lang": "uz", "title": title}],
        "genre_ids": genre_ids,
        **extra,
    }


async def _staff_client(superuser_client: httpx.AsyncClient) -> httpx.AsyncClient:
    await superuser_client.post(
        "/api/v1/staff/accounts",
        json={"username": "staff1", "password": "staffpass1", "role": "staff"},
    )
    transport = httpx.ASGITransport(app=app)
    c = httpx.AsyncClient(transport=transport, base_url="http://test")
    await c.post("/api/v1/auth/staff/login", json={"username": "staff1", "password": "staffpass1"})
    return c


async def test_create_and_get_movie(superuser_client, client):
    gids = await _genre_ids(superuser_client)
    r = await superuser_client.post(
        "/api/v1/movies",
        json=_movie(
            "Sheriklar",
            gids[:2],
            year=2026,
            ratings=[{"source": "imdb", "value": 8.8}],
            video_url="https://cdn/x.m3u8",
        ),
    )
    assert r.status_code == 201
    slug = r.json()["slug"]
    got = await client.get(f"/api/v1/movies/{slug}")
    assert got.status_code == 200
    body = got.json()
    assert len(body["genres"]) == 2
    assert body["ratings"][0]["source"] == "imdb"
    assert body["translations"][0]["title"] == "Sheriklar"


async def test_movie_pagination(superuser_client, client):
    gids = await _genre_ids(superuser_client)
    for i in range(3):
        await superuser_client.post("/api/v1/movies", json=_movie(f"M{i}", gids[:1]))
    page = (await client.get("/api/v1/movies?limit=2&offset=0")).json()
    assert page["total"] == 3 and len(page["items"]) == 2 and page["limit"] == 2


async def test_movie_filter_by_genre(superuser_client, client):
    gids = await _genre_ids(superuser_client)
    genres = (await superuser_client.get("/api/v1/genres")).json()
    await superuser_client.post("/api/v1/movies", json=_movie("Kino One", [gids[0]]))
    await superuser_client.post("/api/v1/movies", json=_movie("Sport One", [gids[1]]))
    page = (await client.get(f"/api/v1/movies?genre={genres[0]['slug']}")).json()
    assert page["total"] == 1


async def test_anonymous_cannot_create_movie(client):
    r = await client.post("/api/v1/movies", json=_movie("X", []))
    assert r.status_code == 401


async def test_staff_can_create_but_not_delete(superuser_client):
    gids = await _genre_ids(superuser_client)
    staff = await _staff_client(superuser_client)
    try:
        r = await staff.post("/api/v1/movies", json=_movie("StaffMovie", gids[:1]))
        assert r.status_code == 201
        slug = r.json()["slug"]
        assert (await staff.delete(f"/api/v1/movies/{slug}")).status_code == 403
        assert (await superuser_client.delete(f"/api/v1/movies/{slug}")).status_code == 200
    finally:
        await staff.aclose()


async def test_series_season_episode_flow(superuser_client, client):
    gids = await _genre_ids(superuser_client)
    series = (
        await superuser_client.post("/api/v1/series", json=_movie("Turnir", gids[:1]))
    ).json()
    slug = series["slug"]
    detail = await superuser_client.post(
        f"/api/v1/series/{slug}/seasons", json={"number": 1}
    )
    season_id = detail.json()["seasons"][0]["id"]
    ep = await superuser_client.post(
        f"/api/v1/seasons/{season_id}/episodes",
        json={"number": 1, "translations": [{"lang": "uz", "title": "1-qism"}]},
    )
    assert ep.status_code == 201
    got = (await client.get(f"/api/v1/series/{slug}")).json()
    assert len(got["seasons"]) == 1 and len(got["seasons"][0]["episodes"]) == 1
