# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the Lingua Universale v0.2 core parser (_parser.py).

Groups:
    1. TestParseProtocol        - protocol structure, roles, name, loc
    2. TestParseStep            - all 5 actions, sender/receiver/payload
    3. TestParseChoice          - choice block, branches, labels
    4. TestParseProperties      - all 9 property variants, invalid values
    5. TestParseProgram         - empty, single, multiple protocols
    6. TestParseErrors          - error messages and line/col accuracy
    7. TestCanonicalProtocols   - Examples 1, 2, 7, 10 from DESIGN_C1_2

NOTE: No __init__.py in this directory (Package Shadowing Fix).
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._parser import ParseError, parse
from cervellaswarm_lingua_universale._ast import (
    AllParticipate,
    AlwaysTerminates,
    BranchNode,
    ChoiceNode,
    ConfidenceProp,
    ExclusionProp,
    Loc,
    NoDeadlock,
    NoDeletionProp,
    OrderingProp,
    ProgramNode,
    ProtocolNode,
    RoleExclusiveProp,
    StepNode,
    TrustProp,
)


# ===========================================================================
# 1. TestParseProtocol
# ===========================================================================


class TestParseProtocol:
    """Protocol structure: name, roles, steps, properties optional."""

    def test_basic_protocol_name(self) -> None:
        src = """
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
        """
        program = parse(src)
        assert len(program.declarations) == 1
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "DelegateTask"

    def test_basic_protocol_roles(self) -> None:
        src = """
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.roles == ("regina", "worker", "guardiana")

    def test_protocol_steps_count(self) -> None:
        src = """
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.steps) == 4

    def test_protocol_without_properties_is_valid(self) -> None:
        src = """
            protocol Simple:
                roles: alpha, beta

                alpha asks beta to do task
                beta returns result to alpha
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.properties == ()

    def test_protocol_with_properties(self) -> None:
        src = """
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina

                properties:
                    always terminates
                    no deadlock
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 2

    def test_protocol_with_choice(self) -> None:
        src = """
            protocol PlanAndBuild:
                roles: regina, architect, worker

                regina asks architect to plan
                architect returns plan to regina

                when regina decides:
                    approve:
                        regina asks worker to do task
                        worker returns result to regina
                    reject:
                        regina tells architect decision
                        architect returns plan to regina
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        # 2 steps + 1 choice
        assert len(proto.steps) == 3

    def test_protocol_loc_is_set(self) -> None:
        src = """
            protocol MyProto:
                roles: a, b

                a asks b to do task
                b returns result to a
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert isinstance(proto.loc, Loc)
        assert proto.loc.line >= 1

    def test_single_role_protocol(self) -> None:
        src = """
            protocol Solo:
                roles: agent

                agent asks agent to do task
                agent returns result to agent
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.roles == ("agent",)

    def test_protocol_no_steps_raises(self) -> None:
        src = """
            protocol Empty:
                roles: a, b
        """
        with pytest.raises(ParseError, match="at least one step"):
            parse(src)

    def test_protocol_no_roles_raises(self) -> None:
        src = """
            protocol Missing:
                a asks b to do task
                b returns result to a
        """
        with pytest.raises(ParseError):
            parse(src)


# ===========================================================================
# 2. TestParseStep
# ===========================================================================


class TestParseStep:
    """Step parsing: all 5 action verbs, payload and receiver extraction."""

    def _single_step(self, action_line: str) -> StepNode:
        """Helper: parse a protocol with a single step."""
        src = f"""
            protocol T:
                roles: a, b

                {action_line}
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        step = proto.steps[0]
        assert isinstance(step, StepNode)
        return step

    def test_asks_action(self) -> None:
        step = self._single_step("regina asks worker to do task")
        assert step.sender == "regina"
        assert step.action == "asks"
        assert step.receiver == "worker"
        assert step.payload == "do task"

    def test_returns_action(self) -> None:
        step = self._single_step("worker returns result to regina")
        assert step.sender == "worker"
        assert step.action == "returns"
        assert step.receiver == "regina"
        assert step.payload == "result"

    def test_tells_action(self) -> None:
        step = self._single_step("regina tells architect decision")
        assert step.sender == "regina"
        assert step.action == "tells"
        assert step.receiver == "architect"
        assert step.payload == "decision"

    def test_proposes_action(self) -> None:
        step = self._single_step("architect proposes plan to regina")
        assert step.sender == "architect"
        assert step.action == "proposes"
        assert step.receiver == "regina"
        assert step.payload == "plan"

    def test_sends_action(self) -> None:
        step = self._single_step("regina sends message to worker")
        assert step.sender == "regina"
        assert step.action == "sends"
        assert step.receiver == "worker"
        assert step.payload == "message"

    def test_step_loc_is_set(self) -> None:
        step = self._single_step("regina asks worker to do task")
        assert isinstance(step.loc, Loc)
        assert step.loc.line >= 1

    def test_unknown_action_raises(self) -> None:
        src = """
            protocol T:
                roles: a, b

                a blasts b to pieces
        """
        with pytest.raises(ParseError, match="cannot parse action"):
            parse(src)

    def test_malformed_asks_missing_to_raises(self) -> None:
        # 'asks' with only 2 words after - not enough for the pattern
        src = """
            protocol T:
                roles: a, b

                a asks b
        """
        with pytest.raises(ParseError):
            parse(src)


