# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_task_orchestration.task_manager."""

import pytest
from pathlib import Path

from cervellaswarm_task_orchestration.task_manager import (
    validate_task_id,
    ensure_tasks_dir,
    create_task,
    list_tasks,
    mark_ready,
    mark_working,
    mark_done,
    ack_received,
    ack_understood,
    get_task_status,
    get_ack_status,
    cleanup_task,
)


# ---------------------------------------------------------------------------
# validate_task_id
# ---------------------------------------------------------------------------


def test_validate_task_id_valid_simple():
    assert validate_task_id("TASK_001") is True


def test_validate_task_id_valid_with_dash():
    assert validate_task_id("my-task-1") is True


def test_validate_task_id_valid_alphanumeric():
    assert validate_task_id("Task123") is True


def test_validate_task_id_valid_underscore_dash_combo():
    assert validate_task_id("TASK_A-B_99") is True


def test_validate_task_id_empty():
    assert validate_task_id("") is False


def test_validate_task_id_too_long():
    assert validate_task_id("A" * 51) is False


def test_validate_task_id_exactly_50_chars():
    assert validate_task_id("A" * 50) is True


def test_validate_task_id_path_traversal_dotdot():
    assert validate_task_id("../../etc/passwd") is False


def test_validate_task_id_path_traversal_slash():
    assert validate_task_id("tasks/evil") is False


def test_validate_task_id_path_traversal_backslash():
    assert validate_task_id("tasks\\evil") is False


def test_validate_task_id_special_chars_at():
    assert validate_task_id("task@1") is False


def test_validate_task_id_special_chars_space():
    assert validate_task_id("task 1") is False


def test_validate_task_id_special_chars_dot():
    assert validate_task_id("task.1") is False


def test_validate_task_id_special_chars_exclamation():
    assert validate_task_id("task!") is False


# ---------------------------------------------------------------------------
# ensure_tasks_dir
# ---------------------------------------------------------------------------


def test_ensure_tasks_dir_creates_new(tmp_path):
    new_dir = str(tmp_path / "tasks" / "nested")
    result = ensure_tasks_dir(new_dir)
    assert result == Path(new_dir)
    assert result.exists()
    assert result.is_dir()


def test_ensure_tasks_dir_already_exists(tmp_path):
    existing = tmp_path / "tasks"
    existing.mkdir()
    result = ensure_tasks_dir(str(existing))
    assert result == existing
    assert result.is_dir()


def test_ensure_tasks_dir_returns_path_object(tmp_path):
    result = ensure_tasks_dir(str(tmp_path / "tasks"))
    assert isinstance(result, Path)


# ---------------------------------------------------------------------------
# create_task
# ---------------------------------------------------------------------------


def test_create_task_creates_file(tmp_path):
    path = create_task("TASK_001", "backend-worker", "Do the thing", tasks_dir=str(tmp_path))
    assert Path(path).exists()
    assert "TASK_001.md" in path


def test_create_task_content_has_description(tmp_path):
    create_task("TASK_001", "backend-worker", "My great task", tasks_dir=str(tmp_path))
    content = (tmp_path / "TASK_001.md").read_text()
    assert "My great task" in content


def test_create_task_content_has_agent(tmp_path):
    create_task("TASK_001", "frontend-worker", "Some task", tasks_dir=str(tmp_path))
    content = (tmp_path / "TASK_001.md").read_text()
    assert "frontend-worker" in content


