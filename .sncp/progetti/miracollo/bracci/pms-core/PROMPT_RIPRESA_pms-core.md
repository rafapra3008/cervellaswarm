<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 306
> **STATO:** 90% LIVE | Health 9.5/10 (FASE 2 Performance 80%)

---

## SESSIONE 306 - FASE 2 QUASI COMPLETA!

```
+================================================================+
|   FASE 2: PERFORMANCE - 4/5 COMPLETATI (80%)                    |
|                                                                |
|   [x] F2.1 Database Indexes        9/10 APPROVED               |
|   [x] F2.2 Caching Layer           9/10 APPROVED               |
|   [x] F2.3 Query N+1 Fix           9/10 APPROVED               |
|   [ ] F2.4 Retry Logic             TODO                        |
|   [x] F2.5 API Compression         10/10 APPROVED              |
+================================================================+
```

**Cosa fatto S306:**
- F2.3 Query N+1: planning_ops.py get_today_arrivals() FIXATO (N→2 query)
- F2.5 API Compression: GZipMiddleware aggiunto (minimum_size=1000, compresslevel=5)

---

## PROSSIMA SESSIONE - DA FARE

1. **F2.4 Retry Logic:** (ultimo task FASE 2!)
   - Target: competitor_scraping, email_poller, cm_poller
   - Tech: tenacity library
   - Dopo questo: FASE 2 = 100%!

---

## SUBROADMAP ATTIVA

**File:** `.sncp/roadmaps/SUBROADMAP_PMS_MIGLIORAMENTI.md`

| Fase | Status | Sessioni |
|------|--------|----------|
| 1 Fondamenta | DONE | 1 (S303) |
| 2 Performance | **80%** | 3 (S303-S306) |
| 3 Feature | TODO | 15-25 |

---

## FILE CHIAVE SESSIONE 306

| File | Azione |
|------|--------|
| `backend/routers/planning_ops.py` | MODIFICATO (batch fix N+1) |
| `backend/main.py` | MODIFICATO (+GZipMiddleware) |

---

## WARNING

- **FK violations:** 1262 nel DB (problema esistente, task separato)

---

*"FASE 2 Performance 80% - Solo F2.4 rimasto!" - Sessione 306*
