from fastapi import FastAPI
from routes import receipt, predict, insights
from database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Receipt Analyzer")

app.include_router(receipt.router)
app.include_router(predict.router)
app.include_router(insights.router)
