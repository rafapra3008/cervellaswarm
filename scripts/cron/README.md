# CervellaSwarm Cron Jobs

Automazione di task ricorrenti per il sistema di memoria collettiva.

---

## 📅 Weekly Retrospective

Report settimanale automatico con analisi metriche e suggerimenti.

### Setup Cron

```bash
# Apri crontab
crontab -e

# Aggiungi questa riga (venerdì alle 18:00)
0 18 * * 5 cd $HOME/Developer/CervellaSwarm && python3 -m scripts.memory.retro.cli --save --quiet >> $HOME/Developer/CervellaSwarm/data/logs/weekly_retro.log 2>&1
```

### Verifica Cron Attivi

```bash
# Lista cron jobs attivi
crontab -l

# Verifica logs
tail -f ~/Developer/CervellaSwarm/data/logs/weekly_retro.log
```

### Schedule Alternative

```bash
# Ogni lunedì alle 9:00
0 9 * * 1 cd /path && python3 -m scripts.memory.retro.cli --save --quiet

# Daily retro (ogni giorno alle 23:00)
0 23 * * * cd /path && python3 -m scripts.memory.retro.cli -d 1 --save --quiet

# Monthly retro (primo del mese alle 10:00)
0 10 1 * * cd /path && python3 -m scripts.memory.retro.cli -d 30 --save --quiet
```

---

## 📝 Test Manuale

Prima di abilitare il cron, testa il comando:

```bash
cd ~/Developer/CervellaSwarm
python3 -m scripts.memory.retro.cli --save --quiet
```

Verifica che il report sia stato creato in `data/retro/YYYY-MM-DD.md`.

---

## 📂 File Generati

```
data/
├── retro/
│   ├── 2026-01-01.md          # Report settimanali
│   ├── 2026-01-08.md
│   └── ...
└── logs/
    └── weekly_retro.log       # Logs cron execution
```

---

---

## SNCP Maintenance (Sessione 209)

### Daily Maintenance

Health check automatico + cleanup file temporanei.

```bash
# Ogni giorno alle 8:30
30 8 * * * $HOME/Developer/CervellaSwarm/scripts/cron/sncp_daily_maintenance.sh
```

**Cosa fa:**
- Esegue health-check.sh e salva report
- Pulisce file temporanei (.DS_Store, *.bak)
- Verifica dimensioni file (warning se > 300 righe)
- Genera statistiche SNCP

**Test manuale:**
```bash
$HOME/Developer/CervellaSwarm/scripts/cron/sncp_daily_maintenance.sh
```

### Weekly Archive

Archivia file vecchi (> 30 giorni) per mantenere SNCP pulito.

```bash
# Ogni Lunedi alle 6:00
0 6 * * 1 $HOME/Developer/CervellaSwarm/scripts/cron/sncp_weekly_archive.sh
```

**Cosa fa:**
- Archivia file da idee/, reports/, decisioni/
- Mantiene stato.md e roadmaps/ sempre attivi
- Pulisce archivi > 90 giorni
- Genera report settimanale

**Test manuale:**
```bash
$HOME/Developer/CervellaSwarm/scripts/cron/sncp_weekly_archive.sh
```

### LAUNCHD (Raccomandato - Nativo Apple)

Meglio di cron! Esegue anche quando apri il Mac.

```bash
# Verifica agents attivi
launchctl list | grep cervellaswarm

# Daily: AL LOGIN + ore 8:30
~/Library/LaunchAgents/com.cervellaswarm.sncp.daily.plist

# Weekly: Lunedi ore 6:00
~/Library/LaunchAgents/com.cervellaswarm.sncp.weekly.plist

# Cleanup logs: Ogni giorno ore 3:00
~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist

# Archive reports: Ogni domenica ore 4:00
~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist

# Ricaricare dopo modifiche
launchctl unload ~/Library/LaunchAgents/com.cervellaswarm.sncp.daily.plist
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.sncp.daily.plist
```

### Crontab (Alternativa)

```bash
# Copia e incolla tutto nel crontab (crontab -e)

# CervellaSwarm Weekly Retro - ogni lunedi alle 8:00
0 8 * * 1 $HOME/Developer/CervellaSwarm/scripts/cron/weekly_retro_cron.sh

# CervellaSwarm Log Rotation - ogni giorno alle 3:00
0 3 * * * $HOME/Developer/CervellaSwarm/scripts/cron/log_rotate_cron.sh

# SNCP Daily Maintenance - ogni giorno alle 8:30
30 8 * * * $HOME/Developer/CervellaSwarm/scripts/cron/sncp_daily_maintenance.sh

# SNCP Weekly Archive - ogni lunedi alle 6:00
0 6 * * 1 $HOME/Developer/CervellaSwarm/scripts/cron/sncp_weekly_archive.sh

# Cleanup swarm logs - ogni giorno alle 3:00
0 3 * * * cd $HOME/Developer/CervellaSwarm && ./scripts/swarm/cleanup-logs.sh --execute

# Archive old reports - ogni domenica alle 4:00
0 4 * * 0 cd $HOME/Developer/CervellaSwarm && ./scripts/archive_old_reports.sh 7
```

---

## Swarm Maintenance (Sessione 327)

### Cleanup Logs

Archivia automaticamente log swarm vecchi (> 30 giorni).

**LAUNCHD (Raccomandato):**
```bash
# Installa agent
cp scripts/swarm/com.cervellaswarm.cleanup-logs.plist.example \
   ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.cleanup-logs.plist

# Verifica
launchctl list | grep cleanup-logs

# Test manuale
launchctl start com.cervellaswarm.cleanup-logs

# Log
cat .swarm/logs/cleanup_launchd.log
```

**Cosa fa:**
- Ogni giorno alle 3:00
- Archivia log .swarm/logs/ > 30 giorni
- Archivia status .swarm/status/ > 30 giorni
- Log in .swarm/logs/cleanup_launchd.log

**Test manuale:**
```bash
./scripts/swarm/cleanup-logs.sh              # Dry-run
./scripts/swarm/cleanup-logs.sh --execute    # Esegui
```

### Archive Reports

Archivia automaticamente report vecchi (> 7 giorni).

**LAUNCHD (Raccomandato):**
```bash
# Installa agent
cp scripts/swarm/com.cervellaswarm.archive-reports.plist.example \
   ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist
launchctl load ~/Library/LaunchAgents/com.cervellaswarm.archive-reports.plist

# Verifica
launchctl list | grep archive-reports

# Test manuale
launchctl start com.cervellaswarm.archive-reports

# Log
cat logs/archive_reports_launchd.log
```

**Cosa fa:**
- Ogni domenica alle 4:00
- Archivia reports/ > 7 giorni
- Archivia .sncp/reports/ > 7 giorni
- Organizza per anno-mese

**Test manuale:**
```bash
./scripts/archive_old_reports.sh              # 7 giorni (default)
DRY_RUN=true ./scripts/archive_old_reports.sh # Test senza spostare
```

---

**Created:** 2026-01-01
**Last Updated:** 2026-02-10 (Sessione 327 - Swarm Maintenance)
**Version:** 2.1.0
