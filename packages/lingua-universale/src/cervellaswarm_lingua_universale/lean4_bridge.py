# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Lean 4 Bridge - Formal verification of agent protocols.

Generates Lean 4 code from Protocol definitions and optionally
verifies it using the Lean 4 theorem prover.  This enables
mathematical proof of protocol properties such as:

- No self-loops (sender != receiver in every step)
- All participants are declared roles
- Non-empty protocol and branch structure
- Minimum role count

Architecture::

    Protocol (Python)
        |
    Lean4Generator  -->  .lean code string
        |
    Lean4Verifier   -->  VerificationResult  (optional, needs ``lean``)

The generator works WITHOUT Lean 4 installed (pure code generation).
The verifier requires Lean 4 on PATH (subprocess call, optional).

ZERO external dependencies.  Pure Python standard library.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Sequence

from ._codegen_common import collect_all_steps as _collect_all_steps
from ._codegen_common import used_message_kinds as _used_message_kinds
from .protocols import Protocol, ProtocolChoice, ProtocolElement
from .types import MessageKind


# ============================================================
# Enums
# ============================================================


class VerificationProperty(Enum):
    """Properties that can be formally verified for a protocol."""

    SENDERS_IN_ROLES = "senders_in_roles"
    RECEIVERS_IN_ROLES = "receivers_in_roles"
    NO_SELF_LOOP = "no_self_loop"
    MIN_ROLES = "min_roles"
    NON_EMPTY = "non_empty"
    BRANCHES_NON_EMPTY = "branches_non_empty"
    DECIDER_IN_ROLES = "decider_in_roles"


# Properties that only apply to protocols with ProtocolChoice
_CHOICE_ONLY_PROPERTIES = frozenset({
    VerificationProperty.BRANCHES_NON_EMPTY,
    VerificationProperty.DECIDER_IN_ROLES,
})

# All properties for flat protocols (no choices)
FLAT_PROPERTIES: tuple[VerificationProperty, ...] = (
    VerificationProperty.SENDERS_IN_ROLES,
    VerificationProperty.RECEIVERS_IN_ROLES,
    VerificationProperty.NO_SELF_LOOP,
    VerificationProperty.MIN_ROLES,
    VerificationProperty.NON_EMPTY,
)

# All properties including choice-specific ones
ALL_PROPERTIES: tuple[VerificationProperty, ...] = (
    *FLAT_PROPERTIES,
    VerificationProperty.BRANCHES_NON_EMPTY,
    VerificationProperty.DECIDER_IN_ROLES,
)


# ============================================================
# Result types (frozen dataclasses)
# ============================================================


@dataclass(frozen=True)
class VerificationResult:
    """Result of verifying a single property."""

    property_name: str
    proved: bool
    lean_theorem: str
    error: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.property_name:
            raise ValueError("property_name cannot be empty")
        if not self.lean_theorem:
            raise ValueError("lean_theorem cannot be empty")


@dataclass(frozen=True)
class VerificationReport:
    """Full verification report for a protocol."""

    protocol_name: str
    results: tuple[VerificationResult, ...]
    lean_code: str
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def all_proved(self) -> bool:
        """True if every property was proved."""
        return len(self.results) > 0 and all(r.proved for r in self.results)

    @property
    def proved_count(self) -> int:
        """Number of proved properties."""
        return sum(1 for r in self.results if r.proved)

    @property
    def total_count(self) -> int:
        """Total number of properties checked."""
        return len(self.results)

    def __post_init__(self) -> None:
        if not self.protocol_name:
            raise ValueError("protocol_name cannot be empty")
        if not self.lean_code:
            raise ValueError("lean_code cannot be empty")


# ============================================================
# Lean 4 Code Generator
# ============================================================


_LEAN_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _lean_constructor(kind: MessageKind) -> str:
    """Convert a MessageKind to a Lean 4 constructor name."""
    return kind.value  # already snake_case: "task_request"


