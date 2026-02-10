# Installazione LaunchAgents - CervellaSwarm

Guida rapida per installare gli automation jobs di CervellaSwarm.

---

## Jobs Disponibili

| Job | Frequenza | Orario | Cosa Fa |
|-----|-----------|--------|---------|
| **cleanup-logs** | Giornaliero | 3:00 AM | Archivia log swarm > 30 giorni |
| **archive-reports** | Settimanale (Domenica) | 4:00 AM | Archivia report > 7 giorni |

---

## Installazione Rapida

### 1. Cleanup Logs (Giornaliero 3:00)

```bash
# Copia plist
cp ~/Developer/CervellaSwarm/scripts/swarm/com.cervellaswarm.cleanup-logs.plist.example \
   ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist

# Carica agent
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist

# Verifica
launchctl list | grep cleanup-logs

# Test manuale (non aspettare domani!)
launchctl start com.cervellaswarm.cleanup-logs

# Controlla log
cat ~/Developer/CervellaSwarm/.swarm/logs/cleanup_launchd.log
```

### 2. Archive Reports (Domenica 4:00)

```bash
# Copia plist
cp ~/Developer/CervellaSwarm/scripts/swarm/com.cervellaswarm.archive-reports.plist.example \
   ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist

# Carica agent
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist

# Verifica
launchctl list | grep archive-reports

# Test manuale (non aspettare domenica!)
launchctl start com.cervellaswarm.archive-reports

# Controlla log
cat ~/Developer/CervellaSwarm/logs/archive_reports_launchd.log
```

---

## Comandi Utili

### Verifica tutti i jobs attivi

```bash
launchctl list | grep cervellaswarm
```

### Disinstallare un job

```bash
# Cleanup logs
launchctl unload ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
rm ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist

# Archive reports
launchctl unload ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
rm ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
```

### Ricaricare dopo modifiche

```bash
launchctl unload ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
```

### Test manuale script (senza launchd)

```bash
# Cleanup logs - dry-run
~/Developer/CervellaSwarm/scripts/swarm/cleanup-logs.sh

# Cleanup logs - esegui
~/Developer/CervellaSwarm/scripts/swarm/cleanup-logs.sh --execute

# Archive reports - dry-run
DRY_RUN=true ~/Developer/CervellaSwarm/scripts/archive_old_reports.sh

# Archive reports - esegui
~/Developer/CervellaSwarm/scripts/archive_old_reports.sh 7
```

---

## Log Files

| Job | Log Path |
|-----|----------|
| cleanup-logs | `.swarm/logs/cleanup_launchd.log` |
| cleanup-logs (errors) | `.swarm/logs/cleanup_launchd.err` |
| archive-reports | `logs/archive_reports_launchd.log` |
| archive-reports (errors) | `logs/archive_reports_launchd.err` |

---

## Troubleshooting

### Job non parte

```bash
# Verifica stato
launchctl list | grep com.cervellaswarm

# Deve mostrare PID (se in esecuzione) o "-" (se idle)
# Se NON appare: non caricato correttamente
```

### Verifica sintassi plist

```bash
plutil -lint ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
```

### Job parte ma fallisce

```bash
# Controlla error log
cat .swarm/logs/cleanup_launchd.err
cat logs/archive_reports_launchd.err
```

### Permessi script

```bash
# Assicurati che gli script siano eseguibili
chmod +x ~/Developer/CervellaSwarm/scripts/swarm/cleanup-logs.sh
chmod +x ~/Developer/CervellaSwarm/scripts/archive_old_reports.sh
```

---

## Jobs Esistenti (già installati)

| Job | File Plist |
|-----|------------|
| SNCP Daily | `~/Library/LaunchAgents/com.cervellaswarm.sncp.daily.plist` |
| SNCP Weekly | `~/Library/LaunchAgents/com.cervellaswarm.sncp.weekly.plist` |

**Tutti i jobs:** `ls -la ~/Library/LaunchAgents/com.cervellaswarm.*`

---

**Created:** 2026-02-10 (Sessione 327)
**Version:** 1.0.0
