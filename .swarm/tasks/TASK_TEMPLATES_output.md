# Output: TASK_TEMPLATES

**Worker:** cervella-backend
**Completato:** 2026-01-06 03:53

---

## Cosa e' stato creato

### 4 Template Task

**Posizione:** `~/.claude/scripts/templates/`

| Template | Uso |
|----------|-----|
| `TASK_TEMPLATE_RICERCA.md` | Task di ricerca/studio |
| `TASK_TEMPLATE_FIX_BUG.md` | Bug fix |
| `TASK_TEMPLATE_FEATURE.md` | Nuove feature |
| `TASK_TEMPLATE_REVIEW.md` | Code review |

### Script: task-new

**Posizione:** `~/.claude/scripts/task-new`

### Uso

```bash
# Crea task ricerca
task-new ricerca "Studio API WhatsApp"

# Crea task bug fix
task-new bug "Fix login error"

# Crea task feature
task-new feature "Add dark mode"

# Crea task review
task-new review "Review auth module"

# Alias disponibili
task-new research "..."  # = ricerca
task-new fix "..."       # = bug
task-new feat "..."      # = feature
task-new rev "..."       # = review
```

### Come Funziona

1. Copia il template corretto in `.swarm/tasks/`
2. Genera nome univoco con timestamp
3. Sostituisce placeholder [TITOLO] con il titolo dato
4. Mostra istruzioni per completare e lanciare

### Esempio

```bash
$ task-new ricerca "Studio API WhatsApp"

Task creato: .swarm/tasks/TASK_20260106_035320_studio_api_whatsapp.md

Prossimi step:
  1. Modifica il file per completare i dettagli
  2. Esegui: touch .swarm/tasks/TASK_20260106_035320_studio_api_whatsapp.ready
  3. Lancia il worker appropriato

Apri con: code .swarm/tasks/TASK_20260106_035320_studio_api_whatsapp.md
```

---

## File Creati

1. `~/.claude/scripts/swarm-report` (chmod +x)
2. `~/.claude/scripts/task-new` (chmod +x)
3. `~/.claude/scripts/templates/TASK_TEMPLATE_RICERCA.md`
4. `~/.claude/scripts/templates/TASK_TEMPLATE_FIX_BUG.md`
5. `~/.claude/scripts/templates/TASK_TEMPLATE_FEATURE.md`
6. `~/.claude/scripts/templates/TASK_TEMPLATE_REVIEW.md`

---

*Completato con successo!*
