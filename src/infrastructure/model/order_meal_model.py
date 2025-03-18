from sqlalchemy import Column, ForeignKey, Integer, Table

from ..config.database import Base

class OrderMealModel(Base):
    __tablename__ = "order_meal"
    
    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    meal_id: int = Column(Integer, ForeignKey("meals.id"), nullable=False)
    order_id: int = Column(Integer, ForeignKey("orders.id"), nullable=False)
    price: int = Column(Integer, nullable=False)
    quantity: int = Column(Integer, nullable=False)