#!/usr/bin/env python3
"""
CervellaSwarm Analytics - Sistema di Reporting

Analizza il database swarm_memory.db e mostra metriche/statistiche
sugli eventi dello sciame, lezioni apprese e pattern di errori.

Usage:
    python analytics.py summary      → Overview generale
    python analytics.py lessons      → Lista lezioni attive
    python analytics.py events       → Ultimi eventi
    python analytics.py agents       → Stats per agente
    python analytics.py patterns     → Pattern di errori
    python analytics.py dashboard    → Dashboard live (Rich)
    python analytics.py auto-detect  → Auto-rileva pattern errori
    python analytics.py retro        → Weekly retrospective
"""

__version__ = "2.0.0"
__version_date__ = "2026-01-01"

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

# Optional rich import
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich import box
    from rich.text import Text
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Pattern detector import
try:
    from pattern_detector import detect_error_patterns, fetch_recent_errors, save_patterns_to_db
except ImportError:
    # Fallback se non trovato
    detect_error_patterns = None
    fetch_recent_errors = None
    save_patterns_to_db = None

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


# === HELPER FUNCTIONS FOR RICH FALLBACK ===

def print_rich_or_plain(rich_fn, plain_fn, *args, **kwargs):
    """Helper per stampare con Rich se disponibile, altrimenti plain text."""
    if HAS_RICH:
        rich_fn(*args, **kwargs)
    else:
        plain_fn(*args, **kwargs)


def plain_print(text: str):
    """Stampa plain text (fallback per console.print)."""
    print(text)


# Import centralizzato path management (dopo altri import)
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path


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


# === COMMAND: DASHBOARD (Rich) ===

