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

    def test_frozen(self) -> None:
        r = EvalResult(ok=True, source_file="test.lu")
        with pytest.raises(AttributeError):
            r.ok = False  # type: ignore[misc]


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


# ============================================================
# T3.4: Property verification in verify_source (S444)
# ============================================================


class TestVerifyProperties:
    """Tests for static property checking in verify_source."""

    def test_verify_proves_basic_properties(self) -> None:
        """Protocol with basic properties should show PROVED."""
        src = """\
protocol Safe:
    roles: user, system

    user asks system to do task
    system returns result to user

    properties:
        always terminates
        no deadlock
        no deletion
        all roles participate
"""
        r = verify_source(src)
        assert r.ok is True
        assert r.property_reports
        report = r.property_reports[0]
        assert report.protocol_name == "Safe"
        assert len(report.results) == 4
        for result in report.results:
            assert result.verdict.name == "PROVED"

    def test_verify_no_properties(self) -> None:
        """Protocol without properties should still verify OK."""
        src = """\
protocol NoProps:
    roles: a, b

    a asks b to do task
"""
        r = verify_source(src)
        assert r.ok is True
        assert any("No properties" in line for line in r.verification)

    def test_verify_violated_all_roles_participate(self) -> None:
        """Protocol with unused roles should VIOLATE all_roles_participate."""
        src = """\
protocol Broken:
    roles: alice, bob, charlie

    alice asks bob to do task
    bob returns result to alice

    properties:
        all roles participate
"""
        r = verify_source(src)
        assert r.ok is False
        report = r.property_reports[0]
        assert report.results[0].verdict.name == "VIOLATED"
        assert "charlie" in report.results[0].evidence

    def test_verify_ordering_skipped_for_role_names(self) -> None:
        """ORDERING with role names (not MessageKind) is SKIPPED."""
        src = """\
protocol Order:
    roles: a, b

    a asks b to do task

    properties:
        a before b
"""
        r = verify_source(src)
        assert r.ok is True
        report = r.property_reports[0]
        assert report.results[0].verdict.name == "SKIPPED"

    def test_verify_confidence_skipped(self) -> None:
        """CONFIDENCE_MIN is runtime-only, should be SKIPPED."""
        src = """\
protocol Conf:
    roles: a, b

    a asks b to do task

    properties:
        confidence >= high
"""
        r = verify_source(src)
        assert r.ok is True
        report = r.property_reports[0]
        assert report.results[0].verdict.name == "SKIPPED"

    def test_verify_mixed_results(self) -> None:
        """Mix of PROVED and VIOLATED properties."""
        src = """\
protocol Mixed:
    roles: a, b, c

    a asks b to do task

    properties:
        always terminates
        all roles participate
"""
        r = verify_source(src)
        assert r.ok is False
        report = r.property_reports[0]
        assert report.results[0].verdict.name == "PROVED"
        assert report.results[1].verdict.name == "VIOLATED"

    def test_verify_no_deletion_proved(self) -> None:
        """no_deletion property should be PROVED for safe protocol."""
        src = """\
protocol DataSafe:
    roles: user, db

    user asks db to do task
    db returns result to user

    properties:
        no deletion
"""
        r = verify_source(src)
        assert r.ok is True
        report = r.property_reports[0]
        assert report.results[0].verdict.name == "PROVED"
        assert report.results[0].spec.kind.value == "no_deletion"

    def test_verify_role_exclusive_skipped(self) -> None:
        """ROLE_EXCLUSIVE with identifier names is SKIPPED."""
        src = """\
protocol Audit:
    roles: auditor, system

    auditor tells system verdict

    properties:
        auditor exclusive verdict
"""
        r = verify_source(src)
        assert r.ok is True
        report = r.property_reports[0]
        assert report.results[0].verdict.name == "SKIPPED"

    def test_verify_all_nine_properties(self) -> None:
        """Verify protocol with all 9 property kinds and expected verdicts."""
        src = """\
protocol Full:
    roles: a, b

    a asks b to do task
    b returns result to a

    properties:
        always terminates
        no deadlock
        no deletion
        all roles participate
        confidence >= medium
        trust >= standard
        a before b
        b cannot send audit
        a exclusive review
"""
        r = verify_source(src)
        assert r.property_reports
        report = r.property_reports[0]
        assert len(report.results) == 9
        # Build kind→verdict map for precise assertions
        kind_verdict = {
            res.spec.kind.value: res.verdict.name for res in report.results
        }
        # Structural properties: PROVED for well-formed 2-role protocol
        assert kind_verdict["always_terminates"] == "PROVED"
        assert kind_verdict["no_deadlock"] == "PROVED"
        assert kind_verdict["no_deletion"] == "PROVED"
        assert kind_verdict["all_roles_participate"] == "PROVED"
        # Runtime-only: confidence is SKIPPED, trust is statically checkable
        assert kind_verdict["confidence_min"] == "SKIPPED"
        assert kind_verdict["trust_min"] == "PROVED"
        # Identifier-name params: SKIPPED (not resolvable to MessageKind)
        assert kind_verdict["ordering"] == "SKIPPED"
        assert kind_verdict["exclusion"] == "SKIPPED"
        assert kind_verdict["role_exclusive"] == "SKIPPED"

    def test_verify_choice_node_protocol(self) -> None:
        """Protocol with choice branches should include branch steps in checking."""
        src = """\
protocol WithChoice:
    roles: manager, worker, auditor

    manager asks worker to do task
    when manager decides:
        approve:
            worker returns result to manager
            manager asks auditor to verify
        reject:
            manager tells worker rejection

    properties:
        all roles participate
"""
        r = verify_source(src)
        assert r.property_reports
        report = r.property_reports[0]
        assert report.protocol_name == "WithChoice"
        # All 3 roles appear across branches, so should PROVE
        assert report.results[0].verdict.name == "PROVED"

    def test_verify_output_format(self) -> None:
        """Verification output contains expected format."""
        src = """\
protocol Fmt:
    roles: a, b

    a asks b to do task

    properties:
        always terminates
"""
        r = verify_source(src)
        assert any("[1/1]" in line for line in r.verification)
        assert any("PROVED" in line for line in r.verification)
        assert any("PASSED" in line for line in r.verification)

    def test_verify_multiple_protocols(self) -> None:
        """File with 2 protocols gets 2 property reports."""
        src = """\
protocol First:
    roles: a, b

    a asks b to do task

    properties:
        always terminates

protocol Second:
    roles: x, y

    x asks y to do task

    properties:
        no deadlock
"""
        r = verify_source(src)
        assert len(r.property_reports) == 2
        assert r.property_reports[0].protocol_name == "First"
        assert r.property_reports[1].protocol_name == "Second"
