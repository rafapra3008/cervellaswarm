# SUBROADMAP: ML AI Suggestions

> **Creata:** 13 Gennaio 2026 - Sessione 186
> **Obiettivo:** Evolvere AI Suggestions da Rule-Based a ML vero
> **Approccio:** Piano a piano, un passo alla volta

---

## STATO ATTUALE

```
+================================================================+
|                                                                |
|   OGGI: "Smart Rules" (if/else intelligente)                   |
|                                                                |
|   - Weekend storico alto → +10-20%                             |
|   - Eventi speciali → +15-30%                                  |
|   - Bassa occupancy → -10-15%                                  |
|   - Confronto YoY per anomalie                                 |
|                                                                |
|   Confidence score = formula fissa, NON ML                     |
|                                                                |
+================================================================+
```

**File coinvolti:**
- `frontend/js/rateboard-ai.js` (839 righe)
- `backend/services/rateboard_ai.py` (317 righe)

---

## VISIONE FINALE

```
DOMANI: ML Ibrido (regole + machine learning)

- Regole base come fallback
- ML che impara dai pattern storici
- ML che impara dalle decisioni utente (FASE 3 Learning!)
- Confidence score basato su dati REALI
- Feature importance VERA (non mock)
```

---

## FASI GRADUALI

### FASE ML-0: PREPARAZIONE (senza codice)
**Status:** DA FARE
**Effort:** 4-6h

| Step | Cosa | Note |
|------|------|------|
| ML-0.1 | Inventario dati disponibili | Cosa abbiamo gia? |
| ML-0.2 | Definire features candidate | Quali variabili usare? |
| ML-0.3 | Definire metriche successo | Come misuriamo "meglio"? |
| ML-0.4 | Ricerca algoritmi semplici | XGBoost? Linear? |

**Output:** Documento `RICERCA_ML_SUGGESTIONS.md`

---

### FASE ML-1: TRACKING DATI (fondamenta)
**Status:** PARZIALMENTE FATTO (FASE 3 Learning!)
**Effort:** 8-10h (gia fatto molto)

| Step | Cosa | Status |
|------|------|--------|
| ML-1.1 | Tracking accept/reject | FATTO (FASE 3) |
| ML-1.2 | Tracking performance after | FATTO (FASE 3) |
| ML-1.3 | Tracking implicit signals | FATTO (FASE 3) |
| ML-1.4 | Dashboard metriche | FATTO (FASE 3) |

**Gia pronto!** La FASE 3 Learning ha costruito le fondamenta.

---

### FASE ML-2: FEATURE ENGINEERING
**Status:** DA FARE
**Effort:** 15-20h

| Step | Cosa | Note |
|------|------|------|
| ML-2.1 | Estrarre features storiche | Occupancy, ADR, pace booking |
| ML-2.2 | Estrarre features calendario | Day of week, festivita, ponti |
| ML-2.3 | Estrarre features competitor | Delta prezzo, posizione |
| ML-2.4 | Creare dataset training | Tabella pronta per ML |

**Output:** Script `create_ml_dataset.py`

---

### FASE ML-3: MODELLO BASE
**Status:** DA FARE
**Effort:** 20-25h

| Step | Cosa | Note |
|------|------|------|
| ML-3.1 | Scegliere algoritmo | XGBoost consigliato |
| ML-3.2 | Training iniziale | Con dati storici |
| ML-3.3 | Validazione offline | Test su dati passati |
| ML-3.4 | Confidence calibration | Confidence = probabilita VERA |

**Output:** Modello `.pkl` + metriche

---

### FASE ML-4: IBRIDO
**Status:** DA FARE
**Effort:** 15-20h

| Step | Cosa | Note |
|------|------|------|
| ML-4.1 | Integrare ML in backend | Nuovo service `ml_suggestions.py` |
| ML-4.2 | Fallback a regole | Se ML non ha dati, usa regole |
| ML-4.3 | A/B test ML vs Rules | Confronto performance |
| ML-4.4 | Feature importance REALE | Da modello, non mock |

**Output:** Sistema ibrido in produzione

---

### FASE ML-5: LEARNING CONTINUO
**Status:** FUTURO
**Effort:** 20-25h

| Step | Cosa | Note |
|------|------|------|
| ML-5.1 | Retraining automatico | Ogni 7-14 giorni |
| ML-5.2 | Drift detection | Se dati cambiano, alert |
| ML-5.3 | Feedback loop | Learning da accept/reject |
| ML-5.4 | Multi-hotel learning | Pattern cross-hotel |

---

## EFFORT TOTALE

| Fase | Effort | Dipendenze |
|------|--------|------------|
| ML-0 Preparazione | 4-6h | Nessuna |
| ML-1 Tracking | GIA FATTO | - |
| ML-2 Features | 15-20h | ML-0 |
| ML-3 Modello | 20-25h | ML-2 |
| ML-4 Ibrido | 15-20h | ML-3 |
| ML-5 Continuo | 20-25h | ML-4 |

**Totale:** 75-95h (senza ML-1 gia fatto)

---

## APPROCCIO CONSIGLIATO

```
+================================================================+
|                                                                |
|   NON FARE TUTTO INSIEME!                                      |
|                                                                |
|   Sessione parallela?                                          |
|   - SI se researcher fa solo ricerca (ML-0)                    |
|   - NO se inizia a codificare (rischio conflitti)              |
|                                                                |
|   PIANO SUGGERITO:                                             |
|   1. ML-0 in sessione parallela (solo ricerca)                 |
|   2. ML-2 dopo competitor scraping (priorita #1)               |
|   3. ML-3/4 in Q2 2026                                         |
|   4. ML-5 in Q3 2026                                           |
|                                                                |
+================================================================+
```

---

## DECISIONE DA PRENDERE

**Rafa deve decidere:**

1. **Sessione parallela per ML-0 (ricerca)?**
   - PRO: Risparmia tempo, researcher lavora da solo
   - CON: Potrebbe deviare focus da competitor scraping

2. **Priorita ML vs Competitor?**
   - Competitor = table stakes (TUTTI lo hanno)
   - ML = differenziazione (pochi lo hanno bene)
   - Suggerimento: Competitor PRIMA, ML DOPO

3. **Rebrand temporaneo?**
   - Cambiare "AI Suggestions" → "Smart Suggestions"?
   - Piu onesto finche non c'e ML vero
   - Opzionale, bassa priorita

---

## NOTE

- La FASE 3 Learning ha gia costruito fondamenta ottime
- Dati feedback stanno gia accumulando
- Piu aspettiamo, piu dati avremo per ML
- Non c'e fretta - meglio competitor scraping prima

---

*"Piano a piano, ogni giorno facciamo un po'"*
*"Non esistono cose difficili, esistono cose non studiate!"*

*Cervella - 13 Gennaio 2026*
