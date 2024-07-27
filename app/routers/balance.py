from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..schemas.balance import Balance as BalanceSchema 
from ..database import get_db
from ..utils import verify_token, get_current_user
from ..models.user import User

router = APIRouter(
    prefix="/balances",
    tags=["balances"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", response_model=BalanceSchema)
def read_balance(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this balance")

    db_balance = db.query(models.Balance).filter(models.Balance.user_id == user_id).first()
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    
    return db_balance
