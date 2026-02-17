# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 17 Febbraio 2026 - Sessione 63
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE (deployato sessione 16) |
| **IP** | 35.193.39.185 STATICO |
| **Main** | d5d10f8 - cron v2.0.0 (pushato + tag vm-deployed-v2.11.0) |
| **Lab 2.0** | branch lab-v2 - S63 Filtro Periodo SPRING |
| **Locale** | ISOLATO! :8000=main (baked), :8001=lab-v2 (mount) |
| **Test** | 957/957 PASS (0 warnings, 0 fail) |
| **Database pkg** | v2.15.0 - 5 Mixin (core, transactions, pareggi, edits, seasons v2.1.0) |
| **Migrations** | v9 (v4-v6=stagione GIR/POS, v7=season_metadata, v8=originated_from_season, v9=INVERNO doppio anno) |
| **SPRING Stack** | Parser v1.0.0 + Matcher v1.0.0 + Router v1.1.0 + UI v1.2.0 + Analysis v1.0.0 |
| **DB LAB** | DATI PRODUZIONE REALI! (sync 16 Feb 2026) - 1,240 cap + 885 GIR + 232 POS |
| **Telegram VM** | FUNZIONANTE! Nuovo token configurato S59 |
| **NO deploy/merge** | Lab v2 resta separato, deploy parallelo quando pronto |

---

## REGOLA SESSIONE

- **SEMPRE su lab-v2** (mai main direttamente)
- Locale :8000 (main/baked) SOLO con conferma esplicita Rafa
- Ogni step fatto -> Guardiana audit -> standard 9.5/10

---

## ULTIME 3 SESSIONI

### S63 - Filtro Periodo SPRING Step 3 (9.5/10)

**Cosa:** Aggiunto filtro per periodo temporale alla riconciliazione SPRING. Idea di Rafa per lavorare mese per mese con Sergio.

**Backend** (`backend/routers/spring.py`):
- `ReconcileRequest` con `data_da`/`data_a` opzionali (YYYY-MM-DD)
- 3 helper: `_parse_date_param`, `_filter_spring_by_date`, `_filter_db_records_by_date`
- Validazione date invertite (400 se data_da > data_a)
- Filtro applicato sia a record SPRING che DB prima del matching
- Campo `filtro_periodo` nella risposta JSON quando attivo

**Frontend** (`spring-reconcile.js` v1.2.0 + `index.html`):
- 2 date picker `<input type="date">` nel pannello controlli
- Bottone "Tutti i periodi" per reset (nascosto quando filtro non attivo)
- Indicatore visuale periodo attivo (label verde)
- Event delegation: `spring-period-changed` (change) + `clear-spring-period` (click)

**Test** (`test_spring_api.py` v1.1.0): 22 nuovi test (15 helper + 7 API)
**Guardiana:** 9.5/10 - 0 P0/P1/P2, 3 P3 fixati (dead code, date invertite, test mancante)

### S62 - Verifica Diamante Step 2: Audit Match Confidence (9.5/10)
- 18 match sospetti analizzati: 16 TRUE MATCH (88.9%), 2 FALSE POSITIVE (0.1%)
- FP: Drewek/Narty (NL), Di Renzo/Ruscitti (HP) - entrambi WEAK
- Pattern: FEST prefix (4), cognome-only (6), parser artifacts (3)
- 6 fix mirati proposti per Step 7

### S61 - Verifica Diamante Step 1: Analisi Unmatched NL (9.3/10)
- Rafa testato browser: SPRING funziona!
- spring_analysis.py v1.0.0, report NL: 390/418 cap (93.3%), 348/352 GIR (98.9%)
- 9 match sospetti, 1 FP confermato

---

## SUBROADMAP: "Verifica Diamante SPRING" (S61+)

| Step | Cosa | Stato |
|------|------|-------|
| 1 | Analisi Unmatched NL (script + report) | COMPLETATO S61 (9.3/10) |
| 2 | Audit Match Confidence (cross-portal) | COMPLETATO S62 (9.5/10) |
| 3 | Filtro Periodo (data_da/data_a + UI date picker) | COMPLETATO S63 (9.5/10) |
| **4** | **Cross-Portal HP + SHE (analisi comparativa)** | **PROSSIMO** |
| 5 | Hard Test Edge Case (+20 test da finding reali) | - |
| 6 | Test Endpoint Reconcile API (+10 test) | - |
| 7 | Fix Mirati (6 fix proposti con evidenza concreta) | - |
| 8 | Report Diamante (metriche finali per portale) | - |

**Finding da Step 1+2:**
- P1: 2 FP confermati (Drewek/Narty NL, Di Renzo/Ruscitti HP) - entrambi WEAK
- Fix proposti Step 7: P1 strip FEST (4 match), P2 doppio NL (1), P3 suffix HP (1)
- Caparre negative = rimborsi (legittimo)
- Nomi "/" e "NO SHOW" = dato sporco alla fonte

---

## NOTE IMPORTANTI
- **Telegram VM**: FUNZIONANTE con nuovo token (17 Feb 2026)
- **SPRING Stack completo**: Parser + Matcher + Router + UI v1.2.0 + File Management + Analysis
- **DB LAB**: dati PRODUZIONE REALI (sync 16 Feb 2026)
- **FASE 4 tab**: NASCOSTO (logica matching INTATTA!)
- **TICKET tab**: NASCOSTO (funzione attiva)
- **Dark mode**: NASCOSTO (forza tema light)
- **CSP ready**: 0 inline scripts
- **Nota merge**: unificare APP_ENV -> ENVIRONMENT prima del merge

---

*"Ultrapassar os proprios limites!" - Un progresso al giorno, sempre!*
