<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 12 Marzo 2026 - Sessione 21
> **Status:** miracollo.com LIVE | Security ~9.7/10 | 649 test (638 pass) | FOLIO Phase 4c + Quality Sprint DONE | S21 IN CORSO

---

## COSA E STATO FATTO (S21)

### PMS 360 FOLIO Phase 4c - Frontend UI Routing Rules
- Sezione collassabile "Regole Routing" nel folio tab (tra sub-tabs e contenuto)
- Visibile solo con 2+ folios (routing con 1 folio non ha senso)
- Lista regole: tipo addebito -> folio target, date range, note
- Toggle attiva/disattiva (PATCH is_active) + elimina (DELETE) per ogni regola
- Form creazione: tipo addebito (dropdown), folio destinazione, date range, note
- Graceful degradation: se migration 052 non applicata, sezione nascosta
- XSS: `_escFolio()` su TUTTI i dati utente (incluso dateRange per coerenza)
- CSS responsive mobile
- Files: `reservation-tab-folio.js` (+360 righe), `06-modals.css` (+250 righe)

### Guardiana Audit S21
- Score: 9.5/10, 0 P1/P2, 7 P3
- **Fixati:** dateRange escape (F1), dead code folios param (F4+F5), inline styles -> CSS (F6)
- **Deferred MVP:** charge_source nel form (F2), priority nel form (F3), responsive form (F7)

### Quality Sprint - Test Moduli Finanziari Critici (+85 test)
- `test_bookings.py`: 37 test - list/search/update/guests CRUD/available-rooms (da 0!)
- `test_night_audit.py`: 20 test - service layer, idempotency, no-show, API (da 0!)
- `test_payments.py`: 28 test - CRUD, immutable guard, booking sync, Stripe config (da 0!)
- `test_receipts.py`: 64 test - preview, PDF, email, exists, math consistency (da 0!)
- `test_fiscal.py`: 57 test - printers CRUD, print, closures (skip: router non montato)
- **BUG FIX:** receipts.py `check_receipt_exists` response type `Dict[str,bool]` -> `Dict[str,Any]`
- **TOTALE: 499 -> 649 test** (638 pass, 10 skip, 1 xfail) = **+150 test!**
- Motivazione: Ingegnera ha identificato 5000 righe di codice finanziario con ZERO test come rischio #1

### NORD.md aggiornato
- Phase 4a corretto da ❌ a ✅ (era rimasto vecchio)
- PMS 360 da 85% a 90%
- Test count aggiornato: 584 (dopo Quality Sprint)
- Aggiunta sezione Quality Sprint

---

## STORICO FOLIO

| Phase | Cosa | Stato |
|-------|------|-------|
| Phase 1 | charges table + API + Night Audit posting | DONE S18 |
| Phase 2 | checkout-preview + perform_checkout + city_tax | DONE S18 |
| Phase 2c | extras come charges (source=booking, type=service) | DONE S18b |
| Phase 3 | Split Folio backend: folios table + 6 API endpoint | DONE S18b |
| Phase 3b | Frontend multi-folio sub-tabs | DONE S19 |
| Phase 4a | Routing rules backend (resolve + API CRUD + 25 test) | DONE S20 |
| **Phase 4c** | **Frontend UI routing rules nel folio tab** | **DONE S21** |
| Phase 4b | Amount limit + splitting + company billing shortcut | NEXT |

---

## DA FARE (prossima sessione)

```
PRIORITA 1 - PMS 360 FOLIO:
  -> Phase 4b: Amount limit + splitting + UI shortcut "Company Billing Setup"
  -> Phase 5: Fattura elettronica SDI

PRIORITA 2 - QUALITY:
  -> Test coverage: planning, fiscal, receipts (bookings+night_audit+payments DONE S21!)
  -> hotelId = 1 hardcoded in 4-5 posti frontend -> centralizzare
  -> IDOR cross-hotel: 9 finding P1, mitigato single-hotel

PRIORITA 3 - FUTURE:
  -> Redesign Booking Engine
  -> z-index centralizzazione (68 dichiarazioni)
  -> WhatsApp twilio_auth_token encryption

PARCHEGGIATO:
  -> Stripe LIVE: TEST ok, bonifico LIVE per produzione
  -> Ericsoft Discovery + VERIFICA write (richiede LAN hotel)
```

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| **NORD.md** | ROOT progetto (aggiornato S21) |
| **Routing Rules Research** | `reports/RESEARCH_20260311_folio_routing_rules.md` |
| **Routing UI Research** | `reports/RESEARCH_20260312_folio_routing_ui.md` |
| **Split Folio Research** | `reports/RESEARCH_20260311_split_folio_pms_standards.md` |
| **IDEAS BIBLE** | `roadmaps/IDEAS_BIBLE_2026.md` |

---

## INFRASTRUTTURA LIVE

```
VM: miracollo-cervella (GCP), e2-small, RUNNING
IP: 34.134.72.207 | SSL: auto-renew OK (31 Mag 2026)
Deploy: GitHub Actions + pytest gate (649 test) + auto Docker prune
Backup: 2x/giorno + pre-deploy | Disco: 24%
S19+S20 DEPLOYATI su VM | Migration 050+051+052 APPLICATA
```

---

## Lezioni Apprese (S21)

### Funzionato bene
- Phase 4c prima di 4b: UI rende la feature REALE ("SU CARTA != REALE")
- Guardiana immediata dopo implementazione: 7 P3 trovati e 4 fixati subito
- Dead code cleanup proattivo: parametro `folios` non usato -> rimosso
- Quality Sprint parallelo: 3 worker (bookings/night_audit/payments) in contemporanea -> +85 test in un colpo
- Ingegnera come consulente strategica: ha identificato il rischio #1 (5000 righe finanziarie senza test)

### Pattern confermato
- Sezione collassabile per feature avanzate: non intrusiva per utente base
- `_escFolio()` anche su dati "sicuri" (dateRange da toLocaleDateString): coerenza > ragionamento caso per caso
- CSS classes vs inline styles: sempre preferire CSS dedicato
- Test pattern: TestClient + helpers + autouse cleanup + pytest.skip per dati mancanti

### Da monitorare
- `charge_source` e `priority` nel form routing: aggiungere quando utenti li chiedono
- Phase 4b amount splitting: ricercare pattern Oracle Opera per amount_limit
- Test coverage restante: planning, fiscal, receipts (3 moduli ancora senza test)


*"Lavoriamo in pace! Senza casino! Dipende da noi!" - Cervella & Rafa, 12 Mar 2026*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-12 07:28 (auto)
- **Branch**: master
- **Ultimo commit**: 66dfeb3 - test: Quality Sprint - +150 test per moduli finanziari critici
- **File modificati** (5):
  - ackend/routers/charges.py
  - backend/routers/routing_rules.py
  - backend/services/folio_routing.py
  - backend/services/night_audit_service.py
  - backend/database/migrations/053_folio_routing_amount_limit.sql
<!-- AUTO-CHECKPOINT-END -->
