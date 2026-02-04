"""
CervellaSwarm Analytics - Helper Module

Funzioni helper per output Rich/plain e setup console.
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

# Optional rich import
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich import box
    from rich.text import Text
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None
    Table = None
    Panel = None
    Layout = None
    box = None
    Text = None


def print_rich_or_plain(rich_fn, plain_fn, *args, **kwargs):
    """Helper per stampare con Rich se disponibile, altrimenti plain text."""
    if HAS_RICH:
        rich_fn(*args, **kwargs)
    else:
        plain_fn(*args, **kwargs)


def plain_print(text: str):
    """Stampa plain text (fallback per console.print)."""
    print(text)


def get_console():
    """Ritorna console Rich se disponibile."""
    return console


def rich_available() -> bool:
    """Check se Rich è disponibile."""
    return HAS_RICH
