from pydantic import BaseModel, ConfigDict


class MovieOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    kind: str
    title_uz: str
    title_ru: str | None = None
    title_en: str | None = None
    description_uz: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    genre_uz: str | None = None
    genre_ru: str | None = None
    age: str | None = None
    year: int | None = None
    image: str | None = None
    poster: str | None = None
    background: str | None = None
    color: str | None = None
    video_url: str | None = None
    rating_imdb: float | None = None
    rating_kinopoisk: float | None = None
    rating_ntv: float | None = None
    sort_order: int = 0
