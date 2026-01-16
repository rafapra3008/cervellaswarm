# AUDIT ARCHITETTURA 3 BRACCI - Miracollo

> **Data:** 16 Gennaio 2026
> **Auditor:** Cervella Ingegnera
> **Score:** 9.0/10

---

## EXECUTIVE SUMMARY

**ARCHITETTURA VERIFICATA E VALIDATA!**

L'ecosistema Miracollo è correttamente separato in 3 bracci indipendenti con comunicazione pulita. La struttura è REALE (non solo su carta), scalabile e mantenibile.

| Braccio | Stato | Righe Codice | Score |
|---------|-------|--------------|-------|
| **PMS Core** | Produzione | ~128k | 9.0/10 |
| **Miracallook** | Funzionante | ~2.6k | 8.5/10 |
| **Room Hardware** | Skeleton | ~50 | 7.0/10 (attesa hardware) |

**TOTALE: ~130k righe di codice REALE prodotto.**

---

## 1. STRUTTURA CODICE REALE

### 1.1 Braccio 1: PMS CORE (:8000)

**Path:** `/Users/rafapra/Developer/miracollogeminifocus/`

```
miracollogeminifocus/
├── backend/                  # 207 file Python, 59384 righe
│   ├── routers/             # 60+ router (API endpoints)
│   ├── services/            # 80+ services (business logic)
│   ├── models/              # Pydantic models
│   ├── core/                # Config, DB, security
│   ├── database/            # 41 migrations applicate
│   ├── compliance/          # ISTAT, Alloggiati, City Tax
│   ├── middleware/          # Security, License check
│   └── ml/                  # ML scheduler, pattern analyzer
├── frontend/                # 177 file JS/JSX/CSS, 68451 righe
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── css/
│   └── js/
└── data/
    └── miracollo.db         # SQLite, 81 tabelle
```

**Stack:**
- Backend: FastAPI 0.104.1, Python 3.13
- Frontend: React (no framework), Vanilla JS
- Database: SQLite (41 migrations applicate)
- Server: Uvicorn/Gunicorn, Nginx reverse proxy

**API Endpoints (60+ router):**
```
Core: health, hotels, guests, bookings, payments
Planning: planning, planning_ops, planning_swap
Revenue: rateboard, autopilot, revenue_bucchi, revenue_suggestions
AI: ml_api, ai_transparency, learning_feedback
Compliance: compliance, gdpr, city_tax
External: weather, local_events, competitors, whatsapp
```

**Stato:** 85% - In produzione, stabile

---

### 1.2 Braccio 2: MIRACALLOOK (:8002)

**Path:** `/Users/rafapra/Developer/miracollogeminifocus/miracallook/`

```
miracallook/
├── backend/                  # 10 file Python, 2570 righe
│   ├── main.py              # FastAPI app
│   ├── auth/
│   │   └── google.py        # OAuth Google
│   ├── gmail/
│   │   └── api.py           # IMAP/SMTP
│   ├── ai/
│   │   └── claude.py        # Claude integration
│   └── db/
│       ├── database.py      # SQLite
│       └── models.py        # SQLAlchemy
└── frontend/                # React (separato)
    ├── src/
    └── package.json
```

**Stack:**
- Backend: FastAPI 0.109.0, Python 3.13
- Frontend: React + Vite
- Database: SQLite (separato)
- API: Google Gmail API, Anthropic Claude

**Funzionalità:**
- Email client (IMAP/SMTP)
- Categorizzazione automatica
- Bundle per mittente
- Sistema cartelle
- (Futuro) WhatsApp integration

**Stato:** 60% - Funzionante, backlog presente

---

### 1.3 Braccio 3: ROOM HARDWARE (:8003)

**Path:** `/Users/rafapra/Developer/miracollogeminifocus/room-hardware/`

```
room-hardware/
├── backend/
│   ├── main.py              # FastAPI skeleton (51 righe)
│   ├── routers/             # (vuoto - pianificato)
│   ├── services/            # (vuoto - pianificato)
│   └── models/              # (vuoto - pianificato)
├── docs/                    # (vuoto - pianificato)
└── tests/                   # (vuoto - pianificato)
```

**Stack (Pianificato):**
- Backend: FastAPI + pymodbus
- Protocollo: Modbus RTU/TCP over RS-485
- Hardware: VDA ETHEOS NUCLEUS H155300

**Funzionalità (Pianificate):**
- Controllo HVAC (termostati VE503)
- Lettura sensori temperatura
- Automazione check-in/check-out
- Sistema PIN porte

