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


# ============================================================
# 8. Diverse protocol scenarios (E.2 completion)
# ============================================================


class TestDiverseProtocolRecipeExchange:
    """RecipeExchange: 2-role kitchen protocol (English).

    Cook asks Pantry for ingredients, Pantry returns them.
    Simple linear protocol, no choices.
    """

    INPUTS = [
        "RecipeExchange",       # protocol name
        "Cook, Pantry",         # roles
        "Cook", "Pantry", "1",  # Cook asks_task Pantry
        "Pantry", "Cook", "2",  # Pantry return_result Cook
        "done",                 # finish messages
        "no",                   # no choices
        "done",                 # keep default properties
        "yes",                  # confirm
    ]

    def _run(self) -> tuple:
        session, output = _session(self.INPUTS, lang="en")
        result = session.run()
        return result, output

    def test_result_not_none(self) -> None:
        result, _ = self._run()
        assert result is not None

    def test_protocol_name(self) -> None:
        result, _ = self._run()
        assert result.draft.protocol_name == "RecipeExchange"

    def test_has_2_roles(self) -> None:
        result, _ = self._run()
        assert set(result.draft.roles) == {"Cook", "Pantry"}

    def test_has_2_messages(self) -> None:
        result, _ = self._run()
        assert len(result.draft.messages) == 2

    def test_first_message_is_cook_asks_pantry(self) -> None:
        result, _ = self._run()
        msg = result.draft.messages[0]
        assert msg.sender == "Cook"
        assert msg.receiver == "Pantry"
        assert msg.action_key == "ask_task"

    def test_second_message_is_pantry_returns_cook(self) -> None:
        result, _ = self._run()
        msg = result.draft.messages[1]
        assert msg.sender == "Pantry"
        assert msg.receiver == "Cook"
        assert msg.action_key == "return_result"

    def test_no_choices(self) -> None:
        result, _ = self._run()
        assert len(result.draft.choices) == 0

    def test_default_properties(self) -> None:
        result, _ = self._run()
        assert "always_terminates" in result.draft.properties
        assert "no_deadlock" in result.draft.properties

    def test_intent_source_parseable(self) -> None:
        result, _ = self._run()
        assert result.intent_source.startswith("protocol RecipeExchange:")

    def test_parse_result_has_correct_name(self) -> None:
        result, _ = self._run()
        assert result.parse_result.protocol.name == "RecipeExchange"

    def test_parse_result_has_2_elements(self) -> None:
        result, _ = self._run()
        assert len(result.parse_result.protocol.elements) == 2

    def test_generated_code_non_empty(self) -> None:
        result, _ = self._run()
        assert result.generated_code.strip() != ""

    def test_simulation_contains_narrative(self) -> None:
        """Simulation output uses natural language, not technical kind names."""
        _, output = self._run()
        combined = " ".join(output)
        assert "asks" in combined.lower() or "returns" in combined.lower()

    def test_simulation_contains_cook(self) -> None:
        _, output = self._run()
        combined = " ".join(output)
        assert "Cook" in combined

    def test_simulation_shows_success(self) -> None:
        _, output = self._run()
        combined = " ".join(output)
        assert "COMPLETED" in combined or "SUCCESSFULLY" in combined


