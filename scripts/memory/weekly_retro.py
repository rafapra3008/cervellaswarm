#!/usr/bin/env python3
"""
CervellaSwarm Weekly Retrospective v2.0.0 - Report Settimanale Automatico

Genera un report retrospettivo settimanale con:
- Metriche chiave (eventi totali, success rate, errori)
- Top 3 pattern errori
- Lezioni apprese della settimana
- Breakdown per agente
- Raccomandazioni automatiche
- 🆕 Lezioni suggerite basate su pattern ripetuti
- 🆕 Salvataggio report in markdown
- 🆕 Modalità quiet per cron jobs

Usage:
    python weekly_retro.py              → Report ultimi 7 giorni
    python weekly_retro.py -d 14        → Report ultimi 14 giorni
    python weekly_retro.py --save       → Salva in data/retro/
    python weekly_retro.py -s -q        → Salva in quiet mode (cron)
"""

__version__ = "2.0.0"
__version_date__ = "2026-01-01"

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# Import centralizzato path management
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path


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


def suggest_new_lessons(conn: sqlite3.Connection, period_start: str) -> List[Tuple[str, int, str]]:
    """
    Suggerisce nuove lezioni basandosi su pattern errori ripetuti.

    Analizza:
    1. Pattern errori con count >= 3 senza lezione associata
    2. Agenti con success rate < 80%

    Args:
        conn: Connessione database
        period_start: Data inizio periodo (ISO format)

    Returns:
        Lista di tuple (tipo_suggerimento, valore, descrizione)
    """
    cursor = conn.cursor()
    suggestions = []

    # 1. Pattern ripetuti senza lezione documentata
    cursor.execute("""
        SELECT ep.pattern_name, ep.occurrence_count
        FROM error_patterns ep
        WHERE ep.status = 'ACTIVE'
          AND ep.occurrence_count >= 3
          AND NOT EXISTS (
              SELECT 1 FROM lessons_learned ll
              WHERE ll.pattern LIKE '%' || ep.pattern_name || '%'
          )
        ORDER BY ep.occurrence_count DESC
        LIMIT 5
    """)
    patterns = cursor.fetchall()

    for pattern in patterns:
        suggestions.append((
            'pattern',
            pattern['occurrence_count'],
            f"Pattern '{pattern['pattern_name']}' ripetuto {pattern['occurrence_count']} volte senza lezione"
        ))

    # 2. Agenti con basso success rate
    cursor.execute(f"""
        SELECT
            agent_name,
            COUNT(*) as total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successes,
            ROUND(100.0 * SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
        FROM swarm_events
        WHERE datetime(timestamp) >= datetime('{period_start}')
          AND agent_name IS NOT NULL
        GROUP BY agent_name
        HAVING total >= 5 AND success_rate < 80
        ORDER BY success_rate ASC
        LIMIT 3
    """)
    low_performers = cursor.fetchall()

    for agent in low_performers:
        suggestions.append((
            'agent',
            int(agent['success_rate']),
            f"Agente '{agent['agent_name']}' con {agent['success_rate']}% success rate ({agent['total']} task)"
        ))

    return suggestions


