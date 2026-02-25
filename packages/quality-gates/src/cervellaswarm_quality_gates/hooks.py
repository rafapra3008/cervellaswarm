# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Hook validation for AI agent swarms.

Validates hook file integrity:
- File existence
- Execute permission
- Shebang line correctness
- File is not empty

Hook statuses:
- OK: Hook exists, is executable, has valid shebang
- BROKEN: Hook exists but has errors (bad shebang, empty)
- DISABLED: Hook file name starts with _ or .disabled suffix
- NOT_EXEC: Hook exists but lacks execute permission
- MISSING: Hook file not found
"""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class HookStatus(Enum):
    """Status of a hook file."""

    OK = "OK"
    BROKEN = "BROKEN"
    DISABLED = "DISABLED"
    NOT_EXEC = "NOT_EXEC"
    MISSING = "MISSING"


_VALID_SHEBANGS: tuple[str, ...] = (
    "#!/usr/bin/env python3",
    "#!/usr/bin/env python",
    "#!/usr/bin/env bash",
    "#!/usr/bin/env sh",
    "#!/usr/bin/env node",
    "#!/bin/bash",
    "#!/bin/sh",
    "#!/usr/bin/python3",
    "#!/usr/bin/python",
)


@dataclass(frozen=True)
class HookReport:
    """Validation report for a single hook file."""

    name: str
    path: str
    status: HookStatus
    issues: tuple[str, ...] = field(default=())

    @property
    def is_healthy(self) -> bool:
        """True if hook status is OK."""
        return self.status == HookStatus.OK


def _check_disabled(path: Path) -> bool:
    """Check if a hook is intentionally disabled.

    Files starting with single underscore are disabled.
    Dunder files (__init__.py, __main__.py) are NOT considered disabled.
    Files ending with .disabled suffix are disabled.
    """
    name = path.name
    if name.startswith("__"):
        return False
    return name.startswith("_") or name.endswith(".disabled")


def _check_shebang(path: Path) -> tuple[bool, str]:
    """Check if file has a valid shebang line.

    Returns:
        (is_valid, message) tuple.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
    except (OSError, UnicodeDecodeError):
        return False, "Cannot read file"

    if not first_line:
        return False, "File is empty"

    if not first_line.startswith("#!"):
        return False, f"No shebang found (first line: {first_line[:40]})"

    for valid in _VALID_SHEBANGS:
        if first_line.startswith(valid):
            return True, ""

    return False, f"Unknown shebang: {first_line[:60]}"


def validate_hook(path: str | Path) -> HookReport:
    """Validate a single hook file.

    Args:
        path: Path to the hook file.

    Returns:
        HookReport with status and any issues found.
    """
    p = Path(path)
    name = p.name

    if not p.exists():
        return HookReport(name=name, path=str(p), status=HookStatus.MISSING)

    if _check_disabled(p):
        return HookReport(name=name, path=str(p), status=HookStatus.DISABLED)

    issues: list[str] = []

    # Check execute permission
    file_stat = p.stat()
    is_executable = bool(file_stat.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

    if not is_executable:
        return HookReport(
            name=name,
            path=str(p),
            status=HookStatus.NOT_EXEC,
            issues=("Missing execute permission",),
        )

    # Check file is not empty
    if file_stat.st_size == 0:
        issues.append("File is empty")
        return HookReport(
            name=name,
            path=str(p),
            status=HookStatus.BROKEN,
            issues=tuple(issues),
        )

    # Check shebang
    shebang_ok, shebang_msg = _check_shebang(p)
    if not shebang_ok:
        issues.append(shebang_msg)
        return HookReport(
            name=name,
            path=str(p),
            status=HookStatus.BROKEN,
            issues=tuple(issues),
        )

    return HookReport(name=name, path=str(p), status=HookStatus.OK)


def validate_hooks(
    directory: str | Path,
    required_hooks: list[str] | None = None,
) -> list[HookReport]:
    """Validate all hook files in a directory.

    Args:
        directory: Path to the hooks directory.
        required_hooks: Optional list of hook names that must exist.

    Returns:
        List of HookReport for each hook found (+ missing required hooks).
    """
    dir_path = Path(directory)
    reports: list[HookReport] = []

    if not dir_path.is_dir():
        if required_hooks:
            for hook_name in required_hooks:
                reports.append(HookReport(
                    name=hook_name,
                    path=str(dir_path / hook_name),
                    status=HookStatus.MISSING,
                ))
        return reports

    # Validate existing files
    seen_names: set[str] = set()
    for entry in sorted(dir_path.iterdir()):
        if entry.is_file():
            report = validate_hook(entry)
            reports.append(report)
            seen_names.add(entry.name)

    # Check for required hooks that are missing
    if required_hooks:
        for hook_name in required_hooks:
            if hook_name not in seen_names:
                reports.append(HookReport(
                    name=hook_name,
                    path=str(dir_path / hook_name),
                    status=HookStatus.MISSING,
                ))

    return reports


def hooks_summary(reports: list[HookReport]) -> dict[str, int]:
    """Summarize hook validation results.

    Args:
        reports: List of HookReport from validate_hooks.

    Returns:
        Dict with counts per status (e.g. {"OK": 3, "BROKEN": 1}).
    """
    summary: dict[str, int] = {}
    for report in reports:
        key = report.status.value
        summary[key] = summary.get(key, 0) + 1
    return summary
