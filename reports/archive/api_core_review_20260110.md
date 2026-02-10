# API Core Review - Miracollo PMS
## Data: 10 Gennaio 2026
## Reviewer: Cervella Guardiana Ops

---

# SCORE GENERALE: 7.5/10

Le API Core di Miracollo sono ben strutturate e mostrano buone pratiche in molte aree.
Ci sono alcuni problemi critici da risolvere, ma la base e solida.

---

# 1. BUG CRITICI (da fixare SUBITO)

## CRITICO-1: Mancanza Transazioni Atomiche in create_booking (public/booking.py)

**File:** `/backend/routers/public/booking.py`
**Linee:** 185-213

**Problema:**
La creazione di una prenotazione pubblica esegue:
1. INSERT in `bookings` (linea 185)
2. `conn.commit()` (linea 213)
3. INSERT in `booking_rooms` (linea 203)
4. `conn.commit()` (linea 213 - duplicate!)

Se il secondo INSERT fallisce DOPO il primo commit, rimane una prenotazione orfana
senza booking_rooms. Non c'e rollback possibile.

**Fix Suggerito:**
```python
# Rimuovere il primo conn.commit() alla linea 213
# Usare un unico commit alla fine dopo TUTTI gli insert
cursor = conn.execute("INSERT INTO bookings ...")
booking_id = cursor.lastrowid
cursor = conn.execute("INSERT INTO booking_rooms ...")
conn.commit()  # Un solo commit atomico
```

**Severita:** CRITICA - Possibile corruzione dati in produzione

---

## CRITICO-2: Race Condition in generate_booking_number (booking_utils.py)

**File:** `/backend/services/booking_utils.py`
**Linee:** 39-65

**Problema:**
La generazione del booking_number usa MAX + 1, ma non c'e lock o transazione.
Se due richieste arrivano contemporaneamente:
- Request A legge MAX = 2025-000042
- Request B legge MAX = 2025-000042
- Entrambe generano 2025-000043 (DUPLICATO!)

**Fix Suggerito:**
```python
def generate_booking_number(conn) -> str:
    year = datetime.now().year
    # Usare INSERT con sequence o lock
    # Oppure usare transaction serializable
    conn.execute("BEGIN IMMEDIATE")  # Lock esclusivo
    cursor = conn.execute("SELECT MAX...")
    ...
    # Il commit del chiamante rilascia il lock
```

**Alternativa:** Usare UUID o sequence nel DB.

**Severita:** CRITICA - Possibili booking duplicati

---

## CRITICO-3: Bare except nasconde errori (booking_detail.py)

**File:** `/backend/routers/booking_detail.py`
**Linee:** 202, 211, 237, 251

**Problema:**
```python
try:
    cursor = conn.execute(...)
except:
    pass  # SILENZIOSAMENTE IGNORA TUTTO!
```

Questi `except:` silenziano TUTTI gli errori, inclusi:
- Errori di sintassi SQL
- Problemi di connessione DB
- Errori di memoria

**Fix Suggerito:**
```python
try:
    cursor = conn.execute(...)
except sqlite3.OperationalError as e:
    # Tabella non esiste, OK
    logger.debug(f"Table not found: {e}")
except Exception as e:
    # Log altri errori per debugging
    logger.warning(f"Unexpected error: {e}")
```

**Severita:** CRITICA per debugging - nasconde bug reali

---

# 2. BUG ALTI (importanti)

## ALTO-1: N+1 Query Pattern in arrivals/departures

**File:** `/backend/routers/planning_ops.py`
**Linee:** 494-538

**Problema:**
Per ogni arrivo nel loop:
```python
for row in rows:
    compliance = validate_guest_compliance(conn, booking_id)  # QUERY PER OGNI ROW!
```

Con 50 arrivi = 50 query extra!

**Fix Suggerito:**
Pre-caricare i dati compliance in batch:
```python
# Prima del loop
guest_ids = [row['guest_id'] for row in rows]
compliance_data = batch_validate_compliance(conn, guest_ids)
# Nel loop
compliance = compliance_data.get(row['guest_id'])
```

**Impatto:** Performance degradata con molti arrivi

---

## ALTO-2: Input Validation Mancante su hotel_code

**File:** `/backend/routers/bookings.py`
**Linee:** 37, 77

**Problema:**
`hotel_code.upper()` viene chiamato direttamente senza validazione.
Se `hotel_code` e None o vuoto, `.upper()` fallisce.

**Fix Suggerito:**
```python
if not hotel_code or not hotel_code.strip():
    raise HTTPException(400, "hotel_code e obbligatorio")
hotel_code = hotel_code.upper().strip()
```

---

## ALTO-3: Possibile Division by Zero in rate calculation

