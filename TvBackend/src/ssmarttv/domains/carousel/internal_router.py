"""Trusted server-to-server carousel CRUD (X-Internal-Secret).

SsmartShop super-admin dashboard (ssmart-dashboard.ssmart.uz/tv-admins) shu
endpointlar orqali (shop backend proxy qilib) bosh sahifa karuselini boshqaradi.
Publik ochilmaydi — nginx /api/v1/internal/ ni bloklaydi, faqat docker tarmoq
ichidan (tv-api:8000) kirish mumkin.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.db.session import get_db
from ssmarttv.domains.auth.dependencies import require_internal_service
from ssmarttv.domains.auth.schemas import MessageOut
from ssmarttv.domains.carousel import service
from ssmarttv.domains.carousel.schemas import SlideIn, SlideOut, SlideUpdate

internal_router = APIRouter(
    prefix="/internal/carousel",
    tags=["internal"],
    dependencies=[Depends(require_internal_service)],
)


@internal_router.get("", response_model=list[SlideOut])
async def list_slides(db: AsyncSession = Depends(get_db)) -> list[SlideOut]:
    slides = await service.list_slides(db)
    return [SlideOut.model_validate(s) for s in slides]


@internal_router.post("", response_model=SlideOut, status_code=status.HTTP_201_CREATED)
async def create_slide(data: SlideIn, db: AsyncSession = Depends(get_db)) -> SlideOut:
    slide = await service.create_slide(db, data)
    return SlideOut.model_validate(slide)


@internal_router.put("/{slide_id}", response_model=SlideOut)
async def update_slide(
    slide_id: int, data: SlideUpdate, db: AsyncSession = Depends(get_db)
) -> SlideOut:
    slide = await service.update_slide(db, slide_id, data)
    return SlideOut.model_validate(slide)


@internal_router.delete("/{slide_id}", response_model=MessageOut)
async def delete_slide(slide_id: int, db: AsyncSession = Depends(get_db)) -> MessageOut:
    await service.delete_slide(db, slide_id)
    return MessageOut(detail="Slide deleted")
