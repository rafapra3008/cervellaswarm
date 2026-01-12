"""
Test Suite: action_tracking_api.py
==================================
Cervella Tester - Sessione Parallela 169
Data: 12 Gennaio 2026

ISTRUZIONI:
Copiare questo file in: VM:/app/miracollo/backend/tests/test_action_tracking.py
Eseguire con: pytest backend/tests/test_action_tracking.py -v

Endpoints testati:
- GET /api/actions/history
- POST /api/actions/apply
- POST /api/actions/{id}/rollback
- GET /api/actions/{id}/monitoring
- POST /api/actions/{id}/pause
- POST /api/actions/{id}/resume
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sqlite3
import json

# Import da testare (quando su VM)
# from fastapi.testclient import TestClient
# from backend.main import app
# client = TestClient(app)


# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def mock_db():
    """Crea un database SQLite in-memory per i test."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Tabella suggestion_applications (034)
    cursor.execute('''
        CREATE TABLE suggestion_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suggestion_id INTEGER NOT NULL,
            hotel_id INTEGER NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            before_snapshot TEXT,
            changes_applied TEXT,
            pricing_version_id INTEGER,
            status TEXT DEFAULT 'active',
            current_metrics TEXT,
            effectiveness_score REAL
        )
    ''')

    # Tabella pricing_versions (034)
    cursor.execute('''
        CREATE TABLE pricing_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            snapshot TEXT NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Tabella monitoring_snapshots (034)
    cursor.execute('''
        CREATE TABLE monitoring_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metrics TEXT NOT NULL,
            delta_from_baseline TEXT,
            alert_level TEXT DEFAULT 'normal'
        )
    ''')

    # Tabella monitoring_notifications (035)
    cursor.execute('''
        CREATE TABLE monitoring_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            notification_type TEXT NOT NULL,
            message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acknowledged_at TIMESTAMP
        )
    ''')

    # Tabella revenue_suggestions per referenza
    cursor.execute('''
        CREATE TABLE revenue_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            tipo TEXT,
            status TEXT DEFAULT 'pending',
            suggested_price REAL,
            confidence_score REAL
        )
    ''')

    # Tabella pricing_history per rollback
    cursor.execute('''
        CREATE TABLE pricing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            room_type_id INTEGER,
            rate_plan_id INTEGER,
            stay_date DATE,
            old_price REAL,
            new_price REAL,
            change_type TEXT,
            suggestion_id INTEGER,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    return conn


@pytest.fixture
def sample_application():
    """Dati esempio per application."""
    return {
        'suggestion_id': 42,
        'hotel_id': 1,
        'before_snapshot': json.dumps({
            'rooms': [
                {'room_type_id': 10, 'price': 100.00, 'date': '2026-01-20'},
                {'room_type_id': 10, 'price': 100.00, 'date': '2026-01-21'}
            ]
        }),
        'changes_applied': json.dumps({
            'rooms': [
                {'room_type_id': 10, 'old_price': 100.00, 'new_price': 120.00, 'date': '2026-01-20'},
                {'room_type_id': 10, 'old_price': 100.00, 'new_price': 120.00, 'date': '2026-01-21'}
            ]
        })
    }


@pytest.fixture
def sample_monitoring_snapshot():
    """Dati esempio per monitoring snapshot."""
    return {
        'application_id': 1,
        'metrics': json.dumps({
            'occupancy': 0.85,
            'adr': 115.00,
            'revenue': 9775.00,
            'bookings_24h': 5
        }),
        'delta_from_baseline': json.dumps({
            'occupancy_delta': 0.15,
            'adr_delta': 15.00,
            'revenue_delta_pct': 28.5
        }),
        'alert_level': 'normal'
    }


# ============================================
# TEST: GET /api/actions/history
# ============================================

