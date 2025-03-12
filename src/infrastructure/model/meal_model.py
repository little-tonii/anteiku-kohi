from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from ...infrastructure.config.database import Base

class MealModel(Base):
    __tablename__ = "meals"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)
    is_available: bool = Column(Boolean, default=True, nullable=False)
    created_at: datetime = Column(DateTime, default=func.now(), nullable=False)
    updated_at: datetime = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)