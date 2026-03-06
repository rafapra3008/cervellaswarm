# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _colors.py -- ANSI color state management."""

from __future__ import annotations

import os

from cervellaswarm_lingua_universale._colors import (
    _ColorState,
    colors,
    init_colors,
    reset_colors,
)


class TestColorState:
    """Tests for _ColorState dataclass."""

    def test_default_state_is_empty(self):
        state = _ColorState()
        assert state.RESET == ""
        assert state.BOLD == ""
        assert state.RED == ""
        assert state.GREEN == ""
        assert state.YELLOW == ""
        assert state.CYAN == ""

    def test_state_is_mutable(self):
        state = _ColorState()
        state.RED = "\033[31m"
        assert state.RED == "\033[31m"


class TestInitColors:
    """Tests for init_colors()."""

    def setup_method(self):
        reset_colors()
        # Clean env for each test
        for var in ("NO_COLOR", "FORCE_COLOR", "CLICOLOR_FORCE"):
            os.environ.pop(var, None)

    def teardown_method(self):
        reset_colors()
        for var in ("NO_COLOR", "FORCE_COLOR", "CLICOLOR_FORCE"):
            os.environ.pop(var, None)

    def test_no_color_disables_colors(self):
        os.environ["NO_COLOR"] = "1"
        os.environ["FORCE_COLOR"] = "1"  # Even with FORCE_COLOR
        init_colors()
        assert colors.RED == ""
        assert colors.GREEN == ""
        assert colors.RESET == ""

    def test_force_color_enables_colors(self):
        os.environ["FORCE_COLOR"] = "1"
        init_colors()
        assert colors.RED == "\033[31m"
        assert colors.GREEN == "\033[32m"
        assert colors.YELLOW == "\033[33m"
        assert colors.CYAN == "\033[36m"
        assert colors.BOLD == "\033[1m"
        assert colors.RESET == "\033[0m"

    def test_clicolor_force_enables_colors(self):
        os.environ["CLICOLOR_FORCE"] = "1"
        init_colors()
        assert colors.RED == "\033[31m"

    def test_no_tty_no_force_stays_empty(self):
        # Without FORCE_COLOR and without TTY, colors stay empty
        init_colors()
        # In test env, stdout is not a TTY
        assert colors.RED == ""


class TestResetColors:
    """Tests for reset_colors()."""

    def test_reset_clears_all(self):
        os.environ["FORCE_COLOR"] = "1"
        init_colors()
        assert colors.RED != ""

        reset_colors()
        assert colors.RESET == ""
        assert colors.BOLD == ""
        assert colors.RED == ""
        assert colors.GREEN == ""
        assert colors.YELLOW == ""
        assert colors.CYAN == ""
        os.environ.pop("FORCE_COLOR", None)


class TestModuleSingleton:
    """Tests for module-level colors singleton."""

    def test_colors_is_singleton(self):
        assert isinstance(colors, _ColorState)

    def test_init_modifies_singleton(self):
        reset_colors()
        os.environ["FORCE_COLOR"] = "1"
        init_colors()
        # The module-level `colors` should be modified
        assert colors.GREEN == "\033[32m"
        reset_colors()
        os.environ.pop("FORCE_COLOR", None)
