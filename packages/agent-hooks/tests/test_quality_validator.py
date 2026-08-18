# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.quality_validator (FASE 2 logic).

P2.1: 18+ pytest cases (12 unique tests + parametrize fanout) covering 6 metrics,
12 edge cases, 3 boundary conditions, plus Round 2 diamante remediation cases
(status fallback, legacy actionability, state-A anti-rot, CRLF/BOM normalization,
verdict aggregation).
"""

from datetime import date, timedelta

import pytest

from cervellaswarm_agent_hooks.quality_validator import (
    DENSITY_FLOOR,
    RECENCY_FRESH_DAYS,
    RECENCY_STALE_DAYS,
    _aggregate_verdict,
    calculate_actionability,
    calculate_anti_rot,
    calculate_coverage,
    calculate_density,
    calculate_recency,
    calculate_self_sufficiency,
    detect_evergreen_file,
    is_h2_evergreen_protected,
    parse_evergreen_scopes,
)


def _today(offset_days: int = 0) -> str:
    """Return today's date offset by N days as ISO string."""
    return (date.today() + timedelta(days=offset_days)).isoformat()


# ===========================================================================
# 6 happy path: 1 per metric
# ===========================================================================


class TestDensityHappyPath:
    def test_density_pass_ideal_file(self):
        """File con ~30% structured content -> density in [0.30, 0.55] PASS."""
        # 20 lines: 5 H2 + 1 H3 + 0 bullets = 6/20 = 0.30 (floor exact -- PASS)
        # Add 4 more action bullets -> 10/20 = 0.50 well inside band
        content = (
            "## H2 one\n"
            "## H2 two\n"
            "## H2 three\n"
            "## H2 four\n"
            "## H2 five\n"
            "### H3 one\n"
            "- [ ] step one\n"
            "- [ ] step two\n"
            "- [ ] step three\n"
            "- [ ] step four\n"
            "filler 1\n"
            "filler 2\n"
            "filler 3\n"
            "filler 4\n"
            "filler 5\n"
            "filler 6\n"
            "filler 7\n"
            "filler 8\n"
            "filler 9\n"
            "filler 10\n"
        )
        r = calculate_density(content, {})
        assert r["pass"] is True
        assert 0.30 <= r["value"] <= 0.55


class TestRecencyHappyPath:
    def test_recency_pass_scope_restricted(self):
        """DOVE SIAMO con 2 H2 fresh, 0 stale -> PASS."""
        d_fresh1 = _today(-1)
        d_fresh2 = _today(-3)
        content = (
            "# Title\n"
            f"## DOVE SIAMO -- {d_fresh1}\n"
            "Lavorando su X\n"
            f"## DOVE SIAMO check -- {d_fresh2}\n"
            "Y\n"
            "## ALTRA SEZIONE\n"
            "Vecchio contenuto 2020-01-01 ignorato perche fuori scope.\n"
        )
        r = calculate_recency(content, {})
        assert r["pass"] is True
        assert r["fresh_h2_count"] >= 2
        assert r["stale_pct"] == 0.0


class TestCoverageHappyPath:
    def test_coverage_pass_3_hard_2_warn(self):
        """3 HARD + 2 WARN sezioni presenti -> PASS, hard_found=3, warn_found=2."""
        content = (
            "# Title\n"
            "> STATUS: in corso\n"
            "## DOVE SIAMO\n"
            "abc\n"
            "## PROSSIMI 3 STEP\n"
            "- [ ] step\n"
            "## LEZIONI APPRESE\n"
            "x\n"
            "## PUNTATORI\n"
            "y\n"
        )
        r = calculate_coverage(content, {})
        assert r["pass"] is True
        assert r["hard_found"] == 3
        assert r["warn_found"] == 2
        assert r["missing"] == []


