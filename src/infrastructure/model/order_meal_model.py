from sqlalchemy import Column, ForeignKey, Integer
from ..config.database import Base

class OrderMealModel(Base):
    __tablename__ = "order_meal"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
