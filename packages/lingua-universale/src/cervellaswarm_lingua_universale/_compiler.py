# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Compiler: Lingua Universale AST -> Python source code (C2).

Translates a ``ProgramNode`` AST (produced by the C1 parser) into executable
Python source.  The generated code includes runtime contract enforcement via
``ContractViolation`` and source annotations ``# [LU:line:col]`` for tracing.

Architecture (STUDIO C2.1, S412):
  - **String emission** -- generates Python source as strings (like codegen.py).
  - **isinstance dispatch** -- visitor pattern via ``_compile_declaration``.
  - **Separate from codegen.py** -- different pipeline (AST vs Protocol objects).
  - **Zero external dependencies** -- stdlib + internal modules only.

Implementation plan (7 sub-steps):
  C2.2.1  _contracts.py                DONE (S413)
  C2.2.2  _compiler.py core scaffold   DONE (S413)
          - CompiledModule, ASTCompiler, compile()
          - _expr_to_python, _type_to_python, _compile_use
  C2.2.3  _compile_variant_type, _compile_record_type     DONE (S413)
  C2.2.4  _compile_agent (contracts + metadata)           DONE (S414)
  C2.2.5  _compile_protocol (bridge to codegen.py)        DONE (S414)
  C2.2.6  Golden file tests + round-trip exec             DONE (S415)
  C2.2.7  Guardiana audit finale C2.2                     DONE (S415, 9.5/10)

C2.3 Python Interop (ongoing):
  C2.3.1  Hardening + types tracking                      S416
