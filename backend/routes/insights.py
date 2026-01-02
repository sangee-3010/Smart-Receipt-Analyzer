from fastapi import APIRouter
from database.db import SessionLocal
from models.expense import Expense
from sqlalchemy import func

router = APIRouter()

@router.get("/insights")
def insights(user_id: str):
    db = SessionLocal()

    total = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id
    ).scalar() or 0

    top = db.query(
        Expense.category, func.count(Expense.category)
    ).group_by(Expense.category).first()

    return {
        "total_spent": total,
        "top_category": top[0] if top else "None",
        "message": "Spending analysis ready"
    }
