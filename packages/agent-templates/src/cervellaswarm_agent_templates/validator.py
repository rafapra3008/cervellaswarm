# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Validate agent definition files (Markdown with YAML frontmatter)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {"name", "description", "model", "tools"}

VALID_MODELS = {"opus", "sonnet", "haiku"}

VALID_TOOLS = {
    "Read",
    "Edit",
    "Bash",
    "Glob",
    "Grep",
    "Write",
    "WebSearch",
    "WebFetch",
    "Task",
    "AskUserQuestion",
    "NotebookEdit",
    "EnterPlanMode",
    "ExitPlanMode",
}

VALID_ROLES = {
    "Coordinator",
    "Quality Gate",
    "Architect",
    "Worker",
    "Researcher",
    "Reviewer",
}

VALID_PERMISSION_MODES = {"default", "plan", "bypassPermissions", "acceptEdits"}

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ValidationIssue:
    """A single validation issue."""

    level: str  # "error" | "warning" | "info"
    field: str
    message: str


@dataclass
class ValidationResult:
    """Result of validating an agent file."""

    path: str
    valid: bool
    frontmatter: dict[str, Any] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == "warning"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Extract YAML frontmatter from markdown content.

    Returns the parsed dict or None if no frontmatter found.
    """
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def validate_agent(path: str | Path) -> ValidationResult:
    """Validate an agent definition file.

    Checks:
    - File exists and is readable
    - Has valid YAML frontmatter
    - Required fields present (name, description, model, tools)
    - Model is valid (opus/sonnet/haiku)
    - Tools are recognized
    - Optional fields have valid values
    """
    path = Path(path)
    issues: list[ValidationIssue] = []

    # File existence
    if not path.exists():
        return ValidationResult(
            path=str(path),
            valid=False,
            issues=[ValidationIssue("error", "file", f"File not found: {path}")],
        )

    if not path.suffix == ".md":
        issues.append(
            ValidationIssue("warning", "file", "Agent files should use .md extension")
        )

    # Read and parse
    content = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)

    if frontmatter is None:
        return ValidationResult(
            path=str(path),
            valid=False,
            issues=[
                ValidationIssue(
                    "error", "frontmatter", "No valid YAML frontmatter found"
                )
            ],
        )

    # Required fields
    for req in REQUIRED_FIELDS:
        if req not in frontmatter:
            issues.append(
                ValidationIssue("error", req, f"Required field '{req}' is missing")
            )

    # Model validation
    model = frontmatter.get("model")
    if model and model not in VALID_MODELS:
        issues.append(
            ValidationIssue(
                "error",
                "model",
                f"Invalid model '{model}'. Valid: {', '.join(sorted(VALID_MODELS))}",
            )
        )

    # Tools validation
    tools_str = frontmatter.get("tools", "")
    if isinstance(tools_str, str) and tools_str:
        tools = [t.strip() for t in tools_str.split(",")]
        for tool in tools:
            if tool and tool not in VALID_TOOLS:
                issues.append(
                    ValidationIssue(
                        "warning", "tools", f"Unrecognized tool '{tool}'"
                    )
                )

    # Optional field validation
    role = frontmatter.get("role")
    if role and role not in VALID_ROLES:
        issues.append(
            ValidationIssue(
                "info",
                "role",
                f"Custom role '{role}'. Standard roles: {', '.join(sorted(VALID_ROLES))}",
            )
        )

    permission_mode = frontmatter.get("permissionMode")
    if permission_mode and permission_mode not in VALID_PERMISSION_MODES:
        issues.append(
            ValidationIssue(
                "warning",
                "permissionMode",
                f"Invalid permissionMode '{permission_mode}'. "
                f"Valid: {', '.join(sorted(VALID_PERMISSION_MODES))}",
            )
        )

    max_turns = frontmatter.get("maxTurns")
    if max_turns is not None:
        if not isinstance(max_turns, int) or max_turns < 1:
            issues.append(
                ValidationIssue(
                    "warning", "maxTurns", "maxTurns should be a positive integer"
                )
            )

    version = frontmatter.get("version")
    if version and not re.match(r"^\d+\.\d+\.\d+$", str(version)):
        issues.append(
            ValidationIssue(
                "warning", "version", f"Version '{version}' is not valid semver"
            )
        )

    # Body content check
    body_start = FRONTMATTER_PATTERN.match(content)
    if body_start:
        body = content[body_start.end() :].strip()
        if len(body) < 50:
            issues.append(
                ValidationIssue(
                    "warning",
                    "body",
                    "Agent body is very short. Add role description and instructions.",
                )
            )

    has_errors = any(i.level == "error" for i in issues)

    return ValidationResult(
        path=str(path),
        valid=not has_errors,
        frontmatter=frontmatter,
        issues=issues,
    )
