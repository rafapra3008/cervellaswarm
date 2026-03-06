# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Python code generation from verified protocol definitions.

Generates type-safe Python code from Protocol definitions. The generated
code uses SessionChecker for runtime protocol enforcement, creating a
complete pipeline::

    Protocol (DSL or Python)
        |
    PythonGenerator  -->  Python source code
        |
    exec() / save   -->  Working module with runtime enforcement

The generated code includes:
- Typed role classes with ``send_*`` methods per protocol step
- A ``ProtocolSession`` class wrapping ``SessionChecker``
- Proper imports from ``cervellaswarm_lingua_universale``
- Full type hints for IDE support

This completes the CervellaSwarm verification pipeline:
    specify  ->  verify (Lean 4)  ->  GENERATE (this module)  ->  run

Architecture follows ``lean4_bridge.py`` (template-based, pure string
generation).  ZERO external dependencies.
"""

from __future__ import annotations

import keyword
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Sequence

from .protocols import Protocol, ProtocolChoice, ProtocolElement, ProtocolStep
from .types import MessageKind


# ============================================================
# Result types (frozen dataclasses)
# ============================================================


@dataclass(frozen=True)
class GeneratedCode:
    """Result of Python code generation for a protocol.

    Contains the generated source code and metadata about
    what was generated.
    """

    protocol_name: str
    source: str
    roles_generated: tuple[str, ...]
    methods_generated: tuple[str, ...]
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        if not self.protocol_name:
            raise ValueError("protocol_name cannot be empty")
        if not self.source:
            raise ValueError("source cannot be empty")

    @property
    def line_count(self) -> int:
        """Number of lines in the generated source."""
        return len(self.source.splitlines())


# ============================================================
# Helpers
# ============================================================


def _safe_python_ident(name: str) -> str:
    """Sanitize a string into a valid Python identifier.

    Replaces non-alphanumeric characters with ``_``.
    Prefixes with ``_`` if the result starts with a digit or is a keyword.
    Raises ``ValueError`` if the input is empty.
    """
    if not name:
        raise ValueError("cannot create Python identifier from empty string")
    result = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if result[0].isdigit():
        result = f"_{result}"
    if keyword.iskeyword(result) or keyword.issoftkeyword(result):
        result = f"{result}_"
    return result


def _escape_string(s: str) -> str:
    """Escape a string for safe embedding in generated Python source.

    Handles backslash, double quotes, newlines, and carriage returns.
    """
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )


def _validate_protocol_name(name: str) -> None:
    """Validate that a protocol name can be used as a Python constant.

    The name is upper-cased for use as a module-level constant
    (e.g., ``DelegateTask`` -> ``DELEGATETASK``), so it must be
    sanitizable to a valid Python identifier.

    Raises ``ValueError`` if the name is empty or cannot be sanitized.
    """
    if not name:
        raise ValueError("protocol name cannot be empty")
    sanitized = _safe_python_ident(name.upper())
    if not sanitized.isidentifier():
        raise ValueError(
            f"protocol name '{name}' cannot be used as a Python identifier"
        )


def _to_class_name(role: str) -> str:
    """Convert a role name to PascalCase class name.

    Examples: "regina" -> "Regina", "guardiana" -> "Guardiana",
    "worker" -> "Worker", "my_role" -> "MyRole"
    """
    safe = _safe_python_ident(role)
    parts = safe.split("_")
    return "".join(p.capitalize() for p in parts if p)


def _to_method_name(kind: MessageKind) -> str:
    """Convert a MessageKind to a send method name.

    Example: MessageKind.TASK_REQUEST -> "send_task_request"
    """
    return f"send_{kind.value}"


def _collect_role_steps(
    protocol: Protocol,
) -> dict[str, list[tuple[ProtocolStep, Optional[str]]]]:
    """Collect all steps where each role is the SENDER.

    Returns a dict mapping role -> list of (step, branch_name).
    branch_name is None for flat steps, or the branch name for choice steps.
    """
    role_steps: dict[str, list[tuple[ProtocolStep, Optional[str]]]] = {
        r: [] for r in protocol.roles
    }

    for elem in protocol.elements:
        if isinstance(elem, ProtocolStep):
            role_steps[elem.sender].append((elem, None))
        elif isinstance(elem, ProtocolChoice):
            for branch_name, steps in elem.branches.items():
                for step in steps:
                    role_steps[step.sender].append((step, branch_name))

    return role_steps


def _collect_all_steps(
    elements: Sequence[ProtocolElement],
) -> list[ProtocolStep]:
    """Collect all ProtocolSteps from elements, including choice branches."""
    steps: list[ProtocolStep] = []
    for elem in elements:
        if isinstance(elem, ProtocolStep):
            steps.append(elem)
        elif isinstance(elem, ProtocolChoice):
            for branch_steps in elem.branches.values():
                steps.extend(branch_steps)
    return steps


def _used_message_kinds(protocol: Protocol) -> list[MessageKind]:
    """Collect MessageKinds used in a protocol (preserving enum order)."""
    used: set[MessageKind] = set()
    for step in _collect_all_steps(protocol.elements):
        used.add(step.message_kind)
    return [k for k in MessageKind if k in used]


def _has_choices(protocol: Protocol) -> bool:
    """Check if a protocol contains any ProtocolChoice elements."""
    return any(isinstance(e, ProtocolChoice) for e in protocol.elements)


# ============================================================
# Python Code Generator
# ============================================================


class PythonGenerator:
    """Generates Python code from Protocol definitions.

    Pure string generation.  No exec(), no eval(), no side effects.
    The generated code is a complete, self-contained Python module.
    """

    _HEADER = (
        '"""Auto-generated by CervellaSwarm Code Generation Layer.\n'
        "\n"
        "Protocol: {name}\n"
        "Generated: {timestamp}\n"
        "DO NOT EDIT - regenerate from Python source.\n"
        '"""\n'
    )

    def generate_header(self, protocol: Protocol) -> str:
        """Generate the module docstring header."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        return self._HEADER.format(name=protocol.name, timestamp=timestamp)

    def generate_imports(self, protocol: Protocol) -> str:
        """Generate the import block for the generated module.

        Only imports the types actually used by this protocol.
        """
        lines = [
            "from __future__ import annotations",
            "",
            "from typing import Optional",
            "",
            "from cervellaswarm_lingua_universale.types import (",
        ]

        # Always import MessageKind
        kinds = _used_message_kinds(protocol)
        lines.append("    MessageKind,")

        # Import message dataclasses for the used kinds
        kind_to_class = _kind_to_message_class()
        classes_needed: list[str] = []
        for kind in kinds:
            cls_name = kind_to_class.get(kind)
            if cls_name and cls_name not in classes_needed:
                classes_needed.append(cls_name)
        for cls_name in sorted(classes_needed):
            lines.append(f"    {cls_name},")
        lines.append("    message_kind,")
        lines.append(")")

        lines.extend([
            "from cervellaswarm_lingua_universale.protocols import (",
            "    Protocol,",
            "    ProtocolChoice,",
            "    ProtocolStep,",
            ")",
            "from cervellaswarm_lingua_universale.checker import (",
            "    SessionChecker,",
            "    ProtocolViolation,",
            "    SessionComplete,",
            ")",
        ])

        return "\n".join(lines) + "\n"

    def generate_protocol_definition(self, protocol: Protocol) -> str:
        """Generate the Protocol constant definition.

        Embeds the full protocol definition so the generated module
        is self-contained.
        """
        lines = [
            "",
            f"# {'=' * 60}",
            f"# Protocol: {protocol.name}",
            f"# {'=' * 60}",
            "",
        ]

        # Generate the elements
        elem_lines = self._render_elements(protocol.elements)

        lines.append(f"{protocol.name.upper()} = Protocol(")
        lines.append(f'    name="{protocol.name}",')
        roles_str = ", ".join(f'"{r}"' for r in protocol.roles)
        lines.append(f"    roles=({roles_str},),")
        if protocol.description:
            desc_escaped = _escape_string(protocol.description)
            lines.append(f'    description="{desc_escaped}",')
        lines.append(f"    max_repetitions={protocol.max_repetitions},")
        lines.append("    elements=(")
        lines.extend(elem_lines)
        lines.append("    ),")
        lines.append(")")

        return "\n".join(lines) + "\n"

    def _render_elements(
        self, elements: Sequence[ProtocolElement], indent: int = 8,
    ) -> list[str]:
        """Render protocol elements as Python source lines."""
        pad = " " * indent
        lines: list[str] = []

        for elem in elements:
            if isinstance(elem, ProtocolStep):
                lines.append(f"{pad}ProtocolStep(")
                lines.append(f'{pad}    sender="{elem.sender}",')
                lines.append(f'{pad}    receiver="{elem.receiver}",')
                lines.append(f"{pad}    message_kind=MessageKind.{elem.message_kind.name},")
                if elem.description:
                    desc = _escape_string(elem.description)
                    lines.append(f'{pad}    description="{desc}",')
                lines.append(f"{pad}),")
            elif isinstance(elem, ProtocolChoice):
                lines.append(f"{pad}ProtocolChoice(")
                lines.append(f'{pad}    decider="{elem.decider}",')
                if elem.description:
                    desc = _escape_string(elem.description)
                    lines.append(f'{pad}    description="{desc}",')
                lines.append(f"{pad}    branches={{")
                for branch_name, branch_steps in elem.branches.items():
                    lines.append(f'{pad}        "{branch_name}": (')
                    for step in branch_steps:
                        lines.append(f"{pad}            ProtocolStep(")
                        lines.append(f'{pad}                sender="{step.sender}",')
                        lines.append(f'{pad}                receiver="{step.receiver}",')
                        lines.append(
                            f"{pad}                message_kind=MessageKind.{step.message_kind.name},"
                        )
                        if step.description:
                            sd = _escape_string(step.description)
                            lines.append(f'{pad}                description="{sd}",')
                        lines.append(f"{pad}            ),")
                    lines.append(f"{pad}        ),")
                lines.append(f"{pad}    }},")
                lines.append(f"{pad}),")

        return lines

    def generate_role_classes(self, protocol: Protocol) -> str:
        """Generate a typed class for each role with send_* methods.

        Each role gets a class with methods for every message it can send
        in the protocol.  The methods call through to the session's
        ``SessionChecker.send()`` for runtime enforcement.
        """
        role_steps = _collect_role_steps(protocol)
        parts: list[str] = []

        for role in protocol.roles:
            class_name = _to_class_name(role)
            steps = role_steps.get(role, [])

            lines = [
                "",
                f"class {class_name}Role:",
                f'    """Typed role wrapper for \\"{role}\\" in {protocol.name}.',
                "",
                f"    Provides send_* methods for every message this role can send.",
                '    Each method validates the message via SessionChecker."""',
                "",
                "    def __init__(self, session: ProtocolSession) -> None:",
                "        self._session = session",
                f'        self._role = "{role}"',
            ]

            # Deduplicate methods (same message_kind + receiver)
            seen_methods: set[str] = set()
            for step, branch_name in steps:
                method_name = _to_method_name(step.message_kind)
                method_key = f"{method_name}_{step.receiver}"

                if method_key in seen_methods:
                    continue
                seen_methods.add(method_key)

                cls_name = _kind_to_message_class().get(step.message_kind)
                type_hint = cls_name if cls_name else "object"

                lines.extend([
                    "",
                    f"    def {method_name}(",
                    f"        self, msg: {type_hint},",
                    f"    ) -> None:",
                    f'        """Send {step.message_kind.value} to {step.receiver}."""',
                    f'        self._session.send(self._role, "{step.receiver}", msg)',
                ])

            # If role has no send methods, add a docstring-only note
            if not steps:
                lines.extend([
                    "",
                    "    # This role only receives messages in this protocol.",
                ])

            parts.append("\n".join(lines) + "\n")

        return "\n".join(parts)

    def generate_session_class(self, protocol: Protocol) -> str:
        """Generate the ProtocolSession class.

        Wraps SessionChecker and provides typed role accessors.
        """
        init_lines: list[str] = []
        property_lines: list[str] = []

        for role in protocol.roles:
            class_name = _to_class_name(role)
            attr_name = _safe_python_ident(role)

            init_lines.append(f"        self._{attr_name} = {class_name}Role(self)")
            property_lines.extend([
                "",
                "    @property",
                f"    def {attr_name}(self) -> {class_name}Role:",
                f'        """Access the {role} role interface."""',
                f"        return self._{attr_name}",
            ])

        lines = [
            "",
            f"class ProtocolSession:",
            f'    """Runtime-enforced session for {protocol.name}.',
            "",
            "    Wraps SessionChecker to provide typed role accessors",
            '    and runtime protocol enforcement."""',
            "",
            "    def __init__(",
            "        self,",
            '        session_id: str = "",',
            "        role_bindings: Optional[dict[str, str]] = None,",
            "    ) -> None:",
            f"        self._checker = SessionChecker(",
            f"            protocol={protocol.name.upper()},",
            f"            session_id=session_id,",
            f"            role_bindings=role_bindings,",
            f"        )",
        ]
        lines.extend(init_lines)

        # send() method
        lines.extend([
            "",
            "    def send(self, sender: str, receiver: str, msg: object) -> None:",
            '        """Send a message through the session checker."""',
            "        self._checker.send(sender, receiver, msg)",
        ])

        # choose_branch() for protocols with choices
        if _has_choices(protocol):
            lines.extend([
                "",
                "    def choose_branch(self, branch_name: str) -> None:",
                '        """Choose a branch at a choice point."""',
                "        self._checker.choose_branch(branch_name)",
            ])

        # Properties
        lines.extend([
            "",
            "    @property",
            "    def is_complete(self) -> bool:",
            '        """True when the protocol session has completed."""',
            "        return self._checker.is_complete",
            "",
            "    @property",
            "    def session_id(self) -> str:",
            '        """The session identifier."""',
            "        return self._checker.session_id",
            "",
            "    @property",
            "    def checker(self) -> SessionChecker:",
            '        """Access the underlying SessionChecker."""',
            "        return self._checker",
        ])

        lines.extend(property_lines)

        return "\n".join(lines) + "\n"

    def generate(self, protocol: Protocol) -> str:
        """Generate a complete Python module for a protocol.

        The module is self-contained: includes imports, protocol definition,
        role classes, and a ProtocolSession class.

        Raises ``ValueError`` if the protocol name is not a valid Python identifier
        (after sanitization for use as a constant).
        """
        _validate_protocol_name(protocol.name)
        sections = [
            self.generate_header(protocol),
            self.generate_imports(protocol),
            self.generate_protocol_definition(protocol),
            self.generate_role_classes(protocol),
            self.generate_session_class(protocol),
        ]

        return "\n".join(sections)


