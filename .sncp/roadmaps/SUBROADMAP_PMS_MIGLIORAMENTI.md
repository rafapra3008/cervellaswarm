# SUBROADMAP - Miglioramenti PMS Miracollo

> **Creata:** 20 Gennaio 2026 - Sessione 303
> **Analisi:** Cervella Ingegnera
> **Validata:** Cervella Guardiana Qualità
> **Approvata:** Rafa
> **Status PMS:** Health 9.0/10 | 90% LIVE

---

## OVERVIEW

| Fase | Focus | Sessioni | Timeline |
|------|-------|----------|----------|
| 1 | Fondamenta (Sicurezza + Resilienza) | 4-5 | 1 settimana |
| 2 | Performance (Velocità + Stabilità) | 8-10 | 2-3 settimane |
| 3 | Feature (Valore Business) | 15-25 | 1-2 mesi |

**Principio:** Fondamenta PRIMA, Feature POI.

---

## FASE 1: FONDAMENTA (Priorità CRITICA)

> "Senza fondamenta solide, le feature crollano"

### F1.1 Rate Limiting Globale [1 sessione]
- **Cosa:** Estendere rate limiting a TUTTI gli endpoint pubblici
- **Esistente:** WhatsApp, scraping (slowapi)
- **Da fare:** Middleware globale FastAPI
- **Dipendenze:** Nessuna
- **Rischio:** BASSO
- **Status:** [x] DONE - Sessione 303
- **Audit:** 10/10 APPROVED
- **Note:** slowapi con get_ipaddr (proxy-aware), 30 req/min, health esenti

### F1.2 Backup Automation [1 sessione]
- **Cosa:** Cron job backup SQLite + verifica restore
- **Script:** backup_db.sh + test_restore.sh
- **Dipendenze:** Nessuna
- **Rischio:** MEDIO (business continuity!)
- **Status:** [x] DONE - Sessione 303
- **Audit:** 9/10 APPROVED
- **Note:** Hot backup + gzip (90% compression), retention 30 giorni, integrity check
- **Warning:** 1262 FK violations nel DB (problema esistente, task separato)

### F1.3 Health Checks Avanzati [1 sessione]
- **Cosa:** /health che verifica DB + servizi esterni
- **Esistente:** /health base
- **Da fare:** Check DB connectivity, disk space, external APIs
- **Dipendenze:** Nessuna
- **Rischio:** BASSO
- **Status:** [x] DONE - Sessione 303
- **Audit:** 9.5/10 APPROVED
- **Note:** Pattern Kubernetes (/live, /ready, /startup, /detailed), HTTP 503 per unhealthy, cache 30s

### F1.4 Structured Logging PMS [1-2 sessioni]
- **Cosa:** Migrare a structlog (come Miracollook)
- **Esistente:** Miracollook usa structlog
- **Da fare:** Copy pattern da Miracollook, JSON output
- **Dipendenze:** Nessuna
- **Rischio:** BASSO
- **Status:** [x] DONE - Sessione 303
- **Audit:** 9/10 APPROVED
- **Note:** JSON (prod) + Pretty (dev), Request ID automatico, health escluso

**FASE 1 TOTALE:** 4-5 sessioni

