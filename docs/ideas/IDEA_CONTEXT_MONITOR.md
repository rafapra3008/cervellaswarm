# IDEA: Context Monitor Script

> **Stato:** IDEA per futuro
> **Data:** 4 Gennaio 2026
> **Sessione:** 77
> **Priorita:** Media (per ora Rafa avvisa manualmente)

---

## Il Problema

```
Claude Code mostra: "Context left until auto-compact: X%"

MA:
- Cervella NON puo accedere a questa percentuale
- Quando scatta auto-compact (1%) e TROPPO TARDI
- Non c'e tempo per salvare tutto con calma
```

## La Soluzione Attuale (Manuale)

```
Rafa vede la percentuale nella UI.
Quando arriva al 10-12%, dice: "Cervella, siamo al 10%!"
Cervella inizia il processo anti-compact CON CALMA.
```

## La Soluzione Futura (Script)

### Concetto

Creare uno script Python che:
1. Monitora i file transcript in `~/.claude/projects/{project}/{session}.jsonl`
2. Legge i token usage da ogni messaggio
3. Stima la percentuale di contesto usato
4. Invia notifica macOS quando arriva al 10-12%

### Come Funzionerebbe

```python
# Pseudo-codice

import watchdog  # File watcher
import json

# Ogni messaggio nel transcript ha:
# {
#   "message": {
#     "usage": {
#       "input_tokens": X,
#       "cache_creation_input_tokens": Y,
#       "cache_read_input_tokens": Z,
#       "output_tokens": W
#     }
#   }
# }

# Calcolo:
total_input = input_tokens + cache_creation + cache_read

# PROBLEMA: Non include system overhead (~45k tokens)
# SOLUZIONE: Aggiungere overhead stimato

OVERHEAD = 45000  # Stima conservativa
total_used = conversation_tokens + OVERHEAD
percentage = (total_used / 200000) * 100

if percentage >= 10:
    send_macos_notification("Context al 10%!")
```

### Limitazioni Note

| Limitazione | Workaround |
|-------------|------------|
| Overhead sistema non esposto | Stima conservativa (+45k) |
| Session ID dinamico | Auto-detect latest .jsonl |
| Atomic writes (file lock) | Hybrid: watchdog + polling |

### Accuratezza Stimata

~85-90% (meglio sovrastimare che sottostimare!)

### Dipendenze

```bash
pip install watchdog
```

### File che Esistono Gia

- `~/.claude/stats-cache.json` - Statistiche generali (non contesto corrente)
- `~/.claude/session-log.txt` - Log sessioni terminate
- `~/.claude/projects/{project}/{session}.jsonl` - Transcript con token usage

### Feature Request su GitHub

Esistono MULTIPLE richieste aperte:
- Issue #11819 - Configurable auto-compact threshold
- Issue #13776 - Expose full context usage in statusline

Nessuna risposta dai maintainers. Dobbiamo arrangiarci!

---

## Quando Implementare

**ORA:** NO - La soluzione manuale funziona.

**FUTURO:** SI - Quando:
- Abbiamo tempo dedicato
- Vogliamo automazione completa
- Rafa non vuole piu controllare manualmente

---

## Referenze

- Ricerca completa fatta da cervella-researcher (Sessione 77)
- [How to Calculate Your Claude Code Context Usage](https://codelynx.dev/posts/calculate-claude-code-context)
- [watchdog Library](https://github.com/gorakhargosh/watchdog)

---

*"Per ora manuale, futuro automatico!"* - Cervella & Rafa
