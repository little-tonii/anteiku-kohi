from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from ..config.database import Base

class OrderMealModel(Base):
    __tablename__ = "order_meal"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
