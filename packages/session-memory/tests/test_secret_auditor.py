# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_session_memory.secret_auditor."""

from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_session_memory.secret_auditor import (
    AuditResult,
    Finding,
    Severity,
    audit_directory,
    audit_file,
    is_sanitized,
    should_skip_file,
)


# ---------------------------------------------------------------------------
# Severity enum
# ---------------------------------------------------------------------------


def test_severity_values():
    """CRITICAL and HIGH have the expected string values."""
    assert Severity.CRITICAL.value == "critical"
    assert Severity.HIGH.value == "high"


# ---------------------------------------------------------------------------
# AuditResult.clean property
# ---------------------------------------------------------------------------


def test_audit_result_clean():
    """clean is True when both counts are zero."""
    result = AuditResult(scanned_files=1, critical_count=0, high_count=0)
    assert result.clean is True


def test_audit_result_not_clean():
    """clean is False when there are findings."""
    result = AuditResult(scanned_files=1, critical_count=1, high_count=0)
    assert result.clean is False

    result2 = AuditResult(scanned_files=1, critical_count=0, high_count=2)
    assert result2.clean is False


# ---------------------------------------------------------------------------
# should_skip_file
# ---------------------------------------------------------------------------


def test_should_skip_test_file():
    """Files with 'test' in the name are skipped."""
    assert should_skip_file(Path("my_test_file.md")) is True


def test_should_skip_mock_file():
    """Files with 'mock' in the name are skipped."""
    assert should_skip_file(Path("mock_secrets.yaml")) is True


def test_should_skip_audit_file():
    """Files matching 'audit-secrets' in the name are skipped."""
    assert should_skip_file(Path("audit-secrets-report.md")) is True


def test_should_skip_normal_file():
    """Regular files are not skipped."""
    assert should_skip_file(Path("SESSION_STATE_myproject.md")) is False


# ---------------------------------------------------------------------------
# is_sanitized
# ---------------------------------------------------------------------------


def test_is_sanitized_env_reference():
    """Lines with '[stored in .env' are considered sanitized."""
    assert is_sanitized("api_key=[stored in .env as OPENAI_KEY]") is True


def test_is_sanitized_redacted():
    """Lines with '[REDACTED' are considered sanitized."""
    assert is_sanitized("password=[REDACTED]") is True


def test_is_sanitized_placeholder():
    """Lines with 'YOUR_' are considered sanitized."""
    assert is_sanitized("token=YOUR_KEY_HERE") is True


def test_is_sanitized_real_secret():
    """A real-looking secret is not considered sanitized."""
    assert is_sanitized("sk-abcdefghijklmnopqrstuvwxyz12345") is False


# ---------------------------------------------------------------------------
# audit_file - CRITICAL patterns
# ---------------------------------------------------------------------------


def test_audit_file_openai_key(tmp_path):
    """OpenAI/Anthropic sk- keys trigger CRITICAL finding."""
    f = tmp_path / "state.md"
    f.write_text("api_key=sk-abcdefghijklmnopqrstu\n", encoding="utf-8")
    result = audit_file(f)
    assert result.critical_count >= 1
    assert any("OpenAI" in x.pattern_name or "Anthropic" in x.pattern_name for x in result.findings)


def test_audit_file_github_token(tmp_path):
    """GitHub Personal Access Tokens (ghp_...) trigger CRITICAL finding."""
    f = tmp_path / "state.md"
    f.write_text("token=ghp_" + "a" * 36 + "\n", encoding="utf-8")
    result = audit_file(f)
    assert result.critical_count >= 1
    assert any("GitHub" in x.pattern_name for x in result.findings)


def test_audit_file_google_key(tmp_path):
    """Google API keys (AIza...) trigger CRITICAL finding."""
    f = tmp_path / "state.md"
    f.write_text("key=AIza" + "a" * 35 + "\n", encoding="utf-8")
    result = audit_file(f)
    assert result.critical_count >= 1
    assert any("Google" in x.pattern_name for x in result.findings)


