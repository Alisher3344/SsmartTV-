"""Comments, likes, watch history and recommendations."""
import httpx
import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def _genre_ids(c: httpx.AsyncClient) -> list[int]:
    return [g["id"] for g in (await c.get("/api/v1/genres")).json()]


async def _movie(superuser_client, title, genres) -> dict:
    return (
        await superuser_client.post(
            "/api/v1/movies",
            json={"translations": [{"lang": "uz", "title": title}], "genre_ids": genres},
        )
    ).json()


async def test_comment_and_moderation(superuser_client, user_client, client):
    gids = await _genre_ids(superuser_client)
    m = await _movie(superuser_client, "Film", gids[:1])
    cid = m["id"]
    posted = await user_client.post(
        f"/api/v1/content/{cid}/comments", json={"body": "Zo'r!"}
    )
    assert posted.status_code == 201
    comment_id = posted.json()["id"]
    assert (await client.get(f"/api/v1/content/{cid}/comments")).json()["total"] == 1
    # Moderator hides it -> gone for the public, visible to moderators.
    await superuser_client.patch(
        f"/api/v1/comments/{comment_id}/moderate", json={"status": "hidden"}
    )
    assert (await client.get(f"/api/v1/content/{cid}/comments")).json()["total"] == 0
    assert (await superuser_client.get(f"/api/v1/content/{cid}/comments")).json()["total"] == 1


async def test_like_is_idempotent(superuser_client, user_client, client):
    gids = await _genre_ids(superuser_client)
    cid = (await _movie(superuser_client, "Likeable", gids[:1]))["id"]
    await user_client.post(f"/api/v1/content/{cid}/like")
    r = await user_client.post(f"/api/v1/content/{cid}/like")
    assert r.json()["likes"] == 1 and r.json()["liked"] is True
    assert (await client.get(f"/api/v1/content/{cid}/likes")).json()["likes"] == 1
    unliked = await user_client.request("DELETE", f"/api/v1/content/{cid}/like")
    assert unliked.json()["likes"] == 0


async def test_comment_requires_auth(superuser_client, client):
    gids = await _genre_ids(superuser_client)
    cid = (await _movie(superuser_client, "X", gids[:1]))["id"]
    assert (
        await client.post(f"/api/v1/content/{cid}/comments", json={"body": "hi"})
    ).status_code == 401


async def test_recommendations_use_watch_history(superuser_client, user_client):
    gids = await _genre_ids(superuser_client)
    watched = await _movie(superuser_client, "Watched", gids[:2])
    rec_target = await _movie(superuser_client, "Suggested", [gids[0]])
    await _movie(superuser_client, "Unrelated", [gids[2]])
    await user_client.post("/api/v1/me/watch", json={"content_id": watched["id"]})

    recs = (await user_client.get("/api/v1/me/recommendations")).json()
    rec_ids = [r["content_id"] for r in recs]
    assert watched["id"] not in rec_ids  # watched is excluded
    assert rec_target["id"] in rec_ids  # shares a genre


async def test_history_records_progress(superuser_client, user_client):
    gids = await _genre_ids(superuser_client)
    cid = (await _movie(superuser_client, "Hist", gids[:1]))["id"]
    await user_client.post("/api/v1/me/watch", json={"content_id": cid, "progress_sec": 120})
    await user_client.post("/api/v1/me/watch", json={"content_id": cid, "progress_sec": 300})
    hist = (await user_client.get("/api/v1/me/history")).json()
    assert hist["total"] == 1 and hist["items"][0]["progress_sec"] == 300
