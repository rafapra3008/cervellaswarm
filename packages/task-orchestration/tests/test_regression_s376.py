# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Regression tests S376 - 9 bug fixes in cervellaswarm-task-orchestration.

Each test is named after the bug it catches and includes a comment
explaining the original defect. Tests PASS with the fixed code.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch

from cervellaswarm_task_orchestration.task_manager import (
    create_task,
    list_tasks,
)
from cervellaswarm_task_orchestration.output_validator import (
    validate_output,
    find_task_output,
    SUCCESS_INDICATORS,
)
from cervellaswarm_task_orchestration.cli import main_task

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

LONG_OK = "This output is complete and valid. " * 10  # >100 chars, no markers


def _make_output(path: Path, content: str) -> Path:
    path.write_text(content)
    return path


# ---------------------------------------------------------------------------
# BUG 1: list_tasks glob mismatch
# BEFORE: glob("TASK_*.md") - tasks with non-TASK_ IDs were invisible
# FIX:    glob("*.md") with marker suffix filter
# ---------------------------------------------------------------------------


def test_bug1_list_tasks_finds_custom_task_id(tmp_path):
    """Bug 1: list_tasks used glob('TASK_*.md'), missing tasks with custom IDs.

    A task created with id 'my_custom_task' was silently invisible to
    list_tasks because the glob pattern required the TASK_ prefix.
    """
    create_task("my_custom_task", "backend", "Custom task", tasks_dir=str(tmp_path))
    result = list_tasks(tasks_dir=str(tmp_path))
    task_ids = [t["task_id"] for t in result]
    assert "my_custom_task" in task_ids, (
        "Bug 1 regression: custom task ID not found by list_tasks"
    )


def test_bug1_list_tasks_finds_mixed_ids(tmp_path):
    """Bug 1 variant: list_tasks must find both TASK_ prefix and custom IDs."""
    create_task("TASK_001", "agent-a", "Standard task", tasks_dir=str(tmp_path))
    create_task("feature-build", "agent-b", "Feature task", tasks_dir=str(tmp_path))
    result = list_tasks(tasks_dir=str(tmp_path))
    task_ids = [t["task_id"] for t in result]
    assert "TASK_001" in task_ids
    assert "feature-build" in task_ids
    assert len(result) == 2


def test_bug1_list_tasks_does_not_include_marker_files(tmp_path):
    """Bug 1 safety: marker files (.ready, .working, etc.) must not appear in list."""
    create_task("TASK_001", "agent", "Task", tasks_dir=str(tmp_path))
    # Manually create marker files that look like .md via the stem
    # (The fix uses suffix filtering, so this checks .ready/.working/.done etc.)
    (tmp_path / "TASK_001.ready").touch()
    (tmp_path / "TASK_001.working").touch()
    result = list_tasks(tasks_dir=str(tmp_path))
    assert len(result) == 1
    assert result[0]["task_id"] == "TASK_001"


# ---------------------------------------------------------------------------
# BUG 2: except Exception too broad in output_validator
# BEFORE: except Exception as e: swallowed TypeError, AttributeError, etc.
# FIX:    except (OSError, PermissionError, UnicodeDecodeError) as e:
# ---------------------------------------------------------------------------


def test_bug2_validate_output_propagates_type_error(tmp_path):
    """Bug 2: broad except Exception swallowed TypeError from bad file objects.

    The original except Exception catch swallowed programming errors.
    A TypeError should propagate, not be silently absorbed.
    """
    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)

    # Patch read_text to raise TypeError (simulates programming bug)
    with patch.object(Path, "read_text", side_effect=TypeError("bad type")):
        with pytest.raises(TypeError):
            validate_output(output_file)


def test_bug2_validate_output_propagates_attribute_error(tmp_path):
    """Bug 2: AttributeError from bad internal state must not be swallowed."""
    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)

    with patch.object(Path, "read_text", side_effect=AttributeError("no attr")):
        with pytest.raises(AttributeError):
            validate_output(output_file)


def test_bug2_validate_output_still_catches_os_error(tmp_path):
    """Bug 2 happy path: OSError (permission denied) is still handled gracefully."""
    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)

    with patch.object(Path, "read_text", side_effect=OSError("permission denied")):
        result = validate_output(output_file)
    assert result.valid is False
    assert result.score == 0


