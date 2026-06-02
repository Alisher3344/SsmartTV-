"""Small text utilities."""
import re

_NON_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Lowercase, collapse non-alphanumerics to single hyphens, trim."""
    return _NON_SLUG.sub("-", value.lower()).strip("-")
