# Output: Sistema Auto-Review

**Task:** TASK_AUTO_REVIEW
**Worker:** cervella-devops
**Completato:** 2026-01-06

---

## Cosa Ho Creato

### 1. Hook `auto_review_hook.py`

**Posizione:** `~/.claude/hooks/auto_review_hook.py`

**Funzionalita:**
- Si attiva quando viene scritto un file `.done`
- Cerca task completati senza review
- Crea automaticamente task di review per `cervella-guardiana-qualita`
- Include criteri di valutazione strutturati (Completezza, Qualita, Best Practices, Efficienza)

**Trigger:** PostToolUse su Write

### 2. Script `swarm-auto-review`

**Posizione:** `~/.claude/scripts/swarm-auto-review`

**Uso:**
```bash
swarm-auto-review           # Crea task review per task completati
swarm-auto-review --check   # Solo verifica, non crea task
swarm-auto-review --launch  # Crea task e lancia guardiana automaticamente
```

**Funzionalita:**
- Scansiona `.swarm/tasks/*.done`
- Identifica task senza review
- Crea task di review con template strutturato
- Opzione per lanciare guardiana automaticamente
- Notifica macOS quando ci sono task da revieware

---

## Test Eseguito

```
=== SWARM AUTO-REVIEW ===

Task completati totali: 33
Task che necessitano review: 31
```

Il sistema ha correttamente identificato 31 task che necessitano review.

---

## Come Configurare Hook (Opzionale)

Se vuoi che l'hook si attivi automaticamente, aggiungi in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "python3 ~/.claude/hooks/auto_review_hook.py"
      }
    ]
  }
}
```

**NOTA:** L'hook funziona anche chiamato manualmente o tramite `swarm-auto-review`.

---

## File Creati

| File | Posizione | Permessi |
|------|-----------|----------|
| auto_review_hook.py | ~/.claude/hooks/ | +x |
| swarm-auto-review | ~/.claude/scripts/ | +x |

---

## Integrazione con Watcher

Il sistema e' progettato per integrarsi con `watcher-regina.sh`. Quando la guardiana completa una review, il file `_review.md` viene creato e puo' essere rilevato dal watcher.

---

*"Qualita automatica = zero dimenticanze!"*