**File:** `/backend/routers/planning.py`
**Linea:** 459

**Problema:**
```python
rate_per_night = round(total_from_rates / nights, 2)
```

Se `nights = 0` (anche se validato prima), crash!

**File:** `/backend/routers/rateboard.py`
**Linea:** 221 (stesso pattern)

**Fix Suggerito:**
```python
rate_per_night = round(total_from_rates / max(nights, 1), 2)
```

---

## ALTO-4: Missing Index Warning (potenziale)

**Problema identificato nelle query:**
Le seguenti query usano frequentemente campi che potrebbero non avere indici:

- `booking_number` in ricerche (usato in WHERE senza LIKE)
- `check_in_date` e `check_out_date` range queries
- `room_id` in booking_rooms JOIN

**Raccomandazione:**
Verificare che esistano indici su:
```sql
CREATE INDEX IF NOT EXISTS idx_bookings_number ON bookings(booking_number);
CREATE INDEX IF NOT EXISTS idx_bookings_dates ON bookings(check_in_date, check_out_date);
CREATE INDEX IF NOT EXISTS idx_booking_rooms_room ON booking_rooms(room_id);
```

---

# 3. BUG MEDI/BASSI (miglioramenti)

## MEDIO-1: Magic Numbers sparsi

**File:** Vari
**Esempi:**
- `base = 100` (rateboard.py:165)
- `total_rooms = 19` (rateboard.py:312, 371)
- `meal_plan_id = 2` (planning.py:548)

**Fix:** Usare costanti o config.

---

## MEDIO-2: Logging Inconsistente

Alcuni endpoint loggano con emoji, altri no.
Alcuni usano `logger.info`, altri `logger.warning` per stessi scenari.

**Raccomandazione:** Standardizzare formato log.

---

## MEDIO-3: Response Model Mancanti

Molti endpoint ritornano `dict` invece di Pydantic models:
```python
return {"success": True, "booking_id": ...}
```

**Raccomandazione:** Definire response models per OpenAPI docs migliori.

---

## BASSO-1: Commenti TODO dimenticati

**File:** `/backend/routers/bookings.py`
**Linea:** 215

```python
# Ricalcola notti se necessario
pass 
```

Il `pass` indica codice incompleto.

---

## BASSO-2: Duplicate Code in GUEST_SELECT_FIELDS

Il campo e definito identico in:
- planning.py (linea 45)
- planning_ops.py (linea 48)

**Fix:** Spostare in modulo condiviso.

---

# 4. COSA VA BENE (Pattern Corretti)

## Sicurezza
- Parametrized queries OVUNQUE (niente SQL injection!)
- Input validation presente per la maggior parte dei campi
- IRON DOME protection per delete booking (planning_ops.py:265-295)
- PAST GUARD per prevenire modifiche a booking concluse

## Transazioni
- `transaction_savepoint` per operazioni swap (eccellente!)
- Context manager `with get_db() as conn` consistente
- Rollback implicito su eccezioni

## Architettura
- Separazione routers/services pulita
- Models Pydantic ben definiti
- Logging presente e generalmente utile
- Error handling con HTTPException consistente
- Optimistic locking con `check_and_increment_version`

## Conflict Detection
- Check room availability ben implementato
- Verifica segmenti, bookings E blocks
- Multi-source conflict check (room_assignments + booking_rooms)

## Sanity Check
- `sanity_check_database()` all'avvio e ottimo!
- Auto-fix per inconsistenze (orfani, overbooking)

---

# 5. RACCOMANDAZIONI PRIORITARIE

## Immediate (prima del prossimo deploy)
1. Fixare transazione atomica in public/booking.py
2. Fixare race condition in generate_booking_number
3. Sostituire bare except con gestione errori specifica

## Breve termine (1-2 settimane)
4. Ottimizzare N+1 query in arrivals/departures
5. Aggiungere indici mancanti
6. Validazione input piu robusta

## Medio termine (1 mese)
7. Response models Pydantic per tutti gli endpoint
8. Standardizzare logging
9. Rifattorizzare costanti magic numbers

---

# VERDETTO FINALE

**Score:** 7.5/10

**Strengths:**
- Architettura solida
- Buona separazione concerns
- Eccellente conflict detection
- Transazioni atomiche per swap (savepoint)

**Weaknesses:**
- 3 bug critici da fixare
- N+1 query in alcuni punti
- Inconsistenze minori

**Recommendation:** 
PROCEDI con cautela. I 3 bug critici devono essere fixati PRIMA del prossimo deploy
che coinvolge creazione booking o generazione booking_number.

---

*Report generato da Cervella Guardiana Ops*
*"Una verifica approfondita ora = zero disastri dopo."*
