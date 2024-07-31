from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperationBase(BaseModel):
    pass

class OperationCreate(BaseModel):
    type: str
    amount1: Optional[float] = None
    amount2: Optional[float] = None

class OperationOut(BaseModel):
    id: int
    result: str
    cost: float 

    class Config:
        from_attributes = True

class RecordOut(BaseModel):
    id: int
    operation_id: int
    user_id: int
    amount: float
    user_balance: float
    operation_response: str
    date: datetime

    class Config:
        from_attributes = True
