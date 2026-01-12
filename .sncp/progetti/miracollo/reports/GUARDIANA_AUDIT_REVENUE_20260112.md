# AUDIT COMPLETO: Revenue Intelligence System
## Guardiana Qualita - 12 Gennaio 2026

**Progetto:** Miracollo
**Sistema:** Revenue Intelligence (FASE 7)
**Audit Depth:** DEEP DIVE
**Auditor:** Cervella Guardiana Qualita

---

## EXECUTIVE SUMMARY

| Categoria | Status | Score |
|-----------|--------|-------|
| Database Integrity | WARNING | 7/10 |
| API Endpoints | PASS | 8/10 |
| Frontend-Backend Sync | PASS | 8/10 |
| Code Quality | PASS | 8/10 |
| Test Coverage | CRITICAL | 4/10 |
| Migration Status | WARNING | 6/10 |

**Verdetto Globale:** CHANGES REQUIRED
**Score Totale:** 6.8/10

---

## 1. DATABASE INTEGRITY

### 1.1 Tabelle Revenue Intelligence

| Tabella | Esiste (Code) | Migrazione | Status |
|---------|---------------|------------|--------|
| `pricing_history` | SI | 031 | OK |
| `suggestion_performance` | SI | 031 | OK |
| `ai_model_health` | SI | 032 | OK |
| `suggestion_applications` | SI | 034 | CRITICO - DA VERIFICARE SU VM |
| `pricing_versions` | SI | 034 | DA VERIFICARE SU VM |
| `monitoring_snapshots` | SI | 034 | DA VERIFICARE SU VM |
| `monitoring_notifications` | SI | 035 | DA VERIFICARE SU VM |

### 1.2 Problemi Trovati

#### CRITICAL: Migration 034/035 non applicata su VM

**Severity:** CRITICAL
**File:** `backend/database/migrations/034_action_tracking.sql`
**Problema:** La migrazione 034 crea `suggestion_applications`, `pricing_versions`, `monitoring_snapshots` - tabelle essenziali per l'Action Tracking. Se non applicate, tutto il sistema di monitoring fallisce.

**Come fixare:**
```bash
ssh miracollo-cervella
cd /app/miracollo
python3 backend/database/apply_all_missing_migrations.py
```

**Effort:** 5 minuti

---

### 1.3 Schema Corretto (Verificato)

**pricing_history** (031):
- [x] id, hotel_id, room_type_id, rate_plan_id, stay_date
- [x] old_price, new_price, change_type
- [x] suggestion_id, bucco_id (FK)
- [x] changed_by, changed_at, reason
- [x] occupancy_at_change, adr_at_change, days_to_arrival

**suggestion_performance** (031):
- [x] id, suggestion_id, hotel_id, pricing_history_id
- [x] evaluation_started_at, evaluation_window_hours
- [x] baseline_* metrics, actual_* metrics
- [x] performance_score, performance_status

**suggestion_applications** (034):
- [x] id, suggestion_id, hotel_id, applied_at
- [x] before_snapshot (JSON), changes_applied (JSON)
- [x] pricing_version_id, status
- [x] current_metrics, effectiveness_score

### 1.4 Indici Presenti

**pricing_history:**
- [x] idx_pricing_history_hotel_date
- [x] idx_pricing_history_suggestion
- [x] idx_pricing_history_changed_at
- [x] idx_pricing_history_change_type

**suggestion_performance:**
- [x] idx_sugg_perf_suggestion
- [x] idx_sugg_perf_hotel
- [x] idx_sugg_perf_status
- [x] idx_sugg_perf_pending (parziale)

---

## 2. API ENDPOINTS

### 2.1 Pricing Tracking

| Endpoint | File | Status | Notes |
|----------|------|--------|-------|
| `GET /api/pricing/history` | pricing_tracking.py | OK | Funziona |
| `GET /api/pricing/ai-health` | pricing_tracking.py | OK | Funziona |
| `POST /api/pricing/log-change` | pricing_tracking.py | OK | Internal use |

### 2.2 Revenue Suggestions

| Endpoint | File | Status | Notes |
|----------|------|--------|-------|
| `GET /api/revenue/suggestions` | revenue_suggestions.py | OK | Funziona |
| `POST /api/revenue/suggestions/{id}/action` | revenue_suggestions.py | OK | accept/reject/undo |
| `GET /api/revenue/suggestions/{id}/feedback` | revenue_suggestions.py | OK | Feedback loop |

### 2.3 Revenue Bucchi

