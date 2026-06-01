from pydantic import BaseModel, ConfigDict


class ChannelBase(BaseModel):
    slug: str
    name: str
    logo: str | None = None
    current_show: str | None = None
    time: str | None = None
    description_uz: str | None = None
    description_ru: str | None = None
    image: str | None = None
    category: str = "barcasi"  # country
    subcategory: str | None = None  # genre
    video_url: str | None = None
    is_live: bool = False
    sort_order: int = 0


class ChannelCreate(ChannelBase):
    pass


class ChannelUpdate(BaseModel):
    name: str | None = None
    logo: str | None = None
    current_show: str | None = None
    time: str | None = None
    description_uz: str | None = None
    description_ru: str | None = None
    image: str | None = None
    category: str | None = None
    subcategory: str | None = None
    video_url: str | None = None
    is_live: bool | None = None
    sort_order: int | None = None


class ChannelOut(ChannelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # Proxy URL the client should play; null for non-live channels.
    stream_url: str | None = None
