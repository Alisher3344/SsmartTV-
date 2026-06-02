"""Engagement endpoints: comments, likes, watch history, recommendations."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ssmarttv.core.pagination import Page, PageParams, page_params
from ssmarttv.core.schemas import MessageOut
from ssmarttv.db.session import get_db
from ssmarttv.domains.auth.dependencies import (
    get_current_user,
    get_optional_user,
    require_permission,
)
from ssmarttv.domains.auth.models import User
from ssmarttv.domains.auth.permissions import COMMENT_MODERATE
from ssmarttv.domains.engagement import service
from ssmarttv.domains.engagement.models import Comment
from ssmarttv.domains.engagement.schemas import (
    CommentIn,
    CommentModerateIn,
    CommentOut,
    LikeStatusOut,
    RecommendationOut,
    WatchIn,
    WatchOut,
)

router = APIRouter(tags=["engagement"])


def _comment_out(c: Comment) -> CommentOut:
    return CommentOut(
        id=c.id,
        content_id=c.content_id,
        user_id=c.user_id,
        author_name=service.author_name(c.user),
        parent_id=c.parent_id,
        body=c.body,
        status=c.status,
        created_at=c.created_at,
    )


# --- Comments ------------------------------------------------------------
@router.post("/content/{content_id}/comments", response_model=CommentOut, status_code=201)
async def add_comment(
    content_id: int,
    data: CommentIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CommentOut:
    c = await service.add_comment(db, user.id, content_id, data.body, data.parent_id)
    return _comment_out(c)


@router.get("/content/{content_id}/comments", response_model=Page[CommentOut])
async def list_comments(
    content_id: int,
    params: PageParams = Depends(page_params),
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> Page[CommentOut]:
    include_hidden = user is not None and user.has_permission(COMMENT_MODERATE)
    items, total = await service.list_comments(
        db, content_id, params, include_hidden=include_hidden
    )
    return Page.create([_comment_out(c) for c in items], total, params)


@router.delete("/comments/{comment_id}", response_model=MessageOut)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageOut:
    await service.delete_comment(db, user, comment_id)
    return MessageOut(detail="Comment deleted")


@router.patch("/comments/{comment_id}/moderate", response_model=CommentOut)
async def moderate_comment(
    comment_id: int,
    data: CommentModerateIn,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_permission(COMMENT_MODERATE)),
) -> CommentOut:
    return _comment_out(await service.set_comment_status(db, comment_id, data.status))


# --- Likes ---------------------------------------------------------------
@router.post("/content/{content_id}/like", response_model=LikeStatusOut)
async def like(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LikeStatusOut:
    likes, liked = await service.like(db, user.id, content_id)
    return LikeStatusOut(content_id=content_id, likes=likes, liked=liked)


@router.delete("/content/{content_id}/like", response_model=LikeStatusOut)
async def unlike(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LikeStatusOut:
    likes, liked = await service.unlike(db, user.id, content_id)
    return LikeStatusOut(content_id=content_id, likes=likes, liked=liked)


@router.get("/content/{content_id}/likes", response_model=LikeStatusOut)
async def likes(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> LikeStatusOut:
    likes, liked = await service.like_status(db, content_id, user.id if user else None)
    return LikeStatusOut(content_id=content_id, likes=likes, liked=liked)


# --- Watch history & recommendations -------------------------------------
@router.post("/me/watch", response_model=WatchOut, status_code=201)
async def record_watch(
    data: WatchIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> WatchOut:
    w = await service.record_watch(
        db, user.id, data.content_id, data.episode_id, data.progress_sec
    )
    return WatchOut(
        content_id=w.content_id,
        episode_id=w.episode_id,
        progress_sec=w.progress_sec,
        watched_at=w.watched_at,
    )


@router.get("/me/history", response_model=Page[WatchOut])
async def history(
    params: PageParams = Depends(page_params),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Page[WatchOut]:
    items, total = await service.list_history(db, user.id, params)
    out = [
        WatchOut(
            content_id=w.content_id,
            episode_id=w.episode_id,
            progress_sec=w.progress_sec,
            watched_at=w.watched_at,
        )
        for w in items
    ]
    return Page.create(out, total, params)


@router.get("/me/recommendations", response_model=list[RecommendationOut])
async def recommendations(
    limit: int = Query(default=12, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[RecommendationOut]:
    rows = await service.recommend(db, user.id, limit)
    return [
        RecommendationOut(
            content_id=c.id,
            slug=c.slug,
            type=c.type,
            title=service.content_title(c),
            poster=c.poster,
            access_level=c.access_level,
            score=score,
        )
        for c, score in rows
    ]
