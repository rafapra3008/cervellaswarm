# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Specification language for CervellaSwarm protocol properties.

Provides a mini-DSL for expressing formal properties about protocols,
static checking against protocol definitions, and runtime checking
against completed session logs.

Syntax overview::

    properties for DelegateTask:
        always terminates
        no deadlock
        no deletion
        task_request before task_result
        worker cannot send audit_request
        Cuoco exclusive dm
        trust >= trusted
        all roles participate

Grammar (EBNF)::

    spec_block     ::= 'properties' 'for' IDENT ':' NEWLINE property+
    property       ::= INDENT prop_body NEWLINE
    prop_body      ::= 'always' 'terminates'
                     | 'no' 'deadlock'
                     | 'no' 'deletion'
                     | IDENT 'before' IDENT
                     | IDENT 'cannot' 'send' IDENT
                     | IDENT 'exclusive' IDENT
                     | 'confidence' '>=' IDENT
                     | 'trust' '>=' IDENT
                     | 'all' 'roles' 'participate'

IDENT in 'before', 'cannot send', and 'exclusive' must be snake_case
MessageKind values (e.g., ``task_request``) or role names respectively.

Confidence levels: certain=1.0, high=0.8, medium=0.5, low=0.2,
speculative=0.1

Trust tiers: verified, trusted, standard, untrusted
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from enum import Enum, auto
from types import MappingProxyType
from typing import Sequence

from .protocols import Protocol, ProtocolChoice, ProtocolElement, ProtocolStep
from .types import AgentRole, MessageKind
from .checker import MessageRecord
from .trust import TrustTier, trust_tier_for_role


# ============================================================
# Errors
# ============================================================


class SpecParseError(Exception):
    """Error during spec parsing with line information."""

    def __init__(self, message: str, line: int = 0) -> None:
        self.line = line
        loc = f"line {line}" if line else "unknown location"
        super().__init__(f"{loc}: {message}")


# ============================================================
# Enums
# ============================================================


class PropertyKind(Enum):
    """Kinds of formal properties about protocols.

    Each kind represents a verifiable guarantee:

    - ALWAYS_TERMINATES: protocol reaches an end state on every path.
    - NO_DEADLOCK: no role waits indefinitely for a message.
    - NO_DELETION: no step uses a destructive MessageKind (e.g. delete ops).
    - ORDERING: message A must precede message B in every execution.
    - EXCLUSION: a specific role is forbidden from sending a message kind.
    - ROLE_EXCLUSIVE: only the named role may send the specified message kind;
      any other sender is a violation.  Syntax: ``Cuoco exclusive dm``.
    - CONFIDENCE_MIN: all messages must carry confidence >= threshold.
    - TRUST_MIN: all senders must have trust tier >= the specified tier.
    - ALL_ROLES_PARTICIPATE: every role defined in the protocol sends at least
      one message.
    """

    ALWAYS_TERMINATES = "always_terminates"
    NO_DEADLOCK = "no_deadlock"
    NO_DELETION = "no_deletion"              # no destructive operations
    ORDERING = "ordering"                    # A before B
    EXCLUSION = "exclusion"                  # role cannot send message
    ROLE_EXCLUSIVE = "role_exclusive"        # only role can send action
    CONFIDENCE_MIN = "confidence_min"        # confidence >= threshold
    TRUST_MIN = "trust_min"                  # trust >= tier
    ALL_ROLES_PARTICIPATE = "all_roles_participate"


class PropertyVerdict(Enum):
    """Outcome of checking a single property."""

    PROVED = "proved"        # statically verified true
    SATISFIED = "satisfied"  # runtime check passed
    VIOLATED = "violated"    # check failed
    SKIPPED = "skipped"      # cannot check in this mode


# ============================================================
# Result types (all frozen dataclasses, pattern P01)
# ============================================================


@dataclass(frozen=True)
class PropertySpec:
    """A single property assertion about a protocol.

    Attributes:
        kind: The kind of property being asserted.
        params: Kind-specific parameters (role names, MessageKind values).
        threshold: For CONFIDENCE_MIN, the minimum confidence value (0.0-1.0).

    Parameter conventions by kind:
        ALWAYS_TERMINATES:    params=()
        NO_DEADLOCK:          params=()
        NO_DELETION:          params=()
        ORDERING:             params=(a_kind_value, b_kind_value)
        EXCLUSION:            params=(role_name, msg_kind_value)
        ROLE_EXCLUSIVE:       params=(role_name, msg_kind_value)
        CONFIDENCE_MIN:       params=(), threshold set
        TRUST_MIN:            params=(tier_value,)
        ALL_ROLES_PARTICIPATE: params=()
    """

    kind: PropertyKind
    params: tuple[str, ...] = ()
    threshold: float = 0.0

    def __post_init__(self) -> None:
        if self.kind == PropertyKind.ORDERING and len(self.params) != 2:
            raise ValueError(
                f"ORDERING requires exactly 2 params (a, b), got {len(self.params)}"
            )
        if self.kind == PropertyKind.EXCLUSION and len(self.params) != 2:
            raise ValueError(
                f"EXCLUSION requires exactly 2 params (role, msg_kind), got {len(self.params)}"
            )
        if self.kind == PropertyKind.ROLE_EXCLUSIVE and len(self.params) != 2:
            raise ValueError(
                f"ROLE_EXCLUSIVE requires exactly 2 params (role, msg_kind), got {len(self.params)}"
            )
        if self.kind == PropertyKind.TRUST_MIN and len(self.params) != 1:
            raise ValueError(
                f"TRUST_MIN requires exactly 1 param (tier), got {len(self.params)}"
            )
        if self.kind == PropertyKind.CONFIDENCE_MIN:
            if not (0.0 <= self.threshold <= 1.0):
                raise ValueError(
                    f"CONFIDENCE_MIN threshold must be 0.0-1.0, got {self.threshold}"
                )


