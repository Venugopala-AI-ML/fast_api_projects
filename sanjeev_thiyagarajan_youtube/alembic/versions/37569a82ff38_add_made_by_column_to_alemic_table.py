"""add made_by column to alemic table

Revision ID: 37569a82ff38
Revises: 85e0a836065f
Create Date: 2026-03-20 20:21:59.208307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37569a82ff38'
down_revision: Union[str, Sequence[str], None] = '85e0a836065f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# alembic revision -m "add made_by column to alemic table"
# alembic upgrade head ( this is used for applying the migration )
# downgrade -1 ( this is used for rolling back the migration )
# downgrade 85e0a836065f
# alembic revision -m "add user table"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('alembic_posts', sa.Column('made_by', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('alembic_posts', 'made_by')
    pass
