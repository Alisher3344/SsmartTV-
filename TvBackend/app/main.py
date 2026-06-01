from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.redis import client as session_store
from app.routers import auth, channels, movies, stream
from app.services import stream_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Shared httpx client for the HLS proxy.
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(20.0, connect=10.0),
        headers={"User-Agent": "Mozilla/5.0 (SsmartTv proxy)"},
    )
    stream_service.set_client(client)
    try:
        yield
    finally:
        await client.aclose()
        await session_store.redis_client.aclose()


app = FastAPI(title="SsmartTv API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,  # any localhost port in dev
    allow_credentials=True,  # required so the browser sends the session cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(channels.router)
app.include_router(movies.router)
app.include_router(stream.router)
