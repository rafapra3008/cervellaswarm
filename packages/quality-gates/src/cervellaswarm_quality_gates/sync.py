# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Agent directory sync for AI agent swarms.

Compares and synchronizes agent definition directories:
- Find files only in source, only in target, or in both
- Detect content differences between matching files
- Generate sync actions (copy, update, delete)
"""

from __future__ import annotations

import fnmatch
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class SyncAction(Enum):
    """Action to perform for a sync item."""

    COPY = "copy"
    UPDATE = "update"
    DELETE = "delete"
    SKIP = "skip"


@dataclass(frozen=True)
class FileDiff:
    """Difference between a file in source and target."""

    name: str
    source_path: str | None
    target_path: str | None
    action: SyncAction
    reason: str


@dataclass(frozen=True)
class SyncResult:
    """Result of comparing two agent directories."""

    source_dir: str
    target_dir: str
    only_in_source: tuple[str, ...]
    only_in_target: tuple[str, ...]
    different: tuple[str, ...]
    identical: tuple[str, ...]
    diffs: tuple[FileDiff, ...] = field(default=())

    @property
    def is_synced(self) -> bool:
        """True if directories are fully in sync."""
        return not self.only_in_source and not self.only_in_target and not self.different

    @property
    def total_files(self) -> int:
        """Total unique files across both directories."""
        return (
            len(self.only_in_source)
            + len(self.only_in_target)
            + len(self.different)
            + len(self.identical)
        )


def _file_hash(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _should_ignore(name: str, patterns: list[str]) -> bool:
    """Check if a filename matches any ignore pattern."""
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def _list_files(directory: Path, ignore_patterns: list[str]) -> dict[str, Path]:
    """List files at the top level of a directory, filtered by ignore patterns.

    Non-recursive: only lists files at the top level, not in subdirectories.

    Returns:
        Dict mapping filename to absolute Path.
    """
    result: dict[str, Path] = {}
    if not directory.is_dir():
        return result

    for entry in sorted(directory.iterdir()):
        if entry.is_file() and not _should_ignore(entry.name, ignore_patterns):
            result[entry.name] = entry

    return result


def compare_agents(
    source: str | Path,
    target: str | Path,
    ignore_patterns: list[str] | None = None,
) -> SyncResult:
    """Compare two agent directories.

    Args:
        source: Path to source agent directory.
        target: Path to target agent directory.
        ignore_patterns: Glob patterns to ignore (e.g. ["*.pyc", "__pycache__"]).

    Returns:
        SyncResult with detailed comparison.
    """
    patterns = list(ignore_patterns) if ignore_patterns else ["*.pyc", "__pycache__", ".DS_Store"]
    src_path = Path(source)
    tgt_path = Path(target)

    src_files = _list_files(src_path, patterns)
    tgt_files = _list_files(tgt_path, patterns)

    src_names = set(src_files.keys())
    tgt_names = set(tgt_files.keys())

    only_source = sorted(src_names - tgt_names)
    only_target = sorted(tgt_names - src_names)
    common = sorted(src_names & tgt_names)

    different: list[str] = []
    identical: list[str] = []

    for name in common:
        src_hash = _file_hash(src_files[name])
        tgt_hash = _file_hash(tgt_files[name])
        if src_hash == tgt_hash:
            identical.append(name)
        else:
            different.append(name)

    # Build diffs
    diffs: list[FileDiff] = []
    for name in only_source:
        diffs.append(FileDiff(
            name=name,
            source_path=str(src_files[name]),
            target_path=None,
            action=SyncAction.COPY,
            reason="Only in source",
        ))
    for name in different:
        diffs.append(FileDiff(
            name=name,
            source_path=str(src_files[name]),
            target_path=str(tgt_files[name]),
            action=SyncAction.UPDATE,
            reason="Content differs",
        ))
    for name in only_target:
        diffs.append(FileDiff(
            name=name,
            source_path=None,
            target_path=str(tgt_files[name]),
            action=SyncAction.DELETE,
            reason="Only in target",
        ))

    return SyncResult(
        source_dir=str(src_path),
        target_dir=str(tgt_path),
        only_in_source=tuple(only_source),
        only_in_target=tuple(only_target),
        different=tuple(different),
        identical=tuple(identical),
        diffs=tuple(diffs),
    )
