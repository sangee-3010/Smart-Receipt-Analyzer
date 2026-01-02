from fastapi import APIRouter
from backend.database.db import SessionLocal
from backend.models.expense import Expense
from backend.ml.classifier import predict_category

router = APIRouter()

@router.post("/upload-receipt")
def upload(data: dict):
    db = SessionLocal()

    category = predict_category(data["merchant"])

    expense = Expense(
        user_id=data["user_id"],
        merchant=data["merchant"],
        amount=data["amount"],
        category=category
    )

    db.add(expense)
    db.commit()
    return {"status": "success"}
