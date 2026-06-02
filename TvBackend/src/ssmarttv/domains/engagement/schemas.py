"""Engagement request/response schemas."""
from datetime import datetime

from pydantic import BaseModel, Field


class CommentIn(BaseModel):
    body: str = Field(min_length=1, max_length=2000)
    parent_id: int | None = None


class CommentOut(BaseModel):
    id: int
    content_id: int
    user_id: int
    author_name: str
    parent_id: int | None
    body: str
    status: str
    created_at: datetime


class CommentModerateIn(BaseModel):
    status: str = Field(pattern="^(visible|hidden|pending)$")


class LikeStatusOut(BaseModel):
    content_id: int
    likes: int
    liked: bool


class WatchIn(BaseModel):
    content_id: int
    episode_id: int | None = None
    progress_sec: int = Field(default=0, ge=0)


class WatchOut(BaseModel):
    content_id: int
    episode_id: int | None = None
    progress_sec: int
    watched_at: datetime


class RecommendationOut(BaseModel):
    content_id: int
    slug: str
    type: str
    title: str
    poster: str | None = None
    access_level: str
    score: int
