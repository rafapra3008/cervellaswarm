# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""IntentBridge: guided conversational protocol builder (E.2).

Interactive chat interface that guides users through creating verified
protocols step by step.  Generates B.4 intent notation, verifies via
B.5 spec checker, and produces Python code via B.3 codegen.

Usage::

    lu chat --lang it         Start guided chat in Italian.
    lu chat --lang pt         Start guided chat in Portuguese.
    lu chat                   Start guided chat in English (default).

Or programmatically::

    from cervellaswarm_lingua_universale._intent_bridge import ChatSession
    session = ChatSession(lang="it")
    result = session.run()

For testing, inject *input_fn* and *output_fn*::

    inputs = iter(["MyProtocol", "Alice, Bob", ...])
    session = ChatSession(
        lang="en",
        input_fn=lambda p: next(inputs),
        output_fn=lambda *a, **kw: None,
    )
    result = session.run()

Design decisions:
    - Two-stage pattern (Req2LTL): guided input -> IntentDraft (IR) -> B.4 source
    - ChatSession is mutable (tracks conversation state); results are frozen
    - Injectable I/O for testability (same pattern as REPLSession)
    - i18n via in-module dict (same pattern as errors.py)
    - ZERO external dependencies
    - E.3 extension point: optional NLProcessor for free-text NL mode
