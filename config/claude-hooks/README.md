# Claude Code Hooks - Backup

Backup versionato degli hooks globali di Claude Code.

## Posizione Originale
```
~/.claude/hooks/
~/.claude/settings.json
```

## File

| File | Scopo |
|------|-------|
| `pre_compact_save.py` | Salva snapshot prima del compact |
| `session_end_save.py` | Salva snapshot quando chiudi sessione |
| `update_prompt_ripresa.py` | Aggiorna PROMPT_RIPRESA.md automaticamente |
| `git_reminder.py` | Reminder file non committati (ogni 30 min) |
| `settings.json` | Configurazione hooks + permessi |

## Ripristino

Se perdi ~/.claude/, ripristina con:
```bash
cp config/claude-hooks/*.py ~/.claude/hooks/
cp config/claude-hooks/settings.json ~/.claude/
```

---
*Creato: 1 Gennaio 2026*
