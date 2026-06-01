"""Declarative base.

Models import ``Base`` from here. To register every model on
``Base.metadata`` for Alembic autogenerate, import the model modules in
``alembic/env.py`` (and anywhere else metadata must be complete) — not here,
to avoid circular imports.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
