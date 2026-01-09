"""
Test base per Cervella

Verifica che i moduli siano importabili e funzionanti.
"""

import os
import sys
import tempfile
from pathlib import Path

# Aggiungi parent al path per import
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Verifica che tutti i moduli siano importabili."""
    # API
    from api.client import ClaudeClient, Message, Response
    assert ClaudeClient is not None
    assert Message is not None

    # SNCP
    from sncp.manager import SNSCPManager
    assert SNSCPManager is not None

    # Agents
    from agents.loader import AgentLoader, AgentDefinition, BUILTIN_AGENTS
    assert AgentLoader is not None
    assert len(BUILTIN_AGENTS) >= 5

    print("Tutti i moduli importati correttamente!")


def test_sncp_manager():
    """Verifica SNCP Manager."""
    from sncp.manager import SNSCPManager

    # Crea temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SNSCPManager(tmpdir)

        # Non inizializzato
        assert not manager.is_initialized()

        # Inizializza
        manager.initialize()
        assert manager.is_initialized()

        # Verifica struttura
        sncp_path = Path(tmpdir) / ".sncp"
        assert (sncp_path / "idee").exists()
        assert (sncp_path / "memoria" / "decisioni").exists()
        assert (sncp_path / "coscienza").exists()
        assert (sncp_path / "config.yaml").exists()

        # Test stats
        stats = manager.get_stats()
        assert stats["idee"] == 0
        assert stats["decisioni"] == 0

        # Test save idea
        filepath = manager.save_idea("Test Idea", "Contenuto di test")
        assert filepath.exists()
        stats = manager.get_stats()
        assert stats["idee"] == 1

        # Test save decision
        filepath = manager.save_decision(
            "Test Decision",
            "Ho deciso X",
            "Perché Y è meglio di Z"
        )
        assert filepath.exists()
        stats = manager.get_stats()
        assert stats["decisioni"] == 1

        print("SNCP Manager funziona correttamente!")


def test_agent_loader():
    """Verifica Agent Loader."""
    from agents.loader import AgentLoader, BUILTIN_AGENTS

    loader = AgentLoader()

    # Lista agenti
    agents = loader.list_agents()
    assert len(agents) >= 5

    # Get agente specifico
    backend = loader.get_agent("backend")
    assert backend is not None
    assert backend.name == "backend"
    assert "Python" in backend.description

    # Get con prefisso
    backend2 = loader.get_agent("cervella-backend")
    assert backend2 is not None
    assert backend2.name == backend.name

    # Agente non esistente
    fake = loader.get_agent("nonexistent")
    assert fake is None

    # Regina
    regina = loader.get_agent("regina")
    assert regina is not None
    assert regina.model == "opus"

    print("Agent Loader funziona correttamente!")


def test_api_client_init():
    """Verifica inizializzazione API client."""
    from api.client import ClaudeClient

    # Senza API key dovrebbe fallire
    old_key = os.environ.get("ANTHROPIC_API_KEY")
    if old_key:
        del os.environ["ANTHROPIC_API_KEY"]

    try:
        client = ClaudeClient()
        assert False, "Doveva fallire senza API key"
    except ValueError as e:
        assert "API key" in str(e)
        print("API client validation funziona!")
    finally:
        if old_key:
            os.environ["ANTHROPIC_API_KEY"] = old_key


if __name__ == "__main__":
    print("=" * 50)
    print("CERVELLA - Test Suite Base")
    print("=" * 50)

    test_imports()
    print()

    test_sncp_manager()
    print()

    test_agent_loader()
    print()

    test_api_client_init()
    print()

    print("=" * 50)
    print("TUTTI I TEST PASSATI!")
    print("=" * 50)