def test_create_task_default_risk_level_1(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    content = (tmp_path / "TASK_001.md").read_text()
    assert "Risk level: 1" in content
    assert "LOW" in content


def test_create_task_risk_level_2(tmp_path):
    create_task("TASK_002", "agent", "Task", risk_level=2, tasks_dir=str(tmp_path))
    content = (tmp_path / "TASK_002.md").read_text()
    assert "Risk level: 2" in content
    assert "MEDIUM" in content


def test_create_task_risk_level_3(tmp_path):
    create_task("TASK_003", "agent", "Task", risk_level=3, tasks_dir=str(tmp_path))
    content = (tmp_path / "TASK_003.md").read_text()
    assert "Risk level: 3" in content
    assert "HIGH" in content


def test_create_task_invalid_id_raises(tmp_path):
    with pytest.raises(ValueError, match="Invalid task ID"):
        create_task("../../evil", "agent", "Task", tasks_dir=str(tmp_path))


def test_create_task_duplicate_raises(tmp_path):
    create_task("TASK_001", "agent", "First", tasks_dir=str(tmp_path))
    with pytest.raises(FileExistsError, match="already exists"):
        create_task("TASK_001", "agent", "Second", tasks_dir=str(tmp_path))


def test_create_task_custom_tasks_dir(tmp_path):
    custom = str(tmp_path / "my_tasks")
    path = create_task("TASK_001", "agent", "Task", tasks_dir=custom)
    assert Path(path).exists()
    assert custom in path


# ---------------------------------------------------------------------------
# list_tasks
# ---------------------------------------------------------------------------


def test_list_tasks_empty_dir(tmp_path):
    result = list_tasks(tasks_dir=str(tmp_path))
    assert result == []


def test_list_tasks_single_task(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = list_tasks(tasks_dir=str(tmp_path))
    assert len(result) == 1
    assert result[0]["task_id"] == "TASK_001"
    assert result[0]["status"] == "created"
    assert result[0]["agent"] == "agent"


def test_list_tasks_multiple_tasks(tmp_path):
    create_task("TASK_001", "agent-a", "Task A", tasks_dir=str(tmp_path))
    create_task("TASK_002", "agent-b", "Task B", tasks_dir=str(tmp_path))
    create_task("TASK_003", "agent-c", "Task C", tasks_dir=str(tmp_path))
    result = list_tasks(tasks_dir=str(tmp_path))
    assert len(result) == 3
    ids = [t["task_id"] for t in result]
    assert "TASK_001" in ids
    assert "TASK_002" in ids
    assert "TASK_003" in ids


def test_list_tasks_has_required_keys(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = list_tasks(tasks_dir=str(tmp_path))
    assert set(result[0].keys()) == {"task_id", "status", "ack", "agent", "file"}


def test_list_tasks_custom_dir(tmp_path):
    custom = str(tmp_path / "custom")
    create_task("TASK_001", "agent", "Task", tasks_dir=custom)
    result = list_tasks(tasks_dir=custom)
    assert len(result) == 1


# ---------------------------------------------------------------------------
# mark_ready
# ---------------------------------------------------------------------------


def test_mark_ready_success(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = mark_ready("TASK_001", tasks_dir=str(tmp_path))
    assert result is True
    assert (tmp_path / "TASK_001.ready").exists()


def test_mark_ready_invalid_id(tmp_path):
    result = mark_ready("../../evil", tasks_dir=str(tmp_path))
    assert result is False


def test_mark_ready_nonexistent_task(tmp_path):
    result = mark_ready("TASK_999", tasks_dir=str(tmp_path))
    assert result is False


def test_mark_ready_custom_dir(tmp_path):
    custom = str(tmp_path / "tasks")
    create_task("TASK_001", "agent", "Task", tasks_dir=custom)
    result = mark_ready("TASK_001", tasks_dir=custom)
    assert result is True


# ---------------------------------------------------------------------------
# mark_working
# ---------------------------------------------------------------------------


def test_mark_working_success(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = mark_working("TASK_001", tasks_dir=str(tmp_path))
    assert result is True
    assert (tmp_path / "TASK_001.working").exists()


def test_mark_working_race_condition_double_claim(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    first = mark_working("TASK_001", tasks_dir=str(tmp_path))
    second = mark_working("TASK_001", tasks_dir=str(tmp_path))
    assert first is True
    assert second is False


def test_mark_working_invalid_id(tmp_path):
    result = mark_working("bad/id", tasks_dir=str(tmp_path))
    assert result is False


def test_mark_working_nonexistent_task(tmp_path):
    result = mark_working("TASK_999", tasks_dir=str(tmp_path))
    assert result is False


def test_mark_working_file_has_timestamp(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_working("TASK_001", tasks_dir=str(tmp_path))
    content = (tmp_path / "TASK_001.working").read_text()
    assert "started:" in content


# ---------------------------------------------------------------------------
# mark_done
# ---------------------------------------------------------------------------


def test_mark_done_success(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = mark_done("TASK_001", tasks_dir=str(tmp_path))
    assert result is True
    assert (tmp_path / "TASK_001.done").exists()


def test_mark_done_invalid_id(tmp_path):
    result = mark_done("../evil", tasks_dir=str(tmp_path))
    assert result is False


def test_mark_done_nonexistent_task(tmp_path):
    result = mark_done("TASK_999", tasks_dir=str(tmp_path))
    assert result is False


# ---------------------------------------------------------------------------
# ack_received / ack_understood
# ---------------------------------------------------------------------------


def test_ack_received_success(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = ack_received("TASK_001", tasks_dir=str(tmp_path))
    assert result is True
    assert (tmp_path / "TASK_001.ack_received").exists()


def test_ack_received_invalid_id(tmp_path):
    result = ack_received("bad id", tasks_dir=str(tmp_path))
    assert result is False


def test_ack_received_nonexistent_task(tmp_path):
    result = ack_received("TASK_999", tasks_dir=str(tmp_path))
    assert result is False


def test_ack_understood_success(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = ack_understood("TASK_001", tasks_dir=str(tmp_path))
    assert result is True
    assert (tmp_path / "TASK_001.ack_understood").exists()


def test_ack_understood_invalid_id(tmp_path):
    result = ack_understood("../bad", tasks_dir=str(tmp_path))
    assert result is False


def test_ack_understood_nonexistent_task(tmp_path):
    result = ack_understood("TASK_999", tasks_dir=str(tmp_path))
    assert result is False


# ---------------------------------------------------------------------------
# get_task_status
# ---------------------------------------------------------------------------


def test_get_task_status_created(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    assert get_task_status("TASK_001", tasks_dir=str(tmp_path)) == "created"


def test_get_task_status_ready(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_ready("TASK_001", tasks_dir=str(tmp_path))
    assert get_task_status("TASK_001", tasks_dir=str(tmp_path)) == "ready"


def test_get_task_status_working(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_working("TASK_001", tasks_dir=str(tmp_path))
    assert get_task_status("TASK_001", tasks_dir=str(tmp_path)) == "working"


def test_get_task_status_done(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_done("TASK_001", tasks_dir=str(tmp_path))
    assert get_task_status("TASK_001", tasks_dir=str(tmp_path)) == "done"


def test_get_task_status_not_found(tmp_path):
    assert get_task_status("TASK_999", tasks_dir=str(tmp_path)) == "not_found"


def test_get_task_status_invalid_id():
    assert get_task_status("../../evil") == "invalid"


def test_get_task_status_done_overrides_working(tmp_path):
    """done marker takes priority over working."""
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_working("TASK_001", tasks_dir=str(tmp_path))
    mark_done("TASK_001", tasks_dir=str(tmp_path))
    assert get_task_status("TASK_001", tasks_dir=str(tmp_path)) == "done"


# ---------------------------------------------------------------------------
# get_ack_status
# ---------------------------------------------------------------------------


def test_get_ack_status_no_ack(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    assert get_ack_status("TASK_001", tasks_dir=str(tmp_path)) == "-/-/-"


def test_get_ack_status_received_only(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    ack_received("TASK_001", tasks_dir=str(tmp_path))
    assert get_ack_status("TASK_001", tasks_dir=str(tmp_path)) == "Y/-/-"


def test_get_ack_status_received_and_understood(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    ack_received("TASK_001", tasks_dir=str(tmp_path))
    ack_understood("TASK_001", tasks_dir=str(tmp_path))
    assert get_ack_status("TASK_001", tasks_dir=str(tmp_path)) == "Y/Y/-"


def test_get_ack_status_all_done(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    ack_received("TASK_001", tasks_dir=str(tmp_path))
    ack_understood("TASK_001", tasks_dir=str(tmp_path))
    mark_done("TASK_001", tasks_dir=str(tmp_path))
    assert get_ack_status("TASK_001", tasks_dir=str(tmp_path)) == "Y/Y/Y"


def test_get_ack_status_invalid_id():
    assert get_ack_status("bad/id") == "---"


# ---------------------------------------------------------------------------
# cleanup_task
# ---------------------------------------------------------------------------


def test_cleanup_task_removes_all_markers(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_ready("TASK_001", tasks_dir=str(tmp_path))
    mark_working("TASK_001", tasks_dir=str(tmp_path))
    mark_done("TASK_001", tasks_dir=str(tmp_path))
    ack_received("TASK_001", tasks_dir=str(tmp_path))
    ack_understood("TASK_001", tasks_dir=str(tmp_path))

    result = cleanup_task("TASK_001", tasks_dir=str(tmp_path))
    assert result is True

    for marker in [".ready", ".working", ".done", ".ack_received", ".ack_understood"]:
        assert not (tmp_path / f"TASK_001{marker}").exists()


def test_cleanup_task_task_file_remains(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_ready("TASK_001", tasks_dir=str(tmp_path))
    cleanup_task("TASK_001", tasks_dir=str(tmp_path))
    assert (tmp_path / "TASK_001.md").exists()


def test_cleanup_task_no_markers_returns_true(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    result = cleanup_task("TASK_001", tasks_dir=str(tmp_path))
    assert result is True


def test_cleanup_task_invalid_id(tmp_path):
    result = cleanup_task("../../evil", tasks_dir=str(tmp_path))
    assert result is False


def test_cleanup_task_after_cleanup_status_is_created(tmp_path):
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    mark_ready("TASK_001", tasks_dir=str(tmp_path))
    mark_working("TASK_001", tasks_dir=str(tmp_path))
    cleanup_task("TASK_001", tasks_dir=str(tmp_path))
    assert get_task_status("TASK_001", tasks_dir=str(tmp_path)) == "created"
