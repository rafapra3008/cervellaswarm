#!/usr/bin/env python3
"""
CervellaSwarm Weekly Retrospective - Report Settimanale Automatico

Genera un report retrospettivo settimanale con:
- Metriche chiave (eventi totali, success rate, errori)
- Top 3 pattern errori
- Lezioni apprese della settimana
- Breakdown per agente
- Raccomandazioni automatiche

Usage:
    python weekly_retro.py              → Report ultimi 7 giorni
    python weekly_retro.py -d 14        → Report ultimi 14 giorni
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def get_db_path() -> Path:
    """Ritorna il path al database swarm_memory.db."""
    script_dir = Path(__file__).parent
    db_path = script_dir / "../../data/swarm_memory.db"
    return db_path.resolve()


def connect_db() -> sqlite3.Connection:
    """Connessione al database con gestione errori."""
    db_path = get_db_path()

    if not db_path.exists():
        console.print(f"[red]❌ Database non trovato: {db_path}[/red]")
        sys.exit(1)

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        console.print(f"[red]❌ Errore connessione database: {e}[/red]")
        sys.exit(1)


def generate_retro(days: int = 7):
    """
    Genera weekly retrospective report.

    Args:
        days: Numero di giorni da analizzare (default: 7)
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Periodo analisi
    period_start = (datetime.now() - timedelta(days=days)).isoformat()
    period_end = datetime.now().isoformat()

    console.print("\n")
    console.print(Panel(
        f"[bold magenta]📅 WEEKLY RETROSPECTIVE[/bold magenta]\n"
        f"[dim]Periodo: {period_start[:10]} → {period_end[:10]}[/dim]",
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
        WHERE datetime(timestamp) >= datetime('{period_start}')
    """)
    metrics = cursor.fetchone()

    total = metrics['total']
    successes = metrics['successes']
    failures = metrics['failures']
    success_rate = (successes / total * 100) if total > 0 else 0

    metrics_table = Table(title="📊 METRICHE CHIAVE", box=box.SIMPLE, show_header=False)
    metrics_table.add_column("Metrica", style="cyan", width=20)
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
        patterns_table.add_column("Severity", justify="center", width=15)
        patterns_table.add_column("Pattern", style="white")
        patterns_table.add_column("Count", justify="right", style="yellow", width=8)

        for pattern in top_patterns:
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')

            patterns_table.add_row(
                f"{severity_emoji} {pattern['severity_level']}",
                pattern['pattern_name'][:60],
                str(pattern['occurrence_count'])
            )

        console.print(patterns_table)
        console.print("\n")
    else:
        console.print("[dim]   Nessun pattern errore attivo[/dim]\n")

    # === 3. LEZIONI APPRESE ===

    cursor.execute(f"""
        SELECT pattern, severity
        FROM lessons_learned
        WHERE datetime(created_at) >= datetime('{period_start}')
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
        lessons_text = "\n".join([
            f"• [{l['severity']}] {l['pattern']}"
            for l in new_lessons
        ])
        lessons_panel = Panel(
            lessons_text,
            title=f"📚 LEZIONI APPRESE ({len(new_lessons)})",
            border_style="green"
        )
        console.print(lessons_panel)
        console.print("\n")
    else:
        console.print("[dim]   Nessuna nuova lezione questo periodo[/dim]\n")

    # === 4. BREAKDOWN PER AGENTE ===

    cursor.execute(f"""
        SELECT
            agent_name,
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failures,
            ROUND(AVG(duration_ms), 0) as avg_duration
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime('{period_start}')
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY total DESC
        LIMIT 5
    """)
    agents = cursor.fetchall()

    if agents:
        agents_table = Table(title="👥 BREAKDOWN PER AGENTE (Top 5)", box=box.SIMPLE)
        agents_table.add_column("Agente", style="cyan", width=20)
        agents_table.add_column("Total", justify="right", width=8)
        agents_table.add_column("Success", justify="right", style="green", width=8)
        agents_table.add_column("Failures", justify="right", style="red", width=8)
        agents_table.add_column("Avg Duration", justify="right", style="dim", width=12)

        for agent in agents:
            avg_dur = f"{int(agent['avg_duration'])}ms" if agent['avg_duration'] else "N/A"
            agents_table.add_row(
                agent['agent_name'][:20],
                str(agent['total']),
                str(agent['successes']),
                str(agent['failures']),
                avg_dur
            )

        console.print(agents_table)
        console.print("\n")
    else:
        console.print("[dim]   Nessun dato agente disponibile[/dim]\n")

    # === 5. RACCOMANDAZIONI ===

    recommendations = []

    if success_rate < 80:
        recommendations.append("⚠️  Success rate < 80% - Investigare cause degli errori")

    if failures > 10:
        recommendations.append("🔍 Alto numero di errori - Eseguire auto-detect per pattern")

    cursor.execute("SELECT COUNT(*) as active FROM lessons_learned WHERE status = 'ACTIVE'")
    active_lessons_count = cursor.fetchone()['active']
    if active_lessons_count > 5:
        recommendations.append(f"📚 {active_lessons_count} lezioni ACTIVE - Pianificare fix")

    cursor.execute("SELECT COUNT(*) as active FROM error_patterns WHERE status = 'ACTIVE'")
    active_patterns_count = cursor.fetchone()['active']
    if active_patterns_count > 3:
        recommendations.append(f"🔴 {active_patterns_count} pattern ACTIVE - Review necessaria")

    if total == 0:
        recommendations.append("⚪ Nessun evento in questo periodo - Sistema inattivo")
    elif not recommendations:
        recommendations.append("✅ Sistema stabile - Continuare così!")

    recommendations_panel = Panel(
        "\n".join(recommendations),
        title="💡 RACCOMANDAZIONI",
        border_style="yellow"
    )
    console.print(recommendations_panel)
    console.print("\n")

    # === 6. PROSSIMI PASSI SUGGERITI ===

    next_steps = []

    if active_patterns_count > 0:
        next_steps.append("1. Review pattern attivi con `analytics.py patterns`")

    if active_lessons_count > 0:
        next_steps.append("2. Review lezioni attive con `analytics.py lessons`")

    if failures > 5:
        next_steps.append("3. Analizzare ultimi errori con `analytics.py events -n 20`")

    if not next_steps:
        next_steps.append("✅ Nessuna azione richiesta - Sistema OK!")

    steps_panel = Panel(
        "\n".join(next_steps),
        title="📝 PROSSIMI PASSI",
        border_style="cyan"
    )
    console.print(steps_panel)
    console.print("\n")

    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Weekly Retrospective",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python weekly_retro.py              # Report ultimi 7 giorni
  python weekly_retro.py -d 14        # Report ultimi 14 giorni
  python weekly_retro.py --days 30    # Report ultimo mese
        """
    )

    parser.add_argument(
        '-d', '--days',
        type=int,
        default=7,
        help='Numero di giorni da analizzare (default: 7)'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__} ({__version_date__})'
    )

    args = parser.parse_args()

    # Validazione
    if args.days < 1:
        console.print("[red]❌ Errore: --days deve essere >= 1[/red]")
        sys.exit(1)

    if args.days > 365:
        console.print("[yellow]⚠️  Attenzione: Analisi > 1 anno potrebbe essere lenta[/yellow]")

    # Genera retrospettiva
    generate_retro(days=args.days)


if __name__ == '__main__':
    main()
