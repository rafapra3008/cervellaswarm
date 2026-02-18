# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for SpawnManager operations: spawn_team, get_status, kill_all/worker, cleanup, signal."""

import signal
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_spawn_workers.backend import ProcessInfo
from cervellaswarm_spawn_workers.spawner import SpawnManager, SpawnResult
from cervellaswarm_spawn_workers.team_loader import AgentConfig, SpawnConfig, TeamConfig


# ---------------------------------------------------------------------------
# Helpers (duplicated for independence - no __init__.py cross-import)
# ---------------------------------------------------------------------------


def _make_process_info(backend="tmux", session_name="swarm_test_1", pid=None, log_file=None):
    """Build a ProcessInfo stub."""
    return ProcessInfo(
        backend=backend,
        session_name=session_name,
        pid=pid,
        log_file=log_file or Path("/tmp/test.log"),
        start_time=time.time(),
    )


def _make_manager(tmp_path, backend="tmux", max_workers=5, claude_bin="/usr/bin/claude",
                   status_dir=None):
    """Build a SpawnManager with mocked backend detection, no real signals."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value=backend), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value=claude_bin):
        return SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=status_dir or str(tmp_path / "status"),
            max_workers=max_workers,
            register_signals=False,
        )


# ---------------------------------------------------------------------------
# spawn_team()
# ---------------------------------------------------------------------------


def test_spawn_team_spawns_all_spawnables(tmp_path):
    """spawn_team spawns all agents with spawn_on_start=True and type worker/guardian."""
    mgr = _make_manager(tmp_path)
    team = TeamConfig(
        name="test",
        agents=[
            AgentConfig(name="worker-1", type="worker", spawn_on_start=True),
            AgentConfig(name="guardian-1", type="guardian", spawn_on_start=True),
            AgentConfig(name="leader-1", type="leader", spawn_on_start=True),  # not spawnable
        ],
        spawn=SpawnConfig(),
    )
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        result = mgr.spawn_team(team)

    assert result.spawned == 2
    assert result.failed == 0


def test_spawn_team_returns_spawn_result(tmp_path):
    """spawn_team returns a SpawnResult with correct counts."""
    mgr = _make_manager(tmp_path)
    team = TeamConfig(
        name="test",
        agents=[AgentConfig(name="w1", type="worker", spawn_on_start=True)],
        spawn=SpawnConfig(),
    )
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        result = mgr.spawn_team(team)

    assert isinstance(result, SpawnResult)
    assert result.spawned == 1
    assert result.failed == 0
    assert len(result.workers) == 1


def test_spawn_team_tracks_failures(tmp_path):
    """spawn_team records failures in errors list."""
    mgr = _make_manager(tmp_path, max_workers=0)
    team = TeamConfig(
        name="test",
        agents=[AgentConfig(name="w1", type="worker", spawn_on_start=True)],
        spawn=SpawnConfig(),
    )

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        result = mgr.spawn_team(team)

    assert result.failed == 1
    assert result.spawned == 0
    assert len(result.errors) == 1
    assert "w1" in result.errors[0]


def test_spawn_team_continues_after_individual_failure(tmp_path):
    """spawn_team keeps spawning after an individual failure."""
    mgr = _make_manager(tmp_path, max_workers=1)
    team = TeamConfig(
        name="test",
        agents=[
            AgentConfig(name="w1", type="worker", spawn_on_start=True),
            AgentConfig(name="w2", type="worker", spawn_on_start=True),
        ],
        spawn=SpawnConfig(),
    )
    info = _make_process_info()
    call_count = {"n": 0}

    def side_effect(*args, **kwargs):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return info
        raise RuntimeError("max reached")

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=True), \
         patch("cervellaswarm_spawn_workers.spawner.launch_tmux", side_effect=side_effect):
        result = mgr.spawn_team(team)

    # First succeeds, second fails - both were attempted
    assert result.spawned + result.failed == 2


# ---------------------------------------------------------------------------
# get_status()
# ---------------------------------------------------------------------------


def test_get_status_returns_all_workers(tmp_path):
    """get_status returns status for all tracked workers."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")
        mgr.spawn_worker("beta")

    statuses = mgr.get_status()
    assert len(statuses) == 2
    names = {s.name for s in statuses}
    assert "alpha" in names
    assert "beta" in names


