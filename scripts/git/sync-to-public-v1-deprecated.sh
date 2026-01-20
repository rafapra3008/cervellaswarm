#!/bin/bash
# =============================================================================
# sync-to-public.sh - Sync sicuro da privato a pubblico
# =============================================================================
#
# PROBLEMA RISOLTO:
# - origin (privato) contiene TUTTO (6900+ file)
# - public (pubblico) deve avere SOLO file pubblici
# - git push public main ESPORREBBE file sensibili!
#
# SOLUZIONE:
# Questo script crea commit selettivi per il repo pubblico
#
# USO:
#   ./scripts/git/sync-to-public.sh
#
# LEZIONE APPRESA (Sessione 286):
# "Se vedi questo problema la QUARTA volta, qualcosa è andato storto!"
#
# =============================================================================

set -e

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# File/cartelle PRIVATE (MAI nel public)
PRIVATE_PATTERNS=(
    ".sncp/"
    "NORD.md"
    "docs/studio/"
    "scripts/memory/"
    "scripts/learning/"
    "scripts/engineer/"
    "reports/"
    "data/"
    "*.db"
    "COSTITUZIONE.md"
    "PROMPT_RIPRESA*.md"
    "MAPPA_*.md"
    "MANIFESTO.md"
    "*_PRIVATO*"
    "*_INTERNO*"
)

# File/cartelle PUBBLICHE (da sincronizzare)
PUBLIC_PATTERNS=(
    "packages/"
    "docs/AGENTS_REFERENCE.md"
    "docs/ARCHITECTURE.md"
    "docs/GETTING_STARTED.md"
    "docs/SNCP_GUIDE.md"
    "docs/SEMANTIC_SEARCH.md"
    "docs/ARCHITECT_PATTERN.md"
    "docs/GIT_ATTRIBUTION.md"
    "README.md"
    "CHANGELOG.md"
    "LICENSE"
    "NOTICE"
    "CONTRIBUTING.md"
    ".github/"
    ".gitignore"
)

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  SYNC TO PUBLIC REPO${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

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

# Mostra stato
echo -e "${YELLOW}Remote pubblico:${NC} $(git remote get-url public)"
echo -e "${YELLOW}Branch corrente:${NC} $(git branch --show-current)"
echo ""

# Verifica file sensibili NON siano staged
echo -e "${CYAN}Verifico file sensibili...${NC}"
SENSITIVE_FOUND=0
for pattern in "${PRIVATE_PATTERNS[@]}"; do
    if git ls-files | grep -q "$pattern" 2>/dev/null; then
        echo -e "${YELLOW}  Tracciato (privato): ${pattern}${NC}"
        SENSITIVE_FOUND=1
    fi
done

if [ $SENSITIVE_FOUND -eq 1 ]; then
    echo ""
    echo -e "${GREEN}OK: File sensibili esistono ma NON saranno pushati al public.${NC}"
    echo -e "${GREEN}Il sync usa un commit SELETTIVO.${NC}"
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  FILE CHE SARANNO SINCRONIZZATI${NC}"
echo -e "${CYAN}========================================${NC}"

# Mostra file pubblici che verranno sincronizzati
for pattern in "${PUBLIC_PATTERNS[@]}"; do
    if [ -e "$pattern" ] || ls $pattern &>/dev/null 2>&1; then
        echo -e "${GREEN}  + ${pattern}${NC}"
    fi
done

echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  CONFERMA RICHIESTA${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Stai per sincronizzare i file pubblici al repo:"
echo "  $(git remote get-url public)"
echo ""
echo -e "${RED}ATTENZIONE: Questa operazione è PUBBLICA e visibile a tutti!${NC}"
echo ""
read -p "Vuoi procedere? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Sync annullato.${NC}"
    exit 0
fi

# Crea branch temporaneo per sync
SYNC_BRANCH="sync-public-$(date +%Y%m%d-%H%M%S)"
echo ""
echo -e "${CYAN}Creo branch temporaneo: ${SYNC_BRANCH}${NC}"

# Fetch public
git fetch public

# Checkout public/main in nuovo branch
git checkout -b "$SYNC_BRANCH" public/main

# Copia file pubblici dal main
echo -e "${CYAN}Copio file pubblici...${NC}"
git checkout main -- packages/
git checkout main -- README.md
git checkout main -- CHANGELOG.md
git checkout main -- LICENSE
git checkout main -- CONTRIBUTING.md 2>/dev/null || true
git checkout main -- NOTICE 2>/dev/null || true
git checkout main -- .github/ 2>/dev/null || true
git checkout main -- docs/AGENTS_REFERENCE.md 2>/dev/null || true
git checkout main -- docs/ARCHITECTURE.md 2>/dev/null || true
git checkout main -- docs/GETTING_STARTED.md 2>/dev/null || true
git checkout main -- docs/SNCP_GUIDE.md 2>/dev/null || true
git checkout main -- docs/SEMANTIC_SEARCH.md 2>/dev/null || true
git checkout main -- docs/ARCHITECT_PATTERN.md 2>/dev/null || true
git checkout main -- docs/GIT_ATTRIBUTION.md 2>/dev/null || true

# Verifica finale: nessun file sensibile
echo -e "${CYAN}Verifica finale sicurezza...${NC}"
for pattern in "${PRIVATE_PATTERNS[@]}"; do
    if git status --porcelain | grep -q "$pattern" 2>/dev/null; then
        echo -e "${RED}ERRORE: File sensibile trovato: ${pattern}${NC}"
        echo -e "${RED}Annullo sync per sicurezza!${NC}"
        git checkout main
        git branch -D "$SYNC_BRANCH"
        exit 1
    fi
done

echo -e "${GREEN}Verifica sicurezza: PASSATA${NC}"
echo ""

# Mostra diff
echo -e "${CYAN}Modifiche da committare:${NC}"
git status --short

echo ""
read -p "Confermi commit e push? (yes/no): " confirm2

if [ "$confirm2" != "yes" ]; then
    echo -e "${YELLOW}Sync annullato. Torno a main.${NC}"
    git checkout main
    git branch -D "$SYNC_BRANCH"
    exit 0
fi

# Commit
git add -A
git commit -m "Release v2.0.0-beta - Sync from private

Features:
- W1: Git Flow 2.0 with worker attribution
- W2: Tree-sitter AST parsing with PageRank
- W3: Semantic Search + Architect Pattern
- W4: Polish, test coverage, CI

Co-Authored-By: Cervella <noreply@cervellaswarm.com>"

# Push
echo -e "${CYAN}Push to public...${NC}"
git push public "$SYNC_BRANCH":main

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  SYNC COMPLETATO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Il repo pubblico è stato aggiornato."
echo ""

# Torna a main
git checkout main
git branch -D "$SYNC_BRANCH"

echo -e "${GREEN}Tornato a branch main.${NC}"
echo ""
echo "Prossimi step:"
echo "  1. Verifica su GitHub: https://github.com/rafapra3008/cervellaswarm"
echo "  2. npm publish (se non già fatto)"
echo "  3. Crea tag: git tag v2.0.0-beta && git push public v2.0.0-beta"
