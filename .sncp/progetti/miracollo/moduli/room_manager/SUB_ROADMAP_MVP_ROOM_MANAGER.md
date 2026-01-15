# SUB-ROADMAP MVP ROOM MANAGER - MIRACOLLO

> **Creata:** 15 Gennaio 2026 - Sessione 213
> **Filosofia:** Una cosa alla volta, fino al 100000%!
> **Principio:** "Non importa il TEMPO - abbiamo TEMPO!"

---

## SITUAZIONE ATTUALE

### Cosa Esiste GIA'

```
DATABASE:
+--------------------------------------------------------------+
| rooms                                                        |
|   - id, hotel_id, room_type_id, room_number, floor, notes    |
|   - housekeeping_status (5 stati!)                           |
|   - housekeeping_updated_at, housekeeping_updated_by         |
+--------------------------------------------------------------+
| room_blocks (MICRO-08)                                       |
|   - Blocchi temporanei: maintenance, out_of_order, etc.      |
+--------------------------------------------------------------+
| room_assignments (MICRO-10)                                  |
|   - Segmenti cambio camera durante soggiorno                 |
+--------------------------------------------------------------+

BACKEND:
+--------------------------------------------------------------+
| routers/planning.py      | GET planning con rooms            |
| routers/housekeeping.py  | PATCH status, GET housekeeping    |
| models/room.py           | RoomStatusUpdate, RoomBlockCreate |
+--------------------------------------------------------------+

FRONTEND:
+--------------------------------------------------------------+
| planning.html + planning.js  | Planning board completo       |
| planning/modal-room.js       | Modals blocco + info camera   |
| planning/housekeeping-core.js| Config stati housekeeping     |
+--------------------------------------------------------------+
```

### Cosa MANCA per MVP

```
P0 - CRITICO (MVP Core):
[ ] Room Grid View (UI dedicata Room Manager)
[ ] Room Card Dettaglio (click su camera)
[ ] Activity Log base (storico housekeeping)
[ ] API CRUD rooms completo

P1 - IMPORTANTE (Post-MVP immediato):
[ ] VDA Temperature Read (mock per ora)
[ ] PIN Generation base
[ ] Bulk status update

P2 - NICE TO HAVE (Futuro):
[ ] Mobile App Housekeeping
[ ] HVAC Control
[ ] Energy Dashboard
```

---

## ARCHITETTURA MVP

### Schema Dati Esteso

```sql
-- NUOVI CAMPI per rooms (migration 041)
ALTER TABLE rooms ADD COLUMN
  status TEXT DEFAULT 'available',           -- available, out_of_service, out_of_order
  current_temperature REAL,                  -- da VDA (futuro)
  target_temperature REAL,                   -- da VDA (futuro)
  door_status TEXT DEFAULT 'unknown',        -- closed, open, unknown
  presence_detected BOOLEAN DEFAULT FALSE,   -- sensore presenza
  dnd_active BOOLEAN DEFAULT FALSE,          -- Do Not Disturb
  mur_active BOOLEAN DEFAULT FALSE;          -- Make Up Room request

-- NUOVA TABELLA: room_activity_log (audit trail)
CREATE TABLE room_activity_log (
  id INTEGER PRIMARY KEY,
  room_id INTEGER REFERENCES rooms(id),
  event_type TEXT NOT NULL,
    -- 'status_change', 'housekeeping_change', 'access', 'temperature', 'block'
  old_value TEXT,
  new_value TEXT,
  changed_by TEXT,
  source TEXT DEFAULT 'manual',              -- 'manual', 'system', 'vda', 'api'
  metadata TEXT,                             -- JSON extra info
  created_at TEXT DEFAULT (datetime('now'))
);

-- NUOVA TABELLA: room_access_codes (PIN generation)
CREATE TABLE room_access_codes (
  id INTEGER PRIMARY KEY,
  room_id INTEGER REFERENCES rooms(id),
  booking_id INTEGER REFERENCES bookings(id),
  code_type TEXT DEFAULT 'pin',              -- 'pin', 'rfid', 'ble'
  code_value TEXT NOT NULL,
  role TEXT DEFAULT 'guest',                 -- 'guest', 'staff', 'maintenance'
  valid_from TEXT NOT NULL,
  valid_until TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_by TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
```

