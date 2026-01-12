# ROADMAP: Revenue Intelligence da 7/10 a 10/10

**Data:** 12 Gennaio 2026
**Autore:** Cervella Guardiana Qualita
**Progetto:** Miracollo Revenue Intelligence
**Status:** ACTIONABLE

---

## EXECUTIVE SUMMARY

**Stato Attuale:** 7/10
- Backend API funzionanti (bucchi, suggestions, price history, applications, AI health)
- Frontend split completato (5 file, 1290 righe)
- 63 test passati
- GAP #1 (Price History) RISOLTO
- GAP #2 (Modal Preview) FIX applicato, DA TESTARE

**Target:** 10/10
- Sistema stabile con monitoring
- ML Enhancement (GAP #3) implementato
- What-If Simulator (GAP #4) attivo
- Test coverage >80%
- Documentazione completa

**Timeline:** 2-3 mesi per 10/10 completo

---

## FASE 1: IMMEDIATA (Settimana 1)

### Obiettivo
Stabilizzare cio che esiste e verificare fix GAP #2.

### Task 1.1: Test Manuale GAP #2 Modal Preview
**Effort:** 2-3 ore
**Owner:** cervella-tester
**Metriche Successo:**
- [ ] Modal apre correttamente con dati application
- [ ] Campi title, property_name, expected_impact visibili
- [ ] Bottoni "Accetta"/"Rifiuta" funzionanti
- [ ] Nessun errore console

**Rischi:**
- Backend potrebbe restituire campi diversi da quelli attesi
- Mitigazione: Log dettagliato su API response

### Task 1.2: RateBoard Hard Tests
**Effort:** 4-5 ore
**Owner:** cervella-tester
**Metriche Successo:**
- [ ] Test con 100+ date range diverse
- [ ] Test con property senza dati competitor
- [ ] Test con bucchi vuoti
- [ ] Test con suggestions vuote
- [ ] Latency API <500ms per tutte le chiamate

**Test specifici:**
```
1. /api/revenue/bucchi/{property_id}
   - property esistente: 200 OK, JSON valido
   - property inesistente: 404 o 200 vuoto (definire)
   - date range > 90 giorni: warning o limit

2. /api/revenue/suggestions/{property_id}
   - con suggestions attive: array non vuoto
   - senza suggestions: array vuoto (non errore)
   - suggestion scaduta: non inclusa

3. /api/revenue/price-history/{property_id}
   - 50 record: OK
   - 500 record: latency <1s
   - filtro per date: funzionante
```

### Task 1.3: Fix Bug Trovati
**Effort:** 4-8 ore (dipende da quanti)
**Owner:** cervella-backend + cervella-frontend
**Metriche Successo:**
- [ ] Tutti i bug trovati in 1.1/1.2 risolti
- [ ] Test ripetuti: PASS

### Task 1.4: formatDateRange Verification
**Effort:** 1 ora
**Owner:** cervella-frontend
**Metriche Successo:**
- [ ] Funzione presente in revenue-core.js
- [ ] Chiamata in revenue-bucchi.js funziona
- [ ] Nessun ReferenceError in console

---

## FASE 2: STABILIZZAZIONE (Settimana 2-3)

### Obiettivo
Infrastruttura production-ready con monitoring.

### Task 2.1: docker-compose.prod.yml
**Effort:** 8-10 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] docker-compose.prod.yml creato e testato
- [ ] Backend + DB + Nginx in un unico compose
- [ ] Health checks configurati
- [ ] Restart policy: always
- [ ] Logs persistenti (volume montato)

**Contenuto minimo:**
```yaml
version: '3.8'
services:
  backend:
    image: miracollo-backend:latest
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=${DATABASE_URL}

  db:
    image: postgres:15
    restart: always
    volumes:
      - pgdata:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
```

### Task 2.2: Monitoring Dashboard
**Effort:** 10-12 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Endpoint /metrics con Prometheus format
- [ ] Metriche: requests/sec, latency p50/p95/p99, errors/sec
- [ ] Grafana dashboard (o alternativa)
- [ ] Alert email se errori >5%

**Metriche da tracciare:**
| Metrica | Tipo | Soglia Alert |
|---------|------|--------------|
| api_requests_total | Counter | - |
| api_latency_seconds | Histogram | p99 >2s |
| api_errors_total | Counter | >5% |
| db_connections | Gauge | >80% pool |
| ml_predictions_total | Counter | - |
| ml_accuracy_rolling | Gauge | <70% |

### Task 2.3: Error Tracking Migliorato
**Effort:** 4-6 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Sentry o alternativa integrato
- [ ] Errori raggruppati per tipo
- [ ] Context (user_id, property_id) incluso
- [ ] Alert Slack/email per errori critici

**Rischi:**
- Sentry ha costi se volumi alti
- Mitigazione: usare sampling 10% in produzione, 100% in dev

### Task 2.4: Test Coverage 80%+
**Effort:** 12-15 ore
**Owner:** cervella-tester
**Metriche Successo:**
- [ ] 63 test attuali passano su VM (non solo simulati)
- [ ] +20 test nuovi per edge cases
- [ ] Coverage misurata con pytest-cov: >80%
- [ ] CI/CD pipeline con test automatici

**Aree da coprire:**
```
- [ ] revenue_api.py: 15 test
- [ ] pricing_tracking_service.py: 20 test
- [ ] confidence_scorer.py: 25 test
- [ ] action_tracking (tutti i 10 endpoint): 30 test
- [ ] Integration test API->DB->Response: 10 test
```

---

## FASE 3: ENHANCEMENT - What-If Simulator MVP (Settimana 4-6)

### Obiettivo
Implementare What-If Simulator base (GAP #4) per dare valore SUBITO agli utenti.

### Task 3.1: Backend API What-If
**Effort:** 30-35 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] POST /api/v1/what-if/simulate funzionante
- [ ] Calcolo elasticity-based (formula semplice)
- [ ] Response <300ms uncached, <50ms cached
- [ ] Explanation text generato

**Endpoint spec:**
```python
# Request
POST /api/v1/what-if/simulate
{
    "property_id": 42,
    "date_target": "2026-01-20",
    "room_type_id": 3,
    "price_adjustment": 0.10  # +10%
}

# Response
{
    "predicted_occupancy": 0.75,
    "occupancy_delta": -0.03,
    "predicted_revenue": 9000.00,
    "revenue_delta": 450.00,
    "competitor_position": "match",
    "confidence": "medium",
    "explanation": "Con prezzo +10%, prevedo..."
}
```

### Task 3.2: Caching What-If
**Effort:** 8-10 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Cache PostgreSQL o Redis
- [ ] TTL 1 ora
- [ ] Cache hit rate >60%
- [ ] Cleanup automatico (cron ogni 30min)

### Task 3.3: Frontend What-If UI
**Effort:** 40-50 ore
**Owner:** cervella-frontend
**Metriche Successo:**
- [ ] Componente WhatIfSimulator in pagina revenue
- [ ] Slider prezzo con debounce 300ms
- [ ] Cards KPI (occupancy, revenue, competitor pos)
- [ ] Grafico price vs occupancy (Recharts o Chart.js)
- [ ] Mobile responsive

**Wireframe:**
```
+------------------------------------------+
| What-If Simulator                        |
+------------------------------------------+
| Property: [Dropdown]  Date: [Picker]     |
|                                          |
| Current Price: EUR120                    |
| EUR80 [====O=======] EUR180              |
|       -33%    +10%      +50%             |
+------------------------------------------+
| OCCUPANCY    | REVENUE     | COMPETITOR  |
| 82% (+4%)    | EUR9840     | Match       |
|   [OK]       | (+EUR480)   |             |
+------------------------------------------+
| Chart: Price vs Occupancy curve          |
| [grafico interattivo]                    |
+------------------------------------------+
| Explanation:                             |
| "Con prezzo +10%, prevedo occupancy..."  |
+------------------------------------------+
```

### Task 3.4: Test What-If
**Effort:** 8-10 ore
**Owner:** cervella-tester
**Metriche Successo:**
- [ ] 15 test backend (API, caching, edge cases)
- [ ] 10 test frontend (E2E con Playwright)
- [ ] Test performance: 100 request/sec

---

## FASE 4: ENHANCEMENT - ML Database Foundation (Settimana 7-8)

### Obiettivo
Preparare infrastruttura per ML training (GAP #3).

### Task 4.1: Database Schema ML
**Effort:** 20-25 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Tabella ai_pricing_decisions creata
- [ ] Tabella ml_training_runs creata
- [ ] Tabella ml_model_metrics creata
- [ ] Partitioning mensile attivo
- [ ] Migration Alembic pronta

**Schema chiave:**
```sql
CREATE TABLE ai_pricing_decisions (
    id BIGSERIAL PRIMARY KEY,
    property_id BIGINT NOT NULL,
    date_target DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    features JSONB NOT NULL,
    suggested_price DECIMAL(10,2),
    user_decision VARCHAR(20),
    final_price DECIMAL(10,2),
    outcome_occupancy DECIMAL(3,2),
    outcome_revenue DECIMAL(10,2),
    outcome_evaluated_at TIMESTAMP
) PARTITION BY RANGE (created_at);
```

### Task 4.2: API Tracking Decisioni
**Effort:** 15-20 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] POST /api/v1/pricing/decide implementato
- [ ] Ogni suggerimento ML viene tracciato
- [ ] Decisione utente (accept/reject/modify) salvata
- [ ] Latency <50ms

### Task 4.3: Feature Engineering Base
**Effort:** 30-35 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Funzione build_features() implementata
- [ ] 8 features MVP estratte (occupancy, pace, competitor, etc.)
- [ ] Features salvate in JSON nella tabella decisioni
- [ ] Latency <200ms

**Features MVP:**
```
1. occupancy_rate (0.0-1.0)
2. booking_pace_7d (count)
3. lead_time_days (int)
4. day_of_week (0-6)
5. season (high/low)
6. competitor_avg_price (EUR)
7. historical_revpar (EUR)
8. current_price_acceptance_rate (0.0-1.0)
```

---

## FASE 5: ADVANCED - ML Model Training (Mese 2-3)

### Obiettivo
Primo modello ML funzionante.

### Task 5.1: XGBoost Model Training
**Effort:** 40-50 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Training script funzionante
- [ ] Accuracy (R2) >70% su test set
- [ ] MAE <EUR15
- [ ] Model versioning attivo

**Rischi:**
- Samples insufficienti (<500)
- Mitigazione: usare synthetic data per bootstrap, aspettare raccolta dati reali

### Task 5.2: API /pricing/suggest
**Effort:** 15-20 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Suggerimento ML restituito
- [ ] Confidence score incluso
- [ ] Explanation generata
- [ ] Latency <100ms

### Task 5.3: Feedback Loop Prevention
**Effort:** 20-25 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Delayed evaluation (60 giorni) implementato
- [ ] Exploration 15% attivo
- [ ] Sample weighting (accept=1.0, reject=0.3)
- [ ] Monitoring feedback loop metrics

### Task 5.4: Retraining Automatico
**Effort:** 20-25 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Celery Beat schedule ogni 14 giorni
- [ ] Auto-deployment se nuovo model migliore
- [ ] Rollback se performance peggiora
- [ ] Alert se retraining fallisce

### Task 5.5: Drift Monitoring
**Effort:** 20-25 ore
**Owner:** cervella-backend
**Metriche Successo:**
- [ ] Evidently AI integrato
- [ ] Daily drift check
- [ ] Alert se drift >30%
- [ ] Dashboard drift metrics

---

## RISCHI E MITIGAZIONI

### Rischi Tecnici

| Rischio | Prob | Impatto | Mitigazione |
|---------|------|---------|-------------|
| Samples ML insufficienti | ALTA | ALTO | Synthetic data + aspettare raccolta |
| Container legacy su VM | MEDIA | ALTO | docker-compose.prod.yml |
| Test non eseguibili su VM | MEDIA | MEDIO | Adattare import, verificare schema |
| Performance What-If lenta | BASSA | MEDIO | Caching aggressivo |

### Rischi Business

| Rischio | Prob | Impatto | Mitigazione |
|---------|------|---------|-------------|
| Utenti non fidano ML | ALTA | CRITICO | Explainability, confidence, override |
| What-If non usato | MEDIA | ALTO | Onboarding, UX iterazione |
| Revenue managers preferiscono manuale | MEDIA | MEDIO | A/B test, education |

---

## METRICHE DI SUCCESSO GLOBALI

### Score Target per Fase

| Fase | Score Attuale | Score Target | Criterio |
|------|---------------|--------------|----------|
| Fase 1 | 7/10 | 7.5/10 | Bug fix, test GAP #2 |
| Fase 2 | 7.5/10 | 8/10 | Monitoring, docker-compose, 80% coverage |
| Fase 3 | 8/10 | 8.5/10 | What-If MVP funzionante |
| Fase 4 | 8.5/10 | 9/10 | ML database, tracking, feature eng |
| Fase 5 | 9/10 | 10/10 | ML model attivo, feedback loop |

### KPIs Tecnici

| Metrica | Attuale | Target Fase 2 | Target Fase 5 |
|---------|---------|---------------|---------------|
| Test passati | 63 | 100+ | 150+ |
| Coverage | ~60% | 80% | 90% |
| API Latency p95 | ? | <500ms | <200ms |
| Errori/giorno | ? | <10 | <5 |
| Uptime | ~95% | 99% | 99.9% |

### KPIs Business

| Metrica | Attuale | Target Q1 | Target Q2 |
|---------|---------|-----------|-----------|
| ML Acceptance Rate | N/A | >50% | >75% |
| What-If Usage | N/A | 20% | 50% |
| Time Saved/Day | N/A | 30min | 2h |
| Revenue Lift | baseline | +5% | +15% |

---

## TIMELINE VISUALE

```
Gennaio 2026
|----- Settimana 1 -----|
[ FASE 1: Test GAP #2, RateBoard hard tests, bug fix ]

|----- Settimana 2-3 -----|
[ FASE 2: docker-compose, monitoring, coverage 80% ]

Febbraio 2026
|----- Settimana 4-6 -----|
[ FASE 3: What-If Simulator MVP (backend + frontend) ]

|----- Settimana 7-8 -----|
[ FASE 4: ML Database Foundation ]

Marzo 2026
|----- Settimana 9-12 -----|
[ FASE 5: ML Model Training, Feedback Loop, Retraining ]

April 2026
[ 10/10 RAGGIUNTO ]
```

---

## OWNER ASSIGNMENT

| Fase | Task | Owner Primario | Owner Backup |
|------|------|----------------|--------------|
| 1 | Test GAP #2 | cervella-tester | cervella-frontend |
| 1 | Bug fix | cervella-backend/frontend | - |
| 2 | docker-compose | cervella-backend | - |
| 2 | Monitoring | cervella-backend | - |
| 2 | Test 80% | cervella-tester | - |
| 3 | What-If Backend | cervella-backend | - |
| 3 | What-If Frontend | cervella-frontend | - |
| 4 | ML Database | cervella-backend | - |
| 4 | Feature Eng | cervella-backend | cervella-researcher |
| 5 | ML Training | cervella-backend | cervella-researcher |
| 5 | Drift Monitor | cervella-backend | - |

---

## CHECKLIST DEPLOYMENT

### Prima di ogni deploy

- [ ] Test locali passano
- [ ] Code review completata (Guardiana)
- [ ] Backup database attivo
- [ ] Rollback plan documentato
- [ ] Monitoring attivo

### Post-deploy

- [ ] Health check OK
- [ ] Test smoke passano
- [ ] Metriche normali
- [ ] Nessun errore in log
- [ ] User acceptance (se applicabile)

---

## PROSSIMA AZIONE

**ADESSO:**
1. Lanciare cervella-tester per Task 1.1 (Test GAP #2)
2. Verificare formatDateRange e in core.js

**QUESTA SETTIMANA:**
1. Completare Fase 1 (test, bug fix)
2. Iniziare docker-compose.prod.yml

**PROSSIMA SETTIMANA:**
1. Completare Fase 2 (monitoring, coverage)
2. Iniziare What-If backend

---

*Roadmap creata da Cervella Guardiana Qualita*
*"Qualita non e optional. E la BASELINE."*
*12 Gennaio 2026*
