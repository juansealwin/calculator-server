from pydantic import BaseModel

class Balance(BaseModel):
    id: int
    user_id: int
    amount: float

    class Config:
        from_attributes = True

class UpdateBalanceSchema(BaseModel):
    amount: float        
