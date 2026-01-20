<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 302
> **STATO:** 90% LIVE | Health 9.0/10 (PULIZIA CASA 100%!)

---

## SESSIONE 302 - PULIZIA CASA COMPLETATA!

```
+================================================================+
|   SPLIT FILE GIGANTI: 6/6 COMPLETATI! (100%)                   |
|                                                                |
|   [x] test_action_tracking.py: 820 -> 8 file  (S300)          |
|   [x] ml_api.py: 705 -> 7 file               (S300)          |
|   [x] cm_import_service.py: 762 -> 8 file    (S301)          |
|   [x] planning_core.py: 746 -> 5 file        (S301)          |
|   [x] ab_testing_api.py: 768 -> 5 file       (S302)          |
|   [x] city_tax.py: 721 -> 6 file             (S302)          |
|                                                                |
|   TOTALE: 4,522 righe -> 39 file modulari!                    |
+================================================================+
```

**Commit S302:**
- `8842536` - Split ab_testing_api.py (5 file)
- `a9c34da` - Split city_tax.py (6 file)

---

## STRUTTURA NUOVA (S302)

```
routers/ab_testing/             # A/B Testing (5 file)
├── __init__.py, models.py, utils.py
├── metrics.py, endpoints.py

routers/city_tax/               # City Tax (6 file)
├── __init__.py, models.py, config.py
├── calculation.py, collection.py, reports.py
```

---

## MAPPA SPLIT FILE - COMPLETATA!

| # | File | Righe | Split | Sessione |
|---|------|-------|-------|----------|
| 1 | test_action_tracking.py | 820 | 8 file | S300 |
| 2 | ml_api.py | 705 | 7 file | S300 |
| 3 | cm_import_service.py | 762 | 8 file | S301 |
| 4 | planning_core.py | 746 | 5 file | S301 |
| 5 | ab_testing_api.py | 768 | 5 file | S302 |
| 6 | city_tax.py | 721 | 6 file | S302 |

---

## MODULO FINANZIARIO

| Fase | Componente | Stato |
|------|------------|-------|
| 1 | Ricevute PDF | 100% REALE |
| 1B | Checkout UI | 100% REALE |
| 2 | Scontrini RT | 90% - test stampante |
| 3-4 | Fatture/Export | PARCHEGGIATO |

---

## PARCHEGGIATI

| Cosa | Motivo |
|------|--------|
| Subscription system | In `modules/`, pronto |
| Fatture XML | Test SPRING OK |
| Notifiche CM | Modulo futuro |

---

## ARCHITETTURA

```
Internet -> Nginx (443) -> Backend (8001) -> SQLite
VM: miracollo-cervella (Google Cloud)
```

---

*"PULIZIA CASA 100%! Health 9.0/10!" - Sessione 302*
