# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.budget module and CLI main_budget."""

import json
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cervellaswarm_event_store.budget import (
    BudgetAlert,
    BudgetConfig,
    BudgetStatus,
    check_budget,
    load_config,
    save_config,
)
from cervellaswarm_event_store.cli import main_budget


# ====================================================================
# BudgetConfig dataclass
# ====================================================================


class TestBudgetConfig:
    def test_defaults_are_zero(self):
        cfg = BudgetConfig()
        assert cfg.daily == 0.0
        assert cfg.weekly == 0.0
        assert cfg.monthly == 0.0

    def test_custom_values(self):
        cfg = BudgetConfig(daily=10.0, weekly=50.0, monthly=200.0)
        assert cfg.daily == 10.0
        assert cfg.weekly == 50.0
        assert cfg.monthly == 200.0

    def test_frozen(self):
        cfg = BudgetConfig(daily=5.0)
        with pytest.raises(AttributeError):
            cfg.daily = 10.0


# ====================================================================
# BudgetAlert dataclass
# ====================================================================


class TestBudgetAlert:
    def test_fields(self):
        alert = BudgetAlert(
            period="daily", threshold=100.0, actual=80.0, over=False, percent=80.0
        )
        assert alert.period == "daily"
        assert alert.threshold == 100.0
        assert alert.actual == 80.0
        assert alert.over is False
        assert alert.percent == 80.0

    def test_over_flag(self):
        alert = BudgetAlert(
            period="weekly", threshold=50.0, actual=75.0, over=True, percent=150.0
        )
        assert alert.over is True


# ====================================================================
# BudgetStatus dataclass
# ====================================================================


class TestBudgetStatus:
    def test_defaults(self):
        status = BudgetStatus()
        assert status.alerts == []
        assert status.any_over is False

    def test_any_over_true(self):
        alerts = [
            BudgetAlert(period="daily", threshold=10, actual=15, over=True, percent=150),
        ]
        status = BudgetStatus(alerts=alerts, any_over=True)
        assert status.any_over is True

    def test_any_over_false_with_alerts(self):
        alerts = [
            BudgetAlert(period="daily", threshold=100, actual=50, over=False, percent=50),
        ]
        status = BudgetStatus(alerts=alerts, any_over=False)
        assert status.any_over is False


# ====================================================================
# load_config
# ====================================================================


class TestLoadConfig:
    def test_file_not_exists_returns_defaults(self, tmp_path):
        path = tmp_path / "nonexistent" / "budget.json"
        cfg = load_config(path)
        assert cfg == BudgetConfig()

    def test_valid_json(self, tmp_path):
        path = tmp_path / "budget.json"
        path.write_text(json.dumps({"daily": 25.0, "weekly": 100.0, "monthly": 500.0}))
        cfg = load_config(path)
        assert cfg.daily == 25.0
        assert cfg.weekly == 100.0
        assert cfg.monthly == 500.0

    def test_partial_json_fills_defaults(self, tmp_path):
        path = tmp_path / "budget.json"
        path.write_text(json.dumps({"daily": 10.0}))
        cfg = load_config(path)
        assert cfg.daily == 10.0
        assert cfg.weekly == 0.0
        assert cfg.monthly == 0.0

    def test_invalid_json_returns_defaults(self, tmp_path):
        path = tmp_path / "budget.json"
        path.write_text("not json at all {{{")
        cfg = load_config(path)
        assert cfg == BudgetConfig()

    def test_empty_file_returns_defaults(self, tmp_path):
        path = tmp_path / "budget.json"
        path.write_text("")
        cfg = load_config(path)
        assert cfg == BudgetConfig()

    def test_json_with_extra_keys_ignored(self, tmp_path):
        path = tmp_path / "budget.json"
        path.write_text(json.dumps({"daily": 5.0, "unknown_key": 999}))
        cfg = load_config(path)
        assert cfg.daily == 5.0

    def test_non_numeric_values_returns_defaults(self, tmp_path):
        path = tmp_path / "budget.json"
        path.write_text(json.dumps({"daily": "not-a-number"}))
        cfg = load_config(path)
        assert cfg == BudgetConfig()


# ====================================================================
# save_config
# ====================================================================


class TestSaveConfig:
    def test_creates_parent_dirs(self, tmp_path):
        path = tmp_path / "deep" / "nested" / "budget.json"
        cfg = BudgetConfig(daily=10.0)
        save_config(cfg, path)
        assert path.exists()

    def test_writes_valid_json(self, tmp_path):
        path = tmp_path / "budget.json"
        cfg = BudgetConfig(daily=10.0, weekly=50.0, monthly=200.0)
        save_config(cfg, path)
        data = json.loads(path.read_text())
        assert data["daily"] == 10.0
        assert data["weekly"] == 50.0
        assert data["monthly"] == 200.0

    def test_returns_path(self, tmp_path):
        path = tmp_path / "budget.json"
        result = save_config(BudgetConfig(), path)
        assert result == path

    def test_overwrites_existing(self, tmp_path):
        path = tmp_path / "budget.json"
        save_config(BudgetConfig(daily=5.0), path)
        save_config(BudgetConfig(daily=99.0), path)
        data = json.loads(path.read_text())
        assert data["daily"] == 99.0

    def test_roundtrip(self, tmp_path):
        path = tmp_path / "budget.json"
        original = BudgetConfig(daily=42.5, weekly=300.0, monthly=1200.0)
        save_config(original, path)
        loaded = load_config(path)
        assert loaded == original


