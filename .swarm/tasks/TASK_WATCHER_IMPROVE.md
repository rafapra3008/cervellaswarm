# Task: Migliorare Watcher Regina per Headless

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorità:** MEDIA
**Data:** 2026-01-08

## Obiettivo

Migliorare watcher-regina.sh per supportare meglio il modo headless e garantire notifiche affidabili.

## File da Modificare

`scripts/swarm/watcher-regina.sh` (versione attuale: 1.4.0)

## Miglioramenti

### 1. Aggiungere log delle notifiche

Dopo ogni notifica, loggare in `~/.swarm/notifications.log`:

```bash
log_notification() {
    local msg="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $msg" >> ~/.swarm/notifications.log
}
```

### 2. Double notification per affidabilità

Aggiungere terminal bell oltre alla notifica macOS:

```bash
sveglia_regina() {
    local task_name="$1"

    # Terminal bell (attenzione immediata)
    printf '\a'
    sleep 0.3
    printf '\a'

    # Log
    log_notification "TASK_DONE: $task_name"

    # Notifica macOS...
}
```

### 3. Monitorare sessioni tmux (opzionale)

Aggiungere funzione per check sessioni tmux ogni 30s:

```bash
check_tmux_sessions() {
    # Lista sessioni swarm
    local sessions=$(tmux list-sessions 2>/dev/null | grep "^swarm_" | cut -d: -f1)

    for session in $sessions; do
        # Check se il pane è "dead" (comando terminato)
        local status=$(tmux display-message -t "$session" -p '#{pane_dead}' 2>/dev/null)
        if [ "$status" = "1" ]; then
            echo "Sessione $session terminata"
            log_notification "TMUX_DONE: $session"
        fi
    done
}
```

### 4. Aggiornare versione

```bash
# Versione: 1.5.0
# v1.5.0: HEADLESS SUPPORT! Log notifiche, double bell, tmux monitoring
```

## Output

Scrivi conferma in `TASK_WATCHER_IMPROVE_output.md`

---

*Regina - Sessione 122*
