# CHANGELOG - CervellaSwarm

Tutti i cambiamenti notevoli al sistema di memoria collettiva.

Il formato si basa su [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Email notifications per report settimanali
- Dashboard web per visualizzare metriche
- Export report in PDF

---

## [2.0.0] - 2026-01-01

### Added - weekly_retro.py
- **Lesson Suggestions**: Suggerisce automaticamente nuove lezioni basandosi su:
  - Pattern errori con count >= 3 senza lezione associata
  - Agenti con success rate < 80%
- **Save to File**: Salva report in markdown (`data/retro/YYYY-MM-DD.md`)
- **Quiet Mode**: Output minimale per cron jobs (`--quiet`)
- **Custom Output Directory**: Opzione `--output` per directory custom
- Nuova sezione "🎯 LEZIONI SUGGERITE" nel report
- File `scripts/cron/weekly_retro.cron` con configurazione cron
- File `scripts/cron/README.md` con guida setup

### Changed - weekly_retro.py
- CLI estesa con opzioni: `--save`, `--quiet`, `--output`
- Documentazione aggiornata con esempi v2.0.0
- `generate_retro()` ora supporta modalità file/quiet

### Technical
- Nuova funzione `suggest_new_lessons()`: analizza pattern e agenti
- Nuova funzione `save_report()`: salvataggio file markdown
- Dual output: Rich console + plain text markdown
- Type hints aggiunti per `Optional[Path]` e `List[Tuple]`

---

## [1.0.0] - 2026-01-01

### Added - Sistema Base
- Script `weekly_retro.py` con report settimanale
- Metriche chiave (eventi totali, success rate, errori)
- Top 3 pattern errori attivi
- Lezioni apprese nel periodo
- Breakdown per agente (top 5)
- Raccomandazioni automatiche
- Prossimi passi suggeriti
- Output colorato con Rich library

### Features
- Analisi periodo configurabile (`--days`)
- Connessione database `swarm_memory.db`
- Gestione errori graceful
- Version flag (`--version`)

---

## Schema Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (es. schema database cambiato)
MINOR: Nuove funzionalità backward-compatible (es. nuove opzioni CLI)
PATCH: Bug fixes backward-compatible
```

---

**Legend:**
- `Added`: Nuove funzionalità
- `Changed`: Modifiche a funzionalità esistenti
- `Deprecated`: Funzionalità deprecate (saranno rimosse)
- `Removed`: Funzionalità rimosse
- `Fixed`: Bug fixes
- `Security`: Fix di sicurezza
- `Technical`: Dettagli tecnici implementazione

---

*Ultimo aggiornamento: 2026-01-01*
*Formato: Keep a Changelog 1.0.0*
