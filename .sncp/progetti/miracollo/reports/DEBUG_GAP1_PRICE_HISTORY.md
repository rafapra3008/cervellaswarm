# DEBUG GAP1: Price History Vuoto Dopo "Applica"

**Data**: 2026-01-11
**Investigator**: Cervella Backend
**Status**: 🔴 ROOT CAUSE IDENTIFIED

---

## EXECUTIVE SUMMARY

**PROBLEMA:**
Dopo che utente clicca "Applica" su suggerimento AI, Price History resta vuoto con messaggio "Nessun cambio prezzo negli ultimi 30 giorni", anche se i prezzi VENGONO effettivamente applicati.

**ROOT CAUSE:**
❌ **La tabella `pricing_history` NON ESISTE nel database!**

La migrazione `031_pricing_tracking.sql` è stata creata ma **MAI APPLICATA** al database `miracollo.db`.

---

## ANALISI DETTAGLIATA

### 1. CODICE È CORRETTO ✅

**File**: `backend/services/suggerimenti_actions.py`

Il codice chiama CORRETTAMENTE `log_price_change()` per ogni cambio prezzo:

```python
# Linea 221-244 - CODICE CORRETTO
try:
    pricing_history_id = log_price_change(
        conn=conn,
        hotel_id=hotel_id,
        room_type_id=update['room_type_id'],
        rate_plan_id=rate_plan_id,
        stay_date=update['date'],
        old_price=update['old_price'],
        new_price=update['new_price'],
        change_type='AI_APPLIED',
        changed_by='system',
        suggestion_id=suggestion_id,
        bucco_id=bucco_id,
        reason=f"AI suggestion: sconto {sconto_percent}%"
    )
    pricing_history_ids.append(...)
except Exception as e:
    logger.error(f"⚠️ Errore log price change tracking: {e}")
    # Non blocchiamo l'applicazione del prezzo per errore tracking
```

**File**: `backend/services/pricing_tracking_service.py`

La funzione `log_price_change()` esegue INSERT corretto:

```python
# Linea 69-83 - CODICE CORRETTO
cursor = conn.execute("""
    INSERT INTO pricing_history
    (hotel_id, room_type_id, rate_plan_id, stay_date,
     old_price, new_price, change_type,
     suggestion_id, bucco_id,
     changed_by, reason,
     occupancy_at_change, adr_at_change, days_to_arrival)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (...))
```

**File**: `backend/routers/pricing_tracking.py`

L'endpoint `/api/pricing/history` interroga correttamente:

```python
# Linea 102-128 - CODICE CORRETTO
query_parts = ["SELECT ph.*, rt.name as room_type_name"]
query_parts.append("FROM pricing_history ph")
query_parts.append("LEFT JOIN room_types rt ON ph.room_type_id = rt.id")
query_parts.append("WHERE ph.hotel_id = ?")
```

---

### 2. DATABASE MANCA TABELLA ❌

**Verifica attuale:**

```bash
sqlite3 miracollo.db ".tables" | grep pricing
# Output: pricing_versions (tabella DIVERSA!)
```

**Verifica migrazioni applicate:**

```sql
SELECT version, description FROM schema_version ORDER BY applied_at DESC LIMIT 1;
# Output: 1.7.0 | Action Tracking + Monitoring + Notifications (034, 035)
```

**Migrazione MANCANTE:**

```
File: backend/database/migrations/031_pricing_tracking.sql
Status: EXISTS ✅
Applied: NO ❌
```

La migrazione `031_pricing_tracking.sql` crea 3 tabelle:
1. `pricing_history` - Audit trail cambi prezzo
2. `suggestion_performance` - Metriche performance suggerimenti
3. `ai_model_health` - Salute modello AI

Nessuna di queste esiste nel database corrente!

---

### 3. CONSEGUENZE

1. **`log_price_change()` fallisce silenziosamente**
   - L'INSERT genera errore "table pricing_history not found"
   - Catch exception non blocca applicazione prezzo (by design)
   - Errore loggato ma non visibile all'utente

2. **Endpoint `/api/pricing/history` ritorna vuoto**
   - Query `FROM pricing_history` ritorna errore o 0 righe
   - Frontend mostra "Nessun cambio prezzo"

3. **Performance tracking NON funziona**
   - `start_performance_evaluation()` non può creare record
   - Metriche AI salute inaccessibili

---

## FIX PROPOSTO

### STEP 1: Applicare Migrazione 031

Creare script `apply_031_pricing_tracking.py`:

```python
#!/usr/bin/env python3
"""
Apply Migration 031 - Pricing Tracking System
==============================================
Applica tabelle pricing_history, suggestion_performance, ai_model_health.

Usage:
    python backend/database/apply_031_pricing_tracking.py
"""

import sqlite3
import os
import sys
from pathlib import Path

DB_PATH = "backend/database/miracollo.db"
MIGRATION_FILE = "backend/database/migrations/031_pricing_tracking.sql"

def apply_migration():
    """Applica migration 031."""
    print("=" * 60)
    print("APPLY MIGRATION 031 - Pricing Tracking System")
    print("=" * 60)

    # Verifica DB esiste
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return False

    # Verifica migration file esiste
    if not os.path.exists(MIGRATION_FILE):
        print(f"❌ Migration file not found: {MIGRATION_FILE}")
        return False

    # Connect DB
    print(f"\n1. Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se già applicata
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='pricing_history'
    """)
    if cursor.fetchone():
        print("   ⚠️ Table 'pricing_history' already exists!")
        print("   Migration already applied. Skipping.")
        conn.close()
        return True

    # Read migration SQL
    print(f"2. Reading {MIGRATION_FILE}...")
    with open(MIGRATION_FILE, 'r') as f:
        migration_sql = f.read()

    # Execute migration
    print("3. Executing migration...")
    try:
        cursor.executescript(migration_sql)
        conn.commit()
        print("   ✓ Migration executed successfully")
    except Exception as e:
        print(f"   ❌ Error executing migration: {e}")
        conn.rollback()
        conn.close()
        return False

    # Verify tabelle create
    print("\n4. Verifying tables...")
    expected_tables = ['pricing_history', 'suggestion_performance', 'ai_model_health']

    for table in expected_tables:
        cursor.execute(f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{table}'
        """)
        if cursor.fetchone():
            print(f"   ✓ Table '{table}' created")
        else:
            print(f"   ❌ Table '{table}' NOT found")
            conn.close()
            return False

    # Verify schema version
    print("\n5. Verifying schema version...")
    cursor.execute("""
        SELECT version FROM schema_version WHERE version='1.9.0'
    """)
    if cursor.fetchone():
        print("   ✓ Schema version 1.9.0 recorded")
    else:
        print("   ⚠️ Schema version 1.9.0 NOT found in schema_version")

    # Close
    conn.close()

    print("\n" + "=" * 60)
    print("✅ MIGRATION 031 APPLIED SUCCESSFULLY")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Test API: GET /api/pricing/history?hotel_code=NL")
    print("2. Apply AI suggestion and verify Price History populated")
    print("3. Verify Performance metrics tracked")

    return True


if __name__ == "__main__":
    success = apply_migration()
    sys.exit(0 if success else 1)
```

### STEP 2: Eseguire Migrazione

```bash
cd /Users/rafapra/Developer/miracollogeminifocus
python backend/database/apply_031_pricing_tracking.py
```

### STEP 3: Verificare Fix

**Test 1: Tabella esiste**
```bash
sqlite3 backend/database/miracollo.db "SELECT name FROM sqlite_master WHERE type='table' AND name='pricing_history'"
# Expected: pricing_history
```

**Test 2: Endpoint funziona**
```bash
curl "http://localhost:8000/api/pricing/history?hotel_code=NL"
# Expected: {"hotel_code": "NL", "total": 0, "timeline": []}
```

**Test 3: Applica suggerimento**
1. Vai su Revenue Intelligence → Suggerimenti
2. Clicca "Applica" su un suggerimento prezzo
3. Vai su Price History
4. **EXPECTED**: Vedere cambio prezzo registrato!

**Test 4: Verifica database**
```bash
sqlite3 backend/database/miracollo.db "SELECT * FROM pricing_history LIMIT 5"
# Expected: Record con change_type='AI_APPLIED'
```

---

## PERCHÉ È SUCCESSO?

1. **Migrazione creata ma non applicata**
   - File `031_pricing_tracking.sql` esiste da 10 Gennaio
   - Script `apply_017.py` applica migrazione 035 (più recente)
   - Migrazione 031 saltata per errore sequenza

2. **Code before schema**
   - Codice sviluppato assumendo tabella esistente
   - Database non aggiornato in sync
   - No test integration che verifichi schema

3. **Error handling silenzioso**
   - Catch exception in `suggerimenti_actions.py` (linea 242-244)
   - Errore loggato ma non bloccante
   - Utente non vede warning

---

## PREVENZIONE FUTURA

### 1. Checklist Pre-Deploy

**Prima di fare commit codice che usa nuove tabelle:**

- [ ] Migrazione SQL scritta
- [ ] Script apply_XXX.py creato
- [ ] Migrazione applicata a DB locale
- [ ] Test integration verificano tabella esiste
- [ ] README aggiornato con step migrazione

### 2. Test Integration

Aggiungere test che verifichi schema:

```python
# tests/test_pricing_tracking_schema.py
def test_pricing_history_table_exists():
    """Verifica che tabella pricing_history esista."""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='pricing_history'
        """)
        assert cursor.fetchone() is not None, "Table pricing_history not found!"
```

### 3. Migration Log

Aggiungere log esplicito quando tabella manca:

```python
# pricing_tracking_service.py, linea 94-96
except Exception as e:
    if "no such table: pricing_history" in str(e):
        logger.error("❌ CRITICAL: Table pricing_history does not exist!")
        logger.error("   Run: python backend/database/apply_031_pricing_tracking.py")
    logger.error(f"❌ Errore log price change: {e}")
    raise
```

---

## TIMELINE FIX

1. **Immediate** (5 min): Applicare migrazione 031
2. **Verify** (2 min): Test endpoint + apply suggestion
3. **Monitor** (ongoing): Check logs per errori simili

---

## FILES COINVOLTI

### Corretti (no modifica)
- `backend/services/suggerimenti_actions.py` - Linea 221-244 ✅
- `backend/services/pricing_tracking_service.py` - Linea 29-96 ✅
- `backend/routers/pricing_tracking.py` - Linea 73-171 ✅

### Da creare
- `backend/database/apply_031_pricing_tracking.py` - Script migrazione 🔧

### Da applicare
- `backend/database/migrations/031_pricing_tracking.sql` - Migrazione esistente ⏳

---

## CONCLUSIONE

**CAUSA ROOT**: Tabella `pricing_history` non esiste nel database.

**FIX**: Applicare migrazione `031_pricing_tracking.sql`.

**URGENZA**: 🔴 Alta - Feature Price History completamente non funzionante.

**EFFORT**: 5 minuti (applicare migrazione).

**RISK**: Basso - Migrazione idempotente, nessun dato esistente da modificare.

---

*Report generato da Cervella Backend - 11 Gennaio 2026*
