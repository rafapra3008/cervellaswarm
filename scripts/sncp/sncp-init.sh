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
# Versione: 2.0.0
# Data: 3 Febbraio 2026
# Cervella & Rafa
#
# CHANGELOG v2.0.0:
#   - Crea PROMPT_RIPRESA da template
#   - Crea NORD.md nella root del progetto
#   - Crea archivio/ e ricerche/
#   - Naming consistente (underscore)
# ==============================================================================

set -e

# ==============================================================================
# CONFIG
# ==============================================================================

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
TEMPLATES_PATH="${SNCP_ROOT}/../scripts/sncp/templates"
TODAY=$(date +%Y-%m-%d)
VERSION="2.0.0"

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

# Normalizza nome progetto: trattini -> underscore, minuscolo
normalize_name() {
    local name="$1"
    echo "$name" | tr '-' '_' | tr '[:upper:]' '[:lower:]'
}

# Crea PROMPT_RIPRESA da template
create_prompt_ripresa() {
    local project_name="$1"
    local base_path="$2"
    local normalized_name=$(normalize_name "$project_name")
    local template_file="$TEMPLATES_PATH/PROMPT_RIPRESA_TEMPLATE.md"
    local output_file="$base_path/PROMPT_RIPRESA_${normalized_name}.md"

    if [ -f "$template_file" ]; then
        # Sostituisci placeholder
        sed -e "s/{{NOME_PROGETTO}}/$project_name/g" \
            -e "s/{{DATA}}/$TODAY/g" \
            -e "s/{{NUMERO_SESSIONE}}/1/g" \
            -e "s/{{PROSSIMA_SESSIONE}}/2/g" \
            -e "s/{{STATUS_BREVE}}/Setup SNCP completato/g" \
            -e "s/{{TITOLO_SESSIONE}}/Setup Iniziale/g" \
            -e "s/{{TASK_1}}/Setup SNCP/g" \
            -e "s/{{NOTE_1}}/Struttura creata/g" \
            -e "s/{{TASK_2}}/Compilare stato.md/g" \
            -e "s/{{NOTE_2}}/Da fare/g" \
            -e "s|{{PATH_FILE_1}}|.sncp/progetti/${normalized_name}/stato.md|g" \
            -e "s/{{RIGHE_1}}/~80/g" \
            -e "s/{{DESC_1}}/Stato iniziale/g" \
            -e "s/{{DECISIONE_1}}/Stack tecnico/g" \
            -e "s/{{SCELTA_1}}/[da definire]/g" \
            -e "s/{{MOTIVO_1}}/[da documentare]/g" \
            -e "s/{{FASE_O_FILONE_1}}/SETUP/g" \
            -e "s/{{PERCENTUALE_1}}/100/g" \
            -e "s/{{FASE_O_FILONE_2}}/SVILUPPO/g" \
            -e "s/{{PERCENTUALE_2}}/0/g" \
            -e "s/{{FASE_O_FILONE_3}}/DEPLOY/g" \
            -e "s/{{PERCENTUALE_3}}/0/g" \
            -e "s/{{STEP_1}}/Completare stato.md/g" \
            -e "s/{{DESC_STEP_1}}/Info reali progetto/g" \
            -e "s/{{STEP_2}}/Definire roadmap/g" \
            -e "s/{{DESC_STEP_2}}/Obiettivi e milestone/g" \
            -e "s/{{STEP_3}}/Iniziare sviluppo/g" \
            -e "s/{{DESC_STEP_3}}/Prima feature/g" \
            -e "s/{{N-3}}/--/g" \
            -e "s/{{N-2}}/--/g" \
            -e "s/{{N-1}}/--/g" \
            -e "s/{{N}}/1/g" \
            -e "s/{{RIASSUNTO_SESSIONE_N-3}}/(nessuna)/g" \
            -e "s/{{RIASSUNTO_SESSIONE_N-2}}/(nessuna)/g" \
            -e "s/{{RIASSUNTO_SESSIONE_N-1}}/(nessuna)/g" \
            -e "s/{{RIASSUNTO_SESSIONE_CORRENTE}}/Setup SNCP iniziale/g" \
            -e "s/{{CITAZIONE_MOTIVAZIONALE}}/Ultrapassar os proprios limites!/g" \
            -e "s/{{DESCRIZIONE_RUOLO_FILE}}/[opzionale]/g" \
            -e "s/{{LINK_AD_ALTRI_FILE}}/[opzionale]/g" \
            "$template_file" > "$output_file"
        return 0
    else
        echo -e "${YELLOW}[!]${NC} Template PROMPT_RIPRESA non trovato: $template_file"
        return 1
    fi
}

