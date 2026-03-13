# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Session tests for _intent_bridge.py (E.2) - Part 1: init, ROLES, MESSAGES, CHOICES.

Covers:
    - ChatSession initialization (lang, phase, default attributes)
    - ChatSession ROLES phase (protocol name + role collection)
    - ChatSession MESSAGES phase (sender/receiver/action sub-state)
    - ChatSession CHOICES phase (branching, decider, branch names)

PROPERTIES + CONFIRM + E2E + edge cases: test_intent_bridge_session_e2e.py
Data model + render + i18n: test_intent_bridge_core.py
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._intent_bridge import (
    ChatPhase,
    ChatSession,
    IntentDraft,
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
# 0. ChatSession initialization
# ============================================================


class TestChatSessionInit:
    """ChatSession initialization and default attribute values."""

    def test_default_lang_is_en(self) -> None:
        session = ChatSession(output_fn=lambda *a, **kw: None)
        assert session.lang == "en"

    def test_invalid_lang_falls_back_to_en(self) -> None:
        session = ChatSession(lang="de", output_fn=lambda *a, **kw: None)
        assert session.lang == "en"

    def test_custom_output_fn_called(self) -> None:
        captured: list[str] = []
        session = ChatSession(
            output_fn=lambda *a, **kw: captured.append(str(a[0]) if a else ""),
            input_fn=lambda p: (_ for _ in ()).throw(EOFError),
        )
        session.run()
        assert len(captured) > 0

    def test_phase_is_welcome_before_run(self) -> None:
        session = ChatSession(output_fn=lambda *a, **kw: None)
        assert session.phase == ChatPhase.WELCOME

    def test_phase_is_roles_after_run_begins(self) -> None:
        """run() transitions from WELCOME to ROLES then reads first input."""
        session = ChatSession(
            output_fn=lambda *a, **kw: None,
            # First input triggers ROLES; raise EOFError to stop immediately.
            input_fn=lambda p: (_ for _ in ()).throw(EOFError),
        )
        session.run()
        # After run() exits via EOFError the phase has advanced to ROLES.
        assert session.phase == ChatPhase.ROLES

    def test_msg_step_initialized_to_sender(self) -> None:
        session = ChatSession(output_fn=lambda *a, **kw: None)
        assert session._msg_step == "sender"

    def test_choice_step_initialized_to_ask(self) -> None:
        session = ChatSession(output_fn=lambda *a, **kw: None)
        assert session._choice_step == "ask"

    def test_properties_initialized_with_defaults(self) -> None:
        session = ChatSession(output_fn=lambda *a, **kw: None)
        assert "always_terminates" in session._properties
        assert "no_deadlock" in session._properties

    def test_result_is_none_before_run(self) -> None:
        session = ChatSession(output_fn=lambda *a, **kw: None)
        assert session.result is None


# ============================================================
# 1. ROLES phase
# ============================================================


class TestChatSessionRolesPhase:
    """ROLES phase: protocol name then role list."""

    def test_valid_name_asks_for_roles(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        resp = session.process_input("MyProtocol")
        assert (
            "roles" in resp.lower()
            or "ruoli" in resp.lower()
            or "papeis" in resp.lower()
        )

    def test_invalid_name_numbers_at_start(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        resp = session.process_input("1BadName")
        # Error message mentions names/letters
        assert (
            "letter" in resp.lower()
            or "lettere" in resp.lower()
            or "letras" in resp.lower()
            or "nomi" in resp.lower()
            or "nomes" in resp.lower()
            or "names" in resp.lower()
        )

    def test_invalid_name_special_chars_not_accepted(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("My-Protocol!")
        assert session._protocol_name == ""  # name was not accepted

    def test_valid_name_accepted(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("ValidName")
        assert session._protocol_name == "ValidName"

    def test_name_with_spaces_converted_to_underscore(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("My Protocol")
        assert session._protocol_name == "My_Protocol"

    def test_valid_2_roles_transitions_to_messages(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("TestProto")
        session.process_input("Alice, Bob")
        assert session._phase == ChatPhase.MESSAGES

    def test_valid_3_roles_accepted(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("TestProto")
        session.process_input("Alice, Bob, Charlie")
        assert len(session._roles) == 3

    def test_only_1_role_gives_error(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("TestProto")
        resp = session.process_input("OnlyOne")
        assert (
            "2" in resp
            or "least" in resp.lower()
            or "almeno" in resp.lower()
            or "menos" in resp.lower()
        )
        assert session._phase == ChatPhase.ROLES

    def test_roles_with_invalid_name_rejected(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("TestProto")
        session.process_input("Alice, 1Bad")
        assert session._phase == ChatPhase.ROLES  # still in ROLES

    def test_roles_confirmed_message_shows_role_names(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        resp = session.process_input("Alice, Bob")
        assert "Alice" in resp
        assert "Bob" in resp

    def test_underscore_name_valid(self) -> None:
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("My_Protocol_V2")
        assert session._protocol_name == "My_Protocol_V2"

    def test_roles_with_extra_spaces_trimmed(self) -> None:
        """Roles like ' Alice , Bob ' are trimmed and accepted."""
        session, _ = _session([])
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        session.process_input(" Alice , Bob ")
        assert "Alice" in session._roles
        assert "Bob" in session._roles


# ============================================================
# 2. MESSAGES phase
# ============================================================


class TestChatSessionMessagesPhase:
    """MESSAGES phase: collect sender, receiver, action."""

    def _setup(self, lang: str = "en") -> ChatSession:
        """Return session in MESSAGES phase with Alice, Bob."""
        session, _ = _session([], lang=lang)
        session._phase = ChatPhase.ROLES
        session.process_input("TestProto")
        session.process_input("Alice, Bob")
        assert session._phase == ChatPhase.MESSAGES
        return session

    def test_valid_sender_asks_receiver(self) -> None:
        session = self._setup()
        resp = session.process_input("Alice")
        # en: "Who receives?", it: "Chi riceve?", pt: "Quem recebe?"
        assert (
            "receive" in resp.lower()
            or "riceve" in resp.lower()
            or "recebe" in resp.lower()
        )

    def test_invalid_sender_gives_error(self) -> None:
        session = self._setup()
        resp = session.process_input("Charlie")
        assert (
            "unknown" in resp.lower()
            or "sconosciuto" in resp.lower()
            or "desconhecido" in resp.lower()
            or "charlie" in resp.lower()
        )

    def test_valid_receiver_shows_action_menu(self) -> None:
        session = self._setup()
        session.process_input("Alice")  # sender
        resp = session.process_input("Bob")  # receiver
        assert "1" in resp or "2" in resp

    def test_same_sender_receiver_gives_error(self) -> None:
        session = self._setup()
        session.process_input("Alice")  # sender
        resp = session.process_input("Alice")  # same as sender
        assert (
            "different" in resp.lower()
            or "diversi" in resp.lower()
            or "diferentes" in resp.lower()
        )

    def test_action_selection_by_number_adds_message(self) -> None:
        session = self._setup()
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        assert len(session._messages) == 1

    def test_done_with_messages_transitions_to_choices(self) -> None:
        session = self._setup()
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("done")
        assert session._phase == ChatPhase.CHOICES

    def test_fatto_transitions_to_choices_italian(self) -> None:
        session = self._setup(lang="it")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("fatto")
        assert session._phase == ChatPhase.CHOICES

    def test_pronto_transitions_to_choices_portuguese(self) -> None:
        session = self._setup(lang="pt")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("pronto")
        assert session._phase == ChatPhase.CHOICES

    def test_done_with_no_messages_gives_error(self) -> None:
        session = self._setup()
        resp = session.process_input("done")
        assert session._phase == ChatPhase.MESSAGES
        assert (
            "1" in resp
            or "least" in resp.lower()
            or "almeno" in resp.lower()
            or "menos" in resp.lower()
        )

    def test_out_of_range_action_number_not_added(self) -> None:
        session = self._setup()
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("99")  # out of range
        assert len(session._messages) == 0

    def test_non_numeric_action_not_added(self) -> None:
        session = self._setup()
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("notanumber")
        assert len(session._messages) == 0

    def test_two_messages_added_sequentially(self) -> None:
        session = self._setup()
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input("Bob")
        session.process_input("Alice")
        session.process_input("2")
        assert len(session._messages) == 2

    def test_message_added_confirmation_shown(self) -> None:
        session = self._setup()
        session.process_input("Alice")
        session.process_input("Bob")
        resp = session.process_input("1")
        assert "Added" in resp or "Aggiunto" in resp or "Adicionado" in resp

    def test_invalid_receiver_gives_error(self) -> None:
        session = self._setup()
        session.process_input("Alice")  # valid sender
        resp = session.process_input("Nobody")  # invalid receiver
        assert (
            "unknown" in resp.lower()
            or "sconosciuto" in resp.lower()
            or "nobody" in resp.lower()
        )

    def test_msg_substep_cycles_sender_receiver_action(self) -> None:
        """Sub-state cycles: sender -> receiver -> action -> back to sender."""
        session = self._setup()
        assert session._msg_step == "sender"
        session.process_input("Alice")
        assert session._msg_step == "receiver"
        session.process_input("Bob")
        assert session._msg_step == "action"
        session.process_input("1")
        assert session._msg_step == "sender"


# ============================================================
# 3. CHOICES phase
# ============================================================


class TestChatSessionChoicesPhase:
    """CHOICES phase: optional branching."""

    def _setup(self, lang: str = "en") -> ChatSession:
        """Return session in CHOICES phase with 1 message Alice->Bob."""
        done_word = {"en": "done", "it": "fatto", "pt": "pronto"}.get(lang, "done")
        session, _ = _session([], lang=lang)
        session._phase = ChatPhase.ROLES
        session.process_input("Proto")
        session.process_input("Alice, Bob")
        session.process_input("Alice")
        session.process_input("Bob")
        session.process_input("1")
        session.process_input(done_word)
        assert session._phase == ChatPhase.CHOICES
        return session

    def test_no_transitions_to_properties(self) -> None:
        session = self._setup()
        session.process_input("no")
        assert session._phase == ChatPhase.PROPERTIES

    def test_yes_asks_for_decider(self) -> None:
        session = self._setup()
        resp = session.process_input("yes")
        assert "decide" in resp.lower() or "decider" in resp.lower()

    def test_si_asks_for_decider_italian(self) -> None:
        session = self._setup(lang="it")
        resp = session.process_input("si")
        assert "decide" in resp.lower() or "ruolo" in resp.lower()

    def test_invalid_decider_role_gives_error(self) -> None:
        session = self._setup()
        session.process_input("yes")
        resp = session.process_input("Nobody")
        assert "unknown" in resp.lower() or "nobody" in resp.lower()

    def test_valid_decider_asks_for_branches(self) -> None:
        session = self._setup()
        session.process_input("yes")
        resp = session.process_input("Alice")
        assert (
            "branch" in resp.lower()
            or "option" in resp.lower()
            or "nome" in resp.lower()
            or "name" in resp.lower()
        )

    def test_single_branch_name_rejected(self) -> None:
        session = self._setup()
        session.process_input("yes")
        session.process_input("Alice")
        session.process_input("only_one")
        assert session._phase == ChatPhase.CHOICES  # stays

    def test_two_branches_accepted_transitions_to_properties(self) -> None:
        session = self._setup()
        session.process_input("yes")
        session.process_input("Alice")
        session.process_input("approve, reject")
        assert session._phase == ChatPhase.PROPERTIES
        assert len(session._choices) == 1

    def test_choice_decider_stored_correctly(self) -> None:
        session = self._setup()
        session.process_input("yes")
        session.process_input("Alice")
        session.process_input("approve, reject")
        assert session._choices[0].decider == "Alice"

    def test_three_branches_stored(self) -> None:
        session = self._setup()
        session.process_input("yes")
        session.process_input("Alice")
        session.process_input("left, right, middle")
        assert len(session._choices[0].branches) == 3

    def test_ambiguous_input_stays_in_choices_phase(self) -> None:
        session = self._setup()
        session.process_input("maybe")
        assert session._phase == ChatPhase.CHOICES

    def test_draft_choice_created_correctly(self) -> None:
        """DraftChoice branches have correct structure after acceptance."""
        session = self._setup()
        session.process_input("yes")
        session.process_input("Alice")
        session.process_input("approve, reject")
        choice = session._choices[0]
        branch_names = [label for label, _ in choice.branches]
        assert "approve" in branch_names
        assert "reject" in branch_names
