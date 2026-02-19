# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 19 Febbraio 2026 - Sessione 102
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S102: Fix 429 Multi-Cell Save

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, zero modifiche) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (HTTPS, sync auto ATTIVO) |
| **V3 VM** | **LIVE** su v3.contabilitafamigliapra.it (health OK, watermark 3857) |
| **Agent hotel NL** | **AUTOMATICO!** Task Scheduler ogni ora, background |
| **FASE E.10** | IN CORSO - Task Scheduler OK, watermark 3857 (attesa chiusura cassa) |
| **Test** | 1522/1522 PASS (0 warnings) - 1286 portale + 236 agent |
| **Prossimo** | Endpoint batch backend (fix definitivo) + audit + deploy V3 |

---

## S102 - Fix 429 Rate Limit Multi-Cell Save

| Cosa | Dettaglio |
|------|-----------|
| **Bug** | Multi-cell select + "s" causava 429 (Nginx V3 rate limit 60r/m burst=20) |
| **Fix** | `batchedSave()` batch da 10 + merge fatto+sig_sergio in 1 call + fix selezione mista |
| **Guardiana** | R1: 9.3 -> R2: **9.5/10 APPROVED** |
| **File** | `frontend/js/selection.js` v1.3.0, commit `ae4af2a` |
| **NON deployato** | Fix solo locale, deploy nella prossima sessione |

## S101 - Task Scheduler + Timing Ericsoft

| Cosa | Dettaglio |
|------|-----------|
| **Task Scheduler** | ContabilitaSync-NL, ogni 1 ora, background (anche senza login) |
| **Scoperta timing** | Movimenti visibili in UI Ericsoft ma NON nel DB SQL Server fino a chiusura cassa |
| **Delay reale** | Max 12-18 ore, completamente automatico (zero intervento umano) |

## S100 - PRIMO SYNC REALE ERICSOFT (STORICA!)

| Metrica | Valore |
|---------|--------|
| **Movimenti** | 2114 (3 batch: 1000+1000+114), 0 errori |
| **Caparre** | 1081 (source='ericsoft') |
| **Giroconti** | 1033 (source='ericsoft') |
| **Watermark** | 3857 |

---

## Prossimi step

1. **Endpoint batch backend** - `POST /api/batch-update-transactions` (fix definitivo, con calma)
2. **Verifica watermark** - controllare se > 3857 (chiusura cassa)
3. **Deploy fix 429 su V3** - dopo audit endpoint batch
4. **FASE F** - Confronto Ericsoft vs PDF

---

## Dove leggere

| Cosa | File (lab-v3 worktree) |
|------|------|
| **selection.js v1.3.0** | `frontend/js/selection.js` |
| Agent (8 moduli) | `agent/` directory |
| Feedback doc riuso | `docs/FEEDBACK_AGENT_WINDOWS_SQLSERVER.md` |
| Router V3 | `backend/routers/ericsoft.py` |

---

*Per dettagli completi: leggi NORD.md nella root del progetto (lab-v3)*
