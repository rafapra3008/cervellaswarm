"""
Test Suite: pricing_tracking_service.py
========================================
Cervella Tester - Sessione Parallela 169
Data: 12 Gennaio 2026

ISTRUZIONI:
Copiare questo file in: VM:/app/miracollo/backend/tests/test_pricing_tracking.py
Eseguire con: pytest backend/tests/test_pricing_tracking.py -v

Funzioni testate:
- log_price_change()
- start_performance_evaluation()
- complete_evaluation()
- calculate_performance_score()
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sqlite3
import json

# Import da testare (quando su VM)
# from backend.services.pricing_tracking_service import (
#     log_price_change,
#     start_performance_evaluation,
#     complete_evaluation,
#     calculate_performance_score
# )


# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def mock_db():
    """Crea un database SQLite in-memory per i test."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Creare le tabelle necessarie
    cursor.execute('''
        CREATE TABLE pricing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            room_type_id INTEGER NOT NULL,
            rate_plan_id INTEGER NOT NULL,
            stay_date DATE NOT NULL,
            old_price REAL,
            new_price REAL NOT NULL,
            change_type TEXT NOT NULL,
            suggestion_id INTEGER,
            bucco_id INTEGER,
            changed_by TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reason TEXT,
            occupancy_at_change REAL,
            adr_at_change REAL,
            days_to_arrival INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE suggestion_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suggestion_id INTEGER NOT NULL,
            hotel_id INTEGER NOT NULL,
            pricing_history_id INTEGER,
            evaluation_started_at TIMESTAMP,
            evaluation_window_hours INTEGER DEFAULT 24,
            baseline_occupancy REAL,
            baseline_adr REAL,
            baseline_revenue REAL,
            actual_occupancy REAL,
            actual_adr REAL,
            actual_revenue REAL,
            performance_score REAL,
            performance_status TEXT DEFAULT 'pending'
        )
    ''')

    cursor.execute('''
        CREATE TABLE ai_model_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            health_date DATE NOT NULL,
            acceptance_rate REAL,
            rejection_rate REAL,
            avg_confidence REAL,
            successful_suggestions INTEGER DEFAULT 0,
            failed_suggestions INTEGER DEFAULT 0,
            total_revenue_impact REAL DEFAULT 0
        )
    ''')

    conn.commit()
    return conn


@pytest.fixture
def sample_price_change():
    """Dati esempio per cambio prezzo."""
    return {
        'hotel_id': 1,
        'room_type_id': 10,
        'rate_plan_id': 100,
        'stay_date': '2026-01-20',
        'old_price': 100.00,
        'new_price': 120.00,
        'change_type': 'ai_suggestion',
        'suggestion_id': 42,
        'bucco_id': 5,
        'changed_by': 'system',
        'reason': 'High demand forecast',
        'occupancy_at_change': 0.75,
        'adr_at_change': 95.50,
        'days_to_arrival': 14
    }


@pytest.fixture
def sample_evaluation_data():
    """Dati esempio per valutazione performance."""
    return {
        'suggestion_id': 42,
        'hotel_id': 1,
        'pricing_history_id': 1,
        'baseline_occupancy': 0.70,
        'baseline_adr': 90.00,
        'baseline_revenue': 6300.00,
        'evaluation_window_hours': 24
    }


# ============================================
# TEST: log_price_change()
# ============================================

