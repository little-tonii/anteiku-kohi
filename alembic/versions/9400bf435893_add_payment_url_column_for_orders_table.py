"""add payment_url column for orders table

Revision ID: 9400bf435893
Revises: 60345c715313
Create Date: 2025-04-18 01:07:23.484239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9400bf435893'
down_revision: Union[str, None] = '571e23f3222f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'orders',
        sa.Column('payment_url', sa.Text(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('orders', 'payment_url')
