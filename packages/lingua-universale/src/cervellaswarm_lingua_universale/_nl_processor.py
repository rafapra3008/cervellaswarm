# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""NL Processor: natural language -> IntentDraft via Claude API (E.3).

Implements the ``NLProcessor`` protocol defined in ``_intent_bridge.py``.
Uses Claude's tool_use for structured output extraction -- the two-stage
pattern validated by Req2LTL (ASE 2025): LLM -> structured IR -> deterministic.

The ``anthropic`` package is an **optional** dependency::

    pip install cervellaswarm-lingua-universale[nl]

Design decisions:
    - tool_use for structured output (auto mode allows clarification questions)
    - Few-shot examples embedded in the system prompt
    - Multilingual: detects input language, responds accordingly
    - Fallback: raises ImportError clearly if anthropic not installed
    - ZERO hard dependencies: anthropic is imported lazily
"""

from __future__ import annotations

from typing import Any

from ._intent_bridge import (
    DraftChoice,
    DraftMessage,
    IntentDraft,
    NLClarificationNeeded,
    Turn,
    _ACTION_VERBS,
    _PROPERTY_NAMES,
)


# ============================================================
# Tool schema for Claude API (structured output)
# ============================================================

TOOL_SCHEMA: dict[str, Any] = {
    "name": "create_protocol",
    "description": (
        "Extract a structured communication protocol from the user's "
        "natural language description. Use this tool to return "
        "the protocol structure when you have enough information."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "protocol_name": {
                "type": "string",
                "description": (
                    "A PascalCase or snake_case identifier for the protocol "
                    "(letters, digits, underscores only, starts with letter)."
                ),
            },
            "roles": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "description": "The participant roles (at least 2). Use PascalCase names.",
            },
            "messages": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "sender": {
                            "type": "string",
                            "description": "Role that sends the message.",
                        },
                        "receiver": {
                            "type": "string",
                            "description": "Role that receives the message.",
                        },
                        "action_key": {
                            "type": "string",
                            "enum": list(_ACTION_VERBS.keys()),
                            "description": "Type of action for this message step.",
                        },
                    },
                    "required": ["sender", "receiver", "action_key"],
                },
                "description": "Ordered sequence of message exchanges.",
            },
            "choices": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "decider": {
                            "type": "string",
                            "description": "Role that makes the decision.",
                        },
                        "branch_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2,
                            "description": "Names for each branch option.",
                        },
                    },
                    "required": ["decider", "branch_names"],
                },
                "description": "Branching decisions (optional). Each has a decider and 2+ branches.",
            },
            "properties": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": list(_PROPERTY_NAMES),
                },
                "description": (
                    "Safety properties to verify. Defaults: always_terminates, no_deadlock."
                ),
            },
        },
        "required": ["protocol_name", "roles", "messages"],
    },
}


# ============================================================
# System prompt
# ============================================================

SYSTEM_PROMPT = """\
You are a protocol extraction assistant for Lingua Universale, a programming \
language for verified communication protocols.

Your task: given a natural language description of a communication protocol, \
extract its structure using the create_protocol tool.

## Rules
- protocol_name: PascalCase identifier (e.g., RecipeExchange, TaskDelegation)
- roles: at least 2 participants, PascalCase names
- messages: ordered sequence of interactions between roles
- choices: optional branching decisions
- properties: safety guarantees (default: always_terminates, no_deadlock)
- Detect the user's language and respond with appropriate role names
- When uncertain, prefer simpler protocols (fewer messages/choices)
- If the description is too vague to determine roles or message flow, \
ask ONE short clarifying question instead of using the tool. \
Keep questions concise and in the user's language.

## Action key reference
- ask_task: role asks another to do something
- return_result: role sends back a result
- ask_verify: role asks for verification/audit
- return_verdict: role returns verification result
- ask_plan: role asks for a plan
- propose_plan: role proposes a plan
- tell_decision: role communicates a decision
- ask_research: role asks for research
- return_report: role returns a report
- send_message: generic message between roles

## Examples

Input: "I want a recipe system where the cook asks the pantry for ingredients \
and the pantry sends them back"
-> protocol_name: RecipeExchange, roles: [Cook, Pantry], \
messages: [{Cook, Pantry, ask_task}, {Pantry, Cook, return_result}]

Input: "Un sistema dove il manager delega al lavoratore, il lavoratore fa il \
compito e poi il revisore verifica"
-> protocol_name: TaskDelegation, roles: [Manager, Worker, Reviewer], \
messages: [{Manager, Worker, ask_task}, {Worker, Manager, return_result}, \
{Manager, Reviewer, ask_verify}, {Reviewer, Manager, return_verdict}]

