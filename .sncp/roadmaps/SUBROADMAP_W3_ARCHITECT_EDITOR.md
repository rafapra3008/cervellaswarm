# SUBROADMAP W3 - Architect/Editor

> **Creata:** 19 Gennaio 2026 - Sessione 281
> **Obiettivo:** Planning + Navigazione Semantica per Worker
> **Standard:** Minimo 9.5/10
> **Ricerca:** `.swarm/tasks/TASK_W3_RESEARCH_OUTPUT.md`

---

## PERCHE W3

```
+================================================================+
|   PROBLEMA ATTUALE:                                            |
|   Worker iniziano subito a codare (no planning)                |
|   Usano grep testuale (no semantic search)                     |
|   Non capiscono impatto modifiche                              |
|   Success rate: ~70%                                           |
|                                                                |
|   SOLUZIONE W3:                                                |
|   Semantic Search API (naviga codebase intelligente)           |
|   Architect Pattern (piano PRIMA di codare)                    |
|   Success rate target: 85%+                                    |
+================================================================+
```

---

## ORDINE (Guardiana Qualita approved)

```
W3-A: Semantic Search (4 giorni)  ← PRIMA (enabler)
W3-B: Architect Pattern (3 giorni) ← USA semantic search
```

**Motivazione:** F#3 wrappa W2 esistente, rischio minore. F#1 usa `estimate_impact()`.

---

## W3-A: SEMANTIC SEARCH (Day 1-4)

### Obiettivo

API per query semantiche su dependency graph esistente.

### Day 1: Core API (semantic_search.py)

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | `find_symbol(name)` - trova definizione | REQ-01 | 1h |
| 2 | `find_callers(symbol)` - chi chiama | REQ-02 | 2h |
| 3 | `find_callees(symbol)` - chi viene chiamato | REQ-03 | 1h |
| 4 | `find_references(symbol)` - tutti gli usi | REQ-04 | 2h |

**File:** `scripts/utils/semantic_search.py`

### Day 2: Impact Analysis (impact_analyzer.py)

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | `estimate_impact(symbol)` - rischio modifica | REQ-05 | 3h |
| 2 | `find_dependencies(file)` - dipendenze file | REQ-06 | 1h |
| 3 | `find_dependents(file)` - chi dipende da file | REQ-07 | 1h |
| 4 | Risk score algorithm | REQ-08 | 1h |

**File:** `scripts/utils/impact_analyzer.py`

### Day 3: Integration + Test

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | Test suite completa (T01-T15) | - | 3h |
| 2 | Performance benchmark | REQ-09 | 1h |
| 3 | CLI interface `swarm-search` | REQ-10 | 2h |

**File:** `tests/utils/test_semantic_search.py`, `scripts/swarm-search`

### Day 4: Docs + Audit

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | Documentazione API | - | 2h |
| 2 | Worker prompt update | REQ-11 | 2h |
| 3 | Audit Guardiana Qualita | - | 2h |

**File:** `docs/SEMANTIC_SEARCH.md`, worker prompts

---

## W3-A TEST SUITE (T01-T15)

| Test | Cosa Verifica | Input | Expected |
|------|---------------|-------|----------|
| T01 | find_symbol base | `"Symbol"` | `symbol_extractor.py:50` |
| T02 | find_symbol not found | `"NonExistent"` | `None` |
| T03 | find_callers single | `"parse_file"` | `["repo_mapper.py:process"]` |
| T04 | find_callers multiple | `"Symbol"` | `>5 callers` |
| T05 | find_callees function | `"build_map"` | lista funzioni chiamate |
| T06 | find_references all | `"DependencyGraph"` | imports + instantiation |
| T07 | estimate_impact low | file isolato | `risk_score < 0.3` |
| T08 | estimate_impact high | file centrale | `risk_score > 0.7` |
| T09 | find_dependencies | `"repo_mapper.py"` | include `symbol_extractor` |
| T10 | find_dependents | `"symbol_extractor.py"` | include `repo_mapper` |
| T11 | Performance small | 100 file repo | `< 100ms` |
| T12 | Performance medium | 1K file repo | `< 500ms` |
| T13 | Performance large | 10K+ file repo | `< 2s` |
| T14 | Cache hit | same query 2x | 2nd `< 10ms` |
| T15 | Graceful error | invalid symbol | `None`, no crash |

---

## W3-A ACCEPTANCE CRITERIA

| # | Criterio | Peso | Threshold |
|---|----------|------|-----------|
| AC1 | Core API funziona | 25% | T01-T06 PASS |
| AC2 | Impact analysis funziona | 25% | T07-T10 PASS |
| AC3 | Performance small repo | 20% | < 100ms |
| AC4 | Performance large repo | 10% | < 2s |
| AC5 | Cache funziona | 10% | T14 PASS |
| AC6 | No regressioni W2 | 10% | All W2 tests PASS |

### Formula Score W3-A

```
Score = (AC1*0.25 + AC2*0.25 + AC3*0.2 + AC4*0.1 + AC5*0.1 + AC6*0.1) * 10
Target: >= 9.5/10
```

---

