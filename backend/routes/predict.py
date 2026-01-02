from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.ml.classifier import predict_category

router = APIRouter()

# 1️⃣ Define request schema
class PredictRequest(BaseModel):
    merchant: str
    description: Optional[str] = None

@router.post("/predict-category")
def predict(data: PredictRequest):
    category = predict_category(data.merchant)
    return {"category": category}
