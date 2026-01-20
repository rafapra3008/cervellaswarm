<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 305
> **STATO:** 90% LIVE | Health 9.5/10 (FASE 2 Performance IN PROGRESS)

---

## SESSIONE 305 - FASE 2 PERFORMANCE (Parziale)

```
+================================================================+
|   FASE 2: PERFORMANCE - 2/5 COMPLETATI, 1 IN PROGRESS          |
|                                                                |
|   [x] F2.1 Database Indexes        9/10 APPROVED               |
|   [x] F2.2 Caching Layer           9/10 APPROVED               |
|   [~] F2.3 Query N+1 Fix           IN PROGRESS                 |
|   [ ] F2.4 Retry Logic             TODO                        |
|   [ ] F2.5 API Compression         TODO                        |
+================================================================+
```

**F2.1 Database Indexes (DONE):**
- Migration: `043_performance_indexes_v2.sql`
- Index: idx_guests_email (fix), idx_room_assignments_dates, idx_bookings_status_dates
- EXPLAIN QUERY PLAN confermato uso index

**F2.2 Caching Layer (DONE):**
- File: `backend/core/cache.py` (cachetools TTLCache)
- TTL: room_types 60min, rate_plans 15min, hotel_config 30min
- Invalidazione: room_types.py, rate_plans.py, hotel.py
- Endpoint: /health/cache-stats

**F2.3 Query N+1 (IN PROGRESS):**
- dashboard.py: FIXATO (bug schema + 3→1 query)
- guest_validation.py: Funzione batch CREATA
- planning_ops.py: Import aggiunto, **LOOP DA MODIFICARE**

---

## PROSSIMA SESSIONE - DA FARE

1. **COMPLETARE F2.3:**
   - Modificare loop in `planning_ops.py:496-539` per usare `validate_guests_compliance_batch`
   - Fare stessa fix per `get_today_departures()`
   - Guardiana audit F2.3

2. **F2.4 Retry Logic:**
   - Target: competitor_scraping, email_poller, cm_poller
   - Tech: tenacity library

3. **F2.5 API Compression:**
   - GZipMiddleware FastAPI

---

## SUBROADMAP ATTIVA

**File:** `.sncp/roadmaps/SUBROADMAP_PMS_MIGLIORAMENTI.md`

| Fase | Status | Sessioni |
|------|--------|----------|
| 1 Fondamenta | DONE | 1 (S303) |
| 2 Performance | **IN PROGRESS** | 2/? (S305) |
| 3 Feature | TODO | 15-25 |

---

## FILE CHIAVE SESSIONE 305

| File | Azione |
|------|--------|
| `backend/database/migrations/043_performance_indexes_v2.sql` | CREATO |
| `backend/core/cache.py` | CREATO |
| `backend/routers/public/helpers.py` | MODIFICATO (usa cache) |
| `backend/routers/settings/room_types.py` | MODIFICATO (+invalidazione) |
| `backend/routers/settings/rate_plans.py` | MODIFICATO (+invalidazione) |
| `backend/routers/settings/hotel.py` | MODIFICATO (+invalidazione) |
| `backend/routers/health.py` | MODIFICATO (+/health/cache-stats) |
| `backend/routers/dashboard.py` | MODIFICATO (fix schema + 3→1 query) |
| `backend/services/guest_validation.py` | MODIFICATO (+batch function) |
| `backend/routers/planning_ops.py` | PARZIALE (import ok, loop TODO) |
| `requirements.txt` | MODIFICATO (+cachetools) |

---

## WARNING

- **FK violations:** 1262 nel DB (problema esistente, task separato)
- **planning_ops.py:** Loop N+1 ancora da fixare (riga 496-539)

---

*"FASE 2 Performance 40% - F2.1 e F2.2 DONE!" - Sessione 305*
