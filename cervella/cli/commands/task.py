"""
cervella task - Delega un task agli agenti
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

console = Console()


@click.command()
@click.argument("description", required=True)
@click.option("--agent", "-a", default=None, help="Specifica agente (default: Regina decide)")
@click.option("--dry-run", is_flag=True, help="Mostra cosa farebbe senza eseguire")
def task(description: str, agent: str, dry_run: bool):
    """Delega un task agli agenti Cervella.

    La Regina analizza il task e lo assegna all'agente più adatto.

    Esempi:

        cervella task "Implementa autenticazione JWT"

        cervella task "Scrivi test per il modulo users" --agent tester

        cervella task "Analizza i competitor" --agent scienziata
    """
    console.print(Panel.fit(
        f"[bold]Task:[/bold] {description}",
        title="Cervella",
        border_style="blue"
    ))

    if dry_run:
        console.print("\n[yellow][DRY RUN] Ecco cosa farei:[/yellow]")
        console.print(f"  1. Analizzare il task")
        console.print(f"  2. Scegliere l'agente migliore")
        console.print(f"  3. Delegare e monitorare")
        return

    # Import e esegui
    from agents.runner import AgentRunner
    from api.client import ClaudeClient

    try:
        client = ClaudeClient()
        runner = AgentRunner(client)

        with console.status("[bold blue]Regina sta analizzando...[/bold blue]"):
            result = runner.run_task(description, agent_name=agent)

        console.print("\n[green]Task completato![/green]")
        console.print(Panel(result.output, title="Risultato", border_style="green"))

        if result.files_created:
            console.print("\n[cyan]File creati:[/cyan]")
            for f in result.files_created:
                console.print(f"  - {f}")

    except Exception as e:
        console.print(f"\n[red]Errore:[/red] {e}")
        raise click.Abort()
