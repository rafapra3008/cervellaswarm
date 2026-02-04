"""
CervellaSwarm Weekly Retrospective - Output Module

Gestione rendering multi-formato (rich/plain/markdown).

v2.2.0: Tutte le funzioni _print_*_section spostate da cli.py qui.
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

from typing import List, Dict, Any, Optional
from enum import Enum

# Optional rich import
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


class OutputMode(str, Enum):
    """Modalità di output supportate."""
    RICH = "rich"
    PLAIN = "plain"
    MARKDOWN = "markdown"


def print_section_header(title: str, mode: OutputMode = OutputMode.RICH) -> Optional[str]:
    """
    Stampa header di sezione.

    Args:
        title: Titolo sezione
        mode: Modalità output (rich/plain/markdown)

    Returns:
        Stringa markdown se mode=MARKDOWN, altrimenti None (stampa diretta)
    """
    if mode == OutputMode.MARKDOWN:
        return f"## {title}\n\n"

    if mode == OutputMode.RICH and HAS_RICH:
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        console.print()
    else:
        print(f"\n{title}")
        print("-" * 40)

    return None


def print_table(
    data: List[Dict[str, Any]],
    columns: List[tuple],  # [(name, key, justify, style, width), ...]
    title: str,
    mode: OutputMode = OutputMode.RICH
) -> Optional[str]:
    """
    Stampa tabella dati.

    Args:
        data: Lista di dizionari con i dati
        columns: Lista di tuple (name, key, justify, style, width)
        title: Titolo tabella
        mode: Modalità output

    Returns:
        Stringa markdown se mode=MARKDOWN, altrimenti None
    """
    if not data:
        return None

    if mode == OutputMode.MARKDOWN:
        # Header markdown
        header = "| " + " | ".join([col[0] for col in columns]) + " |\n"
        separator = "|" + "|".join(["---" for _ in columns]) + "|\n"

        # Rows
        rows = []
        for row in data:
            cells = []
            for col in columns:
                key = col[1]
                value = row.get(key, "N/A")
                cells.append(str(value))
            rows.append("| " + " | ".join(cells) + " |")

        return header + separator + "\n".join(rows) + "\n\n"

    if mode == OutputMode.RICH and HAS_RICH:
        table = Table(title=title, box=box.SIMPLE)

        # Add columns
        for col in columns:
            name, _, justify, style, width = col
            table.add_column(name, justify=justify, style=style, width=width)

        # Add rows
        for row in data:
            cells = []
            for col in columns:
                key = col[1]
                value = row.get(key, "N/A")
                cells.append(str(value))
            table.add_row(*cells)

        console.print(table)
        console.print()
    else:
        # Plain text table
        print(title)
        print("-" * 70)

        # Header
        header_format = " ".join([f"{{:<{col[4] or 10}}}" for col in columns])
        header_values = [col[0] for col in columns]
        print(header_format.format(*header_values))
        print("-" * 70)

        # Rows
        for row in data:
            values = []
            for col in columns:
                key = col[1]
                value = row.get(key, "N/A")
                values.append(str(value))
            print(header_format.format(*values))
        print()

    return None


def print_panel(
    content: str,
    title: str,
    style: str = "white",
    mode: OutputMode = OutputMode.RICH
) -> Optional[str]:
    """
    Stampa panel/box con contenuto.

    Args:
        content: Contenuto da stampare
        title: Titolo panel
        style: Stile colore (rich)
        mode: Modalità output

    Returns:
        Stringa markdown se mode=MARKDOWN, altrimenti None
    """
    if mode == OutputMode.MARKDOWN:
        return f"**{title}:**\n\n{content}\n\n"

    if mode == OutputMode.RICH and HAS_RICH:
        panel = Panel(content, title=title, border_style=style)
        console.print(panel)
        console.print()
    else:
        print(f"\n{title}")
        print("-" * 40)
        print(content)
        print()

    return None


def print_metrics_table(metrics: Dict[str, Any], mode: OutputMode = OutputMode.RICH) -> Optional[str]:
    """
    Stampa tabella metriche chiave.

    Args:
        metrics: Dict con total, successes, failures, success_rate
        mode: Modalità output

    Returns:
        Stringa markdown se mode=MARKDOWN, altrimenti None
    """
    if mode == OutputMode.MARKDOWN:
        md = "## 📊 METRICHE CHIAVE\n\n"
        md += f"- **Eventi Totali:** {metrics['total']}\n"
        md += f"- **Successi:** {metrics['successes']}\n"
        md += f"- **Errori:** {metrics['failures']}\n"
        md += f"- **Success Rate:** {metrics['success_rate']:.1f}%\n\n"
        return md

    if mode == OutputMode.RICH and HAS_RICH:
        table = Table(title="📊 METRICHE CHIAVE", box=box.SIMPLE, show_header=False)
        table.add_column("Metrica", style="cyan", width=20)
        table.add_column("Valore", justify="right", style="bold white")

        table.add_row("Eventi Totali", str(metrics['total']))
        table.add_row("Successi", f"[green]{metrics['successes']}[/green]")
        table.add_row("Errori", f"[red]{metrics['failures']}[/red]")
        table.add_row("Success Rate", f"[bold]{metrics['success_rate']:.1f}%[/bold]")

        console.print(table)
        console.print("\n")
    else:
        print("📊 METRICHE CHIAVE")
        print("-" * 40)
        print(f"Eventi Totali:    {metrics['total']}")
        print(f"Successi:         {metrics['successes']}")
        print(f"Errori:           {metrics['failures']}")
        print(f"Success Rate:     {metrics['success_rate']:.1f}%")
        print()

    return None


def print_patterns_section(patterns: List[Dict[str, Any]]) -> None:
    """Stampa sezione pattern errori."""
    if HAS_RICH:
        patterns_table = Table(title="🔍 TOP 3 PATTERN ERRORI", box=box.SIMPLE)
        patterns_table.add_column("Severity", justify="center", width=15)
        patterns_table.add_column("Pattern", style="white")
        patterns_table.add_column("Count", justify="right", style="yellow", width=8)

        for pattern in patterns:
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
        print("🔍 TOP 3 PATTERN ERRORI")
        print("-" * 40)
        for pattern in patterns:
            severity_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(pattern['severity_level'], '⚪')
            print(f"{severity_emoji} [{pattern['severity_level']}] {pattern['pattern_name'][:60]}")
            print(f"   Count: {pattern['occurrence_count']}")
        print()


def print_lessons_section(lessons: List[Dict[str, Any]]) -> None:
    """Stampa sezione lezioni apprese."""
    if HAS_RICH:
        lessons_text = "\n".join([
            f"• [{l['severity']}] {l['pattern']}"
            for l in lessons
        ])
        lessons_panel = Panel(
            lessons_text,
            title=f"📚 LEZIONI APPRESE ({len(lessons)})",
            border_style="green"
        )
        console.print(lessons_panel)
        console.print("\n")
    else:
        print(f"📚 LEZIONI APPRESE ({len(lessons)})")
        print("-" * 40)
        for l in lessons:
            print(f"• [{l['severity']}] {l['pattern']}")
        print()


def print_agents_section(agents: List[Dict[str, Any]]) -> None:
    """Stampa sezione breakdown agenti."""
    if HAS_RICH:
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
        print("👥 BREAKDOWN PER AGENTE (Top 5)")
        print("-" * 70)
        print(f"{'Agente':<20} {'Total':>8} {'Success':>8} {'Failures':>8} {'Avg Duration':>12}")
        print("-" * 70)
        for agent in agents:
            avg_dur = f"{int(agent['avg_duration'])}ms" if agent['avg_duration'] else "N/A"
            print(f"{agent['agent_name'][:20]:<20} {agent['total']:>8} {agent['successes']:>8} {agent['failures']:>8} {avg_dur:>12}")
        print()


def print_recommendations_section(recommendations: List[str]) -> None:
    """Stampa sezione raccomandazioni."""
    if HAS_RICH:
        recommendations_panel = Panel(
            "\n".join(recommendations),
            title="💡 RACCOMANDAZIONI",
            border_style="yellow"
        )
        console.print(recommendations_panel)
        console.print("\n")
    else:
        print("💡 RACCOMANDAZIONI")
        print("-" * 40)
        for rec in recommendations:
            print(rec)
        print()


def print_suggestions_section(pattern_suggestions: List, agent_suggestions: List) -> None:
    """Stampa sezione lezioni suggerite."""
    if HAS_RICH:
        suggestions_text = []

        if pattern_suggestions:
            suggestions_text.append("[bold yellow]Pattern ripetuti senza lezione documentata:[/bold yellow]")
            for _, count, desc in pattern_suggestions:
                suggestions_text.append(f"  • {desc}")
            suggestions_text.append("")

        if agent_suggestions:
            suggestions_text.append("[bold orange]Agenti con basso success rate:[/bold orange]")
            for _, rate, desc in agent_suggestions:
                suggestions_text.append(f"  • {desc}")

        suggestions_panel = Panel(
            "\n".join(suggestions_text),
            title="🎯 LEZIONI SUGGERITE (Nuovo in v2.0.0)",
            border_style="magenta"
        )
        console.print(suggestions_panel)
        console.print("\n")
    else:
        print("🎯 LEZIONI SUGGERITE")
        print("-" * 40)

        if pattern_suggestions:
            print("Pattern ripetuti senza lezione documentata:")
            for _, count, desc in pattern_suggestions:
                print(f"  • {desc}")
            print()

        if agent_suggestions:
            print("Agenti con basso success rate:")
            for _, rate, desc in agent_suggestions:
                print(f"  • {desc}")
        print()


def print_next_steps_section(next_steps: List[str]) -> None:
    """Stampa sezione prossimi passi."""
    if HAS_RICH:
        steps_panel = Panel(
            "\n".join(next_steps),
            title="📝 PROSSIMI PASSI",
            border_style="cyan"
        )
        console.print(steps_panel)
        console.print("\n")
    else:
        print("📝 PROSSIMI PASSI")
        print("-" * 40)
        for step in next_steps:
            print(step)
        print()


def print_empty_message(message: str) -> None:
    """Stampa messaggio vuoto."""
    if HAS_RICH:
        console.print(f"[dim]   {message}[/dim]\n")
    else:
        print(f"   {message}\n")


def print_header(period_start: str, period_end: str, quiet: bool = False) -> None:
    """Stampa header retrospettiva."""
    if quiet:
        return

    if HAS_RICH:
        console.print("\n")
        console.print(Panel(
            f"[bold magenta]📅 WEEKLY RETROSPECTIVE[/bold magenta]\n"
            f"[dim]Periodo: {period_start[:10]} → {period_end[:10]}[/dim]",
            style="magenta",
            box=box.DOUBLE
        ))
        console.print("\n")
    else:
        print("\n" + "="*60)
        print("📅 WEEKLY RETROSPECTIVE")
        print(f"Periodo: {period_start[:10]} → {period_end[:10]}")
        print("="*60 + "\n")
