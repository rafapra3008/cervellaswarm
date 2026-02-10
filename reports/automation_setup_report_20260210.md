# Automation Setup Report - CervellaSwarm
**Data:** 2026-02-10 (Sessione 327)
**DevOps:** Cervella DevOps

---

## Missione Completata ✅

Setup automazione per:
1. **Cleanup swarm logs** - giornaliero
2. **Archive old reports** - settimanale

---

## File Creati/Modificati

### Nuovi File

| File | Scopo |
|------|-------|
| `scripts/swarm/com.cervellaswarm.archive-reports.plist.example` | LaunchAgent per archive reports (domenica 4:00) |
| `scripts/swarm/INSTALL_LAUNCHD.md` | Guida installazione completa |
| `reports/automation_setup_report_20260210.md` | Questo report |

### File Modificati

| File | Modifica |
|------|----------|
| `scripts/swarm/com.cervellaswarm.cleanup-logs.plist.example` | Corretto schedule (era lunedì, ora giornaliero 3:00) |
| `scripts/cron/README.md` | Aggiunta sezione Swarm Maintenance (v2.1.0) |

---

## Configurazione

### Cleanup Logs
- **Frequenza:** Ogni giorno alle 3:00 AM
- **Script:** `scripts/swarm/cleanup-logs.sh --execute`
- **Retention:** 30 giorni
- **Log:** `.swarm/logs/cleanup_launchd.log`
- **Archivio:** `.swarm/archive/YYYY-MM/`

**Cosa fa:**
- Archivia log `.swarm/logs/` > 30 giorni
- Archivia status `.swarm/status/` > 30 giorni
- Mai delete, solo move

### Archive Reports
- **Frequenza:** Ogni domenica alle 4:00 AM
- **Script:** `scripts/archive_old_reports.sh 7`
- **Retention:** 7 giorni
- **Log:** `logs/archive_reports_launchd.log`
- **Archivio:** `reports/archive/YYYY-MM/` + `.sncp/reports/archive/YYYY-MM/`

**Cosa fa:**
- Archivia `reports/*.json|md|txt` > 7 giorni
- Archivia `.sncp/reports/*.json|md|txt` > 7 giorni
- Organizza per anno-mese

---

## Test Eseguiti

### Cleanup Logs
```bash
./scripts/swarm/cleanup-logs.sh
```
**Risultato:** ✅ OK
- 0 log vecchi trovati
- 11 status heartbeat > 30 giorni identificati
- Dry-run funziona correttamente

### Archive Reports
```bash
DRY_RUN=true ./scripts/archive_old_reports.sh
```
**Risultato:** ✅ OK
- 179 file in `reports/` > 7 giorni identificati
- 4 file in `.sncp/reports/` > 7 giorni identificati
- Dry-run funziona correttamente

### Sintassi plist
```bash
plutil -lint *.plist.example
```
**Risultato:** ✅ OK per entrambi i plist

---

## Come Installare

### 1. Cleanup Logs (RACCOMANDATO)

```bash
cp scripts/swarm/com.cervellaswarm.cleanup-logs.plist.example \
   ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
launchctl list | grep cleanup-logs
```

### 2. Archive Reports (RACCOMANDATO)

```bash
cp scripts/swarm/com.cervellaswarm.archive-reports.plist.example \
   ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
launchctl list | grep archive-reports
```

### Test Manuale (prima di installare)

```bash
# Test cleanup
launchctl start com.cervellaswarm.cleanup-logs
cat .swarm/logs/cleanup_launchd.log

# Test archive
launchctl start com.cervellaswarm.archive-reports
cat logs/archive_reports_launchd.log
```

---

## Documentazione

| Documento | Path |
|-----------|------|
| **Installazione LaunchAgents** | `scripts/swarm/INSTALL_LAUNCHD.md` |
| **Riferimento cron/launchd** | `scripts/cron/README.md` |
| **Cleanup logs README** | Inline in `scripts/swarm/cleanup-logs.sh --help` |
| **Archive reports README** | Header in `scripts/archive_old_reports.sh` |

---

## Pattern Usato

**LAUNCHD** (non crontab) - coerente con:
- `com.cervellaswarm.sncp.daily.plist` (già installato)
- `com.cervellaswarm.sncp.weekly.plist` (già installato)

**Motivo:** LaunchAgents Apple nativo, esegue anche al boot/login.

---

## Rollback

Se qualcosa va male:

```bash
# Disinstalla cleanup-logs
launchctl unload ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
rm ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist

# Disinstalla archive-reports
launchctl unload ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
rm ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
```

---

## Next Steps (opzionali)

Installare gli agents seguendo `scripts/swarm/INSTALL_LAUNCHD.md`.

**Raccomandazione:** Installare entrambi per mantenere repository pulito automaticamente.

---

**Status:** ✅ COMPLETATO
**Check:** Pre ✅ | Post ✅
**Rollback:** File example creati, nessuna installazione automatica
**Next:** Installazione manuale da parte di Rafa (se vuole)

---

*Report generato da Cervella DevOps*
*CervellaSwarm v2.1.0*
