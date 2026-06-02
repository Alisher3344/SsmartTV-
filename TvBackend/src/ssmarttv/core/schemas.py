"""Shared response schemas."""
from pydantic import BaseModel


class MessageOut(BaseModel):
    detail: str