# ===========================================================================
# 3. TestParseChoice
# ===========================================================================


class TestParseChoice:
    """Choice block: decider, branches, labels, steps."""

    def _parse_choice_proto(self, src: str) -> ProtocolNode:
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        return proto

    def test_choice_two_branches(self) -> None:
        src = """
            protocol PlanAndBuild:
                roles: regina, architect, worker, guardiana

                regina asks architect to plan
                architect returns plan to regina

                when regina decides:
                    approve:
                        regina asks worker to do task
                        worker returns result to regina
                    reject:
                        regina tells architect decision
                        architect returns plan to regina
        """
        proto = self._parse_choice_proto(src)
        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        assert choice.decider == "regina"
        assert len(choice.branches) == 2

    def test_choice_branch_labels(self) -> None:
        src = """
            protocol PlanAndBuild:
                roles: regina, architect, worker, guardiana

                regina asks architect to plan
                architect returns plan to regina

                when regina decides:
                    approve:
                        regina asks worker to do task
                        worker returns result to regina
                    reject:
                        regina tells architect decision
                        architect returns plan to regina
        """
        proto = self._parse_choice_proto(src)
        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        labels = [b.label for b in choice.branches]
        assert "approve" in labels
        assert "reject" in labels

    def test_choice_branch_steps(self) -> None:
        src = """
            protocol T:
                roles: a, b

                when a decides:
                    yes:
                        a asks b to do task
                        b returns result to a
                    no:
                        a tells b decision
        """
        proto = self._parse_choice_proto(src)
        choice = proto.steps[0]
        assert isinstance(choice, ChoiceNode)
        yes_branch = next(br for br in choice.branches if br.label == "yes")
        assert isinstance(yes_branch, BranchNode)
        assert len(yes_branch.steps) == 2

    def test_choice_branch_loc_is_set(self) -> None:
        src = """
            protocol T:
                roles: a, b

                when a decides:
                    option:
                        a asks b to do task
        """
        proto = self._parse_choice_proto(src)
        choice = proto.steps[0]
        assert isinstance(choice, ChoiceNode)
        assert isinstance(choice.branches[0].loc, Loc)

    def test_empty_branch_raises(self) -> None:
        # A branch label with no indented body: tokenizer emits no INDENT,
        # so the parser raises ParseError (missing INDENT or no steps).
        src = """
            protocol T:
                roles: a, b

                when a decides:
                    yes:
        """
        with pytest.raises(ParseError):
            parse(src)

    def test_empty_choice_raises(self) -> None:
        src = """
            protocol T:
                roles: a, b

                when a decides:
        """
        with pytest.raises(ParseError):
            parse(src)


