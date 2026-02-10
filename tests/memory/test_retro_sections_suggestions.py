"""
Test per scripts.memory.retro.sections e scripts.memory.retro.suggestions.

Coverage focus: Data extraction e generazione suggerimenti (no rendering).
Fixture retro_db e populated_retro_db definite in conftest.py.
"""

import pytest
import sqlite3
from datetime import datetime, timedelta

from scripts.memory.retro.sections import (
    fetch_metrics,
    fetch_top_patterns,
    fetch_lessons,
    fetch_agent_breakdown,
    generate_recommendations,
    generate_next_steps
)
from scripts.memory.retro.suggestions import suggest_new_lessons


# === TEST SECTIONS.PY ===

def test_fetch_metrics_with_mixed_events(populated_retro_db):
    """fetch_metrics calcola correttamente metriche con eventi misti."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    metrics = fetch_metrics(conn, period_start)

    assert metrics['total'] == 7
    assert metrics['successes'] == 5
    assert metrics['failures'] == 2
    assert metrics['success_rate'] == pytest.approx(71.43, rel=0.1)

    conn.close()


def test_fetch_metrics_empty_db(retro_db):
    """fetch_metrics con DB vuoto ritorna total=0 e success_rate=0."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    metrics = fetch_metrics(conn, period_start)

    assert metrics['total'] == 0
    # SQLite SUM ritorna None quando non ci sono righe da sommare
    assert metrics['successes'] == 0 or metrics['successes'] is None
    assert metrics['failures'] == 0 or metrics['failures'] is None
    assert metrics['success_rate'] == 0

    conn.close()


def test_fetch_top_patterns_orders_by_severity_then_count(populated_retro_db):
    """fetch_top_patterns ordina per severity (CRITICAL > HIGH > MEDIUM) poi per count."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    patterns = fetch_top_patterns(conn, limit=3)

    assert len(patterns) == 3
    # CRITICAL first (Import Error)
    assert patterns[0]['pattern_name'] == "Import Error"
    assert patterns[0]['severity_level'] == "CRITICAL"
    assert patterns[0]['occurrence_count'] == 5

    # HIGH second (DB Connection)
    assert patterns[1]['pattern_name'] == "DB Connection"
    assert patterns[1]['severity_level'] == "HIGH"

    # MEDIUM third (CSS z-index)
    assert patterns[2]['pattern_name'] == "CSS z-index"
    assert patterns[2]['severity_level'] == "MEDIUM"

    conn.close()


def test_fetch_top_patterns_only_active(populated_retro_db):
    """fetch_top_patterns ritorna solo pattern con status=ACTIVE."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    patterns = fetch_top_patterns(conn, limit=10)

    # Old Pattern e RESOLVED, non deve apparire
    pattern_names = [p['pattern_name'] for p in patterns]
    assert "Old Pattern" not in pattern_names

    conn.close()


def test_fetch_lessons_orders_by_severity(populated_retro_db):
    """fetch_lessons ordina per severity (CRITICAL > HIGH > MEDIUM)."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    lessons = fetch_lessons(conn, period_start, limit=5)

    assert len(lessons) == 3
    assert lessons[0]['severity'] == "CRITICAL"
    assert lessons[1]['severity'] == "HIGH"
    assert lessons[2]['severity'] == "MEDIUM"

    conn.close()


def test_fetch_lessons_filters_by_period(populated_retro_db):
    """fetch_lessons filtra per created_at >= period_start."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    # Period start 1 giorno fa (esclude lezione da 2 giorni fa)
    period_start = (datetime.now() - timedelta(days=1)).isoformat()
    lessons = fetch_lessons(conn, period_start, limit=5)

    # Solo le 2 lezioni di oggi
    assert len(lessons) == 2

    conn.close()


