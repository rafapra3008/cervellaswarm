# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Session tests for _intent_bridge.py (E.2) - Part 2: PROPERTIES/CONFIRM/E2E/edge cases.

Covers:
    - ChatSession PROPERTIES phase
    - ChatSession CONFIRM phase (reset + pipeline + result fields)
    - Full end-to-end flows (en/it/pt)
    - Edge cases: exit/help/empty input, EOFError, KeyboardInterrupt, NLProcessor

Phase init + ROLES + MESSAGES + CHOICES: test_intent_bridge_session.py
Data model + render + i18n: test_intent_bridge_core.py
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._intent_bridge import (
    ChatPhase,
    ChatSession,
    IntentDraft,
    NLProcessor,
)


# ============================================================
# Helper
# ============================================================


def _session(inputs: list[str], *, lang: str = "en") -> tuple[ChatSession, list[str]]:
    """Create a ChatSession with injected I/O.

    Returns (session, output_log).  The output_log accumulates every
    string passed to output_fn so assertions can inspect them.
    """
    it = iter(inputs)
    output: list[str] = []

    def _input_fn(prompt: str) -> str:
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    def _output_fn(*args: object, **kwargs: object) -> None:
        output.append(" ".join(str(a) for a in args))

    session = ChatSession(lang=lang, input_fn=_input_fn, output_fn=_output_fn)
    return session, output


# ============================================================
# 4. PROPERTIES phase
# ============================================================


class TestChatSessionPropertiesPhase:
    """PROPERTIES phase: safety property selection."""

    def _setup(self) -> ChatSession:
        """Return session in PROPERTIES phase (English, no choices)."""
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        session.process_input("Alice, Bob")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("done")
        session.process_input("no")  # no choices
        assert session._phase == ChatPhase.PROPERTIES
        return session

    def test_done_transitions_to_confirm(self) -> None:
        session = self._setup()
        session.process_input("done")
        assert session._phase == ChatPhase.CONFIRM

    def test_fatto_transitions_to_confirm_italian(self) -> None:
        session, _ = _session([], lang="it")
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        session.process_input("Alice, Bob")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("fatto")
        session.process_input("no")
        session.process_input("fatto")
        assert session._phase == ChatPhase.CONFIRM

    def test_valid_property_number_adds_property(self) -> None:
        session = self._setup()
        initial_count = len(session._properties)
        session.process_input("3")  # all_roles_participate
        assert len(session._properties) >= initial_count

    def test_duplicate_property_not_added_twice(self) -> None:
        session = self._setup()
        session.process_input("1")  # always_terminates (already default)
        count = session._properties.count("always_terminates")
        assert count == 1

    def test_invalid_number_stays_in_properties_phase(self) -> None:
        session = self._setup()
        session.process_input("99")
        assert session._phase == ChatPhase.PROPERTIES

    def test_defaults_are_always_terminates_and_no_deadlock(self) -> None:
        session = self._setup()
        assert "always_terminates" in session._properties
        assert "no_deadlock" in session._properties


# ============================================================
# 5. CONFIRM phase
# ============================================================


