# Test Report: scripts/common/paths.py

## Status
✅ **OK** - Coverage 95% raggiunto

## Test Completati
- 14 test totali
- 14 passati, 0 falliti
- Tempo esecuzione: 0.02s

## Coverage
**95%** (79 stmts, 4 missed)

### Linee NON coperte (accettabili)
- Lines 231-235: `__main__` block (OK - non testabile/non necessario)

### Linee COPERTE (da spec)
- ✅ Line 41: fallback in `_get_project_root()`
- ✅ Line 66: env var override in `get_agents_path()`
- ✅ Line 83: env var override in `get_data_dir()`
- ✅ Line 100: env var override in `get_db_path()`
- ✅ Lines 150-152: `ensure_data_dir()`
- ✅ Lines 162-164: `ensure_logs_dir()`
- ✅ Lines 179-184: `get_agent_file()` normalization
- ✅ Lines 194-203: `list_agents()` directory listing
- ✅ Lines 212-226: `print_paths()` debug output

## File Test
`tests/common/test_paths.py` (214 righe - sotto limite 250)

## Test Categories
1. **Project root detection** (2 test)
   - Con marker CLAUDE.md
   - Fallback senza marker

2. **Path getters con env override** (3 test)
   - `get_agents_path()` con CERVELLASWARM_AGENTS_PATH
   - `get_data_dir()` con CERVELLASWARM_DATA_DIR
   - `get_db_path()` con CERVELLASWARM_DB_PATH

3. **Directory creation** (2 test)
   - `ensure_data_dir()` crea directory
   - `ensure_logs_dir()` crea directory

4. **Agent file utilities** (3 test)
   - `get_agent_file()` - nome corto "frontend"
   - `get_agent_file()` - nome completo "cervella-frontend"
   - `get_agent_file()` - con estensione ".md"

5. **Agent listing** (2 test)
   - `list_agents()` - directory non esistente
   - `list_agents()` - directory popolata (filtra correttamente)

6. **Debug utilities** (1 test)
   - `print_paths()` - output senza errori

## Comando Esecuzione
```bash
python3 -m pytest tests/common/test_paths.py -v
```

## Note Tecniche
- Import corretto: `from scripts.common.paths import ...` (no shadowing)
- NO `__init__.py` in tests/common/
- Usa `tmp_path` fixture per filesystem tests
- Usa `monkeypatch` per env vars e `__file__` mock
- Usa `capsys` per testing print output

## Gap Accettabili
Solo `__main__` block (standard pattern - eseguito manualmente se necessario)
