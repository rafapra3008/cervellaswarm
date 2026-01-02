#!/usr/bin/env python3
"""
Database Migration System per CervellaSwarm
============================================

Sistema di versioning del database SQLite che permette upgrade
di schema incrementali senza perdita di dati.

USAGE:
    python migrate.py --status      # Mostra versione attuale
    python migrate.py --dry-run     # Mostra cosa farebbe senza eseguire
    python migrate.py --upgrade     # Applica tutte le migration mancanti
    python migrate.py --rollback    # Torna indietro di 1 versione (se possibile)

STRUCTURE:
    migrations/
    ├── 001_initial.sql
    ├── 002_lessons_learned.sql
    └── 003_error_patterns.sql

Versione: 1.0.0
Data: 2 Gennaio 2026
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-02"

import sqlite3
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Tuple, Optional

# Import path management
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path, ensure_data_dir


# =============================================================================
# PATHS
# =============================================================================

def get_migrations_dir() -> Path:
    """Ritorna la directory delle migration."""
    return Path(__file__).parent / "migrations"


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_current_version(conn: sqlite3.Connection) -> int:
    """
    Legge la versione corrente dello schema dal database.

    Args:
        conn: Connessione al database

    Returns:
        int: Versione corrente (0 se tabella schema_version non esiste)
    """
    cursor = conn.cursor()

    try:
        # Verifica se esiste la tabella schema_version
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='schema_version'
        """)

        if cursor.fetchone() is None:
            # Tabella non esiste = versione 0
            return 0

        # Leggi la versione corrente
        cursor.execute("SELECT version FROM schema_version ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        if row is None:
            return 0

        return row[0]

    except sqlite3.Error:
        return 0


def create_schema_version_table(conn: sqlite3.Connection) -> None:
    """
    Crea la tabella schema_version se non esiste.

    Args:
        conn: Connessione al database
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version INTEGER NOT NULL,
            applied_at TEXT NOT NULL,
            migration_file TEXT NOT NULL,
            description TEXT
        )
    """)

    conn.commit()


def get_available_migrations() -> List[Tuple[int, Path]]:
    """
    Trova tutte le migration disponibili nella directory migrations/.

    Returns:
        List[Tuple[int, Path]]: Lista di tuple (versione, path_file)
                                 ordinata per versione
    """
    migrations_dir = get_migrations_dir()

    if not migrations_dir.exists():
        return []

    migrations = []

    for sql_file in migrations_dir.glob("*.sql"):
        # Estrai numero versione dal nome file (es: "001_initial.sql" -> 1)
        try:
            version = int(sql_file.stem.split("_")[0])
            migrations.append((version, sql_file))
        except (ValueError, IndexError):
            # Ignora file con nome non valido
            continue

    # Ordina per versione
    migrations.sort(key=lambda x: x[0])

    return migrations


