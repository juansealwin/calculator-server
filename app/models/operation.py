from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User

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
    date = Column(String)

    operation = relationship("Operation")
    user = relationship("User")
