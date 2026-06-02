"""Carousel slide request/response schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SlideIn(BaseModel):
    image: str  # data URL (data:image/...) yoki manzil
    title_uz: str | None = None
    title_ru: str | None = None
    link_url: str | None = None
    sort_order: int = 0
    is_active: bool = True


class SlideUpdate(BaseModel):
    image: str | None = None
    title_uz: str | None = None
    title_ru: str | None = None
    link_url: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class SlideOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image: str
    title_uz: str | None = None
    title_ru: str | None = None
    link_url: str | None = None
    sort_order: int
    is_active: bool
    created_at: datetime
