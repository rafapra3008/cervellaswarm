# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for errors.py humanize() - custom exceptions.

Covers: ProtocolViolation -> LU-R00X, SessionComplete -> LU-R007,
DSLParseError -> LU-D00X, SpecParseError -> LU-S00X.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale.errors import (
    ErrorCategory,
    ErrorSeverity,
    humanize,
)
from cervellaswarm_lingua_universale.checker import ProtocolViolation, SessionComplete
from cervellaswarm_lingua_universale.dsl import DSLParseError
from cervellaswarm_lingua_universale.spec import SpecParseError


# ============================================================
# Helpers
# ============================================================


def _pv(expected: str, got: str, step: int = 0) -> ProtocolViolation:
    """Build a minimal ProtocolViolation."""
    return ProtocolViolation(
        protocol="TestProto",
        session_id="sess-001",
        expected=expected,
        got=got,
        step=step,
    )


# ============================================================
# ProtocolViolation -> LU-R00X
# ============================================================


class TestHumanizeProtocolViolation:
    """ProtocolViolation maps to the right LU-R code."""

    def test_wrong_sender_lu_r001(self):
        exc = _pv(expected="sender=regina", got="worker", step=1)
        err = humanize(exc)
        assert err.code == "LU-R001"
        assert err.category == ErrorCategory.PROTOCOL
        assert err.severity == ErrorSeverity.ERROR

    def test_wrong_sender_message_contains_step(self):
        exc = _pv(expected="sender=regina", got="worker", step=3)
        err = humanize(exc)
        assert "3" in err.message

    def test_wrong_receiver_lu_r002(self):
        exc = _pv(expected="receiver=worker", got="researcher", step=2)
        err = humanize(exc)
        assert err.code == "LU-R002"

    def test_wrong_message_kind_lu_r003(self):
        exc = _pv(expected="message=task_request", got="audit_request", step=1)
        err = humanize(exc)
        assert err.code == "LU-R003"

    def test_not_at_choice_point_lu_r004(self):
        exc = _pv(expected="n/a", got="not at a choice point")
        err = humanize(exc)
        assert err.code == "LU-R004"

    def test_branch_not_found_lu_r005(self):
        exc = _pv(expected="branch in {approve, reject}", got="unknown_branch")
        err = humanize(exc)
        assert err.code == "LU-R005"

    def test_needs_branch_selection_lu_r006(self):
        exc = _pv(expected="branch selection required", got="TaskRequest")
        err = humanize(exc)
        assert err.code == "LU-R006"

    def test_got_field_populated(self):
        exc = _pv(expected="sender=regina", got="worker", step=1)
        err = humanize(exc)
        assert err.got == "worker"

    def test_expected_field_populated(self):
        exc = _pv(expected="sender=regina", got="worker", step=1)
        err = humanize(exc)
        assert err.expected == "sender=regina"

    def test_location_source_is_checker(self):
        exc = _pv(expected="sender=regina", got="worker")
        err = humanize(exc)
        assert err.location is not None
        assert err.location.source == "checker"

    def test_technical_contains_original_message(self):
        exc = _pv(expected="sender=regina", got="worker", step=1)
        err = humanize(exc)
        assert "TestProto" in err.technical

    def test_locale_it(self):
        exc = _pv(expected="sender=regina", got="worker", step=1)
        err = humanize(exc, locale="it")
        assert err.locale == "it"
        assert err.message != humanize(exc, locale="en").message

    def test_locale_pt(self):
        exc = _pv(expected="sender=regina", got="worker", step=1)
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"
        assert err.message != humanize(exc, locale="en").message


# ============================================================
# SessionComplete -> LU-R007
# ============================================================


class TestHumanizeSessionComplete:
    """SessionComplete maps to LU-R007."""

    def test_code_lu_r007(self):
        exc = SessionComplete(protocol="DelegateTask", session_id="sess-42")
        err = humanize(exc)
        assert err.code == "LU-R007"

    def test_category_is_protocol(self):
        exc = SessionComplete(protocol="DelegateTask", session_id="sess-42")
        err = humanize(exc)
        assert err.category == ErrorCategory.PROTOCOL

    def test_got_is_session_id(self):
        exc = SessionComplete(protocol="DelegateTask", session_id="sess-42")
        err = humanize(exc)
        assert err.got == "sess-42"

    def test_message_contains_session(self):
        exc = SessionComplete(protocol="DelegateTask", session_id="sess-xyz")
        err = humanize(exc)
        assert "sess-xyz" in err.message

    def test_locale_it(self):
        exc = SessionComplete(protocol="DelegateTask", session_id="s1")
        err = humanize(exc, locale="it")
        assert err.locale == "it"

    def test_locale_pt(self):
        exc = SessionComplete(protocol="DelegateTask", session_id="s1")
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"


# ============================================================
# DSLParseError -> LU-D00X
# ============================================================


