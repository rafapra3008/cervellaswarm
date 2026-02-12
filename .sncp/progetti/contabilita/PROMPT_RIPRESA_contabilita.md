# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 12 Febbraio 2026 - Sessione 7
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.10.0 LIVE (parser v1.9.0) - NON TOCCARE |
| **IP** | 35.193.39.185 STATICO |
| **Lab 2.0** | Branch lab-v2, 19 commit avanti a main |
| **Score lab** | ~9.2/10 (Guardiana audit) |
| **Test** | 281/281 PASS |
| **Telegram** | Solo produzione (locale/lab disabilitato) |

---

## 3 AMBIENTI

| Ambiente | Porta | Branch | Scopo |
|----------|-------|--------|-------|
| Produzione | VM :8000 | main | Famiglia USA il sistema. NON TOCCARE |
| Locale | :8000 | main | Uguale produzione. Prove, bug fix |
| Lab 2.0 | :8001 | lab-v2 | Sviluppo v2.0. Tutto il lavoro nuovo |

---

## MAPPA v2.0

### Qualita (COMPLETATE - sessioni 1-6)

| Fase | Cosa | Score |
|------|------|-------|
| 0 | Occhi Nuovi (review) | - |
| A | Fondamenta (IP statico, Lab, security) | - |
| B | Pulizia (console.log, TODO, DB, backups) | 8.5/10 |
| D | Hardening (deps fantasma, Docker user, MIME, CSP) | 9.0/10 |
| C.1 | Split main.py (3427 -> 408 righe, 6 router) | - |
| FIX | Test suite 281/281 PASS | - |
| C.2 | Split database.py (4372 -> 5 file, Mixin pattern) | 9.2/10 |
| C.3 | Split pareggi.js (4796 -> 6 file) | 9.0/10 |

### Fix & Hardening (PROSSIMO STEP)

| Fase | Cosa | Stato |
|------|------|-------|
| G | **Bug Fix** (report fatto, audit tables, bare except, js-min) | DA FARE |
| H | **Hardening fatto/sig.sergio** + dedup manual_edits | DA FARE |

Dettagli: `SUBROADMAP_FIX_v2.md` nel progetto

### Feature v2.0 (DA FARE - dopo G+H)

| Fase | Cosa | Stato |
|------|------|-------|
| E | **Chiusura Stagioni** - gestione fine stagione, riconciliazione finale | DA PIANIFICARE |
| F | **Confronto SPRING per portale** - validazione file SPRING generati | DA PIANIFICARE |

### Parcheggiati (NON v2.0)

- Landing page (`landing/`) - Sprint 1-3 completati, parcheggiata

### Deploy v2.0

- Merge lab-v2 -> main + deploy SOLO DOPO fasi G + H + E + F
- FORTEZZA MODE obbligatorio

---

## ARCHITETTURA LAB (post serie C)

### Backend (Python/FastAPI)
- `main.py` (408 righe) - hub: middleware, config, root routes
- `routers/` - 6 file (auth, export, processing, admin, transactions, pareggi)
- `database/` - package con 4 Mixin (core, transactions, pareggi, edits)
- `dependencies.py` (61 righe) - limiter, get_portal_from_request, api_metrics
- `matching.py` (2150 righe) - algoritmo matching (NON toccare)

### Frontend (Vanilla JS)
- `pareggi-*.js` - 6 file (core, display, parking, fase4, manual, puzzle)
- `event-delegation.js` - dispatch centralizzato (data-action pattern)
- NO ES modules, NO bundler - scope globale, script tag

---

## DECISIONI CHIAVE

| Decisione | Perche |
|-----------|--------|
| Backend Mixin pattern (non Repository) | ZERO modifiche consumer |
| Frontend split scope globale (no ES modules) | Progetto senza bundler |
| formatDateForInput in manual.js | Caricato prima di puzzle, evita duplicati |
| Telegram solo APP_ENV=production | Locale/Lab non sporcano il canale |
| Landing page parcheggiata | Focus su v2.0, non prioritaria |
| Deploy DOPO fasi G+H+E+F | v2.0 completa = fix + hardening + feature |

---

## DATI PRODUZIONE

| Cosa | Valore |
|------|--------|
| Host | contabilitafamigliapra.it |
| IP | 35.193.39.185 (STATICO) |
| Path | /opt/contabilita-system/ |
| VM | cervello-contabilita (us-central1-c, g1-small) |
| Tag Git | vm-deployed-v2.10.0 |

---

*Prossimo: FASE G (bug fix) + FASE H (hardening fatto/sig.sergio). Poi fasi E + F.*
