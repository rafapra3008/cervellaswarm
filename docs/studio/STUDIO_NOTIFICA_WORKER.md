# STUDIO: Notifica Automatica quando Worker Finisce

**Data:** 5 Gennaio 2026
**Autore:** cervella-devops
**Versione:** 1.0.0

---

## Obiettivo

Quando una finestra worker si chiude, la Regina deve ricevere una notifica automatica con:
- Nome del task completato
- Tempo di esecuzione
- Esito (successo/errore)
- Click per aprire l'output (opzionale)

---

## Ricerca: Opzioni Disponibili

### 1. osascript (Nativo macOS)

```bash
osascript -e 'display notification "Messaggio" with title "Titolo" sound name "Glass"'
```

**Pro:**
- Nativo, nessuna installazione richiesta
- Funziona su qualsiasi Mac

**Contro:**
- **Click NON configurabile** - Apre sempre Script Editor
- Nessun controllo sull'azione post-click
- In macOS Sequoia ci sono problemi di compatibilita

**Suoni disponibili:** `/System/Library/Sounds/`
- Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink

### 2. terminal-notifier (Richiede installazione)

```bash
terminal-notifier -title "Titolo" -message "Messaggio" -sound default -open "file:///path/to/file"
```

**Pro:**
- **Click CONFIGURABILE!**
  - `-activate ID` - Apre un'app specifica
  - `-open URL` - Apre un URL/file
  - `-execute COMMAND` - Esegue un comando shell
- Icona personalizzabile
- Supporta gruppi di notifiche

**Contro:**
- Richiede installazione: `brew install terminal-notifier`
- Non presente di default

**Installazione:**
```bash
brew install terminal-notifier
```

---

## Soluzione Proposta: Approccio Ibrido

**DECISIONE:** Usare osascript come default (funziona sempre), con fallback a terminal-notifier se disponibile per click action.

### Implementazione

1. **Tracciare tempo di avvio** (gia fatto con `.start` file)
2. **Al termine, calcolare durata**
3. **Determinare esito** (guardando exit code o presenza .done)
4. **Notifica appropriata:**
   - Se terminal-notifier disponibile: con click per aprire log
   - Altrimenti: osascript semplice

---

## Formato Notifica

```
+------------------------------------------+
|  CervellaSwarm                           |
|                                          |
|  Worker: cervella-backend               |
|  Task: TASK_20260105_123456             |
|  Tempo: 2m 34s                          |
|  Esito: Completato                      |
|                                          |
|  [Click per vedere output]              |
+------------------------------------------+
```

---

## Modifiche a spawn-workers.sh

### Nuova funzione: `notify_worker_completion()`

```bash
notify_worker_completion() {
    local worker_name="$1"
    local start_time="$2"
    local exit_code="$3"
    local log_file="$4"

    # Calcola durata
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))
    local duration_str="${minutes}m ${seconds}s"

    # Determina esito
    local esito="Completato"
    local sound="Glass"
    if [ "$exit_code" -ne 0 ]; then
        esito="ERRORE (exit $exit_code)"
        sound="Basso"
    fi

    # Messaggio
    local message="Worker: ${worker_name}\nTempo: ${duration_str}\nEsito: ${esito}"

    # Prova terminal-notifier, fallback a osascript
    if command -v terminal-notifier &>/dev/null; then
        terminal-notifier \
            -title "CervellaSwarm" \
            -subtitle "Worker terminato" \
            -message "cervella-${worker_name}: ${esito} (${duration_str})" \
            -sound "$sound" \
            -open "file://${log_file}"
    else
        osascript -e "display notification \"cervella-${worker_name}: ${esito} (${duration_str})\" with title \"CervellaSwarm\" sound name \"${sound}\""
    fi
}
```

### Modifiche al runner script

Nel file runner generato, alla fine (prima di chiudere finestra):

```bash
# Salva exit code di Claude
CLAUDE_EXIT=$?

# Calcola durata
START_TIME=$(cat "${SWARM_DIR}/status/worker_${WORKER_NAME}.start" 2>/dev/null || echo "0")
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

# Notifica con dettagli
if command -v terminal-notifier &>/dev/null; then
    terminal-notifier \
        -title "CervellaSwarm" \
        -message "cervella-${WORKER_NAME} terminato (${MINUTES}m ${SECONDS}s)" \
        -sound "Glass" \
        -open "file://${LOG_FILE}"
else
    osascript -e "display notification \"cervella-${WORKER_NAME} terminato (${MINUTES}m ${SECONDS}s)\" with title \"CervellaSwarm\" sound name \"Glass\""
fi
```

---

## Configurazione Opzionale

In `~/.swarm/config`:

```bash
# Notifiche worker
SWARM_NOTIFY_SOUND="Glass"          # Suono successo
SWARM_NOTIFY_ERROR_SOUND="Basso"    # Suono errore
SWARM_NOTIFY_USE_TERMINAL_NOTIFIER=true  # Preferisci terminal-notifier se disponibile
```

---

## Test

```bash
# 1. Test osascript base
osascript -e 'display notification "Test worker terminato (2m 30s)" with title "CervellaSwarm" sound name "Glass"'

# 2. Test terminal-notifier (se installato)
terminal-notifier -title "CervellaSwarm" -message "Test click" -sound Glass -open "file:///tmp/test.log"
```

---

## Conclusioni

| Opzione | Pro | Contro | Raccomandato |
|---------|-----|--------|--------------|
| osascript solo | Nativo, zero setup | No click action | DEFAULT |
| terminal-notifier | Click action! | Richiede brew | OPZIONALE |
| Ibrido | Meglio di entrambi | Logica extra | CONSIGLIATO |

**IMPLEMENTAZIONE:** Approccio ibrido - osascript di default, terminal-notifier se disponibile.

---

## Fonti

- [terminal-notifier GitHub](https://github.com/julienXX/terminal-notifier)
- [macOS Notifications from Terminal](https://swissmacuser.ch/native-macos-notifications-from-terminal-scripts/)
- [Apple Scripting Guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/DisplayNotifications.html)

---

*Studio completato da cervella-devops - 5 Gennaio 2026*