def test_get_status_checks_tmux_alive_for_tmux_workers(tmp_path):
    """get_status calls is_alive_tmux for tmux backend workers."""
    mgr = _make_manager(tmp_path, backend="tmux")
    info = _make_process_info(session_name="swarm_alpha_1")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=True) as mock_alive:
        statuses = mgr.get_status()

    mock_alive.assert_called_once_with("swarm_alpha_1")
    assert statuses[0].alive is True


def test_get_status_checks_pid_alive_for_nohup_workers(tmp_path):
    """get_status calls is_alive_pid for nohup backend workers."""
    mgr = _make_manager(tmp_path, backend="nohup")
    info = _make_process_info(backend="nohup", session_name=None, pid=1234)

    with patch("cervellaswarm_spawn_workers.spawner.launch_nohup", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", return_value=True) as mock_alive:
        statuses = mgr.get_status()

    mock_alive.assert_called_once_with(1234)
    assert statuses[0].alive is True


def test_get_status_calculates_uptime_for_alive_workers(tmp_path):
    """get_status sets uptime_seconds > 0 for alive workers."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    mgr.workers[0].start_time = time.time() - 10.0

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=True):
        statuses = mgr.get_status()

    assert statuses[0].uptime_seconds > 0


def test_get_status_sets_uptime_zero_for_dead_workers(tmp_path):
    """get_status sets uptime_seconds=0.0 for dead workers."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        statuses = mgr.get_status()

    assert statuses[0].uptime_seconds == 0.0


# ---------------------------------------------------------------------------
# kill_all()
# ---------------------------------------------------------------------------


def test_kill_all_kills_tmux_sessions(tmp_path):
    """kill_all calls kill_tmux for tmux workers."""
    mgr = _make_manager(tmp_path, backend="tmux")
    info = _make_process_info(session_name="swarm_alpha_1")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.kill_tmux", return_value=True) as mock_kill:
        killed = mgr.kill_all()

    mock_kill.assert_called_once_with("swarm_alpha_1")
    assert killed == 1


def test_kill_all_kills_pids_for_nohup_workers(tmp_path):
    """kill_all calls kill_pid for nohup workers."""
    mgr = _make_manager(tmp_path, backend="nohup")
    info = _make_process_info(backend="nohup", session_name=None, pid=5678)

    with patch("cervellaswarm_spawn_workers.spawner.launch_nohup", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.kill_pid", return_value=True) as mock_kill:
        killed = mgr.kill_all()

    mock_kill.assert_called_once_with(5678, 5.0)
    assert killed == 1


def test_kill_all_returns_killed_count(tmp_path):
    """kill_all returns the correct count of killed workers."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")
        mgr.spawn_worker("beta")

    with patch("cervellaswarm_spawn_workers.spawner.kill_tmux", return_value=True):
        killed = mgr.kill_all()

    assert killed == 2


def test_kill_all_handles_already_dead_workers(tmp_path):
    """kill_all counts 0 for workers kill_tmux returns False (already dead)."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.kill_tmux", return_value=False):
        killed = mgr.kill_all()

    assert killed == 0


# ---------------------------------------------------------------------------
# kill_worker()
# ---------------------------------------------------------------------------


def test_kill_worker_kills_specific_worker_by_name(tmp_path):
    """kill_worker kills the named worker."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info(session_name="swarm_alpha_1")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    with patch("cervellaswarm_spawn_workers.spawner.kill_tmux", return_value=True) as mock_kill:
        result = mgr.kill_worker("alpha")

    mock_kill.assert_called_once_with("swarm_alpha_1")
    assert result is True


def test_kill_worker_returns_false_for_unknown_name(tmp_path):
    """kill_worker returns False when worker name is not tracked."""
    mgr = _make_manager(tmp_path)
    result = mgr.kill_worker("nonexistent")
    assert result is False


# ---------------------------------------------------------------------------
# cleanup()
# ---------------------------------------------------------------------------


def test_cleanup_removes_tracking_files(tmp_path):
    """cleanup removes worker_* tracking files from status dir."""
    mgr = _make_manager(tmp_path)
    mgr.status_dir.mkdir(parents=True, exist_ok=True)

    (mgr.status_dir / "worker_alpha.pid").write_text("1234")
    (mgr.status_dir / "worker_alpha.session").write_text("swarm_alpha")
    (mgr.status_dir / "worker_alpha.start").write_text("1700000000")

    mgr.cleanup()

    assert not (mgr.status_dir / "worker_alpha.pid").exists()
    assert not (mgr.status_dir / "worker_alpha.session").exists()
    assert not (mgr.status_dir / "worker_alpha.start").exists()


def test_cleanup_handles_missing_status_dir(tmp_path):
    """cleanup does not raise if status dir does not exist."""
    mgr = _make_manager(tmp_path)
    # status_dir was never created
    mgr.cleanup()  # should not raise


def test_cleanup_only_removes_worker_prefixed_files(tmp_path):
    """cleanup leaves non-worker files untouched."""
    mgr = _make_manager(tmp_path)
    mgr.status_dir.mkdir(parents=True, exist_ok=True)

    other_file = mgr.status_dir / "other_stuff.txt"
    other_file.write_text("keep me")
    (mgr.status_dir / "worker_alpha.pid").write_text("1234")

    mgr.cleanup()

    assert other_file.exists()
    assert not (mgr.status_dir / "worker_alpha.pid").exists()


# ---------------------------------------------------------------------------
# _signal_handler()
# ---------------------------------------------------------------------------


def test_signal_handler_calls_kill_all(tmp_path):
    """_signal_handler kills all workers before exiting."""
    mgr = _make_manager(tmp_path)
    mgr.kill_all = MagicMock(return_value=0)

    with pytest.raises(SystemExit):
        mgr._signal_handler(signal.SIGINT, None)

    mgr.kill_all.assert_called_once()


def test_signal_handler_raises_system_exit(tmp_path):
    """_signal_handler raises SystemExit."""
    mgr = _make_manager(tmp_path)
    mgr.kill_all = MagicMock(return_value=0)

    with pytest.raises(SystemExit):
        mgr._signal_handler(signal.SIGTERM, None)


# --- _load_tracked_workers tests (F3 fix) ---


def test_load_tracked_workers_loads_tmux_worker(tmp_path):
    """Loads a tmux worker from status dir tracking files."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()
    (status_dir / "worker_backend.start").write_text("1700000000")
    (status_dir / "worker_backend.session").write_text("swarm_backend_1700000000")
    (status_dir / "worker_backend.pid").write_text("12345")

    mgr = _make_manager(tmp_path, status_dir=str(status_dir))
    assert len(mgr.workers) == 1
    w = mgr.workers[0]
    assert w.name == "backend"
    assert w.backend == "tmux"
    assert w.session_name == "swarm_backend_1700000000"
    assert w.pid == 12345
    assert w.start_time == 1700000000.0


def test_load_tracked_workers_loads_nohup_worker(tmp_path):
    """Loads a nohup worker (no session file) from status dir."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()
    (status_dir / "worker_tester.start").write_text("1700000001")
    (status_dir / "worker_tester.pid").write_text("99999")

    mgr = _make_manager(tmp_path, status_dir=str(status_dir))
    assert len(mgr.workers) == 1
    w = mgr.workers[0]
    assert w.name == "tester"
    assert w.backend == "nohup"
    assert w.session_name is None
    assert w.pid == 99999


def test_load_tracked_workers_handles_missing_status_dir(tmp_path):
    """No crash when status dir doesn't exist."""
    mgr = _make_manager(tmp_path, status_dir=str(tmp_path / "nonexistent"))
    assert len(mgr.workers) == 0


def test_load_tracked_workers_handles_invalid_pid(tmp_path):
    """Gracefully handles non-integer PID file."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()
    (status_dir / "worker_bad.start").write_text("1700000000")
    (status_dir / "worker_bad.pid").write_text("not_a_number")

    mgr = _make_manager(tmp_path, status_dir=str(status_dir))
    assert len(mgr.workers) == 1
    assert mgr.workers[0].pid is None


def test_load_tracked_workers_multiple_workers(tmp_path):
    """Loads multiple workers from status dir."""
    status_dir = tmp_path / "status"
    status_dir.mkdir()
    (status_dir / "worker_alpha.start").write_text("1700000000")
    (status_dir / "worker_alpha.session").write_text("swarm_alpha")
    (status_dir / "worker_beta.start").write_text("1700000001")
    (status_dir / "worker_beta.pid").write_text("55555")

    mgr = _make_manager(tmp_path, status_dir=str(status_dir))
    assert len(mgr.workers) == 2
    names = {w.name for w in mgr.workers}
    assert names == {"alpha", "beta"}