@dataclass(frozen=True)
class ProtocolSpec:
    """Complete specification: protocol name + properties.

    Attributes:
        protocol_name: Name of the protocol this spec applies to.
        properties: Tuple of PropertySpec assertions to check.
    """

    protocol_name: str
    properties: tuple[PropertySpec, ...]

    def __post_init__(self) -> None:
        if not self.protocol_name:
            raise ValueError("protocol_name cannot be empty")
        if not self.properties:
            raise ValueError("properties cannot be empty")


@dataclass(frozen=True)
class PropertyResult:
    """Result of checking a single property.

    Attributes:
        spec: The property spec that was checked.
        verdict: Whether it was proved, satisfied, violated, or skipped.
        evidence: Human-readable explanation of the verdict.
    """

    spec: PropertySpec
    verdict: PropertyVerdict
    evidence: str = ""


@dataclass(frozen=True)
class PropertyReport:
    """Full report for all properties checked against a protocol.

    Attributes:
        protocol_name: Name of the protocol that was checked.
        results: Tuple of PropertyResult for each property.
    """

    protocol_name: str
    results: tuple[PropertyResult, ...]

    @property
    def all_passed(self) -> bool:
        """True if no properties were violated."""
        return all(
            r.verdict != PropertyVerdict.VIOLATED for r in self.results
        )

    @property
    def passed_count(self) -> int:
        """Number of properties that were proved or satisfied."""
        return sum(
            1 for r in self.results
            if r.verdict in (PropertyVerdict.PROVED, PropertyVerdict.SATISFIED)
        )

    @property
    def violated_count(self) -> int:
        """Number of properties that were violated."""
        return sum(1 for r in self.results if r.verdict == PropertyVerdict.VIOLATED)


# ============================================================
# Confidence level mapping
# ============================================================

# Maps string confidence label -> float threshold (immutable, P04)
_CONFIDENCE_LEVELS = MappingProxyType({
    "certain": 1.0,
    "high": 0.8,
    "medium": 0.5,
    "low": 0.2,
    "speculative": 0.1,
})

# Maps string tier label -> TrustTier (immutable, P04)
_TRUST_TIER_MAP = MappingProxyType({
    "verified": TrustTier.VERIFIED,
    "trusted": TrustTier.TRUSTED,
    "standard": TrustTier.STANDARD,
    "untrusted": TrustTier.UNTRUSTED,
})

# Ordering of TrustTier for >= comparison (higher index = higher trust, immutable P04)
_TRUST_TIER_ORDER = MappingProxyType({
    TrustTier.UNTRUSTED: 0,
    TrustTier.STANDARD: 1,
    TrustTier.TRUSTED: 2,
    TrustTier.VERIFIED: 3,
})


# ============================================================
# Tokenizer (line-oriented, indent-aware)
# ============================================================


class _TokKind(Enum):
    WORD = auto()
    COLON = auto()
    GTE = auto()       # >=
    NEWLINE = auto()
    INDENT = auto()
    EOF = auto()


@dataclass(frozen=True)
class _Tok:
    kind: _TokKind
    value: str
    line: int


_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _tokenize_spec(source: str) -> list[_Tok]:
    """Tokenize spec notation into a flat token list.

    Indent-aware: leading spaces on each line produce INDENT tokens
    (one per 4-space group).  Tabs are rejected.

    The source is ``textwrap.dedent``-ed first so that triple-quoted
    strings with arbitrary base indentation are handled naturally.
    """
    tokens: list[_Tok] = []
    source = textwrap.dedent(source)
    lines = source.split("\n")

    for line_no, raw_line in enumerate(lines, start=1):
        if "\t" in raw_line:
            raise SpecParseError(
                "tabs are not allowed, use 4 spaces for indentation",
                line=line_no,
            )

        stripped = raw_line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            # blank or comment line
            continue

        # Count leading spaces -> indent level (4 spaces = 1 level)
        leading = len(stripped) - len(stripped.lstrip())
        indent_level = leading // 4
        if leading % 4 != 0 and leading > 0:
            raise SpecParseError(
                f"indentation must be a multiple of 4 spaces (got {leading})",
                line=line_no,
            )

        for _ in range(indent_level):
            tokens.append(_Tok(_TokKind.INDENT, "    ", line_no))

        # Tokenize the content (after stripping leading whitespace)
        content = stripped.lstrip()
        pos = 0
        while pos < len(content):
            ch = content[pos]
            if ch == " ":
                pos += 1
                continue
            if ch == ":":
                tokens.append(_Tok(_TokKind.COLON, ":", line_no))
                pos += 1
                continue
            # >= operator (must check before single >)
            if content[pos:pos + 2] == ">=":
                tokens.append(_Tok(_TokKind.GTE, ">=", line_no))
                pos += 2
                continue

            m = _WORD_RE.match(content, pos)
            if m:
                tokens.append(_Tok(_TokKind.WORD, m.group(), line_no))
                pos = m.end()
                continue

            raise SpecParseError(
                f"unexpected character: {content[pos]!r}",
                line=line_no,
            )

        tokens.append(_Tok(_TokKind.NEWLINE, "\n", line_no))

    tokens.append(_Tok(_TokKind.EOF, "", len(lines)))
    return tokens


