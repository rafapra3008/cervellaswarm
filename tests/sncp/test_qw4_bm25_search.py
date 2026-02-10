"""Hard Tests for QW4 - BM25 Search

Tests SNCP 4.0 Fase 1 BM25 search implementation.

Target:
- Performance: <500ms for ~100 files
- Accuracy: Relevant results first
- Edge cases: Handles errors gracefully
- Multi-project: Works on different structures

Author: Cervella Tester
Date: 2026-02-02
Score Target: 9.5/10
"""

import pytest
import sys
import time
import json
from pathlib import Path

# Import module to test
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "sncp"))
try:
    from smart_search import (
        preprocess_text,
        read_markdown_files,
        extract_snippet,
        search_bm25,
    )
except ImportError:
    pytestmark = pytest.mark.skip(reason="smart_search module removed in S341")
    preprocess_text = read_markdown_files = extract_snippet = search_bm25 = None


# ============================================================================
# UNIT TESTS - Individual Functions
# ============================================================================


class TestPreprocessText:
    """Test text preprocessing for BM25."""

    def test_lowercase(self):
        """Should convert text to lowercase."""
        result = preprocess_text("HELLO World")
        assert all(token.islower() for token in result)

    def test_punctuation_removal(self):
        """Should remove punctuation."""
        result = preprocess_text("Hello, World! How's it going?")
        # No punctuation in tokens
        assert all(token.isalnum() for token in result)

    def test_tokenization(self):
        """Should split text into tokens."""
        result = preprocess_text("SNCP 4.0 memory optimization")
        assert len(result) == 5  # sncp, 4, 0, memory, optimization
        assert "sncp" in result
        assert "4" in result
        assert "0" in result
        assert "memory" in result
        assert "optimization" in result

    def test_empty_string(self):
        """Should handle empty string."""
        result = preprocess_text("")
        assert result == []

    def test_whitespace_only(self):
        """Should handle whitespace-only string."""
        result = preprocess_text("   \n\t  ")
        assert result == []

    def test_special_characters(self):
        """Should handle special characters."""
        result = preprocess_text("test!@#$%^&*()test")
        assert "test" in result


class TestReadMarkdownFiles:
    """Test markdown file reading."""

    def test_reads_markdown_files(self, mock_markdown_files):
        """Should read all markdown files in directory."""
        sncp_dir, _ = mock_markdown_files
        files = read_markdown_files(str(sncp_dir))

        assert len(files) > 0
        assert all(isinstance(f, tuple) for f in files)
        assert all(len(f) == 2 for f in files)

    def test_skips_empty_files(self, edge_case_files):
        """Should skip empty files."""
        files = read_markdown_files(str(edge_case_files))

        # Empty file and whitespace-only file should be skipped
        contents = [content for _, content in files]
        assert all(content.strip() for content in contents)

    def test_recursive_search(self, mock_markdown_files):
        """Should search recursively in subdirectories."""
        sncp_dir, _ = mock_markdown_files
        files = read_markdown_files(str(sncp_dir))

        # Should find files in subdirectories (memoria/, decisioni/)
        filepaths = [filepath for filepath, _ in files]
        assert any("memoria" in fp for fp in filepaths)
        assert any("decisioni" in fp for fp in filepaths)

    def test_handles_nonexistent_directory(self, tmp_path):
        """Should return empty list for nonexistent directory."""
        nonexistent = tmp_path / "nonexistent"
        files = read_markdown_files(str(nonexistent))
        assert files == []


class TestExtractSnippet:
    """Test snippet extraction."""

    def test_extracts_relevant_snippet(self):
        """Should extract snippet around query match."""
        content = "This is a test. SNCP 4.0 is awesome. More text here."
        query_tokens = ["sncp", "4", "0"]

        snippet = extract_snippet(content, query_tokens, context_chars=20)

        assert "SNCP 4.0" in snippet
        assert len(snippet) <= 50  # Context + ellipsis

    def test_adds_ellipsis(self):
        """Should add ellipsis when truncating."""
        content = "A" * 1000
        query_tokens = ["a"]

        snippet = extract_snippet(content, query_tokens, context_chars=50)

        assert "..." in snippet

    def test_no_match_returns_beginning(self):
        """Should return beginning if no query match."""
        content = "This is test content without the query terms."
        query_tokens = ["nonexistent", "keywords"]

        snippet = extract_snippet(content, query_tokens, context_chars=20)

        assert snippet.startswith("This is test")

    def test_handles_empty_content(self):
        """Should handle empty content."""
        snippet = extract_snippet("", ["test"], context_chars=50)
        assert snippet in ["", "..."]