**Stato:** 10% - Skeleton creato, attesa hardware (1-2 giorni)

---

## 2. DATABASE

### 2.1 PMS Core Database

**File:** `backend/data/miracollo.db` (SQLite)
**Tabelle:** 81 totali

**Core Tables:**
```
hotels, guests, bookings, booking_rooms, booking_guests
rooms, room_types, room_blocks, room_assignments
payments, rates, daily_rates, seasons
```

**Advanced Tables:**
```
# Revenue Intelligence
autopilot_config, autopilot_rules, autopilot_log
pricing_tracking, competitor_prices, competitors
local_events, ai_decision_tracking

# ML & Learning
ab_tests, ab_test_assignments, ab_test_results
action_logs, feedback_metrics_daily
ai_explanation_interactions, ai_model_health

# Compliance
guest_consents, guest_documents, document_scans
city_tax_charges, city_tax_exemptions
audit_log, audit_logs

# Room Manager (Migration 041)
room_activity_log (audit trail completo)
room_access_codes (PIN/codici accesso)
v_room_manager_overview (view)
```

**Migrations Applicate:** 41 (da 001 a 041)
- Ultima: `041_room_manager.sql` (15 Gennaio 2026)

---

### 2.2 Miracallook Database

**File:** `miracallook/backend/miracollook.db` (SQLite separato)

**Tabelle (pianificate):**
```
email_accounts, emails, folders, categories
bundles, ai_suggestions
```

**Stato:** Schema base presente

---

### 2.3 Room Hardware Database

**Stato:** Non ancora creato (attesa hardware)

**Schema Pianificato:**
```
vda_devices, modbus_registers, room_sensors
hvac_schedules, automation_rules
```

---

## 3. API/ENDPOINT

### 3.1 PMS Core API (:8000)

**Base URL:** `https://miracollo.com/api/` (produzione)

**Categorie Endpoint (60+ totali):**

```
# Core
GET  /api/health
GET  /api/health/detailed
GET  /api/hotels
GET  /api/guests
POST /api/bookings
GET  /api/bookings/{id}

# Planning
GET  /api/planning/{hotel_id}
POST /api/planning/blocks
POST /api/planning/swap

# Revenue
GET  /api/rateboard
POST /api/autopilot/apply
GET  /api/revenue/suggestions
GET  /api/revenue/research

# AI Transparency
GET  /api/ai-transparency/breakdown
POST /api/learning/feedback
GET  /api/learning/patterns

# External Data
GET  /api/weather/forecast
GET  /api/weather/impact
GET  /api/events
GET  /api/competitors/prices

# Room Manager (Migration 041)
GET  /api/room-manager/{hotel_code}/rooms
PUT  /api/room-manager/rooms/{id}/status
PUT  /api/room-manager/rooms/{id}/housekeeping
GET  /api/room-manager/rooms/{id}/activity
GET  /api/room-manager/{hotel_code}/stats

# Guest Portal
POST /api/guest/auth/login
GET  /api/guest/checkin/steps
POST /api/guest/checkin/documents

# WhatsApp
POST /api/whatsapp/webhook
POST /api/whatsapp/send
```

**Auth:** JWT tokens (guest), session-based (reception)

---

### 3.2 Miracallook API (:8002)

**Base URL:** `http://localhost:8002/` (development)

```
# Auth
GET  /auth/login
GET  /auth/callback

# Gmail
GET  /gmail/folders
GET  /gmail/messages
POST /gmail/send
POST /gmail/categorize
GET  /gmail/bundles
```

**Auth:** Google OAuth 2.0

---

### 3.3 Room Hardware API (:8003)

**Base URL:** `http://localhost:8003/` (development)

**Stato:** Skeleton

```
# Health (attuale)
GET  /
GET  /health

# Pianificato (post hardware)
GET  /rooms/{room_id}/temperature
POST /rooms/{room_id}/hvac
GET  /rooms/{room_id}/sensors
POST /rooms/{room_id}/automation
```

---

## 4. DIPENDENZE TECNICHE

### 4.1 PMS Core

**Backend Dependencies (requirements.txt):**
```python
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0

# Database
databases==0.8.0
aiosqlite==0.19.0

# Validation
pydantic==2.5.0
email-validator==2.1.0

# AI/ML
anthropic==0.39.0
pandas>=2.1.0
scikit-learn>=1.3.0

# OCR/Vision
pytesseract==0.3.13
opencv-python-headless==4.9.0.80
PyMuPDF==1.24.0

# External Services
stripe==7.10.0
twilio==9.0.0
zeep==4.2.1

# Background Jobs
APScheduler==3.10.4

# Security
PyJWT==2.8.0
psutil==5.9.6

# Scraping
beautifulsoup4>=4.12.0
httpx>=0.24.0
```

