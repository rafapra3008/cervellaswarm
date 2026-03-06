# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Core tests for _intent_bridge.py (E.2) - Part 1: data model, render, i18n.

Covers:
    - Data model: frozen dataclasses (DraftMessage, DraftChoice, IntentDraft,
      Turn, ChatResult, ChatPhase)
    - render_intent_source(): deterministic B.4 output and round-trips
    - i18n: _t(), _STRINGS, _DONE_WORDS, _YES_WORDS, _NO_WORDS, _ACTION_MENU

Session + edge-case tests: test_intent_bridge_session.py
"""

from __future__ import annotations

import dataclasses

import pytest

from cervellaswarm_lingua_universale._intent_bridge import (
    _ACTION_MENU,
    _ACTION_VERBS,
    _DONE_WORDS,
    _NO_WORDS,
    _STRINGS,
    _YES_WORDS,
    _t,
    ChatPhase,
    ChatResult,
    DraftChoice,
    DraftMessage,
    IntentDraft,
    Turn,
    render_intent_source,
)
from cervellaswarm_lingua_universale.intent import parse_intent


# ============================================================
# 1. Data Model (frozen dataclasses)
# ============================================================


class TestDraftMessage:
    """DraftMessage is a frozen dataclass."""

    def test_creation(self) -> None:
        msg = DraftMessage(sender="Alice", receiver="Bob", action_key="ask_task")
        assert msg.sender == "Alice"
        assert msg.receiver == "Bob"
        assert msg.action_key == "ask_task"

    def test_frozen(self) -> None:
        msg = DraftMessage(sender="Alice", receiver="Bob", action_key="ask_task")
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            msg.sender = "Charlie"  # type: ignore[misc]

    def test_equality(self) -> None:
        a = DraftMessage("Alice", "Bob", "ask_task")
        b = DraftMessage("Alice", "Bob", "ask_task")
        assert a == b

    def test_inequality(self) -> None:
        a = DraftMessage("Alice", "Bob", "ask_task")
        b = DraftMessage("Alice", "Bob", "return_result")
        assert a != b


class TestDraftChoice:
    """DraftChoice is a frozen dataclass."""

    def test_creation(self) -> None:
        msg = DraftMessage("Alice", "Bob", "send_message")
        choice = DraftChoice(
            decider="Alice",
            branches=(("approve", (msg,)),),
        )
        assert choice.decider == "Alice"
        assert len(choice.branches) == 1

    def test_frozen(self) -> None:
        msg = DraftMessage("Alice", "Bob", "send_message")
        choice = DraftChoice(decider="Alice", branches=(("yes", (msg,)),))
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            choice.decider = "Bob"  # type: ignore[misc]

    def test_branches_is_tuple(self) -> None:
        msg = DraftMessage("Alice", "Bob", "send_message")
        choice = DraftChoice(decider="Alice", branches=(("opt", (msg,)),))
        assert isinstance(choice.branches, tuple)


class TestIntentDraft:
    """IntentDraft is a frozen dataclass with defaults."""

    def test_creation_with_defaults(self) -> None:
        draft = IntentDraft(
            protocol_name="MyProto",
            roles=("Alice", "Bob"),
        )
        assert draft.protocol_name == "MyProto"
        assert draft.roles == ("Alice", "Bob")
        assert draft.messages == ()
        assert draft.choices == ()
        assert "always_terminates" in draft.properties
        assert "no_deadlock" in draft.properties

    def test_frozen(self) -> None:
        draft = IntentDraft(protocol_name="P", roles=("A", "B"))
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            draft.protocol_name = "Q"  # type: ignore[misc]

    def test_custom_messages(self) -> None:
        msg = DraftMessage("Alice", "Bob", "ask_task")
        draft = IntentDraft(
            protocol_name="P",
            roles=("Alice", "Bob"),
            messages=(msg,),
        )
        assert len(draft.messages) == 1
        assert draft.messages[0] == msg

    def test_custom_properties(self) -> None:
        draft = IntentDraft(
            protocol_name="P",
            roles=("A", "B"),
            properties=("always_terminates",),
        )
        assert draft.properties == ("always_terminates",)


class TestTurn:
    """Turn is a frozen dataclass."""

    def test_creation(self) -> None:
        turn = Turn(speaker="user", text="hello", phase=ChatPhase.ROLES)
        assert turn.speaker == "user"
        assert turn.text == "hello"
        assert turn.phase == ChatPhase.ROLES

    def test_frozen(self) -> None:
        turn = Turn("user", "hello", ChatPhase.ROLES)
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            turn.text = "bye"  # type: ignore[misc]


class TestChatResult:
    """ChatResult is a frozen dataclass."""

    def test_creation(self) -> None:
        from cervellaswarm_lingua_universale.spec import PropertyReport
        draft = IntentDraft(protocol_name="P", roles=("A", "B"))
        source = render_intent_source(draft)
        parse_result = parse_intent(source)
        report = PropertyReport(protocol_name="P", results=())
        result = ChatResult(
            draft=draft,
            intent_source=source,
            parse_result=parse_result,
            property_report=report,
            generated_code="# code",
        )
        assert result.draft is draft
        assert result.intent_source == source

    def test_frozen(self) -> None:
        from cervellaswarm_lingua_universale.spec import PropertyReport
        draft = IntentDraft(protocol_name="P", roles=("A", "B"))
        source = render_intent_source(draft)
        parse_result = parse_intent(source)
        report = PropertyReport(protocol_name="P", results=())
        result = ChatResult(
            draft=draft,
            intent_source=source,
            parse_result=parse_result,
            property_report=report,
            generated_code="",
        )
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            result.generated_code = "new"  # type: ignore[misc]


class TestChatPhaseEnum:
    """ChatPhase enum has all expected values."""

    def test_welcome(self) -> None:
        assert ChatPhase.WELCOME is not None

    def test_roles(self) -> None:
        assert ChatPhase.ROLES is not None

    def test_messages(self) -> None:
        assert ChatPhase.MESSAGES is not None

    def test_choices(self) -> None:
        assert ChatPhase.CHOICES is not None

    def test_properties(self) -> None:
        assert ChatPhase.PROPERTIES is not None

    def test_confirm(self) -> None:
        assert ChatPhase.CONFIRM is not None

    def test_verify(self) -> None:
        assert ChatPhase.VERIFY is not None

    def test_codegen(self) -> None:
        assert ChatPhase.CODEGEN is not None

    def test_done(self) -> None:
        assert ChatPhase.DONE is not None

    def test_all_are_distinct(self) -> None:
        phases = list(ChatPhase)
        assert len(phases) == len(set(phases))


# ============================================================
# 2. render_intent_source()
# ============================================================


class TestRenderIntentSource:
    """render_intent_source() produces valid B.4 intent notation."""

    def test_simple_2role_starts_with_protocol(self) -> None:
        draft = IntentDraft(
            protocol_name="Ping",
            roles=("Alice", "Bob"),
            messages=(DraftMessage("Alice", "Bob", "ask_task"),),
        )
        src = render_intent_source(draft)
        assert src.startswith("protocol Ping:")

    def test_simple_2role_contains_roles_line(self) -> None:
        draft = IntentDraft(
            protocol_name="Ping",
            roles=("Alice", "Bob"),
        )
        src = render_intent_source(draft)
        assert "roles: Alice, Bob" in src

    def test_simple_2role_roundtrip_parse(self) -> None:
        draft = IntentDraft(
            protocol_name="SimpleTask",
            roles=("Alice", "Bob"),
            messages=(
                DraftMessage("Alice", "Bob", "ask_task"),
                DraftMessage("Bob", "Alice", "return_result"),
            ),
        )
        src = render_intent_source(draft)
        result = parse_intent(src)
        proto = result.protocol
        assert proto.name == "SimpleTask"
        assert set(proto.roles) == {"Alice", "Bob"}
        assert len(proto.elements) == 2

    def test_3role_protocol_roundtrip(self) -> None:
        draft = IntentDraft(
            protocol_name="Audit",
            roles=("Regina", "Worker", "Guardiana"),
            messages=(
                DraftMessage("Regina", "Worker", "ask_task"),
                DraftMessage("Worker", "Regina", "return_result"),
                DraftMessage("Regina", "Guardiana", "ask_verify"),
                DraftMessage("Guardiana", "Regina", "return_verdict"),
            ),
        )
        src = render_intent_source(draft)
        result = parse_intent(src)
        assert len(result.protocol.elements) == 4

    def test_all_action_verbs_render(self) -> None:
        """All 10 action verbs must produce output containing protocol header."""
        for key in _ACTION_VERBS:
            draft = IntentDraft(
                protocol_name="Test",
                roles=("Alice", "Bob"),
                messages=(DraftMessage("Alice", "Bob", key),),
            )
            src = render_intent_source(draft)
            assert "protocol Test:" in src

    def test_protocol_name_with_underscore(self) -> None:
        draft = IntentDraft(
            protocol_name="My_Protocol_V2",
            roles=("A", "B"),
        )
        src = render_intent_source(draft)
        assert "protocol My_Protocol_V2:" in src

    def test_empty_messages_renders_valid(self) -> None:
        draft = IntentDraft(
            protocol_name="Empty",
            roles=("A", "B"),
            messages=(),
        )
        src = render_intent_source(draft)
        assert "protocol Empty:" in src
        assert "roles: A, B" in src

    def test_with_choice_renders_when_block(self) -> None:
        msg = DraftMessage("Alice", "Bob", "send_message")
        choice = DraftChoice(
            decider="Alice",
            branches=(
                ("approve", (msg,)),
                ("reject", (msg,)),
            ),
        )
        draft = IntentDraft(
            protocol_name="Branch",
            roles=("Alice", "Bob"),
            choices=(choice,),
        )
        src = render_intent_source(draft)
        assert "when Alice decides:" in src
        assert "approve:" in src
        assert "reject:" in src

    def test_roundtrip_roles_match(self) -> None:
        """After render -> parse, roles are identical."""
        draft = IntentDraft(
            protocol_name="RolesCheck",
            roles=("Cook", "Pantry"),
            messages=(DraftMessage("Cook", "Pantry", "ask_task"),),
        )
        src = render_intent_source(draft)
        result = parse_intent(src)
        assert set(result.protocol.roles) == {"Cook", "Pantry"}

    def test_returns_string_ending_newline(self) -> None:
        draft = IntentDraft(protocol_name="P", roles=("A", "B"))
        src = render_intent_source(draft)
        assert isinstance(src, str)
        assert src.endswith("\n")

    def test_4role_roundtrip(self) -> None:
        draft = IntentDraft(
            protocol_name="Complex",
            roles=("A", "B", "C", "D"),
            messages=(
                DraftMessage("A", "B", "ask_task"),
                DraftMessage("B", "C", "ask_verify"),
                DraftMessage("C", "D", "return_result"),
            ),
        )
        src = render_intent_source(draft)
        result = parse_intent(src)
        assert len(result.protocol.elements) == 3

    def test_action_verb_receiver_interpolated(self) -> None:
        draft = IntentDraft(
            protocol_name="P",
            roles=("Sender", "Receiver"),
            messages=(DraftMessage("Sender", "Receiver", "return_result"),),
        )
        src = render_intent_source(draft)
        assert "Receiver" in src

    def test_multiple_choices_render(self) -> None:
        msg = DraftMessage("Alice", "Bob", "send_message")
        choice1 = DraftChoice(
            decider="Alice",
            branches=(("yes", (msg,)), ("no", (msg,))),
        )
        choice2 = DraftChoice(
            decider="Bob",
            branches=(("done", (DraftMessage("Bob", "Alice", "return_result"),)),),
        )
        draft = IntentDraft(
            protocol_name="Multi",
            roles=("Alice", "Bob"),
            choices=(choice1, choice2),
        )
        src = render_intent_source(draft)
        assert "when Alice decides:" in src
        assert "when Bob decides:" in src

    def test_ten_action_verbs_count(self) -> None:
        assert len(_ACTION_VERBS) == 10

    def test_roundtrip_protocol_name_preserved(self) -> None:
        draft = IntentDraft(
            protocol_name="SpecialName",
            roles=("X", "Y"),
            messages=(DraftMessage("X", "Y", "ask_task"),),
        )
        src = render_intent_source(draft)
        result = parse_intent(src)
        assert result.protocol.name == "SpecialName"


# ============================================================
# 3. i18n
# ============================================================


class TestI18n:
    """Tests for _t() translation helper and string dictionaries."""

    def test_t_returns_english_string(self) -> None:
        result = _t("welcome", "en")
        assert "Lingua Universale" in result

    def test_t_returns_italian_string(self) -> None:
        result = _t("welcome", "it")
        assert "Lingua Universale" in result
        assert "aiuto" in result

    def test_t_returns_portuguese_string(self) -> None:
        result = _t("welcome", "pt")
        assert "Lingua Universale" in result
        assert "ajuda" in result

    def test_t_falls_back_to_english_for_unknown_lang(self) -> None:
        result = _t("welcome", "de")  # German not supported
        assert "Lingua Universale" in result

    def test_t_returns_key_for_unknown_key(self) -> None:
        result = _t("nonexistent_key_xyz", "en")
        assert result == "nonexistent_key_xyz"

    def test_t_with_kwargs_interpolated(self) -> None:
        result = _t("roles_confirmed", "en", roles="Alice, Bob")
        assert "Alice, Bob" in result

    def test_t_with_kwargs_italian(self) -> None:
        result = _t("roles_confirmed", "it", roles="Alice, Bob")
        assert "Alice, Bob" in result

    def test_all_strings_keys_have_en(self) -> None:
        for key, entry in _STRINGS.items():
            assert "en" in entry, f"Key '{key}' missing 'en' translation"

    def test_all_strings_keys_have_it(self) -> None:
        for key, entry in _STRINGS.items():
            assert "it" in entry, f"Key '{key}' missing 'it' translation"

    def test_all_strings_keys_have_pt(self) -> None:
        for key, entry in _STRINGS.items():
            assert "pt" in entry, f"Key '{key}' missing 'pt' translation"

    def test_done_words_have_all_3_locales(self) -> None:
        for lang in ("en", "it", "pt"):
            assert lang in _DONE_WORDS, f"_DONE_WORDS missing '{lang}'"

    def test_yes_words_have_all_3_locales(self) -> None:
        for lang in ("en", "it", "pt"):
            assert lang in _YES_WORDS, f"_YES_WORDS missing '{lang}'"

    def test_no_words_have_all_3_locales(self) -> None:
        for lang in ("en", "it", "pt"):
            assert lang in _NO_WORDS, f"_NO_WORDS missing '{lang}'"

    def test_action_menu_has_all_3_locales(self) -> None:
        for lang in ("en", "it", "pt"):
            assert lang in _ACTION_MENU, f"_ACTION_MENU missing '{lang}'"

    def test_action_menu_locales_have_matching_keys(self) -> None:
        """All locale menus must have the same action keys."""
        en_keys = set(_ACTION_MENU["en"].keys())
        it_keys = set(_ACTION_MENU["it"].keys())
        pt_keys = set(_ACTION_MENU["pt"].keys())
        assert en_keys == it_keys, f"it keys differ: {en_keys ^ it_keys}"
        assert en_keys == pt_keys, f"pt keys differ: {en_keys ^ pt_keys}"

    def test_done_words_are_frozensets(self) -> None:
        for lang, words in _DONE_WORDS.items():
            assert isinstance(words, frozenset), f"_DONE_WORDS[{lang}] is not frozenset"