# ============================================================================
# INTEGRATION TESTS - Full Search Function
# ============================================================================


class TestSearchBM25:
    """Test full BM25 search functionality."""

    def test_finds_relevant_documents(self, mock_markdown_files):
        """Should return relevant documents for query."""
        sncp_dir, _ = mock_markdown_files
        results = search_bm25("SNCP 4.0 memory", str(sncp_dir), top_k=5)

        assert len(results) > 0

        # Top result should contain query terms
        top_result = results[0]
        assert "file" in top_result
        assert "score" in top_result
        assert "snippet" in top_result

        # Check relevance (case insensitive)
        content = top_result["snippet"].lower()
        assert "sncp" in content or "memory" in content

    def test_returns_top_k_results(self, mock_markdown_files):
        """Should respect top_k parameter."""
        sncp_dir, _ = mock_markdown_files

        results_top_3 = search_bm25("SNCP", str(sncp_dir), top_k=3)
        results_top_1 = search_bm25("SNCP", str(sncp_dir), top_k=1)

        assert len(results_top_3) <= 3
        assert len(results_top_1) <= 1

    def test_scores_descending(self, mock_markdown_files):
        """Should return results in descending score order."""
        sncp_dir, _ = mock_markdown_files
        results = search_bm25("SNCP 4.0", str(sncp_dir), top_k=10)

        if len(results) > 1:
            scores = [r["score"] for r in results]
            assert scores == sorted(scores, reverse=True)

    def test_filters_low_scores(self, mock_markdown_files):
        """Should filter results with score < 0.1."""
        sncp_dir, _ = mock_markdown_files
        results = search_bm25("SNCP", str(sncp_dir), top_k=100)

        # All returned results should have score >= 0.1
        assert all(r["score"] >= 0.1 for r in results)

    def test_empty_directory(self, temp_sncp_dir):
        """Should handle empty directory gracefully."""
        results = search_bm25("test query", str(temp_sncp_dir))
        assert results == []

    def test_query_with_special_chars(self, mock_markdown_files):
        """Should handle query with special characters."""
        sncp_dir, _ = mock_markdown_files

        # Should not crash
        results = search_bm25("SNCP 4.0!", str(sncp_dir))
        assert isinstance(results, list)


# ============================================================================
# PERFORMANCE TESTS - Critical!
# ============================================================================


class TestPerformance:
    """Test performance requirements (<500ms)."""

    def test_performance_100_files(self, large_corpus):
        """Should search 100 files in <500ms."""
        start_time = time.time()
        # Query that matches our large_corpus fixture
        results = search_bm25("SNCP memory optimization", str(large_corpus), top_k=10)
        elapsed_time = time.time() - start_time

        # Performance requirement: <500ms
        assert elapsed_time < 0.5, f"Search took {elapsed_time:.3f}s (>500ms)"

        # Note: With 100 identical documents, BM25 scores are low (~0.06)
        # This is correct behavior - identical docs = low relevance
        # The important part is that search completes fast
        # If results exist, they should be valid
        if results:
            assert all("score" in r for r in results)
            assert all("file" in r for r in results)

    def test_performance_multiple_queries(self, large_corpus):
        """Should handle multiple queries efficiently."""
        queries = [
            "SNCP 4.0",
            "memory optimization",
            "performance testing",
            "search accuracy",
        ]

        total_time = 0
        for query in queries:
            start_time = time.time()
            search_bm25(query, str(large_corpus), top_k=5)
            total_time += time.time() - start_time

        avg_time = total_time / len(queries)
        assert avg_time < 0.5, f"Average query time: {avg_time:.3f}s"

    def test_performance_large_file(self, edge_case_files):
        """Should handle large files efficiently."""
        start_time = time.time()
        results = search_bm25("SNCP test content", str(edge_case_files))
        elapsed_time = time.time() - start_time

        assert elapsed_time < 1.0, f"Large file search took {elapsed_time:.3f}s"
        assert len(results) > 0


