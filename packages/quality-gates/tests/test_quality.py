# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_quality_gates.quality module."""

import pytest

from cervellaswarm_quality_gates.quality import (
    DEFAULT_WEIGHTS,
    QualityScore,
    _extract_file_path,
    _score_actionability,
    _score_conciseness,
    _score_freshness,
    _score_specificity,
    score_content,
    score_file,
)


class TestQualityScore:
    """Tests for QualityScore dataclass."""

    def test_frozen(self):
        qs = QualityScore(actionability=8.0, specificity=7.0, freshness=6.0, conciseness=5.0, total=6.7)
        with pytest.raises(AttributeError):
            qs.total = 10.0

    def test_passes_above_threshold(self):
        qs = QualityScore(actionability=8.0, specificity=8.0, freshness=8.0, conciseness=8.0, total=8.0)
        assert qs.passes(7.0) is True

    def test_fails_below_threshold(self):
        qs = QualityScore(actionability=3.0, specificity=3.0, freshness=3.0, conciseness=3.0, total=3.0)
        assert qs.passes(7.0) is False

    def test_passes_exact_threshold(self):
        qs = QualityScore(actionability=7.0, specificity=7.0, freshness=7.0, conciseness=7.0, total=7.0)
        assert qs.passes(7.0) is True

    def test_passes_default_threshold(self):
        qs = QualityScore(actionability=8.0, specificity=8.0, freshness=8.0, conciseness=8.0, total=8.0)
        assert qs.passes() is True


class TestScoreActionability:
    """Tests for _score_actionability."""

    def test_empty_content(self):
        assert _score_actionability("") == 0.0

    def test_whitespace_only(self):
        assert _score_actionability("   \n  \n  ") == 0.0

    def test_no_action_items(self):
        assert _score_actionability("Just some text with no actions.") == 0.0

    def test_checklist_item(self):
        score = _score_actionability("- [ ] Fix the bug\n- [x] Done")
        assert score > 0.0

    def test_todo_keyword(self):
        score = _score_actionability("TODO: update the docs")
        assert score > 0.0

    def test_next_steps_header(self):
        score = _score_actionability("## Next Steps\n1. Deploy")
        assert score > 0.0

    def test_multiple_action_patterns(self):
        content = """## Next steps
1. TODO: Fix auth
- [ ] Deploy to staging
We should update the docs
Decisioni importanti"""
        score = _score_actionability(content)
        assert score >= 8.0

    def test_numbered_list(self):
        score = _score_actionability("1. First step\n2. Second step\n3. Third step")
        assert score > 0.0

    def test_will_should_must(self):
        score = _score_actionability("We will deploy tomorrow. You should review.")
        assert score > 0.0

    def test_italian_prossimi_step(self):
        score = _score_actionability("## Prossimi step\n- Fixare il bug")
        assert score > 0.0

    def test_max_score_reachable(self):
        content = """## Next steps
1. TODO: Deploy
2. FIXME: Bug in auth
- [ ] Review code
We must update
Decisioni prese
Action items here"""
        score = _score_actionability(content)
        assert score >= 9.0


class TestScoreSpecificity:
    """Tests for _score_specificity."""

    def test_empty_content(self):
        assert _score_specificity("") == 0.0

    def test_whitespace_only(self):
        assert _score_specificity("  \n  ") == 0.0

    def test_vague_content(self):
        score = _score_specificity("things are going well")
        assert score <= 4.0

    def test_filename_reference(self):
        score = _score_specificity("Fixed bug in auth_handler.py")
        assert score > 0.0

    def test_version_number(self):
        score = _score_specificity("Updated to v0.2.1 from v0.1.0")
        assert score > 0.0

    def test_session_number(self):
        score = _score_specificity("S392 completed successfully")
        assert score > 0.0

    def test_inline_code(self):
        score = _score_specificity("Fixed `login_handler` function")
        assert score > 0.0

    def test_count_with_unit(self):
        score = _score_specificity("Added 15 tests for 3 modules")
        assert score > 0.0

    def test_camelcase_identifier(self):
        score = _score_specificity("Updated QualityScore class")
        assert score > 0.0

    def test_snake_case_identifier(self):
        score = _score_specificity("Changed score_content function")
        assert score > 0.0

    def test_highly_specific_content(self):
        content = "Fixed `auth_handler.py` v0.2.1 (S392): added 15 tests for QualityScore"
        score = _score_specificity(content)
        assert score >= 8.0


class TestScoreFreshness:
    """Tests for _score_freshness."""

    def test_empty_content(self):
        assert _score_freshness("") == 0.0

    def test_whitespace_only(self):
        assert _score_freshness("  \n  ") == 0.0

    def test_no_dates(self):
        score = _score_freshness("Some old content without dates")
        assert score == 0.0

    def test_iso_date(self):
        score = _score_freshness("Updated: 2026-02-24")
        assert score > 0.0

    def test_session_number(self):
        score = _score_freshness("Session 42 completed")
        assert score > 0.0

    def test_s_number_style(self):
        score = _score_freshness("S392 checkpoint")
        assert score > 0.0

    def test_today_keyword(self):
        score = _score_freshness("Today we fixed the bug")
        assert score > 0.0

    def test_italian_oggi(self):
        score = _score_freshness("Oggi abbiamo fixato il bug")
        assert score > 0.0

    def test_ultimo_aggiornamento(self):
        score = _score_freshness("Ultimo aggiornamento: febbraio")
        assert score > 0.0

    def test_multiple_freshness_signals(self):
        content = "2026-02-24 - Session 42 - S392 - today updated"
        score = _score_freshness(content)
        assert score >= 8.0

    def test_english_date_format(self):
        score = _score_freshness("24 Feb meeting notes")
        assert score > 0.0


