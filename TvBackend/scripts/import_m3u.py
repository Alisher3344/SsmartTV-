"""Import live channels from an M3U/M3U8 playlist into Postgres.

Resolves country (``--country`` code/slug) and a keyword-derived genre to their
reference FKs. Upserts by slug, so re-running updates existing rows. Imported
channels are marked ``is_live`` and default to ``free`` access.

Usage:
    python scripts/import_m3u.py data/uzbek-channels.m3u --country uz
    python scripts/import_m3u.py data/belarus-channels.m3u --country by --access premium
"""
import argparse
import asyncio
import re

import httpx
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.db.session import async_session_maker
from ssmarttv.domains.catalog.models import Country, Genre
from ssmarttv.domains.channels.models import Channel

_TVG_ID = re.compile(r'tvg-id="([^"]*)"')
_DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
)
_RES_SUFFIX = re.compile(r"\s*[\(\[].*$")  # strip " (1080p)", " [Not 24/7]"

# (substrings, genre slug) — first match wins; slugs must exist in `genres`.
# Matched against the lowercased channel name (Latin + Cyrillic).
_GENRE_RULES: list[tuple[tuple[str, ...], str]] = [
    (("cinema", "kino", "дом кино", "победа"), "kino"),
    (("music", "navo", "муз"), "musiqiy"),
    (("bolajon", "bola", "карусель"), "bolalar"),
    (("dunyo",), "sayohat"),
    (("madaniyat", "россия к"), "madaniyat"),
    (("tarixi", "documentary", "документ"), "hujjatli"),
    (("sevimli", "mahalla", "dasturxon", "makon"), "oilaviy"),
    (("yoshlar", "zo'r", "zor", "ftv", "my5", "renessans", "biz",
      "стс", "тнт", "пятница", "тв3", "за!тв"), "kongilochar"),
    (
        ("24", "toshkent", "uzreport", "qaraqalpaq", "mtrk", "milliy", "navoiy",
         "buxoro", "farg", "andijon", "o'zbekiston", "ozbekiston",
         "нтв", "первый", "россия", "рен", "отр", "мир", "тв центр", "5 канал",
         "звезда", "крым", "луганск", "спас", "таврия"),
        "yangiliklar",
    ),
]


def categorize(name: str) -> str | None:
    low = name.lower()
    for keywords, slug in _GENRE_RULES:
        if any(k in low for k in keywords):
            return slug
    return None


def slugify(tvg_id: str, name: str) -> str:
    base = tvg_id.split(".")[0] if tvg_id else name
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return slug or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def parse_m3u(text: str) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    pending: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#EXTINF") and "," in line:
            tvg_match = _TVG_ID.search(line)
            tvg_id = tvg_match.group(1) if tvg_match else ""
            name = _RES_SUFFIX.sub("", line.split(",", 1)[1].strip()).strip()
            pending = {"tvg_id": tvg_id, "name": name, "headers": {}}
        elif line.startswith("#EXTVLCOPT") and pending is not None:
            # Player options carrying upstream request headers some CDNs require.
            if "http-referrer=" in line:
                pending["headers"]["Referer"] = line.split("http-referrer=", 1)[1].strip()
            elif "http-user-agent=" in line:
                pending["headers"]["User-Agent"] = (
                    line.split("http-user-agent=", 1)[1].strip()
                )
        elif line and not line.startswith("#") and pending is not None:
            slug = slugify(pending["tvg_id"], pending["name"])
            if slug not in seen:
                seen.add(slug)
                rows.append(
                    {
                        "slug": slug,
                        "name": pending["name"],
                        "genre_slug": categorize(pending["name"]),
                        "stream_url": line,
                        "stream_headers": pending["headers"] or None,
                    }
                )
            pending = None
    return rows


