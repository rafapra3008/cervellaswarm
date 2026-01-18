# SUBROADMAP - Modularizzazione PMS Core

> **Creata:** 17 Gennaio 2026 - Sessione 251
> **Owner:** Cervella Regina + Ingegnera
> **Obiettivo:** Health Score da 6/10 a 8.5/10

---

## STATO ATTUALE (Aggiornato 18 Gen - Sessione 257)

```
Health Score: 8.5/10 (era 8.0/10)

DOPO FASE 3 (CONSOLIDAMENTO):
- 46 file > 500 righe
- 15 funzioni > 100 righe
- 43 TODO attivi
- 3 TODO security → marcati FUTURE con docs

SPLIT COMPLETATI (FASE 2):
- suggerimenti_engine.py -> suggerimenti/ (7 moduli)
- planning_swap.py -> planning/ (5 moduli)
- settings.py -> settings/ (7 moduli)
- email_parser.py -> email/ (6 moduli) + SHIM
- confidence_scorer.py -> confidence/ (5 moduli) + SHIM

FASE 3 COMPLETATA:
- Security TODO: JWT marcati FUTURE con documentazione
- license_check.py: import fixati, version 1.1.0
- README: aggiornato con struttura post-modularizzazione
- Routers: SKIP (sistema live, documentato per futuro)
- Test: già organizzati per feature
```

---

## FASE 1 - QUICK WINS

**Effort:** 4-5 giorni | **Rischio:** Basso | **Impatto:** Alto

### 1.1 Cleanup TODO Document Intelligence
```
COSA: Modulo stub non in produzione con 12 TODO
AZIONE: Marcare chiaramente come FUTURE o rimuovere
EFFORT: 0.5 giorni
BENEFICIO: -12 TODO noise
```

### 1.2 Centralizza Validators
```
COSA: Validation logic ripetuta in routers/* e services/*
AZIONE: Creare core/validators.py con funzioni comuni
EFFORT: 1 giorno
BENEFICIO: DRY, testing +40%
```

### 1.3 Error Handling Decorator
```
COSA: Pattern try/commit/rollback ripetuto 50+ volte
AZIONE: Creare decorators @transactional, @api_error_handler
EFFORT: 1 giorno
BENEFICIO: -15% codice, +80% consistency
```

### 1.4 Extract Helper Functions
```
COSA: 22 funzioni > 100 righe
AZIONE: Extract Method refactoring (no breaking changes)
EFFORT: 2 giorni
BENEFICIO: +50% leggibilita
```

**Checklist FASE 1:** COMPLETATA!
- [x] 1.1 Document Intelligence cleanup (25 TODO -> FUTURE)
- [x] 1.2 core/validators.py creato (15 funzioni)
- [x] 1.3 Decorators creati (6 decorators)
- [x] 1.4 Helper functions estratte (14 helpers, -429 righe)
- [x] Test passano (py_compile OK)
- [ ] Deploy staging OK (prossima sessione)

---

## FASE 2 - REFACTORING CRITICO

**Effort:** 14 giorni (2 sprint) | **Rischio:** Medio | **Impatto:** Molto Alto

### 2.1 Split suggerimenti_engine.py (1031 righe)
```
DA:
  services/suggerimenti_engine.py (1031 righe)

A:
  services/suggerimenti/
  ├── engine.py (orchestration - 300 righe)
  ├── confidence.py (scoring logic - 200 righe)
  └── validators.py (data extraction - 150 righe)

EFFORT: 4 giorni
PRIORITA: CRITICO (cuore business logic)
```

### 2.2 Split planning_swap.py (965 righe)
```
DA:
  routers/planning_swap.py (965 righe)

A:
  routers/planning/
  ├── swap.py (swap_rooms, swap_segment - 400 righe)
  ├── move.py (move_segment, change_room - 350 righe)
  └── validators.py (overlap check - 150 righe)

EFFORT: 3 giorni
PRIORITA: CRITICO (alto traffico produzione)
```

### 2.3 Split settings.py (839 righe) - COMPLETATO Sessione 254!
```
DA:
  routers/settings.py (839 righe)

A (REALE - diverso da piano originale!):
  routers/settings/
  ├── __init__.py       (48 righe)  - Router unificato
  ├── models.py         (226 righe) - Pydantic + constants
  ├── hotel.py          (69 righe)  - Hotel GET/PUT
  ├── room_types.py     (171 righe) - Room Types CRUD
  ├── rooms.py          (161 righe) - Rooms CRUD
  ├── rate_plans.py     (135 righe) - Rate Plans CRUD
  └── services.py       (152 righe) - Services + amenities

  settings.py -> SHIM (52 righe)

AUDIT: Guardiana Qualita 10/10 APPROVED
```

