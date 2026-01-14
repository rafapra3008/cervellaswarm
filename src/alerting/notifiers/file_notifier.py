"""
File Notifier - Scrive alert su file log
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..alert_system import Alert


class FileNotifier:
    """Notifier che scrive alert su file JSON Lines"""

    def __init__(self, file_path: Union[str, Path]):
        """
        Inizializza file notifier.

        Args:
            file_path: Path del file di log
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def send(self, alert: "Alert") -> bool:
        """
        Scrive alert su file.

        Args:
            alert: Alert da scrivere

        Returns:
            True se scritto con successo
        """
        try:
            record = {
                "id": alert.id,
                "severity": alert.severity.name,
                "title": alert.title,
                "message": alert.message,
                "source": alert.source,
                "timestamp": alert.timestamp.isoformat(),
                "context": alert.context,
                "dedupe_key": alert.dedupe_key,
                "logged_at": datetime.now().isoformat(),
            }

            with open(self.file_path, "a") as f:
                f.write(json.dumps(record) + "\n")

            return True

        except Exception as e:
            print(f"[FILE NOTIFIER ERROR] {e}")
            return False