# ====================================================================
# check_budget
# ====================================================================


class TestCheckBudget:
    def test_no_thresholds_returns_empty(self):
        """All thresholds at 0 = disabled, no alerts generated."""
        cfg = BudgetConfig()
        status = check_budget(10.0, 50.0, 200.0, cfg)
        assert status.alerts == []
        assert status.any_over is False

    def test_under_budget(self):
        cfg = BudgetConfig(daily=100.0, weekly=500.0, monthly=2000.0)
        status = check_budget(50.0, 200.0, 800.0, cfg)
        assert len(status.alerts) == 3
        assert status.any_over is False
        for alert in status.alerts:
            assert alert.over is False
            assert alert.percent < 100.0

    def test_over_budget_daily(self):
        cfg = BudgetConfig(daily=10.0)
        status = check_budget(15.0, 0.0, 0.0, cfg)
        assert len(status.alerts) == 1
        assert status.alerts[0].period == "daily"
        assert status.alerts[0].over is True
        assert status.alerts[0].percent == 150.0
        assert status.any_over is True

    def test_over_budget_multiple_periods(self):
        cfg = BudgetConfig(daily=10.0, weekly=50.0, monthly=200.0)
        status = check_budget(15.0, 60.0, 100.0, cfg)
        assert status.any_over is True
        daily_alert = [a for a in status.alerts if a.period == "daily"][0]
        weekly_alert = [a for a in status.alerts if a.period == "weekly"][0]
        monthly_alert = [a for a in status.alerts if a.period == "monthly"][0]
        assert daily_alert.over is True
        assert weekly_alert.over is True
        assert monthly_alert.over is False

    def test_exact_threshold_not_over(self):
        """Spend == threshold should NOT trigger over (strict >)."""
        cfg = BudgetConfig(daily=100.0)
        status = check_budget(100.0, 0.0, 0.0, cfg)
        assert status.alerts[0].over is False
        assert status.alerts[0].percent == 100.0

    def test_zero_threshold_disabled(self):
        """A threshold of 0 means disabled for that period."""
        cfg = BudgetConfig(daily=0.0, weekly=100.0, monthly=0.0)
        status = check_budget(999.0, 50.0, 999.0, cfg)
        assert len(status.alerts) == 1
        assert status.alerts[0].period == "weekly"

    def test_actual_rounded_to_cents(self):
        cfg = BudgetConfig(daily=100.0)
        status = check_budget(33.3333333, 0.0, 0.0, cfg)
        assert status.alerts[0].actual == 33.33

    def test_percent_rounded_to_one_decimal(self):
        cfg = BudgetConfig(daily=3.0)
        status = check_budget(1.0, 0.0, 0.0, cfg)
        assert status.alerts[0].percent == 33.3

    def test_zero_spend(self):
        cfg = BudgetConfig(daily=100.0)
        status = check_budget(0.0, 0.0, 0.0, cfg)
        assert status.alerts[0].actual == 0.0
        assert status.alerts[0].percent == 0.0
        assert status.alerts[0].over is False


# ====================================================================
# CLI: main_budget
# ====================================================================


@dataclass
class _FakeUsage:
    """Minimal mock for UsageSummary returned by query_usage."""

    total_cost_usd: float = 0.0


