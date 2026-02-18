"""
Test per ImpactAnalyzer - Core functionality.

Verifica: ImpactResult, init, estimate_impact,
find_dependencies, find_dependents, risk calculation.

Split da test_impact_analyzer.py (869 righe > limite 500).

Sessione 341 - Split test file.
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Setup path
project_root = Path(__file__).parent.parent.parent

from cervellaswarm_code_intelligence.impact_analyzer import (
    ImpactAnalyzer,
    ImpactResult,
)

# Fixtures mock_symbol, temp_repo from conftest.py


# === IMPACTRESULT TESTS ===


class TestImpactResult:
    """Test ImpactResult dataclass."""

    def test_impact_result_creation(self):
        """Verifica creazione ImpactResult con tutti i parametri."""
        result = ImpactResult(
            symbol_name="MyClass",
            risk_score=0.65,
            risk_level="high",
            files_affected=5,
            callers_count=12,
            importance_score=0.08,
            reasons=["Many callers", "High importance"],
        )

        assert result.symbol_name == "MyClass"
        assert result.risk_score == 0.65
        assert result.risk_level == "high"
        assert result.files_affected == 5
        assert result.callers_count == 12
        assert result.importance_score == 0.08
        assert len(result.reasons) == 2

    def test_impact_result_repr(self):
        """Verifica rappresentazione string."""
        result = ImpactResult(
            symbol_name="TestFunc",
            risk_score=0.3,
            risk_level="medium",
            files_affected=2,
            callers_count=5,
            importance_score=0.02,
            reasons=["test"],
        )

        repr_str = repr(result)
        assert "TestFunc" in repr_str
        assert "MEDIUM" in repr_str
        assert "0.30" in repr_str
        assert "5 callers" in repr_str


# === IMPACTANALYZER INITIALIZATION TESTS ===


class TestImpactAnalyzerInit:
    """Test inizializzazione ImpactAnalyzer."""

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_init_with_valid_repo(self, mock_search_class, temp_repo):
        """Verifica init con repo valido."""
        mock_search_class.return_value = MagicMock()

        analyzer = ImpactAnalyzer(temp_repo)

        assert analyzer.repo_root == Path(temp_repo).resolve()
        assert analyzer.search is not None
        mock_search_class.assert_called_once_with(temp_repo)

    def test_init_with_nonexistent_repo(self):
        """Verifica errore con repo non esistente."""
        with pytest.raises(ValueError, match="does not exist"):
            ImpactAnalyzer("/nonexistent/path/to/repo")

    def test_init_with_file_not_directory(self, tmp_path):
        """Verifica errore con file invece di directory."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        with pytest.raises(ValueError, match="not a directory"):
            ImpactAnalyzer(str(file_path))


# === ESTIMATE_IMPACT TESTS ===


class TestEstimateImpact:
    """Test estimate_impact() method."""

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_estimate_impact_symbol_not_found(self, mock_search_class, temp_repo):
        """Verifica ritorno None per simbolo non trovato."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = None
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("NonExistentSymbol")

        assert result is None
        mock_search.get_symbol_info.assert_called_once_with("NonExistentSymbol")

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_estimate_impact_no_callers(self, mock_search_class, temp_repo, mock_symbol):
        """Verifica estimate_impact con zero callers (low risk)."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = mock_symbol
        mock_search.find_callers.return_value = []
        mock_search.graph.get_symbol_importance.return_value = 0.01
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("TestClass")

        assert result is not None
        assert result.symbol_name == "TestClass"
        assert result.callers_count == 0
        assert result.files_affected == 1
        assert result.risk_level in ["low", "medium"]
        assert any("No callers" in reason for reason in result.reasons)

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_estimate_impact_many_callers(self, mock_search_class, temp_repo, mock_symbol):
        """Verifica estimate_impact con molti callers (high risk)."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = mock_symbol

        callers = [
            (f"/test/file{i}.py", 20, f"caller_{i}")
            for i in range(25)
        ]
        mock_search.find_callers.return_value = callers
        mock_search.graph.get_symbol_importance.return_value = 0.08
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("TestClass")

        assert result is not None
        assert result.callers_count == 25
        assert result.risk_level in ["high", "critical"]
        assert any("callers" in reason.lower() for reason in result.reasons)

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_estimate_impact_high_importance(self, mock_search_class, temp_repo, mock_symbol):
        """Verifica estimate_impact con alta PageRank importance."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = mock_symbol
        mock_search.find_callers.return_value = []
        mock_search.graph.get_symbol_importance.return_value = 0.15
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("TestClass")

        assert result is not None
        assert result.importance_score == 0.15
        assert any("PageRank" in reason for reason in result.reasons)


# === FIND_DEPENDENCIES TESTS ===


