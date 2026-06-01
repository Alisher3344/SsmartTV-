"""Seed channels and movies into Postgres from the original frontend data.

Run with:  python -m app.seed
Idempotent: upserts by ``slug``. The 24 channels are transcribed from
TVFrontend/src/pages/TVChannels.jsx, plus РОССИЯ 1 from src/data/movies.js.
Upstream m3u8 URLs for the 4 live channels come from the old proxy-server.cjs.
"""
import asyncio

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import async_session_maker
from app.models.channel import Channel
from app.models.movie import Movie
from app.models.user import User

# --- Upstream stream URLs (Russian channels; Uzbek channels come from the
#     M3U importer — see app/import_m3u.py + data/uzbek-channels.m3u) ---------
KARUSEL_URL = "https://streaming.goodstream.icu/live/232-req_offset_28000000-req_window_0-3k_v5.m3u8"
RUSSIA1_URL = "https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8"
RUSSIA24_URL = "https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia24-hd/1080p.m3u8"

CHANNELS = [
    # Russian streams kept from the original app; Uzbek channels are imported
    # separately from the M3U playlist.
    dict(slug="karusel", name="Карусель", category="rossiya", subcategory="bolalar",
         is_live=True,
         video_url=KARUSEL_URL, logo="/karusel-logo.svg", current_show="Ералаш",
         time="18:05 - 19:00", description_uz="Bolalar kanali", description_ru="Детский канал",
         image="https://images.unsplash.com/photo-1587049016823-69d14b5b5628?w=400&h=250&fit=crop"),
    dict(slug="russia24", name="Россия 24", category="rossiya", subcategory="yangiliklar",
         is_live=True,
         video_url=RUSSIA24_URL, logo="/russia24-logo.svg", current_show="Вести в 20:00",
         time="20:00 - 20:40", description_uz="24/7 yangiliklar kanali",
         description_ru="Информационный канал 24/7",
         image="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=250&fit=crop"),
    dict(slug="russia1", name="РОССИЯ 1", category="rossiya", subcategory="yangiliklar",
         is_live=True,
         video_url=RUSSIA1_URL, logo="/russia1-logo.svg", current_show="Вести",
         time="20:00 - 21:00", description_uz="Rossiya milliy telekanali",
         description_ru="Национальный телеканал России",
         image="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=250&fit=crop"),
]

MOVIES = [
    dict(slug="sheriklar-3", kind="hero", title_uz="SHERIKLAR III", title_ru="ШЕРИКLAR III",
         description_uz="Komediya, 2026, 12+, Qyrgyzstan",
         description_ru="Комедия, 2026, 12+, Кыргызстан", genre_uz="Komediya", genre_ru="Комедия",
         age="12+", year=2026, rating_imdb=8.8, rating_kinopoisk=8.8, rating_ntv=8.8,
         image="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=1200&h=600&fit=crop",
         sort_order=1),
    dict(slug="turnir", kind="featured", title_uz="Turnir", title_ru="Турнир",
         description_uz="Fasl 1, Seriya 1", description_ru="Сезон 1, Серия 1",
         image="https://images.unsplash.com/photo-1574267432644-f610a4e1dd6e?w=300&h=400&fit=crop",
         sort_order=1),
    dict(slug="premiere-34-yillik-orzu", kind="premiere", title_uz="34 yillik o'rzu",
         title_ru="34-летняя мечта", genre_uz="Badiiy", genre_ru="Художественный",
         image="https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop",
         sort_order=1),
    dict(slug="premiere-jannat-2", kind="premiere", title_uz="Jannat 2: Onamga maktub",
         title_ru="Джаннат 2: Письмо маме", genre_uz="Oilaga", genre_ru="Для семьи", age="12+",
         image="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop",
         sort_order=2),
    dict(slug="premiere-krik-7", kind="premiere", title_uz="KRIK 7", title_ru="КРИК 7",
         genre_uz="Qo'rqinchli", genre_ru="Ужасы", age="18+",
         image="https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=300&h=450&fit=crop",
         sort_order=3),
    dict(slug="premiere-salom-yevropa", kind="premiere", title_uz="Salom Yevropa!",
         title_ru="Привет Европа!", genre_uz="Oilaga", genre_ru="Для семьи",
         image="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop",
         sort_order=4),
    dict(slug="premiere-priguny", kind="premiere", title_uz="Priguny", title_ru="Прыгуны",
         genre_uz="Subtitrlash", genre_ru="Субтитры",
         image="https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=300&h=450&fit=crop",
         sort_order=5),
    dict(slug="premiere-sheriklar-3", kind="premiere", title_uz="Sheriklar 3",
         title_ru="Шерикlar 3", genre_uz="Oilaga", genre_ru="Для семьи",
         image="https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop",
         sort_order=6),
    dict(slug="cinema-viju", kind="cinema", title_uz="viju", title_ru="viju", color="#00d9c0",
         poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%2300d9c0'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='28' font-weight='bold' fill='white' text-anchor='middle'%3Eviju%3C/text%3E%3C/svg%3E",
         sort_order=1),
    dict(slug="cinema-premier", kind="cinema", title_uz="PREMIER", title_ru="PREMIER",
         color="#ffd700", sort_order=2),
    dict(slug="cinema-disney-plus", kind="cinema", title_uz="Disney+", title_ru="Disney+",
         color="#0063e5", sort_order=3),
    dict(slug="cinema-ssmart-tv", kind="cinema", title_uz="SSMART TV", title_ru="SSMART TV",
         color="#710087", sort_order=4),
    dict(slug="cinema-salom-tv", kind="cinema", title_uz="salom.tv", title_ru="salom.tv",
         color="#0080ff", sort_order=5),
    dict(slug="cinema-paramount-plus", kind="cinema", title_uz="Paramount+", title_ru="Paramount+",
         color="#0063e5", sort_order=6),
]


async def _upsert(session, model, key_field, rows):
    created = updated = 0
    for row in rows:
        key = row[key_field]
        existing = await session.scalar(
            select(model).where(getattr(model, key_field) == key)
        )
        if existing:
            for field, value in row.items():
                setattr(existing, field, value)
            updated += 1
        else:
            session.add(model(**row))
            created += 1
    return created, updated


async def seed() -> None:
    # Default admin for the admin panel (login: admin123 / password: admin123).
    # Hash computed here (not at import time) since hashing is relatively costly.
    users = [
        dict(
            email="admin@ssmart.tv",
            username="admin123",
            password_hash=hash_password("admin123"),
            is_admin=True,
        ),
    ]
    async with async_session_maker() as session:
        u_new, u_upd = await _upsert(session, User, "username", users)
        c_new, c_upd = await _upsert(session, Channel, "slug", CHANNELS)
        m_new, m_upd = await _upsert(session, Movie, "slug", MOVIES)
        await session.commit()
    print(f"Users:    +{u_new} new, {u_upd} updated (admin123)")
    print(f"Channels: +{c_new} new, {c_upd} updated")
    print(f"Movies:   +{m_new} new, {m_upd} updated")


if __name__ == "__main__":
    asyncio.run(seed())
