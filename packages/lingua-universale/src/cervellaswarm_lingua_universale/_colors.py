# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared ANSI color state for CLI and REPL (C3.6).

Respects the `NO_COLOR <https://no-color.org/>`_ de-facto standard,
``FORCE_COLOR``, and ``CLICOLOR_FORCE`` environment variables.

Usage::

    from ._colors import colors, init_colors

    init_colors()          # call once at startup
    print(f"{colors.GREEN}OK{colors.RESET}")
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass


@dataclass
class _ColorState:
    """Mutable holder for ANSI escape sequences."""

    RESET: str = ""
    BOLD: str = ""
    RED: str = ""
    GREEN: str = ""
    YELLOW: str = ""
    CYAN: str = ""


colors = _ColorState()


def init_colors() -> None:
    """Enable ANSI colors respecting NO_COLOR / FORCE_COLOR / TTY."""
    if os.environ.get("NO_COLOR"):
        return
    force = os.environ.get("FORCE_COLOR") or os.environ.get("CLICOLOR_FORCE")
    is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    if force or is_tty:
        colors.RESET = "\033[0m"
        colors.BOLD = "\033[1m"
        colors.RED = "\033[31m"
        colors.GREEN = "\033[32m"
        colors.YELLOW = "\033[33m"
        colors.CYAN = "\033[36m"


def reset_colors() -> None:
    """Reset all colors to empty strings (useful for testing)."""
    colors.RESET = ""
    colors.BOLD = ""
    colors.RED = ""
    colors.GREEN = ""
    colors.YELLOW = ""
    colors.CYAN = ""
