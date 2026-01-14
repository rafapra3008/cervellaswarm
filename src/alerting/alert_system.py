"""
Alert System - Core del sistema di alerting CervellaSwarm
==========================================================

Monitora log per pattern critici e invia notifiche.

Funzionalita:
- Check periodico database eventi
- Pattern detection (errori ripetuti, task bloccati, etc)
- Multi-channel notifications (console, file, slack)
- Deduplication (evita spam)
- Severity scoring

Uso:
    from src.alerting import AlertSystem

    # Check manuale
    alerts = AlertSystem()
    found = alerts.check_recent_errors(hours=1)

    # Monitoring continuo
    alerts.start_monitoring(interval_seconds=300)

Versione: 1.0.0
Data: 14 Gennaio 2026
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import os


class AlertSeverity(Enum):
    """Livelli di severity per gli alert"""
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@dataclass
class Alert:
    """Rappresenta un singolo alert"""
    id: str
    severity: AlertSeverity
    title: str
    message: str
    source: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    dedupe_key: str = ""

    def __post_init__(self):
        if not self.dedupe_key:
            # Genera chiave per deduplication
            content = f"{self.severity.name}:{self.title}:{self.source}"
            self.dedupe_key = hashlib.md5(content.encode()).hexdigest()[:12]


class AlertSystem:
    """
    Sistema centrale di alerting per CervellaSwarm.

    Monitora il database eventi e genera alert per:
    - Errori critici
    - Task bloccati (stuck)
    - Pattern anomali
    - Problemi di sistema
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        config: Optional[Dict] = None
    ):
        """
        Inizializza il sistema di alerting.

        Args:
            db_path: Path al database SwarmLogger
            config: Configurazione opzionale
        """
        self.db_path = db_path or self._find_db()
        self.config = config or self._default_config()
        self.notifiers = []
        self._sent_alerts: Dict[str, datetime] = {}  # Dedupe cache

        # Inizializza notifiers di default
        self._init_notifiers()

    def _find_db(self) -> str:
        """Trova il database SwarmLogger"""
        possible_paths = [
            Path.home() / ".swarm" / "logs" / "swarm_events.db",
            Path.cwd() / ".swarm" / "logs" / "swarm_events.db",
            Path("/Users/rafapra/Developer/CervellaSwarm/.swarm/logs/swarm_events.db"),
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        # Fallback
        return str(possible_paths[0])

    def _default_config(self) -> Dict:
        """Configurazione di default"""
        return {
            # Soglie
            "error_threshold_per_hour": 5,  # Alert se > 5 errori/ora
            "stuck_task_minutes": 30,        # Task considerato stuck dopo 30 min
            "critical_keywords": ["CRITICAL", "FATAL", "CRASH", "OOM"],

            # Deduplication
            "dedupe_window_minutes": 60,     # Ignora duplicati per 1 ora

            # Notifiers
            "slack_webhook_url": os.getenv("SLACK_WEBHOOK_URL"),
            "alert_file_path": Path.home() / ".swarm" / "alerts.log",

            # Monitoring
            "check_interval_seconds": 300,   # 5 minuti
        }

    def _init_notifiers(self):
        """Inizializza i canali di notifica"""
        try:
            from .notifiers import ConsoleNotifier, FileNotifier
        except ImportError:
            # Fallback per esecuzione diretta
            from notifiers import ConsoleNotifier, FileNotifier

        # Console sempre attivo
        self.notifiers.append(ConsoleNotifier())

        # File alert log
        self.notifiers.append(FileNotifier(self.config["alert_file_path"]))

        # Slack se configurato
        if self.config.get("slack_webhook_url"):
            try:
                from .notifiers import SlackNotifier
            except ImportError:
                from notifiers import SlackNotifier
            self.notifiers.append(SlackNotifier(self.config["slack_webhook_url"]))

    def check_recent_errors(self, hours: int = 1) -> List[Alert]:
        """
        Controlla gli errori recenti nel database.

        Args:
            hours: Finestra temporale in ore

        Returns:
            Lista di Alert generati
        """
        alerts = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Query errori recenti
            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            cursor.execute("""
                SELECT timestamp, level, agent, message, task_id, trace_id
                FROM events
                WHERE level IN ('ERROR', 'CRITICAL')
                AND timestamp > ?
                ORDER BY timestamp DESC
            """, (since,))

            errors = cursor.fetchall()
            conn.close()

            if not errors:
                return []

            # Genera alert per errori critici
            for row in errors:
                timestamp, level, agent, message, task_id, trace_id = row

                severity = AlertSeverity.CRITICAL if level == "CRITICAL" else AlertSeverity.ERROR

                alert = Alert(
                    id=f"err_{trace_id or task_id or 'unknown'}_{timestamp[:19].replace(':', '')}",
                    severity=severity,
                    title=f"{level} in {agent}",
                    message=message[:500],  # Troncato
                    source=agent or "unknown",
                    timestamp=datetime.fromisoformat(timestamp),
                    context={
                        "task_id": task_id,
                        "trace_id": trace_id,
                        "level": level,
                    }
                )
                alerts.append(alert)

            # Check soglia errori/ora
            if len(errors) > self.config["error_threshold_per_hour"]:
                alerts.append(Alert(
                    id=f"threshold_{datetime.now().strftime('%Y%m%d%H')}",
                    severity=AlertSeverity.WARNING,
                    title="Alto numero di errori",
                    message=f"{len(errors)} errori nell'ultima ora (soglia: {self.config['error_threshold_per_hour']})",
                    source="alert_system",
                    timestamp=datetime.now(),
                    context={"error_count": len(errors)}
                ))

        except Exception as e:
            alerts.append(Alert(
                id=f"system_error_{datetime.now().strftime('%Y%m%d%H%M')}",
                severity=AlertSeverity.ERROR,
                title="Errore sistema alerting",
                message=str(e),
                source="alert_system",
                timestamp=datetime.now(),
            ))

        return alerts

    def check_stuck_tasks(self) -> List[Alert]:
        """
        Controlla task che potrebbero essere bloccati.

        Returns:
            Lista di Alert per task stuck
        """
        alerts = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            threshold = (datetime.now() - timedelta(
                minutes=self.config["stuck_task_minutes"]
            )).isoformat()

            # Cerca task iniziati ma non completati
            cursor.execute("""
                SELECT task_id, agent, timestamp, message
                FROM events
                WHERE level = 'INFO'
                AND message LIKE '%start%'
                AND timestamp < ?
                AND task_id NOT IN (
                    SELECT task_id FROM events
                    WHERE level = 'INFO'
                    AND (message LIKE '%complete%' OR message LIKE '%finish%' OR message LIKE '%done%')
                    AND timestamp > ?
                )
                LIMIT 10
            """, (threshold, threshold))

            stuck = cursor.fetchall()
            conn.close()

            for row in stuck:
                task_id, agent, timestamp, message = row

                alerts.append(Alert(
                    id=f"stuck_{task_id}",
                    severity=AlertSeverity.WARNING,
                    title=f"Task potenzialmente bloccato",
                    message=f"Task {task_id} avviato da {agent} sembra bloccato (>{self.config['stuck_task_minutes']} min)",
                    source=agent or "unknown",
                    timestamp=datetime.fromisoformat(timestamp),
                    context={"task_id": task_id}
                ))

        except Exception as e:
            pass  # Silently ignore DB errors for stuck check

        return alerts

    def _should_send(self, alert: Alert) -> bool:
        """
        Controlla se l'alert deve essere inviato (deduplication).

        Args:
            alert: Alert da verificare

        Returns:
            True se deve essere inviato
        """
        now = datetime.now()
        dedupe_window = timedelta(minutes=self.config["dedupe_window_minutes"])

        if alert.dedupe_key in self._sent_alerts:
            last_sent = self._sent_alerts[alert.dedupe_key]
            if now - last_sent < dedupe_window:
                return False  # Duplicato recente

        self._sent_alerts[alert.dedupe_key] = now
        return True

    def send_alert(self, alert: Alert) -> bool:
        """
        Invia un alert attraverso tutti i notifiers.

        Args:
            alert: Alert da inviare

        Returns:
            True se inviato con successo
        """
        if not self._should_send(alert):
            return False

        success = True
        for notifier in self.notifiers:
            try:
                notifier.send(alert)
            except Exception as e:
                success = False
                print(f"[ALERT ERROR] Notifier {notifier.__class__.__name__} failed: {e}")

        return success

    def run_checks(self) -> List[Alert]:
        """
        Esegue tutti i check e invia gli alert.

        Returns:
            Lista di tutti gli alert trovati
        """
        all_alerts = []

        # Check errori recenti
        error_alerts = self.check_recent_errors(hours=1)
        all_alerts.extend(error_alerts)

        # Check task stuck
        stuck_alerts = self.check_stuck_tasks()
        all_alerts.extend(stuck_alerts)

        # Invia tutti gli alert
        for alert in all_alerts:
            self.send_alert(alert)

        return all_alerts

    def start_monitoring(self, interval_seconds: Optional[int] = None):
        """
        Avvia monitoring continuo in foreground.

        Args:
            interval_seconds: Intervallo tra check (default da config)
        """
        import time

        interval = interval_seconds or self.config["check_interval_seconds"]

        print(f"[ALERT SYSTEM] Starting monitoring (interval: {interval}s)")
        print(f"[ALERT SYSTEM] Database: {self.db_path}")
        print(f"[ALERT SYSTEM] Notifiers: {[n.__class__.__name__ for n in self.notifiers]}")
        print("")

        try:
            while True:
                alerts = self.run_checks()

                if alerts:
                    print(f"[ALERT SYSTEM] {len(alerts)} alert(s) at {datetime.now().isoformat()}")
                else:
                    print(f"[ALERT SYSTEM] No alerts at {datetime.now().isoformat()}")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n[ALERT SYSTEM] Monitoring stopped")


# CLI Entry Point
if __name__ == "__main__":
    import sys

    system = AlertSystem()

    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        system.start_monitoring()
    else:
        # Single check
        alerts = system.run_checks()
        print(f"Found {len(alerts)} alert(s)")
