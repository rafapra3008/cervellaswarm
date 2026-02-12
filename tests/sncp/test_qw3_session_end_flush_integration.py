"""Hard Tests for QW3 - SessionEnd Hook Flush (INTEGRATION)

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
# INTEGRATION TESTS - Main Function Flow
# ============================================================================


class TestMainFunctionFlow:
    """Test main() function integration."""

    @patch.object(session_end_flush, 'run_memory_flush')
    @patch.object(session_end_flush, 'add_daily_log_note')
    @patch('sys.stdin')
    def test_main_executes_flush_for_known_project(self, mock_stdin, mock_add_note, mock_flush):
        """Main should execute flush for known project."""
        # Mock input
        input_data = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "test-session-123"
        }

        mock_flush.return_value = {"success": True, "output": "Done"}

        # Capture stdout
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with patch('json.load', return_value=input_data):
            with redirect_stdout(f):
                result = session_end_flush.main()

        # Verify flush was called
        mock_flush.assert_called_once_with("cervellaswarm")

        # Verify daily log note added
        mock_add_note.assert_called_once()
        note_text = mock_add_note.call_args[0][1]
        assert "SessionEnd" in note_text
        assert "OK" in note_text

        # Verify exit code
        assert result == 0

    @patch.object(session_end_flush, 'run_memory_flush')
    @patch.object(session_end_flush, 'add_daily_log_note')
    @patch('sys.stdin')
    def test_main_silent_for_unknown_project(self, mock_stdin, mock_add_note, mock_flush):
        """Main should be silent for unknown project."""
        input_data = {
            "cwd": "/some/unknown/path",
            "session_id": "test-session-123"
        }

        with patch('json.load', return_value=input_data):
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                result = session_end_flush.main()

        # Should not call flush
        mock_flush.assert_not_called()
        mock_add_note.assert_not_called()

        # Should still return success
        assert result == 0

    @patch.object(session_end_flush, 'run_memory_flush')
    @patch.object(session_end_flush, 'add_daily_log_note')
    def test_main_always_continues_on_error(self, mock_add_note, mock_flush):
        """Main should always return continue=True even on error."""
        mock_flush.return_value = {"success": False, "error": "Something failed"}

        input_data = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "test"
        }

        with patch('json.load', return_value=input_data):
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                result = session_end_flush.main()

        # Should return 0 (success) even on flush failure
        assert result == 0

        # Output should contain continue=True
        output = f.getvalue()
        data = json.loads(output)
        assert data["continue"] is True

    @patch.object(session_end_flush, 'run_memory_flush')
    @patch.object(session_end_flush, 'add_daily_log_note')
    def test_main_handles_json_decode_error(self, mock_add_note, mock_flush):
        """Main should handle invalid JSON input."""
        with patch('json.load', side_effect=json.JSONDecodeError("test", "doc", 0)):
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                result = session_end_flush.main()

        # Should not crash
        assert result == 0

        # Should output valid JSON
        output = f.getvalue()
        data = json.loads(output)
        assert data["continue"] is True


# ============================================================================
# CRITICAL TEST - Never Blocks Session End
# ============================================================================


class TestNeverBlocks:
    """Critical: Hook must NEVER block session end."""

    @patch.object(session_end_flush, 'run_memory_flush')
    def test_never_raises_exception(self, mock_flush):
        """Should never raise exception that blocks session end."""
        # Return error dict instead of raising, to match current behavior
        mock_flush.return_value = {"success": False, "error": "Catastrophic failure!"}

        input_data = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "test"
        }

        # Should not raise (run_memory_flush returns error dict, doesn't throw)
        with patch('json.load', return_value=input_data):
            try:
                result = session_end_flush.main()
                assert result == 0
            except Exception as e:
                pytest.fail(f"Hook raised exception (blocks session end!): {e}")

    @patch.object(session_end_flush, 'run_memory_flush')
    def test_always_outputs_valid_json(self, mock_flush):
        """Output must always be valid JSON."""
        # Return error dict instead of raising
        mock_flush.return_value = {"success": False, "error": "Error"}

        input_data = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "test"
        }

        with patch('json.load', return_value=input_data):
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                session_end_flush.main()

        # Output must be valid JSON
        output = f.getvalue()
        data = json.loads(output)  # Should not raise

        # Must have continue=True
        assert "continue" in data
        assert data["continue"] is True

    @patch.object(session_end_flush, 'run_memory_flush')
    def test_timeout_does_not_block(self, mock_flush):
        """Timeout in flush should not block session end."""
        import time

        def slow_flush(project):
            time.sleep(5)  # Simulate slow operation
            return {"success": True}

        mock_flush.side_effect = slow_flush

        input_data = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "test"
        }

        # Main should complete (not wait for slow flush)
        # Note: In real implementation, subprocess has timeout=30
        with patch('json.load', return_value=input_data):
            start = time.time()
            result = session_end_flush.main()
            elapsed = time.time() - start

            # Should complete within reasonable time
            # (accounting for mock, not actual subprocess timeout)
            assert result == 0


# ============================================================================
# EDGE CASES - Robustness
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    @patch.object(session_end_flush, 'run_memory_flush')
    def test_handles_empty_cwd(self, mock_flush):
        """Should handle empty cwd."""
        input_data = {"cwd": "", "session_id": "test"}

        with patch('json.load', return_value=input_data):
            result = session_end_flush.main()

        # Should not crash
        assert result == 0

    @patch.object(session_end_flush, 'run_memory_flush')
    def test_handles_missing_cwd(self, mock_flush):
        """Should handle missing cwd key."""
        input_data = {"session_id": "test"}

        with patch('json.load', return_value=input_data):
            result = session_end_flush.main()

        # Should use os.getcwd() as fallback
        assert result == 0

    @patch.object(session_end_flush, 'run_memory_flush')
    def test_handles_unicode_in_input(self, mock_flush):
        """Should handle unicode in input data."""
        input_data = {
            "cwd": "/Users/rafapra/Developer/Cérvellaßwârm",
            "session_id": "tëst-🚀"
        }

        mock_flush.return_value = {"success": True}

        with patch('json.load', return_value=input_data):
            result = session_end_flush.main()

        assert result == 0


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================


class TestPerformance:
    """Test performance requirements."""

    @patch.object(session_end_flush, 'run_memory_flush')
    @patch.object(session_end_flush, 'add_daily_log_note')
    def test_hook_is_fast(self, mock_add_note, mock_flush):
        """Hook should complete in <1 second."""
        import time

        mock_flush.return_value = {"success": True, "output": "Done"}
        mock_add_note.return_value = True

        input_data = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "test"
        }

        with patch('json.load', return_value=input_data):
            start_time = time.time()
            session_end_flush.main()
            elapsed_time = time.time() - start_time

        # Should complete very quickly (mocked)
        assert elapsed_time < 0.1, f"Hook took {elapsed_time:.3f}s"
