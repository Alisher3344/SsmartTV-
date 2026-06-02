# SsmartTv

IPTV + VOD streaming platform. The repo is split into two apps:

```
SsmartTv/
├── TvBackend/          # FastAPI: phone/OTP auth, RBAC, catalog, channels,
│                       #   premium gating, HLS proxy, engagement (see its README)
├── TvFrontend/         # React 19 + Vite SPA (UI, HLS player, i18n uz/ru)
├── docker-compose.yml  # PostgreSQL + Redis + the API service
└── .github/workflows/  # CI: ruff + mypy + pytest
```

> The backend was re-architected to a senior-level, domain-driven FastAPI app
> (`src/ssmarttv`, RBAC, phone+OTP, premium content). The frontend still calls
> the old endpoints and will be reconnected to `/api/v1` in a follow-up.

## Backend stack

FastAPI · async SQLAlchemy 2.0 + asyncpg · Alembic · PostgreSQL · Redis ·
Argon2 (staff passwords) · eskiz.uz (SMS OTP) · httpx (HLS proxy). Fully typed
(mypy), linted (ruff), tested (pytest).

**Auth:** regular users sign in with **phone + OTP** (60-day sessions);
staff/admin/superuser with **username + password** (7-day sessions). Sessions
are opaque ids in Redis behind an HttpOnly cookie, with multi-device listing and
"log out everywhere". RBAC (Role + Permission) is DB-driven.

**Access tiers:** every channel/movie/series/episode is `free` or `premium`.
Browsing is open to all; free content plays without auth, premium needs auth +
entitlement (granted by a superuser — payment is deferred).

## Quick start

```bash
# 1. Infra
docker compose up -d postgres redis

# 2. Backend (see TvBackend/README.md for details)
cd TvBackend
make install && cp .env.example .env
make migrate && make seed
make superuser u=admin p='your-password'
make run                     # http://localhost:8000  (/docs, /health)

# …or run the whole API in a container:
cd .. && docker compose up -d api
```

## Tests & quality

```bash
cd TvBackend && make check   # ruff + mypy + pytest
```

CI runs the same gates on every push/PR (`.github/workflows/ci.yml`).
