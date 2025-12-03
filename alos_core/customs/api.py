# alos_core/customs/api.py
from fastapi import FastAPI
from pydantic import BaseModel

from .engine import CustomsEngine

app = FastAPI(
    title="ALOS ANI MVP",
    description="Mini MVP of Automated Neural Inspector for customs HS classification",
    version="0.1.0",
)

engine = CustomsEngine()


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    raw_input: str
    normalized: str
    matched_desc: str | None
    confidence: float
    hs_code: str | None
    risk_flag: str | None


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    result = engine.predict_hs(req.text)
    return ClassifyResponse(**result)


# для локального запуска:
# uvicorn alos_core.customs.api:app --reload
