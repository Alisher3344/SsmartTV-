"""Public carousel endpoint — bosh sahifadagi slaydlar (faqat faollari)."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.db.session import get_db
from ssmarttv.domains.carousel import service
from ssmarttv.domains.carousel.schemas import SlideOut

router = APIRouter(prefix="/carousel", tags=["carousel"])


@router.get("", response_model=list[SlideOut])
async def list_carousel(db: AsyncSession = Depends(get_db)) -> list[SlideOut]:
    slides = await service.list_slides(db, active_only=True)
    return [SlideOut.model_validate(s) for s in slides]
