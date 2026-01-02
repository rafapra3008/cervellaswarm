#!/usr/bin/env python3
"""
CervellaSwarm - Centralized Path Management
===========================================

Questo modulo centralizza tutti i path usati dallo sciame.
Supporta override via environment variables per packaging.

Versione: 1.0.0
Data: 2 Gennaio 2026

USAGE:
    from common.paths import AGENTS_PATH, DB_PATH, DATA_DIR

    # Oppure:
    from common.paths import get_db_path, get_agents_path

ENVIRONMENT VARIABLES:
    CERVELLASWARM_AGENTS_PATH  - Override path degli agent files
    CERVELLASWARM_DB_PATH      - Override path del database
    CERVELLASWARM_DATA_DIR     - Override directory data
"""

import os
from pathlib import Path


def _get_project_root() -> Path:
    """
    Trova la root del progetto CervellaSwarm.
    Risale dalla posizione dello script fino a trovare CLAUDE.md o .git
    """
    current = Path(__file__).resolve()

    # Risali fino a trovare un marker del progetto
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists() or (parent / ".git").exists():
            return parent

    # Fallback: 3 livelli su da scripts/common/paths.py
    return current.parent.parent.parent


def _get_home_agents_path() -> Path:
    """Path standard degli agent in ~/.claude/agents/"""
    return Path.home() / ".claude" / "agents"


# =============================================================================
# CORE PATHS (con supporto env vars)
# =============================================================================

def get_agents_path() -> Path:
    """
    Ritorna il path dove sono salvati i file agent (.md).

    Priorita:
    1. CERVELLASWARM_AGENTS_PATH (env var)
    2. ~/.claude/agents/ (default globale)

    Returns:
        Path: Directory contenente i file agent
    """
    env_path = os.getenv("CERVELLASWARM_AGENTS_PATH")
    if env_path:
        return Path(env_path)
    return _get_home_agents_path()


def get_data_dir() -> Path:
    """
    Ritorna la directory dei dati (database, logs, etc).

    Priorita:
    1. CERVELLASWARM_DATA_DIR (env var)
    2. {project_root}/data/ (default)

    Returns:
        Path: Directory dei dati
    """
    env_path = os.getenv("CERVELLASWARM_DATA_DIR")
    if env_path:
        return Path(env_path)
    return _get_project_root() / "data"


def get_db_path() -> Path:
    """
    Ritorna il path del database SQLite swarm_memory.db.

    Priorita:
    1. CERVELLASWARM_DB_PATH (env var) - path completo al file
    2. {data_dir}/swarm_memory.db (default)

    Returns:
        Path: Path al file database
    """
    env_path = os.getenv("CERVELLASWARM_DB_PATH")
    if env_path:
        return Path(env_path)
    return get_data_dir() / "swarm_memory.db"


def get_logs_dir() -> Path:
    """
    Ritorna la directory dei log.

    Returns:
        Path: Directory dei log
    """
    return get_data_dir() / "logs"


def get_scripts_dir() -> Path:
    """
    Ritorna la directory degli script.

    Returns:
        Path: Directory scripts/
    """
    return _get_project_root() / "scripts"


# =============================================================================
# CONVENIENCE CONSTANTS (importabili direttamente)
# =============================================================================

# Questi vengono valutati all'import, quindi non supportano modifiche
# runtime delle env vars. Usare le funzioni se serve dinamismo.

PROJECT_ROOT = _get_project_root()
AGENTS_PATH = get_agents_path()
DATA_DIR = get_data_dir()
DB_PATH = get_db_path()
LOGS_DIR = get_logs_dir()
SCRIPTS_DIR = get_scripts_dir()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def ensure_data_dir() -> Path:
    """
    Assicura che la directory data esista, creandola se necessario.

    Returns:
        Path: Directory data (garantita esistente)
    """
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def ensure_logs_dir() -> Path:
    """
    Assicura che la directory logs esista, creandola se necessario.

    Returns:
        Path: Directory logs (garantita esistente)
    """
    logs_dir = get_logs_dir()
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def get_agent_file(agent_name: str) -> Path:
    """
    Ritorna il path completo di un file agent.

    Args:
        agent_name: Nome dell'agent (es: "frontend", "backend")
                   Accetta sia "frontend" che "cervella-frontend"

    Returns:
        Path: Path al file agent (es: ~/.claude/agents/cervella-frontend.md)
    """
    # Normalizza il nome
    if not agent_name.startswith("cervella-"):
        agent_name = f"cervella-{agent_name}"
    if not agent_name.endswith(".md"):
        agent_name = f"{agent_name}.md"

    return get_agents_path() / agent_name


def list_agents() -> list:
    """
    Lista tutti i file agent disponibili.

    Returns:
        list: Lista di nomi agent (senza cervella- e .md)
    """
    agents_path = get_agents_path()
    if not agents_path.exists():
        return []

    agents = []
    for f in agents_path.glob("cervella-*.md"):
        name = f.stem.replace("cervella-", "")
        agents.append(name)

    return sorted(agents)


# =============================================================================
# DEBUG / INFO
# =============================================================================

def print_paths():
    """Stampa tutti i path configurati (utile per debug)."""
    print("=" * 60)
    print("CervellaSwarm - Path Configuration")
    print("=" * 60)
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"AGENTS_PATH:  {AGENTS_PATH}")
    print(f"DATA_DIR:     {DATA_DIR}")
    print(f"DB_PATH:      {DB_PATH}")
    print(f"LOGS_DIR:     {LOGS_DIR}")
    print(f"SCRIPTS_DIR:  {SCRIPTS_DIR}")
    print("-" * 60)
    print("Environment overrides:")
    print(f"  CERVELLASWARM_AGENTS_PATH: {os.getenv('CERVELLASWARM_AGENTS_PATH', '(not set)')}")
    print(f"  CERVELLASWARM_DB_PATH:     {os.getenv('CERVELLASWARM_DB_PATH', '(not set)')}")
    print(f"  CERVELLASWARM_DATA_DIR:    {os.getenv('CERVELLASWARM_DATA_DIR', '(not set)')}")
    print("=" * 60)


if __name__ == "__main__":
    # Se eseguito direttamente, mostra la configurazione
    print_paths()

    print("\nAgents disponibili:")
    for agent in list_agents():
        print(f"  - {agent}")
