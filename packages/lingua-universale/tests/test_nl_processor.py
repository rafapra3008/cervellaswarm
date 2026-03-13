# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _nl_processor.py (E.3) -- NL -> IntentDraft via Claude API.

Strategy: mock the anthropic client. Test the pure parsing functions
directly, and the full processor with injected mocks.

Covers:
    - TOOL_SCHEMA structure and completeness
    - _build_draft(): pure function, valid + invalid inputs
    - _extract_tool_input(): dict-based + attr-based responses
    - ClaudeNLProcessor: mocked API, NL mode session integration
    - Error handling: missing fields, invalid roles, bad action keys
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_lingua_universale._nl_processor import (
    SYSTEM_PROMPT,
    TOOL_SCHEMA,
    ClaudeNLProcessor,
    NLProcessorError,
    _build_draft,
    _extract_text_response,
    _extract_tool_input,
)
from cervellaswarm_lingua_universale._intent_bridge import (
    ChatPhase,
    ChatSession,
    DraftChoice,
    DraftMessage,
    IntentDraft,
    NLClarificationNeeded,
    Turn,
    _ACTION_VERBS,
)


# ============================================================
# 1. TOOL_SCHEMA structure
# ============================================================


class TestToolSchema:
    """TOOL_SCHEMA is well-formed for Claude API."""

    def test_has_name(self) -> None:
        assert TOOL_SCHEMA["name"] == "create_protocol"

    def test_has_description(self) -> None:
        assert isinstance(TOOL_SCHEMA["description"], str)

    def test_has_input_schema(self) -> None:
        assert "input_schema" in TOOL_SCHEMA

    def test_required_fields(self) -> None:
        required = TOOL_SCHEMA["input_schema"]["required"]
        assert "protocol_name" in required
        assert "roles" in required
        assert "messages" in required

    def test_action_key_enum_matches_action_verbs(self) -> None:
        """The enum in the schema must match _ACTION_VERBS keys."""
        props = TOOL_SCHEMA["input_schema"]["properties"]
        msg_props = props["messages"]["items"]["properties"]
        schema_keys = set(msg_props["action_key"]["enum"])
        code_keys = set(_ACTION_VERBS.keys())
        assert schema_keys == code_keys

    def test_properties_enum_has_4_entries(self) -> None:
        props = TOOL_SCHEMA["input_schema"]["properties"]
        prop_enum = props["properties"]["items"]["enum"]
        assert len(prop_enum) == 4


# ============================================================
# 2. SYSTEM_PROMPT quality
# ============================================================


class TestSystemPrompt:
    """SYSTEM_PROMPT contains essential guidance."""

    def test_mentions_protocol(self) -> None:
        assert "protocol" in SYSTEM_PROMPT.lower()

    def test_mentions_create_protocol_tool(self) -> None:
        assert "create_protocol" in SYSTEM_PROMPT

    def test_has_examples(self) -> None:
        assert "RecipeExchange" in SYSTEM_PROMPT
        assert "TaskDelegation" in SYSTEM_PROMPT
        assert "DataPipeline" in SYSTEM_PROMPT

    def test_mentions_all_action_keys(self) -> None:
        for key in _ACTION_VERBS:
            assert key in SYSTEM_PROMPT, f"Missing action key: {key}"


# ============================================================
# 3. _build_draft() -- pure function
# ============================================================


