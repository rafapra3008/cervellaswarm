# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Regression tests for S377 bug fixes in cervellaswarm_agent_templates."""

import os
import sys
from unittest.mock import patch

import pytest

from cervellaswarm_agent_templates.validator import ValidationResult, validate_agent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
# Fix 1: validator.py:132 - path.read_text() wrapped in try/except
# (OSError, UnicodeDecodeError)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(sys.platform == "win32", reason="No chmod on Windows")
def test_validate_agent_permission_error_returns_result(tmp_path):
    """OSError on read returns ValidationResult(valid=False), not an exception."""
    p = _write(tmp_path, "agent.md", MINIMAL_VALID)
    os.chmod(p, 0o000)
    try:
        result = validate_agent(p)
    finally:
        os.chmod(p, 0o644)

    assert isinstance(result, ValidationResult)
    assert result.valid is False
    assert len(result.errors) == 1
    assert "Cannot read file" in result.errors[0].message
    assert result.errors[0].field == "file"
    assert result.errors[0].level == "error"


def test_validate_agent_binary_content_returns_result(tmp_path):
    """UnicodeDecodeError on read returns ValidationResult(valid=False)."""
    p = tmp_path / "agent.md"
    p.write_bytes(b"\xff\xfe invalid utf-8 \x80\x81")

    result = validate_agent(p)

    assert isinstance(result, ValidationResult)
    assert result.valid is False
    assert len(result.errors) == 1
    assert "Cannot read file" in result.errors[0].message
    assert result.errors[0].field == "file"
    assert result.errors[0].level == "error"


def test_validate_agent_valid_file_still_works(tmp_path):
    """Valid agent file with frontmatter succeeds after fix (regression guard)."""
    p = _write(tmp_path, "agent.md", MINIMAL_VALID)

    result = validate_agent(p)

    assert isinstance(result, ValidationResult)
    assert result.valid is True
    assert result.errors == []
    assert result.frontmatter.get("name") == "agent"
    assert result.frontmatter.get("model") == "opus"


def test_validate_agent_other_exceptions_propagate(tmp_path):
    """RuntimeError from read_text is not caught by the OSError/UnicodeDecodeError handler."""
    p = _write(tmp_path, "agent.md", MINIMAL_VALID)

    with patch.object(p.__class__, "read_text", side_effect=RuntimeError("unexpected")):
        with pytest.raises(RuntimeError, match="unexpected"):
            validate_agent(p)
