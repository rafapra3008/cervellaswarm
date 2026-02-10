"""
Test per CervellaSwarm Task Manager (CORE)

Validazione, directory, creazione task, marker files.

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
    mark_ready,
    mark_working,
    ack_received,
    ack_understood,
    mark_done,
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
            "a" * 50,
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
        assert not validate_task_id("")
        assert not validate_task_id("a" * 51)

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
        tasks_path = ensure_tasks_dir()
        assert tasks_path.exists()
        assert tasks_path.is_dir()

    def test_idempotent(self, temp_tasks_dir):
        """Chiamate multiple non devono causare errori."""
        ensure_tasks_dir()
        ensure_tasks_dir()
        ensure_tasks_dir()

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
        task_file = create_task("TASK_001", "worker", "Low risk", risk_level=1)
        content = Path(task_file).read_text()
        assert "BASSO - nuovo file" in content

        task_file = create_task("TASK_002", "worker", "Medium risk", risk_level=2)
        content = Path(task_file).read_text()
        assert "MEDIO - modifica file esistente" in content

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
        assert mark_working("TASK_001") is True
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
