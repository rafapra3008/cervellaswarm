# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Task Manager - File-based task state management for multi-agent systems.

Uses marker files (.ready, .working, .done) for synchronization between agents.
Git-friendly: all state is plain files, creating a natural audit trail.
Atomic operations prevent race conditions when multiple workers compete.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
import logging
import os
import re

logger = logging.getLogger(__name__)

DEFAULT_TASKS_DIR = ".swarm/tasks"


def validate_task_id(task_id: str) -> bool:
    """
    Validate task_id for safety and path traversal prevention.

    Checks that task_id:
    - Contains only alphanumeric characters, underscores, and dashes
    - Does not exceed 50 characters
    - Does not contain dangerous sequences (.., /, \\\\)

    Args:
        task_id: Task ID to validate.

    Returns:
        True if task_id is valid.

    Examples:
        >>> validate_task_id("TASK_001")
        True
        >>> validate_task_id("../../etc/passwd")
        False
    """
    if not task_id or len(task_id) > 50:
        return False

    dangerous_patterns = ["..", "/", "\\"]
    if any(pattern in task_id for pattern in dangerous_patterns):
        return False

    if not re.match(r"^[a-zA-Z0-9_-]+$", task_id):
        return False

    return True


def ensure_tasks_dir(tasks_dir: Optional[str] = None) -> Path:
    """
    Ensure the tasks directory exists.

    Args:
        tasks_dir: Custom tasks directory (default: .swarm/tasks).

    Returns:
        Path to the tasks directory.

    Raises:
        PermissionError: If permissions are insufficient.
        OSError: If creation fails.
    """
    tasks_path = Path(tasks_dir or DEFAULT_TASKS_DIR)
    try:
        tasks_path.mkdir(parents=True, exist_ok=True)
        return tasks_path
    except PermissionError:
        logger.error("Insufficient permissions to create %s", tasks_path)
        raise
    except OSError as e:
        logger.error("Error creating directory %s: %s", tasks_path, e)
        raise


def create_task(
    task_id: str,
    agent: str,
    description: str,
    risk_level: int = 1,
    tasks_dir: Optional[str] = None,
) -> str:
    """
    Create a new task with a structured template.

    Args:
        task_id: Unique task ID (e.g., TASK_001).
        agent: Assigned agent name (e.g., backend-worker).
        description: Task description.
        risk_level: Risk level 1-3 (1=low, 2=medium, 3=high).
        tasks_dir: Custom tasks directory.

    Returns:
        Path of the created task file.

    Raises:
        ValueError: If task_id is invalid.
        FileExistsError: If task already exists.
    """
    if not validate_task_id(task_id):
        raise ValueError(
            f"Invalid task ID: {task_id}. Use only alphanumeric, underscore, dash (max 50 chars)."
        )

    tasks_path = ensure_tasks_dir(tasks_dir)
    task_file = tasks_path / f"{task_id}.md"

    if task_file.exists():
        raise FileExistsError(f"Task {task_id} already exists!")

    risk_map = {
        1: "LOW - new file, no risk",
        2: "MEDIUM - modifying existing file",
        3: "HIGH - critical system or deploy",
    }

    template = f"""# TASK: {description}

## METADATA
- ID: {task_id}
- Assigned to: {agent}
- Risk level: {risk_level} ({risk_map.get(risk_level, "UNDEFINED")})
- Timeout: 15 minutes
- Created: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## SUCCESS CRITERIA
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests passing

## FILES TO MODIFY
- [files to create/modify]

## REVIEWER
Quality gate (Level {risk_level} - {'functional check' if risk_level == 1 else 'full tests' if risk_level == 2 else 'complete audit'})

## DETAILS

[Detailed task description]
"""

    task_file.write_text(template)
    return str(task_file)


def list_tasks(tasks_dir: Optional[str] = None) -> list[dict]:
    """
    List all tasks with their status.

    Args:
        tasks_dir: Custom tasks directory.

    Returns:
        List of dicts with: task_id, status, ack, agent, file.
    """
    tasks_path = ensure_tasks_dir(tasks_dir)
    tasks: list[dict] = []

    for task_file in sorted(tasks_path.glob("TASK_*.md")):
        task_id = task_file.stem
        status = get_task_status(task_id, tasks_dir)
        ack = get_ack_status(task_id, tasks_dir)

        agent = "unknown"
        try:
            content = task_file.read_text()
            for line in content.split("\n"):
                if line.startswith("- Assigned to:"):
                    agent = line.split(":", 1)[1].strip()
                    break
        except (PermissionError, UnicodeDecodeError, OSError) as e:
            logger.warning("Error reading %s: %s", task_file, e)

        tasks.append(
            {
                "task_id": task_id,
                "status": status,
                "ack": ack,
                "agent": agent,
                "file": str(task_file),
            }
        )

    return tasks


