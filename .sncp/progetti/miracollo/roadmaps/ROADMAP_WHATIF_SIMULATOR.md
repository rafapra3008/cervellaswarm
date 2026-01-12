# ROADMAP - What-If Pricing Simulator
> Creato: 12 Gennaio 2026 - Sessione 171
> Filosofia: "Una cosa alla volta, fatta BENE"

---

## Visione

```
+================================================================+
|                                                                |
|   "Cosa succede se cambio il prezzo?"                          |
|                                                                |
|   L'utente muove uno slider, vede SUBITO:                      |
|   - Occupancy prevista                                         |
|   - Revenue stimato                                            |
|   - Posizione vs competitor                                    |
|   - Spiegazione AI                                             |
|                                                                |
|   VALORE: Decisioni informate, fiducia nel sistema             |
|                                                                |
+================================================================+
```

---

## Perché What-If PRIMA di ML Avanzato

1. **Valore IMMEDIATO** - Utenti vedono subito l'utilità
2. **Funziona con elasticity semplice** - Non serve ML complesso
3. **Costruisce fiducia** - Prima di automatizzare, mostriamo che capiamo
4. **Base per ML** - Stessa UI, poi aggiungiamo cervello

---

## Fasi di Implementazione

### FASE 1: Backend API Base

**Obiettivo:** Endpoint funzionante che calcola impatto prezzo

**Task:**
```
[ ] 1.1 Creare file routers/what_if_api.py
    - POST /api/v1/what-if/simulate
    - Input: property_id, date, room_type, price_adjustment
    - Output: occupancy, revenue, confidence, explanation

[ ] 1.2 Implementare calcolo elasticity-based
    - Formula: elasticity = -0.5 (standard hotel)
    - Se prezzo +10% → occupancy -5%
    - Calcolo revenue = price * occupancy * rooms

[ ] 1.3 Aggiungere competitor position
    - Fetch prezzo medio competitor
    - above/match/below

[ ] 1.4 Generare explanation testuale
    - Template con variabili
    - "Con prezzo €X, prevedo occupancy Y% perché..."

[ ] 1.5 Test endpoint
    - Test con curl
    - Verificare response JSON
```

**File da creare:**
- `backend/routers/what_if_api.py`
- `backend/services/what_if_calculator.py`

---

### FASE 2: Frontend UI Base

**Obiettivo:** Interfaccia con slider funzionante

**Task:**
```
[ ] 2.1 Creare componente WhatIfSimulator
    - Slider prezzo (-30% a +50%)
    - Display prezzo corrente e nuovo
    - Bottone "Simula"

[ ] 2.2 Aggiungere Impact Preview
    - Card Occupancy (prima → dopo)
    - Card Revenue (prima → dopo)
    - Card Competitor Position

[ ] 2.3 Integrare con API
    - Fetch on slider change (debounce 300ms)
    - Loading state
    - Error handling

[ ] 2.4 Styling base
    - Coerente con Revenue Dashboard
    - Colori: verde positivo, rosso negativo
    - Responsive
```

**File da creare/modificare:**
- `frontend/js/what-if.js`
- `frontend/css/what-if.css`
- Sezione in `revenue.html` o pagina dedicata

---

### FASE 3: Grafico e Visualizzazioni

**Obiettivo:** Grafico price vs occupancy curve

**Task:**
```
[ ] 3.1 Aggiungere grafico Chart.js
    - Asse X: prezzo (range)
    - Asse Y: occupancy prevista
    - Punto evidenziato: scenario corrente

[ ] 3.2 Calcolare curve completa
    - Backend: endpoint per range di prezzi
    - O calcolo frontend con formula

[ ] 3.3 Aggiungere indicatore competitor
    - Linea verticale: prezzo medio competitor
    - Label con valore
```

---

### FASE 4: AI Explanation Avanzata

**Obiettivo:** Spiegazioni contestuali e utili

**Task:**
```
[ ] 4.1 Arricchire explanation con contesto
    - Booking pace (sopra/sotto media)
    - Eventi locali (se presenti)
    - Stagionalità
    - Day of week

[ ] 4.2 Template explanation per scenario
    - Prezzo alto: "Rischio occupancy bassa ma margine alto"
    - Prezzo basso: "Volume alto ma margine ridotto"
    - Prezzo ottimale: "Balance tra occupancy e revenue"

[ ] 4.3 Confidence indicator
    - Barra visuale (low/medium/high)
    - Tooltip con spiegazione
```

---

### FASE 5: Azioni e Integrazione

**Obiettivo:** Connettere simulazione ad azioni reali

**Task:**
```
[ ] 5.1 Bottone "Applica Prezzo"
    - Conferma modale
    - Chiama API per applicare
    - Feedback successo/errore

[ ] 5.2 Bottone "Salva Scenario"
    - Salva in localStorage o DB
    - Lista scenari salvati
    - Confronto scenari

[ ] 5.3 Integrazione con Suggerimenti AI
    - Link da suggerimento a simulatore
    - Pre-popola con dati suggerimento
    - "Simula questo suggerimento"
```

---

### FASE 6: Ottimizzazioni

**Obiettivo:** Performance e UX fluida