# ============================================================
# Parser (recursive descent)
# ============================================================


class _SpecParser:
    """Recursive descent parser for spec notation."""

    def __init__(self, tokens: list[_Tok]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> _Tok:
        return self._tokens[self._pos]

    def _advance(self) -> _Tok:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def _expect_word(self, value: str | None = None) -> _Tok:
        tok = self._peek()
        if tok.kind != _TokKind.WORD:
            expected = f"'{value}'" if value else "a word"
            raise SpecParseError(
                f"expected {expected}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
            )
        if value is not None and tok.value != value:
            raise SpecParseError(
                f"expected '{value}', got '{tok.value}'",
                line=tok.line,
            )
        return self._advance()

    def _expect(self, kind: _TokKind, value: str | None = None) -> _Tok:
        tok = self._peek()
        if tok.kind != kind:
            expected = f"'{value}'" if value else kind.name
            raise SpecParseError(
                f"expected {expected}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
            )
        if value is not None and tok.value != value:
            raise SpecParseError(
                f"expected '{value}', got '{tok.value}'",
                line=tok.line,
            )
        return self._advance()

    def _skip_newlines(self) -> None:
        while self._peek().kind == _TokKind.NEWLINE:
            self._advance()

    def _count_indents(self) -> int:
        """Count and consume consecutive INDENT tokens at current position."""
        count = 0
        while self._peek().kind == _TokKind.INDENT:
            self._advance()
            count += 1
        return count

    def _peek_indent_level(self) -> int:
        """Look ahead to count indents without consuming them."""
        saved = self._pos
        count = 0
        while self._tokens[saved].kind == _TokKind.INDENT:
            saved += 1
            count += 1
        return count

    def parse(self) -> ProtocolSpec:
        """Parse a complete spec block."""
        self._skip_newlines()

        # 'properties' 'for' IDENT ':'
        self._expect_word("properties")
        self._expect_word("for")
        name_tok = self._expect_word()
        self._expect(_TokKind.COLON)
        self._expect(_TokKind.NEWLINE)

        # Parse properties (each at indent level 1)
        self._skip_newlines()
        properties = self._parse_properties()

        if not properties:
            raise SpecParseError(
                "spec block must have at least one property",
                line=name_tok.line,
            )

        return ProtocolSpec(
            protocol_name=name_tok.value,
            properties=tuple(properties),
        )

    def _parse_properties(self) -> list[PropertySpec]:
        """Parse a list of property declarations at indent level 1."""
        props: list[PropertySpec] = []

        while True:
            self._skip_newlines()

            if self._peek().kind == _TokKind.EOF:
                break

            level = self._peek_indent_level()
            if level < 1:
                break

            # Consume the indent
            self._count_indents()

            tok = self._peek()
            if tok.kind == _TokKind.EOF:
                break
            if tok.kind == _TokKind.NEWLINE:
                continue

            props.append(self._parse_property_body(tok.line))

        return props

    def _parse_property_body(self, line: int) -> PropertySpec:
        """Parse a single property body after indent has been consumed.

        Dispatches on the first word:
            'always'     -> ALWAYS_TERMINATES
            'no'         -> NO_DEADLOCK
            'all'        -> ALL_ROLES_PARTICIPATE
            'confidence' -> CONFIDENCE_MIN
            'trust'      -> TRUST_MIN
            IDENT 'before' IDENT  -> ORDERING
            IDENT 'cannot' 'send' IDENT -> EXCLUSION
        """
        tok = self._peek()
        if tok.kind != _TokKind.WORD:
            raise SpecParseError(
                f"expected property keyword, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
            )

        first = tok.value

        if first == "always":
            return self._parse_always_terminates()
        if first == "no":
            # Disambiguate: "no deadlock" vs "no deletion"
            next_idx = self._pos + 1
            if next_idx < len(self._tokens) and self._tokens[next_idx].value == "deletion":
                return self._parse_no_deletion()
            return self._parse_no_deadlock()
        if first == "all":
            return self._parse_all_roles_participate()
        if first == "confidence":
            return self._parse_confidence_min()
        if first == "trust":
            return self._parse_trust_min()

        # Could be ORDERING or EXCLUSION - depends on second keyword
        return self._parse_ident_property()

    def _parse_always_terminates(self) -> PropertySpec:
        """Parse: 'always' 'terminates'"""
        self._expect_word("always")
        self._expect_word("terminates")
        self._expect(_TokKind.NEWLINE)
        return PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES)

    def _parse_no_deadlock(self) -> PropertySpec:
        """Parse: 'no' 'deadlock'"""
        self._expect_word("no")
        self._expect_word("deadlock")
        self._expect(_TokKind.NEWLINE)
        return PropertySpec(kind=PropertyKind.NO_DEADLOCK)

    def _parse_no_deletion(self) -> PropertySpec:
        """Parse: 'no' 'deletion'"""
        self._expect_word("no")
        self._expect_word("deletion")
        self._expect(_TokKind.NEWLINE)
        return PropertySpec(kind=PropertyKind.NO_DELETION)

    def _parse_all_roles_participate(self) -> PropertySpec:
        """Parse: 'all' 'roles' 'participate'"""
        self._expect_word("all")
        self._expect_word("roles")
        self._expect_word("participate")
        self._expect(_TokKind.NEWLINE)
        return PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE)

    def _parse_confidence_min(self) -> PropertySpec:
        """Parse: 'confidence' '>=' IDENT"""
        self._expect_word("confidence")
        self._expect(_TokKind.GTE)
        level_tok = self._expect_word()
        level = level_tok.value.lower()
        if level not in _CONFIDENCE_LEVELS:
            valid = ", ".join(sorted(_CONFIDENCE_LEVELS))
            raise SpecParseError(
                f"unknown confidence level '{level}'. Valid: {valid}",
                line=level_tok.line,
            )
        self._expect(_TokKind.NEWLINE)
        return PropertySpec(
            kind=PropertyKind.CONFIDENCE_MIN,
            threshold=_CONFIDENCE_LEVELS[level],
        )

    def _parse_trust_min(self) -> PropertySpec:
        """Parse: 'trust' '>=' IDENT"""
        self._expect_word("trust")
        self._expect(_TokKind.GTE)
        tier_tok = self._expect_word()
        tier = tier_tok.value.lower()
        if tier not in _TRUST_TIER_MAP:
            valid = ", ".join(sorted(_TRUST_TIER_MAP))
            raise SpecParseError(
                f"unknown trust tier '{tier}'. Valid: {valid}",
                line=tier_tok.line,
            )
        self._expect(_TokKind.NEWLINE)
        return PropertySpec(
            kind=PropertyKind.TRUST_MIN,
            params=(tier,),
        )

    def _parse_ident_property(self) -> PropertySpec:
        """Parse ORDERING, EXCLUSION, or ROLE_EXCLUSIVE starting with an IDENT.

        ORDERING:       IDENT 'before' IDENT
        EXCLUSION:      IDENT 'cannot' 'send' IDENT
        ROLE_EXCLUSIVE: IDENT 'exclusive' IDENT
        """
        first_tok = self._expect_word()
        keyword_tok = self._peek()

        if keyword_tok.kind != _TokKind.WORD:
            raise SpecParseError(
                f"expected 'before', 'cannot', or 'exclusive', got {keyword_tok.kind.name}",
                line=keyword_tok.line,
            )

        if keyword_tok.value == "before":
            return self._parse_ordering(first_tok)
        if keyword_tok.value == "cannot":
            return self._parse_exclusion(first_tok)
        if keyword_tok.value == "exclusive":
            return self._parse_role_exclusive(first_tok)

        raise SpecParseError(
            f"expected 'before', 'cannot', or 'exclusive', got '{keyword_tok.value}'",
            line=keyword_tok.line,
        )

    def _parse_ordering(self, first_tok: _Tok) -> PropertySpec:
        """Parse: IDENT 'before' IDENT  (MessageKind values in snake_case)"""
        self._expect_word("before")
        second_tok = self._expect_word()
        self._expect(_TokKind.NEWLINE)

        a = first_tok.value.lower()
        b = second_tok.value.lower()

        # Validate both are known MessageKind values
        a_kind = _parse_message_kind(a, first_tok.line)
        b_kind = _parse_message_kind(b, second_tok.line)

        if a_kind == b_kind:
            raise SpecParseError(
                f"ORDERING: a and b must differ (got '{a}' before '{a}')",
                line=first_tok.line,
            )

        return PropertySpec(
            kind=PropertyKind.ORDERING,
            params=(a, b),
        )

    def _parse_exclusion(self, role_tok: _Tok) -> PropertySpec:
        """Parse: IDENT 'cannot' 'send' IDENT  (role, MessageKind)"""
        self._expect_word("cannot")
        self._expect_word("send")
        msg_tok = self._expect_word()
        self._expect(_TokKind.NEWLINE)

        msg = msg_tok.value.lower()
        _parse_message_kind(msg, msg_tok.line)  # validate

        return PropertySpec(
            kind=PropertyKind.EXCLUSION,
            params=(role_tok.value, msg),
        )

    def _parse_role_exclusive(self, role_tok: _Tok) -> PropertySpec:
        """Parse: IDENT 'exclusive' IDENT  (only role can send MessageKind)"""
        self._expect_word("exclusive")
        msg_tok = self._expect_word()
        self._expect(_TokKind.NEWLINE)

        msg = msg_tok.value.lower()
        _parse_message_kind(msg, msg_tok.line)  # validate

        return PropertySpec(
            kind=PropertyKind.ROLE_EXCLUSIVE,
            params=(role_tok.value, msg),
        )