# ===========================================================================
# 4. TestParseProperties
# ===========================================================================


class TestParseProperties:
    """All 9 property variants and validation errors."""

    def _props(self, *prop_lines: str) -> list:
        lines = "\n                    ".join(prop_lines)
        src = f"""
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a

                properties:
                    {lines}
        """
        proto = parse(src).declarations[0]
        assert isinstance(proto, ProtocolNode)
        return list(proto.properties)

    def test_always_terminates(self) -> None:
        props = self._props("always terminates")
        assert len(props) == 1
        assert isinstance(props[0], AlwaysTerminates)

    def test_no_deadlock(self) -> None:
        props = self._props("no deadlock")
        assert len(props) == 1
        assert isinstance(props[0], NoDeadlock)

    def test_all_roles_participate(self) -> None:
        props = self._props("all roles participate")
        assert len(props) == 1
        assert isinstance(props[0], AllParticipate)

    def test_confidence_high(self) -> None:
        props = self._props("confidence >= high")
        assert len(props) == 1
        prop = props[0]
        assert isinstance(prop, ConfidenceProp)
        assert prop.level == "high"

    def test_confidence_all_levels(self) -> None:
        for level in ("certain", "high", "medium", "low", "speculative"):
            props = self._props(f"confidence >= {level}")
            assert isinstance(props[0], ConfidenceProp)
            assert props[0].level == level

    def test_trust_trusted(self) -> None:
        props = self._props("trust >= trusted")
        assert len(props) == 1
        prop = props[0]
        assert isinstance(prop, TrustProp)
        assert prop.tier == "trusted"

    def test_trust_all_tiers(self) -> None:
        for tier in ("verified", "trusted", "standard", "untrusted"):
            props = self._props(f"trust >= {tier}")
            assert isinstance(props[0], TrustProp)
            assert props[0].tier == tier

    def test_ordering_prop(self) -> None:
        props = self._props("task_request before task_result")
        assert len(props) == 1
        prop = props[0]
        assert isinstance(prop, OrderingProp)
        assert prop.before == "task_request"
        assert prop.after == "task_result"

    def test_exclusion_prop(self) -> None:
        props = self._props("backend cannot send audit_verdict")
        assert len(props) == 1
        prop = props[0]
        assert isinstance(prop, ExclusionProp)
        assert prop.role == "backend"
        assert prop.message == "audit_verdict"

    def test_no_deletion(self) -> None:
        props = self._props("no deletion")
        assert len(props) == 1
        assert isinstance(props[0], NoDeletionProp)

    def test_role_exclusive(self) -> None:
        props = self._props("approver exclusive verdict")
        assert len(props) == 1
        prop = props[0]
        assert isinstance(prop, RoleExclusiveProp)
        assert prop.role == "approver"
        assert prop.message == "verdict"

    def test_invalid_confidence_level_raises(self) -> None:
        with pytest.raises(ParseError, match="invalid confidence level"):
            self._props("confidence >= extreme")

    def test_invalid_trust_tier_raises(self) -> None:
        with pytest.raises(ParseError, match="invalid trust tier"):
            self._props("trust >= superuser")

    def test_multiple_properties(self) -> None:
        props = self._props(
            "always terminates",
            "no deadlock",
            "confidence >= high",
            "trust >= standard",
            "all roles participate",
        )
        assert len(props) == 5

    def test_property_loc_is_set(self) -> None:
        props = self._props("always terminates")
        assert isinstance(props[0].loc, Loc)
        assert props[0].loc.line >= 1


# ===========================================================================
# 5. TestParseProgram
# ===========================================================================


