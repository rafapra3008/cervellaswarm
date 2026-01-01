#!/usr/bin/env python3
"""
Sistema Memoria CervellaSwarm - Inizializzazione Database

Crea il database SQLite con schema ottimizzato per tracciare:
- Eventi degli agenti (task start/complete/fail)
- Lezioni apprese dal team
- Performance e pattern di lavoro
"""

__version__ = "1.1.0"
__version_date__ = "2026-01-01"

import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timezone


def get_db_path() -> Path:
    """Ritorna il path del database."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "swarm_memory.db"


def upgrade_schema(conn: sqlite3.Connection) -> bool:
    """
    Aggiorna lo schema del database con nuove colonne e tabelle.
    Chiamato DOPO init_database() per aggiornamenti incrementali.

    Returns:
        True se successo, False altrimenti
    """
    cursor = conn.cursor()

    try:
        # ===== UPGRADE LESSONS_LEARNED =====
        # Aggiungi nuove colonne se non esistono
        new_columns = [
            ("category", "TEXT"),
            ("severity", "TEXT DEFAULT 'MEDIUM'"),
            ("root_cause", "TEXT"),
            ("prevention", "TEXT"),
            ("time_wasted_minutes", "INTEGER"),
            ("occurrence_count", "INTEGER DEFAULT 1"),
            ("status", "TEXT DEFAULT 'ACTIVE'"),
            ("related_pattern_id", "INTEGER"),
            ("project", "TEXT"),
        ]

        for col_name, col_type in new_columns:
            try:
                cursor.execute(f"ALTER TABLE lessons_learned ADD COLUMN {col_name} {col_type}")
                print(f"  ✅ Colonna aggiunta: {col_name}", file=sys.stderr)
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"  ⏭️  Colonna già esistente: {col_name}", file=sys.stderr)
                else:
                    raise

        # ===== TABELLA ERROR_PATTERNS =====
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT UNIQUE NOT NULL,
                pattern_type TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                occurrence_count INTEGER DEFAULT 1,
                severity_level TEXT DEFAULT 'MEDIUM',
                error_signature TEXT,
                affected_agents TEXT,
                affected_files TEXT,
                root_cause_hypothesis TEXT,
                mitigation_applied INTEGER DEFAULT 0,
                mitigation_description TEXT,
                status TEXT DEFAULT 'ACTIVE'
            )
        """)

        # Indici per error_patterns
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_patterns_severity
            ON error_patterns(severity_level)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_patterns_status
            ON error_patterns(status)
        """)

        print(f"  ✅ Tabella error_patterns creata/verificata", file=sys.stderr)

        conn.commit()
        return True

    except Exception as e:
        print(f"  ❌ Errore upgrade schema: {e}", file=sys.stderr)
        conn.rollback()
        return False


def init_database() -> bool:
    """
    Inizializza il database con schema completo.

    Returns:
        True se successo, False altrimenti
    """
    db_path = get_db_path()

    try:
        # Connessione con WAL mode per performance
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")

        cursor = conn.cursor()

        # ===== TABELLA EVENTI =====
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS swarm_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                session_id TEXT,
                event_type TEXT NOT NULL,

                -- Agent info
                agent_name TEXT,
                agent_role TEXT,

                -- Task info
                task_id TEXT,
                parent_task_id TEXT,
                task_description TEXT,
                task_status TEXT,

                -- Execution
                duration_ms INTEGER,
                success INTEGER,
                error_message TEXT,

                -- Context
                project TEXT,
                files_modified TEXT,

                -- Metadata
                tags TEXT,
                notes TEXT,

                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Indici per query comuni
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON swarm_events(timestamp DESC)",
            "CREATE INDEX IF NOT EXISTS idx_events_agent ON swarm_events(agent_name)",
            "CREATE INDEX IF NOT EXISTS idx_events_project ON swarm_events(project)",
            "CREATE INDEX IF NOT EXISTS idx_events_task_status ON swarm_events(task_status)",
            "CREATE INDEX IF NOT EXISTS idx_events_session ON swarm_events(session_id)",
        ]

        for idx in indices:
            cursor.execute(idx)

        # ===== TABELLA LESSONS LEARNED =====
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons_learned (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                context TEXT,
                problem TEXT,
                solution TEXT,
                pattern TEXT,
                agents_involved TEXT,
                confidence REAL DEFAULT 0.5,
                times_applied INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Indici per lessons
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lessons_confidence
            ON lessons_learned(confidence DESC)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_lessons_pattern
            ON lessons_learned(pattern)
        """)

        conn.commit()

        # ===== UPGRADE SCHEMA =====
        print("\n🔄 Upgrade schema a v1.1.0...", file=sys.stderr)
        if not upgrade_schema(conn):
            print("⚠️  Upgrade schema fallito (ma database base funziona)", file=sys.stderr)

        conn.close()

        print(f"\n✅ Database inizializzato: {db_path}", file=sys.stderr)
        print(f"✅ Tabelle create: swarm_events, lessons_learned, error_patterns", file=sys.stderr)
        print(f"✅ Indici creati: 9 totali", file=sys.stderr)
        print(f"✅ WAL mode: attivo", file=sys.stderr)

        # Output JSON per script automation
        print({
            "status": "success",
            "db_path": str(db_path),
            "tables": ["swarm_events", "lessons_learned", "error_patterns"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        return True

    except Exception as e:
        print(f"❌ Errore inizializzazione: {e}", file=sys.stderr)
        print({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        return False


def verify_schema() -> bool:
    """Verifica che lo schema sia corretto."""
    db_path = get_db_path()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verifica tabelle
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name IN ('swarm_events', 'lessons_learned', 'error_patterns')
        """)
        tables = [row[0] for row in cursor.fetchall()]

        if len(tables) != 3:
            print(f"❌ Tabelle mancanti. Trovate: {tables}", file=sys.stderr)
            return False

        # Verifica indici
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name LIKE 'idx_%'
        """)
        indices = cursor.fetchall()

        # Verifica colonne lessons_learned (v1.1.0)
        cursor.execute("PRAGMA table_info(lessons_learned)")
        columns = [row[1] for row in cursor.fetchall()]
        required_cols = ["category", "severity", "root_cause", "prevention", "status"]
        missing_cols = [col for col in required_cols if col not in columns]

        if missing_cols:
            print(f"⚠️  Colonne mancanti in lessons_learned: {missing_cols}", file=sys.stderr)
            print(f"   Esegui di nuovo lo script per upgrade completo!", file=sys.stderr)

        print(f"✅ Schema verificato: {len(tables)} tabelle, {len(indices)} indici",
              file=sys.stderr)
        print(f"✅ Colonne lessons_learned: {len(columns)} totali", file=sys.stderr)

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Errore verifica: {e}", file=sys.stderr)
        return False


def main():
    """Entry point."""
    print("🐝 CervellaSwarm - Inizializzazione Database Memoria", file=sys.stderr)
    print(f"📅 Versione {__version__} ({__version_date__})", file=sys.stderr)
    print("-" * 60, file=sys.stderr)

    if init_database():
        if verify_schema():
            print("\n🎉 Database pronto per l'uso!", file=sys.stderr)
            sys.exit(0)

    print("\n💥 Inizializzazione fallita!", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