def cmd_dashboard():
    """Dashboard live con Rich - Panoramica visuale del sistema."""
    if not HAS_RICH:
        print(f"\n{RED}❌ Comando 'dashboard' richiede Rich installato!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} pip install rich")
        print(f"{CYAN}Alternativa:{RESET} Usa 'python analytics.py summary' per output base\n")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch metriche settimana corrente
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()

    cursor.execute(f"""
        SELECT COUNT(*) as total
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime('{week_ago}')
    """)
    events_week = cursor.fetchone()['total']

    cursor.execute(f"""
        SELECT COUNT(*) as success
        FROM swarm_events
        WHERE success = 1 AND datetime(timestamp) >= datetime('{week_ago}')
    """)
    success_week = cursor.fetchone()['success']

    success_rate = (success_week / events_week * 100) if events_week > 0 else 0

    cursor.execute(f"""
        SELECT COUNT(*) as errors
        FROM swarm_events
        WHERE success = 0 AND datetime(timestamp) >= datetime('{week_ago}')
    """)
    errors_week = cursor.fetchone()['errors']

    # Pattern attivi
    cursor.execute("""
        SELECT COUNT(*) as active
        FROM error_patterns
        WHERE status = 'ACTIVE'
    """)
    active_patterns = cursor.fetchone()['active']

    # Lezioni attive
    cursor.execute("""
        SELECT COUNT(*) as active
        FROM lessons_learned
        WHERE status = 'ACTIVE'
    """)
    active_lessons = cursor.fetchone()['active']

    # Top agente della settimana
    cursor.execute(f"""
        SELECT agent_name, COUNT(*) as tasks
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime('{week_ago}')
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY tasks DESC
        LIMIT 1
    """)
    top_agent_row = cursor.fetchone()
    top_agent = top_agent_row['agent_name'] if top_agent_row else "N/A"
    top_agent_tasks = top_agent_row['tasks'] if top_agent_row else 0

    conn.close()

    # === RICH OUTPUT ===

    # Tabella metriche
    metrics_table = Table(
        title="📊 METRICHE SETTIMANA",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    metrics_table.add_column("Metrica", style="white")
    metrics_table.add_column("Valore", justify="right", style="bold green")
    metrics_table.add_column("Trend", justify="center")

    metrics_table.add_row("Eventi Totali", str(events_week), "📈")
    metrics_table.add_row(
        "Success Rate",
        f"{success_rate:.1f}%",
        "✅" if success_rate > 80 else "⚠️"
    )
    metrics_table.add_row("Errori", str(errors_week), "❌" if errors_week > 5 else "✅")
    metrics_table.add_row("Pattern Attivi", str(active_patterns), "🔍")
    metrics_table.add_row("Lessons Attive", str(active_lessons), "📚")

    # Panel agente top
    top_agent_panel = Panel(
        f"[bold yellow]{top_agent}[/bold yellow]\n[dim]{top_agent_tasks} task completati[/dim]",
        title="🏆 TOP AGENTE SETTIMANA",
        border_style="yellow"
    )

    # Layout
    console.print("\n")
    console.print(Panel(
        "[bold cyan]🐝 CERVELLASWARM DASHBOARD[/bold cyan]",
        style="cyan",
        box=box.DOUBLE
    ))
    console.print("\n")
    console.print(metrics_table)
    console.print("\n")
    console.print(top_agent_panel)
    console.print("\n")


# === COMMAND: AUTO-DETECT ===

def cmd_auto_detect(days: int = 7):
    """Auto-rileva pattern di errori ricorrenti."""
    if not detect_error_patterns or not fetch_recent_errors or not save_patterns_to_db:
        print(f"\n{RED}❌ pattern_detector.py non disponibile!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} Verifica che pattern_detector.py sia nella stessa directory\n")
        return

    print(f"\n{CYAN}🔍 Auto-detection pattern errori (ultimi {days} giorni)...{RESET}\n")

    # Fetch errori
    errors = fetch_recent_errors(days=days)

    if not errors:
        print(f"{GREEN}✅ Nessun errore trovato! Sistema stabile.{RESET}\n")
        return

    print(f"   Trovati {YELLOW}{len(errors)}{RESET} errori")

    # Rileva pattern
    print(f"\n{CYAN}🔎 Rilevamento pattern in corso...{RESET}")
    patterns = detect_error_patterns(
        errors=errors,
        similarity_threshold=0.7,
        min_occurrences=3
    )

    if not patterns:
        print(f"{GREEN}✅ Nessun pattern ricorrente rilevato (soglia: 3+ occorrenze){RESET}\n")
        return

    print(f"   Rilevati {BOLD}{YELLOW}{len(patterns)}{RESET} pattern\n")

    # Salva nel database
    print(f"{CYAN}💾 Salvataggio pattern nel database...{RESET}")
    new, updated = save_patterns_to_db(patterns)
    print(f"   {GREEN}✅ Nuovi: {new} | Aggiornati: {updated}{RESET}\n")

    # Pattern rilevati (Rich se disponibile, altrimenti plain text)
    if HAS_RICH:
        patterns_table = Table(
            title="📋 PATTERN RILEVATI",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        patterns_table.add_column("#", justify="right", style="dim")
        patterns_table.add_column("Severity", justify="center")
        patterns_table.add_column("Pattern Name", style="white")
        patterns_table.add_column("Occorrenze", justify="right", style="yellow")

        for i, pattern in enumerate(patterns, 1):
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')

            severity_color = {
                'CRITICAL': 'red',
                'HIGH': 'yellow',
                'MEDIUM': 'cyan',
                'LOW': 'green'
            }.get(pattern['severity_level'], 'white')

            patterns_table.add_row(
                str(i),
                f"[{severity_color}]{severity_emoji} {pattern['severity_level']}[/{severity_color}]",
                pattern['pattern_name'][:60],
                str(pattern['occurrence_count'])
            )

        console.print(patterns_table)
        console.print("\n[green]✅ Pattern detection completato![/green]\n")
    else:
        # Plain text fallback
        print("\n📋 PATTERN RILEVATI")
        print("-" * 80)
        for i, pattern in enumerate(patterns, 1):
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')

            print(f"{i}. {severity_emoji} [{pattern['severity_level']}] {pattern['pattern_name'][:60]}")
            print(f"   Occorrenze: {pattern['occurrence_count']}")
        print(f"\n{GREEN}✅ Pattern detection completato!{RESET}\n")


# === COMMAND: RETRO (Weekly Retrospective) ===

def cmd_retro():
    """Genera weekly retrospective report."""
    if not HAS_RICH:
        print(f"\n{RED}❌ Comando 'retro' richiede Rich installato!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} pip install rich")
        print(f"{CYAN}Alternativa:{RESET} Usa 'python weekly_retro.py' che supporta fallback plain text\n")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Periodo: ultimi 7 giorni
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()

    console.print("\n")
    console.print(Panel(
        "[bold magenta]📅 WEEKLY RETROSPECTIVE[/bold magenta]",
        style="magenta",
        box=box.DOUBLE
    ))
    console.print("\n")

    # === 1. METRICHE CHIAVE ===

    cursor.execute(f"""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime('{week_ago}')
    """)
    metrics = cursor.fetchone()

    total = metrics['total']
    successes = metrics['successes']
    failures = metrics['failures']
    success_rate = (successes / total * 100) if total > 0 else 0

    metrics_table = Table(title="📊 METRICHE CHIAVE", box=box.SIMPLE, show_header=False)
    metrics_table.add_column("Metrica", style="cyan")
    metrics_table.add_column("Valore", justify="right", style="bold white")

    metrics_table.add_row("Eventi Totali", str(total))
    metrics_table.add_row("Successi", f"[green]{successes}[/green]")
    metrics_table.add_row("Errori", f"[red]{failures}[/red]")
    metrics_table.add_row("Success Rate", f"[bold]{success_rate:.1f}%[/bold]")

    console.print(metrics_table)
    console.print("\n")

    # === 2. TOP 3 PATTERN ERRORI ===

    cursor.execute("""
        SELECT pattern_name, severity_level, occurrence_count
        FROM error_patterns
        WHERE status = 'ACTIVE'
        ORDER BY
            CASE severity_level
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            occurrence_count DESC
        LIMIT 3
    """)
    top_patterns = cursor.fetchall()

    if top_patterns:
        patterns_table = Table(title="🔍 TOP 3 PATTERN ERRORI", box=box.SIMPLE)
        patterns_table.add_column("Severity", justify="center")
        patterns_table.add_column("Pattern", style="white")
        patterns_table.add_column("Count", justify="right", style="yellow")

        for pattern in top_patterns:
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')

            patterns_table.add_row(
                f"{severity_emoji} {pattern['severity_level']}",
                pattern['pattern_name'][:50],
                str(pattern['occurrence_count'])
            )

        console.print(patterns_table)
        console.print("\n")

    # === 3. LEZIONI APPRESE ===

    cursor.execute(f"""
        SELECT pattern, severity
        FROM lessons_learned
        WHERE datetime(created_at) >= datetime('{week_ago}')
        ORDER BY
            CASE severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END
        LIMIT 5
    """)
    new_lessons = cursor.fetchall()

    if new_lessons:
        lessons_panel = Panel(
            "\n".join([f"• [{l['severity']}] {l['pattern']}" for l in new_lessons]),
            title="📚 LEZIONI APPRESE QUESTA SETTIMANA",
            border_style="green"
        )
        console.print(lessons_panel)
        console.print("\n")

    # === 4. BREAKDOWN PER AGENTE ===

    cursor.execute(f"""
        SELECT
            agent_name,
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime('{week_ago}')
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY total DESC
        LIMIT 5
    """)
    agents = cursor.fetchall()

    if agents:
        agents_table = Table(title="👥 BREAKDOWN PER AGENTE (Top 5)", box=box.SIMPLE)
        agents_table.add_column("Agente", style="cyan")
        agents_table.add_column("Total", justify="right")
        agents_table.add_column("Success", justify="right", style="green")
        agents_table.add_column("Failures", justify="right", style="red")

        for agent in agents:
            agents_table.add_row(
                agent['agent_name'],
                str(agent['total']),
                str(agent['successes']),
                str(agent['failures'])
            )

        console.print(agents_table)
        console.print("\n")

    # === 5. RACCOMANDAZIONI ===

    recommendations = []

    if success_rate < 80:
        recommendations.append("⚠️ Success rate < 80% - Investigare cause degli errori")

    if failures > 10:
        recommendations.append("🔍 Alto numero di errori - Eseguire auto-detect per pattern")

    cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
    active_lessons_count = cursor.fetchone()['active']
    if active_lessons_count > 5:
        recommendations.append(f"📚 {active_lessons_count} lezioni ACTIVE - Pianificare fix")

    if not recommendations:
        recommendations.append("✅ Sistema stabile - Continuare così!")

    recommendations_panel = Panel(
        "\n".join(recommendations),
        title="💡 RACCOMANDAZIONI",
        border_style="yellow"
    )
    console.print(recommendations_panel)
    console.print("\n")

    conn.close()


# === MAIN ===

def main():
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Analytics - Sistema di Reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandi disponibili:
  summary      - Overview generale del sistema
  lessons      - Lista tutte le lezioni apprese
  events       - Mostra ultimi eventi (default: 10)
  agents       - Statistiche per agente
  patterns     - Pattern di errori attivi
  dashboard    - Dashboard live con Rich (NUOVO!)
  auto-detect  - Auto-rileva pattern errori (NUOVO!)
  retro        - Weekly retrospective (NUOVO!)

Esempi:
  python analytics.py summary
  python analytics.py dashboard
  python analytics.py auto-detect
  python analytics.py retro
        """
    )

    parser.add_argument(
        'command',
        choices=['summary', 'lessons', 'events', 'agents', 'patterns', 'dashboard', 'auto-detect', 'retro'],
        help='Comando da eseguire'
    )

    parser.add_argument(
        '-n', '--limit',
        type=int,
        default=10,
        help='Numero di eventi da mostrare (solo per "events")'
    )

    parser.add_argument(
        '-d', '--days',
        type=int,
        default=7,
        help='Numero di giorni da analizzare (solo per "auto-detect")'
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
    elif args.command == 'dashboard':
        cmd_dashboard()
    elif args.command == 'auto-detect':
        cmd_auto_detect(args.days)
    elif args.command == 'retro':
        cmd_retro()


if __name__ == '__main__':
    main()
