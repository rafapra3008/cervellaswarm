# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for stdlib Communication protocols (5 protocols)."""

from __future__ import annotations

from cervellaswarm_lingua_universale._eval import check_source, verify_source
from cervellaswarm_lingua_universale._init_project import _STDLIB_DIR

_STDLIB = _STDLIB_DIR / "communication"


def _read(name: str) -> str:
    return (_STDLIB / f"{name}.lu").read_text(encoding="utf-8")


# ── RequestResponse ──────────────────────────────────────────────

class TestRequestResponse:
    SRC = _read("request_response")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_compiles(self):
        r = check_source(self.SRC)
        assert r.compiled is not None

    def test_always_terminates_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["always_terminates"] == "PROVED"

    def test_no_deadlock_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["no_deadlock"] == "PROVED"


# ── PingPong ─────────────────────────────────────────────────────

class TestPingPong:
    SRC = _read("ping_pong")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_compiles(self):
        r = check_source(self.SRC)
        assert r.compiled is not None

    def test_all_properties_proved(self):
        r = verify_source(self.SRC)
        for rpt in (r.property_reports or []):
            for res in rpt.results:
                assert res.verdict.name == "PROVED"


# ── PubSub ───────────────────────────────────────────────────────

class TestPubSub:
    SRC = _read("pub_sub")

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

    def test_all_properties_proved(self):
        r = verify_source(self.SRC)
        for rpt in (r.property_reports or []):
            for res in rpt.results:
                assert res.verdict.name == "PROVED"


# ── ScatterGather ────────────────────────────────────────────────

class TestScatterGather:
    SRC = _read("scatter_gather")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"


# ── Pipeline ─────────────────────────────────────────────────────

class TestPipeline:
    SRC = _read("pipeline")

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

    def test_ordering_properties_present(self):
        r = verify_source(self.SRC)
        ordering_count = sum(
            1 for rpt in (r.property_reports or [])
            for res in rpt.results if res.spec.kind.value == "ordering"
        )
        assert ordering_count == 3  # source<proc, proc<trans, trans<sink
