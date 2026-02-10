# Commands Package - Changelog

## v2.2.0 - 2026-02-04

### Created
- **dashboard.py**: Dashboard live con Rich (metriche settimana + top agent)
  - FIX: Query SQL parametrizzate per prevenire SQL injection
  - Sostituito f-string con `?` placeholder in tutte le query temporali

- **auto_detect.py**: Auto-rilevamento pattern errori
  - Import opzionale di pattern_detector
  - Supporto Rich per output tabellare
  - Fallback plain text se Rich non disponibile

- **retro.py**: Wrapper leggero per weekly retrospective
  - Riutilizza il modulo `scripts/memory/retro/`
  - Solo 43 righe (wrapper minimale)
  - Delega tutta la logica al modulo dedicato

- **__init__.py**: Package initialization
  - Esporta cmd_dashboard, cmd_auto_detect, cmd_retro

### Security
- **SQL Injection Fix**: Tutte le query in dashboard.py ora usano parametri (?, ?)
  - Prima: `f"... datetime('{week_ago}')"`
  - Dopo: `"... datetime(?)", (week_ago,)`

### Architecture
- Pattern: Command Pattern per modularità
- Ogni comando = 1 file = 1 responsabilità
- Import centralizzati da common.*
- Version tracking: __version__ = "2.2.0"
