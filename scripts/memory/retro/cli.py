"""
CervellaSwarm Weekly Retrospective - CLI Entry Point

Entry point CLI con main() e generate_retro().
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Optional rich import
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Import centralizzato (W4 DRY - Sessione 284)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.paths import get_db_path
from common.db import connect_db, DatabaseNotFoundError, DatabaseConnectionError

# Import moduli interni
from .sections import (
    fetch_metrics,
    fetch_top_patterns,
    fetch_lessons,
    fetch_agent_breakdown,
    generate_recommendations,
    generate_next_steps
)
from .suggestions import suggest_new_lessons
from .output import (
    print_metrics_table,
    print_header,
    print_patterns_section,
    print_lessons_section,
    print_agents_section,
    print_recommendations_section,
    print_suggestions_section,
    print_next_steps_section,
    print_empty_message,
    OutputMode
)


__version__ = "2.2.0"
__version_date__ = "2026-02-04"


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
        output_dir = script_dir / "../../../data/retro"

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
    # Setup
    conn = connect_db()
    period_start = (datetime.now() - timedelta(days=days)).isoformat()
    period_end = datetime.now().isoformat()
    plain_text = [] if save_to_file else None

    # Fetch all data
    metrics = fetch_metrics(conn, period_start)
    patterns = fetch_top_patterns(conn, limit=3)
    lessons = fetch_lessons(conn, period_start, limit=5)
    agents = fetch_agent_breakdown(conn, period_start, limit=5)
    recommendations = generate_recommendations(metrics, conn)
    suggestions = suggest_new_lessons(conn, period_start)
    next_steps = generate_next_steps(conn, metrics)

    # Print header
    print_header(period_start, period_end, quiet)

    # Save header to markdown
    if save_to_file:
        plain_text.append("# WEEKLY RETROSPECTIVE\n")
        plain_text.append(f"**Periodo:** {period_start[:10]} → {period_end[:10]}\n")
        plain_text.append(f"**Generato:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    # Print metrics
    _print_and_save_metrics(metrics, plain_text, quiet)

    # Print patterns
    _print_and_save_patterns(patterns, plain_text, quiet)

    # Print lessons
    _print_and_save_lessons(lessons, plain_text, quiet)

    # Print agents
    _print_and_save_agents(agents, plain_text, quiet)

    # Print recommendations
    _print_and_save_recommendations(recommendations, plain_text, quiet)

    # Print suggestions
    _print_and_save_suggestions(suggestions, plain_text, quiet)

    # Print next steps
    _print_and_save_next_steps(next_steps, plain_text, quiet)

    # Save report if requested
    if save_to_file:
        _save_and_notify(plain_text, output_dir, quiet)

    conn.close()


# === HELPER FUNCTIONS (print + save sections) ===

def _print_and_save_metrics(metrics, plain_text, quiet):
    """Stampa e salva sezione metriche."""
    if not quiet:
        mode = OutputMode.RICH if HAS_RICH else OutputMode.PLAIN
        print_metrics_table(metrics, mode)

    if plain_text is not None:
        md_metrics = print_metrics_table(metrics, OutputMode.MARKDOWN)
        plain_text.append(md_metrics)


def _print_and_save_patterns(patterns, plain_text, quiet):
    """Stampa e salva sezione pattern."""
    if patterns:
        if not quiet:
            print_patterns_section(patterns)

        if plain_text is not None:
            plain_text.append("## 🔍 TOP 3 PATTERN ERRORI\n\n")
            for pattern in patterns:
                plain_text.append(f"- **[{pattern['severity_level']}]** {pattern['pattern_name']} (Count: {pattern['occurrence_count']})\n")
            plain_text.append("\n")
    else:
        if not quiet:
            print_empty_message("Nessun pattern errore attivo")
        if plain_text is not None:
            plain_text.append("## 🔍 TOP 3 PATTERN ERRORI\n\nNessun pattern attivo.\n\n")


def _print_and_save_lessons(lessons, plain_text, quiet):
    """Stampa e salva sezione lezioni."""
    if lessons:
        if not quiet:
            print_lessons_section(lessons)

        if plain_text is not None:
            plain_text.append(f"## 📚 LEZIONI APPRESE ({len(lessons)})\n\n")
            for lesson in lessons:
                plain_text.append(f"- **[{lesson['severity']}]** {lesson['pattern']}\n")
            plain_text.append("\n")
    else:
        if not quiet:
            print_empty_message("Nessuna nuova lezione questo periodo")
        if plain_text is not None:
            plain_text.append("## 📚 LEZIONI APPRESE\n\nNessuna nuova lezione.\n\n")


def _print_and_save_agents(agents, plain_text, quiet):
    """Stampa e salva sezione agenti."""
    if agents:
        if not quiet:
            print_agents_section(agents)

        if plain_text is not None:
            plain_text.append("## 👥 BREAKDOWN PER AGENTE (Top 5)\n\n")
            plain_text.append("| Agente | Total | Success | Failures | Avg Duration |\n")
            plain_text.append("|--------|-------|---------|----------|-------------|\n")
            for agent in agents:
                avg_dur = f"{int(agent['avg_duration'])}ms" if agent['avg_duration'] else "N/A"
                plain_text.append(f"| {agent['agent_name'][:20]} | {agent['total']} | {agent['successes']} | {agent['failures']} | {avg_dur} |\n")
            plain_text.append("\n")
    else:
        if not quiet:
            print_empty_message("Nessun dato agente disponibile")
        if plain_text is not None:
            plain_text.append("## 👥 BREAKDOWN PER AGENTE\n\nNessun dato disponibile.\n\n")


def _print_and_save_recommendations(recommendations, plain_text, quiet):
    """Stampa e salva sezione raccomandazioni."""
    if not quiet:
        print_recommendations_section(recommendations)

    if plain_text is not None:
        plain_text.append("## 💡 RACCOMANDAZIONI\n\n")
        for rec in recommendations:
            plain_text.append(f"{rec}\n")
        plain_text.append("\n")


def _print_and_save_suggestions(suggestions, plain_text, quiet):
    """Stampa e salva sezione suggerimenti."""
    if suggestions:
        pattern_suggestions = [s for s in suggestions if s[0] == 'pattern']
        agent_suggestions = [s for s in suggestions if s[0] == 'agent']

        if not quiet:
            print_suggestions_section(pattern_suggestions, agent_suggestions)

        if plain_text is not None:
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
            print_empty_message("Nessuna lezione suggerita - Sistema OK")
        if plain_text is not None:
            plain_text.append("## 🎯 LEZIONI SUGGERITE\n\nNessuna lezione suggerita.\n\n")


def _print_and_save_next_steps(next_steps, plain_text, quiet):
    """Stampa e salva sezione next steps."""
    if not quiet:
        print_next_steps_section(next_steps)

    if plain_text is not None:
        plain_text.append("## 📝 PROSSIMI PASSI\n\n")
        for step in next_steps:
            plain_text.append(f"{step}\n")
        plain_text.append("\n")


def _save_and_notify(plain_text, output_dir, quiet):
    """Salva report e notifica utente."""
    report_content = "".join(plain_text)
    saved_path = save_report(report_content, output_dir)

    if quiet:
        print(f"Report salvato: {saved_path}")
    else:
        if HAS_RICH:
            console.print(f"[green]✅ Report salvato:[/green] {saved_path}\n")
        else:
            print(f"✅ Report salvato: {saved_path}\n")


def main():
    """Entry point CLI."""
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Weekly Retrospective v2.2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python weekly_retro.py              # Report ultimi 7 giorni
  python weekly_retro.py -d 14        # Report ultimi 14 giorni
  python weekly_retro.py --save       # Salva report in data/retro/
  python weekly_retro.py --quiet      # Output minimale (per cron)
  python weekly_retro.py -s -q        # Salva report in modalità quiet
  python weekly_retro.py -o ~/reports # Salva in directory custom

Novità v2.2.0 (Step 2 Refactor):
  🔒 SECURITY FIX: SQL injection eliminato (parametrized queries)
  📦 Funzioni _print_* spostate in output.py
  🎯 generate_retro() ridotto a 60 righe (orchestratore puro)
  ✅ cli.py sceso da 527 a 364 righe
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
        if HAS_RICH:
            console.print("[red]❌ Errore: --days deve essere >= 1[/red]")
        else:
            print("❌ Errore: --days deve essere >= 1")
        sys.exit(1)

    if args.days > 365 and not args.quiet:
        if HAS_RICH:
            console.print("[yellow]⚠️  Attenzione: Analisi > 1 anno potrebbe essere lenta[/yellow]")
        else:
            print("⚠️  Attenzione: Analisi > 1 anno potrebbe essere lenta")

    # Genera retrospettiva
    generate_retro(
        days=args.days,
        save_to_file=args.save,
        quiet=args.quiet,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
