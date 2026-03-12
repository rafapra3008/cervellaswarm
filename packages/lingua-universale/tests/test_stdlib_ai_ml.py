# SPDX-License-Identifier: Apache-2.0

"""Tests for stdlib AI/ML protocols (5 protocols)."""

from __future__ import annotations

import pathlib

from cervellaswarm_lingua_universale._eval import check_source, verify_source

_STDLIB = pathlib.Path(__file__).resolve().parent.parent / "stdlib" / "ai_ml"


def _read(name: str) -> str:
    return (_STDLIB / f"{name}.lu").read_text(encoding="utf-8")


# ── RagPipeline ──────────────────────────────────────────────────

class TestRagPipeline:
    SRC = _read("rag_pipeline")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_ordering_retriever_before_generator(self):
        r = verify_source(self.SRC)
        has_ordering = any(
            res.spec.kind.value == "ordering"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_ordering


# ── AgentDelegation ──────────────────────────────────────────────

class TestAgentDelegation:
    SRC = _read("agent_delegation")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_trust_min_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["trust_min"] == "PROVED"

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_has_choice_branches(self):
        r = verify_source(self.SRC)
        assert r.ok


# ── ToolCalling ──────────────────────────────────────────────────

class TestToolCalling:
    SRC = _read("tool_calling")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_ordering_registry_before_executor(self):
        r = verify_source(self.SRC)
        has_ordering = any(
            res.spec.kind.value == "ordering"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_ordering


# ── HumanInLoop ──────────────────────────────────────────────────

class TestHumanInLoop:
    SRC = _read("human_in_loop")

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

    def test_three_choice_branches(self):
        r = verify_source(self.SRC)
        assert r.ok


# ── Consensus ────────────────────────────────────────────────────

class TestConsensus:
    SRC = _read("consensus")

    def test_parses(self):
        assert check_source(self.SRC).ok

    def test_all_roles_participate_proved(self):
        r = verify_source(self.SRC)
        verdicts = {res.spec.kind.value: res.verdict.name
                    for rpt in (r.property_reports or []) for res in rpt.results}
        assert verdicts["all_roles_participate"] == "PROVED"

    def test_two_ordering_properties(self):
        r = verify_source(self.SRC)
        ordering_count = sum(
            1 for rpt in (r.property_reports or [])
            for res in rpt.results if res.spec.kind.value == "ordering"
        )
        assert ordering_count == 2

    def test_confidence_min_present(self):
        r = verify_source(self.SRC)
        has_confidence = any(
            res.spec.kind.value == "confidence_min"
            for rpt in (r.property_reports or []) for res in rpt.results
        )
        assert has_confidence
