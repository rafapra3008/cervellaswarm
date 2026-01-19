# SUBROADMAP: Split File Giganti - Miracollo PMS

> "Fatto BENE > Fatto VELOCE" - Costituzione CervellaSwarm

**Data**: 19 Gennaio 2026 - Sessione 272
**Autore**: Cervella Guardiana Qualita
**Standard**: Max 500 righe per file

---

## EXECUTIVE SUMMARY

| # | File | Righe | Priorita | Sessioni | Rischio |
|---|------|-------|----------|----------|---------|
| 1 | tests/test_action_tracking.py | 820 | BASSA | 1 | Basso |
| 2 | routers/ab_testing_api.py | 768 | MEDIA | 1.5 | Medio |
| 3 | services/cm_import_service.py | 762 | ALTA | 1.5 | Medio |
| 4 | routers/planning_core.py | 746 | ALTA | 2 | Alto |
| 5 | routers/city_tax.py | 721 | MEDIA | 1.5 | Medio |
| 6 | routers/ml_api.py | 705 | MEDIA | 1 | Basso |

**Totale stimato**: 8-9 sessioni

---

## ORDINE CONSIGLIATO DI ESECUZIONE

### Fase 1: File a Basso Rischio (2 sessioni)

**1. test_action_tracking.py** - Iniziare qui
- SOLO test, zero impatto su produzione
- Perfetto per "scaldarsi" con il pattern

**2. ml_api.py** - Router contenuto
- Pochi endpoint, ben isolato
- Dipendenze chiare (ml/ module)

### Fase 2: File Business-Critical (4 sessioni)

**3. cm_import_service.py** - Cuore import CM
- Impatta prenotazioni in arrivo
- Richiede test post-split

**4. planning_core.py** - IL CUORE DEL PMS
- File piu critico del sistema
- Richiede attenzione massima

### Fase 3: File Funzionalita Avanzate (3 sessioni)

**5. ab_testing_api.py** - Feature AB
- Logica complessa ma isolata
- Test esistenti come safety net

**6. city_tax.py** - Modulo fiscale
- Impatto legale/compliance
- Verificare report dopo split

---

## ANALISI DETTAGLIATA PER FILE

### 1. tests/test_action_tracking.py (820 righe)

**Cosa fa:**
- Test suite per action_tracking_api.py
- Test per history, apply, rollback, monitoring, pause/resume
- Fixtures e edge cases

**Come splittare:**

```
tests/
  test_action_tracking/
    __init__.py
    conftest.py              # Fixtures condivise (~125 righe)
    test_history.py          # TestGetActionsHistory (~100 righe)
    test_apply.py            # TestApplyAction (~110 righe)
    test_rollback.py         # TestRollbackAction (~90 righe)
    test_monitoring.py       # TestGetMonitoring (~120 righe)
    test_pause_resume.py     # TestPauseResumeActions (~65 righe)
    test_effectiveness.py    # TestEffectivenessScore (~55 righe)
    test_edge_cases.py       # TestActionTrackingEdgeCases (~100 righe)
```

**Dipendenze da verificare:**
- Nessuna dipendenza esterna
- Verificare che pytest scopra correttamente la nuova struttura

**Rischio:** BASSO - Solo test, zero impatto produzione

**Effort:** 1 sessione

---

### 2. routers/ab_testing_api.py (768 righe)

**Cosa fa:**
- API per A/B testing strategie pricing
- CRUD test, assegnazione, calcolo winner
- Modelli Pydantic + utility functions

**Come splittare:**

```
routers/
  ab_testing/
    __init__.py              # Re-export router
    models.py                # Tutti i Pydantic models (~115 righe)
    endpoints.py             # Endpoints CRUD (~300 righe)
    winner_logic.py          # _calculate_winner_logic + helpers (~150 righe)
    assignment_logic.py      # assign_strategy_logic + _get_aggregated_metrics (~100 righe)
```

**Dipendenze da verificare:**
- `from ..core import get_db, logger`
- Import in `main.py` da aggiornare
- Tabelle: ab_tests, ab_test_results, ab_test_assignments

**Rischio:** MEDIO - Feature usata ma non critica

**Effort:** 1.5 sessioni

---

### 3. services/cm_import_service.py (762 righe)

**Cosa fa:**
- Import prenotazioni da Channel Manager
- Guest matching/creation
- Booking generation
- Room assignment automatico

**Come splittare:**

```
services/
  cm_import/
    __init__.py              # Re-export funzioni pubbliche
    guest_service.py         # extract_*, normalize_*, find_or_create_guest (~215 righe)
    booking_service.py       # generate_booking_number, create_booking_from_cm (~180 righe)
    room_service.py          # create_booking_room, get_available_rooms (~170 righe)
    auto_import.py           # auto_import_reservation, mark_cm_reservation_imported (~200 righe)
```

**Dipendenze da verificare:**
- `from ..core import get_db, logger`
- Usato da: `routers/cm_reservation.py`
- Tabelle: guests, bookings, booking_rooms, cm_reservations, rooms, channels

**Rischio:** MEDIO - Impatta import CM, testare con BeSync

**Effort:** 1.5 sessioni

---

### 4. routers/planning_core.py (746 righe) - CRITICO

**Cosa fa:**
- IL CUORE DEL SISTEMA
- Vista planning (camere, prenotazioni, blocchi)
- Quick booking, resize, cambio camera
- Validazione disponibilita

**Come splittare:**

```
routers/
  planning/                  # Directory GIA ESISTENTE!
    __init__.py              # Aggiungere re-export
    core.py                  # get_planning, get_rooms, get_available_rooms (~230 righe)
    booking_create.py        # create_quick_booking + helpers (~200 righe)
    booking_dates.py         # update_booking_dates (~140 righe)
    utils.py                 # _find_or_create_guest, _calculate_smart_pricing, _validate_room_availability (~180 righe)
```

