# ANALISI PMS ESISTENTE - Miracollo Room Manager

**Data:** 12 Gennaio 2026  
**Analista:** Cervella Ingegnera  
**Obiettivo:** Capire cosa esiste GIA' nel PMS Miracollo per evitare duplicazioni nel modulo Room Manager

---

## EXECUTIVE SUMMARY

**Stato:** ⚠️ SOVRAPPOSIZIONI CRITICHE TROVATE

Miracollo ha GIA' funzionalita housekeeping di base, ma sparse in diversi moduli. Il nuovo Room Manager (creato oggi) introduce DUPLICAZIONI con il sistema esistente.

**Health Score:** 5/10 - Servono decisioni architetturali chiare

---

## 1. BACKEND - ROUTER ESISTENTI

### 1.1 Router Housekeeping (`routers/housekeeping.py`)

**GIA' ESISTE!** 103 righe di codice funzionante.

**Endpoint:**
- `PATCH /api/rooms/{room_id}/status` - Aggiorna stato housekeeping
- `GET /api/housekeeping/{hotel_code}` - Vista rapida housekeeping

**Stati supportati:**
```python
VALID_HOUSEKEEPING_STATUS = ['clean', 'dirty', 'cleaning', 'maintenance', 'inspected']
```

**Cosa fa:**
- Aggiorna `housekeeping_status` nella tabella `rooms`
- Traccia chi e quando ha aggiornato (`housekeeping_updated_by`, `housekeeping_updated_at`)
- Calcola statistiche per stato

**DUPLICAZIONE:** Il nuovo Room Manager ha endpoint identici!

---

### 1.2 Router Planning (`routers/planning.py`)

**IL CUORE DEL SISTEMA!** 723+ righe di codice.

**Endpoint rilevanti per camere:**
- `GET /api/planning/{hotel_code}` - Ottiene camere con stato housekeeping
- `GET /api/rooms/{hotel_code}` - Lista camere fisiche
- `GET /api/planning/{hotel_code}/available-rooms` - Smart Room Selection

**Integrazione camere:**
```sql
SELECT 
    r.id, r.room_number, r.floor,
    r.housekeeping_status,  -- ⬅️ GIA' INTEGRATO!
    rt.code, rt.name
FROM rooms r
JOIN room_types rt ON r.room_type_id = rt.id
```

**Nota critica:** Planning GIA' mostra housekeeping_status per ogni camera!

---

### 1.3 Router Room Manager (NUOVO!)

**Path:** `routers/room_manager/router.py`  
**Creato:** 12 Gennaio 2026  
**Status:** 278 righe, placeholder `hotel_id = 1`

**Endpoint:**
- `GET /api/room-manager/rooms` - Lista camere
- `PUT /api/room-manager/rooms/{room_id}/status` - Aggiorna stato
- `GET /api/room-manager/housekeeping` - Dashboard housekeeping
- `POST /api/room-manager/housekeeping` - Crea task

**⚠️ PROBLEMA:** Duplica endpoint gia esistenti in `housekeeping.py`!

---

## 2. BACKEND - SERVICES ESISTENTI

**File trovati:** 45 services in `backend/services/`

**Nessun servizio specifico per housekeeping.**

Il nuovo Room Manager ha creato:
- `RoomService` (services.py)
- `HousekeepingService` (services.py)

**RACCOMANDAZIONE:** Questi services sono NUOVI e utili. Centralizzano logica business che prima era sparsa nei router.

---

## 3. FRONTEND - PAGINE ESISTENTI

### 3.1 Planning.html

**IL CUORE VISUALE DEL SISTEMA**

**Features:**
- Vista planning visuale camere
- Quick stats widget con icona housekeeping
- Click su icona housekeeping → pannello camere da pulire

**Codice rilevante:**
```html
<div class="stat-item housekeeping" title="Camere da pulire - Click per lista">
    <svg class="stat-icon"><!-- Icona scopa/pulizia --></svg>
    <span class="stat-value" id="stat-housekeeping">-</span>
</div>
```

