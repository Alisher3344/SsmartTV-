"""FastAPI application factory: middleware, lifespan, health, router wiring."""
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from ssmarttv import __version__
from ssmarttv.api.v1 import api_router
from ssmarttv.core.config import settings
from ssmarttv.core.exceptions import register_exception_handlers
from ssmarttv.core.logging import configure_logging, request_id_ctx
from ssmarttv.db.session import engine
from ssmarttv.domains.streaming import service as stream_service
from ssmarttv.redis import client as redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.LOG_LEVEL, settings.LOG_JSON)
    # Shared httpx client for the HLS proxy.
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(20.0, connect=10.0),
        headers={"User-Agent": "Mozilla/5.0 (SsmartTv proxy)"},
    )
    stream_service.set_client(http_client)
    try:
        yield
    finally:
        await http_client.aclose()
        await redis.redis_client.aclose()
        await engine.dispose()


def create_app() -> FastAPI:
    configure_logging(settings.LOG_LEVEL, settings.LOG_JSON)
    app = FastAPI(title="SsmartTv API", version=__version__, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_origin_regex=settings.CORS_ORIGIN_REGEX,
        allow_credentials=True,  # browser must send the session cookie
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def _request_id(request: Request, call_next) -> Response:  # type: ignore[no-untyped-def]
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        token = request_id_ctx.set(request_id)
        try:
            response = await call_next(request)
        finally:
            request_id_ctx.reset(token)
        response.headers["x-request-id"] = request_id
        return response

    register_exception_handlers(app)
    app.include_router(api_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        """Liveness probe — process is up."""
        return {"status": "ok", "version": __version__}

    @app.get("/health/ready", tags=["health"])
    async def ready() -> dict[str, object]:
        """Readiness probe — dependencies (Postgres, Redis) reachable."""
        checks: dict[str, str] = {}
        ok = True
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            checks["database"] = "ok"
        except Exception:
            checks["database"] = "error"
            ok = False
        try:
            await redis.ping()
            checks["redis"] = "ok"
        except Exception:
            checks["redis"] = "error"
            ok = False
        return {"status": "ok" if ok else "degraded", "checks": checks}

    return app


app = create_app()
