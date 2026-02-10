# AUDIT PROFONDO - MODULI CORE PMS MIRACOLLO
**Ingegnera**: cervella-ingegnera  
**Data**: 16 Gennaio 2026  
**Path Analizzato**: `/Users/rafapra/Developer/miracollogeminifocus/backend/`

---

## EXECUTIVE SUMMARY

**Health Score**: 7.5/10

**Status**: ✅ SOLIDO - Architettura pulita, poche criticità

**Top 3 Issues**:
1. **CRITICO**: File `planning.py` (722 righe) e `planning_swap.py` (965 righe) - Split urgente
2. **ALTO**: Modulo OSPITI frammentato (guest_auth, guests, guest_checkin separati)
3. **MEDIO**: Alcuni endpoint duplicano logica (bookings vs planning per aggiornamenti)

---

## 1. MODULO PRENOTAZIONI (BOOKINGS)

### Funzionalità ESISTENTI

**Router**: `routers/bookings.py` (521 righe)  
**Model**: `models/booking.py` (118 righe)  
**Services**: `services/booking_utils.py`, `services/booking_conflicts.py`

#### Endpoint API

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/bookings` | GET | Lista prenotazioni con filtri | ✅ COMPLETO |
| `/api/bookings/search` | GET | Ricerca globale (nome, booking#) | ✅ COMPLETO |
| `/api/bookings/{booking_id}` | PUT | Aggiorna booking (room, date, status) | ✅ COMPLETO |
| `/api/bookings/{booking_number}/guests` | GET | Lista ospiti prenotazione | ✅ COMPLETO |
| `/api/bookings/{booking_number}/guests` | POST | Crea e aggiunge ospite | ✅ COMPLETO |
| `/api/bookings/{booking_number}/guests/{guest_id}` | POST | Aggiunge ospite esistente | ✅ COMPLETO |
| `/api/bookings/{booking_number}/guests/{guest_id}` | DELETE | Rimuove ospite | ✅ COMPLETO |
| `/api/bookings/{booking_id}/available-rooms` | GET | Camere disponibili per booking | ✅ COMPLETO |

#### Capabilities

- ✅ CRUD prenotazioni base
- ✅ Ricerca full-text (nome ospite, booking number)
- ✅ Gestione multi-ospiti (principale + accompagnatori)
- ✅ Compliance check (campi obbligatori ALLOGGIATI)
- ✅ Validazione modifica bookings passati (BLOCK su date/room)
- ✅ Gestione room_assignments (multi-segmento)
- ✅ Soft delete protection

#### Dipendenze

```
bookings.py
├── core (get_db, logger)
├── models.Booking
├── services.booking_utils (generate_booking_number)
└── Usa: guests, channels, booking_rooms, booking_guests
```

#### Stato Completezza

**95%** - Modulo MATURO

**Gap**:
- ⚠️ Manca endpoint CREATE booking (esiste solo QuickBooking in planning.py)
- ⚠️ Endpoint `/bookings/{booking_id}` (GET singolo) rimosso - logica in legacy

---

## 2. MODULO OSPITI (GUESTS)

### Funzionalità ESISTENTI

**Router Principale**: `routers/guests.py` (225 righe)  
**Router Auth**: `routers/guest_auth.py` (540 righe)  
**Router Checkin**: `routers/guest_checkin/` (5 file)  
**Model**: `models/guest.py` (130 righe)  
**Services**: `services/guest_validation.py`, `services/checkin_service.py`, `services/magic_link_service.py`

#### Endpoint API - Anagrafica Ospiti

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/guests` | GET | Lista ospiti (con search) | ✅ COMPLETO |
| `/api/guests` | POST | Crea ospite | ✅ COMPLETO |
| `/api/guests/{guest_id}` | GET | Dettaglio ospite | ✅ COMPLETO |
| `/api/guests/{guest_id}` | PATCH | Aggiorna ospite (partial) | ✅ COMPLETO |
| `/api/guests/{guest_id}` | DELETE | Soft delete ospite | ✅ COMPLETO |

