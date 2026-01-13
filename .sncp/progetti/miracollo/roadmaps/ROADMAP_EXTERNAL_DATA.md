# ROADMAP EXTERNAL DATA - Miracollo RMS

> **Versione:** 1.0.0
> **Data:** 13 Gennaio 2026
> **Autore:** Cervella Regina
> **Status:** APPROVATA - Pronta per Implementazione

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|   "L'AI CHE CAPISCE IL MONDO"                                  |
|                                                                |
|   OBIETTIVO: Integrare dati esterni per suggerimenti           |
|   intelligenti che nessun competitor SMB ha!                   |
|                                                                |
|   COMPONENTI:                                                  |
|   1. METEO - Neve, pioggia, temperature                        |
|   2. EVENTI LOCALI - Concerti, fiere, sport, festivita         |
|                                                                |
|   RISULTATO ATTESO:                                            |
|   - +3-5% RevPAR (solo meteo)                                  |
|   - +10-15% RevPAR durante eventi                              |
|   - RATEBOARD: da 9.0/10 a 9.5/10!                            |
|                                                                |
+================================================================+
```

**Differenziazione UNICA:**
- IDeaS, Duetto, Atomize → NON hanno meteo nativo per SMB
- Noi → Native PMS + Meteo + Eventi = PERFECT FIT!

---

## STATO ATTUALE - Cosa Abbiamo Gia

### Festivita Italiane (calendar_events.py)

```
FILE: backend/services/calendar_events.py

GIA IMPLEMENTATO:
- 13+ festivita italiane (Capodanno, Epifania, Pasqua, etc.)
- Impact % per ogni festivita
- Calcolo Pasqua dinamico (2024-2030)
- Stagionalita (alta/media/bassa)
- Weekend detection
- Integrato in AI Suggestions
```

| Festivita | Impact % | Tipo |
|-----------|----------|------|
| San Silvestro | 50% | holiday |
| Ferragosto | 45% | holiday |
| Capodanno | 40% | holiday |
| Natale | 40% | holiday |
| San Valentino | 35% | romantic |
| Santo Stefano | 35% | holiday |
| Pasqua | 35% | holiday |
| Pasquetta | 30% | holiday |
| Epifania | 25% | holiday |
| Immacolata | 25% | holiday |
| Liberazione | 20% | holiday |
| Festa Lavoro | 20% | holiday |
| Repubblica | 15% | holiday |
| Ognissanti | 15% | holiday |

**VERDICT:** Festivita = FATTO! Non serve toccare.

---

## COSA MANCA

| Componente | Status | Valore | Effort |
|------------|--------|--------|--------|
| **METEO** | DA FARE | ALTO | 5-6 giorni |
| **EVENTI LOCALI** | DA FARE | ALTO | 3 settimane |

---

## FASE 1: INTEGRAZIONE METEO

### 1.0 Overview

```
+================================================================+
|   METEO INTEGRATION                                            |
|                                                                |
|   API: WeatherAPI.com (FREE 1000 call/mese)                    |
|   EFFORT: 5-6 giorni                                           |
|   ROI: 694% anno 1 (+17K euro/hotel)                           |
|                                                                |
|   IMPATTO NEVE (hotel montagna):                               |
|   - Neve fresca forecast: +20-40% occupancy                    |
|   - No neve vs media: -10-15% occupancy                        |
|   - Con dynamic pricing: +3-5% RevPAR annuale                  |
|                                                                |
+================================================================+
```

### 1.1 Sub-Roadmap Meteo

#### FASE 1.1: Setup e Spike (Giorno 1)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 1.1.1 Registrazione WeatherAPI.com | Backend | 30min | API Key attiva |
| 1.1.2 Test API con location Naturae Lodge | Backend | 2h | Response JSON valida |
| 1.1.3 Verifica dati neve disponibili | Backend | 1h | Conferma snow_cm presente |
| 1.1.4 Setup Redis per cache (se non esiste) | DevOps | 1h | Redis running |

**Criteri Completamento:**
- [ ] API Key funzionante
- [ ] Chiamata test con risposta 200
- [ ] Dati neve presenti nella risposta
- [ ] Redis disponibile

---

#### FASE 1.2: Backend Service (Giorni 2-3)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 1.2.1 WeatherService class | Backend | 4h | weather_service.py |
| 1.2.2 Caching layer (Redis 6h TTL) | Backend | 2h | Cache funzionante |
| 1.2.3 extract_snow_metrics() | Backend | 2h | Metriche neve estratte |
| 1.2.4 Error handling + fallback | Backend | 2h | Resilienza |
| 1.2.5 Unit tests (coverage 70%) | Tester | 4h | Tests passing |

**File da creare:**
```
backend/services/weather_service.py
backend/services/demand_forecast_service.py (modifica)
backend/tests/test_weather_service.py
```

**Metriche da estrarre:**
- `next_3_days_snow_cm` - Neve prossimi 3 giorni
- `next_7_days_snow_cm` - Neve prossima settimana
- `snow_days_count_7d` - Giorni con neve
- `avg_daily_chance_snow_7d` - Probabilita media neve
- `alerts` - Allerte meteo

**Criteri Completamento:**
- [ ] WeatherService instanziabile
- [ ] Cache hit rate > 90%
- [ ] Metriche neve estratte correttamente
- [ ] Fallback funziona se API down
- [ ] Tests passing

---

#### FASE 1.3: API Endpoints (Giorno 3)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 1.3.1 GET /api/weather/forecast/{hotel_id} | Backend | 2h | Endpoint attivo |
| 1.3.2 GET /api/weather/impact/{hotel_id} | Backend | 2h | Impatto calcolato |
| 1.3.3 Documentazione API | Docs | 1h | OpenAPI spec |

**Endpoint Specs:**

```
GET /api/weather/forecast/1?days=7
Response:
{
  "hotel_id": 1,
  "snow_metrics": {
    "next_3_days_snow_cm": 15.5,
    "next_7_days_snow_cm": 28.0,
    "snow_days_count_7d": 4,
    "avg_daily_chance_snow_7d": 65,
    "alerts": []
  },
  "last_updated": "2026-01-13T10:00:00"
}

