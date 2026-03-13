# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for stdlib Data protocols (3 protocols)."""

from __future__ import annotations

from cervellaswarm_lingua_universale._eval import check_source, verify_source
from cervellaswarm_lingua_universale._init_project import _STDLIB_DIR

_STDLIB = _STDLIB_DIR / "data"


def _read(name: str) -> str:
    return (_STDLIB / f"{name}.lu").read_text(encoding="utf-8")


# ── CrudSafe ─────────────────────────────────────────────────────

class TestCrudSafe:
    SRC = _read("crud_safe")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_no_deletion_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["no_deletion"] == "PROVED"

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_all_core_properties_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["always_terminates"] == "PROVED"
        assert verdicts["no_deadlock"] == "PROVED"


# ── DataSync ─────────────────────────────────────────────────────

class TestDataSync:
    SRC = _read("data_sync")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_ordering_properties_present(self):
        r = verify_source(self.SRC)
        ordering_count = sum(
            1 for rpt in (r.property_reports or [])
            for res in rpt.results if res.spec.kind.value == "ordering"
        )
        assert ordering_count == 2  # primary<replica, replica<monitor


# ── CacheInvalidation ────────────────────────────────────────────

class TestCacheInvalidation:
    SRC = _read("cache_invalidation")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_has_choice_branches(self):
        r = check_source(self.SRC)
        assert r.compiled is not None

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_all_properties_proved(self):
        r = verify_source(self.SRC)
        for rpt in (r.property_reports or []):
            for res in rpt.results:
                assert res.verdict.name == "PROVED"