| Endpoint | File | Status | Notes |
|----------|------|--------|-------|
| `GET /api/revenue/bucchi` | revenue_bucchi.py | OK | Funziona |
| `GET /api/revenue/research` | revenue_research.py | OK | Booking pace, etc |
| `GET /api/revenue/occupancy-forecast` | revenue_research.py | OK | Forecast |
| `GET /api/revenue/events` | revenue_research.py | OK | Eventi locali |

### 2.4 Action Tracking

| Endpoint | File | Status | Notes |
|----------|------|--------|-------|
| `GET /api/actions/history` | action_tracking_api.py | OK | History tracking |
| `POST /api/actions/apply` | action_tracking_api.py | WARNING | Dipende da tabelle 034 |
| `POST /api/actions/{id}/rollback` | action_tracking_api.py | WARNING | Dipende da tabelle 034 |
| `GET /api/actions/{id}/monitoring` | action_tracking_api.py | WARNING | Dipende da tabelle 034 |

### 2.5 ML Enhancement

| Endpoint | File | Status | Notes |
|----------|------|--------|-------|
| `GET /api/ml/model-info` | ml_api.py | OK | Model metadata |
| `POST /api/ml/what-if` | ml_api.py | OK | Simulazione scenari |
| `POST /api/ml/train` | ml_api.py | OK | Manual retrain |

### 2.6 Problemi Trovati

#### MEDIUM: Error Handling Inconsistente

**Severity:** MEDIUM
**File:** `backend/routers/revenue_suggestions.py` (righe 295-350)
**Problema:** L'INSERT in `suggestion_applications` non ha try/catch robusto. Se tabella non esiste, errore non chiaro.

**Come fixare:**
```python
try:
    conn.execute("INSERT INTO suggestion_applications ...")
except sqlite3.OperationalError as e:
    if "no such table" in str(e):
        logger.error("Table suggestion_applications not found! Run migration 034")
        raise HTTPException(500, "Database migration required")
    raise
```

**Effort:** 15 minuti

---

## 3. FRONTEND-BACKEND SYNC

### 3.1 File Analizzati

- `frontend/js/revenue.js` (1282 righe)

### 3.2 API Calls Match

| Frontend Call | Backend Endpoint | Match |
|---------------|------------------|-------|
| `/api/revenue/bucchi` | revenue_bucchi_router | OK |
| `/api/revenue/suggestions` | revenue_suggestions_router | OK |
| `/api/revenue/occupancy-forecast` | revenue_research_router | OK |
| `/api/revenue/events` | revenue_research_router | OK |
| `/api/revenue/research` | revenue_research_router | OK |
| `/api/pricing/history` | pricing_tracking_router | OK |
| `/api/pricing/ai-health` | pricing_tracking_router | OK |
| `/api/ml/model-info` | ml_api_router | OK |
| `/api/ml/what-if` | ml_api_router | OK |

### 3.3 Response Fields Match

**Bucchi Response:**
- Frontend expects: `bucchi[]`, `summary.totale_bucchi`, `summary.impatto_euro_totale`
- Backend returns: OK

**Suggestions Response:**
- Frontend expects: `suggestions[]` with `id, tipo, azione, motivazione, priorita, confidence_score, confidence_level, suggested_price, bucco_id`
- Backend returns: OK

**Price History Response:**
- Frontend expects: `changes[]` with `changed_at, old_price, new_price, ai_applied, performance_status, revenue_delta_pct`
- Backend returns: OK

### 3.4 Problemi Trovati

#### LOW: console.log di Debug

**Severity:** LOW
**File:** `frontend/js/revenue.js`
**Righe:** 62, 217, 278, 525, 543, 798, 921, 1246
**Problema:** Vari console.log rimasti in produzione.

**Come fixare:**
Rimuovere o condizionare a DEBUG mode:
```javascript
const DEBUG = false;
if (DEBUG) console.log('...');
```

**Effort:** 10 minuti

#### LOW: TODO Rimasto

**Severity:** LOW
**File:** `frontend/js/revenue.js`
**Riga:** 391, 796
**Problema:** `// TODO: get from hotel code mapping` e `// TODO: Implementare logica`

**Come fixare:**
Implementare la mappatura hotel_code -> hotel_id o documentare come feature request.

**Effort:** 30 minuti

---

## 4. CODE QUALITY

### 4.1 File Size Analysis

