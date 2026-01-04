"""
Test suite for hello module.

Tests the hello_world() function from api/hello.py.
Created by: cervella-tester
Task: TASK_GOLD_TESTER
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.hello import hello_world


class TestHelloWorld:
    """Test cases for hello_world function."""

    def test_hello_world_returns_string(self):
        """Test that hello_world returns a string type."""
        result = hello_world()
        assert isinstance(result, str), "hello_world should return a string"

    def test_hello_world_correct_message(self):
        """Test that hello_world returns the correct greeting message."""
        expected = "Hello CervellaSwarm!"
        result = hello_world()
        assert result == expected, f"Expected '{expected}', got '{result}'"

    def test_hello_world_not_empty(self):
        """Test that hello_world does not return an empty string."""
        result = hello_world()
        assert len(result) > 0, "hello_world should not return empty string"

    def test_hello_world_contains_cervellaswarm(self):
        """Test that the greeting contains 'CervellaSwarm'."""
        result = hello_world()
        assert "CervellaSwarm" in result, "Greeting should mention CervellaSwarm"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
