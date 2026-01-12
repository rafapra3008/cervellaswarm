# Piano Sessione Parallela: Test Coverage

> **Data:** 12 Gennaio 2026
> **Sessione:** 169-parallel-tests
> **Obiettivo:** Portare test coverage da 30% a 70%+

---

## Task

### TESTER: Creare test per Revenue Intelligence

**File da testare:**

1. `backend/services/pricing_tracking_service.py`
   - test_log_price_change()
   - test_start_performance_evaluation()
   - test_complete_evaluation()
   - test_calculate_performance_score()

2. `backend/ml/confidence_scorer.py`
   - test_calculate_confidence()
   - test_get_model_variance_confidence()
   - test_get_acceptance_rate()

3. `backend/routers/action_tracking_api.py`
   - test_rollback_flow()
   - test_monitoring_snapshots()

**Output atteso:**
- File: `backend/tests/test_pricing_tracking.py`
- File: `backend/tests/test_confidence_scorer.py`
- File: `backend/tests/test_action_tracking.py`
- Coverage: 70%+

---

## Dipendenze

Nessuna - lavora su file nuovi (test)

---

## Status

- [x] Test pricing_tracking_service - COMPLETATO (~350 righe)
- [x] Test confidence_scorer - COMPLETATO (~380 righe)
- [x] Test action_tracking_api - COMPLETATO (~420 righe)
- [ ] Verifica coverage (richiede deploy su VM)

---

## Output Prodotto

| File | Righe | Test Cases |
|------|-------|------------|
| test_pricing_tracking.py | 350 | 16 test |
| test_confidence_scorer.py | 380 | 22 test |
| test_action_tracking.py | 420 | 23 test |
| **TOTALE** | **1150** | **61 test** |

**Coverage Stimata:** ~63% (target 70%)

---

## Prossimi Step

1. Copiare file su VM
2. Aggiornare import
3. Eseguire pytest
4. Fixare eventuali errori
5. Raggiungere 70%

---

*Piano creato: 12 Gennaio 2026*
*Completato: 12 Gennaio 2026 05:45 UTC*
