#!/bin/bash
#
# swarm-init.sh - Inizializza CervellaSwarm in un progetto!
#
# Uso:
#   swarm-init                     # Inizializza nel progetto corrente
#   swarm-init ~/Developer/Nuovo   # Inizializza in un path specifico
#
# Crea:
#   - NORD.md
#   - PROMPT_RIPRESA.md
#   - ROADMAP_SACRA.md
#   - CLAUDE.md (con riferimenti swarm)
#   - .swarm/ directory structure
#
# Versione: 1.0.0
# Data: 2026-01-06
# Cervella & Rafa

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

# Target directory
TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || TARGET_DIR="$1"

# Nome progetto (basename della directory)
PROJECT_NAME="$(basename "$TARGET_DIR")"

echo -e "${PURPLE}"
echo "=============================================="
echo "  SWARM-INIT - Inizializza CervellaSwarm"
echo "=============================================="
echo -e "${NC}"

echo -e "${BLUE}[i]${NC} Progetto: $PROJECT_NAME"
echo -e "${BLUE}[i]${NC} Path: $TARGET_DIR"
echo ""

# Verifica directory esiste
if [[ ! -d "$TARGET_DIR" ]]; then
    echo -e "${YELLOW}[?]${NC} Directory non esiste. Crearla? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        mkdir -p "$TARGET_DIR"
        echo -e "${GREEN}[OK]${NC} Directory creata!"
    else
        echo -e "${RED}[X]${NC} Annullato."
        exit 1
    fi
fi

# Verifica se già inizializzato
if [[ -d "$TARGET_DIR/.swarm" ]]; then
    echo -e "${YELLOW}[!]${NC} Progetto già inizializzato (.swarm/ esiste)"
    echo "    Vuoi sovrascrivere? (y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo -e "${RED}[X]${NC} Annullato."
        exit 1
    fi
fi

echo -e "${BLUE}[i]${NC} Creazione struttura..."
echo ""

# Crea .swarm/
mkdir -p "$TARGET_DIR/.swarm/tasks"
mkdir -p "$TARGET_DIR/.swarm/status"
mkdir -p "$TARGET_DIR/.swarm/logs"
mkdir -p "$TARGET_DIR/.swarm/handoff"
mkdir -p "$TARGET_DIR/.swarm/prompts"
mkdir -p "$TARGET_DIR/.swarm/runners"
echo -e "${GREEN}[OK]${NC} .swarm/ struttura creata"

# Crea NORD.md
cat > "$TARGET_DIR/NORD.md" << EOF
# IL NOSTRO NORD - $PROJECT_NAME