GET /api/weather/impact/1?date=2026-01-20
Response:
{
  "hotel_id": 1,
  "date": "2026-01-20",
  "weather_multiplier": 1.25,
  "impact_pct": 25.0,
  "note": "Heavy snow forecast - strong demand expected"
}
```

**Criteri Completamento:**
- [ ] Entrambi endpoint funzionanti
- [ ] Response < 500ms
- [ ] Documentazione aggiornata

---

#### FASE 1.4: Integrazione AI Suggestions (Giorno 4)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 1.4.1 Modifica suggerimenti_engine.py | Backend | 3h | Weather in suggestions |
| 1.4.2 Nuovo tipo WEATHER_BOOST | Backend | 2h | Tipo suggestion |
| 1.4.3 Nuovo tipo WEATHER_PROMO | Backend | 1h | Tipo suggestion |
| 1.4.4 Tests integrazione | Tester | 2h | Tests passing |

**Logica Business (Hotel Montagna):**

```python
# Calcolo weather_multiplier
if days_until <= 3:
    if snow_cm > 15:
        return 1.30  # +30% demand - WEATHER_BOOST
    elif snow_cm > 5:
        return 1.15  # +15% demand
    elif snow_cm == 0:
        return 0.90  # -10% demand - WEATHER_PROMO

elif days_until <= 7:
    if snow_days >= 4:
        return 1.20  # +20% demand
    elif snow_days <= 1:
        return 0.92  # -8% demand

else:
    # Long-term: solo alert importanti
    return 1.0  # Neutral
