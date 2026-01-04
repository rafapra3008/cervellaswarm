# API Reference - test-orchestrazione

> Documentazione delle funzioni disponibili nel modulo `api/`

---

## Indice

1. [hello.py](#hellopy) - Modulo Hello World
2. [validators.py](#validatorspy) - Funzioni di validazione
3. [file_reader.py](#file_readerpy) - Lettura file config
4. [greeting.py](#greetingpy) - Saluto del Giorno
5. [countdown.py](#countdownpy) - Countdown Evento
6. [helpers.py](#helperspy) - Funzioni helper
7. [utils.py](#utilspy) - Utility functions

---

## hello.py

Modulo di test per il sistema di comunicazione dello sciame.

### `hello_world() -> str`

Ritorna un messaggio di saluto per CervellaSwarm.

**Returns:**
- `str`: Il messaggio "Hello CervellaSwarm!"

**Esempio:**
```python
>>> hello_world()
'Hello CervellaSwarm!'
```

---

## validators.py

Funzioni di validazione riutilizzabili per input utente e dati API.

### `validate_name(name: str) -> bool`

Valida un nome secondo i criteri standard.

**Criteri di validazione:**
- Nome non deve essere vuoto o contenere solo spazi
- Nome non deve superare 100 caratteri
- Nome deve contenere solo lettere, spazi e trattini

**Args:**
- `name` (str): Il nome da validare

**Returns:**
- `bool`: True se il nome e valido, False altrimenti

**Esempi:**
```python
>>> validate_name("Mario Rossi")
True
>>> validate_name("Anna-Maria")
True
>>> validate_name("")
False
>>> validate_name("John123")
False
```

---

## file_reader.py

Modulo per la lettura di file config con gestione errori graceful.

### `read_config(path: str = "/path/che/non/esiste/config.json") -> dict[str, Any]`

Tenta di leggere un file JSON config con gestione errori graceful.

**Args:**
- `path` (str): Percorso del file config. Default: path inesistente per test.

**Returns:**
- `dict`: Il JSON parsato se successo, oppure un dict fallback con:
  - `"error"`: Descrizione dell'errore
  - `"fallback"`: Indicatore che si sta usando config default

**Errori gestiti:**
- `FileNotFoundError`: File non trovato
- `JSONDecodeError`: Formato JSON invalido
- `PermissionError`: Permessi negati
- Altre eccezioni generiche

**Esempio:**
```python
>>> result = read_config()  # File non esiste
>>> result["error"]
'File not found'
>>> result["fallback"]
'default_config'
```

---

## greeting.py

Endpoint API per saluto personalizzato basato sull'ora corrente.

**Versione:** 1.0.0

### `get_greeting() -> dict`

Ritorna un saluto basato sull'ora corrente.

**Logica:**
| Orario | Saluto |
|--------|--------|
| 05:00-12:00 | Buongiorno! |
| 12:00-18:00 | Buon pomeriggio! |
| 18:00-22:00 | Buonasera! |
| 22:00-05:00 | Buonanotte! |

**Returns:**
- `dict`: `{"greeting": str, "hour": int}`

### `handle_request() -> str`

Handler principale per l'endpoint GET /api/greeting.

**Returns:**
- `str`: JSON response con greeting e hour

**Esempio Response:**
```json
{
  "status": "success",
  "data": {
    "greeting": "Buongiorno!",
    "hour": 9
  }
}
```

---

## countdown.py

Endpoint API per calcolare giorni rimanenti fino a un evento.

**Versione:** 1.0.0

### `get_countdown(target_date: str, event_name: str = "Evento") -> dict`

Calcola i giorni rimanenti fino a una data target.

**Args:**
- `target_date` (str): Data target in formato "YYYY-MM-DD"
- `event_name` (str): Nome dell'evento (default: "Evento")

**Returns:**
- `dict`:
  - `days_remaining` (int): Giorni rimanenti (negativo se passato)
  - `target_date` (str): Data formattata "YYYY-MM-DD"
  - `event_name` (str): Nome evento
  - `is_past` (bool): True se data passata
  - `is_today` (bool): True se data e oggi

**Raises:**
- `ValueError`: Se target_date non e in formato valido

### `handle_request(target_date: str, event_name: str = "Evento") -> str`

Handler principale per l'endpoint GET /api/countdown.

**Esempio Response:**
```json
{
  "status": "success",
  "data": {
    "days_remaining": 364,
    "target_date": "2026-12-31",
    "event_name": "Fine Anno",
    "is_past": false,
    "is_today": false
  }
}
```

---

## helpers.py

Funzioni helper riutilizzabili per formattazione e manipolazione dati.

### `format_date(date: datetime) -> str`

Formatta una data nel formato DD/MM/YYYY.

**Args:**
- `date` (datetime): Oggetto datetime da formattare

**Returns:**
- `str`: Data formattata come "DD/MM/YYYY"

**Esempio:**
```python
>>> from datetime import datetime
>>> format_date(datetime(2026, 1, 4))
'04/01/2026'
```

### `format_currency(amount: float, symbol: str = "EUR") -> str`

Formatta un importo monetario con simbolo valuta (formato europeo).

**Args:**
- `amount` (float): Importo numerico
- `symbol` (str): Simbolo valuta (default: "EUR")

**Returns:**
- `str`: Formato "SYMBOL X.XXX,XX"

**Esempi:**
```python
>>> format_currency(1234.56)
'EUR 1.234,56'
>>> format_currency(1000000, "USD")
'USD 1.000.000,00'
```

### `truncate_string(text: str, max_length: int = 50) -> str`

Tronca una stringa aggiungendo "..." se supera la lunghezza massima.

**Args:**
- `text` (str): Testo da troncare
- `max_length` (int): Lunghezza massima (default: 50)

**Returns:**
- `str`: Stringa troncata con "..." se necessario

**Esempio:**
```python
>>> truncate_string("Hello World", 5)
'Hello...'
```

### `capitalize_words(text: str) -> str`

Rende maiuscola la prima lettera di ogni parola.

**Args:**
- `text` (str): Testo da trasformare

**Returns:**
- `str`: Stringa con prima lettera di ogni parola maiuscola

**Esempio:**
```python
>>> capitalize_words("hello world")
'Hello World'
```

### `slugify(text: str) -> str`

Converte una stringa in slug URL-friendly.

**Args:**
- `text` (str): Testo da convertire

**Returns:**
- `str`: Slug (lowercase, solo lettere/numeri/trattini)

**Esempi:**
```python
>>> slugify("Hello World")
'hello-world'
>>> slugify("Caffe Italiano!")
'caffe-italiano'
```

---

## utils.py

Utility functions per gestione date e validazione.

**Versione:** 1.0.0

### `format_date(date: Optional[datetime], format: DateFormat = "DD/MM/YYYY") -> str`

Formatta una data secondo il formato specificato.

**Args:**
- `date` (datetime | None): Oggetto datetime da formattare
- `format` (DateFormat): Formato desiderato:
  - `"DD/MM/YYYY"`: Es. "02/01/2026"
  - `"YYYY-MM-DD"`: Es. "2026-01-02" (ISO 8601)
  - `"human"`: Es. "2 Gennaio 2026"

**Returns:**
- `str`: Data formattata, o stringa vuota se date e None

**Esempi:**
```python
>>> dt = datetime(2026, 1, 2)
>>> format_date(dt, "DD/MM/YYYY")
'02/01/2026'
>>> format_date(dt, "human")
'2 Gennaio 2026'
>>> format_date(None)
''
```

### `validate_email(email: Optional[str]) -> bool`

Valida un indirizzo email secondo le convenzioni standard.

**Criteri:**
- Contiene esattamente un @
- Parte locale (prima di @) non vuota
- Dominio (dopo @) con almeno un punto
- No caratteri non validi

**Args:**
- `email` (str | None): Indirizzo email da validare

**Returns:**
- `bool`: True se formato valido, False altrimenti

**Esempi:**
```python
>>> validate_email("user@example.com")
True
>>> validate_email("invalid-email")
False
>>> validate_email(None)
False
```

---

## Riepilogo Funzioni

| Modulo | Funzione | Descrizione |
|--------|----------|-------------|
| hello.py | `hello_world()` | Ritorna "Hello CervellaSwarm!" |
| validators.py | `validate_name()` | Valida nomi (lettere, spazi, trattini) |
| file_reader.py | `read_config()` | Legge JSON config con fallback |
| greeting.py | `get_greeting()` | Saluto basato su ora corrente |
| greeting.py | `handle_request()` | Handler endpoint /api/greeting |
| countdown.py | `get_countdown()` | Calcola giorni a evento |
| countdown.py | `handle_request()` | Handler endpoint /api/countdown |
| helpers.py | `format_date()` | Formatta data DD/MM/YYYY |
| helpers.py | `format_currency()` | Formatta importo EUR X.XXX,XX |
| helpers.py | `truncate_string()` | Tronca stringa con "..." |
| helpers.py | `capitalize_words()` | Maiuscola prima lettera parole |
| helpers.py | `slugify()` | Converte in slug URL-friendly |
| utils.py | `format_date()` | Formatta data (multi-formato) |
| utils.py | `validate_email()` | Valida indirizzo email |

---

*Generato da cervella-docs | 2026-01-04*
