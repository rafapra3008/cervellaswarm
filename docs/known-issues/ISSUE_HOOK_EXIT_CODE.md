# ISSUE: Hook PreToolUse - Exit Code Sbagliato

> **Data scoperta:** 7 Gennaio 2026 - Sessione 116
> **Severity:** CRITICA
> **Status:** RISOLTA

---

## Il Problema

Gli hook PreToolUse per bloccare Edit/Write e Task NON funzionavano.
Pensavamo funzionassero (test manuale OK), ma in pratica Claude Code li ignorava.

### Sintomi

- Edit su file non in whitelist: PASSAVA (doveva bloccare)
- Task con cervella-* agents: PASSAVA (doveva bloccare)
- Debug hook: NON veniva nemmeno chiamato (log vuoto)

---

## Root Cause

**EXIT CODE SBAGLIATO!**

| Exit Code | Significato in Claude Code |
|-----------|---------------------------|
| `0` | OK - permetti l'azione |
| `1` | Errore generico - NON blocca! |
| `2` | **BLOCCO** - impedisce l'azione! |

I nostri hook usavano `sys.exit(1)` per bloccare.
Ma Claude Code richiede `sys.exit(2)` per bloccare!

### Codice sbagliato

```python
# ❌ NON FUNZIONA
sys.exit(1)  # Claude Code ignora, non blocca
```

### Codice corretto

```python
# ✅ FUNZIONA
sys.exit(2)  # Claude Code BLOCCA l'azione
```

---

## File Interessati

1. `~/.claude/hooks/block_edit_non_whitelist.py`
   - Riga 151: `sys.exit(1)` → `sys.exit(2)`

2. `~/.claude/hooks/block_task_for_agents.py`
   - Riga 76: `sys.exit(1)` → `sys.exit(2)`

---

## Come Abbiamo Scoperto

1. Test hook manuale → OK (exit 1 funziona in bash)
2. Test in Claude Code → FALLITO (edit passa)
3. Debug hook aggiunto → Log VUOTO
4. Ricerca documentazione Claude Code → EXIT CODE 2!

---

## Lezione Imparata

**SEMPRE consultare la documentazione ufficiale per i dettagli implementativi!**

Il test manuale (`echo | python hook.py`) NON è sufficiente.
Claude Code ha semantica specifica per exit codes.

---

## Riferimento Documentazione

Da Claude Code docs:

```
Exit code 0: Success - action permitted
Exit code 1: Generic error - action still permitted
Exit code 2: Blocking error - action BLOCKED
```

Per PreToolUse:
- Exit 0 → Tool eseguito
- Exit 2 → Tool BLOCCATO, stderr mostrato a Claude

---

## Fix Applicato

Sessione 116 - 7 Gennaio 2026:
- [x] Documentato problema (questo file)
- [x] Fix block_edit_non_whitelist.py
- [x] Fix block_task_for_agents.py
- [x] Testato hook fixati

---

*"Debug con calma. La fretta è nemica della qualità."*

**Cervella & Rafa** 💙