| File | Righe | Status | Note |
|------|-------|--------|------|
| revenue_suggestions.py | ~450 | OK | Sotto limite 500 |
| revenue_bucchi.py | ~300 | OK | Sotto limite 500 |
| pricing_tracking.py | ~250 | OK | Sotto limite 500 |
| action_tracking_api.py | ~950 | WARNING | Sopra limite! |
| bucchi_engine.py | ~400 | OK | Sotto limite 500 |
| suggerimenti_engine.py | ~350 | OK | Sotto limite 500 |
| confidence_scorer.py | 674 | WARNING | Sopra limite 500 |
| pricing_tracking_service.py | 588 | WARNING | Sopra limite 500 |
| revenue.js (frontend) | 1282 | CRITICAL | TROPPO GRANDE |

### 4.2 Problemi Trovati

#### HIGH: action_tracking_api.py troppo grande

**Severity:** HIGH
**File:** `backend/routers/action_tracking_api.py`
**Righe:** ~950
**Problema:** File sopra il limite di 500 righe. Difficile da mantenere.

**Come fixare:**
Split in:
1. `action_tracking_api.py` - Router endpoints (~300 righe)
2. `action_tracking_service.py` - Business logic (~400 righe)
3. `action_tracking_rollback.py` - Rollback logic (~250 righe)

**Effort:** 2 ore

#### HIGH: revenue.js troppo grande

**Severity:** HIGH
**File:** `frontend/js/revenue.js`
**Righe:** 1282
**Problema:** File MOLTO sopra il limite di 500 righe.

**Come fixare:**
Split in:
1. `revenue-core.js` - Init, config, helpers (~200 righe)
2. `revenue-bucchi.js` - Bucchi rendering (~200 righe)
3. `revenue-suggestions.js` - Suggestions + what-if (~300 righe)
4. `revenue-charts.js` - Timeline, pace, charts (~300 righe)
5. `revenue-actions.js` - Apply, undo, monitoring (~280 righe)

**Effort:** 3 ore

#### MEDIUM: confidence_scorer.py sopra limite

**Severity:** MEDIUM
**File:** `backend/ml/confidence_scorer.py`
**Righe:** 674
**Problema:** Sopra limite di 500 righe ma contiene logica coesa.

**Come fixare:**
Split in:
1. `confidence_scorer.py` - Main calculation (~350 righe)
2. `confidence_components.py` - Individual components (~200 righe)
3. `confidence_utils.py` - Utilities (~124 righe)

**Effort:** 1 ora

### 4.3 Type Hints

| File | Type Hints | Status |
|------|------------|--------|
| pricing_tracking_service.py | 100% | OK |
| confidence_scorer.py | 95% | OK |
| suggerimenti_engine.py | 90% | OK |
| bucchi_engine.py | 85% | OK |
| action_tracking_api.py | 80% | OK |

### 4.4 Docstrings

| File | Docstrings | Status |
|------|------------|--------|
| confidence_scorer.py | EXCELLENT | OK |
| pricing_tracking_service.py | EXCELLENT | OK |
| suggerimenti_engine.py | GOOD | OK |
| bucchi_engine.py | GOOD | OK |
| action_tracking_api.py | BASIC | IMPROVE |

---

## 5. TEST COVERAGE

### 5.1 Test Esistenti

| File | Righe | Coverage Stimata |
|------|-------|------------------|
| test_revenue_intelligence.py | ~200 | 30% |

### 5.2 Cosa NON e Testato

#### CRITICAL: Missing Tests

**Severity:** CRITICAL
**Problema:** Coverage stimata ~30%. Manca testing su:

1. **pricing_tracking_service.py**
   - `log_price_change()` - nessun test
   - `start_performance_evaluation()` - nessun test
   - `complete_evaluation()` - nessun test
   - `calculate_performance_score()` - nessun test

2. **confidence_scorer.py**
   - `calculate_confidence()` - nessun test
   - `get_model_variance_confidence()` - nessun test
   - `get_acceptance_rate()` - nessun test

3. **action_tracking_api.py**
   - Rollback flow - nessun test
   - Monitoring snapshots - nessun test
   - Pause/resume - nessun test

4. **Edge Cases mancanti:**
   - Empty database
   - Invalid hotel_id
   - Missing suggestions
   - Concurrent updates
   - Rollback di rollback

**Come fixare:**
Creare `test_pricing_tracking.py`:
```python
def test_log_price_change():
    # Setup test DB
    # Call log_price_change()
    # Verify record created
    pass

def test_performance_evaluation_window():
    # Test finestre 6h, 24h, 168h
    pass

def test_calculate_performance_score():
    # Test SUCCESS, NEUTRAL, WARNING, FAILURE
    pass
```

**Effort:** 8 ore per coverage 70%+

---

