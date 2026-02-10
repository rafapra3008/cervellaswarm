"""Tests for convert_agents_to_agent_hq.py"""
import pytest
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
import yaml

from scripts.convert_agents_to_agent_hq import (
    parse_frontmatter,
    convert_tools,
    get_handoff_for_agent,
    convert_agent,
    main,
    TOOL_MAPPING,
    MODEL_MAPPING,
)


# --- parse_frontmatter tests ---


def test_parse_frontmatter_valid():
    """Test parsing valid YAML frontmatter."""
    content = """---
name: test-agent
description: Test agent
tools: Read, Edit
model: sonnet
---

Agent body content here."""

    frontmatter, body = parse_frontmatter(content)

    assert frontmatter == {
        "name": "test-agent",
        "description": "Test agent",
        "tools": "Read, Edit",
        "model": "sonnet",
    }
    assert body == "Agent body content here."


def test_parse_frontmatter_no_frontmatter():
    """Test content without frontmatter."""
    content = "Just plain content without frontmatter"

    frontmatter, body = parse_frontmatter(content)

    assert frontmatter == {}
    assert body == content


def test_parse_frontmatter_no_closing_delimiter():
    """Test content with opening --- but no closing."""
    content = """---
name: test-agent
description: Test agent

More content without closing delimiter"""

    frontmatter, body = parse_frontmatter(content)

    assert frontmatter == {}
    assert body == content


def test_parse_frontmatter_empty():
    """Test empty frontmatter (just delimiters)."""
    content = """---
---

Body content here."""

    frontmatter, body = parse_frontmatter(content)

    assert frontmatter == {}
    assert body == "Body content here."


def test_parse_frontmatter_invalid_yaml():
    """Test invalid YAML in frontmatter."""
    content = """---
name: test-agent
invalid: yaml: content: here
---

Body content."""

    frontmatter, body = parse_frontmatter(content)

    # Should return empty dict on YAML error
    assert frontmatter == {}
    assert body == content


def test_parse_frontmatter_yaml_returns_none():
    """Test frontmatter that parses to None (e.g., just comments)."""
    content = """---
# Just a comment
# Another comment
---

Body content."""

    frontmatter, body = parse_frontmatter(content)

    assert frontmatter == {}
    assert body == "Body content."


# --- convert_tools tests ---


def test_convert_tools_empty():
    """Test empty tools_str returns defaults."""
    result = convert_tools("")
    assert set(result) == {"read", "edit", "search"}


def test_convert_tools_none():
    """Test None tools_str returns defaults."""
    result = convert_tools(None)
    assert set(result) == {"read", "edit", "search"}


def test_convert_tools_known_single():
    """Test single known tool."""
    result = convert_tools("Read")
    assert result == ["read"]


def test_convert_tools_known_multiple():
    """Test multiple known tools."""
    result = convert_tools("Read, Edit, Bash")
    assert set(result) == {"read", "edit", "terminal"}


def test_convert_tools_unknown():
    """Test unknown tool is lowercased."""
    result = convert_tools("CustomTool")
    assert result == ["customtool"]


def test_convert_tools_mixed():
    """Test mix of known and unknown tools."""
    result = convert_tools("Read, CustomTool, Bash")
    assert set(result) == {"read", "customtool", "terminal"}


def test_convert_tools_deduplication():
    """Test that tools mapping to same value are deduplicated."""
    # Both Glob and Grep map to "search"
    result = convert_tools("Glob, Grep")
    assert result == ["search"]


# --- get_handoff_for_agent tests ---


def test_get_handoff_guardian_agent():
    """Test guardians return None (no handoffs)."""
    assert get_handoff_for_agent("cervella-guardiana-qualita") is None
    assert get_handoff_for_agent("cervella-guardiana-ops") is None
    assert get_handoff_for_agent("cervella-guardiana-ricerca") is None


def test_get_handoff_orchestrator():
    """Test orchestrator returns None."""
    assert get_handoff_for_agent("cervella-orchestrator") is None


def test_get_handoff_frontend():
    """Test frontend agent gets qualita handoff."""
    result = get_handoff_for_agent("cervella-frontend")

    assert result is not None
    assert len(result) == 1
    assert result[0]["agent"] == "cervella-guardiana-qualita"
    assert result[0]["label"] == "Escalate to Quality Guardian"
    assert result[0]["send"] is False


