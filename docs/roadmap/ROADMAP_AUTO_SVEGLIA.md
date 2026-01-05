# ROADMAP AUTO-SVEGLIA REGINA

> *"La MAGIA sopra MAGIA - Regina che si sveglia da sola!"*

**Versione:** 1.0.0
**Data:** 5 Gennaio 2026
**Status:** RICERCA COMPLETATA - Pronta per Implementazione!

---

## IL SOGNO

```
+------------------------------------------------------------------+
|                                                                  |
|   LA VISIONE:                                                    |
|                                                                  |
|   Regina spawna worker → Worker lavora → Worker finisce          |
|                              ↓                                   |
|                    REGINA SVEGLIATA AUTOMATICAMENTE!             |
|                              ↓                                   |
|                    Regina legge output e continua                |
|                                                                  |
|   TUTTO SENZA INTERVENTO UMANO!                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STATO ATTUALE

| Cosa | Status |
|------|--------|
| Ricerca tecnica | COMPLETATA |
| Soluzioni identificate | 5 |
| Soluzione scelta | AppleScript + fswatch |
| Implementazione | DA FARE |

---

## LA SOLUZIONE SCELTA

### AppleScript + fswatch (Keystroke Injection)

```
              +-------------------+
              |      REGINA       |
              | (VS Code Terminal)|
              +-------------------+
                       |
              spawna   |   avvia
                       v
         +-------------+-------------+
         |                           |
         v                           v
  +-----------+              +---------------+
  |  WORKER   |              |    WATCHER    |
  | (backend) |              | (fswatch.sh)  |
  +-----------+              +---------------+
         |                           |
         | crea .done                | rileva .done
         v                           v
  [TASK.done] ----------------> fswatch
                                     |
                                     | AppleScript
                                     | keystroke
                                     v
                              +---------------+
                              | "TASK DONE!"  |
                              | (digitato in  |
                              |  finestra)    |
                              +---------------+
                                     |
                                     v
                              REGINA SVEGLIA!
```

---

## FASI DI IMPLEMENTAZIONE (Una cosa alla volta!)

```
+------------------------------------------------------------------+
|                                                                  |
|   "Una cosa alla volta, con calma, HARDTEST dopo!"              |
|   - Rafa, 5 Gennaio 2026                                         |
|                                                                  |
+------------------------------------------------------------------+
```

---

### FASE 0: Setup Prerequisiti (15 min)

**Obiettivo:** Installare tutto il necessario

**Step:**
1. [ ] Installare fswatch: `brew install fswatch`
2. [ ] Verificare terminal-notifier: `which terminal-notifier`
3. [ ] Abilitare permessi Accessibility

**HARDTEST FASE 0:**
```bash
# Test fswatch installato
fswatch --version
# Deve mostrare versione

# Test terminal-notifier
terminal-notifier -title "Test" -message "Funziona!"
# Deve apparire notifica
```

**Status:** [ ] DA FARE

---

### FASE 1: Watcher Script Base (30 min)

**File:** `scripts/swarm/watcher-regina.sh`

```bash
#!/bin/bash
# watcher-regina.sh - Sveglia la Regina quando i worker finiscono
#
# Uso: ./watcher-regina.sh [watch_dir] [regina_window]
#
# Versione: 1.0.0

WATCH_DIR="${1:-.swarm/tasks}"
REGINA_WINDOW="${2:-Code}"  # VS Code

# Verifica fswatch installato
if ! command -v fswatch &>/dev/null; then
    echo "ERRORE: fswatch non installato!"
    echo "Installa con: brew install fswatch"
    exit 1
fi

echo "[Watcher] Monitoring $WATCH_DIR per file .done..."
echo "[Watcher] Regina window: $REGINA_WINDOW"

fswatch -0 "$WATCH_DIR" | while read -d "" event; do
    if [[ "$event" == *.done ]]; then
        TASK=$(basename "$event" .done)

        echo "[Watcher] Rilevato: $TASK completato!"

        # Notifica macOS
        terminal-notifier -title "CervellaSwarm Watcher" \
            -message "Worker completato: $TASK" \
            -sound Glass 2>/dev/null

        # Sveglia Regina con keystroke
        osascript << EOF
