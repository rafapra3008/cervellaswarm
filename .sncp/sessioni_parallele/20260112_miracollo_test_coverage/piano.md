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

- [ ] Test pricing_tracking_service
- [ ] Test confidence_scorer
- [ ] Test action_tracking_api
- [ ] Verifica coverage

---

*Piano creato: 12 Gennaio 2026*
