# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for errors.py humanize() - ValueError, RuntimeError, fallback.

Covers: IntentParseError -> LU-I00X, ValueError patterns -> LU-T/P/L/G/C/A,
RuntimeError/TimeoutError -> LU-L, fallback LU-X001, unsupported locale,
custom context parameter, and return-type contract.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale.errors import (
    ErrorCategory,
    HumanError,
    humanize,
)
from cervellaswarm_lingua_universale.checker import ProtocolViolation, SessionComplete
from cervellaswarm_lingua_universale.dsl import DSLParseError
from cervellaswarm_lingua_universale.spec import SpecParseError
from cervellaswarm_lingua_universale.intent import IntentParseError


# ============================================================
# IntentParseError -> LU-I00X
# ============================================================


class TestHumanizeIntentParseError:
    """IntentParseError maps to the right LU-I code."""

    def test_tabs_not_allowed_lu_i001(self):
        exc = IntentParseError("tabs are not allowed in intent source", line=1)
        err = humanize(exc)
        assert err.code == "LU-I001"

    def test_cannot_parse_action_lu_i003(self):
        exc = IntentParseError("cannot parse action: unknown verb phrase 'flings'", line=3)
        err = humanize(exc)
        assert err.code == "LU-I003"

    def test_cannot_parse_action_got_set(self):
        exc = IntentParseError("cannot parse action: unknown verb phrase 'flings'", line=3)
        err = humanize(exc)
        assert err.got is not None
        assert "flings" in err.got

    def test_expected_indented_roles_lu_i004(self):
        exc = IntentParseError("expected indented 'roles:' declaration", line=2)
        err = humanize(exc)
        assert err.code == "LU-I004"

    def test_generic_intent_error_lu_i005(self):
        exc = IntentParseError("expected 'protocol', got 'roles:'", line=4)
        err = humanize(exc)
        assert err.code == "LU-I005"

    def test_location_set(self):
        exc = IntentParseError("tabs are not allowed in intent source", line=7)
        err = humanize(exc)
        assert err.location is not None
        assert err.location.line == 7
        assert err.location.source == "intent"

    def test_locale_it(self):
        exc = IntentParseError("tabs are not allowed in intent source", line=1)
        err_en = humanize(exc, locale="en")
        err_it = humanize(exc, locale="it")
        assert err_it.locale == "it"
        assert err_it.message != err_en.message

    def test_locale_pt(self):
        exc = IntentParseError("tabs are not allowed in intent source", line=1)
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"


# ============================================================
# ValueError patterns
# ============================================================


