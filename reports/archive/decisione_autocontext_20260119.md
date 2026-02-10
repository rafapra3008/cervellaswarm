# DECISIONE AUTO-CONTEXT - Sessione 276

> **Data:** 19 Gennaio 2026
> **Decisione:** OPZIONE A - Aspettare W2.5
> **Standard richiesto:** Minimo 9.5/10

---

## CONTESTO

Durante il test di AUTO-CONTEXT su Miracollo PMS, abbiamo scoperto:

- `extract_references()` ritorna lista vuota (documentato come W2.5)
- Senza references, PageRank non funziona
- File ordinati ALFABETICAMENTE invece che per importanza
- `.claude/hooks/` appare prima di `backend/routers/`

---

## ANALISI GUARDIANE

| Guardiana | Verdetto | Score Attuale |
|-----------|----------|---------------|
| Qualita | USA_CON_WORKAROUND | 6/10 |
| Ops | USE_WITH_CAUTION | - |

**Concordano:** Feature SAFE ma SUBOTTIMALE

---

## DECISIONE RAFA

```
"Non abbiamo fretta nessunaaa"
"Facciamo tutto fino alla fine che raggiungiamo il nostro standard"
"Minimo 9.5 di score"
```

**SCELTA: OPZIONE A - Aspettare W2.5**

---

## COSA SIGNIFICA

1. **NON usare `--with-context`** fino a W2.5 completato
2. **W2.5 = reference extraction** implementato correttamente
3. **PageRank funzionante** con dipendenze reali
4. **Score target: 9.5/10** prima di rilasciare

---

## PIANO W2.5

| Task | Descrizione | Sessioni stimate |
|------|-------------|------------------|
| 1 | Implementare `extract_references()` per Python | 1 |
| 2 | Implementare per TypeScript/JavaScript | 1 |
| 3 | Test su CervellaSwarm | 0.5 |
| 4 | Test su Miracollo | 0.5 |
| 5 | Audit Guardiana Qualita (target 9.5/10) | 0.5 |

**Totale stimato:** 3-4 sessioni

---

## PRINCIPI COSTITUZIONE APPLICATI

- **"Fatto BENE > Fatto VELOCE"** - Aspettiamo per fare bene
- **"Una feature perfetta > Dieci mediocri"** - AUTO-CONTEXT perfetto
- **"Il tempo non ci interessa"** - Nessuna fretta
- **"SU CARTA != REALE"** - Vogliamo REALE funzionante

---

## STATO ATTUALE W2

```
W2 Tree-sitter Progress:
├── Day 1: Core modules          DONE (142 test)
├── Day 2: Spawn integration     DONE (26 test)
├── Day 3: Test Miracollo        DONE (problema trovato!)
├── Day 4-5: W2.5 references     PIANIFICATO
├── Day 6-7: Polish + 9.5/10     PIANIFICATO
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*

**Cervella & Rafa - Sessione 276**