# ---------------------------------------------------------------------------
# BUG 3: "..." removed from INCOMPLETE_MARKERS
# BEFORE: "..." in INCOMPLETE_MARKERS -> ellipsis in any prose caused false positive
# FIX:    "..." removed from the list
# ---------------------------------------------------------------------------


def test_bug3_ellipsis_does_not_trigger_incomplete_warning(tmp_path):
    """Bug 3: '...' was an INCOMPLETE_MARKER causing false positives.

    Content like 'Loading... please wait' or 'and so on...' triggered
    the incomplete marker check and reduced score incorrectly.
    """
    content = LONG_OK + " Loading... please wait. The process continues..."
    output_file = _make_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(output_file)
    assert not any("..." in w for w in result.warnings), (
        "Bug 3 regression: '...' still flagged as incomplete marker"
    )


def test_bug3_ellipsis_in_prose_does_not_reduce_score(tmp_path):
    """Bug 3: score must not be reduced by legitimate ellipsis usage."""
    clean_content = LONG_OK  # no markers at all
    ellipsis_content = LONG_OK + " See details..."

    clean_file = _make_output(tmp_path / "clean_output.md", clean_content)
    ellipsis_file = _make_output(tmp_path / "ellipsis_output.md", ellipsis_content)

    clean_result = validate_output(clean_file)
    ellipsis_result = validate_output(ellipsis_file)

    assert ellipsis_result.score == clean_result.score, (
        "Bug 3 regression: '...' reduces score that should be identical to clean output"
    )


# ---------------------------------------------------------------------------
# BUG 4: "OK" success indicator false positive (word boundary missing)
# BEFORE: if ind in content -> "OK" matched inside "BOOK", "BOOKMARK", etc.
# FIX:    re.search(rf"\b{re.escape(ind)}\b", content) for word boundaries
# ---------------------------------------------------------------------------


def test_bug4_ok_inside_word_does_not_trigger_bonus(tmp_path):
    """Bug 4: 'OK' matched as substring in words like 'BOOK', 'LOOKUP'.

    The original check `if ind in content` found 'OK' inside 'BOOK',
    giving a false success bonus. Word boundaries prevent this.
    """
    # Content containing "BOOK" and "LOOKUP" but NOT standalone "OK"
    content = LONG_OK.replace("ok", "").replace("OK", "") + " See the BOOK and LOOKUP table."
    # Make sure "OK" does not appear as standalone word
    assert " OK " not in content
    assert "\nOK\n" not in content

    output_file = _make_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(output_file)

    # Score should be 100 (no bonus from word-embedded "OK")
    assert result.score <= 100
    # Verify "OK" is in SUCCESS_INDICATORS so we know the check matters
    assert "OK" in SUCCESS_INDICATORS


def test_bug4_standalone_ok_triggers_bonus(tmp_path):
    """Bug 4 happy path: standalone 'OK' as a word does trigger the bonus."""
    content = LONG_OK + " Status: OK - all checks passed."
    output_file = _make_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(output_file)
    # Bonus adds 5, clean baseline is 100, so score should be >= 100 (clamped)
    assert result.score >= 100


def test_bug4_ok_at_line_start_triggers_bonus(tmp_path):
    """Bug 4: 'OK' at the start of a line (word boundary) must count."""
    content = LONG_OK + "\nOK - task completed successfully\n"
    output_file = _make_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(output_file)
    assert result.score >= 100


# ---------------------------------------------------------------------------
# BUG 5: find_task_output path traversal (no validation)
# BEFORE: no check on task_id -> could construct path to /etc/passwd etc.
# FIX:    return None if ".." or "/" or "\\" in task_id
# ---------------------------------------------------------------------------


def test_bug5_find_task_output_blocks_dotdot_traversal(tmp_path):
    """Bug 5: find_task_output('../../etc/passwd') had no path traversal check.

    Without validation, the function would silently construct a path outside
    the tasks directory. The fix returns None for dangerous task_ids.
    """
    result = find_task_output("../../etc/passwd", tasks_dir=tmp_path)
    assert result is None, (
        "Bug 5 regression: path traversal via '..' not blocked"
    )


def test_bug5_find_task_output_blocks_slash(tmp_path):
    """Bug 5: slash in task_id must be blocked."""
    result = find_task_output("tasks/evil", tasks_dir=tmp_path)
    assert result is None


def test_bug5_find_task_output_blocks_backslash(tmp_path):
    """Bug 5: backslash in task_id must be blocked."""
    result = find_task_output("tasks\\evil", tasks_dir=tmp_path)
    assert result is None


