# SUBROADMAP - Modularizzazione PMS Core

> **Creata:** 17 Gennaio 2026 - Sessione 251
> **Owner:** Cervella Regina + Ingegnera
> **Obiettivo:** Health Score da 6/10 a 8.5/10

---

## STATO ATTUALE

```
Health Score: 6/10

PROBLEMI:
- 51 file > 500 righe (soglia: 10)
- 22 funzioni > 100 righe (soglia: 5)
- 72 TODO attivi (soglia: 30)
- 8 TODO security critici
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

**Checklist FASE 1:**
- [ ] 1.1 Document Intelligence cleanup
- [ ] 1.2 core/validators.py creato
- [ ] 1.3 Decorators creati
- [ ] 1.4 Helper functions estratte
- [ ] Test passano
- [ ] Deploy staging OK

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

### 2.3 Split settings.py (838 righe)
```
DA:
  routers/settings.py (838 righe)

A:
  routers/settings/
  ├── hotel.py (hotel config - 300 righe)
  ├── user.py (user preferences - 250 righe)
  └── system.py (system config - 200 righe)

EFFORT: 2 giorni
PRIORITA: ALTO
```

### 2.4 Split email_parser.py (829 righe)
```
DA:
  services/email_parser.py (829 righe)

A:
  services/email/
  ├── parser.py (orchestration - 200 righe)
  ├── extractors.py (date, guest, price - 350 righe)
  └── patterns.py (regex constants - 100 righe)

EFFORT: 2 giorni
PRIORITA: ALTO
```

### 2.5 Split confidence_scorer.py (778 righe)
```
DA:
  ml/confidence_scorer.py (778 righe)

A:
  ml/confidence/
  ├── scorer.py (main scoring - 300 righe)
  ├── validators.py (threshold check - 200 righe)
  └── utils.py (stats helpers - 150 righe)

EFFORT: 3 giorni
PRIORITA: ALTO
```

**Checklist FASE 2:**
- [ ] 2.1 suggerimenti/ modulo creato
- [ ] 2.2 planning/ modulo creato
- [ ] 2.3 settings/ modulo creato
- [ ] 2.4 email/ modulo creato
- [ ] 2.5 confidence/ modulo creato
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

**Checklist FASE 3:**
- [ ] routers/ organizzati
- [ ] Security TODO risolti
- [ ] Test organizzati
- [ ] Documentazione aggiornata

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