def test_get_handoff_backend():
    """Test backend agent gets qualita handoff."""
    result = get_handoff_for_agent("cervella-backend")

    assert result is not None
    assert result[0]["agent"] == "cervella-guardiana-qualita"


def test_get_handoff_researcher():
    """Test researcher agent gets ricerca handoff."""
    result = get_handoff_for_agent("cervella-researcher")

    assert result is not None
    assert len(result) == 1
    assert result[0]["agent"] == "cervella-guardiana-ricerca"
    assert result[0]["label"] == "Escalate to Research Guardian"


def test_get_handoff_devops():
    """Test devops agent gets ops handoff."""
    result = get_handoff_for_agent("cervella-devops")

    assert result is not None
    assert len(result) == 1
    assert result[0]["agent"] == "cervella-guardiana-ops"
    assert result[0]["label"] == "Escalate to Ops Guardian"


def test_get_handoff_unknown():
    """Test unknown agent type returns None."""
    assert get_handoff_for_agent("cervella-marketing") is None
    assert get_handoff_for_agent("cervella-unknown") is None


# --- convert_agent tests ---


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
def test_convert_agent_basic(mock_dest_dir, tmp_path):
    """Test basic agent conversion."""
    # Setup
    source_file = tmp_path / "test-agent.md"
    source_content = """---
name: test-agent
description: Test agent
tools: Read, Edit
model: sonnet
---

Agent instructions here."""
    source_file.write_text(source_content)

    dest_file = MagicMock(spec=Path)
    mock_dest_dir.__truediv__.return_value = dest_file

    # Execute
    convert_agent(source_file)

    # Verify
    dest_file.write_text.assert_called_once()
    written_content = dest_file.write_text.call_args[0][0]

    # Parse written content
    frontmatter, body = parse_frontmatter(written_content)

    assert frontmatter["name"] == "test-agent"
    assert frontmatter["description"] == "Test agent"
    assert set(frontmatter["tools"]) == {"read", "edit"}
    assert frontmatter["model"] == "claude-sonnet-4-5"
    assert frontmatter["target"] == "vscode"
    assert frontmatter["infer"] is True
    assert body == "Agent instructions here."


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
def test_convert_agent_with_handoffs(mock_dest_dir, tmp_path):
    """Test agent conversion with handoffs."""
    # Setup
    source_file = tmp_path / "cervella-frontend.md"
    source_content = """---
name: cervella-frontend
description: Frontend specialist
tools: Read, Edit
model: sonnet
---

Frontend instructions."""
    source_file.write_text(source_content)

    dest_file = MagicMock(spec=Path)
    mock_dest_dir.__truediv__.return_value = dest_file

    # Execute
    convert_agent(source_file)

    # Verify
    written_content = dest_file.write_text.call_args[0][0]
    frontmatter, _ = parse_frontmatter(written_content)

    assert "handoffs" in frontmatter
    assert len(frontmatter["handoffs"]) == 1
    assert frontmatter["handoffs"][0]["agent"] == "cervella-guardiana-qualita"


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
def test_convert_agent_no_handoffs_guardian(mock_dest_dir, tmp_path):
    """Test guardian agent has no handoffs."""
    # Setup
    source_file = tmp_path / "cervella-guardiana-qualita.md"
    source_content = """---
name: cervella-guardiana-qualita
description: Quality guardian
tools: Read, Edit
model: opus
---

Guardian instructions."""
    source_file.write_text(source_content)

    dest_file = MagicMock(spec=Path)
    mock_dest_dir.__truediv__.return_value = dest_file

    # Execute
    convert_agent(source_file)

    # Verify
    written_content = dest_file.write_text.call_args[0][0]
    frontmatter, _ = parse_frontmatter(written_content)

    assert "handoffs" not in frontmatter


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
def test_convert_agent_model_mapping(mock_dest_dir, tmp_path):
    """Test model mapping works correctly."""
    source_file = tmp_path / "test-agent.md"
    source_content = """---
name: test-agent
description: Test agent
tools: Read
model: opus
---

Body."""
    source_file.write_text(source_content)

    dest_file = MagicMock(spec=Path)
    mock_dest_dir.__truediv__.return_value = dest_file

    # Execute
    convert_agent(source_file)

    # Verify
    written_content = dest_file.write_text.call_args[0][0]
    frontmatter, _ = parse_frontmatter(written_content)

    assert frontmatter["model"] == "claude-opus-4-5"


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
def test_convert_agent_default_values(mock_dest_dir, tmp_path):
    """Test default values when frontmatter is missing."""
    source_file = tmp_path / "test-agent.md"
    source_content = "Just body content, no frontmatter."
    source_file.write_text(source_content)

    dest_file = MagicMock(spec=Path)
    mock_dest_dir.__truediv__.return_value = dest_file

    # Execute
    convert_agent(source_file)

    # Verify
    written_content = dest_file.write_text.call_args[0][0]
    frontmatter, body = parse_frontmatter(written_content)

    # Should use filename stem as name
    assert frontmatter["name"] == "test-agent"
    # Should use default description
    assert "CervellaSwarm" in frontmatter["description"]
    # Should use default tools (Read, Glob, Grep -> read, search)
    assert set(frontmatter["tools"]) == {"read", "search"}
    # Should use default model
    assert frontmatter["model"] == "claude-sonnet-4-5"


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
def test_convert_agent_destination_filename(mock_dest_dir, tmp_path):
    """Test destination filename format."""
    source_file = tmp_path / "my-agent.md"
    source_content = """---
name: my-agent
---

Body."""
    source_file.write_text(source_content)

    # Execute
    convert_agent(source_file)

    # Verify
    mock_dest_dir.__truediv__.assert_called_once_with("my-agent.agent.md")