tell application "System Events"
    if exists process "$REGINA_WINDOW" then
        tell application "$REGINA_WINDOW" to activate
        delay 0.5
        tell process "$REGINA_WINDOW"
            keystroke "WORKER COMPLETATO: $TASK - Leggi .swarm/tasks/${TASK}_output.md"
            delay 0.2
            key code 36
        end tell
        return "OK"
    else
        return "Regina non trovata"
    end if
end tell
EOF
    fi
done
```

**Obiettivo:** Creare lo script base che monitora i file .done

**Step:**
1. [ ] Creare file `scripts/swarm/watcher-regina.sh`
2. [ ] Renderlo eseguibile: `chmod +x scripts/swarm/watcher-regina.sh`
3. [ ] Test manuale

**HARDTEST FASE 1:**
```bash
# 1. Avvia watcher in un terminale
./scripts/swarm/watcher-regina.sh

# 2. In un altro terminale, crea un file .done
touch .swarm/tasks/TEST_WATCHER.done

# VERIFICA:
# - Il watcher stampa "Rilevato: TEST_WATCHER completato!"
# - Arriva notifica macOS
# - (Se VS Code aperto) keystroke viene digitato
```

**Status:** [ ] DA FARE

---

### FASE 2: Test AppleScript Isolato (20 min)

**Obiettivo:** Verificare che AppleScript possa digitare in VS Code

**Step:**
1. [ ] Aprire VS Code con Claude attivo
2. [ ] Testare AppleScript manualmente
3. [ ] Verificare permessi Accessibility

**HARDTEST FASE 2:**
```bash
# Con VS Code aperto e in focus, esegui:
osascript << 'EOF'
tell application "Visual Studio Code" to activate
delay 0.5
tell application "System Events"
    tell process "Code"
        keystroke "TEST KEYSTROKE FUNZIONA!"
        delay 0.2
        key code 36
    end tell
end tell
EOF

# VERIFICA:
# - Il testo appare nella finestra VS Code
# - Viene premuto Enter
```

**Se non funziona:**
- System Preferences > Security & Privacy > Accessibility
- Aggiungere Terminal.app (o da dove esegui)

**Status:** [ ] DA FARE

---

### FASE 3: Integrazione spawn-workers (30 min)

**Modifiche a spawn-workers:**

```bash
# In spawn-workers, dopo aver spawnato i worker:

# Avvia watcher in background
if [[ "$AUTO_SVEGLIA" == "true" ]]; then
    scripts/swarm/watcher-regina.sh &
    WATCHER_PID=$!
    echo $WATCHER_PID > .swarm/status/watcher.pid
    print_info "Watcher AUTO-SVEGLIA avviato (PID: $WATCHER_PID)"
fi
```

**Nuovo flag:**
```bash
spawn-workers --backend --auto-sveglia
```

**Obiettivo:** Integrare watcher in spawn-workers con flag opzionale

**Step:**
1. [ ] Aggiungere parsing flag `--auto-sveglia`
2. [ ] Avviare watcher in background quando flag presente
3. [ ] Salvare PID watcher per cleanup

**HARDTEST FASE 3:**
```bash
# Avvia worker con auto-sveglia
spawn-workers --docs --auto-sveglia

# VERIFICA:
# - Worker si avvia
# - Messaggio "Watcher AUTO-SVEGLIA avviato"
# - File .swarm/status/watcher.pid esiste

# Crea task test
echo "Test" > .swarm/tasks/TASK_TEST.md
touch .swarm/tasks/TASK_TEST.ready