class TestScoreConciseness:
    """Tests for _score_conciseness."""

    def test_empty_content(self):
        assert _score_conciseness("") == 0.0

    def test_whitespace_only(self):
        assert _score_conciseness("  \n  \n  ") == 0.0

    def test_dense_content(self):
        content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
        score = _score_conciseness(content)
        assert score >= 8.0

    def test_sparse_content(self):
        content = "Line 1\n\n\n\n\nLine 2\n\n\n\n\nLine 3"
        score = _score_conciseness(content)
        assert score <= 6.0

    def test_very_long_content_penalized(self):
        content = "\n".join([f"Line {i}" for i in range(350)])
        score = _score_conciseness(content)
        # Should have length penalty
        assert score < 10.0

    def test_moderately_long_content(self):
        content = "\n".join([f"Line {i}" for i in range(250)])
        score_long = _score_conciseness(content)
        content_short = "\n".join([f"Line {i}" for i in range(50)])
        score_short = _score_conciseness(content_short)
        assert score_short >= score_long

    def test_perfect_density(self):
        content = "A\nB\nC\nD\nE"
        score = _score_conciseness(content)
        assert score == 10.0


class TestScoreContent:
    """Tests for score_content integration."""

    def test_empty_content_returns_zeros(self):
        result = score_content("")
        assert result.total == 0.0
        assert result.actionability == 0.0
        assert result.specificity == 0.0
        assert result.freshness == 0.0
        assert result.conciseness == 0.0

    def test_rich_session_content(self, sample_session_content):
        result = score_content(sample_session_content)
        assert result.total > 5.0
        assert result.actionability > 0.0
        assert result.specificity > 0.0
        assert result.freshness > 0.0
        assert result.conciseness > 0.0

    def test_default_weights(self):
        assert sum(DEFAULT_WEIGHTS.values()) == pytest.approx(1.0)

    def test_custom_weights(self):
        content = "## Next steps\n1. TODO: Deploy\n2. Fix bug"
        custom = {"actionability": 1.0, "specificity": 0.0, "freshness": 0.0, "conciseness": 0.0}
        result = score_content(content, weights=custom)
        assert result.total == pytest.approx(result.actionability, abs=0.1)

    def test_custom_weights_not_mutated(self):
        """P11: defensive copy of weights dict."""
        original = {"actionability": 0.25, "specificity": 0.25, "freshness": 0.25, "conciseness": 0.25}
        weights_copy = dict(original)
        score_content("test content", weights=weights_copy)
        assert weights_copy == original

    def test_total_clamped_to_10(self):
        # Even with maximum scores, total shouldn't exceed 10
        content = """## Next steps
1. TODO: Deploy auth_handler.py v0.2.1
2. FIXME: Fix `QualityScore` in S392
- [ ] Update session_memory.py
We must fix 15 bugs by 2026-02-24
Decisioni: Chose JWT. Action items below.
Today - Sessione 42 - ultimo aggiornamento"""
        result = score_content(content)
        assert result.total <= 10.0

    def test_total_not_negative(self):
        result = score_content("x")
        assert result.total >= 0.0

    def test_invalid_weights_sum_raises(self):
        """P3-7 regression: weights that don't sum to ~1.0 raise ValueError."""
        bad_weights = {"actionability": 5.0, "specificity": 5.0, "freshness": 5.0, "conciseness": 5.0}
        with pytest.raises(ValueError, match="must sum to"):
            score_content("test", weights=bad_weights)

    def test_default_weights_immutable(self):
        """P2-1 regression: DEFAULT_WEIGHTS should be MappingProxyType."""
        with pytest.raises(TypeError):
            DEFAULT_WEIGHTS["actionability"] = 0.99


class TestExtractFilePath:
    """Tests for _extract_file_path helper."""

    def test_python_file(self):
        assert _extract_file_path("Fixed bug in auth.py") == "auth.py"

    def test_nested_path(self):
        result = _extract_file_path("Updated src/handlers/login.py")
        assert result == "src/handlers/login.py"

    def test_relative_path(self):
        result = _extract_file_path("See ./config.yaml for details")
        assert result == "./config.yaml"

    def test_absolute_path(self):
        result = _extract_file_path("File at /etc/config.toml")
        assert result == "/etc/config.toml"

    def test_no_file_path(self):
        assert _extract_file_path("No file here") is None

    def test_markdown_file(self):
        assert _extract_file_path("Updated README.md") == "README.md"

    def test_yaml_file(self):
        result = _extract_file_path("Config in .cervella/quality-gates.yaml")
        assert result is not None
        assert result.endswith(".yaml")

    def test_toml_file(self):
        result = _extract_file_path("Changed pyproject.toml")
        assert result == "pyproject.toml"

    def test_shell_script(self):
        result = _extract_file_path("Running deploy.sh script")
        assert result == "deploy.sh"


class TestScoreFile:
    """Tests for score_file."""

    def test_score_existing_file(self, tmp_path, sample_session_content):
        f = tmp_path / "session.md"
        f.write_text(sample_session_content)
        result = score_file(str(f))
        assert result.total > 0.0

    def test_score_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            score_file("/nonexistent/file.md")

    def test_score_empty_file(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        result = score_file(str(f))
        assert result.total == 0.0

    def test_score_file_with_custom_weights(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("## Next steps\n1. Deploy\n2. Test")
        custom = {"actionability": 0.50, "specificity": 0.20, "freshness": 0.15, "conciseness": 0.15}
        result = score_file(str(f), weights=custom)
        assert result.total > 0.0
