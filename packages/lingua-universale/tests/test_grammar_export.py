# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _grammar_export.py (C2.4.3 -- Validation).

Test structure:
  - Basic: GrammarExporter returns non-empty strings with correct markers
  - GBNF structure: rule count, root rule, ws/ws1, closed lists
  - Lark parsability: lark.Lark() accepts the grammar without errors
  - Lark round-trip: 10 canonical .lu examples parse with the exported Lark
  - Version: GRAMMAR_VERSION embedded in output

Dependency: ``lark`` (test-only, pure Python).
"""

from __future__ import annotations

import re

import pytest

from cervellaswarm_lingua_universale._grammar_export import (
    GRAMMAR_VERSION,
    GrammarExporter,
)


# =====================================================================
# 1. BASIC OUTPUT
# =====================================================================


class TestBasicOutput:
    """GrammarExporter returns well-formed grammar strings."""

    def test_to_gbnf_returns_string(self) -> None:
        result = GrammarExporter.to_gbnf()
        assert isinstance(result, str)
        assert len(result) > 100

    def test_to_lark_returns_string(self) -> None:
        result = GrammarExporter.to_lark()
        assert isinstance(result, str)
        assert len(result) > 100

    def test_gbnf_contains_root_rule(self) -> None:
        assert "root" in GrammarExporter.to_gbnf()
        assert 'root           ::= ws program ws' in GrammarExporter.to_gbnf()

    def test_lark_contains_start_rule(self) -> None:
        assert "?start: program" in GrammarExporter.to_lark()

    def test_version_in_gbnf(self) -> None:
        assert f"Version: {GRAMMAR_VERSION}" in GrammarExporter.to_gbnf()

    def test_version_in_lark(self) -> None:
        assert f"Version: {GRAMMAR_VERSION}" in GrammarExporter.to_lark()

    def test_version_method(self) -> None:
        assert GrammarExporter.version() == GRAMMAR_VERSION

    def test_instance_call_also_works(self) -> None:
        """STUDIO C2.4 shows usage with instance; verify it works."""
        exporter = GrammarExporter()
        assert exporter.to_gbnf() == GrammarExporter.to_gbnf()
        assert exporter.to_lark() == GrammarExporter.to_lark()


# =====================================================================
# 2. GBNF STRUCTURE
# =====================================================================


class TestGBNFStructure:
    """GBNF grammar has the expected 47 rules and structure."""

    @pytest.fixture()
    def gbnf(self) -> str:
        return GrammarExporter.to_gbnf()

    def test_rule_count_47(self, gbnf: str) -> None:
        rules = re.findall(r"^[a-z][\w-]*\s+::=", gbnf, re.MULTILINE)
        assert len(rules) == 47, f"Expected 47 rules, got {len(rules)}: {rules}"

    def test_ws_rule(self, gbnf: str) -> None:
        assert r'ws             ::= [ \t\n\r]*' in gbnf

    def test_ws1_rule(self, gbnf: str) -> None:
        assert r'ws1            ::= [ \t\n]+' in gbnf

    def test_verb_closed_list(self, gbnf: str) -> None:
        for v in ("do", "verify", "plan", "research", "shutdown"):
            assert f'"{v}"' in gbnf

    def test_noun_closed_list(self, gbnf: str) -> None:
        for n in ("result", "verdict", "plan", "decision", "report",
                  "message", "broadcast", "context", "ack"):
            assert f'"{n}"' in gbnf

    def test_no_indent_dedent(self, gbnf: str) -> None:
        assert "INDENT" not in gbnf
        assert "DEDENT" not in gbnf

    def test_comparison_operators(self, gbnf: str) -> None:
        for op in ("==", "!=", "<=", ">=", "<", ">"):
            assert f'"{op}"' in gbnf

    def test_string_no_newline(self, gbnf: str) -> None:
        """STRING rule excludes newlines (D6)."""
        assert r'[^"\n]*' in gbnf
        assert r"[^'\n]*" in gbnf


# =====================================================================
# 3. LARK PARSABILITY
# =====================================================================


class TestLarkParsability:
    """The exported Lark grammar is accepted by lark.Lark()."""

    @pytest.fixture()
    def parser(self):
        lark = pytest.importorskip("lark")
        grammar = GrammarExporter.to_lark()
        return lark.Lark(grammar, parser="earley")

    def test_lark_accepts_grammar(self, parser) -> None:
        """lark.Lark() does not raise on the exported grammar."""
        assert parser is not None

    def test_lark_lalr_also_works(self) -> None:
        """LALR(1) parser also accepts the grammar (faster runtime)."""
        lark = pytest.importorskip("lark")
        grammar = GrammarExporter.to_lark()
        p = lark.Lark(grammar, parser="lalr")
        assert p is not None

    def test_lark_rule_count_46(self) -> None:
        """40 rules + 4 terminals + 2 directives = 46."""
        grammar = GrammarExporter.to_lark()
        # Rules: lowercase name (or ?start) followed by ":"
        rules = re.findall(r"^\??[a-z]\w*\s*:", grammar, re.MULTILINE)
        # Terminals: UPPERCASE name followed by ":"
        terminals = re.findall(r"^[A-Z]\w*\s*:", grammar, re.MULTILINE)
        # Directives: %ignore
        directives = re.findall(r"^%ignore", grammar, re.MULTILINE)
        total = len(rules) + len(terminals) + len(directives)
        assert len(rules) == 40, f"Expected 40 rules, got {len(rules)}"
        assert len(terminals) == 4, f"Expected 4 terminals, got {len(terminals)}"
        assert len(directives) == 2, f"Expected 2 directives, got {len(directives)}"
        assert total == 46


# =====================================================================
# 4. LARK ROUND-TRIP: 10 CANONICAL EXAMPLES
# =====================================================================


# The 10 golden examples from DESIGN_C1_2 / test_compiler_golden.py.
# Each must parse with the whitespace-lenient Lark grammar.

_G1_VARIANT = "type Status = Active | Inactive | Pending"

_G2_RECORD = """\
type TaskData =
    name: str
    priority: int
    tags: List[str]
    notes: str?
    confidence: Confident[str]
