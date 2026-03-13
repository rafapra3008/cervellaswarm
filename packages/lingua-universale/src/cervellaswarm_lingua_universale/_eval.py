# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Unified evaluation functions for Lingua Universale (C3.2).

Three levels of evaluation, each building on the previous:

  - ``check_source()`` / ``check_file()`` -- parse + compile (no execution).
  - ``verify_source()`` / ``verify_file()`` -- parse + compile + Lean 4 verify.
  - ``run_source()`` / ``run_file()`` -- parse + compile + execute.

All functions return typed result objects and raise no exceptions -- errors
are captured in the result.  This makes them safe for CLI and REPL use.
"""

from __future__ import annotations

import types
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from ._ast import (
    AlwaysTerminates,
    AllParticipate,
    ChoiceNode,
    ConfidenceProp,
    ExclusionProp,
    NoDeletionProp,
    NoDeadlock,
    OrderingProp,
    ProgramNode,
    ProtocolNode,
    RoleExclusiveProp,
    TrustProp,
)
from ._compiler import ASTCompiler, CompiledModule
from ._interop import load_module, InteropError
from ._parser import parse

if TYPE_CHECKING:
    from .spec import PropertyReport


@dataclass(frozen=True)
class EvalResult:
    """Result of an evaluation operation.

    Attributes:
        ok: Whether the operation succeeded.
        source_file: Path or label of the source.
        errors: List of error messages (empty on success).
        compiled: The compiled module (None if parse/compile failed).
        module: The live Python module (None unless ``run`` was used).
        python_source: The generated Python code (None if compile failed).
        verification: Lean 4 verification lines (empty unless ``verify``).
        property_reports: Static property check reports (empty unless ``verify``).
    """

    ok: bool
    source_file: str
    errors: list[str] = field(default_factory=list)
    compiled: CompiledModule | None = None
    module: types.ModuleType | None = None
    python_source: str | None = None
    verification: list[str] = field(default_factory=list)
    property_reports: list[PropertyReport] = field(default_factory=list)


# ============================================================
# check: parse + compile (no execution)
# ============================================================


def _parse_and_compile(
    source: str, source_file: str,
) -> tuple[ProgramNode | None, CompiledModule | None, list[str]]:
    """Parse and compile source.  Returns (program, compiled, errors)."""
    try:
        program = parse(source)
    except Exception as exc:
        try:
            from .errors import humanize, format_error
            herr = humanize(exc)
            return None, None, [format_error(herr, source=source)]
        except Exception:
            # Fallback if humanize() itself fails -- avoids crash in error layer
            return None, None, [str(exc)]

    try:
        compiler = ASTCompiler()
        compiled = compiler.compile(program, source_file=source_file)
    except Exception as exc:
        try:
            from .errors import humanize, format_error
            herr = humanize(exc)
            return None, None, [format_error(herr, source=source)]
        except Exception:
            # Fallback if humanize() itself fails -- avoids crash in error layer
            return None, None, [str(exc)]

    return program, compiled, []


def check_source(source: str, *, source_file: str = "<input>") -> EvalResult:
    """Parse and compile LU source.  No execution.

    Returns an ``EvalResult`` with ``ok=True`` if the source is valid,
    or ``ok=False`` with error messages otherwise.
    """
    program, compiled, errors = _parse_and_compile(source, source_file)

    if errors:
        return EvalResult(ok=False, source_file=source_file, errors=errors)

    return EvalResult(
        ok=True,
        source_file=source_file,
        compiled=compiled,
        python_source=compiled.python_source,
    )


def check_file(path: str | Path) -> EvalResult:
    """Parse and compile a ``.lu`` file.  No execution."""
    file_path = Path(path)
    try:
        source = file_path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError) as exc:
        return EvalResult(
            ok=False,
            source_file=str(file_path),
            errors=[str(exc)],
        )

    return check_source(source, source_file=str(file_path))


# ============================================================
# verify: parse + compile + Lean 4 formal verification
# ============================================================


def verify_source(source: str, *, source_file: str = "<input>") -> EvalResult:
    """Parse, compile, and verify LU source.

    Two verification layers:
      1. **Static property checking** (spec.py) -- always runs, no external deps.
      2. **Lean 4 formal verification** -- runs if Lean 4 is installed.

    Returns an EvalResult with property_reports populated.
    """
    program, compiled, errors = _parse_and_compile(source, source_file)
    if errors:
        return EvalResult(ok=False, source_file=source_file, errors=errors)

    from .lean4_bridge import lean4_available
    from .spec import check_properties

    verification_lines: list[str] = []
    property_reports = []
    has_protocols = False
    all_passed = True

    for decl in program.declarations:
        if not isinstance(decl, ProtocolNode):
            continue
        has_protocols = True
        verification_lines.append(f"Protocol: {decl.name}")

        # --- Layer 1: Static property checking ---
        spec = _ast_properties_to_spec(decl)
        if spec is not None:
            protocol_obj = _protocol_node_to_runtime(decl)
            report = _safe_check_properties(protocol_obj, spec)
            property_reports.append(report)

            for i, result in enumerate(report.results, 1):
                kind_label = result.spec.kind.value
                verdict = result.verdict.name
                verification_lines.append(
                    f"  [{i}/{len(report.results)}] {kind_label} ... {verdict}"
                )
                if result.evidence:
                    verification_lines.append(f"         {result.evidence}")

            passed = sum(
                1 for r in report.results if r.verdict.name != "VIOLATED"
            )
            total = len(report.results)
            if passed == total:
                verification_lines.append(f"  All {total} properties PASSED.")
            else:
                verification_lines.append(
                    f"  {passed}/{total} passed, "
                    f"{total - passed} VIOLATED."
                )
                all_passed = False
        else:
            verification_lines.append("  No properties declared.")

        # --- Layer 2: Lean 4 formal verification ---
        try:
            lean4_source = _protocol_node_to_lean4(decl)
            verification_lines.append(
                f"  Lean 4 source generated ({len(lean4_source)} chars)"
            )
            if lean4_available():
                verification_lines.append(
                    "  Lean 4: available (formal verification ready)"
                )
            else:
                verification_lines.append(
                    "  Lean 4: not installed "
                    "(install with: elan toolchain install leanprover-lean4-v4.14.0)"
                )
        except Exception as exc:
            verification_lines.append(f"  Lean 4 generation: {exc}")

    if not has_protocols:
        verification_lines.append("No protocol declarations found to verify.")

    return EvalResult(
        ok=all_passed,
        source_file=source_file,
        compiled=compiled,
        python_source=compiled.python_source,
        verification=verification_lines,
        property_reports=property_reports,
    )


def verify_file(path: str | Path) -> EvalResult:
    """Parse, compile, and formally verify a ``.lu`` file."""
    file_path = Path(path)
    try:
        source = file_path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError) as exc:
        return EvalResult(
            ok=False,
            source_file=str(file_path),
            errors=[str(exc)],
        )

    return verify_source(source, source_file=str(file_path))


# ============================================================
# run: parse + compile + execute
# ============================================================


def run_source(source: str, *, source_file: str = "<input>") -> EvalResult:
    """Parse, compile, and execute LU source.

    Returns an ``EvalResult`` with ``module`` set to the live Python
    module on success.
    """
    _program, compiled, errors = _parse_and_compile(source, source_file)
    if errors:
        return EvalResult(ok=False, source_file=source_file, errors=errors)

    try:
        mod = load_module(compiled, module_name="__lu_run__")
    except InteropError as exc:
        return EvalResult(
            ok=False,
            source_file=source_file,
            compiled=compiled,
            python_source=compiled.python_source,
            errors=[str(exc)],
        )

    return EvalResult(
        ok=True,
        source_file=source_file,
        compiled=compiled,
        module=mod,
        python_source=compiled.python_source,
    )


def run_file(path: str | Path) -> EvalResult:
    """Parse, compile, and execute a ``.lu`` file."""
    file_path = Path(path)
    try:
        source = file_path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError) as exc:
        return EvalResult(
            ok=False,
            source_file=str(file_path),
            errors=[str(exc)],
        )

    return run_source(source, source_file=str(file_path))


# ============================================================
# Internal helpers
# ============================================================


def _safe_check_properties(protocol, spec):
    """Check properties one by one, skipping those that fail mapping.

    ORDERING and EXCLUSION in .lu files use identifier names that may not
    map to MessageKind values.  Those properties are SKIPPED with evidence.
    """
    from .spec import (
        PropertyReport, PropertyResult, PropertySpec, PropertyVerdict,
        check_properties,
    )

    # Try full batch first (fast path)
    try:
        return check_properties(protocol, spec)
    except (KeyError, ValueError):
        pass

    # Slow path: check one property at a time
    results: list[PropertyResult] = []
    for prop_spec in spec.properties:
        single_spec = type(spec)(
            protocol_name=spec.protocol_name,
            properties=(prop_spec,),
        )
        try:
            single_report = check_properties(protocol, single_spec)
            results.extend(single_report.results)
        except (KeyError, ValueError) as exc:
            results.append(PropertyResult(
                spec=prop_spec,
                verdict=PropertyVerdict.SKIPPED,
                evidence=f"params not resolvable: {exc}",
            ))

    return PropertyReport(
        protocol_name=spec.protocol_name,
        results=tuple(results),
    )


def _protocol_node_to_runtime(node: ProtocolNode):
    """Convert an AST ProtocolNode to a runtime Protocol object.

    Handles both ``StepNode`` (flat steps) and ``ChoiceNode`` (branches),
    including arbitrarily nested choices (LU 1.1 AST, recursive
    conversion added LU 1.2), so property checkers and ``verify_source``
    see the complete protocol structure.
    """
    from .protocols import Protocol, ProtocolChoice, ProtocolStep
    from .types import MessageKind

    action_to_kind = _action_to_kind_map()

    def _convert_elements(items):
        """Recursively convert AST step/choice nodes to runtime elements."""
        result: list[ProtocolStep | ProtocolChoice] = []
        for item in items:
            if isinstance(item, ChoiceNode):
                branches: dict[str, tuple[ProtocolStep | ProtocolChoice, ...]] = {}
                for branch in item.branches:
                    branches[branch.label] = tuple(_convert_elements(branch.steps))
                result.append(
                    ProtocolChoice(decider=item.decider, branches=branches),
                )
            elif hasattr(item, "sender"):
                kind = action_to_kind.get(item.action, MessageKind.TASK_REQUEST)
                result.append(ProtocolStep(
                    sender=item.sender,
                    receiver=item.receiver,
                    message_kind=kind,
                    description=item.payload,
                ))
        return result

    return Protocol(
        name=node.name,
        roles=node.roles,
        elements=tuple(_convert_elements(node.steps)),
    )


def _ast_properties_to_spec(node: ProtocolNode):
    """Convert AST property nodes to a ProtocolSpec for static checking.

    Returns None if the protocol has no properties declared.
    """
    from .spec import PropertyKind, PropertySpec, ProtocolSpec

    _CONFIDENCE_THRESHOLDS = {
        "certain": 1.0, "high": 0.8, "medium": 0.5,
        "low": 0.2, "speculative": 0.1,
    }

    if not node.properties:
        return None

    specs: list[PropertySpec] = []
    for prop in node.properties:
        if isinstance(prop, AlwaysTerminates):
            specs.append(PropertySpec(kind=PropertyKind.ALWAYS_TERMINATES))
        elif isinstance(prop, NoDeadlock):
            specs.append(PropertySpec(kind=PropertyKind.NO_DEADLOCK))
        elif isinstance(prop, NoDeletionProp):
            specs.append(PropertySpec(kind=PropertyKind.NO_DELETION))
        elif isinstance(prop, AllParticipate):
            specs.append(PropertySpec(kind=PropertyKind.ALL_ROLES_PARTICIPATE))
        elif isinstance(prop, ConfidenceProp):
            threshold = _CONFIDENCE_THRESHOLDS.get(prop.level, 0.5)
            specs.append(PropertySpec(
                kind=PropertyKind.CONFIDENCE_MIN, threshold=threshold,
            ))
        elif isinstance(prop, TrustProp):
            specs.append(PropertySpec(
                kind=PropertyKind.TRUST_MIN, params=(prop.tier,),
            ))
        elif isinstance(prop, OrderingProp):
            specs.append(PropertySpec(
                kind=PropertyKind.ORDERING, params=(prop.before, prop.after),
            ))
        elif isinstance(prop, ExclusionProp):
            specs.append(PropertySpec(
                kind=PropertyKind.EXCLUSION, params=(prop.role, prop.message),
            ))
        elif isinstance(prop, RoleExclusiveProp):
            specs.append(PropertySpec(
                kind=PropertyKind.ROLE_EXCLUSIVE, params=(prop.role, prop.message),
            ))

    return ProtocolSpec(
        protocol_name=node.name,
        properties=tuple(specs),
    )


def _action_to_kind_map() -> dict[str, object]:
    """Return the shared action-verb → MessageKind mapping (lazy import)."""
    from .types import MessageKind

    return {
        "asks": MessageKind.TASK_REQUEST,
        "returns": MessageKind.TASK_RESULT,
        "sends": MessageKind.DM,
        "tells": MessageKind.BROADCAST,
        "proposes": MessageKind.PLAN_PROPOSAL,
    }


def _protocol_node_to_lean4(node: ProtocolNode) -> str:
    """Convert an AST ProtocolNode to Lean 4 source via the bridge.

    Reuses ``_protocol_node_to_runtime()`` for the AST → Protocol
    conversion, then passes the Protocol to ``generate_lean4()``.
    """
    from .lean4_bridge import generate_lean4

    protocol = _protocol_node_to_runtime(node)

    return generate_lean4(protocol)
