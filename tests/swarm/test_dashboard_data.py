#!/usr/bin/env python3
"""
Test suite per scripts/swarm/dashboard/data.py

Coverage: get_worker_status, get_task_queue_stats, get_recent_activity,
calculate_session_duration, get_system_resources, get_stuck_workers,
get_live_activity_from_heartbeat, get_task_description

Split da test_dashboard_cli.py (934 righe > limite 500).
Sessione 341.
"""

import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest

from scripts.swarm.dashboard.data import (
    get_worker_status,
    get_task_queue_stats,
    get_recent_activity,
    calculate_session_duration,
    get_system_resources,
    get_stuck_workers,
    get_live_activity_from_heartbeat,
    get_task_description,
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


@pytest.fixture
def sample_tasks():
    """Sample task list per testing."""
    return [
        {'task_id': 'TASK_001', 'agent': 'cervella-backend', 'status': 'working', 'created_at': 1700000000},
        {'task_id': 'TASK_002', 'agent': 'cervella-frontend', 'status': 'ready', 'created_at': 1700000100},
        {'task_id': 'TASK_003', 'agent': 'cervella-tester', 'status': 'done', 'created_at': 1700000200},
        {'task_id': 'TASK_004', 'agent': 'cervella-backend', 'status': 'created', 'created_at': 1700000300},
    ]


# ========== get_worker_status ==========

def test_get_worker_status_active(sample_tasks):
    """Test worker con task 'working' (ACTIVE)."""
    status = get_worker_status('cervella-backend', sample_tasks)
    assert status['status'] == 'active'
    assert 'TASK_001' in status['current_task']
    assert status['task_count'] == 2


def test_get_worker_status_ready(sample_tasks):
    """Test worker con task 'ready' (READY)."""
    status = get_worker_status('cervella-frontend', sample_tasks)
    assert status['status'] == 'ready'
    assert '1 task pending' in status['current_task']
    assert status['task_count'] == 1


def test_get_worker_status_idle(sample_tasks):
    """Test worker senza task (IDLE)."""
    status = get_worker_status('cervella-researcher', sample_tasks)
    assert status['status'] == 'idle'
    assert status['current_task'] == '-'
    assert status['task_count'] == 0


def test_get_worker_status_done_only(sample_tasks):
    """Test worker con solo task 'done' (IDLE)."""
    status = get_worker_status('cervella-tester', sample_tasks)
    assert status['status'] == 'idle'
    assert status['current_task'] == '-'
    assert status['task_count'] == 1


# ========== get_task_queue_stats ==========

def test_get_task_queue_stats(sample_tasks):
    """Test calcolo stats task queue."""
    stats = get_task_queue_stats(sample_tasks)
    assert stats['pending'] == 1
    assert stats['ready'] == 1
    assert stats['in_progress'] == 1
    assert stats['completed'] == 1
    assert stats['failed'] == 0


def test_get_task_queue_stats_empty():
    """Test stats con lista vuota."""
    stats = get_task_queue_stats([])
    assert stats['pending'] == 0
    assert stats['ready'] == 0
    assert stats['in_progress'] == 0
    assert stats['completed'] == 0
    assert stats['failed'] == 0


def test_get_task_queue_stats_all_done():
    """Test stats con tutti task done."""
    tasks = [
        {'task_id': 'TASK_001', 'agent': 'cervella-backend', 'status': 'done'},
        {'task_id': 'TASK_002', 'agent': 'cervella-frontend', 'status': 'done'},
    ]
    stats = get_task_queue_stats(tasks)
    assert stats['completed'] == 2
    assert stats['pending'] == 0
    assert stats['in_progress'] == 0


# ========== get_recent_activity ==========

@patch('scripts.swarm.dashboard.data.Path')
def test_get_recent_activity(mock_path_cls, temp_tasks_dir, sample_tasks):
    """Test estrazione recent activity."""
    mock_tasks_path = MagicMock()
    mock_path_cls.return_value = mock_tasks_path

    now = time.time()
    done_file = MagicMock()
    done_file.stem = "TASK_001"
    done_file.suffix = ".done"
    done_file.stat.return_value.st_mtime = now - 10

    working_file = MagicMock()
    working_file.stem = "TASK_002"
    working_file.suffix = ".working"
    working_file.stat.return_value.st_mtime = now - 5

    mock_tasks_path.glob.return_value = [done_file, working_file]
    activities = get_recent_activity(sample_tasks, limit=5)

    assert len(activities) <= 5
    if len(activities) > 1:
        assert activities[0]['timestamp'] >= activities[1]['timestamp']


@patch('scripts.swarm.dashboard.data.Path')
def test_get_recent_activity_empty(mock_path_cls, sample_tasks):
    """Test recent activity con nessun marker file."""
    mock_tasks_path = MagicMock()
    mock_path_cls.return_value = mock_tasks_path
    mock_tasks_path.glob.return_value = []
    activities = get_recent_activity(sample_tasks, limit=5)
    assert len(activities) == 0


@patch('scripts.swarm.dashboard.data.Path')
def test_get_recent_activity_limit(mock_path_cls, temp_tasks_dir, sample_tasks):
    """Test limit parameter."""
    mock_tasks_path = MagicMock()
    mock_path_cls.return_value = mock_tasks_path

    files = []
    for i in range(10):
        f = temp_tasks_dir / f"TASK_{i:03d}.done"
        f.touch()
        files.append(f)

    mock_tasks_path.glob.return_value = files
    activities = get_recent_activity(sample_tasks, limit=3)
    assert len(activities) == 3


# ========== calculate_session_duration ==========

@patch('scripts.swarm.dashboard.data.Path')
@patch('time.time')
def test_calculate_session_duration_from_file(mock_time, mock_path_cls):
    """Test durata da session_start file."""
    mock_time.return_value = 1700001000
    mock_session_file = MagicMock()
    mock_session_file.exists.return_value = True
    mock_session_file.read_text.return_value = "1700000000"
    mock_path_cls.return_value = mock_session_file

    duration = calculate_session_duration()
    assert duration == "16m"


@patch('scripts.swarm.dashboard.data.Path')
@patch('time.time')
def test_calculate_session_duration_hours(mock_time, mock_path_cls):
    """Test durata con ore."""
    mock_time.return_value = 1700010000
    mock_session_file = MagicMock()
    mock_session_file.exists.return_value = True
    mock_session_file.read_text.return_value = "1700000000"
    mock_path_cls.return_value = mock_session_file

    duration = calculate_session_duration()
    assert "h" in duration
    assert "m" in duration


@patch('scripts.swarm.dashboard.data.Path')
def test_calculate_session_duration_no_file(mock_path_cls):
    """Test senza session_start file."""
    mock_session_file = MagicMock()
    mock_session_file.exists.return_value = False
    mock_status_dir = MagicMock()
    mock_status_dir.exists.return_value = False
    mock_path_cls.side_effect = [mock_session_file, mock_status_dir]

    duration = calculate_session_duration()
    assert duration == "N/A"


# ========== get_system_resources ==========

def test_get_system_resources_with_psutil():
    """Test risorse di sistema (struttura valida)."""
    resources = get_system_resources()
    assert isinstance(resources, dict)
    assert 'cpu_percent' in resources
    assert 'memory_used_gb' in resources
    assert 'memory_total_gb' in resources
    assert 'memory_percent' in resources
    assert isinstance(resources['cpu_percent'], float)
    assert resources['cpu_percent'] >= 0.0


@patch('scripts.swarm.dashboard.data.PSUTIL_AVAILABLE', False)
@patch('subprocess.check_output')
def test_get_system_resources_without_psutil(mock_subprocess):
    """Test senza psutil (fallback a shell commands)."""
    top_output = "Processes: 500\nCPU usage: 12.5% user, 5.5% sys, 82.0% idle\n"
    vm_output = "Pages free: 1000000\nPages active: 2000000\nPages inactive: 500000\nPages wired down: 1000000\n"
    mock_subprocess.side_effect = [top_output.encode(), vm_output.encode()]

    resources = get_system_resources()
    assert resources['cpu_percent'] > 0
    assert resources['memory_used_gb'] > 0
    assert resources['memory_total_gb'] > 0


@patch('scripts.swarm.dashboard.data.PSUTIL_AVAILABLE', False)
@patch('subprocess.check_output')
def test_get_system_resources_fallback_error(mock_subprocess):
    """Test fallback quando subprocess fallisce."""
    mock_subprocess.side_effect = Exception("Command failed")
    resources = get_system_resources()
    assert resources['cpu_percent'] == 0.0
    assert resources['memory_used_gb'] == 0.0
    assert resources['memory_total_gb'] == 0.0
    assert resources['memory_percent'] == 0.0


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
