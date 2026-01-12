# Code Review What-If Simulator - Sessione 173
> Data: 12 Gennaio 2026
> Reviewer: cervella-reviewer
> Verdetto: REQUEST CHANGES

---

## Score Attuale vs Target

```
ATTUALE:  7.0/10  ██████████████░░░░░░
TARGET:   9.5/10  ███████████████████░
GAP:      2.5 punti
```

---

## Breakdown Score per Area

| Area | Score | Note |
|------|-------|------|
| Architettura | 8.0/10 | Pattern OK, manca service layer dedicato |
| Code Quality | 7.5/10 | Buono ma funzioni troppo lunghe |
| Test Coverage | 3.0/10 | **CRITICO** - quasi zero test! |
| Security | 8.0/10 | Buono, manca rate limiting |
| Performance | 7.0/10 | OK, può ottimizzare batch predict |

---

## Top Issues (Ordinati per Priorità)

### P0 - BLOCKER: Test Coverage

**Problema**: ZERO test per What-If
- Nessun test per endpoint `/api/ml/what-if`
- Nessun test per `predict_scenario()`
- Nessun integration test E2E

**Fix Richiesto**:
- [ ] Creare `test_ml_api.py`
- [ ] Creare `test_model_trainer.py`
- [ ] Creare `test_what_if_integration.py`

**Effort**: L (8-10h)

---

### P1 - MAJOR: Architettura Service Layer

**Problema**: Logica business in `model_trainer.py` invece di service dedicato
- `predict_scenario()` fa troppo (validation + merge + predict + error handling)
- Non segue pattern Router -> Service -> DB

**Fix Richiesto**:
- [ ] Creare `services/what_if_service.py`
- [ ] Separare logica in metodi atomici
- [ ] Router chiama service, service chiama model

**Effort**: M (4-6h)

---

### P1 - MAJOR: Frontend Code Quality

**Problema**: Funzioni troppo lunghe e codice hardcoded
- `toggleWhatIfPanel()` = 144 righe (max consigliato: 50)
- `hotel_id=1` hardcoded
- CSS inline invece di classi

**Fix Richiesto**:
- [ ] Split `toggleWhatIfPanel()` in funzioni più piccole
- [ ] Config `hotel_id` da settings o URL
- [ ] CSS refactor in what-if.css dedicato

**Effort**: M (5-7h)

---

## File Analizzati

### Backend
- `routers/ml_api.py` - Endpoint What-If
- `services/model_trainer.py` - Logica predict
- `main.py` - Router registration

### Frontend
- `revenue.html` - What-If Panel integrato
- `js/revenue_intelligence.js` - `toggleWhatIfPanel()`

---

## Piano per 9.5/10

| Priorità | Task | Effort | Impatto |
|----------|------|--------|---------|
| P0 | Test Suite ML | L (8-10h) | +2.0 punti |
| P1 | Service Layer | M (4-6h) | +0.5 punti |
| P1 | Frontend Refactor | M (5-7h) | +0.3 punti |
| P2 | Rate Limiting | S (2h) | +0.2 punti |

**Totale**: 17-23h lavoro

---

## Raccomandazione

**Approccio consigliato**:
1. **FASE 3 What-If** (Grafico) - Nuova feature con qualità alta
2. **Test Suite** - Scrivi test MENTRE implementi FASE 3
3. **Refactor** - Migliora architettura durante implementazione

In questo modo alzi qualità + aggiungi feature nello stesso tempo!

---

## Note Positive

- Pattern architetturale base è solido
- ML integration funziona
- Frontend UX è buona
- Endpoint risponde correttamente
- No security issues critici

---

*"Una cosa alla volta, fatta BENE!"*
*"Score 9.5/10 MINIMO SEMPRE"*
