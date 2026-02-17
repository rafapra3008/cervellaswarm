#!/bin/bash
# =============================================================================
# sync-to-public.sh - Sync SICURO da repo privato a pubblico
# =============================================================================
# Version: 3.0.0 (S363 - Open Source hardening)
#
# COME FUNZIONA:
# 1. Crea worktree temporaneo da public/main
# 2. Copia SOLO file pubblici nella worktree (whitelist)
# 3. Verifica sicurezza: blacklist + CONTENT SCANNING
# 4. Commit e push dalla worktree
# 5. Rimuove worktree
#
# USO:
#   ./scripts/git/sync-to-public.sh [commit-message]
#   ./scripts/git/sync-to-public.sh --dry-run    # Preview senza push
#
# =============================================================================

set -e

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configurazione
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORKTREE_DIR="/tmp/cervellaswarm-public-sync-$$"
WORKTREE_BRANCH="public-sync-temp-$$"
DRY_RUN=0

# Parse arguments
for arg in "$@"; do
    if [ "$arg" = "--dry-run" ]; then
        DRY_RUN=1
        shift
    fi
done

# File/cartelle PUBBLICHE (whitelist - SOLO questi vanno nel public)
PUBLIC_FILES=(
    "packages"
    "README.md"
    "CHANGELOG.md"
    "LICENSE"
    "NOTICE"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "SECURITY.md"
    ".github"
    ".gitignore"
    "docs/AGENTS_REFERENCE.md"
    "docs/ARCHITECTURE.md"
    "docs/GETTING_STARTED.md"
    "docs/SNCP_GUIDE.md"
    "docs/SEMANTIC_SEARCH.md"
    "docs/ARCHITECT_PATTERN.md"
    "docs/GIT_ATTRIBUTION.md"
    "docs/DUAL_REPO_STRATEGY.md"
)

# File che NON DEVONO MAI apparire nella ROOT (blacklist precisa)
BLACKLIST_ROOT_PATHS=(
    ".sncp"
    ".swarm"
    ".mcp.json"
    "NORD.md"
    "COSTITUZIONE.md"
    "MANIFESTO.md"
    "data"
    "reports"
    "logs"
    "config"
    "cervellaswarm-extension"
)

# Pattern che non devono apparire da NESSUNA parte nel nome file
BLACKLIST_FILENAME_PATTERNS=(
    "PROMPT_RIPRESA"
    "MAPPA_"
    "_PRIVATO"
    "_INTERNO"
    "RESEARCH_"
    "RICERCA_"
    "PASSAGGIO_CONSEGNA"
    "HANDOFF_"
    "CREDENZIALI"
)

# Directory che non devono esistere
BLACKLIST_DIRS=(
    "docs/studio"
    "scripts/memory"
    "scripts/learning"
    "scripts/engineer"
    "scripts/cron"
)

# Content patterns that must NOT appear in any published file
# These are scanned INSIDE file content, not filenames
BLACKLIST_CONTENT_PATTERNS=(
    "/Users/rafapra"
    "~/Developer/"
    '$HOME/Developer'
    # NOTE: rafapra3008 is the PUBLIC GitHub username (repo URL) - NOT blacklisted
    # Email is already caught by @gmail.com, local paths by /Users/rafapra
    "@gmail.com"
    "192.168."
    "acct_1"
    "data-frame-476309"
    "miracollogeminifocus"
    "ContabilitaAntigravity"
    "CervellaBrasil"
    "cervellabrasil"
    "chavefy"
    "progetti/cervellacostruzione"
    # NOTE: "contabilita" removed - common Italian word (=accounting), repo name
    # "ContabilitaAntigravity" (above) already catches the private repo name.
    # MCP code uses "contabilita" as SNCP project alias - will be made configurable in F3.
)

cleanup() {
    echo -e "\n${CYAN}Pulizia...${NC}"
    cd "$REPO_ROOT"
    git worktree remove "$WORKTREE_DIR" --force 2>/dev/null || true
    git branch -D "$WORKTREE_BRANCH" 2>/dev/null || true
}

trap cleanup EXIT