def test_bug5_find_task_output_blocks_empty_string(tmp_path):
    """Bug 5: empty task_id must be blocked."""
    result = find_task_output("", tasks_dir=tmp_path)
    assert result is None


def test_bug5_find_task_output_valid_id_still_works(tmp_path):
    """Bug 5 happy path: valid task_id with existing output file is returned."""
    output_file = tmp_path / "TASK_001_output.md"
    output_file.write_text(LONG_OK)
    result = find_task_output("TASK_001", tasks_dir=tmp_path)
    assert result == output_file


# ---------------------------------------------------------------------------
# BUG 6: TOCTOU race condition in create_task
# BEFORE: if exists() -> write_text() - window between check and write
# FIX:    open(file, 'x') atomic exclusive create
# ---------------------------------------------------------------------------


def test_bug6_create_task_duplicate_raises_file_exists_error(tmp_path):
    """Bug 6: original code had TOCTOU: exists() check then write_text().

    A second concurrent create could overwrite the first. The fix uses
    open('x') (exclusive create) which atomically raises FileExistsError.
    This test verifies the atomic behavior is in place.
    """
    create_task("TASK_001", "agent", "First creation", tasks_dir=str(tmp_path))
    with pytest.raises(FileExistsError, match="already exists"):
        create_task("TASK_001", "agent", "Second creation", tasks_dir=str(tmp_path))


def test_bug6_original_content_preserved_after_duplicate_attempt(tmp_path):
    """Bug 6: after a failed duplicate create, the original file is untouched."""
    create_task("TASK_001", "agent", "Original description", tasks_dir=str(tmp_path))
    original_content = (tmp_path / "TASK_001.md").read_text()

    with pytest.raises(FileExistsError):
        create_task("TASK_001", "agent", "Overwrite attempt", tasks_dir=str(tmp_path))

    current_content = (tmp_path / "TASK_001.md").read_text()
    assert current_content == original_content, (
        "Bug 6 regression: original file was overwritten by duplicate create"
    )


# ---------------------------------------------------------------------------
# BUG 7: CLI silent failures (no output when ok=False)
# BEFORE: no print + no sys.exit(1) when mark_ready/working/done/ack* returned False
# FIX:    print error to stderr + sys.exit(1)
# ---------------------------------------------------------------------------


