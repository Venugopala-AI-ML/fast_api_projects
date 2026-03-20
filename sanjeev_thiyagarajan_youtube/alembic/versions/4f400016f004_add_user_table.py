"""add user table

Revision ID: 4f400016f004
Revises: 37569a82ff38
Create Date: 2026-03-20 20:29:52.018452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f400016f004'
down_revision: Union[str, Sequence[str], None] = '37569a82ff38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# alembic history
def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('alembic_users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
