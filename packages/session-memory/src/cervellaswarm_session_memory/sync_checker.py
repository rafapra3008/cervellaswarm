# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Sync checker for session memory freshness and coherence.

Verifies that session state files are up-to-date, within size limits,
and consistent with the project's git state.
"""

import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

from cervellaswarm_session_memory.config import DEFAULTS, load_config


class CheckStatus(Enum):
    """Status of a sync check."""

    OK = "ok"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class SyncResult:
    """Result of sync checks for one project."""

    project: str
    checks: dict[str, CheckStatus] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def overall(self) -> CheckStatus:
        """Overall status based on individual checks."""
        statuses = list(self.checks.values())
        if any(s == CheckStatus.ERROR for s in statuses):
            return CheckStatus.ERROR
        if any(s == CheckStatus.WARNING for s in statuses):
            return CheckStatus.WARNING
        return CheckStatus.OK


def check_state_freshness(
    state_file: Path,
    max_days: int = 7,
    warn_days: int = 3,
) -> tuple[CheckStatus, str]:
    """Check if the session state file is fresh enough.

    Args:
        state_file: Path to the state file.
        max_days: Days after which status is ERROR.
        warn_days: Days after which status is WARNING.

    Returns:
        Tuple of (status, description message).
    """
    if not state_file.exists():
        return CheckStatus.ERROR, f"State file not found: {state_file}"

    mtime = datetime.fromtimestamp(state_file.stat().st_mtime)
    days_old = (datetime.now() - mtime).days

    if days_old <= warn_days:
        return CheckStatus.OK, f"Updated {days_old} day(s) ago"
    elif days_old <= max_days:
        return CheckStatus.WARNING, f"Updated {days_old} days ago (consider refreshing)"
    else:
        return CheckStatus.ERROR, f"Stale: {days_old} days since last update"


def check_file_size(
    file_path: Path,
    max_lines: int = 300,
    warning_lines: int = 200,
) -> tuple[CheckStatus, str]:
    """Check if a file is within size limits.

    Args:
        file_path: Path to the file.
        max_lines: Maximum allowed lines.
        warning_lines: Warning threshold.

    Returns:
        Tuple of (status, description message).
    """
    if not file_path.exists():
        return CheckStatus.ERROR, f"File not found: {file_path}"

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return CheckStatus.ERROR, f"Cannot read file: {e}"

    line_count = len(content.split("\n"))

    if line_count < warning_lines:
        return CheckStatus.OK, f"{line_count} lines (limit: {max_lines})"
    elif line_count < max_lines:
        return CheckStatus.WARNING, f"{line_count} lines (approaching limit: {max_lines})"
    else:
        return CheckStatus.ERROR, f"{line_count} lines (OVER limit: {max_lines})"


def check_git_uncommitted(
    project_path: Path,
) -> tuple[CheckStatus, str]:
    """Check if there are uncommitted changes in the project.

    Args:
        project_path: Path to the project directory.

    Returns:
        Tuple of (status, description message).
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        return CheckStatus.WARNING, "git not available"
    except subprocess.TimeoutExpired:
        return CheckStatus.WARNING, "git status timed out"

    if result.returncode != 0:
        return CheckStatus.WARNING, "Not a git repository"

    changes = result.stdout.strip()
    if not changes:
        return CheckStatus.OK, "Working tree clean"

    change_count = len(changes.split("\n"))
    return CheckStatus.WARNING, f"{change_count} uncommitted change(s)"


def check_state_in_git(
    state_file: Path,
    project_path: Path,
) -> tuple[CheckStatus, str]:
    """Check if the session state file is tracked in git.

    Args:
        state_file: Path to the state file.
        project_path: Path to the project root.

    Returns:
        Tuple of (status, description message).
    """
    if not state_file.exists():
        return CheckStatus.ERROR, "State file does not exist"

    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(state_file)],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return CheckStatus.WARNING, "Cannot check git tracking"

    if result.returncode == 0:
        return CheckStatus.OK, "State file is tracked in git"
    else:
        return CheckStatus.WARNING, "State file is NOT tracked in git"


def verify_project(
    project_name: str,
    base_dir: Path | None = None,
    config: dict | None = None,
) -> SyncResult:
    """Run all sync checks on a project.

    Args:
        project_name: Name of the project.
        base_dir: Base directory. Defaults to CWD.
        config: Pre-loaded config.

    Returns:
        SyncResult with all check results.
    """
    from cervellaswarm_session_memory.project_manager import get_project

    if config is None:
        config = load_config()

    result = SyncResult(project=project_name)

    project = get_project(project_name, base_dir, config)
    if project is None:
        result.checks["exists"] = CheckStatus.ERROR
        result.errors.append(f"Project '{project_name}' not found")
        return result

    result.checks["exists"] = CheckStatus.OK

    # Check freshness
    max_lines = config.get("max_lines", DEFAULTS["max_lines"])
    warning_lines = config.get("warning_lines", DEFAULTS["warning_lines"])

    status, msg = check_state_freshness(project.state_file)
    result.checks["freshness"] = status
    if status != CheckStatus.OK:
        (result.warnings if status == CheckStatus.WARNING else result.errors).append(
            f"Freshness: {msg}"
        )

    # Check file size
    status, msg = check_file_size(project.state_file, max_lines, warning_lines)
    result.checks["size"] = status
    if status != CheckStatus.OK:
        (result.warnings if status == CheckStatus.WARNING else result.errors).append(
            f"Size: {msg}"
        )

    # Check git state (use project root from memory_dir parent)
    project_root = base_dir if base_dir else Path.cwd()

    status, msg = check_git_uncommitted(project_root)
    result.checks["git_clean"] = status
    if status != CheckStatus.OK:
        result.warnings.append(f"Git: {msg}")

    status, msg = check_state_in_git(project.state_file, project_root)
    result.checks["git_tracked"] = status
    if status != CheckStatus.OK:
        result.warnings.append(f"Tracking: {msg}")

    return result


def verify_all(
    base_dir: Path | None = None,
    config: dict | None = None,
) -> list[SyncResult]:
    """Run sync checks on all discovered projects.

    Args:
        base_dir: Base directory. Defaults to CWD.
        config: Pre-loaded config.

    Returns:
        List of SyncResult objects.
    """
    from cervellaswarm_session_memory.project_manager import discover_projects

    if config is None:
        config = load_config()

    projects = discover_projects(base_dir, config)
    return [verify_project(p.name, base_dir, config) for p in projects]