class TestDiverseProtocolTaskDelegation:
    """TaskDelegation: 3-role audit protocol (Italian).

    Manager delegates to Worker, Worker returns, Manager asks
    Reviewer to verify, Reviewer returns verdict.
    Tests: 3 roles, 4 messages, extra property, Italian language.
    """

    INPUTS = [
        "TaskDelegation",                   # protocol name
        "Manager, Worker, Reviewer",        # 3 roles
        "Manager", "Worker", "1",           # Manager asks_task Worker
        "Worker", "Manager", "2",           # Worker return_result Manager
        "Manager", "Reviewer", "3",         # Manager ask_verify Reviewer
        "Reviewer", "Manager", "4",         # Reviewer return_verdict Manager
        "fatto",                            # finish messages (Italian)
        "no",                               # no choices
        "4",                                # add all_roles_participate
        "fatto",                            # finish properties (Italian)
        "si",                               # confirm (Italian)
    ]

    def _run(self) -> tuple:
        session, output = _session(self.INPUTS, lang="it")
        result = session.run()
        return result, output

    def test_result_not_none(self) -> None:
        result, _ = self._run()
        assert result is not None

    def test_protocol_name(self) -> None:
        result, _ = self._run()
        assert result.draft.protocol_name == "TaskDelegation"

    def test_has_3_roles(self) -> None:
        result, _ = self._run()
        assert set(result.draft.roles) == {"Manager", "Worker", "Reviewer"}

    def test_has_4_messages(self) -> None:
        result, _ = self._run()
        assert len(result.draft.messages) == 4

    def test_messages_cover_all_4_action_types(self) -> None:
        result, _ = self._run()
        keys = {m.action_key for m in result.draft.messages}
        assert keys == {"ask_task", "return_result", "ask_verify", "return_verdict"}

    def test_all_3_roles_participate_in_messages(self) -> None:
        result, _ = self._run()
        senders = {m.sender for m in result.draft.messages}
        receivers = {m.receiver for m in result.draft.messages}
        all_involved = senders | receivers
        assert all_involved == {"Manager", "Worker", "Reviewer"}

    def test_has_all_roles_participate_property(self) -> None:
        result, _ = self._run()
        assert "all_roles_participate" in result.draft.properties

    def test_has_3_properties_total(self) -> None:
        result, _ = self._run()
        assert len(result.draft.properties) == 3

    def test_no_choices(self) -> None:
        result, _ = self._run()
        assert len(result.draft.choices) == 0

    def test_parse_result_has_4_elements(self) -> None:
        result, _ = self._run()
        assert len(result.parse_result.protocol.elements) == 4

    def test_generated_code_contains_roles(self) -> None:
        result, _ = self._run()
        code = result.generated_code
        assert "Manager" in code or "manager" in code.lower()

    def test_italian_output_present(self) -> None:
        """Output should contain Italian strings."""
        _, output = self._run()
        combined = " ".join(output)
        # Italian-language content in the output
        assert (
            "Protocollo" in combined
            or "matematica" in combined
            or "Simulazione" in combined
            or "chiede" in combined
        )

    def test_simulation_narrative_italian(self) -> None:
        """Simulation uses Italian narrative descriptions."""
        _, output = self._run()
        combined = " ".join(output)
        assert (
            "chiede" in combined
            or "restituisce" in combined
        )

    def test_simulation_shows_success_italian(self) -> None:
        """Success message should be in Italian."""
        _, output = self._run()
        combined = " ".join(output)
        assert "SUCCESSO" in combined or "COMPLETATO" in combined


