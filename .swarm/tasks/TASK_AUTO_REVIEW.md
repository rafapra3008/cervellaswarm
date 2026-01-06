# Task: Creare Sistema Auto-Review

**Assegnato a:** cervella-devops
**Priorita:** ALTA
**Stato:** ready

---

## Obiettivo

Creare un sistema che AUTOMATICAMENTE fa review dopo ogni task completato.

## Come Funziona Ora

1. Worker completa task
2. Crea file .done
3. FINE - nessuna review automatica

## Come Deve Funzionare

1. Worker completa task
2. Crea file .done
3. **NUOVO:** Hook rileva .done
4. **NUOVO:** Lancia cervella-guardiana-qualita per review
5. **NUOVO:** Guardiana scrive score in _review.md

## Implementazione

### 1. Hook post-task (in ~/.claude/hooks/)

Crea `auto_review_hook.py`:

```python
#!/usr/bin/env python3
"""
Auto-Review Hook
Quando un task viene completato (.done), lancia automaticamente
la Guardiana della Qualita per review.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def main():
    # Leggi input hook
    hook_input = json.loads(sys.stdin.read())

    # Cerca file .done recenti
    swarm_tasks = Path(".swarm/tasks")
    if not swarm_tasks.exists():
        return

    for done_file in swarm_tasks.glob("*.done"):
        task_name = done_file.stem
        output_file = swarm_tasks / f"{task_name}_output.md"
        review_file = swarm_tasks / f"{task_name}_review.md"

        # Se output esiste e review non esiste, lancia review
        if output_file.exists() and not review_file.exists():
            # Crea task review
            review_task = swarm_tasks / f"REVIEW_{task_name}.md"
            review_task.write_text(f"""# Task: Auto-Review {task_name}

**Assegnato a:** cervella-guardiana-qualita
**Priorita:** ALTA
**Stato:** ready

## Obiettivo
Review automatica del task {task_name}

## File da Revieware
- {output_file}

## Criteri
- Completezza (task fatto al 100%?)
- Qualita output
- Eventuali problemi

## Output
Score /10 + commenti in {review_file}
""")
            # Marca ready
            (swarm_tasks / f"REVIEW_{task_name}.ready").touch()

            print(f"[AUTO-REVIEW] Creato task review per {task_name}")

if __name__ == "__main__":
    main()
```

### 2. Configurazione Hook

Aggiungi in settings.json:
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

### 3. Script swarm-auto-review

Crea `swarm-auto-review` in ~/.claude/scripts/:

```bash
#!/bin/bash
# Controlla task completati senza review e lancia review

TASKS_DIR=".swarm/tasks"

for done_file in "$TASKS_DIR"/*.done; do
    [ -f "$done_file" ] || continue

    task_name=$(basename "$done_file" .done)
    output_file="$TASKS_DIR/${task_name}_output.md"
    review_file="$TASKS_DIR/${task_name}_review.md"

    if [ -f "$output_file" ] && [ ! -f "$review_file" ]; then
        echo "Review needed: $task_name"
        # Lancia guardiana
        spawn-workers --guardiana-qualita
    fi
done
```

## Output Atteso

1. Hook `auto_review_hook.py` in ~/.claude/hooks/
2. Script `swarm-auto-review` in ~/.claude/scripts/
3. Istruzioni per configurare hook
4. Test che funziona

## Bonus

Se possibile, integrare con watcher-regina.sh per notificare quando review completata.

---

*"Qualita automatica = zero dimenticanze!"*
