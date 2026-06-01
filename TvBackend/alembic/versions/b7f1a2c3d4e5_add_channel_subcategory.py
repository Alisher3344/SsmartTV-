"""add channel subcategory and reclassify category as country

Revision ID: b7f1a2c3d4e5
Revises: e28f36fecaa2
Create Date: 2026-06-01 19:00:00.000000

Category becomes the primary grouping = country (ozbekiston/rossiya/belarus),
and the old genre value moves into the new `subcategory` column.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7f1a2c3d4e5'
down_revision: Union[str, None] = 'e28f36fecaa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Channels seeded from the Russian streams (everything else in the initial data
# set is Uzbek). Used to assign the country on existing rows.
_RUSSIAN_SLUGS = ("karusel", "russia24", "russia1")


def upgrade() -> None:
    op.add_column(
        "channels", sa.Column("subcategory", sa.String(length=50), nullable=True)
    )
    op.create_index(
        op.f("ix_channels_subcategory"), "channels", ["subcategory"], unique=False
    )
    # Move the existing genre into subcategory, then set category to the country.
    op.execute("UPDATE channels SET subcategory = category")
    op.execute(
        "UPDATE channels SET category = CASE "
        "WHEN slug IN ('karusel', 'russia24', 'russia1') THEN 'rossiya' "
        "ELSE 'ozbekiston' END"
    )


def downgrade() -> None:
    # Restore the genre back into category, then drop the new column.
    op.execute("UPDATE channels SET category = subcategory WHERE subcategory IS NOT NULL")
    op.drop_index(op.f("ix_channels_subcategory"), table_name="channels")
    op.drop_column("channels", "subcategory")
