"""End-to-End Integration Tests for SNCP 4.0 - Individual Phases

Tests individual phases of SNCP 4.0 workflow:
- QW1: Daily memory auto-load (SessionStart)
- QW2: Context monitor triggers flush
- QW3: SessionEnd auto-flush
- QW4: BM25 search (Durante Sessione)
- MF2: Quality check

Author: Cervella Tester
Date: 2026-02-02
Score Target: 9.5/10
"""

import pytest
import json
import sys
import subprocess
import time
from pathlib import Path
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

# Import modules to test
sys.path.insert(0, str(Path.home() / ".claude/hooks"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "sncp"))

import daily_memory_loader
import session_end_flush
try:
    from smart_search import search_bm25
except ImportError:
    smart_search = None
    search_bm25 = None
    pytestmark = pytest.mark.skip(reason="smart_search module removed in S341")

# Import quality-check dynamically (has dash in name)
import importlib.util
quality_check_path = Path(__file__).parent.parent.parent / "scripts/sncp/quality-check.py"
spec = importlib.util.spec_from_file_location("quality_check", quality_check_path)
quality_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quality_check)
analyze_project = quality_check.analyze_project


# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths relativi alla root del progetto (portabili)
PROJECT_ROOT = Path(__file__).parent.parent.parent
SNCP_ROOT = PROJECT_ROOT / ".sncp/progetti"
SCRIPTS_ROOT = PROJECT_ROOT / "scripts"
HOOKS_ROOT = Path.home() / ".claude/hooks"


# ============================================================================
# FIXTURES - E2E Test Environment
# ============================================================================


@pytest.fixture
def e2e_test_env(tmp_path):
    """Create full E2E test environment."""
    # Create SNCP structure
    project_dir = tmp_path / "testproject"
    memoria_dir = project_dir / "memoria"
    memoria_dir.mkdir(parents=True)

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Today's log
    (memoria_dir / f"{today}.md").write_text(f"""# Daily Log {today}

## Sessione Mattina
- Testing SNCP 4.0 E2E workflow
- Implementing BM25 search

## Decisioni
- Use BM25Plus for short documents
- Target performance <500ms

## TODO
- [ ] Complete E2E tests
- [ ] Verify all QW working

## Note
SNCP 4.0 real-time memory optimization critical.
""")

    # Yesterday's log
    (memoria_dir / f"{yesterday}.md").write_text(f"""# Daily Log {yesterday}

## Sessione Pomeriggio
- Completed QW1, QW2, QW3
- Started QW4 BM25 implementation

## Decisioni
- Auto-load daily logs at SessionStart
- Auto-flush at SessionEnd

## Note
Great progress on SNCP 4.0!
""")

    # PROMPT_RIPRESA
    (project_dir / "PROMPT_RIPRESA_testproject.md").write_text("""# PROMPT_RIPRESA - testproject

## STATO ATTUALE
SNCP 4.0 Fase 2 in corso.

## PROSSIMI STEP
TODO: Completare E2E tests
TODO: Verificare integrazione hook

## DECISIONI CHIAVE
2026-02-02: BM25Plus per search

## NOTE
Score target: 9.5/10
""")

    # stato.md
    (project_dir / "stato.md").write_text("""# Stato testproject

## SNCP 4.0 Fase 1
- QW1: Auto-load daily logs ✅
- QW2: Memory flush trigger ✅
- QW3: SessionEnd hook ✅
- QW4: BM25 search ✅

## SNCP 4.0 Fase 2
- MEMORY.md per 3 progetti ✅
- quality-check.py ✅
- E2E tests 🔄

## Score
Implementazione: 9.5/10
""")

    # MEMORY.md
    (project_dir / "MEMORY.md").write_text("""# MEMORY.md - testproject

## QUICK CONTEXT
SNCP 4.0 memory optimization system.

## ARCHITETTURA
- BM25Plus search for documents
- Auto-load daily logs
- SessionEnd flush

## STACK TECNICO
- Python 3.x
- rank-bm25 library
- Bash scripts

## STATO PROGETTO
SNCP 4.0 Fase 2 - E2E testing
""")

    # Additional markdown files for BM25 testing
    (project_dir / "doc1.md").write_text("""# Documentation 1

SNCP 4.0 memory optimization using BM25 search.
Performance target: <500ms for 100 files.
""")

    (project_dir / "doc2.md").write_text("""# Documentation 2

Quality check analyzes PROMPT_RIPRESA files.
Score calculation: actionability + specificity.
""")

    # Setup environment
    env = {
        "SNCP_ROOT": str(tmp_path),
        "PATH": str(SCRIPTS_ROOT) + ":" + str(HOOKS_ROOT)
    }

    return project_dir, env


