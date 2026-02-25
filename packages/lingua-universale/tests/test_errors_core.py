# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for errors.py core structures.

Covers: HumanError dataclass, ErrorCategory/ErrorSeverity enums,
ErrorLocation, _SafeDict behavior, format_error(), suggest_similar(),
DEFAULT_LOCALE/SUPPORTED_LOCALES constants, and __init__.py re-exports.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale.errors import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    ErrorCategory,
    ErrorLocation,
    ErrorSeverity,
    HumanError,
    _SafeDict,
    format_error,
    suggest_similar,
)


# ============================================================
# ErrorCategory
# ============================================================


class TestErrorCategory:
    """All 7 ErrorCategory values exist and are accessible."""

    def test_validation_value(self):
        assert ErrorCategory.VALIDATION.value == "validation"

    def test_protocol_value(self):
        assert ErrorCategory.PROTOCOL.value == "protocol"

    def test_parse_value(self):
        assert ErrorCategory.PARSE.value == "parse"

    def test_verification_value(self):
        assert ErrorCategory.VERIFICATION.value == "verification"

    def test_codegen_value(self):
        assert ErrorCategory.CODEGEN.value == "codegen"

    def test_confidence_value(self):
        assert ErrorCategory.CONFIDENCE.value == "confidence"

    def test_integration_value(self):
        assert ErrorCategory.INTEGRATION.value == "integration"

    def test_membership(self):
        """All 7 members are present."""
        members = {m.value for m in ErrorCategory}
        assert members == {
            "validation", "protocol", "parse",
            "verification", "codegen", "confidence", "integration",
        }


# ============================================================
# ErrorSeverity
# ============================================================


class TestErrorSeverity:
    """All 3 ErrorSeverity values exist and are accessible."""

    def test_error_value(self):
        assert ErrorSeverity.ERROR.value == "error"

    def test_warning_value(self):
        assert ErrorSeverity.WARNING.value == "warning"

    def test_info_value(self):
        assert ErrorSeverity.INFO.value == "info"

    def test_membership(self):
        members = {m.value for m in ErrorSeverity}
        assert members == {"error", "warning", "info"}


# ============================================================
# ErrorLocation
# ============================================================


class TestErrorLocation:
    """ErrorLocation is a frozen dataclass with optional fields."""

    def test_all_defaults_none(self):
        loc = ErrorLocation()
        assert loc.line is None
        assert loc.col is None
        assert loc.source is None

    def test_with_line_only(self):
        loc = ErrorLocation(line=5)
        assert loc.line == 5
        assert loc.col is None
        assert loc.source is None

    def test_with_all_fields(self):
        loc = ErrorLocation(line=10, col=3, source="spec")
        assert loc.line == 10
        assert loc.col == 3
        assert loc.source == "spec"

    def test_frozen_immutable(self):
        loc = ErrorLocation(line=1)
        with pytest.raises((AttributeError, TypeError)):
            loc.line = 99  # type: ignore[misc]

    def test_equality(self):
        loc1 = ErrorLocation(line=3, source="dsl")
        loc2 = ErrorLocation(line=3, source="dsl")
        assert loc1 == loc2


# ============================================================
# HumanError
# ============================================================


