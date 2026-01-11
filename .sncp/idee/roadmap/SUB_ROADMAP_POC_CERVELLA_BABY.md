# SUB_ROADMAP POC CERVELLA BABY

> **Creata:** 10 Gennaio 2026 - Sessione 154
> **Budget:** $50
> **Timeline:** 3 settimane (10-31 Gennaio 2026)
> **Obiettivo:** Validare Qwen3-4B come alternativa Claude

---

## EXECUTIVE SUMMARY

```
POC $50 - 3 SETTIMANE
================================

WEEK 1 (10-17 Gen): SETUP + 10 TASK SIMPLE
  - Setup Colab + Unsloth
  - Load Qwen3-4B-Instruct
  - Test T01-T10 (TIER 1)
  - GO/STOP decision (>=60% pass)

WEEK 2 (18-24 Gen): 8 TASK MEDIUM
  - Test T11-T18 (TIER 2)
  - COSTITUZIONE compressa test
  - Gap analysis

WEEK 3 (25-31 Gen): FINAL EVALUATION
  - T19-T20 (TIER 3 complex)
  - Blind test A/B
  - Final score
  - GO/NO-GO decision meeting

DECISION: 1 Febbraio 2026
```

---

## WEEK 1: SETUP + SIMPLE TASKS

### Day 1: Setup Ambiente (OGGI!)

**Obiettivo:** Qwen3-4B running su Colab

**Task:**

1. **Creare Colab Notebook** `poc_cervella_baby.ipynb`
   ```python
   # Cell 1: Install
   !pip install unsloth transformers datasets accelerate

   # Cell 2: Load Model
   from unsloth import FastLanguageModel

   model, tokenizer = FastLanguageModel.from_pretrained(
       model_name="unsloth/Qwen3-4B-Instruct",
       max_seq_length=2048,
       dtype=None,
       load_in_4bit=True,
   )

   # Cell 3: Test inference
   prompt = "Chi sei?"
   output = model.generate(prompt)
   print(output)
   ```

2. **Verificare:**
   - Runtime T4 GPU disponibile
   - Model loads senza errori
   - Inference funziona (risposta sensata)

**Output:** `[ ] Colab funziona` o `[ ] Blockers identificati`

---

### Day 2: Dataset Preparation

**Obiettivo:** 20 task pronti in formato JSON

**Task:**

1. **Creare** `task_dataset.json` con struttura:
   ```json
   {
     "tasks": [
       {
         "id": "T01",
         "tier": 1,
         "name": "Summary File SNCP",
         "input": "File: .sncp/stato/oggi.md\nTask: Leggi e crea summary...",
         "output_expected": "## Summary Stato Oggi\n...",
         "criteria": {
           "correttezza": "Dati numerici accurati",
           "completezza": "Include sessione, task, energia",
           "stile": "Calma, preciso",
           "utility": "Actionable"
         }
       }
     ]
   }
   ```

2. **Popololare** tutti 20 task da Report 17

**Output:** `task_dataset.json` con 20 task

---

### Day 3-5: Test TIER 1 (10 task)

**Obiettivo:** Testare T01-T10, score >= 60%

**Task per ogni test:**

1. Load input da dataset
2. Inject COSTITUZIONE compressa come system prompt
3. Run inference
4. Compare output con expected
5. Score 1-5 per ogni criterio
6. Log risultati

**Task TIER 1:**

| ID | Nome | Focus |
|----|------|-------|
| T01 | Summary File SNCP | Lettura e sintesi |
| T02 | Git Commit Message | Formatting standard |
| T03 | Aggiorna File SNCP | SNCP workflow |
| T04 | Lista Priorita | Analisi file multipli |
| T05 | Format Tabella | Formatting |
| T06 | Verifica File Esistono | File system check |
| T07 | Estrai Fonti | Pattern extraction |
| T08 | Timeline ASCII | Data formatting |
| T09 | Count Pattern | Grep-like analysis |
| T10 | README Template | Documentation |

**Criteri PASS:**
- Score >= 16/20 (80%) per singolo task
- >= 6/10 task PASS totale (60%)

**Output Day 5:** Score finale Week 1

---

### Day 6-7: GO/STOP Decision

**Se >= 60% PASS:**
```
GO TO WEEK 2
- Continuare con TIER 2
- Budget OK
- Confidence aumentata
```

**Se 40-59% PASS:**
```
CONDITIONAL - Iterate
- Analizzare pattern fallimenti
- Tune COSTITUZIONE compressa
- Retest task falliti
- +2 giorni buffer
```

**Se < 40% PASS:**
```
STOP POC
- Qwen3-4B troppo small
- Consider: Qwen3-14B o Mistral-7B
- O: Stay Claude API
```