# Crea NORD.md nella root del progetto
create_nord_md() {
    local project_name="$1"
    local project_path="$2"
    local normalized_name=$(normalize_name "$project_name")
    local template_file="$TEMPLATES_PATH/NORD_TEMPLATE.md"
    local output_file="$project_path/NORD.md"

    if [ -z "$project_path" ] || [ ! -d "$project_path" ]; then
        echo -e "${YELLOW}[!]${NC} Project path non trovato, NORD.md non creato"
        return 1
    fi

    if [ -f "$output_file" ]; then
        echo -e "${YELLOW}[!]${NC} NORD.md gia' esistente in $project_path"
        return 1
    fi

    if [ -f "$template_file" ]; then
        sed -e "s/{{NOME_PROGETTO}}/$project_name/g" \
            -e "s/{{nome_progetto}}/$normalized_name/g" \
            -e "s/{{DATA}}/$TODAY/g" \
            -e "s/{{NUMERO_SESSIONE}}/1/g" \
            -e "s/{{SINTESI_UNA_RIGA}}/[descrizione breve]/g" \
            -e "s/{{DESCRIZIONE_LINEA_1}}/[cosa fa - linea 1]/g" \
            -e "s/{{DESCRIZIONE_LINEA_2}}/[cosa fa - linea 2]/g" \
            -e "s/{{DESCRIZIONE_LINEA_3}}/[cosa fa - linea 3]/g" \
            -e "s/{{CITAZIONE_MOTIVAZIONALE}}/Ultrapassar os proprios limites!/g" \
            -e "s/{{FASE_1}}/SETUP/g" \
            -e "s/{{PERC_1}}/100/g" \
            -e "s/{{FASE_2}}/SVILUPPO/g" \
            -e "s/{{PERC_2}}/0/g" \
            -e "s/{{FASE_3}}/DEPLOY/g" \
            -e "s/{{PERC_3}}/0/g" \
            -e "s/{{COMPONENTE_1}}/[componente 1]/g" \
            -e "s/{{STATUS_1}}/[status]/g" \
            -e "s/{{COMPONENTE_2}}/[componente 2]/g" \
            -e "s/{{STATUS_2}}/[status]/g" \
            -e "s/{{COMPONENTE_3}}/[componente 3]/g" \
            -e "s/{{STATUS_3}}/[status]/g" \
            -e "s/{{DECISIONE_1}}/Setup SNCP/g" \
            -e "s/{{SCELTA_1}}/Attivato/g" \
            -e "s/{{MOTIVO_1}}/Memoria persistente/g" \
            -e "s/{{DATA_1}}/$TODAY/g" \
            -e "s/{{DECISIONE_2}}/[altra decisione]/g" \
            -e "s/{{SCELTA_2}}/[scelta]/g" \
            -e "s/{{MOTIVO_2}}/[motivo]/g" \
            -e "s/{{DATA_2}}/[data]/g" \
            -e "s/{{COSA_1}}/[feature parcheggiata]/g" \
            -e "s/{{MOTIVO_PARCHEGGIO_1}}/[motivo]/g" \
            -e "s/{{DATA_P1}}/[data]/g" \
            -e "s/{{COSA_2}}/[altra feature]/g" \
            -e "s/{{MOTIVO_PARCHEGGIO_2}}/[motivo]/g" \
            -e "s/{{DATA_P2}}/[data]/g" \
            -e "s/{{PUNTATORE_EXTRA_1}}/Roadmap/g" \
            -e "s|{{PATH_1}}|.sncp/progetti/${normalized_name}/roadmaps/|g" \
            -e "s/{{PUNTATORE_EXTRA_2}}/Decisioni/g" \
            -e "s|{{PATH_2}}|.sncp/progetti/${normalized_name}/decisioni/|g" \
            "$template_file" > "$output_file"
        return 0
    else
        echo -e "${YELLOW}[!]${NC} Template NORD.md non trovato: $template_file"
        return 1
    fi
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
mkdir -p "$BASE_PATH/archivio"
mkdir -p "$BASE_PATH/ricerche"

echo -e "${GREEN}[OK]${NC} Cartelle create (6 totali)"

# Create stato.md
create_stato_md "$PROJECT_NAME" "$BASE_PATH" "$STACK" "$DEPLOY"
echo -e "${GREEN}[OK]${NC} stato.md creato"

# Create CONFIG.md
create_config_md "$PROJECT_NAME" "$BASE_PATH" "$PROJECT_PATH" "$STACK" "$DEPLOY"
echo -e "${GREEN}[OK]${NC} CONFIG.md creato"

# Create PROMPT_RIPRESA (v2.0.0)
NORMALIZED_NAME=$(normalize_name "$PROJECT_NAME")
if create_prompt_ripresa "$PROJECT_NAME" "$BASE_PATH"; then
    echo -e "${GREEN}[OK]${NC} PROMPT_RIPRESA_${NORMALIZED_NAME}.md creato"
else
    echo -e "${YELLOW}[!]${NC} PROMPT_RIPRESA non creato (template mancante)"
fi

# Create NORD.md in project root (v2.0.0)
if [ -n "$PROJECT_PATH" ] && [ -d "$PROJECT_PATH" ]; then
    if create_nord_md "$PROJECT_NAME" "$PROJECT_PATH"; then
        echo -e "${GREEN}[OK]${NC} NORD.md creato in $PROJECT_PATH"
    fi
else
    echo -e "${YELLOW}[!]${NC} NORD.md non creato (project path non trovato)"
    echo -e "${CYAN}[TIP]${NC} Crea manualmente NORD.md nella root del progetto"
fi

# Summary
echo ""
echo -e "${PURPLE}+================================================================+${NC}"
echo -e "${PURPLE}|              INIZIALIZZAZIONE COMPLETATA v$VERSION               |${NC}"
echo -e "${PURPLE}+================================================================+${NC}"
echo ""
echo -e "${GREEN}Struttura SNCP creata:${NC}"
echo ""
echo "  $BASE_PATH/"
echo "  ├── PROMPT_RIPRESA_${NORMALIZED_NAME}.md  <- Stato sessioni (LEGGI QUESTO!)"
echo "  ├── stato.md                        <- Stato tecnico progetto"
echo "  ├── CONFIG.md                       <- Configurazione e convenzioni"
echo "  ├── decisioni/                      <- Decisioni importanti"
echo "  ├── roadmaps/                       <- Piani e subroadmap"
echo "  ├── handoff/                        <- Sessioni parallele"
echo "  ├── archivio/                       <- Sessioni vecchie"
echo "  └── ricerche/                       <- Studi e analisi"
echo ""
if [ -n "$PROJECT_PATH" ] && [ -f "$PROJECT_PATH/NORD.md" ]; then
    echo -e "${GREEN}NORD.md creato in:${NC}"
    echo "  $PROJECT_PATH/NORD.md  <- LA BUSSOLA (sacro!)"
    echo ""
fi
echo -e "${CYAN}PROSSIMI STEP:${NC}"
echo "  1. Leggi e compila PROMPT_RIPRESA_${NORMALIZED_NAME}.md"
echo "  2. Compila NORD.md con la visione del progetto"
echo "  3. Aggiorna stato.md con info tecniche"
echo "  4. Inizia a lavorare!"
echo ""
echo -e "${BLUE}Comandi utili:${NC}"
echo "  - pre-session-check.sh $PROJECT_NAME   # Check inizio sessione"
echo "  - check-ripresa-size.sh $PROJECT_NAME  # Verifica limiti (150 righe)"
echo "  - health-check.sh                      # Check completo SNCP"
echo ""
echo -e "${GREEN}SNCP v2.0 pronto per: $PROJECT_NAME${NC}"
echo ""
echo -e "${PURPLE}\"La memoria e' il fondamento dell'intelligenza collettiva.\"${NC}"
echo -e "${PURPLE}\"Ultrapassar os proprios limites!\"${NC}"
echo ""
