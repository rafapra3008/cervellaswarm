#!/usr/bin/env python3
"""Test suite for scripts/utils/measure_context_tokens.py - Core Functions"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import io

# Fix imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.utils.measure_context_tokens import (
    count_tokens,
    measure_file,
    print_table,
    CLAUDE_MD_FILES,
    HOOK_FILES,
    DNA_FILES,
)


# ============================================================================
# count_tokens Tests
# ============================================================================

def test_count_tokens_empty_string():
    """Should return 0 for empty string."""
    result = count_tokens("")
    assert result == 0


def test_count_tokens_single_word():
    """Should calculate tokens for single word."""
    result = count_tokens("hello")
    # words=1, tokens=1*1.3=1.3->1
    assert result == 1


def test_count_tokens_multiple_words():
    """Should calculate tokens for multiple words."""
    text = "hello world this is a test"
    result = count_tokens(text)
    # words=6, tokens=6*1.3=7.8->7
    assert result == 7


def test_count_tokens_formula():
    """Should apply formula: int(words * 1.3)."""
    text = " ".join(["word"] * 10)  # 10 words
    result = count_tokens(text)
    # 10 * 1.3 = 13.0 -> 13
    assert result == 13


def test_count_tokens_with_newlines():
    """Should count words correctly with newlines."""
    text = "line one\nline two\nline three"
    result = count_tokens(text)
    # words=6, tokens=6*1.3=7.8->7
    assert result == 7


def test_count_tokens_with_multiple_spaces():
    """Should handle multiple spaces between words."""
    text = "word1    word2     word3"
    result = count_tokens(text)
    # split() handles multiple spaces: words=3, tokens=3*1.3=3.9->3
    assert result == 3


# ============================================================================
# measure_file Tests
# ============================================================================

def test_measure_file_non_existing():
    """Should return exists=False for non-existing file."""
    fake_path = Path("/fake/path/to/file.txt")

    with patch.object(Path, 'exists', return_value=False):
        result = measure_file(fake_path)

    assert result["exists"] is False
    assert result["path"] == str(fake_path)
    assert "name" not in result
    assert "lines" not in result


def test_measure_file_existing():
    """Should measure existing file correctly."""
    fake_path = Path("/fake/file.txt")
    content = "line one\nline two\nline three"
    # lines=3, chars=28, words=6, tokens=7

    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.read_text.return_value = content
    mock_path.name = "file.txt"

    with patch('scripts.utils.measure_context_tokens.Path', return_value=mock_path):
        result = measure_file(mock_path)

    assert result["exists"] is True
    assert result["path"] == str(mock_path)
    assert result["name"] == "file.txt"
    assert result["lines"] == 3
    assert result["chars"] == 28
    assert result["words"] == 6
    assert result["tokens"] == 7


def test_measure_file_empty_file():
    """Should measure empty file correctly."""
    fake_path = Path("/fake/empty.txt")
    content = ""

    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.read_text.return_value = content
    mock_path.name = "empty.txt"

    with patch('scripts.utils.measure_context_tokens.Path', return_value=mock_path):
        result = measure_file(mock_path)

    assert result["exists"] is True
    assert result["lines"] == 1  # empty string split('\n') gives ['']
    assert result["chars"] == 0
    assert result["words"] == 0
    assert result["tokens"] == 0


def test_measure_file_single_line_no_newline():
    """Should measure single line file without trailing newline."""
    fake_path = Path("/fake/single.txt")
    content = "single line"

    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.read_text.return_value = content
    mock_path.name = "single.txt"

    with patch('scripts.utils.measure_context_tokens.Path', return_value=mock_path):
        result = measure_file(mock_path)

    assert result["exists"] is True
    assert result["lines"] == 1
    assert result["chars"] == 11
    assert result["words"] == 2
    assert result["tokens"] == 2  # int(2*1.3)=2


def test_measure_file_with_utf8():
    """Should handle UTF-8 content correctly."""
    fake_path = Path("/fake/utf8.txt")
    content = "hello 世界 café"

    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.read_text.return_value = content
    mock_path.name = "utf8.txt"

    with patch('scripts.utils.measure_context_tokens.Path', return_value=mock_path):
        result = measure_file(mock_path)

    assert result["exists"] is True
    assert result["words"] == 3
    assert result["tokens"] == 3  # int(3*1.3)=3


# ============================================================================
# print_table Tests
# ============================================================================

def test_print_table_all_existing_files():
    """Should print table with all existing files and return total tokens."""
    files = [Path("file1.txt"), Path("file2.txt")]
    results = [
        {"exists": True, "name": "file1.txt", "lines": 10, "chars": 100, "tokens": 20},
        {"exists": True, "name": "file2.txt", "lines": 15, "chars": 150, "tokens": 30},
    ]

    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        total_tokens = print_table("Test Files", files, results)

    output = captured_output.getvalue()

    # Check header
    assert "Test Files" in output
    assert "File" in output
    assert "Lines" in output
    assert "Chars" in output
    assert "Tokens" in output

    # Check data rows
    assert "file1.txt" in output
    assert "10" in output
    assert "100" in output
    assert "20" in output

    assert "file2.txt" in output
    assert "15" in output
    assert "150" in output
    assert "30" in output

    # Check totals
    assert "TOTALE" in output
    assert "25" in output  # 10+15 lines
    assert "250" in output  # 100+150 chars
    assert "50" in output  # 20+30 tokens

    # Check return value
    assert total_tokens == 50


def test_print_table_all_non_existing_files():
    """Should print N/A for non-existing files and return 0 tokens."""
    files = [Path("/fake/file1.txt"), Path("/fake/file2.txt")]
    results = [
        {"exists": False, "path": "/fake/file1.txt"},
        {"exists": False, "path": "/fake/file2.txt"},
    ]

    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        total_tokens = print_table("Missing Files", files, results)

    output = captured_output.getvalue()

    # Check N/A entries
    assert "file1.txt" in output
    assert "N/A" in output

    # Check totals are 0
    assert total_tokens == 0
    lines = output.split('\n')
    total_line = [l for l in lines if "TOTALE" in l][0]
    # Should have 0s
    assert "0" in total_line


def test_print_table_mixed_existing_and_non_existing():
    """Should handle mix of existing and non-existing files."""
    files = [Path("exists.txt"), Path("/fake/missing.txt")]
    results = [
        {"exists": True, "name": "exists.txt", "lines": 10, "chars": 100, "tokens": 20},
        {"exists": False, "path": "/fake/missing.txt"},
    ]

    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        total_tokens = print_table("Mixed Files", files, results)

    output = captured_output.getvalue()

    # Check existing file
    assert "exists.txt" in output
    assert "10" in output
    assert "100" in output
    assert "20" in output

    # Check non-existing file
    assert "missing.txt" in output
    assert "N/A" in output

    # Total should only include existing file
    assert total_tokens == 20


def test_print_table_empty_list():
    """Should handle empty file list."""
    files = []
    results = []

    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        total_tokens = print_table("Empty", files, results)

    output = captured_output.getvalue()

    assert "Empty" in output
    assert total_tokens == 0


def test_print_table_title_formatting():
    """Should format title and separators correctly."""
    files = []
    results = []

    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        print_table("Custom Title", files, results)

    output = captured_output.getvalue()

    # Check title appears
    assert "Custom Title" in output
    # Check separators (60 chars)
    assert "=" * 60 in output
    assert "-" * 35 in output  # Column separator


# ============================================================================
# Module Constants Tests
# ============================================================================

def test_claude_md_files_constant():
    """Should have CLAUDE_MD_FILES list with Path objects."""
    assert isinstance(CLAUDE_MD_FILES, list)
    assert len(CLAUDE_MD_FILES) == 3
    assert all(isinstance(f, Path) for f in CLAUDE_MD_FILES)

    # Check expected files
    assert any("COSTITUZIONE.md" in str(f) for f in CLAUDE_MD_FILES)
    assert any(".claude/CLAUDE.md" in str(f) for f in CLAUDE_MD_FILES)
    assert any("CervellaSwarm/CLAUDE.md" in str(f) for f in CLAUDE_MD_FILES)


def test_hook_files_constant():
    """Should have HOOK_FILES list with Path objects."""
    assert isinstance(HOOK_FILES, list)
    assert len(HOOK_FILES) == 2
    assert all(isinstance(f, Path) for f in HOOK_FILES)

    # Check expected files
    assert any("NORD.md" in str(f) for f in HOOK_FILES)
    assert any("PROMPT_RIPRESA_cervellaswarm.md" in str(f) for f in HOOK_FILES)


def test_dna_files_constant():
    """Should have DNA_FILES list with Path objects."""
    assert isinstance(DNA_FILES, list)
    assert len(DNA_FILES) == 3
    assert all(isinstance(f, Path) for f in DNA_FILES)

    # Check expected files (agent files)
    assert any("cervella-ingegnera.md" in str(f) for f in DNA_FILES)
    assert any("cervella-backend.md" in str(f) for f in DNA_FILES)
    assert any("cervella-frontend.md" in str(f) for f in DNA_FILES)
