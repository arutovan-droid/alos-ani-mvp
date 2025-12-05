from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from alos_core.customs.engine import CustomsEngine
from alos_core.logistics.api import RouteOption, RouteLeg


app = FastAPI(
    title="ALOS Orchestrator",
    description=(
        "MVP orchestrator that combines route planning (logistics) "
        "and HS classification (customs ANI)."
    ),
    version="0.1.0",
)

# ----- Входные / выходные модели -----


class ShipmentPlanRequest(BaseModel):
    origin: str = Field(..., example="Yerevan, AM")
    destination: str = Field(..., example="Hamburg, DE")
    goods_description: str = Field(..., example="բլուտուզ խոսփաքեր")
    goods_type: str = Field(..., example="electronics")
    cargo_value_usd: float = Field(..., example=120_000)
    total_weight_kg: float = Field(..., example=1500)
    deadline_days: int = Field(..., example=10)


class CustomsDecision(BaseModel):
    hs_code: str
    risk_flag: str
    confidence: float
    normalized: str


class ShipmentPlanResponse(BaseModel):
    selected_route: RouteOption
    customs: CustomsDecision


# ----- Внутренняя логика (упрощённая логистика) -----


def build_route_options(req: ShipmentPlanRequest) -> List[RouteOption]:
    """
    Простая заглушка для логистики.
    В реале здесь будет запрос к отдельному сервису /routes/quote
    или более сложный движок.
    """

    opt_air = RouteOption(
        option_id="opt_air_fast",
        mode="air",
        eta_days=4,
        base_price=18_000.0,
        currency="USD",
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

    opt_multi = RouteOption(
        option_id="opt_multi_saver",
        mode="multimodal",
        eta_days=9,
        base_price=11_000.0,
        currency="USD",
        risk_score=0.25,
        legs=[
            RouteLeg(
                from_location=req.origin,
                to_location="POTI",
                mode="road",
                carrier=None,
            ),
            RouteLeg(
                from_location="POTI",
                to_location=req.destination,
                mode="sea",
                carrier="MAERSK",
            ),
        ],
    )

    return [opt_air, opt_multi]


customs_engine = CustomsEngine()


# ----- Orchestrator endpoints -----


@app.get("/health")
async def health():
    return {"status": "ok", "service": "orchestrator"}


@app.post("/shipments/plan", response_model=ShipmentPlanResponse)
async def plan_shipment(request: ShipmentPlanRequest) -> ShipmentPlanResponse:
    """
    1) Строим несколько маршрутов.
    2) Выбираем самый дешёвый, который укладывается в дедлайн.
    3) Гоним описание товара через ANI и получаем HS + риск.
    """

    # 1. Кандидаты маршрутов
    options = build_route_options(request)

    # 2. Фильтруем по дедлайну
    feasible = [o for o in options if o.eta_days <= request.deadline_days]
    if not feasible:
        feasible = options

    # Берём самый дешёвый среди подходящих
    selected = sorted(feasible, key=lambda o: o.base_price)[0]

    # 3. Таможенная классификация через ANI
    hs_result = customs_engine.predict_hs(request.goods_description)

    customs = CustomsDecision(
        hs_code=hs_result["hs_code"],
        risk_flag=hs_result["risk_flag"],
        confidence=hs_result["confidence"],
        normalized=hs_result["normalized"],
    )

    return ShipmentPlanResponse(selected_route=selected, customs=customs)