Input: "Um pipeline de dados onde o coletor envia dados ao processador, \
o processador pede ao analisador para verificar, e o analisador decide \
se e valido ou invalido"
-> protocol_name: DataPipeline, roles: [Collector, Processor, Analyzer], \
messages: [{Collector, Processor, send_message}, \
{Processor, Analyzer, ask_verify}], \
choices: [{decider: Analyzer, branch_names: [valid, invalid]}]

When you have enough information, use the create_protocol tool to return the protocol.\
"""


# ============================================================
# ClaudeNLProcessor
# ============================================================


class NLProcessorError(Exception):
    """Raised when NL processing fails."""


class ClaudeNLProcessor:
    """NL -> IntentDraft via Claude API.

    Implements the ``NLProcessor`` protocol from ``_intent_bridge.py``.

    Parameters:
        api_key:  Anthropic API key. If ``None``, reads from
                  ``ANTHROPIC_API_KEY`` environment variable.
        model:    Claude model to use. Default: ``claude-sonnet-4-20250514``.

    Raises:
        ImportError: If ``anthropic`` package is not installed.

    Usage::

        processor = ClaudeNLProcessor()
        draft = processor.process(
            "A system where the cook asks the pantry for ingredients",
            lang="en",
            context=[],
        )
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "The 'anthropic' package is required for NL mode.\n"
                "Install it with: pip install cervellaswarm-lingua-universale[nl]"
            ) from None

        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def process(
        self, text: str, lang: str, context: list[Turn]
    ) -> IntentDraft:
        """Convert natural language to IntentDraft via Claude API.

        Parameters:
            text:     User's natural language description.
            lang:     Interface language (``"en"``, ``"it"``, ``"pt"``).
            context:  Previous conversation turns (for multi-turn).

        Returns:
            An ``IntentDraft`` with the extracted protocol structure.

        Raises:
            NLProcessorError: If extraction fails or response is invalid.
        """
        messages = self._build_messages(text, lang, context)

        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=[TOOL_SCHEMA],
                tool_choice={"type": "auto"},
                messages=messages,
            )
        except Exception as exc:
            raise NLProcessorError(f"Claude API error: {exc}") from exc

        return self._parse_response(response)

    # --------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------

    def _build_messages(
        self,
        text: str,
        lang: str,
        context: list[Turn],
    ) -> list[dict[str, str]]:
        """Build the messages list for the Claude API call."""
        messages: list[dict[str, str]] = []

        # Add context from previous turns (if any)
        for turn in context:
            role = "user" if turn.speaker == "user" else "assistant"
            messages.append({"role": role, "content": turn.text})

        # Add the current user input
        lang_hint = {"en": "English", "it": "Italian", "pt": "Portuguese"}.get(
            lang, "English"
        )
        user_content = (
            f"[Language: {lang_hint}]\n\n"
            f"Describe the protocol you want to create:\n{text}"
        )
        messages.append({"role": "user", "content": user_content})

        return messages

    def _parse_response(self, response: object) -> IntentDraft:
        """Parse Claude's tool_use response into an IntentDraft.

        Parameters:
            response: The raw response from ``client.messages.create()``.

        Returns:
            An ``IntentDraft`` built from the tool call arguments.

        Raises:
            NLClarificationNeeded: If Claude responds with a question
                instead of using the tool.
            NLProcessorError: If the response is invalid.
        """
        # Check for text-only response (clarification question)
        question = _extract_text_response(response)
        if question is not None:
            raise NLClarificationNeeded(question)

        # Extract tool use block from response
        tool_input = _extract_tool_input(response)

        # Validate and build IntentDraft
        return _build_draft(tool_input)


# ============================================================
# Response parsing (pure functions for testability)
# ============================================================


def _extract_text_response(response: object) -> str | None:
    """Extract a text-only response (clarification question) if present.

    Returns ``None`` if the response contains a tool_use block,
    meaning it has structured output rather than a question.
    """
    # Handle dict responses (for testing)
    if isinstance(response, dict):
        content = response.get("content", [])
        has_tool = any(
            isinstance(b, dict) and b.get("type") == "tool_use"
            for b in content
        )
        if has_tool:
            return None
        texts = [
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        ]
        return " ".join(texts).strip() or None

    # Handle real Anthropic response objects
    content = getattr(response, "content", None)
    if content is None:
        return None

    has_tool = any(getattr(b, "type", None) == "tool_use" for b in content)
    if has_tool:
        return None

    texts = [
        getattr(b, "text", "")
        for b in content
        if getattr(b, "type", None) == "text"
    ]
    return " ".join(texts).strip() or None


