# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for SpawnManager.__init__ and spawn_worker(). All process calls mocked."""

import signal
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_spawn_workers.backend import ProcessInfo
from cervellaswarm_spawn_workers.spawner import SpawnManager, WorkerInfo


# ---------------------------------------------------------------------------
# Helpers
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


def _make_manager(tmp_path, backend="tmux", max_workers=5, claude_bin="/usr/bin/claude"):
    """Build a SpawnManager with mocked backend detection, no real signals."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value=backend), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value=claude_bin):
        return SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            max_workers=max_workers,
            register_signals=False,
        )


# ---------------------------------------------------------------------------
# SpawnManager.__init__
# ---------------------------------------------------------------------------


def test_init_default_values(tmp_path):
    """SpawnManager sets default paths and max_workers."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value="tmux"), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value="/usr/bin/claude"):
        mgr = SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            register_signals=False,
        )
    assert mgr.tasks_dir == tmp_path / "tasks"
    assert mgr.logs_dir == tmp_path / "logs"
    assert mgr.status_dir == tmp_path / "status"
    assert mgr.max_workers == 5


def test_init_auto_detects_backend(tmp_path):
    """SpawnManager calls detect_backend when no backend given."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value="nohup") as mock_detect, \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value=None):
        mgr = SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            register_signals=False,
        )
    mock_detect.assert_called_once()
    assert mgr.backend == "nohup"


def test_init_accepts_custom_backend(tmp_path):
    """SpawnManager uses custom backend override without calling detect_backend."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend") as mock_detect, \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value=None):
        mgr = SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            backend="nohup",
            register_signals=False,
        )
    mock_detect.assert_not_called()
    assert mgr.backend == "nohup"


def test_init_finds_claude_binary_via_which(tmp_path):
    """SpawnManager finds claude binary via shutil.which."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value="tmux"), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which",
               return_value="/usr/local/bin/claude") as mock_which:
        mgr = SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            register_signals=False,
        )
    mock_which.assert_called_once_with("claude")
    assert mgr.claude_bin == "/usr/local/bin/claude"


def test_init_uses_custom_claude_bin(tmp_path):
    """SpawnManager uses custom claude_bin, skipping shutil.which."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value="tmux"), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value="/fallback/claude"):
        mgr = SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            claude_bin="/custom/bin/claude",
            register_signals=False,
        )
    assert mgr.claude_bin == "/custom/bin/claude"


def test_init_registers_signal_handlers(tmp_path):
    """SpawnManager registers signal handlers when register_signals=True."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value="tmux"), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value=None), \
         patch("cervellaswarm_spawn_workers.spawner.signal.signal") as mock_signal, \
         patch("cervellaswarm_spawn_workers.spawner.atexit.register"):
        SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            register_signals=True,
        )
    assert mock_signal.call_count == 2
    calls = [c[0][0] for c in mock_signal.call_args_list]
    assert signal.SIGINT in calls
    assert signal.SIGTERM in calls


def test_init_skips_signal_handlers_when_false(tmp_path):
    """SpawnManager does not register signals when register_signals=False."""
    with patch("cervellaswarm_spawn_workers.spawner.detect_backend", return_value="tmux"), \
         patch("cervellaswarm_spawn_workers.spawner.shutil.which", return_value=None), \
         patch("cervellaswarm_spawn_workers.spawner.signal.signal") as mock_signal:
        SpawnManager(
            tasks_dir=str(tmp_path / "tasks"),
            logs_dir=str(tmp_path / "logs"),
            status_dir=str(tmp_path / "status"),
            register_signals=False,
        )
    mock_signal.assert_not_called()


# ---------------------------------------------------------------------------
# spawn_worker()
# ---------------------------------------------------------------------------


def test_spawn_worker_creates_directories(tmp_path):
    """spawn_worker creates logs, status, and prompts directories."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info(backend="tmux", session_name="swarm_alpha_1")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    assert mgr.logs_dir.exists()
    assert mgr.status_dir.exists()
    assert (mgr.logs_dir.parent / "prompts").exists()


