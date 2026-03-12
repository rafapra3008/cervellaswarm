# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the observability hook transcript parser."""

import json
import tempfile
from pathlib import Path

import pytest

# Import hook functions directly
import sys
sys.path.insert(0, str(Path(__file__).parents[3] / ".claude" / "hooks"))
# We need cervella_hooks_common on the path for the import to work
sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))

from observability_hook import parse_transcript, find_transcript, store_usage


def _write_transcript(lines: list[dict], tmp_path: Path) -> Path:
    """Write a list of dicts as JSONL to a temp file."""
    filepath = tmp_path / "test_transcript.jsonl"
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")
    return filepath


class TestParseTranscript:
    def test_empty_file(self, tmp_path):
        filepath = tmp_path / "empty.jsonl"
        filepath.write_text("")
        result = parse_transcript(filepath)
        assert result["total_messages"] == 0
        assert result["input_tokens"] == 0

    def test_single_assistant_message(self, tmp_path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Hello"}],
                    "usage": {
                        "input_tokens": 100,
                        "output_tokens": 50,
                        "cache_read_input_tokens": 200,
                        "cache_creation_input_tokens": 30,
                    },
                },
            }
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["total_messages"] == 1
        assert result["input_tokens"] == 100
        assert result["output_tokens"] == 50
        assert result["cache_read_tokens"] == 200
        assert result["cache_creation_tokens"] == 30
        assert result["models"]["claude-opus-4-6"] == 1

    def test_multiple_messages(self, tmp_path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 100, "output_tokens": 50},
                },
            },
            {
                "type": "user",
                "message": {"content": "test"},
            },
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 200, "output_tokens": 100},
                },
            },
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["total_messages"] == 2  # Only assistant messages
        assert result["input_tokens"] == 300
        assert result["output_tokens"] == 150

    def test_tool_calls_counted(self, tmp_path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [
                        {"type": "text", "text": "Let me read that file."},
                        {"type": "tool_use", "name": "Read", "id": "t1"},
                        {"type": "tool_use", "name": "Bash", "id": "t2"},
                    ],
                    "usage": {"input_tokens": 50, "output_tokens": 30},
                },
            }
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["total_tool_calls"] == 2

    def test_mixed_models(self, tmp_path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 100, "output_tokens": 50},
                },
            },
            {
                "type": "assistant",
                "message": {
                    "model": "claude-sonnet-4-6",
                    "content": [],
                    "usage": {"input_tokens": 200, "output_tokens": 100},
                },
            },
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["models"]["claude-opus-4-6"] == 1
        assert result["models"]["claude-sonnet-4-6"] == 1

    def test_progress_messages_ignored(self, tmp_path):
        lines = [
            {"type": "progress", "data": {"something": True}},
            {"type": "progress", "data": {"something": False}},
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 100, "output_tokens": 50},
                },
            },
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["total_messages"] == 1

    def test_missing_usage_field(self, tmp_path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    # No usage field
                },
            }
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["total_messages"] == 1
        assert result["input_tokens"] == 0

    def test_malformed_json_lines_skipped(self, tmp_path):
        filepath = tmp_path / "bad.jsonl"
        with open(filepath, "w") as f:
            f.write("not valid json\n")
            f.write(json.dumps({
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 42, "output_tokens": 10},
                },
            }) + "\n")
        result = parse_transcript(filepath)
        assert result["total_messages"] == 1
        assert result["input_tokens"] == 42

    def test_nonexistent_file(self, tmp_path):
        result = parse_transcript(tmp_path / "nonexistent.jsonl")
        assert result["total_messages"] == 0

    def test_missing_cache_fields_default_to_zero(self, tmp_path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 100, "output_tokens": 50},
                    # No cache_read_input_tokens or cache_creation_input_tokens
                },
            }
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["cache_read_tokens"] == 0
        assert result["cache_creation_tokens"] == 0

    def test_system_messages_ignored(self, tmp_path):
        lines = [
            {"type": "system", "content": "system message"},
            {
                "type": "assistant",
                "message": {
                    "model": "claude-opus-4-6",
                    "content": [],
                    "usage": {"input_tokens": 10, "output_tokens": 5},
                },
            },
        ]
        result = parse_transcript(_write_transcript(lines, tmp_path))
        assert result["total_messages"] == 1


class TestFindTranscript:
    def test_nonexistent_dir(self):
        result = find_transcript("no-such-session", "/tmp/nonexistent-dir-xyz")
        assert result is None

    def test_with_real_project_dir(self, tmp_path):
        # Create a fake .claude-insiders project structure
        project_key = "-tmp-fakedir"
        project_dir = tmp_path / "projects" / project_key
        project_dir.mkdir(parents=True)

        # Write a fake transcript
        transcript = project_dir / "test-session-123.jsonl"
        transcript.write_text('{"type":"progress"}\n')

        # Monkey-patch home to use tmp_path
        import unittest.mock
        with unittest.mock.patch("pathlib.Path.home", return_value=tmp_path):
            # Rename to match expected .claude-insiders structure
            insiders_dir = tmp_path / ".claude-insiders" / "projects" / project_key
            insiders_dir.mkdir(parents=True)
            insiders_transcript = insiders_dir / "test-session-123.jsonl"
            insiders_transcript.write_text('{"type":"progress"}\n')

            result = find_transcript("test-session-123", "/tmp/fakedir")
            assert result is not None
            assert result.name == "test-session-123.jsonl"


class TestStoreUsage:
    def test_store_with_valid_data(self, tmp_path):
        import os
        db_path = tmp_path / "test-obs.db"
        os.environ["CERVELLASWARM_EVENT_STORE_DB"] = str(db_path)
        try:
            totals = {
                "input_tokens": 100,
                "output_tokens": 50,
                "cache_read_tokens": 200,
                "cache_creation_tokens": 30,
                "total_messages": 5,
                "total_tool_calls": 2,
                "models": {"claude-opus-4-6": 5},
            }
            result = store_usage("test-session", "cervellaswarm", totals)
            assert result is True

            # Verify data was stored
            from cervellaswarm_event_store.database import EventStore
            with EventStore(db_path) as store:
                summary = store.query_usage()
                assert summary.total_sessions == 1
                assert summary.total_input_tokens == 100
        finally:
            os.environ.pop("CERVELLASWARM_EVENT_STORE_DB", None)

    def test_store_with_empty_models(self, tmp_path):
        import os
        db_path = tmp_path / "test-obs2.db"
        os.environ["CERVELLASWARM_EVENT_STORE_DB"] = str(db_path)
        try:
            totals = {
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_tokens": 0,
                "cache_creation_tokens": 0,
                "total_messages": 0,
                "total_tool_calls": 0,
                "models": {},
            }
            result = store_usage("test-session", "test", totals)
            assert result is True
        finally:
            os.environ.pop("CERVELLASWARM_EVENT_STORE_DB", None)
