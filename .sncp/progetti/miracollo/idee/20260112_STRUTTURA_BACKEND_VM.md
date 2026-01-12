# STRUTTURA BACKEND MIRACOLLO - VM
> **Data**: 12 Gennaio 2026
> **Ricercatrice**: Cervella Researcher
> **Obiettivo**: Mappare struttura backend per inserimento What-If Simulator

---

## EXECUTIVE SUMMARY

**VM**: miracollo-cervella (34.27.179.164)
**Path Backend**: `/app/miracollo/backend/`
**Status**: Backend funzionante, pattern chiari identificati

### TL;DR

```
STRUTTURA ESISTENTE:
- 6 router principali (revenue, pricing, properties)
- Pattern: router → service → database
- Pydantic models per validazione
- Prefissi API: /api/revenue, /api/pricing

DOVE INSERIRE WHAT-IF:
- Nuovo router: routers/what_if_api.py
- Nuovo service: services/what_if_calculator.py
- Plug-in in main.py: 2 righe
- NO modifiche a codice esistente
```

---

## 1. STRUTTURA CARTELLE BACKEND

```
/app/miracollo/backend/
│
├── main.py                           # Entry point (registrazione router)
├── requirements.txt                  # Dipendenze Python
│
├── routers/                          # API Endpoints (FastAPI)
│   ├── __init__.py
│   ├── revenue_bucchi.py             # 205 righe - GET /bucchi, /occupancy-forecast
│   ├── revenue_suggestions.py        # 341 righe - GET /suggestions, POST /{id}/action
│   ├── revenue_research.py           # 234 righe - GET /research, /events
│   ├── pricing_tracking.py           # 587 righe - GET /history, /ai-health
│   ├── properties.py                 # Gestione properties
│   ├── notifications_api.py          # Notifiche
│   └── ml_api.py                     # ML endpoints
│
├── services/                         # Business Logic
│   ├── bucchi_engine.py              # 479 righe - Calcola bucchi revenue
│   ├── suggerimenti_engine.py        # 404 righe - Genera suggerimenti AI
│   ├── suggerimenti_actions.py       # 489 righe - ESEGUE azioni (modifica prezzi)
│   ├── pricing_tracking_service.py   # 587 righe - Traccia modifiche prezzi
│   ├── pricing_performance_scheduler.py  # 209 righe - Valuta performance
│   ├── metrics_calculator.py         # Calcola metriche revenue
│   ├── notification_worker.py        # Worker notifiche
│   └── research_orchestrator.py      # Orchestrazione ricerca eventi
│
├── ml/                               # Machine Learning
│   ├── model_trainer.py              # 733 righe - Training modelli ML
│   ├── ml_scheduler.py               # 687 righe - Scheduler training
│   ├── confidence_scorer.py          # 673 righe - Confidence score
│   ├── data_preparation.py           # 495 righe - Dataset prep
│   └── feature_engineering.py        # 496 righe - Feature extraction
│
├── models/                           # Database Models (SQLAlchemy)
│   ├── property.py
│   ├── pricing.py
│   ├── suggestion.py
│   └── ...
│
├── schemas/                          # Pydantic Schemas (validazione)
│   ├── revenue.py
│   ├── pricing.py
│   └── ...
│
├── database/                         # Database
│   ├── miracollo.db                  # SQLite produzione (SACRO!)
│   └── connection.py                 # DB connection logic
│
├── migrations/                       # Alembic Migrations
│   └── versions/
│       ├── 010_autopilot.sql
│       ├── 016_suggestion_feedback.sql
│       ├── 026_revenue_targets.sql
│       ├── 027_revenue_suggestions.sql
│       ├── 031_pricing_tracking.sql
│       └── ...
│
├── tests/                            # Test Suite
│   ├── test_revenue_intelligence.py  # 200 righe - 30% coverage
│   └── ...
│
└── scripts/                          # Utility scripts
    ├── backup-prod-db.sh
    ├── reset-lab-db.sh
    └── seed_lab_data.py
```

---

## 2. FILE PRICING/REVENUE ESISTENTI

### 2.1 Router (API Layer)

| File | Righe | Prefisso | Endpoints | Status |
|------|-------|----------|-----------|--------|
| **revenue_bucchi.py** | 205 | `/api/revenue` | `GET /bucchi`<br>`GET /occupancy-forecast` | ✅ Funziona |
| **revenue_suggestions.py** | 341 | `/api/revenue` | `GET /suggestions`<br>`POST /suggestions/{id}/action`<br>`GET /suggestions/{id}/feedback` | ✅ Funziona |
| **revenue_research.py** | 234 | `/api/revenue` | `GET /research`<br>`GET /research/status`<br>`GET /events`<br>`POST /events` | ✅ Funziona |
| **pricing_tracking.py** | 587 | `/api/pricing` | `GET /history`<br>`POST /history`<br>`GET /suggestions/{id}/performance`<br>`GET /ai-health` | ✅ Funziona |

