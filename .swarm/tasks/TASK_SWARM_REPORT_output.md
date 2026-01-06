# Output: TASK_SWARM_REPORT

**Worker:** cervella-backend
**Completato:** 2026-01-06 03:53

---

## Cosa e' stato creato

### Script: swarm-report

**Posizione:** `~/.claude/scripts/swarm-report`

### Funzionalita

| Flag | Descrizione |
|------|-------------|
| (nessuno) | Report di oggi |
| `--week` | Report ultima settimana |
| `--all` | Tutti i task |
| `--json` | Output JSON |
| `--agent [tipo]` | Filtra per agente |
| `-h, --help` | Help |

### Uso

```bash
# Report di oggi
swarm-report

# Report ultima settimana
swarm-report --week

# Tutti i task
swarm-report --all

# Output JSON per integrazione
swarm-report --json

# Solo task di un agente specifico
swarm-report --agent cervella-backend
```

### Output

1. **Console**: Statistiche colorate + lista task
2. **File**: `.swarm/reports/report_YYYY-MM-DD.md`

### Esempio Output

```
+------------------------------------------------------------------+
|                      SWARM REPORT                                |
+------------------------------------------------------------------+

Periodo: Tutti i task

Task completati: 34
Task pending:    2
Task in corso:   2

=== TASK COMPLETATI ===

  TASK_SWARM_REPORT (cervella-backend)
  TASK_FIX_CONFIG (cervella-backend)
  ...

Report salvato: .swarm/reports/report_2026-01-06.md
```

---

*Completato con successo!*