**Task:**
```
[ ] 6.1 Caching backend
    - Cache scenari comuni (TTL 1h)
    - Pre-calcola 10 scenari standard

[ ] 6.2 Debounce ottimizzato
    - 300ms delay su slider
    - Cancel previous request

[ ] 6.3 Loading states
    - Skeleton mentre carica
    - Transizioni smooth
```

---

## Architettura

```
┌─────────────────────────────────────────┐
│           FRONTEND (React/JS)           │
├─────────────────────────────────────────┤
│  WhatIfSimulator Component              │
│  - Slider (price adjustment)            │
│  - Impact Cards (occ, rev, pos)         │
│  - Chart (price vs occupancy)           │
│  - Actions (apply, save, reset)         │
└─────────────────────────────────────────┘
                    ↓ API
┌─────────────────────────────────────────┐
│          BACKEND (FastAPI)              │
├─────────────────────────────────────────┤
│  POST /api/v1/what-if/simulate          │
│  - what_if_calculator.py                │
│  - Elasticity-based (MVP)               │
│  - ML-based (futuro)                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         DATABASE (PostgreSQL)           │
├─────────────────────────────────────────┤
│  - pricing_history (prezzi attuali)     │
│  - competitor_prices (competitor)       │
│  - what_if_cache (opzionale)            │
└─────────────────────────────────────────┘
```

---

## API Contract

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
  "explanation": "Con prezzo €132 (+10%), prevedo occupancy 75% (-3%) ma revenue +€450 (+5%). Competitors a €135 - posizione competitiva buona."
}
```

---

## UI Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ What-If Pricing Simulator                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📅 Data: 20 Gen 2026    🏠 Standard Double                  │
│                                                             │
│ ── Prezzo Attuale: €120 ─────────────────────────────────  │
│                                                             │
│ Nuovo Prezzo:                                               │
│ €80 ◄─────────────●──────────────────────► €180            │
│                  €132 (+10%)                                │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ IMPATTO PREVISTO                                            │
├──────────────────┬──────────────────┬──────────────────────┤
│   OCCUPANCY      │     REVENUE      │   VS COMPETITOR      │
│   78% → 75%      │  €9,360 → €9,900 │   €132 vs €135       │
│   -3% ⚠️         │   +€540 ✅       │   Match ✅           │
└──────────────────┴──────────────────┴──────────────────────┘
│                                                             │
│ 💡 "Con prezzo €132, occupancy cala leggermente ma          │
│    revenue aumenta. Posizione competitiva buona."           │
│                                                             │
│ Confidence: ███████░░░ Medium                               │
│                                                             │
│ [Reset]  [Salva Scenario]  [Applica Prezzo]                │
└─────────────────────────────────────────────────────────────┘
```

---

## Formula Elasticity (MVP)

```python
# Price Elasticity of Demand per hotel: tipicamente -0.5
# Se prezzo +10%, domanda -5%

def calculate_impact(current_price, new_price, current_occupancy):
    elasticity = -0.5  # hotel standard

    price_change = (new_price - current_price) / current_price
    occupancy_change = elasticity * price_change

    new_occupancy = current_occupancy * (1 + occupancy_change)
    new_occupancy = max(0.0, min(1.0, new_occupancy))

    # Revenue = prezzo * occupancy * camere
    rooms = 86  # Nido Lodge
    current_revenue = current_price * current_occupancy * rooms
    new_revenue = new_price * new_occupancy * rooms

    return {
        'new_occupancy': new_occupancy,
        'occupancy_delta': new_occupancy - current_occupancy,
        'new_revenue': new_revenue,
        'revenue_delta': new_revenue - current_revenue
    }
```

---

## Ordine di Esecuzione

```
FASE 1: Backend API Base
    ↓
FASE 2: Frontend UI Base
    ↓
FASE 3: Grafico
    ↓
FASE 4: AI Explanation
    ↓
FASE 5: Azioni
    ↓
FASE 6: Ottimizzazioni
```

**Ogni fase è indipendente e testabile.**

---

## Criteri di Successo

| Fase | Criterio |
|------|----------|
| 1 | API risponde con dati corretti |
| 2 | Slider funziona, mostra impatto |
| 3 | Grafico si aggiorna dinamicamente |
| 4 | Explanation utile e contestuale |
| 5 | Utente può applicare prezzo |
| 6 | UX fluida, <200ms response |

---

## File di Riferimento

| File | Contenuto |
|------|-----------|
| `idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md` | Ricerca completa (1600+ righe) |
| `reports/MAPPA_REVENUE_INTELLIGENCE_166.md` | Mappa sistema Revenue |
| `roadmaps/20260112_ROADMAP_REVENUE_7_TO_10.md` | Roadmap Revenue generale |

---

## Note

- **MVP con Elasticity**: Funziona SENZA ML complesso
- **ML Futuro**: Stessa UI, sostituiamo calcolo backend
- **Valore Immediato**: Utenti vedono subito l'utilità
- **Una cosa alla volta**: Prima funziona, poi miglioriamo

---

*"Ultrapassar os próprios limites!"*
*"La MAGIA ora è nascosta! E ora con coscienza!"*

---

*Roadmap creata con calma e organizzazione*
*12 Gennaio 2026 - Sessione 171*
