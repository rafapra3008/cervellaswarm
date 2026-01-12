# SUB-ROADMAP: What-If Simulator - FASE 1 Backend
> Data: 12 Gennaio 2026 - Sessione 172
> Status: PRONTA PER IMPLEMENTAZIONE

---

## OBIETTIVO

Endpoint funzionante: `POST /api/v1/what-if/simulate`

Input: property_id, date, room_type, price_adjustment
Output: occupancy, revenue, competitor_position, explanation, confidence

---

## FILE DA CREARE (3 nuovi file)

### 1. backend/schemas/what_if.py (~50 righe)

```
Contenuto:
- WhatIfRequest (Pydantic model)
- WhatIfResponse (Pydantic model)
- PriceCurvePoint (per endpoint curva)
```

### 2. backend/services/what_if_calculator.py (~250 righe)

```
Contenuto:
- class WhatIfCalculator
  - __init__(db)
  - calculate_impact() - calcolo principale
  - generate_price_curve() - curva prezzi
  - _get_current_price() - helper DB
  - _get_current_occupancy() - helper DB
  - _get_total_rooms() - helper DB
  - _get_competitor_avg_price() - helper DB
  - _determine_position() - above/match/below
  - _generate_explanation() - template testo
  - _calculate_confidence() - low/medium/high
```

### 3. backend/routers/what_if_api.py (~100 righe)

```
Contenuto:
- router = APIRouter(prefix="/api/v1/what-if")
- POST /simulate - simulazione singola
- GET /price-curve - curva per grafico
```

---

## MODIFICHE A FILE ESISTENTI (2 righe)

### backend/main.py

```python
# AGGIUNTA 1: Import (riga ~10)
from routers import what_if_api

# AGGIUNTA 2: Registrazione (riga ~30)
app.include_router(what_if_api.router, tags=["What-If"])
```

**TOTALE: 2 righe, 1 file**

---

## ORDINE IMPLEMENTAZIONE

```
STEP 1: schemas/what_if.py
        - Definisce contratto API
        - Nessuna dipendenza

STEP 2: services/what_if_calculator.py
        - Business logic
        - Dipende da: database connection

STEP 3: routers/what_if_api.py
        - Endpoint FastAPI
        - Dipende da: schemas, services

STEP 4: main.py (2 righe)
        - Registrazione router
        - Dipende da: router funzionante

STEP 5: Test curl
        - Verifica endpoint risponde
        - Verifica JSON corretto
```

---

## API CONTRACT

### POST /api/v1/what-if/simulate

**Request:**
```json
{
  "property_id": 42,
  "date_target": "2026-01-20",
  "room_type_id": 3,
  "price_adjustment": 0.10
}
```

**Response:**
```json
{
  "current_price": 120.00,
  "new_price": 132.00,
  "predicted_occupancy": 0.75,
  "occupancy_delta": -0.03,
  "predicted_revenue": 9900.00,
  "revenue_delta": 450.00,
  "competitor_position": "match",
  "competitor_avg": 135.00,
  "confidence": "medium",
  "explanation": "Con prezzo 132 (+10%), prevedo occupancy 75% (-3%) ma revenue +450 (+5%). Competitors a 135 - posizione competitiva buona."
}
```

---

## FORMULA ELASTICITY

```python
elasticity = -0.5  # Standard hotel

price_change = (new_price - current_price) / current_price
occupancy_change = elasticity * price_change

# Se prezzo +10% -> occupancy -5%
# Se prezzo -10% -> occupancy +5%
```

---

## CHECKLIST IMPLEMENTAZIONE

```
[ ] 1. Creare schemas/what_if.py
[ ] 2. Creare services/what_if_calculator.py
[ ] 3. Creare routers/what_if_api.py
[ ] 4. Aggiungere 2 righe main.py
[ ] 5. Test curl localhost
[ ] 6. Test curl produzione
```

---

## DOPO FASE 1

- FASE 2: Frontend UI (slider + cards)
- FASE 3: Grafico Chart.js
- FASE 4: AI Explanation avanzata
- FASE 5: Azioni (applica prezzo)
- FASE 6: Ottimizzazioni

---

## TEMPO STIMATO

- Schemas: 10 min
- Service: 30 min
- Router: 15 min
- Main.py: 2 min
- Test: 15 min

**TOTALE FASE 1: ~1 ora**

---

*"Una cosa alla volta, fatta BENE!"*
