# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 26 Febbraio 2026 - Sessione 168
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | Frontend S165 + Backend v1.6.0 (INTATTO) |
| **Agent NL/SHE/HP** | **v2.1.0 LIVE** - 3/3 attivi |
| **Test** | **1874 PASS** (1 fail pre-esistente test_migration_v11_rollback) |
| **Audit Generale** | **3/6 step completati** - Step 4-5-6 in sessione fresh |

---

## S168 - Audit Generale (3/6 step completati)

```
+====================================================================+
|  AUDIT GENERALE S168 - MAPPA                                       |
+====================================================================+
|                                                                    |
|  COMPLETATI (S168)                  DA FARE (sessione fresh)       |
|  +----------------------------+    +----------------------------+  |
|  | Step 1: Backend V3         |    | Step 4: Test Suite         |  |
|  |   Guardiana R153: 9.3->fix |    |   1518+356 test            |  |
|  |   3 P2 + 6 P3 = 9 fix     |    |   coverage, fragilita      |  |
|  +----------------------------+    +----------------------------+  |
|  | Step 2: Agent Hotel        |    | Step 5: Security           |  |
|  |   Guardiana R154: 8.8->fix |    |   Auth duale, OWASP, CORS  |  |
|  |   1 P1 + 3 P2 + 5 P3 fix  |    +----------------------------+  |
|  +----------------------------+    | Step 6: Coerenza Docs      |  |
|  | Step 3: Frontend V3        |    |   NORD vs codice reale     |  |
|  |   Guardiana R155: 9.3->fix |    +----------------------------+  |
|  |   2 P2 + 1 P3 fix         |    |                            |  |
|  +----------------------------+    | + Deploy VM monitoring     |  |
|                                    | + Punti di Rafa (S159)     |  |
|                                    | + Code review fix (S165)   |  |
+====================================================================+
```

### Step 1: Backend V3 - Guardiana R153 (9.3 -> fix -> DONE)

| # | Sev | Fix |
|---|-----|-----|
| F1 | P2 | POST /reprocess: aggiunto `record_sync_metric(reprocess_ok/fail)` |
| F2 | P2 | POST /backfill: aggiunto `record_sync_metric(backfill_ok)` + CHECK constraint |
| F3 | P2 | `datetime.utcnow()` -> `datetime.now(timezone.utc)` in logger_config |
| F4 | P3 | f-string -> lazy `%s` in migrations.py (27 occorrenze) |
| F5 | P3 | f-string -> lazy `%s` in main.py (10 occorrenze) |
| F6 | P3 | `max_length=50` su parametro stagione GET /movimenti |
| F7 | P3 | `row[0]` -> `row['max_id']` con alias SQL in ericsoft.py |
| F8 | P3 | CSP commento stale aggiornato (inline handler rimossi S155-S156) |
| F9 | P3 | logger_config version 1.0.0 -> 1.1.0 |

### Step 2: Agent Hotel - Guardiana R154 (8.8 -> fix -> DONE)

| # | Sev | Fix |
|---|-----|-----|
| F1 | **P1** | **SECURITY: `diagnose_conn_she.py` RIMOSSO** (password SQL Server hardcoded) |
| F2 | P2 | `datetime.now()` -> `datetime.now(timezone(timedelta(hours=1)))` in reconcile |
| F3 | P2 | `__version__` reconcile: locale "1.0.0" -> import da `agent.__init__` (2.1.0) |
| F4 | P2 | `_get_connection` -> `get_connection` metodo pubblico in DBReader |
| F5 | P3 | `TIPI_SKIP` commento chiarificato (reference, non usata nel codice) |
| F8 | P3 | `ServerError` estratta in `agent/exceptions.py` (eliminata duplicazione) |
| F9 | P3 | 4 righe vuote -> 2 in config.py (PEP 8) |
| F10 | P3 | Import lazy -> top-level in reconcile.py |
| F11 | P3 | `import math` -> `from math import isnan, isinf` in models.py |

### Step 3: Frontend V3 - Guardiana R155 (9.3 -> fix -> DONE)

| # | Sev | Fix |
|---|-----|-----|
| F1 | P2 | `escapeHtml(msg)` su validation.messages in data.js (XSS difensivo) |
| F3 | P2 | `escapeHtml(opt)` su POS dropdown options in rows.js (XSS difensivo) |
| F9 | P3 | Cache bust landing.html allineato (202602161700 -> 202602261300) |

### Finding P3 frontend NON fixati (bassa priorita, da fare gradualmente)

- **F2**: Landing page CSS inline (290 righe `<style>`) -> estrarre in file esterno
- **F4**: Inline style eccessivi nelle modali HTML -> creare classi CSS
- **F5**: ~20 `!important` evitabili -> aumentare specificita selettori
- **F6**: z-index non standardizzato -> variabili CSS `--z-*`
- **F7**: 34 console.warn/log residui -> wrappare in DEBUG flag
- **F8**: Responsive limitato (manca breakpoint 768px)
- **F10**: config.js version header stale

---

## PROSSIMO (sessione fresh)

### Audit Generale Step 4-5-6

| Step | Area | Cosa |
|------|------|------|
| 4 | Test Suite | Coverage aree critiche, test fragili, mocking corretto |
| 5 | Security | Auth duale, OWASP top 10, secrets, CORS |
| 6 | Coerenza Docs | NORD.md, PROMPT_RIPRESA vs codice reale |

### Dopo l'audit

| Cosa | Dettaglio |
|------|-----------|
| Deploy VM monitoring | migration v15 + LOG_JSON_FORMAT=true |
| Verificare RECONCILE_HC_URL | Potrebbe mancare nei .env reali hotel |
| Punti di Rafa | 2-3 da S159 (chiedere quali) |
| Code review fix | 3 P2 backend + 4 P2 agent (da S165) |
| Frequenza agent scheduler | Rafa: "non fanno piu ogni ora" - verificare |

---

## Dove leggere

| Cosa | File (lab-v3) |
|------|---------------|
| Fix reprocess/backfill metric | `backend/routers/ericsoft.py:486` e `:531` |
| Fix lazy logging | `backend/main.py`, `backend/migrations.py` |
| Fix watermark row access | `backend/database/ericsoft.py:297` |
| Fix logger_config timezone | `backend/logger_config.py:24` |
| RIMOSSO password script | `agent/scripts/diagnose_conn_she.py` (eliminato) |
| Fix reconcile timezone | `agent/reconcile.py:62` |
| Fix get_connection pubblico | `agent/db_reader.py:199` |
| ServerError condiviso | `agent/exceptions.py` (NUOVO) |
| Fix XSS frontend | `frontend/js/data.js:130`, `frontend/js/rows.js:120` |

---

## Lezioni Apprese (Sessione 168)

### Cosa ha funzionato bene
- **Audit per area + Guardiana**: 3 audit (R153-R155), finding mirati per area, fix sistematici
- **P1 security trovato**: password hardcoded in script di debug - rimosso subito
- **Pattern diamante confermato**: fix TUTTI i P2+P3 -> score sale da 8.8-9.3 a 9.5+

### Cosa non ha funzionato
- **Troppi step in una sessione**: 6 step audit + fix e' troppo per una sessione. Meglio splitare 3+3.

### Pattern candidato
- **Audit generale: max 3 step per sessione**: evita accumulo context. Evidenza: S168. PROMUOVERE.

---

*S168: Audit Generale 3/6 step (Backend+Agent+Frontend). 1 P1 security fixato, 6 P2 fixati, 15 P3 fixati. 1874 PASS. Prossimo: Step 4-5-6 in sessione fresh.*

---