### Backend Services

```
backend/services/
├── room_manager_service.py    # NUOVO - Core room management
├── room_activity_service.py   # NUOVO - Activity log
└── room_access_service.py     # NUOVO - PIN/codes (P1)
```

### API Endpoints

```
/api/room-manager/rooms                    GET    Lista camere con status
/api/room-manager/rooms/{id}               GET    Dettaglio camera
/api/room-manager/rooms/{id}/status        PUT    Cambia status camera
/api/room-manager/rooms/{id}/housekeeping  PUT    Cambia housekeeping
/api/room-manager/rooms/{id}/activity      GET    Activity log camera
/api/room-manager/activity                 GET    Activity log globale
/api/room-manager/stats                    GET    Statistiche
```

### Frontend

```
frontend/
├── room-manager.html          # NUOVA pagina Room Manager
└── js/
    └── room-manager/
        ├── core.js            # Init, fetch, state
        ├── grid.js            # Room Grid View
        ├── card.js            # Room Card Dettaglio
        ├── activity.js        # Activity Log Panel
        └── stats.js           # Statistiche panel
```

---

## SESSIONI DI LAVORO

### SESSIONE A: Database + Backend Core

**Obiettivo:** Migration DB + Service base + API lista

**Task:**
1. [ ] Creare migration `041_room_manager.sql`
   - Nuovi campi rooms (status, temperature, door, presence, dnd, mur)
   - Tabella room_activity_log
   - Indici per performance

2. [ ] Creare `room_manager_service.py`
   - `get_rooms(hotel_id)` - Lista con housekeeping + status
   - `get_room(room_id)` - Dettaglio singola camera
   - `update_room_status(room_id, status, changed_by)`
   - `update_housekeeping(room_id, status, changed_by)`
   - `log_activity(room_id, event_type, old, new, by, source)`

3. [ ] Creare `routers/room_manager.py`
   - `GET /api/room-manager/rooms`
   - `GET /api/room-manager/rooms/{id}`
   - `PUT /api/room-manager/rooms/{id}/status`
   - `PUT /api/room-manager/rooms/{id}/housekeeping`

4. [ ] Aggiornare `models/room.py`
   - RoomManagerRoom (response model completo)
   - RoomStatusChange (input model)
   - RoomActivity (log entry model)

**Output:** API funzionanti, testabili con curl/Postman

---

### SESSIONE B: Activity Log Backend

**Obiettivo:** Activity log completo con storico

**Task:**
1. [ ] Creare `room_activity_service.py`
   - `get_room_activity(room_id, limit, offset)`
   - `get_global_activity(hotel_id, filters, limit, offset)`
   - `get_activity_stats(hotel_id, date_range)`

2. [ ] Aggiungere endpoint activity
   - `GET /api/room-manager/rooms/{id}/activity`
   - `GET /api/room-manager/activity`
   - `GET /api/room-manager/stats`

3. [ ] Trigger automatici activity log
   - Ogni cambio housekeeping_status -> log
   - Ogni cambio status camera -> log
   - Ogni creazione/eliminazione block -> log

**Output:** Activity log popolato automaticamente

---

### SESSIONE C: Frontend Room Grid

**Obiettivo:** Pagina Room Manager con grid camere

**Task:**
1. [ ] Creare `room-manager.html`
   - Header con titolo + filtri
   - Grid camere (cards)
   - Sidebar per dettaglio/activity

2. [ ] Creare `js/room-manager/core.js`
   - Fetch rooms da API
   - State management locale
   - Event handlers

3. [ ] Creare `js/room-manager/grid.js`
   - Render grid camere
   - Colori per stato (come planning)
   - Click per aprire dettaglio
   - Filtri per floor/status/housekeeping

4. [ ] CSS styling
   - Grid responsive
   - Cards con colori stato
   - Dark mode support

