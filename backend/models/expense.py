from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database.db import Base
from datetime import datetime

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    merchant = Column(String)
    amount = Column(Float)
    category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
