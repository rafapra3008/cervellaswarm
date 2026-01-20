<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 306
> **STATO:** 90% LIVE | Health 9.5/10 (FASE 2 Performance 60%)

---

## SESSIONE 306 - F2.3 COMPLETATO!

```
+================================================================+
|   FASE 2: PERFORMANCE - 3/5 COMPLETATI (60%)                    |
|                                                                |
|   [x] F2.1 Database Indexes        9/10 APPROVED               |
|   [x] F2.2 Caching Layer           9/10 APPROVED               |
|   [x] F2.3 Query N+1 Fix           9/10 APPROVED               |
|   [ ] F2.4 Retry Logic             TODO                        |
|   [ ] F2.5 API Compression         TODO                        |
+================================================================+
```

**F2.3 Query N+1 (DONE S306):**
- dashboard.py: FIXATO (bug schema + 3→1 query)
- guest_validation.py: `validate_guests_compliance_batch()` CREATA
- planning_ops.py: `get_today_arrivals()` FIXATO (N→2 query)
- get_today_departures(): Non richiede fix (non usa compliance validation)

---

## PROSSIMA SESSIONE - DA FARE

1. **F2.4 Retry Logic:**
   - Target: competitor_scraping, email_poller, cm_poller
   - Tech: tenacity library

2. **F2.5 API Compression:**
   - GZipMiddleware FastAPI

---

## SUBROADMAP ATTIVA

**File:** `.sncp/roadmaps/SUBROADMAP_PMS_MIGLIORAMENTI.md`

| Fase | Status | Sessioni |
|------|--------|----------|
| 1 Fondamenta | DONE | 1 (S303) |
| 2 Performance | **60%** | 3 (S303-S306) |
| 3 Feature | TODO | 15-25 |

---

## FILE CHIAVE SESSIONE 306

| File | Azione |
|------|--------|
| `backend/routers/planning_ops.py` | MODIFICATO (batch fix N+1) |
| `.sncp/roadmaps/SUBROADMAP_PMS_MIGLIORAMENTI.md` | AGGIORNATO (F2.3 DONE) |

---

## WARNING

- **FK violations:** 1262 nel DB (problema esistente, task separato)

---

*"FASE 2 Performance 60% - F2.1, F2.2, F2.3 DONE!" - Sessione 306*
