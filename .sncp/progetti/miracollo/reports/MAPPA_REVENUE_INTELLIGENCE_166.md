# MAPPA COMPLETA - REVENUE INTELLIGENCE SYSTEM
## Auditoria Sessione 166 - 11 Gennaio 2026

**Analista:** Cervella-Ingegnera  
**Status:** ⚠️ PROBLEMI IDENTIFICATI  
**Health Score:** 6/10

---

## EXECUTIVE SUMMARY

### Problema Identificato
**404 su `/api/revenue/suggestions`** - Frontend chiama endpoint, backend risponde 404.

### Causa Root
Router registrato in `main.py` ma potrebbero esserci problemi di:
- Prefisso duplicato
- Import errato
- Conflitto di route

### Sistema Mappato
- **64 file backend** coinvolti nel sistema Revenue Intelligence
- **140 file frontend** con pattern revenue/pricing/tracking
- **6 router API** principali
- **3 servizi core** (bucchi, suggerimenti, actions)
- **8+ tabelle database** per tracking e ML

---

## BACKEND - FILE STRUCTURE

### 📁 ROUTERS (API Endpoints)

| File | Righe | Prefisso | Endpoints | Status |
|------|-------|----------|-----------|--------|
| `revenue_bucchi.py` | 205 | `/api/revenue` | `GET /bucchi`, `GET /occupancy-forecast` | ✅ OK |
| `revenue_suggestions.py` | 341 | `/api/revenue` | `GET /suggestions`, `POST /suggestions/{id}/action` | ⚠️ 404 |
| `revenue_research.py` | 234 | `/api/revenue` | `GET /research`, `GET /research/status`, `GET /events`, `POST /events` | ❓ Da testare |
| `pricing_tracking.py` | 587 | `/api/pricing` | `GET /history`, `POST /history`, `GET /suggestions/{id}/performance`, `GET /ai-health` | ❓ Da testare |
| `ml_api.py` | ? | ? | ML endpoints | ❓ Da verificare |
| `notifications_api.py` | ? | ? | Notification endpoints | ❓ Da verificare |

**⚠️ PROBLEMA CRITICO:** Due router usano stesso prefisso `/api/revenue`:
- `revenue_bucchi.py`
- `revenue_suggestions.py`
- `revenue_research.py`

Possibile conflitto di route!

### 📁 SERVICES (Business Logic)

| File | Righe | Responsabilità | Dipendenze |
|------|-------|----------------|------------|
| `bucchi_engine.py` | 479 | Identifica periodi sotto target | `database`, `datetime` |
| `suggerimenti_engine.py` | 404 | Genera suggerimenti AI da bucchi | `bucchi_engine`, `ml/confidence_scorer` |
| `suggerimenti_actions.py` | 489 | **ESEGUE azioni** (modifica prezzi) | `database`, `suggerimenti_engine` |
| `pricing_tracking_service.py` | 587 | Traccia modifiche prezzi | `database` |
| `pricing_performance_scheduler.py` | 209 | Valuta performance suggerimenti | `database`, `scheduler` |
| `metrics_calculator.py` | ? | Calcola metriche revenue | ? |
| `notification_worker.py` | ? | Worker notifiche | ? |
| `research_orchestrator.py` | ? | Orchestrazione ricerca eventi | ? |

### 📁 ML (Machine Learning)

| File | Righe | Responsabilità | Criticità |
|------|-------|----------------|-----------|
| `model_trainer.py` | 733 | **CRITICO** - Addestra modelli ML | ALTO |
| `ml_scheduler.py` | 687 | Scheduler training automatico | ALTO |
| `confidence_scorer.py` | 673 | Calcola confidence score suggerimenti | ALTO |
| `data_preparation.py` | 495 | Prepara dataset per training | MEDIO |
| `feature_engineering.py` | 496 | Feature extraction | MEDIO |

**⚠️ FILE GRANDI:** 5 file > 500 righe = candidati per refactoring!

### 📁 DATABASE MIGRATIONS

| Migration | File | Tabelle Create | Status |
|-----------|------|----------------|--------|
| 010 | `autopilot.sql` | `autopilot_config`, `autopilot_log`, `autopilot_rules` | ✅ Applicata |
| 016 | `suggestion_feedback.sql` | `suggestion_feedback` | ✅ Applicata |
| 026 | `revenue_targets.sql` | ? | ❓ Da verificare |
| 027 | `revenue_suggestions.sql` | `suggestion_applications`, `pricing_versions` | ❓ Da verificare |
| 028 | `revenue_research.sql` | ? | ❓ Da verificare |
| 031 | `pricing_tracking.sql` | `pricing_history`, `pricing_changes` | ❓ Da verificare |
| 032 | `ai_model_health.sql` | ? | ❓ Da verificare |
| 034 | `action_tracking.sql` | ? | ❓ Da verificare |
| 035 | `notifications.sql` | ? | ❓ Da verificare |

