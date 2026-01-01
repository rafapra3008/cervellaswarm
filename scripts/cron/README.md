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
0 18 * * 5 cd /Users/rafapra/Developer/CervellaSwarm && python3 scripts/memory/weekly_retro.py --save --quiet >> /Users/rafapra/Developer/CervellaSwarm/data/logs/weekly_retro.log 2>&1
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
0 9 * * 1 cd /path && python3 scripts/memory/weekly_retro.py --save --quiet

# Daily retro (ogni giorno alle 23:00)
0 23 * * * cd /path && python3 scripts/memory/weekly_retro.py -d 1 --save --quiet

# Monthly retro (primo del mese alle 10:00)
0 10 1 * * cd /path && python3 scripts/memory/weekly_retro.py -d 30 --save --quiet
```

---

## 📝 Test Manuale

Prima di abilitare il cron, testa il comando:

```bash
cd ~/Developer/CervellaSwarm
python3 scripts/memory/weekly_retro.py --save --quiet
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

**Created:** 2026-01-01
**Last Updated:** 2026-01-01
**Version:** 1.0.0
