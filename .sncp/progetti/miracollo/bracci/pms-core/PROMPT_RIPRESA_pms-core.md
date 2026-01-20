<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 301
> **STATO:** 90% LIVE | Health 7.2/10 (SPLIT FILE 67%!)

---

## SESSIONE 301 - DUE FILE SPLITTATI!

```
+================================================================+
|   SPLIT FILE GIGANTI: 4/6 COMPLETATI! (67%)                     |
|                                                                |
|   [x] test_action_tracking.py: 820 → 8 file                    |
|   [x] ml_api.py: 705 → 7 file                                  |
|   [x] cm_import_service.py: 762 → 8 file (services/cm/)        |
|   [x] planning_core.py: 746 → 5 file (routers/planning/)       |
|   [ ] ab_testing_api.py: 768 (PROSSIMO)                        |
|   [ ] city_tax.py: 721                                         |
+================================================================+
```

**Commit S301:**
- `a6acb84` - Split cm_import_service.py
- `fe31ec5` - Split planning_core.py

---

## STRUTTURA NUOVA (S301)

```
services/cm/                    # CM Import (8 file)
├── __init__.py, guest_management.py, booking_management.py
├── booking_room.py, availability.py, import_tracking.py
└── auto_import.py

routers/planning/               # Planning Core (5 file nuovi)
├── utils.py, core.py, booking_create.py, booking_dates.py
└── (+ swap.py, segment_swap.py, room_change.py, etc.)
```

---

## MAPPA SPLIT FILE

**SUBROADMAP:** `.sncp/progetti/miracollo/roadmaps/SUBROADMAP_SPLIT_FILE_GIGANTI.md`

| # | File | Stato |
|---|------|-------|
| 1 | test_action_tracking.py | DONE S300 |
| 2 | ml_api.py | DONE S300 |
| 3 | cm_import_service.py | DONE S301 |
| 4 | planning_core.py | DONE S301 |
| 5 | ab_testing_api.py | PROSSIMO |
| 6 | city_tax.py | TODO |

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

*"Pulizia casa 67%! Due file splittati oggi!" - Sessione 301*
