# TvBackend

FastAPI backend for SsmartTv.

## Layout

```
app/
├── main.py            # FastAPI app, CORS, lifespan, router includes
├── core/
│   ├── config.py      # pydantic-settings (.env)
│   └── security.py    # Argon2 hashing + session-id generation
├── db/
│   ├── base.py        # DeclarativeBase
│   └── session.py     # async engine + get_db()
├── redis/client.py    # redis.asyncio session store
├── models/            # User, Channel, Movie
├── schemas/           # pydantic request/response models
├── services/          # auth, channel, stream (HLS proxy) logic
├── routers/           # auth, channels, movies, stream
├── deps/auth.py       # get_current_user / require_admin
└── seed.py            # load channels + movies into Postgres
alembic/               # async migrations
```

## Commands

```bash
source .venv/bin/activate

alembic revision --autogenerate -m "msg"   # new migration
alembic upgrade head                        # apply migrations
python -m app.seed                          # seed Russian channels + movies (idempotent)
python -m app.import_m3u data/uzbek-channels.m3u   # import channels from an M3U playlist
uvicorn app.main:app --reload --port 8000   # run dev server
```

## Notes

- **Sessions:** opaque id (`secrets.token_urlsafe`) → Redis key `session:{id}`
  with TTL `SESSION_TTL_SECONDS`; delivered via HttpOnly cookie. No JWT.
- **Passwords:** Argon2id via `argon2-cffi`; auto-rehash on parameter changes.
- **HLS proxy:** `stream_service.py` fetches the upstream m3u8 (stored in
  `channels.video_url`), rewrites media lines to `/api/segment?url=...`, and
  streams segments back with permissive CORS — replaces the old Node proxy.
- **CORS:** `allow_credentials=True`, so origins must be listed explicitly
  (no `*`) in `CORS_ORIGINS`.
- Make the first admin: `UPDATE users SET is_admin = true WHERE email = '...';`