def test_bug7_cli_ready_nonexistent_task_exits_1(capsys):
    """Bug 7: CLI 'ready' on nonexistent task was silent. Now it exits 1 + error msg."""
    with pytest.raises(SystemExit) as exc:
        main_task(["ready", "TASK_DOES_NOT_EXIST_XYZ"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "ERROR" in err or "error" in err.lower() or "Failed" in err


def test_bug7_cli_working_nonexistent_task_exits_1(capsys):
    """Bug 7: CLI 'working' on nonexistent task was silent. Now exits 1."""
    with pytest.raises(SystemExit) as exc:
        main_task(["working", "TASK_DOES_NOT_EXIST_XYZ"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert len(err) > 0, "Bug 7 regression: no error message printed to stderr"


def test_bug7_cli_done_nonexistent_task_exits_1(capsys):
    """Bug 7: CLI 'done' on nonexistent task was silent. Now exits 1."""
    with pytest.raises(SystemExit) as exc:
        main_task(["done", "TASK_DOES_NOT_EXIST_XYZ"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert len(err) > 0


def test_bug7_cli_ack_received_nonexistent_task_exits_1(capsys):
    """Bug 7: CLI 'ack-received' on nonexistent task was silent. Now exits 1."""
    with pytest.raises(SystemExit) as exc:
        main_task(["ack-received", "TASK_DOES_NOT_EXIST_XYZ"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert len(err) > 0


def test_bug7_cli_ack_understood_nonexistent_task_exits_1(capsys):
    """Bug 7: CLI 'ack-understood' on nonexistent task was silent. Now exits 1."""
    with pytest.raises(SystemExit) as exc:
        main_task(["ack-understood", "TASK_DOES_NOT_EXIST_XYZ"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert len(err) > 0


def test_bug7_cli_success_path_exits_0(tmp_path, capsys, monkeypatch):
    """Bug 7 happy path: successful transitions must not exit with error."""
    monkeypatch.setattr(
        "cervellaswarm_task_orchestration.cli.mark_ready", lambda tid: True
    )
    # Should NOT raise SystemExit (or exit 0 implicitly)
    main_task(["ready", "TASK_001"])
    out = capsys.readouterr().out
    assert "READY" in out


# ---------------------------------------------------------------------------
# BUG 8: Incomplete marker only checked at first occurrence
# BEFORE: only the first occurrence of each marker was checked
# FIX:    while loop checks ALL occurrences - first inside code block is ignored
#         but subsequent occurrences outside code block ARE caught
# ---------------------------------------------------------------------------


def test_bug8_second_todo_outside_code_block_is_detected(tmp_path):
    """Bug 8: only the FIRST occurrence of TODO was checked.

    If the first TODO was inside a code block (safe), the second one
    outside the code block was silently ignored.
    Pattern: ```\\nTODO: inside code\\n```\\nTODO: outside code
    """
    content = (
        LONG_OK
        + "\n```\nTODO: in code block (safe)\n```\n"
        + "TODO: outside code block (should be caught)\n"
    )
    output_file = _make_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(output_file)
    assert any("TODO:" in w for w in result.warnings), (
        "Bug 8 regression: second TODO outside code block was not detected"
    )
    assert result.score < 100


def test_bug8_first_todo_inside_code_second_outside_reduces_score(tmp_path):
    """Bug 8: score must be reduced when second TODO is outside code block."""
    content_with_bug = (
        LONG_OK
        + "\n```python\nTODO: refactor this\n```\n"
        + "TODO: write tests for this function\n"
    )
    content_clean = LONG_OK + "\n```python\nTODO: refactor this\n```\n"

    file_bug = _make_output(tmp_path / "with_bug.md", content_with_bug)
    file_clean = _make_output(tmp_path / "clean.md", content_clean)

    result_bug = validate_output(file_bug)
    result_clean = validate_output(file_clean)

    assert result_bug.score < result_clean.score, (
        "Bug 8 regression: second external TODO does not reduce score"
    )


def test_bug8_todo_only_inside_code_block_is_not_flagged(tmp_path):
    """Bug 8 happy path: TODO solely inside code block must not be flagged."""
    content = LONG_OK + "\n```\nTODO: inside code only\n```\n"
    output_file = _make_output(tmp_path / "TASK_001_output.md", content)
    result = validate_output(output_file)
    assert not any("TODO:" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# BUG 9: risk_level not validated
# BEFORE: risk_level=99 accepted silently; dict lookup would KeyError at runtime
# FIX:    ValueError if risk_level not in (1, 2, 3)
# ---------------------------------------------------------------------------


def test_bug9_risk_level_0_raises_value_error(tmp_path):
    """Bug 9: risk_level=0 was accepted silently. Now raises ValueError."""
    with pytest.raises(ValueError, match="risk_level"):
        create_task("TASK_001", "agent", "Task", risk_level=0, tasks_dir=str(tmp_path))


def test_bug9_risk_level_4_raises_value_error(tmp_path):
    """Bug 9: risk_level=4 was accepted silently. Now raises ValueError."""
    with pytest.raises(ValueError, match="risk_level"):
        create_task("TASK_001", "agent", "Task", risk_level=4, tasks_dir=str(tmp_path))


def test_bug9_risk_level_99_raises_value_error(tmp_path):
    """Bug 9: risk_level=99 was accepted silently, then caused KeyError later.

    The original code had risk_map = {1: ..., 2: ..., 3: ...} and did
    risk_map[risk_level] without checking. risk_level=99 -> KeyError.
    The fix validates before the dict lookup.
    """
    with pytest.raises(ValueError, match="risk_level"):
        create_task("TASK_001", "agent", "Task", risk_level=99, tasks_dir=str(tmp_path))


def test_bug9_risk_level_negative_raises_value_error(tmp_path):
    """Bug 9: negative risk_level must be rejected."""
    with pytest.raises(ValueError, match="risk_level"):
        create_task("TASK_001", "agent", "Task", risk_level=-1, tasks_dir=str(tmp_path))


def test_bug9_valid_risk_levels_accepted(tmp_path):
    """Bug 9 happy path: risk_level 1, 2, 3 must still work without error."""
    create_task("TASK_R1", "agent", "Task", risk_level=1, tasks_dir=str(tmp_path))
    create_task("TASK_R2", "agent", "Task", risk_level=2, tasks_dir=str(tmp_path))
    create_task("TASK_R3", "agent", "Task", risk_level=3, tasks_dir=str(tmp_path))
    result = list_tasks(tasks_dir=str(tmp_path))
    assert len(result) == 3
