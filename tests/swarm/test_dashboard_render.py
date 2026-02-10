#!/usr/bin/env python3
"""
Test suite per scripts/swarm/dashboard/render.py + cli.py

Coverage: render_header, render_workers, render_stats, render_activity,
render_resources, render_alerts, render_heartbeat, render_footer,
render_dashboard, render_json, clear_screen, main

Split da test_dashboard_cli.py (934 righe > limite 500).
Sessione 341.
"""

import sys
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest

from scripts.swarm.dashboard.render import (
    render_header,
    render_workers,
    render_stats,
    render_activity,
    render_resources,
    render_alerts,
    render_heartbeat,
    render_footer,
    render_dashboard,
    render_json,
    WORKERS,
)


# ========== FIXTURES ==========

@pytest.fixture
def sample_tasks():
    """Sample task list per testing."""
    return [
        {'task_id': 'TASK_001', 'agent': 'cervella-backend', 'status': 'working', 'created_at': 1700000000},
        {'task_id': 'TASK_002', 'agent': 'cervella-frontend', 'status': 'ready', 'created_at': 1700000100},
        {'task_id': 'TASK_003', 'agent': 'cervella-tester', 'status': 'done', 'created_at': 1700000200},
        {'task_id': 'TASK_004', 'agent': 'cervella-backend', 'status': 'created', 'created_at': 1700000300},
    ]


# ========== render_header ==========

def test_render_header():
    """Test rendering header."""
    header = render_header()
    assert "CERVELLASWARM" in header
    assert "\u2554" in header  # box char
    assert "\u2560" in header


# ========== render_workers ==========

def test_render_workers(sample_tasks):
    """Test rendering workers table."""
    output = render_workers(sample_tasks)
    assert "WORKERS STATUS" in output
    assert "backend" in output
    assert "frontend" in output
    assert "ACTIVE" in output or "IDLE" in output


def test_render_workers_all_idle():
    """Test rendering con tutti worker idle."""
    output = render_workers([])
    assert "WORKERS STATUS" in output
    idle_count = output.count("IDLE")
    assert idle_count == len(WORKERS)


def test_render_workers_shows_16_workers():
    """Test che mostra tutti i 16 worker."""
    output = render_workers([])
    for worker in WORKERS:
        worker_name = worker['name'].replace('cervella-', '')
        assert worker_name in output


# ========== render_stats ==========

def test_render_stats(sample_tasks):
    """Test rendering stats."""
    output = render_stats(sample_tasks)
    assert "TASK QUEUE" in output
    assert "METRICS" in output
    assert "Pending:" in output
    assert "Completed:" in output


def test_render_stats_empty():
    """Test stats con lista vuota."""
    output = render_stats([])
    assert "TASK QUEUE" in output
    assert "0" in output


# ========== render_activity ==========

def test_render_activity(sample_tasks):
    """Test rendering activity."""
    with patch('scripts.swarm.dashboard.render.get_recent_activity') as mock_activity:
        mock_activity.return_value = [
            {'timestamp': time.time(), 'agent': 'backend', 'action': 'Completed', 'task_id': 'TASK_001'}
        ]
        output = render_activity(sample_tasks)
        assert "LAST ACTIVITY" in output
        assert "backend" in output
        assert "TASK_001" in output


def test_render_activity_empty(sample_tasks):
    """Test activity con nessuna attivita."""
    with patch('scripts.swarm.dashboard.render.get_recent_activity') as mock_activity:
        mock_activity.return_value = []
        output = render_activity(sample_tasks)
        assert "LAST ACTIVITY" in output
        assert "No recent activity" in output


# ========== render_resources ==========

def test_render_resources():
    """Test rendering system resources."""
    with patch('scripts.swarm.dashboard.render.get_system_resources') as mock_resources:
        mock_resources.return_value = {
            'cpu_percent': 45.5, 'memory_used_gb': 8.0,
            'memory_total_gb': 16.0, 'memory_percent': 50.0
        }
        output = render_resources()
        assert "SYSTEM RESOURCES" in output
        assert "CPU:" in output
        assert "RAM:" in output


def test_render_resources_na():
    """Test resources quando non disponibili."""
    with patch('scripts.swarm.dashboard.render.get_system_resources') as mock_resources:
        mock_resources.return_value = {
            'cpu_percent': 0.0, 'memory_used_gb': 0.0,
            'memory_total_gb': 0.0, 'memory_percent': 0.0
        }
        output = render_resources()
        assert "N/A" in output


# ========== render_alerts ==========

def test_render_alerts_with_stuck():
    """Test alerts con worker stuck."""
    with patch('scripts.swarm.dashboard.render.get_stuck_workers') as mock_stuck:
        mock_stuck.return_value = [{'worker': 'backend', 'last_seen_sec': 600, 'last_task': 'TASK_001'}]
        output = render_alerts()
        assert "ALERTS" in output
        assert "stuck" in output
        assert "backend" in output


def test_render_alerts_empty():
    """Test alerts senza worker stuck."""
    with patch('scripts.swarm.dashboard.render.get_stuck_workers') as mock_stuck:
        mock_stuck.return_value = []
        output = render_alerts()
        assert output == ""


# ========== render_heartbeat ==========