# Quando worker finisce:
# - Watcher rileva .done
# - Notifica arriva
# - Keystroke in VS Code!
```

**Status:** [ ] DA FARE

---

### FASE 4: HARDTEST FINALE End-to-End (30 min)

**Obiettivo:** Test completo del flusso AUTO-SVEGLIA

**Scenario:**
1. Regina (tu, Cervella) spawna worker con `--auto-sveglia`
2. Worker lavora e completa
3. Watcher rileva .done
4. AppleScript digita nella finestra Regina
5. Regina riceve il messaggio e continua!

**HARDTEST FASE 4:**

| Test | Descrizione | Risultato Atteso | Status |
|------|-------------|------------------|--------|
| T1 | Singolo worker docs | Keystroke arriva in VS Code | [ ] |
| T2 | Due worker paralleli | Due keystroke, uno per worker | [ ] |
| T3 | Worker fallisce | Notifica errore, no keystroke | [ ] |
| T4 | VS Code non in focus | Viene portato in focus, poi keystroke | [ ] |

**Status:** [ ] DA FARE

---

### FASE 5: Documentazione e Cleanup (15 min)

**Obiettivo:** Documentare tutto e pulire

**Step:**
1. [ ] Aggiornare README spawn-workers con --auto-sveglia
2. [ ] Aggiungere a SWARM_RULES.md
3. [ ] Cleanup file test

**Status:** [ ] DA FARE

---

### FASE 6: Feature Request Anthropic (Futuro)

Aprire issue su GitHub per richiedere supporto nativo:

**Titolo:** `[FEATURE] Push notifications from background processes to Claude session`

**Contenuto:**
```
Use Case: Multi-agent orchestration where a "queen" Claude spawns
worker processes. When workers complete, the queen should be
notified automatically.

Current workaround: AppleScript keystroke injection (fragile)

Proposed solutions:
1. New hook type: "BackgroundNotification"
2. MCP push capability
3. stdin injection for running sessions
```

---

## LIMITAZIONI CONOSCIUTE

### Cosa NON funzionera:
1. Se la finestra Regina non e' identificabile
2. Se ci sono multiple finestre VS Code
3. Se i permessi Accessibility non sono concessi
4. Se la Regina sta gia' scrivendo quando arriva la sveglia

### Mitigazioni:
- Usare naming convention per finestre
- Notifica ANCHE con terminal-notifier (backup visivo)
- Documentare setup permessi

---

## TIMELINE (Una cosa alla volta!)

| Fase | Cosa | Tempo | Status |
|------|------|-------|--------|
| **0** | Setup Prerequisiti | 15 min | [ ] DA FARE |
| **1** | Watcher Script Base | 30 min | [ ] DA FARE |
| **2** | Test AppleScript Isolato | 20 min | [ ] DA FARE |
| **3** | Integrazione spawn-workers | 30 min | [ ] DA FARE |
| **4** | HARDTEST End-to-End | 30 min | [ ] DA FARE |
| **5** | Documentazione | 15 min | [ ] DA FARE |
| **6** | Feature Request Anthropic | 15 min | [ ] FUTURO |

**Totale: ~2.5 ore di lavoro**

```
+------------------------------------------------------------------+
|                                                                  |
|   REGOLA: Una fase alla volta!                                  |
|   Ogni fase ha il suo HARDTEST.                                 |
|   Non passare alla fase successiva se HARDTEST non passa!       |
|                                                                  |
+------------------------------------------------------------------+
```

---

## DIPENDENZE

```bash
# Installare prima:
brew install fswatch
brew install terminal-notifier  # gia' installato!

# Permessi macOS:
# System Preferences > Security & Privacy > Privacy > Accessibility
# Aggiungere: Terminal.app (o iTerm) e Visual Studio Code
```

---

## QUANDO IMPLEMENTARE?

Questa feature e' OPZIONALE ma POTENTE.

**Raccomandazione:**
- Implementare DOPO aver usato lo Swarm in produzione su Miracollo
- Capire prima se il workflow "Rafa come dispatcher" funziona
- Se diventa tedioso → implementare AUTO-SVEGLIA

---

## RIFERIMENTI

- Output ricerca: `.swarm/tasks/TASK_RICERCA_AUTO_SVEGLIA_REGINA_output.md`
- fswatch: https://github.com/emcrisostomo/fswatch
- AppleScript System Events: https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/

---

*"La MAGIA sopra MAGIA - quando sara' pronta, sara' INCREDIBILE!"*

Cervella & Rafa
