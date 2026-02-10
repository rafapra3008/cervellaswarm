"""
Test per scripts.memory.retro.output.

Coverage focus: Rendering multi-formato (rich/plain/markdown).
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from io import StringIO

from scripts.memory.retro.output import (
    OutputMode,
    print_section_header,
    print_table,
    print_panel,
    print_metrics_table,
    print_patterns_section,
    print_lessons_section,
    print_agents_section,
    print_recommendations_section,
    print_suggestions_section,
    print_next_steps_section,
    print_empty_message,
    print_header
)


# === TEST OUTPUT.PY ===

def test_output_mode_enum_values():
    """OutputMode enum ha i valori corretti."""
    assert OutputMode.RICH == "rich"
    assert OutputMode.PLAIN == "plain"
    assert OutputMode.MARKDOWN == "markdown"


def test_print_section_header_markdown_returns_string():
    """print_section_header in MARKDOWN mode ritorna stringa formattata."""
    result = print_section_header("Test Section", OutputMode.MARKDOWN)

    assert result == "## Test Section\n\n"


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_section_header_plain_prints_to_stdout(capsys):
    """print_section_header in PLAIN mode (HAS_RICH=False) stampa su stdout."""
    result = print_section_header("Test Section", OutputMode.PLAIN)

    assert result is None
    captured = capsys.readouterr()
    assert "Test Section" in captured.out
    assert "---" in captured.out


def test_print_table_markdown_generates_table():
    """print_table in MARKDOWN mode genera tabella markdown."""
    data = [
        {"name": "Alice", "age": 30, "city": "Rome"},
        {"name": "Bob", "age": 25, "city": "Milan"},
    ]
    columns = [
        ("Name", "name", "left", "cyan", 15),
        ("Age", "age", "right", "white", 8),
        ("City", "city", "left", "white", 15),
    ]

    result = print_table(data, columns, "Test Table", OutputMode.MARKDOWN)

    assert "| Name | Age | City |" in result
    assert "|---|---|---|" in result
    assert "| Alice | 30 | Rome |" in result
    assert "| Bob | 25 | Milan |" in result


def test_print_table_empty_data_returns_none():
    """print_table con data vuota ritorna None."""
    columns = [("Name", "name", "left", "cyan", 15)]

    result = print_table([], columns, "Empty Table", OutputMode.MARKDOWN)

    assert result is None


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_table_plain_mode(capsys):
    """print_table in PLAIN mode stampa tabella su stdout."""
    data = [{"name": "Alice", "score": 100}]
    columns = [
        ("Name", "name", "left", "cyan", 15),
        ("Score", "score", "right", "white", 10),
    ]

    result = print_table(data, columns, "Test Table", OutputMode.PLAIN)

    assert result is None
    captured = capsys.readouterr()
    assert "Test Table" in captured.out
    assert "Name" in captured.out
    assert "Score" in captured.out
    assert "Alice" in captured.out
    assert "100" in captured.out


def test_print_panel_markdown_generates_bold_title():
    """print_panel in MARKDOWN mode genera titolo bold."""
    result = print_panel("Test content here", "Panel Title", "white", OutputMode.MARKDOWN)

    assert result == "**Panel Title:**\n\nTest content here\n\n"


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_panel_plain_mode(capsys):
    """print_panel in PLAIN mode stampa su stdout."""
    result = print_panel("Content", "Title", "white", OutputMode.PLAIN)

    assert result is None
    captured = capsys.readouterr()
    assert "Title" in captured.out
    assert "Content" in captured.out


def test_print_metrics_table_markdown():
    """print_metrics_table in MARKDOWN mode genera metriche."""
    metrics = {
        'total': 100,
        'successes': 80,
        'failures': 20,
        'success_rate': 80.0
    }

    result = print_metrics_table(metrics, OutputMode.MARKDOWN)

    assert "## 📊 METRICHE CHIAVE" in result
    assert "**Eventi Totali:** 100" in result
    assert "**Successi:** 80" in result
    assert "**Errori:** 20" in result
    assert "**Success Rate:** 80.0%" in result


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_metrics_table_plain_mode(capsys):
    """print_metrics_table in PLAIN mode stampa su stdout."""
    metrics = {
        'total': 50,
        'successes': 45,
        'failures': 5,
        'success_rate': 90.0
    }

    result = print_metrics_table(metrics, OutputMode.PLAIN)

    assert result is None
    captured = capsys.readouterr()
    assert "METRICHE CHIAVE" in captured.out
    assert "Eventi Totali:    50" in captured.out
    assert "Successi:         45" in captured.out
    assert "Errori:           5" in captured.out
    assert "Success Rate:     90.0%" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_patterns_section_plain_mode(capsys):
    """print_patterns_section in PLAIN mode stampa pattern."""
    patterns = [
        {"pattern_name": "Import Error", "severity_level": "CRITICAL", "occurrence_count": 5},
        {"pattern_name": "DB Error", "severity_level": "HIGH", "occurrence_count": 3},
    ]

    print_patterns_section(patterns)

    captured = capsys.readouterr()
    assert "TOP 3 PATTERN ERRORI" in captured.out
    assert "Import Error" in captured.out
    assert "CRITICAL" in captured.out
    assert "DB Error" in captured.out
    assert "HIGH" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_lessons_section_plain_mode(capsys):
    """print_lessons_section in PLAIN mode stampa lezioni."""
    lessons = [
        {"pattern": "Fix import paths", "severity": "HIGH"},
        {"pattern": "Add DB pool", "severity": "MEDIUM"},
    ]

    print_lessons_section(lessons)

    captured = capsys.readouterr()
    assert "LEZIONI APPRESE" in captured.out
    assert "Fix import paths" in captured.out
    assert "HIGH" in captured.out
    assert "Add DB pool" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_agents_section_plain_mode(capsys):
    """print_agents_section in PLAIN mode stampa agenti."""
    agents = [
        {
            "agent_name": "cervella-backend",
            "total": 10,
            "successes": 8,
            "failures": 2,
            "avg_duration": 2500.0
        }
    ]

    print_agents_section(agents)

    captured = capsys.readouterr()
    assert "BREAKDOWN PER AGENTE" in captured.out
    assert "cervella-backend" in captured.out
    assert "10" in captured.out
    assert "8" in captured.out
    assert "2" in captured.out
    assert "2500ms" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_recommendations_section_plain_mode(capsys):
    """print_recommendations_section in PLAIN mode stampa raccomandazioni."""
    recommendations = [
        "Success rate < 80% - Investigate",
        "Alto numero di errori - Review"
    ]

    print_recommendations_section(recommendations)

    captured = capsys.readouterr()
    assert "RACCOMANDAZIONI" in captured.out
    assert "Success rate < 80%" in captured.out
    assert "Alto numero di errori" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_suggestions_section_plain_mode(capsys):
    """print_suggestions_section in PLAIN mode stampa suggerimenti."""
    pattern_suggestions = [
        ("pattern", 5, "Pattern 'Import Error' ripetuto 5 volte senza lezione")
    ]
    agent_suggestions = [
        ("agent", 60, "Agente 'cervella-bad' con 60% success rate")
    ]

    print_suggestions_section(pattern_suggestions, agent_suggestions)

    captured = capsys.readouterr()
    assert "LEZIONI SUGGERITE" in captured.out
    assert "Pattern ripetuti" in captured.out
    assert "Import Error" in captured.out
    assert "Agenti con basso success rate" in captured.out
    assert "cervella-bad" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_next_steps_section_plain_mode(capsys):
    """print_next_steps_section in PLAIN mode stampa step."""
    next_steps = [
        "1. Review pattern attivi",
        "2. Review lezioni attive"
    ]

    print_next_steps_section(next_steps)

    captured = capsys.readouterr()
    assert "PROSSIMI PASSI" in captured.out
    assert "Review pattern attivi" in captured.out
    assert "Review lezioni attive" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_empty_message_plain_mode(capsys):
    """print_empty_message in PLAIN mode stampa messaggio."""
    print_empty_message("Nessun dato disponibile")

    captured = capsys.readouterr()
    assert "Nessun dato disponibile" in captured.out


@patch('scripts.memory.retro.output.HAS_RICH', False)
def test_print_header_plain_mode(capsys):
    """print_header in PLAIN mode stampa header."""
    period_start = "2026-01-01T00:00:00"
    period_end = "2026-01-07T23:59:59"

    print_header(period_start, period_end, quiet=False)

    captured = capsys.readouterr()
    assert "WEEKLY RETROSPECTIVE" in captured.out
    assert "2026-01-01" in captured.out
    assert "2026-01-07" in captured.out


def test_print_header_quiet_mode(capsys):
    """print_header in quiet mode non stampa nulla."""
    period_start = "2026-01-01T00:00:00"
    period_end = "2026-01-07T23:59:59"

    print_header(period_start, period_end, quiet=True)

    captured = capsys.readouterr()
    assert captured.out == ""


# === RICH MODE TESTS ===

@patch('scripts.memory.retro.output.console')
def test_print_section_header_rich_mode(mock_console):
    """print_section_header in RICH mode calls console.print."""
    result = print_section_header("Test Section", OutputMode.RICH)

    assert result is None
    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_table_rich_mode(mock_console):
    """print_table in RICH mode calls console.print con Table."""
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    columns = [
        ("Name", "name", "left", "cyan", 15),
        ("Age", "age", "right", "white", 8)
    ]

    result = print_table(data, columns, "Test Table", OutputMode.RICH)

    assert result is None
    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_panel_rich_mode(mock_console):
    """print_panel in RICH mode calls console.print con Panel."""
    result = print_panel("Test content", "Panel Title", "white", OutputMode.RICH)

    assert result is None
    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_metrics_table_rich_mode(mock_console):
    """print_metrics_table in RICH mode calls console.print con Table."""
    metrics = {
        'total': 100,
        'successes': 80,
        'failures': 20,
        'success_rate': 80.0
    }

    result = print_metrics_table(metrics, OutputMode.RICH)

    assert result is None
    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_patterns_section_rich_mode(mock_console):
    """print_patterns_section in RICH mode calls console.print."""
    patterns = [
        {"pattern_name": "Import Error", "severity_level": "CRITICAL", "occurrence_count": 5},
        {"pattern_name": "DB Error", "severity_level": "HIGH", "occurrence_count": 3}
    ]

    print_patterns_section(patterns)

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_lessons_section_rich_mode(mock_console):
    """print_lessons_section in RICH mode calls console.print."""
    lessons = [
        {"pattern": "Fix import paths", "severity": "HIGH"},
        {"pattern": "Add DB pool", "severity": "MEDIUM"}
    ]

    print_lessons_section(lessons)

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_agents_section_rich_mode(mock_console):
    """print_agents_section in RICH mode calls console.print."""
    agents = [
        {
            "agent_name": "cervella-backend",
            "total": 10,
            "successes": 8,
            "failures": 2,
            "avg_duration": 2500.0
        }
    ]

    print_agents_section(agents)

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_recommendations_section_rich_mode(mock_console):
    """print_recommendations_section in RICH mode calls console.print."""
    recommendations = [
        "Success rate < 80% - Investigate",
        "Alto numero di errori - Review"
    ]

    print_recommendations_section(recommendations)

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_suggestions_section_rich_mode(mock_console):
    """print_suggestions_section in RICH mode calls console.print."""
    pattern_suggestions = [
        ("pattern", 5, "Pattern 'Import Error' ripetuto 5 volte senza lezione")
    ]
    agent_suggestions = [
        ("agent", 60, "Agente 'cervella-bad' con 60% success rate")
    ]

    print_suggestions_section(pattern_suggestions, agent_suggestions)

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_next_steps_section_rich_mode(mock_console):
    """print_next_steps_section in RICH mode calls console.print."""
    next_steps = [
        "1. Review pattern attivi",
        "2. Review lezioni attive"
    ]

    print_next_steps_section(next_steps)

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_empty_message_rich_mode(mock_console):
    """print_empty_message in RICH mode calls console.print."""
    print_empty_message("Nessun dato disponibile")

    assert mock_console.print.called


@patch('scripts.memory.retro.output.console')
def test_print_header_rich_mode(mock_console):
    """print_header in RICH mode calls console.print."""
    period_start = "2026-01-01T00:00:00"
    period_end = "2026-01-07T23:59:59"

    print_header(period_start, period_end, quiet=False)

    assert mock_console.print.called


