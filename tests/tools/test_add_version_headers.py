"""
Tests for scripts/tools/add_version_headers.py

Coverage: parse_frontmatter, build_frontmatter, update_agent_file, main.
"""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.tools.add_version_headers import (
    parse_frontmatter,
    build_frontmatter,
    update_agent_file,
    main,
    DEFAULT_VERSION,
    DEFAULT_COMPATIBLE,
)


class TestParseFrontmatter:
    """Test parse_frontmatter function."""

    def test_no_frontmatter(self):
        """Content without frontmatter."""
        content = "# Agent File\n\nThis is content."
        frontmatter, rest, original = parse_frontmatter(content)
        assert frontmatter == {}
        assert rest == content
        assert original == ""

    def test_valid_frontmatter(self):
        """Valid frontmatter with key-value pairs."""
        content = "---\nname: TestAgent\nversion: 1.0.0\n---\n# Agent Content"
        frontmatter, rest, original = parse_frontmatter(content)
        assert frontmatter == {"name": "TestAgent", "version": "1.0.0"}
        assert rest == "# Agent Content"
        assert original == "name: TestAgent\nversion: 1.0.0"

    def test_frontmatter_edge_cases(self):
        """Edge cases: spaces, empty values, colons in values."""
        # Spaces
        content = "---\nname:   TestAgent  \nversion:  1.0.0\n---\nContent"
        fm, _, _ = parse_frontmatter(content)
        assert fm == {"name": "TestAgent", "version": "1.0.0"}

        # Empty value
        content = "---\nname: TestAgent\ndescription:\n---\nContent"
        fm, _, _ = parse_frontmatter(content)
        assert fm["description"] == ""

        # Colon in value
        content = "---\nname: Test:Agent\n---\nContent"
        fm, _, _ = parse_frontmatter(content)
        assert fm["name"] == "Test:Agent"

        # No colon line (skipped)
        content = "---\nname: TestAgent\ninvalid line\nversion: 1.0.0\n---\nContent"
        fm, _, _ = parse_frontmatter(content)
        assert len(fm) == 2


class TestBuildFrontmatter:
    """Test build_frontmatter function."""

    def test_ordered_fields(self):
        """Fields follow preferred order."""
        data = {
            "model": "opus",
            "version": "1.0.0",
            "name": "TestAgent",
            "description": "Test",
            "updated": "2026-01-01",
            "compatible_with": "cervellaswarm >= 1.0.0",
            "tools": "read,write",
        }
        result = build_frontmatter(data)
        lines = result.split('\n')
        assert lines[0] == "name: TestAgent"
        assert lines[1] == "version: 1.0.0"
        assert lines[2] == "updated: 2026-01-01"
        assert lines[3] == "compatible_with: cervellaswarm >= 1.0.0"
        assert lines[4] == "description: Test"
        assert lines[5] == "tools: read,write"
        assert lines[6] == "model: opus"

    def test_partial_and_custom_fields(self):
        """Partial preferred fields + custom fields."""
        data = {"name": "TestAgent", "version": "1.0.0", "custom_field": "custom"}
        result = build_frontmatter(data)
        lines = result.split('\n')
        assert lines[0] == "name: TestAgent"
        assert lines[1] == "version: 1.0.0"
        assert lines[2] == "custom_field: custom"

    def test_empty_and_single_field(self):
        """Empty dict and single field."""
        assert build_frontmatter({}) == ""
        assert build_frontmatter({"name": "Agent"}) == "name: Agent"


class TestUpdateAgentFile:
    """Test update_agent_file function."""

    def test_no_frontmatter_error(self, tmp_path):
        """File without frontmatter returns error."""
        file = tmp_path / "agent.md"
        file.write_text("# Agent\n\nNo frontmatter here.")
        result = update_agent_file(file, "1.0.0", dry_run=True)
        assert result["had_frontmatter"] is False
        assert "error" in result

    def test_add_new_fields_dry_run(self, tmp_path):
        """Add version/updated/compatible_with (dry-run)."""
        file = tmp_path / "agent.md"
        content = "---\nname: TestAgent\ndescription: Test\n---\n# Content"
        file.write_text(content)
        result = update_agent_file(file, "2.0.0", dry_run=True)
        assert result["had_frontmatter"] is True
        assert len(result["changes"]) == 3
        assert file.read_text() == content  # No modification

    def test_add_new_fields_apply(self, tmp_path):
        """Add fields and apply changes."""
        file = tmp_path / "agent.md"
        file.write_text("---\nname: TestAgent\n---\n# Content")
        result = update_agent_file(file, "3.0.0", dry_run=False)
        assert len(result["changes"]) == 3
        new_content = file.read_text()
        assert "version: 3.0.0" in new_content
        assert "compatible_with: cervellaswarm >= 1.0.0" in new_content
        assert "# Content" in new_content

    def test_update_existing_version(self, tmp_path):
        """Update existing version."""
        file = tmp_path / "agent.md"
        file.write_text(
            "---\nname: TestAgent\nversion: 1.0.0\n"
            "updated: 2025-01-01\ncompatible_with: cervellaswarm >= 1.0.0\n---\n# Content"
        )
        result = update_agent_file(file, "2.0.0", dry_run=True)
        assert any("Updated version: 1.0.0 -> 2.0.0" in c for c in result["changes"])

    def test_no_changes_needed(self, tmp_path):
        """File already correct."""
        file = tmp_path / "agent.md"
        today = datetime.now().strftime("%Y-%m-%d")
        file.write_text(
            f"---\nname: TestAgent\nversion: 1.0.0\nupdated: {today}\n"
            f"compatible_with: cervellaswarm >= 1.0.0\n---\n# Content"
        )
        result = update_agent_file(file, "1.0.0", dry_run=True)
        assert result["changes"] == []

    def test_preserves_content_and_custom_version(self, tmp_path):
        """Rest content preserved, custom version works."""
        file = tmp_path / "agent.md"
        rest_content = "# Agent\n\n## Section\n\nContent here."
        file.write_text(f"---\nname: TestAgent\n---\n{rest_content}")
        result = update_agent_file(file, "10.5.3-beta", dry_run=False)
        new_content = file.read_text()
        assert rest_content in new_content
        assert "version: 10.5.3-beta" in new_content


