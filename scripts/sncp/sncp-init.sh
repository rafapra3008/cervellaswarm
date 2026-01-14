#!/bin/bash
# ==============================================================================
# SNCP-INIT - Wizard per inizializzare un nuovo progetto SNCP
# ==============================================================================
#
# Uso:
#   sncp-init nome-progetto            # Crea struttura in .sncp/progetti/nome-progetto/
#   sncp-init nome-progetto --analyze  # Analizza codebase e genera CONFIG.md smart
#
# Crea:
#   - stato.md (stato attuale progetto)
#   - CONFIG.md (configurazione progetto)
#   - decisioni/
#   - roadmaps/
#   - handoff/
#
# Versione: 1.0.0
# Data: 14 Gennaio 2026
# Cervella & Rafa
# ==============================================================================

set -e

# ==============================================================================
# CONFIG
# ==============================================================================

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
TODAY=$(date +%Y-%m-%d)
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ==============================================================================
# FUNCTIONS
# ==============================================================================

print_header() {
    echo ""
    echo -e "${PURPLE}+================================================================+${NC}"
    echo -e "${PURPLE}|                  SNCP-INIT WIZARD v$VERSION                     |${NC}"
    echo -e "${PURPLE}|            \"La memoria e' il fondamento\"                       |${NC}"
    echo -e "${PURPLE}+================================================================+${NC}"
    echo ""
}

print_usage() {
    echo "Uso: sncp-init <nome-progetto> [opzioni]"
    echo ""
    echo "Opzioni:"
    echo "  --analyze    Analizza codebase e genera CONFIG.md intelligente"
    echo "  --help       Mostra questo messaggio"
    echo ""
    echo "Esempi:"
    echo "  sncp-init mio-progetto"
    echo "  sncp-init mio-progetto --analyze"
    echo ""
}

detect_stack() {
    local project_path="$1"
    local stack=""

    # Detect Backend
    if [ -f "$project_path/requirements.txt" ] || [ -f "$project_path/pyproject.toml" ]; then
        stack="${stack}Python, "
        if grep -q "fastapi" "$project_path/requirements.txt" 2>/dev/null || \
           grep -q "fastapi" "$project_path/pyproject.toml" 2>/dev/null; then
            stack="${stack}FastAPI, "
        fi
        if grep -q "django" "$project_path/requirements.txt" 2>/dev/null; then
            stack="${stack}Django, "
        fi
    fi

    # Detect Frontend
    if [ -f "$project_path/package.json" ]; then
        stack="${stack}Node.js, "
        if grep -q '"react"' "$project_path/package.json" 2>/dev/null; then
            stack="${stack}React, "
        fi
        if grep -q '"next"' "$project_path/package.json" 2>/dev/null; then
            stack="${stack}Next.js, "
        fi
        if grep -q '"vue"' "$project_path/package.json" 2>/dev/null; then
            stack="${stack}Vue.js, "
        fi
        if grep -q '"typescript"' "$project_path/package.json" 2>/dev/null; then
            stack="${stack}TypeScript, "
        fi
    fi

    # Detect Database
    if [ -d "$project_path/migrations" ] || \
       grep -rq "postgres\|postgresql" "$project_path" 2>/dev/null; then
        stack="${stack}PostgreSQL, "
    fi
    if grep -rq "sqlite" "$project_path" 2>/dev/null; then
        stack="${stack}SQLite, "
    fi

    # Remove trailing comma and space
    stack="${stack%, }"

    if [ -z "$stack" ]; then
        stack="[da compilare]"
    fi

    echo "$stack"
}

detect_deploy() {
    local project_path="$1"
    local deploy=""

    if [ -f "$project_path/Dockerfile" ] || [ -f "$project_path/docker-compose.yml" ]; then
        deploy="${deploy}Docker, "
    fi
    if [ -f "$project_path/vercel.json" ] || [ -d "$project_path/.vercel" ]; then
        deploy="${deploy}Vercel, "
    fi
    if [ -f "$project_path/netlify.toml" ]; then
        deploy="${deploy}Netlify, "
    fi
    if [ -d "$project_path/.github/workflows" ]; then
        deploy="${deploy}GitHub Actions, "
    fi
    if grep -rq "cloud run\|cloudrun" "$project_path" 2>/dev/null; then
        deploy="${deploy}Cloud Run, "
    fi

    deploy="${deploy%, }"

    if [ -z "$deploy" ]; then
        deploy="[da configurare]"
    fi

    echo "$deploy"
}