class TestFindDependencies:
    """Test find_dependencies() method."""

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependencies_success(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con dipendenze trovate."""
        mock_search = MagicMock()

        symbol1 = MagicMock()
        symbol1.references = ["OtherClass", "helper_func"]
        symbol2 = MagicMock()
        symbol2.references = ["AnotherClass"]

        mock_search.extractor.extract_symbols.return_value = [symbol1, symbol2]

        def find_symbol_side_effect(ref_name):
            if ref_name == "OtherClass":
                return ("/test/other.py", 10)
            elif ref_name == "helper_func":
                return ("/test/utils.py", 5)
            elif ref_name == "AnotherClass":
                return ("/test/another.py", 20)
            return None

        mock_search.find_symbol.side_effect = find_symbol_side_effect
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/main.py")

        assert len(deps) == 3
        assert "/test/other.py" in deps
        assert "/test/utils.py" in deps
        assert "/test/another.py" in deps
        assert "/test/main.py" not in deps

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependencies_no_symbols(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con file senza simboli."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.return_value = []
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/empty.py")

        assert deps == []

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependencies_extraction_error(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con errore extraction."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.side_effect = Exception("Parse error")
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/broken.py")

        assert deps == []

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependencies_self_reference_excluded(self, mock_search_class, temp_repo):
        """Verifica che self-references siano escluse."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.references = ["SelfClass"]
        mock_search.extractor.extract_symbols.return_value = [symbol]

        mock_search.find_symbol.return_value = ("/test/main.py", 10)
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/main.py")

        assert deps == []


# === FIND_DEPENDENTS TESTS ===


class TestFindDependents:
    """Test find_dependents() method."""

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependents_success(self, mock_search_class, temp_repo):
        """Verifica find_dependents con dependents trovati."""
        mock_search = MagicMock()

        symbol1 = MagicMock()
        symbol1.name = "MyClass"
        symbol2 = MagicMock()
        symbol2.name = "my_function"

        mock_search.extractor.extract_symbols.return_value = [symbol1, symbol2]

        def find_callers_side_effect(symbol_name):
            if symbol_name == "MyClass":
                return [
                    ("/test/caller1.py", 10, "Caller1"),
                    ("/test/caller2.py", 20, "Caller2"),
                ]
            elif symbol_name == "my_function":
                return [
                    ("/test/caller2.py", 30, "Caller3"),
                    ("/test/caller3.py", 40, "Caller4"),
                ]
            return []

        mock_search.find_callers.side_effect = find_callers_side_effect
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        dependents = analyzer.find_dependents("/test/main.py")

        assert len(dependents) == 3
        assert "/test/caller1.py" in dependents
        assert "/test/caller2.py" in dependents
        assert "/test/caller3.py" in dependents
        assert "/test/main.py" not in dependents

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependents_no_symbols(self, mock_search_class, temp_repo):
        """Verifica find_dependents con file senza simboli."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.return_value = []
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        dependents = analyzer.find_dependents("/test/empty.py")

        assert dependents == []

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_find_dependents_extraction_error(self, mock_search_class, temp_repo):
        """Verifica find_dependents con errore extraction."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.side_effect = Exception("Parse error")
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        dependents = analyzer.find_dependents("/test/broken.py")

        assert dependents == []


# === RISK CALCULATION TESTS ===


class TestRiskCalculation:
    """Test _calculate_risk_score() method."""

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_risk_score_low(self, mock_search_class, temp_repo):
        """Verifica risk score LOW (< 0.3)."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "type"

        risk = analyzer._calculate_risk_score(symbol, callers_count=0, importance_score=0.01)
        assert risk < 0.3

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_risk_score_medium(self, mock_search_class, temp_repo):
        """Verifica risk score MEDIUM (0.3-0.5)."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "function"

        risk = analyzer._calculate_risk_score(symbol, callers_count=2, importance_score=0.01)
        assert 0.3 <= risk < 0.5

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_risk_score_high(self, mock_search_class, temp_repo):
        """Verifica risk score HIGH (0.5-0.7)."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "type"

        risk = analyzer._calculate_risk_score(symbol, callers_count=6, importance_score=0.02)
        assert 0.5 <= risk < 0.7

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_risk_score_critical(self, mock_search_class, temp_repo):
        """Verifica risk score CRITICAL (>= 0.7)."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        risk = analyzer._calculate_risk_score(symbol, callers_count=25, importance_score=0.1)
        assert risk >= 0.7

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_risk_score_capped_at_1(self, mock_search_class, temp_repo):
        """Verifica che risk score non superi mai 1.0."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        risk = analyzer._calculate_risk_score(symbol, callers_count=1000, importance_score=0.5)
        assert risk <= 1.0

    @patch("cervellaswarm_code_intelligence.impact_analyzer.SemanticSearch")
    def test_risk_type_weights(self, mock_search_class, temp_repo):
        """Verifica pesi diversi per type diversi."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        symbol_class = MagicMock()
        symbol_class.type = "class"
        risk_class = analyzer._calculate_risk_score(symbol_class, 10, 0.05)

        symbol_func = MagicMock()
        symbol_func.type = "function"
        risk_func = analyzer._calculate_risk_score(symbol_func, 10, 0.05)

        assert risk_class > risk_func


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