def test_fetch_agent_breakdown_includes_duration(populated_retro_db):
    """fetch_agent_breakdown include avg_duration calcolato da duration_ms."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    agents = fetch_agent_breakdown(conn, period_start, limit=5)

    assert len(agents) > 0
    # cervella-backend ha 4 eventi nel periodo: 2500, 3000, 2000, 1800 -> avg = 2325
    backend_agent = next((a for a in agents if a['agent_name'] == 'cervella-backend'), None)
    assert backend_agent is not None
    assert backend_agent['avg_duration'] == pytest.approx(2325, abs=10)
    assert backend_agent['total'] == 4
    assert backend_agent['successes'] == 4
    assert backend_agent['failures'] == 0

    conn.close()


def test_fetch_agent_breakdown_excludes_null_agents(populated_retro_db):
    """fetch_agent_breakdown esclude eventi con agent_name=NULL."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Aggiungi evento con agent_name=NULL
    cursor.execute("""
        INSERT INTO swarm_events (timestamp, agent_name, success)
        VALUES (?, NULL, 1)
    """, (datetime.now().isoformat(),))
    conn.commit()

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    agents = fetch_agent_breakdown(conn, period_start, limit=10)

    # Nessun agente NULL deve apparire
    agent_names = [a['agent_name'] for a in agents]
    assert None not in agent_names

    conn.close()


def test_generate_recommendations_low_success_rate(retro_db):
    """generate_recommendations genera warning se success_rate < 80."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {
        'total': 100,
        'successes': 50,
        'failures': 50,
        'success_rate': 50.0
    }

    recs = generate_recommendations(metrics, conn)

    # Deve contenere warning su success rate
    assert any("Success rate < 80%" in rec for rec in recs)

    conn.close()


def test_generate_recommendations_high_failures(retro_db):
    """generate_recommendations genera warning se failures > 10."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {
        'total': 100,
        'successes': 85,
        'failures': 15,
        'success_rate': 85.0
    }

    recs = generate_recommendations(metrics, conn)

    # Deve contenere warning su alto numero errori
    assert any("Alto numero di errori" in rec for rec in recs)

    conn.close()


def test_generate_recommendations_inactive_system(retro_db):
    """generate_recommendations genera messaggio inattivo se total=0."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {
        'total': 0,
        'successes': 0,
        'failures': 0,
        'success_rate': 0
    }

    recs = generate_recommendations(metrics, conn)

    # Deve contenere messaggio sistema inattivo
    assert any("Sistema inattivo" in rec for rec in recs)

    conn.close()


def test_generate_recommendations_stable_system(retro_db):
    """generate_recommendations genera messaggio positivo se tutto OK."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {
        'total': 50,
        'successes': 48,
        'failures': 2,
        'success_rate': 96.0
    }

    recs = generate_recommendations(metrics, conn)

    # Deve contenere messaggio sistema stabile
    assert any("Sistema stabile" in rec for rec in recs)

    conn.close()


def test_generate_recommendations_many_active_lessons(retro_db):
    """generate_recommendations segnala se > 5 lezioni ACTIVE."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    # Inserisci 6 lezioni ACTIVE
    for i in range(6):
        conn.execute(
            "INSERT INTO lessons_learned (pattern, status) VALUES (?, 'ACTIVE')",
            (f"lesson_{i}",)
        )
    conn.commit()

    metrics = {'total': 50, 'successes': 48, 'failures': 2, 'success_rate': 96.0}
    recs = generate_recommendations(metrics, conn)

    assert any("6 lezioni ACTIVE" in rec for rec in recs)
    conn.close()


def test_generate_recommendations_many_active_patterns(retro_db):
    """generate_recommendations segnala se > 3 pattern ACTIVE."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    # Inserisci 4 pattern ACTIVE
    for i in range(4):
        conn.execute(
            "INSERT INTO error_patterns (pattern_name, status) VALUES (?, 'ACTIVE')",
            (f"pattern_{i}",)
        )
    conn.commit()

    metrics = {'total': 50, 'successes': 48, 'failures': 2, 'success_rate': 96.0}
    recs = generate_recommendations(metrics, conn)

    assert any("4 pattern ACTIVE" in rec for rec in recs)
    conn.close()


