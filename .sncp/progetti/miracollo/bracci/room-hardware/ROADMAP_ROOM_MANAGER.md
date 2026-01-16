# ROADMAP ROOM MANAGER - MIRACOLLO

> **Creata:** 14 Gennaio 2026 - Sessione 212
> **Obiettivo:** Room Manager PIU' SMART, FLUIDO, BELLO di VDA!
> **Filosofia:** Una cosa alla volta, fino al 100000%!

---

## LA VISIONE

```
+================================================================+
|                                                                |
|   "Non copiamo VDA - facciamo PIU' SMART, FLUIDO, BELLO!"     |
|                                                                |
|   VDA = Sistema industriale, funzionale ma RIGIDO              |
|   NOI = AI-first, fluido, bello, SMART                        |
|                                                                |
+================================================================+
```

---

## FASE 0: STUDIO E RICERCA (Sessioni 210-212+)

### 0.1 Studio VDA Etheos ✅ COMPLETATO!

| Task | Status | Sessione |
|------|--------|----------|
| Screenshot 1-3 (Overview) | ✅ | 210 |
| Screenshot 4-21 (Dettagli) | ✅ | 211 |
| Screenshot 22-26 (Activity Log) | ✅ | 212 |
| Documento PARTE 1 | ✅ | 210 |
| Documento PARTE 2 | ✅ | 211 |
| Documento PARTE 3 | ✅ | 212 |

**Output:**
- `.sncp/progetti/miracollo/moduli/room_manager/studi/20260114_ANALISI_VDA_ETHEOS_PARTE1.md`
- `.sncp/progetti/miracollo/moduli/room_manager/studi/20260114_ANALISI_VDA_ETHEOS_PARTE2.md`
- `.sncp/progetti/miracollo/moduli/room_manager/studi/20260114_ANALISI_VDA_ETHEOS_PARTE3.md`

### 0.2 Studio Big Players ⏳ IN CORSO

| Player | Tipo | Priorità | Status |
|--------|------|----------|--------|
| **Mews** | Cloud PMS + RM | ALTA | ⏳ |
| **Opera Cloud** (Oracle) | Enterprise PMS | ALTA | ⏳ |
| **Cloudbeds** | SMB Cloud PMS | ALTA | ⏳ |
| **Apaleo** | API-first PMS | MEDIA | ⏳ |
| **Protel** | Enterprise PMS | MEDIA | ⏳ |
| **RoomRaccoon** | SMB AI PMS | MEDIA | ⏳ |
| **Clock PMS** | Boutique PMS | BASSA | ⏳ |

**Cosa studiare per ogni player:**
```
1. ROOM STATUS
   - Quali stati? (clean, dirty, inspected, OOO, OOS)
   - Come visualizzano?
   - Workflow housekeeping?

2. ACCESSI / CHIAVI
   - Integrazione serrature?
   - Mobile key?
   - Codici PIN?

3. HVAC / ENERGIA
   - Controllo temperatura?
   - Automazioni?
   - Risparmio energetico?

4. ACTIVITY LOG / AUDIT
   - Cosa loggano?
   - Come visualizzano?
   - Analytics?

5. UI/UX
   - Design?
   - Mobile app?
   - Facilità d'uso?

6. INTEGRAZIONI
   - API aperte?
   - Hardware supportato?
   - PMS integrati?
```

### 0.3 Confronto e Decisioni

| Task | Status |
|------|--------|
| Tabella confronto VDA vs Big Players | ⏳ |
| Identificare best practices | ⏳ |
| Decidere feature MVP | ⏳ |
| Decidere architettura | ⏳ |

---

## FASE 1: ARCHITETTURA E DECISIONI

### 1.1 Decisioni Chiave

```
DOMANDE DA RISPONDERE:

1. STATI CAMERA
   - Quanti stati? Quali?
   - Un campo o due (status + housekeeping)?
   - Decisione Sessione 207: DUE CAMPI ✅

2. FRONTEND
   - Dentro Planning o separato?
   - Decisione Sessione 207: SEPARATO ✅
   - Path: /room-manager

3. HARDWARE
   - Supportare VDA esistente?
   - Protocollo MODBUS?
   - API wrapper?

4. ACCESSI
   - Generare codici PIN?
   - Integrazione BLE?
   - Mobile key futuro?

5. AUTOMAZIONI
   - HVAC automatico?
   - Trigger presenza?
   - Risparmio energetico?
```

### 1.2 Architettura Tecnica

```
COMPONENTI:

BACKEND:
├── rooms_service.py (esistente, da estendere)
├── room_manager_service.py (NUOVO)
├── access_service.py (NUOVO - chiavi/codici)
├── hvac_service.py (NUOVO - clima)
└── activity_log_service.py (NUOVO - audit)

FRONTEND:
├── /room-manager (NUOVO)
│   ├── RoomGrid.jsx
│   ├── RoomCard.jsx
│   ├── HousekeepingPanel.jsx
│   ├── AccessPanel.jsx
│   └── ActivityLog.jsx

DATABASE:
├── rooms (esistente, da estendere)
├── room_status_history (NUOVO)
├── room_access_codes (NUOVO)
├── room_access_log (NUOVO)
└── room_hvac_settings (NUOVO)

INTEGRAZIONI:
├── VDA MODBUS (futuro)
├── Serrature smart (futuro)
└── Termostati smart (futuro)
```

