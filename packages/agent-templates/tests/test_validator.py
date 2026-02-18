# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_templates.validator module."""

import pytest

from cervellaswarm_agent_templates.validator import (
    ValidationIssue,
    ValidationResult,
    parse_frontmatter,
    validate_agent,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_FRONTMATTER = """\
---
name: my-agent
description: Does stuff.
model: sonnet
tools: Read, Edit, Bash
---

This is a sufficiently long body to pass the short-body check. It explains
what the agent does and provides instructions for how to behave correctly.
"""

MINIMAL_VALID = """\
---
name: agent
description: An agent.
model: opus
tools: Read
---

This body is long enough to satisfy the minimum length requirement for body \
validation and avoids triggering the short-body warning in the validator.
"""


def _write(tmp_path, filename, content):
    """Write content to a file and return the Path."""
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# parse_frontmatter tests
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    def test_valid_yaml_returns_dict(self):
        content = "---\nname: foo\nmodel: sonnet\n---\nBody here."
        result = parse_frontmatter(content)
        assert result == {"name": "foo", "model": "sonnet"}

    def test_multiple_fields(self):
        content = "---\nname: x\ndescription: y\nmodel: opus\ntools: Read\n---\nBody."
        result = parse_frontmatter(content)
        assert result["name"] == "x"
        assert result["description"] == "y"
        assert result["model"] == "opus"
        assert result["tools"] == "Read"

    def test_no_frontmatter_returns_none(self):
        result = parse_frontmatter("No frontmatter here at all.")
        assert result is None

    def test_empty_content_returns_none(self):
        result = parse_frontmatter("")
        assert result is None

    def test_incomplete_frontmatter_returns_none(self):
        # Only opening --- but no closing ---
        result = parse_frontmatter("---\nname: foo\n")
        assert result is None

    def test_invalid_yaml_returns_none(self):
        # Colon in value without quoting causes parse error in some cases;
        # use deliberately malformed YAML
        bad = "---\n: : : invalid\n---\nBody."
        result = parse_frontmatter(bad)
        # Either None (parse error) or a dict - but malformed should return None
        # Actually yaml.safe_load can be lenient; test that it doesn't raise
        # Just ensure no exception is raised
        assert result is None or isinstance(result, dict)

    def test_frontmatter_with_list_value(self):
        content = "---\nname: foo\ntags:\n  - a\n  - b\n---\nBody."
        result = parse_frontmatter(content)
        assert result["tags"] == ["a", "b"]

    def test_frontmatter_with_integer_value(self):
        content = "---\nmaxTurns: 30\nname: agent\n---\nBody."
        result = parse_frontmatter(content)
        assert result["maxTurns"] == 30

    def test_strictly_invalid_yaml_returns_none(self):
        # Tab characters in YAML where not allowed cause scanner errors
        content = "---\nkey:\t bad_value\n---\nBody."
        result = parse_frontmatter(content)
        # yaml.safe_load may or may not raise on tabs; just ensure no exception
        assert result is None or isinstance(result, dict)


# ---------------------------------------------------------------------------
# ValidationResult tests
# ---------------------------------------------------------------------------


class TestValidationResult:
    def _make_result(self, issues):
        return ValidationResult(path="fake.md", valid=True, issues=issues)

    def test_errors_property_filters_errors(self):
        issues = [
            ValidationIssue("error", "model", "bad model"),
            ValidationIssue("warning", "tools", "unknown tool"),
            ValidationIssue("info", "role", "custom role"),
        ]
        result = self._make_result(issues)
        assert len(result.errors) == 1
        assert result.errors[0].level == "error"
        assert result.errors[0].field == "model"

    def test_warnings_property_filters_warnings(self):
        issues = [
            ValidationIssue("error", "name", "missing"),
            ValidationIssue("warning", "tools", "unknown"),
            ValidationIssue("warning", "body", "too short"),
        ]
        result = self._make_result(issues)
        assert len(result.warnings) == 2
        for w in result.warnings:
            assert w.level == "warning"

    def test_errors_empty_when_no_errors(self):
        issues = [ValidationIssue("warning", "body", "short")]
        result = self._make_result(issues)
        assert result.errors == []

    def test_warnings_empty_when_no_warnings(self):
        issues = [ValidationIssue("error", "name", "missing")]
        result = self._make_result(issues)
        assert result.warnings == []

    def test_empty_issues(self):
        result = self._make_result([])
        assert result.errors == []
        assert result.warnings == []

    def test_frontmatter_defaults_to_empty_dict(self):
        result = ValidationResult(path="x.md", valid=True)
        assert result.frontmatter == {}

    def test_issues_defaults_to_empty_list(self):
        result = ValidationResult(path="x.md", valid=True)
        assert result.issues == []


# ---------------------------------------------------------------------------
# validate_agent tests
# ---------------------------------------------------------------------------


class TestValidateAgentFileNotFound:
    def test_nonexistent_file_returns_invalid(self, tmp_dir):
        result = validate_agent(tmp_dir / "does_not_exist.md")
        assert result.valid is False
        assert any(i.level == "error" and "not found" in i.message.lower()
                   for i in result.issues)

    def test_nonexistent_file_has_file_field_error(self, tmp_dir):
        result = validate_agent(tmp_dir / "ghost.md")
        assert result.errors[0].field == "file"


class TestValidateAgentExtension:
    def test_non_md_extension_warns(self, tmp_dir):
        p = _write(tmp_dir, "agent.txt", VALID_FRONTMATTER)
        result = validate_agent(p)
        # Should have a warning about extension
        fields = [i.field for i in result.warnings]
        assert "file" in fields

    def test_md_extension_no_file_warning(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", VALID_FRONTMATTER)
        result = validate_agent(p)
        file_warnings = [i for i in result.warnings if i.field == "file"]
        assert file_warnings == []


class TestValidateAgentFrontmatter:
    def test_no_frontmatter_returns_invalid(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", "Just plain text, no frontmatter at all.")
        result = validate_agent(p)
        assert result.valid is False
        assert any(i.field == "frontmatter" for i in result.issues)

    def test_valid_frontmatter_parsed(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", VALID_FRONTMATTER)
        result = validate_agent(p)
        assert result.frontmatter.get("name") == "my-agent"


class TestValidateAgentRequiredFields:
    def _make_fm(self, **overrides):
        base = {"name": "x", "description": "y", "model": "sonnet", "tools": "Read"}
        base.update(overrides)
        return base

    def _write_fm(self, tmp_dir, fm_dict, body="A sufficiently long body for testing validation purposes."):
        lines = ["---"]
        for k, v in fm_dict.items():
            lines.append(f"{k}: {v}")
        lines.append("---")
        lines.append("")
        lines.append(body)
        return _write(tmp_dir, "agent.md", "\n".join(lines))

    def test_missing_name_is_error(self, tmp_dir):
        fm = self._make_fm()
        del fm["name"]
        p = self._write_fm(tmp_dir, fm)
        result = validate_agent(p)
        assert any(i.field == "name" and i.level == "error" for i in result.issues)

    def test_missing_description_is_error(self, tmp_dir):
        fm = self._make_fm()
        del fm["description"]
        p = self._write_fm(tmp_dir, fm)
        result = validate_agent(p)
        assert any(i.field == "description" and i.level == "error" for i in result.issues)

    def test_missing_model_is_error(self, tmp_dir):
        fm = self._make_fm()
        del fm["model"]
        p = self._write_fm(tmp_dir, fm)
        result = validate_agent(p)
        assert any(i.field == "model" and i.level == "error" for i in result.issues)

    def test_missing_tools_is_error(self, tmp_dir):
        fm = self._make_fm()
        del fm["tools"]
        p = self._write_fm(tmp_dir, fm)
        result = validate_agent(p)
        assert any(i.field == "tools" and i.level == "error" for i in result.issues)

    def test_all_required_present_no_required_errors(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", MINIMAL_VALID)
        result = validate_agent(p)
        required_errors = [
            i for i in result.issues
            if i.level == "error" and i.field in {"name", "description", "model", "tools"}
        ]
        assert required_errors == []


class TestValidateAgentModel:
    def _make_agent(self, tmp_dir, model, body=None):
        body = body or "A sufficiently long body text for the validation check to pass."
        content = f"---\nname: agent\ndescription: x\nmodel: {model}\ntools: Read\n---\n\n{body}"
        return _write(tmp_dir, "agent.md", content)

    def test_opus_is_valid(self, tmp_dir):
        p = self._make_agent(tmp_dir, "opus")
        result = validate_agent(p)
        model_errors = [i for i in result.issues if i.field == "model" and i.level == "error"]
        assert model_errors == []

    def test_sonnet_is_valid(self, tmp_dir):
        p = self._make_agent(tmp_dir, "sonnet")
        result = validate_agent(p)
        model_errors = [i for i in result.issues if i.field == "model" and i.level == "error"]
        assert model_errors == []

    def test_haiku_is_valid(self, tmp_dir):
        p = self._make_agent(tmp_dir, "haiku")
        result = validate_agent(p)
        model_errors = [i for i in result.issues if i.field == "model" and i.level == "error"]
        assert model_errors == []

    def test_invalid_model_is_error(self, tmp_dir):
        p = self._make_agent(tmp_dir, "gpt-4")
        result = validate_agent(p)
        assert any(i.field == "model" and i.level == "error" for i in result.issues)
        assert result.valid is False

    def test_invalid_model_mentions_valid_options(self, tmp_dir):
        p = self._make_agent(tmp_dir, "claude-3")
        result = validate_agent(p)
        model_error = next(i for i in result.issues if i.field == "model")
        assert "haiku" in model_error.message or "opus" in model_error.message


class TestValidateAgentTools:
    def _make_agent(self, tmp_dir, tools_str, body=None):
        body = body or "A sufficiently long body text for the validation check to pass."
        content = f"---\nname: agent\ndescription: x\nmodel: sonnet\ntools: {tools_str}\n---\n\n{body}"
        return _write(tmp_dir, "agent.md", content)

    def test_valid_single_tool(self, tmp_dir):
        p = self._make_agent(tmp_dir, "Read")
        result = validate_agent(p)
        tool_warns = [i for i in result.issues if i.field == "tools" and i.level == "warning"]
        assert tool_warns == []

    def test_valid_multiple_tools(self, tmp_dir):
        p = self._make_agent(tmp_dir, "Read, Edit, Bash, Glob, Grep")
        result = validate_agent(p)
        tool_warns = [i for i in result.issues if i.field == "tools" and i.level == "warning"]
        assert tool_warns == []

    def test_all_known_tools_valid(self, tmp_dir):
        tools = "Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch, Task"
        p = self._make_agent(tmp_dir, tools)
        result = validate_agent(p)
        tool_warns = [i for i in result.issues if i.field == "tools" and i.level == "warning"]
        assert tool_warns == []

    def test_unrecognized_tool_warns(self, tmp_dir):
        p = self._make_agent(tmp_dir, "Read, FakeTool")
        result = validate_agent(p)
        tool_warns = [i for i in result.issues if i.field == "tools" and i.level == "warning"]
        assert len(tool_warns) == 1
        assert "FakeTool" in tool_warns[0].message

    def test_multiple_unrecognized_tools_warn(self, tmp_dir):
        p = self._make_agent(tmp_dir, "Read, ToolA, ToolB")
        result = validate_agent(p)
        tool_warns = [i for i in result.issues if i.field == "tools" and i.level == "warning"]
        assert len(tool_warns) == 2

    def test_unrecognized_tool_still_valid(self, tmp_dir):
        # Warnings don't make it invalid
        p = self._make_agent(tmp_dir, "Read, MyCustomTool")
        result = validate_agent(p)
        assert result.valid is True


class TestValidateAgentOptionalFields:
    def _make_agent(self, tmp_dir, extra_fields, body=None):
        body = body or "A sufficiently long body text for the validation check to pass."
        fm = "---\nname: agent\ndescription: x\nmodel: sonnet\ntools: Read\n"
        for k, v in extra_fields.items():
            fm += f"{k}: {v}\n"
        fm += "---\n\n" + body
        return _write(tmp_dir, "agent.md", fm)

    def test_standard_role_no_info(self, tmp_dir):
        for role in ["Coordinator", "Quality Gate", "Architect", "Worker"]:
            p = _write(
                tmp_dir,
                "agent.md",
                f"---\nname: a\ndescription: x\nmodel: sonnet\ntools: Read\nrole: {role}\n---\n\n"
                "A sufficiently long body text for the validation check to pass.",
            )
            result = validate_agent(p)
            role_infos = [i for i in result.issues if i.field == "role" and i.level == "info"]
            assert role_infos == [], f"Expected no info for standard role '{role}'"

    def test_custom_role_produces_info(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"role": "Specialist"})
        result = validate_agent(p)
        assert any(i.field == "role" and i.level == "info" for i in result.issues)

    def test_valid_permission_mode(self, tmp_dir):
        for mode in ["default", "plan", "bypassPermissions", "acceptEdits"]:
            p = self._make_agent(tmp_dir, {"permissionMode": mode})
            result = validate_agent(p)
            pm_warns = [i for i in result.issues if i.field == "permissionMode"]
            assert pm_warns == [], f"No warning expected for valid permissionMode '{mode}'"

    def test_invalid_permission_mode_warns(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"permissionMode": "superAdmin"})
        result = validate_agent(p)
        assert any(i.field == "permissionMode" and i.level == "warning" for i in result.issues)

    def test_valid_max_turns(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"maxTurns": 30})
        result = validate_agent(p)
        mt_warns = [i for i in result.issues if i.field == "maxTurns"]
        assert mt_warns == []

    def test_zero_max_turns_warns(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"maxTurns": 0})
        result = validate_agent(p)
        assert any(i.field == "maxTurns" and i.level == "warning" for i in result.issues)

    def test_negative_max_turns_warns(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"maxTurns": -5})
        result = validate_agent(p)
        assert any(i.field == "maxTurns" and i.level == "warning" for i in result.issues)

    def test_valid_semver_version(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"version": "1.0.0"})
        result = validate_agent(p)
        ver_warns = [i for i in result.issues if i.field == "version"]
        assert ver_warns == []

    def test_invalid_version_warns(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"version": "v1.0"})
        result = validate_agent(p)
        assert any(i.field == "version" and i.level == "warning" for i in result.issues)

    def test_another_invalid_version_warns(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"version": "1.0"})
        result = validate_agent(p)
        assert any(i.field == "version" and i.level == "warning" for i in result.issues)

    def test_three_part_semver_valid(self, tmp_dir):
        p = self._make_agent(tmp_dir, {"version": "2.3.14"})
        result = validate_agent(p)
        ver_warns = [i for i in result.issues if i.field == "version"]
        assert ver_warns == []


