# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Shared fixtures for agent-templates test suite."""

import pytest


@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a temporary directory for file operations."""
    return tmp_path
