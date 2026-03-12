# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for C3.5: .lu example files, showcase_v2, error codes, REPL demo.

Test organization:
  - test_lu_files_*    -- parse/compile/run validation of .lu examples
  - test_showcase_*    -- showcase_v2 sections run without error
  - test_error_codes_* -- new LU-N013/LU-N014 error codes
  - test_repl_demo_*   -- REPL automated session
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale import (
    check_file,
    check_source,
    run_file,
    verify_file,
    REPLSession,
)
from cervellaswarm_lingua_universale.errors import humanize, format_error
from cervellaswarm_lingua_universale._parser import ParseError

EXAMPLES = Path(__file__).parent.parent / "examples"


# ============================================================
# .lu file parse/compile tests
# ============================================================


class TestLuFilesParse:
    """All valid .lu files must parse and compile without error."""

    @pytest.mark.parametrize("name", ["hello.lu", "confidence.lu", "multiagent.lu", "ricette.lu"])
    def test_check_file_ok(self, name: str) -> None:
        result = check_file(EXAMPLES / name)
        assert result.ok, f"{name} failed: {result.errors}"
        assert result.compiled is not None
        assert result.python_source is not None

    @pytest.mark.parametrize("name", ["hello.lu", "confidence.lu", "multiagent.lu", "ricette.lu"])
    def test_run_file_ok(self, name: str) -> None:
        result = run_file(EXAMPLES / name)
        assert result.ok, f"{name} run failed: {result.errors}"
        assert result.module is not None

    @pytest.mark.parametrize("name", ["hello.lu", "confidence.lu", "ricette.lu"])
    def test_verify_file_ok(self, name: str) -> None:
        result = verify_file(EXAMPLES / name)
        assert result.ok, f"{name} verify failed: {result.errors}"

    def test_verify_multiagent_has_property_reports(self) -> None:
        """multiagent.lu has property violations (all_roles_participate)."""
        result = verify_file(EXAMPLES / "multiagent.lu")
        assert result.compiled is not None
        assert len(result.verification) > 0
        assert result.property_reports

    def test_errors_lu_fails(self) -> None:
        """errors.lu must fail compilation with a meaningful error."""
        result = check_file(EXAMPLES / "errors.lu")
        assert not result.ok
        assert len(result.errors) > 0
        assert "legendary" in result.errors[0].lower() or "trust" in result.errors[0].lower()


class TestLuFilesContent:
    """Validate specific declarations in compiled .lu files."""

    def test_hello_declarations(self) -> None:
        result = check_file(EXAMPLES / "hello.lu")
        assert result.ok
        c = result.compiled
        assert c.types == ("TaskStatus",)
        assert c.agents == ("Worker",)
        assert c.protocols == ("DelegateTask",)

    def test_confidence_declarations(self) -> None:
        result = check_file(EXAMPLES / "confidence.lu")
        assert result.ok
        c = result.compiled
        assert "AnalysisStatus" in c.types
        assert "AnalysisResult" in c.types
        assert "Analyst" in c.agents
        assert "Reviewer" in c.agents
        assert "ConfidenceReview" in c.protocols

    def test_multiagent_declarations(self) -> None:
        result = check_file(EXAMPLES / "multiagent.lu")
        assert result.ok
        c = result.compiled
        assert "Priority" in c.types
        assert "DeploymentPlan" in c.types
        assert "DeploymentResult" in c.types
        assert "Architect" in c.agents
        assert "Builder" in c.agents
        assert "Guardian" in c.agents
        assert "DeployPipeline" in c.protocols
        assert "datetime" in c.imports

    def test_ricette_declarations(self) -> None:
        result = check_file(EXAMPLES / "ricette.lu")
        assert result.ok
        c = result.compiled
        assert "Category" in c.types
        assert "Recipe" in c.types
        assert "SearchResult" in c.types
        assert "RecipeManager" in c.agents
        assert "QualityChecker" in c.agents
        assert "AddRecipe" in c.protocols

    def test_hello_agent_metadata(self) -> None:
        """Agent metadata survives compilation + execution."""
        result = run_file(EXAMPLES / "hello.lu")
        assert result.ok
        mod = result.module
        worker_cls = getattr(mod, "Worker")
        inst = worker_cls()
        assert inst.__lu_role__ == "backend"
        assert inst.__lu_trust__ == "standard"

    def test_confidence_record_type(self) -> None:
        """Record types generate dataclass with correct fields."""
        result = run_file(EXAMPLES / "confidence.lu")
        assert result.ok
        mod = result.module
        cls = getattr(mod, "AnalysisResult")
        # Verify it's a dataclass with expected fields
        import dataclasses
        assert dataclasses.is_dataclass(cls)
        field_names = {f.name for f in dataclasses.fields(cls)}
        assert "summary" in field_names
        assert "score" in field_names
        assert "details" in field_names
        assert "status" in field_names


# ============================================================
# Error code tests (LU-N013, LU-N014)
# ============================================================