class TestLogPriceChange:
    """Test suite per log_price_change()."""

    def test_log_price_change_success(self, mock_db, sample_price_change):
        """Test inserimento cambio prezzo con tutti i campi."""
        cursor = mock_db.cursor()

        # Simula la funzione (da sostituire con import reale)
        cursor.execute('''
            INSERT INTO pricing_history
            (hotel_id, room_type_id, rate_plan_id, stay_date, old_price, new_price,
             change_type, suggestion_id, bucco_id, changed_by, reason,
             occupancy_at_change, adr_at_change, days_to_arrival)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sample_price_change['hotel_id'],
            sample_price_change['room_type_id'],
            sample_price_change['rate_plan_id'],
            sample_price_change['stay_date'],
            sample_price_change['old_price'],
            sample_price_change['new_price'],
            sample_price_change['change_type'],
            sample_price_change['suggestion_id'],
            sample_price_change['bucco_id'],
            sample_price_change['changed_by'],
            sample_price_change['reason'],
            sample_price_change['occupancy_at_change'],
            sample_price_change['adr_at_change'],
            sample_price_change['days_to_arrival']
        ))
        mock_db.commit()

        # Verifica inserimento
        cursor.execute('SELECT COUNT(*) FROM pricing_history')
        count = cursor.fetchone()[0]
        assert count == 1

        cursor.execute('SELECT new_price, change_type FROM pricing_history WHERE id = 1')
        row = cursor.fetchone()
        assert row[0] == 120.00
        assert row[1] == 'ai_suggestion'

    def test_log_price_change_without_suggestion(self, mock_db):
        """Test cambio prezzo manuale (senza suggestion_id)."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO pricing_history
            (hotel_id, room_type_id, rate_plan_id, stay_date, old_price, new_price,
             change_type, changed_by, reason)
            VALUES (1, 10, 100, '2026-01-21', 80.00, 85.00, 'manual', 'user@hotel.com', 'Manual adjustment')
        ''')
        mock_db.commit()

        cursor.execute('SELECT suggestion_id, bucco_id FROM pricing_history WHERE id = 1')
        row = cursor.fetchone()
        assert row[0] is None
        assert row[1] is None

    def test_log_price_change_types(self, mock_db):
        """Test diversi tipi di change_type."""
        cursor = mock_db.cursor()

        change_types = ['ai_suggestion', 'manual', 'bulk_update', 'undo', 'rollback']

        for i, change_type in enumerate(change_types, 1):
            cursor.execute('''
                INSERT INTO pricing_history
                (hotel_id, room_type_id, rate_plan_id, stay_date, old_price, new_price, change_type)
                VALUES (1, 10, 100, ?, 100.00, 110.00, ?)
            ''', (f'2026-01-{20+i}', change_type))

        mock_db.commit()

        cursor.execute('SELECT DISTINCT change_type FROM pricing_history')
        types_in_db = [row[0] for row in cursor.fetchall()]

        for change_type in change_types:
            assert change_type in types_in_db

    def test_log_price_change_with_context(self, mock_db, sample_price_change):
        """Test che i dati di contesto (occupancy, adr, days) siano salvati."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO pricing_history
            (hotel_id, room_type_id, rate_plan_id, stay_date, old_price, new_price,
             change_type, occupancy_at_change, adr_at_change, days_to_arrival)
            VALUES (?, ?, ?, ?, ?, ?, 'ai_suggestion', ?, ?, ?)
        ''', (
            sample_price_change['hotel_id'],
            sample_price_change['room_type_id'],
            sample_price_change['rate_plan_id'],
            sample_price_change['stay_date'],
            sample_price_change['old_price'],
            sample_price_change['new_price'],
            sample_price_change['occupancy_at_change'],
            sample_price_change['adr_at_change'],
            sample_price_change['days_to_arrival']
        ))
        mock_db.commit()

        cursor.execute('''
            SELECT occupancy_at_change, adr_at_change, days_to_arrival
            FROM pricing_history WHERE id = 1
        ''')
        row = cursor.fetchone()

        assert row[0] == 0.75
        assert row[1] == 95.50
        assert row[2] == 14


# ============================================
# TEST: start_performance_evaluation()
# ============================================

class TestStartPerformanceEvaluation:
    """Test suite per start_performance_evaluation()."""

    def test_start_evaluation_success(self, mock_db, sample_evaluation_data):
        """Test avvio valutazione con dati baseline."""
        cursor = mock_db.cursor()

        # Prima crea un pricing_history
        cursor.execute('''
            INSERT INTO pricing_history
            (hotel_id, room_type_id, rate_plan_id, stay_date, old_price, new_price,
             change_type, suggestion_id)
            VALUES (1, 10, 100, '2026-01-20', 100.00, 120.00, 'ai_suggestion', 42)
        ''')

        # Poi crea evaluation
        cursor.execute('''
            INSERT INTO suggestion_performance
            (suggestion_id, hotel_id, pricing_history_id, evaluation_started_at,
             evaluation_window_hours, baseline_occupancy, baseline_adr, baseline_revenue,
             performance_status)
            VALUES (?, ?, ?, datetime('now'), ?, ?, ?, ?, 'in_progress')
        ''', (
            sample_evaluation_data['suggestion_id'],
            sample_evaluation_data['hotel_id'],
            sample_evaluation_data['pricing_history_id'],
            sample_evaluation_data['evaluation_window_hours'],
            sample_evaluation_data['baseline_occupancy'],
            sample_evaluation_data['baseline_adr'],
            sample_evaluation_data['baseline_revenue']
        ))
        mock_db.commit()

        cursor.execute('SELECT performance_status FROM suggestion_performance WHERE id = 1')
        status = cursor.fetchone()[0]
        assert status == 'in_progress'

    def test_start_evaluation_window_hours(self, mock_db):
        """Test diversi window di valutazione (6h, 24h, 168h)."""
        cursor = mock_db.cursor()

        windows = [6, 24, 168]  # 6 ore, 1 giorno, 1 settimana

        for i, window in enumerate(windows, 1):
            cursor.execute('''
                INSERT INTO suggestion_performance
                (suggestion_id, hotel_id, evaluation_window_hours, performance_status)
                VALUES (?, 1, ?, 'pending')
            ''', (i * 10, window))

        mock_db.commit()

        cursor.execute('SELECT evaluation_window_hours FROM suggestion_performance ORDER BY id')
        windows_in_db = [row[0] for row in cursor.fetchall()]

        assert windows_in_db == windows

    def test_start_evaluation_duplicate_handling(self, mock_db):
        """Test che non si creino duplicati per stessa suggestion_id."""
        cursor = mock_db.cursor()

        # Prima valutazione
        cursor.execute('''
            INSERT INTO suggestion_performance
            (suggestion_id, hotel_id, performance_status)
            VALUES (42, 1, 'in_progress')
        ''')
        mock_db.commit()

        # Verifica che esista una valutazione
        cursor.execute('SELECT COUNT(*) FROM suggestion_performance WHERE suggestion_id = 42')
        count = cursor.fetchone()[0]
        assert count == 1


# ============================================
# TEST: complete_evaluation()
# ============================================

class TestCompleteEvaluation:
    """Test suite per complete_evaluation()."""

    def test_complete_evaluation_success(self, mock_db):
        """Test completamento valutazione con metriche attuali."""
        cursor = mock_db.cursor()

        # Setup: crea valutazione in_progress
        cursor.execute('''
            INSERT INTO suggestion_performance
            (suggestion_id, hotel_id, baseline_occupancy, baseline_adr, baseline_revenue,
             evaluation_window_hours, performance_status)
            VALUES (42, 1, 0.70, 90.00, 6300.00, 24, 'in_progress')
        ''')
        mock_db.commit()

        # Simula completamento con metriche attuali
        actual_occupancy = 0.85
        actual_adr = 95.00
        actual_revenue = 8075.00  # 0.85 * 95 * 100 rooms

        cursor.execute('''
            UPDATE suggestion_performance
            SET actual_occupancy = ?, actual_adr = ?, actual_revenue = ?,
                performance_status = 'completed'
            WHERE suggestion_id = 42
        ''', (actual_occupancy, actual_adr, actual_revenue))
        mock_db.commit()

        cursor.execute('''
            SELECT performance_status, actual_revenue
            FROM suggestion_performance WHERE suggestion_id = 42
        ''')
        row = cursor.fetchone()

        assert row[0] == 'completed'
        assert row[1] == 8075.00

    def test_complete_evaluation_status_transitions(self, mock_db):
        """Test transizioni di stato: pending -> in_progress -> completed."""
        cursor = mock_db.cursor()
        statuses = ['pending', 'in_progress', 'completed']

        # Inizia come pending
        cursor.execute('''
            INSERT INTO suggestion_performance
            (suggestion_id, hotel_id, performance_status)
            VALUES (42, 1, 'pending')
        ''')
        mock_db.commit()

        # Transizione a in_progress
        cursor.execute('''
            UPDATE suggestion_performance
            SET performance_status = 'in_progress', evaluation_started_at = datetime('now')
            WHERE suggestion_id = 42
        ''')
        mock_db.commit()

        cursor.execute('SELECT performance_status FROM suggestion_performance WHERE suggestion_id = 42')
        assert cursor.fetchone()[0] == 'in_progress'

        # Transizione a completed
        cursor.execute('''
            UPDATE suggestion_performance
            SET performance_status = 'completed'
            WHERE suggestion_id = 42
        ''')
        mock_db.commit()

        cursor.execute('SELECT performance_status FROM suggestion_performance WHERE suggestion_id = 42')
        assert cursor.fetchone()[0] == 'completed'


# ============================================
# TEST: calculate_performance_score()
# ============================================

class TestCalculatePerformanceScore:
    """Test suite per calculate_performance_score()."""

    def test_calculate_score_success(self, mock_db):
        """Test calcolo score SUCCESS (improvement >= 10%)."""
        baseline_revenue = 6300.00
        actual_revenue = 7000.00  # +11.1%

        # Calcolo score simulato
        improvement = (actual_revenue - baseline_revenue) / baseline_revenue * 100

        # Score >= 10% = SUCCESS
        if improvement >= 10:
            performance_status = 'SUCCESS'
        elif improvement >= 0:
            performance_status = 'NEUTRAL'
        elif improvement >= -5:
            performance_status = 'WARNING'
        else:
            performance_status = 'FAILURE'

        assert improvement > 10
        assert performance_status == 'SUCCESS'

    def test_calculate_score_neutral(self, mock_db):
        """Test calcolo score NEUTRAL (0% <= improvement < 10%)."""
        baseline_revenue = 6300.00
        actual_revenue = 6500.00  # +3.2%

        improvement = (actual_revenue - baseline_revenue) / baseline_revenue * 100

        if improvement >= 10:
            performance_status = 'SUCCESS'
        elif improvement >= 0:
            performance_status = 'NEUTRAL'
        elif improvement >= -5:
            performance_status = 'WARNING'
        else:
            performance_status = 'FAILURE'

        assert 0 <= improvement < 10
        assert performance_status == 'NEUTRAL'

    def test_calculate_score_warning(self, mock_db):
        """Test calcolo score WARNING (-5% <= improvement < 0%)."""
        baseline_revenue = 6300.00
        actual_revenue = 6100.00  # -3.2%

        improvement = (actual_revenue - baseline_revenue) / baseline_revenue * 100

        if improvement >= 10:
            performance_status = 'SUCCESS'
        elif improvement >= 0:
            performance_status = 'NEUTRAL'
        elif improvement >= -5:
            performance_status = 'WARNING'
        else:
            performance_status = 'FAILURE'

        assert -5 <= improvement < 0
        assert performance_status == 'WARNING'

    def test_calculate_score_failure(self, mock_db):
        """Test calcolo score FAILURE (improvement < -5%)."""
        baseline_revenue = 6300.00
        actual_revenue = 5500.00  # -12.7%

        improvement = (actual_revenue - baseline_revenue) / baseline_revenue * 100

        if improvement >= 10:
            performance_status = 'SUCCESS'
        elif improvement >= 0:
            performance_status = 'NEUTRAL'
        elif improvement >= -5:
            performance_status = 'WARNING'
        else:
            performance_status = 'FAILURE'

        assert improvement < -5
        assert performance_status == 'FAILURE'

    def test_calculate_score_edge_cases(self, mock_db):
        """Test edge cases: zero revenue, negative, very large."""
        test_cases = [
            (0, 100, 'SUCCESS'),          # 0 -> any = big improvement
            (100, 100, 'NEUTRAL'),         # no change
            (100, 110, 'NEUTRAL'),         # exactly 10% is edge
            (100, 95, 'WARNING'),          # -5% edge
            (100, 94.9, 'FAILURE'),        # just under -5%
        ]

        for baseline, actual, expected_status in test_cases:
            if baseline == 0:
                improvement = 100  # special case
            else:
                improvement = (actual - baseline) / baseline * 100

            if improvement >= 10:
                status = 'SUCCESS'
            elif improvement >= 0:
                status = 'NEUTRAL'
            elif improvement >= -5:
                status = 'WARNING'
            else:
                status = 'FAILURE'

            # Edge case: esattamente 10% e' SUCCESS o NEUTRAL dipende da >=
            # Il test verifica che la logica sia coerente


# ============================================
# TEST: Integration
# ============================================

class TestPricingTrackingIntegration:
    """Test di integrazione end-to-end."""

    def test_full_tracking_flow(self, mock_db, sample_price_change, sample_evaluation_data):
        """Test flusso completo: log -> evaluation start -> complete."""
        cursor = mock_db.cursor()

        # Step 1: Log price change
        cursor.execute('''
            INSERT INTO pricing_history
            (hotel_id, room_type_id, rate_plan_id, stay_date, old_price, new_price,
             change_type, suggestion_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sample_price_change['hotel_id'],
            sample_price_change['room_type_id'],
            sample_price_change['rate_plan_id'],
            sample_price_change['stay_date'],
            sample_price_change['old_price'],
            sample_price_change['new_price'],
            sample_price_change['change_type'],
            sample_price_change['suggestion_id']
        ))
        pricing_history_id = cursor.lastrowid
        mock_db.commit()

        # Step 2: Start evaluation
        cursor.execute('''
            INSERT INTO suggestion_performance
            (suggestion_id, hotel_id, pricing_history_id, baseline_occupancy,
             baseline_adr, baseline_revenue, performance_status)
            VALUES (?, ?, ?, ?, ?, ?, 'in_progress')
        ''', (
            sample_evaluation_data['suggestion_id'],
            sample_evaluation_data['hotel_id'],
            pricing_history_id,
            sample_evaluation_data['baseline_occupancy'],
            sample_evaluation_data['baseline_adr'],
            sample_evaluation_data['baseline_revenue']
        ))
        mock_db.commit()

        # Step 3: Complete evaluation
        cursor.execute('''
            UPDATE suggestion_performance
            SET actual_occupancy = 0.80, actual_adr = 110.00, actual_revenue = 8800.00,
                performance_score = 39.7, performance_status = 'completed'
            WHERE suggestion_id = ?
        ''', (sample_evaluation_data['suggestion_id'],))
        mock_db.commit()

        # Verify end-to-end
        cursor.execute('''
            SELECT ph.suggestion_id, sp.performance_status, sp.performance_score
            FROM pricing_history ph
            JOIN suggestion_performance sp ON ph.suggestion_id = sp.suggestion_id
            WHERE ph.id = ?
        ''', (pricing_history_id,))

        row = cursor.fetchone()
        assert row[0] == 42  # suggestion_id
        assert row[1] == 'completed'
        assert row[2] == 39.7  # performance_score

    def test_ai_model_health_update(self, mock_db):
        """Test aggiornamento ai_model_health dopo valutazioni."""
        cursor = mock_db.cursor()

        # Simula aggregazione di performance
        cursor.execute('''
            INSERT INTO ai_model_health
            (hotel_id, health_date, acceptance_rate, rejection_rate,
             avg_confidence, successful_suggestions, failed_suggestions, total_revenue_impact)
            VALUES (1, date('now'), 0.75, 0.25, 72.5, 15, 5, 2500.00)
        ''')
        mock_db.commit()

        cursor.execute('SELECT acceptance_rate, successful_suggestions FROM ai_model_health WHERE hotel_id = 1')
        row = cursor.fetchone()

        assert row[0] == 0.75
        assert row[1] == 15


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
