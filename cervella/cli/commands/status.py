"""
cervella status - Mostra stato del progetto
"""

import os
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Output dettagliato")
def status(verbose: bool):
    """Mostra lo stato di Cervella nel progetto corrente.

    Visualizza:
    - Stato inizializzazione
    - Agenti disponibili
    - Ultimi task eseguiti
    - Memoria SNCP
    """
    cwd = os.getcwd()
    sncp_path = os.path.join(cwd, ".sncp")

    # Header
    console.print(Panel.fit(
        "[bold blue]Cervella[/bold blue] - Status",
        subtitle=cwd
    ))

    # Check inizializzazione
    if not os.path.exists(sncp_path):
        console.print("\n[yellow]Cervella non inizializzata.[/yellow]")
        console.print("Esegui: [cyan]cervella init[/cyan]")
        return

    console.print("\n[green]Cervella attiva[/green]")

    # Tabella agenti
    table = Table(title="Agenti Disponibili")
    table.add_column("Agente", style="cyan")
    table.add_column("Specializzazione", style="white")
    table.add_column("Status", style="green")

    from agents.loader import AgentLoader
    loader = AgentLoader()
    agents = loader.list_agents()

    for agent in agents:
        table.add_row(
            agent.name,
            agent.specialization,
            "Pronto"
        )

    console.print(table)

    # Memoria SNCP
    if verbose:
        console.print("\n[bold]Memoria SNCP:[/bold]")
        from sncp.manager import SNSCPManager
        manager = SNSCPManager(cwd)
        stats = manager.get_stats()
        console.print(f"  Idee: {stats['idee']}")
        console.print(f"  Decisioni: {stats['decisioni']}")
        console.print(f"  Sessioni: {stats['sessioni']}")
