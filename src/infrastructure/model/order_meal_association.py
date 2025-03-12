from sqlalchemy import Column, ForeignKey, Integer, Table

from ...infrastructure.config.database import Base


order_meal_association = Table(
    "order_meal_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("meal_id", Integer, ForeignKey("meals.id"), primary_key=True)
)