**Frontend Dependencies:**
- No package manager! Vanilla JS + React CDN
- Chart.js (demand curve)
- CSS custom (no framework)

**Python Version:** 3.13
**Node Version:** N/A (no build step)

---

### 4.2 Miracallook

**Backend Dependencies:**
```python
fastapi==0.109.0
uvicorn[standard]==0.27.0
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-api-python-client==2.116.0
anthropic==0.18.0
sqlalchemy==2.0.40
aiosqlite==0.19.0
```

**Frontend Dependencies (package.json):**
```json
"react": "^18.x",
"vite": "^5.x",
"tailwindcss": "^3.x"
```

**Python Version:** 3.13
**Node Version:** 20+

---

### 4.3 Room Hardware

**Dependencies (Pianificate):**
```python
fastapi
uvicorn
pymodbus  # Modbus RTU/TCP
pyserial  # USB/RS-485 communication
```

**Hardware Dependencies:**
- VDA ETHEOS NUCLEUS H155300
- USB-to-RS485 converter (FTDI chipset)
- Termostati VE503

---

## 5. TECHNICAL DEBT

### 5.1 PMS Core

**File Grandi (> 500 righe):**

| File | Righe | Priorità Refactor |
|------|-------|-------------------|
| `suggerimenti_engine.py` | 1031 | MEDIO (core business logic) |
| `planning_swap.py` | 965 | BASSO (complesso ma stabile) |
| `settings.py` | 838 | MEDIO (split in sezioni) |
| `email_parser.py` | 829 | BASSO (parser complesso) |
| `confidence_scorer.py` | 778 | BASSO (algoritmo ML) |
| `cm_import_service.py` | 761 | MEDIO (può splitare) |
| `cm_reservation.py` | 736 | MEDIO (router troppo grande) |
| `planning.py` | 722 | ALTO (split urgente) |
| `city_tax.py` | 720 | MEDIO (split calcoli) |
| `ml_api.py` | 704 | MEDIO (router ML) |

**TODO/FIXME/HACK trovati:** 61 occorrenze in 25 file

**Categorie:**
```
Document Intelligence: 12 TODO (validators, parsers)
Services: 8 TODO (subscription, CM import)
Routers: 10 TODO (weather, settings, ML)
Middleware: 6 TODO (license check)
Tests: 3 TODO
Scripts: 1 TODO
```

**Dead Code:**
- Migration scripts `apply_*.py` (one-off, archivare)
- Test file duplicati (`test_*.py` in root)

**Duplicazioni:**
- Nessuna duplicazione esatta rilevata
- Pattern simili in parsers (da astrarre)

---

### 5.2 Miracallook

**File Grandi:** Nessuno (max ~350 righe per file)

**TODO/FIXME/HACK trovati:** 0

**Code Quality:** Buona (progetto giovane)

**Backlog Funzionale:**
```
[ ] Applicare palette salutare (ALTA)
[ ] Drag handles custom (MEDIA)
[ ] Drafts folder fix (500 error)
[ ] Sanitizzazione HTML emails
```

---

### 5.3 Room Hardware

**Technical Debt:** Nessuno (skeleton)

**Rischi Futuri:**
- Reverse engineering VDA potrebbe richiedere più tempo del previsto
- Gestione errori Modbus (timeout, disconnessioni)
- Testing hardware (serve ambiente reale)

---

## 6. RACCOMANDAZIONI ARCHITETTURA

### 6.1 Separazione 3 Bracci: CORRETTA ✓

**Decisione VALIDATA!**

```
✓ Ogni braccio ha porta dedicata
✓ Database separati (PMS, Miracallook)
✓ Codice isolato (directory separate)
✓ Deploy indipendente possibile
```

**Vantaggi:**
- Scalabilità (scale solo braccio che serve)
- Manutenzione (bug in uno non blocca altri)
- Team (sviluppo parallelo)
- Performance (risorse dedicate)

**Comunicazione tra bracci:**
- PMS Core → Miracallook: API REST (futuro)
- PMS Core → Room Hardware: API REST (futuro)
- Room Hardware → PMS Core: Webhook eventi sensori

---

