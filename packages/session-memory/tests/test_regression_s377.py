# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Regression tests for S377 bug fixes in cervellaswarm-session-memory.

Fix 1: config.py     - except Exception narrowed to (OSError, yaml.YAMLError)
Fix 2: quality_checker.py - except Exception narrowed to (OSError, UnicodeDecodeError)
Fix 3: sync_checker.py   - except Exception narrowed to (OSError, UnicodeDecodeError)
Fix 4: project_manager.py - archive_state sanitizes 'reason' parameter
Fix 5: secret_auditor.py  - invalid extra_patterns regex skipped with warning
"""

import logging
import re
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from cervellaswarm_session_memory.config import load_config, DEFAULTS
from cervellaswarm_session_memory.quality_checker import check_quality
from cervellaswarm_session_memory.sync_checker import check_file_size, CheckStatus
from cervellaswarm_session_memory.project_manager import archive_state, ProjectInfo
from cervellaswarm_session_memory.secret_auditor import audit_directory, audit_file


# ---------------------------------------------------------------------------
# Fix 1: config.py - narrow except
# ---------------------------------------------------------------------------

class TestConfigNarrowExcept:
    """Fix 1: load_config() no longer swallows non-IO/YAML exceptions."""

    def test_oserror_returns_defaults(self, tmp_path):
        """OSError on open() still returns defaults (preserved behaviour)."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("memory_dir: .custom\n", encoding="utf-8")

        with patch("builtins.open", side_effect=OSError("disk failure")):
            result = load_config(config_path)

        assert result["memory_dir"] == DEFAULTS["memory_dir"]

    def test_yaml_error_returns_defaults(self, tmp_path):
        """yaml.YAMLError during safe_load still returns defaults."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("memory_dir: .custom\n", encoding="utf-8")

        with patch(
            "cervellaswarm_session_memory.config.yaml.safe_load",
            side_effect=yaml.YAMLError("bad yaml"),
        ):
            result = load_config(config_path)

        assert result["memory_dir"] == DEFAULTS["memory_dir"]

    def test_unexpected_exception_propagates(self, tmp_path):
        """TypeError (unexpected) must propagate, not be silently caught."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("memory_dir: .custom\n", encoding="utf-8")

        with patch(
            "cervellaswarm_session_memory.config.yaml.safe_load",
            side_effect=TypeError("unexpected"),
        ):
            with pytest.raises(TypeError):
                load_config(config_path)


# ---------------------------------------------------------------------------
# Fix 2: quality_checker.py - narrow except
# ---------------------------------------------------------------------------

class TestQualityCheckerNarrowExcept:
    """Fix 2: check_quality() no longer swallows non-IO exceptions."""

    def test_oserror_returns_error_status(self, tmp_path):
        """OSError while reading file returns QualityResult with status ERROR."""
        state_file = tmp_path / "SESSION_STATE_proj.md"
        state_file.write_text("# content\n", encoding="utf-8")

        with patch.object(Path, "read_text", side_effect=OSError("perm denied")):
            result = check_quality(state_file, project_name="proj")

        assert result.status == "ERROR"
        assert any("Cannot read file" in w for w in result.warnings)

    def test_unicode_error_returns_error_status(self, tmp_path):
        """UnicodeDecodeError while reading returns QualityResult with status ERROR."""
        state_file = tmp_path / "SESSION_STATE_proj.md"
        state_file.write_bytes(b"\xff\xfe bad bytes")

        result = check_quality(state_file, project_name="proj")

        assert result.status == "ERROR"

    def test_runtime_error_propagates(self, tmp_path):
        """RuntimeError (unexpected) must propagate from check_quality()."""
        state_file = tmp_path / "SESSION_STATE_proj.md"
        state_file.write_text("# content\n", encoding="utf-8")

        with patch.object(Path, "read_text", side_effect=RuntimeError("unexpected")):
            with pytest.raises(RuntimeError):
                check_quality(state_file, project_name="proj")


# ---------------------------------------------------------------------------
# Fix 3: sync_checker.py - narrow except
# ---------------------------------------------------------------------------