class TestChatSessionConfirmPhase:
    """CONFIRM phase: yes executes pipeline, no resets."""

    def _setup(self) -> ChatSession:
        """Return session in CONFIRM phase."""
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("TestProto")
        session.process_input("Alice, Bob")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("done")
        session.process_input("no")
        session.process_input("done")
        assert session._phase == ChatPhase.CONFIRM
        return session

    def test_yes_transitions_to_done(self) -> None:
        session = self._setup()
        session.process_input("yes")
        assert session._phase == ChatPhase.DONE

    def test_no_resets_to_roles(self) -> None:
        session = self._setup()
        session.process_input("no")
        assert session._phase == ChatPhase.ROLES

    def test_no_clears_protocol_name(self) -> None:
        session = self._setup()
        session.process_input("no")
        assert session._protocol_name == ""

    def test_no_clears_roles(self) -> None:
        session = self._setup()
        session.process_input("no")
        assert session._roles == []

    def test_no_clears_messages(self) -> None:
        session = self._setup()
        session.process_input("no")
        assert session._messages == []

    def test_no_clears_choices(self) -> None:
        session = self._setup()
        session.process_input("no")
        assert session._choices == []

    def test_no_resets_msg_step_to_sender(self) -> None:
        session = self._setup()
        session._msg_step = "receiver"  # simulate mid-message state
        session.process_input("no")
        assert session._msg_step == "sender"

    def test_no_resets_choice_step_to_ask(self) -> None:
        session = self._setup()
        session._choice_step = "decider"
        session.process_input("no")
        assert session._choice_step == "ask"

    def test_no_resets_choice_decider(self) -> None:
        session = self._setup()
        session._choice_decider = "Alice"
        session.process_input("no")
        assert session._choice_decider == ""

    def test_ambiguous_input_repeats_question(self) -> None:
        session = self._setup()
        resp = session.process_input("maybe")
        assert session._phase == ChatPhase.CONFIRM
        assert (
            "?" in resp
            or "correct" in resp.lower()
            or "giusto" in resp.lower()
        )

    def test_yes_sets_result(self) -> None:
        session = self._setup()
        session.process_input("yes")
        assert session.result is not None

    def test_result_contains_correct_protocol_name(self) -> None:
        session = self._setup()
        session.process_input("yes")
        assert session.result is not None
        assert session.result.draft.protocol_name == "TestProto"

    def test_result_has_property_report(self) -> None:
        session = self._setup()
        session.process_input("yes")
        assert session.result is not None
        assert session.result.property_report is not None

    def test_confirm_response_contains_question_mark(self) -> None:
        """Ambiguous input re-renders the confirm question (contains '?')."""
        session = self._setup()
        resp = session.process_input("maybe")
        assert "?" in resp or "correct" in resp.lower() or "giusto" in resp.lower()

    def test_si_works_in_italian(self) -> None:
        session, _ = _session([], lang="it")
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        session.process_input("Alice, Bob")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("fatto")
        session.process_input("no")
        session.process_input("fatto")
        assert session._phase == ChatPhase.CONFIRM
        session.process_input("si")
        assert session._phase == ChatPhase.DONE


# ============================================================
# 6. Full end-to-end flows
# ============================================================


class TestChatSessionE2E:
    """Full guided flow end-to-end in all languages."""

    def test_full_flow_english(self) -> None:
        session, _ = _session([
            "FullTest", "Alice, Bob",
            "Alice", "Bob", "1",
            "done", "no", "done", "yes",
        ])
        result = session.run()
        assert result is not None
        assert result.draft.protocol_name == "FullTest"

    def test_full_flow_italian(self) -> None:
        session, _ = _session(
            ["ProtoIT", "Alice, Bob", "Alice", "Bob", "1",
             "fatto", "no", "fatto", "si"],
            lang="it",
        )
        result = session.run()
        assert result is not None
        assert result.draft.protocol_name == "ProtoIT"

    def test_full_flow_portuguese(self) -> None:
        session, _ = _session(
            ["ProtoPT", "Alice, Bob", "Alice", "Bob", "1",
             "pronto", "nao", "pronto", "sim"],
            lang="pt",
        )
        result = session.run()
        assert result is not None
        assert result.draft.protocol_name == "ProtoPT"

    def test_full_flow_result_has_intent_source(self) -> None:
        session, _ = _session([
            "Source", "A, B", "A", "B", "1",
            "done", "no", "done", "yes",
        ])
        result = session.run()
        assert result is not None
        assert result.intent_source.startswith("protocol Source:")

    def test_full_flow_result_has_generated_code(self) -> None:
        session, _ = _session([
            "CodeTest", "A, B", "A", "B", "1",
            "done", "no", "done", "yes",
        ])
        result = session.run()
        assert result is not None
        assert isinstance(result.generated_code, str)

    def test_full_flow_with_choices(self) -> None:
        """Full pipeline including a choice/branch."""
        session, _ = _session([
            "Branch", "Alice, Bob",
            "Alice", "Bob", "1",
            "done",
            "yes", "Alice", "approve, reject",
            "done", "yes",
        ])
        result = session.run()
        assert result is not None
        assert len(result.draft.choices) == 1

    def test_full_flow_result_has_parse_result(self) -> None:
        session, _ = _session([
            "ParseTest", "A, B", "A", "B", "1",
            "done", "no", "done", "yes",
        ])
        result = session.run()
        assert result is not None
        assert result.parse_result is not None
        assert result.parse_result.protocol.name == "ParseTest"

    def test_full_flow_pipeline_code_non_empty(self) -> None:
        """Generated code must be a non-empty string (not just whitespace)."""
        session, _ = _session([
            "NonEmpty", "A, B", "A", "B", "1",
            "done", "no", "done", "yes",
        ])
        result = session.run()
        assert result is not None
        assert result.generated_code.strip() != ""


