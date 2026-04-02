# SPDX-License-Identifier: Apache-2.0
"""Edge-case tests for _codegen_common.py -- collect_all_steps, used_message_kinds.

S486 HARDTEST: empty protocols, choice-only protocols, deep nesting,
empty branches, mixed steps/choices.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._codegen_common import (
    collect_all_steps,
    used_message_kinds,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _step(sender: str, receiver: str, kind: MessageKind, desc: str = "") -> ProtocolStep:
    return ProtocolStep(sender=sender, receiver=receiver, message_kind=kind, description=desc)


def _choice(decider: str, branches: dict) -> ProtocolChoice:
    return ProtocolChoice(decider=decider, branches=branches)


# ---------------------------------------------------------------------------
# collect_all_steps
# ---------------------------------------------------------------------------


class TestCollectAllStepsEmpty:
    """Edge: protocol with zero elements."""

    def test_empty_elements(self):
        """Empty sequence returns empty list."""
        assert collect_all_steps(()) == []

    def test_empty_list(self):
        """Empty list (not tuple) also works."""
        assert collect_all_steps([]) == []


class TestCollectAllStepsChoiceOnly:
    """Edge: protocol containing ONLY ProtocolChoice, no bare ProtocolStep."""

    def test_single_choice_collects_branch_steps(self):
        s1 = _step("a", "b", MessageKind.TASK_REQUEST)
        s2 = _step("b", "a", MessageKind.TASK_RESULT)
        choice = _choice("a", {
            "left": (s1,),
            "right": (s2,),
        })
        steps = collect_all_steps((choice,))
        assert len(steps) == 2
        assert s1 in steps
        assert s2 in steps

    def test_multiple_choices_no_bare_steps(self):
        """Two consecutive choices, zero bare steps at the top."""
        s1 = _step("a", "b", MessageKind.TASK_REQUEST)
        s2 = _step("b", "a", MessageKind.TASK_RESULT)
        s3 = _step("a", "b", MessageKind.AUDIT_REQUEST)
        c1 = _choice("a", {"x": (s1,)})
        c2 = _choice("b", {"y": (s2, s3)})
        steps = collect_all_steps((c1, c2))
        assert len(steps) == 3


class TestCollectAllStepsDeepNesting:
    """Edge: nested choices 3+ levels deep."""

    def test_three_levels_deep(self):
        """Steps buried 3 levels deep must be collected."""
        leaf = _step("a", "b", MessageKind.DM)
        inner = _choice("a", {"deep": (leaf,)})
        mid = _choice("a", {"mid": (inner,)})
        outer = _choice("a", {"outer": (mid,)})
        steps = collect_all_steps((outer,))
        assert len(steps) == 1
        assert steps[0] is leaf

    def test_five_levels_deep(self):
        """5 levels of nesting -- stress test recursion."""
        leaf = _step("a", "b", MessageKind.BROADCAST)
        elem = leaf
        for _ in range(5):
            elem = _choice("a", {"branch": (elem,)})
        steps = collect_all_steps((elem,))
        assert len(steps) == 1
        assert steps[0].message_kind == MessageKind.BROADCAST

    def test_deep_nesting_multiple_branches_each_level(self):
        """Each nesting level has 2 branches, each with a step."""
        s1 = _step("a", "b", MessageKind.TASK_REQUEST)
        s2 = _step("b", "a", MessageKind.TASK_RESULT)
        s3 = _step("a", "b", MessageKind.AUDIT_REQUEST)
        s4 = _step("b", "a", MessageKind.AUDIT_VERDICT)
        inner = _choice("a", {
            "left": (s3,),
            "right": (s4,),
        })
        outer = _choice("a", {
            "alpha": (s1, inner),
            "beta": (s2,),
        })
        steps = collect_all_steps((outer,))
        assert len(steps) == 4
        assert set(steps) == {s1, s2, s3, s4}


class TestCollectAllStepsEmptyBranch:
    """Edge: ProtocolChoice with a branch containing zero elements.

    Note: ProtocolChoice.__post_init__ requires branches to be non-empty dict,
    but individual branch values can be empty tuples.
    """

    def test_branch_with_empty_tuple(self):
        """A branch mapped to an empty tuple contributes zero steps."""
        s1 = _step("a", "b", MessageKind.TASK_REQUEST)
        choice = _choice("a", {
            "populated": (s1,),
            "empty": (),
        })
        steps = collect_all_steps((choice,))
        assert len(steps) == 1
        assert steps[0] is s1

    def test_all_branches_empty(self):
        """All branches are empty tuples -- zero steps collected."""
        choice = _choice("a", {
            "b1": (),
            "b2": (),
        })
        steps = collect_all_steps((choice,))
        assert steps == []


class TestCollectAllStepsMixed:
    """Edge: interleaving bare steps and choices."""

    def test_step_choice_step(self):
        """step -> choice -> step pattern collects all."""
        s1 = _step("a", "b", MessageKind.TASK_REQUEST)
        s2 = _step("b", "a", MessageKind.TASK_RESULT)
        s3 = _step("a", "b", MessageKind.AUDIT_REQUEST)
        choice = _choice("a", {"x": (s2,)})
        steps = collect_all_steps((s1, choice, s3))
        assert len(steps) == 3
        assert steps[0] is s1
        assert steps[1] is s2
        assert steps[2] is s3

    def test_ordering_preserved(self):
        """Steps are collected in DFS order: bare steps before branch steps."""
        s_top = _step("a", "b", MessageKind.TASK_REQUEST)
        s_branch = _step("b", "a", MessageKind.TASK_RESULT)
        s_bottom = _step("a", "b", MessageKind.AUDIT_REQUEST)
        choice = _choice("a", {"x": (s_branch,)})
        steps = collect_all_steps((s_top, choice, s_bottom))
        assert steps == [s_top, s_branch, s_bottom]


# ---------------------------------------------------------------------------
# used_message_kinds
# ---------------------------------------------------------------------------


class TestUsedMessageKindsEmpty:
    """Edge: protocol with no elements has no used kinds."""

    def test_empty_protocol(self):
        proto = Protocol(
            name="Empty",
            roles=("a", "b"),
            elements=(),
        )
        assert used_message_kinds(proto) == []


class TestUsedMessageKindsDedup:
    """Edge: same MessageKind used multiple times appears once."""

    def test_duplicated_kind(self):
        s1 = _step("a", "b", MessageKind.TASK_REQUEST)
        s2 = _step("b", "a", MessageKind.TASK_REQUEST)
        proto = Protocol(name="Dup", roles=("a", "b"), elements=(s1, s2))
        kinds = used_message_kinds(proto)
        assert kinds.count(MessageKind.TASK_REQUEST) == 1


class TestUsedMessageKindsEnumOrder:
    """Edge: results follow MessageKind enum order, not insertion order."""

    def test_enum_order_not_insertion_order(self):
        """Even if AUDIT_VERDICT is first in elements, it appears after TASK_REQUEST in result."""
        s1 = _step("a", "b", MessageKind.AUDIT_VERDICT)
        s2 = _step("b", "a", MessageKind.TASK_REQUEST)
        proto = Protocol(name="Order", roles=("a", "b"), elements=(s1, s2))
        kinds = used_message_kinds(proto)
        assert len(kinds) == 2
        # TASK_REQUEST comes before AUDIT_VERDICT in enum definition
        assert kinds.index(MessageKind.TASK_REQUEST) < kinds.index(MessageKind.AUDIT_VERDICT)


class TestUsedMessageKindsFromChoice:
    """Edge: message kinds used only inside choice branches are still collected."""

    def test_kinds_from_nested_choice(self):
        s1 = _step("a", "b", MessageKind.DM)
        choice = _choice("a", {"branch": (s1,)})
        proto = Protocol(name="Nested", roles=("a", "b"), elements=(choice,))
        kinds = used_message_kinds(proto)
        assert MessageKind.DM in kinds
