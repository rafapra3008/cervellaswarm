<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 13 Marzo 2026 - Sessione 26 (checkpoint finale)
> **Status:** miracollo.com LIVE | Security ~9.1/10 | **2878 test** (0 fail) | Sprint 1-9a
> **Prossima Cervella:** Leggi questo + NORD.md + TODO_MAESTRO.md

---

## COSA E STATO FATTO (S26 - 13 Marzo 2026)

### Sprint 9a: +362 test + 12 bug fix + 100% router coverage
- **+362 test** per 7 router/aree (copertura 100% - TUTTI i router hanno test!)
  - test_what_if_api.py (73), test_ml_endpoints.py (67), test_competitor_scraping.py (54)
  - test_learning_feedback.py (58), test_revenue_research.py (47)
  - test_ollama_api.py (39), test_pages.py (24)
- **12 BUG REALI** scoperti e fixati (tutti crash runtime):
  1. what_if_api: SQLAlchemy text() su raw SQLite
  2. what_if_api: SELECT rate -> price (colonna inesistente)
  3. what_if_api: property_id -> hotel_id + competitor_prices JOIN
  4. what_if_api: Depends(get_db) TypeError
  5. learning_feedback: SELECT nome -> name
  6. learning_service: WHERE suggestion_id -> WHERE id (PK errata)
  7. competitor_scraping: FROM rateboard_prices -> daily_rates
  8-9. local_events: Body=None AttributeError crash (2 endpoint)
  10. local_event model: date senza pattern validation
  11. main.py: router count stale (41 vs 60)
  12. whatsapp.py: aiosqlite senza PRAGMA foreign_keys (8 punti)
- **Security: SQL whitelist** su guests.py e agencies.py (PATCH endpoints)
- **Guardiana Sprint 9a:** 9.4/10, 0 P1/P2

### Code Review Friday: Score 7.8/10 -> tutti P1/P2 fixati
### Deep Bug Hunt: Ingegnera 8.2/10 + Security 9.1/10
### datetime.now() naive: ~28 file convertiti a timezone.utc (in corso)

### Booking Engine Redesign: FONDAMENTA PRONTE
- **3 report di ricerca** completati:
  - Researcher: best practices + dati (68% drop-off a date picker!)
  - Marketing: UX specs 3-step con wireframe + copy IT/EN/DE
  - Analisi tecnica: widget GIA 3 step, serve upgrade visivo
- **Backend pronto:**
  - Migration 057: photo_url + photos_json su room_types
  - GET /api/public/v1/calendar-prices (prezzo minimo/giorno + disponibilita)
  - API availability/rooms aggiornate con foto (backward-compatible)
- **Report salvati in:** `CervellaSwarm/.sncp/progetti/miracollo/ricerche/` e `handoff/`

---

## DA FARE (prossima sessione)

```
PRIORITA 1 - BOOKING ENGINE REDESIGN (ricerca FATTA, backend PRONTO):
  Sprint A (4-5 ore): Quick wins frontend
    -> Extras spostati da Step 3 a Step 2 (+25% revenue!)
    -> Trust badge "0% commissioni" prominente
    -> City tax visibile da Step 2
    -> Urgency badge basato su dati reali
    -> CTA sticky su mobile
  Sprint B (3-5 giorni): Core redesign
    -> Calendario custom con prezzi (hotel-datepicker lib)
    -> Galleria foto camere (swipe mobile)
    -> Split layout desktop (form sx, riepilogo sticky dx)
    -> Inline validation (via alert())
    -> WCAG 2.1 AA base
  Sprint C (5-7 giorni): Game changer
    -> Stripe Elements embedded (NO redirect = +15-20% conversioni!)
    -> Apple Pay + Google Pay (1 config Stripe)
  Sprint D: Differenziatori
    -> Rate comparison vs OTA
    -> Cart abandonment email recovery

PRIORITA 2 - QUALITA:
  -> datetime.now() naive fix (28 file, agente in corso S26)
  -> Security P2 residui (str(e) residui, auth consistency)
  -> f-string logger batch fix (859 occorrenze in 134 file - P3)

BLOCCATI (serve Rafa):
  -> Stripe LIVE keys (onboarding Stripe Dashboard)
  -> WhatsApp Meta template approval
  -> Foto camere NL (serve upload foto reali!)
  -> P2-INFRA-1: backup offsite (VM scope upgrade)

FUTURO:
  -> SDI fattura elettronica
  -> Ericsoft discovery camere/tariffe + write test
  -> Multi-tenant guard (prep FASE 1)
```

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| **NORD.md** | ROOT progetto |
| **TODO MAESTRO** | `CervellaSwarm/.sncp/progetti/miracollo/TODO_MAESTRO.md` |
| **IDEAS BIBLE** | `CervellaSwarm/.sncp/progetti/miracollo/roadmaps/IDEAS_BIBLE_2026.md` |
| **VISIONE** | `CervellaSwarm/.sncp/progetti/miracollo/roadmaps/VISIONE_PIATTAFORMA_2026.md` |
| **BE UX Specs** | `CervellaSwarm/.sncp/progetti/miracollo/handoff/MARKETING_20260313.md` |
| **BE Best Practices** | `CervellaSwarm/.sncp/progetti/miracollo/ricerche/RESEARCH_20260313_booking_engine_redesign_best_practices.md` |
| **Security Audit** | `CervellaSwarm/.sncp/progetti/miracollo/reports/SECURITY_20260313.md` |
| **Ingegnera Audit** | `CervellaSwarm/.sncp/progetti/miracollo/reports/ENGINEER_20260313_deep_code_audit.md` |

