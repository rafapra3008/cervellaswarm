# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _eval.py -- unified evaluation functions (C3.2)."""

from __future__ import annotations

import pytest
from pathlib import Path

from cervellaswarm_lingua_universale._eval import (
    EvalResult,
    check_source,
    check_file,
    verify_source,
    verify_file,
    run_source,
    run_file,
)


# ============================================================
# Fixtures
# ============================================================

_VALID_SOURCE = """\
type TaskStatus = Pending | Running | Done

agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: task.well_defined
    ensures: result.done

protocol DelegateTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
    properties:
        always terminates
        no deadlock
"""

_INVALID_SYNTAX = "protocol invalid syntax here"

_MINIMAL_PROTOCOL = """\
protocol Ping:
    roles: a, b
    a sends message to b
    b returns reply to a
"""

_TYPE_ONLY = "type Color = Red | Green | Blue"

_AGENT_ONLY = """\
agent Tester:
    role: tester
    trust: standard
    accepts: TestRequest
    produces: TestResult
"""


@pytest.fixture
def hello_lu(tmp_path: Path) -> Path:
    """Write a valid .lu file and return its path."""
    f = tmp_path / "hello.lu"
    f.write_text(_VALID_SOURCE, encoding="utf-8")
    return f


@pytest.fixture
def bad_lu(tmp_path: Path) -> Path:
    """Write an invalid .lu file and return its path."""
    f = tmp_path / "bad.lu"
    f.write_text(_INVALID_SYNTAX, encoding="utf-8")
    return f


# ============================================================
# EvalResult
# ============================================================


class TestEvalResult:
    """EvalResult dataclass is frozen and has correct defaults."""

    def test_ok_result(self) -> None:
        r = EvalResult(ok=True, source_file="test.lu")
        assert r.ok is True
        assert r.source_file == "test.lu"
        assert r.errors == []
        assert r.compiled is None
        assert r.module is None
        assert r.python_source is None
        assert r.verification == []

    def test_error_result(self) -> None:
        r = EvalResult(ok=False, source_file="bad.lu", errors=["parse error"])
        assert r.ok is False
        assert len(r.errors) == 1


# ============================================================
# check_source / check_file
# ============================================================


class TestCheckSource:
    """check_source: parse + compile without execution."""

    def test_valid_source(self) -> None:
        r = check_source(_VALID_SOURCE)
        assert r.ok is True
        assert r.errors == []
        assert r.compiled is not None
        assert r.python_source is not None
        assert "TaskStatus" in r.python_source

    def test_invalid_syntax(self) -> None:
        r = check_source(_INVALID_SYNTAX)
        assert r.ok is False
        assert len(r.errors) >= 1
        assert r.compiled is None

    def test_minimal_protocol(self) -> None:
        r = check_source(_MINIMAL_PROTOCOL)
        assert r.ok is True
        assert r.compiled is not None
        assert "Ping" in r.compiled.protocols

    def test_type_only(self) -> None:
        r = check_source(_TYPE_ONLY)
        assert r.ok is True
        assert r.compiled is not None
        assert "Color" in r.compiled.types

    def test_agent_only(self) -> None:
        r = check_source(_AGENT_ONLY)
        assert r.ok is True
        assert r.compiled is not None
        assert "Tester" in r.compiled.agents

    def test_empty_source(self) -> None:
        r = check_source("")
        assert r.ok is True

    def test_custom_source_file(self) -> None:
        r = check_source(_TYPE_ONLY, source_file="custom.lu")
        assert r.source_file == "custom.lu"


class TestCheckFile:
    """check_file: read file + parse + compile."""

    def test_valid_file(self, hello_lu: Path) -> None:
        r = check_file(hello_lu)
        assert r.ok is True
        assert r.compiled is not None

    def test_invalid_file(self, bad_lu: Path) -> None:
        r = check_file(bad_lu)
        assert r.ok is False
        assert len(r.errors) >= 1

    def test_nonexistent_file(self) -> None:
        r = check_file("/nonexistent/path/file.lu")
        assert r.ok is False
        assert len(r.errors) >= 1

    def test_source_file_in_result(self, hello_lu: Path) -> None:
        r = check_file(hello_lu)
        assert str(hello_lu) in r.source_file


# ============================================================
# verify_source / verify_file
# ============================================================


class TestVerifySource:
    """verify_source: parse + compile + Lean 4 bridge."""

    def test_valid_with_protocol(self) -> None:
        r = verify_source(_VALID_SOURCE)
        assert r.ok is True
        assert len(r.verification) >= 1
        # Should mention the protocol name
        assert any("DelegateTask" in line for line in r.verification)

    def test_valid_no_protocol(self) -> None:
        r = verify_source(_TYPE_ONLY)
        assert r.ok is True
        assert any("No protocol" in line for line in r.verification)

    def test_invalid_syntax(self) -> None:
        r = verify_source(_INVALID_SYNTAX)
        assert r.ok is False
        assert r.verification == []

    def test_lean4_source_generated(self) -> None:
        r = verify_source(_MINIMAL_PROTOCOL)
        assert r.ok is True
        assert any("Lean 4 source generated" in line for line in r.verification)


class TestVerifyFile:
    """verify_file: file I/O + verify."""

    def test_valid_file(self, hello_lu: Path) -> None:
        r = verify_file(hello_lu)
        assert r.ok is True
        assert len(r.verification) >= 1

    def test_nonexistent_file(self) -> None:
        r = verify_file("/nonexistent/path/file.lu")
        assert r.ok is False


# ============================================================
# run_source / run_file
# ============================================================


class TestRunSource:
    """run_source: parse + compile + execute."""

    def test_valid_source(self) -> None:
        r = run_source(_VALID_SOURCE)
        assert r.ok is True
        assert r.module is not None
        assert hasattr(r.module, "TaskStatus")
        assert hasattr(r.module, "Worker")

    def test_invalid_syntax(self) -> None:
        r = run_source(_INVALID_SYNTAX)
        assert r.ok is False
        assert r.module is None

    def test_type_only(self) -> None:
        r = run_source(_TYPE_ONLY)
        assert r.ok is True
        assert r.module is not None
        assert hasattr(r.module, "Color")

    def test_minimal_protocol(self) -> None:
        r = run_source(_MINIMAL_PROTOCOL)
        assert r.ok is True
        assert r.module is not None

    def test_python_source_present(self) -> None:
        r = run_source(_VALID_SOURCE)
        assert r.python_source is not None


class TestRunFile:
    """run_file: file I/O + run."""

    def test_valid_file(self, hello_lu: Path) -> None:
        r = run_file(hello_lu)
        assert r.ok is True
        assert r.module is not None

    def test_nonexistent_file(self) -> None:
        r = run_file("/nonexistent/path/file.lu")
        assert r.ok is False
        assert r.module is None

    def test_invalid_file(self, bad_lu: Path) -> None:
        r = run_file(bad_lu)
        assert r.ok is False