### 2.2 Services (Business Logic Layer)

| File | Righe | Responsabilità | Dipendenze |
|------|-------|----------------|------------|
| **bucchi_engine.py** | 479 | Identifica periodi sotto target revenue | `database`, `datetime` |
| **suggerimenti_engine.py** | 404 | Genera suggerimenti AI da bucchi | `bucchi_engine`, `ml/confidence_scorer` |
| **suggerimenti_actions.py** | 489 | **ESEGUE azioni** (modifica daily_rates) | `database`, `suggerimenti_engine` |
| **pricing_tracking_service.py** | 587 | Traccia modifiche prezzi | `database` |
| **pricing_performance_scheduler.py** | 209 | Valuta performance suggerimenti | `database`, `scheduler` |

### 2.3 ML Layer

| File | Righe | Responsabilità |
|------|-------|----------------|
| **model_trainer.py** | 733 | Addestra modelli ML pricing |
| **ml_scheduler.py** | 687 | Scheduler automatico training |
| **confidence_scorer.py** | 673 | Calcola confidence score suggerimenti |
| **data_preparation.py** | 495 | Prepara dataset per training |
| **feature_engineering.py** | 496 | Estrazione features |

---

## 3. PATTERN USATI

### 3.1 Pattern Architetturale

```
REQUEST
  ↓
ROUTER (FastAPI endpoint)
  ↓
SERVICE (Business logic)
  ↓
DATABASE (SQLAlchemy models)
  ↓
RESPONSE (Pydantic schema)
```

### 3.2 Esempio Router (revenue_bucchi.py)

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services.bucchi_engine import BucchiEngine
from schemas.revenue import BucchiResponse
from database import get_db

router = APIRouter(prefix="/api/revenue", tags=["Revenue"])

@router.get("/bucchi", response_model=List[BucchiResponse])
async def get_bucchi(
    hotel_code: str,
    finestra: str,
    db = Depends(get_db)
):
    """Endpoint per ottenere bucchi revenue"""
    engine = BucchiEngine(db)
    bucchi = engine.trova_bucchi(hotel_code, finestra)
    return bucchi

@router.get("/occupancy-forecast")
async def get_occupancy_forecast(
    hotel_code: str,
    date: str,
    db = Depends(get_db)
):
    """Endpoint per forecast occupancy"""
    engine = BucchiEngine(db)
    forecast = engine.calcola_occupancy_prevista(hotel_code, date)
    return forecast
```

**Pattern identificato:**
1. Router definisce endpoint
2. Dependency injection per DB (Depends(get_db))
3. Chiama service per logica
4. Ritorna response validata con Pydantic

### 3.3 Esempio Service (bucchi_engine.py)

```python
class BucchiEngine:
    def __init__(self, db):
        self.db = db

    def trova_bucchi(self, hotel_code: str, finestra: str):
        """Logica per trovare bucchi"""
        # 1. Calcola target
        target = self.calcola_target(hotel_code)

        # 2. Calcola occupancy prevista
        occupancy = self.calcola_occupancy_prevista(hotel_code, finestra)

        # 3. Identifica periodi sotto target
        bucchi = self._identifica_bucchi(target, occupancy)

        return bucchi

    def calcola_target(self, hotel_code: str):
        """Calcola target revenue"""
        # Query database per dati storici
        # Algoritmo calcolo target
        pass

    def calcola_occupancy_prevista(self, hotel_code: str, finestra: str):
        """Calcola occupancy forecast"""
        # Query prenotazioni
        # Algoritmo forecast
        pass
```

**Pattern identificato:**
1. Service class con constructor injection DB
2. Metodi pubblici (interfaccia)
3. Metodi privati (_nome) per logica interna
4. Separazione calcoli: target, forecast, identificazione

### 3.4 Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BucchiResponse(BaseModel):
    id: str
    hotel_code: str
    date_target: date
    occupancy_prevista: float = Field(ge=0, le=1)
    target_revenue: float
    gap_revenue: float
    confidence: str  # low, medium, high

    class Config:
        from_attributes = True  # Per SQLAlchemy models
```