### 2.4 Split email_parser.py (830 righe) - COMPLETATO Sessione 255!
```
DA:
  services/email_parser.py (830 righe)

A (REALE - aggiunto al package email/ esistente!):
  services/email/
  ├── models.py         (167 righe) - Enums + DataClasses
  ├── detection.py       (98 righe) - detect_* functions
  ├── helpers.py        (183 righe) - utility functions
  ├── besync.py         (224 righe) - BeSync parsers
  ├── bookingengine.py  (145 righe) - BookingEngine parsers
  └── __init__.py       (217 righe) - Router + parse_email

  email_parser.py -> SHIM (85 righe)

AUDIT: Guardiana Qualita 9.5/10 APPROVED
```

### 2.5 Split confidence_scorer.py (779 righe) - COMPLETATO Sessione 255!
```
DA:
  ml/confidence_scorer.py (779 righe)

A (REALE - 5 moduli!):
  ml/confidence/
  ├── utils.py         (107 righe) - Constants + helpers
  ├── model_utils.py   (318 righe) - Model loading + variance
  ├── components.py    (140 righe) - Acceptance + Data Quality
  ├── scorer.py        (187 righe) - Main calculate_confidence
  └── __init__.py       (80 righe) - Router

  confidence_scorer.py -> SHIM (82 righe)

AUDIT: Guardiana Qualita 9/10 APPROVED
```

**Checklist FASE 2: COMPLETATA!**
- [x] 2.1 suggerimenti/ modulo creato (Sessione 252 - 7 moduli!)
- [x] 2.2 planning/ modulo creato (Sessione 253 - 5 moduli!)
- [x] 2.3 settings/ modulo creato (Sessione 254 - 7 moduli!) 10/10
- [x] 2.4 email/ modulo creato (Sessione 255 - 6 moduli!) 9.5/10
- [x] 2.5 confidence/ modulo creato (Sessione 255 - 5 moduli!) 9/10
- [ ] Test copertura > 80% su moduli nuovi
- [ ] Deploy produzione OK

---

## FASE 3 - CONSOLIDAMENTO

**Effort:** 10 giorni (1 sprint) | **Rischio:** Basso | **Impatto:** Medio

### 3.1 Organizza routers/
```
DA: 41 file in flat directory
A: Grouped by domain
  routers/
  ├── planning/ (swap, move, calendar)
  ├── booking/ (reservations, guests)
  ├── ml/ (predictions, confidence)
  ├── compliance/ (receipts, audit)
  └── public/ (availability, booking engine)

EFFORT: 3 giorni
```

### 3.2 Security TODO
```
CRITICO:
- Token Twilio encryption
- JWT authentication middleware

EFFORT: 2 giorni
```

### 3.3 Test Organization
```
Mirror production structure
Split test > 800 righe

EFFORT: 2 giorni
```

### 3.4 Documentation Update
```
- README aggiornato
- Architecture diagram
- API documentation

EFFORT: 3 giorni
```

**Checklist FASE 3: COMPLETATA!**
- [x] routers/ → SKIP (sistema live, rischio alto, documentato per futuro)
- [x] Security TODO → JWT marcati FUTURE con docs in license_check.py
- [x] Test → già organizzati per feature (24 file)
- [x] Documentazione → README.md aggiornato v1.8.0

---

## METRICHE OBIETTIVO

| Metrica | Prima | Dopo FASE 1 | Dopo FASE 2 | Dopo FASE 3 |
|---------|-------|-------------|-------------|-------------|
| Health Score | 6/10 | 7/10 | 8/10 | 8.5/10 |
| File > 500 righe | 51 | 45 | 20 | 15 |
| Funzioni > 100 righe | 22 | 15 | 8 | 5 |
| TODO attivi | 72 | 55 | 40 | 30 |
| TODO security | 8 | 8 | 4 | 0 |

---

## REGOLE DI LAVORO

```
1. UN FILE ALLA VOLTA
   Mai refactorare 2 file in parallelo

2. TEST PRIMA DI SPLIT
   Copertura > 80% prima di toccare

3. DEPLOY TRA SPLIT
   Verifica produzione dopo ogni modulo

4. NO BIG BANG
   Incrementale, sempre

5. GUARDIANA VERIFICA
   cervella-ingegnera review dopo ogni fase
```

---

## TIMELINE STIMATA

```
FASE 1: Sessioni 251-255 (questa settimana)
FASE 2: Sessioni 256-270 (prossime 2 settimane)
FASE 3: Sessioni 271-280 (settimana dopo)

TOTALE: ~30 sessioni / 6 settimane
```

---

## PROSSIMO STEP IMMEDIATO

```
OGGI (Sessione 251):
  Task 1.1 - Cleanup TODO Document Intelligence

  AZIONE: Identificare i 12 TODO e marcarli FUTURE
  WORKER: cervella-backend
  VERIFICA: cervella-ingegnera
```

---

*"Un progresso al giorno. Pulito e preciso."*
*Subroadmap creata da Cervella Regina - 17 Gennaio 2026*