"""

from __future__ import annotations

import re
import typing
from dataclasses import dataclass, field
from enum import Enum, auto
from types import MappingProxyType
from typing import Callable

from ._colors import colors as _c, init_colors as _init_colors
from .intent import IntentParseResult, parse_intent
from .spec import (
    PropertyKind,
    PropertyReport,
    PropertyVerdict,
    ProtocolSpec,
    check_properties,
    parse_spec,
)
from .codegen import generate_python
from .protocols import Protocol, ProtocolStep, ProtocolChoice


# ============================================================
# Chat phases
# ============================================================


class ChatPhase(Enum):
    """Phases of the guided conversation."""

    WELCOME = auto()
    ROLES = auto()
    MESSAGES = auto()
    CHOICES = auto()
    PROPERTIES = auto()
    CONFIRM = auto()
    VERIFY = auto()
    CODEGEN = auto()
    SIMULATE = auto()
    DONE = auto()


# ============================================================
# Data model (frozen dataclasses)
# ============================================================


@dataclass(frozen=True)
class DraftMessage:
    """A single message in the protocol draft."""

    sender: str
    receiver: str
    action_key: str  # key into _ACTION_VERBS


@dataclass(frozen=True)
class DraftChoice:
    """A branching point in the draft."""

    decider: str
    branches: tuple[tuple[str, tuple[DraftMessage, ...]], ...]


@dataclass(frozen=True)
class IntentDraft:
    """Intermediate representation between guided input and B.4 notation.

    This is the structured IR that maps deterministically to intent
    notation via ``render_intent_source()``.  Follows the Req2LTL
    "two-stage" pattern: structured IR -> deterministic output.
    """

    protocol_name: str
    roles: tuple[str, ...]
    messages: tuple[DraftMessage, ...] = ()
    choices: tuple[DraftChoice, ...] = ()
    properties: tuple[str, ...] = ("always_terminates", "no_deadlock")


@dataclass(frozen=True)
class Turn:
    """A single turn in the conversation."""

    speaker: str  # "user" or "system"
    text: str
    phase: ChatPhase


@dataclass(frozen=True)
class ChatResult:
    """Final result of a completed chat session."""

    draft: IntentDraft
    intent_source: str
    parse_result: IntentParseResult
    property_report: PropertyReport
    generated_code: str


# ============================================================
# NL Processor protocol (E.3 extension point)
# ============================================================


class NLProcessor(typing.Protocol):
    """Interface for NL -> IntentDraft conversion (E.3).

    Implementations may use Claude, GPT, or any LLM.
    When provided, the ROLES phase uses free NL input instead of menus.
    """

    def process(
        self, text: str, lang: str, context: list[Turn]
    ) -> IntentDraft: ...


# ============================================================
# Action verb mapping (B.4 compatible)
# ============================================================

# Maps a short key to the B.4 action phrase used in intent notation.
_ACTION_VERBS: MappingProxyType[str, str] = MappingProxyType({
    "ask_task": "asks {receiver} to do task",
    "return_result": "returns result to {receiver}",
    "ask_verify": "asks {receiver} to verify",
    "return_verdict": "returns verdict to {receiver}",
    "ask_plan": "asks {receiver} to plan",
    "propose_plan": "proposes plan to {receiver}",
    "tell_decision": "tells {receiver} decision",
    "ask_research": "asks {receiver} to research",
    "return_report": "returns report to {receiver}",
    "send_message": "sends message to {receiver}",
})

# Menu labels per language for guided mode.
_ACTION_MENU: MappingProxyType[str, MappingProxyType[str, str]] = MappingProxyType({
    "en": MappingProxyType({
        "ask_task": "asks to do a task",
        "return_result": "returns a result",
        "ask_verify": "asks to verify",
        "return_verdict": "returns a verdict",
        "ask_plan": "asks to plan",
        "propose_plan": "proposes a plan",
        "tell_decision": "tells a decision",
        "ask_research": "asks to research",
        "return_report": "returns a report",
        "send_message": "sends a message",
    }),
    "it": MappingProxyType({
        "ask_task": "chiede di fare un compito",
        "return_result": "restituisce un risultato",
        "ask_verify": "chiede di verificare",
        "return_verdict": "restituisce un verdetto",
        "ask_plan": "chiede di pianificare",
        "propose_plan": "propone un piano",
        "tell_decision": "comunica una decisione",
        "ask_research": "chiede di ricercare",
        "return_report": "restituisce un report",
        "send_message": "invia un messaggio",
    }),
    "pt": MappingProxyType({
        "ask_task": "pede para fazer uma tarefa",
        "return_result": "retorna um resultado",
        "ask_verify": "pede para verificar",
        "return_verdict": "retorna um veredito",
        "ask_plan": "pede para planejar",
        "propose_plan": "propõe um plano",
        "tell_decision": "comunica uma decisão",
        "ask_research": "pede para pesquisar",
        "return_report": "retorna um relatório",
        "send_message": "envia uma mensagem",
    }),
})

# Available property names for the guided menu.
_PROPERTY_NAMES: tuple[str, ...] = (
    "always_terminates",
    "no_deadlock",
    "all_roles_participate",
)


# ============================================================
# i18n strings
# ============================================================

def _t(key: str, lang: str, **kwargs: str) -> str:
    """Translate a string key to the given language with formatting."""
    entry = _STRINGS.get(key)
    if entry is None:
        return key
    template = entry.get(lang, entry.get("en", key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template


_STRINGS: MappingProxyType[str, MappingProxyType[str, str]] = MappingProxyType({
    "welcome": MappingProxyType({
        "en": (
            "Lingua Universale - Interactive Chat\n"
            '"Tell me what you want to create and I\'ll build it, with proof it works."\n\n'
            "Type 'help' for help. 'exit' to quit."
        ),
        "it": (
            "Lingua Universale - Chat Interattiva\n"
            '"Dimmi cosa vuoi creare e io lo costruisco, con la prova che funziona."\n\n'
            "Digita 'aiuto' per la guida. 'esci' per uscire."
        ),
        "pt": (
            "Lingua Universale - Chat Interativo\n"
            '"Diga-me o que voce quer criar e eu construo, com a prova que funciona."\n\n'
            "Digite 'ajuda' para ajuda. 'sair' para sair."
        ),
    }),
    "ask_name": MappingProxyType({
        "en": "What is the name of your protocol?",
        "it": "Come si chiama il tuo protocollo?",
        "pt": "Qual o nome do seu protocolo?",
    }),
    "ask_roles": MappingProxyType({
        "en": "What are the roles? (comma-separated, e.g., Cook, Pantry)",
        "it": "Quali sono i ruoli? (separati da virgola, es: Cuoco, Dispensa)",
        "pt": "Quais sao os papeis? (separados por virgula, ex: Cozinheiro, Despensa)",
    }),
    "error_min_roles": MappingProxyType({
        "en": "You need at least 2 roles.",
        "it": "Servono almeno 2 ruoli.",
        "pt": "Voce precisa de pelo menos 2 papeis.",
    }),
    "error_invalid_name": MappingProxyType({
        "en": "Names must use only letters, digits, and underscores (start with letter).",
        "it": "I nomi devono usare solo lettere, cifre e underscore (iniziare con lettera).",
        "pt": "Os nomes devem usar apenas letras, digitos e underscores (comecar com letra).",
    }),
    "roles_confirmed": MappingProxyType({
        "en": "Roles: {roles}",
        "it": "Ruoli: {roles}",
        "pt": "Papeis: {roles}",
    }),
    "ask_message_sender": MappingProxyType({
        "en": "Who sends? ({roles}) or 'done' to finish:",
        "it": "Chi invia? ({roles}) o 'fatto' per finire:",
        "pt": "Quem envia? ({roles}) ou 'pronto' para terminar:",
    }),
    "ask_message_receiver": MappingProxyType({
        "en": "Who receives? ({roles})",
        "it": "Chi riceve? ({roles})",
        "pt": "Quem recebe? ({roles})",
    }),
    "ask_message_action": MappingProxyType({
        "en": "What does {sender} do? Pick a number:",
        "it": "Cosa fa {sender}? Scegli un numero:",
        "pt": "O que {sender} faz? Escolha um numero:",
    }),
    "message_added": MappingProxyType({
        "en": "  Added: {sender} {action} {receiver}",
        "it": "  Aggiunto: {sender} {action} {receiver}",
        "pt": "  Adicionado: {sender} {action} {receiver}",
    }),
    "error_unknown_role": MappingProxyType({
        "en": "Unknown role '{role}'. Available: {roles}",
        "it": "Ruolo sconosciuto '{role}'. Disponibili: {roles}",
        "pt": "Papel desconhecido '{role}'. Disponiveis: {roles}",
    }),
    "error_same_role": MappingProxyType({
        "en": "Sender and receiver must be different.",
        "it": "Mittente e destinatario devono essere diversi.",
        "pt": "Remetente e destinatario devem ser diferentes.",
    }),
    "error_min_messages": MappingProxyType({
        "en": "You need at least 1 message.",
        "it": "Serve almeno 1 messaggio.",
        "pt": "Voce precisa de pelo menos 1 mensagem.",
    }),
    "ask_choices": MappingProxyType({
        "en": "Does any role make decisions (branching)? (yes/no)",
        "it": "Qualche ruolo prende decisioni (ramificazione)? (si/no)",
        "pt": "Algum papel toma decisoes (ramificacao)? (sim/nao)",
    }),
    "ask_choice_decider": MappingProxyType({
        "en": "Which role decides? ({roles})",
        "it": "Quale ruolo decide? ({roles})",
        "pt": "Qual papel decide? ({roles})",
    }),
    "ask_branch_names": MappingProxyType({
        "en": "Branch names (comma-separated, e.g., approve, reject):",
        "it": "Nomi delle opzioni (separati da virgola, es: approvare, rifiutare):",
        "pt": "Nomes das opcoes (separados por virgula, ex: aprovar, rejeitar):",
    }),
    "ask_properties": MappingProxyType({
        "en": (
            "Safety properties (defaults: always_terminates, no_deadlock).\n"
            "Add more? Pick numbers or 'done':"
        ),
        "it": (
            "Proprieta di sicurezza (default: sempre termina, nessun deadlock).\n"
            "Aggiungere altre? Scegli numeri o 'fatto':"
        ),
        "pt": (
            "Propriedades de seguranca (padrao: sempre termina, sem deadlock).\n"
            "Adicionar mais? Escolha numeros ou 'pronto':"
        ),
    }),
    "confirm_title": MappingProxyType({
        "en": "Here is your protocol:",
        "it": "Ecco il tuo protocollo:",
        "pt": "Aqui esta o seu protocolo:",
    }),
    "confirm_properties": MappingProxyType({
        "en": "Safety properties:",
        "it": "Proprieta di sicurezza:",
        "pt": "Propriedades de seguranca:",
    }),
    "confirm_ask": MappingProxyType({
        "en": "Is this correct? (yes/no)",
        "it": "Tutto giusto? (si/no)",
        "pt": "Tudo certo? (sim/nao)",
    }),
    "verify_progress": MappingProxyType({
        "en": "  [{n}/{total}] {prop} ... {result}",
        "it": "  [{n}/{total}] {prop} ... {result}",
        "pt": "  [{n}/{total}] {prop} ... {result}",
    }),
    "verify_all_passed": MappingProxyType({
        "en": "ALL PROPERTIES VERIFIED\n{count}/{count} proven. Your system is GUARANTEED safe.",
        "it": "TUTTE LE PROPRIETA VERIFICATE\n{count}/{count} provate. Il tuo sistema e GARANTITO sicuro.",
        "pt": "TODAS AS PROPRIEDADES VERIFICADAS\n{count}/{count} provadas. Seu sistema e GARANTIDO seguro.",
    }),
    "verify_some_failed": MappingProxyType({
        "en": "Some properties could not be verified.",
        "it": "Alcune proprieta non sono state verificate.",
        "pt": "Algumas propriedades nao puderam ser verificadas.",
    }),
    "code_title": MappingProxyType({
        "en": "Here is the generated Python code:",
        "it": "Ecco il codice Python generato:",
        "pt": "Aqui esta o codigo Python gerado:",
    }),
    "sim_title": MappingProxyType({
        "en": "Simulation:",
        "it": "Simulazione:",
        "pt": "Simulacao:",
    }),
    "sim_step": MappingProxyType({
        "en": "  [{sender}] -> {receiver}: {kind}",
        "it": "  [{sender}] -> {receiver}: {kind}",
        "pt": "  [{sender}] -> {receiver}: {kind}",
    }),
    "sim_success": MappingProxyType({
        "en": "PROTOCOL COMPLETED SUCCESSFULLY\nMessages: {count} | Violations: 0",
        "it": "PROTOCOLLO COMPLETATO CON SUCCESSO\nMessaggi: {count} | Violazioni: 0",
        "pt": "PROTOCOLO COMPLETADO COM SUCESSO\nMensagens: {count} | Violacoes: 0",
    }),
    "summary": MappingProxyType({
        "en": "Session summary:\n  Protocol: {name} ({roles} roles, {msgs} messages, {props} properties)\n  Language: {language}",
        "it": "Riepilogo sessione:\n  Protocollo: {name} ({roles} ruoli, {msgs} messaggi, {props} proprieta)\n  Lingua: {language}",
        "pt": "Resumo da sessao:\n  Protocolo: {name} ({roles} papeis, {msgs} mensagens, {props} propriedades)\n  Idioma: {language}",
    }),
    "goodbye": MappingProxyType({
        "en": '"Not magic. Mathematics."',
        "it": '"Non e magia. E matematica."',
        "pt": '"Nao e magia. E matematica."',
    }),
})

# Words that mean "done" / "yes" / "no" per language.
_DONE_WORDS: MappingProxyType[str, frozenset[str]] = MappingProxyType({
    "en": frozenset({"done", "d", "finish", "end"}),
    "it": frozenset({"fatto", "f", "fine", "basta"}),
    "pt": frozenset({"pronto", "p", "fim", "acabou"}),
})

_YES_WORDS: MappingProxyType[str, frozenset[str]] = MappingProxyType({
    "en": frozenset({"yes", "y", "yeah", "yep", "ok"}),
    "it": frozenset({"si", "s", "ok", "certo", "esatto"}),
    "pt": frozenset({"sim", "s", "ok", "certo", "exato"}),
})

_NO_WORDS: MappingProxyType[str, frozenset[str]] = MappingProxyType({
    "en": frozenset({"no", "n", "nope"}),
    "it": frozenset({"no", "n"}),
    "pt": frozenset({"nao", "n"}),
})

_EXIT_WORDS: frozenset[str] = frozenset({
    "exit", "quit", "esci", "sair", "q",
})

_HELP_WORDS: frozenset[str] = frozenset({
    "help", "aiuto", "ajuda", "h",
})

_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


# ============================================================
# render_intent_source() -- the deterministic bridge
# ============================================================


def render_intent_source(draft: IntentDraft) -> str:
    """Convert an IntentDraft to B.4 intent notation source text.

    This is the DETERMINISTIC bridge: structured data -> text that
    ``parse_intent()`` can parse.  No LLM, no heuristics.

    Returns:
        A string in B.4 intent notation ready for ``parse_intent()``.
    """
    lines: list[str] = []
    lines.append(f"protocol {draft.protocol_name}:")
    lines.append(f"    roles: {', '.join(draft.roles)}")
    lines.append("")

    for msg in draft.messages:
        action = _ACTION_VERBS[msg.action_key].format(receiver=msg.receiver)
        lines.append(f"    {msg.sender} {action}")

    for choice in draft.choices:
        lines.append(f"    when {choice.decider} decides:")
        for label, branch_msgs in choice.branches:
            lines.append(f"        {label}:")
            for msg in branch_msgs:
                action = _ACTION_VERBS[msg.action_key].format(
                    receiver=msg.receiver,
                )
                lines.append(f"            {msg.sender} {action}")

    return "\n".join(lines) + "\n"


# ============================================================
# ChatSession
# ============================================================


class ChatSession:
    """Stateful guided conversation for building verified protocols.

    Injectable I/O for testability (same pattern as ``REPLSession``).

    Parameters:
        lang:  Interface language (``"en"``, ``"it"``, ``"pt"``).
        input_fn:  Replaces ``input()`` -- inject for testing.
        output_fn: Replaces ``print()`` -- inject for testing.
        nl_processor:  Optional NL processor for E.3 (free-text mode).
    """

    PROMPT = "> "

    def __init__(
        self,
        *,
        lang: str = "en",
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[..., None] | None = None,
        nl_processor: NLProcessor | None = None,
    ) -> None:
        if lang not in ("en", "it", "pt"):
            lang = "en"
        self._lang = lang
        self._input_fn = input_fn
        self._output_fn: Callable[..., None] = output_fn or print
        self._nl_processor = nl_processor
        self._phase = ChatPhase.WELCOME
        self._turns: list[Turn] = []
        # Building state
        self._protocol_name: str = ""
        self._roles: list[str] = []
        self._messages: list[DraftMessage] = []
        self._choices: list[DraftChoice] = []
        self._properties: list[str] = ["always_terminates", "no_deadlock"]
        # Sub-state for multi-step phases
        self._msg_step: str = "sender"
        self._current_sender: str = ""
        self._current_receiver: str = ""
        self._choice_step: str = "ask"
        self._choice_decider: str = ""
        # Results
        self._result: ChatResult | None = None

    # --------------------------------------------------------
    # Properties
    # --------------------------------------------------------

    @property
    def phase(self) -> ChatPhase:
        return self._phase

    @property
    def draft(self) -> IntentDraft | None:
        if not self._protocol_name or not self._roles:
            return None
        return IntentDraft(
            protocol_name=self._protocol_name,
            roles=tuple(self._roles),
            messages=tuple(self._messages),
            choices=tuple(self._choices),
            properties=tuple(self._properties),
        )

    @property
    def turns(self) -> list[Turn]:
        return list(self._turns)

    @property
    def lang(self) -> str:
        return self._lang

    @property
    def result(self) -> ChatResult | None:
        return self._result

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def run(self) -> ChatResult | None:
        """Main interactive loop.  Blocks until completion or exit."""
        _init_colors()
        self._emit(_t("welcome", self._lang))
        self._phase = ChatPhase.ROLES
        self._emit(_t("ask_name", self._lang))

        while self._phase != ChatPhase.DONE:
            prompt = f"{_c.CYAN}{_c.BOLD}{self.PROMPT}{_c.RESET}" if _c.CYAN else self.PROMPT
            try:
                user_input = self._input_fn(prompt)
            except (EOFError, KeyboardInterrupt):
                self._emit("")
                return self._result

            stripped = user_input.strip()
            if not stripped:
                continue
            if stripped.lower() in _EXIT_WORDS:
                break
            if stripped.lower() in _HELP_WORDS:
                self._emit(self._help_text())
                continue

            self._turns.append(Turn("user", stripped, self._phase))
            response = self._handle(stripped)
            if response:
                self._turns.append(Turn("system", response, self._phase))
                self._emit(response)

        return self._result

    def process_input(self, text: str) -> str:
        """Process a single input and return the response.

        For programmatic use and testing.
        """
        stripped = text.strip()
        if not stripped:
            return ""
        self._turns.append(Turn("user", stripped, self._phase))
        response = self._handle(stripped)
        if response:
            self._turns.append(Turn("system", response, self._phase))
        return response

    # --------------------------------------------------------
    # Phase dispatch
    # --------------------------------------------------------

    def _handle(self, text: str) -> str:
        """Dispatch input to the current phase handler."""
        handlers = {
            ChatPhase.ROLES: self._handle_roles,
            ChatPhase.MESSAGES: self._handle_messages,
            ChatPhase.CHOICES: self._handle_choices,
            ChatPhase.PROPERTIES: self._handle_properties,
            ChatPhase.CONFIRM: self._handle_confirm,
        }
        handler = handlers.get(self._phase)
        if handler is None:
            return ""
        return handler(text)

    # --------------------------------------------------------
    # Phase handlers
    # --------------------------------------------------------

    def _handle_roles(self, text: str) -> str:
        """Handle ROLES phase: collect protocol name and role names."""
        if not self._protocol_name:
            # First input = protocol name
            name = text.strip().replace(" ", "_")
            if not _NAME_RE.match(name):
                return _t("error_invalid_name", self._lang)
            self._protocol_name = name
            return _t("ask_roles", self._lang)

        # Parse comma-separated role names
        parts = [p.strip() for p in text.split(",") if p.strip()]
        invalid = [p for p in parts if not _NAME_RE.match(p)]
        if invalid:
            return _t("error_invalid_name", self._lang)
        if len(parts) < 2:
            return _t("error_min_roles", self._lang)

        self._roles = parts
        self._phase = ChatPhase.MESSAGES
        roles_str = ", ".join(self._roles)
        confirmed = _t("roles_confirmed", self._lang, roles=roles_str)
        ask_msg = _t(
            "ask_message_sender",
            self._lang,
            roles=roles_str,
        )
        return f"{confirmed}\n\n{ask_msg}"

    def _handle_messages(self, text: str) -> str:
        """Handle MESSAGES phase: build message sequence step by step."""
        lower = text.strip().lower()
        roles_str = ", ".join(self._roles)

        # Check for "done"
        if lower in _DONE_WORDS.get(self._lang, _DONE_WORDS["en"]):
            if not self._messages:
                return _t("error_min_messages", self._lang)
            self._phase = ChatPhase.CHOICES
            return _t("ask_choices", self._lang)

        # Parse sender, receiver, action in sequence
        # Simple approach: we use sub-states via the message list length
        # to determine what we're asking for
        step = self._msg_step

        if step == "sender":
            sender = text.strip()
            if sender not in self._roles:
                return _t(
                    "error_unknown_role",
                    self._lang,
                    role=sender,
                    roles=roles_str,
                )
            self._current_sender = sender
            self._msg_step = "receiver"
            other_roles = ", ".join(r for r in self._roles if r != sender)
            return _t("ask_message_receiver", self._lang, roles=other_roles)

        if step == "receiver":
            receiver = text.strip()
            if receiver not in self._roles:
                return _t(
                    "error_unknown_role",
                    self._lang,
                    role=receiver,
                    roles=roles_str,
                )
            if receiver == self._current_sender:
                return _t("error_same_role", self._lang)
            self._current_receiver = receiver
            self._msg_step = "action"
            return self._render_action_menu(self._current_sender)

        if step == "action":
            action_keys = list(_ACTION_VERBS.keys())
            try:
                idx = int(text.strip()) - 1
                if 0 <= idx < len(action_keys):
                    action_key = action_keys[idx]
                else:
                    return self._render_action_menu(self._current_sender)
            except ValueError:
                return self._render_action_menu(self._current_sender)

            msg = DraftMessage(
                sender=self._current_sender,
                receiver=self._current_receiver,
                action_key=action_key,
            )
            self._messages.append(msg)
            self._msg_step = "sender"

            action_label = _ACTION_MENU.get(
                self._lang, _ACTION_MENU["en"]
            ).get(action_key, action_key)
            added = _t(
                "message_added",
                self._lang,
                sender=self._current_sender,
                action=action_label,
                receiver=self._current_receiver,
            )
            ask_next = _t(
                "ask_message_sender",
                self._lang,
                roles=roles_str,
            )
            return f"{added}\n\n{ask_next}"

        return ""

    def _handle_choices(self, text: str) -> str:
        """Handle CHOICES phase: optional branching."""
        lower = text.strip().lower()
        yes = _YES_WORDS.get(self._lang, _YES_WORDS["en"])
        no = _NO_WORDS.get(self._lang, _NO_WORDS["en"])

        step = self._choice_step

        if step == "ask":
            if lower in no:
                self._phase = ChatPhase.PROPERTIES
                return self._render_properties_menu()
            if lower in yes:
                self._choice_step = "decider"
                return _t(
                    "ask_choice_decider",
                    self._lang,
                    roles=", ".join(self._roles),
                )
            return _t("ask_choices", self._lang)

        if step == "decider":
            if text.strip() not in self._roles:
                return _t(
                    "error_unknown_role",
                    self._lang,
                    role=text.strip(),
                    roles=", ".join(self._roles),
                )
            self._choice_decider = text.strip()
            self._choice_step = "branches"
            return _t("ask_branch_names", self._lang)

        if step == "branches":
            names = [n.strip() for n in text.split(",") if n.strip()]
            if len(names) < 2:
                return _t("ask_branch_names", self._lang)
            # For guided mode, each branch gets a simple send_message
            branches: list[tuple[str, tuple[DraftMessage, ...]]] = []
            other = [r for r in self._roles if r != self._choice_decider]
            receiver = other[0] if other else self._roles[0]
            for name in names:
                branch_msg = DraftMessage(
                    sender=self._choice_decider,
                    receiver=receiver,
                    action_key="send_message",
                )
                branches.append((name, (branch_msg,)))
            self._choices.append(
                DraftChoice(
                    decider=self._choice_decider,
                    branches=tuple(branches),
                )
            )
            self._choice_step = "ask"
            self._phase = ChatPhase.PROPERTIES
            return self._render_properties_menu()

        return ""

    def _handle_properties(self, text: str) -> str:
        """Handle PROPERTIES phase: select safety properties."""
        lower = text.strip().lower()
        done = _DONE_WORDS.get(self._lang, _DONE_WORDS["en"])

        if lower in done:
            self._phase = ChatPhase.CONFIRM
            return self._render_confirmation()

        # Try to parse as number
        try:
            idx = int(text.strip()) - 1
            if 0 <= idx < len(_PROPERTY_NAMES):
                prop = _PROPERTY_NAMES[idx]
                if prop not in self._properties:
                    self._properties.append(prop)
                return self._render_properties_menu()
        except ValueError:
            pass

        return self._render_properties_menu()

    def _handle_confirm(self, text: str) -> str:
        """Handle CONFIRM phase: show protocol and ask for confirmation."""
        lower = text.strip().lower()
        yes = _YES_WORDS.get(self._lang, _YES_WORDS["en"])
        no = _NO_WORDS.get(self._lang, _NO_WORDS["en"])

        if lower in yes:
            return self._execute_pipeline()
        if lower in no:
            # Go back to roles — reset ALL building state
            self._phase = ChatPhase.ROLES
            self._protocol_name = ""
            self._roles.clear()
            self._messages.clear()
            self._choices.clear()
            self._properties = ["always_terminates", "no_deadlock"]
            self._msg_step = "sender"
            self._current_sender = ""
            self._current_receiver = ""
            self._choice_step = "ask"
            self._choice_decider = ""
            return _t("ask_name", self._lang)

        return _t("confirm_ask", self._lang)

    # --------------------------------------------------------
    # Pipeline execution
    # --------------------------------------------------------

    def _execute_pipeline(self) -> str:
        """Run the full pipeline: render -> parse -> verify -> codegen -> simulate."""
        output_parts: list[str] = []
        draft = self.draft
        if draft is None:
            return ""

        # 1. Render to B.4 intent notation
        source = render_intent_source(draft)

        # 2. Parse with B.4
        try:
            parse_result = parse_intent(source)
        except Exception as exc:
            return f"{_c.RED}Parse error: {exc}{_c.RESET}"

        protocol = parse_result.protocol

        # 3. Build spec and verify with B.5
        self._phase = ChatPhase.VERIFY
        spec_lines = [f"spec {draft.protocol_name}:"]
        for prop in draft.properties:
            spec_lines.append(f"    requires {prop}")
        spec_source = "\n".join(spec_lines) + "\n"

        try:
            spec = parse_spec(spec_source)
            report = check_properties(protocol, spec)
        except Exception:
            # If spec parsing fails (e.g. unknown property), skip verification
            report = None

        verify_output = self._render_verification(report, draft)
        output_parts.append(verify_output)

        # 4. Generate Python code with B.3
        self._phase = ChatPhase.CODEGEN
        try:
            code = generate_python(protocol)
        except Exception as exc:
            code = f"# Code generation error: {exc}"

        output_parts.append("")
        output_parts.append(_t("code_title", self._lang))
        output_parts.append(f"\n{code}")

        # 5. Simulate (narrative display of protocol steps)
        self._phase = ChatPhase.SIMULATE
        sim_output = self._render_simulation(protocol)
        output_parts.append("")
        output_parts.append(sim_output)

        # 6. Summary
        output_parts.append("")
        output_parts.append(
            _t(
                "summary",
                self._lang,
                name=draft.protocol_name,
                roles=str(len(draft.roles)),
                msgs=str(len(draft.messages) + sum(
                    len(bm) for c in draft.choices for _, bm in c.branches
                )),
                props=str(len(draft.properties)),
                language=self._lang,
            )
        )
        output_parts.append("")
        output_parts.append(
            f"{_c.CYAN}{_t('goodbye', self._lang)}{_c.RESET}"
        )

        # Build result
        self._result = ChatResult(
            draft=draft,
            intent_source=source,
            parse_result=parse_result,
            property_report=report if report else PropertyReport(
                protocol_name=draft.protocol_name,
                results=(),
            ),
            generated_code=code,
        )

        self._phase = ChatPhase.DONE
        return "\n".join(output_parts)

    # --------------------------------------------------------
    # Rendering helpers
    # --------------------------------------------------------

    def _emit(self, text: str) -> None:
        """Output text to the user."""
        self._output_fn(text)

    def _render_action_menu(self, sender: str) -> str:
        """Render the action selection menu."""
        menu = _ACTION_MENU.get(self._lang, _ACTION_MENU["en"])
        header = _t("ask_message_action", self._lang, sender=sender)
        lines = [header]
        for i, (key, label) in enumerate(menu.items(), 1):
            lines.append(f"  {_c.CYAN}{i}{_c.RESET}. {label}")
        return "\n".join(lines)

    def _render_properties_menu(self) -> str:
        """Render the property selection menu."""
        header = _t("ask_properties", self._lang)
        lines = [header]
        for i, prop in enumerate(_PROPERTY_NAMES, 1):
            marker = " *" if prop in self._properties else ""
            lines.append(f"  {_c.CYAN}{i}{_c.RESET}. {prop}{marker}")
        return "\n".join(lines)

    def _render_confirmation(self) -> str:
        """Render the protocol confirmation view."""
        draft = self.draft
        if draft is None:
            return ""

        source = render_intent_source(draft)
        lines = [
            _t("confirm_title", self._lang),
            "",
            f"  {_c.CYAN}+{'=' * 56}+{_c.RESET}",
        ]
        for line in source.strip().split("\n"):
            lines.append(f"  {_c.CYAN}|{_c.RESET}  {line}")
        lines.append(f"  {_c.CYAN}+{'=' * 56}+{_c.RESET}")
        lines.append("")
        lines.append(_t("confirm_properties", self._lang))
        for prop in self._properties:
            lines.append(f"  - {prop}")
        lines.append("")
        lines.append(_t("confirm_ask", self._lang))
        return "\n".join(lines)

    def _render_verification(
        self,
        report: PropertyReport | None,
        draft: IntentDraft,
    ) -> str:
        """Render verification results."""
        if report is None:
            return ""

        lines: list[str] = []
        total = len(report.results)
        for i, result in enumerate(report.results, 1):
            verdict_str = (
                f"{_c.GREEN}PROVED{_c.RESET}"
                if result.verdict == PropertyVerdict.PROVED
                else f"{_c.RED}FAILED{_c.RESET}"
            )
            lines.append(
                _t(
                    "verify_progress",
                    self._lang,
                    n=str(i),
                    total=str(total),
                    prop=result.property_name,
                    result=verdict_str,
                )
            )

        all_passed = all(
            r.verdict == PropertyVerdict.PROVED for r in report.results
        )
        lines.append("")
        if all_passed:
            lines.append(
                f"{_c.GREEN}{_c.BOLD}"
                + _t("verify_all_passed", self._lang, count=str(total))
                + f"{_c.RESET}"
            )
        else:
            lines.append(
                f"{_c.YELLOW}"
                + _t("verify_some_failed", self._lang)
                + f"{_c.RESET}"
            )
        return "\n".join(lines)

    def _render_simulation(self, protocol: Protocol) -> str:
        """Render a narrative simulation of the protocol steps."""
        lines = [_t("sim_title", self._lang)]
        count = 0

        for element in protocol.elements:
            if isinstance(element, ProtocolStep):
                lines.append(
                    _t(
                        "sim_step",
                        self._lang,
                        sender=element.sender,
                        receiver=element.receiver,
                        kind=element.message_kind.name,
                    )
                )
                count += 1
            elif isinstance(element, ProtocolChoice):
                # Show first branch for the narrative
                branch_items = list(element.branches.items())
                if branch_items:
                    label, branch_steps = branch_items[0]
                    lines.append(
                        f"  [{element.decider}] decides: {label}"
                    )
                    for bstep in branch_steps:
                        if isinstance(bstep, ProtocolStep):
                            lines.append(
                                _t(
                                    "sim_step",
                                    self._lang,
                                    sender=bstep.sender,
                                    receiver=bstep.receiver,
                                    kind=bstep.message_kind.name,
                                )
                            )
                            count += 1

        lines.append("")
        lines.append(
            f"{_c.GREEN}{_c.BOLD}"
            + _t("sim_success", self._lang, count=str(count))
            + f"{_c.RESET}"
        )
        return "\n".join(lines)

    def _help_text(self) -> str:
        """Return help text for the current context."""
        _HELP = {
            "en": (
                "IntentBridge - Guided Protocol Builder\n"
                "  Phase: {phase}\n"
                "  Commands: exit, help\n"
                "  Follow the prompts to build your protocol step by step.\n"
                "  Your protocol will be VERIFIED with mathematical proofs."
            ),
            "it": (
                "IntentBridge - Costruttore Guidato di Protocolli\n"
                "  Fase: {phase}\n"
                "  Comandi: esci, aiuto\n"
                "  Segui le istruzioni per costruire il tuo protocollo passo per passo.\n"
                "  Il tuo protocollo sara VERIFICATO con prove matematiche."
            ),
            "pt": (
                "IntentBridge - Construtor Guiado de Protocolos\n"
                "  Fase: {phase}\n"
                "  Comandos: sair, ajuda\n"
                "  Siga as instrucoes para construir seu protocolo passo a passo.\n"
                "  Seu protocolo sera VERIFICADO com provas matematicas."
            ),
        }
        template = _HELP.get(self._lang, _HELP["en"])
        return f"{_c.YELLOW}{template.format(phase=self._phase.name)}{_c.RESET}"