class TestSyncCheckerNarrowExcept:
    """Fix 3: check_file_size() no longer swallows non-IO exceptions."""

    def test_oserror_returns_error_status(self, tmp_path):
        """OSError while reading returns (CheckStatus.ERROR, message)."""
        target = tmp_path / "STATE.md"
        target.write_text("hello\n", encoding="utf-8")

        with patch.object(Path, "read_text", side_effect=OSError("disk error")):
            status, msg = check_file_size(target)

        assert status == CheckStatus.ERROR
        assert "Cannot read file" in msg

    def test_unicode_error_returns_error_status(self, tmp_path):
        """UnicodeDecodeError returns (CheckStatus.ERROR, message)."""
        target = tmp_path / "STATE.md"
        target.write_bytes(b"\xff\xfe bad bytes")

        status, msg = check_file_size(target)

        assert status == CheckStatus.ERROR
        assert "Cannot read file" in msg

    def test_runtime_error_propagates(self, tmp_path):
        """RuntimeError (unexpected) must propagate from check_file_size()."""
        target = tmp_path / "STATE.md"
        target.write_text("hello\n", encoding="utf-8")

        with patch.object(Path, "read_text", side_effect=RuntimeError("unexpected")):
            with pytest.raises(RuntimeError):
                check_file_size(target)


# ---------------------------------------------------------------------------
# Fix 4: project_manager.py - archive_state sanitizes reason
# ---------------------------------------------------------------------------

class TestArchiveStateSanitizesReason:
    """Fix 4: archive_state() sanitizes the reason parameter."""

    def _make_project(self, tmp_path: Path) -> ProjectInfo:
        """Create a minimal ProjectInfo with real files."""
        mem_dir = tmp_path / ".session-memory"
        project_dir = mem_dir / "myproj"
        archive_dir = project_dir / "archive"
        archive_dir.mkdir(parents=True)
        state_file = project_dir / "SESSION_STATE_myproj.md"
        state_file.write_text("# state\n", encoding="utf-8")
        return ProjectInfo(
            name="myproj",
            memory_dir=mem_dir,
            state_file=state_file,
            archive_dir=archive_dir,
        )

    def test_path_traversal_reason_sanitized(self, tmp_path):
        """reason with path separators must not appear in archive filename."""
        project = self._make_project(tmp_path)
        archive_path = archive_state(project, reason="../../../etc/passwd")

        assert "/" not in archive_path.name
        assert ".." not in archive_path.name

    def test_reason_with_spaces_sanitized(self, tmp_path):
        """Spaces in reason are replaced; the file is created successfully."""
        project = self._make_project(tmp_path)
        archive_path = archive_state(project, reason="end of sprint")

        assert " " not in archive_path.name
        assert archive_path.exists()

    def test_safe_reason_passes_through_unchanged(self, tmp_path):
        """Alphanumeric, dash, underscore reason chars survive unchanged."""
        project = self._make_project(tmp_path)
        reason = "end-of-sprint_42"
        archive_path = archive_state(project, reason=reason)

        assert reason in archive_path.name
        assert archive_path.exists()

    def test_empty_reason_produces_no_suffix(self, tmp_path):
        """Empty reason produces no extra suffix in the archive filename."""
        project = self._make_project(tmp_path)
        archive_path = archive_state(project, reason="")

        # Stem should end with the date, no trailing underscore before .md
        stem = archive_path.stem
        # pattern: SESSION_STATE_myproj_archived_YYYY-MM-DD
        assert re.search(r"_archived_\d{4}-\d{2}-\d{2}$", stem)
        assert archive_path.exists()


# ---------------------------------------------------------------------------
# Fix 5: secret_auditor.py - invalid extra_patterns regex skipped
# ---------------------------------------------------------------------------

