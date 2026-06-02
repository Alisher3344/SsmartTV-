"""Limit/offset pagination helpers shared by list endpoints."""
from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class PageParams(BaseModel):
    limit: int = 20
    offset: int = 0


def page_params(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PageParams:
    """FastAPI dependency yielding validated pagination parameters."""
    return PageParams(limit=limit, offset=offset)


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int

    @classmethod
    def create(cls, items: list[T], total: int, params: PageParams) -> "Page[T]":
        return cls(items=items, total=total, limit=params.limit, offset=params.offset)
