"""Bosh sahifa karusel slaydi (super-admin tomonidan boshqariladi).

Rasm data URL ko'rinishida (kanallar `logo`/`image` kabi) Text ustunda saqlanadi
— alohida fayl yuklash infratuzilmasi kerak emas.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ssmarttv.db.base import Base, TimestampMixin


class CarouselSlide(Base, TimestampMixin):
    __tablename__ = "carousel_slides"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(Text)  # data URL yoki rasm manzili
    title_uz: Mapped[str | None] = mapped_column(String(200))
    title_ru: Mapped[str | None] = mapped_column(String(200))
    link_url: Mapped[str | None] = mapped_column(Text)  # bosilganda o'tiladigan havola
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