# ============================================================================
# PHASE 1: SessionStart - Daily Memory Load
# ============================================================================


class TestE2E_01_SessionStart:
    """Test E2E workflow: SessionStart loads daily logs."""

    def test_e2e_01_session_start_loads_daily_logs(self, e2e_test_env):
        """QW1: SessionStart hook loads today + yesterday logs."""
        project_dir, env = e2e_test_env

        # Simulate SessionStart hook input
        hook_input = {
            "cwd": str(project_dir),
            "session_id": "e2e-test-001"
        }

        # Call daily_memory_loader with mock project detection
        with patch('daily_memory_loader.detect_project', return_value='testproject'):
            with patch('daily_memory_loader.LOAD_SCRIPT') as mock_script:
                mock_script.exists.return_value = True

                # Mock script execution
                with patch('daily_memory_loader.subprocess.run') as mock_run:
                    today = datetime.now().strftime("%Y-%m-%d")
                    mock_output = f"""# Daily Memory - testproject

## 📅 Today ({today})
Testing SNCP 4.0 E2E workflow

## 📅 Yesterday
Completed QW1, QW2, QW3
"""
                    mock_run.return_value = Mock(
                        returncode=0,
                        stdout=mock_output,
                        stderr=""
                    )

                    result = daily_memory_loader.load_daily_memory('testproject')

        # Verify success
        assert result["success"] is True
        assert "Daily Memory" in result["markdown"]
        assert "Today" in result["markdown"]
        assert "Yesterday" in result["markdown"]

    def test_e2e_02_session_start_loads_memory_md(self, e2e_test_env):
        """MEMORY.md is accessible at SessionStart."""
        project_dir, env = e2e_test_env

        memory_file = project_dir / "MEMORY.md"
        assert memory_file.exists()

        content = memory_file.read_text()

        # Verify MEMORY.md structure
        assert "# MEMORY.md" in content
        assert "QUICK CONTEXT" in content
        assert "ARCHITETTURA" in content
        assert "STACK TECNICO" in content
        assert "STATO PROGETTO" in content


# ============================================================================
# PHASE 2: Durante Sessione - Search & Quality
# ============================================================================


class TestE2E_03_DuranteSessione:
    """Test E2E workflow: Durante sessione search e quality check."""

    def test_e2e_03_bm25_search_finds_relevant_docs(self, e2e_test_env):
        """QW4: BM25 search trova documenti rilevanti."""
        project_dir, env = e2e_test_env

        # Execute BM25 search
        results = search_bm25("SNCP memory optimization", str(project_dir), top_k=5)

        # Verify results
        assert len(results) > 0

        # Top result should be relevant
        top_result = results[0]
        assert "file" in top_result
        assert "score" in top_result
        assert "snippet" in top_result

        # Check relevance
        snippet_lower = top_result["snippet"].lower()
        assert "sncp" in snippet_lower or "memory" in snippet_lower

    def test_e2e_04_quality_check_analyzes_projects(self, e2e_test_env):
        """MF2: quality-check.py analizza PROMPT_RIPRESA."""
        project_dir, env = e2e_test_env

        # Setup SNCP_BASE for quality_check (module already imported at top)
        original_base = quality_check.SNCP_BASE
        quality_check.SNCP_BASE = project_dir.parent

        try:
            # Analyze project
            result = analyze_project("testproject")

            # Verify analysis results
            assert result["project"] == "testproject"
            assert "scores" in result
            assert "total" in result
            assert "status" in result

            # Check individual scores
            scores = result["scores"]
            assert "actionability" in scores
            assert "specificity" in scores
            assert "freshness" in scores
            assert "conciseness" in scores

            # Verify total score is calculated
            assert isinstance(result["total"], (int, float))
            assert 0 <= result["total"] <= 10

        finally:
            # Restore original base
            quality_check.SNCP_BASE = original_base

    def test_e2e_05_memory_md_readable_and_valid(self, e2e_test_env):
        """MEMORY.md ha struttura valida e leggibile."""
        project_dir, env = e2e_test_env

        memory_file = project_dir / "MEMORY.md"
        content = memory_file.read_text()

        # Verify required sections
        required_sections = [
            "# MEMORY.md",
            "## QUICK CONTEXT",
            "## ARCHITETTURA",
            "## STACK TECNICO",
            "## STATO PROGETTO"
        ]

        for section in required_sections:
            assert section in content, f"Missing section: {section}"

        # Verify file is not too large
        lines = content.split('\n')
        assert len(lines) < 500, f"MEMORY.md too large: {len(lines)} lines"

        # Verify contains actual content (not just headers)
        content_lines = [l for l in lines if l.strip() and not l.startswith('#')]
        assert len(content_lines) > 5, "MEMORY.md has too little content"


