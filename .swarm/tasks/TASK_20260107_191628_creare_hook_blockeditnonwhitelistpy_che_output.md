# Output: Hook block_edit_non_whitelist.py

**Data:** 2026-01-07
**Worker:** cervella-backend
**Durata:** ~5 minuti

---

## Risultato

✅ **TASK COMPLETATO CON SUCCESSO**

---

## Cosa Ho Fatto

### 1. Creato Hook
**File:** `~/.claude/hooks/block_edit_non_whitelist.py`

Hook PreToolUse che blocca Edit/Write su file non in whitelist.

### 2. Whitelist Implementata
- `NORD.md` - Bussola progetto
- `PROMPT_RIPRESA.md` - Stato sessione
- `ROADMAP_SACRA.md` - Roadmap principale
- `.swarm/tasks/*` - Task per worker
- `.swarm/handoff/*` - Comunicazione worker
- `.swarm/feedback/*` - Feedback (risposte)
- `.swarm/status/*` - Status files

### 3. Aggiornato settings.json
Aggiunto hook a PreToolUse per matcher `Edit` e `Write`.

### 4. Test Eseguiti
| Test | File | Risultato |
|------|------|-----------|
| Whitelist | NORD.md | ✅ PASSA (exit 0) |
| Whitelist | .swarm/tasks/TEST.md | ✅ PASSA (exit 0) |
| NON Whitelist | backend/main.py | ✅ BLOCCA (exit 1) |

---

## File Creati/Modificati

1. **CREATO:** `~/.claude/hooks/block_edit_non_whitelist.py`
   - 140 righe Python
   - Pattern matching con fnmatch
   - Messaggio errore chiaro con istruzioni

2. **MODIFICATO:** `~/.claude/settings.json`
   - Aggiunto PreToolUse per Edit
   - Aggiunto PreToolUse per Write

---

## Note Tecniche

- Hook usa `fnmatch` per glob patterns
- Supporta sia path assoluti che relativi
- Fail-safe: in caso di errore parsing, lascia passare
- Messaggio blocco include whitelist e istruzioni

---

## Verifica

```bash
# Test manuale
echo '{"tool_name": "Edit", "tool_input": {"file_path": "backend/main.py"}}' | \
  python3 ~/.claude/hooks/block_edit_non_whitelist.py
# Risultato: BLOCCATO con exit 1
```

---

**Task completato!**

*cervella-backend*
