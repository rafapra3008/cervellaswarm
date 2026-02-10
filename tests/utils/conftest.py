"""
Shared fixtures per tests/utils/.

Sessione 341 - Estratte da test_impact_analyzer_*.py (DRY).
"""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_symbol():
    """Mock Symbol object."""
    symbol = MagicMock()
    symbol.name = "TestClass"
    symbol.type = "class"
    symbol.file = "/test/file.py"
    symbol.line = 10
    symbol.references = ["OtherClass", "helper_func"]
    return symbol


@pytest.fixture
def temp_repo(tmp_path):
    """Temporary repo directory."""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    (repo / "main.py").write_text("class Main: pass")
    (repo / "utils.py").write_text("def helper(): pass")
    return str(repo)