class TestMainBudgetSetThresholds:
    def test_set_daily(self, tmp_path, capsys):
        config_path = str(tmp_path / "budget.json")
        main_budget(["--set-daily", "50", "--config-path", config_path])
        out = capsys.readouterr().out
        assert "saved" in out.lower() or "50" in out
        data = json.loads(Path(config_path).read_text())
        assert data["daily"] == 50.0

    def test_set_weekly_json(self, tmp_path, capsys):
        config_path = str(tmp_path / "budget.json")
        main_budget(["--set-weekly", "300", "--config-path", config_path, "--json"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["status"] == "saved"
        assert data["config"]["weekly"] == 300.0

    def test_set_monthly(self, tmp_path, capsys):
        config_path = str(tmp_path / "budget.json")
        main_budget(["--set-monthly", "1000", "--config-path", config_path])
        data = json.loads(Path(config_path).read_text())
        assert data["monthly"] == 1000.0

    def test_set_multiple_at_once(self, tmp_path, capsys):
        config_path = str(tmp_path / "budget.json")
        main_budget([
            "--set-daily", "10",
            "--set-weekly", "60",
            "--set-monthly", "250",
            "--config-path", config_path,
        ])
        data = json.loads(Path(config_path).read_text())
        assert data["daily"] == 10.0
        assert data["weekly"] == 60.0
        assert data["monthly"] == 250.0

    def test_set_preserves_existing(self, tmp_path, capsys):
        config_path = tmp_path / "budget.json"
        config_path.write_text(json.dumps({"daily": 100.0, "weekly": 500.0, "monthly": 2000.0}))
        main_budget(["--set-daily", "200", "--config-path", str(config_path)])
        data = json.loads(config_path.read_text())
        assert data["daily"] == 200.0
        assert data["weekly"] == 500.0  # preserved
        assert data["monthly"] == 2000.0  # preserved

    def test_set_zero_disables(self, tmp_path, capsys):
        config_path = str(tmp_path / "budget.json")
        main_budget(["--set-daily", "0", "--config-path", config_path])
        data = json.loads(Path(config_path).read_text())
        assert data["daily"] == 0.0


class TestMainBudgetCheck:
    def _run_check(self, tmp_path, capsys, config, extra_args=None, cost=5.0):
        """Helper: write config, mock EventStore, run --check."""
        config_path = tmp_path / "budget.json"
        config_path.write_text(json.dumps(config))

        mock_store = MagicMock()
        mock_store.query_usage.return_value = _FakeUsage(total_cost_usd=cost)
        mock_store.__enter__ = MagicMock(return_value=mock_store)
        mock_store.__exit__ = MagicMock(return_value=False)

        args = ["--check", "--config-path", str(config_path)]
        if extra_args:
            args.extend(extra_args)

        with patch(
            "cervellaswarm_event_store.database.EventStore", return_value=mock_store
        ):
            main_budget(args)

        return capsys.readouterr().out

    def test_check_under_budget_text(self, tmp_path, capsys):
        out = self._run_check(
            tmp_path, capsys,
            config={"daily": 100.0, "weekly": 500.0, "monthly": 2000.0},
            cost=5.0,
        )
        assert "OK" in out
        assert "OVER" not in out

    def test_check_over_budget_text(self, tmp_path, capsys):
        out = self._run_check(
            tmp_path, capsys,
            config={"daily": 2.0, "weekly": 0.0, "monthly": 0.0},
            cost=5.0,
        )
        assert "OVER" in out
        assert "WARNING" in out

    def test_check_json_output(self, tmp_path, capsys):
        out = self._run_check(
            tmp_path, capsys,
            config={"daily": 100.0, "weekly": 0.0, "monthly": 0.0},
            extra_args=["--json"],
            cost=30.0,
        )
        data = json.loads(out)
        assert "any_over" in data
        assert isinstance(data["alerts"], list)
        assert data["alerts"][0]["period"] == "daily"

    def test_check_no_thresholds_text(self, tmp_path, capsys):
        out = self._run_check(
            tmp_path, capsys,
            config={"daily": 0.0, "weekly": 0.0, "monthly": 0.0},
            cost=5.0,
        )
        assert "no budget" in out.lower() or "not configured" in out.lower() or "set with" in out.lower()

    def test_check_no_config_file(self, tmp_path, capsys):
        """No config file at all -> defaults (all 0) -> no thresholds message."""
        config_path = tmp_path / "does_not_exist" / "budget.json"

        mock_store = MagicMock()
        mock_store.query_usage.return_value = _FakeUsage(total_cost_usd=5.0)
        mock_store.__enter__ = MagicMock(return_value=mock_store)
        mock_store.__exit__ = MagicMock(return_value=False)

        with patch(
            "cervellaswarm_event_store.database.EventStore", return_value=mock_store
        ):
            main_budget(["--check", "--config-path", str(config_path)])

        out = capsys.readouterr().out
        assert "no budget" in out.lower() or "set with" in out.lower()

    def test_check_json_over_budget(self, tmp_path, capsys):
        out = self._run_check(
            tmp_path, capsys,
            config={"daily": 1.0, "weekly": 0.0, "monthly": 0.0},
            extra_args=["--json"],
            cost=5.0,
        )
        data = json.loads(out)
        assert data["any_over"] is True
        assert data["alerts"][0]["over"] is True

    def test_check_calls_query_usage_three_times(self, tmp_path, capsys):
        """main_budget --check queries daily (1d), weekly (7d), monthly (30d)."""
        config_path = tmp_path / "budget.json"
        config_path.write_text(json.dumps({"daily": 100.0, "weekly": 0.0, "monthly": 0.0}))

        mock_store = MagicMock()
        mock_store.query_usage.return_value = _FakeUsage(total_cost_usd=1.0)
        mock_store.__enter__ = MagicMock(return_value=mock_store)
        mock_store.__exit__ = MagicMock(return_value=False)

        with patch(
            "cervellaswarm_event_store.database.EventStore", return_value=mock_store
        ):
            main_budget(["--check", "--config-path", str(config_path)])

        assert mock_store.query_usage.call_count == 3
        calls = [c.kwargs.get("days") for c in mock_store.query_usage.call_args_list]
        assert 1 in calls
        assert 7 in calls
        assert 30 in calls