class TestHumanError:
    """HumanError is a frozen dataclass."""

    def _make_error(self, **overrides) -> HumanError:
        defaults = dict(
            code="LU-T001",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            locale="en",
            message="test message",
            suggestion="test suggestion",
            technical="original exception text",
        )
        defaults.update(overrides)
        return HumanError(**defaults)

    def test_basic_creation(self):
        err = self._make_error()
        assert err.code == "LU-T001"
        assert err.category == ErrorCategory.VALIDATION
        assert err.severity == ErrorSeverity.ERROR
        assert err.locale == "en"
        assert err.message == "test message"
        assert err.suggestion == "test suggestion"
        assert err.technical == "original exception text"

    def test_optional_defaults(self):
        err = self._make_error()
        assert err.location is None
        assert err.got is None
        assert err.expected is None
        assert err.similar == ()

    def test_with_location(self):
        loc = ErrorLocation(line=5, source="spec")
        err = self._make_error(location=loc)
        assert err.location == loc
        assert err.location.line == 5

    def test_with_got_expected(self):
        err = self._make_error(got="worker", expected="regina")
        assert err.got == "worker"
        assert err.expected == "regina"

    def test_with_similar(self):
        err = self._make_error(similar=("task_request", "task_result"))
        assert err.similar == ("task_request", "task_result")

    def test_frozen_immutable(self):
        err = self._make_error()
        with pytest.raises((AttributeError, TypeError)):
            err.code = "LU-X999"  # type: ignore[misc]

    def test_equality(self):
        err1 = self._make_error(code="LU-P001")
        err2 = self._make_error(code="LU-P001")
        assert err1 == err2

    def test_inequality_different_code(self):
        err1 = self._make_error(code="LU-P001")
        err2 = self._make_error(code="LU-P002")
        assert err1 != err2


# ============================================================
# _SafeDict
# ============================================================


class TestSafeDict:
    """_SafeDict returns '{key}' for missing keys."""

    def test_present_key_returns_value(self):
        d = _SafeDict({"name": "alice"})
        assert d["name"] == "alice"

    def test_missing_key_returns_placeholder(self):
        d = _SafeDict()
        assert d["missing_key"] == "{missing_key}"

    def test_format_map_no_keyerror(self):
        template = "Hello {name}, you have {count} messages."
        d = _SafeDict({"name": "bob"})
        result = template.format_map(d)
        assert "bob" in result
        assert "{count}" in result

    def test_format_map_all_keys_present(self):
        template = "Step {step}: got {got}."
        d = _SafeDict({"step": "3", "got": "worker"})
        result = template.format_map(d)
        assert result == "Step 3: got worker."

    def test_empty_dict_all_placeholders(self):
        template = "{a} + {b} = {c}"
        result = template.format_map(_SafeDict())
        assert result == "{a} + {b} = {c}"

    def test_inherits_from_dict(self):
        d = _SafeDict({"x": "1"})
        assert isinstance(d, dict)


# ============================================================
# suggest_similar
# ============================================================


class TestSuggestSimilar:
    """suggest_similar() uses difflib for fuzzy matching."""

    def test_exact_match(self):
        result = suggest_similar("task_request", ["task_request", "task_result"])
        assert "task_request" in result

    def test_close_match(self):
        result = suggest_similar("taks_request", ["task_request", "task_result", "audit_request"])
        assert len(result) >= 1
        assert "task_request" in result

    def test_no_match_returns_empty(self):
        result = suggest_similar("xyzzy_nonsense", ["task_request", "task_result"])
        assert result == ()

    def test_empty_got_returns_empty(self):
        result = suggest_similar("", ["task_request", "task_result"])
        assert result == ()

    def test_empty_options_returns_empty(self):
        result = suggest_similar("task_request", [])
        assert result == ()

    def test_returns_tuple(self):
        result = suggest_similar("task_request", ["task_request"])
        assert isinstance(result, tuple)

    def test_max_n_suggestions(self):
        options = ["task_request", "task_result", "task_id", "task_name"]
        result = suggest_similar("task_req", options, n=2)
        assert len(result) <= 2

    def test_high_cutoff_no_match(self):
        result = suggest_similar("tsk_req", ["task_request"], cutoff=0.99)
        assert result == ()


# ============================================================
# format_error
# ============================================================