## W3-B: ARCHITECT PATTERN (Day 5-7)

### Obiettivo

cervella-architect (Opus) genera PLAN.md prima che worker implementino.

### Day 5: Architect Agent

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | Creare `cervella-architect.md` prompt | REQ-12 | 3h |
| 2 | PLAN_TEMPLATE.md struttura | REQ-13 | 1h |
| 3 | Threshold task complesso | REQ-14 | 1h |

**File:** `~/.claude/agents/cervella-architect.md`, `.swarm/templates/PLAN_TEMPLATE.md`

### Day 6: Flow Integration

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | Regina routing (task → architect?) | REQ-15 | 3h |
| 2 | Plan validation logic | REQ-16 | 2h |
| 3 | Fallback se plan rifiutato 2x | REQ-17 | 1h |

**File:** `scripts/swarm/architect_flow.py`

### Day 7: Benchmark + Audit

| # | Task | REQ | Effort |
|---|------|-----|--------|
| 1 | Benchmark 10 task (con/senza architect) | - | 3h |
| 2 | Docs pattern usage | - | 2h |
| 3 | Audit Guardiana Qualita | - | 2h |

**File:** `docs/ARCHITECT_PATTERN.md`, benchmark results

---

## W3-B TEST SUITE (T16-T25)

| Test | Cosa Verifica |
|------|---------------|
| T16 | Architect genera plan valido |
| T17 | Plan contiene: Goal, Files, Steps, Tests |
| T18 | Worker riceve e segue plan |
| T19 | Task semplice bypassa architect |
| T20 | Fallback dopo 2 plan rifiutati |
| T21 | Plan usa estimate_impact() |
| T22 | Benchmark: success rate > 80% |
| T23 | Human readable plan |
| T24 | Plan limit: max 20 steps |
| T25 | Timeout architect: 5 min |

---

## W3-B ACCEPTANCE CRITERIA

| # | Criterio | Peso | Threshold |
|---|----------|------|-----------|
| AC7 | Plan strutturato | 25% | T16-T17 PASS |
| AC8 | Worker seguono plan | 25% | T18 PASS |
| AC9 | Bypass task semplici | 15% | T19 PASS |
| AC10 | Fallback funziona | 10% | T20 PASS |
| AC11 | Success rate | 20% | > 80% (benchmark) |
| AC12 | Timeout rispettato | 5% | T25 PASS |

### Formula Score W3-B

```
Score = (AC7*0.25 + AC8*0.25 + AC9*0.15 + AC10*0.1 + AC11*0.2 + AC12*0.05) * 10
Target: >= 9.5/10
```

---

## FILE DA CREARE/MODIFICARE

### Nuovi File

| File | Scopo |
|------|-------|
| `scripts/utils/semantic_search.py` | Core semantic API |
| `scripts/utils/impact_analyzer.py` | Risk analysis |
| `scripts/swarm-search` | CLI interface |
| `scripts/swarm/architect_flow.py` | Architect orchestration |
| `~/.claude/agents/cervella-architect.md` | Architect prompt |
| `.swarm/templates/PLAN_TEMPLATE.md` | Plan structure |
| `tests/utils/test_semantic_search.py` | Test suite |
| `docs/SEMANTIC_SEARCH.md` | API docs |
| `docs/ARCHITECT_PATTERN.md` | Pattern docs |

### File da Modificare

| File | Modifica |
|------|----------|
| Worker prompts (12 file) | Aggiungere semantic search commands |

---

## DIPENDENZE

```
W3-A dipende da:
├── W2 dependency_graph.py ✅ DONE
├── W2 symbol_extractor.py ✅ DONE
└── W2 reference extraction ✅ DONE

W3-B dipende da:
├── W3-A semantic_search.py
└── W3-A impact_analyzer.py
```

---

## METRICHE SUCCESSO W3

| Metrica | Baseline | Target | Come |
|---------|----------|--------|------|
| Task success rate | 70% | 85%+ | Benchmark 20 task |
| Navigation speed | ~5s (grep) | < 500ms | Timer queries |
| Breaking changes | ~30% | < 10% | Track test failures |
| Plan quality | N/A | 8/10 | Human review |

---

## RISCHI & MITIGAZIONI

| Rischio | Mitigazione |
|---------|-------------|
| Architect loop infinito | Max 3 iter + timeout 5min |
| Semantic search lenta | Cache + async |
| Over-engineering | Ship Core FIRST |
| Opus cost alto | Architect solo task complessi |

---

## STIMA TOTALE

| Componente | Effort |
|------------|--------|
| W3-A Semantic Search | 4 giorni |
| W3-B Architect Pattern | 3 giorni |
| **TOTALE** | **7 giorni** |

---

## DOPO W3

Quando score 9.5/10 raggiunto:
- [ ] Aggiornare NORD.md → W3 100%
- [ ] Considerare Visual Plan (Mermaid) per W4
- [ ] Considerare Auto-Context Refresh per W4

---

*"Non abbiamo fretta. Minimo 9.5 di score!"*
*"Fatto BENE > Fatto VELOCE"*

**Cervella & Rafa - Sessione 281**
