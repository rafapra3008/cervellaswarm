# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for backend.py - execution backends for worker processes."""

import signal
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from cervellaswarm_spawn_workers.backend import (
    ProcessInfo,
    detect_backend,
    is_alive_pid,
    is_alive_tmux,
    kill_pid,
    kill_tmux,
    launch_nohup,
    launch_tmux,
    list_tmux_sessions,
)


# ---------------------------------------------------------------------------
# detect_backend
# ---------------------------------------------------------------------------


def test_detect_backend_returns_tmux_when_available():
    """Returns 'tmux' when tmux is on PATH."""
    with patch("cervellaswarm_spawn_workers.backend.shutil.which", return_value="/usr/bin/tmux"):
        assert detect_backend() == "tmux"


def test_detect_backend_returns_nohup_when_tmux_missing():
    """Returns 'nohup' when tmux is not on PATH."""
    with patch("cervellaswarm_spawn_workers.backend.shutil.which", return_value=None):
        assert detect_backend() == "nohup"


# ---------------------------------------------------------------------------
# launch_tmux
# ---------------------------------------------------------------------------


def _make_completed_process(returncode=0, stderr="", stdout=""):
    """Helper: build a mock CompletedProcess."""
    mock = MagicMock()
    mock.returncode = returncode
    mock.stderr = stderr
    mock.stdout = stdout
    return mock


def test_launch_tmux_creates_log_parent_dir(tmp_path):
    """Creates parent directories for the log file."""
    log_file = tmp_path / "deep" / "nested" / "worker.log"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)):
        launch_tmux("sess1", "echo hi", log_file)
    assert log_file.parent.exists()


def test_launch_tmux_calls_new_session(tmp_path):
    """Calls tmux new-session with correct positional args."""
    log_file = tmp_path / "w.log"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)) as mock_run:
        launch_tmux("my-session", "echo hi", log_file)

    first_call_args = mock_run.call_args_list[0][0][0]
    assert first_call_args[0] == "tmux"
    assert first_call_args[1] == "new-session"
    assert "-d" in first_call_args
    assert "-s" in first_call_args
    assert "my-session" in first_call_args


def test_launch_tmux_sets_remain_on_exit(tmp_path):
    """Calls tmux set-option remain-on-exit after creating session."""
    log_file = tmp_path / "w.log"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)) as mock_run:
        launch_tmux("my-session", "echo hi", log_file)

    second_call_args = mock_run.call_args_list[1][0][0]
    assert "set-option" in second_call_args
    assert "remain-on-exit" in second_call_args
    assert "on" in second_call_args


def test_launch_tmux_returns_process_info(tmp_path):
    """Returns ProcessInfo with session_name, backend='tmux', and log_file set."""
    log_file = tmp_path / "w.log"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)):
        info = launch_tmux("sess42", "echo hi", log_file)

    assert isinstance(info, ProcessInfo)
    assert info.session_name == "sess42"
    assert info.backend == "tmux"
    assert info.log_file == log_file


def test_launch_tmux_raises_on_nonzero_returncode(tmp_path):
    """Raises RuntimeError when tmux returns non-zero."""
    log_file = tmp_path / "w.log"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(1, stderr="session exists")):
        with pytest.raises(RuntimeError, match="Failed to create tmux session"):
            launch_tmux("bad-session", "echo hi", log_file)


def test_launch_tmux_passes_env_variables(tmp_path):
    """Merges env dict into environment passed to subprocess."""
    log_file = tmp_path / "w.log"
    extra_env = {"MY_VAR": "hello", "ANOTHER": "world"}

    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)) as mock_run:
        with patch("cervellaswarm_spawn_workers.backend.os.environ", {"BASE": "base"}):
            launch_tmux("s", "cmd", log_file, env=extra_env)

    passed_env = mock_run.call_args_list[0][1]["env"]
    assert passed_env["MY_VAR"] == "hello"
    assert passed_env["ANOTHER"] == "world"
    assert passed_env["BASE"] == "base"


def test_launch_tmux_passes_cwd(tmp_path):
    """Passes cwd as string to subprocess.run when provided."""
    log_file = tmp_path / "w.log"
    cwd = tmp_path / "workdir"
    cwd.mkdir()

    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)) as mock_run:
        launch_tmux("s", "cmd", log_file, cwd=cwd)

    passed_cwd = mock_run.call_args_list[0][1]["cwd"]
    assert passed_cwd == str(cwd)


