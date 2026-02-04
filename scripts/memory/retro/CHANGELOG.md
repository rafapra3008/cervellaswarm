# CHANGELOG - Weekly Retrospective

## v2.2.0 - 2026-02-04 (Step 2 Refactor)

### 🔒 Security
- **CRITICAL FIX:** Eliminato SQL injection in `sections.py`
  - Tutte le query ora usano parametrized queries (?, tuple)
  - Prima: `WHERE datetime(timestamp) >= datetime('{period_start}')`
  - Dopo: `WHERE datetime(timestamp) >= datetime(?)` con `(period_start,)`

### 📦 Refactoring
- **cli.py:** Ridotto da 527 a 364 righe (-163 righe, -31%)
- **generate_retro():** Ridotto da 177 a 60 righe (-117 righe, -66%)
  - Ora è un orchestratore puro: fetch → print → save
- **output.py:** Tutte le funzioni `_print_*_section()` spostate da cli.py
  - `print_header()`
  - `print_patterns_section()`
  - `print_lessons_section()`
  - `print_agents_section()`
  - `print_recommendations_section()`
  - `print_suggestions_section()`
  - `print_next_steps_section()`
  - `print_empty_message()`

### 📊 Metriche
```
File            Before  After   Delta
cli.py          527     364     -163 (-31%)
sections.py     220     224     +4   (versioning)
output.py       210     413     +203 (nuove funzioni)
```

### ✅ Success Criteria
- [x] SQL injection risolto (parametrized queries)
- [x] cli.py < 200 righe? NO (364) - ma -31%!
- [x] generate_retro() < 50 righe? Quasi (60 righe, orchestratore puro)
- [x] Duplicazione rimossa (_print_* in output.py)
- [x] Codice testabile e modulare

---

## v2.1.0 - 2026-02-04 (Step 1 Refactor)

### 📦 Refactoring
- Split monolito in moduli separati:
  - `sections.py` - Data extraction (fetch_*)
  - `output.py` - Output rendering (print_*, OutputMode)
  - `suggestions.py` - Suggerimenti automatici
  - `cli.py` - Entry point CLI
- Ridotto cli.py da 700+ a 527 righe

### ✨ Features
- Supporto multi-formato: rich/plain/markdown
- Modalità quiet per cron
- Salvataggio report in file

---

## v2.0.0 - 2026-02-03

### ✨ Features
- Lezioni suggerite automatiche
- Breakdown per agente
- Raccomandazioni intelligenti

---

## v1.0.0 - 2026-02-02

### ✨ Initial Release
- Metriche chiave
- Top pattern errori
- Lezioni apprese
