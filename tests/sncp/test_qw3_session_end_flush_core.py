"""Hard Tests for QW3 - SessionEnd Hook Flush (CORE/UNIT)

Tests SNCP 4.0 Fase 1 automatic memory flush at session end.

Target:
- Hook Registration: Properly registered with Claude Code
- Execution: Calls memory-flush.sh at session end
- Error Handling: Graceful failures, never blocks session end
- Integration: Works with daily-log.sh

Author: Cervella Tester
Date: 2026-02-02
Score Target: 9.5/10
"""

import pytest
import json
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime


# Import module to test
sys.path.insert(0, str(Path.home() / ".claude/hooks"))
import session_end_flush


# ============================================================================
# CONFIGURATION
# ============================================================================

HOOK_PATH = Path.home() / ".claude/hooks/session_end_flush.py"
MEMORY_FLUSH_SCRIPT = Path.home() / "Developer/CervellaSwarm/scripts/swarm/memory-flush.sh"
DAILY_LOG_SCRIPT = Path.home() / "Developer/CervellaSwarm/scripts/sncp/daily-log.sh"


# ============================================================================
# UNIT TESTS - Hook Existence & Structure
# ============================================================================


class TestHookStructure:
    """Test hook file structure and imports."""

    def test_hook_file_exists(self):
        """Hook file should exist."""
        assert HOOK_PATH.exists(), f"Hook not found: {HOOK_PATH}"
        assert HOOK_PATH.is_file()

    def test_hook_imports_successfully(self):
        """Hook should import without errors."""
        result = subprocess.run(
            ["python3", "-c", f"import sys; sys.path.insert(0, '{HOOK_PATH.parent}'); import session_end_flush"],
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode == 0, f"Import failed: {result.stderr}"

    def test_hook_has_main_function(self):
        """Hook should have main() function."""
        assert hasattr(session_end_flush, 'main')
        assert callable(session_end_flush.main)

    def test_hook_version(self):
        """Hook should have version."""
        assert hasattr(session_end_flush, '__version__')
        assert session_end_flush.__version__ == "1.0.0"


# ============================================================================
# UNIT TESTS - Project Detection
# ============================================================================


class TestProjectDetection:
    """Test project detection from cwd."""

    def test_detect_cervellaswarm(self):
        """Should detect CervellaSwarm project."""
        project = session_end_flush.detect_project("/Users/rafapra/Developer/CervellaSwarm")
        assert project == "cervellaswarm"

    def test_detect_miracollo(self):
        """Should detect Miracollo project."""
        project = session_end_flush.detect_project("/Users/rafapra/Developer/miracollogeminifocus")
        assert project == "miracollo"

    def test_detect_contabilita(self):
        """Should detect Contabilita project."""
        project = session_end_flush.detect_project("/Users/rafapra/Developer/ContabilitaAntigravity")
        assert project == "contabilita"

    def test_detect_unknown_project(self):
        """Should return None for unknown project."""
        project = session_end_flush.detect_project("/some/random/path")
        assert project is None

    def test_detect_case_insensitive(self):
        """Should detect regardless of case."""
        project = session_end_flush.detect_project("/Users/rafapra/Developer/CERVELLASWARM")
        assert project == "cervellaswarm"


# ============================================================================
# UNIT TESTS - Memory Flush Execution
# ============================================================================


class TestMemoryFlushExecution:
    """Test run_memory_flush() function."""

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'MEMORY_FLUSH_SCRIPT')
    def test_calls_memory_flush_script(self, mock_script, mock_subprocess):
        """Should call memory-flush.sh with correct arguments."""
        # Configure mock to return proper path string
        mock_script_path = "/fake/path/memory-flush.sh"
        mock_script.exists.return_value = True
        mock_script.__str__.return_value = mock_script_path
        mock_subprocess.return_value = Mock(returncode=0, stdout="Success", stderr="")

        result = session_end_flush.run_memory_flush("cervellaswarm")

        # Verify subprocess called
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]

        assert "memory-flush.sh" in str(call_args)
        assert "cervellaswarm" in call_args
        assert "session_end" in call_args
        assert "true" in call_args  # Silent mode

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'MEMORY_FLUSH_SCRIPT')
    def test_returns_success_on_success(self, mock_script, mock_subprocess):
        """Should return success=True on successful flush."""
        mock_script.exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=0, stdout="Done", stderr="")

        result = session_end_flush.run_memory_flush("cervellaswarm")

        assert result["success"] is True
        assert "error" not in result or result["error"] is None

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'MEMORY_FLUSH_SCRIPT')
    def test_returns_error_on_failure(self, mock_script, mock_subprocess):
        """Should return success=False on script failure."""
        mock_script.exists.return_value = True
        mock_subprocess.return_value = Mock(returncode=1, stdout="", stderr="Error occurred")

        result = session_end_flush.run_memory_flush("cervellaswarm")

        assert result["success"] is False
        assert "error" in result
        assert result["error"] == "Error occurred"

    @patch.object(session_end_flush, 'MEMORY_FLUSH_SCRIPT')
    def test_handles_missing_script(self, mock_script):
        """Should handle missing script gracefully."""
        mock_script.exists.return_value = False
        mock_script.__str__.return_value = "/fake/path/memory-flush.sh"

        result = session_end_flush.run_memory_flush("cervellaswarm")

        assert result["success"] is False
        assert "not found" in result["error"].lower() or "non trovato" in result["error"].lower()

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'MEMORY_FLUSH_SCRIPT')
    def test_handles_timeout(self, mock_script, mock_subprocess):
        """Should handle subprocess timeout."""
        import subprocess as sp

        mock_script.exists.return_value = True
        mock_subprocess.side_effect = sp.TimeoutExpired("cmd", 30)

        result = session_end_flush.run_memory_flush("cervellaswarm")

        assert result["success"] is False
        assert "timeout" in result["error"].lower()

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'MEMORY_FLUSH_SCRIPT')
    def test_handles_exception(self, mock_script, mock_subprocess):
        """Should handle generic exceptions."""
        mock_script.exists.return_value = True
        mock_subprocess.side_effect = Exception("Unexpected error")

        result = session_end_flush.run_memory_flush("cervellaswarm")

        assert result["success"] is False
        assert "error" in result


