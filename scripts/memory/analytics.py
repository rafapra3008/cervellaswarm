#!/usr/bin/env python3
"""
CervellaSwarm Analytics - Sistema di Reporting

Analizza il database swarm_memory.db e mostra metriche/statistiche
sugli eventi dello sciame, lezioni apprese e pattern di errori.

Usage:
    python analytics.py summary   → Overview generale
    python analytics.py lessons   → Lista lezioni attive
    python analytics.py events    → Ultimi eventi
    python analytics.py agents    → Stats per agente
    python analytics.py patterns  → Pattern di errori
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# === COLORI ANSI ===
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def get_severity_color(severity: str) -> str:
    """Ritorna il colore ANSI per il livello di severity."""
    colors = {
        "CRITICAL": RED,
        "HIGH": YELLOW,
        "MEDIUM": CYAN,
        "LOW": GREEN,
    }
    return colors.get(severity.upper(), RESET)


def get_db_path() -> Path:
    """Ritorna il path al database swarm_memory.db."""
    # Assume che lo script sia in scripts/memory/
    script_dir = Path(__file__).parent
    db_path = script_dir / "../../data/swarm_memory.db"
    return db_path.resolve()


def connect_db() -> sqlite3.Connection:
    """Connessione al database con gestione errori."""
    db_path = get_db_path()

    if not db_path.exists():
        print(f"{RED}❌ Database non trovato: {db_path}{RESET}")
        print(f"\n{YELLOW}Suggerimento:{RESET} Esegui prima:")
        print(f"  cd scripts/memory && ./init_db.py\n")
        sys.exit(1)

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # Accesso per nome colonna
        return conn
    except sqlite3.Error as e:
        print(f"{RED}❌ Errore connessione database: {e}{RESET}")
        sys.exit(1)


# === COMMAND: SUMMARY ===

def cmd_summary():
    """Mostra overview generale del sistema."""
    conn = connect_db()
    cursor = conn.cursor()

    # Calcola metriche
    cursor.execute("SELECT COUNT(*) as total FROM swarm_events")
    total_events = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as success FROM swarm_events WHERE success = 1")
    success_count = cursor.fetchone()['success']

    success_rate = (success_count / total_events * 100) if total_events > 0 else 0

    cursor.execute("SELECT COUNT(*) as total FROM lessons_learned")
    total_lessons = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
    active_lessons = cursor.fetchone()['active']

    cursor.execute("SELECT timestamp FROM swarm_events ORDER BY timestamp DESC LIMIT 1")
    last_event_row = cursor.fetchone()
    last_event = last_event_row['timestamp'] if last_event_row else "N/A"

    # Top 3 lezioni attive
    cursor.execute("""
        SELECT pattern, category, severity
        FROM lessons_learned
        WHERE status = 'ACTIVE'
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
        LIMIT 3
    """)
    top_lessons = cursor.fetchall()

    # === OUTPUT ===
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🐝 CERVELLASWARM ANALYTICS                                      ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("║                                                                  ║")
    print("║  📊 OVERVIEW                                                     ║")
    print("║  ────────────────────────────────────────────────────           ║")
    print(f"║  Total Events:     {str(total_events).ljust(45)}║")
    print(f"║  Success Rate:     {f'{success_rate:.1f}%'.ljust(45)}║")
    print(f"║  Total Lessons:    {str(total_lessons).ljust(45)}║")
    print(f"║  Active Lessons:   {f'{active_lessons} (da risolvere)'.ljust(45)}║")
    print(f"║  Last Event:       {last_event[:43].ljust(45)}║")
    print("║                                                                  ║")

    if top_lessons:
        print("║  📚 TOP LESSONS ATTIVE                                          ║")
        print("║  ────────────────────────────────────────────────────           ║")
        for lesson in top_lessons:
            severity = lesson['severity']
            color = get_severity_color(severity)
            pattern = lesson['pattern'][:35]
            category = lesson['category'][:20] if lesson['category'] else 'N/A'

            line = f"  [{severity}] {pattern} ({category})"
            # Padding per allineare
            padding = 66 - len(line)
            print(f"║{color}{line}{RESET}{' ' * padding}║")
        print("║                                                                  ║")

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()


# === COMMAND: LESSONS ===

def cmd_lessons():
    """Lista tutte le lezioni apprese ordinate per severity."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pattern, category, severity, status,
            prevention, occurrence_count, time_wasted_minutes
        FROM lessons_learned
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
    """)

    lessons = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  📚 LESSONS LEARNED                                              ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not lessons:
        print(f"  {DIM}Nessuna lezione trovata.{RESET}")
        print()
    else:
        for i, lesson in enumerate(lessons, 1):
            color = get_severity_color(lesson['severity'])
            status_icon = "🔴" if lesson['status'] == 'ACTIVE' else "✅"

            print(f"{BOLD}{i}. {status_icon} {color}[{lesson['severity']}]{RESET} {lesson['pattern']}")
            print(f"   Category: {lesson['category'] or 'N/A'}")
            print(f"   Prevention: {lesson['prevention'][:80] or 'N/A'}")
            print(f"   Occurrences: {lesson['occurrence_count']} | Time Wasted: {lesson['time_wasted_minutes'] or 0} min")
            print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()


# === COMMAND: EVENTS ===

def cmd_events(limit: int = 10):
    """Mostra gli ultimi N eventi."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            agent_name, event_type, project, success,
            timestamp, task_description, duration_ms
        FROM swarm_events
        ORDER BY timestamp DESC
        LIMIT {limit}
    """)

    events = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print(f"║  📝 ULTIMI {limit} EVENTI                                             ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not events:
        print(f"  {DIM}Nessun evento trovato.{RESET}")
        print()
    else:
        for i, event in enumerate(events, 1):
            success_icon = f"{GREEN}✅{RESET}" if event['success'] else f"{RED}❌{RESET}"
            agent = event['agent_name'] or "N/A"
            project = event['project'] or "N/A"
            etype = event['event_type']
            timestamp = event['timestamp'][:19]  # Tronca millisecondi
            duration = f"{event['duration_ms']}ms" if event['duration_ms'] else "N/A"

            print(f"{i}. {success_icon} {BOLD}{agent}{RESET} | {etype}")
            print(f"   {DIM}Project:{RESET} {project} | {DIM}Time:{RESET} {timestamp} | {DIM}Duration:{RESET} {duration}")

            if event['task_description']:
                desc = event['task_description'][:70]
                print(f"   {DIM}Task:{RESET} {desc}")
            print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()


# === COMMAND: AGENTS ===

def cmd_agents():
    """Mostra statistiche per agente."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            agent_name,
            COUNT(*) as total_tasks,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures,
            AVG(duration_ms) as avg_duration
        FROM swarm_events
        WHERE agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY total_tasks DESC
    """)

    agents = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  👥 AGENT STATISTICS                                             ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not agents:
        print(f"  {DIM}Nessun agente trovato.{RESET}")
        print()
    else:
        # Header
        print(f"  {BOLD}{'Agent'.ljust(20)} {'Tasks'.ljust(8)} {'Success'.ljust(10)} {'Failures'.ljust(10)} {'Avg Duration'.ljust(15)}{RESET}")
        print(f"  {'-' * 65}")

        for agent in agents:
            name = (agent['agent_name'] or "N/A")[:20].ljust(20)
            total = str(agent['total_tasks']).ljust(8)
            success = str(agent['successes']).ljust(10)
            failures = str(agent['failures']).ljust(10)

            avg_dur = agent['avg_duration']
            avg_str = f"{int(avg_dur)}ms" if avg_dur else "N/A"
            avg_str = avg_str.ljust(15)

            # Colore successi/fallimenti
            if agent['failures'] == 0:
                color = GREEN
            elif agent['failures'] > agent['successes']:
                color = RED
            else:
                color = YELLOW

            print(f"  {name} {total} {color}{success}{RESET} {color}{failures}{RESET} {avg_str}")

        print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()


# === COMMAND: PATTERNS ===

def cmd_patterns():
    """Mostra pattern di errori."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pattern_name, pattern_type, severity_level,
            occurrence_count, status, last_seen,
            root_cause_hypothesis, mitigation_description
        FROM error_patterns
        ORDER BY
            CASE severity_level
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
    """)

    patterns = cursor.fetchall()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🔍 ERROR PATTERNS                                               ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    if not patterns:
        print(f"  {DIM}Nessun pattern trovato.{RESET}")
        print()
    else:
        for i, pattern in enumerate(patterns, 1):
            color = get_severity_color(pattern['severity_level'])
            status_icon = "🔴" if pattern['status'] == 'ACTIVE' else "✅"

            print(f"{BOLD}{i}. {status_icon} {color}[{pattern['severity_level']}]{RESET} {pattern['pattern_name']}")
            print(f"   Type: {pattern['pattern_type']} | Occurrences: {pattern['occurrence_count']}")
            print(f"   Last Seen: {pattern['last_seen'][:19]}")

            if pattern['root_cause_hypothesis']:
                print(f"   Root Cause: {pattern['root_cause_hypothesis'][:70]}")

            if pattern['mitigation_description']:
                print(f"   Mitigation: {pattern['mitigation_description'][:70]}")

            print()

    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    conn.close()


# === MAIN ===

def main():
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Analytics - Sistema di Reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandi disponibili:
  summary   - Overview generale del sistema
  lessons   - Lista tutte le lezioni apprese
  events    - Mostra ultimi eventi (default: 10)
  agents    - Statistiche per agente
  patterns  - Pattern di errori attivi

Esempi:
  python analytics.py summary
  python analytics.py events
  python analytics.py lessons
        """
    )

    parser.add_argument(
        'command',
        choices=['summary', 'lessons', 'events', 'agents', 'patterns'],
        help='Comando da eseguire'
    )

    parser.add_argument(
        '-n', '--limit',
        type=int,
        default=10,
        help='Numero di eventi da mostrare (solo per "events")'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__} ({__version_date__})'
    )

    args = parser.parse_args()

    # Dispatch comando
    if args.command == 'summary':
        cmd_summary()
    elif args.command == 'lessons':
        cmd_lessons()
    elif args.command == 'events':
        cmd_events(args.limit)
    elif args.command == 'agents':
        cmd_agents()
    elif args.command == 'patterns':
        cmd_patterns()


if __name__ == '__main__':
    main()
