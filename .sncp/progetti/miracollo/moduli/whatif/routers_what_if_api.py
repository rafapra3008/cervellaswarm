"""
What-If Pricing Simulator - API Router
Modulo: What-If Simulator
Versione: 1.0.0
Data: 12 Gennaio 2026

DESTINAZIONE: backend/routers/what_if_api.py

Endpoints:
- POST /api/v1/what-if/simulate - Simulazione singola
- GET /api/v1/what-if/price-curve - Curva per grafico
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-12"

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from typing import Optional

# Import interni (adattare ai path reali)
from services.what_if_calculator import WhatIfCalculator
from schemas.what_if import (
    WhatIfRequest,
    WhatIfResponse,
    PriceCurveResponse
)
from database import get_db

# Router con prefisso /api/v1/what-if
router = APIRouter(
    prefix="/api/v1/what-if",
    tags=["What-If Simulator"]
)


@router.post("/simulate", response_model=WhatIfResponse)
async def simulate_price_impact(
    request: WhatIfRequest,
    db=Depends(get_db)
):
    """
    Simula l'impatto di un cambio prezzo.

    **Input:**
    - property_id: ID della property
    - date_target: Data target (YYYY-MM-DD)
    - room_type_id: ID tipo camera
    - price_adjustment: Variazione prezzo (-1.0 a +1.0, es. 0.10 = +10%)

    **Output:**
    - Prezzi (corrente e nuovo)
    - Occupancy (corrente, prevista, delta)
    - Revenue (corrente, previsto, delta)
    - Posizione competitor (above/match/below)
    - Confidence (low/medium/high)
    - Spiegazione AI

    **Esempio:**
    ```json
    {
        "property_id": 42,
        "date_target": "2026-01-20",
        "room_type_id": 3,
        "price_adjustment": 0.10
    }
    ```
    """
    calculator = WhatIfCalculator(db)

    try:
        result = calculator.calculate_impact(
            property_id=request.property_id,
            date_target=request.date_target,
            room_type_id=request.room_type_id,
            price_adjustment=request.price_adjustment
        )
        return WhatIfResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore interno simulazione: {str(e)}"
        )


@router.get("/price-curve", response_model=PriceCurveResponse)
async def get_price_curve(
    property_id: int = Query(..., description="ID della property"),
    date_target: date = Query(..., description="Data target"),
    room_type_id: int = Query(..., description="ID tipo camera"),
    min_adjustment: Optional[float] = Query(-0.30, description="Min adjustment (-30%)"),
    max_adjustment: Optional[float] = Query(0.50, description="Max adjustment (+50%)"),
    step: Optional[float] = Query(0.05, description="Step (5%)"),
    db=Depends(get_db)
):
    """
    Genera curva price vs occupancy per grafico.

    Ritorna una lista di punti con prezzo, occupancy e revenue
    per ogni livello di adjustment nel range specificato.

    **Uso tipico:** Alimentare grafico Chart.js nel frontend.

    **Parametri:**
    - property_id: ID property
    - date_target: Data target
    - room_type_id: Tipo camera
    - min_adjustment: Variazione minima (default -30%)
    - max_adjustment: Variazione massima (default +50%)
    - step: Incremento tra punti (default 5%)

    **Response:**
    ```json
    {
        "current_price": 120.0,
        "competitor_avg": 135.0,
        "points": [
            {"price": 84.0, "occupancy": 0.91, "revenue": 6552.0, "adjustment_percent": -30.0},
            {"price": 90.0, "occupancy": 0.88, "revenue": 6840.0, "adjustment_percent": -25.0},
            ...
        ]
    }
    ```
    """
    calculator = WhatIfCalculator(db)

    try:
        result = calculator.generate_price_curve(
            property_id=property_id,
            date_target=date_target,
            room_type_id=room_type_id,
            min_adjustment=min_adjustment,
            max_adjustment=max_adjustment,
            step=step
        )
        return PriceCurveResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore generazione curva: {str(e)}"
        )


@router.get("/health")
async def what_if_health():
    """
    Health check per il modulo What-If.

    Utile per verificare che il modulo sia caricato correttamente.
    """
    return {
        "status": "healthy",
        "module": "what-if-simulator",
        "version": __version__,
        "endpoints": [
            "POST /simulate",
            "GET /price-curve"
        ]
    }
