# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for spec.py parser: parse_spec() happy paths and error cases.

Covers: all 7 property kinds, confidence levels, trust tiers, comments,
blank lines, triple-quoted strings with indentation, and all error paths.
"""

import pytest

from cervellaswarm_lingua_universale.spec import (
    PropertyKind,
    PropertySpec,
    ProtocolSpec,
    SpecParseError,
    parse_spec,
)


# ============================================================
# Happy path tests
# ============================================================

class TestParseSpecHappyPath:
    """parse_spec() succeeds for all supported property kinds."""

    def test_parse_always_terminates(self):
        spec = parse_spec("""
            properties for DelegateTask:
                always terminates
        """)
        assert spec.protocol_name == "DelegateTask"
        assert len(spec.properties) == 1
        assert spec.properties[0].kind == PropertyKind.ALWAYS_TERMINATES

    def test_parse_no_deadlock(self):
        spec = parse_spec("""
            properties for DelegateTask:
                no deadlock
        """)
        assert spec.properties[0].kind == PropertyKind.NO_DEADLOCK

    def test_parse_ordering_task_request_before_task_result(self):
        spec = parse_spec("""
            properties for DelegateTask:
                task_request before task_result
        """)
        prop = spec.properties[0]
        assert prop.kind == PropertyKind.ORDERING
        assert prop.params == ("task_request", "task_result")

    def test_parse_exclusion_worker_cannot_send_audit_request(self):
        spec = parse_spec("""
            properties for DelegateTask:
                worker cannot send audit_request
        """)
        prop = spec.properties[0]
        assert prop.kind == PropertyKind.EXCLUSION
        assert prop.params == ("worker", "audit_request")

    def test_parse_all_roles_participate(self):
        spec = parse_spec("""
            properties for DelegateTask:
                all roles participate
        """)
        assert spec.properties[0].kind == PropertyKind.ALL_ROLES_PARTICIPATE

    def test_parse_all_seven_properties(self):
        spec = parse_spec("""
            properties for DelegateTask:
                always terminates
                no deadlock
                task_request before task_result
                worker cannot send audit_request
                confidence >= high
                trust >= standard
                all roles participate
        """)
        assert spec.protocol_name == "DelegateTask"
        assert len(spec.properties) == 7
        kinds = [p.kind for p in spec.properties]
        assert PropertyKind.ALWAYS_TERMINATES in kinds
        assert PropertyKind.NO_DEADLOCK in kinds
        assert PropertyKind.ORDERING in kinds
        assert PropertyKind.EXCLUSION in kinds
        assert PropertyKind.CONFIDENCE_MIN in kinds
        assert PropertyKind.TRUST_MIN in kinds
        assert PropertyKind.ALL_ROLES_PARTICIPATE in kinds

    def test_parse_protocol_name_extraction(self):
        spec = parse_spec("""
            properties for MyCustomProtocol:
                always terminates
        """)
        assert spec.protocol_name == "MyCustomProtocol"

    def test_parse_triple_quoted_with_indentation(self):
        # textwrap.dedent should handle arbitrary base indentation
        source = """
            properties for DelegateTask:
                always terminates
                no deadlock
        """
        spec = parse_spec(source)
        assert spec.protocol_name == "DelegateTask"
        assert len(spec.properties) == 2


class TestParseSpecConfidenceLevels:
    """All 5 confidence levels are parsed correctly."""

    @pytest.mark.parametrize("level,expected_threshold", [
        ("high", 0.8),
        ("medium", 0.5),
        ("low", 0.2),
        ("certain", 1.0),
        ("speculative", 0.1),
    ])
    def test_parse_confidence_level(self, level, expected_threshold):
        spec = parse_spec(f"""
            properties for DelegateTask:
                confidence >= {level}
        """)
        prop = spec.properties[0]
        assert prop.kind == PropertyKind.CONFIDENCE_MIN
        assert prop.threshold == expected_threshold


class TestParseSpecTrustTiers:
    """All 4 trust tiers are parsed correctly."""

    @pytest.mark.parametrize("tier", ["trusted", "verified", "standard", "untrusted"])
    def test_parse_trust_tier(self, tier):
        spec = parse_spec(f"""
            properties for DelegateTask:
                trust >= {tier}
        """)
        prop = spec.properties[0]
        assert prop.kind == PropertyKind.TRUST_MIN
        assert prop.params == (tier,)


class TestParseSpecComments:
    """Comments and blank lines are ignored by the parser."""

    def test_comments_ignored(self):
        spec = parse_spec("""
            properties for DelegateTask:
                # This is a comment
                always terminates
                # Another comment
                no deadlock
        """)
        assert len(spec.properties) == 2
        assert spec.properties[0].kind == PropertyKind.ALWAYS_TERMINATES
        assert spec.properties[1].kind == PropertyKind.NO_DEADLOCK

    def test_blank_lines_ignored(self):
        spec = parse_spec("""
            properties for DelegateTask:

                always terminates

                no deadlock

        """)
        assert len(spec.properties) == 2

    def test_mixed_comments_and_blank_lines(self):
        spec = parse_spec("""
            properties for DelegateTask:
                # Check termination
                always terminates

                # Check ordering
                task_request before task_result
        """)
        assert len(spec.properties) == 2


class TestParseSpecOrdering:
    """ORDERING property parsing edge cases."""

    def test_ordering_audit_request_before_audit_verdict(self):
        spec = parse_spec("""
            properties for DelegateTask:
                audit_request before audit_verdict
        """)
        prop = spec.properties[0]
        assert prop.params == ("audit_request", "audit_verdict")

    def test_ordering_plan_request_before_plan_proposal(self):
        spec = parse_spec("""
            properties for ArchitectFlow:
                plan_request before plan_proposal
        """)
        prop = spec.properties[0]
        assert prop.params == ("plan_request", "plan_proposal")


# ============================================================
# Error cases
# ============================================================

class TestParseSpecErrorCases:
    """parse_spec() raises SpecParseError on invalid input."""

    def test_tabs_rejected(self):
        with pytest.raises(SpecParseError, match="tabs are not allowed"):
            parse_spec("properties for DelegateTask:\n\talways terminates\n")

    def test_non_multiple_of_4_indentation_rejected(self):
        with pytest.raises(SpecParseError, match="indentation must be a multiple of 4"):
            parse_spec("properties for DelegateTask:\n   always terminates\n")

    def test_unknown_confidence_level_rejected(self):
        with pytest.raises(SpecParseError, match="unknown confidence level"):
            parse_spec("""
                properties for DelegateTask:
                    confidence >= extreme
            """)

    def test_unknown_trust_tier_rejected(self):
        with pytest.raises(SpecParseError, match="unknown trust tier"):
            parse_spec("""
                properties for DelegateTask:
                    trust >= godlike
            """)

    def test_unknown_message_kind_in_ordering_rejected(self):
        with pytest.raises(SpecParseError, match="unknown message kind"):
            parse_spec("""
                properties for DelegateTask:
                    foobar before task_result
            """)

    def test_same_kind_in_ordering_rejected(self):
        # A before A is invalid
        with pytest.raises(SpecParseError, match="a and b must differ"):
            parse_spec("""
                properties for DelegateTask:
                    task_request before task_request
            """)

    def test_missing_for_keyword_rejected(self):
        with pytest.raises(SpecParseError, match="expected 'for'"):
            parse_spec("""
                properties DelegateTask:
                    always terminates
            """)

    def test_missing_colon_rejected(self):
        with pytest.raises(SpecParseError, match="expected COLON"):
            parse_spec("""
                properties for DelegateTask
                    always terminates
            """)

    def test_empty_spec_no_properties_rejected(self):
        with pytest.raises(SpecParseError, match="at least one property"):
            parse_spec("""
                properties for DelegateTask:
            """)

    def test_unknown_property_keyword_rejected(self):
        with pytest.raises(SpecParseError):
            parse_spec("""
                properties for DelegateTask:
                    something weird here
            """)

    def test_trailing_content_after_spec_rejected(self):
        with pytest.raises(SpecParseError, match="unexpected content after spec block"):
            parse_spec("""
                properties for DelegateTask:
                    always terminates
                properties for OtherProtocol:
                    no deadlock
            """)

    def test_error_has_line_number_tabs(self):
        try:
            parse_spec("properties for DelegateTask:\n\talways terminates\n")
        except SpecParseError as e:
            assert e.line > 0
            assert "line" in str(e)

    def test_error_has_line_number_unknown_kind(self):
        try:
            parse_spec("""
                properties for DelegateTask:
                    unknown_kind before task_result
            """)
        except SpecParseError as e:
            assert e.line > 0

    def test_unknown_message_kind_second_param_rejected(self):
        with pytest.raises(SpecParseError, match="unknown message kind"):
            parse_spec("""
                properties for DelegateTask:
                    task_request before nonexistent_kind
            """)

    def test_missing_properties_keyword_rejected(self):
        with pytest.raises(SpecParseError, match="expected 'properties'"):
            parse_spec("""
                specs for DelegateTask:
                    always terminates
            """)


class TestParseSpecEdgeCases:
    """Edge cases for the parser."""

    def test_multiple_exclusions_parsed(self):
        spec = parse_spec("""
            properties for DelegateTask:
                worker cannot send audit_request
                guardiana cannot send task_request
        """)
        assert len(spec.properties) == 2
        assert all(p.kind == PropertyKind.EXCLUSION for p in spec.properties)

    def test_ordering_and_exclusion_combined(self):
        spec = parse_spec("""
            properties for DelegateTask:
                task_request before task_result
                worker cannot send audit_request
                audit_request before audit_verdict
        """)
        kinds = [p.kind for p in spec.properties]
        assert kinds.count(PropertyKind.ORDERING) == 2
        assert kinds.count(PropertyKind.EXCLUSION) == 1

    def test_spec_is_frozen_dataclass(self):
        spec = parse_spec("""
            properties for DelegateTask:
                always terminates
        """)
        with pytest.raises((AttributeError, TypeError)):
            spec.protocol_name = "Other"  # type: ignore[misc]

    def test_property_spec_is_frozen_dataclass(self):
        spec = parse_spec("""
            properties for DelegateTask:
                always terminates
        """)
        prop = spec.properties[0]
        with pytest.raises((AttributeError, TypeError)):
            prop.kind = PropertyKind.NO_DEADLOCK  # type: ignore[misc]

    def test_parse_spec_returns_protocol_spec_type(self):
        result = parse_spec("""
            properties for DelegateTask:
                always terminates
        """)
        assert isinstance(result, ProtocolSpec)

    def test_properties_are_tuple(self):
        spec = parse_spec("""
            properties for DelegateTask:
                always terminates
                no deadlock
        """)
        assert isinstance(spec.properties, tuple)