**DUPLICAZIONE POTENZIALE:** Room Manager ha pagina separata per housekeeping!

---

### 3.2 Frontdesk.html

**Focus:** Check-in/Check-out di oggi

**Feature housekeeping:**
- Mostra stato camere per arrivi
- Permette cambio stato camera prima check-in

**NON duplica funzionalita housekeeping avanzate.**

---

### 3.3 Room-Manager.html (NUOVO!)

**Creato:** 12 Gennaio 2026  
**Status:** Pagina completa con 3 viste (griglia, lista, piano)

**Features:**
- Vista camere con stato
- Filtri per stato housekeeping
- Toggle tra diverse visualizzazioni

**⚠️ SOVRAPPOSIZIONE:** Planning.html GIA' mostra camere + stato!

---

## 4. DATABASE - SCHEMA ATTUALE

### 4.1 Tabella `rooms`

**Schema base (da schema.sql):**
```sql
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    hotel_id INTEGER NOT NULL,
    room_type_id INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    floor INTEGER,
    notes TEXT,
    
    -- HOUSEKEEPING (MICRO-07 + Migration 001)
    housekeeping_status TEXT DEFAULT 'clean',
    housekeeping_updated_at TEXT,
    housekeeping_updated_by TEXT,
    
    is_active INTEGER DEFAULT 1,
    created_at TEXT,
    updated_at TEXT
);
```

**Migration 036 (Room Manager) AGGIUNGE:**
```sql
ALTER TABLE rooms ADD COLUMN status TEXT DEFAULT 'vacant_clean';
```

**⚠️ PROBLEMA CRITICO:** Ora abbiamo DUE campi stato!
- `housekeeping_status` (vecchio): 'clean', 'dirty', 'cleaning', 'maintenance', 'inspected'
- `status` (nuovo): 'vacant_clean', 'vacant_dirty', 'occupied', 'checkout', 'maintenance', 'out_of_order'

**SOVRAPPOSIZIONE:**
- Entrambi hanno 'maintenance'
- 'clean' vs 'vacant_clean'
- 'dirty' vs 'vacant_dirty'

---

### 4.2 Tabella `room_types`

**GIA' ESISTE!** Schema completo:
```sql
CREATE TABLE room_types (
    id INTEGER PRIMARY KEY,
    hotel_id INTEGER NOT NULL,
    code TEXT NOT NULL,  -- 'ESSENTIA', 'SILVAE'
    name TEXT NOT NULL,
    base_occupancy INTEGER DEFAULT 2,
    max_occupancy INTEGER DEFAULT 4,
    ...
);
```

**Room Manager NON duplica.** ✅

---

### 4.3 Tabella `bookings`

**GIA' ESISTE!** Integrazione completa:
- `check_in_date`, `check_out_date`
- `status` ('confirmed', 'checked_in', 'checked_out', 'cancelled', 'no_show')
- Collegata a `booking_rooms` per assegnazione camera

**Room Manager NON duplica.** ✅

---

### 4.4 NUOVE TABELLE (Migration 036)

**1. `housekeeping_tasks`**
```sql
CREATE TABLE housekeeping_tasks (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL,
    task_type TEXT NOT NULL,  -- checkout_clean, stayover_clean, deep_clean
    status TEXT DEFAULT 'pending',
    assigned_to TEXT,
    due_date TEXT,
    completed_at TEXT,
    notes TEXT,
    ...
);
```

**NOVITA'!** Non esisteva prima. ✅ UTILE!

---

**2. `maintenance_requests`**
```sql
CREATE TABLE maintenance_requests (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'open',
    assigned_to TEXT,
    ...
);
```

**NOVITA'!** Non esisteva prima. ✅ UTILE!

---