**Pattern identificato:**
1. Pydantic BaseModel per validazione
2. Field() per validazioni avanzate (ge=0, le=1)
3. Config per integrazione SQLAlchemy
4. Type hints chiari

### 3.5 Error Handling

```python
from fastapi import HTTPException

try:
    result = engine.trova_bucchi(hotel_code, finestra)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Nessun bucco trovato per {hotel_code}"
        )
    return result
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail="Internal error")
```

**Pattern identificato:**
1. HTTPException per errori API
2. Status code appropriati (404, 400, 500)
3. Detail message chiaro
4. Try-except wrapping

---

## 4. REGISTRAZIONE ROUTER IN MAIN.PY

```python
# main.py

from fastapi import FastAPI
from routers import revenue_bucchi, revenue_suggestions, revenue_research, pricing_tracking

app = FastAPI(
    title="Miracollo API",
    version="1.7.0"
)

# Registrazione router
app.include_router(revenue_bucchi.router, tags=["Revenue"])
app.include_router(revenue_suggestions.router, tags=["Revenue"])
app.include_router(revenue_research.router, tags=["Revenue"])
app.include_router(pricing_tracking.router, tags=["Pricing"])

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.7.0"
    }
```

**Pattern identificato:**
1. Import router
2. app.include_router() per registrazione
3. Tags per organizzazione docs
4. Health endpoint sempre presente

---

## 5. DATABASE SCHEMA (Tabelle Revenue)

```sql
-- suggestion_feedback
CREATE TABLE suggestion_feedback (
    id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    suggestion_id TEXT,
    bucco_id TEXT,
    tipo TEXT,
    azione TEXT,  -- accept, reject, snooze
    motivo_reject TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- suggestion_applications
CREATE TABLE suggestion_applications (
    id INTEGER PRIMARY KEY,
    suggestion_id TEXT,
    hotel_id INTEGER REFERENCES hotels(id),
    suggestion_type TEXT,
    suggestion_action TEXT,
    bucco_id TEXT,
    before_snapshot JSON,
    changes_applied JSON,
    pricing_version_id INTEGER,
    status TEXT,  -- active, completed, rolled_back
    monitoring_start DATE,
    evaluation_period_days INTEGER
);

-- pricing_history
CREATE TABLE pricing_history (
    id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    date DATE,
    room_type_id INTEGER,
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2),
    change_reason TEXT,
    changed_by TEXT,  -- system, user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- pricing_versions
CREATE TABLE pricing_versions (
    version_id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    date_range_start DATE,
    date_range_end DATE,
    previous_prices JSON,
    new_prices JSON,
    is_rollback BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. PIANO INSERIMENTO WHAT-IF

### 6.1 File da Creare

```
backend/routers/what_if_api.py        # Nuovo file (250 righe stimato)
backend/services/what_if_calculator.py # Nuovo file (350 righe stimato)
backend/schemas/what_if.py             # Nuovo file (100 righe stimato)
```

### 6.2 Modifiche Minime a File Esistenti

**File**: `backend/main.py`
**Righe da aggiungere**: 2

```python
# AGGIUNTA 1: Import
from routers import what_if_api

# AGGIUNTA 2: Registrazione
app.include_router(what_if_api.router, tags=["What-If"])
```

**TOTALE MODIFICHE**: 2 righe in 1 file esistente

### 6.3 Struttura Nuovo Router

```python
# backend/routers/what_if_api.py

from fastapi import APIRouter, Depends, HTTPException
from services.what_if_calculator import WhatIfCalculator
from schemas.what_if import WhatIfRequest, WhatIfResponse
from database import get_db

router = APIRouter(prefix="/api/v1/what-if", tags=["What-If"])

