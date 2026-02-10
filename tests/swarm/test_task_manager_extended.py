"""
Test per CervellaSwarm Task Manager (EXTENDED)

Status, ACK, list, cleanup, edge cases, error handling, CLI.

Split da test_task_manager.py (660 righe > 500 limite).
Sessione 348.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.swarm.task_manager import (
    validate_task_id,
    ensure_tasks_dir,
    create_task,
    list_tasks,
    mark_ready,
    mark_working,
    ack_received,
    ack_understood,
    mark_done,
    get_task_status,
    get_ack_status,
    cleanup_task,
    SWARM_DIR,
    TASKS_DIR,
)


# === FIXTURES ===


@pytest.fixture
def temp_tasks_dir():
    """Crea una directory temporanea per i test."""
    temp_dir = tempfile.mkdtemp()
    original_tasks_dir = TASKS_DIR

    import scripts.swarm.task_manager as tm
    tm.TASKS_DIR = f"{temp_dir}/.swarm/tasks"

    yield temp_dir

    shutil.rmtree(temp_dir, ignore_errors=True)
    tm.TASKS_DIR = original_tasks_dir


# === STATUS TESTS ===


class TestGetTaskStatus:
    """Test lettura status task."""

    def test_status_created(self, temp_tasks_dir):
        """Task appena creato ha status 'created'."""
        create_task("TASK_001", "worker", "Test")
        assert get_task_status("TASK_001") == "created"

    def test_status_ready(self, temp_tasks_dir):
        """Task ready ha status 'ready'."""
        create_task("TASK_001", "worker", "Test")
        mark_ready("TASK_001")
        assert get_task_status("TASK_001") == "ready"

    def test_status_working(self, temp_tasks_dir):
        """Task in lavorazione ha status 'working'."""
        create_task("TASK_001", "worker", "Test")
        mark_working("TASK_001")
        assert get_task_status("TASK_001") == "working"

    def test_status_done(self, temp_tasks_dir):
        """Task completato ha status 'done'."""
        create_task("TASK_001", "worker", "Test")
        mark_done("TASK_001")
        assert get_task_status("TASK_001") == "done"

    def test_status_priority_done_over_working(self, temp_tasks_dir):
        """Status 'done' ha priorita su 'working'."""
        create_task("TASK_001", "worker", "Test")
        mark_working("TASK_001")
        mark_done("TASK_001")
        assert get_task_status("TASK_001") == "done"

    def test_status_not_found(self, temp_tasks_dir):
        """Task inesistente ritorna 'not_found'."""
        assert get_task_status("NONEXISTENT") == "not_found"

    def test_status_invalid_id(self, temp_tasks_dir):
        """ID invalido ritorna 'invalid'."""
        assert get_task_status("../hack") == "invalid"


class TestGetAckStatus:
    """Test lettura status ACK."""

    def test_ack_all_missing(self, temp_tasks_dir):
        """Nessun ACK = -/-/-"""
        create_task("TASK_001", "worker", "Test")
        assert get_ack_status("TASK_001") == "-/-/-"

    def test_ack_received_only(self, temp_tasks_dir):
        """Solo ACK_RECEIVED."""
        create_task("TASK_001", "worker", "Test")
        ack_received("TASK_001")
        assert get_ack_status("TASK_001") == "\u2713/-/-"

    def test_ack_received_and_understood(self, temp_tasks_dir):
        """ACK_RECEIVED + ACK_UNDERSTOOD."""
        create_task("TASK_001", "worker", "Test")
        ack_received("TASK_001")
        ack_understood("TASK_001")
        assert get_ack_status("TASK_001") == "\u2713/\u2713/-"

    def test_ack_all_complete(self, temp_tasks_dir):
        """Tutti gli ACK completi."""
        create_task("TASK_001", "worker", "Test")
        ack_received("TASK_001")
        ack_understood("TASK_001")
        mark_done("TASK_001")
        assert get_ack_status("TASK_001") == "\u2713/\u2713/\u2713"

    def test_ack_invalid_id(self, temp_tasks_dir):
        """ID invalido ritorna ---"""
        assert get_ack_status("../hack") == "---"


# === LIST TASKS TESTS ===


class TestListTasks:
    """Test lista task."""

    def test_list_empty(self, temp_tasks_dir):
        """Lista vuota quando non ci sono task."""
        tasks = list_tasks()
        assert tasks == []

    def test_list_single_task(self, temp_tasks_dir):
        """Lista un singolo task."""
        create_task("TASK_001", "cervella-backend", "Test")
        tasks = list_tasks()

        assert len(tasks) == 1
        assert tasks[0]['task_id'] == "TASK_001"
        assert tasks[0]['status'] == "created"
        assert tasks[0]['agent'] == "cervella-backend"
        assert tasks[0]['ack'] == "-/-/-"

    def test_list_multiple_tasks(self, temp_tasks_dir):
        """Lista multipli task ordinati."""
        create_task("TASK_003", "worker-a", "Third")
        create_task("TASK_001", "worker-b", "First")
        create_task("TASK_002", "worker-c", "Second")

        tasks = list_tasks()
        assert len(tasks) == 3

        task_ids = [t['task_id'] for t in tasks]
        assert task_ids == sorted(task_ids)

    def test_list_with_various_statuses(self, temp_tasks_dir):
        """Lista task con diversi status."""
        create_task("TASK_001", "worker", "Ready task")
        mark_ready("TASK_001")

        create_task("TASK_002", "worker", "Working task")
        mark_working("TASK_002")

        create_task("TASK_003", "worker", "Done task")
        mark_done("TASK_003")

        tasks = list_tasks()
        assert len(tasks) == 3
        assert tasks[0]['status'] == "ready"
        assert tasks[1]['status'] == "working"
        assert tasks[2]['status'] == "done"

    def test_list_handles_corrupted_metadata(self, temp_tasks_dir):
        """Lista task anche se metadata corrotto."""
        create_task("TASK_001", "worker", "Test")

        import scripts.swarm.task_manager as tm
        task_file = Path(tm.TASKS_DIR) / "TASK_001.md"
        task_file.write_text("Corrupted content without metadata")

        tasks = list_tasks()
        assert len(tasks) == 1
        assert tasks[0]['agent'] == "unknown"


# === CLEANUP TESTS ===


class TestCleanupTask:
    """Test cleanup marker files."""

    def test_cleanup_removes_all_markers(self, temp_tasks_dir):
        """Cleanup deve rimuovere tutti i marker files."""
        create_task("TASK_001", "worker", "Test")
        mark_ready("TASK_001")
        mark_working("TASK_001")
        ack_received("TASK_001")
        ack_understood("TASK_001")
        mark_done("TASK_001")

        assert cleanup_task("TASK_001")

        import scripts.swarm.task_manager as tm
        tasks_path = Path(tm.TASKS_DIR)

        assert not (tasks_path / "TASK_001.ready").exists()
        assert not (tasks_path / "TASK_001.working").exists()
        assert not (tasks_path / "TASK_001.done").exists()
        assert not (tasks_path / "TASK_001.ack_received").exists()
        assert not (tasks_path / "TASK_001.ack_understood").exists()

    def test_cleanup_with_invalid_id_fails(self, temp_tasks_dir):
        """Cleanup con ID invalido deve fallire."""
        assert cleanup_task("../hack") is False

    def test_cleanup_idempotent(self, temp_tasks_dir):
        """Cleanup multipli non devono causare errori."""
        create_task("TASK_001", "worker", "Test")
        mark_done("TASK_001")

        assert cleanup_task("TASK_001")
        assert cleanup_task("TASK_001")


# === EDGE CASES ===


class TestEdgeCases:
    """Test edge cases e scenari limite."""

    def test_concurrent_mark_working_simulation(self, temp_tasks_dir):
        """Simula race condition su mark_working."""
        create_task("TASK_001", "worker", "Test")
        assert mark_working("TASK_001") is True
        assert mark_working("TASK_001") is False

    def test_task_lifecycle_complete(self, temp_tasks_dir):
        """Test ciclo completo task: create -> ready -> working -> done."""
        create_task("TASK_001", "worker", "Test lifecycle")
        assert get_task_status("TASK_001") == "created"

        mark_ready("TASK_001")
        assert get_task_status("TASK_001") == "ready"

        mark_working("TASK_001")
        assert get_task_status("TASK_001") == "working"

        ack_received("TASK_001")
        assert get_ack_status("TASK_001") == "\u2713/-/-"

        ack_understood("TASK_001")
        assert get_ack_status("TASK_001") == "\u2713/\u2713/-"

        mark_done("TASK_001")
        assert get_task_status("TASK_001") == "done"
        assert get_ack_status("TASK_001") == "\u2713/\u2713/\u2713"

    def test_task_with_special_description_chars(self, temp_tasks_dir):
        """Descrizione con caratteri speciali deve funzionare."""
        desc = "Test with 'quotes' and \"double\" and <brackets>"
        task_file = create_task("TASK_001", "worker", desc)
        content = Path(task_file).read_text()
        assert desc in content


# === ERROR HANDLING TESTS ===


class TestErrorHandling:
    """Test error handling e logging."""

    @patch('pathlib.Path.read_text')
    def test_list_tasks_handles_permission_error(self, mock_read, temp_tasks_dir):
        """list_tasks deve gestire PermissionError."""
        create_task("TASK_001", "worker", "Test")
        mock_read.side_effect = PermissionError("No permission")
        tasks = list_tasks()
        assert len(tasks) == 1
        assert tasks[0]['agent'] == "unknown"

    @patch('pathlib.Path.read_text')
    def test_list_tasks_handles_unicode_error(self, mock_read, temp_tasks_dir):
        """list_tasks deve gestire UnicodeDecodeError."""
        create_task("TASK_001", "worker", "Test")
        mock_read.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid')
        tasks = list_tasks()
        assert len(tasks) == 1
        assert tasks[0]['agent'] == "unknown"

    @patch('pathlib.Path.read_text')
    def test_list_tasks_handles_os_error(self, mock_read, temp_tasks_dir):
        """list_tasks deve gestire OSError generico."""
        create_task("TASK_001", "worker", "Test")
        mock_read.side_effect = OSError("Generic error")
        tasks = list_tasks()
        assert len(tasks) == 1
        assert tasks[0]['agent'] == "unknown"

    def test_ensure_tasks_dir_handles_os_error(self):
        """ensure_tasks_dir deve sollevare OSError se creazione fallisce."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.side_effect = OSError("Disk full")
            with pytest.raises(OSError):
                ensure_tasks_dir()


