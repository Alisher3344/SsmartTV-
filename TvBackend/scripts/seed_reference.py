"""Seed RBAC reference data: roles, permissions and the role→permission matrix.

Idempotent — safe to re-run. Reference vocabularies for catalog (genres,
countries) are seeded by their own helpers added in the catalog step.

Usage:  python scripts/seed_reference.py
"""
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.db.session import async_session_maker
from ssmarttv.domains.auth.models import Permission, Role
from ssmarttv.domains.auth.permissions import (
    ALL_PERMISSIONS,
    ROLE_NAMES,
    ROLE_PERMISSIONS,
)
from ssmarttv.domains.catalog.models import Country, Genre

# (slug, name_uz, name_ru)
GENRES: list[tuple[str, str, str]] = [
    ("yangiliklar", "Yangiliklar", "Новости"),
    ("sport", "Sport", "Спорт"),
    ("kino", "Kino", "Кино"),
    ("seriallar", "Seriallar", "Сериалы"),
    ("musiqiy", "Musiqiy", "Музыкальные"),
    ("bolalar", "Bolalar", "Детские"),
    ("multfilm", "Multfilm", "Мультфильмы"),
    ("anime", "Anime", "Аниме"),
    ("hujjatli", "Hujjatli", "Документальные"),
    ("kongilochar", "Ko'ngilochar", "Развлекательные"),
    ("talimiy", "Ta'limiy", "Образовательные"),
    ("madaniyat", "Madaniyat", "Культура"),
    ("sayohat", "Sayohat", "Путешествия"),
    ("oilaviy", "Oilaviy", "Семейные"),
    ("komediya", "Komediya", "Комедия"),
    ("drama", "Drama", "Драма"),
    ("jangari", "Jangari", "Боевик"),
    ("qorqinchli", "Qo'rqinchli", "Ужасы"),
]

# (code, slug, name_uz, name_ru)
COUNTRIES: list[tuple[str, str, str, str]] = [
    ("uz", "ozbekiston", "O'zbekiston", "Узбекистан"),
    ("ru", "rossiya", "Rossiya", "Россия"),
    ("by", "belarus", "Belarus", "Беларусь"),
    ("us", "usa", "AQSH", "США"),
    ("tr", "turkiya", "Turkiya", "Турция"),
    ("kz", "qozogiston", "Qozog'iston", "Казахстан"),
]


async def seed_rbac(session: AsyncSession) -> None:
    # Permissions
    perms: dict[str, Permission] = {
        p.slug: p for p in (await session.scalars(select(Permission))).all()
    }
    for slug, name in ALL_PERMISSIONS.items():
        perm = perms.get(slug)
        if perm is None:
            perm = Permission(slug=slug, name=name)
            session.add(perm)
            perms[slug] = perm
        else:
            perm.name = name
    await session.flush()

    # Roles + their permission sets
    existing_roles = {
        r.slug: r for r in (await session.scalars(select(Role))).all()
    }
    for sort_order, (slug, perm_slugs) in enumerate(ROLE_PERMISSIONS.items()):
        role = existing_roles.get(slug)
        if role is None:
            role = Role(slug=slug, name=ROLE_NAMES[slug], sort_order=sort_order)
            session.add(role)
        else:
            role.name = ROLE_NAMES[slug]
            role.sort_order = sort_order
        role.permissions = [perms[s] for s in perm_slugs]


async def seed_catalog_reference(session: AsyncSession) -> None:
    genres = {g.slug: g for g in (await session.scalars(select(Genre))).all()}
    for order, (slug, uz, ru) in enumerate(GENRES):
        genre = genres.get(slug)
        if genre is None:
            session.add(Genre(slug=slug, name_uz=uz, name_ru=ru, sort_order=order))
        else:
            genre.name_uz, genre.name_ru, genre.sort_order = uz, ru, order

    countries = {c.code: c for c in (await session.scalars(select(Country))).all()}
    for order, (code, slug, uz, ru) in enumerate(COUNTRIES):
        country = countries.get(code)
        if country is None:
            session.add(
                Country(code=code, slug=slug, name_uz=uz, name_ru=ru, sort_order=order)
            )
        else:
            country.slug, country.name_uz, country.name_ru = slug, uz, ru
            country.sort_order = order


async def main() -> None:
    async with async_session_maker() as session:
        await seed_rbac(session)
        await seed_catalog_reference(session)
        await session.commit()
    print(
        f"Seeded {len(ALL_PERMISSIONS)} permissions, {len(ROLE_PERMISSIONS)} roles, "
        f"{len(GENRES)} genres, {len(COUNTRIES)} countries."
    )


if __name__ == "__main__":
    asyncio.run(main())
