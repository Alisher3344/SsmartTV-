"""carousel slides

Revision ID: e7a1c0d52f10
Revises: 4beed554afb0
Create Date: 2026-06-02 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7a1c0d52f10'
down_revision: Union[str, None] = '4beed554afb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'carousel_slides',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('image', sa.Text(), nullable=False),
        sa.Column('title_uz', sa.String(length=200), nullable=True),
        sa.Column('title_ru', sa.String(length=200), nullable=True),
        sa.Column('link_url', sa.Text(), nullable=True),
        sa.Column('sort_order', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_carousel_slides')),
    )
    op.create_index(op.f('ix_carousel_slides_sort_order'), 'carousel_slides', ['sort_order'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_carousel_slides_sort_order'), table_name='carousel_slides')
    op.drop_table('carousel_slides')