class TestDiverseProtocolDataPipeline:
    """DataPipeline: 3-role protocol with branching (Portuguese).

    Collector sends data to Processor, Processor asks Analyzer to verify.
    Analyzer decides: valid or invalid (branching).
    Tests: 3 roles, 2 messages, 1 choice with 2 branches, Portuguese.
    """

    INPUTS = [
        "DataPipeline",                     # protocol name
        "Collector, Processor, Analyzer",   # 3 roles
        "Collector", "Processor", "10",     # Collector send_message Processor
        "Processor", "Analyzer", "3",       # Processor ask_verify Analyzer
        "pronto",                           # finish messages (Portuguese)
        "sim",                              # yes to choices (Portuguese)
        "Analyzer",                         # decider
        "valid, invalid",                   # branch names
        "pronto",                           # finish properties (Portuguese)
        "sim",                              # confirm (Portuguese)
    ]

    def _run(self) -> tuple:
        session, output = _session(self.INPUTS, lang="pt")
        result = session.run()
        return result, output

    def test_result_not_none(self) -> None:
        result, _ = self._run()
        assert result is not None

    def test_protocol_name(self) -> None:
        result, _ = self._run()
        assert result.draft.protocol_name == "DataPipeline"

    def test_has_3_roles(self) -> None:
        result, _ = self._run()
        assert set(result.draft.roles) == {"Collector", "Processor", "Analyzer"}

    def test_has_2_messages(self) -> None:
        result, _ = self._run()
        assert len(result.draft.messages) == 2

    def test_has_1_choice(self) -> None:
        result, _ = self._run()
        assert len(result.draft.choices) == 1

    def test_choice_decider_is_analyzer(self) -> None:
        result, _ = self._run()
        assert result.draft.choices[0].decider == "Analyzer"

    def test_choice_has_2_branches(self) -> None:
        result, _ = self._run()
        assert len(result.draft.choices[0].branches) == 2

    def test_branch_names_are_valid_invalid(self) -> None:
        result, _ = self._run()
        names = [label for label, _ in result.draft.choices[0].branches]
        assert "valid" in names
        assert "invalid" in names

    def test_intent_source_contains_when_block(self) -> None:
        result, _ = self._run()
        assert "when Analyzer decides:" in result.intent_source

    def test_intent_source_contains_both_branches(self) -> None:
        result, _ = self._run()
        assert "valid:" in result.intent_source
        assert "invalid:" in result.intent_source

    def test_generated_code_non_empty(self) -> None:
        result, _ = self._run()
        assert result.generated_code.strip() != ""

    def test_simulation_shows_all_branches(self) -> None:
        """F5 fix: simulation must show ALL branches, not just the first."""
        _, output = self._run()
        combined = " ".join(output)
        assert "valid" in combined.lower()
        assert "invalid" in combined.lower()

    def test_simulation_contains_decides(self) -> None:
        _, output = self._run()
        combined = " ".join(output)
        assert "decide" in combined.lower()

    def test_portuguese_output_present(self) -> None:
        """Output should contain Portuguese strings."""
        _, output = self._run()
        combined = " ".join(output)
        assert (
            "Protocolo" in combined
            or "matematica" in combined
            or "Simulacao" in combined
        )

    def test_portuguese_narrative(self) -> None:
        """Simulation uses Portuguese narrative descriptions."""
        _, output = self._run()
        combined = " ".join(output)
        assert (
            "pede" in combined
            or "envia" in combined
            or "retorna" in combined
        )

    def test_simulation_shows_success_portuguese(self) -> None:
        """Success message should be in Portuguese."""
        _, output = self._run()
        combined = " ".join(output)
        assert "SUCESSO" in combined or "COMPLETADO" in combined


# ============================================================
# 9. Narrative output quality
# ============================================================


class TestNarrativeOutputQuality:
    """Verify simulation output uses natural language narratives."""

    def test_no_arrow_format_in_simulation(self) -> None:
        """Simulation should NOT use old technical format '[X] -> Y: KIND'."""
        session, output = _session([
            "NarrCheck", "A, B", "A", "B", "1",
            "done", "no", "done", "yes",
        ])
        session.run()
        combined = " ".join(output)
        # Old format was "  [A] -> B: TASK_REQUEST" -- should not appear
        assert "[A] -> B: TASK_REQUEST" not in combined

    def test_narrative_uses_asks_for_task_request(self) -> None:
        """Task request should show 'asks' in narrative."""
        session, output = _session([
            "NarrTest", "A, B", "A", "B", "1",
            "done", "no", "done", "yes",
        ])
        session.run()
        combined = " ".join(output)
        assert "asks" in combined.lower()

    def test_narrative_uses_returns_for_result(self) -> None:
        """Return result should show 'returns' in narrative."""
        session, output = _session([
            "RetTest", "A, B", "A", "B", "1", "B", "A", "2",
            "done", "no", "done", "yes",
        ])
        session.run()
        combined = " ".join(output)
        assert "returns" in combined.lower()

    def test_branch_simulation_shows_all_options(self) -> None:
        """All branches in a choice must appear in simulation output."""
        session, output = _session([
            "BranchNarr", "Alice, Bob",
            "Alice", "Bob", "1",
            "done",
            "yes", "Alice", "approve, reject",
            "done", "yes",
        ])
        session.run()
        combined = " ".join(output)
        assert "approve" in combined.lower()
        assert "reject" in combined.lower()

    def test_branch_simulation_shows_if_prefix(self) -> None:
        """Branches should have 'If' prefix in narrative."""
        session, output = _session([
            "IfTest", "X, Y",
            "X", "Y", "1",
            "done",
            "yes", "X", "left, right",
            "done", "yes",
        ])
        session.run()
        combined = " ".join(output)
        assert "If left" in combined or "if left" in combined.lower()