```

**Nuovi tipi suggestion:**
- `WEATHER_BOOST` - Neve forte, alza prezzi
- `WEATHER_PROMO` - Poca neve, considera promozione

**Criteri Completamento:**
- [ ] Suggerimenti meteo appaiono quando appropriato
- [ ] Explanation include dettagli meteo
- [ ] Confidence appropriato (82% boost, 75% promo)

---

#### FASE 1.5: Frontend Widget (Giorno 5)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 1.5.1 WeatherWidget component | Frontend | 4h | Widget funzionante |
| 1.5.2 CSS styling (gradient, cards) | Frontend | 2h | Design bello |
| 1.5.3 Integrazione in Rateboard | Frontend | 2h | Widget visibile |
| 1.5.4 Auto-refresh ogni 6h | Frontend | 1h | Aggiornamento auto |

**UI Design:**
```
+------------------------------------------+
| Weather Forecast                   10:00 |
+------------------------------------------+
|  Next 3 Days  |  Next 7 Days  |  Snow   |
|    15.5 cm    |    28.0 cm    |  4 days |
|   (heavy)     |   (moderate)  |         |
+------------------------------------------+
| High demand expected - Consider +15-25% |
+------------------------------------------+
```

**Criteri Completamento:**
- [ ] Widget visibile in Rateboard
- [ ] Dati aggiornati ogni 6h
- [ ] Color coding per intensita neve
- [ ] Note impatto chiara

---

#### FASE 1.6: Deploy e Monitoring (Giorno 6)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 1.6.1 Migration database (tracking) | Backend | 1h | Tabelle create |
| 1.6.2 Cron job cache warming | DevOps | 1h | Cron attivo |
| 1.6.3 Deploy staging | DevOps | 2h | Staging funzionante |
| 1.6.4 Test manuale completo | Tester | 2h | QA passed |
| 1.6.5 Deploy produzione | DevOps | 1h | LIVE! |

**Tabelle Monitoring:**
```sql
-- weather_api_usage (tracking chiamate)
-- weather_impact_tracking (accuracy prediction)
```

**Cron Job:**
```bash
# Ogni 6 ore, refresh cache per hotel attivi
0 */6 * * * python scripts/weather_cache_warmer.py
```

**Criteri Completamento:**
- [ ] Staging testato e approvato
- [ ] Cron job funzionante
- [ ] Monitoring attivo
- [ ] PRODUZIONE LIVE

---

### 1.2 Summary Fase 1 (Meteo)

| Metrica | Target |
|---------|--------|
| **Effort Totale** | 5-6 giorni |
| **API Cost** | 0 euro (free tier) |
| **Test Coverage** | 70%+ |
| **Response Time** | < 500ms |
| **Cache Hit Rate** | > 90% |

**Deliverables Finali:**
- [ ] weather_service.py funzionante
- [ ] 2 API endpoints attivi
- [ ] WeatherWidget in Rateboard
- [ ] Suggerimenti WEATHER_BOOST e WEATHER_PROMO
- [ ] Monitoring attivo
- [ ] Documentazione completa

---

## FASE 2: EVENTI LOCALI

### 2.0 Overview

```
+================================================================+
|   EVENTI LOCALI INTEGRATION                                    |
|                                                                |
|   APPROCCIO: Hybrid (Manual + Scraping)                        |
|   EFFORT: 3 settimane (40-60h)                                 |
|   ROI: +10-15% RevPAR durante eventi                           |
|                                                                |
|   IMPATTO EVENTI:                                              |
|   - Major events (Olimpiadi): +300-500% ADR                    |
|   - Concerti: +100-200% ADR                                    |
|   - Eventi locali: +20-50% ADR                                 |
|                                                                |
|   FOCUS NATURAE LODGE:                                         |
|   - Olimpiadi 2026 Cortina (Feb-Mar)                           |
|   - World Cup Sci                                              |
|   - Mercatini Natale                                           |
|   - Wellness Retreats                                          |
|                                                                |
+================================================================+
```

### 2.1 Sub-Roadmap Eventi Locali

#### FASE 2.1: Database Schema (Settimana 1 - Giorni 1-2)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.1.1 Design schema eventi | Data | 2h | Schema definito |
| 2.1.2 Migration 039_local_events.sql | Backend | 2h | Migration pronta |
| 2.1.3 Models SQLAlchemy | Backend | 2h | Models creati |
| 2.1.4 Test migration | Tester | 1h | Migration testata |

**Schema Database:**

```sql
-- Tabella: local_events
CREATE TABLE local_events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    -- Tipi: concert, sport, festival, conference, local, ski_race, wellness
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    venue_name VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    estimated_attendance INTEGER,
    impact_level VARCHAR(20),
    -- Livelli: low, medium, high, extreme
    data_source VARCHAR(50),
    -- Fonti: manual, scraped_cortina, scraped_dolomiti, api_ticketmaster
    source_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabella: hotel_event_impact
