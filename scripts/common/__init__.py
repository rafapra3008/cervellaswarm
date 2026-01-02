"""
CervellaSwarm Common Utilities
==============================

Moduli condivisi da tutti gli script dello sciame.
"""

from .paths import (
    # Core functions
    get_agents_path,
    get_data_dir,
    get_db_path,
    get_logs_dir,
    get_scripts_dir,

    # Convenience constants
    PROJECT_ROOT,
    AGENTS_PATH,
    DATA_DIR,
    DB_PATH,
    LOGS_DIR,
    SCRIPTS_DIR,

    # Utility functions
    ensure_data_dir,
    ensure_logs_dir,
    get_agent_file,
    list_agents,
    print_paths,
)

__all__ = [
    # Functions
    'get_agents_path',
    'get_data_dir',
    'get_db_path',
    'get_logs_dir',
    'get_scripts_dir',
    'ensure_data_dir',
    'ensure_logs_dir',
    'get_agent_file',
    'list_agents',
    'print_paths',

    # Constants
    'PROJECT_ROOT',
    'AGENTS_PATH',
    'DATA_DIR',
    'DB_PATH',
    'LOGS_DIR',
    'SCRIPTS_DIR',
]

__version__ = "1.0.0"
