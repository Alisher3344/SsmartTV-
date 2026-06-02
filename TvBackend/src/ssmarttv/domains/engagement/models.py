"""Engagement: comments, likes and watch history (feeds recommendations)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ssmarttv.db.base import Base, TimestampMixin

COMMENT_VISIBLE = "visible"
COMMENT_HIDDEN = "hidden"
COMMENT_PENDING = "pending"


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), index=True
    )
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20), default=COMMENT_VISIBLE, server_default=COMMENT_VISIBLE, index=True
    )

    user = relationship("User", lazy="joined")


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("content_id", "user_id", name="content_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class WatchHistory(Base):
    __tablename__ = "watch_history"
    __table_args__ = (UniqueConstraint("user_id", "content_id", name="user_content"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"), index=True
    )
    episode_id: Mapped[int | None] = mapped_column(
        ForeignKey("episodes.id", ondelete="SET NULL")
    )
    progress_sec: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    watched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
