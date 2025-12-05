from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="ALOS Logistics Planner",
    description="MVP service for route & pricing suggestions",
    version="0.1.0",
)


class QuoteRequest(BaseModel):
    origin: str
    destination: str
    goods_type: str
    cargo_value_usd: float
    total_weight_kg: float
    deadline_days: int


class RouteLeg(BaseModel):
    from_location: str = Field(..., description="Origin code or city")
    to_location: str = Field(..., description="Destination code or city")
    mode: str = Field(..., description="air / road / rail / sea")
    carrier: Optional[str] = Field(None, description="Carrier name or code")


class RouteOption(BaseModel):
    option_id: str
    mode: str
    eta_days: int
    base_price: float
    currency: str = "USD"
    risk_score: float = Field(0.0, ge=0.0, le=1.0)
    legs: List[RouteLeg]


@app.post("/routes/quote", response_model=List[RouteOption])
async def create_quote(request: QuoteRequest) -> List[RouteOption]:
    """
    Step 1: Given origin/destination/cargo, return a few route options.

    For now this is a stub (no real carriers), but the API shape is production-like.
    """

    # Option 1: fast / more expensive (air)
    opt1 = RouteOption(
        option_id="opt_air_fast",
        mode="air",
        eta_days=4,
        base_price=18000.0,
        risk_score=0.18,
        legs=[
            RouteLeg(
                from_location="EVN",
                to_location="IST",
                mode="air",
                carrier="TK",
            ),
            RouteLeg(
                from_location="IST",
                to_location="HAM",
                mode="air",
                carrier="TK",
            ),
        ],
    )

    # Option 2: slower / cheaper (multimodal)
    opt2 = RouteOption(
        option_id="opt_multi_saver",
        mode="multimodal",
        eta_days=9,
        base_price=11000.0,
        risk_score=0.25,
        legs=[
            RouteLeg(
                from_location=request.origin,
                to_location="POTI",
                mode="road",
                carrier=None,
            ),
            RouteLeg(
                from_location="POTI",
                to_location=request.destination,
                mode="sea",
                carrier="MAERSK",
            ),
        ],
    )

    return [opt1, opt2]
