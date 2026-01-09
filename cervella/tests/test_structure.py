"""
Test struttura - Verifica senza dipendenze esterne
"""

import os
import sys
import tempfile
from pathlib import Path

# Aggiungi parent al path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_sncp_manager():
    """Verifica SNCP Manager (no external deps)."""
    from sncp.manager import SNSCPManager

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SNSCPManager(tmpdir)

        # Non inizializzato
        assert not manager.is_initialized()
        print("  - is_initialized() OK")

        # Inizializza
        manager.initialize()
        assert manager.is_initialized()
        print("  - initialize() OK")

        # Verifica struttura
        sncp_path = Path(tmpdir) / ".sncp"
        assert (sncp_path / "idee").exists()
        assert (sncp_path / "memoria" / "decisioni").exists()
        assert (sncp_path / "coscienza").exists()
        assert (sncp_path / "config.yaml").exists()
        print("  - struttura cartelle OK")

        # Test stats
        stats = manager.get_stats()
        assert stats["idee"] == 0
        print("  - get_stats() OK")

        # Test save idea
        filepath = manager.save_idea("Test Idea", "Contenuto")
        assert filepath.exists()
        print("  - save_idea() OK")

        # Test save decision
        filepath = manager.save_decision("Test", "Decisione", "Perché")
        assert filepath.exists()
        print("  - save_decision() OK")

        # Test checkpoint
        filepath = manager.create_checkpoint("Test checkpoint")
        assert filepath.exists()
        print("  - create_checkpoint() OK")

    print("SNCP Manager: PASS")


def test_agent_loader():
    """Verifica Agent Loader (no external deps)."""
    from agents.loader import AgentLoader, BUILTIN_AGENTS

    loader = AgentLoader()

    # Lista agenti
    agents = loader.list_agents()
    assert len(agents) >= 5
    print(f"  - list_agents() OK ({len(agents)} agenti)")

    # Get agente
    backend = loader.get_agent("backend")
    assert backend is not None
    assert backend.name == "backend"
    print("  - get_agent('backend') OK")

    # Regina
    regina = loader.get_agent("regina")
    assert regina is not None
    assert regina.model == "opus"
    print("  - get_agent('regina') OK")

    # Agente non esistente
    fake = loader.get_agent("nonexistent")
    assert fake is None
    print("  - agente non esistente handled OK")

    print("Agent Loader: PASS")


def test_file_structure():
    """Verifica struttura file progetto."""
    base = Path(__file__).parent.parent

    required_files = [
        "pyproject.toml",
        "cli/__init__.py",
        "cli/__main__.py",
        "cli/commands/init.py",
        "cli/commands/task.py",
        "cli/commands/status.py",
        "cli/commands/checkpoint.py",
        "api/__init__.py",
        "api/client.py",
        "sncp/__init__.py",
        "sncp/manager.py",
        "agents/__init__.py",
        "agents/loader.py",
        "agents/runner.py",
    ]

    for filepath in required_files:
        full_path = base / filepath
        assert full_path.exists(), f"Missing: {filepath}"
        print(f"  - {filepath} OK")

    print("File Structure: PASS")


if __name__ == "__main__":
    print("=" * 50)
    print("CERVELLA - Structure Tests")
    print("=" * 50)
    print()

    print("1. File Structure")
    test_file_structure()
    print()

    print("2. SNCP Manager")
    test_sncp_manager()
    print()

    print("3. Agent Loader")
    test_agent_loader()
    print()

    print("=" * 50)
    print("TUTTI I TEST PASSATI!")
    print("=" * 50)
