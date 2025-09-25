"""add refresh_token_hash to users

Revision ID: 66ed056b4ef3
Revises: a12905e1928d
Create Date: 2025-09-25 16:03:12.729673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66ed056b4ef3'
down_revision: Union[str, Sequence[str], None] = 'a12905e1928d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('refresh_token_hash', sa.String(length=255), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('users', 'refresh_token_hash')