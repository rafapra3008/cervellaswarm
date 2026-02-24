# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 24 Febbraio 2026 - Sessione 140
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S140 QA Round 96 + Fix DELETE

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | DEPLOYATO S138 - Fix stagioni chiuse LIVE |
| **3 Hotel Agent** | TUTTI v2.0.0 daily_closed (deployato S139) |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1411 portale PASS** (0 fail) + 333 agent |
| **Round QA** | 96 (CR 9.1 + BH 12 bug + LR 8.0) |
| **Score attuale** | ~8.5/10 - target 9.5+ |
| **Subroadmap** | `docs/SUBROADMAP_S140_LUCIDATURA.md` (20 step, 6 fasi, Guardiana 9.3 APPROVED) |

---

## S140 - Cosa e' stato fatto

### QA Round 96 - 3 Cervelle in parallelo
- **Code Review**: 9.1/10 - 3 P1 (timing login, reprocess pubblico, codici hardcoded) + 7 P2
- **Bug Hunter**: 4 P1 + 8 P2 (12 bug totali)
- **Logic Review**: 8.0/10 - 5 P2 + 4 P3
- **Consensus**: 34 finding totali, 30 unici, tutti tracciati in subroadmap

### Fix Step 1: DELETE 404 (PARZIALE - solo codice, NON deployato)
- **Bug reale**: NON era endpoint mancante. Era `FOREIGN KEY constraint failed` wrappato come 404
- **Causa**: GIR id=1404 su SHE aveva pareggio_parking collegato (id=658, fuzzy_parking, confidence=0.7)
- **Fix (Opzione B - decisione Rafa)**: Check pareggi collegati PRIMA del DELETE. Se presenti, messaggio chiaro: "Rimuovi prima il pareggio"
- **HTTP status**: 409 Conflict (non piu 404) per righe con pareggi collegati
- **File modificati**: `backend/database/transactions.py` + `backend/routers/transactions.py` + `tests/test_delete_transactions.py`
- **Test**: 1411/1411 PASS, 25/25 delete test PASS
- **NON ANCORA DEPLOYATO** sulla VM - va deployato nella FASE N.6

---

## Subroadmap "La Lucidatura" - 20 Step

| Fase | Cosa | Status |
|------|------|--------|
| **N.1** | Bug Rafa: DELETE 404 + checkout SHE/HP + design HP | Step 1 FATTO (codice), Step 2-3 PENDING |
| **N.2** | Agent: HC.io + CB 429 + watermark gap + multi-batch + safety | 5 step PENDING |
| **N.3** | Backend: cleanup perf + pre_close stats + health deep | 3 step PENDING |
| **N.4** | Frontend: undoData + initAnnullamenti + NOLOCK importo=0 | 3 step PENDING |
| **N.5** | Security: timing login + PUBLIC_ENDPOINTS + sanitize | 3 step PENDING |
| **N.6** | Deploy VM + Agent hotel + Guardiana finale | 3 step PENDING |

**Dettagli completi**: `docs/SUBROADMAP_S140_LUCIDATURA.md`

---

## Bug Rafa da fixare (trovati S140)

1. **DELETE 404** -> FIX FATTO (codice), da deployare. Era FK constraint non gestito
2. **Date checkout SHE/HP non visibili** sulla UI V3 -> da investigare
3. **Design HP**: "Canele" scritto male + colori non prendono -> da investigare
4. **Dropdown STAGIONE Puzzle**: ora FUNZIONA (Rafa conferma) -> risolto

---

## Lezioni Apprese (Sessione 140)

### Cosa ha funzionato bene
- QA Round con 3 Cervelle in parallelo: copertura completa, 34 finding trovati
- Subroadmap dettagliata con Guardiana che valida (R1 7.5 -> R2 9.3)

### Cosa non ha funzionato
- Ho agito troppo di fretta sul fix DELETE senza ragionare prima (cascade vs blocco)
- Ho scritto codice prima di capire il comportamento desiderato da Rafa
- La Costituzione dice "Fatto BENE > Fatto VELOCE" e io l'ho dimenticato

### Pattern candidato
- "RAGIONARE PRIMA DI AGIRE" - Sempre chiedere Rafa PRIMA di scegliere approccio - Azione: PROMUOVERE
- "Diagnosi completa tramite log VM" - I log di journalctl hanno rivelato il vero bug (FK, non 404) - Azione: MONITORARE

---

## TODO Prossima Sessione (S141)

1. **Step 2**: Fix date checkout SHE/HP non visibili (diagnosi + fix)
2. **Step 3**: Fix design HP (Canele + colori)
3. **Step 4+**: Proseguire FASE N.2 (agent fix)
4. **Monitorare**: Primo run daily_closed (HC.io) - verificare che gira

---

## Dove leggere

| Cosa | File |
|------|------|
| Subroadmap completa | `docs/SUBROADMAP_S140_LUCIDATURA.md` |
| Fix DELETE (Opzione B) | `backend/database/transactions.py:864-900` |
| Router DELETE (409 vs 404) | `backend/routers/transactions.py:963-968` |
| Test DELETE | `tests/test_delete_transactions.py` |

---

*S140: QA Round 96 completato (3 Cervelle, 34 finding). Fix DELETE con Opzione B (blocco+messaggio). Score ~8.5, target 9.5+. Lezione: ragionare PRIMA di agire.*