def test_audit_file_stripe_key(tmp_path):
    """Stripe secret keys (sk_live_...) trigger CRITICAL finding."""
    f = tmp_path / "state.md"
    f.write_text("key=sk_live_" + "a" * 24 + "\n", encoding="utf-8")
    result = audit_file(f)
    assert result.critical_count >= 1
    assert any("Stripe" in x.pattern_name for x in result.findings)


def test_audit_file_private_key(tmp_path):
    """BEGIN PRIVATE KEY headers trigger CRITICAL finding."""
    f = tmp_path / "state.md"
    f.write_text("-----BEGIN RSA PRIVATE KEY-----\n", encoding="utf-8")
    result = audit_file(f)
    assert result.critical_count >= 1
    assert any("Private Key" in x.pattern_name for x in result.findings)


def test_audit_file_aws_key(tmp_path):
    """AWS access key IDs (AKIA...) trigger CRITICAL finding."""
    f = tmp_path / "state.md"
    f.write_text("aws_key=AKIA" + "A" * 16 + "\n", encoding="utf-8")
    result = audit_file(f)
    assert result.critical_count >= 1
    assert any("AWS" in x.pattern_name for x in result.findings)


# ---------------------------------------------------------------------------
# audit_file - HIGH patterns
# ---------------------------------------------------------------------------


def test_audit_file_password(tmp_path):
    """password=xxx assignments trigger HIGH finding."""
    f = tmp_path / "state.md"
    f.write_text("password=supersecretpass\n", encoding="utf-8")
    result = audit_file(f)
    assert result.high_count >= 1
    assert any("Password" in x.pattern_name for x in result.findings)


def test_audit_file_secret_assignment(tmp_path):
    """secret=xxx assignments trigger HIGH finding."""
    f = tmp_path / "state.md"
    f.write_text("Secret=mybigsecretvalue\n", encoding="utf-8")
    result = audit_file(f)
    assert result.high_count >= 1
    assert any("Secret" in x.pattern_name for x in result.findings)


def test_audit_file_token_assignment(tmp_path):
    """token=xxx assignments trigger HIGH finding."""
    f = tmp_path / "state.md"
    f.write_text("Token=abcdefghijklmnop\n", encoding="utf-8")
    result = audit_file(f)
    assert result.high_count >= 1
    assert any("Token" in x.pattern_name for x in result.findings)


# ---------------------------------------------------------------------------
# audit_file - clean / sanitized / edge cases
# ---------------------------------------------------------------------------


def test_audit_file_clean(tmp_path):
    """A file with no secrets returns a clean result."""
    f = tmp_path / "state.md"
    f.write_text("# My Session\n\nNo secrets here.\n", encoding="utf-8")
    result = audit_file(f)
    assert result.clean is True
    assert result.scanned_files == 1


def test_audit_file_sanitized_ignored(tmp_path):
    """Lines containing sanitized markers are not flagged."""
    f = tmp_path / "state.md"
    f.write_text("api_key=[stored in .env as OPENAI_API_KEY]\n", encoding="utf-8")
    result = audit_file(f)
    assert result.clean is True


def test_audit_file_missing():
    """A missing file returns 0 scanned files and no findings."""
    result = audit_file(Path("/nonexistent/path/file.md"))
    assert result.scanned_files == 0
    assert result.clean is True


def test_audit_file_skip_test(tmp_path):
    """Files with 'test' in the name are skipped (scanned_files=1, no findings)."""
    f = tmp_path / "test_secrets.md"
    f.write_text("sk-abcdefghijklmnopqrstu\n", encoding="utf-8")
    result = audit_file(f)
    assert result.scanned_files == 1
    assert result.critical_count == 0


def test_audit_file_binary_ignored(tmp_path):
    """Files that raise UnicodeDecodeError are gracefully handled."""
    f = tmp_path / "state.md"
    f.write_bytes(b"\xff\xfe\x00binary data\x00")
    result = audit_file(f)
    # Should not raise; returns with 1 scanned file and no findings
    assert result.scanned_files == 1
    assert result.clean is True