"""

_G3_USE = """\
use python os.path
use python json as json_lib
"""

_G4_AGENT = """\
agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: task.well_defined
    ensures: result.done
"""

_G5_PROTOCOL = """\
protocol DelegateTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
"""

_G6_PROPERTIES = """\
protocol SafeHandoff:
    roles: regina, worker
    regina asks worker to do task
    worker returns result to regina
    properties:
        always terminates
        no deadlock
"""

_G7_MIXED = """\
use python math

type TaskStatus = Pending | Running | Done

type TaskInfo =
    name: str
    priority: int

agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: task.valid
    ensures: result.ok

protocol SimpleTask:
    roles: regina, worker
    regina asks worker to do task
    worker returns result to regina
"""

_G8_BLOCK_CONTRACTS = """\
agent Analyst:
    role: researcher
    trust: trusted
    accepts: ResearchQuery
    produces: ResearchReport
    requires:
        query.valid
        query.length > 0
    ensures:
        result.complete
        result.score > 5
"""

_G9_CHOICE = """\
protocol ReviewTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    when guardiana decides:
        approve:
            guardiana returns verdict to regina
        reject:
            guardiana returns verdict to regina
            regina asks worker to do task
            worker returns result to regina
"""

_G10_TWO_PROTOCOLS = """\
protocol TaskFlow:
    roles: regina, worker
    regina asks worker to do task
    worker returns result to regina

protocol AuditFlow:
    roles: regina, guardiana
    regina asks guardiana to verify
    guardiana returns verdict to regina
"""


_CANONICAL_EXAMPLES = [
    pytest.param(_G1_VARIANT, id="G1-variant-type"),
    pytest.param(_G2_RECORD, id="G2-record-type"),
    pytest.param(_G3_USE, id="G3-use-statements"),
    pytest.param(_G4_AGENT, id="G4-agent-contracts"),
    pytest.param(_G5_PROTOCOL, id="G5-delegate-task"),
    pytest.param(_G6_PROPERTIES, id="G6-properties"),
    pytest.param(_G7_MIXED, id="G7-mixed-program"),
    pytest.param(_G8_BLOCK_CONTRACTS, id="G8-block-contracts"),
    pytest.param(_G9_CHOICE, id="G9-choice-block"),
    pytest.param(_G10_TWO_PROTOCOLS, id="G10-two-protocols"),
]


class TestLarkRoundTrip:
    """Each canonical .lu example parses with the exported Lark grammar."""

    @pytest.fixture()
    def parser(self):
        lark = pytest.importorskip("lark")
        grammar = GrammarExporter.to_lark()
        return lark.Lark(grammar, parser="earley")

    @pytest.mark.parametrize("source", _CANONICAL_EXAMPLES)
    def test_canonical_example(self, parser, source: str) -> None:
        tree = parser.parse(source)
        assert tree is not None
        assert tree.data == "program"


# =====================================================================
# 5. GRAMMAR CONTENT CONSISTENCY
# =====================================================================


class TestGrammarConsistency:
    """Both grammars cover the same language constructs."""

    def test_both_have_protocol(self) -> None:
        assert "protocol" in GrammarExporter.to_gbnf()
        assert "protocol" in GrammarExporter.to_lark()

    def test_both_have_agent(self) -> None:
        assert "agent" in GrammarExporter.to_gbnf()
        assert "agent" in GrammarExporter.to_lark()

    def test_both_have_type(self) -> None:
        assert '"type"' in GrammarExporter.to_gbnf()
        assert '"type"' in GrammarExporter.to_lark()

    def test_both_have_use(self) -> None:
        assert '"use"' in GrammarExporter.to_gbnf()
        assert '"use"' in GrammarExporter.to_lark()

    def test_both_have_requires_ensures(self) -> None:
        for kw in ("requires", "ensures"):
            assert f'"{kw}"' in GrammarExporter.to_gbnf()
            assert f'"{kw}"' in GrammarExporter.to_lark()

    def test_both_have_when_decides(self) -> None:
        assert '"when"' in GrammarExporter.to_gbnf()
        assert '"decides"' in GrammarExporter.to_gbnf()
        assert '"when"' in GrammarExporter.to_lark()
        assert '"decides"' in GrammarExporter.to_lark()

    def test_both_have_properties(self) -> None:
        assert '"properties"' in GrammarExporter.to_gbnf()
        assert '"properties"' in GrammarExporter.to_lark()