---

## INFRASTRUTTURA LIVE

```
VM: miracollo-cervella (GCP), e2-small, RUNNING
IP: 34.134.72.207 | SSL: auto-renew OK (31 Mag 2026)
Deploy: GitHub Actions + pytest gate (2878 test) + auto Docker prune + rollback
Backup: 2x/giorno + pre-deploy | GCS bucket pronto (scope da upgradare)
Migration: 048-057 (057 = room_type_photos, da applicare su VM)
Monitoring: HetrixTools + dead-man's-switch scheduler (/health/schedulers)
```

---

## BOOKING ENGINE - Stato Tecnico Dettagliato

```
WIDGET ATTUALE (gia 3 step):
  Step 1: Date + Ospiti -> Cerca
  Step 2: Seleziona Camera + Tariffa
  Step 3: Dati + Extras + Pagamento -> Prenota
  (Conferma = inline, non step separato)

  File frontend: frontend/booking-widget/
    - index.html (203 righe)
    - css/widget.css (1091 righe)
    - js/modules/ (6 file, 1395 righe)
    Nuovi moduli da aggiungere: widget-calendar.js, widget-gallery.js, widget-stripe.js

  Backend API: backend/routers/public/ (6 file, 1530 righe)
    - GET /api/public/v1/availability (+ foto!)
    - GET /api/public/v1/rooms (+ foto!)
    - GET /api/public/v1/extras
    - GET /api/public/v1/calendar-prices (NUOVO S26!)
    - POST /api/public/v1/bookings
    - POST /api/public/v1/webhooks/stripe

  Dati reali NL (testato):
    - 4 room_types con prezzo
    - 19 giorni disponibili a marzo
    - Prezzo minimo: 180 EUR/notte
    - Calendar-prices endpoint: FUNZIONANTE

  MANCA per redesign frontend:
    - Foto camere reali (serve upload da Rafa!)
    - Calendario custom (hotel-datepicker lib)
    - Stripe Elements (no redirect)
    - Apple/Google Pay config
```

---

## NUMERI SESSIONE 26

```
COMMIT PUSHATI: 10
TEST: 2516 -> 2878 (+362)
BUG FIX: 12 crash runtime prevenuti
SECURITY FIX: 3 (SQL whitelist, aiosqlite PRAGMA, date validation)
AUDIT: Guardiana 9.4, Code Review 7.8, Ingegnera 8.2, Security 9.1
RICERCA: 3 report BE redesign (Marketing + Researcher + tecnico)
NUOVI ENDPOINT: 1 (calendar-prices)
NUOVE MIGRATION: 1 (057 room_type_photos)
REPORT SALVATI: 3 (Security, Ingegnera, BE best practices)
```

---

## Lezioni Apprese (S26)

### Funzionato bene
- 4 agent test paralleli: 362 test in ~15 min, pattern consolidato
- Strategia "agent -> Regina revisiona -> Guardiana audita": 9.4/10
- Bug hunt multi-livello: Code Review + Ingegnera + Security trovano cose diverse
- what_if_api aveva 4 bug SOVRAPPOSTI: solo test sistematici li trovano tutti
- Ricerca BE con 2 agenti paralleli (Marketing + Researcher) = risultato completo in 10 min

### Da NON fare
- `replace_all` puo creare ricorsione se il pattern appare nella sostituzione (whatsapp.py)
- f-string logger: il linter puo revertire - verificare dopo edit
- ML test: puo accidentalmente ritrainare il modello (side-effect)

### Pattern CONFERMATO (3a sessione consecutiva)
- "Test come schema verifier": S24 5 bug, S25 10 bug, S26 7 bug = GOLD PATTERN

---

*"Il diamante si lucida nei dettagli" - e oggi ne abbiamo lucidati tantissimi!*
*"Ultrapassar os proprios limites!" - da 2516 a 2878 test, 12 bug fix, BE backend pronto*

*Cervella & Rafa, 13 Mar 2026*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-14 07:55 (unknown)
- **Branch**: master
- **Ultimo commit**: ebee416 - fix: S26 datetime.now() naive -> UTC in 35 production files
- **File modificati**: Nessuno (git pulito)
<!-- AUTO-CHECKPOINT-END -->
