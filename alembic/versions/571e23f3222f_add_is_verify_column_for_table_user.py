"""add is_verify column for table user

Revision ID: 571e23f3222f
Revises:
Create Date: 2025-04-16 08:40:26.389372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '571e23f3222f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'is_verified',
            sa.Boolean(),
            nullable=False,
            default=False,
            server_default='false'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'users',
        'is_verified'
    )
