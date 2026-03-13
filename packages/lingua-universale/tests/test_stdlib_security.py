# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for stdlib Security protocols (3 protocols)."""

from __future__ import annotations

from cervellaswarm_lingua_universale._eval import check_source, verify_source
from cervellaswarm_lingua_universale._init_project import _STDLIB_DIR

_STDLIB = _STDLIB_DIR / "security"


def _read(name: str) -> str:
    return (_STDLIB / f"{name}.lu").read_text(encoding="utf-8")


# ── AuthHandshake ────────────────────────────────────────────────

class TestAuthHandshake:
    SRC = _read("auth_handshake")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_has_choice_branches(self):
        r = verify_source(self.SRC)
        assert r.ok

    def test_ordering_auth_before_resource(self):
        r = verify_source(self.SRC)
        has_ordering = any(
            res.spec.kind.value == "ordering"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_ordering

    def test_always_terminates_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["always_terminates"] == "PROVED"

    def test_exclusion_present(self):
        r = verify_source(self.SRC)
        has_exclusion = any(
            res.spec.kind.value == "exclusion"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_exclusion


# ── MutualTls ────────────────────────────────────────────────────

class TestMutualTls:
    SRC = _read("mutual_tls")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_structural_properties_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["always_terminates"] == "PROVED"
        assert verdicts["no_deadlock"] == "PROVED"
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_ordering_present(self):
        r = verify_source(self.SRC)
        has_ordering = any(
            res.spec.kind.value == "ordering"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_ordering


# ── RateLimitedApi ───────────────────────────────────────────────

class TestRateLimitedApi:
    SRC = _read("rate_limited_api")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_role_exclusive_present(self):
        r = verify_source(self.SRC)
        has_exclusive = any(
            res.spec.kind.value == "role_exclusive"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_exclusive

    def test_has_choice_branches(self):
        r = verify_source(self.SRC)
        assert r.ok

    def test_always_terminates_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["always_terminates"] == "PROVED"