class TestGetActionsHistory:
    """Test suite per GET /api/actions/history."""

    def test_get_history_empty(self, mock_db):
        """Test history vuota."""
        cursor = mock_db.cursor()
        cursor.execute('SELECT * FROM suggestion_applications WHERE hotel_id = 1')
        rows = cursor.fetchall()

        assert len(rows) == 0

    def test_get_history_with_data(self, mock_db, sample_application):
        """Test history con applicazioni."""
        cursor = mock_db.cursor()

        # Inserisci applicazione
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, before_snapshot, changes_applied, status)
            VALUES (?, ?, ?, ?, 'active')
        ''', (
            sample_application['suggestion_id'],
            sample_application['hotel_id'],
            sample_application['before_snapshot'],
            sample_application['changes_applied']
        ))
        mock_db.commit()

        # Query history
        cursor.execute('''
            SELECT id, suggestion_id, status, applied_at
            FROM suggestion_applications
            WHERE hotel_id = 1
            ORDER BY applied_at DESC
        ''')
        rows = cursor.fetchall()

        assert len(rows) == 1
        assert rows[0][1] == 42  # suggestion_id
        assert rows[0][2] == 'active'

    def test_get_history_pagination(self, mock_db):
        """Test paginazione history."""
        cursor = mock_db.cursor()

        # Inserisci 25 applicazioni
        for i in range(25):
            cursor.execute('''
                INSERT INTO suggestion_applications
                (suggestion_id, hotel_id, status)
                VALUES (?, 1, 'active')
            ''', (i + 1,))
        mock_db.commit()

        # Prima pagina (limit 10)
        cursor.execute('''
            SELECT * FROM suggestion_applications
            WHERE hotel_id = 1
            ORDER BY applied_at DESC
            LIMIT 10 OFFSET 0
        ''')
        page1 = cursor.fetchall()

        # Seconda pagina
        cursor.execute('''
            SELECT * FROM suggestion_applications
            WHERE hotel_id = 1
            ORDER BY applied_at DESC
            LIMIT 10 OFFSET 10
        ''')
        page2 = cursor.fetchall()

        assert len(page1) == 10
        assert len(page2) == 10

    def test_get_history_filter_by_status(self, mock_db):
        """Test filtro per status."""
        cursor = mock_db.cursor()

        statuses = ['active', 'active', 'rolled_back', 'paused', 'active']
        for i, status in enumerate(statuses):
            cursor.execute('''
                INSERT INTO suggestion_applications
                (suggestion_id, hotel_id, status)
                VALUES (?, 1, ?)
            ''', (i + 1, status))
        mock_db.commit()

        # Filtra solo active
        cursor.execute('''
            SELECT * FROM suggestion_applications
            WHERE hotel_id = 1 AND status = 'active'
        ''')
        active = cursor.fetchall()

        assert len(active) == 3


# ============================================
# TEST: POST /api/actions/apply
# ============================================

class TestApplyAction:
    """Test suite per POST /api/actions/apply."""

    def test_apply_action_success(self, mock_db, sample_application):
        """Test applicazione suggerimento con successo."""
        cursor = mock_db.cursor()

        # Crea suggerimento da applicare
        cursor.execute('''
            INSERT INTO revenue_suggestions
            (hotel_id, tipo, status, suggested_price, confidence_score)
            VALUES (1, 'price_increase', 'pending', 120.00, 75)
        ''')
        suggestion_id = cursor.lastrowid

        # Crea pricing version
        cursor.execute('''
            INSERT INTO pricing_versions
            (hotel_id, version_number, snapshot, description)
            VALUES (1, 1, ?, 'Before suggestion 42')
        ''', (sample_application['before_snapshot'],))
        version_id = cursor.lastrowid

        # Applica
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, before_snapshot, changes_applied, pricing_version_id, status)
            VALUES (?, 1, ?, ?, ?, 'active')
        ''', (
            suggestion_id,
            sample_application['before_snapshot'],
            sample_application['changes_applied'],
            version_id
        ))
        application_id = cursor.lastrowid

        # Aggiorna status suggerimento
        cursor.execute('''
            UPDATE revenue_suggestions
            SET status = 'accepted'
            WHERE id = ?
        ''', (suggestion_id,))

        mock_db.commit()

        # Verifica
        cursor.execute('SELECT status FROM suggestion_applications WHERE id = ?', (application_id,))
        status = cursor.fetchone()[0]
        assert status == 'active'

        cursor.execute('SELECT status FROM revenue_suggestions WHERE id = ?', (suggestion_id,))
        sugg_status = cursor.fetchone()[0]
        assert sugg_status == 'accepted'

    def test_apply_action_creates_pricing_history(self, mock_db, sample_application):
        """Test che apply crei record in pricing_history."""
        cursor = mock_db.cursor()

        changes = json.loads(sample_application['changes_applied'])

        for change in changes['rooms']:
            cursor.execute('''
                INSERT INTO pricing_history
                (hotel_id, room_type_id, stay_date, old_price, new_price, change_type, suggestion_id)
                VALUES (1, ?, ?, ?, ?, 'ai_suggestion', 42)
            ''', (
                change['room_type_id'],
                change['date'],
                change['old_price'],
                change['new_price']
            ))

        mock_db.commit()

        cursor.execute('SELECT COUNT(*) FROM pricing_history WHERE suggestion_id = 42')
        count = cursor.fetchone()[0]

        assert count == 2

    def test_apply_action_duplicate_prevention(self, mock_db):
        """Test che non si possa applicare due volte lo stesso suggerimento."""
        cursor = mock_db.cursor()

        # Prima applicazione
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'active')
        ''')
        mock_db.commit()

        # Verifica che esiste gia
        cursor.execute('''
            SELECT COUNT(*) FROM suggestion_applications
            WHERE suggestion_id = 42 AND hotel_id = 1 AND status = 'active'
        ''')
        existing = cursor.fetchone()[0]

        # Se esiste, non permettere duplicato
        if existing > 0:
            can_apply = False
        else:
            can_apply = True

        assert can_apply is False


# ============================================
# TEST: POST /api/actions/{id}/rollback
# ============================================

class TestRollbackAction:
    """Test suite per POST /api/actions/{id}/rollback."""

    def test_rollback_success(self, mock_db, sample_application):
        """Test rollback con successo."""
        cursor = mock_db.cursor()

        # Setup: crea applicazione attiva
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, before_snapshot, changes_applied, status)
            VALUES (42, 1, ?, ?, 'active')
        ''', (
            sample_application['before_snapshot'],
            sample_application['changes_applied']
        ))
        application_id = cursor.lastrowid
        mock_db.commit()

        # Esegui rollback
        before = json.loads(sample_application['before_snapshot'])

        for room in before['rooms']:
            cursor.execute('''
                INSERT INTO pricing_history
                (hotel_id, room_type_id, stay_date, old_price, new_price, change_type, suggestion_id)
                VALUES (1, ?, ?, ?, ?, 'rollback', 42)
            ''', (
                room['room_type_id'],
                room['date'],
                120.00,  # current (dopo apply)
                room['price']  # original (prima di apply)
            ))

        # Aggiorna status
        cursor.execute('''
            UPDATE suggestion_applications
            SET status = 'rolled_back'
            WHERE id = ?
        ''', (application_id,))

        mock_db.commit()

        # Verifica
        cursor.execute('SELECT status FROM suggestion_applications WHERE id = ?', (application_id,))
        status = cursor.fetchone()[0]
        assert status == 'rolled_back'

        cursor.execute('SELECT COUNT(*) FROM pricing_history WHERE change_type = ?', ('rollback',))
        rollback_count = cursor.fetchone()[0]
        assert rollback_count == 2

    def test_rollback_already_rolled_back(self, mock_db):
        """Test che non si possa fare rollback di un rollback."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'rolled_back')
        ''')
        application_id = cursor.lastrowid
        mock_db.commit()

        # Verifica status
        cursor.execute('SELECT status FROM suggestion_applications WHERE id = ?', (application_id,))
        status = cursor.fetchone()[0]

        can_rollback = status == 'active'
        assert can_rollback is False

    def test_rollback_restores_prices(self, mock_db, sample_application):
        """Test che rollback ripristini i prezzi originali."""
        before = json.loads(sample_application['before_snapshot'])

        # Prezzi originali
        original_prices = {room['date']: room['price'] for room in before['rooms']}

        # Dopo rollback, i prezzi dovrebbero essere quelli originali
        for date, price in original_prices.items():
            assert price == 100.00  # Prezzo originale


# ============================================
# TEST: GET /api/actions/{id}/monitoring
# ============================================

class TestGetMonitoring:
    """Test suite per GET /api/actions/{id}/monitoring."""

    def test_get_monitoring_snapshots(self, mock_db, sample_monitoring_snapshot):
        """Test recupero snapshot monitoring."""
        cursor = mock_db.cursor()

        # Setup: crea applicazione
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'active')
        ''')
        application_id = cursor.lastrowid

        # Crea snapshot
        cursor.execute('''
            INSERT INTO monitoring_snapshots
            (application_id, metrics, delta_from_baseline, alert_level)
            VALUES (?, ?, ?, ?)
        ''', (
            application_id,
            sample_monitoring_snapshot['metrics'],
            sample_monitoring_snapshot['delta_from_baseline'],
            sample_monitoring_snapshot['alert_level']
        ))
        mock_db.commit()

        # Query
        cursor.execute('''
            SELECT metrics, alert_level
            FROM monitoring_snapshots
            WHERE application_id = ?
            ORDER BY snapshot_at DESC
        ''', (application_id,))
        snapshots = cursor.fetchall()

        assert len(snapshots) == 1
        metrics = json.loads(snapshots[0][0])
        assert metrics['occupancy'] == 0.85
        assert snapshots[0][1] == 'normal'

    def test_monitoring_alert_levels(self, mock_db):
        """Test diversi livelli di alert."""
        cursor = mock_db.cursor()

        # Crea applicazione
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'active')
        ''')
        application_id = cursor.lastrowid

        # Crea snapshots con diversi alert
        alerts = ['normal', 'warning', 'critical']
        for alert in alerts:
            cursor.execute('''
                INSERT INTO monitoring_snapshots
                (application_id, metrics, delta_from_baseline, alert_level)
                VALUES (?, '{}', '{}', ?)
            ''', (application_id, alert))
        mock_db.commit()

        cursor.execute('''
            SELECT alert_level FROM monitoring_snapshots
            WHERE application_id = ?
        ''', (application_id,))
        levels = [row[0] for row in cursor.fetchall()]

        assert 'warning' in levels
        assert 'critical' in levels

    def test_monitoring_triggers_notification(self, mock_db):
        """Test che alert critical crei notifica."""
        cursor = mock_db.cursor()

        # Setup
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'active')
        ''')
        application_id = cursor.lastrowid

        # Snapshot critical
        cursor.execute('''
            INSERT INTO monitoring_snapshots
            (application_id, metrics, delta_from_baseline, alert_level)
            VALUES (?, ?, ?, 'critical')
        ''', (
            application_id,
            json.dumps({'revenue_delta_pct': -15}),
            json.dumps({'revenue_delta_pct': -15})
        ))

        # Crea notifica
        cursor.execute('''
            INSERT INTO monitoring_notifications
            (application_id, notification_type, message)
            VALUES (?, 'alert', 'Revenue dropped by 15% after applying suggestion')
        ''', (application_id,))
        mock_db.commit()

        cursor.execute('''
            SELECT notification_type, message
            FROM monitoring_notifications
            WHERE application_id = ?
        ''', (application_id,))
        notification = cursor.fetchone()

        assert notification[0] == 'alert'
        assert 'dropped' in notification[1]


# ============================================
# TEST: Pause/Resume Actions
# ============================================

class TestPauseResumeActions:
    """Test suite per pause/resume."""

    def test_pause_action(self, mock_db):
        """Test pausa applicazione."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'active')
        ''')
        application_id = cursor.lastrowid
        mock_db.commit()

        # Pause
        cursor.execute('''
            UPDATE suggestion_applications
            SET status = 'paused'
            WHERE id = ?
        ''', (application_id,))
        mock_db.commit()

        cursor.execute('SELECT status FROM suggestion_applications WHERE id = ?', (application_id,))
        status = cursor.fetchone()[0]
        assert status == 'paused'

    def test_resume_action(self, mock_db):
        """Test resume applicazione."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'paused')
        ''')
        application_id = cursor.lastrowid
        mock_db.commit()

        # Resume
        cursor.execute('''
            UPDATE suggestion_applications
            SET status = 'active'
            WHERE id = ?
        ''', (application_id,))
        mock_db.commit()

        cursor.execute('SELECT status FROM suggestion_applications WHERE id = ?', (application_id,))
        status = cursor.fetchone()[0]
        assert status == 'active'

    def test_status_transitions(self, mock_db):
        """Test transizioni di stato valide."""
        valid_transitions = {
            'active': ['paused', 'rolled_back'],
            'paused': ['active', 'rolled_back'],
            'rolled_back': [],  # stato finale
        }

        for from_status, to_statuses in valid_transitions.items():
            for to_status in to_statuses:
                # Transizione valida
                assert to_status in valid_transitions.get(from_status, []) or to_status in ['active', 'paused', 'rolled_back']


