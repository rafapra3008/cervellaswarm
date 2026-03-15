# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Code generation bridge: .lu source -> Protocol -> target language.

Parses .lu files, converts AST to runtime Protocol objects via the compiler
bridge, and dispatches to target-specific generators (Python, TypeScript,
JSON Schema).

Architecture::

    .lu source -> parse() -> ProgramNode -> filter ProtocolNode(s)
        -> ASTCompiler._ast_to_protocol() -> Protocol
        -> _ast_properties_to_spec() -> ProtocolSpec | None
        -> target generator -> source code string

Design decision (S469, Guardiana-approved):
    Uses ``ASTCompiler._ast_to_protocol()`` (compiler bridge) instead of
    ``_eval._protocol_node_to_runtime()`` (eval bridge). The compiler bridge
    has richer MessageKind mapping (~30 keyword rules via payload heuristics)
    vs the eval bridge (5 flat action mappings). This ensures ``lu generate``
    output is consistent with ``lu compile``.

    The eval bridge is used by ``lu verify`` and produces different MessageKind
    values -- this is accepted because property checking only needs correct
    structure (sender/receiver/ordering), not precise MessageKind values.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .protocols import Protocol
    from .spec import ProtocolSpec


# -- Target aliases -----------------------------------------------------------

_TARGET_ALIASES: dict[str, str] = {
    "ts": "typescript",
    "json": "json-schema",
}

_VALID_TARGETS = frozenset({"python", "typescript", "json-schema"})

_TARGET_EXTENSIONS: dict[str, str] = {
    "python": ".py",
    "typescript": ".ts",
    "json-schema": ".json",
}


# -- Result dataclass ---------------------------------------------------------

@dataclass(frozen=True)
class GenerateResult:
    """Result of code generation for a single protocol."""

    protocol_name: str
    target: str
    source: str
    file_extension: str
    properties_included: bool


# -- Core bridge --------------------------------------------------------------

def _parse_to_protocols(
    source: str,
) -> list[tuple[Protocol, ProtocolSpec | None]]:
    """Parse LU source and extract Protocol + ProtocolSpec pairs.

    Uses the compiler bridge (``ASTCompiler._ast_to_protocol``) for rich
    MessageKind mapping. Properties are extracted via ``_ast_properties_to_spec``
    from ``_eval.py``.

    Raises ``ValueError`` if no protocol declarations are found.
    """
    from ._ast import ProtocolNode
    from ._compiler import ASTCompiler
    from ._eval import _ast_properties_to_spec
    from ._parser import parse

    program = parse(source)

    protocol_nodes = [
        decl for decl in program.declarations
        if isinstance(decl, ProtocolNode)
    ]

    if not protocol_nodes:
        raise ValueError("No protocol declarations found in source.")

    compiler = ASTCompiler()
    results: list[tuple[Protocol, ProtocolSpec | None]] = []

    for node in protocol_nodes:
        protocol = compiler._ast_to_protocol(node)
        spec = _ast_properties_to_spec(node)
        results.append((protocol, spec))

    return results


def _resolve_target(name: str) -> str:
    """Resolve target name, handling aliases.

    Raises ``ValueError`` for unknown targets.
    """
    resolved = _TARGET_ALIASES.get(name, name)
    if resolved not in _VALID_TARGETS:
        supported = sorted(_VALID_TARGETS | set(_TARGET_ALIASES))
        raise ValueError(
            f"Unknown target: {name!r}. "
            f"Supported targets: {', '.join(supported)}"
        )
    return resolved


# -- Generator dispatch -------------------------------------------------------

def _generate_one(
    protocol: Protocol,
    spec: ProtocolSpec | None,
    target: str,
) -> str:
    """Generate source code for a single protocol in the given target."""
    if target == "python":
        from .codegen import PythonGenerator
        return PythonGenerator().generate(protocol)

    if target == "typescript":
        from .codegen_ts import TypeScriptGenerator
        return TypeScriptGenerator().generate(protocol, properties=spec)

    if target == "json-schema":
        from .codegen_json import JSONSchemaGenerator
        return JSONSchemaGenerator().generate(protocol, properties=spec)

    raise ValueError(f"No generator for target: {target!r}")


# -- Public API ---------------------------------------------------------------

def generate_from_source(
    source: str,
    target: str,
) -> list[GenerateResult]:
    """Generate code from LU source string.

    Args:
        source: LU source code containing one or more protocol declarations.
        target: Target language (``python``, ``typescript``/``ts``,
                ``json-schema``/``json``).

    Returns:
        List of ``GenerateResult``, one per protocol in the source.

    Raises:
        ValueError: If no protocols found or target is unknown.
    """
    resolved = _resolve_target(target)
    protocols = _parse_to_protocols(source)
    ext = _TARGET_EXTENSIONS[resolved]

    results: list[GenerateResult] = []
    for protocol, spec in protocols:
        generated = _generate_one(protocol, spec, resolved)
        results.append(GenerateResult(
            protocol_name=protocol.name,
            target=resolved,
            source=generated,
            file_extension=ext,
            properties_included=spec is not None,
        ))

    return results


def generate_from_file(
    path: str | Path,
    target: str,
) -> list[GenerateResult]:
    """Generate code from a ``.lu`` file.

    Args:
        path: Path to a ``.lu`` file.
        target: Target language (``python``, ``typescript``/``ts``,
                ``json-schema``/``json``).

    Returns:
        List of ``GenerateResult``, one per protocol in the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If no protocols found or target is unknown.
    """
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    source = filepath.read_text(encoding="utf-8")
    return generate_from_source(source, target)