class TestHumanizeDSLParseError:
    """DSLParseError maps to the right LU-D code."""

    def test_unexpected_character_lu_d001(self):
        exc = DSLParseError("unexpected character: '@'", line=3)
        err = humanize(exc)
        assert err.code == "LU-D001"
        assert err.category == ErrorCategory.PARSE

    def test_unexpected_character_got_extracted(self):
        exc = DSLParseError("unexpected character: '@'", line=3)
        err = humanize(exc)
        assert err.got == "@"

    def test_expected_got_lu_d002(self):
        exc = DSLParseError("expected '}', got 'protocol'", line=5)
        err = humanize(exc)
        assert err.code == "LU-D002"

    def test_unknown_message_type_lu_d003(self):
        exc = DSLParseError("unknown message type: 'Foobar'", line=2)
        err = humanize(exc)
        assert err.code == "LU-D003"
        assert err.got == "Foobar"

    def test_unknown_message_type_similar_suggestions(self):
        exc = DSLParseError("unknown message type: 'TaskRequst'", line=1)
        err = humanize(exc)
        assert err.code == "LU-D003"
        assert len(err.similar) >= 1

    def test_duplicate_branch_label_lu_d004(self):
        exc = DSLParseError("duplicate branch label: 'approve'", line=8)
        err = humanize(exc)
        assert err.code == "LU-D004"
        assert err.got == "approve"

    def test_empty_choice_lu_d005(self):
        exc = DSLParseError("empty choice block", line=10)
        err = humanize(exc)
        assert err.code == "LU-D005"

    def test_empty_branch_lu_d005(self):
        exc = DSLParseError("empty branch detected", line=10)
        err = humanize(exc)
        assert err.code == "LU-D005"

    def test_no_protocols_found_lu_d006(self):
        exc = DSLParseError("no protocols found in source", line=0)
        err = humanize(exc)
        assert err.code == "LU-D006"

    def test_unexpected_end_of_input_lu_d007(self):
        exc = DSLParseError("unexpected end of input", line=15)
        err = humanize(exc)
        assert err.code == "LU-D007"

    def test_location_line_set(self):
        exc = DSLParseError("unexpected character: '!'", line=7)
        err = humanize(exc)
        assert err.location is not None
        assert err.location.line == 7
        assert err.location.source == "dsl"

    def test_locale_it(self):
        exc = DSLParseError("unexpected character: '#'", line=1)
        err_en = humanize(exc, locale="en")
        err_it = humanize(exc, locale="it")
        assert err_it.locale == "it"
        assert err_it.message != err_en.message

    def test_locale_pt(self):
        exc = DSLParseError("unexpected character: '#'", line=1)
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"


# ============================================================
# SpecParseError -> LU-S00X
# ============================================================


class TestHumanizeSpecParseError:
    """SpecParseError maps to the right LU-S code."""

    def test_tabs_not_allowed_lu_s001(self):
        exc = SpecParseError("tabs are not allowed in spec source", line=2)
        err = humanize(exc)
        assert err.code == "LU-S001"

    def test_indentation_multiple_of_4_lu_s002(self):
        exc = SpecParseError("indentation must be a multiple of 4 spaces (got 6)", line=4)
        err = humanize(exc)
        assert err.code == "LU-S002"

    def test_indentation_got_extracted(self):
        exc = SpecParseError("indentation must be a multiple of 4 spaces (got 6)", line=4)
        err = humanize(exc)
        assert err.got == "6"

    def test_unknown_message_kind_lu_s003(self):
        exc = SpecParseError("unknown message kind: 'foobar'", line=6)
        err = humanize(exc)
        assert err.code == "LU-S003"
        assert err.got == "foobar"

    def test_unknown_message_kind_similar_suggestions(self):
        exc = SpecParseError("unknown message kind: 'tsk_request'", line=5)
        err = humanize(exc)
        assert err.code == "LU-S003"
        assert len(err.similar) >= 1

    def test_unknown_confidence_level_lu_s004(self):
        exc = SpecParseError("unknown confidence level: 'ultra'", line=8)
        err = humanize(exc)
        assert err.code == "LU-S004"
        assert err.got == "ultra"

    def test_unknown_confidence_level_similar(self):
        exc = SpecParseError("unknown confidence level: 'hig'", line=8)
        err = humanize(exc)
        assert err.code == "LU-S004"
        assert len(err.similar) >= 1

    def test_unknown_trust_tier_lu_s005(self):
        exc = SpecParseError("unknown trust tier: 'mega_trusted'", line=9)
        err = humanize(exc)
        assert err.code == "LU-S005"
        assert err.got == "mega_trusted"

    def test_unknown_trust_tier_similar(self):
        exc = SpecParseError("unknown trust tier: 'truested'", line=9)
        err = humanize(exc)
        assert err.code == "LU-S005"
        assert len(err.similar) >= 1

    def test_ordering_must_differ_lu_s006(self):
        exc = SpecParseError("ORDERING: a and b must differ", line=11)
        err = humanize(exc)
        assert err.code == "LU-S006"

    def test_at_least_one_property_lu_s008(self):
        exc = SpecParseError("spec must have at least one property", line=12)
        err = humanize(exc)
        assert err.code == "LU-S008"

    def test_generic_syntax_error_lu_s007(self):
        exc = SpecParseError("expected 'properties', got 'protocol'", line=3)
        err = humanize(exc)
        assert err.code == "LU-S007"

    def test_location_set(self):
        exc = SpecParseError("tabs are not allowed in spec source", line=5)
        err = humanize(exc)
        assert err.location is not None
        assert err.location.line == 5
        assert err.location.source == "spec"

    def test_locale_it(self):
        exc = SpecParseError("tabs are not allowed in spec source", line=1)
        err_en = humanize(exc, locale="en")
        err_it = humanize(exc, locale="it")
        assert err_it.locale == "it"
        assert err_it.message != err_en.message

    def test_locale_pt(self):
        exc = SpecParseError("tabs are not allowed in spec source", line=1)
        err = humanize(exc, locale="pt")
        assert err.locale == "pt"
