from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .. import models
from ..schemas.balance import Balance as BalanceSchema, UpdateBalanceSchema 
from ..database import get_db
from ..utils import verify_token, get_current_user
from ..models.user import User
from ..models.balance import Balance

router = APIRouter(prefix="/api/v1", tags=["balances"])

@router.get("/balances/{user_id}", response_model=BalanceSchema)
def read_balance(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this balance")

    db_balance = db.query(Balance).filter(Balance.user_id == user_id).first()
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    
    return db_balance


@router.put("/balances/{user_id}", response_model=BalanceSchema)
def update_balance(
    user_id: int,
    update_data: UpdateBalanceSchema = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this balance")
    
    db_balance = db.query(Balance).filter(Balance.user_id == user_id).with_for_update().first()
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    
    db_balance.amount = update_data.amount
    db.commit()
    db.refresh(db_balance)
    
    return db_balance