---

## FASE 2: MVP BACKEND

### 2.1 Estensione Schema Rooms

```sql
-- Campi da aggiungere a rooms
ALTER TABLE rooms ADD COLUMN IF NOT EXISTS
  housekeeping_status VARCHAR(20) DEFAULT 'clean',
  last_cleaned_at TIMESTAMP,
  last_inspected_at TIMESTAMP,
  last_inspected_by INTEGER REFERENCES users(id),
  hvac_mode VARCHAR(20) DEFAULT 'auto',
  target_temperature DECIMAL(4,2),
  current_temperature DECIMAL(4,2),
  door_status VARCHAR(20) DEFAULT 'closed',
  occupancy_sensor BOOLEAN DEFAULT false,
  dnd_status BOOLEAN DEFAULT false,
  mur_status BOOLEAN DEFAULT false;
```

### 2.2 Nuove Tabelle

```sql
-- room_status_history (audit trail)
CREATE TABLE room_status_history (
  id SERIAL PRIMARY KEY,
  room_id INTEGER REFERENCES rooms(id),
  field_changed VARCHAR(50),
  old_value TEXT,
  new_value TEXT,
  changed_by INTEGER REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW()
);

-- room_access_codes (codici PIN)
CREATE TABLE room_access_codes (
  id SERIAL PRIMARY KEY,
  room_id INTEGER REFERENCES rooms(id),
  reservation_id INTEGER REFERENCES reservations(id),
  code_type VARCHAR(20), -- 'pin', 'rfid', 'ble'
  code_value VARCHAR(100),
  role VARCHAR(20), -- 'guest', 'staff'
  valid_from TIMESTAMP,
  valid_until TIMESTAMP,
  created_by INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT true
);

-- room_access_log (log accessi)
CREATE TABLE room_access_log (
  id SERIAL PRIMARY KEY,
  room_id INTEGER REFERENCES rooms(id),
  event_type VARCHAR(50), -- door-open, door-close, etc.
  code_id INTEGER REFERENCES room_access_codes(id),
  timestamp TIMESTAMP DEFAULT NOW(),
  metadata JSONB
);
```

### 2.3 API Endpoints

```
ROOM MANAGER API:

GET  /api/room-manager/rooms
GET  /api/room-manager/rooms/{id}
PUT  /api/room-manager/rooms/{id}/status
PUT  /api/room-manager/rooms/{id}/housekeeping
GET  /api/room-manager/rooms/{id}/history

ACCESS API:
GET  /api/room-manager/access/codes
POST /api/room-manager/access/codes
DELETE /api/room-manager/access/codes/{id}
GET  /api/room-manager/access/log

HVAC API:
GET  /api/room-manager/hvac/settings
PUT  /api/room-manager/hvac/settings/{room_id}
GET  /api/room-manager/hvac/status

ACTIVITY LOG API:
GET  /api/room-manager/activity
GET  /api/room-manager/activity/stats
```

---

## FASE 3: MVP FRONTEND

### 3.1 Room Grid (Vista Principale)

```
DESIGN:
┌─────────────────────────────────────────────────┐
│  ROOM MANAGER                    [Filters] [+]  │
├─────────────────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │ 101 │ │ 102 │ │ 103 │ │ 104 │ │ 105 │      │
│  │ 🟢  │ │ 🟡  │ │ 🔴  │ │ 🟢  │ │ ⚫  │      │
│  │ C/I │ │ C/O │ │ OCC │ │ VAC │ │ OOO │      │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │ 201 │ │ 202 │ │ 203 │ │ 204 │ │ 205 │      │
│  │ ... │ │ ... │ │ ... │ │ ... │ │ ... │      │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │
└─────────────────────────────────────────────────┘

STATI COLORE:
🟢 Verde = Clean + Vacant
🟡 Giallo = Dirty / Needs cleaning
🔴 Rosso = Occupied
⚫ Grigio = OOO/OOS
🔵 Blu = Check-in today
🟠 Arancio = Check-out today
```

### 3.2 Room Card (Dettaglio)

```
DESIGN:
┌─────────────────────────────────────────────────┐
│  ROOM 105 - Suite Deluxe            [X]        │
├─────────────────────────────────────────────────┤
│  STATUS: Occupied                               │
│  HOUSEKEEPING: Clean ✅                         │
│  GUEST: Mario Rossi (Check-out: 16 Jan)        │
├─────────────────────────────────────────────────┤
│  🌡️ HVAC                                       │
│  ├── Current: 21.5°C                           │
│  ├── Target: 22°C                              │
│  └── Mode: Comfort                             │
├─────────────────────────────────────────────────┤
│  🚪 ACCESS                                      │
│  ├── Door: Closed                              │
│  ├── Last access: 14:32                        │
│  └── Active codes: 2                           │
├─────────────────────────────────────────────────┤
│  📋 SENSORS                                     │
│  ├── Presence: Yes                             │
│  ├── DND: Off                                  │
│  └── MUR: Off                                  │
├─────────────────────────────────────────────────┤
│  [Set Dirty] [Generate Code] [View History]    │
└─────────────────────────────────────────────────┘
```