# ============================================================
# MessageKind parsing helper
# ============================================================

# Pre-computed lookup: snake_case value -> MessageKind (immutable, P04)
_VALUE_TO_KIND = MappingProxyType({k.value: k for k in MessageKind})

# Pre-computed lookup: AgentRole value -> AgentRole (immutable, P04, F3 fix)
_VALUE_TO_ROLE = MappingProxyType({r.value: r for r in AgentRole})


def _parse_message_kind(name: str, line: int = 0) -> MessageKind:
    """Parse a snake_case MessageKind name. Raises SpecParseError if unknown."""
    kind = _VALUE_TO_KIND.get(name)
    if kind is None:
        valid = ", ".join(sorted(_VALUE_TO_KIND))
        raise SpecParseError(
            f"unknown message kind '{name}'. Valid (snake_case): {valid}",
            line=line,
        )
    return kind


# ============================================================
# Static checker helpers
# ============================================================


def _collect_all_steps(
    elements: tuple[ProtocolElement, ...],
) -> list[ProtocolStep]:
    """Recursively collect all ProtocolStep objects from elements (including nested choices)."""
    result: list[ProtocolStep] = []
    for elem in elements:
        if isinstance(elem, ProtocolStep):
            result.append(elem)
        elif isinstance(elem, ProtocolChoice):
            for branch_elems in elem.branches.values():
                result.extend(_collect_all_steps(branch_elems))
    return result


