# TASK_AS5 - Output

## Metadata
- **Worker:** cervella-backend
- **Completato:** 2026-01-04 02:45
- **Status:** COMPLETATO

---

## Implementazione

### File Creato
`test-orchestrazione/api/helpers.py`

---

## 1. format_date()

```python
def format_date(date: datetime) -> str:
    """
    Formatta una data nel formato DD/MM/YYYY.
    """
    return date.strftime("%d/%m/%Y")
```

### Test
| Input | Output | Status |
|-------|--------|--------|
| datetime(2026, 1, 4) | "04/01/2026" | PASS |
| datetime(2025, 12, 25) | "25/12/2025" | PASS |
| datetime(2000, 1, 1) | "01/01/2000" | PASS |

---

## 2. format_currency()

```python
def format_currency(amount: float, symbol: str = "EUR") -> str:
    """
    Formatta un importo monetario con simbolo valuta.
    Usa il formato europeo: punto per migliaia, virgola per decimali.
    """
    formatted = f"{amount:,.2f}"
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{symbol} {formatted}"
```

### Test
| Input | Output | Status |
|-------|--------|--------|
| 1234.56 | "EUR 1.234,56" | PASS |
| 1000000, "USD" | "USD 1.000.000,00" | PASS |
| 99.9, "GBP" | "GBP 99,90" | PASS |
| 0.5 | "EUR 0,50" | PASS |

---

## 3. truncate_string()

```python
def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Tronca una stringa aggiungendo "..." se supera la lunghezza massima.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
```

### Test
| Input | Output | Status |
|-------|--------|--------|
| "Hello World", 50 | "Hello World" | PASS |
| "Hello World", 5 | "Hello..." | PASS |
| "Test", 4 | "Test" | PASS |
| "ABCDEFGHIJ", 3 | "ABC..." | PASS |

---

## 4. capitalize_words()

```python
def capitalize_words(text: str) -> str:
    """
    Rende maiuscola la prima lettera di ogni parola.
    """
    return "-".join(word.title() for word in text.split("-"))
```

### Test
| Input | Output | Status |
|-------|--------|--------|
| "hello world" | "Hello World" | PASS |
| "MARIO ROSSI" | "Mario Rossi" | PASS |
| "anna-maria" | "Anna-Maria" | PASS |
| "test" | "Test" | PASS |

---

## 5. slugify()

```python
def slugify(text: str) -> str:
    """
    Converte una stringa in slug URL-friendly.
    """
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text
```

### Test
| Input | Output | Status |
|-------|--------|--------|
| "Hello World" | "hello-world" | PASS |
| "Caffe Italiano!" | "caffe-italiano" | PASS |
| "  Multiple   Spaces  " | "multiple-spaces" | PASS |
| "Test@#$%Special" | "test-special" | PASS |
| "Gia fatto" | "gia-fatto" | PASS |

---

## Criteri di Successo

- [x] File `test-orchestrazione/api/helpers.py` esiste
- [x] Tutte e 5 le funzioni implementate
- [x] Ogni funzione ha docstring
- [x] Ogni funzione ha type hints
- [x] Test manuale per ogni funzione (16 test totali, tutti PASS)

---

## Riepilogo Test

| Funzione | Test | Passati |
|----------|------|---------|
| format_date | 3 | 3 |
| format_currency | 4 | 4 |
| truncate_string | 4 | 4 |
| capitalize_words | 4 | 4 |
| slugify | 5 | 5 |
| **TOTALE** | **16** | **16** |

---

*cervella-backend - Task completato*
