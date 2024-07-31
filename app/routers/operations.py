from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from ..schemas.operation import OperationCreate, OperationOut, RecordOut
from ..models.operation import Operation, Record
from ..models.user import User
from ..database import get_db
from ..utils import verify_token, get_current_user
from typing import List
import math
import requests
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["operations"])

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
    
    operation_cost = OPERATION_COSTS[operation.type]

    # Verify enough money to make the operation
    if not current_user.balance or current_user.balance.amount < operation_cost:
        raise HTTPException(status_code=402, detail="Insufficient balance")

    if operation.type == "addition":
        if operation.amount1 is None or operation.amount2 is None:
            raise HTTPException(status_code=400, detail="amount1 and amount2 are required for addition")
        
        result = operation.amount1 + operation.amount2

    elif operation.type == "subtraction":
        if operation.amount1 is None or operation.amount2 is None:
            raise HTTPException(status_code=400, detail="amount1 and amount2 are required for subtraction")
        
        result = operation.amount1 - operation.amount2
    
    elif operation.type == "multiplication":
        if operation.amount1 is None or operation.amount2 is None:
            raise HTTPException(status_code=400, detail="amount1 and amount2 are required for multiplication")

        result = operation.amount1 * operation.amount2
    
    elif operation.type == "division":
        if operation.amount1 is None or operation.amount2 is None:
            raise HTTPException(status_code=400, detail="amount1 and amount2 are required for division")

        if operation.amount2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")

        result = operation.amount1 / operation.amount2
    
    elif operation.type == "square_root":
        if operation.amount1 is None:
            raise HTTPException(status_code=400, detail="amount1 is required for square_root")
        
        if operation.amount1 < 0:
            raise HTTPException(status_code=400, detail="Cannot take square root of a negative number")
        
        result = math.sqrt(operation.amount1)
    
    elif operation.type == "random_string":
        response = requests.get("https://www.random.org/strings/?num=1&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new")
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error generating random string")
        
        result = response.text.strip()

    # Update user balance
    current_user.balance.amount -= operation_cost
    db.add(current_user)
    
    # Create new Operation and write in db
    new_operation = Operation(type=operation.type, cost=operation_cost)
    db.add(new_operation)
    db.commit()
    db.refresh(new_operation)
    
    # Create new Record and write in db
    record = Record(
        operation_id=new_operation.id,
        user_id=current_user.id,
        # For numeric operations
        amount=result if isinstance(result, (int, float)) else 0,
        user_balance=current_user.balance.amount,
        operation_response=str(result),
        date=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {
        "id": new_operation.id,
        "cost": operation_cost,
        "result": str(result)
    }

@router.get("/records", response_model=List[RecordOut])
def read_records(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(Record).filter(Record.user_id == current_user.id, Record.is_deleted == False).offset(skip).limit(limit).all()

    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    return records


@router.delete("/records/{record_id}")
def delete_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(models.Record).filter(Record.id == record_id, Record.user_id == current_user.id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    record.is_deleted = True
    record.deleted_at = func.now()
    db.commit()

    return {"message": "Record soft-deleted successfully"}