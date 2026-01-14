"""
Pattern Detectors per il sistema di alerting
=============================================

Rileva pattern critici nei log:
- Errori ripetuti
- Keyword critiche
- Anomalie di frequenza
- Task falliti

Uso:
    from src.alerting.detectors import PatternDetector

    detector = PatternDetector(db_path)
    patterns = detector.detect_all()
"""

import sqlite3
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DetectedPattern:
    """Pattern rilevato"""
    pattern_type: str
    description: str
    count: int
    severity: str
    samples: List[str]
    context: Dict[str, Any]


class PatternDetector:
    """Rileva pattern critici nei log"""

    # Keyword che indicano problemi critici
    CRITICAL_KEYWORDS = [
        r"CRITICAL",
        r"FATAL",
        r"CRASH",
        r"OOM",
        r"OutOfMemory",
        r"Segmentation fault",
        r"SIGKILL",
        r"SIGTERM",
        r"ConnectionRefused",
        r"Timeout",
        r"Deadlock",
    ]

    # Pattern che indicano problemi ricorrenti
    RECURRING_PATTERNS = [
        r"retry",
        r"failed.*attempt",
        r"reconnect",
        r"rate.?limit",
    ]

    def __init__(self, db_path: str):
        """
        Inizializza detector.

        Args:
            db_path: Path al database eventi
        """
        self.db_path = db_path

    def detect_critical_keywords(self, hours: int = 24) -> List[DetectedPattern]:
        """
        Cerca keyword critiche nei log.

        Args:
            hours: Finestra temporale

        Returns:
            Lista di pattern rilevati
        """
        patterns = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            since = (datetime.now() - timedelta(hours=hours)).isoformat()

            for keyword in self.CRITICAL_KEYWORDS:
                cursor.execute("""
                    SELECT COUNT(*), GROUP_CONCAT(message, ' | ')
                    FROM events
                    WHERE message LIKE ?
                    AND timestamp > ?
                """, (f"%{keyword}%", since))

                count, samples = cursor.fetchone()

                if count and count > 0:
                    patterns.append(DetectedPattern(
                        pattern_type="critical_keyword",
                        description=f"Keyword critica trovata: {keyword}",
                        count=count,
                        severity="CRITICAL" if count > 5 else "WARNING",
                        samples=(samples or "")[:500].split(" | ")[:3],
                        context={"keyword": keyword, "hours": hours}
                    ))

            conn.close()

        except Exception as e:
            patterns.append(DetectedPattern(
                pattern_type="detector_error",
                description=f"Errore detector: {e}",
                count=1,
                severity="ERROR",
                samples=[str(e)],
                context={}
            ))

        return patterns

    def detect_error_spikes(
        self,
        threshold_per_hour: int = 10,
        hours: int = 6
    ) -> List[DetectedPattern]:
        """
        Rileva spike di errori.

        Args:
            threshold_per_hour: Soglia errori/ora
            hours: Finestra temporale

        Returns:
            Pattern rilevati
        """
        patterns = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Conta errori per ora
            cursor.execute("""
                SELECT
                    strftime('%Y-%m-%d %H:00', timestamp) as hour,
                    COUNT(*) as count
                FROM events
                WHERE level IN ('ERROR', 'CRITICAL')
                AND timestamp > datetime('now', ?)
                GROUP BY hour
                HAVING count > ?
                ORDER BY count DESC
            """, (f"-{hours} hours", threshold_per_hour))

            spikes = cursor.fetchall()
            conn.close()

            for hour, count in spikes:
                patterns.append(DetectedPattern(
                    pattern_type="error_spike",
                    description=f"Spike errori: {count} errori alle {hour}",
                    count=count,
                    severity="CRITICAL" if count > threshold_per_hour * 2 else "WARNING",
                    samples=[],
                    context={"hour": hour, "threshold": threshold_per_hour}
                ))

        except Exception:
            pass

        return patterns

    def detect_stuck_agents(self, minutes: int = 30) -> List[DetectedPattern]:
        """
        Rileva agenti che non producono log da troppo tempo.

        Args:
            minutes: Soglia inattività

        Returns:
            Pattern rilevati
        """
        patterns = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Trova agenti attivi che non loggano da troppo
            cursor.execute("""
                SELECT agent, MAX(timestamp) as last_seen
                FROM events
                WHERE agent IS NOT NULL
                GROUP BY agent
                HAVING datetime(last_seen) < datetime('now', ?)
            """, (f"-{minutes} minutes",))

            stuck = cursor.fetchall()
            conn.close()

            for agent, last_seen in stuck:
                patterns.append(DetectedPattern(
                    pattern_type="stuck_agent",
                    description=f"Agente inattivo: {agent}",
                    count=1,
                    severity="WARNING",
                    samples=[f"Last seen: {last_seen}"],
                    context={"agent": agent, "last_seen": last_seen}
                ))

        except Exception:
            pass

        return patterns

    def detect_all(self) -> List[DetectedPattern]:
        """
        Esegue tutti i detector.

        Returns:
            Tutti i pattern rilevati
        """
        all_patterns = []

        all_patterns.extend(self.detect_critical_keywords())
        all_patterns.extend(self.detect_error_spikes())
        all_patterns.extend(self.detect_stuck_agents())

        return all_patterns


# CLI Entry Point
if __name__ == "__main__":
    import sys
    from pathlib import Path

    db_path = sys.argv[1] if len(sys.argv) > 1 else str(
        Path.home() / ".swarm" / "logs" / "swarm_events.db"
    )

    detector = PatternDetector(db_path)
    patterns = detector.detect_all()

    print(f"\n{'='*60}")
    print(f"PATTERN DETECTION REPORT")
    print(f"{'='*60}\n")

    if not patterns:
        print("No patterns detected - system healthy!")
    else:
        for p in patterns:
            print(f"[{p.severity}] {p.pattern_type}")
            print(f"  {p.description}")
            print(f"  Count: {p.count}")
            if p.samples:
                print(f"  Samples: {p.samples[:2]}")
            print()
