from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from ...infrastructure.config.database import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name: str = Column(String, nullable=False)
    phone_number: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True, index=True)
    address: str = Column(String, nullable=False)
    updated_at: datetime = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    joined_at: datetime = Column(DateTime, default=func.now(), nullable=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    hashed_password: str = Column(String, nullable=False)
    refresh_token: str | None = Column(String, nullable=True)
    role: str = Column(String, nullable=False, default="STAFF")