**Nota:** Directory `routers/planning/` gia esiste con swap, segment_swap, room_change, assignments, history. Integrarsi!

**Dipendenze da verificare:**
- MOLTISSIME: core, models, services/booking_utils
- Import in `main.py`
- Usato da: Frontend Planning, API prenotazioni
- Tabelle: hotels, rooms, room_types, bookings, booking_rooms, guests, channels, room_blocks, room_assignments

**Rischio:** ALTO - Rompere questo = rompere tutto

**Effort:** 2 sessioni (con test estensivi)

---

### 5. routers/city_tax.py (721 righe)

**Cosa fa:**
- Gestione imposta di soggiorno
- Configurazione, esenzioni, calcolo
- Riscossione e report

**Come splittare:**

```
routers/
  city_tax/
    __init__.py              # Re-export router
    models.py                # Pydantic models (~60 righe)
    config.py                # Endpoints config + admin alias (~175 righe)
    exemptions.py            # Endpoints esenzioni (~100 righe)
    calculation.py           # calculate, apply, get_charges (~200 righe)
    collection.py            # collect, exempt (~60 righe)
    reports.py               # summary, export, pending (~180 righe)
```

**Dipendenze da verificare:**
- `from ..core.database import DB_PATH, get_db`
- Tabelle: hotels, bookings, guests, city_tax_exemptions, city_tax_charges, booking_guests

**Rischio:** MEDIO - Impatto fiscale, verificare report

**Effort:** 1.5 sessioni

---

### 6. routers/ml_api.py (705 righe)

**Cosa fa:**
- API per ML model management
- Model info, training stats, retrain
- Confidence scoring, what-if simulation

**Come splittare:**

```
routers/
  ml/
    __init__.py              # Re-export router
    models.py                # Pydantic models (~120 righe)
    info_endpoints.py        # model-info, training-stats, scheduler-status (~150 righe)
    training_endpoints.py    # retrain (~80 righe)
    confidence_endpoints.py  # confidence, confidence-breakdown (~120 righe)
    whatif_endpoints.py      # what-if simulation (~180 righe)
    utils.py                 # _get_confidence_level + helpers (~50 righe)
```

**Dipendenze da verificare:**
- `from ..core import get_db, logger`
- `from ..ml.*` (model_trainer, confidence_scorer, ml_scheduler, data_preparation)

**Rischio:** BASSO - Feature ML isolata

**Effort:** 1 sessione

---

## STRUTTURA TARGET POST-SPLIT

```
backend/
  routers/
    ab_testing/              # NUOVO
      __init__.py
      models.py
      endpoints.py
      winner_logic.py
      assignment_logic.py

    city_tax/                # NUOVO
      __init__.py
      models.py
      config.py
      exemptions.py
      calculation.py
      collection.py
      reports.py

    ml/                      # NUOVO
      __init__.py
      models.py
      info_endpoints.py
      training_endpoints.py
      confidence_endpoints.py
      whatif_endpoints.py
      utils.py

    planning/                # ESISTENTE - ESPANDERE
      __init__.py            # Aggiornare
      core.py                # NUOVO
      booking_create.py      # NUOVO
      booking_dates.py       # NUOVO
      utils.py               # NUOVO
      swap.py                # Esistente
      segment_swap.py        # Esistente
      room_change.py         # Esistente
      assignments.py         # Esistente
      history.py             # Esistente

  services/
    cm_import/               # NUOVO
      __init__.py
      guest_service.py
      booking_service.py
      room_service.py
      auto_import.py

  tests/
    test_action_tracking/    # NUOVO
      __init__.py
      conftest.py
      test_history.py
      test_apply.py
      test_rollback.py
      test_monitoring.py
      test_pause_resume.py
      test_effectiveness.py
      test_edge_cases.py
```

---

## CHECKLIST PRE-SPLIT

Per OGNI file:

```
[ ] Backup file originale
[ ] Identificare TUTTE le dipendenze (grep import)
[ ] Creare directory se non esiste
[ ] Spostare models/types PRIMA
[ ] Spostare utils/helpers DOPO models
[ ] Spostare endpoints/logic ULTIMO
[ ] Aggiornare __init__.py con re-export
[ ] Aggiornare main.py import
[ ] Run test suite COMPLETA
[ ] Verificare endpoint risponde
[ ] Commit atomico per file
```

---

## CHECKLIST POST-SPLIT

```
[ ] Tutti i test passano
[ ] API risponde correttamente
[ ] Import non rotti (python -c "from backend.routers import ...")
[ ] Nessun file > 500 righe
[ ] Log funziona
[ ] Coverage non diminuita
```

---

## TIMELINE CONSIGLIATA

| Settimana | File | Note |
|-----------|------|------|
| 1 | test_action_tracking.py | Warm-up, zero rischio |
| 1 | ml_api.py | Completare warm-up |
| 2 | cm_import_service.py | Test con BeSync dopo |
| 2-3 | planning_core.py | IL PIU CRITICO - con calma! |
| 3 | ab_testing_api.py | Feature isolata |
| 3 | city_tax.py | Ultimo, verificare report |

---

## NOTE FINALI

> "Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"

- **Mai fretta**: Meglio 2 settimane fatto bene che 3 giorni con bug
- **Un file alla volta**: Commit atomici, rollback facile
- **Test sempre**: Prima, durante e dopo ogni split
- **Planning Core con rispetto**: E il cuore del sistema

---

*Creato da Cervella Guardiana Qualita - Sessione 272*
*"Qualita non e optional. E la BASELINE."*