# ============================================================================
# UNIT TESTS - Daily Log Integration
# ============================================================================


class TestDailyLogIntegration:
    """Test add_daily_log_note() function."""

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'DAILY_LOG_SCRIPT')
    def test_adds_note_to_daily_log(self, mock_script, mock_subprocess):
        """Should call daily-log.sh to add note."""
        # Configure mock to return proper path string
        mock_script_path = "/fake/path/daily-log.sh"
        mock_script.exists.return_value = True
        mock_script.__str__.return_value = mock_script_path
        mock_subprocess.return_value = Mock(returncode=0)

        result = session_end_flush.add_daily_log_note("cervellaswarm", "Test note")

        # Verify subprocess called
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]

        assert "daily-log.sh" in str(call_args)
        assert "cervellaswarm" in call_args
        assert "Test note" in call_args

        assert result is True

    @patch.object(session_end_flush, 'DAILY_LOG_SCRIPT')
    def test_handles_missing_daily_log_script(self, mock_script):
        """Should handle missing daily-log.sh gracefully."""
        mock_script.exists.return_value = False

        result = session_end_flush.add_daily_log_note("cervellaswarm", "Note")

        assert result is False

    @patch.object(session_end_flush.subprocess, 'run')
    @patch.object(session_end_flush, 'DAILY_LOG_SCRIPT')
    def test_handles_daily_log_error(self, mock_script, mock_subprocess):
        """Should handle daily-log.sh errors gracefully."""
        mock_script.exists.return_value = True
        mock_subprocess.side_effect = Exception("Error")

        result = session_end_flush.add_daily_log_note("cervellaswarm", "Note")

        assert result is False