class TestBuildDraft:
    """_build_draft() converts tool_use input dict to IntentDraft."""

    def test_simple_2role_protocol(self) -> None:
        data = {
            "protocol_name": "Ping",
            "roles": ["Alice", "Bob"],
            "messages": [
                {"sender": "Alice", "receiver": "Bob", "action_key": "ask_task"},
                {"sender": "Bob", "receiver": "Alice", "action_key": "return_result"},
            ],
        }
        draft = _build_draft(data)
        assert draft.protocol_name == "Ping"
        assert draft.roles == ("Alice", "Bob")
        assert len(draft.messages) == 2

    def test_3role_with_choices(self) -> None:
        data = {
            "protocol_name": "DataPipeline",
            "roles": ["Collector", "Processor", "Analyzer"],
            "messages": [
                {"sender": "Collector", "receiver": "Processor", "action_key": "send_message"},
            ],
            "choices": [
                {"decider": "Analyzer", "branch_names": ["valid", "invalid"]},
            ],
        }
        draft = _build_draft(data)
        assert len(draft.choices) == 1
        assert draft.choices[0].decider == "Analyzer"
        assert len(draft.choices[0].branches) == 2

    def test_custom_properties(self) -> None:
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
            "properties": ["always_terminates", "no_deadlock", "all_roles_participate"],
        }
        draft = _build_draft(data)
        assert len(draft.properties) == 3

    def test_default_properties_when_missing(self) -> None:
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
        }
        draft = _build_draft(data)
        assert "always_terminates" in draft.properties
        assert "no_deadlock" in draft.properties

    def test_name_with_spaces_normalized(self) -> None:
        data = {
            "protocol_name": "My Protocol",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
        }
        draft = _build_draft(data)
        assert draft.protocol_name == "My_Protocol"

    def test_roles_are_frozen_tuple(self) -> None:
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
        }
        draft = _build_draft(data)
        assert isinstance(draft.roles, tuple)

    def test_error_missing_protocol_name(self) -> None:
        with pytest.raises(NLProcessorError, match="protocol_name"):
            _build_draft({"roles": ["A", "B"], "messages": []})

    def test_error_empty_protocol_name(self) -> None:
        with pytest.raises(NLProcessorError, match="protocol_name"):
            _build_draft({"protocol_name": "", "roles": ["A", "B"], "messages": []})

    def test_error_less_than_2_roles(self) -> None:
        with pytest.raises(NLProcessorError, match="2 roles"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A"],
                "messages": [],
            })

    def test_error_no_messages(self) -> None:
        with pytest.raises(NLProcessorError, match="1 message"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [],
            })

    def test_error_unknown_sender(self) -> None:
        with pytest.raises(NLProcessorError, match="Unknown sender"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "C", "receiver": "B", "action_key": "ask_task"}],
            })

    def test_error_unknown_receiver(self) -> None:
        with pytest.raises(NLProcessorError, match="Unknown receiver"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "A", "receiver": "C", "action_key": "ask_task"}],
            })

    def test_error_same_sender_receiver(self) -> None:
        with pytest.raises(NLProcessorError, match="must differ"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "A", "receiver": "A", "action_key": "ask_task"}],
            })

    def test_error_invalid_action_key(self) -> None:
        with pytest.raises(NLProcessorError, match="Invalid action_key"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "A", "receiver": "B", "action_key": "invalid"}],
            })

    def test_error_choice_less_than_2_branches(self) -> None:
        with pytest.raises(NLProcessorError, match="2 branches"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
                "choices": [{"decider": "A", "branch_names": ["only_one"]}],
            })

    def test_error_choice_unknown_decider(self) -> None:
        with pytest.raises(NLProcessorError, match="Unknown decider"):
            _build_draft({
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
                "choices": [{"decider": "C", "branch_names": ["x", "y"]}],
            })

    def test_all_10_action_keys_accepted(self) -> None:
        """Every valid action_key must be accepted by _build_draft."""
        for key in _ACTION_VERBS:
            data = {
                "protocol_name": "P",
                "roles": ["A", "B"],
                "messages": [{"sender": "A", "receiver": "B", "action_key": key}],
            }
            draft = _build_draft(data)
            assert draft.messages[0].action_key == key

    def test_invalid_properties_filtered(self) -> None:
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
            "properties": ["always_terminates", "invalid_prop", "no_deadlock"],
        }
        draft = _build_draft(data)
        assert "always_terminates" in draft.properties
        assert "no_deadlock" in draft.properties
        assert "invalid_prop" not in draft.properties


# ============================================================
# 4. _extract_tool_input()
# ============================================================


