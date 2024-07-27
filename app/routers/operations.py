from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from ..schemas.operation import OperationCreate, OperationOut, RecordOut
from ..models.operation import Operation, Record
from ..models.user import User
from ..database import get_db
from ..utils import verify_token, get_current_user
from typing import List

router = APIRouter()

OPERATION_COSTS = {
    "addition": 0.25,
    "subtraction": 0.25,
    "multiplication": 0.25,
    "division": 0.25,
    "square_root": 0.5,
    "random_string": 1.0
}

@router.post("/operations", response_model=OperationOut)
def create_operation(
    operation: OperationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if operation.type not in OPERATION_COSTS:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    
    operation.cost = OPERATION_COSTS[operation.type]

    # Verify enough money to make the operation
    if not current_user.balances or current_user.balances[0].amount < operation.cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if operation.type == "addition":
        result = operation.amount1 + operation.amount2

    elif operation.type == "subtraction":
        result = operation.amount1 - operation.amount2
    
    elif operation.type == "multiplication":
        result = operation.amount1 * operation.amount2
    
    elif operation.type == "division":
        if operation.amount2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = operation.amount1 / operation.amount2
    
    elif operation.type == "square_root":
        if operation.amount1 < 0:
            raise HTTPException(status_code=400, detail="Cannot take square root of a negative number")
        result = math.sqrt(operation.amount1)
    
    elif operation.type == "random_string":
        response = requests.get("https://www.random.org/strings/?num=1&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error generating random string")
        result = response.text.strip()

    # Update user balance
    current_user.balances[0].amount -= operation.cost
    db.add(current_user)
    
    # Create new Operation and write in db
    new_operation = Operation(type=operation.type, cost=operation.cost)
    db.add(new_operation)
    db.commit()
    db.refresh(new_operation)
    
    # Create new Record and write in db
    record = Record(
        operation_id=new_operation.id,
        user_id=current_user.id,
        # For numeric operations
        amount=result if isinstance(result, (int, float)) else 0,
        user_balance=current_user.balances[0].amount,
        operation_response=str(result)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return new_operation

@router.get("/records", response_model=List[RecordOut])
def read_records(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(Record).filter(Record.user_id == current_user.id).offset(skip).limit(limit).all()

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return records