#### Endpoint API - Guest Authentication (Magic Link)

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/guest/auth/generate` | POST | Genera magic link | ✅ COMPLETO |
| `/api/guest/auth/verify/{token}` | GET | Verifica magic link | ✅ COMPLETO |
| `/api/guest/me` | GET | Info sessione ospite | ✅ COMPLETO |
| `/api/guest/auth/logout` | POST | Invalida sessione | ✅ COMPLETO |

#### Endpoint API - Guest Checkin

**Directory**: `routers/guest_checkin/`

| File | Funzione | Status |
|------|----------|--------|
| `auth.py` | Autenticazione guest | ✅ COMPLETO |
| `steps.py` | Step checkin (dati personali, doc, consensi) | ✅ COMPLETO |
| `complete.py` | Completamento checkin | ✅ COMPLETO |
| `notifications.py` | Notifiche email ospite | ✅ COMPLETO |

#### Capabilities

**Anagrafica**:
- ✅ CRUD ospiti completo
- ✅ Tutti campi COMPLIANCE (ALLOGGIATI, ISTAT, GDPR)
- ✅ Ricerca full-text
- ✅ Soft delete con validazione prenotazioni attive
- ✅ Statistiche ospite (total_stays, loyalty, etc)

**Autenticazione**:
- ✅ Magic Link passwordless
- ✅ Session token JWT
- ✅ Rate limiting IP-based (in-memory)
- ✅ Verifica email opzionale

**Checkin Online**:
- ✅ Multi-step wizard
- ✅ Upload documenti
- ✅ Consensi GDPR
- ✅ Notifiche email automatiche

#### Dipendenze

```
guests.py
├── core (get_db, logger, security)
├── models.Guest
└── Usa: guests table

guest_auth.py
├── core (get_db, logger, config)
├── services.magic_link_service
└── Usa: bookings, guests

guest_checkin/
├── services.checkin_service
├── services.guest_validation
└── Usa: bookings, guests, checkin_sessions
```

#### Stato Completezza

**90%** - Modulo MATURO ma FRAMMENTATO

**Gap**:
- ⚠️ Architettura frammentata (3 router separati per ospiti)
- ⚠️ Rate limiter in-memory (non production-ready, serve Redis)
- ⚠️ Manca integrazione checkin con compliance validation centralizzata

**Raccomandazione**:
- Unificare sotto `/api/guests/` con sub-router
- Migrare rate limit a Redis

---

## 3. MODULO PLANNING

### Funzionalità ESISTENTI

**Router Principale**: `routers/planning.py` (722 righe) ⚠️  
**Router Operazioni**: `routers/planning_ops.py` (650 righe)  
**Router Swap**: `routers/planning_swap.py` (965 righe) ⚠️⚠️  

#### Endpoint API - Planning Core

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/planning/{hotel_code}` | GET | Vista planning completa | ✅ COMPLETO |
| `/api/planning/bookings/{booking_id}/room` | PUT | Cambio camera (drag&drop) | ✅ COMPLETO |
| `/api/planning/bookings/{booking_id}/dates` | PUT | Modifica date (resize) | ✅ COMPLETO |
| `/api/planning/bookings/{booking_id}/notes` | PATCH | Aggiorna note | ✅ COMPLETO |
| `/api/planning/bookings/{booking_id}/cancel` | POST | Cancella prenotazione | ✅ COMPLETO |
| `/api/planning/bookings/quick` | POST | Creazione rapida booking | ✅ COMPLETO |
| `/api/planning/bookings/{booking_id}/check-in` | POST | Check-in | ✅ COMPLETO |
| `/api/planning/bookings/{booking_id}/check-out` | POST | Check-out | ✅ COMPLETO |

#### Endpoint API - Swap Camere (planning_swap.py)

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/planning/swap` | POST | Swap singolo | ✅ COMPLETO |
| `/api/planning/swap/multi` | POST | Swap multiplo (1<->N) | ✅ COMPLETO |
| `/api/planning/swap/segment` | POST | Swap segmento | ✅ COMPLETO |
| `/api/planning/swap/validate` | POST | Valida swap | ✅ COMPLETO |
| `/api/planning/swap/history` | GET | Storico swap | ✅ COMPLETO |
| `/api/planning/swap/undo` | POST | Undo swap | ✅ COMPLETO |

#### Endpoint API - Room Change (planning.py)

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/planning/bookings/{booking_id}/room-change` | POST | Cambio camera durante soggiorno | ✅ COMPLETO |

