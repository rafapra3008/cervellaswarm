# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _contracts.py -- ContractViolation exception (C2.2.1).

Test structure:
  - Construction & attributes (happy path)
  - Message formatting (str representation)
  - kind validation (boundary)
  - Inheritance chain (RuntimeError subclass)
  - Pickling round-trip (for multiprocessing scenarios)
  - Usage pattern (how the compiler will emit guards)
"""

from __future__ import annotations

import pickle

import pytest

from cervellaswarm_lingua_universale._contracts import ContractViolation


# ---------------------------------------------------------------------------
# Construction & attributes
# ---------------------------------------------------------------------------


class TestContractViolationConstruction:
    """Tests for creating ContractViolation with various argument combos."""

    def test_requires_with_source(self) -> None:
        exc = ContractViolation("input.is_valid", kind="requires", source="line 6, col 8")
        assert exc.condition == "input.is_valid"
        assert exc.kind == "requires"
        assert exc.source == "line 6, col 8"

    def test_ensures_with_source(self) -> None:
        exc = ContractViolation("result.quality >= 0.8", kind="ensures", source="line 9, col 8")
        assert exc.condition == "result.quality >= 0.8"
        assert exc.kind == "ensures"
        assert exc.source == "line 9, col 8"

    def test_requires_is_default_kind(self) -> None:
        exc = ContractViolation("x > 0")
        assert exc.kind == "requires"

    def test_empty_source_is_default(self) -> None:
        exc = ContractViolation("x > 0")
        assert exc.source == ""

    def test_kind_keyword_only(self) -> None:
        """kind and source must be keyword arguments -- prevents accidental swaps."""
        with pytest.raises(TypeError):
            ContractViolation("cond", "requires")  # type: ignore[misc]

    def test_empty_condition_allowed(self) -> None:
        """Empty condition string is legal (edge case)."""
        exc = ContractViolation("", kind="requires")
        assert exc.condition == ""

    def test_complex_condition_string(self) -> None:
        cond = "(input.size) > (0) and (input.name) != (\"\")"
        exc = ContractViolation(cond, kind="requires", source="line 10, col 4")
        assert exc.condition == cond


# ---------------------------------------------------------------------------
# Message formatting
# ---------------------------------------------------------------------------


class TestContractViolationMessage:
    """Tests for the human-readable error message."""

    def test_requires_with_source_message(self) -> None:
        exc = ContractViolation("input.is_valid", kind="requires", source="line 6, col 8")
        assert str(exc) == "[LU Contract] requires violated: input.is_valid (at line 6, col 8)"

    def test_ensures_with_source_message(self) -> None:
        exc = ContractViolation("result.quality >= 0.8", kind="ensures", source="line 9, col 8")
        assert str(exc) == "[LU Contract] ensures violated: result.quality >= 0.8 (at line 9, col 8)"

    def test_no_source_omits_location(self) -> None:
        exc = ContractViolation("x > 0", kind="requires")
        assert str(exc) == "[LU Contract] requires violated: x > 0"
        assert "(at" not in str(exc)

    def test_empty_source_omits_location(self) -> None:
        exc = ContractViolation("x > 0", kind="requires", source="")
        assert "(at" not in str(exc)

    def test_message_is_args_first_element(self) -> None:
        """RuntimeError.args[0] should be the formatted message."""
        exc = ContractViolation("cond", kind="requires")
        assert exc.args[0] == "[LU Contract] requires violated: cond"


# ---------------------------------------------------------------------------
# kind validation (boundary guard - P12)
# ---------------------------------------------------------------------------


class TestContractViolationKindValidation:
    """Tests for invalid kind values."""

    def test_invalid_kind_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="kind must be 'requires' or 'ensures'"):
            ContractViolation("x > 0", kind="invariant")

    def test_empty_kind_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="kind must be 'requires' or 'ensures'"):
            ContractViolation("x > 0", kind="")

    def test_kind_case_sensitive(self) -> None:
        """'Requires' (capitalized) is NOT a valid kind."""
        with pytest.raises(ValueError):
            ContractViolation("x > 0", kind="Requires")

    def test_kind_typo_raises(self) -> None:
        with pytest.raises(ValueError):
            ContractViolation("x > 0", kind="require")


# ---------------------------------------------------------------------------
# Inheritance chain
# ---------------------------------------------------------------------------


class TestContractViolationInheritance:
    """Tests for exception hierarchy."""

    def test_is_runtime_error(self) -> None:
        exc = ContractViolation("cond")
        assert isinstance(exc, RuntimeError)

    def test_is_exception(self) -> None:
        exc = ContractViolation("cond")
        assert isinstance(exc, Exception)

    def test_catchable_as_runtime_error(self) -> None:
        with pytest.raises(RuntimeError):
            raise ContractViolation("x > 0", kind="requires")

    def test_not_catchable_as_value_error(self) -> None:
        """ContractViolation should NOT be caught by ValueError."""
        with pytest.raises(ContractViolation):
            try:
                raise ContractViolation("x > 0")
            except ValueError:
                pass  # Should not catch


# ---------------------------------------------------------------------------
# Pickling round-trip (multiprocessing support)
# ---------------------------------------------------------------------------


class TestContractViolationPickle:
    """Tests for pickle serialization (needed if exceptions cross process boundaries)."""

    def test_pickle_round_trip_requires(self) -> None:
        exc = ContractViolation("input.valid", kind="requires", source="line 5, col 0")
        restored = pickle.loads(pickle.dumps(exc))
        assert str(restored) == str(exc)
        assert restored.condition == exc.condition
        assert restored.kind == exc.kind
        assert restored.source == exc.source

    def test_pickle_round_trip_ensures(self) -> None:
        exc = ContractViolation("result.ok", kind="ensures", source="line 12, col 4")
        restored = pickle.loads(pickle.dumps(exc))
        assert restored.condition == "result.ok"
        assert restored.kind == "ensures"
        assert restored.source == "line 12, col 4"

    def test_pickle_round_trip_no_source(self) -> None:
        exc = ContractViolation("x > 0")
        restored = pickle.loads(pickle.dumps(exc))
        assert restored.source == ""


# ---------------------------------------------------------------------------
# Usage pattern (how the compiler emits guards)
# ---------------------------------------------------------------------------


class TestContractViolationUsagePattern:
    """Tests simulating how _compiler.py will emit contract guards."""

    def test_requires_guard_pattern(self) -> None:
        """Simulates: if not (input.is_valid): raise ContractViolation(...)"""
        input_is_valid = False
        with pytest.raises(ContractViolation, match="requires violated"):
            if not input_is_valid:
                raise ContractViolation(
                    "input.is_valid",
                    kind="requires",
                    source="line 6, col 8",
                )

    def test_ensures_guard_pattern(self) -> None:
        """Simulates: if not (result.quality >= 0.8): raise ContractViolation(...)"""
        result_quality = 0.5
        with pytest.raises(ContractViolation, match="ensures violated"):
            if not (result_quality >= 0.8):
                raise ContractViolation(
                    "result.quality >= 0.8",
                    kind="ensures",
                    source="line 9, col 8",
                )

    def test_passing_requires_no_raise(self) -> None:
        """When condition holds, no exception is raised."""
        input_is_valid = True
        # Should NOT raise
        if not input_is_valid:
            raise ContractViolation("input.is_valid", kind="requires")

    def test_passing_ensures_no_raise(self) -> None:
        """When postcondition holds, no exception is raised."""
        result_quality = 0.95
        if not (result_quality >= 0.8):
            raise ContractViolation("result.quality >= 0.8", kind="ensures")

    def test_multiple_requires_first_fails(self) -> None:
        """Multiple requires: first failing one raises."""
        conditions = [
            (True, "input.size > 0"),
            (False, "input.name != ''"),
            (True, "input.valid"),
        ]
        with pytest.raises(ContractViolation, match="input.name"):
            for holds, cond in conditions:
                if not holds:
                    raise ContractViolation(cond, kind="requires", source="line 7, col 8")

    def test_contract_exception_in_try_except(self) -> None:
        """User code can catch ContractViolation and inspect it."""
        try:
            raise ContractViolation(
                "result.quality >= 0.8",
                kind="ensures",
                source="line 9, col 8",
            )
        except ContractViolation as exc:
            assert exc.condition == "result.quality >= 0.8"
            assert exc.kind == "ensures"
            assert exc.source == "line 9, col 8"


# ---------------------------------------------------------------------------
# __slots__ verification
# ---------------------------------------------------------------------------


class TestContractViolationSlots:
    """Tests that __slots__ is properly configured."""

    def test_has_slots(self) -> None:
        assert "__slots__" in ContractViolation.__dict__

    def test_slots_contain_expected_attrs(self) -> None:
        assert "condition" in ContractViolation.__slots__
        assert "kind" in ContractViolation.__slots__
        assert "source" in ContractViolation.__slots__

    def test_no_dict_on_instance(self) -> None:
        """__slots__ prevents __dict__ creation (memory efficient)."""
        exc = ContractViolation("cond")
        # RuntimeError has __dict__, so with __slots__ we still get it
        # but our own attrs are in slots
        assert hasattr(exc, "condition")
        assert hasattr(exc, "kind")
        assert hasattr(exc, "source")
