"""Analytics dashboard command - Live visual dashboard."""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Aggiungi path per import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.db import connect_db

# Rich import opzionale
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Colori ANSI per fallback
from common.colors import RED, GREEN, YELLOW, CYAN, RESET


def cmd_dashboard():
    """Dashboard live con Rich - Panoramica visuale del sistema."""
    if not HAS_RICH:
        print(f"\n{RED}❌ Comando 'dashboard' richiede Rich installato!{RESET}")
        print(f"{YELLOW}Suggerimento:{RESET} pip install rich")
        print(f"{CYAN}Alternativa:{RESET} Usa 'python -m scripts.memory.analytics.cli summary' per output base\n")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch metriche settimana corrente
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()

    # FIX SQL INJECTION: usa query parametrizzate
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime(?)
    """, (week_ago,))
    events_week = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) as success
        FROM swarm_events
        WHERE success = 1 AND datetime(timestamp) >= datetime(?)
    """, (week_ago,))
    success_week = cursor.fetchone()['success']

    success_rate = (success_week / events_week * 100) if events_week > 0 else 0

    cursor.execute("""
        SELECT COUNT(*) as errors
        FROM swarm_events
        WHERE success = 0 AND datetime(timestamp) >= datetime(?)
    """, (week_ago,))
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
    cursor.execute("""
        SELECT agent_name, COUNT(*) as tasks
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime(?)
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        ORDER BY tasks DESC
        LIMIT 1
    """, (week_ago,))
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