def test_render_heartbeat():
    """Test rendering heartbeat live."""
    with patch('scripts.swarm.dashboard.render.get_live_activity_from_heartbeat') as mock_hb:
        mock_hb.return_value = [
            {'worker': 'backend', 'timestamp': time.time(), 'task': 'TASK_001',
             'action': 'Processing...', 'age': 30, 'is_active': True}
        ]
        output = render_heartbeat()
        assert "LIVE HEARTBEAT" in output
        assert "backend" in output
        assert "ACTIVE" in output


def test_render_heartbeat_empty():
    """Test heartbeat senza worker attivi."""
    with patch('scripts.swarm.dashboard.render.get_live_activity_from_heartbeat') as mock_hb:
        mock_hb.return_value = []
        output = render_heartbeat()
        assert "LIVE HEARTBEAT" in output
        assert "Nessun heartbeat" in output


# ========== render_footer ==========

def test_render_footer():
    """Test rendering footer."""
    footer = render_footer()
    assert "\u255a" in footer  # box char


# ========== render_dashboard ==========

def test_render_dashboard(sample_tasks):
    """Test rendering dashboard completa."""
    output = render_dashboard(sample_tasks)
    assert "CERVELLASWARM" in output
    assert "WORKERS STATUS" in output
    assert "TASK QUEUE" in output
    assert "SYSTEM RESOURCES" in output
    assert "LIVE HEARTBEAT" in output
    assert "LAST ACTIVITY" in output
    assert "\u2554" in output
    assert "\u255a" in output


def test_render_dashboard_with_alerts(sample_tasks):
    """Test dashboard con alerts."""
    with patch('scripts.swarm.dashboard.render.get_stuck_workers') as mock_stuck:
        mock_stuck.return_value = [{'worker': 'backend', 'last_seen_sec': 600, 'last_task': 'TASK_001'}]
        output = render_dashboard(sample_tasks)
        assert "ALERTS" in output


def test_render_dashboard_no_alerts(sample_tasks):
    """Test dashboard senza alerts."""
    with patch('scripts.swarm.dashboard.render.get_stuck_workers') as mock_stuck:
        mock_stuck.return_value = []
        output = render_dashboard(sample_tasks)
        assert output.count("ALERTS") == 0


# ========== render_json ==========

def test_render_json(sample_tasks):
    """Test rendering JSON output."""
    output = render_json(sample_tasks)
    data = json.loads(output)
    assert 'timestamp' in data
    assert 'workers' in data
    assert 'queue_stats' in data
    assert 'system_resources' in data
    assert 'session_duration' in data
    assert 'stuck_workers' in data
    assert 'recent_activity' in data


def test_render_json_workers_list(sample_tasks):
    """Test JSON contiene lista workers."""
    output = render_json(sample_tasks)
    data = json.loads(output)
    assert len(data['workers']) == len(WORKERS)
    worker = data['workers'][0]
    assert 'name' in worker
    assert 'emoji' in worker
    assert 'type' in worker
    assert 'status' in worker


def test_render_json_queue_stats(sample_tasks):
    """Test JSON contiene queue stats."""
    output = render_json(sample_tasks)
    data = json.loads(output)
    stats = data['queue_stats']
    assert 'pending' in stats
    assert 'ready' in stats
    assert 'in_progress' in stats
    assert 'completed' in stats


def test_render_json_pretty_format(sample_tasks):
    """Test JSON formattato (indent=2)."""
    output = render_json(sample_tasks)
    assert '\n' in output
    assert '  ' in output


# ========== cli.py - clear_screen ==========

def test_clear_screen(capsys):
    """Test clear screen function."""
    from scripts.swarm.dashboard.cli import clear_screen
    clear_screen()
    captured = capsys.readouterr()
    assert '\033[2J' in captured.out
    assert '\033[H' in captured.out


# ========== cli.py - main ==========

@patch('scripts.swarm.dashboard.cli.list_tasks')
@patch('scripts.swarm.dashboard.cli.render_dashboard')
def test_cli_main_single_shot(mock_render, mock_list_tasks, capsys):
    """Test CLI main in single shot mode."""
    from scripts.swarm.dashboard.cli import main
    mock_list_tasks.return_value = []
    mock_render.return_value = "Dashboard output"
    with patch('sys.argv', ['cli.py']):
        try:
            main()
        except SystemExit:
            pass
    captured = capsys.readouterr()
    assert "Dashboard output" in captured.out


@patch('scripts.swarm.dashboard.cli.list_tasks')
@patch('scripts.swarm.dashboard.cli.render_json')
def test_cli_main_json_output(mock_render, mock_list_tasks, capsys):
    """Test CLI main con --json flag."""
    from scripts.swarm.dashboard.cli import main
    mock_list_tasks.return_value = []
    mock_render.return_value = '{"test": "data"}'
    with patch('sys.argv', ['cli.py', '--json']):
        try:
            main()
        except SystemExit:
            pass
    captured = capsys.readouterr()
    assert '{"test": "data"}' in captured.out


# ========== Integration ==========

def test_integration_full_pipeline(sample_tasks):
    """Test integrazione completa data -> render -> output."""
    output = render_dashboard(sample_tasks)
    assert len(output) > 0
    assert isinstance(output, str)
    assert "CERVELLASWARM" in output
    assert "WORKERS STATUS" in output


def test_integration_json_pipeline(sample_tasks):
    """Test integrazione JSON completo."""
    output = render_json(sample_tasks)
    data = json.loads(output)
    assert data['timestamp']
    assert len(data['workers']) > 0
    assert isinstance(data['queue_stats'], dict)