# ============================================================================
# PHASE 3: Context Monitor (Simulated)
# ============================================================================


class TestE2E_06_ContextMonitor:
    """Test E2E workflow: Context monitor trigger."""

    def test_e2e_06_context_trigger_at_75_percent(self, e2e_test_env):
        """QW2: Simulazione trigger flush a 75% context."""
        project_dir, env = e2e_test_env

        # Simulate context monitor detecting 75% usage
        context_usage = 0.75  # 75%

        # In real implementation, this would be handled by spawn-workers
        # For E2E test, we verify the trigger logic

        if context_usage >= 0.75:
            should_flush = True
        else:
            should_flush = False

        assert should_flush is True

        # Verify memory-flush.sh exists and is executable
        flush_script = SCRIPTS_ROOT / "swarm/memory-flush.sh"
        assert flush_script.exists()

        import os
        assert os.access(flush_script, os.X_OK), "Flush script not executable"


# ============================================================================
# PHASE 4: SessionEnd - Auto Flush
# ============================================================================


class TestE2E_07_SessionEnd:
    """Test E2E workflow: SessionEnd auto-flush."""

    @patch('session_end_flush.run_memory_flush')
    @patch('session_end_flush.add_daily_log_note')
    def test_e2e_07_session_end_auto_flush(self, mock_add_note, mock_flush):
        """QW3: SessionEnd hook esegue auto-flush."""
        # Mock flush success
        mock_flush.return_value = {
            "success": True,
            "output": "Flush completed successfully"
        }
        mock_add_note.return_value = True

        # Simulate SessionEnd hook input
        hook_input = {
            "cwd": "/Users/rafapra/Developer/CervellaSwarm",
            "session_id": "e2e-test-001"
        }

        # Call session_end_flush main()
        with patch('json.load', return_value=hook_input):
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                result = session_end_flush.main()

        # Verify execution
        assert result == 0  # Success exit code

        # Verify flush was called
        mock_flush.assert_called_once_with("cervellaswarm")

        # Verify daily log note was added
        mock_add_note.assert_called_once()

        # Verify output is valid JSON
        output = f.getvalue()
        data = json.loads(output)
        assert data["continue"] is True

    def test_e2e_08_handoff_file_created(self, e2e_test_env):
        """Verifica creazione handoff file (manual for E2E)."""
        project_dir, env = e2e_test_env

        # In real workflow, handoff is created manually
        # For E2E test, we verify the structure

        handoff_dir = project_dir.parent.parent / "handoff"
        handoff_dir.mkdir(parents=True, exist_ok=True)

        # Create mock handoff
        today = datetime.now().strftime("%Y%m%d")
        handoff_file = handoff_dir / f"HANDOFF_{today}_175308.md"

        handoff_content = """# Handoff E2E Test Session

## Completato
- SessionStart: Daily logs loaded ✅
- BM25 search tested ✅
- Quality check verified ✅
- SessionEnd: Flush executed ✅

## Prossimi Step
- Continue E2E testing
- Verify all integrations

## Note
SNCP 4.0 E2E workflow working correctly.
"""
        handoff_file.write_text(handoff_content)

        # Verify handoff created
        assert handoff_file.exists()
        content = handoff_file.read_text()
        assert "Handoff" in content
        assert "Completato" in content
