from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserOut
from ..models.user import User
from ..models.balance import Balance
from ..database import get_db
from ..utils import get_password_hash, verify_password, create_access_token
import re

router = APIRouter(prefix="/api/v1", tags=["auth"])

def validate_password(password: str) -> bool:
    if len(password) <= 6:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@router.post("/register", response_model=UserOut)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    if not validate_password(user.password):
        raise HTTPException(
            status_code=400, 
            detail="Password must be more than 6 characters, contain at least one number, one letter, and one special character"
        )

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    initial_balance = Balance(user_id=new_user.id, amount=100.0)
    db.add(initial_balance)
    db.commit()
    db.refresh(initial_balance)
    
    return new_user

@router.post("/login")
def login(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": db_user.username})
    return {
        "accessToken": access_token, 
        "tokenType": "bearer",
        "userData": {
            "id": db_user.id,
            "username": db_user.username,
            "status": db_user.status
        } 
    }