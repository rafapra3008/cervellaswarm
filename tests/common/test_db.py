#!/usr/bin/env python3
"""
Test suite for scripts/common/db.py
"""

import sqlite3
import pytest
from pathlib import Path
from unittest.mock import patch

# Import del modulo da testare (usa path completo per evitare conflitto
# con tests/common/ package)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.common.db import (
    connect_db,
    connect_db_safe,
    get_connection,
    DatabaseNotFoundError,
    DatabaseConnectionError,
)


class TestConnectDb:
    """Test per connect_db() - funzione principale"""

    def test_connect_db_success(self, tmp_path):
        """Testa connessione a database esistente"""
        # Arrange: Crea un database temporaneo
        db_path = tmp_path / "test_memory.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        # Act: Connettiti usando connect_db con path mockato
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            result = connect_db()

        # Assert
        assert result is not None
        assert isinstance(result, sqlite3.Connection)
        assert result.row_factory == sqlite3.Row  # Verifica Row factory

        # Verifica che possa eseguire query
        cursor = result.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert len(tables) > 0

        result.close()

    def test_connect_db_missing_database(self, tmp_path):
        """Testa errore quando database non esiste"""
        # Arrange: Path a database inesistente
        db_path = tmp_path / "nonexistent.db"

        # Act & Assert
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            with pytest.raises(DatabaseNotFoundError) as exc_info:
                connect_db()

        # Verifica messaggio errore
        error_msg = str(exc_info.value)
        assert "Database non trovato" in error_msg
        assert "init_db.py" in error_msg

    def test_connect_db_row_factory(self, tmp_path):
        """Verifica che Row factory permetta accesso per nome colonna"""
        # Arrange
        db_path = tmp_path / "test_memory.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Alice')")
        conn.commit()
        conn.close()

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            result = connect_db()

        # Assert: Accesso per nome colonna
        cursor = result.cursor()
        cursor.execute("SELECT * FROM users")
        row = cursor.fetchone()

        assert row["id"] == 1
        assert row["name"] == "Alice"

        result.close()

    def test_connect_db_invalid_db_file(self, tmp_path):
        """Testa che un file corrotto si connette ma fallisce alle query.

        SQLite non valida il file al connect - solo quando si eseguono query.
        """
        # Arrange: Crea file non-database
        db_path = tmp_path / "corrupt.db"
        db_path.write_text("This is not a database")

        # Act: La connessione riesce (SQLite e' lazy)
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            conn = connect_db()

        # Assert: Ma le query falliscono
        assert conn is not None
        with pytest.raises(sqlite3.DatabaseError):
            conn.execute("SELECT * FROM sqlite_master")
        conn.close()


class TestConnectDbSafe:
    """Test per connect_db_safe() - versione safe che ritorna None"""

    def test_connect_db_safe_success(self, tmp_path):
        """Testa che connect_db_safe ritorni connection quando database esiste"""
        # Arrange
        db_path = tmp_path / "test_memory.db"
        conn = sqlite3.connect(str(db_path))
        conn.close()

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            result = connect_db_safe()

        # Assert
        assert result is not None
        assert isinstance(result, sqlite3.Connection)
        result.close()

    def test_connect_db_safe_missing_database(self, tmp_path):
        """Testa che connect_db_safe ritorni None quando database manca"""
        # Arrange
        db_path = tmp_path / "nonexistent.db"

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            result = connect_db_safe()

        # Assert
        assert result is None

    def test_connect_db_safe_invalid_database(self, tmp_path):
        """Testa che connect_db_safe con file corrotto connette (SQLite lazy).

        SQLite non valida il file al connect. connect_db_safe ritorna
        una connection valida che fallira' solo alle query.
        """
        # Arrange
        db_path = tmp_path / "corrupt.db"
        db_path.write_text("Not a database")

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            result = connect_db_safe()

        # Assert: Connection esiste ma query falliscono
        assert result is not None
        with pytest.raises(sqlite3.DatabaseError):
            result.execute("SELECT 1")
        result.close()


class TestGetConnection:
    """Test per get_connection() - alias deprecato"""

    def test_get_connection_is_alias(self, tmp_path):
        """Verifica che get_connection sia un alias per connect_db"""
        # Arrange
        db_path = tmp_path / "test_memory.db"
        conn = sqlite3.connect(str(db_path))
        conn.close()

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            result = get_connection()

        # Assert
        assert result is not None
        assert isinstance(result, sqlite3.Connection)
        result.close()

    def test_get_connection_raises_same_errors(self, tmp_path):
        """Verifica che get_connection sollevi stessi errori di connect_db"""
        # Arrange
        db_path = tmp_path / "nonexistent.db"

        # Act & Assert
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            with pytest.raises(DatabaseNotFoundError):
                get_connection()


class TestEdgeCases:
    """Test per edge cases e situazioni particolari"""

    def test_multiple_connections_same_db(self, tmp_path):
        """Verifica che si possano aprire multiple connessioni"""
        # Arrange
        db_path = tmp_path / "test_memory.db"
        conn = sqlite3.connect(str(db_path))
        conn.close()

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            conn1 = connect_db()
            conn2 = connect_db()

        # Assert
        assert conn1 is not None
        assert conn2 is not None
        assert conn1 is not conn2  # Connessioni diverse

        conn1.close()
        conn2.close()

    def test_connection_after_close(self, tmp_path):
        """Verifica che si possa riconnettere dopo close"""
        # Arrange
        db_path = tmp_path / "test_memory.db"
        conn = sqlite3.connect(str(db_path))
        conn.close()

        # Act
        with patch("scripts.common.db.get_db_path", return_value=db_path):
            conn1 = connect_db()
            conn1.close()
            conn2 = connect_db()

        # Assert
        assert conn2 is not None
        conn2.close()
