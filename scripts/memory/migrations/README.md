# Database Migrations

Questa directory contiene le migration del database SQLite di CervellaSwarm.

## Struttura

```
migrations/
├── README.md                    # Questo file
├── 001_initial.sql              # Schema base (swarm_events + lessons_learned)
├── 002_lessons_learned.sql      # Estensione lessons_learned (15 colonne)
└── 003_error_patterns.sql       # Tabella error_patterns
```

## Naming Convention

I file SQL seguono il formato:

```
{numero}_{descrizione}.sql
```

Dove:
- `numero`: Versione a 3 cifre (es: 001, 002, 003)
- `descrizione`: Breve descrizione della migration (snake_case)

## Come Usare

### Verificare lo stato

```bash
python scripts/memory/migrate.py --status
```

Output esempio:
```
Current version: 0
Latest version: 3
Status: 3 migration(s) available
```

### Preview delle migration

```bash
python scripts/memory/migrate.py --dry-run
```

Mostra cosa verrebbe applicato senza eseguire.

### Applicare migration

```bash
python scripts/memory/migrate.py --upgrade
```

Applica tutte le migration mancanti in ordine.

### Rollback (limitato)

```bash
python scripts/memory/migrate.py --rollback
```

**ATTENZIONE:** Questo comando rimuove solo il record da `schema_version`, ma **NON annulla** le modifiche al database (SQLite non supporta DROP COLUMN).

## Aggiungere una Nuova Migration

1. Crea un nuovo file SQL con numero incrementale:

```bash
touch scripts/memory/migrations/004_my_feature.sql
```

2. Scrivi le istruzioni SQL (solo DDL - CREATE/ALTER):

```sql
-- Migration 004: My Feature
-- Descrizione dettagliata
-- Data: 2026-01-XX

ALTER TABLE swarm_events ADD COLUMN my_new_column TEXT;

CREATE INDEX IF NOT EXISTS idx_my_new_column
ON swarm_events(my_new_column);
```

3. Applica la migration:

```bash
python scripts/memory/migrate.py --upgrade
```

## Schema Versioning

Il sistema usa una tabella `schema_version` per tracciare le migration applicate:

```sql
CREATE TABLE schema_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version INTEGER NOT NULL,
    applied_at TEXT NOT NULL,
    migration_file TEXT NOT NULL,
    description TEXT
);
```

## Best Practices

1. **Mai modificare migration già applicate** - Crea sempre una nuova migration
2. **Testa localmente** - Usa `--dry-run` prima di applicare
3. **Backup** - Fai backup del database prima di migration importanti
4. **Idempotenza** - Usa sempre `IF NOT EXISTS` / `IF EXISTS`
5. **Atomicità** - Ogni migration deve essere completa e indipendente

## Environment Variables

Override dei path (per testing/packaging):

```bash
# Override path database
export CERVELLASWARM_DB_PATH=/custom/path/swarm_memory.db

# Override directory dati
export CERVELLASWARM_DATA_DIR=/custom/data/
```

## Note Tecniche

- Il database usa **WAL mode** per performance
- Le migration vengono applicate in una **transazione**
- Se una migration fallisce, viene fatto **rollback automatico**
- Il versioning è basato sul **numero nel nome file**, non sull'ordine alfabetico

---

*Versione: 1.0.0*
*Data: 2 Gennaio 2026*
