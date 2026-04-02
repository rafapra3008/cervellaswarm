# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Budget alert module for cervellaswarm-event-store.

Configurable cost thresholds (daily, weekly, monthly) stored as JSON.
Checks current spend against thresholds and returns alert status.

Usage:
    from cervellaswarm_event_store.budget import load_config, check_budget

Config file: ~/.config/cervellaswarm/budget.json
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "cervellaswarm" / "budget.json"

# Default thresholds (USD). 0 = disabled.
_DEFAULTS = {
    "daily": 0.0,
    "weekly": 0.0,
    "monthly": 0.0,
}


@dataclass(frozen=True)
class BudgetConfig:
    """Budget threshold configuration.

    Attributes:
        daily: Max daily spend in USD. 0 = no limit.
        weekly: Max weekly spend in USD. 0 = no limit.
        monthly: Max monthly spend in USD. 0 = no limit.
    """

    daily: float = 0.0
    weekly: float = 0.0
    monthly: float = 0.0


@dataclass(frozen=True)
class BudgetAlert:
    """Result of a budget check.

    Attributes:
        period: 'daily', 'weekly', or 'monthly'.
        threshold: Configured threshold in USD.
        actual: Actual spend in USD.
        over: True if actual > threshold.
        percent: Percentage of threshold used (0-100+).
    """

    period: str
    threshold: float
    actual: float
    over: bool
    percent: float


@dataclass(frozen=True)
class BudgetStatus:
    """Overall budget status.

    Attributes:
        alerts: List of BudgetAlert for each configured period.
        any_over: True if any threshold is exceeded.
    """

    alerts: "list[BudgetAlert]" = field(default_factory=list)
    any_over: bool = False


def load_config(path: Optional[Path] = None) -> BudgetConfig:
    """Load budget config from JSON file.

    Creates default config if file doesn't exist.

    Args:
        path: Override config file path.

    Returns:
        BudgetConfig with thresholds.
    """
    path = path or DEFAULT_CONFIG_PATH
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return BudgetConfig(
                daily=float(data.get("daily", 0)),
                weekly=float(data.get("weekly", 0)),
                monthly=float(data.get("monthly", 0)),
            )
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    return BudgetConfig()


def save_config(config: BudgetConfig, path: Optional[Path] = None) -> Path:
    """Save budget config to JSON file.

    Args:
        config: BudgetConfig to save.
        path: Override config file path.

    Returns:
        Path to saved config file.
    """
    path = path or DEFAULT_CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "daily": config.daily,
        "weekly": config.weekly,
        "monthly": config.monthly,
    }
    path.write_text(json.dumps(data, indent=2) + "\n")
    return path


def check_budget(
    daily_cost: float,
    weekly_cost: float,
    monthly_cost: float,
    config: BudgetConfig,
) -> BudgetStatus:
    """Check current spend against budget thresholds.

    Args:
        daily_cost: Today's spend in USD.
        weekly_cost: This week's spend in USD.
        monthly_cost: This month's spend in USD.
        config: Budget thresholds.

    Returns:
        BudgetStatus with alerts for each configured period.
    """
    alerts = []
    periods = [
        ("daily", config.daily, daily_cost),
        ("weekly", config.weekly, weekly_cost),
        ("monthly", config.monthly, monthly_cost),
    ]

    for period, threshold, actual in periods:
        if threshold <= 0:
            continue
        percent = (actual / threshold * 100) if threshold > 0 else 0
        alerts.append(BudgetAlert(
            period=period,
            threshold=threshold,
            actual=round(actual, 2),
            over=actual > threshold,
            percent=round(percent, 1),
        ))

    return BudgetStatus(
        alerts=alerts,
        any_over=any(a.over for a in alerts),
    )