class TestExtractToolInput:
    """_extract_tool_input() handles dict and object responses."""

    def test_dict_response_with_tool_use(self) -> None:
        response = {
            "content": [
                {"type": "tool_use", "input": {"protocol_name": "Test"}},
            ]
        }
        result = _extract_tool_input(response)
        assert result["protocol_name"] == "Test"

    def test_dict_response_without_tool_use_raises(self) -> None:
        response = {"content": [{"type": "text", "text": "hello"}]}
        with pytest.raises(NLProcessorError, match="No tool_use"):
            _extract_tool_input(response)

    def test_dict_response_empty_content_raises(self) -> None:
        response = {"content": []}
        with pytest.raises(NLProcessorError, match="No tool_use"):
            _extract_tool_input(response)

    def test_object_response_with_tool_use(self) -> None:
        @dataclass
        class Block:
            type: str
            input: dict

        @dataclass
        class Response:
            content: list

        block = Block(type="tool_use", input={"protocol_name": "ObjTest"})
        response = Response(content=[block])
        result = _extract_tool_input(response)
        assert result["protocol_name"] == "ObjTest"

    def test_object_response_without_content_raises(self) -> None:
        with pytest.raises(NLProcessorError, match="no content"):
            _extract_tool_input(object())

    def test_multiple_blocks_finds_tool_use(self) -> None:
        response = {
            "content": [
                {"type": "text", "text": "thinking..."},
                {"type": "tool_use", "input": {"protocol_name": "Found"}},
            ]
        }
        result = _extract_tool_input(response)
        assert result["protocol_name"] == "Found"


# ============================================================
# 5. ClaudeNLProcessor with mocked API
# ============================================================


class TestClaudeNLProcessorMocked:
    """ClaudeNLProcessor with mocked anthropic client."""

    def _mock_response(self, tool_input: dict) -> dict:
        """Create a mock Claude API response with tool_use."""
        return {
            "content": [
                {"type": "tool_use", "name": "create_protocol", "input": tool_input},
            ]
        }

    @patch("cervellaswarm_lingua_universale._nl_processor.ClaudeNLProcessor.__init__", return_value=None)
    def test_process_returns_intent_draft(self, mock_init: MagicMock) -> None:
        processor = ClaudeNLProcessor.__new__(ClaudeNLProcessor)
        processor._model = "test-model"
        processor._client = MagicMock()
        processor._client.messages.create.return_value = self._mock_response({
            "protocol_name": "RecipeExchange",
            "roles": ["Cook", "Pantry"],
            "messages": [
                {"sender": "Cook", "receiver": "Pantry", "action_key": "ask_task"},
                {"sender": "Pantry", "receiver": "Cook", "action_key": "return_result"},
            ],
        })

        # Mock _extract_tool_input to handle dict response
        draft = processor.process("A recipe system", "en", [])
        assert isinstance(draft, IntentDraft)
        assert draft.protocol_name == "RecipeExchange"

    @patch("cervellaswarm_lingua_universale._nl_processor.ClaudeNLProcessor.__init__", return_value=None)
    def test_process_api_error_raises_nl_error(self, mock_init: MagicMock) -> None:
        processor = ClaudeNLProcessor.__new__(ClaudeNLProcessor)
        processor._model = "test-model"
        processor._client = MagicMock()
        processor._client.messages.create.side_effect = RuntimeError("API down")

        with pytest.raises(NLProcessorError, match="Claude API error"):
            processor.process("test", "en", [])

    @patch("cervellaswarm_lingua_universale._nl_processor.ClaudeNLProcessor.__init__", return_value=None)
    def test_build_messages_includes_lang_hint(self, mock_init: MagicMock) -> None:
        processor = ClaudeNLProcessor.__new__(ClaudeNLProcessor)
        messages = processor._build_messages("ciao", "it", [])
        assert len(messages) == 1
        assert "Italian" in messages[0]["content"]

    @patch("cervellaswarm_lingua_universale._nl_processor.ClaudeNLProcessor.__init__", return_value=None)
    def test_build_messages_includes_context(self, mock_init: MagicMock) -> None:
        processor = ClaudeNLProcessor.__new__(ClaudeNLProcessor)
        context = [Turn(speaker="user", text="hello", phase=ChatPhase.NL_INPUT)]
        messages = processor._build_messages("describe protocol", "en", context)
        assert len(messages) == 2  # context + current input

    @patch("cervellaswarm_lingua_universale._nl_processor.ClaudeNLProcessor.__init__", return_value=None)
    def test_build_messages_portuguese_hint(self, mock_init: MagicMock) -> None:
        processor = ClaudeNLProcessor.__new__(ClaudeNLProcessor)
        messages = processor._build_messages("ola", "pt", [])
        assert "Portuguese" in messages[0]["content"]


# ============================================================
# 6. NL mode session integration
# ============================================================


