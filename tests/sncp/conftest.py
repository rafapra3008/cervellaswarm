"""Pytest fixtures for SNCP tests.

Author: Cervella Tester
Date: 2026-02-02
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_sncp_dir(tmp_path):
    """Create temporary SNCP directory structure with test files."""
    sncp_dir = tmp_path / "test_sncp"
    progetti_dir = sncp_dir / "progetti" / "testproject"
    progetti_dir.mkdir(parents=True)

    return progetti_dir


@pytest.fixture
def mock_markdown_files(temp_sncp_dir):
    """Create mock markdown files for testing."""
    files = {
        "PROMPT_RIPRESA_testproject.md": """# Test Project

## Stato Attuale
SNCP 4.0 memory optimization in progress.
BM25 search implementation complete.

## Decisioni
- Using BM25Plus algorithm
- Target performance: <500ms
        """,

        "stato.md": """# Stato Test Project

**SNCP 4.0 Fase 1:**
- QW1: Auto-load daily logs ✅
- QW2: Memory flush trigger ✅
- QW3: SessionEnd hook ✅
- QW4: BM25 search ✅
        """,

        "memoria/2026-02-02.md": """# Daily Log 2026-02-02

## Sessione Mattina
- Testing BM25 search performance
- Target: <500ms per 100 files

## Note
SNCP 4.0 real-time optimization critical.
        """,

        "decisioni/architettura.md": """# Decisioni Architetturali

## BM25 vs TF-IDF
**Decisione:** BM25Plus
**Motivo:** Migliore per documenti corti
**Data:** 2026-02-02
        """,
    }

    # Create files
    created_files = []
    for filename, content in files.items():
        filepath = temp_sncp_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        created_files.append(str(filepath))

    return temp_sncp_dir, created_files


@pytest.fixture
def large_corpus(temp_sncp_dir):
    """Create large corpus of files for performance testing."""
    # Create 100 markdown files
    for i in range(100):
        filepath = temp_sncp_dir / f"file_{i:03d}.md"
        content = f"""# Document {i}

This is test document number {i}.
It contains various keywords for testing BM25 search.

## Topics
- SNCP 4.0 memory optimization
- Performance testing
- Search accuracy
- Document {i} specific content

## Random Content
{"Lorem ipsum dolor sit amet. " * 20}
        """
        filepath.write_text(content)

    return temp_sncp_dir


@pytest.fixture
def edge_case_files(temp_sncp_dir):
    """Create edge case files for testing."""
    # Empty file
    (temp_sncp_dir / "empty.md").write_text("")

    # File with special characters
    (temp_sncp_dir / "special_chars.md").write_text("""
    # Special Characters Test

    Test with: !@#$%^&*()_+-=[]{}|;':",.<>?/
    Unicode: 🚀 ❤️‍🔥 ✅ 🧪
    """)

    # Very large file (>10k lines)
    large_content = "\n".join([f"Line {i}: SNCP test content" for i in range(10001)])
    (temp_sncp_dir / "very_large.md").write_text(large_content)

    # File with only whitespace
    (temp_sncp_dir / "whitespace.md").write_text("   \n\n\t\t\n   ")

    return temp_sncp_dir


@pytest.fixture
def real_sncp_projects():
    """Path to real SNCP projects for integration testing."""
    base_path = Path("/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti")

    projects = {
        "cervellaswarm": base_path / "cervellaswarm",
        "miracollo": base_path / "miracollo",
    }

    # Return only existing projects
    return {name: path for name, path in projects.items() if path.exists()}
