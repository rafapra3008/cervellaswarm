"""
Notifiers per il sistema di alerting CervellaSwarm
==================================================

Canali di notifica disponibili:
- ConsoleNotifier: Stampa su console (sempre attivo)
- FileNotifier: Scrive su file log
- SlackNotifier: Invia a Slack webhook

Uso:
    from src.alerting.notifiers import ConsoleNotifier, SlackNotifier

    console = ConsoleNotifier()
    console.send(alert)

    slack = SlackNotifier("https://hooks.slack.com/...")
    slack.send(alert)
"""

from .console_notifier import ConsoleNotifier
from .file_notifier import FileNotifier
from .slack_notifier import SlackNotifier

__all__ = ['ConsoleNotifier', 'FileNotifier', 'SlackNotifier']
