# SPDX-License-Identifier: Apache-2.0
"""Edge-case tests for _mcp_audit.py helper functions.

S486 HARDTEST: 0 tools, unknown categories, empty descriptions,
short tool names, MAX_ORDERINGS overflow, self-reference in descriptions.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._mcp_audit import (
    ToolDefinition,
    InferredStep,
    _categorize_tools,
    _order_lifecycle_first,
    _order_cleanup_last,
    _order_crud_sequence,
    _order_by_schema_refs,
    _order_by_description,
    _infer_orderings,
    infer_protocol,
    check_annotations,
)


# ---------------------------------------------------------------------------
# _order_lifecycle_first
# ---------------------------------------------------------------------------


class TestOrderLifecycleFirst:
    """Edge cases for lifecycle-before-everything ordering."""

    def test_zero_tools(self):
        """Empty tool list produces zero orderings."""
        result = _order_lifecycle_first([], {})
        assert result == []

    def test_no_lifecycle_category(self):
        """No LIFECYCLE category means no orderings from this helper."""
        tools = [ToolDefinition("query", "Query data", {})]
        cats = {"READ": ["query"]}
        result = _order_lifecycle_first(tools, cats)
        assert result == []

    def test_lifecycle_only_no_others(self):
        """Only lifecycle tools, no non-lifecycle: zero orderings (nothing to order before)."""
        tools = [ToolDefinition("connect", "Connect", {})]
        cats = {"LIFECYCLE": ["connect"]}
        result = _order_lifecycle_first(tools, cats)
        assert result == []

    def test_cleanup_excluded_from_non_lifecycle(self):
        """Cleanup tools are excluded from 'non-lifecycle' side (avoids redundant ordering)."""
        tools = [
            ToolDefinition("init", "", {}),
            ToolDefinition("close", "", {}),
            ToolDefinition("query", "", {}),
        ]
        cats = {"LIFECYCLE": ["init"], "CLEANUP": ["close"], "READ": ["query"]}
        result = _order_lifecycle_first(tools, cats)
        # init -> query, but NOT init -> close
        assert any(o.before == "init" and o.after == "query" for o in result)
        assert not any(o.after == "close" for o in result)


# ---------------------------------------------------------------------------
# _order_cleanup_last
# ---------------------------------------------------------------------------


class TestOrderCleanupLast:
    """Edge cases for operation-before-cleanup ordering."""

    def test_zero_tools(self):
        result = _order_cleanup_last([], {})
        assert result == []

    def test_no_cleanup_category(self):
        tools = [ToolDefinition("query", "", {})]
        cats = {"READ": ["query"]}
        result = _order_cleanup_last(tools, cats)
        assert result == []

    def test_cleanup_only_no_others(self):
        """Only cleanup tools, nothing else to order before."""
        tools = [ToolDefinition("close", "", {})]
        cats = {"CLEANUP": ["close"]}
        result = _order_cleanup_last(tools, cats)
        assert result == []

    def test_lifecycle_excluded_from_non_cleanup(self):
        """Lifecycle tools are excluded from 'non-cleanup' side."""
        tools = [
            ToolDefinition("init", "", {}),
            ToolDefinition("close", "", {}),
            ToolDefinition("query", "", {}),
        ]
        cats = {"LIFECYCLE": ["init"], "CLEANUP": ["close"], "READ": ["query"]}
        result = _order_cleanup_last(tools, cats)
        # query -> close, but NOT init -> close
        assert any(o.before == "query" and o.after == "close" for o in result)
        assert not any(o.before == "init" for o in result)


# ---------------------------------------------------------------------------
# _order_crud_sequence
# ---------------------------------------------------------------------------


class TestOrderCrudSequence:
    """Edge cases for CREATE-before-READ/UPDATE/DELETE ordering."""

    def test_empty_categories(self):
        result = _order_crud_sequence({})
        assert result == []

    def test_create_only(self):
        """CREATE with no READ/UPDATE/DELETE means no CRUD orderings."""
        cats = {"CREATE": ["create_user"]}
        result = _order_crud_sequence(cats)
        assert result == []

    def test_read_only_no_create(self):
        """READ without CREATE means no CRUD orderings."""
        cats = {"READ": ["get_data"]}
        result = _order_crud_sequence(cats)
        assert result == []


# ---------------------------------------------------------------------------
# _order_by_schema_refs
# ---------------------------------------------------------------------------


class TestOrderBySchemaRefs:
    """Edge cases for schema-based ordering inference."""

    def test_zero_tools(self):
        result = _order_by_schema_refs([], {})
        assert result == []

    def test_tool_with_empty_schema(self):
        """Tool with empty schema has no id fields to cross-reference."""
        tools = [ToolDefinition("process", "Do stuff", {})]
        cats = {"CREATE": ["create_thing"]}
        result = _order_by_schema_refs(tools, cats)
        assert result == []

    def test_no_create_category(self):
        """No CREATE tools means no schema cross-references possible."""
        tools = [
            ToolDefinition("process", "Do stuff", {
                "required": ["user_id"],
                "properties": {"user_id": {"type": "string"}},
            }),
        ]
        result = _order_by_schema_refs(tools, {})
        assert result == []

    def test_id_field_no_matching_create(self):
        """Tool has user_id but no create_user tool exists."""
        tools = [
            ToolDefinition("process", "", {
                "required": ["user_id"],
                "properties": {"user_id": {"type": "string"}},
            }),
        ]
        # CREATE tool name doesn't contain 'user'
        cats = {"CREATE": ["create_widget"]}
        result = _order_by_schema_refs(tools, cats)
        assert result == []


# ---------------------------------------------------------------------------
# _order_by_description
# ---------------------------------------------------------------------------


class TestOrderByDescription:
    """Edge cases for description-keyword ordering inference."""

    def test_zero_tools(self):
        result = _order_by_description([])
        assert result == []

    def test_empty_description(self):
        """Tool with empty description matches nothing."""
        tools = [
            ToolDefinition("setup", "", {}),
            ToolDefinition("process", "", {}),
        ]
        result = _order_by_description(tools)
        assert result == []

    def test_no_keyword_in_description(self):
        """Description without 'after', 'requires', 'must first' yields nothing."""
        tools = [
            ToolDefinition("setup", "Initialize the system", {}),
            ToolDefinition("process", "Process data quickly", {}),
        ]
        result = _order_by_description(tools)
        assert result == []

    def test_short_tool_name_word_boundary(self):
        """Tool name of 1-2 chars uses word boundary matching (regex \\b)."""
        tools = [
            ToolDefinition("ab", "Do ab thing", {}),
            ToolDefinition("process", "Must call ab first before this after ab", {}),
        ]
        result = _order_by_description(tools)
        # 'ab' is <= 3 chars, uses word boundary regex
        assert any(o.before == "ab" and o.after == "process" for o in result)

    def test_short_name_no_false_match_in_substring(self):
        """Short tool name 'ab' should NOT match inside 'abstract'."""
        tools = [
            ToolDefinition("ab", "Do ab", {}),
            ToolDefinition("abstract_process", "Must run abstract_process after start", {}),
        ]
        result = _order_by_description(tools)
        # 'ab' should NOT match inside 'abstract_process' description because
        # the description says "after start", not "after ab"
        ab_refs = [o for o in result if o.before == "ab"]
        assert len(ab_refs) == 0

    def test_self_reference_excluded(self):
        """Tool referencing itself in description should NOT create self-ordering."""
        tools = [
            ToolDefinition("setup", "Call setup to initialize. Requires setup.", {}),
        ]
        result = _order_by_description(tools)
        assert all(o.before != o.after for o in result)

    def test_self_name_in_own_description_with_other_tools(self):
        """Tool mentions its own name AND another tool in description."""
        tools = [
            ToolDefinition("init", "Initialize the system", {}),
            ToolDefinition("process", "Process requires init. This is process.", {}),
        ]
        result = _order_by_description(tools)
        # process mentions "init" in a "requires" context
        assert any(o.before == "init" and o.after == "process" for o in result)
        # process should NOT self-reference
        assert not any(o.before == "process" and o.after == "process" for o in result)

    def test_long_tool_name_uses_substring(self):
        """Tool name > 3 chars uses simple substring matching (not regex)."""
        tools = [
            ToolDefinition("initialize_system", "Init sys", {}),
            ToolDefinition("run_pipeline", "Must run after initialize_system", {}),
        ]
        result = _order_by_description(tools)
        assert any(
            o.before == "initialize_system" and o.after == "run_pipeline"
            for o in result
        )


# ---------------------------------------------------------------------------
# _infer_orderings -- MAX_ORDERINGS cap
# ---------------------------------------------------------------------------


class TestInferOrderingsMaxCap:
    """Edge: orderings exceeding _MAX_ORDERINGS (200) are truncated."""

    def test_many_tools_capped_at_200(self):
        """With 20 lifecycle + 20 other tools = 400 potential orderings, capped at 200."""
        lifecycle_tools = [
            ToolDefinition(f"init_{i}", "", {}) for i in range(20)
        ]
        other_tools = [
            ToolDefinition(f"do_{i}", "", {}) for i in range(20)
        ]
        all_tools = lifecycle_tools + other_tools
        cats = _categorize_tools(all_tools)
        orderings = _infer_orderings(all_tools, cats)
        assert len(orderings) <= 200

    def test_deduplication_before_cap(self):
        """Duplicate (before, after) pairs are deduplicated before cap check."""
        tools = [
            ToolDefinition("connect", "Connect to DB", {}),
            ToolDefinition("query", "Query data. Requires connect.", {}),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        # connect -> query appears from lifecycle AND from description
        # Should be deduplicated
        connect_query = [(o.before, o.after) for o in orderings if o.before == "connect" and o.after == "query"]
        assert len(connect_query) == 1

    def test_self_ordering_excluded(self):
        """step.before != step.after is enforced globally."""
        tools = [
            ToolDefinition("setup", "Must call setup after setup", {}),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        assert all(o.before != o.after for o in orderings)


# ---------------------------------------------------------------------------
# _categorize_tools -- unknown categories
# ---------------------------------------------------------------------------


class TestCategorizeToolsEdge:
    """Edge: tools with no matching category pattern."""

    def test_zero_tools(self):
        cats = _categorize_tools([])
        # No categories should be populated (all empty removed)
        assert cats == {}

    def test_all_unrecognized(self):
        """All tools go to OTHER when none match known patterns."""
        tools = [
            ToolDefinition("frobnicate", "", {}),
            ToolDefinition("quuxify", "", {}),
        ]
        cats = _categorize_tools(tools)
        assert list(cats.keys()) == ["OTHER"]
        assert set(cats["OTHER"]) == {"frobnicate", "quuxify"}

    def test_single_char_name(self):
        """Single character tool name still categorized."""
        tools = [ToolDefinition("x", "", {})]
        cats = _categorize_tools(tools)
        assert "x" in cats["OTHER"]


# ---------------------------------------------------------------------------
# infer_protocol -- warnings
# ---------------------------------------------------------------------------


class TestInferProtocolWarnings:
    """Edge: small servers and destructive tool warnings."""

    def test_two_tools_warning(self):
        """Server with <= 2 tools gets a 'limited ordering inference' warning."""
        tools = [
            ToolDefinition("do_thing", "", {}),
            ToolDefinition("do_other", "", {}),
        ]
        protocol = infer_protocol("tiny", tools)
        assert any("limited ordering inference" in w for w in protocol.warnings)

    def test_one_tool_warning(self):
        tools = [ToolDefinition("only_tool", "", {})]
        protocol = infer_protocol("solo", tools)
        assert any("limited ordering inference" in w for w in protocol.warnings)

    def test_empty_server_name_fallback(self):
        """Empty string server name falls back to 'McpServer'."""
        tools = [ToolDefinition("tool", "", {}), ToolDefinition("other", "", {}), ToolDefinition("more", "", {})]
        protocol = infer_protocol("", tools)
        assert protocol.name == "McpServer"

    def test_special_chars_cleaned(self):
        """Server name with special characters is cleaned for LU identifier."""
        tools = [ToolDefinition("a", "", {}), ToolDefinition("b", "", {}), ToolDefinition("c", "", {})]
        protocol = infer_protocol("my-cool_server!v2", tools)
        # Should be title-cased with special chars removed
        assert protocol.name.isalnum()


# ---------------------------------------------------------------------------
# check_annotations -- more edge cases
# ---------------------------------------------------------------------------


class TestCheckAnnotationsEdge:
    """Edge cases for annotation coherence checks."""

    def test_tool_with_empty_description_no_crash(self):
        """Empty description should not crash pattern matching."""
        tools = [ToolDefinition("mystery", "", {}, {"readOnlyHint": True})]
        findings = check_annotations(tools)
        # No critical finding -- empty name/desc don't match destructive/write
        critical = [f for f in findings if f.severity == "critical"]
        assert len(critical) == 0

    def test_tool_name_only_action_verb(self):
        """Tool named exactly 'delete' (single action verb) triggers destructive checks."""
        tools = [ToolDefinition("delete", "", {}, {"readOnlyHint": True})]
        findings = check_annotations(tools)
        critical = [f for f in findings if f.severity == "critical"]
        assert len(critical) >= 1

    def test_single_tool_no_annotations(self):
        """Single tool with no annotations: coverage warning + destructive warning if applicable."""
        tools = [ToolDefinition("get_data", "Fetch data", {})]
        findings = check_annotations(tools)
        coverage = [f for f in findings if f.tool_name == "*"]
        assert len(coverage) == 1
        assert "0/1" in coverage[0].message

    def test_more_than_5_missing_shows_count(self):
        """When > 5 tools missing annotations, message shows '(+N more)'."""
        annotated = ToolDefinition("read", "Read", {}, {"readOnlyHint": True})
        missing = [ToolDefinition(f"tool_{i}", f"Tool {i}", {}) for i in range(7)]
        tools = [annotated] + missing
        findings = check_annotations(tools)
        coverage = [f for f in findings if f.tool_name == "*"]
        assert len(coverage) == 1
        assert "+2 more" in coverage[0].message