CREATE TABLE hotel_event_impact (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    event_id INTEGER REFERENCES local_events(id),
    distance_km DECIMAL(5, 2),
    impact_score DECIMAL(3, 2),
    -- 1.0 = neutral, 1.5 = +50%, 2.0 = +100%
    estimated_adr_increase_pct DECIMAL(5, 2),
    manual_override BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hotel_id, event_id)
);

-- Indici
CREATE INDEX idx_events_dates ON local_events(start_date, end_date);
CREATE INDEX idx_events_city ON local_events(city);
CREATE INDEX idx_events_type ON local_events(event_type);
CREATE INDEX idx_impact_hotel ON hotel_event_impact(hotel_id);
CREATE INDEX idx_impact_event ON hotel_event_impact(event_id);

-- View: eventi con impatto per hotel
CREATE VIEW v_hotel_events AS
SELECT
    h.id as hotel_id,
    h.name as hotel_name,
    e.*,
    hei.distance_km,
    hei.impact_score,
    hei.estimated_adr_increase_pct
FROM hotels h
CROSS JOIN local_events e
LEFT JOIN hotel_event_impact hei
    ON hei.hotel_id = h.id AND hei.event_id = e.id
WHERE e.is_active = true;
```

**Criteri Completamento:**
- [ ] Migration eseguita senza errori
- [ ] Models SQLAlchemy funzionanti
- [ ] View creata
- [ ] Indici ottimizzati

---

#### FASE 2.2: Backend Service (Settimana 1 - Giorni 3-5)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.2.1 EventService class | Backend | 4h | event_service.py |
| 2.2.2 Impact calculator | Backend | 4h | Algoritmo impatto |
| 2.2.3 Distance calculator (Haversine) | Backend | 2h | Calcolo distanza |
| 2.2.4 CRUD operations | Backend | 3h | Create/Read/Update/Delete |
| 2.2.5 Unit tests | Tester | 4h | Tests passing |

**File da creare:**
```
backend/services/event_service.py
backend/services/impact_calculator.py
backend/tests/test_event_service.py
```

**Algoritmo Calcolo Impatto:**

```python
def calculate_event_impact(event, hotel_location):
    """
    Calcola impatto evento su hotel basato su:
    - Distanza (decay esponenziale)
    - Tipo evento
    - Attendance stimata
    - Durata evento
    """
    # 1. Calcola distanza (Haversine)
    distance_km = haversine(
        hotel_location.lat, hotel_location.lon,
        event.latitude, event.longitude
    )

    # 2. Distance decay (oltre 20km = no impact)
    if distance_km > 20:
        return 1.0  # No impact

    distance_factor = 1.0 - (distance_km / 20) * 0.5
    # 0km = 1.0, 10km = 0.75, 20km = 0.5

    # 3. Event type multiplier
    type_multipliers = {
        'concert': 1.8,      # Concerti = alto
        'sport': 1.5,        # Sport = medio-alto
        'festival': 2.0,     # Festival = molto alto
        'conference': 1.3,   # Conferenze = medio
        'local': 1.2,        # Locali = basso
        'ski_race': 1.6,     # Gare sci = alto
        'wellness': 1.15,    # Wellness = basso
        'olympics': 2.5,     # Olimpiadi = MASSIMO!
    }
    type_factor = type_multipliers.get(event.event_type, 1.2)

    # 4. Attendance factor (se disponibile)
    if event.estimated_attendance:
        if event.estimated_attendance > 50000:
            attendance_factor = 1.5
        elif event.estimated_attendance > 10000:
            attendance_factor = 1.3
        elif event.estimated_attendance > 1000:
            attendance_factor = 1.1
        else:
            attendance_factor = 1.0
    else:
        attendance_factor = 1.0

    # 5. Calcolo finale
    impact_score = 1.0 + (type_factor - 1.0) * distance_factor * attendance_factor

    # Cap a 2.5 (max +150%)
    return min(impact_score, 2.5)
