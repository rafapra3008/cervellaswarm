# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 19 Febbraio 2026 - Sessione 99
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S99 COMPLETATA (FASE E.6 - Endpoint Reprocess)

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, zero modifiche) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (HTTPS, DB v10, sync auto ATTIVO) |
| **V3 VM** | **LIVE su https://v3.contabilitafamigliapra.it** (SSL, 12 headers, Health OK) |
| **Lab v2 locale** | INTOCCATO, branch lab-v2, porta 8001 |
| **Lab V3 locale** | branch lab-v3, porta 8003, Docker healthy |
| **FASE E.6** | **COMPLETATA S99** - POST /api/v3/reprocess + get_stuck_movimenti, Guardiana 9.6/10 |
| **Test** | 1522/1522 PASS (0 warnings) - 1286 portale + 236 agent |
| **Prossimo** | **FASE E.7 - Prerequisiti hotel NL (Rafa)** |

---

## S99 - Cosa e stato fatto

### FASE E.6 - Endpoint Reprocess Movimenti Stuck

| File | Modifica |
|------|----------|
| `backend/database/ericsoft.py` | EricsoftMixin v1.3.0: +get_stuck_movimenti(portale, limit=1000) |
| `backend/routers/ericsoft.py` | Router v1.3.0: +POST /api/v3/reprocess (auth Bearer, try/except, portale_ok) |
| `backend/main.py` | PUBLIC_ENDPOINTS: +/api/v3/reprocess |
| `tests/test_ericsoft.py` | +15 test (8 mixin + 7 router) = 152 ericsoft totali |

### Guardiana QA

| Round | Score | Fix |
|-------|-------|-----|
| R1 | 9.3/10 | 1 P2 (try/except) + 5 P3 (LIMIT, docstring, test manual, test error) |
| R2 | 9.6/10 | Tutti fix verificati, APPROVED |

---

## Subroadmap FASE E

| Step | Cosa | Status |
|------|------|--------|
| **E.1** | Studio + File deploy | **COMPLETATO S95** |
| **E.2** | DNS record A | **COMPLETATO S97** |
| **E.3** | Deploy V3 backend | **COMPLETATO S97** |
| **E.4** | SSL + Nginx + HTTPS | **COMPLETATO S97** |
| **E.5** | Script .bat Windows + README agent | **COMPLETATO S98** |
| **E.6** | Endpoint reprocess (movimenti stuck) | **COMPLETATO S99** |
| **E.7** | Prerequisiti hotel NL (Rafa) | **PROSSIMO** |
| **E.8** | Deploy agent su NL + dry-run | PENDING |
| **E.9** | Prima sync REALE E2E | PENDING |
| **E.10** | Verifica nel portale + audit finale | PENDING |

---

## Dove leggere

| Cosa | File (lab-v3 worktree) |
|------|------|
| **Endpoint reprocess** | `backend/routers/ericsoft.py` (POST /api/v3/reprocess) |
| **get_stuck_movimenti** | `backend/database/ericsoft.py` (EricsoftMixin) |
| **Script Windows** | `agent/scripts/` (4 file .bat/.py) |
| **Guida Windows** | `agent/README_WINDOWS.md` |
| **Script deploy** | `scripts/deploy_v3_setup.sh` + `scripts/deploy_v3_nginx.sh` |
| Agent (8 moduli) | `agent/` directory |

---

*Per dettagli completi: leggi NORD.md nella root del progetto (lab-v3)*
