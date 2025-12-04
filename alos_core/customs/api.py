from fastapi import FastAPI
from pydantic import BaseModel
from .engine import CustomsEngine

app = FastAPI(
    title="ALOS - Customs Broker Service",
    description="Microservice for HS code suggestion and customs risk checks",
    version="0.1.0",
)

engine = CustomsEngine()


class ClassifyRequest(BaseModel):
    text: str


@app.post("/classify")
async def classify(req: ClassifyRequest):
    return engine.predict_hs(req.text)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "customs_broker"}