```

**Criteri Completamento:**
- [ ] EventService instanziabile
- [ ] Calcolo distanza preciso
- [ ] Impatto calcolato correttamente
- [ ] CRUD funzionanti
- [ ] Tests passing

---

#### FASE 2.3: API Endpoints (Settimana 2 - Giorni 1-2)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.3.1 POST /api/events/ (create) | Backend | 2h | Endpoint attivo |
| 2.3.2 GET /api/events/ (list) | Backend | 2h | Endpoint attivo |
| 2.3.3 PUT /api/events/{id} (update) | Backend | 1h | Endpoint attivo |
| 2.3.4 DELETE /api/events/{id} (soft delete) | Backend | 1h | Endpoint attivo |
| 2.3.5 PUT /api/events/{id}/impact-override | Backend | 2h | Override impatto |
| 2.3.6 Documentazione API | Docs | 1h | OpenAPI spec |

**File da creare:**
```
backend/routers/local_events.py
```

**Endpoint Specs:**

```
POST /api/events/
Body:
{
  "event_name": "Olimpiadi Milano-Cortina 2026",
  "event_type": "olympics",
  "start_date": "2026-02-06",
  "end_date": "2026-02-22",
  "venue_name": "Cortina d'Ampezzo",
  "city": "Cortina d'Ampezzo",
  "latitude": 46.5369,
  "longitude": 12.1389,
  "estimated_attendance": 100000,
  "description": "Olimpiadi Invernali 2026"
}
Response: 201 Created
{
  "id": 1,
  "event_name": "Olimpiadi Milano-Cortina 2026",
  "impact_calculations": [
    {"hotel_id": 1, "distance_km": 5.2, "impact_score": 2.3}
  ]
}

GET /api/events/?hotel_id=1&start_date=2026-02-01&end_date=2026-02-28
Response:
{
  "events": [
    {
      "id": 1,
      "event_name": "Olimpiadi Milano-Cortina 2026",
      "start_date": "2026-02-06",
      "end_date": "2026-02-22",
      "impact_score": 2.3,
      "distance_km": 5.2,
      "estimated_adr_increase_pct": 130
    }
  ],
  "total": 1
}

PUT /api/events/1/impact-override
Body:
{
  "hotel_id": 1,
  "impact_score": 2.5,
  "reason": "Hotelier override - evento piu importante del previsto"
}
Response: 200 OK
```

**Criteri Completamento:**
- [ ] Tutti endpoint funzionanti
- [ ] Validazione input corretta
- [ ] Calcolo impatto automatico su create
- [ ] Override funzionante
- [ ] Documentazione aggiornata

---

#### FASE 2.4: Integrazione AI Suggestions (Settimana 2 - Giorni 3-4)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.4.1 Modifica suggerimenti_engine.py | Backend | 3h | Eventi in suggestions |
| 2.4.2 Nuovo tipo EVENT_DRIVEN_INCREASE | Backend | 2h | Tipo suggestion |
| 2.4.3 Query eventi per date range | Backend | 2h | Query ottimizzata |
| 2.4.4 Tests integrazione | Tester | 3h | Tests passing |

**Integrazione in suggerimenti_engine.py:**

```python
async def generate_ai_suggestions(hotel_id, date_range):
    suggestions = []

    # ... existing suggestions ...

    # NEW: Eventi locali
    event_suggestions = await consider_local_events(hotel_id, date_range)
    suggestions.extend(event_suggestions)

    return suggestions