class TestErrorCodes:
    """Test new error codes for invalid trust/confidence values."""

    def test_lu_n013_invalid_trust_tier(self) -> None:
        """LU-N013: invalid trust tier in agent declaration."""
        source = "agent X:\n    trust: legendary\n"
        result = check_source(source)
        assert not result.ok
        assert "LU-N013" in result.errors[0]
        assert "legendary" in result.errors[0]

    def test_lu_n013_suggests_valid_tiers(self) -> None:
        """LU-N013 hint includes valid tier names."""
        source = "agent X:\n    trust: legendary\n"
        result = check_source(source)
        assert not result.ok
        error_text = result.errors[0]
        assert "verified" in error_text or "trusted" in error_text

    def test_lu_n014_invalid_confidence_level(self) -> None:
        """LU-N014: invalid confidence level in protocol properties."""
        source = (
            "protocol P:\n"
            "    roles: a, b\n"
            "    a asks b to do task\n"
            "    properties:\n"
            "        confidence >= extreme\n"
        )
        result = check_source(source)
        assert not result.ok
        assert "LU-N014" in result.errors[0]
        assert "extreme" in result.errors[0]

    def test_lu_n013_humanize_direct(self) -> None:
        """Humanize ParseError with invalid trust tier directly."""
        exc = ParseError("invalid trust tier: 'awesome'. Valid: verified, trusted, standard, untrusted", line=5, col=10)
        herr = humanize(exc)
        assert herr.code == "LU-N013"
        assert "awesome" in format_error(herr)

    def test_lu_n014_humanize_direct(self) -> None:
        """Humanize ParseError with invalid confidence level directly."""
        exc = ParseError("invalid confidence level: 'mega'. Valid: certain, high, medium, low, speculative", line=3, col=5)
        herr = humanize(exc)
        assert herr.code == "LU-N014"
        assert "mega" in format_error(herr)

    def test_lu_n013_fuzzy_suggestion(self) -> None:
        """LU-N013 should suggest similar trust tiers."""
        source = "agent X:\n    trust: truested\n"
        result = check_source(source)
        assert not result.ok
        # "truested" is close to "trusted" -- should suggest it
        assert "trusted" in result.errors[0]

    def test_lu_n014_fuzzy_suggestion(self) -> None:
        """LU-N014 should suggest similar confidence levels."""
        source = (
            "protocol P:\n"
            "    roles: a, b\n"
            "    a asks b to do task\n"
            "    properties:\n"
            "        confidence >= higgh\n"
        )
        result = check_source(source)
        assert not result.ok
        # "higgh" is close to "high" -- should suggest it
        assert "high" in result.errors[0]


# ============================================================
# REPL demo tests
# ============================================================


class TestReplDemo:
    """Test REPL automated session as used by showcase_v2."""

    def test_repl_type_definition(self) -> None:
        inputs = iter(["type X = A | B", ":quit"])
        outputs: list[str] = []
        session = REPLSession(
            input_fn=lambda p: next(inputs),
            output_fn=lambda *a: outputs.append(" ".join(str(x) for x in a)),
        )
        session.run()
        combined = "\n".join(outputs)
        assert "OK" in combined
        assert "1 type(s)" in combined

    def test_repl_check_command(self) -> None:
        inputs = iter([":check type Y = P | Q", ":quit"])
        outputs: list[str] = []
        session = REPLSession(
            input_fn=lambda p: next(inputs),
            output_fn=lambda *a: outputs.append(" ".join(str(x) for x in a)),
        )
        session.run()
        combined = "\n".join(outputs)
        assert "OK" in combined

    def test_repl_history_shows_entries(self) -> None:
        inputs = iter(["type Z = M | N", ":history", ":quit"])
        outputs: list[str] = []
        session = REPLSession(
            input_fn=lambda p: next(inputs),
            output_fn=lambda *a: outputs.append(" ".join(str(x) for x in a)),
        )
        session.run()
        combined = "\n".join(outputs)
        assert "type Z = M | N" in combined

    def test_repl_error_on_bad_input(self) -> None:
        # Feed multiline agent block with bad trust, then empty line to execute
        inputs = iter([
            "agent X:",        # starts block (colon at end)
            "    trust: nope", # bad trust tier
            "",                # empty line -> execute
            ":quit",
        ])
        outputs: list[str] = []
        session = REPLSession(
            input_fn=lambda p: next(inputs),
            output_fn=lambda *a: outputs.append(" ".join(str(x) for x in a)),
        )
        session.run()
        combined = "\n".join(outputs)
        # Must show the specific trust tier error
        assert "LU-N013" in combined or "nope" in combined.lower()


# ============================================================
# Showcase v2 integration test
# ============================================================


class TestShowcaseV2:
    """Test that showcase_v2.py runs without errors."""

    def test_showcase_v2_main(self) -> None:
        """Import and run showcase_v2.main() -- must return 0."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "showcase_v2", EXAMPLES / "showcase_v2.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        # Set NO_COLOR to avoid terminal issues in test
        old = os.environ.get("NO_COLOR")
        os.environ["NO_COLOR"] = "1"
        try:
            spec.loader.exec_module(mod)
            result = mod.main()
            assert result == 0
        finally:
            if old is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = old

    def test_showcase_v1_still_works(self) -> None:
        """Original showcase.py must still run without errors."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "showcase", EXAMPLES / "showcase.py",
        )
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        old = os.environ.get("NO_COLOR")
        os.environ["NO_COLOR"] = "1"
        try:
            spec.loader.exec_module(mod)
            mod.main()  # No explicit return, just must not raise
        finally:
            if old is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = old