def test_audit_file_extra_patterns(tmp_path):
    """Custom extra_patterns are detected."""
    f = tmp_path / "state.md"
    f.write_text("custom_token=MYTOKEN123\n", encoding="utf-8")
    result = audit_file(f, extra_patterns=[(r"MYTOKEN\d+", "Custom Token")])
    assert result.high_count >= 1
    assert any("Custom Token" in x.pattern_name for x in result.findings)


# ---------------------------------------------------------------------------
# audit_directory
# ---------------------------------------------------------------------------


def test_audit_directory_recursive(tmp_path):
    """audit_directory scans all matching files recursively."""
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "file.md").write_text("# Clean file\n", encoding="utf-8")
    (tmp_path / "top.md").write_text("# Also clean\n", encoding="utf-8")

    result = audit_directory(tmp_path)
    assert result.scanned_files == 2
    assert result.clean is True


def test_audit_directory_multiple_findings(tmp_path):
    """audit_directory aggregates findings from multiple files."""
    (tmp_path / "a.md").write_text("sk-abcdefghijklmnopqrstu\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("ghp_" + "z" * 36 + "\n", encoding="utf-8")

    result = audit_directory(tmp_path)
    assert result.critical_count >= 2
    assert result.scanned_files >= 2


def test_audit_directory_empty(tmp_path):
    """An empty directory returns 0 scanned files."""
    result = audit_directory(tmp_path)
    assert result.scanned_files == 0
    assert result.clean is True


def test_audit_directory_missing():
    """A non-existent directory returns 0 scanned files."""
    result = audit_directory(Path("/nonexistent/dir"))
    assert result.scanned_files == 0
    assert result.clean is True


def test_audit_directory_custom_extensions(tmp_path):
    """Only files with the specified extensions are scanned."""
    (tmp_path / "keep.md").write_text("sk-abcdefghijklmnopqrstu\n", encoding="utf-8")
    (tmp_path / "skip.txt").write_text("sk-abcdefghijklmnopqrstu\n", encoding="utf-8")

    result = audit_directory(tmp_path, extensions={".md"})
    assert result.scanned_files == 1  # only .md


def test_audit_directory_skip_files(tmp_path):
    """Files matching skip_files patterns are excluded."""
    (tmp_path / "important.md").write_text("sk-abcdefghijklmnopqrstu\n", encoding="utf-8")
    (tmp_path / "skip_me.md").write_text("sk-abcdefghijklmnopqrstu\n", encoding="utf-8")

    result = audit_directory(tmp_path, skip_files=["skip_me"])
    # skip_me.md should be excluded; important.md should be scanned
    assert result.scanned_files == 1
    assert result.critical_count >= 1


def test_audit_directory_config_extra(tmp_path):
    """Extra patterns from config are applied during directory audit."""
    (tmp_path / "notes.md").write_text("MY_SPECIAL_KEY=abc123def456\n", encoding="utf-8")

    config_patch = {
        "secrets": {
            "extra_patterns": [{"pattern": r"MY_SPECIAL_KEY=\w+", "name": "Custom Secret"}],
            "skip_files": [],
        }
    }

    with patch(
        "cervellaswarm_session_memory.secret_auditor.load_config", return_value=config_patch
    ):
        result = audit_directory(tmp_path)

    assert result.high_count >= 1
    assert any("Custom Secret" in f.pattern_name for f in result.findings)


# ---------------------------------------------------------------------------
# Finding data integrity
# ---------------------------------------------------------------------------


def test_finding_has_no_content(tmp_path):
    """Finding dataclass does not store the secret value itself."""
    f = tmp_path / "state.md"
    secret = "sk-abcdefghijklmnopqrstu"
    f.write_text(f"key={secret}\n", encoding="utf-8")

    result = audit_file(f)
    assert result.critical_count >= 1

    finding = result.findings[0]
    # Finding only has severity, pattern_name, file, line_number - not content
    assert not hasattr(finding, "content")
    assert not hasattr(finding, "matched_text")
    assert finding.line_number == 1
    assert finding.severity == Severity.CRITICAL
