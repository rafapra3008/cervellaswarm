"""
Test per scripts/swarm/dashboard/data.py - Extended

Coverage: get_stuck_workers, get_live_activity_from_heartbeat, get_task_description.
Split da test_dashboard_data.py per rispettare limite 500 righe.
"""

import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest

from scripts.swarm.dashboard.data import (
    get_stuck_workers,
    get_live_activity_from_heartbeat,
    get_task_description,
    get_system_resources,
)


# ========== FIXTURES ==========

@pytest.fixture
def temp_tasks_dir(tmp_path):
    """Crea directory temporanea per task."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    return tasks_dir


@pytest.fixture
def temp_status_dir(tmp_path):
    """Crea directory temporanea per status (heartbeat)."""
    status_dir = tmp_path / ".swarm" / "status"
    status_dir.mkdir(parents=True)
    return status_dir


# ========== get_stuck_workers ==========

def test_get_stuck_workers(temp_status_dir):
    """Test identificazione worker stuck."""
    now = int(time.time())
    stuck_hb = temp_status_dir / "heartbeat_cervella-backend.log"
    stuck_hb.write_text(f"{now - 600}|TASK_001|Processing...")
    active_hb = temp_status_dir / "heartbeat_cervella-frontend.log"
    active_hb.write_text(f"{now - 60}|TASK_002|Working...")
    idle_hb = temp_status_dir / "heartbeat_cervella-tester.log"
    idle_hb.write_text(f"{now - 600}|-|Idle...")

    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True
        mock_status.glob.return_value = [stuck_hb, active_hb, idle_hb]
        mock_path.return_value = mock_status

        stuck = get_stuck_workers(threshold_sec=300)
        assert len(stuck) == 1
        assert stuck[0]['worker'] == 'cervella-backend'
        assert stuck[0]['last_seen_sec'] >= 600


def test_get_stuck_workers_empty_dir():
    """Test con directory status vuota."""
    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = False
        mock_path.return_value = mock_status
        stuck = get_stuck_workers()
        assert len(stuck) == 0


def test_get_stuck_workers_invalid_format(temp_status_dir):
    """Test con heartbeat file formato invalido."""
    bad_hb = temp_status_dir / "heartbeat_cervella-bad.log"
    bad_hb.write_text("invalid format")

    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True
        mock_status.glob.return_value = [bad_hb]
        mock_path.return_value = mock_status
        stuck = get_stuck_workers()
        assert len(stuck) == 0


def test_get_stuck_workers_empty_content(temp_status_dir):
    """Test skip empty heartbeat content (line 350)."""
    empty_hb = temp_status_dir / "heartbeat_cervella-empty.log"
    empty_hb.write_text("")

    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True
        mock_status.glob.return_value = [empty_hb]
        mock_path.return_value = mock_status
        stuck = get_stuck_workers()
        assert len(stuck) == 0


def test_get_stuck_workers_exception(temp_status_dir):
    """Test continue on exception (lines 369-370)."""
    bad_hb = temp_status_dir / "heartbeat_cervella-error.log"
    bad_hb.write_text("some content")

    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True

        mock_bad_file = MagicMock()
        mock_bad_file.read_text.side_effect = Exception("Read error")
        mock_status.glob.return_value = [mock_bad_file]
        mock_path.return_value = mock_status

        stuck = get_stuck_workers()
        assert len(stuck) == 0


# ========== get_live_activity_from_heartbeat ==========

def test_get_live_activity_from_heartbeat(temp_status_dir):
    """Test lettura live activity da heartbeat."""
    now = int(time.time())
    active_hb = temp_status_dir / "heartbeat_cervella-backend.log"
    active_hb.write_text(f"{now - 30}|TASK_001|Processing...")
    stale_hb = temp_status_dir / "heartbeat_cervella-frontend.log"
    stale_hb.write_text(f"{now - 200}|TASK_002|Working...")

    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True
        mock_status.glob.return_value = [active_hb, stale_hb]
        mock_path.return_value = mock_status

        activities = get_live_activity_from_heartbeat()
        assert len(activities) == 2
        backend = [a for a in activities if a['worker'] == 'cervella-backend'][0]
        assert backend['is_active'] is True
        frontend = [a for a in activities if a['worker'] == 'cervella-frontend'][0]
        assert frontend['is_active'] is False


def test_get_live_activity_empty():
    """Test con nessun heartbeat."""
    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = False
        mock_path.return_value = mock_status
        activities = get_live_activity_from_heartbeat()
        assert len(activities) == 0


def test_get_live_activity_empty_content(temp_status_dir):
    """Test skip empty content (line 392)."""
    empty_hb = temp_status_dir / "heartbeat_cervella-empty.log"
    empty_hb.write_text("")

    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True
        mock_status.glob.return_value = [empty_hb]
        mock_path.return_value = mock_status

        activities = get_live_activity_from_heartbeat()
        assert len(activities) == 0


def test_get_live_activity_exception(temp_status_dir):
    """Test continue on exception (lines 414-415)."""
    with patch('scripts.swarm.dashboard.data.Path') as mock_path:
        mock_status = MagicMock()
        mock_status.exists.return_value = True

        mock_bad_file = MagicMock()
        mock_bad_file.read_text.side_effect = Exception("Read error")
        mock_status.glob.return_value = [mock_bad_file]
        mock_path.return_value = mock_status

        activities = get_live_activity_from_heartbeat()
        assert len(activities) == 0


# ========== get_task_description ==========

def test_get_task_description(temp_tasks_dir):
    """Test estrazione descrizione da file task."""
    task_file = temp_tasks_dir / "TASK_001.md"
    task_file.write_text("# TASK: Write tests for dashboard module\n\n## Details\n...")
    with patch('scripts.swarm.dashboard.data.TASKS_DIR', str(temp_tasks_dir)):
        desc = get_task_description('TASK_001')
        assert desc == "Write tests for dashboard module"


def test_get_task_description_truncation(temp_tasks_dir):
    """Test troncamento descrizione > 40 caratteri."""
    task_file = temp_tasks_dir / "TASK_002.md"
    long_desc = "This is a very long task description that exceeds forty characters"
    task_file.write_text(f"# TASK: {long_desc}\n")
    with patch('scripts.swarm.dashboard.data.TASKS_DIR', str(temp_tasks_dir)):
        desc = get_task_description('TASK_002')
        assert len(desc) <= 40
        assert desc.endswith('...')


def test_get_task_description_missing_file(temp_tasks_dir):
    """Test con file task mancante."""
    with patch('scripts.swarm.dashboard.data.TASKS_DIR', str(temp_tasks_dir)):
        desc = get_task_description('TASK_999')
        assert desc == "Unknown task"


def test_get_task_description_no_header(temp_tasks_dir):
    """Test con file senza header '# TASK:'."""
    task_file = temp_tasks_dir / "TASK_003.md"
    task_file.write_text("Some content without proper header")
    with patch('scripts.swarm.dashboard.data.TASKS_DIR', str(temp_tasks_dir)):
        desc = get_task_description('TASK_003')
        assert desc == "No description"


def test_get_task_description_exception(temp_tasks_dir):
    """Test exception handler in read_task_description (lines 100-101)."""
    task_file = temp_tasks_dir / "TASK_999.md"
    task_file.write_text("content")

    with patch('scripts.swarm.dashboard.data.TASKS_DIR', str(temp_tasks_dir)):
        original_read_text = Path.read_text
        def mock_read_text(self, *args, **kwargs):
            if self.name == "TASK_999.md":
                raise IOError("Read error")
            return original_read_text(self, *args, **kwargs)

        with patch('pathlib.Path.read_text', mock_read_text):
            desc = get_task_description('TASK_999')
            assert desc == "Error reading task"


# ========== get_system_resources - psutil branch ==========

def test_get_system_resources_psutil_available():
    """Test get_system_resources con psutil disponibile (lines 248-258)."""
    mock_mem = MagicMock()
    mock_mem.used = 8 * (1024**3)  # 8 GB
    mock_mem.total = 16 * (1024**3)  # 16 GB
    mock_mem.percent = 50.0

    mock_psutil = MagicMock()
    mock_psutil.cpu_percent.return_value = 25.0
    mock_psutil.virtual_memory.return_value = mock_mem

    with patch('scripts.swarm.dashboard.data.PSUTIL_AVAILABLE', True), \
         patch('scripts.swarm.dashboard.data.psutil', mock_psutil, create=True):
        result = get_system_resources()

    assert result['cpu_percent'] == 25.0
    assert result['memory_used_gb'] == pytest.approx(8.0)
    assert result['memory_total_gb'] == pytest.approx(16.0)
    assert result['memory_percent'] == 50.0


def test_get_system_resources_psutil_exception():
    """Test get_system_resources fallback quando psutil lancia eccezione."""
    mock_psutil = MagicMock()
    mock_psutil.cpu_percent.side_effect = RuntimeError("psutil error")

    with patch('scripts.swarm.dashboard.data.PSUTIL_AVAILABLE', True), \
         patch('scripts.swarm.dashboard.data.psutil', mock_psutil, create=True), \
         patch('subprocess.check_output', side_effect=Exception("no shell")):
        result = get_system_resources()

    # Fallback returns zeros on all failures
    assert 'cpu_percent' in result
    assert result['cpu_percent'] == 0