@router.post("/simulate", response_model=WhatIfResponse)
async def simulate_price_impact(
    request: WhatIfRequest,
    db = Depends(get_db)
):
    """
    Simula impatto di un cambio prezzo

    Input:
    - property_id: int
    - date_target: date
    - room_type_id: int
    - price_adjustment: float (-1.0 a +1.0, es. 0.10 = +10%)

    Output:
    - occupancy prevista
    - revenue stimato
    - competitor position
    - explanation AI
    - confidence score
    """
    calculator = WhatIfCalculator(db)

    try:
        result = calculator.calculate_impact(
            property_id=request.property_id,
            date_target=request.date_target,
            room_type_id=request.room_type_id,
            price_adjustment=request.price_adjustment
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Simulation error")

@router.get("/price-curve")
async def get_price_curve(
    property_id: int,
    date_target: str,
    room_type_id: int,
    db = Depends(get_db)
):
    """
    Genera curve price vs occupancy per grafico

    Output: array di punti [{price, occupancy, revenue}]
    """
    calculator = WhatIfCalculator(db)
    curve = calculator.generate_price_curve(property_id, date_target, room_type_id)
    return curve
```

### 6.4 Struttura Service

```python
# backend/services/what_if_calculator.py

class WhatIfCalculator:
    def __init__(self, db):
        self.db = db
        self.elasticity = -0.5  # Standard hotel elasticity

    def calculate_impact(self, property_id, date_target, room_type_id, price_adjustment):
        """Calcola impatto cambio prezzo"""

        # 1. Ottieni dati attuali
        current_price = self._get_current_price(property_id, date_target, room_type_id)
        current_occupancy = self._get_current_occupancy(property_id, date_target)

        # 2. Calcola nuovo prezzo
        new_price = current_price * (1 + price_adjustment)

        # 3. Calcola impatto occupancy (elasticity-based)
        occupancy_change = self.elasticity * price_adjustment
        new_occupancy = max(0.0, min(1.0, current_occupancy * (1 + occupancy_change)))

        # 4. Calcola revenue
        rooms = self._get_total_rooms(property_id, room_type_id)
        current_revenue = current_price * current_occupancy * rooms
        new_revenue = new_price * new_occupancy * rooms

        # 5. Competitor position
        competitor_avg = self._get_competitor_avg_price(property_id, date_target)
        position = self._determine_position(new_price, competitor_avg)

        # 6. Generate explanation
        explanation = self._generate_explanation(
            current_price, new_price,
            current_occupancy, new_occupancy,
            current_revenue, new_revenue,
            position, competitor_avg
        )

        # 7. Confidence score
        confidence = self._calculate_confidence(date_target, current_occupancy)

        return {
            "current_price": current_price,
            "new_price": new_price,
            "predicted_occupancy": new_occupancy,
            "occupancy_delta": new_occupancy - current_occupancy,
            "predicted_revenue": new_revenue,
            "revenue_delta": new_revenue - current_revenue,
            "competitor_position": position,
            "competitor_avg": competitor_avg,
            "confidence": confidence,
            "explanation": explanation
        }

    def generate_price_curve(self, property_id, date_target, room_type_id):
        """Genera curve price vs occupancy"""
        current_price = self._get_current_price(property_id, date_target, room_type_id)

        curve = []
        for adjustment in range(-30, 51, 5):  # -30% a +50%, step 5%
            adj_decimal = adjustment / 100.0
            result = self.calculate_impact(property_id, date_target, room_type_id, adj_decimal)
            curve.append({
                "price": result["new_price"],
                "occupancy": result["predicted_occupancy"],
                "revenue": result["predicted_revenue"]
            })

        return curve

    # Helper methods privati
    def _get_current_price(self, property_id, date_target, room_type_id):
        """Query DB per prezzo corrente"""
        pass

    def _get_current_occupancy(self, property_id, date_target):
        """Query DB per occupancy corrente/prevista"""
        pass

    def _get_total_rooms(self, property_id, room_type_id):
        """Query DB per numero camere"""
        pass

    def _get_competitor_avg_price(self, property_id, date_target):
        """Query DB competitor prices (se disponibile)"""
        pass

    def _determine_position(self, our_price, competitor_avg):
        """above, match, below"""
        if our_price > competitor_avg * 1.05:
            return "above"
        elif our_price < competitor_avg * 0.95:
            return "below"
        else:
            return "match"

    def _generate_explanation(self, current_price, new_price, current_occ, new_occ, current_rev, new_rev, position, comp_avg):
        """Template explanation"""
        price_change_pct = ((new_price - current_price) / current_price) * 100
        occ_change_pct = ((new_occ - current_occ) / current_occ) * 100 if current_occ > 0 else 0
        rev_change_pct = ((new_revenue - current_revenue) / current_revenue) * 100 if current_revenue > 0 else 0

        return (
            f"Con prezzo €{new_price:.2f} ({price_change_pct:+.1f}%), "
            f"prevedo occupancy {new_occ*100:.1f}% ({occ_change_pct:+.1f}%) "
            f"e revenue €{new_revenue:.0f} ({rev_change_pct:+.1f}%). "
            f"Competitor a €{comp_avg:.2f} - posizione {position}."
        )

    def _calculate_confidence(self, date_target, current_occupancy):
        """low, medium, high"""
        # Logic basata su lead time, booking pace, dati storici
        pass
```

### 6.5 Pydantic Schemas

```python
# backend/schemas/what_if.py

from pydantic import BaseModel, Field
from datetime import date

class WhatIfRequest(BaseModel):
    property_id: int
    date_target: date
    room_type_id: int
    price_adjustment: float = Field(ge=-1.0, le=1.0)  # -100% a +100%

class WhatIfResponse(BaseModel):
    current_price: float
    new_price: float
    predicted_occupancy: float = Field(ge=0, le=1)
    occupancy_delta: float
    predicted_revenue: float
    revenue_delta: float
    competitor_position: str  # above, match, below
    competitor_avg: float
    confidence: str  # low, medium, high
    explanation: str
```

---

## 7. VANTAGGI APPROCCIO PLUG-IN

### Zero Modifiche Codice Esistente

```
✅ revenue_bucchi.py → NO TOUCH
✅ revenue_suggestions.py → NO TOUCH
✅ suggerimenti_engine.py → NO TOUCH
✅ Database schema esistente → NO TOUCH

✏️ main.py → 2 righe aggiunte
```

### Modulo Isolato

- Se What-If si rompe, resto del sistema funziona
- Test isolati, nessun side effect
- Facile rollback (rimuovi 2 righe import)

### Scalabile

- Futura integrazione ML: modifica solo `what_if_calculator.py`
- Aggiungi endpoint: modifica solo `what_if_api.py`
- Zero impatto su altri moduli

---

## 8. CHECKLIST IMPLEMENTAZIONE

### FASE 1: Backend Base

```
[ ] Creare backend/routers/what_if_api.py
    - POST /simulate
    - GET /price-curve

[ ] Creare backend/services/what_if_calculator.py
    - calculate_impact()
    - generate_price_curve()
    - Helper methods

[ ] Creare backend/schemas/what_if.py
    - WhatIfRequest
    - WhatIfResponse

[ ] Aggiungere 2 righe in main.py
    - Import
    - include_router()

[ ] Test con curl
    - curl -X POST /api/v1/what-if/simulate
    - Verificare response JSON
```

### FASE 2: Test

```
[ ] Test unitari service
    - test_calculate_impact()
    - test_generate_price_curve()

[ ] Test API
    - test_simulate_endpoint()
    - test_price_curve_endpoint()

[ ] Test integrazione
    - Con database reale
    - Con dati Nido Lodge
```

### FASE 3: Deploy

```
[ ] Backup database
[ ] Deploy su Lab VM (/app/miracollo-lab)
[ ] Test smoke
[ ] Deploy produzione (/app/miracollo)
[ ] Monitor logs 30 min
```

---

## 9. RISORSE UTILI

### Documentazione

| Risorsa | Path | Contenuto |
|---------|------|-----------|
| Mappa Revenue | `.sncp/progetti/miracollo/reports/MAPPA_REVENUE_INTELLIGENCE_166.md` | 487 righe - mappa completa sistema |
| Audit VM | `.sncp/progetti/miracollo/reports/AUDIT_MIRACOLLO_VM_20260112.md` | 962 righe - stato infrastruttura |
| Roadmap What-If | `.sncp/progetti/miracollo/roadmaps/ROADMAP_WHATIF_SIMULATOR.md` | 385 righe - piano implementazione |
| Protocollo Ibrido | `.sncp/progetti/miracollo/workflow/20260111_PROTOCOLLO_IBRIDO_DEFINITIVO.md` | 451 righe - workflow VM+Locale |

### Comandi SSH VM

```bash
# Accesso VM
ssh miracollo-cervella

# Backend path
cd /app/miracollo/backend

# Verifica struttura
ls -la routers/
ls -la services/

# Test endpoint
curl http://localhost:8000/health
curl http://localhost:8000/api/revenue/bucchi?hotel_code=NL&finestra=1_settimana

# Logs backend
docker logs miracollo-backend-35 -f
```

---

## 10. CONCLUSIONI

### Pattern Chiari Identificati

✅ Router → Service → Database
✅ Pydantic per validazione input/output
✅ Dependency injection (Depends)
✅ HTTPException per error handling
✅ Registrazione router in main.py
✅ Separazione concerns (API, Business, Data)

### What-If Fit Perfetto

✅ Stesso pattern esistente
✅ Zero modifiche codice esistente
✅ Plug-in pulito (2 righe main.py)
✅ Isolato e testabile
✅ Scalabile per ML futuro

### Ready to Implement

- Struttura chiara
- Pattern definiti
- File template pronti
- Checklist pronta
- Zero rischio sistema esistente

---

*"Ricerca 3h + Implementazione 10 minuti = Risultato PERFETTO!"*

*Mappatura completata da Cervella Researcher*
*12 Gennaio 2026*