#### Capabilities

- ✅ Vista planning visuale (camere, prenotazioni, blocchi)
- ✅ Drag & Drop (cambio camera)
- ✅ Resize (modifica date)
- ✅ Quick booking da planning
- ✅ Check-in/Check-out
- ✅ Cancellazione prenotazione
- ✅ Room Change durante soggiorno (MICRO-10)
- ✅ Swap camere (singolo, multiplo, segmento)
- ✅ Validazione conflitti
- ✅ History e Undo
- ✅ Versioning ottimistico

#### Dipendenze

```
planning.py
├── core (get_db, check_and_increment_version, logger)
├── models (Booking models)
├── services.booking_utils
└── Usa: bookings, guests, rooms, booking_rooms, room_assignments, cm_reservations

planning_swap.py
├── services.swap_* (operations, validation, queries, history, transaction)
└── Usa: bookings, booking_rooms, room_assignments
```

#### Stato Completezza

**98%** - Modulo COMPLETISSIMO ma FILE TROPPO GRANDE!

**Gap**:
- 🔴 **CRITICO**: `planning.py` (722 righe) - Split urgente
- 🔴 **CRITICO**: `planning_swap.py` (965 righe) - Split URGENTISSIMO!
- ⚠️ Logica duplicata tra bookings.py e planning.py per aggiornamenti

**Raccomandazione URGENTE**:

**planning.py** → Split in:
- `planning_view.py` (GET planning)
- `planning_booking_ops.py` (quick, check-in/out)
- `planning_booking_updates.py` (room, dates, notes, cancel)
- `planning_room_change.py` (room change durante soggiorno)

**planning_swap.py** → Split in:
- `planning_swap_single.py` (swap singolo)
- `planning_swap_multi.py` (swap multiplo)
- `planning_swap_segment.py` (swap segmento)
- `planning_swap_utils.py` (validate, history, undo)

---

## 4. MODULO CAMERE (ROOMS)

### Funzionalità ESISTENTI

**Router Housekeeping**: `routers/housekeeping.py` (126 righe)  
**Router Blocks**: `routers/blocks.py` (201 righe)  
**Router Room Manager**: `routers/room_manager.py` (Sessione 213)  
**Model**: `models/room.py` (127 righe)  
**Service**: `services/room_manager_service.py` (542 righe)

#### Endpoint API - Housekeeping

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/rooms/{room_id}/status` | PATCH | Aggiorna stato housekeeping | ✅ COMPLETO |
| `/api/housekeeping/{hotel_code}` | GET | Vista housekeeping tutte camere | ✅ COMPLETO |

#### Endpoint API - Room Blocks

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/rooms/{room_id}/blocks` | GET | Lista blocchi camera | ✅ COMPLETO |
| `/api/rooms/{room_id}/blocks` | POST | Crea blocco | ✅ COMPLETO |
| `/api/rooms/{room_id}/blocks/{block_id}` | DELETE | Rimuove blocco | ✅ COMPLETO |
| `/api/blocks/{hotel_code}` | GET | Tutti blocchi hotel | ✅ COMPLETO |

#### Endpoint API - Room Manager (NUOVO - Sessione 213)

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/room-manager/{hotel_code}` | GET | Lista camere con status completo | ✅ COMPLETO |
| `/api/room-manager/{hotel_code}/stats` | GET | Statistiche camere | ✅ COMPLETO |
| `/api/room-manager/{hotel_code}/activity` | GET | Activity log globale | ✅ COMPLETO |
| `/api/room-manager/rooms/{room_id}` | GET | Dettaglio camera | ✅ COMPLETO |
| `/api/room-manager/rooms/{room_id}/status` | PUT | Aggiorna status camera | ✅ COMPLETO |
| `/api/room-manager/rooms/{room_id}/housekeeping` | PUT | Aggiorna housekeeping | ✅ COMPLETO |
| `/api/room-manager/rooms/{room_id}/activity` | GET | Activity log camera | ✅ COMPLETO |

#### Capabilities

**Housekeeping**:
- ✅ Stati: clean, dirty, cleaning, maintenance, inspected
- ✅ Tracking chi/quando ha aggiornato
- ✅ Vista globale per governante

**Blocks**:
- ✅ Tipi: maintenance, out_of_service, owner_use, other
- ✅ Validazione prenotazioni esistenti
- ✅ Activity log automatico

**Room Manager (NUOVO)**:
- ✅ Vista camere con status completo
- ✅ Aggiornamento status (available, out_of_service, out_of_order)
- ✅ Activity log automatico per ogni cambio
- ✅ Statistiche per dashboard
- ✅ Occupancy check oggi
- ✅ Preparato per VDA (sensori temperatura, presenza, DND, MUR)

#### Dipendenze

```
housekeeping.py
├── core (get_db, logger, VALID_HOUSEKEEPING_STATUS)
├── models.RoomStatusUpdate
├── services.room_manager_service (log_activity)
└── Usa: rooms

