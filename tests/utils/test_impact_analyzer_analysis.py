"""
Test per ImpactAnalyzer - Analysis & Integration.

Verifica: risk levels, reasons generation, stats,
convenience function, edge cases, full integration.

Split da test_impact_analyzer.py (869 righe > limite 500).

Sessione 341 - Split test file.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Setup path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts" / "utils"))

from impact_analyzer import (
    ImpactAnalyzer,
    ImpactResult,
    estimate_symbol_impact,
)

# Fixtures mock_symbol, temp_repo from conftest.py


# === RISK LEVEL TESTS ===


class TestRiskLevel:
    """Test _get_risk_level() method."""

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_level_low(self, mock_search_class, temp_repo):
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)
        assert analyzer._get_risk_level(0.1) == "low"
        assert analyzer._get_risk_level(0.29) == "low"

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_level_medium(self, mock_search_class, temp_repo):
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)
        assert analyzer._get_risk_level(0.3) == "medium"
        assert analyzer._get_risk_level(0.49) == "medium"

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_level_high(self, mock_search_class, temp_repo):
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)
        assert analyzer._get_risk_level(0.5) == "high"
        assert analyzer._get_risk_level(0.69) == "high"

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_level_critical(self, mock_search_class, temp_repo):
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)
        assert analyzer._get_risk_level(0.7) == "critical"
        assert analyzer._get_risk_level(1.0) == "critical"


# === REASONS GENERATION TESTS ===


class TestReasonsGeneration:
    """Test _generate_reasons() method."""

    @patch("impact_analyzer.SemanticSearch")
    def test_reasons_no_callers(self, mock_search_class, temp_repo):
        """Verifica reasons con zero callers."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "function"

        reasons = analyzer._generate_reasons(symbol, 0, 1, 0.01, 0.2)

        assert any("No callers" in r for r in reasons)
        assert any("LOW RISK" in r for r in reasons)

    @patch("impact_analyzer.SemanticSearch")
    def test_reasons_many_files(self, mock_search_class, temp_repo):
        """Verifica reasons con molti file affetti."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        reasons = analyzer._generate_reasons(symbol, 15, 12, 0.05, 0.6)

        assert any("files" in r.lower() for r in reasons)
        assert any("HIGH RISK" in r for r in reasons)

    @patch("impact_analyzer.SemanticSearch")
    def test_reasons_high_importance(self, mock_search_class, temp_repo):
        """Verifica reasons con alta importance."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        reasons = analyzer._generate_reasons(symbol, 10, 5, 0.08, 0.65)

        assert any("PageRank" in r for r in reasons)

    @patch("impact_analyzer.SemanticSearch")
    def test_reasons_class_type(self, mock_search_class, temp_repo):
        """Verifica reasons specifiche per class type."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        reasons = analyzer._generate_reasons(symbol, 5, 3, 0.03, 0.4)

        assert any("Class type" in r for r in reasons)

    @patch("impact_analyzer.SemanticSearch")
    def test_reasons_interface_type(self, mock_search_class, temp_repo):
        """Verifica reasons specifiche per interface type."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "interface"

        reasons = analyzer._generate_reasons(symbol, 5, 3, 0.03, 0.4)

        assert any("Interface type" in r for r in reasons)


# === GET_STATS TESTS ===


class TestGetStats:
    """Test get_stats() method."""

    @patch("impact_analyzer.SemanticSearch")
    def test_get_stats_returns_dict(self, mock_search_class, temp_repo):
        """Verifica che get_stats ritorni un dict."""
        mock_search = MagicMock()
        mock_search.get_stats.return_value = {
            "total_symbols": 100,
            "unique_names": 80,
            "graph_nodes": 90,
            "graph_edges": 200,
        }
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        stats = analyzer.get_stats()

        assert isinstance(stats, dict)
        assert stats["total_symbols"] == 100
        assert stats["unique_names"] == 80
        mock_search.get_stats.assert_called_once()


# === CONVENIENCE FUNCTION TESTS ===


class TestConvenienceFunction:
    """Test estimate_symbol_impact() convenience function."""

    @patch("impact_analyzer.ImpactAnalyzer")
    def test_estimate_symbol_impact_creates_analyzer(self, mock_analyzer_class, temp_repo):
        """Verifica che la convenience function crei ImpactAnalyzer."""
        mock_analyzer = MagicMock()
        mock_result = ImpactResult(
            symbol_name="Test",
            risk_score=0.5,
            risk_level="medium",
            files_affected=3,
            callers_count=5,
            importance_score=0.03,
            reasons=["test"],
        )
        mock_analyzer.estimate_impact.return_value = mock_result
        mock_analyzer_class.return_value = mock_analyzer

        result = estimate_symbol_impact(temp_repo, "TestSymbol")

        mock_analyzer_class.assert_called_once_with(temp_repo)
        mock_analyzer.estimate_impact.assert_called_once_with("TestSymbol")
        assert result == mock_result

    @patch("impact_analyzer.ImpactAnalyzer")
    def test_estimate_symbol_impact_symbol_not_found(self, mock_analyzer_class, temp_repo):
        """Verifica comportamento con simbolo non trovato."""
        mock_analyzer = MagicMock()
        mock_analyzer.estimate_impact.return_value = None
        mock_analyzer_class.return_value = mock_analyzer

        result = estimate_symbol_impact(temp_repo, "NonExistent")

        assert result is None