# ============================================================
# MessageKind -> Message dataclass mapping
# ============================================================


_KIND_TO_CLASS: dict[MessageKind, str] | None = None


def _kind_to_message_class() -> dict[MessageKind, str]:
    """Map each MessageKind to its corresponding dataclass name.

    Cached after first call for performance.
    """
    global _KIND_TO_CLASS  # noqa: PLW0603
    if _KIND_TO_CLASS is not None:
        return _KIND_TO_CLASS
    _KIND_TO_CLASS = {
        MessageKind.TASK_REQUEST: "TaskRequest",
        MessageKind.TASK_RESULT: "TaskResult",
        MessageKind.AUDIT_REQUEST: "AuditRequest",
        MessageKind.AUDIT_VERDICT: "AuditVerdict",
        MessageKind.PLAN_REQUEST: "PlanRequest",
        MessageKind.PLAN_PROPOSAL: "PlanProposal",
        MessageKind.PLAN_DECISION: "PlanDecision",
        MessageKind.RESEARCH_QUERY: "ResearchQuery",
        MessageKind.RESEARCH_REPORT: "ResearchReport",
        MessageKind.DM: "DirectMessage",
        MessageKind.BROADCAST: "Broadcast",
        MessageKind.SHUTDOWN_REQUEST: "ShutdownRequest",
        MessageKind.SHUTDOWN_ACK: "ShutdownAck",
        MessageKind.CONTEXT_INJECT: "ContextInject",
    }
    return _KIND_TO_CLASS