def _safe_lean_ident(name: str) -> str:
    """Sanitize a string into a valid Lean 4 identifier.

    Replaces any character that is not alphanumeric or underscore with ``_``.
    Prefixes with ``_`` if the result starts with a digit.
    Raises ``ValueError`` if the input is empty.
    """
    if not name:
        raise ValueError("cannot create Lean 4 identifier from empty string")
    result = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if result[0].isdigit():
        result = f"_{result}"
    return result


def _validate_lean_name(name: str) -> None:
    """Raise ValueError if *name* is not a valid Lean 4 identifier."""
    if not _LEAN_IDENT_RE.match(name):
        raise ValueError(
            f"'{name}' is not a valid Lean 4 identifier "
            f"(must match {_LEAN_IDENT_RE.pattern})"
        )


def _collect_choices(elements: Sequence[ProtocolElement]) -> list[ProtocolChoice]:
    """Collect all ProtocolChoice instances from elements."""
    return [e for e in elements if isinstance(e, ProtocolChoice)]


def _has_choices(protocol: Protocol) -> bool:
    """Check if a protocol contains any ProtocolChoice elements."""
    return any(isinstance(e, ProtocolChoice) for e in protocol.elements)


class Lean4Generator:
    """Generates Lean 4 code from Protocol definitions.

    Works WITHOUT Lean 4 installed.  Pure string generation.
    """

    # Header template
    _HEADER = (
        "-- Auto-generated by CervellaSwarm Lean 4 Bridge\n"
        "-- Protocol: {name}\n"
        "-- Generated: {timestamp}\n"
        "-- DO NOT EDIT - regenerate from Python source\n"
    )

    def generate_message_kind(self, kinds: Optional[Sequence[MessageKind]] = None) -> str:
        """Generate the MessageKind inductive type.

        If *kinds* is ``None``, all 14 standard kinds are included.
        """
        if kinds is None:
            kinds = list(MessageKind)
        constructors = "\n  | ".join(_lean_constructor(k) for k in kinds)
        return (
            "inductive MessageKind where\n"
            f"  | {constructors}\n"
            "  deriving DecidableEq, Repr, BEq\n"
        )

    def generate_step_structure(self) -> str:
        """Generate the ProtocolStep structure definition."""
        return (
            "structure ProtocolStep where\n"
            "  sender : String\n"
            "  receiver : String\n"
            "  message_kind : MessageKind\n"
            "  deriving Repr, BEq, DecidableEq\n"
        )

    def generate_roles(self, protocol: Protocol) -> str:
        """Generate the roles list for a protocol."""
        items = ", ".join(f'"{r}"' for r in protocol.roles)
        return (
            f"def {protocol.name}_roles : List String :=\n"
            f"  [{items}]\n"
        )

    def generate_steps(self, protocol: Protocol) -> str:
        """Generate all steps (flat list, including those inside choices)."""
        all_steps = _collect_all_steps(protocol.elements)
        if not all_steps:
            return f"def {protocol.name}_all_steps : List ProtocolStep := []\n"

        lines = [f"def {protocol.name}_all_steps : List ProtocolStep :="]
        for i, step in enumerate(all_steps):
            prefix = "  [ " if i == 0 else "  , "
            ctor = _lean_constructor(step.message_kind)
            lines.append(
                f'{prefix}{{ sender := "{step.sender}", '
                f'receiver := "{step.receiver}", '
                f"message_kind := .{ctor} }}"
            )
        lines.append("  ]")
        return "\n".join(lines) + "\n"

    @staticmethod
    def _branch_def_names(
        protocol_name: str, choices: list,
    ) -> dict[tuple[int, str], str]:
        """Compute de-duplicated Lean 4 definition names for all branches.

        Returns a mapping (choice_index, branch_name) -> def_name.
        Shared between generate_branches() and generate_theorems()
        so they always use the same names.
        """
        result: dict[tuple[int, str], str] = {}
        seen: set[str] = set()
        for ci, choice in enumerate(choices):
            for branch_name in choice.branches:
                safe_name = _safe_lean_ident(branch_name)
                def_name = f"{protocol_name}_branch_{safe_name}"
                if ci > 0:
                    def_name = f"{protocol_name}_choice{ci}_branch_{safe_name}"
                base_def_name = def_name
                suffix = 2
                while def_name in seen:
                    def_name = f"{base_def_name}_{suffix}"
                    suffix += 1
                seen.add(def_name)
                result[(ci, branch_name)] = def_name
        return result

    def generate_branches(self, protocol: Protocol) -> str:
        """Generate per-branch step lists for protocols with choices."""
        choices = _collect_choices(protocol.elements)
        if not choices:
            return ""

        name_map = self._branch_def_names(protocol.name, choices)
        parts: list[str] = []
        for ci, choice in enumerate(choices):
            for branch_name, branch_steps in choice.branches.items():
                def_name = name_map[(ci, branch_name)]

                lines = [f"def {def_name} : List ProtocolStep :="]
                for i, step in enumerate(branch_steps):
                    prefix = "  [ " if i == 0 else "  , "
                    ctor = _lean_constructor(step.message_kind)
                    lines.append(
                        f'{prefix}{{ sender := "{step.sender}", '
                        f'receiver := "{step.receiver}", '
                        f"message_kind := .{ctor} }}"
                    )
                lines.append("  ]")
                parts.append("\n".join(lines) + "\n")
        return "\n".join(parts)

    def generate_theorems(self, protocol: Protocol) -> str:
        """Generate standard theorems for the protocol."""
        name = protocol.name
        theorems: list[str] = []

        # T1: senders_valid
        theorems.append(
            f"theorem {name}_senders_valid :\n"
            f"    ∀ step ∈ {name}_all_steps, step.sender ∈ {name}_roles := by decide\n"
        )

        # T2: receivers_valid
        theorems.append(
            f"theorem {name}_receivers_valid :\n"
            f"    ∀ step ∈ {name}_all_steps, step.receiver ∈ {name}_roles := by decide\n"
        )

        # T3: no_self_loop
        theorems.append(
            f"theorem {name}_no_self_loop :\n"
            f"    ∀ step ∈ {name}_all_steps, step.sender ≠ step.receiver := by decide\n"
        )

        # T4: min_roles
        theorems.append(
            f"theorem {name}_min_roles :\n"
            f"    {name}_roles.length ≥ 2 := by decide\n"
        )

        # T5: non_empty
        theorems.append(
            f"theorem {name}_non_empty :\n"
            f"    {name}_all_steps.length > 0 := by decide\n"
        )

        # Choice-specific theorems
        choices = _collect_choices(protocol.elements)
        if choices:
            name_map = self._branch_def_names(name, choices)
            # T6: branches_non_empty
            for ci, choice in enumerate(choices):
                branch_checks: list[str] = []
                for branch_name in choice.branches:
                    def_name = name_map[(ci, branch_name)]
                    branch_checks.append(f"{def_name}.length > 0")

                conjunction = " ∧\n    ".join(branch_checks)
                suffix = "" if ci == 0 else f"_choice{ci}"
                theorems.append(
                    f"theorem {name}_branches_non_empty{suffix} :\n"
                    f"    {conjunction} := by decide\n"
                )

            # T7: decider_in_roles
            for ci, choice in enumerate(choices):
                suffix = "" if ci == 0 else f"_choice{ci}"
                theorems.append(
                    f'theorem {name}_decider_in_roles{suffix} :\n'
                    f'    "{choice.decider}" ∈ {name}_roles := by decide\n'
                )

        return "\n".join(theorems)

    def generate(self, protocol: Protocol) -> str:
        """Generate a complete Lean 4 file for a protocol.

        The file includes type definitions, protocol data, and theorems.
        It is self-contained and can be verified by ``lean --json``.

        Raises ``ValueError`` if the protocol name is not a valid Lean 4 identifier.
        """
        _validate_lean_name(protocol.name)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        header = self._HEADER.format(name=protocol.name, timestamp=timestamp)

        # Collect only the MessageKinds used in this protocol
        used_kinds = _used_message_kinds(protocol)

        sections = [
            header,
            "-- " + "=" * 60,
            "-- Types",
            "-- " + "=" * 60,
            "",
            self.generate_message_kind(used_kinds),
            "",
            self.generate_step_structure(),
            "",
            "-- " + "=" * 60,
            f"-- Protocol: {protocol.name}",
            "-- " + "=" * 60,
            "",
            self.generate_roles(protocol),
            "",
            self.generate_steps(protocol),
        ]

        branches = self.generate_branches(protocol)
        if branches:
            sections.extend(["", branches])

        sections.extend([
            "",
            "-- " + "=" * 60,
            "-- Theorems",
            "-- " + "=" * 60,
            "",
            self.generate_theorems(protocol),
        ])

        return "\n".join(sections)