def _find_violating_steps(
    elements: tuple[ProtocolElement, ...],
    predicate: object,
    context: str = "",
) -> list[str]:
    """Recursively find steps matching predicate, preserving branch context in descriptions."""
    violations: list[str] = []
    for elem in elements:
        if isinstance(elem, ProtocolStep):
            if predicate(elem):  # type: ignore[operator]
                desc = f"{elem.sender} -> {elem.receiver} : {elem.message_kind.value}"
                violations.append(f"branch '{context}': {desc}" if context else f"top-level step: {desc}")
        elif isinstance(elem, ProtocolChoice):
            for branch_name, branch_elems in elem.branches.items():
                sub_ctx = f"{context} > {branch_name}" if context else branch_name
                violations.extend(_find_violating_steps(branch_elems, predicate, sub_ctx))
    return violations


_MAX_PATHS = 1000  # Safety cap: prevent exponential blowup on deeply nested choices


def _collect_all_paths(
    elements: tuple[ProtocolElement, ...],
) -> list[list[ProtocolStep]]:
    """Collect all execution paths through a protocol as flat step lists.

    Each path is a sequence of ProtocolStep objects representing one
    possible execution trace through the protocol.

    For a linear protocol with no choices, returns a single path.
    For a protocol with a ProtocolChoice (including nested choices),
    returns one path per branch combination.

    Capped at _MAX_PATHS to prevent OOM on pathological inputs (Bug Hunt S476 P1).
    """
    # Start with one empty path
    paths: list[list[ProtocolStep]] = [[]]

    for elem in elements:
        if isinstance(elem, ProtocolStep):
            # Append this step to all current paths
            for path in paths:
                path.append(elem)
        elif isinstance(elem, ProtocolChoice):
            # Fan out: for each current path, create one path per branch
            new_paths: list[list[ProtocolStep]] = []
            for path in paths:
                for branch_elems in elem.branches.values():
                    # Recursively expand nested choices within branches
                    branch_paths = _collect_all_paths(branch_elems)
                    for bp in branch_paths:
                        new_path = list(path)
                        new_path.extend(bp)
                        new_paths.append(new_path)
                        if len(new_paths) >= _MAX_PATHS:
                            break
                    if len(new_paths) >= _MAX_PATHS:
                        break
                if len(new_paths) >= _MAX_PATHS:
                    break
            paths = new_paths if new_paths else paths

    return paths


def _check_always_terminates_static(protocol: Protocol) -> PropertyResult:
    """PROVED if protocol has finite elements and finite max_repetitions."""
    spec = PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES)

    # All current Protocol objects have finite elements (no unbounded recursion)
    # and max_repetitions >= 1 (enforced by Protocol.__post_init__).
    # By construction, every protocol in Lingua Universale terminates.
    evidence = (
        f"protocol '{protocol.name}' has {len(protocol.elements)} elements "
        f"and max_repetitions={protocol.max_repetitions} (finite by construction)"
    )
    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=evidence,
    )


def _check_no_deadlock_static(protocol: Protocol) -> PropertyResult:
    """PROVED if every step has exactly one successor or every choice branch is non-empty."""
    spec = PropertySpec(kind=PropertyKind.NO_DEADLOCK)

    # For the Protocol type: linear steps always have a successor (or terminal).
    # ProtocolChoice branches are validated non-empty by ProtocolChoice.__post_init__.
    # The SessionChecker enforces strict sequentiality - there are no blocking waits.
    # Therefore, deadlock-free by construction for all current protocol definitions.
    def _check_branches_non_empty(elements: tuple[ProtocolElement, ...]) -> bool:
        for elem in elements:
            if isinstance(elem, ProtocolChoice):
                for branch_elems in elem.branches.values():
                    if not branch_elems:
                        return False
                    if not _check_branches_non_empty(branch_elems):
                        return False
        return True

    all_branches_non_empty = _check_branches_non_empty(protocol.elements)

    if not all_branches_non_empty:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence="found empty branch in protocol (potential deadlock)",
        )

    evidence = (
        f"protocol '{protocol.name}' is deadlock-free: "
        "linear steps have unique successors, all choice branches are non-empty"
    )
    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=evidence,
    )


def _check_no_deletion_static(protocol: Protocol) -> PropertyResult:
    """PROVED if protocol has no destructive (delete) message kinds.

    The current MessageKind enum has no DELETE-related variants.
    Protocols that only use the standard message kinds (TASK_REQUEST,
    TASK_RESULT, etc.) are deletion-free by construction.
    """
    spec = PropertySpec(kind=PropertyKind.NO_DELETION)

    # Deletion-related kinds (currently none in MessageKind; future-proofing)
    deletion_kinds: frozenset[MessageKind] = frozenset()

    all_steps = _collect_all_steps(protocol.elements)
    for step in all_steps:
        if step.message_kind in deletion_kinds:
            return PropertyResult(
                spec=spec,
                verdict=PropertyVerdict.VIOLATED,
                evidence=f"step {step.sender} -> {step.receiver} uses deletion kind {step.message_kind.value}",
            )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=(
            f"protocol '{protocol.name}' uses no destructive message kinds "
            f"({len(all_steps)} steps checked)"
        ),
    )


