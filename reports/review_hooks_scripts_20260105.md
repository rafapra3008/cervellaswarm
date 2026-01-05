# REVIEW HOOKS E SCRIPTS - 5 Gennaio 2026

**Reviewer:** cervella-reviewer
**Versione Report:** 1.0.0
**Task:** TASK_REVIEW_HOOKS_SCRIPTS

---

## Rating Globale: 8.5/10

Sistema ben strutturato con buone pratiche di modularizzazione. La creazione di `swarm-common.sh` e `~/.swarm/config` dimostra attenzione al DRY. Alcuni problemi di sicurezza e robustezza da correggere.

---

## Problemi ALTI (da fixare subito)

### 1. **[SICUREZZA] Path hardcodato NVM in fallback**
**File:** `~/.swarm/config:52`, `~/.local/lib/swarm-common.sh:161`, `spawn-workers:51`
```bash
elif [[ -f "$HOME/.nvm/versions/node/v24.11.0/bin/claude" ]]; then
```
**Problema:** Versione Node hardcodata (`v24.11.0`). Se l'utente aggiorna Node, il fallback non funziona.
**Soluzione:** Usare glob pattern per trovare qualsiasi versione:
```bash
local nvm_claude=$(ls -t $HOME/.nvm/versions/node/*/bin/claude 2>/dev/null | head -1)
```

### 2. **[SICUREZZA] Escape incompleto in AppleScript**
**File:** `context_check.py:193-204`, `swarm-review.sh:379-381`
**Problema:** L'escape delle virgolette nel prompt non copre tutti i caratteri speciali AppleScript (es. backslash, apostrofi).
```python
safe_prompt = prompt.replace('"', '\\"')  # Insufficiente!
```
**Soluzione:** Aggiungere escape per: `\`, `'`, newlines, tab

### 3. **[SICUREZZA] Command injection potenziale**
**File:** `spawn-workers:438`
```bash
osascript -e "tell application \"Terminal\" to do script \"${runner_script}\""
```
**Problema:** Se `runner_script` contiene caratteri speciali, potrebbe causare comportamenti inattesi.
**Soluzione:** Sanitizzare il path o usare heredoc

---

## Problemi MEDI (da fixare presto)

### 4. **[ROBUSTEZZA] Error handling silenzioso**
**File:** Tutti gli hooks Python
```python
except:
    pass  # Errori nascosti!
```
**Files specifici:**
- `context_check.py:79`, `91`, `206`, `216`
- `pre_compact_save.py:146`, `227-228`
- `session_end_save.py:142`, `174`

**Problema:** Eccezioni catturate e ignorate rendono difficile il debug.
**Soluzione:** Almeno loggare l'errore:
```python
except Exception as e:
    logging.debug(f"Errore ignorato: {e}")
```

### 5. **[DRY] Codice duplicato tra hooks**
**Files:** `pre_compact_save.py`, `session_end_save.py`, `update_prompt_ripresa.py`

Le seguenti funzioni sono IDENTICHE o quasi:
- `detect_project()` - 3 implementazioni
- `get_git_info()` - 2 implementazioni
- `send_notification()` - 2 implementazioni
- `KNOWN_PROJECTS` dict - 3 copie

**Soluzione:** Creare `~/.claude/hooks/common.py` con funzioni condivise

### 6. **[ROBUSTEZZA] Timeout mancanti subprocess**
**File:** `context_check.py:152-156`
```python
subprocess.Popen(
    ["code", "--new-window", str(project_path)],
    ...
)  # Nessun timeout!
```
**Problema:** Se VS Code non risponde, lo script si blocca.
**Soluzione:** Aggiungere timeout o usare `subprocess.run` con timeout

### 7. **[MANUTENIBILITA] Script bash senza shebang coerente**
**Files:** Tutti gli script bash
- `spawn-workers`: `#!/bin/bash` OK
- `swarm-health`: `#!/bin/bash` OK, ma dipende da `swarm-common.sh`

**Problema:** Se `swarm-common.sh` non esiste, `swarm-health` esce con errore criptico.
**Soluzione:** Messaggio di errore piu' chiaro con istruzioni di fix

### 8. **[ROBUSTEZZA] Race condition spawning**
**File:** `spawn-workers:599-600`
```bash
sleep 0.5  # Pausa arbitraria
```
**Problema:** 0.5s potrebbe non bastare su sistemi lenti.
**Soluzione:** Verificare che il processo precedente sia effettivamente avviato

