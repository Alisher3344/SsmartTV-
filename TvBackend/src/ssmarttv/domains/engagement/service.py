"""Engagement logic: comments, likes, watch history and recommendations."""
from datetime import UTC, datetime

from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.exceptions import NotFoundError, PermissionDeniedError
from ssmarttv.core.pagination import PageParams
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.auth.permissions import COMMENT_MODERATE
from ssmarttv.domains.catalog.models import Content, content_genres
from ssmarttv.domains.engagement.models import (
    COMMENT_VISIBLE,
    Comment,
    Like,
    WatchHistory,
)


async def _ensure_content(db: AsyncSession, content_id: int) -> None:
    if not await db.scalar(select(Content.id).where(Content.id == content_id)):
        raise NotFoundError("Content not found")


def author_name(user: User) -> str:
    if user.full_name:
        return user.full_name
    if user.username:
        return user.username
    phone = user.phone or ""
    return f"{phone[:7]}***{phone[-2:]}" if len(phone) >= 9 else "User"


# --- Comments ------------------------------------------------------------
async def add_comment(
    db: AsyncSession, user_id: int, content_id: int, body: str, parent_id: int | None
) -> Comment:
    await _ensure_content(db, content_id)
    if parent_id is not None:
        parent = await db.get(Comment, parent_id)
        if parent is None or parent.content_id != content_id:
            raise NotFoundError("Parent comment not found")
    comment = Comment(
        content_id=content_id, user_id=user_id, body=body, parent_id=parent_id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment, ["user"])
    return comment


async def list_comments(
    db: AsyncSession, content_id: int, params: PageParams, *, include_hidden: bool = False
) -> tuple[list[Comment], int]:
    stmt = select(Comment).where(Comment.content_id == content_id)
    if not include_hidden:
        stmt = stmt.where(Comment.status == COMMENT_VISIBLE)
    total = await db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    stmt = stmt.order_by(Comment.created_at.desc()).limit(params.limit).offset(params.offset)
    return list((await db.scalars(stmt)).all()), total


async def delete_comment(db: AsyncSession, user: User, comment_id: int) -> None:
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise NotFoundError("Comment not found")
    if comment.user_id != user.id and not user.has_permission(COMMENT_MODERATE):
        raise PermissionDeniedError("Not your comment")
    await db.delete(comment)
    await db.commit()


async def set_comment_status(db: AsyncSession, comment_id: int, status: str) -> Comment:
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise NotFoundError("Comment not found")
    comment.status = status
    await db.commit()
    await db.refresh(comment, ["user"])
    return comment


# --- Likes ---------------------------------------------------------------
async def _like_status(db: AsyncSession, content_id: int, user_id: int | None) -> tuple[int, bool]:
    likes = await db.scalar(
        select(func.count()).select_from(Like).where(Like.content_id == content_id)
    ) or 0
    liked = False
    if user_id is not None:
        liked = bool(
            await db.scalar(
                select(Like.id).where(
                    Like.content_id == content_id, Like.user_id == user_id
                )
            )
        )
    return likes, liked


async def like(db: AsyncSession, user_id: int, content_id: int) -> tuple[int, bool]:
    await _ensure_content(db, content_id)
    stmt = (
        pg_insert(Like)
        .values(content_id=content_id, user_id=user_id)
        .on_conflict_do_nothing(index_elements=["content_id", "user_id"])
    )
    await db.execute(stmt)
    await db.commit()
    return await _like_status(db, content_id, user_id)


async def unlike(db: AsyncSession, user_id: int, content_id: int) -> tuple[int, bool]:
    await db.execute(
        delete(Like).where(Like.content_id == content_id, Like.user_id == user_id)
    )
    await db.commit()
    return await _like_status(db, content_id, user_id)


async def like_status(db: AsyncSession, content_id: int, user_id: int | None) -> tuple[int, bool]:
    return await _like_status(db, content_id, user_id)


# --- Watch history -------------------------------------------------------
async def record_watch(
    db: AsyncSession,
    user_id: int,
    content_id: int,
    episode_id: int | None,
    progress_sec: int,
) -> WatchHistory:
    await _ensure_content(db, content_id)
    now = datetime.now(UTC)
    stmt = (
        pg_insert(WatchHistory)
        .values(
            user_id=user_id,
            content_id=content_id,
            episode_id=episode_id,
            progress_sec=progress_sec,
            watched_at=now,
        )
        .on_conflict_do_update(
            index_elements=["user_id", "content_id"],
            set_={"episode_id": episode_id, "progress_sec": progress_sec, "watched_at": now},
        )
    )
    await db.execute(stmt)
    await db.commit()
    row = await db.scalar(
        select(WatchHistory).where(
            WatchHistory.user_id == user_id, WatchHistory.content_id == content_id
        )
    )
    assert row is not None
    return row


async def list_history(
    db: AsyncSession, user_id: int, params: PageParams
) -> tuple[list[WatchHistory], int]:
    stmt = select(WatchHistory).where(WatchHistory.user_id == user_id)
    total = await db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    stmt = stmt.order_by(WatchHistory.watched_at.desc()).limit(params.limit).offset(params.offset)
    return list((await db.scalars(stmt)).all()), total


# --- Recommendations -----------------------------------------------------
async def recommend(db: AsyncSession, user_id: int, limit: int) -> list[tuple[Content, int]]:
    """Content-based: rank unseen content by shared genres with what the user
    has watched. Falls back to newest content for users with no history."""
    watched = set(
        (await db.scalars(
            select(WatchHistory.content_id).where(WatchHistory.user_id == user_id)
        )).all()
    )

    if watched:
        genre_ids = (await db.scalars(
            select(content_genres.c.genre_id)
            .where(content_genres.c.content_id.in_(watched))
            .distinct()
        )).all()
        if genre_ids:
            # Rank content ids by shared-genre count (no entity in the grouped
            # query — eager joins would break GROUP BY), then load the entities.
            score = func.count(content_genres.c.genre_id).label("score")
            ranked = (
                select(content_genres.c.content_id, score)
                .where(
                    content_genres.c.genre_id.in_(genre_ids),
                    content_genres.c.content_id.notin_(watched),
                )
                .group_by(content_genres.c.content_id)
                .order_by(score.desc(), content_genres.c.content_id)
                .limit(limit)
            )
            rows = (await db.execute(ranked)).all()
            if rows:
                pairs = [(int(r[0]), int(r[1])) for r in rows]
                ids = [cid for cid, _ in pairs]
                contents = (
                    await db.scalars(select(Content).where(Content.id.in_(ids)))
                ).all()
                by_id = {c.id: c for c in contents}
                return [(by_id[cid], sc) for cid, sc in pairs if cid in by_id]

    # Fallback: newest content.
    stmt2 = (
        select(Content)
        .where(Content.id.notin_(watched) if watched else Content.id.is_not(None))
        .order_by(Content.created_at.desc())
        .limit(limit)
    )
    return [(c, 0) for c in (await db.scalars(stmt2)).all()]


def content_title(content: Content) -> str:
    by_lang = {t.lang: t.title for t in content.translations}
    if by_lang.get("uz"):
        return by_lang["uz"]
    if by_lang:
        return next(iter(by_lang.values()))
    return content.slug