async def consider_local_events(hotel_id, date_range):
    """
    Genera suggerimenti basati su eventi locali con impatto > 1.1
    """
    events = await db.fetch("""
        SELECT
            e.id, e.event_name, e.event_type,
            e.start_date, e.end_date,
            e.estimated_attendance,
            hei.distance_km, hei.impact_score,
            hei.estimated_adr_increase_pct
        FROM local_events e
        JOIN hotel_event_impact hei ON e.id = hei.event_id
        WHERE hei.hotel_id = $1
            AND e.is_active = true
            AND e.start_date <= $2
            AND e.end_date >= $3
            AND hei.impact_score > 1.1
        ORDER BY hei.impact_score DESC
    """, hotel_id, date_range.end, date_range.start)

    suggestions = []
    for event in events:
        suggestion = {
            'id': f"event_{event['id']}",
            'type': 'EVENT_DRIVEN_INCREASE',
            'category': 'external_data',
            'date_from': event['start_date'],
            'date_to': event['end_date'],
            'suggested_action': 'increase_price',
            'suggested_value': event['impact_score'],
            'confidence': 85,
            'reason': f"Evento: {event['event_name']}",
            'explanation_breakdown': [
                f"Evento locale rilevato: {event['event_name']}",
                f"Distanza: {event['distance_km']:.1f} km",
                f"Tipo: {event['event_type']}",
                f"Impatto stimato: +{event['estimated_adr_increase_pct']:.0f}% ADR",
                f"Suggerimento: Aumenta prezzi del {(event['impact_score'] - 1) * 100:.0f}%"
            ],
            'impact_data': {
                'event_id': event['id'],
                'event_name': event['event_name'],
                'event_type': event['event_type'],
                'distance_km': event['distance_km'],
                'attendance': event['estimated_attendance']
            }
        }
        suggestions.append(suggestion)

    return suggestions
