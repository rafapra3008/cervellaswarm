#!/usr/bin/env python3
"""
Sistema Memoria CervellaSwarm - Query Eventi

Script utility per interrogare il database memoria.
Supporta vari filtri e statistiche.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Import centralizzato path management
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path


def query_recent_events(conn: sqlite3.Connection, limit: int = 50) -> list:
    """Query eventi recenti."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            agent_name,
            task_description,
            project,
            success,
            duration_ms,
            files_modified
        FROM swarm_events
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    events = []
    for row in cursor.fetchall():
        events.append({
            "timestamp": row[0],
            "agent": row[1],
            "task": row[2],
            "project": row[3],
            "success": bool(row[4]),
            "duration_ms": row[5],
            "files_modified": json.loads(row[6]) if row[6] else [],
        })

    return events


def query_by_agent(conn: sqlite3.Connection, agent_name: str) -> list:
    """Query eventi per agent."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            task_description,
            project,
            success,
            duration_ms
        FROM swarm_events
        WHERE agent_name = ?
        ORDER BY timestamp DESC
        LIMIT 100
    """, (agent_name,))

    events = []
    for row in cursor.fetchall():
        events.append({
            "timestamp": row[0],
            "task": row[1],
            "project": row[2],
            "success": bool(row[3]),
            "duration_ms": row[4],
        })

    return events


def query_by_project(conn: sqlite3.Connection, project: str) -> list:
    """Query eventi per progetto."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            agent_name,
            task_description,
            success,
            duration_ms
        FROM swarm_events
        WHERE project = ?
        ORDER BY timestamp DESC
        LIMIT 100
    """, (project,))

    events = []
    for row in cursor.fetchall():
        events.append({
            "timestamp": row[0],
            "agent": row[1],
            "task": row[2],
            "success": bool(row[3]),
            "duration_ms": row[4],
        })

    return events


def query_failed_tasks(conn: sqlite3.Connection) -> list:
    """Query task falliti."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            agent_name,
            task_description,
            project,
            error_message
        FROM swarm_events
        WHERE success = 0
        ORDER BY timestamp DESC
        LIMIT 50
    """)

    events = []
    for row in cursor.fetchall():
        events.append({
            "timestamp": row[0],
            "agent": row[1],
            "task": row[2],
            "project": row[3],
            "error": row[4],
        })

    return events


def get_statistics(conn: sqlite3.Connection) -> dict:
    """Statistiche generali."""
    cursor = conn.cursor()

    stats = {}

    # Totale eventi
    cursor.execute("SELECT COUNT(*) FROM swarm_events")
    stats["total_events"] = cursor.fetchone()[0]

    # Eventi per agent
    cursor.execute("""
        SELECT agent_name, COUNT(*) as count
        FROM swarm_events
        WHERE agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY count DESC
    """)
    stats["by_agent"] = {row[0]: row[1] for row in cursor.fetchall()}

    # Eventi per progetto
    cursor.execute("""
        SELECT project, COUNT(*) as count
        FROM swarm_events
        WHERE project IS NOT NULL
        GROUP BY project
        ORDER BY count DESC
    """)
    stats["by_project"] = {row[0]: row[1] for row in cursor.fetchall()}

    # Success rate
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(success) as successful
        FROM swarm_events
    """)
    row = cursor.fetchone()
    total = row[0]
    successful = row[1] or 0
    stats["success_rate"] = (successful / total * 100) if total > 0 else 0

    # Task falliti
    cursor.execute("SELECT COUNT(*) FROM swarm_events WHERE success = 0")
    stats["failed_tasks"] = cursor.fetchone()[0]

    return stats


def format_output(data: any, format_type: str = "json") -> str:
    """Formatta output."""
    if format_type == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)

    elif format_type == "table":
        # Formato tabella semplice
        if isinstance(data, list) and data:
            # Header
            keys = data[0].keys()
            output = [" | ".join(keys)]
            output.append("-" * 80)

            # Rows
            for item in data:
                values = [str(item.get(k, ""))[:50] for k in keys]
                output.append(" | ".join(values))

            return "\n".join(output)

        elif isinstance(data, dict):
            output = []
            for key, value in data.items():
                output.append(f"{key}: {value}")
            return "\n".join(output)

    return str(data)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Query CervellaSwarm Memory Database"
    )

    parser.add_argument(
        "--recent",
        type=int,
        metavar="N",
        help="Show N most recent events (default: 20)"
    )
    parser.add_argument(
        "--agent",
        type=str,
        metavar="NAME",
        help="Show events for specific agent"
    )
    parser.add_argument(
        "--project",
        type=str,
        metavar="NAME",
        help="Show events for specific project"
    )
    parser.add_argument(
        "--failed",
        action="store_true",
        help="Show only failed tasks"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show general statistics"
    )
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Verifica database
    db_path = get_db_path()
    if not db_path.exists():
        print(f"❌ Database non trovato: {db_path}", file=sys.stderr)
        print("💡 Esegui prima: ./scripts/memory/init_db.py", file=sys.stderr)
        sys.exit(1)

    try:
        conn = sqlite3.connect(db_path)

        # Esegui query richiesta
        if args.stats:
            result = get_statistics(conn)
            print("\n📊 Statistiche Generali")
            print("=" * 60)
            print(format_output(result, args.format))

        elif args.failed:
            result = query_failed_tasks(conn)
            print(f"\n❌ Task Falliti ({len(result)} totali)")
            print("=" * 60)
            print(format_output(result, args.format))

        elif args.agent:
            result = query_by_agent(conn, args.agent)
            print(f"\n🐝 Eventi per Agent: {args.agent} ({len(result)} totali)")
            print("=" * 60)
            print(format_output(result, args.format))

        elif args.project:
            result = query_by_project(conn, args.project)
            print(f"\n📂 Eventi per Progetto: {args.project} ({len(result)} totali)")
            print("=" * 60)
            print(format_output(result, args.format))

        elif args.recent:
            result = query_recent_events(conn, args.recent)
            print(f"\n📅 Ultimi {len(result)} Eventi")
            print("=" * 60)
            print(format_output(result, args.format))

        else:
            # Default: ultimi 20 eventi
            result = query_recent_events(conn, 20)
            print("\n📅 Ultimi 20 Eventi")
            print("=" * 60)
            print(format_output(result, args.format))

        conn.close()
        sys.exit(0)

    except Exception as e:
        print(f"❌ Errore: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