def _nl_session(
    inputs: list[str], *, lang: str = "en", nl_draft: IntentDraft | None = None,
) -> tuple[ChatSession, list[str]]:
    """Create a ChatSession in NL mode with a mock NLProcessor."""
    it = iter(inputs)
    output: list[str] = []

    def _input_fn(prompt: str) -> str:
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    def _output_fn(*args: object, **kwargs: object) -> None:
        output.append(" ".join(str(a) for a in args))

    # Mock NLProcessor that returns the given draft
    mock_processor = MagicMock()
    if nl_draft is not None:
        mock_processor.process.return_value = nl_draft
    else:
        mock_processor.process.return_value = IntentDraft(
            protocol_name="MockProto",
            roles=("Alice", "Bob"),
            messages=(DraftMessage("Alice", "Bob", "ask_task"),),
        )

    session = ChatSession(
        lang=lang,
        input_fn=_input_fn,
        output_fn=_output_fn,
        nl_processor=mock_processor,
    )
    return session, output


class TestNLModeSession:
    """ChatSession with NLProcessor (NL mode)."""

    def test_nl_mode_starts_at_nl_input_phase(self) -> None:
        session, _ = _nl_session(["exit"])
        assert session.phase == ChatPhase.WELCOME
        # After run starts, should be NL_INPUT
        session.run()
        # After exit, phase stays at NL_INPUT
        assert session.phase == ChatPhase.NL_INPUT

    def test_nl_mode_shows_nl_ask_prompt(self) -> None:
        session, output = _nl_session(["exit"])
        session.run()
        combined = " ".join(output)
        assert "Describe" in combined or "Descrivi" in combined or "Descreva" in combined

    def test_nl_input_calls_processor(self) -> None:
        session, _ = _nl_session(["a recipe system", "yes"])
        result = session.run()
        assert result is not None
        assert result.draft.protocol_name == "MockProto"

    def test_nl_full_flow_produces_result(self) -> None:
        session, output = _nl_session(["describe something", "yes"])
        result = session.run()
        assert result is not None
        assert result.generated_code.strip() != ""

    def test_nl_confirm_no_returns_to_nl_input(self) -> None:
        """Saying 'no' at confirm goes back to NL_INPUT (not ROLES)."""
        session, output = _nl_session([
            "first attempt",  # NL input
            "no",             # reject
            "second attempt", # NL input again
            "yes",            # confirm
        ])
        result = session.run()
        assert result is not None

    def test_nl_processor_error_shows_error_message(self) -> None:
        it = iter(["bad input", "exit"])
        output: list[str] = []

        mock_processor = MagicMock()
        mock_processor.process.side_effect = RuntimeError("API error")

        session = ChatSession(
            lang="en",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: output.append(" ".join(str(x) for x in a)),
            nl_processor=mock_processor,
        )
        session.run()
        combined = " ".join(output)
        assert "try again" in combined.lower() or "Could not" in combined

    def test_nl_mode_italian(self) -> None:
        draft = IntentDraft(
            protocol_name="ProtoIT",
            roles=("Alice", "Bob"),
            messages=(DraftMessage("Alice", "Bob", "ask_task"),),
        )
        session, output = _nl_session(["un sistema di ricette", "si"], lang="it", nl_draft=draft)
        result = session.run()
        assert result is not None
        assert result.draft.protocol_name == "ProtoIT"

    def test_nl_mode_portuguese(self) -> None:
        draft = IntentDraft(
            protocol_name="ProtoPT",
            roles=("A", "B"),
            messages=(DraftMessage("A", "B", "send_message"),),
        )
        session, output = _nl_session(["um pipeline", "sim"], lang="pt", nl_draft=draft)
        result = session.run()
        assert result is not None

    def test_nl_mode_result_has_property_report(self) -> None:
        session, _ = _nl_session(["test", "yes"])
        result = session.run()
        assert result is not None
        assert result.property_report is not None

    def test_nl_mode_result_has_intent_source(self) -> None:
        session, _ = _nl_session(["test", "yes"])
        result = session.run()
        assert result is not None
        assert result.intent_source.startswith("protocol MockProto:")

    def test_guided_mode_unaffected(self) -> None:
        """Without nl_processor, session works in guided mode as before."""
        it = iter(["TestProto", "A, B", "A", "B", "1", "done", "no", "done", "yes"])
        session = ChatSession(
            lang="en",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: None,
            nl_processor=None,
        )
        result = session.run()
        assert result is not None
        assert result.draft.protocol_name == "TestProto"

    def test_nl_error_shows_detail(self) -> None:
        """F5: NL error includes exception detail for debugging."""
        mock_proc = MagicMock()
        mock_proc.process.side_effect = RuntimeError("rate limit exceeded")
        output: list[str] = []
        it = iter(["test input", "quit"])
        session = ChatSession(
            lang="en",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: output.append(" ".join(str(x) for x in a)),
            nl_processor=mock_proc,
        )
        session.run()
        combined = " ".join(output)
        assert "rate limit exceeded" in combined


