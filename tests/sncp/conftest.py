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


# ============================================================================
# QW1 FIXTURES - Daily Memory Auto-Load
# ============================================================================


@pytest.fixture
def sncp_test_env(tmp_path):
    """Create SNCP_ROOT environment variable for tests."""
    import os
    env = os.environ.copy()
    env["SNCP_ROOT"] = str(tmp_path)
    return env, tmp_path


@pytest.fixture
def mock_daily_logs_both(sncp_test_env):
    """Create project with both today and yesterday logs."""
    from datetime import datetime, timedelta

    env, tmp_path = sncp_test_env
    project_dir = tmp_path / "testproject"
    memoria_dir = project_dir / "memoria"
    memoria_dir.mkdir(parents=True)

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Today's log
    (memoria_dir / f"{today}.md").write_text(f"""# Daily Log {today}

## Sessione Mattina
- Testing QW1 implementation
- Daily memory auto-load

## Note
Today's log content for testing.
""")

    # Yesterday's log
    (memoria_dir / f"{yesterday}.md").write_text(f"""# Daily Log {yesterday}

## Sessione Pomeriggio
- Completed previous tasks
- Ready for new session

## Note
Yesterday's log content for testing.
""")

    return project_dir, env


@pytest.fixture
def mock_daily_logs_today(sncp_test_env):
    """Create project with only today's log."""
    from datetime import datetime

    env, tmp_path = sncp_test_env
    project_dir = tmp_path / "testproject"
    memoria_dir = project_dir / "memoria"
    memoria_dir.mkdir(parents=True)

    today = datetime.now().strftime("%Y-%m-%d")

    (memoria_dir / f"{today}.md").write_text(f"""# Daily Log {today}

## Sessione
- Only today's log exists

## Note
Testing missing yesterday scenario.
""")

    return project_dir, env


@pytest.fixture
def mock_daily_logs_empty(sncp_test_env):
    """Create project with no logs."""
    env, tmp_path = sncp_test_env
    project_dir = tmp_path / "testproject"
    memoria_dir = project_dir / "memoria"
    memoria_dir.mkdir(parents=True)

    return project_dir, env


@pytest.fixture
def mock_project_no_memoria(sncp_test_env):
    """Create project without memoria directory."""
    env, tmp_path = sncp_test_env
    project_dir = tmp_path / "testproject"
    project_dir.mkdir(parents=True)

    return project_dir, env


@pytest.fixture
def mock_daily_logs_special_chars(sncp_test_env):
    """Create log with special characters."""
    from datetime import datetime

    env, tmp_path = sncp_test_env
    project_dir = tmp_path / "testproject"
    memoria_dir = project_dir / "memoria"
    memoria_dir.mkdir(parents=True)

    today = datetime.now().strftime("%Y-%m-%d")

    (memoria_dir / f"{today}.md").write_text("""# Daily Log with Special Chars

## Content
- Emoji: 🚀 ❤️‍🔥 ✅ 🧪
- Quotes: "double" and 'single'
- Unicode: Ñoño, café, naïve
- Special: !@#$%^&*()

## Note
Testing JSON escaping.
""")

    return project_dir, env


@pytest.fixture
def mock_daily_logs_large(sncp_test_env):
    """Create project with very large log file (>10k lines)."""
    from datetime import datetime

    env, tmp_path = sncp_test_env
    project_dir = tmp_path / "testproject"
    memoria_dir = project_dir / "memoria"
    memoria_dir.mkdir(parents=True)

    today = datetime.now().strftime("%Y-%m-%d")

    # Generate large content
    lines = [f"Line {i}: Daily log content for performance testing" for i in range(10001)]
    large_content = "\n".join(lines)

    (memoria_dir / f"{today}.md").write_text(f"""# Daily Log {today}

{large_content}
""")

    return project_dir, env
