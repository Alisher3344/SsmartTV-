"""Auth: OTP login, staff login, sessions, RBAC account management."""
import httpx
import pytest

from ssmarttv.main import app
from tests.helpers import latest_otp

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def _otp_login(c: httpx.AsyncClient, phone: str) -> dict:
    await c.post("/api/v1/auth/otp/request", json={"phone": phone})
    r = await c.post("/api/v1/auth/otp/verify", json={"phone": phone, "code": latest_otp()})
    assert r.status_code == 200
    return r.json()


async def test_otp_login_creates_regular_user(client):
    user = await _otp_login(client, "+998901112233")
    assert user["role"] == "user"
    assert user["phone"] == "+998901112233"
    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 200 and me.json()["id"] == user["id"]


async def test_me_requires_auth(client):
    assert (await client.get("/api/v1/auth/me")).status_code == 401


async def test_invalid_otp_rejected(client):
    await client.post("/api/v1/auth/otp/request", json={"phone": "+998901112233"})
    r = await client.post(
        "/api/v1/auth/otp/verify", json={"phone": "+998901112233", "code": "000000"}
    )
    assert r.status_code == 400 and r.json()["error"]["code"] == "otp_invalid"


async def test_sessions_and_logout(user_client):
    sessions = (await user_client.get("/api/v1/auth/sessions")).json()
    assert len(sessions) == 1 and sessions[0]["current"] is True
    assert (await user_client.post("/api/v1/auth/logout")).status_code == 200
    assert (await user_client.get("/api/v1/auth/me")).status_code == 401


async def test_logout_all_revokes_every_device(client):
    # Two devices for the same phone.
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c2:
        await _otp_login(client, "+998905550011")
        await _otp_login(c2, "+998905550011")
        r = await client.post("/api/v1/auth/logout-all")
        assert r.status_code == 200
        assert (await client.get("/api/v1/auth/me")).status_code == 401
        assert (await c2.get("/api/v1/auth/me")).status_code == 401


async def test_staff_login(superuser_client):
    me = (await superuser_client.get("/api/v1/auth/me")).json()
    assert me["role"] == "superuser" and me["permissions"] == ["*"]


async def test_regular_user_cannot_manage_accounts(user_client):
    r = await user_client.post(
        "/api/v1/staff/accounts",
        json={"username": "x", "password": "password1", "role": "staff"},
    )
    assert r.status_code == 403


async def test_superuser_creates_staff(superuser_client):
    r = await superuser_client.post(
        "/api/v1/staff/accounts",
        json={"username": "editor", "password": "editorpass1", "role": "staff"},
    )
    assert r.status_code == 201 and r.json()["role"] == "staff"


async def test_cannot_create_superuser_via_api(superuser_client):
    r = await superuser_client.post(
        "/api/v1/staff/accounts",
        json={"username": "boss", "password": "bosspass12", "role": "superuser"},
    )
    assert r.status_code == 403


async def test_premium_toggle_is_superuser_only(superuser_client, client):
    user = await _otp_login(client, "+998901119999")
    r = await superuser_client.post(
        f"/api/v1/users/{user['id']}/premium", json={"is_premium": True}
    )
    assert r.status_code == 200 and r.json()["is_premium"] is True
    # The regular user cannot toggle premium.
    assert (
        await client.post(f"/api/v1/users/{user['id']}/premium", json={"is_premium": False})
    ).status_code == 403