def test_launch_tmux_cwd_none_when_not_provided(tmp_path):
    """Passes cwd=None to subprocess.run when cwd not given."""
    log_file = tmp_path / "w.log"

    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)) as mock_run:
        launch_tmux("s", "cmd", log_file)

    passed_cwd = mock_run.call_args_list[0][1]["cwd"]
    assert passed_cwd is None


# ---------------------------------------------------------------------------
# launch_nohup
# ---------------------------------------------------------------------------


def test_launch_nohup_creates_log_parent_dir(tmp_path):
    """Creates parent directories for the log file."""
    log_file = tmp_path / "deep" / "nested" / "worker.log"
    mock_proc = MagicMock()
    mock_proc.pid = 9999

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen", return_value=mock_proc):
        launch_nohup("echo hi", log_file)

    assert log_file.parent.exists()


def test_launch_nohup_opens_log_file(tmp_path):
    """Opens the log file for writing before spawning Popen."""
    log_file = tmp_path / "worker.log"
    mock_proc = MagicMock()
    mock_proc.pid = 1234

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen", return_value=mock_proc):
        launch_nohup("echo hi", log_file)

    assert log_file.exists()


def test_launch_nohup_popen_shell_and_new_session(tmp_path):
    """Creates Popen with shell=True and start_new_session=True."""
    log_file = tmp_path / "w.log"
    mock_proc = MagicMock()
    mock_proc.pid = 5555

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen",
               return_value=mock_proc) as mock_popen:
        launch_nohup("my-cmd", log_file)

    kwargs = mock_popen.call_args[1]
    assert kwargs["shell"] is True
    assert kwargs["start_new_session"] is True


def test_launch_nohup_returns_process_info_with_pid(tmp_path):
    """Returns ProcessInfo with pid and backend='nohup'."""
    log_file = tmp_path / "w.log"
    mock_proc = MagicMock()
    mock_proc.pid = 7777

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen", return_value=mock_proc):
        info = launch_nohup("cmd", log_file)

    assert isinstance(info, ProcessInfo)
    assert info.pid == 7777
    assert info.backend == "nohup"
    assert info.log_file == log_file


def test_launch_nohup_passes_env_variables(tmp_path):
    """Merges env dict into environment passed to Popen."""
    log_file = tmp_path / "w.log"
    mock_proc = MagicMock()
    mock_proc.pid = 100
    extra_env = {"WORKER_ID": "42"}

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen",
               return_value=mock_proc) as mock_popen:
        with patch("cervellaswarm_spawn_workers.backend.os.environ", {"PATH": "/usr/bin"}):
            launch_nohup("cmd", log_file, env=extra_env)

    kwargs = mock_popen.call_args[1]
    assert kwargs["env"]["WORKER_ID"] == "42"
    assert kwargs["env"]["PATH"] == "/usr/bin"


def test_launch_nohup_passes_cwd(tmp_path):
    """Passes cwd as string to Popen when provided."""
    log_file = tmp_path / "w.log"
    cwd = tmp_path / "work"
    cwd.mkdir()
    mock_proc = MagicMock()
    mock_proc.pid = 200

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen",
               return_value=mock_proc) as mock_popen:
        launch_nohup("cmd", log_file, cwd=cwd)

    kwargs = mock_popen.call_args[1]
    assert kwargs["cwd"] == str(cwd)


def test_launch_nohup_cwd_none_when_not_provided(tmp_path):
    """Passes cwd=None when cwd not given."""
    log_file = tmp_path / "w.log"
    mock_proc = MagicMock()
    mock_proc.pid = 300

    with patch("cervellaswarm_spawn_workers.backend.subprocess.Popen",
               return_value=mock_proc) as mock_popen:
        launch_nohup("cmd", log_file)

    kwargs = mock_popen.call_args[1]
    assert kwargs["cwd"] is None


# ---------------------------------------------------------------------------
# is_alive_tmux
# ---------------------------------------------------------------------------


def test_is_alive_tmux_returns_true_when_session_exists():
    """Returns True when tmux has-session returns 0."""
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)):
        assert is_alive_tmux("my-session") is True


def test_is_alive_tmux_returns_false_when_session_missing():
    """Returns False when tmux has-session returns non-zero."""
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(1)):
        assert is_alive_tmux("missing-session") is False


# ---------------------------------------------------------------------------
# is_alive_pid
# ---------------------------------------------------------------------------


def test_is_alive_pid_returns_true_when_process_running():
    """Returns True when os.kill(pid, 0) succeeds."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill", return_value=None):
        assert is_alive_pid(1234) is True


def test_is_alive_pid_returns_false_on_process_lookup_error():
    """Returns False when process does not exist."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=ProcessLookupError):
        assert is_alive_pid(9999) is False


