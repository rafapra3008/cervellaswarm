# Architect Pattern - W3-B

> **Creato:** 19 Gennaio 2026 - Sessione 283
> **Status:** PRODUCTION READY (Benchmark 100%)
> **Score:** 10/10 Guardiana Approved

---

## Overview

L'Architect Pattern introduce un layer di **planning** prima dell'implementazione per task complessi. Un agente specializzato (cervella-architect, Opus) analizza il task e genera un piano strutturato che i worker seguono.

```
+================================================================+
|   SENZA ARCHITECT          |   CON ARCHITECT                  |
|   Task → Worker → Code     |   Task → Classifier → Architect  |
|   Success: ~70%            |         → Plan → Worker → Code   |
|                            |   Success: 85%+ target           |
+================================================================+
```

---

## Come Funziona

```
Task arriva
    │
    ▼
task_classifier.py
    │
    ├─── SIMPLE/MEDIUM ──────► Worker diretto
    │
    └─── COMPLEX/CRITICAL ───► cervella-architect
                                    │
                                    ▼
                              Genera PLAN.md
                                    │
                                    ▼
                              validate_plan()
                                    │
                        ┌───────────┴───────────┐
                        │                       │
                    APPROVED               REJECTED (max 2x)
                        │                       │
                        ▼                       ▼
                    Worker segue           Fallback:
                    il piano               Worker senza plan
```

---

## Classificazione Task

### Livelli di Complessità

| Livello | Score | Architect? | Esempio |
|---------|-------|------------|---------|
| SIMPLE | < 0.3 | No | Fix typo, rename variable |
| MEDIUM | 0.3-0.5 | No (opzionale) | Add logging, minor bug fix |
| COMPLEX | 0.5-0.7 | Sì | Implement feature, integrate system |
| CRITICAL | ≥ 0.7 | Sì (required) | Refactor globale, migrate sistema |

### Keywords e Pesi

**High complexity (0.7-0.9):**
- refactor, architecture, redesign, migrate, restructure, rewrite

**Medium complexity (0.5-0.6):**
- complex, multiple files, across modules, cross-cutting, breaking change

**Pattern triggers (0.4-0.5):**
- integrate, implement, add new, create system, dashboard

**Simple indicators (bypass):**
- fix typo, update comment, rename, minor, small, quick, simple

### Formula Score

```python
keyword_score = sum(matched_keywords_weights)  # cap 1.5
file_score = 0.8 if files >= 5 else 0.5 if files >= 3 else 0
final_score = min((keyword_score + file_score) / 1.5, 1.0)
```

---

## File del Sistema

| File | Scopo | Righe |
|------|-------|-------|
| `scripts/swarm/task_classifier.py` | Classificazione task | 280 |
| `scripts/swarm/architect_flow.py` | Orchestrazione flow | 525 |
| `.swarm/prompts/cervella-architect.md` | Prompt Opus | 259 |
| `.swarm/templates/PLAN_TEMPLATE.md` | Template piano | 150 |

---

## Uso da CLI

### Classificare un Task

```bash
python scripts/swarm/task_classifier.py "refactor authentication module"

# Output:
# Complexity:      critical
# Should Architect: True
# Confidence:      0.93
# Triggers:        refactor
```

### Check Rapido

```python
from scripts.swarm.task_classifier import should_use_architect

if should_use_architect("migrate database to PostgreSQL"):
    # Route to architect
else:
    # Direct to worker
```

---

## Piano Generato

Il piano segue il template in `.swarm/templates/PLAN_TEMPLATE.md`:

```markdown
# PLAN: [Task Name]

## Metadata
- Complexity: COMPLEX
- Estimated Files: 5
- Risk Level: MEDIUM

## Phase 1: Analysis
- [ ] Step 1.1: ...
- [ ] Step 1.2: ...

## Phase 2: Design
- [ ] Step 2.1: ...

## Phase 3: Implementation
- [ ] Step 3.1: ...

## Phase 4: Validation
- [ ] Step 4.1: Run tests
- [ ] Step 4.2: Review changes

## Success Criteria
- [ ] All tests pass
- [ ] No regressions
```

---

## Benchmark Results

```
+================================================================+
|   BENCHMARK W3-B Day 7 - Sessione 283                         |
|   Classification Accuracy: 100% (10/10)                       |
|   Routing Accuracy:        100% (10/10)                       |
|   Status: PASSED                                              |
+================================================================+
```

### Task Distribution Testati

| Tipo | Count | Architect? |
|------|-------|------------|
| SIMPLE | 5 | No |
| COMPLEX | 2 | Yes |
| CRITICAL | 3 | Yes |

---

## Fallback Logic

Se il piano viene rifiutato 2 volte:

1. Prima rejection → Architect rigenera con feedback
2. Seconda rejection → Architect rigenera con feedback
3. Terza rejection → **Fallback**: Worker procede senza piano

```python
MAX_PLAN_REVISIONS = 2

if rejection_count > MAX_PLAN_REVISIONS:
    return fallback_to_worker(task)
```

---

## Integrazione con W3-A

L'Architect usa le API di Semantic Search (W3-A) per:

- `find_symbol()` - Trovare definizioni esistenti
- `find_callers()` - Capire impatto modifiche
- `estimate_impact()` - Valutare rischio

```python
from scripts.utils.impact_analyzer import estimate_impact

impact = estimate_impact("AuthService")
# Returns: risk_score, affected_files, recommendations
```

---

## Best Practices

### Quando Forzare Architect

```python
# Force architect per task critici
result = classify_task(task, force_architect=True)
```

### Quando Bypassare

```python
# Task semplici vanno diretti
result = classify_task("fix typo in README")
# → SIMPLE, architect=False
```

### Tuning Keywords

Per aggiungere nuove keywords:

```python
# In task_classifier.py
COMPLEXITY_KEYWORDS = {
    "new_keyword": 0.6,  # weight 0.0-1.0
    ...
}
```

---

## Metriche di Successo

| Metrica | Baseline | Target | Actual |
|---------|----------|--------|--------|
| Classification Accuracy | - | ≥85% | 100% |
| Routing Accuracy | - | ≥90% | 100% |
| Task Success Rate | 70% | 85%+ | TBD (production) |

---

## Troubleshooting

### Task COMPLEX classificato SIMPLE

Verifica che le keywords siano presenti nella descrizione:
```bash
python scripts/swarm/task_classifier.py "your task description"
```

### Plan rejected troppo spesso

1. Verifica che il task sia ben definito
2. Considera `force_architect=False` per task borderline
3. Rivedi i criteri di validazione in `architect_flow.py`

---

## Changelog

- **Sessione 283**: Benchmark 100%, fix formula normalizzazione
- **Sessione 282**: Day 5-6, task_classifier + architect_flow
- **Sessione 281**: W3-B design, subroadmap creata

---

*"Fatto BENE > Fatto VELOCE"*
*Cervella & Rafa - Sessione 283*