def save_report(content: str, output_dir: Optional[Path] = None) -> Path:
    """
    Salva report in file markdown.

    Args:
        content: Contenuto report (plain text)
        output_dir: Directory output (default: data/retro/)

    Returns:
        Path al file salvato
    """
    if output_dir is None:
        script_dir = Path(__file__).parent
        output_dir = script_dir / "../../data/retro"

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{datetime.now().strftime('%Y-%m-%d')}.md"
    output_path = output_dir / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def generate_retro(days: int = 7, save_to_file: bool = False, quiet: bool = False, output_dir: Optional[Path] = None):
    """
    Genera weekly retrospective report.

    Args:
        days: Numero di giorni da analizzare (default: 7)
        save_to_file: Se True, salva report in file markdown
        quiet: Se True, output minimale (per cron)
        output_dir: Directory output custom
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Periodo analisi
    period_start = (datetime.now() - timedelta(days=days)).isoformat()
    period_end = datetime.now().isoformat()

    # Buffer per plain text (se save_to_file)
    plain_text = []

    if not quiet:
        console.print("\n")
        console.print(Panel(
            f"[bold magenta]📅 WEEKLY RETROSPECTIVE[/bold magenta]\n"
            f"[dim]Periodo: {period_start[:10]} → {period_end[:10]}[/dim]",
            style="magenta",
            box=box.DOUBLE
        ))
        console.print("\n")

    if save_to_file:
        plain_text.append("# WEEKLY RETROSPECTIVE\n")
        plain_text.append(f"**Periodo:** {period_start[:10]} → {period_end[:10]}\n")
        plain_text.append(f"**Generato:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

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

    if not quiet:
        metrics_table = Table(title="📊 METRICHE CHIAVE", box=box.SIMPLE, show_header=False)
        metrics_table.add_column("Metrica", style="cyan", width=20)
        metrics_table.add_column("Valore", justify="right", style="bold white")

        metrics_table.add_row("Eventi Totali", str(total))
        metrics_table.add_row("Successi", f"[green]{successes}[/green]")
        metrics_table.add_row("Errori", f"[red]{failures}[/red]")
        metrics_table.add_row("Success Rate", f"[bold]{success_rate:.1f}%[/bold]")

        console.print(metrics_table)
        console.print("\n")

    if save_to_file:
        plain_text.append("## 📊 METRICHE CHIAVE\n\n")
        plain_text.append(f"- **Eventi Totali:** {total}\n")
        plain_text.append(f"- **Successi:** {successes}\n")
        plain_text.append(f"- **Errori:** {failures}\n")
        plain_text.append(f"- **Success Rate:** {success_rate:.1f}%\n\n")

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
        if not quiet:
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

        if save_to_file:
            plain_text.append("## 🔍 TOP 3 PATTERN ERRORI\n\n")
            for pattern in top_patterns:
                plain_text.append(f"- **[{pattern['severity_level']}]** {pattern['pattern_name']} (Count: {pattern['occurrence_count']})\n")
            plain_text.append("\n")
    else:
        if not quiet:
            console.print("[dim]   Nessun pattern errore attivo[/dim]\n")
        if save_to_file:
            plain_text.append("## 🔍 TOP 3 PATTERN ERRORI\n\nNessun pattern attivo.\n\n")

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
        if not quiet:
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

        if save_to_file:
            plain_text.append(f"## 📚 LEZIONI APPRESE ({len(new_lessons)})\n\n")
            for lesson in new_lessons:
                plain_text.append(f"- **[{lesson['severity']}]** {lesson['pattern']}\n")
            plain_text.append("\n")
    else:
        if not quiet:
            console.print("[dim]   Nessuna nuova lezione questo periodo[/dim]\n")
        if save_to_file:
            plain_text.append("## 📚 LEZIONI APPRESE\n\nNessuna nuova lezione.\n\n")

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
        if not quiet:
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

        if save_to_file:
            plain_text.append("## 👥 BREAKDOWN PER AGENTE (Top 5)\n\n")
            plain_text.append("| Agente | Total | Success | Failures | Avg Duration |\n")
            plain_text.append("|--------|-------|---------|----------|-------------|\n")
            for agent in agents:
                avg_dur = f"{int(agent['avg_duration'])}ms" if agent['avg_duration'] else "N/A"
                plain_text.append(f"| {agent['agent_name'][:20]} | {agent['total']} | {agent['successes']} | {agent['failures']} | {avg_dur} |\n")
            plain_text.append("\n")
    else:
        if not quiet:
            console.print("[dim]   Nessun dato agente disponibile[/dim]\n")
        if save_to_file:
            plain_text.append("## 👥 BREAKDOWN PER AGENTE\n\nNessun dato disponibile.\n\n")

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

    if not quiet:
        recommendations_panel = Panel(
            "\n".join(recommendations),
            title="💡 RACCOMANDAZIONI",
            border_style="yellow"
        )
        console.print(recommendations_panel)
        console.print("\n")

    if save_to_file:
        plain_text.append("## 💡 RACCOMANDAZIONI\n\n")
        for rec in recommendations:
            plain_text.append(f"{rec}\n")
        plain_text.append("\n")

    # === 6. LEZIONI SUGGERITE (NUOVA FUNZIONALITÀ v2.0.0) ===

    suggestions = suggest_new_lessons(conn, period_start)

    if suggestions:
        # Pattern senza lezione
        pattern_suggestions = [s for s in suggestions if s[0] == 'pattern']
        # Agenti con basso success rate
        agent_suggestions = [s for s in suggestions if s[0] == 'agent']

        if not quiet:
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

        if save_to_file:
            plain_text.append("## 🎯 LEZIONI SUGGERITE\n\n")

            if pattern_suggestions:
                plain_text.append("**Pattern ripetuti senza lezione documentata:**\n\n")
                for _, count, desc in pattern_suggestions:
                    plain_text.append(f"- {desc}\n")
                plain_text.append("\n")

            if agent_suggestions:
                plain_text.append("**Agenti con basso success rate:**\n\n")
                for _, rate, desc in agent_suggestions:
                    plain_text.append(f"- {desc}\n")
                plain_text.append("\n")
    else:
        if not quiet:
            console.print("[dim]   Nessuna lezione suggerita - Sistema OK[/dim]\n")
        if save_to_file:
            plain_text.append("## 🎯 LEZIONI SUGGERITE\n\nNessuna lezione suggerita.\n\n")

    # === 7. PROSSIMI PASSI SUGGERITI ===

    next_steps = []

    if active_patterns_count > 0:
        next_steps.append("1. Review pattern attivi con `analytics.py patterns`")

    if active_lessons_count > 0:
        next_steps.append("2. Review lezioni attive con `analytics.py lessons`")

    if failures > 5:
        next_steps.append("3. Analizzare ultimi errori con `analytics.py events -n 20`")

    if not next_steps:
        next_steps.append("✅ Nessuna azione richiesta - Sistema OK!")

    if not quiet:
        steps_panel = Panel(
            "\n".join(next_steps),
            title="📝 PROSSIMI PASSI",
            border_style="cyan"
        )
        console.print(steps_panel)
        console.print("\n")

    if save_to_file:
        plain_text.append("## 📝 PROSSIMI PASSI\n\n")
        for step in next_steps:
            plain_text.append(f"{step}\n")
        plain_text.append("\n")

    # === SALVA REPORT SE RICHIESTO ===

    if save_to_file:
        report_content = "".join(plain_text)
        saved_path = save_report(report_content, output_dir)

        if quiet:
            # In quiet mode, solo il path
            print(f"Report salvato: {saved_path}")
        else:
            console.print(f"[green]✅ Report salvato:[/green] {saved_path}\n")

    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Weekly Retrospective v2.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python weekly_retro.py              # Report ultimi 7 giorni
  python weekly_retro.py -d 14        # Report ultimi 14 giorni
  python weekly_retro.py --save       # Salva report in data/retro/
  python weekly_retro.py --quiet      # Output minimale (per cron)
  python weekly_retro.py -s -q        # Salva report in modalità quiet
  python weekly_retro.py -o ~/reports # Salva in directory custom

Novità v2.0.0:
  🎯 Lezioni suggerite basate su pattern ripetuti
  💾 Salvataggio report in markdown
  🤐 Modalità quiet per cron jobs
        """
    )

    parser.add_argument(
        '-d', '--days',
        type=int,
        default=7,
        help='Numero di giorni da analizzare (default: 7)'
    )

    parser.add_argument(
        '-s', '--save',
        action='store_true',
        help='Salva report in file markdown (data/retro/YYYY-MM-DD.md)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Output minimale (per cron jobs)'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Directory output custom (default: data/retro/)'
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

    if args.days > 365 and not args.quiet:
        console.print("[yellow]⚠️  Attenzione: Analisi > 1 anno potrebbe essere lenta[/yellow]")

    # Genera retrospettiva
    generate_retro(
        days=args.days,
        save_to_file=args.save,
        quiet=args.quiet,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
