# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 12 Febbraio 2026 - Sessione 3 (terza)
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.10.0 LIVE (parser v1.9.0) |
| **IP** | 35.193.39.185 STATICO |
| **Branch attivo** | lab-v2 (8 commit avanti a origin) |
| **Score** | 9.0/10 (target 9.5) |
| **Test** | 31/31 parser PASS |
| **Lab 2.0** | Porta 8001 |
| **Telegram** | Solo produzione |

---

## SESSIONE 12 FEBBRAIO (terza) - FATTO REALE

### FASE D: Hardening (COMPLETATA - score 8.5 -> 9.0)
- D.1: Rimossi 8 dipendenze fantasma (PyPDF2, xlrd, sqlalchemy, alembic, psycopg2-binary, pandas, xlsxwriter, pydantic-settings)
- D.1: Rimosso libpq-dev dal Dockerfile
- D.1: Sincronizzati requirements.txt e requirements-prod.txt
- D.2: Docker USER non-root (contabilita UID 1000)
- D.2: Dockerfile usa requirements-prod.txt (no test deps in prod)
- D.3: CSP documentato (unsafe-inline necessario per JS inline)
- Guardiana: APPROVED 9.0/10

### FASE C Parte 1: Split main.py (COMPLETATA!)
main.py splittato da **3427 -> 408 righe (-88%)**:

| Router | Righe | Endpoint |
|--------|-------|----------|
| auth.py | 139 | 2 (validate-code, verify) |
| export.py | 417 | 6 (Excel, Spring files) |
| processing.py | 310 | 2 (upload, process-pdf) |
| admin.py | 369 | 8 (health, vacuum, merge, scheduler, stats) |
| transactions.py | 807 | 11 (CRUD, POS, update, report, historical) |
| pareggi.py | 1137 | 18 (calcolo, parking, fase4, puzzle, CRUD) |

Anche creato:
- backend/dependencies.py (61 righe) - limiter, get_portal_from_request, api_metrics condivisi
- Fix qualita: rimossi import inline, debug code, import duplicati

### Commits su lab-v2 (8 totali):
1. f3d7587 FASE D: Hardening completo
2. 6df1e0c FASE C.1: auth.py
3. 54e20b3 FASE C.2: export.py + get_portal_from_request
4. cc085da FASE C.3: processing.py
5. 7e4e44b FASE C.4: admin.py
6. 0d45e22 FASE C.5: transactions.py
7. 93f667b FASE C.6: pareggi.py
8. cc91111 Cleanup: ultimi endpoint + fix qualita

---

## PROSSIMA SESSIONE

### Da fare (in ordine):
1. **Push lab-v2** a origin (8 commit da pushare)
2. **FASE C Parte 2**: Split database.py (4372 righe -> 5 moduli db/)
3. **FASE C Parte 3**: Split pareggi.js (4796 righe -> 4 moduli)
4. Audit Guardiana dopo ogni parte
5. Quando score >= 9.5: merge lab-v2 -> main

### Note Guardiana ultimo audit:
- pareggi.py (1137 righe) e' ancora grande - valutare split futuro
- /{portal}/api/historical rimane in main.py (bridge pattern necessario)
- CSP: TODO estrarre JS inline da index.html in file esterno

---

## MAPPA v2.0

| Fase | Stato |
|------|-------|
| 0 Occhi Nuovi | COMPLETATA |
| A Fondamenta | COMPLETATA |
| B Pulizia | COMPLETATA (8.5/10) |
| D Hardening | COMPLETATA (9.0/10) |
| C.1 Split main.py | COMPLETATA (main.py 3427->408) |
| C.2 Split database.py | DA FARE |
| C.3 Split pareggi.js | DA FARE |
| 1 Landing deploy | DA FARE |
| 2-4 Stagioni, SPRING, v2.0 | DA FARE |

---

## DATI PRODUZIONE

| Cosa | Valore |
|------|--------|
| Host | contabilitafamigliapra.it |
| IP | 35.193.39.185 (STATICO) |
| Path | /opt/contabilita-system/ |
| VM | cervello-contabilita (us-central1-c) |
| Tag Git | vm-deployed-v2.10.0 |

---

*FASE D + C.1 completate! Prossimo: C.2 (split database.py) nel Lab.*