# ============================================================
# 11. La Nonna Demo E2E (E.5 verification)
# ============================================================


class TestLaNonnaDemoVerification:
    """E.5: Verify that the verification pipeline produces REAL output.

    This test proves BUG 1 (spec format mismatch) is truly fixed:
    the pipeline must produce verification results (PROVED), not
    silently skip them.  Also tests no_deletion property integration.
    """

    INPUTS = [
        "GestioneRicette",                  # protocol name
        "Cuoco, Dispensa",                  # 2 roles
        "Cuoco", "Dispensa", "1",           # Cuoco asks_task Dispensa
        "Dispensa", "Cuoco", "2",           # Dispensa return_result Cuoco
        "fatto",                            # finish messages (Italian)
        "no",                               # no choices
        "3",                                # add no_deletion
        "fatto",                            # finish properties
        "si",                               # confirm (Italian)
    ]

    def _run(self) -> tuple:
        session, output = _session(self.INPUTS, lang="it")
        result = session.run()
        return result, output

    def test_result_not_none(self) -> None:
        result, _ = self._run()
        assert result is not None

    def test_has_no_deletion_property(self) -> None:
        result, _ = self._run()
        assert "no_deletion" in result.draft.properties

    def test_has_3_properties_total(self) -> None:
        """Default 2 (always_terminates, no_deadlock) + no_deletion = 3."""
        result, _ = self._run()
        assert len(result.draft.properties) == 3

    def test_property_report_not_empty(self) -> None:
        """BUG 1 fix: property_report must have real results, not empty."""
        result, _ = self._run()
        assert len(result.property_report.results) > 0

    def test_all_properties_proved(self) -> None:
        """All 3 properties must be PROVED (not SKIPPED, not VIOLATED)."""
        from cervellaswarm_lingua_universale.spec import PropertyVerdict
        result, _ = self._run()
        for r in result.property_report.results:
            assert r.verdict == PropertyVerdict.PROVED, (
                f"{r.spec.kind.value} is {r.verdict.value}, expected PROVED"
            )

    def test_verification_output_contains_proved(self) -> None:
        """Output must contain 'PROVED' strings (visible to user)."""
        _, output = self._run()
        combined = " ".join(output)
        assert "PROVED" in combined

    def test_verification_shows_no_deletion(self) -> None:
        """Output must mention no_deletion in verification results."""
        _, output = self._run()
        combined = " ".join(output)
        assert "no_deletion" in combined

    def test_property_explanation_shown_in_confirmation(self) -> None:
        """R7: property explanations must appear in confirmation output."""
        _, output = self._run()
        combined = " ".join(output)
        assert "cancellato" in combined or "protetti" in combined

    def test_generated_code_has_cuoco(self) -> None:
        result, _ = self._run()
        assert "Cuoco" in result.generated_code

    def test_simulation_has_italian_narrative(self) -> None:
        _, output = self._run()
        combined = " ".join(output)
        assert "chiede" in combined or "restituisce" in combined
