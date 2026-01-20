# CervellaSwarm Hooks

> **Ultimo aggiornamento:** 20 Gennaio 2026 - W6 Day 2

Documentazione degli hook disponibili in CervellaSwarm.

---

## Git Hooks

### Pre-Commit Hook

**Path:** `.git/hooks/pre-commit`

Il pre-commit hook esegue 5 verifiche prima di ogni commit:

| Check | Tipo | Descrizione |
|-------|------|-------------|
| 1. Limiti Righe | BLOCCANTE | Verifica che PROMPT_RIPRESA (150) e stato.md (500) rispettino i limiti |
| 2. Naming Convention | BLOCCANTE | Verifica naming corretto per PROMPT_RIPRESA e HANDOFF |
| 3. Docs Sync | WARNING | Verifica che stato.md sia aggiornato quando cambia codice |
| 4. Compliance Marker | WARNING | Verifica marker COSTITUZIONE-APPLIED nei report |
| 5. Syntax Validation | BLOCCANTE | Valida sintassi Python/JS/TS con Tree-sitter |

> **NOTA SNCP 2.0:** oggi.md deprecato (Sessione 297). Usiamo solo PROMPT_RIPRESA + handoff.

---

## Syntax Validation Hook (W6 Day 2)

### validate_syntax.py

**Path:** `hooks/validate_syntax.py`
**Version:** 1.0.0
**Aggiunto:** W6 Day 2 (Sessione 293)

Hook che valida la sintassi dei file staged usando Tree-sitter.

### Linguaggi Supportati

| Estensione | Linguaggio |
|------------|------------|
| `.py` | Python |
| `.ts` | TypeScript |
| `.tsx` | TSX (React) |
| `.js` | JavaScript |
| `.jsx` | JSX (React) |

### Usage

```bash
# Validare file specifici
python hooks/validate_syntax.py file1.py file2.js

# Validare tutti i file staged
python hooks/validate_syntax.py --staged
```

### Exit Codes

| Code | Significato |
|------|-------------|
| 0 | Tutti i file hanno sintassi valida |
| 1 | Uno o piu file hanno errori di sintassi |
| 2 | Errore interno (parser non disponibile, etc.) |

### Esempio Output

**File valido:**
```
>> Validating syntax (1 files)...
  OK: src/main.py
Syntax validation passed
```

**File con errori:**
```
>> Validating syntax (1 files)...
  FAIL: src/broken.py
        Syntax error at line 15, column 8

Syntax validation failed: 1 file(s) with errors
```

### Come Funziona

1. Hook riceve lista file staged (o da argomenti)
2. Filtra solo file con estensioni supportate
3. Per ogni file:
   - Parsa con TreesitterParser
   - Controlla `tree.root_node.has_error`
   - Se errore, trova la posizione nell'AST
4. Ritorna exit code appropriato

### Dipendenze

- `tree-sitter` package
- `tree-sitter-language-pack` package
- `scripts/utils/treesitter_parser.py`

### Disabilitare Temporaneamente

Per saltare la validazione in un commit urgente:

```bash
git commit --no-verify -m "emergency fix"
```

**ATTENZIONE:** Usare solo in emergenza. La validazione esiste per proteggere il codebase.

---

## Claude Hooks

Gli hook per Claude Code sono in `.claude/hooks/`:

| Hook | Quando | Cosa Fa |
|------|--------|---------|
| `session_start_swarm.py` | Inizio sessione | Carica COSTITUZIONE e PROMPT_RIPRESA |
| `file_limits_guard.py` | Pre-edit | Verifica limiti righe |
| `subagent_stop.py` | Fine subagent | Log completamento |

---

*"La qualita e nei dettagli"*
*W6 Day 2 - Cervella*
