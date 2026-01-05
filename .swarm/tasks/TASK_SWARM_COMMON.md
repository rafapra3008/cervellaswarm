# Task: Estrarre Codice Comune + Creare swarm-health

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorità:** MEDIA

## Obiettivo

1. Creare `~/.local/lib/swarm-common.sh` con funzioni comuni
2. Modificare gli script per usare swarm-common.sh
3. Creare nuovo comando `swarm-health` per verificare sistema

## Parte 1: swarm-common.sh

Estrarre le funzioni duplicate da swarm-status e swarm-review:

```bash
#!/bin/bash
# swarm-common.sh - Funzioni comuni per CervellaSwarm
# Versione: 1.0.0

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Funzioni output
print_success() { echo -e "${GREEN}[OK]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_info() { echo -e "${BLUE}[i]${NC} $1"; }

# Trova root progetto
find_project_root() {
    local dir="$1"
    local max_levels="${2:-5}"
    local current="$dir"
    
    for ((i=0; i<max_levels; i++)); do
        if [[ -d "$current/.swarm" ]]; then
            echo "$current"
            return 0
        fi
        current="$(dirname "$current")"
    done
    return 1
}

# Calcola tempo passato
time_ago() {
    local timestamp="$1"
    local now=$(date +%s)
    local diff=$((now - timestamp))
    
    if [[ $diff -lt 60 ]]; then
        echo "${diff}s fa"
    elif [[ $diff -lt 3600 ]]; then
        echo "$((diff / 60))m fa"
    else
        echo "$((diff / 3600))h fa"
    fi
}

# Estrae "Assegnato a:" dal task file
get_assigned_to() {
    local file="$1"
    grep -m1 "Assegnato a:" "$file" 2>/dev/null | sed 's/.*: *//' | tr -d '*'
}

# Carica configurazione
load_config() {
    local config_file="$HOME/.swarm/config"
    if [[ -f "$config_file" ]]; then
        source "$config_file"
    fi
}
```

## Parte 2: Modificare script esistenti

Aggiungere all'inizio di spawn-workers, swarm-status, swarm-review:
```bash
# Carica libreria comune
SWARM_LIB="${SWARM_LIB:-$HOME/.local/lib/swarm-common.sh}"
[[ -f "$SWARM_LIB" ]] && source "$SWARM_LIB"
```

Rimuovere le funzioni duplicate (ora sono in swarm-common.sh).

## Parte 3: Creare swarm-health

Nuovo comando `~/.local/bin/swarm-health`:

```bash
#!/bin/bash
# swarm-health - Verifica salute del sistema CervellaSwarm

source "$HOME/.local/lib/swarm-common.sh"
load_config

echo "🏥 SWARM HEALTH CHECK"
echo "===================="

# Check 1: Claude CLI
if command -v claude &>/dev/null; then
    print_success "Claude CLI trovato: $(which claude)"
else
    print_error "Claude CLI non trovato nel PATH"
fi

# Check 2: Config file
if [[ -f "$HOME/.swarm/config" ]]; then
    print_success "Config file: ~/.swarm/config"
else
    print_warning "Config file non trovato (usando defaults)"
fi

# Check 3: Progetti configurati
for project in "${SWARM_PROJECTS[@]}"; do
    if [[ -d "$project/.swarm" ]]; then
        print_success "Progetto OK: $(basename "$project")"
    else
        print_error "Progetto mancante: $project"
    fi
done

# Check 4: Task stale
stale_count=0
for project in "${SWARM_PROJECTS[@]}"; do
    # conta .working vecchi
    ...
done

# Check 5: Spazio disco
...

echo ""
echo "Health check completato!"
```

## Output Richiesto

1. File: ~/.local/lib/swarm-common.sh (nuovo)
2. File: ~/.local/bin/swarm-health (nuovo)
3. File: ~/.local/bin/spawn-workers (modificato - source swarm-common)
4. File: ~/.local/bin/swarm-status (modificato - source swarm-common)
5. File: ~/.local/bin/swarm-review (modificato - source swarm-common)

## Verifica

- [ ] `swarm-health` funziona e mostra stato
- [ ] `swarm-status` funziona ancora
- [ ] `swarm-review` funziona ancora
- [ ] `spawn-workers --backend` funziona ancora