# Funzione per copiare escludendo node_modules e dist
copy_excluding() {
    local src="$1"
    local dst="$2"
    
    if [ -d "$src" ]; then
        # Per directory, usa rsync per escludere node_modules e altri
        rsync -a --exclude='node_modules' --exclude='dist' --exclude='.turbo' "$src/" "$dst/"
    else
        cp "$src" "$dst"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

echo -e "${BOLD}${CYAN}"
echo "=============================================="
echo "  SYNC TO PUBLIC - v3.0 (Content Scanning)"
if [ "$DRY_RUN" -eq 1 ]; then
    echo -e "  ${YELLOW}[DRY RUN - no push]${CYAN}"
fi
echo "=============================================="
echo -e "${NC}"

cd "$REPO_ROOT"

# Verifica siamo nel repo giusto
if [ ! -d ".git" ]; then
    echo -e "${RED}ERRORE: Non sei nella root del repo git!${NC}"
    exit 1
fi

# Verifica remote public esiste
if ! git remote get-url public &>/dev/null; then
    echo -e "${RED}ERRORE: Remote 'public' non configurato!${NC}"
    echo "Esegui: git remote add public https://github.com/rafapra3008/cervellaswarm.git"
    exit 1
fi

echo -e "${YELLOW}Repo privato:${NC}  $(git remote get-url origin)"
echo -e "${YELLOW}Repo pubblico:${NC} $(git remote get-url public)"
echo ""

# =============================================================================
# STEP 1: Fetch public e crea worktree
# =============================================================================

echo -e "${CYAN}[1/6] Fetch public/main...${NC}"
git fetch public

echo -e "${CYAN}[2/6] Creo worktree isolato...${NC}"
git worktree add -b "$WORKTREE_BRANCH" "$WORKTREE_DIR" public/main

# =============================================================================
# STEP 2: Copia file pubblici nel worktree (ESCLUDI node_modules)
# =============================================================================

echo -e "${CYAN}[3/6] Copio file pubblici (escludo node_modules/dist)...${NC}"
cd "$WORKTREE_DIR"

for item in "${PUBLIC_FILES[@]}"; do
    src="$REPO_ROOT/$item"
    if [ -e "$src" ]; then
        # Crea directory parent se necessario
        parent_dir=$(dirname "$item")
        if [ "$parent_dir" != "." ]; then
            mkdir -p "$parent_dir"
        fi
        
        # Copia (file o directory)
        if [ -d "$src" ]; then
            rm -rf "$item" 2>/dev/null || true
            mkdir -p "$item"
            copy_excluding "$src" "$item"
            echo -e "  ${GREEN}+${NC} $item/ (esclusi node_modules)"
        else
            cp "$src" "$item"
            echo -e "  ${GREEN}+${NC} $item"
        fi
    fi
done

# =============================================================================
# STEP 3: Verifica sicurezza - NESSUN file privato
# =============================================================================

echo ""
echo -e "${CYAN}[4/6] Verifica sicurezza...${NC}"

SECURITY_FAIL=0

# Check 1: Path nella ROOT che non devono esistere
for item in "${BLACKLIST_ROOT_PATHS[@]}"; do
    if [ -e "$item" ]; then
        echo -e "  ${RED}TROVATO FILE/DIR PRIVATO NELLA ROOT: ${item}${NC}"
        SECURITY_FAIL=1
    fi
done

# Check 2: Pattern nei nomi file (escludi node_modules e .git)
for pattern in "${BLACKLIST_FILENAME_PATTERNS[@]}"; do
    matches=$(find . -path "./node_modules" -prune -o -path "./.git" -prune -o -path "./packages/*/node_modules" -prune -o -name "*${pattern}*" -print 2>/dev/null | /usr/bin/grep -v "^$" || true)
    if [ -n "$matches" ]; then
        echo -e "  ${RED}TROVATO FILE CON PATTERN PRIVATO: ${pattern}${NC}"
        echo "$matches"
        SECURITY_FAIL=1
    fi
done

# Check 3: Directory specifiche che non devono esistere
for dir in "${BLACKLIST_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${RED}TROVATA DIRECTORY PRIVATA: ${dir}${NC}"
        SECURITY_FAIL=1
    fi
done

# Check 4: Verifica che node_modules NON sia stato copiato
if find . -type d -name "node_modules" 2>/dev/null | /usr/bin/grep -q .; then
    echo -e "  ${RED}TROVATO node_modules - non dovrebbe esserci!${NC}"
    SECURITY_FAIL=1
fi

# Check 5: CONTENT SCANNING - cerca pattern sensibili DENTRO i file
echo -e "  ${CYAN}Scanning contenuto file per pattern sensibili...${NC}"
for pattern in "${BLACKLIST_CONTENT_PATTERNS[@]}"; do
    # Search all text files, exclude .git and node_modules
    matches=$(/usr/bin/grep -rl "$pattern" . --include='*.md' --include='*.ts' --include='*.js' --include='*.json' --include='*.py' --include='*.sh' --include='*.toml' --include='*.yaml' --include='*.yml' 2>/dev/null | /usr/bin/grep -v '.git/' || true)
    if [ -n "$matches" ]; then
        echo -e "  ${RED}CONTENUTO SENSIBILE TROVATO: '${pattern}'${NC}"
        echo "$matches" | head -5
        match_count=$(echo "$matches" | wc -l | tr -d ' ')
        if [ "$match_count" -gt 5 ]; then
            echo "  ... e altri $((match_count - 5)) file"
        fi
        SECURITY_FAIL=1
    fi
done

if [ "$SECURITY_FAIL" -eq 1 ]; then
    echo ""
    echo -e "${RED}=============================================="
    echo -e "  SICUREZZA FALLITA! Sync annullato."
    echo -e "  Correggere i file sopra prima di sync."
    echo -e "==============================================${NC}"
    exit 1
fi

echo -e "  ${GREEN}OK - Nessun file privato o contenuto sensibile trovato${NC}"

# =============================================================================
# STEP 4: Mostra diff e chiedi conferma
# =============================================================================

echo ""
echo -e "${CYAN}[5/6] Modifiche da sincronizzare:${NC}"
git add -A

# Mostra solo file modificati (non tutti)
CHANGES=$(git status --porcelain | wc -l | tr -d ' ')

if [ "$CHANGES" -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}Nessuna modifica da sincronizzare.${NC}"
    echo "Il repo pubblico e gia aggiornato."
    exit 0
fi

# Mostra summary
echo ""
echo "File modificati: $(git status --porcelain | /usr/bin/grep '^M' | wc -l | tr -d ' ')"
echo "File aggiunti:   $(git status --porcelain | /usr/bin/grep '^A' | wc -l | tr -d ' ')"
echo "File eliminati:  $(git status --porcelain | /usr/bin/grep '^D' | wc -l | tr -d ' ')"
echo ""

# Mostra solo primi 20 file
echo "Prime 20 modifiche:"
git status --short | head -20
if [ "$CHANGES" -gt 20 ]; then
    echo "... e altri $((CHANGES - 20)) file"
fi

echo ""
echo -e "${YELLOW}=============================================="
echo -e "  TOTALE: $CHANGES file da sincronizzare"
echo -e "==============================================${NC}"
echo ""
echo "Stai per pushare al repo PUBBLICO:"
echo "  $(git remote get-url public 2>/dev/null || echo 'public')"
echo ""

# Messaggio commit
if [ -n "$1" ]; then
    COMMIT_MSG="$1"
else
    # Default: leggi versione da package.json se esiste
    if [ -f "packages/cli/package.json" ]; then
        VERSION=$(cat packages/cli/package.json | /usr/bin/grep '"version"' | head -1 | sed 's/.*"version": "\([^"]*\)".*/\1/')
        COMMIT_MSG="Sync v${VERSION} from private"
    else
        COMMIT_MSG="Sync from private - $(date +%Y-%m-%d)"
    fi
fi

echo -e "Commit message: ${CYAN}${COMMIT_MSG}${NC}"
echo ""

if [ "$DRY_RUN" -eq 1 ]; then
    echo -e "${YELLOW}=============================================="
    echo -e "  DRY RUN COMPLETATO"
    echo -e "  $CHANGES file pronti per sync"
    echo -e "  Sicurezza: PASS (5 check superati)"
    echo -e "==============================================${NC}"
    exit 0
fi

read -p "Vuoi procedere? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Sync annullato.${NC}"
    exit 0
fi

# =============================================================================
# STEP 5: Commit e push
# =============================================================================

echo ""
echo -e "${CYAN}[6/6] Commit e push...${NC}"

# Commit con --no-verify per evitare hook del repo principale
git commit --no-verify -m "$COMMIT_MSG

Co-Authored-By: Cervella <noreply@cervellaswarm.com>"

# Push dal worktree (usa HEAD perche siamo su branch temporaneo)
git push public HEAD:main

# =============================================================================
# DONE
# =============================================================================

echo ""
echo -e "${GREEN}=============================================="
echo -e "  SYNC COMPLETATO!"
echo -e "==============================================${NC}"
echo ""
echo "Il repo pubblico e stato aggiornato."
echo ""
echo "Prossimi step (se release):"
echo "  1. Verifica su GitHub"
echo "  2. npm publish (se necessario)"
echo "  3. Crea tag: git tag vX.Y.Z && git push public vX.Y.Z"
