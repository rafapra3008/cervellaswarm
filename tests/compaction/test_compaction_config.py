"""
Test per CervellaSwarm Compaction - Config e Handler.

Verifica che la configurazione per ogni ruolo sia corretta
e che l'handler gestisca correttamente le compaction responses.

Sessione 339 - FASE 3.1
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.compaction.config import (
    get_compaction_config,
    get_beta_headers,
    COMPACTION_CONFIG,
    BETA_HEADER,
    COMPACTION_TYPE,
)
from scripts.compaction.handler import (
    handle_compaction_response,
    extract_compaction_usage,
)


# === CONFIG TESTS ===


class TestCompactionConfig:
    """Test configurazione compaction per ruolo."""

    def test_regina_config_enabled(self):
        config = get_compaction_config("regina")
        assert config is not None
        edit = config["edits"][0]
        assert edit["type"] == COMPACTION_TYPE
        assert edit["trigger"]["value"] == 100_000
        assert edit["pause_after_compaction"] is True

    def test_guardiana_config_enabled(self):
        config = get_compaction_config("guardiana")
        assert config is not None
        edit = config["edits"][0]
        assert edit["trigger"]["value"] == 80_000
        assert edit["pause_after_compaction"] is False

    def test_architect_config_enabled(self):
        config = get_compaction_config("architect")
        assert config is not None
        edit = config["edits"][0]
        assert edit["trigger"]["value"] == 120_000
        assert edit["pause_after_compaction"] is True

    def test_worker_config_disabled(self):
        config = get_compaction_config("worker")
        assert config is None

    def test_security_config_enabled(self):
        config = get_compaction_config("security")
        assert config is not None
        edit = config["edits"][0]
        assert edit["trigger"]["value"] == 80_000

    def test_all_roles_have_config(self):
        expected_roles = ["regina", "guardiana", "worker", "architect", "ingegnera", "security"]
        for role in expected_roles:
            assert role in COMPACTION_CONFIG, f"Missing config for role: {role}"

    def test_enabled_roles_have_instructions(self):
        for role, config in COMPACTION_CONFIG.items():
            if config.get("enabled"):
                assert "instructions" in config, f"Missing instructions for {role}"
                assert len(config["instructions"]) > 50, f"Instructions too short for {role}"

    def test_trigger_values_reasonable(self):
        for role, config in COMPACTION_CONFIG.items():
            if config.get("enabled"):
                trigger = config["trigger"]
                assert trigger >= 50_000, f"Trigger too low for {role}: {trigger}"
                assert trigger <= 200_000, f"Trigger too high for {role}: {trigger}"

    def test_beta_headers(self):
        headers = get_beta_headers()
        assert isinstance(headers, list)
        assert BETA_HEADER in headers

    def test_config_structure(self):
        config = get_compaction_config("regina")
        assert "edits" in config
        assert len(config["edits"]) == 1
        edit = config["edits"][0]
        assert "type" in edit
        assert "trigger" in edit
        assert "pause_after_compaction" in edit
        assert "instructions" in edit

    def test_unknown_role_returns_none(self):
        config = get_compaction_config("unknown_role")
        assert config is None


# === HANDLER TESTS ===


class TestCompactionHandler:
    """Test handler per compaction responses."""

    def _make_response(self, stop_reason="end_turn", content=None):
        """Helper per creare mock response."""
        response = MagicMock()
        response.stop_reason = stop_reason
        response.content = content or [MagicMock(type="text", text="Hello")]
        return response

    def test_no_compaction_appends_normally(self):
        messages = [{"role": "user", "content": "test"}]
        response = self._make_response(stop_reason="end_turn")

        result = handle_compaction_response(response, messages)
        assert len(result) == 2
        assert result[1]["role"] == "assistant"

    def test_compaction_rebuilds_messages(self):
        messages = [
            {"role": "user", "content": "msg1"},
            {"role": "assistant", "content": "resp1"},
            {"role": "user", "content": "msg2"},
            {"role": "assistant", "content": "resp2"},
            {"role": "user", "content": "msg3"},
        ]

        compaction_block = MagicMock(type="compaction", content="summary")
        response = self._make_response(
            stop_reason="compaction",
            content=[compaction_block],
        )

        result = handle_compaction_response(response, messages, preserve_last_n=2)

        # compaction block + 2 preserved = 3 messages
        assert len(result) == 3
        assert result[0]["role"] == "assistant"
        assert result[0]["content"] == [compaction_block]

    def test_compaction_preserves_last_n(self):
        messages = [
            {"role": "user", "content": f"msg{i}"} for i in range(10)
        ]
        compaction_block = MagicMock()
        response = self._make_response(
            stop_reason="compaction",
            content=[compaction_block],
        )

        result = handle_compaction_response(response, messages, preserve_last_n=3)
        # 1 compaction + 3 preserved = 4
        assert len(result) == 4

    def test_compaction_with_fewer_messages_than_preserve(self):
        messages = [{"role": "user", "content": "only_one"}]
        compaction_block = MagicMock()
        response = self._make_response(
            stop_reason="compaction",
            content=[compaction_block],
        )

        result = handle_compaction_response(response, messages, preserve_last_n=5)
        # 1 compaction + 1 preserved (all we have)
        assert len(result) == 2


class TestExtractCompactionUsage:
    """Test estrazione metriche usage."""

    def test_no_iterations_returns_none(self):
        response = MagicMock()
        response.usage = MagicMock(spec=[])
        result = extract_compaction_usage(response)
        assert result is None

    def test_with_compaction_iterations(self):
        response = MagicMock()
        response.usage.iterations = [
            {"type": "compaction", "input_tokens": 180000, "output_tokens": 3500},
            {"type": "message", "input_tokens": 23000, "output_tokens": 1000},
        ]

        result = extract_compaction_usage(response)
        assert result is not None
        assert result["compaction_count"] == 1
        assert result["compaction_input_tokens"] == 180000
        assert result["message_input_tokens"] == 23000
        assert result["total_input_tokens"] == 203000

    def test_empty_iterations_returns_none(self):
        response = MagicMock()
        response.usage.iterations = []
        result = extract_compaction_usage(response)
        assert result is None

    def test_no_compaction_in_iterations(self):
        response = MagicMock()
        response.usage.iterations = [
            {"type": "message", "input_tokens": 5000, "output_tokens": 500},
        ]
        result = extract_compaction_usage(response)
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
