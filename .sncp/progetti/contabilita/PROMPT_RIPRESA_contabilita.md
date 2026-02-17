# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 17 Febbraio 2026 - Sessione 61
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE (deployato sessione 16) |
| **IP** | 35.193.39.185 STATICO |
| **Main** | d5d10f8 - cron v2.0.0 (pushato + tag vm-deployed-v2.11.0) |
| **Lab 2.0** | branch lab-v2 - S61 Verifica Diamante SPRING |
| **Locale** | ISOLATO! :8000=main (baked), :8001=lab-v2 (mount) |
| **Test** | 935/935 PASS (0 warnings, 0 fail) |
| **Database pkg** | v2.15.0 - 5 Mixin (core, transactions, pareggi, edits, seasons v2.1.0) |
| **Migrations** | v9 (v4-v6=stagione GIR/POS, v7=season_metadata, v8=originated_from_season, v9=INVERNO doppio anno) |
| **SPRING Stack** | Parser v1.0.0 + Matcher v1.0.0 + Router v1.1.0 + UI v1.1.0 + Analysis v1.0.0 |
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

### S61 - Verifica Diamante SPRING Step 1 (9.3/10)

**Rafa ha testato nel browser:** SPRING funziona! 95.8% match, upload/delete/multi-file tutto OK.

**Decisione Rafa:** Prima di dichiarare lab-v2 completo, fare sessioni di LOGICA, REVIEW, ANALISI per verificare che i dati siano di fiducia. "Enriquecer os dados do diamante."

**Idea Rafa:** Filtro per periodo (mese/trimestre/custom) per analisi mirata.

**Step 1 completato:**
- Script `scripts/spring_analysis.py` v1.0.0 creato (--portal NL/HP/SHE --audit-matches)
- Report NL: `docs/SPRING_ANALYSIS_NL.md` (4181 righe)
- Risultati NL: 390/418 cap (93.3%), 348/352 GIR (98.9%), 724/738 match con confidence 0.95+
- 9 match sospetti (1 falso positivo confermato: Drewek/Narty WEAK)
- 28 cap DB senza match (rimborsi, nomi composti, dati vecchi)
- 187 cap SPRING senza match (mesi Gen-Set 2025, DB parte da Ott)
- Guardiana: 9.3/10 -> fix P2 DRY + P2 params + 4 P3

### S60 - SPRING File Management (media 9.5/10)
- Multi-file checkbox, upload POST, delete DELETE, data modifica
- 17 nuovi test API. spring-reconcile.js v1.1.0, spring.py 2 endpoint

### S59 - Fix Telegram + Footer Cleanup (9.3/10)
- Telegram: nuovo token. Footer: CAPARRE, VS, hide TICKET+Totali

---

## SUBROADMAP: "Verifica Diamante SPRING" (S61+)

| Step | Cosa | Stato |
|------|------|-------|
| 1 | Analisi Unmatched NL (script + report) | COMPLETATO (9.3/10) |
| **2** | **Audit Match Confidence (falsi positivi in dettaglio)** | **PROSSIMO** |
| 3 | Filtro Periodo (data_da/data_a backend + UI date picker) | - |
| 4 | Cross-Portal HP + SHE (analisi comparativa) | - |
| 5 | Hard Test Edge Case (+20 test da finding reali) | - |
| 6 | Test Endpoint Reconcile API (+10 test, gap 0->10) | - |
| 7 | Fix Mirati (SOLO con evidenza concreta, test red->green) | - |
| 8 | Report Diamante (metriche finali per portale, livello fiducia) | - |

**Finding da investigare:**
- P1: Falso positivo Drewek Konrad <-> Narty Marek (WEAK, nome_sim 0.50)
- P2: Radnic Vittorio score 90/100 ma non matchato (consumato da altro?)
- P2: Nomi con "/" (Vernino/Cavallo) non matchano
- P3: client_name "NO SHOW" in GIR DB (dato sporco)
- Info: Caparre negative (-25, -356.4) = rimborsi, legittimo non matchare

---

## NOTE IMPORTANTI
- **Telegram VM**: FUNZIONANTE con nuovo token (17 Feb 2026)
- **SPRING Stack completo**: Parser + Matcher + Router + UI + File Management + Analysis
- **DB LAB**: dati PRODUZIONE REALI (sync 16 Feb 2026)
- **FASE 4 tab**: NASCOSTO (logica matching INTATTA!)
- **TICKET tab**: NASCOSTO (funzione attiva)
- **Dark mode**: NASCOSTO (forza tema light)
- **CSP ready**: 0 inline scripts
- **Nota merge**: unificare APP_ENV -> ENVIRONMENT prima del merge

---

*"Ultrapassar os proprios limites!" - Un progresso al giorno, sempre!*
