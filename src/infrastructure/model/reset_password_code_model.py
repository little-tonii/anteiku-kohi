from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from ..config.database import Base


class ResetPasswordCodeModel(Base):
    __tablename__ = 'reset_password_code'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