```

**Criteri Completamento:**
- [ ] Suggerimenti eventi appaiono correttamente
- [ ] Explanation include dettagli evento
- [ ] Icona distinguibile (calendario)
- [ ] Impact data presente

---

#### FASE 2.5: Frontend UI Eventi (Settimana 2-3)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.5.1 Events Manager page/section | Frontend | 6h | UI gestione eventi |
| 2.5.2 Event Card component | Frontend | 3h | Card evento |
| 2.5.3 Create/Edit Modal | Frontend | 4h | Modal CRUD |
| 2.5.4 Filtri (date, tipo) | Frontend | 2h | Filtri funzionanti |
| 2.5.5 CSS styling | Frontend | 2h | Design coerente |
| 2.5.6 Suggestion card update | Frontend | 2h | Icona evento |

**File da creare:**
```
frontend/js/events-manager.js
frontend/css/events.css
frontend/events.html (o sezione in revenue.html)
```

**UI Design:**

```
+----------------------------------------------------------+
| Eventi Locali                           [+ Aggiungi Evento] |
+----------------------------------------------------------+
| Filtri: [Data inizio] [Data fine] [Tipo: Tutti v]          |
+----------------------------------------------------------+
|                                                           |
| +---------------------------+  +---------------------------+
| | OLIMPIADI 2026            |  | WORLD CUP SCI             |
| | 06 Feb - 22 Feb           |  | 15 Gen - 16 Gen           |
| | olympics                  |  | ski_race                  |
| | 5.2 km - +130% ADR       |  | 12.0 km - +60% ADR        |
| | [Edit] [Delete]           |  | [Edit] [Delete]           |
| +---------------------------+  +---------------------------+
|                                                           |
+----------------------------------------------------------+
```

**Criteri Completamento:**
- [ ] Lista eventi visibile
- [ ] CRUD funzionante
- [ ] Filtri funzionanti
- [ ] Design coerente con resto UI
- [ ] Impact mostrato chiaramente

---

#### FASE 2.6: Scraper Cortina (Settimana 3 - OPZIONALE)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.6.1 Analisi HTML cortinadampezzo.it | Researcher | 2h | Selettori identificati |
| 2.6.2 CortinaEventScraper class | Backend | 4h | Scraper funzionante |
| 2.6.3 DolomitiSuperskiScraper class | Backend | 4h | Scraper funzionante |
| 2.6.4 Cron job settimanale | DevOps | 1h | Sync automatico |
| 2.6.5 Error handling + logging | Backend | 2h | Resilienza |

**NOTA:** Questa fase e OPZIONALE per MVP! Eventi manuali sono sufficienti per dimostrare valore!

**File da creare:**
```
backend/services/event_scrapers/cortina_scraper.py
backend/services/event_scrapers/dolomiti_scraper.py
backend/scripts/weekly_event_sync.py
```

**Criteri Completamento:**
- [ ] Scraper estrae eventi correttamente
- [ ] Cron job attivo (domenica 3am)
- [ ] Logging eventi importati
- [ ] Fallback se scraping fallisce

---

#### FASE 2.7: Deploy e Testing (Settimana 3)

| Task | Owner | Effort | Deliverable |
|------|-------|--------|-------------|
| 2.7.1 Seed data eventi test | Backend | 1h | Dati test inseriti |
| 2.7.2 Integration tests | Tester | 4h | Tests passing |
| 2.7.3 Deploy staging | DevOps | 2h | Staging funzionante |
| 2.7.4 Test manuale completo | Tester | 3h | QA passed |
| 2.7.5 Deploy produzione | DevOps | 1h | LIVE! |
| 2.7.6 Documentazione utente | Docs | 2h | Guide create |

**Seed Data Iniziale (eventi reali Naturae Lodge):**

```python
SEED_EVENTS = [
    {
        "event_name": "Olimpiadi Milano-Cortina 2026",
        "event_type": "olympics",
        "start_date": "2026-02-06",
        "end_date": "2026-02-22",
        "city": "Cortina d'Ampezzo",
        "estimated_attendance": 100000,
        "impact_level": "extreme"
    },
    {
        "event_name": "Paralimpiadi Milano-Cortina 2026",
        "event_type": "olympics",
        "start_date": "2026-03-06",
        "end_date": "2026-03-15",
        "city": "Cortina d'Ampezzo",
        "estimated_attendance": 50000,
        "impact_level": "extreme"
    },
    {
        "event_name": "World Cup Sci Femminile Cortina",
        "event_type": "ski_race",
        "start_date": "2026-01-18",
        "end_date": "2026-01-19",
        "city": "Cortina d'Ampezzo",
        "estimated_attendance": 15000,
        "impact_level": "high"
    },
    {
        "event_name": "Mercatini di Natale Cortina",
        "event_type": "local",
        "start_date": "2026-12-08",
        "end_date": "2026-01-06",
        "city": "Cortina d'Ampezzo",
        "estimated_attendance": 5000,
        "impact_level": "medium"
    }
]
```

**Criteri Completamento:**
- [ ] Seed data inseriti
- [ ] Staging testato
- [ ] Suggerimenti eventi visibili
- [ ] Override funzionante
- [ ] PRODUZIONE LIVE

---

### 2.2 Summary Fase 2 (Eventi Locali)

| Metrica | Target |
|---------|--------|
| **Effort Totale** | 40-60 ore (3 settimane) |
| **API Cost** | 0 euro (manual + scraping) |
| **Test Coverage** | 70%+ |
| **Eventi Seed** | 10+ |

**Deliverables Finali:**
- [ ] Database schema eventi
- [ ] EventService funzionante
- [ ] 5 API endpoints attivi
- [ ] UI gestione eventi
- [ ] Suggerimenti EVENT_DRIVEN_INCREASE
- [ ] (Opzionale) Scraper Cortina
- [ ] Documentazione completa

---

## FASE 3: OTTIMIZZAZIONE (Post-MVP)

### 3.1 Dopo 3 Mesi di Dati

| Task | Quando | Descrizione |
|------|--------|-------------|
| 3.1.1 Analisi accuracy meteo | Mese 3 | Confronto forecast vs actual occupancy |
| 3.1.2 Tuning multiplier meteo | Mese 3 | Aggiusta +/- basato su dati |
| 3.1.3 Analisi ROI eventi | Mese 3 | Quanto ha generato ogni evento? |
| 3.1.4 Tuning impact calculator | Mese 3 | Aggiusta distance decay |

### 3.2 Espansione (Mesi 4-12)

| Task | Priorita | Descrizione |
|------|----------|-------------|
| 3.2.1 Piu fonti scraping | Media | Dolomiti.org, tourism boards |
| 3.2.2 Italian Open Data | Media | Ministero Cultura XML |
| 3.2.3 Ticketmaster API | Bassa | Concerti/sport |
| 3.2.4 PredictHQ evaluation | Bassa | Solo se 50+ hotel |

### 3.3 ML Enhancement (Mese 6+)

| Task | Descrizione |
|------|-------------|
| 3.3.1 Weather prediction model | ML per predire impatto meteo |
| 3.3.2 Event impact model | ML per predire impatto eventi |
| 3.3.3 Combined forecast | Meteo + Eventi + Storico |

---

## SUCCESS METRICS

### Fase 1 (Meteo) - Target

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| Widget visibile | 100% | Visual check |
| API response time | < 500ms | Monitoring |
| Cache hit rate | > 90% | Redis stats |
| Suggerimenti meteo | Presenti quando appropriato | Manual check |
| User satisfaction | Positivo | Feedback |

### Fase 2 (Eventi) - Target

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| Eventi inseriti | 20+ | DB count |
| Eventi high-impact | 5+ | impact_score > 1.5 |
| Suggerimenti eventi | Presenti | Manual check |
| Acceptance rate | > 60% | User accepts suggestions |

### Overall - Target Q1 2026

| Metrica | Attuale | Target |
|---------|---------|--------|
| RATEBOARD Score | 9.0/10 | 9.5/10 |
| RevPAR (meteo) | baseline | +3-5% |
| RevPAR (eventi) | baseline | +10-15% |

---

## TIMELINE GENERALE

```
GENNAIO 2026
+-------+-------+-------+-------+
| W1    | W2    | W3    | W4    |
+-------+-------+-------+-------+
| METEO FASE 1.1-1.3            |
|       | METEO FASE 1.4-1.6    |
+-------+-------+-------+-------+

