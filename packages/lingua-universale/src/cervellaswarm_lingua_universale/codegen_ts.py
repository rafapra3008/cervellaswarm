# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""TypeScript code generation from verified protocol definitions.

Generates type-safe TypeScript code from Protocol definitions using
discriminated unions, interfaces, and a runtime session class.

The generated code includes:
- Discriminated union for MessageKind (string literal types)
- Message interfaces with ``readonly kind`` discriminant
- Role interfaces with typed ``send*`` methods
- Union types for ProtocolChoice branches
- A ``ProtocolSession`` class with role accessors
- JSDoc annotations with ``@verified`` tags for proved properties

Architecture follows ``codegen.py`` (template-based, pure string
generation).  ZERO external dependencies.

Sprint 3 of PLAN_LU_GENERATE.md.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Sequence

from ._codegen_common import collect_all_steps as _collect_all_steps
from ._codegen_common import used_message_kinds as _used_message_kinds
from .protocols import Protocol, ProtocolChoice, ProtocolElement, ProtocolStep
from .types import MessageKind

if TYPE_CHECKING:
    from .spec import PropertySpec, ProtocolSpec


# ============================================================
# TypeScript reserved words
# ============================================================

_TS_RESERVED: frozenset[str] = frozenset({
    "abstract", "any", "as", "async", "await", "bigint", "boolean",
    "break", "case", "catch", "class", "const", "constructor",
    "continue", "debugger", "declare", "default", "delete", "do",
    "else", "enum", "export", "extends", "false", "finally", "for",
    "from", "function", "get", "global", "if", "implements", "import",
    "in", "infer", "instanceof", "interface", "is", "keyof", "let",
    "module", "namespace", "never", "new", "null", "number", "object",
    "of", "package", "private", "protected", "public", "readonly",
    "require", "return", "satisfies", "set", "static", "string",
    "super", "switch", "symbol", "this", "throw", "true", "try",
    "type", "typeof", "undefined", "unique", "unknown", "var", "void",
    "while", "with", "yield",
})


# ============================================================
# Helpers
# ============================================================


def _escape_ts_string(s: str) -> str:
    """Escape a string for safe embedding in generated TypeScript source.

    Handles backslash, single quotes, newlines, and carriage returns.
    """
    return (
        s.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )


def _safe_ts_ident(name: str) -> str:
    """Sanitize a string into a valid TypeScript identifier.

    Replaces non-alphanumeric characters with ``_``.
    Prefixes with ``_`` if the result starts with a digit or is reserved.

    Raises ``ValueError`` if the input is empty.
    """
    if not name:
        raise ValueError("cannot create TypeScript identifier from empty string")
    result = re.sub(r"[^A-Za-z0-9_$]", "_", name)
    if result[0].isdigit():
        result = f"_{result}"
    if result in _TS_RESERVED:
        result = f"{result}_"
    return result


def _to_camel_case(name: str) -> str:
    """Convert a snake_case or plain string to camelCase.

    Examples: "task_request" -> "taskRequest", "hello" -> "hello"
    """
    parts = name.split("_")
    if not parts:
        return name
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def _to_pascal_case(name: str) -> str:
    """Convert a snake_case or plain string to PascalCase.

    Examples: "task_request" -> "TaskRequest", "hello" -> "Hello"
    """
    parts = name.split("_")
    return "".join(p.capitalize() for p in parts if p)


def _kind_to_interface_name(kind: MessageKind) -> str:
    """Convert a MessageKind to its TypeScript interface name.

    Example: MessageKind.TASK_REQUEST -> "TaskRequestMessage"
    """
    return f"{_to_pascal_case(kind.value)}Message"


def _kind_to_literal(kind: MessageKind) -> str:
    """Convert a MessageKind to its TypeScript string literal.

    Example: MessageKind.TASK_REQUEST -> "'task_request'"
    """
    return f"'{kind.value}'"


def _collect_role_steps(
    protocol: Protocol,
) -> dict[str, list[tuple[ProtocolStep, Optional[str]]]]:
    """Collect all steps where each role is the SENDER.

    Returns a dict mapping role -> list of (step, branch_name).
    """
    role_steps: dict[str, list[tuple[ProtocolStep, Optional[str]]]] = {
        r: [] for r in protocol.roles
    }

    def _collect(elements: Sequence[ProtocolElement], branch: Optional[str]) -> None:
        for elem in elements:
            if isinstance(elem, ProtocolStep):
                role_steps[elem.sender].append((elem, branch))
            elif isinstance(elem, ProtocolChoice):
                for branch_name, branch_elems in elem.branches.items():
                    _collect(branch_elems, branch_name)

    _collect(protocol.elements, None)
    return role_steps


