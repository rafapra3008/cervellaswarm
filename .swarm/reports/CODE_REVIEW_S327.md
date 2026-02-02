# CODE REVIEW REPORT - Sessione 327

**Data:** 2 Febbraio 2026
**Reviewer:** Cervella Reviewer
**Scope:** CervellaSwarm codebase completo

---

## Executive Summary

**Overall Health:** 7.5/10
**Critical Issues:** 2
**High Priority:** 5
**Medium Priority:** 8
**Low Priority:** 12

**Verdetto Generale:** Il codebase è in buone condizioni con architettura solida e pattern coerenti. Ci sono 2 issue critici di sicurezza/performance da fixare immediatamente.

---

## Findings by Priority

### CRITICAL (fix immediately)

#### C1. Security: No Input Sanitization in smart-search.py
**File:** `scripts/sncp/smart-search.py:254`

```python
directory = sys.argv[2]  # NO VALIDATION!
```

**Issue:** Path traversal vulnerability. Directory passata senza sanitizzazione.

**Fix Required:**
```python
directory = os.path.abspath(directory)
if not directory.startswith(os.getcwd()):
    print("ERROR: Directory must be within current working directory", file=sys.stderr)
    sys.exit(1)
```

---

#### C2. Performance: N+1 Query Pattern in log_event.py
**File:** `scripts/memory/log_event.py:206-222`

**Issue:** Ogni evento = 1 INSERT + 1 COMMIT. Con 14 agent attivi = centinaia di write/secondo.

**Fix Required:** Implementare batch buffering con flush ogni 50 eventi o 5 secondi.

---

### HIGH (fix soon)

#### H1. Silent Failures in semantic_search.py
**File:** `scripts/utils/semantic_search.py:191-193`
Errori loggati come WARNING ma non tracciati.

#### H2. Race Condition in mark_working()
**File:** `scripts/swarm/task_manager.py:257-265`
Write timestamp non atomica.

#### H3. Memory Leak: SymbolExtractor Cache
Cache cresce indefinitamente, serve LRU.

#### H4. Missing Retry Jitter
**File:** `packages/core/src/client/retry.ts:130`
Thundering herd quando tutti agent vanno in retry insieme.

#### H5. Missing API Key Validation
Nessuna validazione formato key prima delle chiamate.

---

### MEDIUM (improve when possible)

| ID | Issue | File |
|----|-------|------|
| M1 | Code duplication DB connection | Multiple |
| M2 | Inconsistent error response format | Multiple |
| M3 | Magic numbers without constants | smart-search.py:224 |
| M4 | Missing docstrings TypeScript | retry.ts |
| M5 | Task validation too strict | task_manager.py |
| M6 | Inconsistent logging levels | Multiple |
| M7 | Missing version header consistency | db.py |
| M8 | Test coverage gaps | smart-search.py, task_manager race |

---

### LOW (nice to have)

- L1: Print statements instead of logging (919 occurrenze)
- L2: Missing type hints in Python
- L3: Hardcoded paths
- L4: No progress indication
- L5-L12: Vari miglioramenti minori

---

## Files Reviewed

| File | Status | Score |
|------|--------|-------|
| `scripts/sncp/smart-search.py` | NEEDS FIX | 6/10 |
| `scripts/memory/log_event.py` | BLOCKER | 5/10 |
| `scripts/swarm/task_manager.py` | NEEDS FIX | 7/10 |
| `scripts/utils/semantic_search.py` | GOOD | 8/10 |
| `scripts/common/db.py` | GOOD | 8/10 |
| `packages/core/src/client/retry.ts` | GOOD | 8/10 |
| `packages/core/src/client/errors.ts` | EXCELLENT | 9/10 |

---

## Positives

1. Architettura Modulare
2. Error Handling Robusto
3. Versioning Disciplinato
4. Documentation completa
5. Type Safety
6. Retry Logic intelligente
7. Centralized Config

---

## Recommendations

### Immediate (questa sessione)
1. FIX C1 - Sanitize directory input
2. FIX C2 - Batch buffering

### Short-term (entro S330)
3. FIX H1-H5
4. Test coverage per smart-search.py

### Long-term (Q1 2026)
5. Migrare print() a logging
6. Standardizzare response format

---

## Technical Debt

**Totale:** ~8 giorni di lavoro

| Categoria | Priorità |
|-----------|----------|
| Security (C1, H5) | ALTA |
| Performance (C2, H3) | ALTA |
| Reliability (H2, H1) | ALTA |
| Code Quality | MEDIA |
| Documentation | BASSA |

---

**Verdict:** APPROVE con modifiche richieste (C1, C2).

**Reviewer:** Cervella Reviewer
**Next Review:** Lunedì 9 Febbraio 2026
