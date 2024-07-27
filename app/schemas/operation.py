from pydantic import BaseModel

class OperationBase(BaseModel):
    type: str
    cost: float

class OperationCreate(OperationBase):
    pass

class OperationOut(OperationBase):
    id: int

    class Config:
        from_attributes = True


class RecordOut(BaseModel):
    id: int
    operation_id: int
    user_id: int
    amount: float
    user_balance: float
    operation_response: str

    class Config:
        from_attributes = True
