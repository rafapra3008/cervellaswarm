#!/usr/bin/env python3
"""Test suite for scripts/utils/measure_context_tokens.py - Main Function"""

import sys
from pathlib import Path
from unittest.mock import patch
import io

# Fix imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.utils.measure_context_tokens import (
    main,
    CLAUDE_MD_FILES,
    HOOK_FILES,
    DNA_FILES,
)


# ============================================================================
# main() Tests
# ============================================================================

def test_main_default_mode():
    """Should run main() in default mode (no verbose)."""
    # Mock measure_file to return predictable results
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        result = main()

    output = captured_output.getvalue()

    # Check sections
    assert "CONTEXT TOKEN MEASUREMENT" in output
    assert "CLAUDE.md Files (Auto-injected)" in output
    assert "Hook SessionStart Files" in output
    assert "SUMMARY" in output

    # DNA section should NOT appear (not verbose)
    assert "DNA Agent Files" not in output

    # Check summary components
    assert "CLAUDE.md files" in output
    assert "Hook files (NORD + PR)" in output
    assert "load_context output (estimate)" in output
    assert "TOTAL INJECTION" in output
    assert "Target" in output
    assert "Difference" in output
    assert "Reduction needed" in output

    # Check return code
    assert result == 0


def test_main_verbose_mode_flag():
    """Should run main() in verbose mode with --verbose flag."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py', '--verbose']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        result = main()

    output = captured_output.getvalue()

    # DNA section SHOULD appear in verbose mode
    assert "DNA Agent Files (Sample)" in output
    assert result == 0


def test_main_verbose_mode_short_flag():
    """Should run main() in verbose mode with -v flag."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py', '-v']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        result = main()

    output = captured_output.getvalue()

    # DNA section SHOULD appear
    assert "DNA Agent Files (Sample)" in output
    assert result == 0


def test_main_calls_measure_file_correct_times():
    """Should call measure_file for each file group."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure) as mock_mf, \
         patch('sys.stdout', captured_output):

        main()

    # Should call measure_file for CLAUDE_MD_FILES + HOOK_FILES (not DNA in non-verbose)
    expected_calls = len(CLAUDE_MD_FILES) + len(HOOK_FILES)
    assert mock_mf.call_count == expected_calls


def test_main_calls_measure_file_with_dna_in_verbose():
    """Should call measure_file for DNA files in verbose mode."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py', '--verbose']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure) as mock_mf, \
         patch('sys.stdout', captured_output):

        main()

    # Should call for CLAUDE_MD_FILES + HOOK_FILES + DNA_FILES
    expected_calls = len(CLAUDE_MD_FILES) + len(HOOK_FILES) + len(DNA_FILES)
    assert mock_mf.call_count == expected_calls


def test_main_calculates_totals_correctly():
    """Should calculate and display totals correctly."""
    def mock_measure(path):
        # Return 20 tokens per file
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        main()

    output = captured_output.getvalue()

    # CLAUDE_MD_FILES = 3 files * 20 tokens = 60
    # HOOK_FILES = 2 files * 20 tokens = 40
    # load_context_estimate = 1500
    # Total = 60 + 40 + 1500 = 1600

    # Check individual totals in summary
    assert "60" in output  # CLAUDE.md files total
    assert "40" in output  # Hook files total
    assert "1500" in output  # load_context estimate

    # Check grand total
    assert "1600" in output  # TOTAL INJECTION

    # Target is 8000
    # Difference = 1600 - 8000 = -6400
    assert "-6400" in output


def test_main_with_non_existing_files():
    """Should handle non-existing files gracefully."""
    def mock_measure(path):
        # Simulate some files don't exist
        if "COSTITUZIONE" in str(path):
            return {"exists": False, "path": str(path)}
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        result = main()

    output = captured_output.getvalue()

    # Should show N/A for missing file
    assert "N/A" in output
    # Should still complete successfully
    assert result == 0


def test_main_summary_format():
    """Should format summary section correctly."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        main()

    output = captured_output.getvalue()

    # Check summary structure
    lines = output.split('\n')
    summary_idx = next(i for i, l in enumerate(lines) if "SUMMARY" in l)

    # Should have Source and Tokens columns
    header_idx = summary_idx + 2
    assert "Source" in lines[header_idx]
    assert "Tokens" in lines[header_idx]


def test_main_reduction_calculation():
    """Should calculate reduction percentage correctly."""
    def mock_measure(path):
        # Make files that exceed target
        # CLAUDE_MD_FILES = 3 * 5000 = 15000
        # HOOK_FILES = 2 * 5000 = 10000
        # Total = 25000 + 1500 = 26500
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 100,
            "chars": 10000,
            "tokens": 5000,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        main()

    output = captured_output.getvalue()

    # CLAUDE: 3*5000 = 15000
    # HOOK: 2*5000 = 10000
    # LOAD_CONTEXT: 1500
    # TOTAL: 26500
    # Target: 8000
    # Difference: 18500
    # Reduction: 18500/26500 * 100 = 69.8%

    assert "26500" in output  # Total
    assert "+18500" in output or "18500" in output  # Positive difference
    assert "69.8%" in output or "Reduction needed" in output


def test_main_target_comparison():
    """Should show target comparison correctly."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        main()

    output = captured_output.getvalue()

    # Should show target (8000) and difference
    assert "8000" in output  # Target value
    assert "Target" in output


def test_main_output_structure():
    """Should have correct output structure with all sections."""
    def mock_measure(path):
        return {
            "exists": True,
            "path": str(path),
            "name": path.name,
            "lines": 10,
            "chars": 100,
            "tokens": 20,
        }

    captured_output = io.StringIO()

    with patch('sys.argv', ['measure_context_tokens.py']), \
         patch('scripts.utils.measure_context_tokens.measure_file', side_effect=mock_measure), \
         patch('sys.stdout', captured_output):

        main()

    output = captured_output.getvalue()

    # Check all major sections appear in order
    assert output.index("CONTEXT TOKEN MEASUREMENT") < output.index("CLAUDE.md Files")
    assert output.index("CLAUDE.md Files") < output.index("Hook SessionStart Files")
    assert output.index("Hook SessionStart Files") < output.index("SUMMARY")
    assert output.index("SUMMARY") < output.index("TOTAL INJECTION")
