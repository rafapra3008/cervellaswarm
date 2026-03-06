#!/usr/bin/env python3
"""
CervellaSwarm - Centralized Database Connection
================================================

Connessione centralizzata al database swarm_memory.db.
Elimina duplicazione connect_db() presente in 4+ file.

Versione: 1.0.0
Data: 19 Gennaio 2026 - W4 Day 1

USAGE:
    from common.db import connect_db

    conn = connect_db()
    cursor = conn.cursor()
    # ... usa il database
    conn.close()

NOTA:
    Questo modulo solleva eccezioni invece di usare sys.exit().
    Il chiamante decide come gestire gli errori.
"""

import sqlite3
from pathlib import Path
from typing import Optional

from .paths import get_db_path


class DatabaseNotFoundError(Exception):
    """Raised when the swarm_memory.db file is not found."""
    pass


class DatabaseConnectionError(Exception):
    """Raised when connection to database fails."""
    pass


def connect_db() -> sqlite3.Connection:
    """
    Connessione centralizzata al database swarm_memory.db.

    Returns:
        sqlite3.Connection con row_factory = sqlite3.Row

    Raises:
        DatabaseNotFoundError: Se il database non esiste
        DatabaseConnectionError: Se la connessione fallisce

    Example:
        >>> conn = connect_db()
        >>> cursor = conn.cursor()
        >>> cursor.execute("SELECT * FROM events LIMIT 1")
        >>> conn.close()
    """
    db_path = get_db_path()

    if not db_path.exists():
        raise DatabaseNotFoundError(
            f"Database non trovato: {db_path}\n"
            f"Suggerimento: Esegui prima:\n"
            f"  cd scripts/memory && ./init_db.py"
        )

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # Accesso per nome colonna
        return conn
    except sqlite3.Error as e:
        raise DatabaseConnectionError(f"Errore connessione database: {e}")


def connect_db_safe() -> Optional[sqlite3.Connection]:
    """
    Versione safe di connect_db che ritorna None invece di sollevare eccezioni.

    Returns:
        sqlite3.Connection se successo, None se fallisce

    Utile per script che vogliono gestire gracefully l'assenza del database.
    """
    try:
        return connect_db()
    except (DatabaseNotFoundError, DatabaseConnectionError):
        return None


# Alias per compatibilità backward (deprecato)
def get_connection() -> sqlite3.Connection:
    """Alias deprecato per connect_db(). Usa connect_db() invece."""
    return connect_db()