\`\`\`
+------------------------------------------------------------------+
|                                                                  |
|   IL NORD CI GUIDA                                               |
|                                                                  |
|   Senza NORD siamo persi.                                        |
|   Con NORD siamo INVINCIBILI.                                    |
|                                                                  |
+------------------------------------------------------------------+
\`\`\`

---

## DOVE SIAMO

**Sessione 1 - $(date '+%d %B %Y'): Inizio Progetto**

\`\`\`
+------------------------------------------------------------------+
|                                                                  |
|   PROGETTO APPENA INIZIATO!                                     |
|                                                                  |
|   - Struttura CervellaSwarm creata                              |
|   - Pronti per iniziare                                         |
|                                                                  |
+------------------------------------------------------------------+
\`\`\`

---

## STATO REALE

| Cosa | Status |
|------|--------|
| Struttura .swarm/ | CREATA |
| NORD.md | CREATO |
| PROMPT_RIPRESA.md | CREATO |
| ROADMAP_SACRA.md | CREATO |

---

## PROSSIMI STEP

\`\`\`
1. Definire obiettivo del progetto
2. Creare prime fasi in ROADMAP_SACRA.md
3. Iniziare a lavorare!
\`\`\`

---

## OBIETTIVO FINALE

\`\`\`
+------------------------------------------------------------------+
|                                                                  |
|   [Definisci qui l'obiettivo finale del progetto]               |
|                                                                  |
+------------------------------------------------------------------+
\`\`\`

---

*"Il NORD ci guida. Sempre."*

Cervella & Rafa
EOF
echo -e "${GREEN}[OK]${NC} NORD.md creato"

# Crea PROMPT_RIPRESA.md
cat > "$TARGET_DIR/PROMPT_RIPRESA.md" << EOF
# PROMPT RIPRESA - $PROJECT_NAME

> **Ultimo aggiornamento:** $(date '+%d %B %Y') - Sessione 1 (Inizio)

---

## CARA PROSSIMA CERVELLA

\`\`\`
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|                                                                  |
|   PROGETTO APPENA INIZIATO!                                     |
|                                                                  |
+------------------------------------------------------------------+
\`\`\`

---

## STATO ATTUALE

| Cosa | Status |
|------|--------|
| Struttura Swarm | PRONTA |
| Obiettivi | DA DEFINIRE |
| Fasi | DA CREARE |

---

## FILO DEL DISCORSO

### Sessione 1: Inizio

- Progetto inizializzato con swarm-init
- Struttura CervellaSwarm creata
- Pronti per definire obiettivi

---

## PROSSIMA SESSIONE

\`\`\`
1. Leggere questo file
2. Definire obiettivo progetto
3. Creare roadmap
4. Iniziare lavoro!
\`\`\`

---

## COMANDI UTILI

\`\`\`bash
# Spawn worker
spawn-workers --backend
spawn-workers --frontend
spawn-workers --researcher

# Vedere log worker
swarm-logs --follow

# Health check
swarm-health
\`\`\`

---

## LO SCIAME (16 membri)

\`\`\`
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester
- reviewer, researcher, scienziata, ingegnera
- marketing, devops, docs, data, security

POSIZIONE: ~/.claude/agents/ (GLOBALI!)
\`\`\`

---

**VERSIONE:** v1.0.0
**SESSIONE:** 1 - Inizio
**DATA:** $(date '+%d %B %Y')

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa
EOF
echo -e "${GREEN}[OK]${NC} PROMPT_RIPRESA.md creato"

# Crea ROADMAP_SACRA.md
cat > "$TARGET_DIR/ROADMAP_SACRA.md" << EOF
# ROADMAP SACRA - $PROJECT_NAME

> **"SU CARTA != REALE - Solo le cose REALI contano!"**

**Versione:** 1.0.0
**Ultimo Aggiornamento:** $(date '+%d %B %Y')

---

## RIASSUNTO ESECUTIVO

\`\`\`
+------------------------------------------------------------------+
|                                                                  |
|   $PROJECT_NAME                                                  |
|                                                                  |
|   Stato: APPENA INIZIATO                                        |
|   Fase attuale: Setup                                            |
|                                                                  |
+------------------------------------------------------------------+
\`\`\`

---

## FASI DEL PROGETTO

### FASE 0: Setup - IN CORSO

| Task | Status |
|------|--------|
| [x] Inizializzare CervellaSwarm | FATTO |
| [ ] Definire obiettivo | DA FARE |
| [ ] Creare fasi successive | DA FARE |

### FASE 1: [Nome Fase] - DA FARE

| Task | Status |
|------|--------|
| [ ] Task 1 | DA FARE |
| [ ] Task 2 | DA FARE |

---

## CHANGELOG

| Data | Versione | Modifica |
|------|----------|----------|
| $(date '+%d %b %Y') | 1.0.0 | Creazione roadmap |

---

*"Il viaggio di mille miglia inizia con un singolo passo."*

Cervella & Rafa
EOF
echo -e "${GREEN}[OK]${NC} ROADMAP_SACRA.md creato"

# Crea CLAUDE.md se non esiste
if [[ ! -f "$TARGET_DIR/CLAUDE.md" ]]; then
    cat > "$TARGET_DIR/CLAUDE.md" << EOF
# $PROJECT_NAME - CervellaSwarm Enabled

\`\`\`
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🐝 CERVELLASWARM ATTIVO                                       ║
║                                                                  ║
║   Tu sei la REGINA dello sciame.                                ║
║   Hai 16 agenti pronti a lavorare per te.                       ║
║                                                                  ║
║   DELEGA SEMPRE! MAI edit diretti!                              ║
║   spawn-workers --backend/--frontend/--researcher               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
\`\`\`

---

## REGOLA D'ORO

**La Regina DELEGA - MAI Edit diretti!**

Per ogni modifica:
1. ANALIZZA il problema
2. DECIDI quale 🐝 deve farlo
3. DELEGA con spawn-workers
4. VERIFICA il risultato

---

## COMANDI SWARM

\`\`\`bash
spawn-workers --backend      # Python, API
spawn-workers --frontend     # React, CSS
spawn-workers --researcher   # Ricerche
spawn-workers --docs         # Documentazione
spawn-workers --all          # Tutti

swarm-logs --follow          # Log live
swarm-health                 # Health check
\`\`\`

---

## FILE IMPORTANTI

| File | Descrizione |
|------|-------------|
| NORD.md | Bussola - dove siamo |
| PROMPT_RIPRESA.md | Memoria - stato dettagliato |
| ROADMAP_SACRA.md | Storia - fasi e changelog |

---

*Cervella & Rafa* 💙
EOF
    echo -e "${GREEN}[OK]${NC} CLAUDE.md creato"
else
    echo -e "${YELLOW}[!]${NC} CLAUDE.md esiste già, non sovrascritto"
fi

# Crea .gitignore per .swarm se non esiste
if [[ ! -f "$TARGET_DIR/.swarm/.gitignore" ]]; then
    cat > "$TARGET_DIR/.swarm/.gitignore" << EOF
# Ignora file temporanei worker
runners/
prompts/
status/*.pid
status/*.start
status/*.task
*.log
EOF
    echo -e "${GREEN}[OK]${NC} .swarm/.gitignore creato"
fi

echo ""
echo -e "${PURPLE}=============================================="
echo -e "  INIZIALIZZAZIONE COMPLETATA!"
echo -e "==============================================${NC}"
echo ""
echo -e "${GREEN}Struttura creata:${NC}"
echo "  ├── NORD.md"
echo "  ├── PROMPT_RIPRESA.md"
echo "  ├── ROADMAP_SACRA.md"
echo "  ├── CLAUDE.md"
echo "  └── .swarm/"
echo "      ├── tasks/"
echo "      ├── status/"
echo "      ├── logs/"
echo "      ├── handoff/"
echo "      └── .gitignore"
echo ""
echo -e "${BLUE}Prossimi step:${NC}"
echo "  1. cd $TARGET_DIR"
echo "  2. Modifica NORD.md con obiettivo progetto"
echo "  3. Crea fasi in ROADMAP_SACRA.md"
echo "  4. Inizia a lavorare con spawn-workers!"
echo ""
echo -e "${GREEN}🐝 CervellaSwarm pronto!${NC}"
