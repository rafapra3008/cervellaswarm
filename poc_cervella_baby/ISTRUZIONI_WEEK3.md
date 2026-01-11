# POC Week 3 - Istruzioni Esecuzione

> **Data:** 11 Gennaio 2026
> **Task:** T19-T20 (TIER 3 - Complex)
> **Notebook:** `poc_notebook_week3.ipynb`

---

## IMPORTANTE

```
+================================================================+
|                                                                |
|   Week 3 documenta i LIMITI del modello                        |
|   Il POC e' GIA' PASS con Week 1 + Week 2!                     |
|                                                                |
|   17/18 task PASS (94.4%) = SUCCESSO                           |
|                                                                |
+================================================================+
```

---

## Step-by-Step

### 1. Apri Google Colab

```
https://colab.research.google.com
```

### 2. Upload Notebook

- File > Upload notebook
- Seleziona: `poc_notebook_week3.ipynb`

### 3. Configura Runtime

- Runtime > Change runtime type
- Hardware accelerator: **T4 GPU**
- Click "Save"

### 4. Esegui Celle in Ordine

| Cella | Descrizione | Tempo Stimato |
|-------|-------------|---------------|
| 1-5 | Setup + Install | ~3 min |
| 6-7 | Load Model | ~2 min |
| 8-9 | System Prompt | instant |
| 10-11 | Task Dataset | instant |
| 12-13 | Inference Function | instant |
| 14-15 | **Run T19** | ~60-90s |
| 16-17 | **Run T20** | ~60-90s |
| 18-21 | Evaluation | manuale |
| 22-25 | Save Results | instant |

**Tempo totale stimato:** ~10-15 minuti

### 5. Valutazione T19

Dopo aver visto l'output di T19, valuta:

```python
results[0] = evaluate_task(results[0],
    correttezza=?,   # 1-5: Logica sensata?
    completezza=?,   # 1-5: Copre tutti i punti?
    stile=?,         # 1-5: Filosofia Cervella?
    utility=?,       # 1-5: Actionable?
    gap_notes="..."  # Cosa manca?
)
```

### 6. Valutazione T20

Dopo aver visto l'output di T20, valuta:

```python
results[1] = evaluate_task(results[1],
    correttezza=?,   # 1-5: Logica sensata?
    completezza=?,   # 1-5: Copre tutti i punti?
    stile=?,         # 1-5: Filosofia Cervella?
    utility=?,       # 1-5: Actionable?
    gap_notes="..."  # Cosa manca?
)
```

### 7. Salva Risultati

Esegui cella 25 per salvare `week3_results.json`

### 8. Download Risultati

- Click destro su `week3_results.json`
- Download
- Salva in `poc_cervella_baby/results/`

---

## Task Overview

### T19: Strategic Planning 6 Mesi

**Input:** Crea piano strategico per 3 progetti (Miracollo, CervellaSwarm, Cervella Baby)

**Output atteso:**
1. Roadmap mensile con milestone
2. Allocation tempo (ore/settimana)
3. Budget allocation
4. Risk management (top 3)
5. Success criteria
6. Decision points GO/NO-GO

**Cosa valutiamo:** Capacita di ragionamento strategico multi-variabile

### T20: Architettura Major Decision SNCP

**Input:** Scegli architettura per SNCP cross-project tra 4 opzioni

**Output atteso:**
1. Analisi 4 opzioni con score
2. Scelta motivata (PERCHE)
3. Schema architettura
4. Implementation plan
5. Migration plan
6. Risk e mitigation
7. Success criteria

**Cosa valutiamo:** Capacita decisionale architetturale complessa

---

## Criteri Valutazione TIER 3

| Criterio | Cosa Cercare |
|----------|--------------|
| **Correttezza** | Logica sensata, dati plausibili, no allucinazioni |
| **Completezza** | Copre TUTTI i punti richiesti nell'output |
| **Stile Cervella** | Filosofia, PERCHE, struttura, calma |
| **Utility** | Actionable, decision-ready, usabile |

**Pass:** Score >= 70%

---

## GAP Documentation

Per ogni task, documenta i GAP:

```
GAP T19:
- [ ] Manca X
- [ ] Non considera Y
- [ ] Budget non realistico

GAP T20:
- [ ] Schema non chiaro
- [ ] Migration plan incompleto
- [ ] ...
```

Questi GAP informano il MVP Hybrid!

---

## Dopo Week 3

1. Copia `week3_results.json` nel repo
2. Torna su Claude Code
3. Procediamo con GO/NO-GO documentation

---

*"La magia ora e' con coscienza!"*
*"Documentare i LIMITI e' parte del successo!"*
