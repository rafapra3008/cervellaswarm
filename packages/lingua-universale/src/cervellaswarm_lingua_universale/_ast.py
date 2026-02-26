# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""AST node definitions for the Lingua Universale v0.2 unified parser (C1.3).

Every node is an immutable ``@dataclass(frozen=True)``.  Collections use
``tuple`` so that frozen dataclasses can hash their fields without issue.

Node hierarchy (mirrors the 62-production EBNF grammar from C1.2):

  Expr nodes        - IdentExpr, NumberExpr, StringExpr, AttrExpr,
                      MethodCallExpr, BinOpExpr, NotExpr, GroupExpr
  Property nodes    - AlwaysTerminates, NoDeadlock, OrderingProp,
                      ExclusionProp, ConfidenceProp, TrustProp, AllParticipate
  Step/Choice nodes - StepNode, ChoiceNode, BranchNode
  Protocol node     - ProtocolNode
  Agent node        - AgentNode
  Type nodes        - SimpleType, GenericType, FieldNode,
                      VariantTypeDecl, RecordTypeDecl
  Use node          - UseNode
  Top-level         - ProgramNode
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union


# ---------------------------------------------------------------------------
# Source location
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Loc:
    line: int  # 1-indexed
    col: int   # 0-indexed


# ---------------------------------------------------------------------------
# Expression nodes  (grammar section 5b)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IdentExpr:
    name: str
    loc: Loc


@dataclass(frozen=True)
class NumberExpr:
    value: str  # raw text; semantic interpretation deferred to C2
    loc: Loc


@dataclass(frozen=True)
class StringExpr:
    value: str  # includes surrounding quote characters, as emitted by tokenizer
    loc: Loc


@dataclass(frozen=True)
class AttrExpr:
    obj: str   # left-hand identifier  (e.g. "task")
    attr: str  # attribute name        (e.g. "well_defined")
    loc: Loc


@dataclass(frozen=True)
class MethodCallExpr:
    obj: str                    # receiver object   (e.g. "tests")
    method: str                 # method name       (e.g. "pass")
    args: tuple[Expr, ...]      # positional arguments
    loc: Loc


@dataclass(frozen=True)
class BinOpExpr:
    left: Expr
    op: str    # "and", "or", "==", "!=", "<", ">", "<=", ">="
    right: Expr
    loc: Loc


@dataclass(frozen=True)
class NotExpr:
    operand: Expr
    loc: Loc


@dataclass(frozen=True)
class GroupExpr:
    inner: Expr
    loc: Loc


# Recursive union - forward references resolved via __future__.annotations
Expr = Union[
    IdentExpr,
    NumberExpr,
    StringExpr,
    AttrExpr,
    MethodCallExpr,
    BinOpExpr,
    NotExpr,
    GroupExpr,
]


# ---------------------------------------------------------------------------
# Property nodes  (grammar section 3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AlwaysTerminates:
    loc: Loc


@dataclass(frozen=True)
class NoDeadlock:
    loc: Loc


@dataclass(frozen=True)
class OrderingProp:
    before: str  # role/event that must occur first
    after: str   # role/event that follows
    loc: Loc


@dataclass(frozen=True)
class ExclusionProp:
    role: str     # the excluded sender    (e.g. "backend")
    message: str  # the forbidden message  (e.g. "audit_verdict")
    loc: Loc


@dataclass(frozen=True)
class ConfidenceProp:
    level: str  # "certain" | "high" | "medium" | "low" | "speculative"
    loc: Loc


@dataclass(frozen=True)
class TrustProp:
    tier: str   # "verified" | "trusted" | "standard" | "untrusted"
    loc: Loc


@dataclass(frozen=True)
class AllParticipate:
    loc: Loc


Property = Union[
    AlwaysTerminates,
    NoDeadlock,
    OrderingProp,
    ExclusionProp,
    ConfidenceProp,
    TrustProp,
    AllParticipate,
]


# ---------------------------------------------------------------------------
# Step / Choice nodes  (grammar section 2)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StepNode:
    sender: str    # the role initiating the action  (e.g. "regina")
    action: str    # verb keyword: "asks" | "returns" | "tells" | "proposes" | "sends"
    receiver: str  # the target role
    payload: str   # verb phrase or noun  (e.g. "do task", "result", "plan")
    loc: Loc


@dataclass(frozen=True)
class BranchNode:
    label: str                   # branch label  (e.g. "approve", "reject")
    steps: tuple[StepNode, ...]
    loc: Loc


@dataclass(frozen=True)
class ChoiceNode:
    decider: str                         # the deciding role  (e.g. "regina")
    branches: tuple[BranchNode, ...]
    loc: Loc


StepOrChoice = Union[StepNode, ChoiceNode]


# ---------------------------------------------------------------------------
# Protocol node  (grammar section 2)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProtocolNode:
    name: str
    roles: tuple[str, ...]
    steps: tuple[StepOrChoice, ...]
    properties: tuple[Property, ...]
    loc: Loc


# ---------------------------------------------------------------------------
# Type expression nodes  (grammar section 6)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SimpleType:
    name: str       # e.g. "String", "Number"
    optional: bool  # True when written as "String?"
    loc: Loc


@dataclass(frozen=True)
class GenericType:
    name: str        # e.g. "List", "Confident"
    arg: TypeExpr    # the bracketed argument
    optional: bool   # True when written as "List[String]?"
    loc: Loc


TypeExpr = Union[SimpleType, GenericType]


@dataclass(frozen=True)
class FieldNode:
    name: str
    type_expr: TypeExpr
    loc: Loc


@dataclass(frozen=True)
class VariantTypeDecl:
    name: str
    variants: tuple[str, ...]  # at least two variants (grammar: IDENT ('|' IDENT)+)
    loc: Loc


@dataclass(frozen=True)
class RecordTypeDecl:
    name: str
    fields: tuple[FieldNode, ...]
    loc: Loc


# ---------------------------------------------------------------------------
# Agent node  (grammar section 4)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AgentNode:
    name: str
    role: str | None                # from "role: backend"
    trust: str | None               # from "trust: standard"
    accepts: tuple[str, ...]        # from "accepts: TaskRequest, ..."
    produces: tuple[str, ...]       # from "produces: TaskResult, ..."
    requires: tuple[Expr, ...]      # pre-conditions
    ensures: tuple[Expr, ...]       # post-conditions
    loc: Loc


# ---------------------------------------------------------------------------
# Use node  (grammar section 7)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class UseNode:
    module: str          # dotted name as a string  (e.g. "math", "datetime")
    alias: str | None    # from "as X"; None when absent
    loc: Loc


# ---------------------------------------------------------------------------
# Top-level program node
# ---------------------------------------------------------------------------


Declaration = Union[
    ProtocolNode,
    AgentNode,
    VariantTypeDecl,
    RecordTypeDecl,
    UseNode,
]


@dataclass(frozen=True)
class ProgramNode:
    declarations: tuple[Declaration, ...]
    loc: Loc
