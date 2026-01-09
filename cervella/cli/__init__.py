"""
Cervella CLI - AI Team per Developer Professionali

"Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"
"""

import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option(version="0.1.0", prog_name="cervella")
def main():
    """Cervella - AI Team per Developer Professionali

    16 agenti specializzati orchestrati da una Regina.
    """
    pass


# Import e registra i comandi
from cli.commands import init, task, status, checkpoint

main.add_command(init.init)
main.add_command(task.task)
main.add_command(status.status)
main.add_command(checkpoint.checkpoint)


if __name__ == "__main__":
    main()