**Output:** Pagina Room Manager visibile, grid funziona

---

### SESSIONE D: Frontend Room Card + Activity

**Obiettivo:** Dettaglio camera + activity log

**Task:**
1. [ ] Creare `js/room-manager/card.js`
   - Panel dettaglio camera
   - Mostra: numero, tipo, status, housekeeping
   - Bottoni azione: Set Dirty, Set Clean, etc.
   - Sezione sensori (placeholder per VDA)

2. [ ] Creare `js/room-manager/activity.js`
   - Panel activity log
   - Lista eventi con timestamp
   - Filtri per tipo evento
   - Load more (pagination)

3. [ ] Integrazione
   - Click camera -> apre card
   - Azioni card -> aggiorna grid
   - Activity si aggiorna real-time

**Output:** Room Manager completo e usabile!

---

### SESSIONE E: Test + Affinamenti

**Obiettivo:** Tutto funziona al 100%

**Task:**
1. [ ] Test manuali completi
   - Tutti gli stati funzionano
   - Activity log si popola
   - UI responsive

2. [ ] Fix bug trovati

3. [ ] Affinamenti UX
   - Transizioni
   - Loading states
   - Error handling

4. [ ] Documentazione
   - API docs
   - Screenshot funzionalita

**Output:** MVP Room Manager PRONTO!

---

## CHECKLIST FINALE MVP

```
DATABASE:
[ ] Migration 041 in produzione
[ ] Tabella room_activity_log creata
[ ] Nuovi campi rooms aggiunti

BACKEND:
[ ] room_manager_service.py
[ ] room_activity_service.py
[ ] routers/room_manager.py
[ ] Models aggiornati

FRONTEND:
[ ] room-manager.html
[ ] Room Grid funzionante
[ ] Room Card funzionante
[ ] Activity Log funzionante

TEST:
[ ] API testate
[ ] UI testata
[ ] No bug critici

DEPLOY:
[ ] Commit + Push
[ ] Deploy produzione
[ ] Verifica funziona REALE
```

---

## POST-MVP (Sessioni Future)

### FASE P1: VDA Temperature

```
[ ] Mock API temperatura (prima del vero VDA)
[ ] UI mostra temperatura in card
[ ] Storico temperature
```

### FASE P1: PIN Generation

```
[ ] Tabella room_access_codes
[ ] API genera PIN per booking
[ ] UI mostra codici attivi
```

### SESSIONE F: PWA Housekeeping (Parte del MVP!)

```
DECISIONE RAFA: WebApp invece di App Store!
- Uso interno staff
- Ogni uno usa suo cellulare
- Niente store, niente review

[ ] PWA housekeeping
[ ] Offline-first (Service Worker)
[ ] Installabile su home screen
[ ] Push notifications
```

### FASE P2: VDA Integration Reale

```
[ ] MODBUS client
[ ] VDA adapter
[ ] Sync real-time
```

---

## PRINCIPI GUIDA

```
+================================================================+
|                                                                |
|   1. UNA COSA ALLA VOLTA                                       |
|      Finisci una sessione prima di iniziare la prossima        |
|                                                                |
|   2. OGNI SESSIONE HA OUTPUT MISURABILE                        |
|      "Cosa posso testare/vedere alla fine?"                    |
|                                                                |
|   3. NON ABBIAMO FRETTA                                        |
|      Fatto BENE > Fatto VELOCE                                 |
|                                                                |
|   4. DOCUMENTA MENTRE FAI                                      |
|      SNCP aggiornato = Cervella futura felice                  |
|                                                                |
|   5. REALE > SU CARTA                                          |
|      Non e' fatto finche' non funziona IN PRODUZIONE           |
|                                                                |
+================================================================+
```

---

*"Non copiamo VDA - facciamo PIU' SMART, FLUIDO, BELLO!"*
*"La semplicita di Mews + La domotica di Scidoo + L'hardware VDA = MIRACOLLO!"*

*Sub-Roadmap creata: 15 Gennaio 2026 - Sessione 213*
