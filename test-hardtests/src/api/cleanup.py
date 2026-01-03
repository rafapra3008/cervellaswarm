"""
Cleanup utilities for user management.

SAFETY FEATURES:
- DRY RUN mode by default (mai DELETE senza --execute)
- Interactive confirmation required (digita YES)
- Automatic backup before DELETE
- WHERE clause MANDATORY
- Limit 1000 records per execution
- Complete logging
"""

__version__ = "2.0.0"
__version_date__ = "2026-01-02"

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# SAFETY CONSTANTS
MAX_RECORDS_PER_RUN = 1000
CONFIRMATION_WORD = "YES"


class CleanupSafetyError(Exception):
    """Raised when safety checks fail."""
    pass


def _create_backup(db_path: str, records: List[Dict], backup_dir: str = "backups") -> str:
    """
    Crea backup dei record prima di eliminarli.

    Args:
        db_path: Path al database
        records: Record da backuppare
        backup_dir: Directory per i backup (default: "backups")

    Returns:
        str: Path del file di backup creato

    Raises:
        CleanupSafetyError: Se backup fallisce
    """
    try:
        # Crea directory backup se non esiste
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)

        # Nome file con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_name = Path(db_path).stem
        backup_file = backup_path / f"backup_{db_name}_{timestamp}.json"

        # Salva record in JSON
        backup_data = {
            "timestamp": timestamp,
            "database": db_path,
            "record_count": len(records),
            "records": records
        }

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Backup creato: {backup_file}")
        return str(backup_file)

    except Exception as e:
        raise CleanupSafetyError(f"ERRORE CRITICO: Impossibile creare backup: {e}")


def _validate_where_clause(where_clause: Optional[str]) -> None:
    """
    Valida che esista una WHERE clause.

    Args:
        where_clause: La clausola WHERE da validare

    Raises:
        CleanupSafetyError: Se WHERE clause manca o è troppo generica
    """
    if not where_clause or where_clause.strip() == "":
        raise CleanupSafetyError(
            "SAFETY CHECK FAILED: WHERE clause OBBLIGATORIA. "
            "Mai DELETE senza filtro!"
        )

    # Controlla se where_clause è troppo generica (es. "1=1")
    dangerous_patterns = ["1=1", "true", "1 = 1"]
    if any(pattern in where_clause.lower() for pattern in dangerous_patterns):
        raise CleanupSafetyError(
            f"SAFETY CHECK FAILED: WHERE clause troppo generica: '{where_clause}'"
        )


def _confirm_deletion(record_count: int) -> bool:
    """
    Richiede conferma interattiva prima di DELETE.

    Args:
        record_count: Numero di record da eliminare

    Returns:
        bool: True se utente conferma con YES, False altrimenti
    """
    print(f"\n{'='*60}")
    print(f"⚠️  ATTENZIONE: Stai per ELIMINARE {record_count} record")
    print(f"{'='*60}")
    print(f"Questa azione è IRREVERSIBILE!")
    print(f"Digita '{CONFIRMATION_WORD}' per confermare, qualsiasi altro input annulla.")
    print(f"{'='*60}\n")

    user_input = input(f"Conferma eliminazione [{CONFIRMATION_WORD}]: ").strip()

    if user_input == CONFIRMATION_WORD:
        logger.warning(f"✅ Utente ha confermato eliminazione di {record_count} record")
        return True
    else:
        logger.info(f"❌ Eliminazione ANNULLATA dall'utente (input: '{user_input}')")
        return False


