"""Hard Tests for QW1 - Daily Memory Auto-Load

Tests SNCP 4.0 Fase 1 auto-load daily logs (today + yesterday).

Target:
- Functionality: Load today + yesterday logs correctly
- Output: Valid JSON and Markdown formats
- Edge cases: Missing files, invalid paths
- Integration: Works with SessionStart hook

Author: Cervella Tester
Date: 2026-02-02
Score Target: 9.5/10
"""

import pytest
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


# ============================================================================
# CONFIGURATION
# ============================================================================

LOAD_DAILY_SCRIPT = Path("/Users/rafapra/Developer/CervellaSwarm/scripts/sncp/load-daily-memory.sh")
SNCP_ROOT = Path("/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti")


# ============================================================================
# UNIT TESTS - Script Output Formats
# ============================================================================


class TestLoadDailyScript:
    """Test load-daily-memory.sh script."""

    def test_script_exists(self):
        """Script file should exist."""
        assert LOAD_DAILY_SCRIPT.exists(), f"Script not found: {LOAD_DAILY_SCRIPT}"
        assert LOAD_DAILY_SCRIPT.is_file()

    def test_script_executable(self):
        """Script should be executable."""
        import os
        assert os.access(LOAD_DAILY_SCRIPT, os.X_OK), "Script not executable"

    def test_help_flag(self):
        """Should display help with --help flag."""
        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode == 0
        assert "USAGE:" in result.stdout
        assert "load-daily-memory.sh" in result.stdout

    def test_requires_project_argument(self):
        """Should fail without project argument."""
        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode != 0
        assert "Error" in result.stdout or "Error" in result.stderr


class TestMarkdownOutput:
    """Test markdown output format."""

    def test_markdown_format(self, mock_daily_logs_both):
        """Should output valid markdown with both logs."""
        project_dir, env = mock_daily_logs_both

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0
        output = result.stdout

        # Check markdown structure
        assert "# Daily Memory - testproject" in output
        assert "## 📅 Today" in output
        assert "## 📅 Yesterday" in output
        assert "---" in output

    def test_markdown_with_today_only(self, mock_daily_logs_today):
        """Should handle only today's log."""
        project_dir, env = mock_daily_logs_today

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0
        output = result.stdout

        assert "## 📅 Today" in output
        assert "## 📅 Yesterday" in output
        assert "*No daily log for yesterday" in output  # Partial match for period variance

    def test_markdown_with_no_logs(self, mock_daily_logs_empty):
        """Should handle missing logs gracefully."""
        project_dir, env = mock_daily_logs_empty

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0
        output = result.stdout

        assert "*No daily log for today" in output  # Partial match for period/message variance
        assert "*No daily log for yesterday" in output


class TestJSONOutput:
    """Test JSON output format."""

    def test_json_format_both_logs(self, mock_daily_logs_both):
        """Should output valid JSON with both logs."""
        project_dir, env = mock_daily_logs_both

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0

        # Parse JSON
        data = json.loads(result.stdout)

        # Check structure
        assert "project" in data
        assert data["project"] == "testproject"
        assert "today" in data
        assert "yesterday" in data

        # Check today
        assert "date" in data["today"]
        assert "content" in data["today"]
        assert "exists" in data["today"]
        assert data["today"]["exists"] is True

        # Check yesterday
        assert data["yesterday"]["exists"] is True

    def test_json_format_today_only(self, mock_daily_logs_today):
        """Should output valid JSON with only today."""
        project_dir, env = mock_daily_logs_today

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)

        assert data["today"]["exists"] is True
        assert data["yesterday"]["exists"] is False

    def test_json_format_no_logs(self, mock_daily_logs_empty):
        """Should output valid JSON with no logs."""
        project_dir, env = mock_daily_logs_empty

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)

        assert data["today"]["exists"] is False
        assert data["yesterday"]["exists"] is False

    def test_json_date_format(self, mock_daily_logs_both):
        """JSON dates should be in YYYY-MM-DD format."""
        project_dir, env = mock_daily_logs_both

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        data = json.loads(result.stdout)

        # Validate date format
        today_date = data["today"]["date"]
        yesterday_date = data["yesterday"]["date"]

        datetime.strptime(today_date, "%Y-%m-%d")
        datetime.strptime(yesterday_date, "%Y-%m-%d")

        # Yesterday should be 1 day before today
        today = datetime.strptime(today_date, "%Y-%m-%d")
        yesterday = datetime.strptime(yesterday_date, "%Y-%m-%d")
        assert (today - yesterday).days == 1


# ============================================================================
# INTEGRATION TESTS - Hook Integration
# ============================================================================


class TestHookIntegration:
    """Test integration with SessionStart hook."""

    def test_hook_exists(self):
        """SessionStart hook file should exist."""
        hook_path = Path.home() / ".claude/hooks/daily_memory_loader.py"
        assert hook_path.exists(), f"Hook not found: {hook_path}"

    def test_hook_imports(self):
        """Hook should import without errors."""
        hook_path = Path.home() / ".claude/hooks/daily_memory_loader.py"

        result = subprocess.run(
            ["python3", "-c", f"import sys; sys.path.insert(0, '{hook_path.parent}'); import daily_memory_loader"],
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode == 0, f"Import failed: {result.stderr}"

    def test_hook_detect_project(self):
        """Hook should detect project from cwd correctly."""
        import sys
        sys.path.insert(0, str(Path.home() / ".claude/hooks"))

        from daily_memory_loader import detect_project

        # Test project detection
        assert detect_project("/Users/rafapra/Developer/CervellaSwarm") == "cervellaswarm"
        assert detect_project("/Users/rafapra/Developer/miracollogeminifocus") == "miracollo"
        assert detect_project("/Users/rafapra/Developer/ContabilitaAntigravity") == "contabilita"
        assert detect_project("/some/other/path") is None


# ============================================================================
# EDGE CASES - Robustness
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_nonexistent_project(self, sncp_test_env):
        """Should handle nonexistent project gracefully."""
        env, tmp_path = sncp_test_env

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "nonexistent_project_xyz", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        # Script returns 0 but outputs error JSON
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "error" in data

    def test_creates_memoria_directory(self, mock_project_no_memoria):
        """Should create memoria directory if missing."""
        project_dir, env = mock_project_no_memoria
        memoria_dir = project_dir / "memoria"

        # Verify memoria doesn't exist
        assert not memoria_dir.exists()

        # Run script
        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0

        # Verify memoria directory created
        assert memoria_dir.exists()
        assert (memoria_dir / "archivio").exists()

    def test_special_characters_in_content(self, mock_daily_logs_special_chars):
        """Should handle special characters in log content."""
        project_dir, env = mock_daily_logs_special_chars

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)

        # Should handle special chars without breaking JSON
        assert "content" in data["today"]
        content = data["today"]["content"]
        assert isinstance(content, str)

    def test_very_large_log_file(self, mock_daily_logs_large):
        """Should handle large log files (>10k lines)."""
        project_dir, env = mock_daily_logs_large

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=10,  # Give more time for large file
            env=env
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["today"]["exists"] is True


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================


class TestPerformance:
    """Test performance requirements."""

    def test_load_performance(self, mock_daily_logs_both):
        """Should load logs in <1 second."""
        import time
        project_dir, env = mock_daily_logs_both

        start_time = time.time()

        result = subprocess.run(
            ["bash", str(LOAD_DAILY_SCRIPT), "testproject", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        elapsed_time = time.time() - start_time

        assert result.returncode == 0
        assert elapsed_time < 1.0, f"Load took {elapsed_time:.3f}s (>1s)"
