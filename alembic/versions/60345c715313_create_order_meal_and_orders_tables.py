"""Create order_meal and orders tables

Revision ID: 60345c715313
Revises: 571e23f3222f
Create Date: 2025-04-16 15:57:06.168801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '60345c715313'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('orders',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('staff_id', sa.Integer(), nullable=True),
        sa.Column('order_status', sa.Enum('ONQUEUE', 'PROCESSING', 'READY', 'DELIVERED', 'CANCELLED', name='orderstatus'), nullable=False, server_default='ONQUEUE'),
        sa.Column('payment_status', sa.Enum('PENDING', 'PAID', 'REFUNDED', name='paymentstatus'), nullable=False, server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()),
        sa.ForeignKeyConstraint(['staff_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_meal',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('meal_id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('order_meal')
    op.drop_table('orders')
