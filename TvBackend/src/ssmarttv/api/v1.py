"""Aggregates every domain router under the ``/api/v1`` prefix.

Domain routers are registered here as each step lands (auth, catalog,
channels, streaming, engagement). Keeping the wiring in one place makes the
public API surface easy to read.
"""
from fastapi import APIRouter

from ssmarttv.domains.auth.internal_router import internal_router
from ssmarttv.domains.auth.router import accounts_router
from ssmarttv.domains.auth.router import router as auth_router
from ssmarttv.domains.carousel.internal_router import internal_router as carousel_internal_router
from ssmarttv.domains.carousel.router import router as carousel_router
from ssmarttv.domains.catalog.router import router as catalog_router
from ssmarttv.domains.channels.router import router as channels_router
from ssmarttv.domains.engagement.router import router as engagement_router
from ssmarttv.domains.streaming.router import router as streaming_router
from ssmarttv.domains.subscriptions.router import router as subscriptions_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(accounts_router)
api_router.include_router(internal_router)
api_router.include_router(catalog_router)
api_router.include_router(channels_router)
api_router.include_router(carousel_router)
api_router.include_router(carousel_internal_router)
api_router.include_router(subscriptions_router)
api_router.include_router(streaming_router)
api_router.include_router(engagement_router)
