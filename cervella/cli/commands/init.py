"""
cervella init - Inizializza un progetto con Cervella
"""

import os
import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command()
@click.option("--force", "-f", is_flag=True, help="Sovrascrive configurazione esistente")
def init(force: bool):
    """Inizializza Cervella in questo progetto.

    Crea la struttura .sncp/ per la memoria esterna
    e configura il progetto per usare Cervella.
    """
    cwd = os.getcwd()
    sncp_path = os.path.join(cwd, ".sncp")

    # Check se esiste già
    if os.path.exists(sncp_path) and not force:
        console.print("[yellow]Cervella è già inizializzata in questo progetto.[/yellow]")
        console.print("Usa --force per reinizializzare.")
        return

    console.print(Panel.fit(
        "[bold blue]Cervella[/bold blue] - Inizializzazione",
        subtitle="AI Team per Developer"
    ))

    # Crea struttura SNCP
    from sncp.manager import SNSCPManager
    manager = SNSCPManager(cwd)
    manager.initialize()

    console.print("\n[green]Cervella inizializzata![/green]")
    console.print(f"Creata struttura in: [cyan]{sncp_path}[/cyan]")
    console.print("\nProssimi passi:")
    console.print("  1. Configura la tua API key: [cyan]export ANTHROPIC_API_KEY=...[/cyan]")
    console.print("  2. Inizia a lavorare: [cyan]cervella task \"Il tuo task\"[/cyan]")
