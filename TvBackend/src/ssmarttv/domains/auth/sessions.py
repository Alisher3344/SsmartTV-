"""Redis session store with multi-device tracking and sliding expiration.

Layout:
- ``session:{sid}``        → JSON {user_id, created_at, last_seen, device, ip, user_agent}
- ``user_sessions:{uid}``  → SET of the user's active session ids

Listing prunes session ids whose ``session:{sid}`` key has expired, so the set
stays consistent without a background job.
"""
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime

from ssmarttv.core.security import new_token
from ssmarttv.redis.client import redis_client


def _skey(sid: str) -> str:
    return f"session:{sid}"


def _ukey(user_id: int) -> str:
    return f"user_sessions:{user_id}"


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class SessionInfo:
    sid: str
    user_id: int
    created_at: str
    last_seen: str
    device: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    extra: dict = field(default_factory=dict)


async def create(
    user_id: int,
    ttl: int,
    *,
    device: str | None = None,
    ip: str | None = None,
    user_agent: str | None = None,
) -> str:
    sid = new_token()
    now = _now()
    data = {
        "user_id": user_id,
        "created_at": now,
        "last_seen": now,
        "device": device,
        "ip": ip,
        "user_agent": user_agent,
    }
    await redis_client.set(_skey(sid), json.dumps(data), ex=ttl)
    await redis_client.sadd(_ukey(user_id), sid)  # type: ignore[misc]
    await redis_client.expire(_ukey(user_id), ttl)
    return sid


async def get(sid: str, *, touch_ttl: int | None = None) -> dict | None:
    """Return session data, optionally refreshing TTL + last_seen (sliding)."""
    raw = await redis_client.get(_skey(sid))
    if raw is None:
        return None
    data = json.loads(raw)
    if touch_ttl is not None:
        data["last_seen"] = _now()
        await redis_client.set(_skey(sid), json.dumps(data), ex=touch_ttl)
        await redis_client.expire(_ukey(data["user_id"]), touch_ttl)
    return data


async def delete(sid: str) -> None:
    raw = await redis_client.get(_skey(sid))
    if raw is not None:
        user_id = json.loads(raw)["user_id"]
        await redis_client.srem(_ukey(user_id), sid)  # type: ignore[misc]
    await redis_client.delete(_skey(sid))


async def list_for_user(user_id: int) -> list[SessionInfo]:
    sids = await redis_client.smembers(_ukey(user_id))  # type: ignore[misc]
    sessions: list[SessionInfo] = []
    stale: list[str] = []
    for sid in sids:
        raw = await redis_client.get(_skey(sid))
        if raw is None:
            stale.append(sid)
            continue
        d = json.loads(raw)
        sessions.append(
            SessionInfo(
                sid=sid,
                user_id=d["user_id"],
                created_at=d["created_at"],
                last_seen=d["last_seen"],
                device=d.get("device"),
                ip=d.get("ip"),
                user_agent=d.get("user_agent"),
            )
        )
    if stale:
        await redis_client.srem(_ukey(user_id), *stale)  # type: ignore[misc]
    sessions.sort(key=lambda s: s.last_seen, reverse=True)
    return sessions


async def delete_all_for_user(user_id: int) -> int:
    sids = await redis_client.smembers(_ukey(user_id))  # type: ignore[misc]
    if sids:
        await redis_client.delete(*[_skey(s) for s in sids])
    await redis_client.delete(_ukey(user_id))
    return len(sids)