**3. `room_status_history`**
```sql
CREATE TABLE room_status_history (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL,
    old_status TEXT,
    new_status TEXT NOT NULL,
    changed_by TEXT,
    created_at TEXT
);
```

**NOVITA'!** Audit trail. ✅ MOLTO UTILE!

---

## 5. INTEGRAZIONI ESISTENTI

### 5.1 Planning ↔ Camere

**GIA' INTEGRATO perfettamente:**

```javascript
// Planning visualizza camere con stato housekeeping
rooms.forEach(room => {
    const housekeepingClass = getHousekeepingClass(room.housekeeping_status);
    // Mostra indicatore visivo
});
```

**Room Manager non aggiunge valore qui.** ❌

---

### 5.2 Bookings ↔ Camere

**GIA' INTEGRATO tramite:**
- `booking_rooms.room_id` → `rooms.id`
- `room_assignments` (per cambio camera durante soggiorno)

**Planning API include:**
```sql
LEFT JOIN booking_rooms br ON b.id = br.booking_id
WHERE b.status NOT IN ('cancelled', 'no_show')
```

**Smart Room Selection** esclude camere occupate. ✅

---

### 5.3 Check-in/Check-out ↔ Stato Camera

**COLLEGAMENTO MANCANTE!**

Attualmente:
- Check-out → stato booking diventa 'checked_out'
- MA: `housekeeping_status` NON cambia automaticamente a 'dirty'!

**RACCOMANDAZIONE:** Servono trigger o logica applicativa!

---

## 6. COSA ESISTE GIA'

| Feature | Dove | Completezza |
|---------|------|-------------|
| **Lista camere con tipo** | `planning.py`, `planning.html` | ✅ 100% |
| **Stato housekeeping base** | `housekeeping.py`, tabella `rooms` | ✅ 90% |
| **Vista camere nel planning** | `planning.html` | ✅ 100% |
| **Cambio stato housekeeping** | `housekeeping.py` | ✅ 80% |
| **Smart Room Selection** | `planning.py` | ✅ 100% |
| **Floor/piano visualizzazione** | `rooms.floor` | ⚠️ 50% (dato esiste, vista no) |

---

## 7. COSA MANCA

| Feature | Esiste? | Creato da Room Manager? |
|---------|---------|-------------------------|
| **Task housekeeping** | ❌ | ✅ Tabella + API |
| **Assegnazione task a personale** | ❌ | ✅ Campo `assigned_to` |
| **Manutenzione camere** | ❌ | ✅ Tabella `maintenance_requests` |
| **Audit trail stati** | ❌ | ✅ Tabella `room_status_history` |
| **Vista per piano (floor plan)** | ⚠️ Parziale | ✅ Endpoint `/floor-plan` |
| **Dashboard housekeeping** | ❌ | ✅ Endpoint + HTML |

---

## 8. DOVE SI COLLEGA ROOM MANAGER

### 8.1 INTEGRAZIONE NATURALE

**Room Manager DOVREBBE:**
1. **Estendere Planning** - Non sostituirlo
2. **Aggiungere task layer** - Sopra stato semplice
3. **Fornire dashboard housekeeping** - Vista dedicata per governanti

**ARCHITETTURA PROPOSTA:**
```
+------------------+
|   PLANNING       |  ← Vista generale (receptionist)
|   (esistente)    |
+------------------+
        ↓
+------------------+
|  ROOM MANAGER    |  ← Vista specializzata (governante)
|   (nuovo)        |
+------------------+
        ↓
+------------------+
| HOUSEKEEPING API |  ← Logica unificata
|   (consolidare)  |
+------------------+
```

---

### 8.2 UNIFICAZIONE STATI

**PROBLEMA ATTUALE:**
- `rooms.housekeeping_status` (vecchio)
- `rooms.status` (nuovo)

**SOLUZIONE A:** Mantenere solo `status`, mappare vecchi endpoint
```sql
-- Deprecare housekeeping_status
-- Tutti endpoint usano rooms.status
```