# ============================================================
# Lean 4 Verifier (optional - needs lean on PATH)
# ============================================================


def lean4_available() -> bool:
    """Check if the Lean 4 binary is available on PATH."""
    return shutil.which("lean") is not None


class Lean4Verifier:
    """Verifies Lean 4 code using the ``lean`` binary.

    Requires Lean 4 installed and on PATH.
    Uses subprocess with a timeout (default 60s per file).

    If Lean 4 is not installed, ``verify`` raises ``RuntimeError``.
    """

    def __init__(self, timeout: int = 60) -> None:
        if timeout < 1:
            raise ValueError(f"timeout must be positive, got {timeout}")
        self._timeout = timeout

    def verify_code(self, lean_code: str) -> list[dict]:
        """Run ``lean --json`` on a code string and return raw messages.

        Returns a list of message dicts from Lean's JSON output.
        Each dict has at least ``severity`` and ``data`` keys.
        An empty list means the code compiled without errors.

        Raises ``RuntimeError`` if Lean 4 is not installed.
        Raises ``TimeoutError`` if verification exceeds the timeout.
        """
        if not lean4_available():
            raise RuntimeError(
                "Lean 4 is not installed or not on PATH. "
                "Install from https://leanprover.github.io/lean4/doc/setup.html"
            )

        with tempfile.NamedTemporaryFile(
            suffix=".lean", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write(lean_code)
            temp_path = Path(f.name)

        try:
            result = subprocess.run(
                ["lean", "--json", str(temp_path)],
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            # Lean outputs one JSON object per line
            messages: list[dict] = []
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
            return messages
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(
                f"Lean 4 verification timed out after {self._timeout}s"
            ) from exc
        finally:
            temp_path.unlink(missing_ok=True)

    def verify_protocol(
        self,
        protocol: Protocol,
        properties: Optional[Sequence[VerificationProperty]] = None,
    ) -> VerificationReport:
        """Generate Lean 4 code for a protocol and verify it.

        Parameters
        ----------
        protocol:
            The protocol to verify.
        properties:
            Which properties to verify.  ``None`` means all applicable
            properties (choice-specific ones only if the protocol has choices).

        Returns
        -------
        VerificationReport with per-property results.

        Raises ``RuntimeError`` if Lean 4 is not installed.
        """
        generator = Lean4Generator()
        lean_code = generator.generate(protocol)

        # Determine which properties to check
        if properties is None:
            if _has_choices(protocol):
                properties = ALL_PROPERTIES
            else:
                properties = FLAT_PROPERTIES

        # Filter out choice-only properties for flat protocols
        if not _has_choices(protocol):
            properties = tuple(
                p for p in properties if p not in _CHOICE_ONLY_PROPERTIES
            )

        # Verify the full file (all theorems at once)
        messages = self.verify_code(lean_code)
        errors = [m for m in messages if m.get("severity") == "error"]

        # Map errors to specific theorems by matching theorem names
        results: list[VerificationResult] = []
        for prop in properties:
            theorem_name = f"{protocol.name}_{prop.value}"
            # Extract the theorem line from generated code
            theorem_line = _extract_theorem(lean_code, theorem_name)

            # Check if any error mentions this theorem
            prop_errors = [
                e for e in errors
                if theorem_name in e.get("data", "")
                or theorem_name in str(e.get("pos", ""))
            ]

            if prop_errors:
                error_msg = "; ".join(e.get("data", "unknown") for e in prop_errors)
                results.append(VerificationResult(
                    property_name=prop.value,
                    proved=False,
                    lean_theorem=theorem_line,
                    error=error_msg,
                ))
            else:
                results.append(VerificationResult(
                    property_name=prop.value,
                    proved=not bool(errors),
                    lean_theorem=theorem_line,
                ))

        return VerificationReport(
            protocol_name=protocol.name,
            results=tuple(results),
            lean_code=lean_code,
        )


def _extract_theorem(lean_code: str, theorem_name: str) -> str:
    """Extract a theorem block from generated Lean code."""
    lines = lean_code.splitlines()
    collecting = False
    collected: list[str] = []
    for line in lines:
        if f"theorem {theorem_name}" in line:
            collecting = True
        if collecting:
            collected.append(line)
            if line.strip().endswith("by decide"):
                break
    return "\n".join(collected) if collected else f"-- theorem {theorem_name} not found"


# ============================================================
# Convenience functions
# ============================================================


def generate_lean4(protocol: Protocol) -> str:
    """Generate a complete Lean 4 file for a protocol.

    Convenience wrapper around ``Lean4Generator().generate(protocol)``.
    Works without Lean 4 installed.
    """
    return Lean4Generator().generate(protocol)


def generate_lean4_multi(protocols: Sequence[Protocol]) -> str:
    """Generate a single Lean 4 file containing multiple protocols.

    Shares the MessageKind and ProtocolStep definitions across all protocols.
    """
    if not protocols:
        raise ValueError("protocols cannot be empty")

    names = [p.name for p in protocols]
    if len(set(names)) != len(names):
        dupes = [n for n in names if names.count(n) > 1]
        raise ValueError(f"duplicate protocol names: {sorted(set(dupes))}")

    for p in protocols:
        _validate_lean_name(p.name)

    generator = Lean4Generator()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Collect all used message kinds across all protocols
    all_kinds: set[MessageKind] = set()
    for p in protocols:
        all_kinds.update(_used_message_kinds(p))
    sorted_kinds = [k for k in MessageKind if k in all_kinds]

    parts: list[str] = [
        "-- Auto-generated by CervellaSwarm Lean 4 Bridge",
        f"-- Protocols: {', '.join(p.name for p in protocols)}",
        f"-- Generated: {timestamp}",
        "-- DO NOT EDIT - regenerate from Python source",
        "",
        "-- " + "=" * 60,
        "-- Types (shared)",
        "-- " + "=" * 60,
        "",
        generator.generate_message_kind(sorted_kinds),
        "",
        generator.generate_step_structure(),
    ]

    for protocol in protocols:
        parts.extend([
            "",
            "-- " + "=" * 60,
            f"-- Protocol: {protocol.name}",
            "-- " + "=" * 60,
            "",
            generator.generate_roles(protocol),
            "",
            generator.generate_steps(protocol),
        ])
        branches = generator.generate_branches(protocol)
        if branches:
            parts.extend(["", branches])
        parts.extend([
            "",
            "-- Theorems",
            "",
            generator.generate_theorems(protocol),
        ])

    return "\n".join(parts)