def apply_migration(conn: sqlite3.Connection, migration_file: Path) -> bool:
    """
    Applica una singola migration e aggiorna la versione.

    Args:
        conn: Connessione al database
        migration_file: Path al file SQL della migration

    Returns:
        bool: True se successo, False altrimenti
    """
    cursor = conn.cursor()

    try:
        # Leggi il file SQL
        sql_content = migration_file.read_text()

        # Esegui le statement SQL
        cursor.executescript(sql_content)

        # Estrai versione dal nome file
        version = int(migration_file.stem.split("_")[0])

        # Estrai descrizione dal nome file (es: "001_initial.sql" -> "initial")
        description = "_".join(migration_file.stem.split("_")[1:])

        # Aggiorna schema_version
        cursor.execute("""
            INSERT INTO schema_version (version, applied_at, migration_file, description)
            VALUES (?, ?, ?, ?)
        """, (
            version,
            datetime.now(timezone.utc).isoformat(),
            migration_file.name,
            description
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"❌ Errore applicando migration {migration_file.name}: {e}", file=sys.stderr)
        conn.rollback()
        return False


def migrate_to_latest(conn: sqlite3.Connection, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Auto-detect e applica tutte le migration mancanti.

    Args:
        conn: Connessione al database
        dry_run: Se True, mostra solo cosa farebbe senza eseguire

    Returns:
        Tuple[bool, int]: (successo, numero_migration_applicate)
    """
    # Assicura che esista la tabella schema_version
    if not dry_run:
        create_schema_version_table(conn)

    current_version = get_current_version(conn)
    available_migrations = get_available_migrations()

    # Filtra solo le migration non ancora applicate
    pending_migrations = [
        (version, path) for version, path in available_migrations
        if version > current_version
    ]

    if not pending_migrations:
        return True, 0

    if dry_run:
        print(f"Would apply {len(pending_migrations)} migration(s):")
        for version, path in pending_migrations:
            print(f"  → {path.name}")
        return True, len(pending_migrations)

    # Applica le migration in ordine
    applied_count = 0
    for version, migration_path in pending_migrations:
        print(f"  → Applying {migration_path.name}...", end=" ", file=sys.stderr)

        if apply_migration(conn, migration_path):
            print("✅", file=sys.stderr)
            applied_count += 1
        else:
            print("❌", file=sys.stderr)
            return False, applied_count

    return True, applied_count


def rollback_last_migration(conn: sqlite3.Connection) -> bool:
    """
    Torna indietro di 1 versione (se possibile).

    NOTA: Rollback e limitato - SQL non supporta ALTER TABLE DROP COLUMN.
          Questa funzione elimina solo il record da schema_version.

    Args:
        conn: Connessione al database

    Returns:
        bool: True se successo, False altrimenti
    """
    cursor = conn.cursor()

    try:
        # Trova l'ultima migration applicata
        cursor.execute("""
            SELECT id, version, migration_file
            FROM schema_version
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        if row is None:
            print("⚠️  Nessuna migration da annullare", file=sys.stderr)
            return False

        record_id, version, migration_file = row

        # Elimina il record
        cursor.execute("DELETE FROM schema_version WHERE id = ?", (record_id,))
        conn.commit()

        print(f"✅ Rollback completato: {migration_file} (v{version})", file=sys.stderr)
        print(f"⚠️  ATTENZIONE: Le modifiche al database NON sono state annullate!", file=sys.stderr)
        print(f"   Solo il record in schema_version e stato rimosso.", file=sys.stderr)

        return True

    except sqlite3.Error as e:
        print(f"❌ Errore rollback: {e}", file=sys.stderr)
        conn.rollback()
        return False


# =============================================================================
# CLI COMMANDS
# =============================================================================

def cmd_status() -> int:
    """Comando: mostra versione corrente e ultime migration."""
    db_path = get_db_path()

    if not db_path.exists():
        print("Status: DATABASE NON ESISTE")
        print("  Esegui `python migrate.py --upgrade` per creare il database.")
        return 1

    conn = sqlite3.connect(db_path)
    current_version = get_current_version(conn)
    available_migrations = get_available_migrations()

    latest_version = max([v for v, _ in available_migrations]) if available_migrations else 0

    print(f"Current version: {current_version}")
    print(f"Latest version: {latest_version}")

    if current_version == latest_version:
        print("Status: UP TO DATE")
    elif current_version < latest_version:
        pending_count = sum(1 for v, _ in available_migrations if v > current_version)
        print(f"Status: {pending_count} migration(s) available")
    else:
        print("Status: UNKNOWN (version mismatch)")

    # Mostra ultime migration applicate (se la tabella esiste)
    cursor = conn.cursor()

    # Verifica se la tabella schema_version esiste
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='schema_version'
    """)

    if cursor.fetchone() is not None:
        cursor.execute("""
            SELECT version, migration_file, applied_at
            FROM schema_version
            ORDER BY id DESC
            LIMIT 5
        """)

        rows = cursor.fetchall()
        if rows:
            print("\nRecent migrations:")
            for version, migration_file, applied_at in rows:
                # Formatta la data
                try:
                    dt = datetime.fromisoformat(applied_at)
                    date_str = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    date_str = applied_at[:16]

                print(f"  v{version}: {migration_file} ({date_str})")

    conn.close()
    return 0


def cmd_dry_run() -> int:
    """Comando: mostra cosa farebbe --upgrade senza eseguire."""
    db_path = get_db_path()

    if not db_path.exists():
        print("Would create database and apply all migrations:")
        for version, path in get_available_migrations():
            print(f"  → {path.name}")
        return 0

    conn = sqlite3.connect(db_path)
    current_version = get_current_version(conn)

    print(f"Current version: {current_version}")
    print("")

    success, count = migrate_to_latest(conn, dry_run=True)

    if count == 0:
        print("Would apply:")
        print("  ✓ Already at latest version")
    else:
        print(f"\nWould apply {count} migration(s)")

    conn.close()
    return 0 if success else 1


def cmd_upgrade() -> int:
    """Comando: applica tutte le migration mancanti."""
    db_path = get_db_path()

    # Assicura che la directory data esista
    ensure_data_dir()

    # Se DB non esiste, crealo
    if not db_path.exists():
        print(f"Creating new database: {db_path}", file=sys.stderr)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    current_version = get_current_version(conn)
    available_migrations = get_available_migrations()

    if not available_migrations:
        print("❌ Nessuna migration trovata in migrations/", file=sys.stderr)
        conn.close()
        return 1

    latest_version = max([v for v, _ in available_migrations])

    print(f"Migrating from version {current_version} to {latest_version}...", file=sys.stderr)

    success, count = migrate_to_latest(conn, dry_run=False)

    if success:
        if count == 0:
            print("✅ Already at latest version", file=sys.stderr)
        else:
            print(f"✅ Applied {count} migration(s)", file=sys.stderr)
            print(f"Done! Now at version {get_current_version(conn)}", file=sys.stderr)
        conn.close()
        return 0
    else:
        print(f"❌ Migration failed", file=sys.stderr)
        conn.close()
        return 1


def cmd_rollback() -> int:
    """Comando: annulla l'ultima migration."""
    db_path = get_db_path()

    if not db_path.exists():
        print("❌ Database non esiste", file=sys.stderr)
        return 1

    conn = sqlite3.connect(db_path)
    success = rollback_last_migration(conn)
    conn.close()

    return 0 if success else 1


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Database Migration System per CervellaSwarm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python migrate.py --status      # Mostra versione corrente
  python migrate.py --dry-run     # Preview delle migration
  python migrate.py --upgrade     # Applica migration
  python migrate.py --rollback    # Annulla ultima migration
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", action="store_true",
                      help="Mostra versione corrente e stato")
    group.add_argument("--dry-run", action="store_true",
                      help="Mostra cosa farebbe --upgrade senza eseguire")
    group.add_argument("--upgrade", action="store_true",
                      help="Applica tutte le migration mancanti")
    group.add_argument("--rollback", action="store_true",
                      help="Annulla l'ultima migration (LIMITATO)")

    args = parser.parse_args()

    print("🐝 CervellaSwarm - Database Migration System", file=sys.stderr)
    print(f"📅 Version {__version__} ({__version_date__})", file=sys.stderr)
    print("-" * 60, file=sys.stderr)

    if args.status:
        return cmd_status()
    elif args.dry_run:
        return cmd_dry_run()
    elif args.upgrade:
        return cmd_upgrade()
    elif args.rollback:
        return cmd_rollback()

    return 1


if __name__ == "__main__":
    sys.exit(main())
