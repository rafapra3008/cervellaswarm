# Test Report: impact_analyzer_cli.py

## Status
✅ **COMPLETATO**

## File Testato
`scripts/utils/impact_analyzer_cli.py` (85 lines, 60 statements)

## Test Suite
`tests/utils/test_impact_analyzer_cli.py` (300 lines, 15 tests)

## Risultati
- **Test**: 15 pass, 0 fail
- **Coverage**: 98% (59/60 statements)
- **Missing**: Line 85 (`if __name__ == "__main__"`) - **ACCETTABILE**

## Copertura Path

| Path | Test |
|------|------|
| Too few args (< 3) | ✅ test_too_few_args_no_args, test_too_few_args_one_arg |
| Happy path + result + callers > 0 | ✅ test_happy_path_with_result_and_callers |
| Happy path + result + callers == 0 | ✅ test_happy_path_with_result_no_callers |
| Happy path + callers > 10 | ✅ test_happy_path_with_many_callers |
| Symbol not found (None) | ✅ test_symbol_not_found |
| ValueError exception | ✅ test_value_error_exception |
| General Exception + traceback | ✅ test_general_exception |
| Logging configuration | ✅ test_logging_configuration |
| Analyzer initialization | ✅ test_analyzer_initialization |
| estimate_impact call | ✅ test_estimate_impact_called_correctly |
| find_callers call | ✅ test_find_callers_called_when_callers_exist |
| Risk level uppercase | ✅ test_risk_level_uppercase_conversion |
| Risk score formatting (2 decimals) | ✅ test_risk_score_formatting |
| Importance score formatting (6 decimals) | ✅ test_importance_score_formatting |

## Mock Strategy
- Mock `scripts.utils.impact_analyzer_cli.ImpactAnalyzer` (mock where USED)
- Mock `sys.argv` for CLI args
- Use `capsys` for output assertions
- `pytest.raises(SystemExit)` for exit code validation

## Integrazione
Test integra perfettamente con:
- `test_impact_analyzer_core.py` (38 tests)
- `test_impact_analyzer_analysis.py` (18 tests)
- **Totale**: 56 tests impact analyzer suite

## Run
```bash
pytest tests/utils/test_impact_analyzer_cli.py -v
pytest tests/utils/test_impact_analyzer_cli.py --cov=scripts.utils.impact_analyzer_cli --cov-report=term-missing
```

## Note
- Traceback stampato su stderr (non stdout) - gestito correttamente
- File limite 300 righe: **esattamente 300 righe**
- Tutti i path critici coperti (args, output formatting, exceptions, callers list)