class TestParseProgram:
    """Top-level program node: empty, single, multiple declarations."""

    def test_empty_program(self) -> None:
        program = parse("")
        assert isinstance(program, ProgramNode)
        assert program.declarations == ()

    def test_empty_program_whitespace_only(self) -> None:
        program = parse("   \n\n   ")
        assert isinstance(program, ProgramNode)
        assert program.declarations == ()

    def test_single_protocol_program(self) -> None:
        src = """
            protocol Simple:
                roles: a, b

                a asks b to do task
                b returns result to a
        """
        program = parse(src)
        assert len(program.declarations) == 1
        assert isinstance(program.declarations[0], ProtocolNode)

    def test_multiple_protocols_program(self) -> None:
        src = """
            protocol First:
                roles: a, b

                a asks b to do task
                b returns result to a

            protocol Second:
                roles: x, y

                x tells y decision
                y returns result to x
        """
        program = parse(src)
        assert len(program.declarations) == 2
        names = [d.name for d in program.declarations]
        assert names == ["First", "Second"]

    def test_program_loc_is_set(self) -> None:
        src = """
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a
        """
        program = parse(src)
        assert isinstance(program.loc, Loc)


# ===========================================================================
# 6. TestParseErrors
# ===========================================================================


class TestParseErrors:
    """Error quality: line/col attributes, informative messages."""

    def test_parse_error_has_line(self) -> None:
        src = "protocol Missing:\n    roles: a, b\n"
        with pytest.raises(ParseError) as exc_info:
            parse(src)
        assert exc_info.value.line >= 1

    def test_parse_error_has_col(self) -> None:
        src = """
            protocol T:
                roles: a, b

                a blasts b to pieces
        """
        with pytest.raises(ParseError) as exc_info:
            parse(src)
        # col is present (may be 0)
        assert isinstance(exc_info.value.col, int)

    def test_unknown_action_message_is_informative(self) -> None:
        src = """
            protocol T:
                roles: a, b

                a destroys b entirely
        """
        with pytest.raises(ParseError) as exc_info:
            parse(src)
        msg = str(exc_info.value)
        # Must mention the bad action text
        assert "destroys" in msg or "cannot parse action" in msg

    def test_protocol_missing_roles_raises(self) -> None:
        src = """
            protocol NoRoles:
                a asks b to do task
                b returns result to a
        """
        with pytest.raises(ParseError):
            parse(src)

    def test_protocol_missing_steps_raises(self) -> None:
        src = """
            protocol NoSteps:
                roles: a, b
        """
        with pytest.raises(ParseError, match="at least one step"):
            parse(src)

    def test_invalid_confidence_message_lists_valid_levels(self) -> None:
        src = """
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a

                properties:
                    confidence >= impossible
        """
        with pytest.raises(ParseError) as exc_info:
            parse(src)
        msg = str(exc_info.value)
        assert "certain" in msg or "high" in msg or "speculative" in msg

    def test_error_message_includes_location(self) -> None:
        src = """
            protocol T:
                roles: a, b

                a blasts b to pieces
        """
        with pytest.raises(ParseError) as exc_info:
            parse(src)
        msg = str(exc_info.value)
        assert "line" in msg


# ===========================================================================
# 7. TestCanonicalProtocols
# ===========================================================================