class TestFormatError:
    """format_error() builds terminal-friendly output."""

    def _make_error(self, **overrides) -> HumanError:
        defaults = dict(
            code="LU-T001",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            locale="en",
            message="'task_id' cannot be empty.",
            suggestion="Provide a non-empty string for 'task_id'.",
            technical="ValueError: task_id cannot be empty",
        )
        defaults.update(overrides)
        return HumanError(**defaults)

    def test_header_contains_code_and_message(self):
        err = self._make_error()
        output = format_error(err)
        assert "[LU-T001]" in output
        assert "'task_id' cannot be empty." in output

    def test_hint_line_present(self):
        err = self._make_error()
        output = format_error(err)
        assert "Hint:" in output

    def test_technical_hidden_by_default(self):
        err = self._make_error()
        output = format_error(err)
        assert "[technical]" not in output

    def test_verbose_shows_technical(self):
        err = self._make_error()
        output = format_error(err, verbose=True)
        assert "[technical]" in output
        assert "ValueError: task_id cannot be empty" in output

    def test_location_with_line_shown(self):
        loc = ErrorLocation(line=7, source="spec")
        err = self._make_error(location=loc)
        output = format_error(err)
        assert "Line 7" in output

    def test_location_with_col_shown(self):
        loc = ErrorLocation(line=2, col=4, source="dsl")
        err = self._make_error(location=loc)
        output = format_error(err)
        assert "Col 4" in output

    def test_got_and_expected_shown(self):
        err = self._make_error(got="worker", expected="regina")
        output = format_error(err)
        assert "Got:" in output
        assert "worker" in output
        assert "Expected:" in output
        assert "regina" in output

    def test_only_got_shown(self):
        err = self._make_error(got="worker")
        output = format_error(err)
        assert "Got: worker" in output
        assert "Expected:" not in output

    def test_only_expected_shown(self):
        err = self._make_error(expected="task_request")
        output = format_error(err)
        assert "Expected: task_request" in output
        assert "Got:" not in output

    def test_similar_shown_as_did_you_mean(self):
        err = self._make_error(similar=("task_request", "task_result"))
        output = format_error(err)
        assert "Did you mean:" in output
        assert "task_request" in output

    def test_no_location_no_location_line(self):
        err = self._make_error()
        output = format_error(err)
        assert "Line" not in output
        assert "Col" not in output

    def test_returns_string(self):
        err = self._make_error()
        assert isinstance(format_error(err), str)


# ============================================================
# Constants
# ============================================================


class TestConstants:
    """DEFAULT_LOCALE and SUPPORTED_LOCALES."""

    def test_default_locale_is_en(self):
        assert DEFAULT_LOCALE == "en"

    def test_supported_locales_contains_three(self):
        assert len(SUPPORTED_LOCALES) == 3

    def test_supported_locales_contains_en(self):
        assert "en" in SUPPORTED_LOCALES

    def test_supported_locales_contains_it(self):
        assert "it" in SUPPORTED_LOCALES

    def test_supported_locales_contains_pt(self):
        assert "pt" in SUPPORTED_LOCALES

    def test_supported_locales_is_frozenset(self):
        assert isinstance(SUPPORTED_LOCALES, frozenset)

    def test_default_locale_in_supported(self):
        assert DEFAULT_LOCALE in SUPPORTED_LOCALES


# ============================================================
# __init__.py re-exports
# ============================================================


class TestInitReExports:
    """All errors.py symbols are importable from the top-level package."""

    def test_import_error_category(self):
        from cervellaswarm_lingua_universale import ErrorCategory
        assert ErrorCategory.VALIDATION is not None

    def test_import_error_severity(self):
        from cervellaswarm_lingua_universale import ErrorSeverity
        assert ErrorSeverity.ERROR is not None

    def test_import_error_location(self):
        from cervellaswarm_lingua_universale import ErrorLocation
        loc = ErrorLocation(line=1)
        assert loc.line == 1

    def test_import_human_error(self):
        from cervellaswarm_lingua_universale import HumanError
        assert HumanError is not None

    def test_import_humanize(self):
        from cervellaswarm_lingua_universale import humanize
        assert callable(humanize)

    def test_import_format_error(self):
        from cervellaswarm_lingua_universale import format_error
        assert callable(format_error)

    def test_import_suggest_similar(self):
        from cervellaswarm_lingua_universale import suggest_similar
        assert callable(suggest_similar)

    def test_import_default_locale(self):
        from cervellaswarm_lingua_universale import DEFAULT_LOCALE
        assert DEFAULT_LOCALE == "en"

    def test_import_supported_locales(self):
        from cervellaswarm_lingua_universale import SUPPORTED_LOCALES
        assert "en" in SUPPORTED_LOCALES
