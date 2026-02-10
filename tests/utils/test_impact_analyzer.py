"""
Test per ImpactAnalyzer - Analisi impatto modifiche codice.

Verifica che l'impact analyzer calcoli correttamente i risk scores
e identifichi dependencies/dependents.

Target Coverage: > 80%
Sessione 339 - FASE 3.1
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, PropertyMock

# Setup path - aggiunge scripts/utils come fanno gli altri test
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "scripts" / "utils"))

from impact_analyzer import (
    ImpactAnalyzer,
    ImpactResult,
    estimate_symbol_impact,
)


# === FIXTURES ===


@pytest.fixture
def mock_semantic_search():
    """Mock SemanticSearch con comportamento realistico."""
    mock = MagicMock()

    # Mock graph con PageRank
    mock.graph = MagicMock()
    mock.graph.get_symbol_importance = MagicMock(return_value=0.05)

    # Mock extractor
    mock.extractor = MagicMock()

    return mock


@pytest.fixture
def mock_symbol():
    """Mock Symbol object."""
    symbol = MagicMock()
    symbol.name = "TestClass"
    symbol.type = "class"
    symbol.file = "/test/file.py"
    symbol.line = 10
    symbol.references = ["OtherClass", "helper_func"]
    return symbol


@pytest.fixture
def temp_repo(tmp_path):
    """Temporary repo directory."""
    repo = tmp_path / "test_repo"
    repo.mkdir()

    # Create some test files
    (repo / "main.py").write_text("class Main: pass")
    (repo / "utils.py").write_text("def helper(): pass")

    return str(repo)


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

    @patch("impact_analyzer.SemanticSearch")
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

    @patch("impact_analyzer.SemanticSearch")
    def test_estimate_impact_symbol_not_found(self, mock_search_class, temp_repo):
        """Verifica ritorno None per simbolo non trovato."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = None
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("NonExistentSymbol")

        assert result is None
        mock_search.get_symbol_info.assert_called_once_with("NonExistentSymbol")

    @patch("impact_analyzer.SemanticSearch")
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
        assert result.files_affected == 1  # Solo file definizione
        # class type = 0.3, 0 callers = 0, importance 0.01 = 0.1 base => 0.4 total (medium)
        assert result.risk_level in ["low", "medium"]  # Dipende dal type del mock
        assert any("No callers" in reason for reason in result.reasons)

    @patch("impact_analyzer.SemanticSearch")
    def test_estimate_impact_many_callers(self, mock_search_class, temp_repo, mock_symbol):
        """Verifica estimate_impact con molti callers (high risk)."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = mock_symbol

        # Simula 25 callers in 10 file diversi
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

    @patch("impact_analyzer.SemanticSearch")
    def test_estimate_impact_high_importance(self, mock_search_class, temp_repo, mock_symbol):
        """Verifica estimate_impact con alta PageRank importance."""
        mock_search = MagicMock()
        mock_search.get_symbol_info.return_value = mock_symbol
        mock_search.find_callers.return_value = []
        mock_search.graph.get_symbol_importance.return_value = 0.15  # Very high!
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        result = analyzer.estimate_impact("TestClass")

        assert result is not None
        assert result.importance_score == 0.15
        assert any("PageRank" in reason for reason in result.reasons)


# === FIND_DEPENDENCIES TESTS ===


class TestFindDependencies:
    """Test find_dependencies() method."""

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependencies_success(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con dipendenze trovate."""
        mock_search = MagicMock()

        # Mock symbols nel file
        symbol1 = MagicMock()
        symbol1.references = ["OtherClass", "helper_func"]
        symbol2 = MagicMock()
        symbol2.references = ["AnotherClass"]

        mock_search.extractor.extract_symbols.return_value = [symbol1, symbol2]

        # Mock find_symbol per risolvere references
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
        # Non include se stesso
        assert "/test/main.py" not in deps

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependencies_no_symbols(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con file senza simboli."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.return_value = []
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/empty.py")

        assert deps == []

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependencies_extraction_error(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con errore extraction."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.side_effect = Exception("Parse error")
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/broken.py")

        assert deps == []  # Graceful degradation

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependencies_self_reference_excluded(self, mock_search_class, temp_repo):
        """Verifica che self-references siano escluse."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.references = ["SelfClass"]
        mock_search.extractor.extract_symbols.return_value = [symbol]

        # SelfClass e definito nello stesso file
        mock_search.find_symbol.return_value = ("/test/main.py", 10)
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        deps = analyzer.find_dependencies("/test/main.py")

        assert deps == []  # Self-reference escluso


# === FIND_DEPENDENTS TESTS ===


class TestFindDependents:
    """Test find_dependents() method."""

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependents_success(self, mock_search_class, temp_repo):
        """Verifica find_dependents con dependents trovati."""
        mock_search = MagicMock()

        # Mock symbols nel file
        symbol1 = MagicMock()
        symbol1.name = "MyClass"
        symbol2 = MagicMock()
        symbol2.name = "my_function"

        mock_search.extractor.extract_symbols.return_value = [symbol1, symbol2]

        # Mock callers per ogni simbolo
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

        assert len(dependents) == 3  # caller1, caller2, caller3
        assert "/test/caller1.py" in dependents
        assert "/test/caller2.py" in dependents
        assert "/test/caller3.py" in dependents
        assert "/test/main.py" not in dependents  # Non include se stesso

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependents_no_symbols(self, mock_search_class, temp_repo):
        """Verifica find_dependents con file senza simboli."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.return_value = []
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        dependents = analyzer.find_dependents("/test/empty.py")

        assert dependents == []

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependents_extraction_error(self, mock_search_class, temp_repo):
        """Verifica find_dependents con errore extraction."""
        mock_search = MagicMock()
        mock_search.extractor.extract_symbols.side_effect = Exception("Parse error")
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)
        dependents = analyzer.find_dependents("/test/broken.py")

        assert dependents == []  # Graceful degradation


# === RISK CALCULATION TESTS ===


class TestRiskCalculation:
    """Test _calculate_risk_score() method."""

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_score_low(self, mock_search_class, temp_repo):
        """Verifica risk score LOW (< 0.3)."""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        # Mock symbol tipo type (peso 0.1), zero callers, bassa importance
        # base = 0.01 * 10 = 0.1, caller_factor = 0, type_factor = 0.1 => 0.2
        symbol = MagicMock()
        symbol.type = "type"

        risk = analyzer._calculate_risk_score(symbol, callers_count=0, importance_score=0.01)

        assert risk < 0.3

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_score_medium(self, mock_search_class, temp_repo):
        """Verifica risk score MEDIUM (0.3-0.5)."""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        # base = 0.01 * 10 = 0.1, caller_factor = 2/20 = 0.1, type_factor = 0.2 => 0.4
        symbol = MagicMock()
        symbol.type = "function"

        risk = analyzer._calculate_risk_score(symbol, callers_count=2, importance_score=0.01)

        assert 0.3 <= risk < 0.5

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_score_high(self, mock_search_class, temp_repo):
        """Verifica risk score HIGH (0.5-0.7)."""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        # base = 0.02 * 10 = 0.2, caller_factor = 6/20 = 0.3, type_factor = 0.1 => 0.6
        symbol = MagicMock()
        symbol.type = "type"

        risk = analyzer._calculate_risk_score(symbol, callers_count=6, importance_score=0.02)

        assert 0.5 <= risk < 0.7

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_score_critical(self, mock_search_class, temp_repo):
        """Verifica risk score CRITICAL (>= 0.7)."""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        risk = analyzer._calculate_risk_score(symbol, callers_count=25, importance_score=0.1)

        assert risk >= 0.7

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_score_capped_at_1(self, mock_search_class, temp_repo):
        """Verifica che risk score non superi mai 1.0."""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        symbol = MagicMock()
        symbol.type = "class"

        risk = analyzer._calculate_risk_score(symbol, callers_count=1000, importance_score=0.5)

        assert risk <= 1.0

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_type_weights(self, mock_search_class, temp_repo):
        """Verifica pesi diversi per type diversi."""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search

        analyzer = ImpactAnalyzer(temp_repo)

        # Class ha peso maggiore di function
        symbol_class = MagicMock()
        symbol_class.type = "class"
        risk_class = analyzer._calculate_risk_score(symbol_class, 10, 0.05)

        symbol_func = MagicMock()
        symbol_func.type = "function"
        risk_func = analyzer._calculate_risk_score(symbol_func, 10, 0.05)

        assert risk_class > risk_func


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

        # Callers include il file stesso (circular)
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

        # Deve gestire gracefully circular references
        assert result is not None
        assert result.files_affected >= 1

    @patch("impact_analyzer.SemanticSearch")
    def test_find_dependencies_empty_references(self, mock_search_class, temp_repo):
        """Verifica find_dependencies con simboli senza references."""
        mock_search = MagicMock()

        symbol = MagicMock()
        symbol.references = []  # Nessuna reference

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
        mock_search.find_callers.return_value = []  # Nessun caller
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
        symbol.type = "unknown_type"  # Type non previsto

        # Non deve crashare, usa default weight
        risk = analyzer._calculate_risk_score(symbol, 10, 0.05)

        assert 0.0 <= risk <= 1.0


class TestFullIntegration:
    """Test integrazione completa con scenari realistici."""

    @patch("impact_analyzer.SemanticSearch")
    def test_complete_workflow_single_symbol(self, mock_search_class, temp_repo):
        """Test workflow completo: init, estimate, dependencies, dependents."""
        # Setup mock completo
        mock_search = MagicMock()

        # Mock symbol
        symbol = MagicMock()
        symbol.name = "MyService"
        symbol.type = "class"
        symbol.file = "/test/services.py"
        symbol.line = 10
        symbol.references = ["HelperClass", "validate_func"]

        # Mock get_symbol_info
        mock_search.get_symbol_info.return_value = symbol

        # Mock callers (3 callers in 2 files)
        mock_search.find_callers.return_value = [
            ("/test/controller.py", 20, "UserController"),
            ("/test/controller.py", 40, "AdminController"),
            ("/test/api.py", 15, "api_handler"),
        ]

        # Mock importance
        mock_search.graph.get_symbol_importance.return_value = 0.03

        # Mock extractor per dependencies
        mock_search.extractor.extract_symbols.return_value = [symbol]

        # Mock find_symbol per references
        def find_symbol_side_effect(name):
            if name == "HelperClass":
                return ("/test/helpers.py", 5)
            elif name == "validate_func":
                return ("/test/validators.py", 10)
            return None

        mock_search.find_symbol.side_effect = find_symbol_side_effect

        mock_search_class.return_value = mock_search

        # Test workflow
        analyzer = ImpactAnalyzer(temp_repo)

        # 1. Estimate impact
        result = analyzer.estimate_impact("MyService")
        assert result is not None
        assert result.symbol_name == "MyService"
        assert result.callers_count == 3
        assert result.files_affected == 3  # services.py + controller.py + api.py

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

        # Multiple symbols in same file
        symbol1 = MagicMock()
        symbol1.name = "ClassA"
        symbol1.references = ["OtherClass"]

        symbol2 = MagicMock()
        symbol2.name = "ClassB"
        symbol2.references = ["YetAnother"]

        mock_search.extractor.extract_symbols.return_value = [symbol1, symbol2]

        # Mock find_symbol per tutte le references
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

        # Deve trovare entrambe le dipendenze
        assert len(deps) == 2
        assert "/test/other.py" in deps
        assert "/test/another.py" in deps

    @patch("impact_analyzer.SemanticSearch")
    def test_risk_levels_distribution(self, mock_search_class, temp_repo):
        """Test che tutti i risk levels siano raggiungibili."""
        mock_search_class.return_value = MagicMock()
        analyzer = ImpactAnalyzer(temp_repo)

        # Test tutti i boundary risk levels
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
