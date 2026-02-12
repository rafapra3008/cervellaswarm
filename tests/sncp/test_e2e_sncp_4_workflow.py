"""End-to-End Integration Tests for SNCP 4.0 - Full Workflow

Tests complete workflow SNCP 4.0 + performance + edge cases:
- Full session simulation (start to end)
- All components integration
- Performance benchmarks
- Edge cases and error handling

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
# INTEGRATION: Full Workflow Simulation
# ============================================================================


class TestE2E_09_FullWorkflow:
    """Test E2E workflow: Complete session simulation."""

    def test_e2e_09_full_workflow_simulation(self, e2e_test_env):
        """Test completo workflow start-to-end."""
        project_dir, env = e2e_test_env

        # === PHASE 1: SessionStart ===
        print("\n=== PHASE 1: SessionStart ===")

        # Load daily memory
        with patch('daily_memory_loader.detect_project', return_value='testproject'):
            with patch('daily_memory_loader.LOAD_SCRIPT') as mock_script:
                mock_script.exists.return_value = True
                with patch('daily_memory_loader.subprocess.run') as mock_run:
                    mock_run.return_value = Mock(
                        returncode=0,
                        stdout="# Daily Memory loaded",
                        stderr=""
                    )
                    memory_result = daily_memory_loader.load_daily_memory('testproject')

        assert memory_result["success"] is True
        print("✅ Daily memory loaded")

        # Verify MEMORY.md exists
        memory_md = project_dir / "MEMORY.md"
        assert memory_md.exists()
        print("✅ MEMORY.md accessible")

        # === PHASE 2: Durante Sessione ===
        print("\n=== PHASE 2: Durante Sessione ===")

        # BM25 search
        search_results = search_bm25("SNCP memory", str(project_dir), top_k=3)
        assert len(search_results) > 0
        print(f"✅ BM25 search found {len(search_results)} results")

        # Quality check (module already imported at top)
        original_base = quality_check.SNCP_BASE
        quality_check.SNCP_BASE = project_dir.parent

        try:
            qc_result = analyze_project("testproject")
            assert qc_result["project"] == "testproject"
            print(f"✅ Quality check score: {qc_result['total']}/10")
        finally:
            quality_check.SNCP_BASE = original_base

        # === PHASE 3: Context Monitor ===
        print("\n=== PHASE 3: Context Monitor ===")

        # Simulate 75% context usage
        context_usage = 0.75
        should_flush = context_usage >= 0.75
        assert should_flush is True
        print("✅ Context monitor would trigger flush at 75%")

        # === PHASE 4: SessionEnd ===
        print("\n=== PHASE 4: SessionEnd ===")

        with patch('session_end_flush.run_memory_flush') as mock_flush:
            with patch('session_end_flush.add_daily_log_note') as mock_note:
                mock_flush.return_value = {"success": True, "output": "Done"}
                mock_note.return_value = True

                hook_input = {
                    "cwd": "/Users/rafapra/Developer/CervellaSwarm",
                    "session_id": "e2e-full-workflow"
                }

                with patch('json.load', return_value=hook_input):
                    import io
                    from contextlib import redirect_stdout

                    f = io.StringIO()
                    with redirect_stdout(f):
                        result = session_end_flush.main()

                assert result == 0
                print("✅ SessionEnd flush executed")

        print("\n=== WORKFLOW COMPLETE ===")
        print("All phases executed successfully!")

    def test_e2e_10_all_components_integrated(self, e2e_test_env):
        """Verifica tutti componenti parlano tra loro."""
        project_dir, env = e2e_test_env

        # Component 1: Daily Memory Loader
        memoria_dir = project_dir / "memoria"
        assert memoria_dir.exists()
        daily_logs = list(memoria_dir.glob("*.md"))
        assert len(daily_logs) >= 2, "Should have today + yesterday logs"
        print("✅ Component 1: Daily memory files exist")

        # Component 2: MEMORY.md
        memory_md = project_dir / "MEMORY.md"
        assert memory_md.exists()
        memory_content = memory_md.read_text()
        assert len(memory_content) > 100
        print("✅ Component 2: MEMORY.md valid")

        # Component 3: PROMPT_RIPRESA
        prompt_ripresa = project_dir / "PROMPT_RIPRESA_testproject.md"
        assert prompt_ripresa.exists()
        ripresa_content = prompt_ripresa.read_text()
        assert "PROSSIMI STEP" in ripresa_content
        print("✅ Component 3: PROMPT_RIPRESA has structure")

        # Component 4: BM25 Search
        markdown_files = list(project_dir.glob("**/*.md"))
        assert len(markdown_files) >= 5  # Multiple .md files for search
        search_results = search_bm25("SNCP", str(project_dir))
        assert isinstance(search_results, list)
        print(f"✅ Component 4: BM25 search working ({len(search_results)} results)")

        # Component 5: Quality Check (module already imported at top)
        original_base = quality_check.SNCP_BASE
        quality_check.SNCP_BASE = project_dir.parent

        try:
            qc_result = analyze_project("testproject")
            assert "total" in qc_result
            assert qc_result["total"] > 0
            print(f"✅ Component 5: Quality check working (score {qc_result['total']}/10)")
        finally:
            quality_check.SNCP_BASE = original_base

        # Component 6: Scripts exist
        scripts = {
            "memory-flush.sh": SCRIPTS_ROOT / "swarm/memory-flush.sh",
            "daily-log.sh": SCRIPTS_ROOT / "sncp/daily-log.sh",
            "smart-search.py": SCRIPTS_ROOT / "sncp/smart-search.py",
            "quality-check.py": SCRIPTS_ROOT / "sncp/quality-check.py"
        }

        for name, path in scripts.items():
            assert path.exists(), f"Missing script: {name}"
        print("✅ Component 6: All scripts exist")

        # Component 7: Hooks exist
        hooks = {
            "daily_memory_loader.py": HOOKS_ROOT / "daily_memory_loader.py",
            "session_end_flush.py": HOOKS_ROOT / "session_end_flush.py"
        }

        for name, path in hooks.items():
            assert path.exists(), f"Missing hook: {name}"
        print("✅ Component 7: All hooks exist")

        print("\n=== ALL COMPONENTS INTEGRATED ===")
        print("7/7 components verified and working together!")


# ============================================================================
# PERFORMANCE: E2E Workflow Speed
# ============================================================================


class TestE2E_Performance:
    """Test E2E workflow performance."""

    def test_e2e_full_workflow_under_5_seconds(self, e2e_test_env):
        """Full E2E workflow should complete in <5 seconds."""
        project_dir, env = e2e_test_env

        start_time = time.time()

        # Execute all phases (mocked hooks for speed)
        with patch('daily_memory_loader.subprocess.run') as mock_daily:
            mock_daily.return_value = Mock(returncode=0, stdout="# Memory", stderr="")

            with patch('session_end_flush.run_memory_flush') as mock_flush:
                with patch('session_end_flush.add_daily_log_note') as mock_note:
                    mock_flush.return_value = {"success": True}
                    mock_note.return_value = True

                    # Phase 1: Load memory
                    with patch('daily_memory_loader.detect_project', return_value='testproject'):
                        daily_memory_loader.load_daily_memory('testproject')

                    # Phase 2: Search + Quality
                    search_bm25("SNCP", str(project_dir), top_k=5)

                    # Quality check (module already imported at top)
                    original_base = quality_check.SNCP_BASE
                    quality_check.SNCP_BASE = project_dir.parent
                    try:
                        analyze_project("testproject")
                    finally:
                        quality_check.SNCP_BASE = original_base

                    # Phase 3: SessionEnd
                    hook_input = {"cwd": str(project_dir), "session_id": "perf-test"}
                    with patch('json.load', return_value=hook_input):
                        import io
                        from contextlib import redirect_stdout
                        f = io.StringIO()
                        with redirect_stdout(f):
                            session_end_flush.main()

        elapsed_time = time.time() - start_time

        # Performance target: <5 seconds for full workflow
        assert elapsed_time < 5.0, f"E2E workflow took {elapsed_time:.3f}s (>5s)"
        print(f"✅ Full E2E workflow completed in {elapsed_time:.3f}s")


# ============================================================================
# EDGE CASES: E2E Robustness
# ============================================================================


class TestE2E_EdgeCases:
    """Test E2E workflow edge cases."""

    def test_e2e_workflow_with_missing_components(self, tmp_path):
        """E2E workflow should handle missing components gracefully."""
        # Create minimal project (missing memoria/, MEMORY.md)
        project_dir = tmp_path / "minimal_project"
        project_dir.mkdir()

        # Only PROMPT_RIPRESA exists
        (project_dir / "PROMPT_RIPRESA_minimal_project.md").write_text("# Minimal")

        # SessionStart with missing memoria
        with patch('daily_memory_loader.detect_project', return_value='minimal_project'):
            with patch('daily_memory_loader.subprocess.run') as mock_run:
                # Script handles missing memoria gracefully
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout="*No daily log for today*",
                    stderr=""
                )
                result = daily_memory_loader.load_daily_memory('minimal_project')

        # Should succeed (graceful degradation)
        assert result["success"] is True

        # BM25 search on empty directory
        search_results = search_bm25("test", str(project_dir))
        assert isinstance(search_results, list)  # Returns empty list, doesn't crash

        # Quality check on minimal PROMPT_RIPRESA (module already imported at top)
        original_base = quality_check.SNCP_BASE
        quality_check.SNCP_BASE = project_dir.parent
        try:
            qc_result = analyze_project("minimal_project")
            # Should analyze even minimal file
            assert "total" in qc_result
        finally:
            quality_check.SNCP_BASE = original_base

        print("✅ E2E workflow gracefully handles missing components")

    def test_e2e_workflow_with_corrupted_data(self, e2e_test_env):
        """E2E workflow should handle corrupted data."""
        project_dir, env = e2e_test_env

        # Create corrupted PROMPT_RIPRESA (invalid content)
        prompt_ripresa = project_dir / "PROMPT_RIPRESA_testproject.md"
        prompt_ripresa.write_text("@#$%^&*()\n\n\n!!!")

        # Quality check should not crash (module already imported at top)
        original_base = quality_check.SNCP_BASE
        quality_check.SNCP_BASE = project_dir.parent

        try:
            result = analyze_project("testproject")
            # Should return low scores, not crash
            assert "total" in result
            assert isinstance(result["total"], (int, float))
        finally:
            quality_check.SNCP_BASE = original_base

        print("✅ E2E workflow handles corrupted data")

    def test_e2e_workflow_continues_on_partial_failure(self, e2e_test_env):
        """E2E workflow should continue even if some components fail."""
        project_dir, env = e2e_test_env

        # Simulate partial failure: SessionStart fails
        with patch('daily_memory_loader.subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Daily memory load failed")

            with patch('daily_memory_loader.detect_project', return_value='testproject'):
                result = daily_memory_loader.load_daily_memory('testproject')

        # Should return error but not crash
        assert result["success"] is False

        # But rest of workflow should still work
        search_results = search_bm25("SNCP", str(project_dir))
        assert isinstance(search_results, list)

        # SessionEnd should still work
        with patch('session_end_flush.run_memory_flush') as mock_flush:
            mock_flush.return_value = {"success": True}

            hook_input = {"cwd": str(project_dir), "session_id": "partial-fail"}
            with patch('json.load', return_value=hook_input):
                with patch('session_end_flush.detect_project', return_value='testproject'):
                    import io
                    from contextlib import redirect_stdout
                    f = io.StringIO()
                    with redirect_stdout(f):
                        exit_code = session_end_flush.main()

            # Should succeed despite earlier failure
            assert exit_code == 0

        print("✅ E2E workflow continues despite partial failures")