async def _is_playable(client: httpx.AsyncClient, row: dict) -> bool:
    """True if the upstream returns a playable HLS manifest.

    Filters out dead/geo-blocked (non-200), DASH (.mpd — our player is HLS-only)
    and anything that isn't an m3u8. Sends per-channel headers when present.
    """
    url = row["stream_url"]
    if url.split("?", 1)[0].lower().endswith(".mpd"):
        return False
    headers = {"User-Agent": _DEFAULT_UA, **(row["stream_headers"] or {})}
    try:
        resp = await client.get(url, headers=headers)
    except Exception:
        return False
    if resp.status_code != 200:
        return False
    ctype = resp.headers.get("content-type", "").lower()
    body = resp.text[:300].lstrip()
    if "<mpd" in body.lower():  # DASH served without .mpd suffix
        return False
    return "mpegurl" in ctype or body.startswith("#EXTM3U")


async def filter_playable(rows: list[dict], concurrency: int) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)

    async def check(row: dict) -> tuple[dict, bool]:
        async with sem:
            return row, await _is_playable(client, row)

    async with httpx.AsyncClient(timeout=12, follow_redirects=True) as client:
        results = await asyncio.gather(*(check(r) for r in rows))
    working = [r for r, ok in results if ok]
    print(f"Tested {len(rows)} streams → {len(working)} playable, "
          f"{len(rows) - len(working)} skipped (dead/geo-blocked/DASH)")
    return working


async def _resolve_country(session: AsyncSession, country: str | None) -> Country | None:
    if not country:
        return None
    obj = await session.scalar(
        select(Country).where(or_(Country.code == country, Country.slug == country))
    )
    if obj is None:
        raise SystemExit(f"Country '{country}' not found — seed reference data first.")
    return obj


async def import_playlist(
    path: str, country: str | None, access: str,
    test: bool = False, concurrency: int = 24,
) -> None:
    with open(path, encoding="utf-8") as f:
        rows = parse_m3u(f.read())

    if test:
        rows = await filter_playable(rows, concurrency)

    created = updated = 0
    async with async_session_maker() as session:
        country_obj = await _resolve_country(session, country)
        country_id = country_obj.id if country_obj else None
        country_code = country_obj.code if country_obj else None
        genres = {g.slug: g.id for g in (await session.scalars(select(Genre))).all()}

        for row in rows:
            genre_id = genres.get(row["genre_slug"]) if row["genre_slug"] else None
            slug = row["slug"]
            existing = await session.scalar(
                select(Channel).where(Channel.slug == slug)
            )
            # Generated slugs can collide across countries (e.g. uz "BIZ TV" and
            # us "Biz TV" both -> "biztv"). Suffix the newcomer with its country
            # code so we never clobber another country's channel.
            if existing and existing.country_id != country_id and country_code:
                slug = f"{slug}-{country_code}"
                existing = await session.scalar(
                    select(Channel).where(Channel.slug == slug)
                )
            values = {
                "name": row["name"],
                "stream_url": row["stream_url"],
                "stream_headers": row["stream_headers"],
                "country_id": country_id,
                "genre_id": genre_id,
                "access_level": access,
                "is_live": True,
            }
            if existing:
                for k, v in values.items():
                    setattr(existing, k, v)
                updated += 1
            else:
                session.add(Channel(slug=slug, **values))
                created += 1
        await session.commit()

    print(f"Parsed {len(rows)} channels from {path}")
    print(f"Channels: +{created} new, {updated} updated")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import channels from an M3U playlist")
    parser.add_argument("playlist")
    parser.add_argument("--country", default=None, help="country code or slug (e.g. uz)")
    parser.add_argument("--access", default="free", choices=("free", "premium"))
    parser.add_argument(
        "--test", action="store_true",
        help="probe each stream and import only playable HLS (skip dead/geo/DASH)",
    )
    parser.add_argument("--test-concurrency", type=int, default=24)
    args = parser.parse_args()
    asyncio.run(
        import_playlist(
            args.playlist, args.country, args.access,
            test=args.test, concurrency=args.test_concurrency,
        )
    )


if __name__ == "__main__":
    main()
