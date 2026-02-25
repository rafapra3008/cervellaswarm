# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for prompt_builder module."""

import pytest

from cervellaswarm_spawn_workers.prompt_builder import (
    SPECIALTIES,
    build_base_prompt,
    build_worker_prompt,
)


# ---------------------------------------------------------------------------
# SPECIALTIES dict
# ---------------------------------------------------------------------------


def test_specialties_count():
    """SPECIALTIES contains exactly 10 entries."""
    assert len(SPECIALTIES) == 10


def test_specialties_expected_keys():
    """SPECIALTIES has all expected specialty keys."""
    expected = {
        "backend",
        "frontend",
        "tester",
        "docs",
        "devops",
        "data",
        "security",
        "researcher",
        "reviewer",
        "generic",
    }
    assert set(SPECIALTIES.keys()) == expected


def test_specialties_all_values_non_empty():
    """All SPECIALTIES values are non-empty strings."""
    for key, value in SPECIALTIES.items():
        assert isinstance(value, str), f"Specialty '{key}' value is not a string"
        assert value.strip(), f"Specialty '{key}' has an empty description"


# ---------------------------------------------------------------------------
# build_base_prompt()
# ---------------------------------------------------------------------------


def test_base_prompt_contains_worker_mode_header():
    """build_base_prompt returns string containing WORKER MODE header."""
    result = build_base_prompt()
    assert "WORKER MODE" in result


def test_base_prompt_default_tasks_dir():
    """build_base_prompt uses default tasks_dir when none provided."""
    result = build_base_prompt()
    assert ".swarm/tasks" in result


def test_base_prompt_custom_tasks_dir():
    """build_base_prompt uses custom tasks_dir when provided."""
    result = build_base_prompt(tasks_dir="/tmp/custom/tasks")
    assert "/tmp/custom/tasks" in result
    assert ".swarm/tasks" not in result


def test_base_prompt_contains_ready_marker():
    """build_base_prompt mentions .ready marker file."""
    result = build_base_prompt()
    assert ".ready" in result


def test_base_prompt_contains_working_marker():
    """build_base_prompt mentions .working marker file."""
    result = build_base_prompt()
    assert ".working" in result


def test_base_prompt_contains_done_marker():
    """build_base_prompt mentions .done marker file."""
    result = build_base_prompt()
    assert ".done" in result


def test_base_prompt_contains_exit_instruction():
    """build_base_prompt mentions /exit termination command."""
    result = build_base_prompt()
    assert "/exit" in result


def test_base_prompt_returns_string():
    """build_base_prompt always returns a string."""
    result = build_base_prompt()
    assert isinstance(result, str)


# ---------------------------------------------------------------------------
# build_worker_prompt()
# ---------------------------------------------------------------------------


def test_worker_prompt_contains_name_uppercased():
    """build_worker_prompt contains worker name uppercased."""
    result = build_worker_prompt("my-worker", "backend")
    assert "MY-WORKER" in result


def test_worker_prompt_contains_specialty_description():
    """build_worker_prompt contains specialty description."""
    result = build_worker_prompt("alpha", "backend")
    assert SPECIALTIES["backend"] in result


def test_worker_prompt_contains_base_prompt_content():
    """build_worker_prompt includes base prompt content (WORKER MODE header)."""
    result = build_worker_prompt("alpha", "backend")
    assert "WORKER MODE" in result


def test_worker_prompt_falls_back_to_generic_for_unknown_specialty():
    """build_worker_prompt falls back to generic description for unknown specialty."""
    result = build_worker_prompt("alpha", "nonexistent_specialty_xyz")
    assert SPECIALTIES["generic"] in result


def test_worker_prompt_uses_custom_tasks_dir():
    """build_worker_prompt passes tasks_dir to base prompt."""
    result = build_worker_prompt("alpha", "generic", tasks_dir="/opt/tasks")
    assert "/opt/tasks" in result


def test_worker_prompt_contains_assigned_to_instruction():
    """build_worker_prompt instructs worker to look for tasks assigned to 'name'."""
    result = build_worker_prompt("my-worker", "generic")
    assert "my-worker" in result


def test_worker_prompt_different_specialties():
    """build_worker_prompt uses the correct description for each specialty."""
    for key in SPECIALTIES:
        result = build_worker_prompt("test-worker", key)
        assert SPECIALTIES[key] in result


def test_worker_prompt_default_specialty_is_generic():
    """build_worker_prompt defaults to generic specialty."""
    result_default = build_worker_prompt("w")
    result_generic = build_worker_prompt("w", "generic")
    assert result_default == result_generic