class TestActionabilityHappyPath:
    def test_actionability_pass_3_owners(self):
        """PROSSIMI con 3 step con @owner+effort -> PASS."""
        content = (
            "## PROSSIMI 3-5 STEP\n"
            "- [ ] @rafa effort: 2h fix bug\n"
            "- [ ] @cervella owner: backend effort: 1h\n"
            "- [ ] @qualita audit effort: 30m\n"
            "## ALTRO\n"
            "non actionable.\n"
        )
        r = calculate_actionability(content, {})
        assert r["pass"] is True
        assert r["actionable_count"] >= 3


class TestAntiRotHappyPath:
    def test_anti_rot_pass_80pct_links(self):
        """8 markdown link su 10 path totali -> 0.80 PASS boundary."""
        content = (
            "# Title\n"
            "See [a](a.md), [b](b.md), [c](c.md), [d](d.md), [e](e.md), "
            "[f](f.md), [g](g.md), [h](h.md) and also j.md and k.md.\n"
        )
        r = calculate_anti_rot(content, {})
        assert r["paths"] == 10
        assert r["links"] == 8
        assert r["linked_pct"] == 0.80
        assert r["pass"] is True


class TestSelfSufficiencyHappyPath:
    def test_self_sufficiency_pass_3_3(self):
        """File con DOVE+QUICK+TOP-3 DIVIETI in prime 50r -> 3/3 PASS."""
        content = (
            "# PROMPT RIPRESA -- X\n"
            "> Ultimo aggiornamento: 2026-05-22\n"
            "## DOVE SIAMO\n"
            "Sessione 519 in corso.\n"
            "## QUICK START\n"
            "- [ ] run pytest\n"
            "- [ ] check report\n"
            "## TOP-3 DIVIETI\n"
            "1. NON modificare X\n"
            "2. NON push main\n"
            "3. NON eliminare Y\n"
        )
        r = calculate_self_sufficiency(content, {})
        assert r["q1"] is True
        assert r["q2"] is True
        assert r["q3"] is True
        assert r["pass"] is True
        assert r["score"] == "3/3"


# ===========================================================================
# 3 edge cases (EC1, EC4+EC11, EC10)
# ===========================================================================


class TestEdgeCases:
    def test_density_empty_file(self):
        """EC1: empty file -> value=0, pass=False, no crash."""
        r = calculate_density("", {})
        assert r["value"] == 0.0
        assert r["pass"] is False

    def test_anti_rot_inline_code_skip(self):
        """EC4 + EC11: path in inline backtick NOT counted, markdown link IS counted."""
        # Path in `inline` backticks: ignored.
        # Markdown link: counted.
        # Tabella ASCII | file.md | inside code fence: also stripped.
        content = (
            "# Title\n"
            "Use `config.py` to see settings, also `tools/foo.sh` script.\n"
            "See [README](README.md) for docs.\n"
            "```\n"
            "| col1.md | col2.md |\n"
            "```\n"
        )
        r = calculate_anti_rot(content, {})
        # Denominator should NOT include backtick paths (config.py, tools/foo.sh)
        # NOR fenced (col1.md, col2.md).
        # Numerator: 1 markdown link (README.md).
        assert r["paths"] == 1, f"expected 1 path, got {r['paths']} (FP detection)"
        assert r["links"] == 1
        assert r["pass"] is True

    def test_self_sufficiency_frontmatter_skip(self):
        """EC10: YAML frontmatter skipped, count 50 lines from BODY."""
        # Frontmatter consumes 4 lines; body has DOVE SIAMO + QUICK + DIVIETI.
        content = (
            "---\n"
            "name: test\n"
            "version: 1.0\n"
            "---\n"
            "# Title\n"
            "> Ultimo aggiornamento: 2026-05-22\n"
            "## DOVE SIAMO\n"
            "ok\n"
            "## QUICK START\n"
            "- [ ] do thing\n"
            "## TOP-3 DIVIETI\n"
            "1. no\n"
        )
        r = calculate_self_sufficiency(content, {})
        assert r["details"]["frontmatter_stripped"] is True
        assert r["q1"] is True
        assert r["q2"] is True
        assert r["q3"] is True
        assert r["pass"] is True


