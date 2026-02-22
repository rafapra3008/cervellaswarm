<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 22 Febbraio 2026
> **STATO:** 90% LIVE | Health codice 6.5/10 (post-audit dettagliato)

---

## SESSIONE 22 FEB - AUDIT COMPLETO + SUBROADMAP

```
+================================================================+
|   RECAP GIGANTE - 3 Audit Paralleli Completati                 |
|                                                                |
|   Ingegnera:    Codice 6.5/10 (4 critici, 5 alti)             |
|   Guardiana QA: Docs   6.5/10 (3 critici, ~250 orfani)        |
|   DevOps:       VM spenta, DNS sbagliato                       |
|                                                                |
|   SUBROADMAP RINASCITA creata e validata (8.8/10)              |
+================================================================+
```

### Cosa e stato fatto oggi
- Audit codice completo (85 tool calls, 83 file router, 396 endpoint)
- Audit documentazione (46 tool calls, tutte le contraddizioni mappate)
- Audit infrastruttura (32 tool calls, porte, VM, DNS)
- Subroadmap 6 fasi creata e validata dalla Guardiana

### Cosa NON e stato modificato
- Zero righe di codice cambiate
- Zero file di produzione toccati
- Solo documentazione SNCP aggiornata

---

## BUG CRITICI DA FIXARE (FASE 0)

| Bug | File | Dettaglio |
|-----|------|-----------|
| **create_guest ROTTO** | `backend/routers/guests.py:74-88` | INSERT 22 colonne, 9 placeholder. Crash SQLite. |
| **Auth mancante** | 83 router files | Solo 23/396 endpoint protetti (5.8%) |
| **XSS frontend** | 82 file JS | ~362 innerHTML senza escape, no CSP header |
| **DB backup in git history** | storia Git | 2 file con dati personali clienti |

---

## ARCHITETTURA ATTUALE

```
396 endpoint API in 83 file router
Backend: Python 3.11, FastAPI, SQLite, Gunicorn (5 workers)
Frontend: HTML/CSS/JS puro (NON React!)
Docker: Multi-stage build, non-root user, Nginx reverse proxy
```

### Punti di Forza (confermati dall'audit)
- Buona modularizzazione (50+ file < 400 righe)
- Pydantic settings, optimistic locking, security headers
- HMAC webhook validation, GZip compression, rate limiting
- Dockerfile best practices

### Debiti Tecnici Principali
- except Exception generico in 100+ punti
- Rate limiting in-memory (non funziona con multi-worker)
- on_event("startup") deprecato -> migrare a lifespan
- 13 file Python > 650 righe (candidati split)
- revenue.js 1296 righe (piu grande nel frontend)

---

## FASE 3 FEATURE - PROGRESSO REALE: 4/5 (80%)

| Task | Status | Note |
|------|--------|------|
| **F3.1 Batch Operations** | **DONE 9/10** | POST /api/batch/* |
| **F3.2 Webhooks Outbound** | **DONE 9/10** | HMAC, retry, DLQ |
| **F3.3 Revenue Dashboard** | **DONE 8/10** | Gia esistente, enhancement minor |
| **F3.4 Housekeeping Quick Wins** | **DONE 9/10** | Auto-dirty, panel, bulk |
| F3.5 Channel Manager 2-Way | FUTURO | dopo F3.2 (ora possibile!) |

---

## PROSSIMI STEP

**Seguire SUBROADMAP:** `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md`

```
FASE 0 -> Fix bug guests.py + .gitignore
FASE 1 -> Riattivare VM per demo ditta tedesca
FASE 2 -> Auth su tutti endpoint + CSP + XSS fix
```

---

## WARNING ESISTENTI

- **FK violations:** 1262 nel DB (problema pre-esistente)
- **VM:** In pausa, IP non fisso, DNS da aggiornare
- **Contabilita:** USA porte simili in locale (8000, 8001) - NON toccare

---

*"Audit fatto con calma, ogni punto trovato. Ora si sistema."*
*22 Febbraio 2026*
