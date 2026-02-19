# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Secret detection for session memory files.

Scans Markdown and text files for accidentally committed secrets
like API keys, tokens, passwords, and private keys.
"""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from cervellaswarm_session_memory.config import load_config

logger = logging.getLogger(__name__)


class Severity(Enum):
    """Severity level for detected secrets."""

    CRITICAL = "critical"
    HIGH = "high"


@dataclass
class Finding:
    """A detected secret or sensitive pattern."""

    severity: Severity
    pattern_name: str
    file: str
    line_number: int


@dataclass
class AuditResult:
    """Result of a secret audit."""

    scanned_files: int
    critical_count: int
    high_count: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        """Whether the audit found no issues."""
        return self.critical_count == 0 and self.high_count == 0


# Built-in detection patterns
CRITICAL_PATTERNS: list[tuple[str, str]] = [
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI/Anthropic API Key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"AIza[a-zA-Z0-9_-]{35}", "Google API Key"),
    (r"sk_live_[a-zA-Z0-9]{24}", "Stripe Secret Key"),
    (r"-----BEGIN.*PRIVATE KEY-----", "Private Key"),
    (r"AKIA[A-Z0-9]{16}", "AWS Access Key ID"),
]

HIGH_PATTERNS: list[tuple[str, str]] = [
    (r"[Pp]ass(?:word)?\s*[:=]\s*[^\s\[\]\"]{8,40}", "Password Assignment"),
    (r"[Ss]ecret\s*[:=]\s*[^\s\[\]\"]{8,40}", "Secret Assignment"),
    (r"[Tt]oken\s*[:=]\s*[^\s\[\]\"]{8,40}", "Token Assignment"),
]

# File patterns to skip during scanning
SKIP_PATTERNS = [
    "*audit-secrets*",
    "*AUDIT_*",
    "*.env.example*",
    "*test*",
    "*mock*",
    "*fixture*",
]

# Content patterns that indicate a sanitized/placeholder value
SANITIZED_MARKERS = [
    "[stored in .env",
    "[REDACTED",
    "YOUR_",
    "your_",
    "example",
    "placeholder",
    "xxx",
    "***",
]


def should_skip_file(file_path: Path) -> bool:
    """Check if a file should be skipped during audit.

    Args:
        file_path: Path to check.

    Returns:
        True if the file should be skipped.
    """
    name = file_path.name.lower()
    path_str = str(file_path).lower()

    for pattern in SKIP_PATTERNS:
        clean = pattern.strip("*")
        if clean in name or clean in path_str:
            return True

    return False


def is_sanitized(line: str) -> bool:
    """Check if a line contains a sanitized/placeholder value.

    Args:
        line: Line content to check.

    Returns:
        True if the value appears to be a placeholder.
    """
    lower = line.lower()
    return any(marker.lower() in lower for marker in SANITIZED_MARKERS)


def audit_file(
    file_path: Path,
    extra_patterns: list[tuple[str, str]] | None = None,
) -> AuditResult:
    """Audit a single file for secrets.

    Args:
        file_path: Path to file to scan.
        extra_patterns: Additional (pattern, name) tuples to scan for.

    Returns:
        AuditResult with findings.
    """
    if not file_path.exists():
        return AuditResult(scanned_files=0, critical_count=0, high_count=0)

    if should_skip_file(file_path):
        return AuditResult(scanned_files=1, critical_count=0, high_count=0)

    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return AuditResult(scanned_files=1, critical_count=0, high_count=0)

    findings = []
    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        if is_sanitized(line):
            continue

        for pattern, name in CRITICAL_PATTERNS:
            if re.search(pattern, line):
                findings.append(
                    Finding(
                        severity=Severity.CRITICAL,
                        pattern_name=name,
                        file=str(file_path),
                        line_number=line_num,
                    )
                )

        for pattern, name in HIGH_PATTERNS:
            if re.search(pattern, line):
                findings.append(
                    Finding(
                        severity=Severity.HIGH,
                        pattern_name=name,
                        file=str(file_path),
                        line_number=line_num,
                    )
                )

        if extra_patterns:
            for pattern, name in extra_patterns:
                if re.search(pattern, line):
                    findings.append(
                        Finding(
                            severity=Severity.HIGH,
                            pattern_name=name,
                            file=str(file_path),
                            line_number=line_num,
                        )
                    )

    critical = sum(1 for f in findings if f.severity == Severity.CRITICAL)
    high = sum(1 for f in findings if f.severity == Severity.HIGH)

    return AuditResult(
        scanned_files=1,
        critical_count=critical,
        high_count=high,
        findings=findings,
    )


def audit_directory(
    directory: Path,
    extra_patterns: list[tuple[str, str]] | None = None,
    skip_files: list[str] | None = None,
    extensions: set[str] | None = None,
) -> AuditResult:
    """Audit an entire directory tree for secrets.

    Args:
        directory: Directory to scan recursively.
        extra_patterns: Additional (pattern, name) tuples.
        skip_files: Additional file patterns to skip.
        extensions: File extensions to scan. Defaults to common text files.

    Returns:
        AuditResult with aggregated findings.
    """
    if not directory.exists():
        return AuditResult(scanned_files=0, critical_count=0, high_count=0)

    if extensions is None:
        extensions = {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".env"}

    config = load_config()
    config_skip = config.get("secrets", {}).get("skip_files", [])
    all_skip = (skip_files or []) + config_skip

    config_extra = config.get("secrets", {}).get("extra_patterns", [])
    all_extra = list(extra_patterns or [])
    for ep in config_extra:
        if isinstance(ep, dict) and "pattern" in ep and "name" in ep:
            try:
                re.compile(ep["pattern"])
                all_extra.append((ep["pattern"], ep["name"]))
            except re.error as exc:
                logger.warning(
                    "Skipping invalid regex in extra_patterns: %r (%s)",
                    ep["pattern"], exc,
                )

    total_files = 0
    total_critical = 0
    total_high = 0
    all_findings: list[Finding] = []

    for file_path in sorted(directory.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix not in extensions:
            continue

        # Check additional skip patterns
        skip = False
        for sp in all_skip:
            if sp in str(file_path):
                skip = True
                break
        if skip:
            continue

        result = audit_file(file_path, all_extra if all_extra else None)
        total_files += result.scanned_files
        total_critical += result.critical_count
        total_high += result.high_count
        all_findings.extend(result.findings)

    return AuditResult(
        scanned_files=total_files,
        critical_count=total_critical,
        high_count=total_high,
        findings=all_findings,
    )