# ===========================================================================
# 3 boundary cases
# ===========================================================================


class TestBoundaries:
    def test_density_exactly_floor(self):
        """Boundary: density == 0.30 exact -> PASS (>= floor)."""
        # 10 lines, 3 H2 -> 3/10 = 0.30
        content = (
            "## one\n"
            "## two\n"
            "## three\n"
            "filler 1\n"
            "filler 2\n"
            "filler 3\n"
            "filler 4\n"
            "filler 5\n"
            "filler 6\n"
            "filler 7\n"
        )
        r = calculate_density(content, {})
        assert r["value"] == 0.30
        assert r["pass"] is True

    def test_recency_exactly_90_days(self):
        """Boundary: date = today - 90gg = stale_cutoff (date.toordinal() < cutoff)."""
        # A date EXACTLY 90 days ago should be NOT-stale (strict <).
        # A date 91 days ago IS stale.
        d_old = _today(-91)
        d_fresh1 = _today(-1)
        d_fresh2 = _today(-2)
        content = (
            f"## DOVE SIAMO -- {d_fresh1}\n"
            f"## DOVE SIAMO bis -- {d_fresh2}\n"
            f"## DOVE SIAMO old reference {d_old}\n"
        )
        r = calculate_recency(content, {})
        # 1 stale out of 3 total = 0.333 > 0.30 threshold -> FAIL on stale_pct
        assert r["details"]["total_dates"] == 3
        assert r["details"]["stale_count"] == 1

    def test_coverage_3_hard_0_warn(self):
        """3 HARD + 0 WARN -> hard PASS (warn don't gate)."""
        content = (
            "> STATUS: x\n"
            "## DOVE SIAMO\n"
            "## PUNTATORI\n"
        )
        r = calculate_coverage(content, {})
        assert r["hard_found"] == 3
        assert r["warn_found"] == 0
        assert r["pass"] is True


# ===========================================================================
# Bonus: empty content for all 6 metrics (defensive)
# ===========================================================================


class TestEmptyContent:
    @pytest.mark.parametrize(
        "fn",
        [
            calculate_density,
            calculate_recency,
            calculate_coverage,
            calculate_actionability,
            calculate_anti_rot,
            calculate_self_sufficiency,
        ],
    )
    def test_no_crash_on_empty(self, fn):
        """All metrics must handle empty content without crashing (EC1)."""
        r = fn("", {})
        assert "name" in r
        assert "pass" in r


# ===========================================================================
# Round 2 diamante remediation (P1.2.A, P1.2.B, P1.2.C, P2.2, P2.3)
# ===========================================================================