---

## FRONTEND - FILE STRUCTURE

### 📁 CORE FILES

| File | Righe | Responsabilità | Chiamate API |
|------|-------|----------------|--------------|
| `revenue.html` | 216 | Dashboard Revenue Intelligence | - |
| `js/revenue.js` | 1281 | **CRITICO** - Logica dashboard | `GET /api/revenue/suggestions`, `GET /api/revenue/bucchi`, `POST /api/revenue/suggestions/{id}/action` |
| `css/revenue.css` | ? | Stili dashboard | - |
| `js/action-tracking.js` | ? | Traccia azioni utente | ? |
| `js/notifications.js` | ? | Sistema notifiche | ? |
| `js/monitoring.js` | ? | Monitoring dashboard | ? |
| `js/ml-dashboard.js` | ? | Dashboard ML | ? |
| `js/ab-testing.js` | ? | A/B Testing UI | ? |

**⚠️ FILE GRANDE:** `revenue.js` ha 1281 righe = split suggerito!

### 📁 HTML PAGES

- `revenue.html` - Revenue Intelligence Dashboard
- `revenue_test.html` - Pagina test
- `ab-testing.html` - A/B Testing
- `monitoring.html` - Monitoring
- `action-history.html` - Storico azioni

### 📁 CSS

- `css/revenue.css` - Stili Revenue
- `css/action-tracking.css` - Stili tracking
- `css/notifications.css` - Stili notifiche
- `css/monitoring.css` - Stili monitoring
- `css/ml-dashboard.css` - Stili ML dashboard

---

## API ENDPOINTS COMPLETI

### 🔵 `/api/revenue` (Revenue Intelligence)

| Endpoint | Method | Router | Funzione | Status |
|----------|--------|--------|----------|--------|
| `/bucchi` | GET | `revenue_bucchi` | Lista bucchi per finestra | ✅ OK |
| `/occupancy-forecast` | GET | `revenue_bucchi` | Forecast occupancy | ✅ OK |
| `/suggestions` | GET | `revenue_suggestions` | **Lista suggerimenti AI** | ⚠️ **404** |
| `/suggestions/{id}/action` | POST | `revenue_suggestions` | **Applica/Rifiuta suggerimento** | ⚠️ **404** |
| `/research` | GET | `revenue_research` | Ricerca automatica | ❓ Da testare |
| `/research/status` | GET | `revenue_research` | Status ricerca | ❓ Da testare |
| `/events` | GET | `revenue_research` | Lista eventi locali | ❓ Da testare |
| `/events` | POST | `revenue_research` | Aggiungi evento | ❓ Da testare |

### 🟢 `/api/pricing` (Pricing Tracking)

| Endpoint | Method | Router | Funzione | Status |
|----------|--------|--------|----------|--------|
| `/history` | GET | `pricing_tracking` | Storico modifiche prezzi | ❓ Da testare |
| `/history` | POST | `pricing_tracking` | Registra modifica | ❓ Da testare |
| `/suggestions/{id}/performance` | GET | `pricing_tracking` | Performance suggerimento | ❓ Da testare |
| `/ai-health` | GET | `pricing_tracking` | Health modelli AI | ❓ Da testare |

---

## DATABASE SCHEMA

### Tabelle Revenue Intelligence

```
suggestion_feedback
├── id (PK)
├── hotel_id (FK -> hotels)
├── suggestion_id (TEXT)
├── bucco_id (TEXT)
├── tipo (TEXT)
├── azione (TEXT: accept/reject/snooze)
├── motivo_reject (TEXT)
└── created_at (TIMESTAMP)

suggestion_applications (da migration 027)
├── id (PK)
├── suggestion_id
├── hotel_id (FK)
├── suggestion_type
├── suggestion_action
├── bucco_id
├── before_snapshot (JSON)
├── changes_applied (JSON)
├── pricing_version_id (FK)
├── status (active/completed/rolled_back)
├── monitoring_start (DATE)
└── evaluation_period_days (INT)

pricing_versions (da migration 027)
├── version_id (PK)
├── hotel_id (FK)
├── date_range_start
├── date_range_end
├── previous_prices (JSON)
├── new_prices (JSON)
├── is_rollback (BOOL)
└── created_at (TIMESTAMP)

pricing_history (da migration 031)
├── id (PK)
├── hotel_id (FK)
├── date (DATE)
├── room_type_id (FK)
├── old_price (DECIMAL)
├── new_price (DECIMAL)
├── change_reason (TEXT)
├── changed_by (TEXT: system/user)
└── created_at (TIMESTAMP)

autopilot_config (da migration 010)
├── hotel_id (PK, FK)
├── enabled (BOOL)
├── min_confidence (INT)
├── run_frequency (TEXT)
├── notification_channels (JSON)
└── updated_at (TIMESTAMP)

autopilot_log (da migration 010)
├── id (PK)
├── hotel_id (FK)
├── execution_time (TIMESTAMP)
├── suggestions_generated (INT)
├── actions_taken (INT)
├── success (BOOL)
└── details (JSON)

autopilot_rules (da migration 010)
├── id (PK)
├── hotel_id (FK)
├── rule_type (TEXT)
├── conditions (JSON)
├── action (JSON)
├── enabled (BOOL)
└── created_at (TIMESTAMP)
```

