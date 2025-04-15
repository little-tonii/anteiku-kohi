from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from ...infrastructure.config.database import Base

class MealModel(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    image_url = Column(String, nullable=False)