def test_is_alive_pid_returns_true_on_permission_error():
    """Returns True on PermissionError - process exists but no permission to signal."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=PermissionError):
        assert is_alive_pid(9999) is True


# ---------------------------------------------------------------------------
# kill_tmux
# ---------------------------------------------------------------------------


def test_kill_tmux_returns_true_on_success():
    """Returns True when kill-session returns 0."""
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0)):
        assert kill_tmux("my-session") is True


def test_kill_tmux_returns_false_when_session_not_found():
    """Returns False when kill-session returns non-zero."""
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(1)):
        assert kill_tmux("ghost-session") is False


# ---------------------------------------------------------------------------
# kill_pid
# ---------------------------------------------------------------------------


def test_kill_pid_sends_sigterm_first():
    """Sends SIGTERM as first signal."""
    kill_calls = []

    def fake_kill(pid, sig):
        kill_calls.append((pid, sig))
        if sig == signal.SIGTERM:
            return  # allow
        raise ProcessLookupError

    # is_alive_pid: after SIGTERM, pretend process dies immediately
    with patch("cervellaswarm_spawn_workers.backend.os.kill", side_effect=fake_kill):
        with patch("cervellaswarm_spawn_workers.backend.is_alive_pid", return_value=False):
            result = kill_pid(1234, graceful_timeout=0.05)

    assert kill_calls[0] == (1234, signal.SIGTERM)
    assert result is True


def test_kill_pid_returns_true_when_process_dies_before_timeout():
    """Returns True when process exits within graceful_timeout."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill"):
        with patch("cervellaswarm_spawn_workers.backend.is_alive_pid", return_value=False):
            result = kill_pid(1234, graceful_timeout=0.1)
    assert result is True


def test_kill_pid_sends_sigkill_after_timeout():
    """Sends SIGKILL when process does not die before timeout."""
    kill_calls = []

    def fake_kill(pid, sig):
        kill_calls.append((pid, sig))

    with patch("cervellaswarm_spawn_workers.backend.os.kill", side_effect=fake_kill):
        with patch("cervellaswarm_spawn_workers.backend.is_alive_pid", return_value=True):
            with patch("cervellaswarm_spawn_workers.backend.time.sleep"):
                with patch("cervellaswarm_spawn_workers.backend.time.time",
                           side_effect=[0.0, 10.0, 10.0]):
                    result = kill_pid(1234, graceful_timeout=0.01)

    sigs = [sig for _, sig in kill_calls]
    assert signal.SIGTERM in sigs
    assert signal.SIGKILL in sigs
    assert result is True


def test_kill_pid_returns_false_when_process_not_found():
    """Returns False when SIGTERM raises ProcessLookupError (process gone)."""
    with patch("cervellaswarm_spawn_workers.backend.os.kill",
               side_effect=ProcessLookupError):
        result = kill_pid(9999, graceful_timeout=0.01)
    assert result is False


# ---------------------------------------------------------------------------
# list_tmux_sessions
# ---------------------------------------------------------------------------


def test_list_tmux_sessions_returns_matching_sessions():
    """Returns sessions that start with the given prefix."""
    output = "swarm_worker1\nswarm_worker2\nother_session\n"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0, stdout=output)):
        sessions = list_tmux_sessions(prefix="swarm_")
    assert sessions == ["swarm_worker1", "swarm_worker2"]


def test_list_tmux_sessions_filters_non_matching():
    """Excludes sessions that do not start with prefix."""
    output = "myapp_worker\nswarm_alpha\n"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0, stdout=output)):
        sessions = list_tmux_sessions(prefix="swarm_")
    assert sessions == ["swarm_alpha"]
    assert "myapp_worker" not in sessions


def test_list_tmux_sessions_returns_empty_on_error():
    """Returns empty list when tmux list-sessions fails (returncode != 0)."""
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(1)):
        sessions = list_tmux_sessions(prefix="swarm_")
    assert sessions == []


def test_list_tmux_sessions_uses_default_prefix():
    """Uses 'swarm_' as default prefix when none provided."""
    output = "swarm_one\nother_one\n"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0, stdout=output)):
        sessions = list_tmux_sessions()
    assert sessions == ["swarm_one"]


def test_list_tmux_sessions_empty_when_no_matches():
    """Returns empty list when no sessions match prefix."""
    output = "unrelated_session\nanother_unrelated\n"
    with patch("cervellaswarm_spawn_workers.backend.subprocess.run",
               return_value=_make_completed_process(0, stdout=output)):
        sessions = list_tmux_sessions(prefix="swarm_")
    assert sessions == []
