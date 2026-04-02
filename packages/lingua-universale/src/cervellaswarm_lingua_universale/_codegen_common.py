# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared helpers for code generation modules.

Extracts common traversal utilities used across codegen.py, codegen_json.py,
codegen_ts.py, lean4_bridge.py, and spec.py. Single source of truth.
"""

from __future__ import annotations

from collections.abc import Sequence

from .protocols import (
    MessageKind,
    Protocol,
    ProtocolChoice,
    ProtocolElement,
    ProtocolStep,
)


def collect_all_steps(
    elements: Sequence[ProtocolElement],
) -> list[ProtocolStep]:
    """Collect all ProtocolSteps from elements, including nested choice branches."""
    steps: list[ProtocolStep] = []
    for elem in elements:
        if isinstance(elem, ProtocolStep):
            steps.append(elem)
        elif isinstance(elem, ProtocolChoice):
            for branch_elems in elem.branches.values():
                steps.extend(collect_all_steps(branch_elems))
    return steps


def used_message_kinds(protocol: Protocol) -> list[MessageKind]:
    """Collect MessageKinds used in a protocol (preserving enum order)."""
    used: set[MessageKind] = set()
    for step in collect_all_steps(protocol.elements):
        used.add(step.message_kind)
    return [k for k in MessageKind if k in used]