blocks.py
├── core (get_db, logger, VALID_BLOCK_TYPES)
├── models.RoomBlockCreate
├── services.room_manager_service (log_activity)
└── Usa: rooms, room_blocks

room_manager_service.py
├── core (get_db, logger)
└── Usa: rooms, v_room_manager_overview, room_activity_log
```

#### Stato Completezza

**85%** - Modulo SOLIDO, APPENA SVILUPPATO (Sessione 213)

**Gap**:
- ✅ Activity log presente e funzionante
- ⚠️ VDA integration pronta ma non implementata (temperature, sensori)
- ⚠️ Manca endpoint batch update housekeeping (per governante)

---

## 5. MODULO HOTEL

### Funzionalità ESISTENTI

**Router**: `routers/hotels.py` (46 righe)  
**Model**: `models/hotel.py` (651 righe nel file del DB schema)

#### Endpoint API

| Endpoint | Metodo | Funzione | Status |
|----------|--------|----------|--------|
| `/api/hotels` | GET | Lista tutti hotel | ✅ COMPLETO |
| `/api/hotels/{hotel_code}` | GET | Dettaglio hotel | ✅ COMPLETO |

#### Capabilities

- ✅ Lista hotel
- ✅ Dettaglio singolo hotel
- ✅ Soft delete support

#### Dipendenze

```
hotels.py
├── core (get_db)
├── models.Hotel
└── Usa: hotels
```

#### Stato Completezza

**50%** - Modulo MINIMALE

**Gap**:
- ❌ Manca CREATE hotel
- ❌ Manca UPDATE hotel
- ❌ Manca DELETE hotel
- ❌ Nessuna gestione configurazioni hotel
- ❌ Nessuna gestione multi-property

**Raccomandazione**:
- Hotel probabilmente gestito via seed/admin
- OK per MVP, espandere se serve multi-property

---

## ANALISI CROSS-MODULE

### Dipendenze tra Moduli

```
PLANNING
  ├─→ BOOKINGS (bookings table)
  ├─→ GUESTS (guests table)
  ├─→ ROOMS (rooms, booking_rooms)
  └─→ HOTEL (hotel_id)

BOOKINGS
  ├─→ GUESTS (guest_id)
  ├─→ ROOMS (room_id via booking_rooms)
  └─→ HOTEL (hotel_id)

GUESTS
  └─→ HOTEL (indiretto via bookings)

ROOMS
  └─→ HOTEL (hotel_id)

HOTEL
  └─→ (nessuna dipendenza)
