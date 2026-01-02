from fastapi import APIRouter, Query
from backend.database.db import SessionLocal
from backend.models.expense import Expense
from sqlalchemy import func

router = APIRouter()

@router.get("/insights")
def insights(user_id: str = Query(...)):
    db = SessionLocal()

    # Total spent by this user
    total = db.query(func.sum(Expense.amount))\
        .filter(Expense.user_id == user_id)\
        .scalar() or 0

    # Top category for this user
    top = (
        db.query(
            Expense.category,
            func.count(Expense.category).label("cnt")
        )
        .filter(Expense.user_id == user_id)
        .group_by(Expense.category)
        .order_by(func.count(Expense.category).desc())
        .first()
    )

    db.close()

    return {
        "total_spent": total,
        "top_category": top[0] if top else "None",
        "message": "Spending analysis ready"
    }
