# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Runtime contract enforcement for compiled Lingua Universale programs.

The compiler (C2) emits ``if not cond: raise ContractViolation(...)`` guards
for every ``requires`` / ``ensures`` clause.  This module provides the single
exception class used by that generated code.

Design decisions (STUDIO C2.1, S412):
  - ``raise`` instead of ``assert`` -- contracts are NOT disableable with -O.
  - Zero external dependencies -- stdlib only, like the rest of the package.
  - Inline guards instead of decorators -- zero import overhead, zero magic.
"""

from __future__ import annotations


class ContractViolation(RuntimeError):
    """Raised when a Lingua Universale contract is violated at runtime.

    Attributes:
        condition: The contract expression that failed (human-readable).
        kind: ``"requires"`` (precondition) or ``"ensures"`` (postcondition).
        source: Source location string ``"line N, col M"`` from the ``.lu`` file.
    """

    __slots__ = ("condition", "kind", "source")

    def __init__(
        self,
        condition: str,
        *,
        kind: str = "requires",
        source: str = "",
    ) -> None:
        if kind not in ("requires", "ensures"):
            raise ValueError(
                f"kind must be 'requires' or 'ensures', got {kind!r}"
            )
        self.condition = condition
        self.kind = kind
        self.source = source
        msg = f"[LU Contract] {kind} violated: {condition}"
        if source:
            msg += f" (at {source})"
        super().__init__(msg)

    def __reduce__(self) -> tuple:
        """Support pickling with correct attribute reconstruction."""
        return (
            _reconstruct_contract_violation,
            (self.condition, self.kind, self.source),
        )


def _reconstruct_contract_violation(
    condition: str, kind: str, source: str
) -> ContractViolation:
    """Pickle helper -- reconstructs a ContractViolation from its attributes."""
    return ContractViolation(condition, kind=kind, source=source)