# === EDGE CASES TESTS ===


class TestEdgeCases:
    """Test casi limite e situazioni anomale."""

    @patch("impact_analyzer.SemanticSearch")
    def test_estimate_impact_with_circular_dependencies(self, mock_search_class, temp_repo):
        """Verifica gestione circular dependencies."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.name = "CircularClass"
        symbol.type = "class"
        symbol.file = "/test/circular.py"

        callers = [
            ("/test/circular.py", 20, "self_reference"),
            ("/test/other.py", 30, "external_caller"),
        ]

        mock_search.get_symbol_info.return_value = symbol
        mock_search.find_callers.return_value = callers
        mock_search.graph.get_symbol_importance.return_value = 0.03
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("CircularClass")

        assert result is not None
        assert result.files_affected >= 1

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependencies_empty_references(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con simboli senza references."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.references = []

        mock_search.extractor.extract_symbols.return_value = [symbol]
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/isolated.py")

        assert deps == []

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependents_no_callers(self, mock_search_class, temp_repo):
        """Verifica find_dependents con simboli mai chiamati."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.name = "UnusedClass"

        mock_search.extractor.extract_symbols.return_value = [symbol]
        mock_search.find_callers.return_value = []
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        dependents = analyzer.find_dependents("/test/unused.py")

        assert dependents == []

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_score_unknown_symbol_type(self, mock_search_class, temp_repo):
        """Verifica risk score con symbol type sconosciuto."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "unknown_type"

        risk = analyzer._calculate_risk_score(symbol, 10, 0.05)

        assert 0.0 <= risk <= 1.0


# === FULL INTEGRATION TESTS ===


class TestFullIntegration:
    """Test integrazione completa con scenari realistici."""

    @patch("impact_analyzer.SemanticSearch")
    def test_complete_workflow_single_symbol(self, mock_search_class, temp_repo):
        """Test workflow completo: init, estimate, dependencies, dependents."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.name = "MyService"
        symbol.type = "class"
        symbol.file = "/test/services.py"
        symbol.line = 10
        symbol.references = ["HelperClass", "validate_func"]

        mock_search.get_symbol_info.return_value = symbol

        mock_search.find_callers.return_value = [
            ("/test/controller.py", 20, "UserController"),
            ("/test/controller.py", 40, "AdminController"),
            ("/test/api.py", 15, "api_handler"),
        ]

        mock_search.graph.get_symbol_importance.return_value = 0.03
        mock_search.extractor.extract_symbols.return_value = [symbol]

        def find_symbol_side_effect(name):
            if name == "HelperClass":
                return ("/test/helpers.py", 5)
            elif name == "validate_func":
                return ("/test/validators.py", 10)
            return None

        mock_search.find_symbol.side_effect = find_symbol_side_effect
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        # 1. Estimate impact
        result = analyzer.estimate_impact("MyService")
        assert result is not None
        assert result.symbol_name == "MyService"
        assert result.callers_count == 3
        assert result.files_affected == 3

        # 2. Find dependencies
        deps = analyzer.find_dependencies("/test/services.py")
        assert len(deps) == 2
        assert "/test/helpers.py" in deps
        assert "/test/validators.py" in deps

        # 3. Find dependents
        dependents = analyzer.find_dependents("/test/services.py")
        assert len(dependents) == 2
        assert "/test/controller.py" in dependents
        assert "/test/api.py" in dependents

    @patch("impact_analyzer.SemanticSearch")
    def test_multiple_symbols_same_file(self, mock_search_class, temp_repo):
        """Test file con multiple symbols."""
        mock_search = MagicMock()

        symbol1 = MagicMock()
        symbol1.name = "ClassA"
        symbol1.references = ["OtherClass"]

        symbol2 = MagicMock()
        symbol2.name = "ClassB"
        symbol2.references = ["YetAnother"]

        mock_search.extractor.extract_symbols.return_value = [symbol1, symbol2]

        def find_symbol_side_effect(name):
            if name == "OtherClass":
                return ("/test/other.py", 10)
            elif name == "YetAnother":
                return ("/test/another.py", 20)
            return None

        mock_search.find_symbol.side_effect = find_symbol_side_effect
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/multi.py")

        assert len(deps) == 2
        assert "/test/other.py" in deps
        assert "/test/another.py" in deps

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_levels_distribution(self, mock_search_class, temp_repo):
        """Test che tutti i risk levels siano raggiungibili."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        test_cases = [
            (0.0, "low"),
            (0.29, "low"),
            (0.3, "medium"),
            (0.49, "medium"),
            (0.5, "high"),
            (0.69, "high"),
            (0.7, "critical"),
            (1.0, "critical"),
        ]

        for score, expected_level in test_cases:
            level = analyzer._get_risk_level(score)
            assert level == expected_level, f"Score {score} should be {expected_level}, got {level}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