**SOLUZIONE B:** Mantenere separati con semantica chiara
```sql
-- housekeeping_status = stato PULIZIA (clean, dirty, cleaning)
-- status = stato OPERATIVO (vacant, occupied, maintenance, ooo)
```

**RACCOMANDAZIONE:** Soluzione A (semplifica)

---

## 9. RACCOMANDAZIONI ARCHITETTURALI

### 9.1 EVITARE DUPLICAZIONI

**UNIFICARE ENDPOINT:**

| Attuale | Duplicato | Azione |
|---------|-----------|--------|
| `PATCH /api/rooms/{id}/status` | `PUT /api/room-manager/rooms/{id}/status` | ❌ Rimuovere nuovo |
| `GET /api/housekeeping/{hotel}` | `GET /api/room-manager/housekeeping` | ⚠️ Consolidare |

**PROPOSTA:** Router unico `/api/housekeeping` con:
- Endpoint legacy (mantenere per compatibilita)
- Nuovi endpoint con task/maintenance
- Services centralizzati

---

### 9.2 LAYER ARCHITETTURALE

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │
├─────────────────┬───────────────────────┤
│  planning.html  │  room-manager.html    │  ← Viste diverse
│  (receptionist) │  (governante)         │
└─────────────────┴───────────────────────┘
         ↓                 ↓
