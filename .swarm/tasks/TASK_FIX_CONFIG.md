# Task: Configurazione Centralizzata + Fix Path Hardcodati

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorità:** ALTA

## Obiettivo

1. Creare file di configurazione centralizzata `~/.swarm/config`
2. Modificare spawn-workers, swarm-status, swarm-review per usare la config
3. Rimuovere tutti i path hardcodati

## Dettagli

### 1. Creare ~/.swarm/config
```bash
# CervellaSwarm Configuration
# Generato automaticamente, modificabile dall'utente

# Progetti da monitorare (uno per riga)
SWARM_PROJECTS=(
    "$HOME/Developer/CervellaSwarm"
    "$HOME/Developer/miracollogeminifocus"
    "$HOME/Developer/ContabilitaAntigravity"
)

# Path Claude CLI (auto-detect se vuoto)
CLAUDE_BIN=""

# Timeout task stale (secondi)
STALE_THRESHOLD=1800

# Notifiche macOS
NOTIFICATIONS_ENABLED=true
NOTIFICATION_SOUND="Glass"
```

### 2. Modificare gli script

**swarm-status (righe 36-40):**
- Rimuovere array PROJECTS hardcodato
- Sourcare ~/.swarm/config
- Usare $SWARM_PROJECTS

**swarm-review (righe 33-37):**
- Stesso approccio

**spawn-workers (riga 368):**
- Rimuovere path NVM hardcodato
- Usare: `CLAUDE_BIN="${CLAUDE_BIN:-$(which claude)}"`

### 3. Aggiungere funzione load_config()
```bash
load_config() {
    local config_file="$HOME/.swarm/config"
    if [[ -f "$config_file" ]]; then
        source "$config_file"
    else
        # Crea config di default
        create_default_config
    fi
}
```

## Output Richiesto

1. File: ~/.swarm/config (creato)
2. File: ~/.local/bin/spawn-workers (modificato)
3. File: ~/.local/bin/swarm-status (modificato)
4. File: ~/.local/bin/swarm-review (modificato)

## Verifica

- [ ] `swarm-status --all` funziona ancora
- [ ] `spawn-workers --backend` funziona ancora
- [ ] Config file creato in ~/.swarm/
- [ ] Nessun path hardcodato rimasto