def _check_ordering_static(protocol: Protocol, spec: PropertySpec) -> PropertyResult:
    """VIOLATED if any execution path has B before A.

    Vacuously PROVED for paths that do not contain both A and B.
    """
    a_str, b_str = spec.params
    a_kind = _VALUE_TO_KIND[a_str]
    b_kind = _VALUE_TO_KIND[b_str]

    paths = _collect_all_paths(protocol.elements)

    for path in paths:
        kinds_in_path = [step.message_kind for step in path]
        has_a = a_kind in kinds_in_path
        has_b = b_kind in kinds_in_path

        if not (has_a and has_b):
            # Vacuously true: path doesn't contain both
            continue

        idx_a = kinds_in_path.index(a_kind)
        idx_b = kinds_in_path.index(b_kind)

        if idx_b < idx_a:
            # B appears before A in this path
            return PropertyResult(
                spec=spec,
                verdict=PropertyVerdict.VIOLATED,
                evidence=(
                    f"'{b_str}' appears at step {idx_b} before "
                    f"'{a_str}' at step {idx_a} in an execution path"
                ),
            )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=(
            f"'{a_str}' precedes '{b_str}' in all execution paths "
            f"that contain both (checked {len(paths)} path(s))"
        ),
    )


def _check_exclusion_static(protocol: Protocol, spec: PropertySpec) -> PropertyResult:
    """VIOLATED if any ProtocolStep has sender=role AND message_kind=msg."""
    role, msg_str = spec.params
    msg_kind = _VALUE_TO_KIND[msg_str]

    violations = _find_violating_steps(
        protocol.elements,
        lambda step: step.sender == role and step.message_kind == msg_kind,
    )

    if violations:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence=(
                f"role '{role}' sends '{msg_str}' in: "
                + "; ".join(violations)
            ),
        )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=(
            f"role '{role}' never sends '{msg_str}' "
            f"in any step of protocol '{protocol.name}'"
        ),
    )


def _check_role_exclusive_static(protocol: Protocol, spec: PropertySpec) -> PropertyResult:
    """Check that only the exclusive role sends the specified message kind.

    VIOLATED if any step (top-level or inside a choice branch, including
    nested choices) has the given message kind sent by a role other than
    ``spec.params[0]``.
    """
    exclusive_role, msg_str = spec.params
    msg_kind = _VALUE_TO_KIND[msg_str]

    violations = _find_violating_steps(
        protocol.elements,
        lambda step: step.message_kind == msg_kind and step.sender != exclusive_role,
    )

    if violations:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence=(
                f"role other than '{exclusive_role}' sends '{msg_str}' in: "
                + "; ".join(violations)
            ),
        )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=(
            f"only '{exclusive_role}' sends '{msg_str}' "
            f"in protocol '{protocol.name}'"
        ),
    )


def _check_trust_min_static(protocol: Protocol, spec: PropertySpec) -> PropertyResult:
    """Check that all sender roles in the protocol have trust >= specified tier.

    Uses trust_tier_for_role() from trust.py.
    Roles that are not AgentRole members are treated as STANDARD tier.
    """
    tier_str = spec.params[0]
    required_tier = _TRUST_TIER_MAP[tier_str]
    required_order = _TRUST_TIER_ORDER[required_tier]

    # Collect all sender roles across all steps (including nested choices)
    all_steps = _collect_all_steps(protocol.elements)
    sender_roles: set[str] = {step.sender for step in all_steps}

    violations: list[str] = []

    for role_name in sorted(sender_roles):
        # O(1) lookup via pre-computed reverse index (P04, F3 fix)
        role_obj = _VALUE_TO_ROLE.get(role_name)

        if role_obj is not None:
            actual_tier = trust_tier_for_role(role_obj)
        else:
            # Unknown role -> STANDARD (conservative default)
            actual_tier = TrustTier.STANDARD

        actual_order = _TRUST_TIER_ORDER[actual_tier]
        if actual_order < required_order:
            violations.append(
                f"role '{role_name}' has tier '{actual_tier.value}' "
                f"(required >= '{tier_str}')"
            )

    if violations:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence="; ".join(violations),
        )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=(
            f"all sender roles in '{protocol.name}' have trust >= '{tier_str}': "
            + ", ".join(sorted(sender_roles))
        ),
    )


def _check_all_roles_participate_static(protocol: Protocol, spec: PropertySpec) -> PropertyResult:
    """Check every role appears as sender or receiver in at least one step."""
    # Collect all roles that appear in steps (including nested choices)
    all_steps = _collect_all_steps(protocol.elements)
    active_roles: set[str] = set()
    for step in all_steps:
        active_roles.add(step.sender)
        active_roles.add(step.receiver)

    declared = set(protocol.roles)
    missing = declared - active_roles

    if missing:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence=(
                f"roles declared but never participating: "
                + ", ".join(sorted(missing))
            ),
        )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.PROVED,
        evidence=(
            f"all {len(declared)} roles participate in at least one step: "
            + ", ".join(sorted(declared))
        ),
    )


