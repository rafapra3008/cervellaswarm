# TASK_AS2 - Output

## Metadata
- **Worker:** cervella-backend
- **Completato:** 2026-01-04 02:43
- **Status:** COMPLETATO

---

## Implementazione

### File Creato
`test-orchestrazione/api/validators.py`

### Codice

```python
"""
Validators module - Funzioni di validazione per l'API.

Questo modulo contiene funzioni di validazione riutilizzabili
per input utente e dati API.
"""

import re


def validate_name(name: str) -> bool:
    """
    Valida un nome secondo i criteri standard.

    Criteri di validazione:
    - Nome non deve essere vuoto o contenere solo spazi
    - Nome non deve superare 100 caratteri
    - Nome deve contenere solo lettere, spazi e trattini

    Args:
        name: Il nome da validare

    Returns:
        True se il nome e valido, False altrimenti

    Examples:
        >>> validate_name("Mario Rossi")
        True
        >>> validate_name("Anna-Maria")
        True
        >>> validate_name("")
        False
        >>> validate_name("John123")
        False
        >>> validate_name("A" * 101)
        False
    """
    # Check: nome non vuoto
    if not name or not name.strip():
        return False

    # Check: lunghezza max 100 caratteri
    if len(name) > 100:
        return False

    # Check: solo lettere (incluse accentate), spazi e trattini
    pattern = r'^[a-zA-ZàèéìòùÀÈÉÌÒÙäëïöüÄËÏÖÜáéíóúÁÉÍÓÚñÑçÇ\s\-]+$'
    if not re.match(pattern, name):
        return False

    return True
```

---

## Test Eseguiti

### Casi VALIDI (tutti PASS)
| Input | Risultato | Status |
|-------|-----------|--------|
| "Mario Rossi" | True | PASS |
| "Anna-Maria" | True | PASS |
| "Jose Garcia" | True | PASS |
| "Francois" | True | PASS |
| "Muller" | True | PASS |
| "A" | True | PASS |
| "A" * 100 (100 char) | True | PASS |

### Casi INVALIDI (tutti PASS)
| Input | Motivo | Risultato | Status |
|-------|--------|-----------|--------|
| "" | stringa vuota | False | PASS |
| "   " | solo spazi | False | PASS |
| "John123" | contiene numeri | False | PASS |
| "Mario@Rossi" | contiene @ | False | PASS |
| "A" * 101 | 101 caratteri | False | PASS |
| "Hello!" | contiene ! | False | PASS |
| "Test_Name" | contiene underscore | False | PASS |

---

## Criteri di Successo

- [x] File `test-orchestrazione/api/validators.py` esiste
- [x] Funzione `validate_name()` esiste
- [x] Validazione nome vuoto funziona
- [x] Validazione lunghezza max 100 funziona
- [x] Validazione caratteri funziona
- [x] Ha docstring con esempi

---

## Note per Guardiana

Task LIVELLO 2 - Pronto per review!

Caratteristiche implementate:
1. Type hints completi
2. Docstring con esempi doctest
3. Supporto caratteri accentati (italiano, spagnolo, tedesco, francese)
4. Pattern regex robusto
5. Tutti i test passano

---

*cervella-backend - Task completato*
