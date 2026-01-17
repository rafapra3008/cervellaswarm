# Output: Analisi Pattern Validazione Ripetuti

## Status
⚠️ TROVATI PATTERN RIPETUTI SIGNIFICATIVI

## Health Score
6/10 - Buona opportunità per DRY (Don't Repeat Yourself)

## TOP 5 Pattern di Validazione Ripetuti

### 1. CRITICO: Validazione Date "Oggi" (30+ occorrenze)
**Pattern:**
```python
today = datetime.now().strftime("%Y-%m-%d")
if checkout_date < today:
    raise HTTPException(400, "...")
```

**Occorrenze:** 30+ file
**File principali:**
- `routers/bookings.py:183`
- `routers/planning_ops.py:400,454,559`
- `routers/planning_swap.py:199,357`
- `services/swap_validation.py:39,68`
- `services/booking_conflicts.py:139`

**Proposta:**
```python
# core/validators.py
def get_today() -> str:
    """Ritorna data odierna in formato YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")

def validate_not_past_checkout(checkout_date: str, entity_name: str = "prenotazione") -> None:
    """Valida che checkout non sia nel passato."""
    if checkout_date < get_today():
        raise HTTPException(400, f"Impossibile modificare {entity_name} conclusa (checkout passato)")
```

---

### 2. ALTO: HTTPException 404 "non trovato" (121 occorrenze)
**Pattern:**
```python
if not hotel:
    raise HTTPException(status_code=404, detail="Hotel non trovato")
if not booking:
    raise HTTPException(status_code=404, detail="Prenotazione non trovata")
if not room:
    raise HTTPException(status_code=404, detail="Camera non trovata")
```

**Occorrenze:** 121 file
**File principali:** Tutti i routers e molti services

**Proposta:**
```python
# core/validators.py
def validate_entity_exists(entity, entity_name: str = "Risorsa", entity_id = None):
    """Valida esistenza entità, altrimenti HTTPException 404."""
    if not entity:
        detail = f"{entity_name} non trovato"
        if entity_id:
            detail += f" (ID: {entity_id})"
        raise HTTPException(status_code=404, detail=detail)
    return entity

# Uso:
validate_entity_exists(hotel, "Hotel", hotel_code)
validate_entity_exists(booking, "Prenotazione", booking_id)
```

---

### 3. ALTO: hotel_code.upper() (70 occorrenze)
**Pattern:**
```python
cursor = conn.execute("SELECT id FROM hotels WHERE code = ?", (hotel_code.upper(),))
```

**Occorrenze:** 70 in 25 file
**File principali:**
- `routers/bookings.py:39`
- `routers/planning.py:71`
- `routers/dashboard.py` (4 volte)
- `routers/settings.py` (10 volte)

**Proposta:**
```python
# core/validators.py
def validate_hotel_code(conn, hotel_code: str) -> int:
    """Valida hotel_code e ritorna hotel_id.
    
    Args:
        conn: Database connection
        hotel_code: Codice hotel (es: 'nl', 'NL')
        
    Returns:
        int: hotel_id
        
    Raises:
        HTTPException(404): Se hotel non trovato
    """
    cursor = conn.execute(
        "SELECT id FROM hotels WHERE code = ?", 
        (hotel_code.upper(),)
    )
    hotel = cursor.fetchone()
    validate_entity_exists(hotel, "Hotel", hotel_code)
    return hotel[0]

# Uso:
hotel_id = validate_hotel_code(conn, hotel_code)
```

---

### 4. MEDIO: Validazione Email (20+ occorrenze manuali)
**Pattern:**
```python
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not re.match(email_regex, email):
    raise ValueError('Email non valida')
```

**Occorrenze:** 
- `routers/public/models.py:145-150` (Pydantic validator)
- Molti altri luoghi senza validazione formale

**Proposta:**
```python
# core/validators.py
import re
from typing import Optional

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: Optional[str], required: bool = True) -> Optional[str]:
    """Valida formato email.
    
    Args:
        email: Email da validare
        required: Se True, errore se None/vuota
        
    Returns:
        str: Email normalizzata (lowercase)
        
    Raises:
        HTTPException(400): Se email invalida
    """
    if not email:
        if required:
            raise HTTPException(400, "Email obbligatoria")
        return None
    
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(400, "Formato email non valido")
    
    return email.lower().strip()
```

---

### 5. MEDIO: Validazione Date Range (15+ occorrenze)
**Pattern:**
```python
if from_date > to_date:
    raise HTTPException(400, "Data inizio deve essere prima di data fine")

# Variante:
if start_date > end_date:
    raise HTTPException(400, "...")
    
# Con calcolo nights:
check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
nights = (check_out_date - check_in_date).days
if nights <= 0:
    raise HTTPException(400, "Check-out deve essere dopo check-in")
```

**Occorrenze:**
- `routers/competitors/prices.py:134`
- Pattern simili sparsi in molti file

**Proposta:**
```python
# core/validators.py
from datetime import datetime, timedelta

def validate_date_range(
    start_date: str, 
    end_date: str,
    min_nights: int = 1,
    max_nights: Optional[int] = None,
    start_label: str = "Data inizio",
    end_label: str = "Data fine"
) -> int:
    """Valida range date e calcola notti.
    
    Args:
        start_date: Data inizio (YYYY-MM-DD)
        end_date: Data fine (YYYY-MM-DD)
        min_nights: Minimo notti (default 1)
        max_nights: Massimo notti (opzionale)
        start_label: Label per errori (default "Data inizio")
        end_label: Label per errori (default "Data fine")
        
    Returns:
        int: Numero di notti
        
    Raises:
        HTTPException(400): Se range invalido
    """
    try:
        dt_start = datetime.strptime(start_date, '%Y-%m-%d')
        dt_end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        raise HTTPException(400, f"Formato date invalido: {e}")
    
    nights = (dt_end - dt_start).days
    
    if nights < min_nights:
        raise HTTPException(
            400, 
            f"{end_label} deve essere almeno {min_nights} {'notte' if min_nights == 1 else 'notti'} dopo {start_label}"
        )
    
    if max_nights and nights > max_nights:
        raise HTTPException(400, f"Range massimo {max_nights} notti")
    
    return nights

# Uso:
nights = validate_date_range(check_in, check_out, min_nights=1, max_nights=365)
```

---

## Metriche di Duplicazione

| Pattern | Occorrenze | File Coinvolti | Effort Refactor |
|---------|-----------|----------------|-----------------|
| `datetime.now().strftime("%Y-%m-%d")` | 30+ | 15+ | 2h |
| `HTTPException(404, "...non trovato")` | 121 | 44 | 4h |
| `hotel_code.upper()` | 70 | 25 | 3h |
| Validazione email manuale | 20+ | 10+ | 1h |
| Date range validation | 15+ | 8+ | 2h |

**Total Effort:** ~12 ore per centralizzare tutto

---

## File da Creare

### `backend/core/validators.py`

```python
"""
Core Validators - Miracollo Backend
====================================
Funzioni di validazione centralizzate per ridurre duplicazione.

Categorie:
- Date validation (today, range, format)
- Entity validation (exists, hotel_code)
- Input validation (email, phone, etc)
- Business logic validation (capacity, availability)
"""

from datetime import datetime, timedelta
from typing import Optional, Any
from fastapi import HTTPException
import re

__version__ = "1.0.0"

# ============================================
# DATE VALIDATORS
# ============================================

def get_today() -> str:
    """Ritorna data odierna in formato YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def validate_not_past_checkout(
    checkout_date: str, 
    entity_name: str = "prenotazione"
) -> None:
    """Valida che checkout non sia nel passato.
    
    Raises:
        HTTPException(400): Se checkout < oggi
    """
    if checkout_date < get_today():
        raise HTTPException(
            400, 
            f"Impossibile modificare {entity_name} conclusa (checkout passato)"
        )


def validate_date_range(
    start_date: str, 
    end_date: str,
    min_nights: int = 1,
    max_nights: Optional[int] = None,
    start_label: str = "Data inizio",
    end_label: str = "Data fine"
) -> int:
    """Valida range date e calcola notti.
    
    Returns:
        int: Numero di notti
        
    Raises:
        HTTPException(400): Se range invalido
    """
    try:
        dt_start = datetime.strptime(start_date, '%Y-%m-%d')
        dt_end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        raise HTTPException(400, f"Formato date invalido: {e}")
    
    nights = (dt_end - dt_start).days
    
    if nights < min_nights:
        raise HTTPException(
            400, 
            f"{end_label} deve essere almeno {min_nights} notte/i dopo {start_label}"
        )
    
    if max_nights and nights > max_nights:
        raise HTTPException(400, f"Range massimo {max_nights} notti")
    
    return nights


# ============================================
# ENTITY VALIDATORS
# ============================================

def validate_entity_exists(
    entity: Any, 
    entity_name: str = "Risorsa", 
    entity_id: Any = None
) -> Any:
    """Valida esistenza entità.
    
    Raises:
        HTTPException(404): Se entity è None/falsy
        
    Returns:
        entity: L'entità stessa (per chaining)
    """
    if not entity:
        detail = f"{entity_name} non trovato"
        if entity_id:
            detail += f" (ID: {entity_id})"
        raise HTTPException(status_code=404, detail=detail)
    return entity


def validate_hotel_code(conn, hotel_code: str) -> int:
    """Valida hotel_code e ritorna hotel_id.
    
    Args:
        conn: Database connection
        hotel_code: Codice hotel (es: 'nl', 'NL')
        
    Returns:
        int: hotel_id
        
    Raises:
        HTTPException(404): Se hotel non trovato
    """
    cursor = conn.execute(
        "SELECT id FROM hotels WHERE code = ?", 
        (hotel_code.upper(),)
    )
    hotel = cursor.fetchone()
    validate_entity_exists(hotel, "Hotel", hotel_code.upper())
    return hotel[0]


# ============================================
# INPUT VALIDATORS
# ============================================

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(
    email: Optional[str], 
    required: bool = True
) -> Optional[str]:
    """Valida e normalizza email.
    
    Returns:
        str: Email normalizzata (lowercase, trimmed)
        
    Raises:
        HTTPException(400): Se email invalida
    """
    if not email:
        if required:
            raise HTTPException(400, "Email obbligatoria")
        return None
    
    email = email.strip()
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(400, "Formato email non valido")
    
    return email.lower()


def validate_positive_number(
    value: float, 
    field_name: str = "Valore",
    allow_zero: bool = False
) -> float:
    """Valida che numero sia positivo.
    
    Raises:
        HTTPException(400): Se valore negativo o zero (se not allow_zero)
    """
    if allow_zero:
        if value < 0:
            raise HTTPException(400, f"{field_name} deve essere >= 0")
    else:
        if value <= 0:
            raise HTTPException(400, f"{field_name} deve essere > 0")
    return value


# ============================================
# BUSINESS LOGIC VALIDATORS
# ============================================

def validate_booking_not_past(conn, booking_id: int) -> None:
    """Valida che prenotazione non sia conclusa.
    
    Usa validate_not_past_checkout internamente.
    
    Raises:
        HTTPException(404): Se booking non trovato
        HTTPException(400): Se checkout passato
    """
    cursor = conn.execute(
        "SELECT check_out_date FROM bookings WHERE id = ?", 
        (booking_id,)
    )
    booking = cursor.fetchone()
    validate_entity_exists(booking, "Prenotazione", booking_id)
    
    validate_not_past_checkout(booking[0], f"prenotazione {booking_id}")
```

---

## Benefici Attesi

### Immediate
- **-400 righe** di codice duplicato
- **Manutenzione** centralizzata (1 fix = tutti i posti)
- **Consistenza** messaggi di errore

### A Medio Termine
- **Testing** più facile (test validators una volta)
- **Onboarding** più rapido (dove cercare validazioni?)
- **Estensibilità** più semplice (es: log automatico errori)

### Metriche
- **Prima:** 121 occorrenze "non trovato" sparse
- **Dopo:** 1 funzione `validate_entity_exists`
- **Saving:** ~300 righe, 12h lavoro futuro evitato

---

## Next Steps

### Priorità 1 (Subito)
1. Creare `core/validators.py` con funzioni base
2. Testare su 2-3 file pilota
3. Validare approccio con team

### Priorità 2 (1-2 settimane)
4. Migrare gradualmente routers più grandi
5. Aggiungere validators per casi specifici
6. Documentare pattern in `docs/VALIDATORI.md`

### Priorità 3 (Backlog)
7. Aggiungere logging automatico errori validazione
8. Metrics: quanti errori 404 per entità?
9. Auto-suggestions: "Prenotazione 123 non trovata. Intendevi 124?"

---

## Report Completo
`reports/engineer_report_20260117_validation.json`

## Effort Totale Refactoring
~12 ore distribuite su 2 settimane

