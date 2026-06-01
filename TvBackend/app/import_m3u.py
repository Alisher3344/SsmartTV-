"""Import channels from an M3U/M3U8 playlist into Postgres.

Usage:
    python -m app.import_m3u data/uzbek-channels.m3u

Each ``#EXTINF`` line (name + optional tvg-id) followed by a stream URL becomes
a live Channel. The slug is derived from tvg-id (or the name); duplicates by
slug keep the first (highest-quality, since playlists list HD first). Upserts
by slug, so re-running updates existing rows. Channels are marked ``is_live``
and served to clients via the /api/stream/{slug} proxy.
"""
import asyncio
import re
import sys
from urllib.parse import quote

from sqlalchemy import select

from app.db.session import async_session_maker
from app.models.channel import Channel

_TVG_ID = re.compile(r'tvg-id="([^"]*)"')
_RES_SUFFIX = re.compile(r"\s*[\(\[].*$")  # strip " (1080p)", " [Not 24/7]"

# (substrings, category) — checked in order, first match wins.
_CATEGORY_RULES: list[tuple[tuple[str, ...], str]] = [
    (("cinema", "kino"), "kino"),
    (("music", "navo"), "musiqiy"),
    (("bolajon", "bola"), "bolalar"),
    (("dunyo",), "sayohat"),
    (("madaniyat",), "madaniyat"),
    (("tarixi",), "hujjatli"),
    (("sevimli", "mahalla", "dasturxon", "makon"), "oilaviy"),
    (("yoshlar", "zo'r", "zor", "ftv", "my5", "renessans", "biz"), "kongilochar"),
    (
        ("24", "toshkent", "uzreport", "qaraqalpaq", "mtrk", "milliy", "navoiy",
         "buxoro", "farg", "andijon", "o'zbekiston", "ozbekiston"),
        "yangiliklar",
    ),
]


def categorize(name: str) -> str:
    low = name.lower()
    for keywords, category in _CATEGORY_RULES:
        if any(k in low for k in keywords):
            return category
    return "barcasi"


def slugify(tvg_id: str, name: str) -> str:
    base = tvg_id.split(".")[0] if tvg_id else name
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return slug or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def placeholder_logo(name: str) -> str:
    label = quote(name[:14])
    return f"https://via.placeholder.com/120x80/710087/ffffff?text={label}"


def parse_m3u(text: str, country: str | None = None) -> list[dict]:
    """Parse an M3U playlist into channel rows.

    When ``country`` is given, it becomes the channel ``category`` (the primary
    country grouping) and the keyword genre goes into ``subcategory`` (dropped
    when it falls back to the generic default). Without ``country`` (legacy
    behaviour) the genre stays in ``category``.
    """
    rows: list[dict] = []
    seen: set[str] = set()
    pending: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#EXTINF") and "," in line:
            tvg_match = _TVG_ID.search(line)
            tvg_id = tvg_match.group(1) if tvg_match else ""
            raw_name = line.split(",", 1)[1].strip()
            name = _RES_SUFFIX.sub("", raw_name).strip()
            pending = {"tvg_id": tvg_id, "name": name}
        elif line and not line.startswith("#") and pending is not None:
            slug = slugify(pending["tvg_id"], pending["name"])
            if slug not in seen:
                seen.add(slug)
                genre = categorize(pending["name"])
                if country:
                    category = country
                    subcategory = genre if genre != "barcasi" else None
                else:
                    category = genre
                    subcategory = None
                rows.append(
                    dict(
                        slug=slug,
                        name=pending["name"],
                        category=category,
                        subcategory=subcategory,
                        video_url=line,
                        is_live=True,
                        logo=placeholder_logo(pending["name"]),
                        description_uz="Jonli efir",
                        description_ru="Прямой эфир",
                    )
                )
            pending = None
    return rows


async def import_playlist(path: str, country: str | None = None) -> None:
    with open(path, encoding="utf-8") as f:
        rows = parse_m3u(f.read(), country)

    created = updated = 0
    async with async_session_maker() as session:
        for row in rows:
            existing = await session.scalar(
                select(Channel).where(Channel.slug == row["slug"])
            )
            if existing:
                for field, value in row.items():
                    setattr(existing, field, value)
                updated += 1
            else:
                session.add(Channel(**row))
                created += 1
        await session.commit()

    print(f"Parsed {len(rows)} unique channels from {path}")
    print(f"Channels: +{created} new, {updated} updated")


if __name__ == "__main__":
    # Usage: python -m app.import_m3u <path> [--country <country>]
    args = sys.argv[1:]
    country: str | None = None
    positional: list[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--country" and i + 1 < len(args):
            country = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1
    playlist = positional[0] if positional else "data/uzbek-channels.m3u"
    asyncio.run(import_playlist(playlist, country))