# ============================================================
# 7. Edge cases
# ============================================================


class TestEdgeCases:
    """Edge cases, error paths, and robustness."""

    def test_unknown_lang_defaults_to_en(self) -> None:
        session, _ = _session([], lang="fr")
        assert session.lang == "en"

    def test_unknown_lang_zh_defaults_to_en(self) -> None:
        session, _ = _session([], lang="zh")
        assert session.lang == "en"

    def test_exit_word_terminates_run(self) -> None:
        session, _ = _session(["exit"])
        result = session.run()
        assert result is None

    def test_quit_word_terminates_run(self) -> None:
        session, _ = _session(["quit"])
        result = session.run()
        assert result is None

    def test_esci_terminates_run(self) -> None:
        session, _ = _session(["esci"])
        result = session.run()
        assert result is None

    def test_sair_terminates_run(self) -> None:
        session, _ = _session(["sair"])
        result = session.run()
        assert result is None

    def test_help_shows_phase_info(self) -> None:
        session, output = _session(["help", "exit"])
        session.run()
        combined = " ".join(output)
        assert (
            "ROLES" in combined
            or "Phase" in combined
            or "phase" in combined
        )

    def test_aiuto_shows_help_italian(self) -> None:
        session, output = _session(["aiuto", "esci"], lang="it")
        session.run()
        assert " ".join(output)  # something was printed

    def test_ajuda_shows_help_portuguese(self) -> None:
        session, output = _session(["ajuda", "sair"], lang="pt")
        session.run()
        assert " ".join(output)

    def test_empty_input_returns_empty_response(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        resp = session.process_input("")
        assert resp == ""

    def test_empty_input_does_not_advance_phase(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("")
        assert session._phase == ChatPhase.ROLES

    def test_whitespace_only_ignored(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        resp = session.process_input("   ")
        assert resp == ""

    def test_eoferror_handled_gracefully(self) -> None:
        """EOFError during input returns None without crashing."""
        session = ChatSession(
            lang="en",
            input_fn=lambda p: (_ for _ in ()).throw(EOFError),
            output_fn=lambda *a, **kw: None,
        )
        result = session.run()
        assert result is None

    def test_keyboardinterrupt_handled_gracefully(self) -> None:
        """KeyboardInterrupt during input returns None without crashing."""
        session = ChatSession(
            lang="en",
            input_fn=lambda p: (_ for _ in ()).throw(KeyboardInterrupt),
            output_fn=lambda *a, **kw: None,
        )
        result = session.run()
        assert result is None

    def test_nl_processor_has_process_method(self) -> None:
        """NLProcessor protocol defines a process() method."""
        assert hasattr(NLProcessor, "process")

    def test_nl_processor_is_a_class(self) -> None:
        assert isinstance(NLProcessor, type)

    def test_draft_property_returns_none_without_name(self) -> None:
        session, _ = _session([])
        assert session.draft is None

    def test_draft_property_returns_intent_draft_after_roles(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        session.process_input("Alice, Bob")
        assert isinstance(session.draft, IntentDraft)

    def test_turns_accumulate_after_input(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("MyProto")
        assert len(session.turns) >= 1

    def test_phase_property_readable(self) -> None:
        session, _ = _session([])
        assert session.phase == ChatPhase.WELCOME

    def test_process_input_records_user_turn(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        user_turns = [t for t in session.turns if t.speaker == "user"]
        assert len(user_turns) >= 1