# --- main tests ---


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
@patch("scripts.convert_agents_to_agent_hq.SOURCE_DIR")
@patch("scripts.convert_agents_to_agent_hq.convert_agent")
def test_main_empty_agent_list(mock_convert, mock_source_dir, mock_dest_dir, capsys):
    """Test main with no agent files found."""
    mock_source_dir.glob.return_value = []
    mock_dest_dir.mkdir = MagicMock()

    # Execute
    main()

    # Verify
    mock_dest_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_convert.assert_not_called()

    captured = capsys.readouterr()
    assert "No agent files found" in captured.out


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
@patch("scripts.convert_agents_to_agent_hq.SOURCE_DIR")
@patch("scripts.convert_agents_to_agent_hq.convert_agent")
def test_main_multiple_agents(mock_convert, mock_source_dir, mock_dest_dir, tmp_path):
    """Test main with multiple agents."""
    # Setup mock files
    agent1 = tmp_path / "agent1.md"
    agent2 = tmp_path / "agent2.md"
    agent3 = tmp_path / "agent3.md"

    mock_source_dir.glob.return_value = [agent1, agent2, agent3]
    mock_dest_dir.mkdir = MagicMock()

    # Execute
    main()

    # Verify
    assert mock_convert.call_count == 3
    mock_convert.assert_any_call(agent1)
    mock_convert.assert_any_call(agent2)
    mock_convert.assert_any_call(agent3)


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
@patch("scripts.convert_agents_to_agent_hq.SOURCE_DIR")
@patch("scripts.convert_agents_to_agent_hq.convert_agent")
def test_main_agent_exception(mock_convert, mock_source_dir, mock_dest_dir, tmp_path, capsys):
    """Test main handles agent conversion exceptions."""
    # Setup
    agent1 = tmp_path / "good-agent.md"
    agent2 = tmp_path / "bad-agent.md"
    agent3 = tmp_path / "another-good.md"

    mock_source_dir.glob.return_value = [agent1, agent2, agent3]
    mock_dest_dir.mkdir = MagicMock()

    # Make second conversion raise exception
    def convert_side_effect(agent_file):
        if agent_file == agent2:
            raise ValueError("Test error")

    mock_convert.side_effect = convert_side_effect

    # Execute
    main()

    # Verify all agents were attempted
    assert mock_convert.call_count == 3

    # Verify error was printed but execution continued
    captured = capsys.readouterr()
    assert "Error converting bad-agent.md" in captured.out
    assert "Test error" in captured.out


@patch("scripts.convert_agents_to_agent_hq.DEST_DIR")
@patch("scripts.convert_agents_to_agent_hq.SOURCE_DIR")
@patch("scripts.convert_agents_to_agent_hq.convert_agent")
def test_main_mkdir_called(mock_convert, mock_source_dir, mock_dest_dir, tmp_path):
    """Test main creates destination directory."""
    mock_source_dir.glob.return_value = [tmp_path / "agent.md"]
    mock_dest_dir.mkdir = MagicMock()

    # Execute
    main()

    # Verify
    mock_dest_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)