---

## DIAGRAMMA CONNESSIONI

```
FRONTEND (revenue.html)
    │
    ├─[1]─> revenue.js
    │        │
    │        ├─ API: GET /api/revenue/suggestions  ──> ⚠️ 404 ERROR
    │        ├─ API: GET /api/revenue/bucchi        ──> ✅ OK
    │        └─ API: POST /api/revenue/suggestions/{id}/action ──> ⚠️ 404 ERROR
    │
    ├─[2]─> action-tracking.js
    │        └─ Traccia azioni utente
    │
    └─[3]─> notifications.js
             └─ Sistema notifiche

BACKEND (main.py)
    │
    ├─ app.include_router(revenue_bucchi_router)      ✅ Registrato
    ├─ app.include_router(revenue_suggestions_router) ⚠️ Registrato ma 404
    ├─ app.include_router(revenue_research_router)    ❓ Da verificare
    └─ app.include_router(pricing_tracking_router)    ❓ Da verificare

ROUTERS
    │
    ├─ revenue_bucchi.py (prefix: /api/revenue)
    │   └─> bucchi_engine.py
    │        ├─ calcola_target()
    │        ├─ calcola_occupancy_prevista()
    │        └─ trova_bucchi()
    │
    ├─ revenue_suggestions.py (prefix: /api/revenue) ⚠️ PROBLEMA
    │   └─> suggerimenti_engine.py
    │        ├─ genera_tutti_suggerimenti()
    │        └─> confidence_scorer.py (ML)
    │             └─ calcola_confidence()
    │   └─> suggerimenti_actions.py
    │        └─ execute_suggestion_action()
    │             └─ Modifica daily_rates (AZIONE REALE!)
    │
    └─ pricing_tracking.py (prefix: /api/pricing)
         └─> pricing_tracking_service.py
              └─ Traccia modifiche prezzi

ML PIPELINE
    │
    ├─ ml_scheduler.py
    │   └─ Scheduler automatico training
    │
    ├─ model_trainer.py
    │   ├─> data_preparation.py
    │   ├─> feature_engineering.py
    │   └─ Addestra modelli
    │
    └─ confidence_scorer.py
         └─ Usato da suggerimenti_engine
```

---

## ISSUES IDENTIFICATI

### 🔴 CRITICI (blocca funzionalità)

1. **404 su `/api/revenue/suggestions`**
   - Frontend: `revenue.js:145` chiama `GET /api/revenue/suggestions`
   - Backend: Router definito in `revenue_suggestions.py:50`
   - Causa: Da investigare (conflitto prefissi? import errato?)
   - File: `backend/routers/revenue_suggestions.py`
   - Impact: Dashboard Revenue NON funziona

### 🟠 ALTO (tech debt importante)

2. **File ML troppo grandi**
   - `model_trainer.py`: 733 righe
   - `ml_scheduler.py`: 687 righe
   - `confidence_scorer.py`: 673 righe
   - `pricing_tracking_service.py`: 587 righe
   - Suggerimento: Split in moduli più piccoli

3. **Frontend revenue.js troppo grande**
   - `revenue.js`: 1281 righe
   - Suggerimento: Split in:
     - `revenue-bucchi.js`
     - `revenue-suggestions.js`
     - `revenue-api-client.js`
     - `revenue-ui.js`

### 🟡 MEDIO (miglioramenti)

4. **Stesso prefisso `/api/revenue` per 3 router**
   - `revenue_bucchi.py`
   - `revenue_suggestions.py`
   - `revenue_research.py`
   - Possibile conflitto route
   - Suggerimento: Verifica ordine registrazione in `main.py`

5. **Migrations non tutte verificate**
   - 026, 027, 028, 031, 032, 034, 035
   - Alcune potrebbero non essere applicate
   - Suggerimento: Verifica schema_version nel database

6. **Test coverage sconosciuta**
   - Test file non trovati in `/backend/tests/`
   - Solo `test_revenue_intelligence.py` menzionato
   - Suggerimento: Creare test suite completa

### 🟢 BASSO (nice to have)

7. **Documentazione API incompleta**
   - README files esistenti ma non centralizzati
   - Suggerimento: Swagger/OpenAPI documentation

