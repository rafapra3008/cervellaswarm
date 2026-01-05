# RICERCA: Auto-Sveglia Regina - Output Completo

**Data:** 5 Gennaio 2026
**Ricercatore:** cervella-researcher
**Sessione:** 95 - CervellaSwarm

---

## Executive Summary

Dopo un'analisi approfondita di hooks, MCP, stdin/IPC e meccanismi di automazione macOS, la conclusione e':

**NON esiste un modo nativo per "svegliare" una Regina Claude in attesa.**

Claude Code e' progettato come un sistema **PULL-based**: Claude chiede, gli strumenti rispondono. Non esiste un canale **PUSH** dove un worker puo' iniettare messaggi in una sessione Claude in esecuzione.

TUTTAVIA, esistono **workaround creativi** che possono simulare questo comportamento!

---

## 1. Analisi Tecnica - Come Funziona Claude Code

### Architettura Fondamentale

```
+-------------------+     PULL     +------------------+
|   Claude Code     | <----------> |   Tools/MCP     |
|   (richiede)      |              |   (risponde)    |
+-------------------+              +------------------+
        |
        | BLOCCATO IN ATTESA
        | di input utente
        v
   [Prompt utente] --> Unico modo per procedere
```

### Hook System

| Hook | Trigger | Puo' Svegliare? |
|------|---------|-----------------|
| SessionStart | Avvio sessione | NO - solo aggiunge contesto |
| SessionEnd | Fine sessione | NO |
| UserPromptSubmit | Utente invia messaggio | NO - Claude e' gia' sveglio |
| PreCompact | Prima di compattare | NO |
| PostToolUse | Dopo uso tool | NO |

**Limitazione critica:** Gli hook possono solo AGGIUNGERE contesto quando Claude e' gia' attivo. Non possono ATTIVARE Claude.

### MCP (Model Context Protocol)

MCP e' **bidirezionale** ma Claude deve sempre **iniziare** la comunicazione:
- Claude chiede al server MCP -> Server risponde
- Server MCP NON puo' pushare messaggi a Claude spontaneamente

### stdin/IPC

- Claude Code **NON** legge da stdin dopo l'avvio in modalita' interattiva
- Non esistono named pipes o socket per iniettare messaggi
- Il processo Claude non espone API locali

---

## 2. Soluzioni Possibili

### SOLUZIONE A: AppleScript Keystroke Injection (RACCOMANDATA)

**Come funziona:**
1. Worker finisce -> scrive file `.done`
2. Script esterno (watcher) rileva il file
3. AppleScript simula keystroke nella finestra Claude della Regina
4. Claude riceve il "messaggio" come se l'utente avesse digitato

**Implementazione:**

```bash
#!/bin/bash
# watcher-sveglia-regina.sh

WATCH_DIR=".swarm/tasks"

fswatch -0 "$WATCH_DIR" | while read -d "" event; do
    if [[ "$event" == *.done ]]; then
        TASK_NAME=$(basename "$event" .done)

        # Trova la finestra Regina (per esempio, prima finestra VS Code Claude)
        osascript << EOF
tell application "Visual Studio Code" to activate
delay 0.5
tell application "System Events"
    tell process "Code"
        keystroke "Il task $TASK_NAME e' completato! Leggi l'output."
        delay 0.2
        key code 36 -- Enter
    end tell
end tell
EOF
    fi
done
```

**Pro:**
- Funziona SUBITO con l'architettura attuale
- Nessuna modifica a Claude Code
- Testabile immediatamente

**Contro:**
- Richiede permessi Accessibility
- La finestra deve essere identificabile
- Potrebbe digitare nella finestra sbagliata

**Fattibilita': FACILE**

---

### SOLUZIONE B: Polling con Resume Session

**Come funziona:**
1. Regina spawna worker e salva session_id
2. Regina fa "exit" (chiude Claude)
3. Script esterno fa polling su `.swarm/tasks/*.done`
4. Quando worker finisce, script lancia `claude --resume session_id -p "leggi output"`
5. Claude riprende con il contesto precedente

**Implementazione:**

```bash
#!/bin/bash
# polling-regina.sh

SESSION_ID="$1"
TASK_ID="$2"

while true; do
    if [[ -f ".swarm/tasks/${TASK_ID}.done" ]]; then
        claude --resume "$SESSION_ID" -p "Il worker ha completato $TASK_ID. Leggi .swarm/tasks/${TASK_ID}_output.md e continua."
        break
    fi
    sleep 5
done
```

**Pro:**
- Usa API ufficiale Claude
- Affidabile e prevedibile
- Mantiene contesto sessione

**Contro:**
- La Regina deve fare "exit" - non puo' restare in attesa
- Richiede gestione session_id
- Non e' "sveglia" ma "restart"

**Fattibilita': MEDIA**

---

### SOLUZIONE C: Stream-JSON Bidirectional (Sperimentale)

**Come funziona:**
1. Claude avviato con `--input-format stream-json --output-format stream-json`
2. Script esterno legge/scrive da stdin/stdout
3. Worker finisce -> script inietta messaggio JSON nello stream

**Implementazione (teorica):**

```bash
#!/bin/bash
# Avvia Claude in stream mode
claude -p --input-format stream-json --output-format stream-json &
CLAUDE_PID=$!

# Funzione per iniettare messaggio
inject_message() {
    echo '{"type": "user", "content": "Worker completato: '"$1"'"}' > /proc/$CLAUDE_PID/fd/0
}

# ... logica di watching
```

**Pro:**
- Potenzialmente la soluzione piu' elegante
- Usa canale ufficiale