# ============================================================
# 7. Build draft edge cases (Guardiana F7)
# ============================================================


class TestBuildDraftEdgeCases:
    """Additional edge cases found by Guardiana audit."""

    def test_empty_properties_list_gets_defaults(self) -> None:
        """F7: properties: [] should get default properties."""
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
            "properties": [],
        }
        draft = _build_draft(data)
        assert draft.properties == ("always_terminates", "no_deadlock")

    def test_properties_none_gets_defaults(self) -> None:
        """properties: null should get default properties."""
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
            "properties": None,
        }
        draft = _build_draft(data)
        assert draft.properties == ("always_terminates", "no_deadlock")

    def test_properties_with_invalid_filtered_to_empty_gets_defaults(self) -> None:
        """All invalid properties should fall back to defaults."""
        data = {
            "protocol_name": "P",
            "roles": ["A", "B"],
            "messages": [{"sender": "A", "receiver": "B", "action_key": "ask_task"}],
            "properties": ["fake_property", "nonexistent"],
        }
        draft = _build_draft(data)
        assert draft.properties == ("always_terminates", "no_deadlock")


# ============================================================
# 8. CLI argument parsing (Guardiana F4)
# ============================================================


class TestCLIModeParsing:
    """Test CLI --mode nl argument path."""

    def test_cli_parser_accepts_mode_nl(self) -> None:
        """CLI parser accepts --mode nl."""
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--mode", "nl"])
        assert args.mode == "nl"
        assert args.command == "chat"

    def test_cli_parser_default_mode_guided(self) -> None:
        """CLI parser defaults to guided mode."""
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat"])
        assert args.mode == "guided"

    def test_cli_parser_mode_with_lang(self) -> None:
        """CLI parser accepts --mode nl --lang it together."""
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        args = parser.parse_args(["chat", "--mode", "nl", "--lang", "it"])
        assert args.mode == "nl"
        assert args.lang == "it"


# ============================================================
# 9. Disambiguation / Clarification (E.3 step 2)
# ============================================================


class TestExtractTextResponse:
    """_extract_text_response detects clarification questions."""

    def test_text_only_response_returns_text(self) -> None:
        response = {
            "content": [
                {"type": "text", "text": "How many roles do you need?"},
            ]
        }
        assert _extract_text_response(response) == "How many roles do you need?"

    def test_tool_use_response_returns_none(self) -> None:
        response = {
            "content": [
                {"type": "tool_use", "name": "create_protocol", "input": {}},
            ]
        }
        assert _extract_text_response(response) is None

    def test_mixed_with_tool_returns_none(self) -> None:
        """If tool_use is present, it's not a clarification."""
        response = {
            "content": [
                {"type": "text", "text": "Here's your protocol:"},
                {"type": "tool_use", "name": "create_protocol", "input": {}},
            ]
        }
        assert _extract_text_response(response) is None

    def test_empty_content_returns_none(self) -> None:
        response = {"content": []}
        assert _extract_text_response(response) is None

    def test_multiple_text_blocks_joined(self) -> None:
        response = {
            "content": [
                {"type": "text", "text": "I need more details."},
                {"type": "text", "text": "What roles are involved?"},
            ]
        }
        result = _extract_text_response(response)
        assert result == "I need more details. What roles are involved?"

    def test_attr_based_response_text_only(self) -> None:
        """Handles real Anthropic response objects (attr-based)."""
        @dataclass
        class TextBlock:
            type: str = "text"
            text: str = "Can you describe the flow?"

        @dataclass
        class Response:
            content: list = None  # type: ignore[assignment]
            def __post_init__(self):
                if self.content is None:
                    self.content = [TextBlock()]

        assert _extract_text_response(Response()) == "Can you describe the flow?"

    def test_attr_based_response_with_tool_returns_none(self) -> None:
        @dataclass
        class ToolBlock:
            type: str = "tool_use"
            input: dict = None  # type: ignore[assignment]

        @dataclass
        class Response:
            content: list = None  # type: ignore[assignment]
            def __post_init__(self):
                if self.content is None:
                    self.content = [ToolBlock()]

        assert _extract_text_response(Response()) is None