# ============================================================
# Convenience functions
# ============================================================


def generate_python(protocol: Protocol) -> str:
    """Generate a complete Python module for a protocol.

    Convenience wrapper around ``PythonGenerator().generate(protocol)``.

    Example::

        from cervellaswarm_lingua_universale import DelegateTask
        from cervellaswarm_lingua_universale.codegen import generate_python

        code = generate_python(DelegateTask)
        print(code)  # Complete Python module with typed roles
    """
    return PythonGenerator().generate(protocol)


def _generate_multi_imports(
    protocols: Sequence[Protocol],
    kind_to_class: dict[MessageKind, str],
) -> list[str]:
    """Generate shared import block for multi-protocol module."""
    all_kinds: set[MessageKind] = set()
    for p in protocols:
        all_kinds.update(_used_message_kinds(p))

    classes_needed: list[str] = []
    for kind in sorted(all_kinds, key=lambda k: k.value):
        cls_name = kind_to_class.get(kind)
        if cls_name and cls_name not in classes_needed:
            classes_needed.append(cls_name)

    lines = [
        "from __future__ import annotations",
        "",
        "from typing import Optional",
        "",
        "from cervellaswarm_lingua_universale.types import (",
        "    MessageKind,",
    ]
    for cls_name in sorted(classes_needed):
        lines.append(f"    {cls_name},")
    lines.extend([
        "    message_kind,",
        ")",
        "from cervellaswarm_lingua_universale.protocols import (",
        "    Protocol,",
        "    ProtocolChoice,",
        "    ProtocolStep,",
        ")",
        "from cervellaswarm_lingua_universale.checker import (",
        "    SessionChecker,",
        "    ProtocolViolation,",
        "    SessionComplete,",
        ")",
    ])
    return lines


