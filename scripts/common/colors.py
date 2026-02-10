#!/usr/bin/env python3
"""
CervellaSwarm - Centralized ANSI Colors
=======================================

Colori ANSI centralizzati per output CLI consistente.
Elimina duplicazione colori presente in 3+ file.

Versione: 1.0.0
Data: 19 Gennaio 2026 - W4 Day 1

USAGE:
    from common.colors import Colors, RED, GREEN, RESET

    # Usando la classe
    print(f"{Colors.GREEN}Success!{Colors.RESET}")

    # Usando le costanti (shortcut)
    print(f"{RED}Error!{RESET}")

    # Usando get_severity_color
    color = get_severity_color("HIGH")
    print(f"{color}Warning message{RESET}")
"""


class Colors:
    """ANSI color constants per output CLI."""

    # Styles
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Base colors (30-37)
    BLACK = "\033[30m"
    RED_BASE = "\033[31m"
    GREEN_BASE = "\033[32m"
    YELLOW_BASE = "\033[33m"
    BLUE_BASE = "\033[34m"
    MAGENTA_BASE = "\033[35m"
    CYAN_BASE = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors (90-97) - i piu usati
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

    # Bright aliases for dashboard compatibility
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @staticmethod
    def strip(text: str) -> str:
        """Rimuove tutti i codici colore ANSI da una stringa."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)


# Shortcut per compatibilita backward e comodita
RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
BLUE = Colors.BLUE
MAGENTA = Colors.MAGENTA
CYAN = Colors.CYAN
RESET = Colors.RESET
BOLD = Colors.BOLD
DIM = Colors.DIM


def get_severity_color(severity: str) -> str:
    """
    Ritorna il colore ANSI per il livello di severity.

    Args:
        severity: Livello ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")

    Returns:
        Codice ANSI del colore corrispondente
    """
    colors = {
        "CRITICAL": RED,
        "HIGH": YELLOW,
        "MEDIUM": CYAN,
        "LOW": GREEN,
        "INFO": BLUE,
    }
    return colors.get(severity.upper(), RESET)


def colorize(text: str, color: str) -> str:
    """
    Avvolge il testo con il colore specificato.

    Args:
        text: Testo da colorare
        color: Codice ANSI del colore

    Returns:
        Testo con colore applicato

    Example:
        >>> print(colorize("Hello", GREEN))
        # Stampa "Hello" in verde
    """
    return f"{color}{text}{RESET}"


def success(text: str) -> str:
    """Formatta testo come success (verde)."""
    return colorize(text, GREEN)


def error(text: str) -> str:
    """Formatta testo come error (rosso)."""
    return colorize(text, RED)


def warning(text: str) -> str:
    """Formatta testo come warning (giallo)."""
    return colorize(text, YELLOW)


def info(text: str) -> str:
    """Formatta testo come info (ciano)."""
    return colorize(text, CYAN)