class TestCanonicalProtocols:
    """Full parse of canonical examples from DESIGN_C1_2_SYNTAX_GRAMMAR.md."""

    def test_example1_delegate_task(self) -> None:
        """Esempio 1: DelegateTask - basic protocol with all 4 properties."""
        src = """
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    task_request before task_result
                    all roles participate
        """
        program = parse(src)
        assert len(program.declarations) == 1
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "DelegateTask"
        assert proto.roles == ("regina", "worker", "guardiana")
        assert len(proto.steps) == 4
        assert len(proto.properties) == 4

        # Check first step
        step0 = proto.steps[0]
        assert isinstance(step0, StepNode)
        assert step0.sender == "regina"
        assert step0.action == "asks"
        assert step0.receiver == "worker"
        assert step0.payload == "do task"

        # Check last step
        step3 = proto.steps[3]
        assert isinstance(step3, StepNode)
        assert step3.sender == "guardiana"
        assert step3.action == "returns"
        assert step3.receiver == "regina"
        assert step3.payload == "verdict"

        # Check properties
        prop_types = [type(p) for p in proto.properties]
        assert AlwaysTerminates in prop_types
        assert NoDeadlock in prop_types
        assert OrderingProp in prop_types
        assert AllParticipate in prop_types

    def test_example2_plan_and_build(self) -> None:
        """Esempio 2: PlanAndBuild - protocol with choice block."""
        src = """
            protocol PlanAndBuild:
                roles: regina, architect, worker, guardiana

                regina asks architect to plan
                architect returns plan to regina

                when regina decides:
                    approve:
                        regina tells architect decision
                        regina asks worker to do task
                        worker returns result to regina
                        regina asks guardiana to verify
                        guardiana returns verdict to regina
                    reject:
                        regina tells architect decision
                        architect returns plan to regina

                properties:
                    always terminates
                    no deadlock
                    confidence >= high
        """
        program = parse(src)
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "PlanAndBuild"
        assert len(proto.roles) == 4

        # 2 steps + 1 choice = 3 step_or_choice
        assert len(proto.steps) == 3

        choice = proto.steps[2]
        assert isinstance(choice, ChoiceNode)
        assert choice.decider == "regina"
        assert len(choice.branches) == 2

        approve = next(b for b in choice.branches if b.label == "approve")
        reject = next(b for b in choice.branches if b.label == "reject")
        assert len(approve.steps) == 5
        assert len(reject.steps) == 2

        # Properties
        assert len(proto.properties) == 3
        conf_props = [p for p in proto.properties if isinstance(p, ConfidenceProp)]
        assert len(conf_props) == 1
        assert conf_props[0].level == "high"

    def test_example7_secure_audit(self) -> None:
        """Esempio 7: SecureAudit - trust + confidence + exclusion properties."""
        src = """
            protocol SecureAudit:
                roles: regina, guardiana, backend

                regina asks backend to do task
                backend returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    trust >= trusted
                    backend cannot send audit_verdict
                    confidence >= high
        """
        program = parse(src)
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "SecureAudit"
        assert len(proto.properties) == 5

        trust_props = [p for p in proto.properties if isinstance(p, TrustProp)]
        assert len(trust_props) == 1
        assert trust_props[0].tier == "trusted"

        excl_props = [p for p in proto.properties if isinstance(p, ExclusionProp)]
        assert len(excl_props) == 1
        assert excl_props[0].role == "backend"
        assert excl_props[0].message == "audit_verdict"

        conf_props = [p for p in proto.properties if isinstance(p, ConfidenceProp)]
        assert len(conf_props) == 1
        assert conf_props[0].level == "high"

    def test_example10_code_review_protocol(self) -> None:
        """Esempio 10: CodeReview protocol portion - 7 properties."""
        src = """
            protocol CodeReview:
                roles: regina, backend, tester, guardiana

                regina asks backend to do task
                backend returns result to regina
                regina asks tester to verify
                tester returns verdict to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    task_request before task_result
                    backend cannot send audit_verdict
                    tester cannot send task_result
                    trust >= standard
                    all roles participate
        """
        program = parse(src)
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert proto.name == "CodeReview"
        assert len(proto.roles) == 4
        assert len(proto.steps) == 6
        assert len(proto.properties) == 7

        # Verify property types present (7 of 9; no_deletion + exclusive tested in test_parser_constructs)
        prop_types = {type(p) for p in proto.properties}
        assert AlwaysTerminates in prop_types
        assert NoDeadlock in prop_types
        assert OrderingProp in prop_types
        assert ExclusionProp in prop_types
        assert TrustProp in prop_types
        assert AllParticipate in prop_types

        # Two ExclusionProp entries
        excl = [p for p in proto.properties if isinstance(p, ExclusionProp)]
        assert len(excl) == 2
        excl_roles = {p.role for p in excl}
        assert "backend" in excl_roles
        assert "tester" in excl_roles