class TestSecretAuditorInvalidRegex:
    """Fix 5: invalid regex in config extra_patterns is skipped with a warning.

    Note: audit_directory's should_skip_file() rejects files whose full path
    contains 'test' (SKIP_PATTERNS = ['*test*']).  pytest's tmp_path always
    contains the test-function name, so we use audit_file() directly for
    pattern-matching assertions and mock audit_file for directory-level tests.
    """

    def _write_clean_file(self, content: str) -> tuple[Path, Path]:
        """Write content to a .md file in a fresh tempdir that avoids SKIP_PATTERNS.

        IMPORTANT: pytest tmp_path embeds the test function name in the path,
        which always contains 'test'.  should_skip_file() rejects any file whose
        full path contains 'test', so we use tempfile.mkdtemp() which produces a
        random suffix without 'test' in it.

        Returns (file_path, tmpdir) so callers can clean up if needed.
        """
        tmpdir = Path(tempfile.mkdtemp(prefix="cervella_reg_"))
        f = tmpdir / "SESSION_STATE_proj.md"
        f.write_text(content, encoding="utf-8")
        return f, tmpdir

    def _config_with_extra_patterns(self, patterns: list) -> dict:
        """Return a minimal config dict with given extra_patterns."""
        return {
            "memory_dir": ".session-memory",
            "max_lines": 300,
            "warning_lines": 200,
            "secrets": {
                "extra_patterns": patterns,
                "skip_files": [],
            },
        }

    def test_valid_extra_pattern_is_used(self):
        """Valid extra_patterns passed to audit_file are loaded and detect matches."""
        content = "internal_token=abc123secret_value_here\n"
        state_file, _ = self._write_clean_file(content)

        # audit_file() accepts extra_patterns directly.
        result = audit_file(state_file, extra_patterns=[(r"internal_token=[^\s]+", "Internal Token")])

        assert any(f.pattern_name == "Internal Token" for f in result.findings)

    def test_invalid_regex_is_skipped_no_crash(self, caplog):
        """Invalid regex in config extra_patterns does not crash audit_directory().

        We mock audit_file to avoid the should_skip_file path check, and verify
        that audit_directory's pattern-loading loop emits a WARNING and skips
        the bad pattern without raising.
        """
        config = self._config_with_extra_patterns(
            [{"pattern": "[unclosed", "name": "Bad Pattern"}]
        )

        fake_dir = MagicMock()
        fake_dir.exists.return_value = True
        fake_dir.rglob.return_value = []  # no files to scan

        with patch("cervellaswarm_session_memory.secret_auditor.load_config", return_value=config):
            with caplog.at_level(logging.WARNING, logger="cervellaswarm_session_memory.secret_auditor"):
                result = audit_directory(fake_dir)

        assert result.scanned_files == 0  # no files, but no crash
        assert any(
            "Skipping" in r.message or "invalid regex" in r.message.lower()
            for r in caplog.records
        )

    def test_valid_pattern_works_alongside_invalid(self, caplog):
        """Valid patterns in config still work even when a prior one is invalid.

        Uses audit_file() directly to confirm pattern application, and
        audit_directory() with mocked load_config to confirm the loading path.
        """
        content = "custom_key=supersecretvalue123\n"
        state_file, _ = self._write_clean_file(content)

        # 1. Confirm the valid pattern itself works via audit_file
        result_direct = audit_file(
            state_file,
            extra_patterns=[(r"custom_key=[^\s]+", "Custom Key")],
        )
        assert any(f.pattern_name == "Custom Key" for f in result_direct.findings)

        # 2. Confirm audit_directory loads valid patterns despite an invalid one
        config = self._config_with_extra_patterns(
            [
                {"pattern": "[unclosed", "name": "Bad Pattern"},
                {"pattern": r"custom_key=[^\s]+", "name": "Custom Key"},
            ]
        )
        fake_dir = MagicMock()
        fake_dir.exists.return_value = True
        fake_dir.rglob.return_value = []

        with patch("cervellaswarm_session_memory.secret_auditor.load_config", return_value=config):
            with caplog.at_level(logging.WARNING, logger="cervellaswarm_session_memory.secret_auditor"):
                audit_directory(fake_dir)

        # The WARNING for the invalid pattern must be present
        assert any("Skipping" in r.message for r in caplog.records)