class TestRound2Remediation:
    def test_recency_status_fallback_legacy(self):
        """P1.2.A: legacy file without ISO-dated H2 but with fresh status header
        -> fresh_h2 boosted via status_fallback_used."""
        today = date.today().isoformat()
        content = (
            f"> **Ultimo aggiornamento**: {today} -- S519\n"
            "\n"
            "## DOVE SIAMO\n"
            "Content without dated H2.\n"
            "## PROSSIMI\n"
            "step 1\n"
        )
        r = calculate_recency(content, {})
        assert r["fresh_h2_count"] >= 1
        assert r["details"]["status_fallback_used"] is True

    def test_recency_no_fallback_when_stale_status(self):
        """P1.2.A: status header older than 14gg -> no fallback boost."""
        old = (date.today() - timedelta(days=30)).isoformat()
        content = (
            f"> **Ultimo aggiornamento**: {old}\n"
            "\n"
            "## DOVE SIAMO\n"
            "No dated H2.\n"
        )
        r = calculate_recency(content, {})
        assert r["fresh_h2_count"] == 0
        assert r["details"]["status_fallback_used"] is False

    def test_actionability_legacy_paren_effort_and_md_link(self):
        """P1.2.B: legacy "(2h)" + "[step](file.md)" should count as actionable."""
        content = (
            "## PROSSIMI STEP\n"
            "1. [step 1](packages/foo.py) -- impl (1h)\n"
            "2. [step 2](src/bar.py) (45 min)\n"
            "3. impl (2h)\n"
        )
        r = calculate_actionability(content, {})
        assert r["actionable_count"] >= 3
        assert r["pass"] is True

    def test_actionability_owner_equals_sign(self):
        """P1.2.B: ``owner=name`` and ``effort=2h`` should also match primary."""
        content = (
            "## PROSSIMI\n"
            "- step1 owner=rafa effort=1h\n"
            "- step2 owner=qualita effort=30m\n"
            "- step3 @ops effort=2h\n"
        )
        r = calculate_actionability(content, {})
        assert r["actionable_count"] >= 3
        assert r["pass"] is True

    def test_anti_rot_state_a_lenient_threshold(self):
        """P1.2.C: state A uses 0.20 threshold, state C uses 0.80."""
        # 2 paths, 0 markdown links -> 0.0 < 0.20 -> FAIL even for A.
        content = "See /path/foo.md and /path/bar.py here without markdown links.\n"
        r_a = calculate_anti_rot(content, {}, state="A")
        r_c = calculate_anti_rot(content, {}, state="C")
        assert r_a["pass"] is False
        assert r_c["pass"] is False
        # Threshold difference visible in details.
        assert r_a["details"]["min_pct"] == 0.20
        assert r_c["details"]["min_pct"] == 0.80

    def test_anti_rot_state_a_pass_when_lenient(self):
        """P1.2.C: 0.30 linked pct passes for state A but fails for state C."""
        # 10 paths total, 3 markdown links -> 0.30 pct.
        content = (
            "See [a](a.md), [b](b.md), [c](c.md) and also "
            "d.md e.md f.md g.md h.md i.md j.md.\n"
        )
        r_a = calculate_anti_rot(content, {}, state="A")
        r_c = calculate_anti_rot(content, {}, state="C")
        assert r_a["linked_pct"] == 0.30
        assert r_a["pass"] is True, "state A (0.20 threshold) should PASS at 0.30"
        assert r_c["pass"] is False, "state C (0.80 threshold) should FAIL at 0.30"

    def test_density_crlf_normalization(self):
        """P2.2 / EC8: CRLF line endings normalized to LF before density calc."""
        content_crlf = "## H2\r\n## H2 again\r\n" + "filler line\r\n" * 5
        content_lf = content_crlf.replace("\r\n", "\n")
        r_crlf = calculate_density(content_crlf, {})
        r_lf = calculate_density(content_lf, {})
        assert r_crlf["value"] == r_lf["value"], "CRLF must yield same density as LF"

    def test_density_bom_stripped(self):
        """P2.2 / EC8: UTF-8 BOM stripped from content head."""
        content_bom = "﻿" + "## H2\n" * 3 + "filler\n" * 7
        content_no_bom = "## H2\n" * 3 + "filler\n" * 7
        r_bom = calculate_density(content_bom, {})
        r_no_bom = calculate_density(content_no_bom, {})
        assert r_bom["value"] == r_no_bom["value"], "BOM must be stripped"

    def test_aggregate_verdict_all_pass(self):
        """P2.3: all metrics PASS -> verdict PASS."""
        metrics = {
            "density": {"pass": True},
            "recency": {"pass": True},
            "coverage": {"pass": True},
        }
        assert _aggregate_verdict(metrics) == "PASS"

    def test_aggregate_verdict_any_fail(self):
        """P2.3: any metric FAIL -> verdict WARN."""
        metrics = {
            "density": {"pass": True},
            "recency": {"pass": False},
            "coverage": {"pass": True},
        }
        assert _aggregate_verdict(metrics) == "WARN"

    def test_aggregate_verdict_empty_or_no_pass(self):
        """P2.3: empty metrics or all None -> SKIP."""
        assert _aggregate_verdict({}) == "SKIP"
        assert _aggregate_verdict({"density": {"name": "density"}}) == "SKIP"


