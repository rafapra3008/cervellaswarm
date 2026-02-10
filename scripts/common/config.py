#!/usr/bin/env python3
"""
CervellaSwarm - Centralized Configuration Constants
====================================================

Costanti di configurazione centralizzate.
Elimina magic numbers sparsi nel codice.

Versione: 1.0.0
Data: 19 Gennaio 2026 - W4 Day 1

USAGE:
    from common.config import SIMILARITY_THRESHOLD, DEFAULT_EVENT_LIMIT

    if score > SIMILARITY_THRESHOLD:
        # Pattern match!
"""

# =============================================================================
# PATTERN DETECTION
# =============================================================================

# Soglia similarita per pattern detection (0.0 - 1.0)
# Usato in: pattern_detector.py, analytics CLI
SIMILARITY_THRESHOLD = 0.7

# Minimo occorrenze per considerare un pattern valido
MIN_PATTERN_OCCURRENCES = 3

# Massimo pattern da mostrare in output
MAX_PATTERNS_DISPLAY = 10


# =============================================================================
# ANALYTICS
# =============================================================================

# Numero default di eventi da mostrare
DEFAULT_EVENT_LIMIT = 10

# Giorni in una settimana (per calcoli retro)
WEEK_DAYS = 7

# Giorni default per analisi recenti
DEFAULT_ANALYSIS_DAYS = 30


# =============================================================================
# DATABASE
# =============================================================================

# Nome file database
DB_FILENAME = "swarm_memory.db"

# Timeout connessione in secondi
DB_TIMEOUT = 30

# Massimo risultati per query
MAX_QUERY_RESULTS = 1000


# =============================================================================
# WORKERS / SWARM
# =============================================================================

# Timeout default per worker (secondi)
WORKER_TIMEOUT = 300  # 5 minuti

# Intervallo check stuck workers (secondi)
STUCK_CHECK_INTERVAL = 120  # 2 minuti

# Delay prima di considerare worker stuck (secondi)
STUCK_THRESHOLD = 1800  # 30 minuti

# Numero massimo worker paralleli
MAX_PARALLEL_WORKERS = 8


# =============================================================================
# OUTPUT / DISPLAY
# =============================================================================

# Larghezza default terminale
DEFAULT_TERMINAL_WIDTH = 80

# Massimo caratteri per riga log
MAX_LOG_LINE_LENGTH = 200

# Formato timestamp
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


# =============================================================================
# VERSIONING
# =============================================================================

# Versione corrente CervellaSwarm
VERSION = "2.0.0-beta"
VERSION_NAME = "W4 Polish"