def _extract_tool_input(response: object) -> dict[str, Any]:
    """Extract the tool input dict from a Claude API response.

    Supports both the real Anthropic response object and plain dicts
    (for testing).
    """
    # Handle dict responses (for testing)
    if isinstance(response, dict):
        content = response.get("content", [])
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                return block.get("input", {})
        raise NLProcessorError("No tool_use block in response")

    # Handle real Anthropic response objects
    content = getattr(response, "content", None)
    if content is None:
        raise NLProcessorError("Response has no content")

    for block in content:
        if getattr(block, "type", None) == "tool_use":
            return getattr(block, "input", {})

    raise NLProcessorError("No tool_use block in response")


def _validate_roles(data: dict[str, Any]) -> tuple[str, ...]:
    """Validate and extract roles from tool input."""
    protocol_name = data.get("protocol_name")
    if not protocol_name or not isinstance(protocol_name, str):
        raise NLProcessorError("Missing or invalid protocol_name")

    roles = data.get("roles")
    if not roles or not isinstance(roles, list) or len(roles) < 2:
        raise NLProcessorError("Need at least 2 roles")

    for role in roles:
        if not isinstance(role, str) or not role.strip():
            raise NLProcessorError(f"Invalid role: {role!r}")

    return tuple(r.strip() for r in roles)


def _validate_messages(raw_messages: list, roles: tuple[str, ...]) -> tuple[DraftMessage, ...]:
    """Validate and parse messages from tool input."""
    if not raw_messages:
        raise NLProcessorError("Need at least 1 message")

    valid_keys = set(_ACTION_VERBS.keys())
    messages: list[DraftMessage] = []
    for msg_data in raw_messages:
        sender = msg_data.get("sender", "")
        receiver = msg_data.get("receiver", "")
        action_key = msg_data.get("action_key", "")

        if sender not in roles:
            raise NLProcessorError(f"Unknown sender '{sender}'. Available: {roles}")
        if receiver not in roles:
            raise NLProcessorError(f"Unknown receiver '{receiver}'. Available: {roles}")
        if sender == receiver:
            raise NLProcessorError(f"Sender and receiver must differ: '{sender}'")
        if action_key not in valid_keys:
            raise NLProcessorError(f"Invalid action_key '{action_key}'. Valid: {sorted(valid_keys)}")

        messages.append(DraftMessage(sender=sender, receiver=receiver, action_key=action_key))
    return tuple(messages)


def _validate_choices(raw_choices: list, roles: tuple[str, ...]) -> tuple[DraftChoice, ...]:
    """Validate and parse choices from tool input."""
    choices: list[DraftChoice] = []
    for choice_data in raw_choices:
        decider = choice_data.get("decider", "")
        branch_names = choice_data.get("branch_names", [])

        if decider not in roles:
            raise NLProcessorError(f"Unknown decider '{decider}'. Available: {roles}")
        if len(branch_names) < 2:
            raise NLProcessorError("Choices need at least 2 branches")

        other = [r for r in roles if r != decider]
        receiver = other[0] if other else roles[0]
        branches: list[tuple[str, tuple[DraftMessage, ...]]] = []
        for name in branch_names:
            branch_msg = DraftMessage(sender=decider, receiver=receiver, action_key="send_message")
            branches.append((name.strip(), (branch_msg,)))

        choices.append(DraftChoice(decider=decider, branches=tuple(branches)))
    return tuple(choices)


def _validate_properties(data: dict[str, Any]) -> tuple[str, ...]:
    """Validate and extract properties with defaults."""
    raw = data.get("properties")
    default = ("always_terminates", "no_deadlock")
    if raw and isinstance(raw, list):
        valid = set(_PROPERTY_NAMES)
        props = tuple(p for p in raw if p in valid)
        return props if props else default
    return default


def _build_draft(data: dict[str, Any]) -> IntentDraft:
    """Build an IntentDraft from a validated tool input dict.

    This is a pure function -- no API calls, fully testable.

    Parameters:
        data: The ``input`` dict from Claude's tool_use response.

    Returns:
        A validated ``IntentDraft``.

    Raises:
        NLProcessorError: If required fields are missing or invalid.
    """
    roles = _validate_roles(data)
    protocol_name = data["protocol_name"]

    return IntentDraft(
        protocol_name=protocol_name.strip().replace(" ", "_"),
        roles=roles,
        messages=_validate_messages(data.get("messages", []), roles),
        choices=_validate_choices(data.get("choices", []), roles),
        properties=_validate_properties(data),
    )
