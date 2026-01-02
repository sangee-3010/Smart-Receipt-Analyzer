from fastapi import APIRouter
from backend.ml.classifier import predict_category

router = APIRouter()

@router.post("/predict-category")
def predict(data: dict):
    category = predict_category(data["merchant"])
    return {"category": category}