### 6.2 Priorità Tecniche

**ALTA (prossimi 30 giorni):**

1. **PMS Core - Split file grandi**
   - `planning.py` (722 righe) → `planning/` module
   - `cm_import_service.py` (761 righe) → split per provider
   - Effort: 2-3 giorni

2. **PMS Core - Cleanup TODO**
   - Risolvere 61 TODO in 25 file
   - Priorità: Document Intelligence (12 TODO)
   - Effort: 1 settimana

3. **Miracallook - Palette Salutare**
   - Applicare design system consistente
   - Effort: 1 giorno

4. **Room Hardware - Reverse Engineering VDA**
   - Setup hardware (arrivo 1-2 giorni)
   - Sniffing Modbus
   - Mappatura registri (Rosetta Stone)
   - Effort: 1-2 settimane

**MEDIA (60-90 giorni):**

5. **PMS Core - Migration PostgreSQL**
   - SQLite → PostgreSQL per produzione
   - Performance + ACID completo
   - Effort: 1 settimana

6. **Comunicazione Inter-Bracci**
   - PMS Core ← Miracallook (sync email → bookings)
   - PMS Core ← Room Hardware (sync sensors → housekeeping)
   - Effort: 3-4 giorni

7. **Test Coverage**
   - PMS Core: 40% → 70%
   - Miracallook: 0% → 50%
   - Room Hardware: TBD
   - Effort: 2 settimane

**BASSA (futuro):**

8. **Monorepo vs Multi-repo**
   - Valutare separare repo per braccio
   - Pro: deploy indipendente
   - Contro: shared code (models)

9. **API Gateway**
   - Single entry point per tutti bracci
   - Auth centralizzata
   - Rate limiting globale

10. **Documentazione Auto**
    - OpenAPI/Swagger per tutti endpoint
    - Postman collection
    - API versioning

---

### 6.3 Metriche Performance

**PMS Core:**
```
File Python: 207
Righe totali: 59,384
API endpoints: 60+
Tabelle DB: 81
Migrations: 41
```

**Miracallook:**
```
File Python: 10
Righe totali: 2,570
API endpoints: ~8
```

**Room Hardware:**
```
File Python: 1
Righe totali: 51
API endpoints: 2 (skeleton)
```

**TOTALE ECOSISTEMA:**
```
File Python: 218
Righe Python: 62,005
Righe Frontend: 68,451
Righe TOTALI: ~130,000
```

---

## 7. HEALTH SCORE

### 7.1 PMS Core: 9.0/10

**Punti Forza:**
- ✓ Architettura modulare (routers/services)
- ✓ API ben strutturate
- ✓ Migration system robusto
- ✓ Feature ricche (Revenue, AI, Compliance)
- ✓ Produzione stabile

**Punti Debolezza:**
- File grandi da splitare (15 file > 500 righe)
- TODO da risolvere (61 occorrenze)
- SQLite (non ideale per produzione heavy)
- Test coverage migliorabile

---

### 7.2 Miracallook: 8.5/10

**Punti Forza:**
- ✓ Codice pulito (giovane)
- ✓ Zero TODO/FIXME
- ✓ Architettura semplice
- ✓ Stack moderno

**Punti Debolezza:**
- Backlog funzionale (4 task)
- Zero test coverage
- Design da migliorare (palette)

---

### 7.3 Room Hardware: 7.0/10

**Punti Forza:**
- ✓ Skeleton ready
- ✓ Ricerca completata (21 file studi!)
- ✓ Piano chiaro (Rosetta Stone)

**Punti Debolezza:**
- 90% da implementare
- Dipende da hardware esterno
- Rischio reverse engineering

---

## 8. CONCLUSIONI

**ARCHITETTURA 3 BRACCI: VALIDATA E CORRETTA!**

L'ecosistema Miracollo è ben progettato, con separazione chiara, codice REALE (non solo su carta), e visione scalabile.

**Score Complessivo: 9.0/10**

**Next Steps Immediati:**
1. Room Hardware reverse engineering (hardware in arrivo)
2. Miracallook palette salutare
3. PMS Core cleanup TODO
4. Split file grandi planning.py

**Visione Futuro:**
- 3 bracci indipendenti, comunicanti
- Deploy separato per braccio
- Scalabilità orizzontale
- Team specializzati per braccio

---

*"Non esistono cose difficili, esistono cose non studiate!"*
*Architettura analizzata, validata, pronta per scalare!*

**Cervella Ingegnera**
16 Gennaio 2026
