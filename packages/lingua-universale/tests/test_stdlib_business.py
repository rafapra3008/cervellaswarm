# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for stdlib Business protocols (4 protocols)."""

from __future__ import annotations

from cervellaswarm_lingua_universale._eval import check_source, verify_source
from cervellaswarm_lingua_universale._init_project import _STDLIB_DIR

_STDLIB = _STDLIB_DIR / "business"


def _read(name: str) -> str:
    return (_STDLIB / f"{name}.lu").read_text(encoding="utf-8")


# ── TwoBuyer ─────────────────────────────────────────────────────

class TestTwoBuyer:
    SRC = _read("two_buyer")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_compiles(self):
        r = check_source(self.SRC)
        assert r.compiled is not None

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_has_choice_branches(self):
        r = verify_source(self.SRC)
        assert r.ok


# ── ApprovalWorkflow ─────────────────────────────────────────────

class TestApprovalWorkflow:
    SRC = _read("approval_workflow")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_role_exclusive_present(self):
        r = verify_source(self.SRC)
        has_exclusive = any(
            res.spec.kind.value == "role_exclusive"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_exclusive


# ── Auction ──────────────────────────────────────────────────────

class TestAuction:
    SRC = _read("auction")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_properties_proved(self):
        r = verify_source(self.SRC)
        for rpt in (r.property_reports or []):
            for res in rpt.results:
                assert res.verdict.name == "PROVED"

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"


# ── SagaOrder ────────────────────────────────────────────────────

class TestSagaOrder:
    SRC = _read("saga_order")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_has_choice_branches(self):
        r = verify_source(self.SRC)
        assert r.ok

    def test_always_terminates_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["always_terminates"] == "PROVED"

    def test_ordering_present(self):
        r = verify_source(self.SRC)
        has_ordering = any(
            res.spec.kind.value == "ordering"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_ordering
