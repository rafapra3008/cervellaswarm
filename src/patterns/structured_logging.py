"""Structured JSON Logging for CervellaSwarm.

This module provides structured logging in JSON format for better observability
and analysis of swarm operations. Each log entry is a single-line JSON object.

Usage:
    logger = SwarmLogger('backend-worker')
    logger.info("Task started", task_id="task-001", extra={"files": 3})
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-03"

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from enum import Enum


class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SwarmLogger:
    """Structured JSON logger for CervellaSwarm.

    Logs to both file (JSON Lines format) and console (human-readable).
    Each log entry includes: timestamp, level, agent, task_id, message, extra fields.

    Attributes:
        agent: Agent name (e.g., 'backend-worker', 'frontend-worker')
        task_id: Optional task ID for tracking
        log_dir: Directory for log files
    """

    def __init__(
        self,
        agent: str,
        task_id: Optional[str] = None,
        log_dir: Optional[Path] = None,
        console_output: bool = True
    ):
        """Initialize SwarmLogger.

        Args:
            agent: Agent identifier
            task_id: Optional task ID for correlation
            log_dir: Directory for log files (default: logs/)
            console_output: Whether to also log to console
        """
        self.agent = agent
        self.task_id = task_id
        self.log_dir = log_dir or Path("logs")
        self.console_output = console_output

        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Log file path: logs/swarm_YYYY-MM-DD.jsonl
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.log_dir / f"swarm_{today}.jsonl"

        # Console logger for human-readable output
        if console_output:
            self._console_logger = logging.getLogger(f"swarm.{agent}")
            if not self._console_logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter(
                    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                )
                handler.setFormatter(formatter)
                self._console_logger.addHandler(handler)
                self._console_logger.setLevel(logging.DEBUG)

    def _create_log_entry(
        self,
        level: LogLevel,
        message: str,
        **extra: Any
    ) -> Dict[str, Any]:
        """Create structured log entry.

        Args:
            level: Log level
            message: Log message
            **extra: Additional fields to include

        Returns:
            Dictionary with log entry
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "agent": self.agent,
            "message": message
        }

        if self.task_id:
            entry["task_id"] = self.task_id

        # Add extra fields
        if extra:
            entry["extra"] = extra

        return entry

    def _write_log(self, entry: Dict[str, Any]) -> None:
        """Write log entry to file.

        Args:
            entry: Log entry dictionary
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            # Fallback to stderr if file writing fails
            print(f"Failed to write log: {e}", file=sys.stderr)

    def _log(
        self,
        level: LogLevel,
        message: str,
        **extra: Any
    ) -> None:
        """Internal logging method.

        Args:
            level: Log level
            message: Log message
            **extra: Additional fields
        """
        entry = self._create_log_entry(level, message, **extra)
        self._write_log(entry)

        # Also log to console if enabled
        if self.console_output:
            log_method = getattr(
                self._console_logger,
                level.value.lower()
            )
            extra_str = f" | {extra}" if extra else ""
            log_method(f"{message}{extra_str}")

    def debug(self, message: str, **extra: Any) -> None:
        """Log DEBUG level message.

        Args:
            message: Log message
            **extra: Additional fields
        """
        self._log(LogLevel.DEBUG, message, **extra)

    def info(self, message: str, **extra: Any) -> None:
        """Log INFO level message.

        Args:
            message: Log message
            **extra: Additional fields
        """
        self._log(LogLevel.INFO, message, **extra)

    def warning(self, message: str, **extra: Any) -> None:
        """Log WARNING level message.

        Args:
            message: Log message
            **extra: Additional fields
        """
        self._log(LogLevel.WARNING, message, **extra)

    def error(self, message: str, **extra: Any) -> None:
        """Log ERROR level message.

        Args:
            message: Log message
            **extra: Additional fields
        """
        self._log(LogLevel.ERROR, message, **extra)

    def critical(self, message: str, **extra: Any) -> None:
        """Log CRITICAL level message.

        Args:
            message: Log message
            **extra: Additional fields
        """
        self._log(LogLevel.CRITICAL, message, **extra)

    def set_task_id(self, task_id: str) -> None:
        """Update task ID for all subsequent logs.

        Args:
            task_id: New task ID
        """
        self.task_id = task_id


def read_logs(
    log_file: Path,
    agent: Optional[str] = None,
    level: Optional[LogLevel] = None,
    task_id: Optional[str] = None
) -> list[Dict[str, Any]]:
    """Read and filter logs from JSONL file.

    Args:
        log_file: Path to log file
        agent: Filter by agent name
        level: Filter by log level
        task_id: Filter by task ID

    Returns:
        List of matching log entries

    Example:
        >>> logs = read_logs(
        ...     Path("logs/swarm_2026-01-03.jsonl"),
        ...     agent="backend-worker",
        ...     level=LogLevel.ERROR
        ... )
    """
    if not log_file.exists():
        return []

    matching_logs = []

    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())

                # Apply filters
                if agent and entry.get("agent") != agent:
                    continue
                if level and entry.get("level") != level.value:
                    continue
                if task_id and entry.get("task_id") != task_id:
                    continue

                matching_logs.append(entry)

            except json.JSONDecodeError:
                # Skip malformed lines
                continue

    return matching_logs


if __name__ == "__main__":
    # Simple test
    logger = SwarmLogger("test-agent", task_id="task-001")

    logger.debug("Starting test")
    logger.info("Task started", files=3, priority="high")
    logger.warning("Potential issue detected", retry_count=2)
    logger.error("Operation failed", error_code="E001", details="Connection timeout")

    # Change task
    logger.set_task_id("task-002")
    logger.info("Processing new task", items=10)

    print("\n--- Reading logs ---")
    log_file = Path("logs") / f"swarm_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    logs = read_logs(log_file, agent="test-agent")

    for entry in logs:
        print(json.dumps(entry, indent=2))