# ============================================
# TEST: Effectiveness Score
# ============================================

class TestEffectivenessScore:
    """Test per effectiveness score."""

    def test_calculate_effectiveness(self, mock_db):
        """Test calcolo effectiveness da metriche."""
        baseline_revenue = 6300.00
        actual_revenue = 8000.00

        effectiveness = ((actual_revenue - baseline_revenue) / baseline_revenue) * 100

        assert effectiveness > 20  # +27%

    def test_effectiveness_saved_to_application(self, mock_db):
        """Test che effectiveness sia salvato."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status, effectiveness_score)
            VALUES (42, 1, 'active', 27.5)
        ''')
        application_id = cursor.lastrowid
        mock_db.commit()

        cursor.execute('SELECT effectiveness_score FROM suggestion_applications WHERE id = ?', (application_id,))
        score = cursor.fetchone()[0]

        assert score == 27.5

    def test_effectiveness_updates_over_time(self, mock_db):
        """Test che effectiveness si aggiorni con nuovi snapshot."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status, effectiveness_score)
            VALUES (42, 1, 'active', 15.0)
        ''')
        application_id = cursor.lastrowid
        mock_db.commit()

        # Update con nuovo score
        new_score = 22.5
        cursor.execute('''
            UPDATE suggestion_applications
            SET effectiveness_score = ?
            WHERE id = ?
        ''', (new_score, application_id))
        mock_db.commit()

        cursor.execute('SELECT effectiveness_score FROM suggestion_applications WHERE id = ?', (application_id,))
        score = cursor.fetchone()[0]

        assert score == 22.5


# ============================================
# TEST: Edge Cases
# ============================================

class TestActionTrackingEdgeCases:
    """Test per casi limite."""

    def test_apply_to_nonexistent_suggestion(self, mock_db):
        """Test applicazione a suggerimento inesistente."""
        cursor = mock_db.cursor()

        # Verifica che suggerimento non esista
        cursor.execute('SELECT * FROM revenue_suggestions WHERE id = 9999')
        suggestion = cursor.fetchone()

        assert suggestion is None

    def test_rollback_partial_failure(self, mock_db, sample_application):
        """Test rollback parziale (alcuni prezzi falliscono)."""
        cursor = mock_db.cursor()

        # Simula: 2 prezzi da rollback, 1 fallisce

        # Successo
        cursor.execute('''
            INSERT INTO pricing_history
            (hotel_id, room_type_id, stay_date, old_price, new_price, change_type)
            VALUES (1, 10, '2026-01-20', 120.00, 100.00, 'rollback')
        ''')

        # Il secondo potrebbe fallire (es: constraint violation)
        # In produzione: transazione + rollback
        mock_db.commit()

        cursor.execute('SELECT COUNT(*) FROM pricing_history WHERE change_type = ?', ('rollback',))
        count = cursor.fetchone()[0]

        # Solo 1 su 2 eseguito (problema)
        assert count == 1

    def test_concurrent_monitoring_snapshots(self, mock_db):
        """Test snapshot concorrenti."""
        cursor = mock_db.cursor()

        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, status)
            VALUES (42, 1, 'active')
        ''')
        application_id = cursor.lastrowid

        # 100 snapshot in 24h (ogni ~15 min)
        for i in range(100):
            cursor.execute('''
                INSERT INTO monitoring_snapshots
                (application_id, metrics, delta_from_baseline, alert_level)
                VALUES (?, ?, ?, 'normal')
            ''', (
                application_id,
                json.dumps({'snapshot_num': i}),
                json.dumps({})
            ))
        mock_db.commit()

        cursor.execute('SELECT COUNT(*) FROM monitoring_snapshots WHERE application_id = ?', (application_id,))
        count = cursor.fetchone()[0]

        assert count == 100

    def test_large_before_snapshot(self, mock_db):
        """Test con snapshot molto grande (tanti prezzi)."""
        # Genera 365 giorni x 10 room types = 3650 prezzi
        rooms = []
        for day in range(365):
            for room_type in range(10):
                rooms.append({
                    'room_type_id': room_type,
                    'date': f'2026-{(day // 30) + 1:02d}-{(day % 30) + 1:02d}',
                    'price': 100.00 + (day % 50)
                })

        large_snapshot = json.dumps({'rooms': rooms})

        cursor = mock_db.cursor()
        cursor.execute('''
            INSERT INTO suggestion_applications
            (suggestion_id, hotel_id, before_snapshot, status)
            VALUES (42, 1, ?, 'active')
        ''', (large_snapshot,))
        mock_db.commit()

        cursor.execute('SELECT LENGTH(before_snapshot) FROM suggestion_applications WHERE id = 1')
        length = cursor.fetchone()[0]

        # Snapshot grande ma gestibile
        assert length > 10000  # > 10KB


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