┌─────────────────────────────────────────┐
│           API LAYER (Router)            │
├─────────────────────────────────────────┤
│  /api/housekeeping  (UNIFICATO)         │  ← Un solo router
│  - GET /rooms (con stato)               │
│  - PATCH /rooms/{id}/status             │
│  - GET /tasks                           │
│  - POST /tasks                          │
│  - GET /maintenance                     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│         SERVICE LAYER (NEW!)            │
├─────────────────────────────────────────┤
│  RoomService                            │  ← NUOVO! Utile!
│  HousekeepingService                    │  ← NUOVO! Utile!
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│          DATA LAYER                     │
├─────────────────────────────────────────┤
│  rooms (con status unificato)           │
│  housekeeping_tasks (NUOVO!)            │  ← Valore aggiunto!
│  maintenance_requests (NUOVO!)          │  ← Valore aggiunto!
│  room_status_history (NUOVO!)           │  ← Audit trail!
└─────────────────────────────────────────┘
```

---

### 9.3 MIGRAZIONE SICURA

**STEP 1:** Unificare stati (decidere A o B)
**STEP 2:** Consolidare router housekeeping
**STEP 3:** Mantenere planning.html come e
**STEP 4:** Room-manager.html per vista governante
**STEP 5:** Aggiungere trigger check-out → dirty

**PRIORITA:**
1. ⚡ CRITICO: Decisione su `status` vs `housekeeping_status`
2. 🔥 ALTO: Consolidare endpoint duplicati
3. ⚠️ MEDIO: Collegare check-out a cambio stato
4. 📝 BASSO: UI room-manager.html

---

## 10. VALORE AGGIUNTO ROOM MANAGER

**COSA PORTA DI NUOVO:**

✅ **Task System** - Gestione task housekeeping strutturati  
✅ **Assignment** - Assegnazione task a personale  
✅ **Maintenance Tracking** - Sistema richieste manutenzione  
✅ **Audit Trail** - Storico cambi stato  
✅ **Services Layer** - Logica business centralizzata  
✅ **Dashboard Housekeeping** - Vista dedicata governante  

**COSA DUPLICA:**

❌ Cambio stato camera (gia in housekeeping.py)  
❌ Vista camere (gia in planning.html)  
❌ Lista camere con stato (gia in planning API)  

---

## 11. DECISIONI ARCHITETTURALI RICHIESTE

### DECISIONE 1: Stati Camera

**Opzione A:** Un solo campo `status` (semplice)
- Rimuovere `housekeeping_status`
- Mappare endpoint legacy
- Migrare dati esistenti

**Opzione B:** Due campi separati (complesso ma semantico)
- `status` = stato operativo (vacant, occupied, ooo)
- `housekeeping_status` = stato pulizia (clean, dirty, cleaning)

**RACCOMANDAZIONE:** Opzione A

---

### DECISIONE 2: Router

**Opzione A:** Consolidare tutto in `/api/housekeeping`
- Mantenere endpoint legacy per compatibilita
- Aggiungere nuovi endpoint task/maintenance
- Un solo router ben organizzato

**Opzione B:** Mantenere `/api/room-manager` separato
- Due router paralleli
- Planning usa housekeeping.py
- Room Manager usa room_manager/router.py

**RACCOMANDAZIONE:** Opzione A

---

### DECISIONE 3: Frontend

**Opzione A:** Unificare in planning.html
- Aggiungere tab "Housekeeping"
- Mantenere una sola vista

**Opzione B:** Due pagine separate
- planning.html per receptionist
- room-manager.html per governante

**RACCOMANDAZIONE:** Opzione B (diverse user persona)

---

## 12. PIANO DI CONSOLIDAMENTO

**FASE 1: UNIFICAZIONE BACKEND (Priorita ALTA)**

1. Decidere strategia stati (A o B)
2. Creare `routers/housekeeping_v2.py` consolidato
3. Deprecare endpoint duplicati
4. Migrare Planning a usare nuovi endpoint

**FASE 2: SERVICES LAYER (Priorita MEDIA)**

1. Mantenere `RoomService` e `HousekeepingService`
2. Refactorare vecchi router per usare services
3. Centralizzare logica business

**FASE 3: TRIGGER & AUTOMATION (Priorita MEDIA)**

1. Trigger check-out → dirty automatico
2. Trigger check-in → verifica clean
3. Auto-creazione task dopo check-out

**FASE 4: FRONTEND (Priorita BASSA)**

1. Room-manager.html per governanti
2. Planning.html rimane per receptionist
3. Collegare API unificate

---

## 13. RISCHI SE NON CONSOLIDATO

⚠️ **RISCHIO 1: Incoerenza Dati**
- Due sistemi di stato → confusione
- Planning mostra `housekeeping_status`
- Room Manager usa `status`
- Quale e la verita?

⚠️ **RISCHIO 2: Manutenzione Duplicata**
- Stesso bug da fixare in 2 posti
- Stesso endpoint da testare 2 volte
- Technical debt cresce

⚠️ **RISCHIO 3: Performance**
- Due query per stesso dato
- Frontend deve scegliere quale endpoint usare
- Cache invalidation complicata

⚠️ **RISCHIO 4: Developer Confusion**
- Quale endpoint usare?
- Quale campo leggere?
- Documentazione contraddittoria

---

## CONCLUSIONE

**STATUS ATTUALE:**
- ✅ Miracollo ha GIA' housekeeping di base funzionante
- ✅ Room Manager aggiunge VALORE con task/maintenance
- ❌ Room Manager DUPLICA endpoint esistenti
- ⚠️ Serve CONSOLIDAMENTO architetturale

**NEXT STEPS:**
1. **Decidere** strategia stati (Decisione 1)
2. **Consolidare** router backend (Fase 1)
3. **Mantenere** services layer (utili!)
4. **Verificare** frontend separation (planning vs room-manager)

**TEMPO STIMATO CONSOLIDAMENTO:**
- Fase 1 (backend): 4-6 ore
- Fase 2 (services): 2-3 ore
- Fase 3 (trigger): 2-3 ore
- Fase 4 (frontend): variabile (gia fatto in parte)

**RACCOMANDAZIONE FINALE:**
Non proseguire con duplicazioni. Consolidare PRIMA di continuare sviluppo.

---

**Report compilato da:** Cervella Ingegnera  
**Data:** 12 Gennaio 2026, 09:15  
**Versione:** 1.0.0

*"Il debito tecnico si paga con gli interessi."*
