"""
cervella status - Mostra stato del progetto
"""

import os
import click
from pathlib import Path
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
    - Tier e usage
    - Agenti disponibili
    - Memoria SNCP
    """
    cwd = os.getcwd()
    sncp_path = Path(cwd) / ".sncp"

    # Header
    console.print(Panel.fit(
        "[bold blue]Cervella[/bold blue] - Status",
        subtitle=cwd
    ))

    # Check inizializzazione
    if not sncp_path.exists():
        console.print("\n[yellow]Cervella non inizializzata.[/yellow]")
        console.print("Esegui: [cyan]cervella init[/cyan]")
        return

    console.print("\n[green]Cervella attiva[/green]")

    # Tier e Usage
    from tier.tier_manager import TierManager
    tier_mgr = TierManager(sncp_path)
    tier_status = tier_mgr.get_status_summary()

    # Tier Panel
    tier_color = "green" if tier_status["tier_type"] != "free" else "yellow"
    tier_info = f"[bold {tier_color}]{tier_status['tier']}[/bold {tier_color}]"
    if tier_status["price"] != "Gratis":
        tier_info += f" ({tier_status['price']})"

    console.print(f"\n[bold]Tier:[/bold] {tier_info}")

    # Usage
    if tier_status["is_unlimited"]:
        usage_display = f"[green]{tier_status['tasks_this_month']} task questo mese (illimitati)[/green]"
    else:
        remaining = tier_status["tasks_remaining"]
        if remaining <= 5:
            color = "red" if remaining <= 0 else "yellow"
            usage_display = f"[{color}]{tier_status['tasks_display']} task ({remaining} rimanenti)[/{color}]"
        else:
            usage_display = f"{tier_status['tasks_display']} task"
    console.print(f"[bold]Usage:[/bold] {usage_display}")

    # Tabella agenti
    from agents.loader import AgentLoader
    loader = AgentLoader()
    all_agents = loader.list_agents()
    available_agents = tier_mgr.get_available_agents()

    table = Table(title=f"Agenti ({tier_status['agents_count']}/{tier_status['agents_total']} disponibili)")
    table.add_column("Agente", style="cyan")
    table.add_column("Specializzazione", style="white")
    table.add_column("Status", style="green")

    for agent in all_agents:
        clean_name = agent.name.replace("cervella-", "")
        if clean_name in available_agents:
            status_text = "[green]Pronto[/green]"
        else:
            status_text = "[dim]Pro richiesto[/dim]"

        table.add_row(
            agent.name,
            agent.specialization,
            status_text
        )

    console.print(table)

    # Upgrade hint per Free
    if tier_status["tier_type"] == "free":
        console.print("\n[dim]Upgrade a Pro per tutti i 17 agenti: cervella upgrade[/dim]")

    # Memoria SNCP
    if verbose:
        console.print("\n[bold]Memoria SNCP:[/bold]")
        from sncp.manager import SNSCPManager
        manager = SNSCPManager(cwd)
        stats = manager.get_stats()
        console.print(f"  Idee: {stats['idee']}")
        console.print(f"  Decisioni: {stats['decisioni']}")
        console.print(f"  Sessioni: {stats['sessioni']}")

        # Features tier
        console.print(f"\n[bold]Features {tier_status['tier']}:[/bold]")
        for feature in tier_status["features"]:
            console.print(f"  - {feature}")
