"""channel stream_headers

Revision ID: a3d9f1e64b27
Revises: e7a1c0d52f10
Create Date: 2026-06-02 13:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a3d9f1e64b27'
down_revision: Union[str, None] = 'e7a1c0d52f10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'channels',
        sa.Column(
            'stream_headers',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column('channels', 'stream_headers')
