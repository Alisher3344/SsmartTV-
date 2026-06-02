# TvBackend

FastAPI backend for **SsmartTv** — an IPTV + VOD platform with phone/OTP auth,
RBAC, premium content gating, an HLS CORS proxy, and engagement features
(comments, likes, recommendations).

## Stack

FastAPI · async SQLAlchemy 2.0 + asyncpg · Alembic · PostgreSQL · Redis
(sessions/OTP/rate-limit) · Argon2 (staff passwords) · eskiz.uz (SMS OTP) ·
httpx (HLS proxy). Packaged with `pyproject.toml`; linted by **ruff**, typed by
**mypy**, tested with **pytest**.

## Layout (`src/` + domain-driven)

```
src/ssmarttv/
├── main.py              # app factory, lifespan, request-id, /health, /health/ready
├── api/v1.py            # mounts every domain router under /api/v1
├── core/                # config, logging (JSON), exceptions, pagination,
│                        #   ratelimit, security, phone, sms/ (eskiz + console)
├── db/                  # Base + mixins, async session, all_models (Alembic registry)
├── redis/               # shared async Redis client
└── domains/
    ├── auth/            # User/Role/Permission, OTP, sessions/devices, RBAC deps
    ├── subscriptions/   # premium gate + (placeholder) subscriptions
    ├── catalog/         # Content→Movie/Series→Season→Episode, genres/countries/
    │                    #   actors/trailers/ratings/collections (joined inheritance)
    ├── channels/        # live TV channels (manual CRUD + M3U import)
    ├── engagement/      # comments, likes, watch history, recommendations
    └── streaming/       # HLS proxy + SSRF guard
scripts/                 # seed_reference, bootstrap_superuser, import_m3u
alembic/                 # async migrations
tests/                   # pytest (real Postgres test DB + Redis)
```

## Quick start

```bash
docker compose up -d postgres redis      # from the repo root
make install                             # venv + deps (dev extras)
cp .env.example .env
make migrate                             # create tables
make seed                                # roles, permissions, genres, countries
make superuser u=admin p='your-password' # bootstrap the superuser
make run                                 # http://localhost:8000  (/docs, /health)
make import f=data/uzbek-channels.m3u c=uz   # optional: load channels
```

Quality gates: `make check` (ruff + mypy + pytest).

Or run the whole API in Docker: `docker compose up -d api` (builds the image,
runs migrations, serves on :8000).

## Auth model

Two tracks share the `users` table:

- **Regular users** sign in with **phone + OTP** (eskiz.uz; dev prints the code
  to stdout via the `console` SMS backend). Sessions last 60 days.
- **staff / admin / superuser** sign in with **username + password** (Argon2),
  7-day sessions.

Sessions are opaque ids in Redis (`session:{id}` + per-user set) behind an
HttpOnly cookie, with sliding expiry. Users can list devices, log out one, or
log out everywhere.

**RBAC** is DB-driven (Role + Permission). `superuser` creates/deletes
admin & staff accounts (never another superuser — that's CLI-only) and is the
only role that can toggle a user's premium status.

## Access tiers

Channels, movies, series and episodes carry `access_level = free | premium`.
Anyone can browse the full catalogue; **free** content plays without auth.
**premium** playback requires auth + entitlement (`is_premium` flag or an active
subscription) — otherwise the API returns `401` (anonymous) or `402`
(authenticated, not entitled), and premium `video_url`s are withheld. Payment
integration is intentionally deferred; premium is granted by a superuser.

## HLS proxy & SSRF

`GET /api/v1/stream/{slug}` fetches the channel's upstream m3u8 and rewrites
every media line to `/api/v1/segment?url=...`, so the browser only talks to our
origin (solving CORS). The SSRF guard always blocks URLs resolving to
private/loopback/link-local/metadata addresses; set `STREAM_ENFORCE_ALLOWLIST=true`
to additionally restrict to known channel hosts + `STREAM_ALLOWED_HOSTS`.

## API overview (`/api/v1`)

| Area | Endpoints |
|------|-----------|
| Auth | `auth/otp/{request,verify}`, `auth/staff/login`, `auth/{logout,logout-all,sessions,me}` |
| Accounts | `staff/accounts` (CRUD, superuser), `users/{id}/premium`, `users/{id}/subscription` |
| Catalog | `movies`, `series` (+`seasons`/`episodes`), `genres`, `countries`, `actors`, `collections` |
| Channels | `channels` (public GET; `channel:write`/`channel:delete` for CRUD) |
| Engagement | `content/{id}/comments`, `content/{id}/like`, `me/watch`, `me/history`, `me/recommendations` |
| Streaming | `stream/{slug}`, `segment?url=` |
| Health | `/health`, `/health/ready` |

All list endpoints are paginated (`?limit`, `?offset`) and return
`{items, total, limit, offset}`. Errors use a consistent envelope:
`{"error": {"code", "message", "details"}}`.
