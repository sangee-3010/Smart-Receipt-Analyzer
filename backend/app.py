from fastapi import FastAPI
from backend.routes import receipt, predict, insights
from backend.database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Receipt Analyzer")

@app.get("/")
def root():
    return {"status": "API is alive!"}

app.include_router(receipt.router)
app.include_router(predict.router)
app.include_router(insights.router)