class TestHumanizeValueError:
    """ValueError with known substrings maps to the right LU code."""

    def test_task_id_empty_lu_t001(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc)
        assert err.code == "LU-T001"
        assert err.category == ErrorCategory.VALIDATION

    def test_task_id_field_extracted(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc)
        assert "task_id" in err.message

    def test_score_range_lu_t002(self):
        exc = ValueError("score must be 0.0-10.0, got 15.0")
        err = humanize(exc)
        assert err.code == "LU-T002"

    def test_summary_too_long_lu_t003(self):
        exc = ValueError("summary must be <= 200 characters, got 250")
        err = humanize(exc)
        assert err.code == "LU-T003"

    def test_sender_receiver_same_lu_p001(self):
        exc = ValueError("sender and receiver cannot be the same: 'worker'")
        err = humanize(exc)
        assert err.code == "LU-P001"
        assert err.got == "worker"

    def test_not_in_protocol_roles_lu_p005(self):
        exc = ValueError("sender 'coordinator' not in protocol roles")
        err = humanize(exc)
        assert err.code == "LU-P005"
        assert err.got == "coordinator"

    def test_lean4_empty_string_lu_l001(self):
        exc = ValueError("cannot create Lean 4 identifier from empty string")
        err = humanize(exc)
        assert err.code == "LU-L001"
        assert err.category == ErrorCategory.VERIFICATION

    def test_codegen_empty_string_lu_g001(self):
        exc = ValueError("cannot create Python identifier from empty string")
        err = humanize(exc)
        assert err.code == "LU-G001"
        assert err.category == ErrorCategory.CODEGEN

    def test_confidence_range_lu_c001(self):
        exc = ValueError("confidence must be 0.0-1.0, got 1.5")
        err = humanize(exc)
        assert err.code == "LU-C001"
        assert err.category == ErrorCategory.CONFIDENCE

    def test_trust_range_lu_c003(self):
        exc = ValueError("trust must be 0.0-1.0, got -0.1")
        err = humanize(exc)
        assert err.code == "LU-C003"

    def test_agent_name_empty_lu_t001(self):
        exc = ValueError("agent_name cannot be empty")
        err = humanize(exc)
        assert err.code == "LU-T001"

    def test_protocol_name_empty_lu_t001(self):
        exc = ValueError("protocol name cannot be empty")
        err = humanize(exc)
        assert err.code == "LU-T001"

    def test_unknown_valueerror_fallback_lu_x001(self):
        exc = ValueError("some completely unrelated error with no known pattern")
        err = humanize(exc)
        assert err.code == "LU-X001"

    def test_binding_role_lu_a001(self):
        exc = ValueError("binding role 'coordinator' is not in the protocol roles")
        err = humanize(exc)
        assert err.code == "LU-A001"
        assert err.got == "coordinator"

    def test_locale_it_valueerror(self):
        exc = ValueError("task_id cannot be empty")
        err_en = humanize(exc, locale="en")
        err_it = humanize(exc, locale="it")
        assert err_it.locale == "it"
        assert err_it.message != err_en.message

    def test_locale_pt_valueerror(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"


# ============================================================
# RuntimeError and TimeoutError
# ============================================================


class TestHumanizeRuntimeAndTimeout:
    """RuntimeError / TimeoutError for Lean 4 paths."""

    def test_lean_not_installed_lu_l003(self):
        exc = RuntimeError("Lean 4 is not installed or not on PATH")
        err = humanize(exc)
        assert err.code == "LU-L003"
        assert err.category == ErrorCategory.VERIFICATION

    def test_lean_keyword_in_message(self):
        exc = RuntimeError("could not find lean binary")
        err = humanize(exc)
        assert err.code == "LU-L003"

    def test_not_installed_keyword(self):
        exc = RuntimeError("program is not installed")
        err = humanize(exc)
        assert err.code == "LU-L003"

    def test_timeout_error_lu_l004(self):
        exc = TimeoutError("Lean 4 verification timed out after 30s")
        err = humanize(exc)
        assert err.code == "LU-L004"
        assert err.category == ErrorCategory.VERIFICATION

    def test_generic_runtime_error_fallback(self):
        exc = RuntimeError("something else entirely went wrong")
        err = humanize(exc)
        assert err.code == "LU-X001"

    def test_locale_it_lean(self):
        exc = RuntimeError("Lean 4 is not installed")
        err_en = humanize(exc, locale="en")
        err_it = humanize(exc, locale="it")
        assert err_it.locale == "it"
        assert err_it.message != err_en.message

    def test_locale_pt_timeout(self):
        exc = TimeoutError("timed out")
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"


# ============================================================
# Fallback LU-X001
# ============================================================


class TestHumanizeFallback:
    """Unknown exceptions map to LU-X001."""

    def test_unknown_exception_lu_x001(self):
        exc = KeyError("unexpected key")
        err = humanize(exc)
        assert err.code == "LU-X001"

    def test_type_error_fallback(self):
        exc = TypeError("wrong type")
        err = humanize(exc)
        assert err.code == "LU-X001"

    def test_attribute_error_fallback(self):
        exc = AttributeError("no such attribute")
        err = humanize(exc)
        assert err.code == "LU-X001"

    def test_fallback_technical_set(self):
        exc = KeyError("boom")
        err = humanize(exc)
        assert len(err.technical) > 0

    def test_fallback_locale_it(self):
        exc = KeyError("boom")
        err_en = humanize(exc, locale="en")
        err_it = humanize(exc, locale="it")
        assert err_it.locale == "it"
        assert err_it.message != err_en.message


# ============================================================
# Unsupported locale fallback
# ============================================================


class TestHumanizeUnsupportedLocale:
    """Unsupported locale falls back to 'en'."""

    def test_unsupported_locale_fr_falls_back(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc, locale="fr")
        en_err = humanize(exc, locale="en")
        assert err.message == en_err.message

    def test_unsupported_locale_de_falls_back(self):
        exc = SessionComplete(protocol="P", session_id="s")
        err = humanize(exc, locale="de")
        en_err = humanize(exc, locale="en")
        assert err.message == en_err.message

    def test_empty_string_locale_falls_back(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc, locale="")
        en_err = humanize(exc, locale="en")
        assert err.message == en_err.message


# ============================================================
# Custom context parameter
# ============================================================


class TestHumanizeCustomContext:
    """Custom context dict can enrich template substitution."""

    def test_context_is_accepted(self):
        exc = ProtocolViolation(
            protocol="P", session_id="s1",
            expected="sender=regina", got="worker", step=1,
        )
        err = humanize(exc, context={"extra": "value"})
        assert err.code == "LU-R001"

    def test_context_none_accepted(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc, context=None)
        assert err.code == "LU-T001"

    def test_context_empty_dict_accepted(self):
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc, context={})
        assert err.code == "LU-T001"

    def test_context_does_not_break_output(self):
        """Custom context with extra keys must not raise or produce empty messages."""
        exc = ValueError("task_id cannot be empty")
        err = humanize(exc, context={"custom_key": "custom_value"})
        assert err.code == "LU-T001"
        assert err.message


# ============================================================
# Return type and basic contract
# ============================================================


class TestHumanizeContract:
    """humanize() always returns a HumanError with mandatory fields filled."""

    def _assert_valid(self, err: HumanError) -> None:
        assert isinstance(err, HumanError)
        assert err.code.startswith("LU-")
        assert len(err.message) > 0
        assert len(err.suggestion) > 0
        assert err.locale in ("en", "it", "pt")

    def test_protocol_violation_valid(self):
        exc = ProtocolViolation("P", "s", "sender=regina", "worker", 1)
        self._assert_valid(humanize(exc))

    def test_session_complete_valid(self):
        exc = SessionComplete("P", "s")
        self._assert_valid(humanize(exc))

    def test_dsl_parse_error_valid(self):
        exc = DSLParseError("unexpected character: '@'", line=1)
        self._assert_valid(humanize(exc))

    def test_spec_parse_error_valid(self):
        exc = SpecParseError("tabs are not allowed in spec source", line=2)
        self._assert_valid(humanize(exc))

    def test_intent_parse_error_valid(self):
        exc = IntentParseError("tabs are not allowed in intent source", line=3)
        self._assert_valid(humanize(exc))

    def test_value_error_valid(self):
        exc = ValueError("task_id cannot be empty")
        self._assert_valid(humanize(exc))

    def test_runtime_error_valid(self):
        exc = RuntimeError("Lean 4 is not installed")
        self._assert_valid(humanize(exc))

    def test_timeout_error_valid(self):
        exc = TimeoutError("timed out")
        self._assert_valid(humanize(exc))

    def test_unknown_exception_valid(self):
        exc = KeyError("boom")
        self._assert_valid(humanize(exc))
