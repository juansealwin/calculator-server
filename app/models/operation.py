from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime
from ..database import Base
from .user import User
from datetime import datetime

class Operation(Base):
    __tablename__ = "operations"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    cost = Column(Float)

class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    operation_id = Column(Integer, ForeignKey("operations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    user_balance = Column(Float)
    operation_response = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