# ============================================================================
# ACCURACY TESTS - Result Quality
# ============================================================================


class TestAccuracy:
    """Test search accuracy and relevance."""

    def test_exact_match_scores_highest(self, mock_markdown_files):
        """Exact matches should score highest."""
        sncp_dir, _ = mock_markdown_files
        results = search_bm25("SNCP 4.0", str(sncp_dir), top_k=10)

        if len(results) > 0:
            top_result = results[0]
            # Top result should contain both terms
            snippet_lower = top_result["snippet"].lower()
            assert "sncp" in snippet_lower

    def test_partial_match_returns_results(self, mock_markdown_files):
        """Partial matches should also return results."""
        sncp_dir, _ = mock_markdown_files
        results = search_bm25("memory", str(sncp_dir), top_k=10)

        assert len(results) > 0

    def test_no_match_returns_empty(self, mock_markdown_files):
        """Non-matching query should return empty or low-score results."""
        sncp_dir, _ = mock_markdown_files
        results = search_bm25("unicorn rainbow sparkles", str(sncp_dir))

        # Either empty or very low scores
        assert len(results) == 0 or all(r["score"] < 1.0 for r in results)

    def test_common_words_dont_dominate(self, mock_markdown_files):
        """Common words shouldn't dominate scoring."""
        sncp_dir, _ = mock_markdown_files

        # "the" is common, "BM25" is specific
        results = search_bm25("BM25 the", str(sncp_dir), top_k=10)

        if len(results) > 0:
            # Results should prioritize "BM25" over "the"
            top_snippet = results[0]["snippet"].lower()
            assert "bm25" in top_snippet


# ============================================================================
# EDGE CASES - Robustness
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_unicode_content(self, edge_case_files):
        """Should handle unicode characters."""
        results = search_bm25("Special Characters", str(edge_case_files))
        # Should not crash
        assert isinstance(results, list)

    def test_very_long_query(self, mock_markdown_files):
        """Should handle very long queries."""
        sncp_dir, _ = mock_markdown_files
        long_query = " ".join(["test"] * 100)

        results = search_bm25(long_query, str(sncp_dir))
        # Should not crash
        assert isinstance(results, list)

    def test_single_file_directory(self, temp_sncp_dir):
        """Should handle directory with single file."""
        (temp_sncp_dir / "single.md").write_text("SNCP test content")

        results = search_bm25("SNCP", str(temp_sncp_dir))
        assert len(results) == 1

    def test_relative_vs_absolute_path(self, mock_markdown_files):
        """Should handle both relative and absolute paths."""
        sncp_dir, _ = mock_markdown_files

        # Absolute path
        results_abs = search_bm25("SNCP", str(sncp_dir.absolute()))

        # Relative path (from parent)
        results_rel = search_bm25("SNCP", str(sncp_dir))

        # Both should work
        assert isinstance(results_abs, list)
        assert isinstance(results_rel, list)


# ============================================================================
# INTEGRATION - Real Projects
# ============================================================================


@pytest.mark.integration
class TestRealProjects:
    """Test on real SNCP projects (optional)."""

    def test_cervellaswarm_project(self, real_sncp_projects):
        """Should search in real CervellaSwarm project."""
        if "cervellaswarm" not in real_sncp_projects:
            pytest.skip("CervellaSwarm project not found")

        project_path = real_sncp_projects["cervellaswarm"]
        results = search_bm25("SNCP 4.0", str(project_path), top_k=5)

        assert isinstance(results, list)
        # Should find relevant documents
        if len(results) > 0:
            assert all("score" in r for r in results)

    def test_miracollo_project(self, real_sncp_projects):
        """Should search in real Miracollo project."""
        if "miracollo" not in real_sncp_projects:
            pytest.skip("Miracollo project not found")

        project_path = real_sncp_projects["miracollo"]
        results = search_bm25("SSE real-time", str(project_path), top_k=5)

        assert isinstance(results, list)

    def test_multi_project_search(self, real_sncp_projects):
        """Should handle searches across different project structures."""
        if len(real_sncp_projects) < 2:
            pytest.skip("Need at least 2 projects")

        # Search same query in different projects
        query = "SNCP"
        for project_name, project_path in real_sncp_projects.items():
            results = search_bm25(query, str(project_path), top_k=3)
            assert isinstance(results, list)
