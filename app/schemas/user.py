from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    status: bool
    #balances: List["Balance"][0] = []

    class Config:
        from_attributes = True
