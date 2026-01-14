"""
Slack Notifier - Invia alert a Slack webhook
============================================

Per configurare:
1. Crea un Incoming Webhook in Slack: https://api.slack.com/messaging/webhooks
2. Imposta variabile ambiente: export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
3. Oppure passa URL al costruttore

Uso:
    from src.alerting.notifiers import SlackNotifier

    slack = SlackNotifier("https://hooks.slack.com/services/XXX/YYY/ZZZ")
    slack.send(alert)
"""

import json
import urllib.request
import urllib.error
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..alert_system import Alert


class SlackNotifier:
    """Notifier che invia alert a Slack via webhook"""

    # Emoji per severity
    SEVERITY_EMOJI = {
        "INFO": ":information_source:",
        "WARNING": ":warning:",
        "ERROR": ":x:",
        "CRITICAL": ":rotating_light:",
    }

    # Colori per attachment
    SEVERITY_COLOR = {
        "INFO": "#36a64f",      # Green
        "WARNING": "#f9a825",   # Yellow
        "ERROR": "#e74c3c",     # Red
        "CRITICAL": "#9b59b6",  # Purple
    }

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Inizializza Slack notifier.

        Args:
            webhook_url: URL del webhook Slack
        """
        self.webhook_url = webhook_url
        if not self.webhook_url:
            import os
            self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send(self, alert: "Alert") -> bool:
        """
        Invia alert a Slack.

        Args:
            alert: Alert da inviare

        Returns:
            True se inviato con successo
        """
        if not self.webhook_url:
            print("[SLACK NOTIFIER] Webhook URL not configured - skipping")
            return False

        try:
            emoji = self.SEVERITY_EMOJI.get(alert.severity.name, ":question:")
            color = self.SEVERITY_COLOR.get(alert.severity.name, "#808080")

            # Costruisci payload Slack
            payload = {
                "text": f"{emoji} *[{alert.severity.name}]* {alert.title}",
                "attachments": [
                    {
                        "color": color,
                        "fields": [
                            {
                                "title": "Source",
                                "value": alert.source,
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                "short": True
                            },
                            {
                                "title": "Message",
                                "value": alert.message[:500],  # Troncato
                                "short": False
                            },
                        ],
                        "footer": f"CervellaSwarm Alert | ID: {alert.id}",
                    }
                ]
            }

            # Aggiungi context se presente
            if alert.context:
                context_str = ", ".join(f"{k}: {v}" for k, v in alert.context.items())
                payload["attachments"][0]["fields"].append({
                    "title": "Context",
                    "value": context_str[:200],
                    "short": False
                })

            # Invia a Slack
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200

        except urllib.error.URLError as e:
            print(f"[SLACK NOTIFIER ERROR] Network error: {e}")
            return False
        except Exception as e:
            print(f"[SLACK NOTIFIER ERROR] {e}")
            return False