class TestMain:
    """Test main CLI function."""

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_no_agents_path(self, mock_path, capsys):
        """Agents path does not exist."""
        mock_path.return_value = Path("/nonexistent/path")
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["add_version_headers.py"]):
                main()
        assert exc.value.code == 1
        assert "ERROR: Agents path not found" in capsys.readouterr().out

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_no_agent_files(self, mock_path, tmp_path, capsys):
        """Agents path exists but no cervella-*.md files."""
        mock_path.return_value = tmp_path
        with pytest.raises(SystemExit) as exc:
            with patch("sys.argv", ["add_version_headers.py"]):
                main()
        assert exc.value.code == 1
        assert "ERROR: No agent files found" in capsys.readouterr().out

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_dry_run_mode(self, mock_path, tmp_path, capsys):
        """Dry-run mode (default)."""
        mock_path.return_value = tmp_path
        (tmp_path / "cervella-test1.md").write_text("---\nname: Test1\n---\nContent")
        (tmp_path / "cervella-test2.md").write_text("---\nname: Test2\nversion: 1.0.0\n---\nContent")
        with patch("sys.argv", ["add_version_headers.py"]):
            main()
        out = capsys.readouterr().out
        assert "DRY-RUN (preview)" in out
        assert "cervella-test1.md" in out
        assert "Run with --apply to save changes" in out

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_apply_mode(self, mock_path, tmp_path, capsys):
        """Apply mode modifies files."""
        mock_path.return_value = tmp_path
        agent_file = tmp_path / "cervella-test.md"
        agent_file.write_text("---\nname: Test\n---\nContent")
        with patch("sys.argv", ["add_version_headers.py", "--apply"]):
            main()
        assert "APPLY" in capsys.readouterr().out
        assert "version: 1.0.0" in agent_file.read_text()

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_custom_version_flag(self, mock_path, tmp_path, capsys):
        """Custom version flag."""
        mock_path.return_value = tmp_path
        (tmp_path / "cervella-test.md").write_text("---\nname: Test\n---\nContent")
        with patch("sys.argv", ["add_version_headers.py", "--version", "2.5.0"]):
            main()
        assert "Version:     2.5.0" in capsys.readouterr().out

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_custom_agents_path_flag(self, mock_path, tmp_path, capsys):
        """Custom agents path flag."""
        custom_path = tmp_path / "custom"
        custom_path.mkdir()
        (custom_path / "cervella-test.md").write_text("---\nname: Test\n---\nContent")
        with patch("sys.argv", ["add_version_headers.py", "--agents-path", str(custom_path)]):
            main()
        assert str(custom_path) in capsys.readouterr().out

    @patch("scripts.tools.add_version_headers.get_agents_path")
    def test_error_handling_and_summary(self, mock_path, tmp_path, capsys):
        """Error handling and summary output."""
        mock_path.return_value = tmp_path
        # File without frontmatter (error)
        (tmp_path / "cervella-broken.md").write_text("# No frontmatter\n\nContent")
        # File with no changes needed
        today = datetime.now().strftime("%Y-%m-%d")
        (tmp_path / "cervella-ok.md").write_text(
            f"---\nname: OK\nversion: 1.0.0\nupdated: {today}\n"
            f"compatible_with: cervellaswarm >= 1.0.0\n---\nContent"
        )
        # File needing changes
        (tmp_path / "cervella-update.md").write_text("---\nname: Update\n---\nContent")
        with patch("sys.argv", ["add_version_headers.py"]):
            main()
        out = capsys.readouterr().out
        assert "cervella-broken.md" in out
        assert "ERROR" in out
        assert "cervella-ok.md: (no changes needed)" in out
        assert "Files processed: 3" in out
        assert "Errors:          1" in out
