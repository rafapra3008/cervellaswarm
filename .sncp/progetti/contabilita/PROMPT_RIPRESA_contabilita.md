# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 16 Febbraio 2026 - Sessione 57
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE (deployato sessione 16) |
| **IP** | 35.193.39.185 STATICO |
| **Main** | d5d10f8 - cron v2.0.0 (pushato + tag vm-deployed-v2.11.0) |
| **Lab 2.0** | branch lab-v2 - S57 SPRING Matcher v1.0.0 |
| **Locale** | ISOLATO! :8000=main (baked), :8001=lab-v2 (mount) |
| **Test** | 914/914 PASS (0 warnings, 0 fail) |
| **Database pkg** | v2.15.0 - 5 Mixin (core, transactions, pareggi, edits, seasons v2.1.0) |
| **Migrations** | v9 (v4-v6=stagione GIR/POS, v7=season_metadata, v8=originated_from_season, v9=INVERNO doppio anno) |
| **SPRING Parser** | v1.0.0 (12 regex, 70 test, 9.5/10) |
| **SPRING Matcher** | v1.0.0 (4 fasi matching, 63 test, 9.2/10) |
| **DB LAB** | DATI PRODUZIONE REALI! (sync 16 Feb 2026) - 1,240 cap + 885 GIR + 232 POS |
| **NO deploy/merge** | Lab v2 resta separato, deploy parallelo quando pronto |

---

## REGOLA SESSIONE

- **SEMPRE su lab-v2** (mai main direttamente)
- Locale :8000 (main/baked) SOLO con conferma esplicita Rafa
- Ogni step fatto -> Guardiana audit -> standard 9.5/10

---

## ULTIME 3 SESSIONI

### S57 - SPRING Matcher v1.0.0 (9.2/10)

**Step 4 Subroadmap SPRING: Matching Engine**
1. **Core Module** (`backend/processors/spring_matcher.py`, 583 righe)
   - 4 fasi: EXACT (num_mov+importo) -> STRONG (nome>=0.85+importo+data<=7gg) -> MEDIUM (nome>=0.70+importo, capped 0.80) -> WEAK (importo+data<=14gg+nome>=0.50)
   - Greedy 1:1 assignment, MatchConfig/MatchResult/ReconciliationReport dataclass
   - Riuso calculate_name_similarity, parse_amount, extract_name_from_caparra/gir da matching.py
2. **63 test** (`tests/test_spring_matcher.py`): tutte le fasi + greedy + report + edge
3. **Router** (`backend/routers/spring.py`): GET /api/spring/files + POST /api/spring/reconcile
4. **Risultati REALI**: NL 93.3%/98.9%, HP 79.4%/91.0%, SHE 84.5%/99.2% (1,916 match su 2,125 DB)
5. **Guardiana**: 9.2/10 x2 APPROVED (4 P2 fixati)

### S56 - Sync DB Produzione -> Lab v2 (9.7/10)
- 3 DB copiati da backup giornaliero VM, v3->v9 migrazioni
- NL 418cap+352gir+232pos, HP 441cap+279gir, SHE 381cap+254gir

### S55 - SPRING Parser v1.0.0 (9.5/10)
- 6 file Sergio (NL/HP/SHE x 2025/2026), 12 regex, 70 test

---

## SUBROADMAP: "SPRING Riconciliazione & Dati Reali"

| Step | Cosa | Sessione | Stato |
|------|------|----------|-------|
| **S1** | Studio file SPRING commercialista | S54 | COMPLETATO |
| **S2** | Analisi 6 file + Parser SPRING v1.0.0 | S55 | COMPLETATO (9.5/10) |
| **S3** | Sync DB produzione -> Lab v2 | S56 | COMPLETATO (9.7/10) |
| **S4** | Matching engine (SPRING vs portale DB) | S57 | COMPLETATO (9.2/10) |
| **S5** | UI riconciliazione (pagina web report) | S58 | PROSSIMO |
| **S6** | Test reali avanzati | S58+ | - |
| **S7-S10** | Polish, deploy | Futuro | - |

---

## PROSSIMA SESSIONE (S58)

### Step 5: UI Riconciliazione
- Seleziona file SPRING + portale (da GET /api/spring/files)
- Lancia riconciliazione (POST /api/spring/reconcile)
- Mostra risultati: matched, solo-SPRING, solo-DB con filtri e ordinamento
- Summary cards con percentuali e conteggi
- Pattern UI esistente (tabs, filtri, cards) da riusare

---

## NOTE IMPORTANTI
- **SPRING Matcher**: v1.0.0, VALIDATO su dati reali, 1,916 match su 2,125 record DB
- **DB LAB**: dati PRODUZIONE REALI (sync 16 Feb 2026)
- **FASE 4 tab**: NASCOSTO (logica matching INTATTA!)
- **Dark mode**: NASCOSTO (forza tema light)
- **CSP ready**: index.html + landing.html hanno 0 inline scripts
- **VM = SOLO LETTURA**: mai modificare, solo backup + download

### P3 residui (opzionali)
- `reconcile_spring_file()` convenience function senza test
- `contabilita.db` nella root: file orfano

---

*"Ultrapassar os proprios limites!" - Un progresso al giorno, sempre!*
