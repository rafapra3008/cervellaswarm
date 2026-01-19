# AUDIT PMS CORE - 19 Gennaio 2026

**Status**: ⚠️ ISSUES  
**Health**: 6.5/10  
**Top 3**:  
- 48 file >500 righe (CRITICO: planning_core.py 746L, ab_testing_api.py 768L, cm_import_service.py 762L)
- 469 funzioni >50 righe (CRITICO: 47 funzioni >100 righe)
- 18 TODO trovati (alcuni critici: license_check middleware disabilitato)

---

## STRUTTURA CODEBASE

**Totale**: 336 file Python | 88,086 righe codice

### Router Attivi (54 file)
- Core: bookings, planning_core, planning_ops, dashboard
- Revenue: ml_api, autopilot, rateboard, what_if_api, ab_testing_api
- Guest: guest_auth, guest_checkin/*, receipts, payments
- Compliance: fiscal, city_tax, compliance, gdpr
- Integrazioni: cm_reservation, whatsapp, competitor_scraping
- Email: email/automation, email/templates, email/schedules
- Public API: public/booking, public/availability

### Services (44 file)
- Core: night_audit_service, subscription_service, notification_worker
- ML: model_trainer, ml_scheduler, pattern_analyzer
- Scraping: competitor_scraping_service, weather_service
- Email: email_poller, email_scheduler, sender
- Document: document_scanner, document_intelligence/*
- Payment: stripe_service, pagonline/client

### ML/AI (11 file)
- model_trainer.py, ml_scheduler.py, feature_engineering.py
- confidence/scorer.py, confidence/components.py
- data_preparation.py

---

## FILE CRITICI (>500 righe)

### CRITICO (>700 righe)
```
tests/test_action_tracking.py         820L  (SPLIT URGENTE)
ab_testing_api.py                     768L  (SPLIT URGENTE)
cm_import_service.py                  762L  (SPLIT URGENTE)
planning_core.py                      746L  (SPLIT URGENTE)
city_tax.py                           721L  (SPLIT URGENTE)
ml_api.py                             705L  (SPLIT URGENTE)
```

### ALTO (500-700 righe) - 42 file
Includono: fiscal.py, autopilot.py, planning_ops.py, services multipli

**Raccomandazione**: Piano refactoring progressivo.

---

## FUNZIONI GRANDI (>50 righe)

**Totale**: 469 funzioni  
**CRITICO**: 47 funzioni >100 righe

### Top 5 Funzioni Enormi
```
apply_price_suggestion()              318L  services/suggerimenti_actions.py
complete_checkin()                    278L  routers/guest_checkin/complete.py
get_booking_full_details()            268L  routers/booking_detail.py
create_booking()                      259L  routers/public/booking.py
send_scheduled_email()                248L  services/email/scheduler.py
```

**Impatto**: Difficili da testare, debuggare, mantenere.

---

## TODO/FIXME TROVATI

**Totale**: 18 TODO

### Critici
```
middleware/license_check.py:87,96,109  "ATTIVARE BLOCCO" (x3)
services/subscription_service.py:224,272  "ATTIVARE QUANDO RAFA DECIDE!" (x2)
routers/cm_reservation.py:224  "Rimuovere blocco produzione"
```

### Da Completare
```
routers/ml_api.py:447  "Recuperare suggestion_data dal DB"
routers/cm_reservation.py:544  "detect if matched or created"
services/pagonline/client.py:486  "Implementare in FASE successiva"
routers/public/availability.py:174,176  "aggiungere campo/foto" (x2)
```

**Raccomandazione**: Review e decisione su ogni TODO.

---

## DUPLICAZIONI

**Trovate**: 2 file identici
```
compliance/__init__.py = ml/__init__.py
```

**Impatto**: BASSO (probabilmente file vuoti)

---

## ARCHITETTURA

### Organizzazione Modulare (BENE)
```
✅ Router separati per dominio (54 router)
✅ Services layer ben definito (44 services)
✅ ML separato (11 file ML)
✅ Compliance isolato (4 file)
✅ Middleware configurabile (3 file)
```

### Problemi Architetturali

**1. God Files** (file che fanno troppo)
- planning_core.py, cm_import_service.py, ml_api.py
- Suggerimento: Split per responsabilità

**2. Funzioni Monolitiche**
- 47 funzioni >100 righe
- Suggerimento: Extract Method pattern

**3. Coupling Potenziale**
- Services che accedono direttamente al DB
- Suggerimento: Repository pattern per query complesse

---

## METRICHE SALUTE

| Metrica | Valore | Target | Gap |
|---------|--------|--------|-----|
| File >500L | 48 | <10 | -38 |
| Funzioni >100L | 47 | <5 | -42 |
| TODO aperti | 18 | <5 | -13 |
| Duplicazioni | 2 | 0 | -2 |
| Test coverage | N/A | >80% | ? |

**Health Score**: 6.5/10

---

## RACCOMANDAZIONI PRIORITIZZATE

### CRITICO
- [ ] **SPLIT** i 6 file >700 righe (test_action_tracking, ab_testing_api, cm_import_service, planning_core, city_tax, ml_api)
- [ ] **REFACTOR** le 10 funzioni >200 righe (apply_price_suggestion, complete_checkin, etc.)
- [ ] **DECIDERE** sui 3 TODO "ATTIVARE BLOCCO" in license_check

### ALTO
- [ ] **SPLIT** i 42 file 500-700 righe (progressivo)
- [ ] **EXTRACT** le 37 funzioni 100-200 righe
- [ ] **COMPLETARE O RIMUOVERE** i 15 TODO rimanenti

### MEDIO
- [ ] **REFACTOR** le 422 funzioni 50-100 righe (graduale)
- [ ] **PATTERN REPOSITORY** per query DB complesse
- [ ] **UNIFICARE** i 2 file duplicati

### BASSO
- [ ] Aggiungere type hints dove mancano
- [ ] Documentazione docstring per funzioni complesse
- [ ] Code coverage report

---

## EFFORT STIMATO

| Priorità | Task | Effort | Quando |
|----------|------|--------|--------|
| CRITICO | Split 6 file >700L | 2-3 sessioni | Sprint corrente |
| CRITICO | Refactor 10 func >200L | 1-2 sessioni | Sprint corrente |
| ALTO | Split 42 file | 5-8 sessioni | Prossimi 2 sprint |
| ALTO | Extract 37 func | 3-4 sessioni | Prossimi 2 sprint |

**Totale CRITICO+ALTO**: ~12-17 sessioni di lavoro

---

## NEXT STEP

**Proposta Immediata**:
1. cervella-backend: Split planning_core.py (746L) in planning_core/, planning_availability, planning_pricing
2. cervella-backend: Split cm_import_service.py (762L) in cm_import/, cm_guest_mapper, cm_booking_creator
3. cervella-ingegnera: Analisi dipendenze circolari (se presenti)

**Decidere**:
- Priorità refactoring vs nuove feature?
- Allocare sessioni dedicate a tech debt?

---

**Report Completo JSON**: reports/engineer_report_20260119_100530.json

*Cervella Ingegnera - 19 Gennaio 2026*