def _generate_multi_role_class(
    protocol: Protocol,
    role: str,
    steps: list[tuple[ProtocolStep, "str | None"]],
    kind_to_class: dict[MessageKind, str],
) -> str:
    """Generate a single Role class for a multi-protocol module."""
    class_name = f"{protocol.name}{_to_class_name(role)}Role"
    role_lines = [
        "",
        f"class {class_name}:",
        f'    """Typed role for \\"{role}\\" in {protocol.name}."""',
        "",
        f"    def __init__(self, session: {protocol.name}Session) -> None:",
        "        self._session = session",
        f'        self._role = "{role}"',
    ]

    seen_methods: set[str] = set()
    for step, branch_name in steps:
        method_name = _to_method_name(step.message_kind)
        method_key = f"{method_name}_{step.receiver}"
        if method_key in seen_methods:
            continue
        seen_methods.add(method_key)

        cls_name = kind_to_class.get(step.message_kind)
        type_hint = cls_name if cls_name else "object"
        role_lines.extend([
            "",
            f"    def {method_name}(self, msg: {type_hint}) -> None:",
            f'        """Send {step.message_kind.value} to {step.receiver}."""',
            f'        self._session.send(self._role, "{step.receiver}", msg)',
        ])

    if not steps:
        role_lines.append("")
        role_lines.append("    # This role only receives messages.")

    return "\n".join(role_lines) + "\n"