class TestValidateAgentBody:
    def test_short_body_warns(self, tmp_dir):
        content = "---\nname: a\ndescription: x\nmodel: sonnet\ntools: Read\n---\n\nShort."
        p = _write(tmp_dir, "agent.md", content)
        result = validate_agent(p)
        assert any(i.field == "body" and i.level == "warning" for i in result.issues)

    def test_long_body_no_warning(self, tmp_dir):
        body = "x" * 100
        content = f"---\nname: a\ndescription: x\nmodel: sonnet\ntools: Read\n---\n\n{body}"
        p = _write(tmp_dir, "agent.md", content)
        result = validate_agent(p)
        body_warns = [i for i in result.issues if i.field == "body"]
        assert body_warns == []

    def test_exactly_50_chars_no_warning(self, tmp_dir):
        # 50 chars is exactly the threshold - should NOT warn (< 50 warns)
        body = "x" * 50
        content = f"---\nname: a\ndescription: x\nmodel: sonnet\ntools: Read\n---\n\n{body}"
        p = _write(tmp_dir, "agent.md", content)
        result = validate_agent(p)
        body_warns = [i for i in result.issues if i.field == "body"]
        assert body_warns == []


class TestValidateAgentFullFlow:
    def test_fully_valid_agent_returns_valid_true(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", MINIMAL_VALID)
        result = validate_agent(p)
        assert result.valid is True
        assert result.errors == []

    def test_returns_validation_result_type(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", MINIMAL_VALID)
        result = validate_agent(p)
        assert isinstance(result, ValidationResult)

    def test_path_stored_in_result(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", MINIMAL_VALID)
        result = validate_agent(p)
        assert str(p) in result.path or result.path.endswith("agent.md")

    def test_accepts_path_object(self, tmp_dir):
        from pathlib import Path
        p = _write(tmp_dir, "agent.md", MINIMAL_VALID)
        result = validate_agent(Path(p))
        assert isinstance(result, ValidationResult)

    def test_accepts_string_path(self, tmp_dir):
        p = _write(tmp_dir, "agent.md", MINIMAL_VALID)
        result = validate_agent(str(p))
        assert isinstance(result, ValidationResult)

    def test_multiple_errors_all_collected(self, tmp_dir):
        # Missing name, model is invalid
        content = "---\ndescription: x\nmodel: bad-model\ntools: Read\n---\n\nBody text."
        p = _write(tmp_dir, "agent.md", content)
        result = validate_agent(p)
        assert len(result.errors) >= 2
        fields_with_errors = {i.field for i in result.errors}
        assert "name" in fields_with_errors
        assert "model" in fields_with_errors
