from fastapi import APIRouter
from pydantic import BaseModel
from backend.database.db import SessionLocal
from backend.models.expense import Expense

router = APIRouter()

# 1️⃣ Define request body schema
class ReceiptUpload(BaseModel):
    user_id: str
    merchant: str
    amount: float

@router.post("/upload-receipt")
def upload(data: ReceiptUpload):
    db = SessionLocal()

    expense = Expense(
        user_id=data.user_id,
        merchant=data.merchant,
        amount=data.amount,
        category="Other"   # dummy for now
    )

    db.add(expense)
    db.commit()
    db.close()

    return {"status": "success"}