---

## Problemi BASSI (nice to have)

### 9. **[DOCUMENTAZIONE] Versioni inconsistenti**
- `context_check.py`: v4.3.0
- `spawn-workers`: v2.0.0
- `swarm-status`: v1.1.0
- `swarm-review`: v1.1.0
- `swarm-health`: v1.0.0
- `swarm-common.sh`: v1.0.0

**Suggerimento:** Allineare le versioni o documentare il changelog unificato

### 10. **[STILE] Logging inconsistente**
- Alcuni hooks usano `print()` a stderr
- Altri usano `print()` a stdout
- Nessuno usa il modulo `logging` Python

**Suggerimento:** Standardizzare con `logging` module

### 11. **[SICUREZZA MINORE] File temporanei**
**File:** `swarm-review.sh:276`
```bash
local tmp_dir="/tmp/swarm-review-$$"
```
**Problema:** Usando `$$` (PID) c'e' un rischio teorico di race condition.
**Soluzione:** Usare `mktemp -d`

### 12. **[PORTABILITA] stat command**
**Files:** `swarm-status.sh:175-176`, `swarm-review.sh:190-192`
```bash
stat -f %m "$file" 2>/dev/null || stat -c %Y "$file"
```
**OK:** Il fallback per Linux c'e', ma potrebbe essere piu' elegante con una funzione helper

---

## Punti di Forza

### 1. **Architettura Modulare**
- Separazione chiara: config, common lib, scripts specifici
- `~/.swarm/config` centralizza la configurazione
- `swarm-common.sh` evita duplicazione negli script bash

### 2. **Project-Aware Design**
- `find_project_root()` cerca `.swarm/` risalendo le directory
- Funziona da qualsiasi sottodirectory del progetto
- Supporta progetti multipli

### 3. **Graceful Degradation**
- Fallback Terminal.app se VS Code fallisce
- Fallback auto-detect se CLAUDE_BIN non configurato
- Script continuano anche se notifiche falliscono

### 4. **Apple Integration**
- Notifiche macOS native con suoni
- Auto-close finestre Terminal (elegante!)
- AppleScript per interazione VS Code

### 5. **Documentazione Inline**
- Header completi con versione e changelog
- Commenti esplicativi nei punti critici
- Docstrings Python presenti

### 6. **Anti-Compact System**
- `context_check.py` e' sofisticato e ben pensato
- Handoff automatico a 70% contesto
- State file per evitare spam

---

## Raccomandazioni

### Priorita' 1: Sicurezza
1. Fix path NVM hardcodato (glob pattern)
2. Migliorare escape AppleScript
3. Sanitizzare input per osascript

### Priorita' 2: Manutenibilita'
1. Creare `~/.claude/hooks/common.py` per DRY
2. Standardizzare logging con modulo Python
3. Aggiungere logging debug per errori catturati

### Priorita' 3: Robustezza
1. Aggiungere timeout a tutti i subprocess
2. Migliorare error messages
3. Sostituire `sleep` arbitrari con verifica effettiva

### Priorita' 4: Documentazione
1. Creare CHANGELOG.md unificato per sistema hooks
2. Documentare dipendenze (swarm-common.sh, config)
3. Aggiungere README in ~/.claude/hooks/

---

## Checklist Sicurezza

| Check | Status | Note |
|-------|--------|------|
| No secrets hardcodati | OK | Nessun token/password |
| No SQL injection | N/A | No DB queries |
| No command injection | WARN | Escape incompleto AppleScript |
| No path traversal | OK | Path costruiti correttamente |
| Input validation | WARN | JSON input non sempre validato |
| Error handling | WARN | Troppi `except: pass` |

---

## Conclusione

Il sistema hooks e scripts di CervellaSwarm e' **solido e ben progettato**. La recente refactoring con config centralizzata e swarm-common.sh dimostra maturita' del codebase.

I problemi ALTI riguardano principalmente sicurezza (escape caratteri) e robustezza (path hardcodati). Sono tutti risolvibili senza refactoring major.

Il sistema merita un **8.5/10** - funzionale, ben documentato, con margini di miglioramento sulla sicurezza.

---

*Report generato da cervella-reviewer*
*5 Gennaio 2026 - Sessione 89*
*CervellaSwarm Code Review System*
