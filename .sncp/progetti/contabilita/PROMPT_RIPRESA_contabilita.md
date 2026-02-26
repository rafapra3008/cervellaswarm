# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 26 Febbraio 2026 - Sessione 166
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | Frontend S165 + Backend v1.6.0 (INTATTO - non ancora deployato S166) |
| **Agent NL/SHE/HP** | **v2.1.0 LIVE** - 3/3 attivi, primo giorno monitorato S166 |
| **Test** | **1497 PASS** (1 fail pre-esistente test_migration_v11_rollback) |
| **Monitoring S166** | **3/6 step completati** - migration v15 + backend metrics + agent file log |

---

## Cosa abbiamo fatto in S166 (IN CORSO)

### 1. Audit Log Agent 25 Feb (primo giorno v2.1.0)

Analizzato 2.8MB di journal logs VM. Risultati:
- **SHE**: 6 nuovi movimenti, 0 errori - PERFETTO
- **HP**: 3 nuovi movimenti, 0 errori - PERFETTO
- **NL**: 4 batch ~1000 record = full re-sync (spiegato: test manuale fatture S165)
- **Reconcile**: 3/3 hotel chiamati (NL 13:00, SHE 13:10, HP 13:20)
- **Scheduler matching**: 02:00 UTC, 3/3 portali, NL 369 + SHE 282 + HP 242 pareggi
- **Errori**: ZERO errori. Solo WARNING FASE4 (verbose ma non critici)
- **9 service restart**: 7 nostri deploy S165 + 2 da sessione lavoro

### 2. Studio Monitoring & Observability (2 Cervelle in parallelo)

**Ingegnera** (22 file, 3500 righe analizzate):
- Health attuale: 7/10
- 9 GAP trovati (2 P1, 4 P2, 3 P3)
- P1: agent senza file log + senza timing operazioni
- JSONFormatter gia' scritto ma spento (`LOG_JSON_FORMAT=false`)
- Metrics middleware in-memory (perso ad ogni restart)

**Ricercatrice** (10+ fonti: Google SRE, Prefect, Datadog, Booking.com):
- Per noi (3 hotel, ~10 sync/giorno): Metrics + Logs bastano. Traces overkill.
- 4 SLI Google SRE: Freshness (<25h), Completeness (Z-score <3), Correctness, Throughput
- ML: Z-score dopo 30gg dati, Isolation Forest solo tra 1-2 anni
- Raccomandazione: SQLite metrics + Watchdog Telegram (0 MB RAM extra)

### 3. Studio HC.io (Healthchecks.io)

- 2 canali: Sync Agent (per hotel) + Reconcile (globale)
- Dead man's switch: agent pinga HC.io, se non pinga -> alert
- `RECONCILE_HC_URL` potrebbe NON essere configurato nei .env reali
- Backend VM NON ha HC.io (gap)
- Riusabile per watchdog freshness

### 4. Implementazione Fase 1 Monitoring (3/6 step FATTI)

| Step | Cosa | Score Guardiana | Status |
|------|------|-----------------|--------|
| **1** | Migration v15: tabella sync_metrics | **9.3 -> fix -> OK** | FATTO |
| **2** | Backend: record_sync_metric in ingest/heartbeat/reconcile | **9.3 -> fix -> OK** | FATTO |
| **3** | Agent: file log RotatingFileHandler (5MB, 3 backup) | **9.5 -> OK** | FATTO |
| 4 | Agent: timing operazioni (query SQL, POST, totale) | - | PENDING |
| 5 | JSON logging VM + HC.io watchdog | - | PENDING |
| 6 | Test per sync_metrics + review finale | - | PENDING |

### Dettaglio tecnico implementato

**Migration v15** (`backend/migrations.py`):
- Tabella `sync_metrics` con CHECK constraint su portale e evento
- 7 eventi: sync_ok, sync_fail, reconcile_ok, reconcile_fail, heartbeat, reprocess_ok, reprocess_fail
- Indici su (portale, ts) e (evento)
- Upgrade + rollback testati

**record_sync_metric()** (`backend/database/ericsoft.py`):
- Non-blocking (errori loggati, mai propagati)
- Chiamato da: POST /ingest, POST /heartbeat, GET /reconcile-stats
- Evento sync_fail copre sia errori ingest che portale_ok=false
- Watermark riusato da variabile (zero query extra, fix Guardiana F2)

**Agent file log** (`agent/agent.py`):
- RotatingFileHandler 5MB x 3 backup = max 20MB
- encoding="utf-8" (critico per Windows)
- Directory: `<project_root>/logs/` (gitignored)

---

## PROSSIMO (S167)

### Completare Fase 1 Monitoring (Step 4-5-6)

| Step | Cosa | Stima |
|------|------|-------|
| **4** | Agent timing: `time.monotonic()` su query SQL, POST HTTP, sync totale | 30 min |
| **5** | JSON logging ON su VM + HC.io watchdog freshness | 1 ora |
| **6** | Test sync_metrics + review finale + deploy | 1 ora |

### Dopo Fase 1

| Cosa | Quando |
|------|--------|
| **Punti di Rafa** (2-3 da S159) | S167 |
| **Frequenza agent scheduler** | S167 (Rafa: "non fanno piu ogni ora") |
| **Z-score anomaly** | Dopo 30gg dati (fine Marzo) |
| **Code review finding non fixati** | 3 P2 backend + 4 P2 agent (da S165) |

---

## Dove leggere

| Cosa | File |
|------|------|
| Migration v15 sync_metrics | `backend/migrations.py:783` (lab-v3) |
| record_sync_metric | `backend/database/ericsoft.py:937` (lab-v3) |
| Chiamate nel router | `backend/routers/ericsoft.py:271` (ingest), `:312` (heartbeat), `:577` (reconcile) |
| Agent file log | `agent/agent.py:65` (setup_logging) |
| HC.io integration | `agent/http_sender.py:195`, `agent/reconcile_notifier.py:88` |
| Audit log 25 Feb | Sessione 166 context (journal VM) |

---

## Lezioni Apprese (Sessione 166)

### Cosa ha funzionato bene
- **Audit Guardiana dopo ogni step**: 3 audit, tutti 9.3-9.5, finding P2 fixati subito
- **2 Cervelle in parallelo per ricerca**: Ingegnera (codice) + Ricercatrice (stato dell'arte) in parallelo = quadro completo in 5 min
- **Analisi log VM prima di implementare**: capire cosa abbiamo PRIMA di aggiungere

### Cosa non ha funzionato
- **NL full re-sync confuso con bug**: era test manuale nostro (S165 fatture)
- **DB query su VM con escape bash**: dollari nelle variabili shell richiedono single quotes

### Pattern candidato
- **Studio + Ricerca PRIMA di implementare**: evidenza S166 (monitoring). Capire lo stato dell'arte evita reinventare la ruota. PROMUOVERE.

---

*S166: Monitoring Fase 1 al 50% (3/6 step). Zero errori agent primo giorno. Studio HC.io completato.*
