"""
Test per CervellaSwarm Task Manager.

Verifica tutte le funzionalità del task_manager.py:
- Validazione task_id (security)
- Creazione task
- Marker files (ready, working, done, ack)
- Race condition handling (mark_working atomico)
- Lista task
- Cleanup

Sessione 341 - Test Suite Task Manager
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Setup path
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

    # Patch TASKS_DIR nel modulo
    import scripts.swarm.task_manager as tm
    tm.TASKS_DIR = f"{temp_dir}/.swarm/tasks"

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    tm.TASKS_DIR = original_tasks_dir


# === VALIDATION TESTS ===


class TestValidateTaskId:
    """Test validazione task_id per sicurezza."""

    def test_valid_task_ids(self):
        """Task ID validi devono passare."""
        valid_ids = [
            "TASK_001",
            "TASK-123",
            "Task_ABC",
            "task-001-frontend",
            "T1",
            "a" * 50,  # max lunghezza
        ]
        for task_id in valid_ids:
            assert validate_task_id(task_id), f"Dovrebbe essere valido: {task_id}"

    def test_invalid_task_ids_path_traversal(self):
        """Path traversal deve essere bloccato."""
        dangerous_ids = [
            "../etc/passwd",
            "../../secret",
            "task/../../../etc",
            "TASK_001/../hack",
        ]
        for task_id in dangerous_ids:
            assert not validate_task_id(task_id), f"Dovrebbe essere BLOCCATO: {task_id}"

    def test_invalid_task_ids_special_chars(self):
        """Caratteri speciali pericolosi devono essere bloccati."""
        dangerous_ids = [
            "task;rm -rf /",
            "task|cat /etc/passwd",
            "task&whoami",
            "task$USER",
            "TASK_001/hack",
            "TASK_001\\hack",
        ]
        for task_id in dangerous_ids:
            assert not validate_task_id(task_id), f"Dovrebbe essere BLOCCATO: {task_id}"

    def test_invalid_task_ids_length(self):
        """Task ID troppo lunghi devono essere bloccati."""
        assert not validate_task_id("")  # vuoto
        assert not validate_task_id("a" * 51)  # troppo lungo

    def test_invalid_task_ids_spaces(self):
        """Spazi non sono permessi."""
        assert not validate_task_id("TASK 001")
        assert not validate_task_id("TASK_001 ")
        assert not validate_task_id(" TASK_001")


# === DIRECTORY TESTS ===


class TestEnsureTasksDir:
    """Test creazione directory tasks."""

    def test_creates_directory(self, temp_tasks_dir):
        """Deve creare la directory se non esiste."""
        import scripts.swarm.task_manager as tm
        tasks_path = ensure_tasks_dir()
        assert tasks_path.exists()
        assert tasks_path.is_dir()

    def test_idempotent(self, temp_tasks_dir):
        """Chiamate multiple non devono causare errori."""
        ensure_tasks_dir()
        ensure_tasks_dir()
        ensure_tasks_dir()
        # Non deve sollevare eccezioni

    @patch('pathlib.Path.mkdir')
    def test_permission_error(self, mock_mkdir):
        """Deve sollevare PermissionError se mancano i permessi."""
        mock_mkdir.side_effect = PermissionError("No permission")
        with pytest.raises(PermissionError):
            ensure_tasks_dir()


# === CREATE TASK TESTS ===


class TestCreateTask:
    """Test creazione task."""

    def test_create_basic_task(self, temp_tasks_dir):
        """Crea un task base con successo."""
        task_file = create_task("TASK_001", "cervella-backend", "Test task creation")

        assert Path(task_file).exists()
        content = Path(task_file).read_text()
        assert "TASK_001" in content
        assert "cervella-backend" in content
        assert "Test task creation" in content
        assert "Livello rischio: 1" in content

    def test_create_task_with_risk_levels(self, temp_tasks_dir):
        """Test diversi livelli di rischio."""
        # Risk 1 - basso
        task_file = create_task("TASK_001", "worker", "Low risk", risk_level=1)
        content = Path(task_file).read_text()
        assert "BASSO - nuovo file" in content

        # Risk 2 - medio
        task_file = create_task("TASK_002", "worker", "Medium risk", risk_level=2)
        content = Path(task_file).read_text()
        assert "MEDIO - modifica file esistente" in content

        # Risk 3 - alto
        task_file = create_task("TASK_003", "worker", "High risk", risk_level=3)
        content = Path(task_file).read_text()
        assert "ALTO - sistema critico" in content

    def test_create_duplicate_task_fails(self, temp_tasks_dir):
        """Non deve permettere duplicati."""
        create_task("TASK_001", "worker", "First")

        with pytest.raises(FileExistsError, match="già esiste"):
            create_task("TASK_001", "worker", "Second")

    def test_create_with_invalid_id_fails(self, temp_tasks_dir):
        """Task ID invalidi devono fallire."""
        with pytest.raises(ValueError, match="non valido"):
            create_task("../etc/passwd", "worker", "Hack attempt")

    def test_task_has_timestamp(self, temp_tasks_dir):
        """Task deve contenere timestamp di creazione."""
        task_file = create_task("TASK_001", "worker", "Test")
        content = Path(task_file).read_text()

        # Verifica formato data
        assert "Creato: 2026-" in content or "Creato: 2025-" in content

    def test_task_has_required_sections(self, temp_tasks_dir):
        """Task deve avere tutte le sezioni richieste."""
        task_file = create_task("TASK_001", "worker", "Test")
        content = Path(task_file).read_text()

        required_sections = [
            "## METADATA",
            "## PERCHE",
            "## CRITERI DI SUCCESSO",
            "## FILE DA MODIFICARE",
            "## CHI VERIFICHERA",
            "## DETTAGLI",
        ]
        for section in required_sections:
            assert section in content, f"Mancante: {section}"


# === MARKER FILES TESTS ===


class TestMarkerFiles:
    """Test gestione marker files (.ready, .working, .done, .ack)."""

    def test_mark_ready(self, temp_tasks_dir):
        """Segna task come ready."""
        create_task("TASK_001", "worker", "Test")
        assert mark_ready("TASK_001")

        import scripts.swarm.task_manager as tm
        ready_file = Path(tm.TASKS_DIR) / "TASK_001.ready"
        assert ready_file.exists()

    def test_mark_working(self, temp_tasks_dir):
        """Segna task come working."""
        create_task("TASK_001", "worker", "Test")
        assert mark_working("TASK_001")

        import scripts.swarm.task_manager as tm
        working_file = Path(tm.TASKS_DIR) / "TASK_001.working"
        assert working_file.exists()

    def test_mark_working_is_atomic(self, temp_tasks_dir):
        """mark_working deve essere atomico (race condition safe)."""
        create_task("TASK_001", "worker", "Test")

        # Primo worker prende il task
        assert mark_working("TASK_001") is True

        # Secondo worker NON deve poterlo prendere
        assert mark_working("TASK_001") is False

    def test_mark_working_writes_timestamp(self, temp_tasks_dir):
        """mark_working deve scrivere timestamp nel file."""
        create_task("TASK_001", "worker", "Test")
        mark_working("TASK_001")

        import scripts.swarm.task_manager as tm
        working_file = Path(tm.TASKS_DIR) / "TASK_001.working"
        content = working_file.read_text()
        assert "started:" in content

    def test_ack_received(self, temp_tasks_dir):
        """Segna ACK_RECEIVED."""
        create_task("TASK_001", "worker", "Test")
        assert ack_received("TASK_001")

        import scripts.swarm.task_manager as tm
        ack_file = Path(tm.TASKS_DIR) / "TASK_001.ack_received"
        assert ack_file.exists()

    def test_ack_understood(self, temp_tasks_dir):
        """Segna ACK_UNDERSTOOD."""
        create_task("TASK_001", "worker", "Test")
        assert ack_understood("TASK_001")

        import scripts.swarm.task_manager as tm
        ack_file = Path(tm.TASKS_DIR) / "TASK_001.ack_understood"
        assert ack_file.exists()

    def test_mark_done(self, temp_tasks_dir):
        """Segna task come done."""
        create_task("TASK_001", "worker", "Test")
        assert mark_done("TASK_001")

        import scripts.swarm.task_manager as tm
        done_file = Path(tm.TASKS_DIR) / "TASK_001.done"
        assert done_file.exists()

    def test_mark_nonexistent_task_fails(self, temp_tasks_dir):
        """Operazioni su task inesistente devono fallire."""
        assert mark_ready("NONEXISTENT") is False
        assert mark_working("NONEXISTENT") is False
        assert mark_done("NONEXISTENT") is False
        assert ack_received("NONEXISTENT") is False
        assert ack_understood("NONEXISTENT") is False

    def test_mark_with_invalid_id_fails(self, temp_tasks_dir):
        """Operazioni con ID invalido devono fallire."""
        assert mark_ready("../hack") is False
        assert mark_working("../hack") is False
        assert mark_done("../hack") is False


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
        """Status 'done' ha priorità su 'working'."""
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
        """Solo ACK_RECEIVED = ✓/-/-"""
        create_task("TASK_001", "worker", "Test")
        ack_received("TASK_001")
        assert get_ack_status("TASK_001") == "✓/-/-"

    def test_ack_received_and_understood(self, temp_tasks_dir):
        """ACK_RECEIVED + ACK_UNDERSTOOD = ✓/✓/-"""
        create_task("TASK_001", "worker", "Test")
        ack_received("TASK_001")
        ack_understood("TASK_001")
        assert get_ack_status("TASK_001") == "✓/✓/-"

    def test_ack_all_complete(self, temp_tasks_dir):
        """Tutti gli ACK = ✓/✓/✓"""
        create_task("TASK_001", "worker", "Test")
        ack_received("TASK_001")
        ack_understood("TASK_001")
        mark_done("TASK_001")
        assert get_ack_status("TASK_001") == "✓/✓/✓"

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

        # Verifica ordinamento
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
        """Lista task anche se metadata è corrotto."""
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

        # Verifica che nessun marker esista più
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
        assert cleanup_task("TASK_001")  # Secondo cleanup = OK


# === EDGE CASES ===


class TestEdgeCases:
    """Test edge cases e scenari limite."""

    def test_concurrent_mark_working_simulation(self, temp_tasks_dir):
        """Simula race condition su mark_working."""
        create_task("TASK_001", "worker", "Test")

        # Primo worker vince
        result1 = mark_working("TASK_001")
        assert result1 is True

        # Secondo worker perde
        result2 = mark_working("TASK_001")
        assert result2 is False

    def test_task_lifecycle_complete(self, temp_tasks_dir):
        """Test ciclo completo task: create → ready → working → done."""
        # Create
        create_task("TASK_001", "worker", "Test lifecycle")
        assert get_task_status("TASK_001") == "created"

        # Ready
        mark_ready("TASK_001")
        assert get_task_status("TASK_001") == "ready"

        # Working
        mark_working("TASK_001")
        assert get_task_status("TASK_001") == "working"

        # ACK flow
        ack_received("TASK_001")
        assert get_ack_status("TASK_001") == "✓/-/-"

        ack_understood("TASK_001")
        assert get_ack_status("TASK_001") == "✓/✓/-"

        # Done
        mark_done("TASK_001")
        assert get_task_status("TASK_001") == "done"
        assert get_ack_status("TASK_001") == "✓/✓/✓"

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

        # Non deve crashare
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
        import scripts.swarm.task_manager as tm

        # Path al modulo
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
        assert "Usage:" in result.stdout

    def test_cli_version(self):
        """CLI --version deve mostrare versione."""
        result = self._run_cli(["--version"])
        assert result.returncode == 0
        assert "task_manager.py v" in result.stdout

    def test_cli_no_args_shows_help(self):
        """CLI senza argomenti deve mostrare help ed uscire con 1."""
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