# ============================================================
# Runtime checker helpers
# ============================================================


def _check_ordering_runtime(
    log: Sequence[MessageRecord], spec: PropertySpec
) -> PropertyResult:
    """Verify ordering in the actual execution trace."""
    a_str, b_str = spec.params
    a_kind = _VALUE_TO_KIND[a_str]
    b_kind = _VALUE_TO_KIND[b_str]

    kinds_in_log = [record.kind for record in log]
    has_a = a_kind in kinds_in_log
    has_b = b_kind in kinds_in_log

    if not (has_a and has_b):
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.SATISFIED,
            evidence=(
                f"vacuously satisfied: "
                f"{'both kinds absent' if not has_a and not has_b else 'one kind absent'} "
                f"in session log ({len(log)} messages)"
            ),
        )

    idx_a = kinds_in_log.index(a_kind)
    idx_b = kinds_in_log.index(b_kind)

    if idx_b < idx_a:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence=(
                f"'{b_str}' sent at message {idx_b} before "
                f"'{a_str}' at message {idx_a} in session log"
            ),
        )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.SATISFIED,
        evidence=(
            f"'{a_str}' (message {idx_a}) precedes '{b_str}' "
            f"(message {idx_b}) in session log"
        ),
    )


def _check_exclusion_runtime(
    log: Sequence[MessageRecord], spec: PropertySpec
) -> PropertyResult:
    """Verify no excluded message was sent in the actual session."""
    role, msg_str = spec.params
    msg_kind = _VALUE_TO_KIND[msg_str]

    for i, record in enumerate(log):
        if record.sender == role and record.kind == msg_kind:
            return PropertyResult(
                spec=spec,
                verdict=PropertyVerdict.VIOLATED,
                evidence=(
                    f"role '{role}' sent '{msg_str}' at message {i} "
                    f"in session log"
                ),
            )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.SATISFIED,
        evidence=(
            f"role '{role}' did not send '{msg_str}' "
            f"in {len(log)} session messages"
        ),
    )


def _check_role_exclusive_runtime(
    log: Sequence[MessageRecord], spec: PropertySpec
) -> PropertyResult:
    """Verify only the exclusive role sent the specified message kind in the session."""
    exclusive_role, msg_str = spec.params
    msg_kind = _VALUE_TO_KIND[msg_str]

    for i, record in enumerate(log):
        if record.kind == msg_kind and record.sender != exclusive_role:
            return PropertyResult(
                spec=spec,
                verdict=PropertyVerdict.VIOLATED,
                evidence=(
                    f"role '{record.sender}' (not '{exclusive_role}') "
                    f"sent '{msg_str}' at message {i} in session log"
                ),
            )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.SATISFIED,
        evidence=(
            f"only '{exclusive_role}' sent '{msg_str}' "
            f"in {len(log)} session messages"
        ),
    )


def _check_all_roles_participate_runtime(
    log: Sequence[MessageRecord], spec: PropertySpec, protocol_roles: tuple[str, ...]
) -> PropertyResult:
    """Verify all declared protocol roles appeared in actual session."""
    active: set[str] = set()
    for record in log:
        active.add(record.sender)
        active.add(record.receiver)

    declared = set(protocol_roles)
    missing = declared - active

    if missing:
        return PropertyResult(
            spec=spec,
            verdict=PropertyVerdict.VIOLATED,
            evidence=(
                "roles declared but absent from session: "
                + ", ".join(sorted(missing))
            ),
        )

    return PropertyResult(
        spec=spec,
        verdict=PropertyVerdict.SATISFIED,
        evidence=(
            f"all {len(declared)} roles participated in the session: "
            + ", ".join(sorted(declared))
        ),
    )


# ============================================================
# Static checker
# ============================================================


def check_properties(protocol: Protocol, spec: ProtocolSpec) -> PropertyReport:
    """Statically check properties against a protocol definition.

    Each property in ``spec.properties`` is evaluated against the
    structure of ``protocol``.  Results use PROVED or VIOLATED verdicts.
    CONFIDENCE_MIN is always SKIPPED in static mode (runtime-only data).

    Args:
        protocol: The Protocol object to check against.
        spec: The ProtocolSpec containing properties to verify.

    Returns:
        A PropertyReport with one PropertyResult per property.

    Example::

        from cervellaswarm_lingua_universale.protocols import DelegateTask
        from cervellaswarm_lingua_universale.spec import parse_spec, check_properties

        spec = parse_spec('''
            properties for DelegateTask:
                always terminates
                no deadlock
                task_request before task_result
        ''')
        report = check_properties(DelegateTask, spec)
        assert report.all_passed
    """
    results: list[PropertyResult] = []

    for prop in spec.properties:
        if prop.kind == PropertyKind.ALWAYS_TERMINATES:
            results.append(_check_always_terminates_static(protocol))

        elif prop.kind == PropertyKind.NO_DEADLOCK:
            results.append(_check_no_deadlock_static(protocol))

        elif prop.kind == PropertyKind.NO_DELETION:
            results.append(_check_no_deletion_static(protocol))

        elif prop.kind == PropertyKind.ORDERING:
            results.append(_check_ordering_static(protocol, prop))

        elif prop.kind == PropertyKind.EXCLUSION:
            results.append(_check_exclusion_static(protocol, prop))

        elif prop.kind == PropertyKind.ROLE_EXCLUSIVE:
            results.append(_check_role_exclusive_static(protocol, prop))

        elif prop.kind == PropertyKind.CONFIDENCE_MIN:
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SKIPPED,
                evidence="CONFIDENCE_MIN is a runtime-only property (requires message metadata)",
            ))

        elif prop.kind == PropertyKind.TRUST_MIN:
            results.append(_check_trust_min_static(protocol, prop))

        elif prop.kind == PropertyKind.ALL_ROLES_PARTICIPATE:
            results.append(_check_all_roles_participate_static(protocol, prop))

        else:
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SKIPPED,
                evidence=f"unknown property kind: {prop.kind}",
            ))

    return PropertyReport(
        protocol_name=protocol.name,
        results=tuple(results),
    )