FEBBRAIO 2026
+-------+-------+-------+-------+
| W1    | W2    | W3    | W4    |
+-------+-------+-------+-------+
| EVENTI FASE 2.1-2.3           |
|       | EVENTI FASE 2.4-2.5   |
|               | EVENTI 2.6-2.7|
+-------+-------+-------+-------+

MARZO 2026
+-------+-------+-------+-------+
| W1    | W2    | W3    | W4    |
+-------+-------+-------+-------+
| OTTIMIZZAZIONE E TUNING       |
+-------+-------+-------+-------+
```

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| WeatherAPI rate limit | Media | Alto | Cache aggressiva, monitoring |
| Location imprecisa | Bassa | Medio | Fallback regione generica |
| Scraper si rompe | Alta | Medio | Eventi manuali sempre funzionano |
| Impatto calcolato male | Media | Medio | Override manuale hotelier |
| User non inserisce eventi | Media | Alto | Seed data, reminder |

---

## CHECKLIST PRE-IMPLEMENTAZIONE

Prima di iniziare, verificare:

- [ ] Redis disponibile (per cache meteo)
- [ ] WeatherAPI.com account creato
- [ ] Location Naturae Lodge (lat/lon)
- [ ] Accesso a suggerimenti_engine.py
- [ ] Design review UI approvato
- [ ] Rafa approva roadmap

---

## APPENDICE: FILE DA CREARE

### Fase 1 (Meteo)
```
backend/
├── services/
│   ├── weather_service.py        (NUOVO)
│   └── demand_forecast_service.py (MODIFICA)
├── routers/
│   └── weather.py                (NUOVO)
├── tests/
│   └── test_weather_service.py   (NUOVO)
└── scripts/
    └── weather_cache_warmer.py   (NUOVO)

frontend/
├── js/
│   └── components/
│       └── WeatherWidget.js      (NUOVO)
└── css/
    └── weather-widget.css        (NUOVO)
```

### Fase 2 (Eventi)
```
backend/
├── services/
│   ├── event_service.py          (NUOVO)
│   ├── impact_calculator.py      (NUOVO)
│   └── event_scrapers/           (NUOVO - opzionale)
│       ├── cortina_scraper.py
│       └── dolomiti_scraper.py
├── routers/
│   └── local_events.py           (NUOVO)
├── database/migrations/
│   └── 039_local_events.sql      (NUOVO)
├── tests/
│   └── test_event_service.py     (NUOVO)
└── scripts/
    └── weekly_event_sync.py      (NUOVO - opzionale)

frontend/
├── js/
│   └── events-manager.js         (NUOVO)
├── css/
│   └── events.css                (NUOVO)
└── events.html                   (NUOVO o sezione)
```

---

*"L'AI che capisce il mondo - Meteo + Eventi = MAGIA!"*
*"Fatto BENE > Fatto VELOCE"*
*"Una cosa alla volta, standard 100000%!"*

*Roadmap creata: 13 Gennaio 2026*
*Cervella Regina per Miracollo*