### Checkpoint Fase 1 - COMPLETATO! ✅
- [x] Rate limiting attivo su /api/* (30/min, proxy-aware)
- [x] Backup automatico (scripts/backup_db.sh + test_restore.sh)
- [x] Health check Kubernetes-style (/live, /ready, /startup, /detailed)
- [x] Logging JSON queryable (structlog + Request ID)

---

## FASE 2: PERFORMANCE (Priorità ALTA)

> "Velocità è la feature invisibile più importante"

### F2.1 Database Indexes Mancanti [1 sessione]
- **Cosa:** Aggiungere index mancanti
- **GIÀ ESISTONO:** idx_cm_reservations_status, idx_cm_reservations_check_in, idx_cm_reservations_created, idx_bookings_group
- **DA AGGIUNGERE:** idx_bookings_hotel_dates, idx_payments_booking, idx_guests_hotel
- **Dipendenze:** Nessuna
- **Rischio:** BASSO
- **Status:** [x] DONE - Sessione 305
- **Audit:** 9/10 APPROVED
- **Note:** Migration 043_performance_indexes_v2.sql, idx_guests_email fix, idx_room_assignments_dates, idx_bookings_status_dates, EXPLAIN confermato

### F2.2 Caching Layer [2 sessioni]
- **Cosa:** LRU cache per dati quasi-statici
- **Target:** room_types, rate_plans, hotel_config
- **Tech:** functools.lru_cache o cachetools
- **Dipendenze:** Nessuna
- **Rischio:** MEDIO (invalidation!)
- **Status:** [x] DONE - Sessione 305
- **Audit:** 9/10 APPROVED
- **Note:** backend/core/cache.py (cachetools TTLCache), TTL 60/15/30 min, invalidazione in room_types.py/rate_plans.py/hotel.py, endpoint /health/cache-stats

### F2.3 Query N+1 Fix [2-3 sessioni]
- **Cosa:** Eager loading relazioni
- **Target:** bookings.py, planning_ops.py, dashboard.py
- **Tech:** JOIN + prefetch
- **Dipendenze:** F2.1 (indexes)
- **Rischio:** MEDIO
- **Status:** [x] DONE - Sessione 305/306
- **Audit:** 9/10 APPROVED
- **Note:**
  - dashboard.py: FIXATO (bug schema + 3→1 query)
  - guest_validation.py: validate_guests_compliance_batch() CREATA
  - planning_ops.py: get_today_arrivals() FIXATO (N→2 query)
  - get_today_departures() non richiede fix (non usa compliance validation)

### F2.4 Retry Logic [2 sessioni]
- **Cosa:** Exponential backoff su servizi esterni
- **Target:** competitor_scraping, email_poller, cm_poller
- **Tech:** tenacity library
- **Dipendenze:** Nessuna
- **Rischio:** BASSO
- **Status:** [ ] TODO

### F2.5 API Response Compression [0.5 sessione]
- **Cosa:** Abilitare gzip middleware
- **Tech:** GZipMiddleware FastAPI
- **Dipendenze:** Nessuna
- **Rischio:** BASSO
- **Status:** [ ] TODO

**FASE 2 TOTALE:** 8-10 sessioni

### Checkpoint Fase 2
- [ ] Query planning < 50ms (P95)
- [ ] Cache hit rate > 70% su room_types
- [ ] Zero N+1 su endpoint critici
- [ ] Retry attivo su external services
- [ ] Response size -50%

---

## FASE 3: FEATURE (Priorità MEDIA)

> "Feature che generano valore business"

### F3.1 Batch Operations [2 sessioni]
- **Cosa:** Endpoint bulk per operazioni massive
- **Target:** bookings, payments, guests
- **Dipendenze:** F2 completata
- **ROI:** Workflow operativi 3x più veloci
- **Status:** [ ] TODO

### F3.2 Webhooks Outbound [3 sessioni]
- **Cosa:** Sistema webhook per eventi
- **Target:** booking.created, payment.received, guest.checked_in
- **Dipendenze:** Nessuna
- **ROI:** Real-time integrations
- **Status:** [ ] TODO

### F3.3 Revenue Management Dashboard [5-7 sessioni]
- **Cosa:** Dashboard dedicato revenue
- **Include:** Forecasting, alerts competitor, scenario planning
- **Dipendenze:** F2 (performance)
- **ROI:** ADR +5-10%
- **Status:** [ ] TODO

### F3.4 Housekeeping Module [6-8 sessioni]
- **Cosa:** Gestione pulizie intelligente
- **Include:** Routing ottimizzato, task management, mobile view
- **Dipendenze:** Nessuna
- **ROI:** Efficienza operativa +30%
- **Status:** [ ] TODO

### F3.5 Channel Manager 2-Way (FUTURO) [10-15 sessioni]
- **Cosa:** Sync bidirezionale OTA
- **Include:** Rate push, availability sync, mapping
- **Dipendenze:** F3.2 (webhooks)
- **ROI:** Elimina canone CM esterno
- **Note:** Valutare dopo F3.1-F3.4
- **Status:** [ ] FUTURO

**FASE 3 TOTALE:** 15-25 sessioni (escluso CM)

---

## RISCHI IDENTIFICATI

| ID | Rischio | Livello | Mitigation |
|----|---------|---------|------------|
| R1 | SQLite Scalabilità | MEDIO | Monitorare row count, pianificare PostgreSQL |
| R2 | Single Point of Failure | BASSO | Backup automatici (F1.2), monitoring (F1.3) |
| R3 | External API Dependency | MEDIO | Retry logic (F2.4), circuit breaker futuro |
| R4 | Load Testing Assente | BASSO | Setup locust tests dopo F2 |

---

## FILE GRANDI - MONITORAGGIO

| File | Righe | Azione | Priorità |
|------|-------|--------|----------|
| cm_reservation.py | 736 | Monitorare | BASSA |
| autopilot.py | 679 | Nessuna (ben strutturato) | - |
| fiscal.py | 661 | Nessuna (file nuovo, pulito) | - |
| planning_ops.py | 650 | Monitorare | BASSA |
| groups.py | 615 | Monitorare | BASSA |

---

## DIPENDENZE

```
FASE 1 (Fondamenta) - Tutte indipendenti
    |
    v
FASE 2 (Performance)
    +-- F2.1 Indexes (indipendente)
    +-- F2.2 Caching (dopo F2.1)
    +-- F2.3 N+1 Fix (dopo F2.1)
    +-- F2.4 Retry Logic (indipendente)
    +-- F2.5 Compression (indipendente)
    |
    v
FASE 3 (Feature)
    +-- F3.1 Batch Ops (dopo F2)
    +-- F3.2 Webhooks (indipendente)
    +-- F3.3 Revenue Dashboard (dopo F2)
    +-- F3.4 Housekeeping (indipendente)
    +-- F3.5 Channel Manager (dopo F3.2, FUTURO)
```

---

## METRICHE SUCCESSO

| Fase | Metrica | Target |
|------|---------|--------|
| 1 | Uptime | 99.5% |
| 1 | Backup verificati | 100% |
| 2 | Query P95 | < 100ms |
| 2 | Cache hit rate | > 70% |
| 3 | Feature adoption | > 80% |
| 3 | Revenue impact | ADR +5% |

---

## HISTORY

| Data | Sessione | Cosa |
|------|----------|------|
| 20 Gen 2026 | S303 | Creata SUBROADMAP, approvata da Rafa |
| 20 Gen 2026 | S305 | F2.1 DONE, F2.2 DONE, F2.3 parziale (autocompact) |
| 20 Gen 2026 | S306 | F2.3 DONE (planning_ops.py batch fix), FASE 2 = 60% |

---

*"Fondamenta solide = Feature che durano!"*
*Cervella & Rafa*
