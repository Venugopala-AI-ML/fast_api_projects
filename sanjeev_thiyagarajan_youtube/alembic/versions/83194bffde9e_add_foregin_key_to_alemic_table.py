"""add foregin-key to alemic table

Revision ID: 83194bffde9e
Revises: 4f400016f004
Create Date: 2026-03-20 20:39:35.788282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83194bffde9e'
down_revision: Union[str, Sequence[str], None] = '4f400016f004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('alembic_posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_alembic_posts_owner_id', 
                          'alembic_posts', 
                          'alembic_users', 
                          ['owner_id'], 
                          ['id'], 
                          ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_alembic_posts_owner_id', 'alembic_posts', type_='foreignkey')
    op.drop_column('alembic_posts', 'owner_id')
    pass
