# TASK_AS3 - Output

## Status: COMPLETATO

## Implementazione

### File Creato
`test-orchestrazione/api/file_reader.py`

### Codice Scritto

```python
"""
File reader module for CervellaSwarm test orchestration.

This module demonstrates graceful error handling when attempting
to read files that may not exist.
"""

import json
from typing import Any


def read_config(path: str = "/path/che/non/esiste/config.json") -> dict[str, Any]:
    """
    Attempt to read a JSON config file with graceful error handling.
    ...
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "File not found", "fallback": "default_config"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format", "fallback": "default_config"}
    except PermissionError:
        return {"error": "Permission denied", "fallback": "default_config"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "fallback": "default_config"}
```

## Test Manuale

```bash
python3 -c "
import sys
sys.path.insert(0, 'test-orchestrazione')
from api.file_reader import read_config
result = read_config()
print(result)
"
```

**Output:**
```
{'error': 'File not found', 'fallback': 'default_config'}
```

## Gestione Errore - Spiegazione

### Strategia

1. **Try/Except specifico**: Ho catturato `FileNotFoundError` come eccezione primaria (quello che ci aspettavamo)

2. **Fallback graceful**: Invece di crashare, la funzione ritorna un dizionario con:
   - `"error"`: descrizione del problema
   - `"fallback"`: indicatore che stiamo usando config di default

3. **Errori aggiuntivi gestiti**: Ho aggiunto gestione per:
   - `JSONDecodeError`: file esiste ma JSON invalido
   - `PermissionError`: file esiste ma non leggibile
   - `Exception` generica: catch-all per casi imprevisti

4. **Mai crash**: La funzione ritorna SEMPRE un dict valido, mai solleva eccezioni verso il chiamante

### Perche questo approccio?

- **Resilienza**: Il sistema continua a funzionare anche se il config non esiste
- **Trasparenza**: Il chiamante sa cosa e andato storto (`error` field)
- **Fallback chiaro**: Il chiamante sa che sta usando config di default

## Criteri di Successo

- [x] File `test-orchestrazione/api/file_reader.py` esiste
- [x] Funzione `read_config()` esiste
- [x] Gestisce FileNotFoundError
- [x] Ritorna fallback invece di crashare
- [x] Ha docstring che spiega il comportamento

---
*Completato da: cervella-backend*
*Data: 2026-01-03*
