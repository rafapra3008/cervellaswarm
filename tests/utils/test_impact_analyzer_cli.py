"""Tests for scripts/utils/impact_analyzer_cli.py"""
import pytest
import sys
from unittest.mock import patch, MagicMock, PropertyMock
from scripts.utils.impact_analyzer_cli import main


@pytest.fixture
def mock_impact_result():
    """Create a mock ImpactResult."""
    result = MagicMock()
    result.symbol_name = "TestClass"
    result.risk_score = 0.75
    result.risk_level = "high"
    result.files_affected = 5
    result.callers_count = 3
    result.importance_score = 0.123456
    result.reasons = ["Used in 3 places", "High PageRank"]
    return result


@pytest.fixture
def mock_analyzer():
    """Create a mock ImpactAnalyzer."""
    analyzer = MagicMock()
    analyzer.get_stats.return_value = {
        "total_symbols": 100,
        "unique_names": 80,
        "graph_nodes": 90,
        "graph_edges": 150,
    }
    return analyzer


class TestImpactAnalyzerCLI:
    """Tests for impact_analyzer_cli main function."""

    def test_too_few_args_no_args(self, capsys):
        """Test with no arguments (< 3)."""
        with patch.object(sys, "argv", ["script.py"]):
            with pytest.raises(SystemExit) as excinfo:
                main()

            assert excinfo.value.code == 1
            captured = capsys.readouterr()
            assert "Usage:" in captured.out
            assert "<repo_root> <symbol_name>" in captured.out
            assert "Example:" in captured.out

    def test_too_few_args_one_arg(self, capsys):
        """Test with only one argument (< 3)."""
        with patch.object(sys, "argv", ["script.py", "/path/to/repo"]):
            with pytest.raises(SystemExit) as excinfo:
                main()

            assert excinfo.value.code == 1
            captured = capsys.readouterr()
            assert "Usage:" in captured.out
            assert "Estimate impact of modifying a symbol" in captured.out

    def test_happy_path_with_result_and_callers(self, capsys, mock_analyzer, mock_impact_result):
        """Test successful analysis with result found and callers > 0."""
        mock_impact_result.callers_count = 3
        mock_analyzer.estimate_impact.return_value = mock_impact_result
        mock_analyzer.search.find_callers.return_value = [
            ("file1.py", 10, "caller1"),
            ("file2.py", 20, "caller2"),
            ("file3.py", 30, "caller3"),
        ]

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()

        # Check initialization message
        assert "Initializing impact analyzer for: /repo" in captured.out

        # Check stats
        assert "Repository Statistics:" in captured.out
        assert "Total symbols: 100" in captured.out
        assert "Unique names: 80" in captured.out
        assert "Graph nodes: 90" in captured.out
        assert "Graph edges: 150" in captured.out

        # Check analysis message
        assert "Analyzing impact: TestClass" in captured.out

        # Check impact analysis output
        assert "IMPACT ANALYSIS: TestClass" in captured.out
        assert "Risk Level: HIGH" in captured.out
        assert "Risk Score: 0.75 / 1.00" in captured.out

        # Check metrics
        assert "Callers: 3" in captured.out
        assert "Files affected: 5" in captured.out
        assert "PageRank importance: 0.123456" in captured.out

        # Check reasons
        assert "Reasons:" in captured.out
        assert "1. Used in 3 places" in captured.out
        assert "2. High PageRank" in captured.out

        # Check callers list
        assert "Callers (3):" in captured.out
        assert "caller1 at file1.py:10" in captured.out
        assert "caller2 at file2.py:20" in captured.out
        assert "caller3 at file3.py:30" in captured.out

    def test_happy_path_with_result_no_callers(self, capsys, mock_analyzer, mock_impact_result):
        """Test successful analysis with result found but callers == 0."""
        mock_impact_result.callers_count = 0
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()

        # Check basic output
        assert "IMPACT ANALYSIS: TestClass" in captured.out
        assert "Callers: 0" in captured.out

        # Verify callers list not shown
        assert "Callers (0):" not in captured.out
        assert "caller1" not in captured.out

    def test_happy_path_with_many_callers(self, capsys, mock_analyzer, mock_impact_result):
        """Test successful analysis with callers > 10 (truncated list)."""
        mock_impact_result.callers_count = 15
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        # Create 15 callers
        callers = [(f"file{i}.py", i * 10, f"caller{i}") for i in range(15)]
        mock_analyzer.search.find_callers.return_value = callers

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()

        # Check callers list header
        assert "Callers (15):" in captured.out

        # Check first 10 are shown
        assert "caller0 at file0.py:0" in captured.out
        assert "caller9 at file9.py:90" in captured.out

        # Check truncation message
        assert "... and 5 more" in captured.out

        # Check that 11th caller is NOT shown
        assert "caller10" not in captured.out

    def test_symbol_not_found(self, capsys, mock_analyzer):
        """Test when symbol is not found (result is None)."""
        mock_analyzer.estimate_impact.return_value = None

        with patch.object(sys, "argv", ["script.py", "/repo", "UnknownClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()

        # Check stats are still shown
        assert "Repository Statistics:" in captured.out
        assert "Analyzing impact: UnknownClass" in captured.out

        # Check not found message
        assert "Symbol not found: UnknownClass" in captured.out

        # Verify no impact analysis shown
        assert "IMPACT ANALYSIS:" not in captured.out

    def test_value_error_exception(self, capsys):
        """Test ValueError exception handling."""
        with patch.object(sys, "argv", ["script.py", "/invalid/repo", "TestClass"]):
            with patch(
                "scripts.utils.impact_analyzer_cli.ImpactAnalyzer",
                side_effect=ValueError("Invalid repository path")
            ):
                with pytest.raises(SystemExit) as excinfo:
                    main()

                assert excinfo.value.code == 1

        captured = capsys.readouterr()
        assert "Invalid repository path" in captured.out

    def test_general_exception(self, capsys):
        """Test general Exception handling with traceback."""
        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch(
                "scripts.utils.impact_analyzer_cli.ImpactAnalyzer",
                side_effect=RuntimeError("Unexpected error occurred")
            ):
                with pytest.raises(SystemExit) as excinfo:
                    main()

                assert excinfo.value.code == 1

        captured = capsys.readouterr()
        assert "Unexpected error: Unexpected error occurred" in captured.out
        # Traceback should be printed to stderr
        assert "Traceback" in captured.err

    def test_logging_configuration(self, mock_analyzer, mock_impact_result):
        """Test that logging is properly configured."""
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                with patch("scripts.utils.impact_analyzer_cli.logging.basicConfig") as mock_logging:
                    main()

                    # Verify logging was configured
                    mock_logging.assert_called_once()
                    call_kwargs = mock_logging.call_args[1]
                    assert "level" in call_kwargs
                    assert "format" in call_kwargs

    def test_analyzer_initialization(self, mock_analyzer, mock_impact_result):
        """Test that ImpactAnalyzer is initialized with correct repo_root."""
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/test/repo/path", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer") as mock_init:
                mock_init.return_value = mock_analyzer
                main()

                # Verify analyzer was initialized with correct path
                mock_init.assert_called_once_with("/test/repo/path")

    def test_estimate_impact_called_correctly(self, mock_analyzer, mock_impact_result):
        """Test that estimate_impact is called with correct symbol name."""
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/repo", "MySymbol"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

                # Verify estimate_impact was called with correct symbol
                mock_analyzer.estimate_impact.assert_called_once_with("MySymbol")

    def test_find_callers_called_when_callers_exist(self, mock_analyzer, mock_impact_result):
        """Test that find_callers is called when callers_count > 0."""
        mock_impact_result.callers_count = 5
        mock_analyzer.estimate_impact.return_value = mock_impact_result
        mock_analyzer.search.find_callers.return_value = [
            ("file1.py", 10, "caller1"),
        ]

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

                # Verify find_callers was called
                mock_analyzer.search.find_callers.assert_called_once_with("TestClass")

    def test_risk_level_uppercase_conversion(self, capsys, mock_analyzer, mock_impact_result):
        """Test that risk_level is converted to uppercase in output."""
        mock_impact_result.risk_level = "medium"
        mock_impact_result.callers_count = 0
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()
        assert "Risk Level: MEDIUM" in captured.out

    def test_risk_score_formatting(self, capsys, mock_analyzer, mock_impact_result):
        """Test that risk_score is formatted to 2 decimal places."""
        mock_impact_result.risk_score = 0.87654
        mock_impact_result.callers_count = 0
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()
        assert "Risk Score: 0.88 / 1.00" in captured.out

    def test_importance_score_formatting(self, capsys, mock_analyzer, mock_impact_result):
        """Test that importance_score is formatted to 6 decimal places."""
        mock_impact_result.importance_score = 0.123456789
        mock_impact_result.callers_count = 0
        mock_analyzer.estimate_impact.return_value = mock_impact_result

        with patch.object(sys, "argv", ["script.py", "/repo", "TestClass"]):
            with patch("scripts.utils.impact_analyzer_cli.ImpactAnalyzer", return_value=mock_analyzer):
                main()

        captured = capsys.readouterr()
        assert "PageRank importance: 0.123457" in captured.out