def test_generate_next_steps_with_active_patterns(populated_retro_db):
    """generate_next_steps suggerisce review pattern se ci sono pattern attivi."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {'total': 10, 'failures': 2}
    steps = generate_next_steps(conn, metrics)

    # Deve suggerire review pattern
    assert any("pattern attivi" in step for step in steps)

    conn.close()


def test_generate_next_steps_with_active_lessons(populated_retro_db):
    """generate_next_steps suggerisce review lezioni se ci sono lezioni attive."""
    conn = sqlite3.connect(populated_retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {'total': 10, 'failures': 2}
    steps = generate_next_steps(conn, metrics)

    # Deve suggerire review lezioni
    assert any("lezioni attive" in step for step in steps)

    conn.close()


def test_generate_next_steps_with_many_failures(retro_db):
    """generate_next_steps suggerisce analisi errori se failures > 5."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {'total': 100, 'failures': 10}
    steps = generate_next_steps(conn, metrics)

    # Deve suggerire analisi ultimi errori
    assert any("ultimi errori" in step for step in steps)

    conn.close()


def test_generate_next_steps_system_ok(retro_db):
    """generate_next_steps genera messaggio OK se nessuna azione richiesta."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    metrics = {'total': 50, 'failures': 2}
    steps = generate_next_steps(conn, metrics)

    # Deve contenere messaggio sistema OK
    assert any("Sistema OK" in step for step in steps)

    conn.close()


# === TEST SUGGESTIONS.PY ===

def test_suggest_new_lessons_pattern_without_lesson(retro_db):
    """suggest_new_lessons trova pattern ripetuti (count >= 3) senza lezione associata."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Pattern ripetuto 5 volte senza lezione
    cursor.execute("""
        INSERT INTO error_patterns (pattern_name, occurrence_count, status)
        VALUES ('Repeated Error', 5, 'ACTIVE')
    """)
    conn.commit()

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    suggestions = suggest_new_lessons(conn, period_start)

    # Deve suggerire lezione per questo pattern
    pattern_suggestions = [s for s in suggestions if s[0] == 'pattern']
    assert len(pattern_suggestions) > 0
    assert any("Repeated Error" in s[2] for s in pattern_suggestions)

    conn.close()


def test_suggest_new_lessons_agent_low_success_rate(retro_db):
    """suggest_new_lessons trova agenti con success_rate < 80 e total >= 5."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Agente con 10 task, 6 success = 60% success rate
    now = datetime.now()
    for i in range(10):
        success = 1 if i < 6 else 0
        cursor.execute("""
            INSERT INTO swarm_events (timestamp, agent_name, success)
            VALUES (?, 'cervella-bad-agent', ?)
        """, (now.isoformat(), success))
    conn.commit()

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    suggestions = suggest_new_lessons(conn, period_start)

    # Deve suggerire lezione per questo agente
    agent_suggestions = [s for s in suggestions if s[0] == 'agent']
    assert len(agent_suggestions) > 0
    assert any("cervella-bad-agent" in s[2] for s in agent_suggestions)

    conn.close()


def test_suggest_new_lessons_empty_db(retro_db):
    """suggest_new_lessons con DB vuoto ritorna lista vuota."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    suggestions = suggest_new_lessons(conn, period_start)

    assert suggestions == []

    conn.close()


def test_suggest_new_lessons_ignores_existing_lessons(retro_db):
    """suggest_new_lessons ignora pattern che hanno gia una lezione associata."""
    conn = sqlite3.connect(retro_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Pattern ripetuto MA con lezione gia documentata
    cursor.execute("""
        INSERT INTO error_patterns (pattern_name, occurrence_count, status)
        VALUES ('Documented Error', 5, 'ACTIVE')
    """)
    cursor.execute("""
        INSERT INTO lessons_learned (pattern, status)
        VALUES ('Fix for Documented Error - uses pattern name', 'ACTIVE')
    """)
    conn.commit()

    period_start = (datetime.now() - timedelta(days=7)).isoformat()
    suggestions = suggest_new_lessons(conn, period_start)

    # NON deve suggerire lezione per questo pattern
    pattern_suggestions = [s for s in suggestions if s[0] == 'pattern']
    assert not any("Documented Error" in s[2] for s in pattern_suggestions)

    conn.close()
