"""create posts table

Revision ID: 85e0a836065f
Revises: 
Create Date: 2026-03-20 19:52:21.857634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85e0a836065f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('alembic_posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('alembic_posts')
    op.drop_column('alembic_posts', 'owner_id')
    op.drop_column('alembic_posts', 'created_at')
    op.drop_column('alembic_posts', 'published')
    op.drop_column('alembic_posts', 'content')
    op.drop_column('alembic_posts', 'title')

    pass
