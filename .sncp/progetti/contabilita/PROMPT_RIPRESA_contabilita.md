# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 28 Febbraio 2026 - Sessione 223
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

## Quick Status S223

| Cosa | Stato |
|------|-------|
| Produzione V2 | v2.11.0 LIVE (INTATTA) |
| V3 VM | v1.16.0 + 33 file (S199) |
| Agent 3 hotel | v2.1.0 + reconcile v1.1.0, HC.io VERDI |
| **SPRING DB** | **Subroadmap C.7 COMPLETATA! Script INSERT v4.5.0** |
| **Fase D** | **IN CORSO! D.0 endpoint IMPLEMENTATO, audit in corso** |
| **Prossimo** | **Leggere audit Guardiana D.0 + test locale + D.1 pipeline** |

## S223 - Lavoro Fatto

### Studio + Piano (3 cervelle + 2 audit Guardiana)
- Ingegnera: gap analysis planner vs INSERT (7 GAP, 10 rischi)
- Researcher: pattern big players (Trial Balance, Idempotency SHA256, Audit SQLite)
- Scienziata: architettura pipeline professionale (SAP/QuickBooks/Stripe patterns)
- Audit idee Guardiana: **8.7/10** (1 P1 risolto da Rafa, 6 P2, 6 P3)
- Piano completo scritto: `docs/PLAN_FASE_D_AUTOMAZIONE.md`
- Audit piano Guardiana: **9.1/10** (0 P1, 5 P2, 5 P3) -- fix incorporati

### Idea CHIAVE di Rafa (risolve P1)
Come l'agent hotel (Windows -> Ericsoft -> POST -> V3), al contrario:
```
HPTERMINAL01 -> GET -> V3 portale -> INSERT -> SPRING
```
ZERO trasporto file! HPTERMINAL01 ha gia' HTTPS a v3.contabilitafamigliapra.it.

### D.0 Endpoint IMPLEMENTATO (3 file modificati)
1. `backend/database/ericsoft.py` v1.7.0 -- 2 nuovi metodi:
   - `get_gir_for_spring(data_iso)` -- WHERE fatto IN ('si','si') AND source='ericsoft'
   - `get_caparre_for_spring(data_iso)` -- WHERE fatto IN ('si','si') AND source='ericsoft' AND stato='attiva'
2. `backend/routers/ericsoft.py` v1.7.0 -- nuovo endpoint:
   - `GET /api/v3/spring-batch?portale=she&date=2026-01-10` (ISO 8601!)
   - Auth: Bearer ERICSOFT_API_KEY_{PORTALE} (stessa dell'agent hotel)
   - Response: JSON batch v1.0 (documents + summary)
   - Helper: `_normalize_name()` (NFKC), `_parse_amount_spring()`, `_group_spring_documents()`
3. `backend/main.py` riga 248 -- `/api/v3/spring-batch` aggiunto a AGENT_AUTH_ENDPOINTS

### Audit Guardiana D.0 in corso
- Lanciata alla fine della sessione, risultati da leggere in S224
- NON ancora letti -- la prossima Cervella DEVE leggerli prima di procedere

## Prossimi step (S224+)

1. **Leggere audit Guardiana D.0** (risultati da S223, non ancora letti!)
2. **Fixare finding** dell'audit se necessario
3. **Test locale** dell'endpoint: avviare V3, curl con Bearer, confrontare con `c7_step4_she_20260110.json`
4. **D.1: Pipeline script** (`scripts/spring_pipeline.py`) -- vedi piano completo
5. **D.2+D.3: Telegram + HC.io + bat** -- vedi piano completo
6. **D.4: Test E2E** su HPTERMINAL01

## Documenti Fase D

| Documento | Path | Versione |
|-----------|------|----------|
| **Piano completo** | `docs/PLAN_FASE_D_AUTOMAZIONE.md` | **S223 - LEGGERE QUESTO!** |
| Bibbia INSERT | `docs/SPRING_INSERT_STUDIO.md` | S220 |
| Bibbia logica | `docs/SPRING_LOGICA_CONTABILE.md` | v1.5.0 S217 |
| Subroadmap C.7 | `docs/SUBROADMAP_C7_COMMIT_TEST.md` | S222 COMPLETATA |
| Script INSERT | `scripts/spring_insert_hotel.py` | v4.5.0 (su HPTERMINAL01) |
| Script planner | `scripts/spring_day_planner.py` | v1.1.0 S217 |
| JSON Step 4 | `scripts/batch/c7_step4_she_20260110.json` | v1.0 (riferimento test) |

## Architettura Pipeline (da piano)

```
HPTERMINAL01 (Windows)
  spring_pipeline.py (DA CREARE - D.1)
    1. HTTP GET v3.contabilitafamigliapra.it/api/v3/spring-batch (FATTO - D.0)
    2. Check idempotency (spring_audit.db SQLite locale)
    3. INSERT in SPRING DB (riusa spring_insert_hotel.py con confirm_mode="automated")
    4. Trial Balance post-batch: SUM(DARE) - SUM(AVERE) = 0
    5. Log audit in spring_audit.db
    6. Telegram report + HC.io ping
    7. Task Scheduler 12:30 daily (dopo agent sync 11:30-11:50)
```

## Lezioni Apprese (Sessione 223)

### Cosa ha funzionato bene
- **3 cervelle parallele per studio**: ognuna con focus diverso, copertura completa in 1 sessione
- **Audit idee PRIMA del piano**: la Guardiana ha trovato il P1 che Rafa ha risolto con l'idea del GET
- **Audit piano DOPO il piano**: 4 fix incorporati subito (ISO date, EricsoftMixin, NFKC, fatto accento)

### Cosa migliorare
- **Context si riempie velocemente** con studio+piano+implementazione nella stessa sessione
- Meglio: studio+piano in sessione 1, implementazione in sessione 2

### Pattern confermato
- **"Audit dopo ogni step"**: idee 8.7 -> piano 9.1 -> codice (in corso). 3 audit progressivi (S154-S223)
- **"Rafa risolve i P1"**: l'idea del GET reversed ha eliminato tutto il problema trasporto file

---

## AUTO-CHECKPOINT: 2026-02-28 20:40 (manuale)

### Stato Git
- **Branch**: lab-v3
- **Ultimo commit**: (da committare)
- **File modificati**: 3 backend + 1 docs + NORD + PROMPT_RIPRESA
