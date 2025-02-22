from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Balance(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, default=0.0)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="balance")
