"""Shared utilities for agent-hooks."""

from pathlib import Path


def find_project_root(cwd: str) -> Path | None:
    """Find project root by walking up to the nearest .git directory."""
    current = Path(cwd)
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return None