class TestDisambiguationSession:
    """NL mode disambiguation: LLM asks clarifying questions."""

    def test_clarification_shows_question_and_stays_in_nl_input(self) -> None:
        """When LLM asks for clarification, session stays in NL_INPUT."""
        mock_proc = MagicMock()
        # First call: clarification needed; second: returns draft
        draft = IntentDraft(
            protocol_name="TestP",
            roles=("A", "B"),
            messages=(DraftMessage("A", "B", "ask_task"),),
        )
        mock_proc.process.side_effect = [
            NLClarificationNeeded("How many participants?"),
            draft,
        ]
        output: list[str] = []
        it = iter(["vague description", "two participants: A and B", "yes"])
        session = ChatSession(
            lang="en",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: output.append(" ".join(str(x) for x in a)),
            nl_processor=mock_proc,
        )
        result = session.run()
        combined = " ".join(output)
        assert "How many participants?" in combined
        assert result is not None
        assert result.draft.protocol_name == "TestP"
        # process was called twice (clarification + success)
        assert mock_proc.process.call_count == 2

    def test_clarification_preserves_context(self) -> None:
        """Conversation context accumulates across clarification turns."""
        mock_proc = MagicMock()
        draft = IntentDraft(
            protocol_name="P",
            roles=("X", "Y"),
            messages=(DraftMessage("X", "Y", "send_message"),),
        )
        mock_proc.process.side_effect = [
            NLClarificationNeeded("What roles?"),
            draft,
        ]
        output: list[str] = []
        it = iter(["something", "X and Y", "yes"])
        session = ChatSession(
            lang="en",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: output.append(" ".join(str(x) for x in a)),
            nl_processor=mock_proc,
        )
        session.run()
        # First call: no previous context (only current text via _build_messages)
        first_call = mock_proc.process.call_args_list[0]
        first_context = first_call[0][2]
        assert len(first_context) == 0  # past turns empty on first call
        # Second call: previous turns (user + system clarification)
        second_call = mock_proc.process.call_args_list[1]
        context_arg = second_call[0][2]
        assert len(context_arg) == 2  # user turn + system clarification
        # Verify no back-to-back same roles
        roles = [("user" if t.speaker == "user" else "assistant") for t in context_arg]
        for i in range(1, len(roles)):
            assert roles[i] != roles[i - 1], "Back-to-back same roles in context"

    def test_multiple_clarifications(self) -> None:
        """Multiple clarification rounds before success."""
        mock_proc = MagicMock()
        draft = IntentDraft(
            protocol_name="P",
            roles=("A", "B"),
            messages=(DraftMessage("A", "B", "ask_task"),),
        )
        mock_proc.process.side_effect = [
            NLClarificationNeeded("What kind of system?"),
            NLClarificationNeeded("How many roles?"),
            draft,
        ]
        it = iter(["idea", "recipe system", "two roles", "yes"])
        session = ChatSession(
            lang="en",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: None,
            nl_processor=mock_proc,
        )
        result = session.run()
        assert result is not None
        assert mock_proc.process.call_count == 3

    def test_clarification_in_italian(self) -> None:
        """Clarification works in Italian."""
        mock_proc = MagicMock()
        draft = IntentDraft(
            protocol_name="P",
            roles=("A", "B"),
            messages=(DraftMessage("A", "B", "ask_task"),),
        )
        mock_proc.process.side_effect = [
            NLClarificationNeeded("Quanti partecipanti ci sono?"),
            draft,
        ]
        output: list[str] = []
        it = iter(["un sistema", "due: A e B", "si"])
        session = ChatSession(
            lang="it",
            input_fn=lambda p: next(it),
            output_fn=lambda *a, **kw: output.append(" ".join(str(x) for x in a)),
            nl_processor=mock_proc,
        )
        result = session.run()
        combined = " ".join(output)
        assert "Quanti partecipanti" in combined
        assert result is not None