## 6. MIGRATION STATUS

### 6.1 Migrazioni Revenue Intelligence

| ID | File | Tabelle | Status Code | Status VM |
|----|------|---------|-------------|-----------|
| 026 | revenue_targets.sql | revenue_targets | OK | DA VERIFICARE |
| 027 | revenue_suggestions.sql | revenue_suggestions | OK | DA VERIFICARE |
| 028 | revenue_research.sql | occupancy_forecast | OK | DA VERIFICARE |
| 029 | performance_indexes.sql | Indici | OK | DA VERIFICARE |
| 030 | optimized_trigger.sql | Triggers | OK | DA VERIFICARE |
| 031 | pricing_tracking.sql | pricing_history, suggestion_performance, ai_model_health | OK | APPLICATA |
| 032 | ai_model_health.sql | ai_model_health ext | OK | DA VERIFICARE |
| 033 | ab_testing.sql | ab_tests | OK | DA VERIFICARE |
| 034 | action_tracking.sql | suggestion_applications, pricing_versions, monitoring_snapshots | OK | CRITICO - DA APPLICARE |
| 035 | notifications.sql | monitoring_notifications | OK | CRITICO - DA APPLICARE |

### 6.2 Schema Version

**Expected:** 1.9.0+ (dopo 031)
**Actual VM:** DA VERIFICARE

### 6.3 Problemi Trovati

#### CRITICAL: Migrazioni 034-035 probabilmente mancanti su VM

**Severity:** CRITICAL
**Problema:** L'audit precedente indica che tabella `suggestion_applications` non esiste su VM.

**Come verificare:**
```bash
ssh miracollo-cervella
sqlite3 /app/miracollo/backend/database/miracollo.db
.tables
# Cercare: suggestion_applications, pricing_versions, monitoring_snapshots
```

**Come fixare:**
```bash
cd /app/miracollo
python3 backend/database/apply_all_missing_migrations.py
# Oppure manualmente:
sqlite3 backend/database/miracollo.db < backend/database/migrations/034_action_tracking.sql
sqlite3 backend/database/miracollo.db < backend/database/migrations/035_notifications.sql
```

**Effort:** 10 minuti

---

## 7. RIEPILOGO PROBLEMI

### CRITICAL (Blocca funzionalita)

| # | Problema | File | Effort |
|---|----------|------|--------|
| 1 | Migration 034-035 non applicate su VM | migrations/ | 10 min |
| 2 | Test coverage <30% | tests/ | 8 ore |

### HIGH (Degrada qualita)

| # | Problema | File | Effort |
|---|----------|------|--------|
| 3 | action_tracking_api.py >500 righe | routers/ | 2 ore |
| 4 | revenue.js >500 righe | frontend/js/ | 3 ore |

### MEDIUM (Miglioramento)

| # | Problema | File | Effort |
|---|----------|------|--------|
| 5 | confidence_scorer.py >500 righe | ml/ | 1 ora |
| 6 | Error handling inconsistente | revenue_suggestions.py | 15 min |

### LOW (Polish)

| # | Problema | File | Effort |
|---|----------|------|--------|
| 7 | console.log di debug | revenue.js | 10 min |
| 8 | TODO rimasti | revenue.js | 30 min |

---

## 8. PIANO FIX RACCOMANDATO

### Fase 1: URGENT (Oggi)
1. Verificare e applicare migration 034-035 su VM
2. Testare che Action Tracking funzioni

### Fase 2: HIGH PRIORITY (Questa settimana)
3. Split action_tracking_api.py
4. Split revenue.js
5. Creare test base per pricing_tracking_service

### Fase 3: MEDIUM PRIORITY (Prossima settimana)
6. Split confidence_scorer.py
7. Migliorare error handling
8. Aumentare test coverage a 70%

### Fase 4: LOW PRIORITY (Quando possibile)
9. Rimuovere console.log
10. Risolvere TODO

---

## 9. CONCLUSIONE

Il sistema Revenue Intelligence e **funzionalmente completo** nel codice, con:
- API ben strutturate
- Frontend-Backend sincronizzati
- ML confidence scoring implementato
- Action tracking con rollback

**Problemi principali:**
1. **Migrazioni non applicate su VM** - Risolvere SUBITO
2. **Test coverage insufficiente** - Rischio alto per produzione
3. **File troppo grandi** - Difficili da mantenere

**Verdetto:** CHANGES REQUIRED prima di considerare production-ready.

---

*Report generato da Cervella Guardiana Qualita*
*"Qualita non e optional. E la BASELINE."*
