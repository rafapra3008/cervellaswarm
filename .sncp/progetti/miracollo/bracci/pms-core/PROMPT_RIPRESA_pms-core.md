<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 21 Gennaio 2026 - Sessione 307
> **STATO:** 90% LIVE | Health 9.5/10

---

## SESSIONE 307 - DOPPIO COMPLETAMENTO!

```
+================================================================+
|   F2.4 Retry Logic       9/10 DONE - tenacity                  |
|   F3.1 Batch Operations  9/10 DONE - 3 endpoint                |
|                                                                |
|   FASE 2 PERFORMANCE = 100% COMPLETATA!                        |
|   FASE 3 FEATURE = INIZIATA! (1/5)                            |
+================================================================+
```

---

## FASE 2 - 100% COMPLETATA

| Task | Score | Tech |
|------|-------|------|
| F2.1 Database Indexes | 9/10 | 3 index + email fix |
| F2.2 Caching Layer | 9/10 | cachetools TTL |
| F2.3 Query N+1 Fix | 9/10 | batch queries |
| F2.4 Retry Logic | 9/10 | tenacity decorators |
| F2.5 API Compression | 10/10 | GZipMiddleware |

---

## FASE 3 - INIZIATA (1/5)

| Task | Status | Note |
|------|--------|------|
| **F3.1 Batch Operations** | **DONE 9/10** | POST /api/batch/{guests,payments,bookings} |
| F3.2 Webhooks Outbound | TODO | booking.created, payment.received |
| F3.3 Revenue Dashboard | TODO | 5-7 sessioni |
| F3.4 Housekeeping Module | TODO | 6-8 sessioni |
| F3.5 Channel Manager 2-Way | FUTURO | dopo F3.2 |

---

## FILE CHIAVE SESSIONE 307

| File | Azione |
|------|--------|
| `backend/services/email_poller.py` | +tenacity retry |
| `backend/services/competitor_scraping_service.py` | +tenacity retry |
| `backend/models/batch.py` | CREATO |
| `backend/routers/batch.py` | CREATO |

---

## PROSSIMA SESSIONE - OPZIONI

1. **F3.2 Webhooks Outbound** (3 sessioni) - Real-time integrations
2. **F3.3 Revenue Dashboard** (5-7 sessioni) - Richiede subroadmap

---

## WARNING ESISTENTI

- **FK violations:** 1262 nel DB (problema esistente, task separato)

---

*"FASE 2 completata! FASE 3 iniziata!" - Sessione 307*