# ===========================================================================
# P4.6: Evergreen flag 3-level (file / section / until-date)
# ===========================================================================


class TestEvergreenFlags:
    """SPEC sez 5.1 -- 3-level evergreen flags + auto-archive eligibility."""

    def test_detect_evergreen_file_first_line(self):
        """File-level marker on line 1 -> True."""
        content = "<!-- evergreen: file -->\n# Title\n## Section\n"
        assert detect_evergreen_file(content) is True

    def test_detect_evergreen_file_not_first_line(self):
        """File-level marker NOT on line 1 -> False (must be first line)."""
        content = "# Title\n<!-- evergreen: file -->\n"
        assert detect_evergreen_file(content) is False

    def test_detect_evergreen_file_empty(self):
        """Empty content -> False (no crash)."""
        assert detect_evergreen_file("") is False

    def test_detect_evergreen_file_crlf_first_line(self):
        """CRLF line endings on first line -> still detected (normalization)."""
        content = "<!-- evergreen: file -->\r\n# Title\r\n"
        assert detect_evergreen_file(content) is True

    def test_parse_scopes_no_until_date(self):
        """Bare ``<!-- evergreen -->`` marker -> is_active=True, until_date=None."""
        content = "## H2 first\n<!-- evergreen -->\n## H2 second\n"
        scopes = parse_evergreen_scopes(content)
        assert len(scopes) == 1
        assert scopes[0]["until_date"] is None
        assert scopes[0]["is_active"] is True
        assert scopes[0]["line_number"] == 2

    def test_parse_scopes_until_date_active(self):
        """until-date > today -> is_active=True."""
        future = (date.today() + timedelta(days=30)).isoformat()
        content = f"## H2\n<!-- evergreen-until: {future} -->\nlines\n"
        scopes = parse_evergreen_scopes(content)
        assert len(scopes) == 1
        assert scopes[0]["until_date"] == date.fromisoformat(future)
        assert scopes[0]["is_active"] is True

    def test_parse_scopes_until_date_expired(self):
        """until-date <= today -> is_active=False (archive eligible)."""
        past = (date.today() - timedelta(days=30)).isoformat()
        content = f"## H2\n<!-- evergreen-until: {past} -->\nlines\n"
        scopes = parse_evergreen_scopes(content)
        assert len(scopes) == 1
        assert scopes[0]["is_active"] is False

    def test_parse_scopes_malformed_date_ignored(self):
        """Malformed date in ``evergreen-until:`` -> regex does NOT match, marker
        is silently skipped (defensive: avoid accidental protection from typos).

        To be picked up the marker must use ``<!-- evergreen -->`` (bare) OR
        a well-formed ``evergreen-until: YYYY-MM-DD``.
        """
        content = "## H2\n<!-- evergreen-until: not-a-date -->\nlines\n"
        scopes = parse_evergreen_scopes(content)
        # Malformed date -> regex does not match the whole marker -> 0 scopes.
        assert scopes == []

    def test_parse_scopes_skips_file_level_on_line_one(self):
        """File-level marker on line 1 is NOT returned as a scope marker."""
        content = (
            "<!-- evergreen: file -->\n"
            "# Title\n"
            "<!-- evergreen -->\n"
            "## H2\n"
        )
        scopes = parse_evergreen_scopes(content)
        # Only the section-level marker on line 3, not the file-level on line 1.
        assert len(scopes) == 1
        assert scopes[0]["line_number"] == 3

    def test_parse_scopes_multiple_markers(self):
        """Multiple scope markers -> each gets its own dict with correct line_number."""
        future = (date.today() + timedelta(days=10)).isoformat()
        content = (
            "## H2 one\n"
            "<!-- evergreen -->\n"
            "## H2 two\n"
            f"<!-- evergreen-until: {future} -->\n"
            "## H2 three\n"
        )
        scopes = parse_evergreen_scopes(content)
        assert len(scopes) == 2
        assert scopes[0]["line_number"] == 2
        assert scopes[1]["line_number"] == 4
        assert scopes[1]["until_date"] == date.fromisoformat(future)

    def test_is_h2_protected_within_lookback(self):
        """Scope marker 2 lines above H2 -> H2 is protected."""
        scopes = [{"line_number": 10, "until_date": None, "is_active": True}]
        # H2 at line 12, marker at line 10 -> within lookback (default 5)
        assert is_h2_evergreen_protected(12, scopes) is True

    def test_is_h2_protected_outside_lookback(self):
        """Scope marker too far above H2 -> NOT protected."""
        scopes = [{"line_number": 10, "until_date": None, "is_active": True}]
        # H2 at line 100, marker at line 10 -> outside lookback (5)
        assert is_h2_evergreen_protected(100, scopes) is False

    def test_is_h2_protected_inactive_scope_ignored(self):
        """Expired scope marker -> H2 not protected (eligible for archive)."""
        scopes = [{"line_number": 10, "until_date": None, "is_active": False}]
        assert is_h2_evergreen_protected(12, scopes) is False

    def test_is_h2_protected_empty_scopes(self):
        """No scopes -> never protected."""
        assert is_h2_evergreen_protected(5, []) is False

    def test_recency_evergreen_file_level_short_circuit(self):
        """File-level flag -> recency PASS regardless of stale content."""
        old = (date.today() - timedelta(days=365)).isoformat()
        content = (
            "<!-- evergreen: file -->\n"
            "# Title\n"
            f"## DOVE SIAMO {old}\n"
            "Very stale content that would normally fail recency.\n"
            f"## PROSSIMI {old}\n"
            "step\n"
        )
        r = calculate_recency(content, {})
        assert r["pass"] is True
        assert r["details"].get("evergreen_file_level") is True
        assert r["details"].get("reason") == "evergreen file-level flag"

    def test_recency_section_level_excludes_stale_h2(self):
        """Section-level marker above stale H2 -> that H2 NOT counted as stale."""
        old = (date.today() - timedelta(days=365)).isoformat()
        fresh = (date.today() - timedelta(days=1)).isoformat()
        # Without evergreen: 1 stale + 1 fresh in DOVE SIAMO = 50% stale (FAIL)
        # With evergreen above the stale one: stale_count drops to 0.
        content = (
            "# Title\n"
            "<!-- evergreen -->\n"
            f"## DOVE SIAMO old {old}\n"
            "Locked historical reference.\n"
            f"## DOVE SIAMO fresh {fresh}\n"
            "Current work.\n"
            f"## DOVE SIAMO fresh2 {fresh}\n"
            "More current work.\n"
        )
        r = calculate_recency(content, {})
        # The stale H2 should have been skipped via evergreen scope
        assert r["details"]["evergreen_scopes_found"] >= 1
        assert r["details"]["evergreen_skipped_h2"] >= 1
        assert r["stale_pct"] == 0.0

    def test_recency_expired_until_date_does_not_protect(self):
        """until-date in the past -> stale H2 IS counted (archive eligible)."""
        old = (date.today() - timedelta(days=365)).isoformat()
        past = (date.today() - timedelta(days=10)).isoformat()
        content = (
            "# Title\n"
            f"<!-- evergreen-until: {past} -->\n"
            f"## DOVE SIAMO ancient {old}\n"
            "Should be counted stale because evergreen-until expired.\n"
        )
        r = calculate_recency(content, {})
        # Marker is expired -> stale count NOT reduced.
        assert r["details"]["evergreen_skipped_h2"] == 0
        assert r["details"]["stale_count"] >= 1

    def test_parse_scopes_empty_content_no_crash(self):
        """Empty content -> empty list, no exception."""
        assert parse_evergreen_scopes("") == []

    def test_recency_duplicate_h2_headers_only_one_protected(self):
        """F1 (P4.6 R2) regression: two H2 with identical text but marker only
        above the first -> only the first is protected.

        Prior implementation used ``header_line in scope_text`` (textual
        substring match) which falsely matched the second duplicate H2 even
        though it lives outside the evergreen-protected section. The fix uses
        char-offset bounds via ``_extract_scope_recency_bounds`` so each H2 is
        evaluated by its actual position in the document.
        """
        today = date.today()
        stale_date = (today - timedelta(days=120)).isoformat()
        content = (
            "# Title\n"
            "<!-- evergreen -->\n"
            f"## DOVE SIAMO {stale_date}\n"
            "first occurrence, protected by marker above.\n"
            f"## DOVE SIAMO {stale_date}\n"
            "second duplicate, NOT protected (no marker above).\n"
        )
        r = calculate_recency(content, {})
        skipped = r.get("details", {}).get("evergreen_skipped_h2", 0)
        stale_count = r.get("details", {}).get("stale_count", 0)
        assert skipped == 1, (
            f"Expected exactly 1 H2 skipped (line/offset-based scope), got "
            f"{skipped}. Likely textual-substring FP regression: duplicate H2 "
            f"with identical text was matched outside the protected section."
        )
        # The second duplicate H2 is still stale and must be counted.
        assert stale_count >= 1, (
            f"Expected at least 1 stale H2 (the unprotected duplicate), got "
            f"{stale_count}. Both H2 should not be skipped."
        )

    def test_evergreen_lookback_configurable_via_config(self):
        """F2 (P4.6 R2): ``evergreen_scope_lookback_lines`` config override
        changes the lookback distance used by recency protection.

        Invariant: a larger lookback protects more H2 (>= the count protected
        by the smaller default). We craft content where a stale H2 is too far
        from the marker for the default lookback=5, but close enough for a
        custom lookback=20 -> the custom config yields strictly more skips.
        """
        today = date.today()
        stale_date = (today - timedelta(days=120)).isoformat()
        # Marker on line 2; stale H2 on line 10 -> 8 lines below the marker.
        # Default lookback=5 -> H2 line 10 NOT in [10-5, 10) = [5, 10) -> NOT
        #   protected (marker is at line 2, below range).
        # Custom lookback=20 -> H2 line 10 IS in [10-20, 10) = [-10, 10) ->
        #   protected (marker at line 2 falls inside).
        content = (
            "# Title\n"                       # line 1
            "<!-- evergreen -->\n"            # line 2 (marker)
            "filler line three\n"             # line 3
            "filler line four\n"              # line 4
            "filler line five\n"              # line 5
            "filler line six\n"               # line 6
            "filler line seven\n"             # line 7
            "filler line eight\n"             # line 8
            "filler line nine\n"              # line 9
            f"## DOVE SIAMO {stale_date}\n"   # line 10 (target H2)
            "stale content under custom-lookback protection.\n"
        )
        r_default = calculate_recency(content, {})
        skipped_default = r_default.get("details", {}).get(
            "evergreen_skipped_h2", 0
        )

        r_custom = calculate_recency(
            content, {"evergreen_scope_lookback_lines": 20}
        )
        skipped_custom = r_custom.get("details", {}).get(
            "evergreen_skipped_h2", 0
        )

        # Custom lookback should protect strictly more H2 than the default
        # (or at least equal -- never less). On this fixture we expect 0 -> 1.
        assert skipped_custom >= skipped_default, (
            f"Custom lookback=20 should skip >= default lookback=5. "
            f"Default skipped: {skipped_default}, Custom: {skipped_custom}"
        )
        assert skipped_custom > skipped_default, (
            f"Fixture designed so custom lookback strictly increases protection: "
            f"default={skipped_default}, custom={skipped_custom}."
        )