```

### Duplicazioni Logica

**🔴 CRITICO - Aggiornamento Booking**

| Cosa | Dove |
|------|------|
| PUT booking (room, dates, status) | `bookings.py:168` |
| PUT booking room | `planning.py:???` |
| PUT booking dates | `planning.py:???` |

**Problema**: Stessa logica in 2 posti!

**Soluzione**:
- Centralizzare in `services/booking_service.py`
- Router chiamano service layer

---

## METRICHE CODEBASE

### File Size Analysis

| File | Righe | Severità | Azione |
|------|-------|----------|--------|
| `planning_swap.py` | 965 | 🔴 CRITICO | Split urgente in 4 file |
| `planning.py` | 722 | 🔴 CRITICO | Split urgente in 4 file |
| `planning_ops.py` | 650 | 🟡 ALTO | Valutare split |
| `guest_auth.py` | 540 | 🟡 ALTO | Valutare split |
| `room_manager_service.py` | 542 | 🟢 OK | Service layer legittimo |
| `bookings.py` | 521 | 🟢 OK | Accettabile |

### Qualità Codice

**✅ Punti di Forza**:
- Separazione router/model/service RISPETTATA
- Nomi endpoint REST coerenti
- Logging presente ovunque
- Validazione business logic solida
- Activity log automatico (NUOVO!)
- Versioning ottimistico su planning
- Soft delete ovunque

**⚠️ Punti di Attenzione**:
- File planning troppo grandi
- Duplicazione logica bookings/planning
- Rate limiter in-memory (non scalabile)
- Guest module frammentato

---

## RACCOMANDAZIONI PRIORITIZZATE

### 1. CRITICO - Split Planning Files

**File da splittare SUBITO**:

**planning_swap.py** (965 righe) →
```
planning_swap_single.py     (swap singolo)
planning_swap_multi.py      (swap multiplo)  
planning_swap_segment.py    (swap segmento)
planning_swap_utils.py      (validate, history, undo)
```

**planning.py** (722 righe) →
```
planning_view.py            (GET planning)
planning_booking_ops.py     (quick, check-in/out)
planning_booking_updates.py (room, dates, notes, cancel)
planning_room_change.py     (room change)
```

**Effort**: 2-3 giorni  
**Impact**: 🔥🔥🔥 Manutenibilità +50%

---

### 2. ALTO - Unifica Guest Module

**Problema**: Guest logic in 3 posti separati

**Soluzione**:
```
/api/guests/
├── /                    (CRUD anagrafica)
├── /auth/               (magic link)
└── /checkin/            (online checkin)
```

**Effort**: 1 giorno  
**Impact**: 🔥🔥 Coerenza architetturale

---

### 3. ALTO - Centralizza Booking Updates

**Problema**: Duplicazione logica bookings.py vs planning.py

**Soluzione**:
```python
# services/booking_service.py
async def update_booking_room(booking_id, room_id):
    """Usato da bookings.py E planning.py"""
    pass

async def update_booking_dates(booking_id, check_in, check_out):
    """Usato da bookings.py E planning.py"""
    pass
```

**Effort**: 1 giorno  
**Impact**: 🔥 DRY principle

---

### 4. MEDIO - Migra Rate Limiter a Redis

**Problema**: In-memory rate limit non funziona con multi-process

**Soluzione**: Usare Redis per rate limiting

**Effort**: 4 ore  
**Impact**: Production-ready

---

### 5. BASSO - Espandi Hotel Module

**Solo se serve multi-property**

**Effort**: 2 giorni  
**Impact**: Futuro

---

## TECHNICAL DEBT TROVATO

### TODO/FIXME

```bash
# Nessun TODO/FIXME critico trovato nei file CORE!
# Ottimo lavoro di pulizia recente
```

### Codice Commentato

**Minimo** - Solo commenti di documentazione

---

## CONCLUSIONE

### Health Score Breakdown

| Aspetto | Score | Note |
|---------|-------|------|
| **Architettura** | 8/10 | Pulita, ben separata router/model/service |
| **File Size** | 5/10 | 2 file CRITICI troppo grandi |
| **Duplicazione** | 7/10 | Poca, ma presente in bookings update |
| **Naming** | 9/10 | Coerente e chiaro |
| **Documentation** | 8/10 | Buoni docstring |
| **Testing** | ?/10 | Non analizzato in questo audit |

**TOTALE**: 7.5/10

---

### Prossimi Step Raccomandati

1. ✅ **SUBITO**: Split `planning_swap.py` (965 righe)
2. ✅ **SUBITO**: Split `planning.py` (722 righe)
3. ⏰ **1 SETTIMANA**: Unifica Guest module sotto `/api/guests/`
4. ⏰ **1 SETTIMANA**: Centralizza booking updates in service layer
5. 🔮 **FUTURO**: Redis rate limiter

---

**Fine Audit - cervella-ingegnera**  
*"Il progetto si MIGLIORA da solo quando lo analizziamo!"*
