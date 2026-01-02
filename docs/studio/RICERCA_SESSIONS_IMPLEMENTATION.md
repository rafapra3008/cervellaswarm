# RICERCA SESSIONS IMPLEMENTATION - Claude Code CLI

> **Data:** 2 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **REGOLA 11:** PERCHÉ → RICERCA → VERIFICA PERCHÉ

---

## EXECUTIVE SUMMARY

### TL;DR - RISPOSTA AL PERCHÉ

**SCOPERTA CHIAVE:** Claude Code CLI **GIÀ HA** robust session persistence nativo!

- Sessions salvate in `~/.claude/projects/[project-path]/`
- Formato JSONL per transcript completo
- Comandi nativi: `claude -c` (continue), `claude -r [ID]` (resume)
- Hooks SessionStart/SessionEnd per custom logic

**RACCOMANDAZIONE:** NON ricostruire da zero! Usare sistema nativo + estendere con hooks.

---

## COSA ESISTE GIÀ (Nativo)

### Storage Structure

```
~/.claude/
├── projects/                      # Sessions per project
│   └── -Users-rafapra-Developer-CervellaSwarm/
│       ├── [session-id].jsonl     # Full transcript
│       └── ...other sessions
├── todos/                         # Todo lists per session
├── file-history/                  # File versioning
└── shell-snapshots/               # Shell state
```

### Comandi Nativi

| Comando | Funzione |
|---------|----------|
| `claude -c` | Continue last session |
| `claude -r [SESSION_ID]` | Resume specific session |
| `claude --resume` | Same as -r |
| `/clear` | Clear current session |

### Session Persistence Automatico

- **JSONL format** - Ogni messaggio su riga separata
- **Auto-save** - Salvato dopo ogni interazione
- **Project-based** - Isolato per progetto
- **Resumable** - Qualsiasi sessione può essere ripresa

---

## HOOKS DISPONIBILI

### SessionStart

Trigger: Session starts/resumes/clear

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "cat NORD.md && git status --short"
      }]
    }]
  }
}
```

**Use Cases:**
- Load project context (NORD.md, ROADMAP)
- Inject git status
- Set session env vars
- Load sprint goals

### SessionEnd

Trigger: Session ends (not on interrupt)

```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "git add -A && git commit -m '🔄 Auto-commit' || true"
      }]
    }]
  }
}
```

**Use Cases:**
- Auto git commit
- Log session stats
- Cleanup temp files
- Send notification

---

## COSA FARE (Estensioni)

### P0: Session Context Hook (4 ore)

Migliorare SessionStart per iniettare:
- NORD.md (dove siamo)
- Sprint attuale da ROADMAP_SACRA.md
- Git status + last commits
- Todo list attiva

### P1: Session Analytics (6 ore)

Script per analizzare JSONL esistenti:
- Durata sessioni
- Tool usage stats
- Error patterns
- Token consumption estimate

### P2: Session CLI Helper (opzionale)

```bash
# List recent sessions
claude-sessions list --last 10

# Resume with fuzzy search
claude-sessions resume "miracollo"

# Export session to markdown
claude-sessions export [ID] > session.md
```

---

## EFFORT ESTIMATION

| Feature | Ore | Priorità |
|---------|-----|----------|
| SessionStart context injection | 4h | ALTA |
| Analytics scripts | 6h | MEDIA |
| CLI helper | 4h | BASSA |
| **TOTALE P0+P1** | **10h** | - |

---

## RACCOMANDAZIONE FINALE

**NON FARE:**
- ❌ Custom JSONL storage (già c'è!)
- ❌ Custom resume logic (già c'è!)
- ❌ Ricostruire session management

**FARE:**
- ✅ SessionStart hook per context injection
- ✅ SessionEnd hook per logging
- ✅ Analytics scripts su JSONL esistenti

---

**Autrice:** Cervella Researcher 🔬
**Modalità:** "Noi Mode" - Usa quello che c'è, estendi solo dove serve!
