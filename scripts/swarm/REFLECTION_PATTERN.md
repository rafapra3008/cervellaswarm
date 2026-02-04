# Reflection Pattern - Output Validation

> **FASE 2 - Auto-validazione worker output**
> Sessione 336 - 4 Febbraio 2026

## Cos'è

Sistema di auto-validazione output worker per CervellaSwarm.
Dopo che un worker completa un task, valida automaticamente la qualità dell'output.

## Come funziona

```
Worker esegue task
    ↓
Crea _output.md
    ↓
Output Validator analizza
    ↓
Score 0-100 + suggerimenti
```

## Utilizzo

### 1. Validazione manuale

```bash
# Valida ultimo output creato
python3 scripts/swarm/output_validator.py --last-output

# Valida file specifico
python3 scripts/swarm/output_validator.py --file TASK_001_output.md

# Valida task specifico
python3 scripts/swarm/output_validator.py --task TASK_001

# Output JSON (per scripting)
python3 scripts/swarm/output_validator.py --last-output --json
```

### 2. Validazione automatica (spawn-workers)

```bash
# Abilita validazione automatica post-task
spawn-workers.sh --backend --with-validation

# Il worker spawnerà, completerà il task, e l'output sarà validato automaticamente
# Risultato nel log: .swarm/logs/worker_*.log
```

## Checks eseguiti

| Check | Descrizione | Impatto Score |
|-------|-------------|---------------|
| File esiste | Output file creato | BLOCCA (-100) |
| Non vuoto | Contenuto presente | BLOCCA (-100) |
| Lunghezza minima | >100 caratteri | WARNING (-10) |
| Error markers | "Error:", "Traceback", etc. | BLOCCA (-40) |
| Marker incompletezza | "TODO:", "FIXME:", "..." | WARNING (-15) |
| Success indicators | "✓", "DONE", "Success" | BONUS (+5) |
| Log errors | Errori nei log worker | WARNING (-10) |

## Exit codes

- `0` = VALID (output OK)
- `1` = INVALID (errori trovati)
- `2` = ERROR (validazione fallita)

## Formato output JSON

```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Output molto corto (89 caratteri < 100)"],
  "retry_needed": false,
  "retry_context": "",
  "score": 90
}
```

## Interpretazione score

- **90-100**: Ottimo! Output completo e pulito
- **70-89**: Buono, ma con warning minori
- **50-69**: Mediocre, review consigliata
- **0-49**: Problematico, retry suggerito

## Retry logic (FUTURO - FASE 3)

Al momento il validator solo SEGNALA problemi.

**FASE 3** (futura) implementerà retry automatico:
- Se score < 50 → auto-retry 1 volta con context aggiuntivo
- Se score < 30 → escalation a Guardiana
- Max 2 retry per task

## Configurazione

**spawn-workers.sh:**
```bash
# DEFAULT: validazione disabilitata (feature sperimentale)
OUTPUT_VALIDATION=false

# Per abilitare:
OUTPUT_VALIDATION=true
```

**output_validator.py:**
```python
# Minima lunghezza output valido
MIN_OUTPUT_LENGTH = 100

# Error markers da cercare
ERROR_MARKERS = ["Error:", "Traceback", "FAILED", ...]

# Marker incompletezza
INCOMPLETE_MARKERS = ["TODO:", "FIXME:", "...", ...]
```

## Esempi

### Output valido

```
✓ VALID - TASK_001_output.md
Score: 95/100
```

### Output con warning

```
✓ VALID - TASK_002_output.md
Score: 85/100

WARNINGS:
  - Marker incompletezza: TODO:
```

### Output invalido

```
✗ INVALID - TASK_003_output.md
Score: 45/100

ERRORS:
  - Error markers trovati: Error:, Traceback

WARNINGS:
  - Output molto corto (89 caratteri < 100)

⚠️  RETRY SUGGESTED
Context: Qualità output bassa (score: 45). Review consigliata.
```

## Testing

```bash
# Test validator version
python3 scripts/swarm/output_validator.py --version

# Test su file esistente
python3 scripts/swarm/output_validator.py --file .swarm/tasks/TASK_001_output.md

# Test ultimo output
python3 scripts/swarm/output_validator.py --last-output

# Test JSON output
python3 scripts/swarm/output_validator.py --last-output --json | jq .
```

## File modificati

- `scripts/swarm/output_validator.py` - Validator standalone (198 righe)
- `scripts/swarm/spawn-workers.sh` - Integration hook (opzionale, ~10 righe)

## Prossimi step (FASE 3)

- [ ] Retry logic automatico
- [ ] Escalation a Guardiana se retry fallisce
- [ ] Metriche aggregate (score medio per worker)
- [ ] Dashboard validazioni (.swarm/logs/validation_summary.json)
- [ ] Integrazione con task_manager.py (stato NEEDS_REVIEW)

---

*"Fatto BENE > Fatto VELOCE"*
*Sessione 336 - Cervella Backend*