# === CLI INTEGRATION TESTS ===


class TestCLIIntegration:
    """Test CLI interface."""

    def _run_cli(self, args):
        """Helper per eseguire CLI con sys.argv mock."""
        import subprocess
        module_path = Path(__file__).parent.parent.parent / "scripts" / "swarm" / "task_manager.py"
        result = subprocess.run(
            ["python3", str(module_path)] + args,
            capture_output=True,
            text=True
        )
        return result

    def test_cli_help(self):
        """CLI --help deve mostrare usage."""
        result = self._run_cli(["--help"])
        assert result.returncode == 0
        assert "Task Manager" in result.stdout

    def test_cli_version(self):
        """CLI --version deve mostrare versione."""
        result = self._run_cli(["--version"])
        assert result.returncode == 0
        assert "task_manager.py v" in result.stdout

    def test_cli_no_args_shows_help(self):
        """CLI senza argomenti deve mostrare help."""
        result = self._run_cli([])
        assert result.returncode == 1
        assert "Usage:" in result.stdout

    def test_cli_unknown_command(self):
        """CLI con comando sconosciuto deve fallire."""
        result = self._run_cli(["unknown_command"])
        assert result.returncode == 1
        assert "Comando sconosciuto" in result.stdout

    def test_cli_create_missing_args(self):
        """CLI create senza abbastanza argomenti deve fallire."""
        result = self._run_cli(["create", "TASK_001"])
        assert result.returncode == 1
        assert "Uso: task_manager.py create" in result.stdout

    def test_cli_status_missing_args(self):
        """CLI status senza task_id deve fallire."""
        result = self._run_cli(["status"])
        assert result.returncode == 1
        assert "Uso:" in result.stdout


# === ACK INVALID TASK ID ===


class TestAckInvalidTaskId:
    """Test ack_received e ack_understood con task_id invalido."""

    def test_ack_received_invalid_task_id(self, temp_tasks_dir):
        """ack_received con task_id invalido ritorna False."""
        with patch('scripts.swarm.task_manager.TASKS_DIR', str(temp_tasks_dir)):
            assert ack_received("../../../etc/passwd") is False

    def test_ack_understood_invalid_task_id(self, temp_tasks_dir):
        """ack_understood con task_id invalido ritorna False."""
        with patch('scripts.swarm.task_manager.TASKS_DIR', str(temp_tasks_dir)):
            assert ack_understood("INVALID ID WITH SPACES") is False