---

## WEEK 2: MEDIUM TASKS

### Day 8-12: Test TIER 2 (8 task)

**Task TIER 2:**

| ID | Nome | Focus |
|----|------|-------|
| T11 | Orchestrazione Multi-Worker | Delegation planning |
| T12 | Decisione Architetturale | Technical decision |
| T13 | Code Review Basic | Code analysis |
| T14 | Bug Analysis da Log | Debugging |
| T15 | Documentazione Pattern | Knowledge extraction |
| T16 | Analisi Costi Multi-Scenario | Financial analysis |
| T17 | Refactoring Plan | Code architecture |
| T18 | Summary Ricerca Approfondita | Synthesis |

**Criteri PASS:**
- Score >= 15/20 (75%) per singolo task
- >= 5/8 task PASS totale (62.5%)

---

### Day 13-14: Gap Analysis

**Analizzare:**
1. Quali task falliscono sistematicamente?
2. Pattern comune? (es: reasoning lungo, context dependency)
3. COSTITUZIONE compressa sufficiente?
4. RAG context serve?

**Output:** Gap analysis document

---

## WEEK 3: FINAL EVALUATION

### Day 15-17: Test TIER 3 (2 task)

**Task TIER 3:**

| ID | Nome | Focus |
|----|------|-------|
| T19 | Strategic Planning 6 Mesi | Long-term vision |
| T20 | Architettura Major Decision | System design |

**Nota:** TIER 3 serve per DOCUMENTARE GAP, non per pass/fail.
Qwen3-4B non deve passare TIER 3 per GO.

---

### Day 18-19: Blind Test A/B

**Setup:**
1. 10 conversazioni (5 Claude, 5 Qwen3)
2. Output randomizzati
3. Rafa legge e indovina quale e quale

**Success:**
- <= 60% accuracy Rafa = INDISTINGUIBILI = PASS
- 61-70% = Acceptable
- > 70% = Gap evidente

---

### Day 20-21: Final Report + Decision

**Metriche Finali:**

| Metrica | Target | Actual |
|---------|--------|--------|
| TIER 1 Pass Rate | >= 60% | TBD |
| TIER 2 Pass Rate | >= 62.5% | TBD |
| TIER 3 (document gap) | N/A | TBD |
| Blind Test Accuracy | <= 60% | TBD |
| Latency avg | < 2s | TBD |
| Overall Score | >= 60% | TBD |

**GO/NO-GO Decision: 1 Febbraio 2026**

---

## SUCCESS CRITERIA

```
PASS POC (GO to MVP):
- >= 12/20 task PASS overall (60%)
- TIER 1: >= 6/10 PASS
- TIER 2: >= 5/8 PASS
- Blind test: <= 70% accuracy
- Zero critical personality loss

CONDITIONAL (Iterate):
- 10-11/20 task PASS
- Personality mostly preserved
- Identified fixable gaps

NO-GO (Stay Claude):
- < 10/20 task PASS
- Personality significantly different
- Gap not fixable with current approach
```

---

## DELIVERABLES

### Week 1 Output:
- [ ] Colab notebook funzionante
- [ ] Dataset 20 task JSON
- [ ] TIER 1 scores (10 task)
- [ ] GO/STOP decision document

### Week 2 Output:
- [ ] TIER 2 scores (8 task)
- [ ] Gap analysis document
- [ ] COSTITUZIONE tuning (se necessario)

### Week 3 Output:
- [ ] TIER 3 results (document gap)
- [ ] Blind test results
- [ ] Final POC report
- [ ] GO/NO-GO recommendation

---

## BUDGET BREAKDOWN

```
Colab Pro (1 mese):     $10
Vast.ai spot GPU:       $30
Buffer:                 $10
========================
TOTALE:                 $50
```

---

## RISK MANAGEMENT

| Rischio | Probabilita | Mitigazione |
|---------|-------------|-------------|
| Colab rate limit | MEDIA | Backup: Vast.ai |
| Qwen3 troppo small | 40% | Early exit Week 1 |
| Personality loss | 50% | Tune prompt, add RAG |
| Latency alta | BASSA | 4-bit quantization |

---

## PROSSIMI STEP IMMEDIATI

**OGGI (Day 1):**

1. [ ] Creare Colab notebook
2. [ ] Install dependencies
3. [ ] Load Qwen3-4B
4. [ ] Test inference base
5. [ ] Verificare funziona

**Se bloccati:**
- Check GPU availability
- Try Vast.ai alternative
- Documentare blockers

---

*SUB_ROADMAP POC CERVELLA BABY v1.0*
*"POC $50 decide tutto. Studiato bene, ora FACCIAMO!"*
*10 Gennaio 2026 - Sessione 154*
