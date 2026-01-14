"""
Console Notifier - Stampa alert su console
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..alert_system import Alert, AlertSeverity


class ConsoleNotifier:
    """Notifier che stampa alert su console con colori"""

    # ANSI colors
    COLORS = {
        "INFO": "\033[94m",      # Blue
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",
    }

    def send(self, alert: "Alert") -> bool:
        """
        Stampa alert su console.

        Args:
            alert: Alert da stampare

        Returns:
            True sempre (console non fallisce)
        """
        color = self.COLORS.get(alert.severity.name, "")
        reset = self.COLORS["RESET"]

        icon = self._get_icon(alert.severity.name)

        print(f"\n{color}{'='*60}{reset}")
        print(f"{color}{icon} [{alert.severity.name}] {alert.title}{reset}")
        print(f"{'='*60}")
        print(f"Source: {alert.source}")
        print(f"Time:   {alert.timestamp.isoformat()}")
        print(f"ID:     {alert.id}")
        print(f"\n{alert.message}")

        if alert.context:
            print(f"\nContext: {alert.context}")

        print(f"{'='*60}\n")

        return True

    def _get_icon(self, severity: str) -> str:
        """Ritorna icona per severity"""
        icons = {
            "INFO": "[i]",
            "WARNING": "[!]",
            "ERROR": "[X]",
            "CRITICAL": "[!!!]",
        }
        return icons.get(severity, "[?]")