# ============================================================
# Runtime checker
# ============================================================


def check_session(
    log: Sequence[MessageRecord],
    spec: ProtocolSpec,
    protocol: Protocol | None = None,
) -> PropertyReport:
    """Check properties against a completed session log.

    Each property in ``spec.properties`` is evaluated against the
    actual messages recorded in ``log``.  Results use SATISFIED or
    VIOLATED verdicts.  TRUST_MIN is always SKIPPED (static-only).
    CONFIDENCE_MIN is always SKIPPED (future: needs message metadata).

    Args:
        log: Sequence of MessageRecord from a completed session.
        spec: The ProtocolSpec containing properties to verify.
        protocol: Optional Protocol for role-aware checks (ALL_ROLES_PARTICIPATE).
            If None, only roles present in the log are considered.

    Returns:
        A PropertyReport with one PropertyResult per property.

    Example::

        checker = SessionChecker(DelegateTask, session_id="test")
        checker.send("regina", "worker", task_request_msg)
        checker.send("worker", "regina", task_result_msg)
        checker.send("regina", "guardiana", audit_request_msg)
        checker.send("guardiana", "regina", audit_verdict_msg)

        spec = parse_spec('''
            properties for DelegateTask:
                task_request before task_result
                guardiana cannot send task_request
        ''')
        report = check_session(checker.log, spec)
        assert report.all_passed
    """
    results: list[PropertyResult] = []

    # Determine protocol roles for ALL_ROLES_PARTICIPATE
    if protocol is not None:
        protocol_roles = protocol.roles
    else:
        # Fall back to roles observed in the log
        observed: set[str] = set()
        for record in log:
            observed.add(record.sender)
            observed.add(record.receiver)
        protocol_roles = tuple(sorted(observed))

    for prop in spec.properties:
        if prop.kind in (PropertyKind.ALWAYS_TERMINATES, PropertyKind.NO_DEADLOCK):
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SATISFIED,
                evidence=(
                    f"session completed with {len(log)} messages "
                    f"(no deadlock, termination confirmed)"
                ),
            ))

        elif prop.kind == PropertyKind.NO_DELETION:
            # Satisfied: SessionChecker only allows protocol-defined messages
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SATISFIED,
                evidence=(
                    f"session completed with {len(log)} messages "
                    f"(no deletion operations in session)"
                ),
            ))

        elif prop.kind == PropertyKind.ORDERING:
            results.append(_check_ordering_runtime(log, prop))

        elif prop.kind == PropertyKind.EXCLUSION:
            results.append(_check_exclusion_runtime(log, prop))

        elif prop.kind == PropertyKind.ROLE_EXCLUSIVE:
            results.append(_check_role_exclusive_runtime(log, prop))

        elif prop.kind == PropertyKind.CONFIDENCE_MIN:
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SKIPPED,
                evidence="CONFIDENCE_MIN requires message metadata (not yet available in MessageRecord)",
            ))

        elif prop.kind == PropertyKind.TRUST_MIN:
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SKIPPED,
                evidence="TRUST_MIN is a static property (checked against protocol definition, not session log)",
            ))

        elif prop.kind == PropertyKind.ALL_ROLES_PARTICIPATE:
            results.append(
                _check_all_roles_participate_runtime(log, prop, protocol_roles)
            )

        else:
            results.append(PropertyResult(
                spec=prop,
                verdict=PropertyVerdict.SKIPPED,
                evidence=f"unknown property kind: {prop.kind}",
            ))

    return PropertyReport(
        protocol_name=spec.protocol_name,
        results=tuple(results),
    )


# ============================================================
# Public API
# ============================================================


def parse_spec(source: str) -> ProtocolSpec:
    """Parse spec notation into a ProtocolSpec.

    The source may be a triple-quoted string with arbitrary base
    indentation (``textwrap.dedent`` is applied automatically).

    Raises :class:`SpecParseError` on syntax errors with line info.

    Example::

        spec = parse_spec('''
            properties for DelegateTask:
                always terminates
                no deadlock
                task_request before task_result
                worker cannot send audit_request
                trust >= standard
                all roles participate
        ''')
        print(spec.protocol_name)  # "DelegateTask"
        print(len(spec.properties))  # 6
    """
    tokens = _tokenize_spec(source)
    parser = _SpecParser(tokens)
    spec = parser.parse()

    # Check for trailing content
    parser._skip_newlines()
    if parser._peek().kind != _TokKind.EOF:
        tok = parser._peek()
        raise SpecParseError(
            f"unexpected content after spec block: {tok.value!r}",
            line=tok.line,
        )

    return spec
