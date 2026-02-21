# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Regression tests for S386 bug hunt (Code Review + Bug Hunt #9).

All 6 P1 bugs were FIXED in the current codebase.
These tests verify the fixes hold and catch any regression.

  P1-1: Standard protocol instances not re-exported from __init__  -> FIXED
  P1-2: SessionChecker stored role_bindings by reference (aliasing) -> FIXED
  P1-3: _safe_lean_ident did not handle leading digit / empty      -> FIXED
  P1-4: SessionEnded.timestamp could receive None from completed_at -> FIXED
  P1-5: Session duration mixed time.time() and time.monotonic()    -> FIXED
  P1-6: DSL round-trip lost max_repetitions                        -> FIXED
"""

import time
from unittest.mock import patch

import pytest

from cervellaswarm_lingua_universale.checker import SessionChecker
from cervellaswarm_lingua_universale.dsl import parse_protocol, render_protocol
from cervellaswarm_lingua_universale.integration import (
    AgentInfo,
    create_session,
)
from cervellaswarm_lingua_universale.lean4_bridge import (
    _safe_lean_ident,
    generate_lean4_multi,
)
from cervellaswarm_lingua_universale.monitor import (
    EventCollector,
    ProtocolMonitor,
    SessionEnded,
)
from cervellaswarm_lingua_universale.protocols import Protocol, ProtocolStep
from cervellaswarm_lingua_universale.types import AgentRole, MessageKind, TaskRequest


def _one_step_protocol(name: str = "OneStep") -> Protocol:
    step = ProtocolStep(
        sender="regina", receiver="worker",
        message_kind=MessageKind.TASK_REQUEST,
    )
    return Protocol(name=name, roles=("regina", "worker"), elements=(step,))


# ── P1-1: Standard protocol instances re-exported from package root ───────────


class TestBugP1StandardProtocolsExported:
    """DelegateTask / ArchitectFlow / ResearchFlow / SimpleTask must be
    importable directly from cervellaswarm_lingua_universale and in __all__."""

    def test_delegate_task_importable(self):
        from cervellaswarm_lingua_universale import DelegateTask
        assert DelegateTask.name == "DelegateTask"

    def test_architect_flow_importable(self):
        from cervellaswarm_lingua_universale import ArchitectFlow
        assert ArchitectFlow.name == "ArchitectFlow"

    def test_research_flow_importable(self):
        from cervellaswarm_lingua_universale import ResearchFlow
        assert ResearchFlow.name == "ResearchFlow"

    def test_simple_task_importable(self):
        from cervellaswarm_lingua_universale import SimpleTask
        assert SimpleTask.name == "SimpleTask"

    def test_all_four_in_dunder_all(self):
        import cervellaswarm_lingua_universale as pkg
        for name in ("DelegateTask", "ArchitectFlow", "ResearchFlow", "SimpleTask"):
            assert name in pkg.__all__, f"'{name}' missing from __all__"

    def test_exported_symbols_are_protocol_instances(self):
        from cervellaswarm_lingua_universale import (
            DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask,
        )
        for proto in (DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask):
            assert isinstance(proto, Protocol)


# ── P1-2: SessionChecker copies role_bindings (no aliasing) ──────────────────


class TestBugP1BindingsCopied:
    """SessionChecker.__init__ must copy role_bindings with dict(), not alias."""

    def test_stored_bindings_is_different_object(self):
        proto = _one_step_protocol()
        original: dict[str, str] = {"worker": "cervella-backend"}
        checker = SessionChecker(proto, session_id="B001", role_bindings=original)
        assert checker._role_bindings is not original

    def test_mutation_after_construction_not_visible(self):
        proto = _one_step_protocol()
        original: dict[str, str] = {"worker": "cervella-backend"}
        checker = SessionChecker(proto, session_id="B002", role_bindings=original)
        original["worker"] = "cervella-frontend"
        # Must still resolve cervella-backend -> worker (original binding)
        checker.send("regina", "cervella-backend",
                     TaskRequest(task_id="T1", description="x"))
        assert checker.is_complete

    def test_new_key_after_construction_not_visible(self):
        proto = _one_step_protocol()
        original: dict[str, str] = {}
        checker = SessionChecker(proto, session_id="B003", role_bindings=original)
        original["worker"] = "cervella-backend"
        assert "worker" not in checker._role_bindings

    def test_none_bindings_yields_empty_dict(self):
        proto = _one_step_protocol()
        checker = SessionChecker(proto, session_id="B004", role_bindings=None)
        assert checker._role_bindings == {}


# ── P1-3: _safe_lean_ident handles leading digit and empty string ──────────────


class TestBugP1SafeLeanIdent:
    """_safe_lean_ident must: raise on empty, prepend '_' for leading digit."""

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            _safe_lean_ident("")

    def test_leading_digit_gets_prefix(self):
        assert _safe_lean_ident("123") == "_123"

    def test_digit_then_letters_gets_prefix(self):
        assert _safe_lean_ident("42abc") == "_42abc"

    def test_single_digit_gets_prefix(self):
        assert _safe_lean_ident("7") == "_7"

    def test_valid_ident_unchanged(self):
        assert _safe_lean_ident("valid_name") == "valid_name"
        assert _safe_lean_ident("CamelCase") == "CamelCase"

    def test_special_chars_replaced(self):
        assert _safe_lean_ident("hello-world") == "hello_world"


# ── P1-4: SessionEnded.timestamp is always float (never None) ─────────────────


class TestBugP1SessionEndedTimestamp:
    """SessionEnded.timestamp must be float. completed_at guard prevents None."""

    def _run_session(self, session_id: str):
        proto = _one_step_protocol()
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)
        checker = SessionChecker(proto, session_id=session_id, monitor=monitor)
        checker.send("regina", "worker",
                     TaskRequest(task_id="T1", description="x"))
        return collector.events

    def test_timestamp_is_float(self):
        events = self._run_session("TS001")
        ended = [e for e in events if isinstance(e, SessionEnded)]
        assert len(ended) == 1
        assert isinstance(ended[0].timestamp, float)

    def test_timestamp_is_in_valid_range(self):
        t_before = time.time()
        events = self._run_session("TS002")
        t_after = time.time()
        ended = [e for e in events if isinstance(e, SessionEnded)]
        assert t_before <= ended[0].timestamp <= t_after

    def test_completed_at_is_set(self):
        proto = _one_step_protocol()
        checker = SessionChecker(proto, session_id="TS003")
        checker.send("regina", "worker",
                     TaskRequest(task_id="T1", description="x"))
        assert checker._state.completed_at is not None


# ── P1-5: Session duration uses monotonic clock ────────────────────────────────


class TestBugP1DurationMonotonicClock:
    """duration_ms must use time.monotonic() to survive NTP backward jumps."""

    def test_state_has_monotonic_fields(self):
        from cervellaswarm_lingua_universale.checker import SessionState
        fields = SessionState.__dataclass_fields__
        assert "started_at_mono" in fields
        assert "completed_at_mono" in fields

    def test_duration_ms_non_negative(self):
        proto = _one_step_protocol()
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)
        checker = SessionChecker(proto, session_id="DUR001", monitor=monitor)
        checker.send("regina", "worker",
                     TaskRequest(task_id="T1", description="x"))
        ended = [e for e in collector.events if isinstance(e, SessionEnded)]
        assert ended[0].duration_ms >= 0

    def test_duration_survives_ntp_backward_jump(self):
        """Patch time.time() to go backward; duration_ms must still be >= 0."""
        proto = _one_step_protocol()
        monitor = ProtocolMonitor()
        collector = EventCollector()
        monitor.add_listener(collector)

        call_count = 0

        def fake_time() -> float:
            nonlocal call_count
            call_count += 1
            return 1000.0 if call_count <= 1 else 999.0  # backward jump

        with patch("cervellaswarm_lingua_universale.checker.time.time", fake_time):
            checker = SessionChecker(proto, session_id="DUR002", monitor=monitor)
            checker.send("regina", "worker",
                         TaskRequest(task_id="T1", description="ntp"))

        ended = [e for e in collector.events if isinstance(e, SessionEnded)]
        assert ended, "No SessionEnded event"
        assert ended[0].duration_ms >= 0, (
            f"duration_ms={ended[0].duration_ms}: monotonic clock not used"
        )


# ── P1-6: DSL round-trip preserves max_repetitions ────────────────────────────


class TestBugP1DslRoundTripMaxRepetitions:
    """render_protocol() must emit max_repetitions; parse_protocol() must read it."""

    def _make_repeat_protocol(self, n: int) -> Protocol:
        step = ProtocolStep(
            sender="regina", receiver="worker",
            message_kind=MessageKind.TASK_REQUEST,
        )
        return Protocol(
            name=f"Repeat{n}", roles=("regina", "worker"),
            elements=(step,), max_repetitions=n,
        )

    def test_round_trip_max_rep_3(self):
        original = self._make_repeat_protocol(3)
        parsed = parse_protocol(render_protocol(original))
        assert parsed.max_repetitions == 3

    def test_round_trip_max_rep_5(self):
        original = self._make_repeat_protocol(5)
        parsed = parse_protocol(render_protocol(original))
        assert parsed.max_repetitions == 5

    def test_render_includes_max_repetitions(self):
        proto = self._make_repeat_protocol(5)
        rendered = render_protocol(proto)
        assert "max_repetitions" in rendered
        assert "5" in rendered

    def test_default_max_rep_round_trips(self):
        original = self._make_repeat_protocol(1)
        parsed = parse_protocol(render_protocol(original))
        assert parsed.max_repetitions == 1


# ── P2: create_session with custom catalog ───────────────────────────────────


class TestP2CreateSessionCustomCatalog:
    """create_session() must validate bindings against custom catalog."""

    def _mini_catalog(self):
        from types import MappingProxyType
        info = AgentInfo(
            role=AgentRole.REGINA,
            agent_name="cervella-orchestrator",
            protocol_roles=("regina",),
        )
        worker = AgentInfo(
            role=AgentRole.BACKEND,
            agent_name="cervella-backend",
            protocol_roles=("worker",),
        )
        return MappingProxyType({AgentRole.REGINA: info, AgentRole.BACKEND: worker})

    def test_custom_catalog_accepts_known_agent(self):
        proto = _one_step_protocol()
        cat = self._mini_catalog()
        checker = create_session(
            proto,
            bindings={"worker": "cervella-backend"},
            catalog=cat,
        )
        assert not checker.is_complete

    def test_custom_catalog_rejects_unknown_agent(self):
        proto = _one_step_protocol()
        cat = self._mini_catalog()
        with pytest.raises(ValueError, match="unknown agent name"):
            create_session(
                proto,
                bindings={"worker": "cervella-frontend"},
                catalog=cat,
            )


# ── P2: generate_lean4_multi rejects duplicate protocol names ────────────────


class TestP2Lean4MultiDuplicateNames:
    """generate_lean4_multi() must reject protocols with duplicate names."""

    def test_duplicate_names_raises(self):
        p1 = _one_step_protocol("Proto")
        p2 = _one_step_protocol("Proto")
        with pytest.raises(ValueError, match="duplicate protocol names"):
            generate_lean4_multi([p1, p2])

    def test_unique_names_ok(self):
        p1 = _one_step_protocol("ProtoA")
        p2 = _one_step_protocol("ProtoB")
        result = generate_lean4_multi([p1, p2])
        assert "ProtoA" in result
        assert "ProtoB" in result