def test_spawn_worker_writes_prompt_file(tmp_path):
    """spawn_worker writes the system prompt to a file."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info(backend="tmux", session_name="swarm_alpha_1")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha", system_prompt="custom system prompt")

    prompts_dir = mgr.logs_dir.parent / "prompts"
    prompt_file = prompts_dir / "worker_alpha.txt"
    assert prompt_file.exists()
    assert prompt_file.read_text() == "custom system prompt"


def test_spawn_worker_calls_launch_tmux_for_tmux_backend(tmp_path):
    """spawn_worker calls launch_tmux when backend is tmux."""
    mgr = _make_manager(tmp_path, backend="tmux")
    info = _make_process_info(backend="tmux", session_name="swarm_alpha_99")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info) as mock_launch, \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    mock_launch.assert_called_once()


def test_spawn_worker_calls_launch_nohup_for_nohup_backend(tmp_path):
    """spawn_worker calls launch_nohup when backend is nohup."""
    mgr = _make_manager(tmp_path, backend="nohup")
    info = _make_process_info(backend="nohup", session_name=None, pid=12345)

    with patch("cervellaswarm_spawn_workers.spawner.launch_nohup", return_value=info) as mock_launch, \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", return_value=False):
        mgr.spawn_worker("alpha")

    mock_launch.assert_called_once()


def test_spawn_worker_returns_worker_info(tmp_path):
    """spawn_worker returns a WorkerInfo with correct fields."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info(backend="tmux", session_name="swarm_alpha_1")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        worker = mgr.spawn_worker("alpha")

    assert isinstance(worker, WorkerInfo)
    assert worker.name == "alpha"
    assert worker.backend == "tmux"
    assert worker.session_name == "swarm_alpha_1"


def test_spawn_worker_appends_to_workers_list(tmp_path):
    """spawn_worker appends the new WorkerInfo to workers list."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")
        mgr.spawn_worker("beta")

    assert len(mgr.workers) == 2
    assert mgr.workers[0].name == "alpha"
    assert mgr.workers[1].name == "beta"


def test_spawn_worker_writes_session_tracking_file(tmp_path):
    """spawn_worker writes worker_name.session tracking file."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info(session_name="swarm_alpha_42")

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    session_file = mgr.status_dir / "worker_alpha.session"
    assert session_file.exists()
    assert session_file.read_text() == "swarm_alpha_42"


def test_spawn_worker_writes_pid_tracking_file(tmp_path):
    """spawn_worker writes worker_name.pid tracking file when pid is set."""
    mgr = _make_manager(tmp_path, backend="nohup")
    info = _make_process_info(backend="nohup", session_name=None, pid=9999)

    with patch("cervellaswarm_spawn_workers.spawner.launch_nohup", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_pid", return_value=False):
        mgr.spawn_worker("alpha")

    pid_file = mgr.status_dir / "worker_alpha.pid"
    assert pid_file.exists()
    assert pid_file.read_text() == "9999"


def test_spawn_worker_writes_start_tracking_file(tmp_path):
    """spawn_worker always writes worker_name.start tracking file."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    start_file = mgr.status_dir / "worker_alpha.start"
    assert start_file.exists()


def test_spawn_worker_raises_runtime_error_when_max_reached(tmp_path):
    """spawn_worker raises RuntimeError when max_workers limit is reached."""
    mgr = _make_manager(tmp_path, max_workers=1)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=True):
        mgr.spawn_worker("alpha")
        with pytest.raises(RuntimeError, match="Max workers limit reached"):
            mgr.spawn_worker("beta")


def test_spawn_worker_auto_generates_prompt_when_none(tmp_path):
    """spawn_worker auto-generates system_prompt when None provided."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False), \
         patch("cervellaswarm_spawn_workers.spawner.build_worker_prompt",
               return_value="auto-prompt") as mock_build:
        mgr.spawn_worker("alpha", system_prompt=None, specialty="backend")

    mock_build.assert_called_once_with("alpha", "backend", str(mgr.tasks_dir))
    prompt_file = mgr.logs_dir.parent / "prompts" / "worker_alpha.txt"
    assert prompt_file.read_text() == "auto-prompt"


def test_spawn_worker_uses_provided_system_prompt(tmp_path):
    """spawn_worker uses the given system_prompt without calling build_worker_prompt."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", return_value=info), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False), \
         patch("cervellaswarm_spawn_workers.spawner.build_worker_prompt") as mock_build:
        mgr.spawn_worker("alpha", system_prompt="my custom prompt")

    mock_build.assert_not_called()
    prompt_file = mgr.logs_dir.parent / "prompts" / "worker_alpha.txt"
    assert prompt_file.read_text() == "my custom prompt"


def test_spawn_worker_generates_correct_initial_prompt(tmp_path):
    """spawn_worker generates initial_prompt referencing tasks_dir."""
    mgr = _make_manager(tmp_path)
    info = _make_process_info()
    captured_commands = []

    def capture_launch(session_name, command, log_file, cwd=None, env=None):
        captured_commands.append(command)
        return info

    with patch("cervellaswarm_spawn_workers.spawner.launch_tmux", side_effect=capture_launch), \
         patch("cervellaswarm_spawn_workers.spawner.is_alive_tmux", return_value=False):
        mgr.spawn_worker("alpha")

    assert captured_commands
    assert str(mgr.tasks_dir) in captured_commands[0]
