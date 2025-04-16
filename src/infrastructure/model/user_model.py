import enum
import sqlalchemy
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from ...infrastructure.config.database import Base

class UserRole(str, enum.Enum):
    STAFF = "STAFF"
    MANAGER = "MANAGER"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    address = Column(String, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    joined_at = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    role = Column(sqlalchemy.Enum(UserRole), nullable=False, default=UserRole.STAFF)
    is_verified = Column(Boolean, nullable=False, default=False)