def _has_choices(protocol: Protocol) -> bool:
    """Check if a protocol contains any ProtocolChoice elements."""
    return any(isinstance(e, ProtocolChoice) for e in protocol.elements)


def _collect_choices(
    elements: Sequence[ProtocolElement],
) -> list[ProtocolChoice]:
    """Collect all ProtocolChoice elements (including nested)."""
    choices: list[ProtocolChoice] = []
    for elem in elements:
        if isinstance(elem, ProtocolChoice):
            choices.append(elem)
            for branch_elems in elem.branches.values():
                choices.extend(_collect_choices(branch_elems))
    return choices


def _property_display(prop: PropertySpec) -> str:
    """Format a PropertySpec for JSDoc display.

    Example: PropertySpec(ALWAYS_TERMINATES) -> "always_terminates"
    Example: PropertySpec(ORDERING, ("task_request", "task_result")) -> "ordering(task_request, task_result)"
    """
    if prop.params:
        return f"{prop.kind.value}({', '.join(prop.params)})"
    return prop.kind.value


# ============================================================
# TypeScript Code Generator
# ============================================================


class TypeScriptGenerator:
    """Generates TypeScript code from Protocol definitions.

    Pure string generation.  No eval(), no side effects.
    The generated code is a complete, self-contained TypeScript module.
    """

    def generate(
        self,
        protocol: Protocol,
        properties: ProtocolSpec | None = None,
    ) -> str:
        """Generate a complete TypeScript module for a protocol.

        Args:
            protocol: The protocol definition.
            properties: Optional verified properties for JSDoc annotations.

        Returns:
            Complete TypeScript source as a string.
        """
        sections = [
            self._generate_header(protocol, properties),
            self._generate_message_kind_type(protocol),
            self._generate_message_interfaces(protocol),
            self._generate_message_union(protocol),
            self._generate_role_interfaces(protocol),
            self._generate_choice_types(protocol),
            self._generate_session_class(protocol, properties),
        ]
        return "\n".join(s for s in sections if s)

    # -- Header -------------------------------------------------------

    def _generate_header(
        self,
        protocol: Protocol,
        properties: ProtocolSpec | None,
    ) -> str:
        """Generate the file header comment."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        lines = [
            "// Auto-generated by Lingua Universale",
            f"// Protocol: {protocol.name}",
            f"// Generated: {timestamp}",
        ]
        if properties:
            prop_names = ", ".join(p.kind.value for p in properties.properties)
            lines.append(f"// Verified properties: {prop_names}")
        lines.append("// DO NOT EDIT - regenerate from .lu source.")
        lines.append("")
        return "\n".join(lines)

    # -- MessageKind type ---------------------------------------------

    def _generate_message_kind_type(self, protocol: Protocol) -> str:
        """Generate the MessageKind string literal union type."""
        kinds = _used_message_kinds(protocol)
        if not kinds:
            return ""
        literals = " | ".join(_kind_to_literal(k) for k in kinds)
        return (
            "/** Message kinds used in this protocol. */\n"
            f"export type MessageKind = {literals};\n"
        )

    # -- Message interfaces -------------------------------------------

    def _generate_message_interfaces(self, protocol: Protocol) -> str:
        """Generate discriminated union interfaces for each MessageKind."""
        kinds = _used_message_kinds(protocol)
        if not kinds:
            return ""
        parts: list[str] = []
        for kind in kinds:
            iface_name = _kind_to_interface_name(kind)
            parts.append(
                f"/** Message: {kind.value} */\n"
                f"export interface {iface_name} {{\n"
                f"  readonly kind: {_kind_to_literal(kind)};\n"
                f"  readonly payload?: unknown;\n"
                f"}}\n"
            )
        return "\n".join(parts)

    # -- ProtocolMessage union ----------------------------------------

    def _generate_message_union(self, protocol: Protocol) -> str:
        """Generate the union of all message interfaces."""
        kinds = _used_message_kinds(protocol)
        if not kinds:
            return ""
        iface_names = " | ".join(_kind_to_interface_name(k) for k in kinds)
        return (
            "/** Union of all messages in this protocol. */\n"
            f"export type ProtocolMessage = {iface_names};\n"
        )

    # -- Role interfaces ----------------------------------------------

    def _generate_role_interfaces(self, protocol: Protocol) -> str:
        """Generate an interface for each role with send methods."""
        role_steps = _collect_role_steps(protocol)
        parts: list[str] = []

        for role in protocol.roles:
            safe_role = _safe_ts_ident(role)
            iface_name = f"{_to_pascal_case(safe_role)}Role"
            steps = role_steps.get(role, [])

            # Collect unique send methods
            seen_methods: set[str] = set()
            method_lines: list[str] = []
            for step, _branch in steps:
                method_name = f"send{_to_pascal_case(step.message_kind.value)}"
                method_key = f"{method_name}_{step.receiver}"
                if method_key in seen_methods:
                    continue
                seen_methods.add(method_key)

                msg_iface = _kind_to_interface_name(step.message_kind)
                method_lines.append(
                    f"  /** Send {step.message_kind.value} to {step.receiver}. */\n"
                    f"  {method_name}(msg: {msg_iface}): void;"
                )

            lines = [f"/** Role: {role} */"]
            lines.append(f"export interface {iface_name} {{")
            if method_lines:
                lines.extend(method_lines)
            else:
                lines.append(
                    "  // This role only receives messages in this protocol."
                )
            lines.append("}")
            parts.append("\n".join(lines) + "\n")

        return "\n".join(parts)

    # -- Choice types -------------------------------------------------

    def _generate_choice_types(self, protocol: Protocol) -> str:
        """Generate union types for ProtocolChoice branches."""
        choices = _collect_choices(protocol.elements)
        if not choices:
            return ""

        parts: list[str] = []
        # Deduplicate by (decider, branch_names) to handle same decider
        # with different branch sets, and different deciders
        seen: set[tuple[str, frozenset[str]]] = set()
        type_counter: dict[str, int] = {}

        for choice in choices:
            branch_set = frozenset(choice.branches.keys())
            key = (choice.decider, branch_set)
            if key in seen:
                continue
            seen.add(key)

            # Handle multiple choices from same decider with different branches
            base_name = _to_pascal_case(choice.decider)
            count = type_counter.get(choice.decider, 0)
            type_counter[choice.decider] = count + 1
            type_name = f"{base_name}Decision" if count == 0 else f"{base_name}Decision{count + 1}"

            branches = " | ".join(
                f"'{_escape_ts_string(b)}'" for b in choice.branches
            )
            parts.append(
                f"/** Choice branches for {choice.decider}'s decision. */\n"
                f"export type {type_name} = {branches};\n"
            )

        return "\n".join(parts)

    # -- Session class ------------------------------------------------

    def _generate_session_class(
        self,
        protocol: Protocol,
        properties: ProtocolSpec | None,
    ) -> str:
        """Generate the ProtocolSession class."""
        class_name = f"{protocol.name}Session"
        lines: list[str] = []
        has_choice = _has_choices(protocol)

        self._emit_session_jsdoc(lines, protocol, properties)
        lines.append(f"export class {class_name} {{")
        self._emit_session_fields(lines, protocol, has_choice)
        self._emit_session_constructor(lines, protocol, has_choice)
        self._emit_session_send(lines, protocol, has_choice)
        self._emit_session_choose_branch(lines, protocol, has_choice)
        self._emit_session_accessors(lines, protocol)
        lines.append("}")
        lines.append("")
        return "\n".join(lines)

    def _emit_session_jsdoc(self, lines, protocol, properties):
        lines.append("/**")
        lines.append(f" * Runtime-enforced session for {protocol.name}.")
        if protocol.description:
            lines.append(f" * {protocol.description}")
        if properties:
            lines.append(" *")
            for prop in properties.properties:
                lines.append(f" * @verified {_property_display(prop)}")
        lines.append(" */")

    def _emit_session_fields(self, lines, protocol, has_choice):
        lines.append("  private readonly _protocol: string;")
        for role in protocol.roles:
            safe_role = _safe_ts_ident(role)
            lines.append(f"  private readonly _{safe_role}: {_to_pascal_case(safe_role)}Role;")
        lines.append("  private _step: number;")
        lines.append("  private _complete: boolean;")
        if has_choice:
            lines.append("  private _branch: string | null;")
        lines.append("")

    def _emit_session_constructor(self, lines, protocol, has_choice):
        lines.append("  constructor() {")
        lines.append(f"    this._protocol = '{_escape_ts_string(protocol.name)}';")
        lines.append("    this._step = 0;")
        lines.append("    this._complete = false;")
        if has_choice:
            lines.append("    this._branch = null;")
        role_steps = _collect_role_steps(protocol)
        for role in protocol.roles:
            safe_role = _safe_ts_ident(role)
            steps = role_steps.get(role, [])
            escaped_role = _escape_ts_string(role)
            lines.append(f"    this._{safe_role} = {{")
            seen_methods: set[str] = set()
            for step, _branch in steps:
                method_name = f"send{_to_pascal_case(step.message_kind.value)}"
                method_key = f"{method_name}_{step.receiver}"
                if method_key in seen_methods:
                    continue
                seen_methods.add(method_key)
                escaped_receiver = _escape_ts_string(step.receiver)
                lines.append(
                    f"      {method_name}: (msg: ProtocolMessage) => "
                    f"this.send('{escaped_role}', '{escaped_receiver}', msg),"
                )
            lines.append(f"    }} as {_to_pascal_case(safe_role)}Role;")
        lines.append("  }")
        lines.append("")

    def _emit_session_send(self, lines, protocol, has_choice):
        if has_choice:
            lines.extend(["  /**", "   * Send a message from sender to receiver.", "   *",
                          "   * Note: Completion detection is simplified for protocols with choices.",
                          "   * It uses the shortest possible path length. For precise tracking,",
                          "   * integrate with the LU Python runtime (SessionChecker).", "   */"])
        else:
            lines.append("  /** Send a message from sender to receiver. */")
        lines.append("  send(sender: string, receiver: string, msg: ProtocolMessage): void {")
        lines.append("    if (this._complete) {")
        lines.append("      throw new Error('Protocol session already complete');")
        lines.append("    }")
        lines.append("    this._step++;")

        flat_steps = sum(1 for e in protocol.elements if isinstance(e, ProtocolStep))
        completion_steps = self._calc_completion_steps(protocol, flat_steps, has_choice)
        lines.append(f"    if (this._step >= {completion_steps}) {{")
        lines.append("      this._complete = true;")
        lines.append("    }")
        lines.append("  }")
        lines.append("")

    def _calc_completion_steps(self, protocol, flat_steps, has_choice):
        if not has_choice:
            return flat_steps
        min_branch = float("inf")
        for elem in protocol.elements:
            if isinstance(elem, ProtocolChoice):
                for branch_elems in elem.branches.values():
                    count = len(_collect_all_steps(branch_elems))
                    if count < min_branch:
                        min_branch = count
        return flat_steps + (int(min_branch) if min_branch != float("inf") else 0)

    def _emit_session_choose_branch(self, lines, protocol, has_choice):
        if not has_choice:
            return
        choices = _collect_choices(protocol.elements)
        if not choices:
            return
        seen_types: set[str] = set()
        type_counter: dict[str, int] = {}
        all_type_names: list[str] = []
        seen_keys: set[tuple[str, frozenset[str]]] = set()
        for choice in choices:
            branch_set = frozenset(choice.branches.keys())
            key = (choice.decider, branch_set)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            base = _to_pascal_case(choice.decider)
            count = type_counter.get(choice.decider, 0)
            type_counter[choice.decider] = count + 1
            tn = f"{base}Decision" if count == 0 else f"{base}Decision{count + 1}"
            if tn not in seen_types:
                seen_types.add(tn)
                all_type_names.append(tn)
        union_type = " | ".join(all_type_names) if len(all_type_names) > 1 else all_type_names[0]
        lines.append("  /** Choose a branch at a decision point. */")
        lines.append(f"  chooseBranch(branch: {union_type}): void {{")
        lines.append("    this._branch = branch;")
        lines.append("  }")
        lines.append("")

    def _emit_session_accessors(self, lines, protocol):
        lines.append("  /** True when the protocol session has completed. */")
        lines.append("  get isComplete(): boolean {")
        lines.append("    return this._complete;")
        lines.append("  }")
        lines.append("")
        for role in protocol.roles:
            safe_role = _safe_ts_ident(role)
            iface_name = f"{_to_pascal_case(safe_role)}Role"
            lines.append(f"  /** Access the {role} role interface. */")
            lines.append(f"  get {safe_role}(): {iface_name} {{")
            lines.append(f"    return this._{safe_role};")
            lines.append("  }")
            lines.append("")


# ============================================================
# Convenience function
# ============================================================


def generate_typescript(
    protocol: Protocol,
    properties: ProtocolSpec | None = None,
) -> str:
    """Generate a complete TypeScript module for a protocol.

    Convenience wrapper around ``TypeScriptGenerator().generate()``.
    """
    return TypeScriptGenerator().generate(protocol, properties=properties)
