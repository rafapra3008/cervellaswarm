# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 19 Febbraio 2026 - Sessione 91
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S91 COMPLETATA (FASE D Implementazione Agent Python)

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, zero modifiche) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (HTTPS, DB v10) |
| **Lab v2 locale** | INTOCCATO, branch lab-v2, porta 8001 |
| **Lab V3 locale** | branch lab-v3, porta 8003, Docker healthy |
| **FASE C** | COMPLETATA S84-S87 (7/7 step) |
| **FASE D** | **COMPLETATA S89-S91** - Studio + 8 moduli Python + 218 test + 3 Guardiane |
| **Test** | 1488/1488 PASS (0 warnings) - 1270 portale + 218 agent |
| **Prossimo** | **S92 = FASE E - Deploy VM + Agent su NL + E2E** |

---

## S91 - Cosa e stato fatto

### FASE D Implementazione Agent Python (6 step D.10.1-D.10.6)

8 moduli Python in `agent/` directory:

| Modulo | Cosa fa |
|--------|---------|
| `config.py` | AgentConfig/DBConfig/APIConfig frozen dataclass + load_config da .env |
| `models.py` | MovimentoEricsoft frozen dataclass (validazione ericsoft_id, tipo, importo) |
| `db_reader.py` | DBReader con pymssql, NOLOCK, delta query (IdMovimentoCassa > watermark) |
| `http_sender.py` | HTTPSender con tenacity retry (3 tentativi, backoff), 3 endpoint |
| `season_calculator.py` | Calcolo stagione SINCRONIZZATA con EricsoftTransformer |
| `circuit_breaker.py` | CircuitBreaker 3 stati (CLOSED/OPEN/HALF_OPEN), SQLite persistence |
| `state_store.py` | Watermark cache locale (fallback quando VM irraggiungibile) |
| `agent.py` | Flusso completo 8 step: config -> CB -> watermark -> fetch -> validate -> ingest -> cache -> heartbeat |

### 3 Guardiane S91

| Audit | Score | Fix P2 principali |
|-------|-------|-------------------|
| D.10.4 http_sender | 9.3/10 | APIConfig repr masking + resp.text logging + test 403/429 |
| D.10.5 season_calc | 9.6/10 | Solo P3 cosmetici - APPROVATO senza riserve |
| D.10.6 agent+state | 9.2/10 | Watermark solo batch OK (data loss fix) + dead code rimosso + test partial batch |

---

## Subroadmap V3

| Fase | Cosa | Status |
|------|------|--------|
| **A-C** | Setup + Studio + Transformer + Source | **COMPLETATA S80-S87** |
| **QA** | 5 Round QA + Triple Check | **COMPLETATA S82-S90** |
| **D** | Studio + Implementazione Agent Python | **COMPLETATA S89-S91** |
| **E** | Deploy VM + Agent su NL + E2E | **PROSSIMO** |
| **F** | Confronto Ericsoft vs PDF + Decisione | PENDING |

---

## Note per S92 (FASE E)

- **pymssql**: verificare versione 2.3.11 vs 2.3.13 al momento del deploy su NL
- **P1 pending**: endpoint `POST /api/v3/reprocess` per movimenti stuck a `pending`
- **Agent runs on Windows**: Windows Task Scheduler + .bat per scheduling
- **E2E**: primo test reale con SQL Server Ericsoft NL (porta 54081)

## Dove leggere

| Cosa | File (lab-v3 worktree) |
|------|------|
| Agent completo (8 moduli) | `agent/` directory |
| Test agent (7 file, 218 test) | `agent/tests/` directory |
| Studio Agent FASE D | `docs/V3_FASE_D_STUDIO_AGENT.md` |
| EricsoftMixin (ingest + match_status) | `backend/database/ericsoft.py` |
| EricsoftTransformer v1.0.2 | `backend/processors/ericsoft_transformer.py` |
| Router Ericsoft v1.2.0 | `backend/routers/ericsoft.py` |

---

*Per dettagli completi: leggi NORD.md nella root del progetto (lab-v3)*
