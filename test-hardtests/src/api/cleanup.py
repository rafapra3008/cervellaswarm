"""
Cleanup utilities for user management.
"""
import sqlite3
from datetime import datetime, timedelta


def get_inactive_users(db_path: str, days_inactive: int = 365):
    """Get users who haven't logged in for X days."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cutoff_date = datetime.now() - timedelta(days=days_inactive)

    cursor.execute("""
        SELECT id, email, last_login
        FROM users
        WHERE last_login < ?
    """, (cutoff_date.isoformat(),))

    users = cursor.fetchall()
    conn.close()
    return users


def delete_inactive_users(db_path: str, days_inactive: int = 365, dry_run: bool = False) -> dict:
    """
    Elimina utenti che non hanno effettuato login da X giorni.

    Args:
        db_path: Path al database SQLite
        days_inactive: Numero di giorni di inattivita (default: 365)
        dry_run: Se True, simula l'operazione senza eliminare (default: False)

    Returns:
        dict: {
            "deleted_count": int,
            "deleted_users": list[dict],
            "dry_run": bool
        }

    Example:
        # Simulazione (sicura)
        result = delete_inactive_users("app.db", dry_run=True)

        # Eliminazione reale
        result = delete_inactive_users("app.db")
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Calcola data di cutoff
        cutoff_date = datetime.now() - timedelta(days=days_inactive)

        # Recupera utenti da eliminare (per log)
        cursor.execute("""
            SELECT id, email, last_login
            FROM users
            WHERE last_login < ?
        """, (cutoff_date.isoformat(),))

        users_to_delete = cursor.fetchall()
        deleted_users = [
            {
                "id": user[0],
                "email": user[1],
                "last_login": user[2]
            }
            for user in users_to_delete
        ]

        deleted_count = len(deleted_users)

        # Elimina solo se NON e dry_run
        if not dry_run and deleted_count > 0:
            cursor.execute("""
                DELETE FROM users
                WHERE last_login < ?
            """, (cutoff_date.isoformat(),))

            conn.commit()

        return {
            "deleted_count": deleted_count,
            "deleted_users": deleted_users,
            "dry_run": dry_run
        }

    except Exception as e:
        conn.rollback()
        raise Exception(f"Errore durante eliminazione utenti inattivi: {str(e)}")

    finally:
        conn.close()
