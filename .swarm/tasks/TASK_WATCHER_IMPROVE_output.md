# Output: TASK_WATCHER_IMPROVE

**Worker:** cervella-backend
**Data:** 2026-01-08 10:47
**Stato:** COMPLETATO

## Modifiche Implementate

### File Modificato
`scripts/swarm/watcher-regina.sh` - Aggiornato da v1.4.0 a **v1.5.0**

### 1. Log delle Notifiche

Aggiunta funzione `log_notification()` che scrive in `~/.swarm/notifications.log`:

```bash
log_notification() {
    local msg="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $msg" >> "$NOTIFICATION_LOG"
}
```

Tutte le notifiche ora vengono loggate:
- `TASK_DONE: nome_task`
- `FEEDBACK: tipo - filename`
- `TMUX_DONE: session_name`

### 2. Double Notification (Terminal Bell)

Aggiunto terminal bell prima delle notifiche macOS per attenzione immediata:

```bash
# In sveglia_regina():
printf '\a'
sleep 0.3
printf '\a'

# In notifica_feedback():
printf '\a'
```

### 3. Monitoraggio Sessioni Tmux Headless

Nuova funzione `check_tmux_sessions()` che:
- Controlla ogni 30 secondi le sessioni tmux con prefisso `swarm_`
- Rileva quando una sessione ha terminato (pane_dead=1)
- Notifica con bell + notifica macOS
- Logga l'evento

### 4. Configurazione Aggiornata

Nuove variabili:
```bash
LAST_TMUX_CHECK=0
CHECK_TMUX_INTERVAL=30    # 30 secondi per tmux
NOTIFICATION_LOG="$HOME/.swarm/notifications.log"
```

### 5. Output Avvio Aggiornato

Mostra ora:
- Check tmux: ogni 30s
- Log notifiche: path
- Double bell + notifica macOS
- Sessioni tmux headless terminate

## Verifica

Sintassi bash verificata: OK

## Note

Il file `~/.swarm/notifications.log` viene creato automaticamente.
La directory `~/.swarm/` viene creata se non esiste.

---

*cervella-backend - Sessione 122*
