# Weekly Retrospective - Modular Structure

**Version:** 2.1.0 (Refactored)
**Date:** 2026-02-04

## Struttura

```
scripts/memory/retro/
├── __init__.py         # Public exports
├── sections.py         # Data extraction (SQL queries)
├── output.py           # Rendering (rich/plain/markdown)
├── suggestions.py      # suggest_new_lessons()
├── cli.py              # CLI entry point + generate_retro()
└── README.md           # This file
```

## Moduli

### sections.py
Funzioni per estrarre dati dal database. **NO printing**, solo return.

- `fetch_metrics(conn, period_start)` → Dict[total, successes, failures, success_rate]
- `fetch_top_patterns(conn, limit=3)` → List[Dict[pattern_name, severity_level, occurrence_count]]
- `fetch_lessons(conn, period_start, limit=5)` → List[Dict[pattern, severity]]
- `fetch_agent_breakdown(conn, period_start, limit=5)` → List[Dict[agent_name, total, successes, failures, avg_duration]]
- `generate_recommendations(metrics, conn)` → List[str]
- `generate_next_steps(conn, metrics)` → List[str]

**Regole:**
- Ogni funzione < 50 righe
- Solo logica SQL + return
- Type hints sempre

### output.py
Funzioni per rendering multi-formato (rich/plain/markdown).

- `OutputMode` enum (RICH, PLAIN, MARKDOWN)
- `print_section_header(title, mode)`
- `print_table(data, columns, title, mode)`
- `print_panel(content, title, style, mode)`
- `print_metrics_table(metrics, mode)` - Helper specializzato

**Regole:**
- Gestisce HAS_RICH gracefully
- Ritorna `None` per RICH/PLAIN (stampa diretta)
- Ritorna `str` per MARKDOWN (accumula buffer)

### suggestions.py
Suggerimenti lezioni basate su pattern ripetuti.

- `suggest_new_lessons(conn, period_start)` → List[Tuple[tipo, valore, descrizione]]

### cli.py
Entry point CLI con main() e generate_retro().

- `generate_retro(days, save_to_file, quiet, output_dir)` - Funzione principale
- `save_report(content, output_dir)` - Salva markdown
- `main()` - Entry point CLI con argparse
- `_print_*_section()` - Helper di rendering (private)

## Uso

```python
# Import moduli
from scripts.memory.retro import generate_retro, suggest_new_lessons, save_report

# Genera retro
generate_retro(days=7, save_to_file=True, quiet=False)

# Suggerisci lezioni
from common.db import connect_db
conn = connect_db()
suggestions = suggest_new_lessons(conn, period_start="2026-01-01")
```

## CLI

```bash
# Report ultimi 7 giorni
python scripts/memory/retro/cli.py

# Report ultimi 14 giorni
python scripts/memory/retro/cli.py -d 14

# Salva report in markdown
python scripts/memory/retro/cli.py --save

# Modalità quiet (per cron)
python scripts/memory/retro/cli.py -s -q
```

## Prossimi Step

**Step 2:** Refactor generate_retro() per eliminare duplicazione
- Spostare _print_*_section() in output.py
- Ridurre cli.py a < 200 righe

**Step 3:** File legacy deprecati
- `weekly_retro.py` è stato rimosso
- Usare `python3 -m scripts.memory.retro.cli`