def _generate_multi_session_class(protocol: Protocol) -> str:
    """Generate a Session class for a multi-protocol module."""
    session_lines = [
        "",
        f"class {protocol.name}Session:",
        f'    """Runtime-enforced session for {protocol.name}."""',
        "",
        "    def __init__(",
        "        self,",
        '        session_id: str = "",',
        "        role_bindings: Optional[dict[str, str]] = None,",
        "    ) -> None:",
        f"        self._checker = SessionChecker(",
        f"            protocol={protocol.name.upper()},",
        f"            session_id=session_id,",
        f"            role_bindings=role_bindings,",
        f"        )",
    ]

    for role in protocol.roles:
        attr_name = _safe_python_ident(role)
        class_name = f"{protocol.name}{_to_class_name(role)}Role"
        session_lines.append(f"        self._{attr_name} = {class_name}(self)")

    session_lines.extend([
        "",
        "    def send(self, sender: str, receiver: str, msg: object) -> None:",
        '        """Send a message through the session checker."""',
        "        self._checker.send(sender, receiver, msg)",
    ])

    if _has_choices(protocol):
        session_lines.extend([
            "",
            "    def choose_branch(self, branch_name: str) -> None:",
            '        """Choose a branch at a choice point."""',
            "        self._checker.choose_branch(branch_name)",
        ])

    session_lines.extend([
        "",
        "    @property",
        "    def is_complete(self) -> bool:",
        "        return self._checker.is_complete",
        "",
        "    @property",
        "    def session_id(self) -> str:",
        "        return self._checker.session_id",
    ])

    for role in protocol.roles:
        attr_name = _safe_python_ident(role)
        class_name = f"{protocol.name}{_to_class_name(role)}Role"
        session_lines.extend([
            "",
            "    @property",
            f"    def {attr_name}(self) -> {class_name}:",
            f"        return self._{attr_name}",
        ])

    return "\n".join(session_lines) + "\n"


def generate_python_multi(protocols: Sequence[Protocol]) -> str:
    """Generate a single Python module containing multiple protocols.

    Each protocol gets its own set of role classes and session class,
    with the session class named ``{ProtocolName}Session``.
    """
    if not protocols:
        raise ValueError("protocols cannot be empty")

    names = [p.name for p in protocols]
    if len(set(names)) != len(names):
        dupes = [n for n in names if names.count(n) > 1]
        raise ValueError(f"duplicate protocol names: {sorted(set(dupes))}")

    generator = PythonGenerator()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    kind_to_class = _kind_to_message_class()

    parts: list[str] = [
        '"""Auto-generated by CervellaSwarm Code Generation Layer.',
        "",
        f"Protocols: {', '.join(p.name for p in protocols)}",
        f"Generated: {timestamp}",
        "DO NOT EDIT - regenerate from Python source.",
        '"""',
        "",
    ]

    parts.extend(_generate_multi_imports(protocols, kind_to_class))

    for protocol in protocols:
        parts.append(generator.generate_protocol_definition(protocol))

        role_steps = _collect_role_steps(protocol)
        for role in protocol.roles:
            steps = role_steps.get(role, [])
            parts.append(_generate_multi_role_class(
                protocol, role, steps, kind_to_class,
            ))

        parts.append(_generate_multi_session_class(protocol))

    return "\n".join(parts)
