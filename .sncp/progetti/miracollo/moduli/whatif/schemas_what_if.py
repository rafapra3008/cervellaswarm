"""
What-If Pricing Simulator - Schemas
Modulo: What-If Simulator
Versione: 1.0.0
Data: 12 Gennaio 2026

DESTINAZIONE: backend/schemas/what_if.py
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-12"

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


class WhatIfRequest(BaseModel):
    """Request per simulazione What-If"""
    property_id: int = Field(..., description="ID della property")
    date_target: date = Field(..., description="Data target per simulazione")
    room_type_id: int = Field(..., description="ID del tipo camera")
    price_adjustment: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Variazione prezzo (-1.0 = -100%, 1.0 = +100%)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "property_id": 42,
                "date_target": "2026-01-20",
                "room_type_id": 3,
                "price_adjustment": 0.10
            }
        }


class WhatIfResponse(BaseModel):
    """Response della simulazione What-If"""
    # Prezzi
    current_price: float = Field(..., description="Prezzo corrente")
    new_price: float = Field(..., description="Nuovo prezzo simulato")

    # Occupancy
    current_occupancy: float = Field(..., ge=0, le=1, description="Occupancy corrente")
    predicted_occupancy: float = Field(..., ge=0, le=1, description="Occupancy prevista")
    occupancy_delta: float = Field(..., description="Variazione occupancy")

    # Revenue
    current_revenue: float = Field(..., description="Revenue corrente")
    predicted_revenue: float = Field(..., description="Revenue previsto")
    revenue_delta: float = Field(..., description="Variazione revenue")

    # Competitor
    competitor_position: str = Field(..., description="above, match, below")
    competitor_avg: float = Field(..., description="Prezzo medio competitor")

    # Confidence e Explanation
    confidence: str = Field(..., description="low, medium, high")
    explanation: str = Field(..., description="Spiegazione AI")

    class Config:
        json_schema_extra = {
            "example": {
                "current_price": 120.00,
                "new_price": 132.00,
                "current_occupancy": 0.78,
                "predicted_occupancy": 0.75,
                "occupancy_delta": -0.03,
                "current_revenue": 9360.00,
                "predicted_revenue": 9900.00,
                "revenue_delta": 540.00,
                "competitor_position": "match",
                "competitor_avg": 135.00,
                "confidence": "medium",
                "explanation": "Con prezzo 132 (+10%), prevedo occupancy 75% (-3%) ma revenue +540 (+5%)."
            }
        }


class PriceCurvePoint(BaseModel):
    """Singolo punto della curva price vs occupancy"""
    price: float
    occupancy: float
    revenue: float
    adjustment_percent: float


class PriceCurveResponse(BaseModel):
    """Response per curva prezzi (per grafico)"""
    current_price: float
    points: List[PriceCurvePoint]
    competitor_avg: Optional[float] = None