def mark_ready(task_id: str, tasks_dir: Optional[str] = None) -> bool:
    """
    Mark a task as ready (available for workers).

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        True if successful.
    """
    if not validate_task_id(task_id):
        logger.error("Invalid task ID: %s", task_id)
        return False

    tasks_path = ensure_tasks_dir(tasks_dir)
    if not (tasks_path / f"{task_id}.md").exists():
        logger.error("Task %s does not exist!", task_id)
        return False

    (tasks_path / f"{task_id}.ready").touch()
    return True


def mark_working(task_id: str, tasks_dir: Optional[str] = None) -> bool:
    """
    Mark a task as working (in progress).

    ATOMIC: Uses exclusive create to prevent race conditions.
    If two workers try to claim the same task, only one succeeds.

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        True if this worker got the task, False if already claimed.
    """
    if not validate_task_id(task_id):
        logger.error("Invalid task ID: %s", task_id)
        return False

    tasks_path = ensure_tasks_dir(tasks_dir)
    if not (tasks_path / f"{task_id}.md").exists():
        logger.error("Task %s does not exist!", task_id)
        return False

    working_file = tasks_path / f"{task_id}.working"

    # ATOMIC: 'x' mode = exclusive create, fails if file already exists
    try:
        with open(working_file, "x") as f:
            f.write(f"started: {datetime.now().isoformat()}\n")
        return True
    except FileExistsError:
        logger.warning("Task %s already claimed by another worker!", task_id)
        return False


def ack_received(task_id: str, tasks_dir: Optional[str] = None) -> bool:
    """
    Mark a task as ACK_RECEIVED (worker received the task).

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        True if successful.
    """
    if not validate_task_id(task_id):
        logger.error("Invalid task ID: %s", task_id)
        return False

    tasks_path = ensure_tasks_dir(tasks_dir)
    if not (tasks_path / f"{task_id}.md").exists():
        logger.error("Task %s does not exist!", task_id)
        return False

    (tasks_path / f"{task_id}.ack_received").touch()
    return True


def ack_understood(task_id: str, tasks_dir: Optional[str] = None) -> bool:
    """
    Mark a task as ACK_UNDERSTOOD (worker understood the task).

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        True if successful.
    """
    if not validate_task_id(task_id):
        logger.error("Invalid task ID: %s", task_id)
        return False

    tasks_path = ensure_tasks_dir(tasks_dir)
    if not (tasks_path / f"{task_id}.md").exists():
        logger.error("Task %s does not exist!", task_id)
        return False

    (tasks_path / f"{task_id}.ack_understood").touch()
    return True


def mark_done(task_id: str, tasks_dir: Optional[str] = None) -> bool:
    """
    Mark a task as done (completed).

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        True if successful.
    """
    if not validate_task_id(task_id):
        logger.error("Invalid task ID: %s", task_id)
        return False

    tasks_path = ensure_tasks_dir(tasks_dir)
    if not (tasks_path / f"{task_id}.md").exists():
        logger.error("Task %s does not exist!", task_id)
        return False

    (tasks_path / f"{task_id}.done").touch()
    return True


def get_task_status(task_id: str, tasks_dir: Optional[str] = None) -> str:
    """
    Get the status of a task.

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        Status string: 'done', 'working', 'ready', 'created', 'not_found', 'invalid'.
    """
    if not validate_task_id(task_id):
        return "invalid"

    tasks_path = Path(tasks_dir or DEFAULT_TASKS_DIR)

    if not (tasks_path / f"{task_id}.md").exists():
        return "not_found"

    if (tasks_path / f"{task_id}.done").exists():
        return "done"
    if (tasks_path / f"{task_id}.working").exists():
        return "working"
    if (tasks_path / f"{task_id}.ready").exists():
        return "ready"

    return "created"


def get_ack_status(task_id: str, tasks_dir: Optional[str] = None) -> str:
    """
    Get the ACK status of a task (R/U/D format).

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        String with format "R/U/D" where each is a checkmark or dash.
    """
    if not validate_task_id(task_id):
        return "---"

    tasks_path = Path(tasks_dir or DEFAULT_TASKS_DIR)

    r = "Y" if (tasks_path / f"{task_id}.ack_received").exists() else "-"
    u = "Y" if (tasks_path / f"{task_id}.ack_understood").exists() else "-"
    d = "Y" if (tasks_path / f"{task_id}.done").exists() else "-"

    return f"{r}/{u}/{d}"


def cleanup_task(task_id: str, tasks_dir: Optional[str] = None) -> bool:
    """
    Remove marker files for a task.

    Args:
        task_id: Task ID.
        tasks_dir: Custom tasks directory.

    Returns:
        True if successful.
    """
    if not validate_task_id(task_id):
        logger.error("Invalid task ID: %s", task_id)
        return False

    tasks_path = Path(tasks_dir or DEFAULT_TASKS_DIR)

    markers = [".ready", ".working", ".done", ".ack_received", ".ack_understood"]
    for marker in markers:
        marker_file = tasks_path / f"{task_id}{marker}"
        if marker_file.exists():
            marker_file.unlink()

    return True