8. **Performance monitoring**
   - Sistema esiste (`ai_model_health`, `pricing_tracking`)
   - Ma non chiaro se attivo
   - Suggerimento: Dashboard monitoring dedicata

---

## RACCOMANDAZIONI PRIORITIZZATE

### 1. [CRITICO] Fix 404 su `/api/revenue/suggestions`
**Priority:** P0 - BLOCCA TUTTO  
**Effort:** 1-2 ore  
**Azioni:**
- [ ] Verifica import in `main.py` (riga 96-98)
- [ ] Verifica ordine registrazione router
- [ ] Test endpoint con curl/Postman
- [ ] Check logs backend per errori startup
- [ ] Verifica prefisso non duplicato

### 2. [ALTO] Verifica migrations database
**Priority:** P1 - IMPORTANTE  
**Effort:** 30 min  
**Azioni:**
- [ ] Query `SELECT * FROM schema_version ORDER BY version`
- [ ] Applica migrations mancanti (026-035)
- [ ] Verifica tabelle esistenti vs schema atteso

### 3. [ALTO] Test endpoints `/api/pricing`
**Priority:** P1 - IMPORTANTE  
**Effort:** 1 ora  
**Azioni:**
- [ ] Test GET `/api/pricing/history`
- [ ] Test GET `/api/pricing/ai-health`
- [ ] Verifica integrazione con ML pipeline

### 4. [MEDIO] Split file grandi
**Priority:** P2 - BACKLOG  
**Effort:** 4-6 ore (per file)  
**Azioni:**
- [ ] `revenue.js` (1281 righe) → split in 4 moduli
- [ ] `model_trainer.py` (733 righe) → extract helpers
- [ ] `ml_scheduler.py` (687 righe) → separate schedulers
- [ ] `confidence_scorer.py` (673 righe) → extract scorers
- [ ] `pricing_tracking_service.py` (587 righe) → split tracking/reporting

### 5. [BASSO] Documentazione API
**Priority:** P3 - NICE TO HAVE  
**Effort:** 2-3 ore  
**Azioni:**
- [ ] Aggiungi docstring OpenAPI a tutti endpoint
- [ ] Genera Swagger UI
- [ ] README centrale con esempi curl

---

## METRICHE FINALI

```
BACKEND
├── File Python totali:    64
├── Righe codice totali:   54,611
├── Router:                6
├── Services:              9+
├── ML files:              5
├── File > 500 righe:      5 ⚠️
└── File > 1000 righe:     0 ✅

FRONTEND
├── File totali:           140
├── HTML pages:            6
├── JS files:              30+
├── CSS files:             10+
├── File > 1000 righe:     1 (revenue.js) ⚠️
└── Chiamate API:          4+ endpoint

DATABASE
├── Migrations totali:     32
├── Tabelle Revenue:       8+
├── Indici:                10+
└── Migrations da verificare: 7

API ENDPOINTS
├── /api/revenue:          8 endpoints
├── /api/pricing:          4 endpoints
├── Funzionanti:           2 ✅
├── 404 Error:             2 ⚠️
└── Da testare:            10 ❓
```

---

## NEXT STEPS

**IMMEDIATI (oggi):**
1. Fix 404 su `/api/revenue/suggestions` - CRITICO!
2. Test endpoint con curl
3. Verifica logs backend

**BREVE TERMINE (questa settimana):**
4. Verifica migrations database
5. Test completo tutti endpoint `/api/revenue` e `/api/pricing`
6. Crea test suite basica

**LUNGO TERMINE (backlog):**
7. Refactor file grandi (revenue.js, model_trainer.py)
8. Documentazione OpenAPI completa
9. Dashboard monitoring ML

---

## APPENDICE A - COMANDI UTILI

### Verifica Router Registrati
```bash
grep "include_router" /Users/rafapra/Developer/miracollogeminifocus/backend/main.py
```

### Test Endpoint
```bash
# Test bucchi (dovrebbe funzionare)
curl http://localhost:8000/api/revenue/bucchi?hotel_code=NL&finestra=1_settimana

# Test suggestions (404 attualmente)
curl http://localhost:8000/api/revenue/suggestions?hotel_code=NL
```

### Verifica Migrations
```bash
sqlite3 backend/database/miracollo.db "SELECT * FROM schema_version ORDER BY version;"
```

### Conta File Grandi
```bash
find backend -name "*.py" -exec wc -l {} \; | awk '$1 > 500 {print}' | sort -rn
```

---

**Report creato da:** Cervella-Ingegnera  
**Data:** 11 Gennaio 2026, 17:30  
**Versione:** 1.0  
**Prossima azione:** Fix 404 suggerimenti endpoint

*"Analizza e propone, NON modifica!"*
