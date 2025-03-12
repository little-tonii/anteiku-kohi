from datetime import datetime
import enum
import sqlalchemy

from sqlalchemy.orm import relationship

from ...infrastructure.model.user_model import UserModel

from ...infrastructure.model.meal_model import MealModel
from ...infrastructure.model import order_meal_association
from ...infrastructure.config.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, func

class OrderStatus(str, enum.Enum):
    ONQUEUE = "ONQUEUE"
    PROCESSING = "PROCESSING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    
class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"
    
class OrderModel(Base):
    __tablename__ = "orders"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    staff_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    total: int = Column(Integer, nullable=False)
    order_status: str = Column(sqlalchemy.Enum(OrderStatus), default=OrderStatus.ONQUEUE, nullable=False)
    payment_status: str = Column(sqlalchemy.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at: datetime = Column(DateTime, default=func.now(), nullable=False)
    updated_at: datetime = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    meals: MealModel = relationship("MealModel", secondary=order_meal_association, back_populates="orders")