def cleanup_old_records(
    db_path: str,
    days_inactive: int = 365,
    execute: bool = False,
    limit: int = MAX_RECORDS_PER_RUN,
    backup_dir: str = "backups"
) -> Dict:
    """
    Elimina record vecchi dal database con MASSIMA SICUREZZA.

    SAFETY FEATURES:
    - DRY RUN mode di DEFAULT (execute=False)
    - Conferma interattiva richiesta (digita YES)
    - Backup automatico prima di DELETE
    - WHERE clause OBBLIGATORIA
    - Limite 1000 record per esecuzione
    - Logging completo

    Args:
        db_path: Path al database SQLite
        days_inactive: Giorni di inattività per considerare record vecchio (default: 365)
        execute: Se True, esegue DELETE reale. DEFAULT: False (DRY RUN)
        limit: Max record per esecuzione (default: 1000)
        backup_dir: Directory per backup (default: "backups")

    Returns:
        dict: {
            "mode": "DRY_RUN" | "EXECUTED",
            "found_count": int,
            "deleted_count": int,
            "backup_file": str | None,
            "records": list[dict]
        }

    Raises:
        CleanupSafetyError: Se safety checks falliscono

    Examples:
        # DRY RUN (SICURO - default)
        result = cleanup_old_records("app.db")
        print(f"Trovati {result['found_count']} record da eliminare")

        # ESECUZIONE REALE (richiede --execute + conferma YES)
        result = cleanup_old_records("app.db", execute=True)
    """

    # SAFETY CHECK: Limite record
    if limit > MAX_RECORDS_PER_RUN:
        raise CleanupSafetyError(
            f"SAFETY CHECK FAILED: Limite {limit} supera massimo consentito "
            f"({MAX_RECORDS_PER_RUN})"
        )

    # Log mode
    mode = "EXECUTE" if execute else "DRY_RUN"
    logger.info(f"🔧 Cleanup avviato in modalità: {mode}")
    logger.info(f"📂 Database: {db_path}")
    logger.info(f"📅 Giorni inattività: {days_inactive}")
    logger.info(f"🔢 Limite record: {limit}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Calcola data cutoff
        cutoff_date = datetime.now() - timedelta(days=days_inactive)
        where_clause = f"last_login < '{cutoff_date.isoformat()}'"

        # SAFETY CHECK: Valida WHERE clause
        _validate_where_clause(where_clause)

        # Query con LIMIT per sicurezza
        query = f"""
            SELECT id, email, last_login
            FROM users
            WHERE {where_clause}
            LIMIT {limit}
        """

        logger.info(f"🔍 Query: {query}")
        cursor.execute(query)

        records_to_delete = cursor.fetchall()
        found_count = len(records_to_delete)

        # Prepara struttura records
        records = [
            {
                "id": rec[0],
                "email": rec[1],
                "last_login": rec[2]
            }
            for rec in records_to_delete
        ]

        logger.info(f"📊 Trovati {found_count} record che corrispondono ai criteri")

        # Se nessun record, esci
        if found_count == 0:
            logger.info("✅ Nessun record da eliminare")
            return {
                "mode": mode,
                "found_count": 0,
                "deleted_count": 0,
                "backup_file": None,
                "records": []
            }

        # DRY RUN mode (default)
        if not execute:
            logger.info(f"🔍 DRY RUN: Trovati {found_count} record che VERREBBERO eliminati")
            logger.info("ℹ️  Per eseguire eliminazione reale usa: execute=True")

            # Mostra sample dei record
            sample_size = min(5, found_count)
            logger.info(f"\n📋 Sample dei primi {sample_size} record:")
            for rec in records[:sample_size]:
                logger.info(f"  - ID: {rec['id']}, Email: {rec['email']}, "
                          f"Last Login: {rec['last_login']}")

            if found_count > sample_size:
                logger.info(f"  ... e altri {found_count - sample_size} record")

            return {
                "mode": "DRY_RUN",
                "found_count": found_count,
                "deleted_count": 0,
                "backup_file": None,
                "records": records
            }

        # EXECUTE mode - Richiede conferma
        logger.warning(f"⚠️  EXECUTE mode attivo - eliminazione REALE in corso")

        # SAFETY CHECK: Conferma interattiva
        if not _confirm_deletion(found_count):
            logger.info("❌ Eliminazione ANNULLATA dall'utente")
            return {
                "mode": "CANCELLED",
                "found_count": found_count,
                "deleted_count": 0,
                "backup_file": None,
                "records": records
            }

        # SAFETY CHECK: Crea backup PRIMA di DELETE
        logger.info("💾 Creazione backup...")
        backup_file = _create_backup(db_path, records, backup_dir)

        # Esegui DELETE
        logger.warning(f"🗑️  Eliminazione {found_count} record in corso...")

        # FIX: SQLite non supporta LIMIT in DELETE - usa WHERE IN con IDs
        ids_to_delete = [rec['id'] for rec in records]
        if ids_to_delete:
            placeholders = ','.join(['?' for _ in ids_to_delete])
            delete_query = f"DELETE FROM users WHERE id IN ({placeholders})"
            cursor.execute(delete_query, ids_to_delete)
            deleted_count = cursor.rowcount
            conn.commit()
        else:
            deleted_count = 0

        logger.info(f"✅ Eliminati {deleted_count} record con successo")
        logger.info(f"💾 Backup salvato in: {backup_file}")

        return {
            "mode": "EXECUTED",
            "found_count": found_count,
            "deleted_count": deleted_count,
            "backup_file": backup_file,
            "records": records
        }

    except CleanupSafetyError as e:
        # Safety check fallito - NON fare rollback, semplicemente esci
        logger.error(f"🛑 {str(e)}")
        raise

    except Exception as e:
        # Errore generico - Rollback
        conn.rollback()
        logger.error(f"❌ ERRORE durante cleanup: {str(e)}")
        raise Exception(f"Cleanup fallito: {str(e)}")

    finally:
        conn.close()


# Mantieni funzioni legacy per compatibilità
def get_inactive_users(db_path: str, days_inactive: int = 365):
    """
    DEPRECATED: Usa cleanup_old_records() in DRY RUN mode invece.

    Get users who haven't logged in for X days.
    """
    logger.warning(
        "⚠️  get_inactive_users() è DEPRECATED. "
        "Usa cleanup_old_records(execute=False) invece."
    )

    result = cleanup_old_records(db_path, days_inactive, execute=False)
    return [(r['id'], r['email'], r['last_login']) for r in result['records']]


def delete_inactive_users(db_path: str, days_inactive: int = 365, dry_run: bool = True) -> dict:
    """
    DEPRECATED: Usa cleanup_old_records() invece.

    Questa funzione mantiene la vecchia interfaccia ma usa il nuovo sistema sicuro.
    """
    logger.warning(
        "⚠️  delete_inactive_users() è DEPRECATED. "
        "Usa cleanup_old_records() invece."
    )

    # Converti dry_run al nuovo parametro execute
    execute = not dry_run

    result = cleanup_old_records(db_path, days_inactive, execute=execute)

    return {
        "deleted_count": result['deleted_count'],
        "deleted_users": result['records'],
        "dry_run": dry_run
    }