"""

from __future__ import annotations

import keyword
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._ast import (
    AgentNode,
    AttrExpr,
    BinOpExpr,
    BranchNode,
    ChoiceNode,
    GenericType,
    GroupExpr,
    IdentExpr,
    Loc,
    MethodCallExpr,
    NotExpr,
    NumberExpr,
    ProgramNode,
    ProtocolNode,
    RecordTypeDecl,
    SimpleType,
    StepNode,
    StringExpr,
    UseNode,
    VariantTypeDecl,
)

if TYPE_CHECKING:
    from ._ast import Declaration, Expr, StepOrChoice, TypeExpr
    from .protocols import Protocol, ProtocolElement
    from .types import MessageKind


# ============================================================
# LU -> Python type mapping
# ============================================================

_LU_TYPE_MAP: dict[str, str] = {
    "String": "str",
    "Number": "float",
    "Boolean": "bool",
    "Integer": "int",
    "Any": "object",
}

_LU_GENERIC_MAP: dict[str, str] = {
    "List": "list",
    "Map": "dict",
    "Set": "set",
    "Confident": "Confident",
}

# Python keywords that need a trailing underscore when used as identifiers
# in generated code (e.g. method name "pass" -> "pass_").
_PYTHON_KEYWORDS: frozenset[str] = frozenset(keyword.kwlist) | frozenset(
    keyword.softkwlist
)


# ============================================================
# Result type
# ============================================================


@dataclass(frozen=True)
class CompiledModule:
    """Result of compiling a ProgramNode to Python source.

    Attributes:
        source_file: Path or name of the ``.lu`` source file.
        python_source: Generated Python source code.
        agents: Names of agent declarations found in the program.
        protocols: Names of protocol declarations found in the program.
        imports: Module names from ``use`` statements.
        types: Names of variant and record type declarations (C2.3.1).
    """

    source_file: str
    python_source: str
    agents: tuple[str, ...]
    protocols: tuple[str, ...]
    imports: tuple[str, ...]
    types: tuple[str, ...] = ()


# ============================================================
# Compiler
# ============================================================


class ASTCompiler:
    """Compiles a ``ProgramNode`` AST to Python source code.

    Architecture: isinstance-based visitor dispatch, string emission.
    Each declaration type has a dedicated ``_compile_*`` method.

    Usage::

        compiler = ASTCompiler()
        result = compiler.compile(program, source_file="example.lu")
        print(result.python_source)
    """

    def __init__(self) -> None:
        # Preamble import tracker: declaration compilers add lines here.
        # Reset at the start of each compile() call.
        self._preamble_imports: set[str] = set()

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def compile(
        self, program: ProgramNode, *, source_file: str = "<input>"
    ) -> CompiledModule:
        """Compile a full program AST to Python source."""
        # Reset preamble for this compilation
        self._preamble_imports = set()

        body_lines: list[str] = []

        agents: list[str] = []
        protocols: list[str] = []
        imports: list[str] = []
        types: list[str] = []

        for decl in program.declarations:
            decl_lines = self._compile_declaration(decl)
            body_lines.extend(decl_lines)
            body_lines.append("")  # blank separator between declarations

            # Track metadata
            if isinstance(decl, UseNode):
                imports.append(decl.module)
            elif isinstance(decl, AgentNode):
                agents.append(decl.name)
            elif isinstance(decl, ProtocolNode):
                protocols.append(decl.name)
            elif isinstance(decl, (VariantTypeDecl, RecordTypeDecl)):
                types.append(decl.name)

        # Assemble: docstring + preamble imports + body
        lines: list[str] = [
            f'"""Auto-generated from {source_file} by Lingua Universale compiler."""',
        ]
        if self._preamble_imports:
            lines.append("")
            lines.extend(sorted(self._preamble_imports))
        lines.append("")
        lines.extend(body_lines)

        python_source = "\n".join(lines).rstrip("\n") + "\n"

        return CompiledModule(
            source_file=source_file,
            python_source=python_source,
            agents=tuple(agents),
            protocols=tuple(protocols),
            imports=tuple(imports),
            types=tuple(types),
        )

    # ----------------------------------------------------------
    # Declaration dispatch
    # ----------------------------------------------------------

    def _compile_declaration(self, decl: Declaration) -> list[str]:
        """Dispatch a top-level declaration to its compiler method."""
        if isinstance(decl, UseNode):
            return self._compile_use(decl)
        if isinstance(decl, VariantTypeDecl):
            return self._compile_variant_type(decl)
        if isinstance(decl, RecordTypeDecl):
            return self._compile_record_type(decl)
        if isinstance(decl, AgentNode):
            return self._compile_agent(decl)
        if isinstance(decl, ProtocolNode):
            return self._compile_protocol(decl)
        raise TypeError(f"Unknown declaration type: {type(decl).__name__}")

    # ----------------------------------------------------------
    # UseNode -> import statement
    # ----------------------------------------------------------

    def _compile_use(self, node: UseNode) -> list[str]:
        """Compile ``use math`` or ``use datetime as dt`` to Python import."""
        loc = self._loc_comment(node.loc)
        if node.alias:
            return [f"import {node.module} as {node.alias}  {loc}"]
        return [f"import {node.module}  {loc}"]

    # ----------------------------------------------------------
    # Type declarations (C2.2.3)
    # ----------------------------------------------------------

    def _compile_variant_type(self, node: VariantTypeDecl) -> list[str]:
        """Compile ``type Status = Active | Inactive`` to Python.

        Generates ``Status = Literal["Active", "Inactive"]`` and registers
        ``from typing import Literal`` in the preamble imports.
        """
        self._preamble_imports.add("from typing import Literal")
        loc = self._loc_comment(node.loc)
        variants = ", ".join(f'"{v}"' for v in node.variants)
        return [f"{node.name} = Literal[{variants}]  {loc}"]

    def _compile_record_type(self, node: RecordTypeDecl) -> list[str]:
        """Compile ``type TaskData: name: String ...`` to Python.

        Generates a ``@dataclass(frozen=True)`` class with typed fields.
        Registers ``from dataclasses import dataclass`` in the preamble.
        """
        self._preamble_imports.add("from dataclasses import dataclass")
        loc = self._loc_comment(node.loc)
        lines = [
            f"@dataclass(frozen=True)  {loc}",
            f"class {node.name}:",
            f'    """Record type \'{node.name}\' -- compiled from Lingua Universale."""',
        ]
        if not node.fields:
            lines.append("    pass")
        else:
            for field in node.fields:
                type_str = self._type_to_python(field.type_expr)
                field_loc = self._loc_comment(field.loc)
                lines.append(f"    {field.name}: {type_str}  {field_loc}")
        return lines

    # ----------------------------------------------------------
    # Agent declaration (C2.2.4)
    # ----------------------------------------------------------

    def _compile_agent(self, node: AgentNode) -> list[str]:
        """Compile ``agent Worker: ...`` to a Python class.

        Generates:
          - Class with ``__lu_role__``, ``__lu_trust__``, ``__lu_accepts__``,
            ``__lu_produces__`` metadata attributes.
          - ``process()`` method with ``requires`` guards (preconditions) and
            ``ensures`` guards (postconditions) using ``ContractViolation``.
          - ``_execute()`` stub for user implementation.

        Registers ``from cervellaswarm_lingua_universale._contracts import
        ContractViolation`` in the preamble when any contract clause exists.
        """
        loc = self._loc_comment(node.loc)
        name = self._safe_ident(node.name)
        lines: list[str] = [
            f"class {name}:  {loc}",
            f'    """Agent \'{node.name}\' -- compiled from Lingua Universale."""',
        ]

        # --- Metadata attributes ---
        if node.role is not None:
            lines.append(f'    __lu_role__ = "{node.role}"')
        if node.trust is not None:
            lines.append(f'    __lu_trust__ = "{node.trust}"')
        if node.accepts:
            accept_str = ", ".join(f'"{a}"' for a in node.accepts)
            lines.append(f"    __lu_accepts__ = ({accept_str},)")
        if node.produces:
            produce_str = ", ".join(f'"{p}"' for p in node.produces)
            lines.append(f"    __lu_produces__ = ({produce_str},)")

        # --- Register ContractViolation import if contracts exist ---
        has_contracts = bool(node.requires or node.ensures)
        if has_contracts:
            self._preamble_imports.add(
                "from cervellaswarm_lingua_universale._contracts"
                " import ContractViolation"
            )

        # --- process() method ---
        lines.append("")
        lines.append("    def process(self, **kwargs):")

        if not has_contracts:
            lines.append(
                '        """Process input. No contracts declared."""'
            )
            lines.append("        return self._execute(**kwargs)")
        else:
            lines.append(
                '        """Process input with contract enforcement."""'
            )
            # requires (preconditions)
            if node.requires:
                lines.append("        # --- requires (preconditions) ---")
                for req in node.requires:
                    guard_py = self._contract_expr_to_python(req)
                    # Human-readable condition uses plain expr (no kwargs[])
                    human_py = self._expr_to_python(req)
                    req_loc = self._loc_comment(req.loc)
                    source = f"line {req.loc.line}, col {req.loc.col}"
                    lines.append(f"        if not ({guard_py}):  {req_loc}")
                    lines.append(
                        f"            raise ContractViolation("
                        f'"{self._escape_contract_str(human_py)}"'
                        f', kind="requires"'
                        f', source="{source}"'
                        f")"
                    )

            # execute
            lines.append("        _result = self._execute(**kwargs)")

            # ensures (postconditions)
            if node.ensures:
                lines.append("        # --- ensures (postconditions) ---")
                for ens in node.ensures:
                    guard_py = self._contract_expr_to_python(ens)
                    human_py = self._expr_to_python(ens)
                    ens_loc = self._loc_comment(ens.loc)
                    source = f"line {ens.loc.line}, col {ens.loc.col}"
                    lines.append(f"        if not ({guard_py}):  {ens_loc}")
                    lines.append(
                        f"            raise ContractViolation("
                        f'"{self._escape_contract_str(human_py)}"'
                        f', kind="ensures"'
                        f', source="{source}"'
                        f")"
                    )

            lines.append("        return _result")

        # --- _execute() stub ---
        lines.append("")
        lines.append("    def _execute(self, **kwargs):")
        lines.append(
            f'        raise NotImplementedError("{node.name}._execute")'
        )

        return lines

    # ----------------------------------------------------------
    # Protocol declaration (C2.2.5)
    # ----------------------------------------------------------

    def _compile_protocol(self, node: ProtocolNode) -> list[str]:
        """Compile ``protocol DelegateTask: ...`` to Python via codegen bridge.

        Pipeline: ProtocolNode AST -> Protocol runtime object -> PythonGenerator.
        The bridge transforms AST step/choice nodes into runtime ProtocolStep
        and ProtocolChoice objects, then delegates code generation to the
        existing ``codegen.PythonGenerator``.

        Registers protocol-specific imports in the preamble.
        """
        from .codegen import PythonGenerator
        from .protocols import Protocol, ProtocolChoice, ProtocolStep
        from .types import MessageKind

        # 1. Transform AST -> Protocol runtime object
        protocol = self._ast_to_protocol(node)

        # 2. Generate code via PythonGenerator (individual sections)
        gen = PythonGenerator()
        proto_def = gen.generate_protocol_definition(protocol)
        role_classes = gen.generate_role_classes(protocol)
        session_class = gen.generate_session_class(protocol)

        # 2b. Prefix class names to avoid collision in multi-protocol programs.
        # "ProtocolSession" -> "{Name}Session", "{Role}Role" -> "{Name}{Role}Role"
        prefix = node.name
        session_class = session_class.replace(
            "class ProtocolSession:", f"class {prefix}Session:",
        )
        for role in node.roles:
            from .codegen import _to_class_name
            cls_name = f"{_to_class_name(role)}Role"
            prefixed = f"{prefix}{cls_name}"
            role_classes = role_classes.replace(
                f"class {cls_name}:", f"class {prefixed}:",
            )
            session_class = session_class.replace(
                f"{cls_name}(self)", f"{prefixed}(self)",
            )
            session_class = session_class.replace(
                f"-> {cls_name}:", f"-> {prefixed}:",
            )

        # 3. Register preamble imports
        self._preamble_imports.add(
            "from cervellaswarm_lingua_universale.types import MessageKind"
        )
        self._preamble_imports.add(
            "from cervellaswarm_lingua_universale.protocols import ("
            "\n    Protocol,"
            "\n    ProtocolChoice,"
            "\n    ProtocolStep,"
            "\n)"
        )
        self._preamble_imports.add(
            "from cervellaswarm_lingua_universale.checker import ("
            "\n    SessionChecker,"
            "\n    ProtocolViolation,"
            "\n    SessionComplete,"
            "\n)"
        )
        self._preamble_imports.add("from typing import Optional")

        # Import message dataclasses used by this protocol
        from .codegen import _kind_to_message_class, _used_message_kinds
        kind_map = _kind_to_message_class()
        for kind in _used_message_kinds(protocol):
            cls_name = kind_map.get(kind)
            if cls_name:
                self._preamble_imports.add(
                    f"from cervellaswarm_lingua_universale.types import {cls_name}"
                )

        # 4. Assemble output lines with source annotation
        loc = self._loc_comment(node.loc)
        lines: list[str] = [f"# Protocol: {node.name}  {loc}"]

        # Emit declared properties as comments (verification is Lean 4's job)
        if node.properties:
            lines.append(f"# Declared properties ({len(node.properties)}):")
            for prop in node.properties:
                lines.append(f"#   - {type(prop).__name__}")

        # Protocol definition, role classes, session class
        for section in (proto_def, role_classes, session_class):
            for line in section.splitlines():
                lines.append(line)

        return lines

    def _ast_to_protocol(self, node: ProtocolNode) -> Protocol:
        """Transform a ``ProtocolNode`` AST into a runtime ``Protocol`` object.

        Maps StepNode -> ProtocolStep, ChoiceNode -> ProtocolChoice.
        Returns a ``Protocol`` instance ready for code generation.
        """
        from .protocols import Protocol, ProtocolChoice, ProtocolStep

        elements = self._transform_steps(node.steps)

        return Protocol(
            name=node.name,
            roles=node.roles,
            elements=elements,
        )

    def _transform_steps(
        self, steps: tuple[StepOrChoice, ...],
    ) -> tuple[ProtocolElement, ...]:
        """Transform AST step/choice nodes into runtime protocol elements."""
        from .protocols import ProtocolChoice, ProtocolStep

        result: list[object] = []
        for item in steps:
            if isinstance(item, StepNode):
                result.append(ProtocolStep(
                    sender=item.sender,
                    receiver=item.receiver,
                    message_kind=self._step_to_message_kind(item),
                    description=item.payload,
                ))
            elif isinstance(item, ChoiceNode):
                branches: dict[str, tuple[ProtocolStep, ...]] = {}
                for branch in item.branches:
                    branch_steps = tuple(
                        ProtocolStep(
                            sender=s.sender,
                            receiver=s.receiver,
                            message_kind=self._step_to_message_kind(s),
                            description=s.payload,
                        )
                        for s in branch.steps
                    )
                    branches[branch.label] = branch_steps
                result.append(ProtocolChoice(
                    decider=item.decider,
                    branches=branches,
                ))
        return tuple(result)

    @staticmethod
    def _step_to_message_kind(step: StepNode) -> MessageKind:
        """Map a StepNode's action + payload to a ``MessageKind`` enum value.

        Uses keyword-based heuristics on the action verb and payload text.
        Falls back to ``MessageKind.DM`` for unrecognized patterns.

        Mapping rules:
          - asks + "verify"/"audit"/"check" -> AUDIT_REQUEST
          - asks + "plan"                   -> PLAN_REQUEST
          - asks + "research"/"search"      -> RESEARCH_QUERY
          - asks (default)                  -> TASK_REQUEST
          - returns + "verdict"/"audit"     -> AUDIT_VERDICT
          - returns + "plan"/"proposal"     -> PLAN_PROPOSAL
          - returns + "report"/"research"   -> RESEARCH_REPORT
          - returns (default)               -> TASK_RESULT
          - tells + "decision"              -> PLAN_DECISION
          - tells (default)                 -> DM
          - proposes                        -> PLAN_PROPOSAL
          - sends + "shutdown"              -> SHUTDOWN_REQUEST
          - sends + "context"              -> CONTEXT_INJECT
          - sends + "broadcast"            -> BROADCAST
          - sends (default)                -> DM
        """
        from .types import MessageKind

        action = step.action
        payload = step.payload.lower()

        if action == "asks":
            if any(w in payload for w in ("verify", "audit", "check")):
                return MessageKind.AUDIT_REQUEST
            if "plan" in payload:
                return MessageKind.PLAN_REQUEST
            if any(w in payload for w in ("research", "search")):
                return MessageKind.RESEARCH_QUERY
            return MessageKind.TASK_REQUEST

        if action == "returns":
            if any(w in payload for w in ("verdict", "audit")):
                return MessageKind.AUDIT_VERDICT
            if any(w in payload for w in ("plan", "proposal")):
                return MessageKind.PLAN_PROPOSAL
            if any(w in payload for w in ("report", "research")):
                return MessageKind.RESEARCH_REPORT
            return MessageKind.TASK_RESULT

        if action == "tells":
            if "decision" in payload:
                return MessageKind.PLAN_DECISION
            return MessageKind.DM

        if action == "proposes":
            return MessageKind.PLAN_PROPOSAL

        if action == "sends":
            if "shutdown" in payload:
                return MessageKind.SHUTDOWN_REQUEST
            if "context" in payload:
                return MessageKind.CONTEXT_INJECT
            if "broadcast" in payload:
                return MessageKind.BROADCAST
            return MessageKind.DM

        return MessageKind.DM

    # ----------------------------------------------------------
    # Expr -> Python expression string
    # ----------------------------------------------------------

    def _expr_to_python(self, expr: Expr) -> str:
        """Convert any Expr AST node to a Python expression string.

        Always parenthesises binary sub-expressions to avoid precedence issues
        (STUDIO C2.1 risk mitigation).
        """
        if isinstance(expr, IdentExpr):
            return self._safe_ident(expr.name)

        if isinstance(expr, NumberExpr):
            return expr.value

        if isinstance(expr, StringExpr):
            # StringExpr.value already includes surrounding quotes
            return expr.value

        if isinstance(expr, AttrExpr):
            return f"{self._safe_ident(expr.obj)}.{self._safe_ident(expr.attr)}"

        if isinstance(expr, MethodCallExpr):
            obj = self._safe_ident(expr.obj)
            method = self._safe_ident(expr.method)
            args = ", ".join(self._expr_to_python(a) for a in expr.args)
            return f"{obj}.{method}({args})"

        if isinstance(expr, BinOpExpr):
            left = self._expr_to_python(expr.left)
            right = self._expr_to_python(expr.right)
            return f"({left}) {expr.op} ({right})"

        if isinstance(expr, NotExpr):
            operand = self._expr_to_python(expr.operand)
            return f"not ({operand})"

        if isinstance(expr, GroupExpr):
            inner = self._expr_to_python(expr.inner)
            return f"({inner})"

        raise TypeError(f"Unknown Expr type: {type(expr).__name__}")

    # ----------------------------------------------------------
    # TypeExpr -> Python type hint string
    # ----------------------------------------------------------

    def _type_to_python(self, tex: TypeExpr) -> str:
        """Convert a TypeExpr AST node to a Python type annotation string.

        Uses ``X | None`` (PEP 604, Python 3.10+) for optional types instead
        of ``Optional[X]``, avoiding the need to track ``from typing import
        Optional`` in the generated output.
        """
        if isinstance(tex, SimpleType):
            base = _LU_TYPE_MAP.get(tex.name, tex.name)
            if tex.optional:
                return f"{base} | None"
            return base

        if isinstance(tex, GenericType):
            base = _LU_GENERIC_MAP.get(tex.name, tex.name)
            # Fix P2: register preamble import for Confident[T]
            if tex.name == "Confident":
                self._preamble_imports.add(
                    "from cervellaswarm_lingua_universale.confidence"
                    " import Confident"
                )
            arg = self._type_to_python(tex.arg)
            inner = f"{base}[{arg}]"
            if tex.optional:
                return f"{inner} | None"
            return inner

        raise TypeError(f"Unknown TypeExpr type: {type(tex).__name__}")

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------

    @staticmethod
    def _loc_comment(loc: Loc) -> str:
        """Build a source-annotation comment ``# [LU:line:col]``."""
        return f"# [LU:{loc.line}:{loc.col}]"

    @staticmethod
    def _safe_ident(name: str) -> str:
        """Append trailing ``_`` if *name* is a Python keyword.

        Handles e.g. method name ``pass`` -> ``pass_``, ``class`` -> ``class_``.
        """
        if name in _PYTHON_KEYWORDS:
            return f"{name}_"
        return name

    def _contract_expr_to_python(self, expr: Expr) -> str:
        """Convert a contract expression to Python with kwargs lookup.

        Like ``_expr_to_python`` but top-level identifiers resolve to
        ``kwargs["name"]`` so that ``process(**kwargs)`` can evaluate
        contract guards against its keyword arguments.

        ``AttrExpr("task", "valid")`` becomes ``kwargs["task"].valid``
        (the object is looked up in kwargs, the attribute is accessed normally).
        """
        if isinstance(expr, IdentExpr):
            name = self._safe_ident(expr.name)
            return f'kwargs["{name}"]'

        if isinstance(expr, AttrExpr):
            obj = self._safe_ident(expr.obj)
            attr = self._safe_ident(expr.attr)
            return f'kwargs["{obj}"].{attr}'

        if isinstance(expr, MethodCallExpr):
            obj = self._safe_ident(expr.obj)
            method = self._safe_ident(expr.method)
            args = ", ".join(self._contract_expr_to_python(a) for a in expr.args)
            return f'kwargs["{obj}"].{method}({args})'

        # For all other expressions (BinOp, Not, Group, Number, String),
        # recurse normally but with contract-aware sub-expressions.
        if isinstance(expr, BinOpExpr):
            left = self._contract_expr_to_python(expr.left)
            right = self._contract_expr_to_python(expr.right)
            return f"({left}) {expr.op} ({right})"

        if isinstance(expr, NotExpr):
            operand = self._contract_expr_to_python(expr.operand)
            return f"not ({operand})"

        if isinstance(expr, GroupExpr):
            inner = self._contract_expr_to_python(expr.inner)
            return f"({inner})"

        # Literals (Number, String) don't need kwargs lookup
        return self._expr_to_python(expr)

    @staticmethod
    def _escape_contract_str(expr: str) -> str:
        """Escape a Python expression string for embedding in a string literal.

        Handles backslashes, double-quotes, newlines, and carriage returns so
        the generated ``ContractViolation("...")`` call is always valid Python.

        Aligned with ``codegen._escape_string`` (F10 finding, C2.3.1).
        """
        return (
            expr.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