**Contro:**
- Documentazione scarsa
- Bug noto: stream-json input puo' bloccarsi (Issue #3187)
- Modalita' -p non e' interattiva

**Fattibilita': DIFFICILE** (richiede sperimentazione)

---

### SOLUZIONE D: Due Cervelle che si Parlano

**Come funziona:**
1. Regina spawna worker E un "watcher Claude"
2. Watcher Claude fa polling su file
3. Quando worker finisce, Watcher usa AppleScript per svegliare Regina
4. Due istanze Claude coordinate!

**Pro:**
- Elegante concettualmente
- Il watcher e' intelligente (puo' decidere cosa fare)

**Contro:**
- Overhead di risorse
- Complessita' gestione
- Richiede comunque AppleScript per la "sveglia"

**Fattibilita': MEDIA**

---

### SOLUZIONE E: Custom MCP Server con Long-Polling

**Come funziona:**
1. Creare un MCP server custom
2. La Regina chiama periodicamente `mcp.check_workers()`
3. Il server risponde con lista worker completati
4. Regina agisce sui risultati

**Implementazione parziale:**

```python
# mcp_worker_monitor.py
@server.tool()
async def check_workers():
    """Controlla se ci sono worker completati"""
    completed = []
    for f in Path(".swarm/tasks").glob("*.done"):
        task_id = f.stem
        output_file = f.parent / f"{task_id}_output.md"
        if output_file.exists():
            completed.append({
                "task_id": task_id,
                "output": output_file.read_text()[:500]
            })
    return {"completed": completed}
```

**Pro:**
- Usa architettura MCP ufficiale
- Pulito e modulare

**Contro:**
- La Regina DEVE chiamare il tool (non e' push)
- Richiede reminder periodico alla Regina
- Non e' "sveglia automatica"

**Fattibilita': MEDIA**

---

## 3. Soluzione Raccomandata

### APPROCCIO IBRIDO: AppleScript + fswatch + VS Code

Combinando le migliori parti delle soluzioni A e B:

```
                    +-----------------+
                    |     REGINA      |
                    | (VS Code + Term)|
                    +-----------------+
                            |
                   spawna   |
                            v
              +-------------+-------------+
              |                           |
              v                           v
       +-----------+              +-----------+
       |  WORKER   |              |  WATCHER  |
       | (backend) |              | (fswatch) |
       +-----------+              +-----------+
              |                           |
              | crea .done                | rileva
              v                           v
       [TASK.done]  <---------------  fswatch
                                          |
                                          | AppleScript
                                          v
                                   [Sveglia Regina]
```

### Piano di Implementazione

**Fase 1: Watcher Script (1 ora)**
```bash
# scripts/swarm/watcher-regina.sh

#!/bin/bash
WATCH_DIR="${1:-.swarm/tasks}"
REGINA_WINDOW="${2:-VS Code}"

fswatch -0 "$WATCH_DIR" | while read -d "" event; do
    if [[ "$event" == *.done ]]; then
        TASK=$(basename "$event" .done)

        # Notifica macOS
        terminal-notifier -title "Worker Completato" \
            -message "$TASK e' finito!" \
            -sound Glass

        # Sveglia Regina (keystroke in VS Code terminal)
        osascript << EOF
tell application "System Events"
    if exists process "$REGINA_WINDOW" then
        tell application "$REGINA_WINDOW" to activate
        delay 0.5
        tell process "$REGINA_WINDOW"
            keystroke "WORKER COMPLETATO: $TASK - Leggo output..."
            delay 0.2
            key code 36
        end tell
    end if
end tell
EOF
    fi
done
```

**Fase 2: Integrazione in spawn-workers (30 min)**
- Quando Regina spawna worker, avvia anche il watcher
- Quando tutti i worker finiscono, termina il watcher

**Fase 3: Test e Affinamento (1 ora)**
- Testare con task reali
- Gestire edge cases (finestre multiple, focus)

---

## 4. Limitazioni Conosciute

### Cosa NON si puo' fare:
1. **Iniettare messaggi nel transcript** - Claude Code non lo permette
2. **Push da MCP** - Architettura pull-only
3. **Modificare stdin dopo avvio** - Non supportato
4. **Svegliare Claude senza simulare utente** - Non esiste API

### Edge Cases da Gestire:
- Finestra Regina non trovata
- Multiple finestre VS Code aperte
- Regina gia' occupata quando worker finisce
- Permessi Accessibility non concessi

---

## 5. Roadmap Futura

### Feature Request a Anthropic (Issue da Aprire)

Titolo proposto: **"[FEATURE] Push notifications from background processes to Claude session"**

Contenuto:
```
Use Case: Multi-agent orchestration where a "queen" Claude spawns
worker processes. When workers complete, the queen should be
notified automatically.

Current workaround: AppleScript keystroke injection (fragile)

Proposed solution:
- New hook type: "BackgroundNotification"
- MCP push capability
- Or: stdin injection for running sessions
```

---

## Conclusione

**La soluzione piu' pratica oggi e' AppleScript + fswatch.**

E' un workaround, non una soluzione nativa, ma funziona con l'architettura attuale di Claude Code.

Per il futuro, vale la pena aprire una feature request su GitHub per richiedere un meccanismo nativo di push notification.

---

## Riferimenti

- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [fswatch GitHub](https://github.com/emcrisostomo/fswatch)
- [GitHub Issue #6009 - Pipe to Interactive](https://github.com/anthropics/claude-code/issues/6009)
- [GitHub Issue #3187 - Stream JSON Bug](https://github.com/anthropics/claude-code/issues/3187)

---

*Ricerca completata da cervella-researcher*
*CervellaSwarm Sessione 95*
*"La magia e' nell'automazione!" - Rafa*
