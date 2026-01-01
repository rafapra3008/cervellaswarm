#!/usr/bin/env python3
"""
Test salvataggio nel database.
Crea una lezione fittizia e verifica che venga salvata correttamente.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from wizard import LessonWizard, get_db_path

import sqlite3

def test_db_save():
    """Test salvataggio nel database."""
    print("🧪 Test salvataggio database...")
    print("-" * 60)

    # Crea wizard
    wizard = LessonWizard()

    # Popola con dati di test
    wizard.lesson.update({
        "trigger": "TEST: Quando si testa il wizard",
        "context": "TEST: Testing del learning wizard",
        "problem": "TEST: Verifica che il salvataggio funzioni",
        "root_cause": "TEST: Necessità di verificare DB",
        "solution": "TEST: Creare test automatico",
        "prevention": "TEST: Sempre testare prima di usare",
        "example": "TEST: Questo è un esempio",
        "severity": "LOW",
        "agents_involved": ["cervella-tester", "cervella-backend"],
        "tags": ["test", "wizard", "db"],
        "pattern": "test-wizard-db"
    })

    # Mostra dati
    print("\n📋 Dati lezione:")
    print(f"   ID: {wizard.lesson['id']}")
    print(f"   Pattern: {wizard.lesson['pattern']}")
    print(f"   Severity: {wizard.lesson['severity']}")
    print(f"   Agents: {', '.join(wizard.lesson['agents_involved'])}")

    # Salva
    print("\n💾 Tentativo salvataggio...")
    success = wizard.save_to_db()

    if success:
        print("   ✅ Salvataggio riuscito!")

        # Verifica che sia salvato
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM lessons_learned WHERE id = ?",
            (wizard.lesson['id'],)
        )
        row = cursor.fetchone()

        if row:
            print("   ✅ Lezione trovata nel database!")
            print(f"   ✅ Timestamp: {row[1]}")
            print(f"   ✅ Pattern: {row[12]}")

            # Cleanup - rimuovi test
            cursor.execute(
                "DELETE FROM lessons_learned WHERE id = ?",
                (wizard.lesson['id'],)
            )
            conn.commit()
            print("   🧹 Test lesson rimossa (cleanup)")
        else:
            print("   ❌ Lezione NON trovata nel database!")
            success = False

        conn.close()

    else:
        print("   ❌ Salvataggio fallito!")

    return success

def main():
    """Entry point."""
    print("="*60)
    print("🧙 TEST DB SAVE - WIZARD.PY")
    print("="*60)

    try:
        db_path = get_db_path()
        print(f"\n📂 Database: {db_path}")

        if not db_path.exists():
            print("   ⚠️  Database non esiste! Esegui prima init_db.py")
            return 1

        success = test_db_save()

        print("\n" + "="*60)
        if success:
            print("🎉 TEST PASSATO!")
            print("="*60)
            return 0
        else:
            print("❌ TEST FALLITO!")
            print("="*60)
            return 1

    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
