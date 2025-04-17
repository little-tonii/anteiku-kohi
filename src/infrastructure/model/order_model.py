import enum
import sqlalchemy

from ...infrastructure.config.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

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

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    order_status = Column(sqlalchemy.Enum(OrderStatus), default=OrderStatus.ONQUEUE, nullable=False)
    payment_status = Column(sqlalchemy.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    payment_url = Column(String, nullable=True)