### 3.3 Activity Log

```
DESIGN:
┌─────────────────────────────────────────────────┐
│  ACTIVITY LOG                    [Filters]      │
├─────────────────────────────────────────────────┤
│  [Access] [Keys] [Status] [HVAC]               │
├─────────────────────────────────────────────────┤
│  14:32:15 │ 105 │ door-open │ Mario Rossi      │
│  14:32:18 │ 105 │ door-close │                 │
│  14:30:00 │ 203 │ status → dirty │ Maria B.   │
│  14:28:45 │ 301 │ code created │ Reception    │
│  14:25:00 │ 102 │ hvac → 22°C │ Auto          │
│  ...                                           │
├─────────────────────────────────────────────────┤
│  Showing 1-25 of 12,345 │ < 1 2 3 ... 494 >   │
└─────────────────────────────────────────────────┘
```

---

## FASE 4: AUTOMAZIONI SMART

### 4.1 Trigger Automatici

```
AUTOMAZIONI:

1. CHECK-OUT → DIRTY
   Quando: reservation.status = 'checked_out'
   Azione: room.housekeeping_status = 'dirty'

2. PRESENZA → HVAC
   Quando: occupancy_sensor = false per 30 min
   Azione: hvac_mode = 'eco' (risparmio)

3. CHECK-IN → CODICE
   Quando: reservation.status = 'confirmed' + day before
   Azione: Genera codice PIN automatico

4. FINESTRA APERTA → HVAC OFF
   Quando: window_sensor = 'open'
   Azione: hvac_mode = 'off' (risparmio)

5. DND → SKIP HOUSEKEEPING
   Quando: dnd_status = true
   Azione: Salta dalla lista pulizie
```

### 4.2 AI Suggestions (Futuro)

```
SUGGERIMENTI AI:

1. "Camera 105 non pulita da 3 giorni - priorità alta"
2. "Pattern: ospite 203 esce sempre alle 9:00 - programma pulizia"
3. "Anomalia: porta 301 aperta da 2 ore senza presenza"
4. "Risparmio energetico: 15% questo mese grazie a automazioni"
```

---

## FASE 5: INTEGRAZIONE HARDWARE (Futuro)

### 5.1 VDA MODBUS Wrapper

```
OBIETTIVO: Usare hardware VDA esistente (112 dispositivi!)

COMPONENTI:
├── modbus_client.py - Client MODBUS
├── vda_adapter.py - Traduttore VDA → Miracollo
└── device_registry.py - Registro dispositivi

FUNZIONALITA':
├── Leggere stati sensori
├── Controllare HVAC
├── Ricevere eventi porte
└── Sincronizzare in tempo reale
```

### 5.2 Serrature Smart (Futuro)

```
INTEGRAZIONI POSSIBILI:
├── Salto (API cloud)
├── ASSA ABLOY (Visionline)
├── Dormakaba
└── TTLock (economico)
```

---

## TIMELINE (Flessibile!)

```
"Non importa il TEMPO - abbiamo TEMPO!"
"Una cosa alla volta, fino al 100000%!"

FASE 0: Studio e Ricerca
├── VDA: ✅ COMPLETATO (Sess 210-212)
├── Big Players: ⏳ (Sess 212+)
└── Decisioni: ⏳

FASE 1: Architettura
├── Schema DB: ⏳
├── API design: ⏳
└── Frontend wireframe: ⏳

FASE 2: MVP Backend
├── Migration: ⏳
├── Services: ⏳
└── API: ⏳

FASE 3: MVP Frontend
├── Room Grid: ⏳
├── Room Card: ⏳
└── Activity Log: ⏳

FASE 4: Automazioni
├── Trigger base: ⏳
└── AI suggestions: ⏳

FASE 5: Hardware (Futuro)
├── VDA MODBUS: ⏳
└── Serrature smart: ⏳
```

---

## PRINCIPI GUIDA

```
+================================================================+
|                                                                |
|   1. SMART > FUNZIONALE                                        |
|      VDA funziona, noi PENSIAMO                                |
|                                                                |
|   2. FLUIDO > RIGIDO                                           |
|      VDA ha form lunghi, noi FLOW naturale                     |
|                                                                |
|   3. BELLO > TECNICO                                           |
|      VDA sembra software industriale, noi DESIGN moderno       |
|                                                                |
|   4. AI-FIRST                                                  |
|      Suggerimenti, automazioni, predizioni                     |
|                                                                |
|   5. MOBILE-READY                                              |
|      Housekeeping da smartphone                                |
|                                                                |
+================================================================+
```

---

*"Non copiamo VDA - facciamo PIU' SMART, FLUIDO, BELLO!"*
*"Una cosa alla volta, fino al 100000%!"*
*"Ultrapassar os próprios limites!"*

*Roadmap creata: 14 Gennaio 2026 - Sessione 212*