create_stato_md() {
    local project_name="$1"
    local base_path="$2"
    local stack="$3"
    local deploy="$4"

    cat > "$base_path/stato.md" << EOF
# Stato - $project_name

> **Ultimo aggiornamento:** $TODAY
> **Score:** [?/10] - Da valutare
> **Sessione:** 1 - Setup SNCP

---

## TL;DR

[Cosa fa questo progetto in 2-3 righe]

---

## STACK

| Tipo | Tecnologia |
|------|------------|
| Backend | $stack |
| Frontend | [?] |
| Database | [?] |
| Deploy | $deploy |

---

## STATO ATTUALE

\`\`\`
+================================================================+
|                                                                |
|   PROGETTO APPENA INIZIALIZZATO CON SNCP                       |
|                                                                |
|   - Struttura SNCP creata                                      |
|   - stato.md pronto                                            |
|   - CONFIG.md da compilare                                     |
|                                                                |
+================================================================+
\`\`\`

### Cosa Funziona

- [ ] [feature 1]
- [ ] [feature 2]

### Cosa Manca

- [ ] [todo 1]
- [ ] [todo 2]

---

## PROSSIMI STEP

1. [ ] Compilare questo stato.md con info reali
2. [ ] Compilare CONFIG.md
3. [ ] Definire roadmap
4. [ ] Iniziare lavoro!

---

## DECISIONI CHIAVE

| Data | Decisione | Perche | Link |
|------|-----------|--------|------|
| $TODAY | Setup SNCP | Memoria persistente | - |

---

## NOTE SESSION

### $TODAY - Setup

- Struttura SNCP inizializzata con sncp-init
- Da compilare: stack, stato, roadmap

---

*"SNCP funziona solo se lo VIVIAMO!"*

EOF
}

create_config_md() {
    local project_name="$1"
    local base_path="$2"
    local project_path="$3"
    local stack="$4"
    local deploy="$5"

    cat > "$base_path/CONFIG.md" << EOF
# CONFIG - $project_name

> Configurazione progetto per CervellaSwarm
> Ispirato a CLAUDE.md best practices

---

## QUICK FACTS

| Cosa | Valore |
|------|--------|
| **Nome** | $project_name |
| **Stack** | $stack |
| **Repo** | $project_path |
| **Deploy** | $deploy |
| **SNCP Path** | .sncp/progetti/$project_name/ |

---

## CONVENZIONI

### Codice

- [convenzione 1]
- [convenzione 2]

### Naming

- File: \`snake_case.py\`, \`kebab-case.tsx\`
- Variabili: \`camelCase\` (JS/TS), \`snake_case\` (Python)
- Componenti: \`PascalCase\`

### Git

- Commit: \`[tipo]: descrizione breve\`
- Tipi: feat, fix, docs, refactor, test, chore
- Branch: \`feature/nome\`, \`fix/nome\`

---

## COMANDI UTILI

\`\`\`bash
# Development
[comando dev]

# Testing
[comando test]

# Build
[comando build]

# Deploy
[comando deploy]
\`\`\`

---

## STRUTTURA CHIAVE

\`\`\`
$project_name/
├── [cartella principale]/
│   └── [descrizione]
├── [altra cartella]/
│   └── [descrizione]
└── [file importante]
\`\`\`

---

## COSA NON FARE

- [ ] Non committare secrets (.env, credentials)
- [ ] Non pushare senza test
- [ ] Non modificare schema DB senza migration
- [ ] [altro antipattern]

---

## INTEGRAZIONE CERVELLASWARM

### Agenti Consigliati

| Task | Agente |
|------|--------|
| Frontend | cervella-frontend |
| Backend | cervella-backend |
| Database | cervella-data |
| Testing | cervella-tester |
| Review | cervella-reviewer |

### Workflow Tipico

1. Regina analizza task
2. Delega a Worker specializzato
3. Guardiana verifica qualita
4. Update stato.md

---

*Generato da sncp-init v$VERSION*
*$TODAY*

EOF
}

# ==============================================================================
# MAIN
# ==============================================================================

# Parse arguments
PROJECT_NAME=""
ANALYZE_FLAG=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --analyze)
            ANALYZE_FLAG=true
            shift
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        *)
            if [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$1"
            fi
            shift
            ;;
    esac
done

# Validate
if [ -z "$PROJECT_NAME" ]; then
    print_header
    echo -e "${RED}[ERRORE]${NC} Nome progetto richiesto!"
    echo ""
    print_usage
    exit 1
fi

print_header

BASE_PATH="$SNCP_ROOT/progetti/$PROJECT_NAME"

echo -e "${BLUE}[i]${NC} Progetto: ${CYAN}$PROJECT_NAME${NC}"
echo -e "${BLUE}[i]${NC} SNCP Path: ${CYAN}$BASE_PATH${NC}"
echo ""

# Check if already exists
if [ -d "$BASE_PATH" ]; then
    echo -e "${YELLOW}[!]${NC} Progetto gia' esistente!"
    echo ""
    echo "Contenuto attuale:"
    ls -la "$BASE_PATH" 2>/dev/null || echo "  (vuoto)"
    echo ""
    read -p "Vuoi sovrascrivere? (y/n): " response
    if [ "$response" != "y" ]; then
        echo -e "${RED}[X]${NC} Annullato."
        exit 1
    fi
    echo ""
fi

# Try to find project path for analysis
PROJECT_PATH=""
if [ -d "$HOME/Developer/$PROJECT_NAME" ]; then
    PROJECT_PATH="$HOME/Developer/$PROJECT_NAME"
elif [ -d "$(pwd)/$PROJECT_NAME" ]; then
    PROJECT_PATH="$(pwd)/$PROJECT_NAME"
elif [ -d "$(pwd)" ] && [ "$(basename "$(pwd)")" == "$PROJECT_NAME" ]; then
    PROJECT_PATH="$(pwd)"
fi

# Detect stack if analyze flag
STACK="[da compilare]"
DEPLOY="[da configurare]"

if [ "$ANALYZE_FLAG" = true ] && [ -n "$PROJECT_PATH" ] && [ -d "$PROJECT_PATH" ]; then
    echo -e "${BLUE}[i]${NC} Analisi codebase: ${CYAN}$PROJECT_PATH${NC}"
    STACK=$(detect_stack "$PROJECT_PATH")
    DEPLOY=$(detect_deploy "$PROJECT_PATH")
    echo -e "${GREEN}[OK]${NC} Stack rilevato: ${CYAN}$STACK${NC}"
    echo -e "${GREEN}[OK]${NC} Deploy rilevato: ${CYAN}$DEPLOY${NC}"
    echo ""
elif [ "$ANALYZE_FLAG" = true ]; then
    echo -e "${YELLOW}[!]${NC} Path progetto non trovato, skip analisi automatica"
    echo ""
fi

# Create structure
echo -e "${BLUE}[i]${NC} Creazione struttura..."

mkdir -p "$BASE_PATH/decisioni"
mkdir -p "$BASE_PATH/roadmaps"
mkdir -p "$BASE_PATH/handoff"

echo -e "${GREEN}[OK]${NC} Cartelle create"

# Create stato.md
create_stato_md "$PROJECT_NAME" "$BASE_PATH" "$STACK" "$DEPLOY"
echo -e "${GREEN}[OK]${NC} stato.md creato"

# Create CONFIG.md
create_config_md "$PROJECT_NAME" "$BASE_PATH" "$PROJECT_PATH" "$STACK" "$DEPLOY"
echo -e "${GREEN}[OK]${NC} CONFIG.md creato"

# Summary
echo ""
echo -e "${PURPLE}+================================================================+${NC}"
echo -e "${PURPLE}|                   INIZIALIZZAZIONE COMPLETATA                  |${NC}"
echo -e "${PURPLE}+================================================================+${NC}"
echo ""
echo -e "${GREEN}Struttura creata:${NC}"
echo ""
echo "  $BASE_PATH/"
echo "  ├── stato.md          <- UNICA fonte di verita"
echo "  ├── CONFIG.md         <- Configurazione progetto"
echo "  ├── decisioni/        <- Decisioni importanti"
echo "  ├── roadmaps/         <- Piani attivi"
echo "  └── handoff/          <- Sessioni parallele"
echo ""
echo -e "${CYAN}PROSSIMI STEP:${NC}"
echo "  1. Compila stato.md con info reali del progetto"
echo "  2. Compila CONFIG.md con convenzioni"
echo "  3. Crea prima roadmap in roadmaps/"
echo "  4. Inizia a lavorare!"
echo ""
echo -e "${BLUE}Comandi utili:${NC}"
echo "  - pre-session-check.sh $PROJECT_NAME   # Check salute SNCP"
echo "  - health-check.sh                      # Check completo"
echo "  - compact-state.sh $PROJECT_NAME       # Compatta se troppo grande"
echo ""
echo -e "${GREEN}SNCP pronto per: $PROJECT_NAME${NC}"
echo ""
echo -e "${PURPLE}\"La memoria e' il fondamento dell'intelligenza collettiva.\"${NC}"
echo ""
