# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""lu visualize -- generate diagrams from .lu protocol files.

Supported formats:
  - mermaid: Mermaid sequence diagram (renders on GitHub, GitLab, Notion)

Usage:
    lu visualize protocol.lu                   # Mermaid to stdout
    lu visualize protocol.lu -o diagram.md     # save to file
    lu visualize protocol.lu --format mermaid  # explicit format
"""

from __future__ import annotations

from pathlib import Path

from ._ast import (
    ChoiceNode,
    ProgramNode,
    ProtocolNode,
    StepNode,
    StepOrChoice,
)


# ---------------------------------------------------------------------------
# Mermaid sequence diagram generator
# ---------------------------------------------------------------------------

def _sanitize_mermaid_label(text: str) -> str:
    """Escape characters that break Mermaid sequence diagram labels."""
    # Mermaid treats : ; # as syntax -- escape them
    for ch in (":", ";", "#"):
        text = text.replace(ch, f"&{ord(ch):x};")
    return text


def _mermaid_action_label(step: StepNode) -> str:
    """Build a readable label for a protocol step."""
    payload = step.payload.replace("_", " ")
    return _sanitize_mermaid_label(f"{step.action} {payload}")


def _render_steps_mermaid(
    steps: tuple[StepOrChoice, ...],
    lines: list[str],
    indent: str = "    ",
) -> None:
    """Recursively render protocol steps as Mermaid sequence diagram lines."""
    for step in steps:
        if isinstance(step, StepNode):
            label = _mermaid_action_label(step)
            lines.append(f"{indent}{step.sender}->>+{step.receiver}: {label}")
        elif isinstance(step, ChoiceNode):
            for i, branch in enumerate(step.branches):
                keyword = "alt" if i == 0 else "else"
                lines.append(f"{indent}{keyword} {branch.label} ({step.decider} decides)")
                _render_steps_mermaid(branch.steps, lines, indent + "    ")
            lines.append(f"{indent}end")


def generate_mermaid(protocol: ProtocolNode) -> str:
    """Generate a Mermaid sequence diagram from a ProtocolNode AST.

    Returns the complete Mermaid diagram as a string (without fences).
    """
    lines: list[str] = []

    lines.append("sequenceDiagram")

    # Participants in declared order
    for role in protocol.roles:
        lines.append(f"    participant {role}")

    lines.append("")

    # Protocol steps
    _render_steps_mermaid(protocol.steps, lines)

    return "\n".join(lines)


def generate_mermaid_fenced(protocol: ProtocolNode) -> str:
    """Generate a Mermaid diagram wrapped in markdown fences.

    Suitable for direct embedding in .md files (renders on GitHub).
    """
    diagram = generate_mermaid(protocol)
    return f"```mermaid\n{diagram}\n```"


# ---------------------------------------------------------------------------
# High-level API: source/file → diagram
# ---------------------------------------------------------------------------

def visualize_source(
    source: str,
    *,
    fmt: str = "mermaid",
    fenced: bool = False,
) -> str:
    """Generate a diagram from .lu source text.

    Args:
        source: The .lu source code.
        fmt: Output format ("mermaid").
        fenced: Wrap in markdown code fences (```mermaid ... ```).

    Returns:
        The diagram as a string.

    Raises:
        ValueError: If no protocols found or format unsupported.
    """
    from ._parser import parse

    program: ProgramNode = parse(source)

    protocols = [
        node for node in program.declarations
        if isinstance(node, ProtocolNode)
    ]

    if not protocols:
        raise ValueError("No protocol declarations found in source")

    if len(protocols) > 1:
        import sys
        print(
            f"Warning: {len(protocols)} protocols found, visualizing first "
            f"({protocols[0].name!r}). Use --protocol to select.",
            file=sys.stderr,
        )
    protocol = protocols[0]

    if fmt == "mermaid":
        if fenced:
            return generate_mermaid_fenced(protocol)
        return generate_mermaid(protocol)
    else:
        raise ValueError(f"Unsupported format: {fmt!r} (available: mermaid)")


def visualize_file(
    path: str | Path,
    *,
    fmt: str = "mermaid",
    fenced: bool = False,
) -> str:
    """Generate a diagram from a .lu file.

    Args:
        path: Path to a .lu file.
        fmt: Output format ("mermaid").
        fenced: Wrap in markdown code fences.

    Returns:
        The diagram as a string.
    """
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    return visualize_source(source, fmt=fmt, fenced=fenced)
