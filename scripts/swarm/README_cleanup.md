# Swarm Log Cleanup

**Script:** `cleanup-logs.sh`
**Versione:** 1.0.0
**Data:** 4 Febbraio 2026

---

## Scopo

Archivia automaticamente i log e status file vecchi per prevenire accumulo.

**Strategia:** Move (NON delete) in `.swarm/archive/YYYY-MM/`

---

## Uso

### Dry-run (default)

```bash
./cleanup-logs.sh
# Mostra cosa verrebbe archiviato

./cleanup-logs.sh --days 60
# Dry-run con retention personalizzata
```

### Esecuzione

```bash
./cleanup-logs.sh --execute
# Archivia file > 30 giorni

./cleanup-logs.sh --execute --days 7
# Archivia file > 7 giorni (aggressivo!)
```

### Help

```bash
./cleanup-logs.sh --help
```

---

## Cosa Archivia

| Directory | File Type | Note |
|-----------|-----------|------|
| `.swarm/logs/` | `*.log` | Worker logs, spawn logs |
| `.swarm/status/` | `heartbeat_*.log` | Heartbeat files |

**NON tocca:**
- `.swarm/tasks/` (outputs persistenti)
- `.swarm/plans/` (piani architect)
- `.swarm/outputs/` (risultati worker)

---

## Integrazione Cron

### Opzione 1: Weekly (raccomandato)

```bash
# Ogni lunedì alle 03:00
0 3 * * 1 cd /Users/rafapra/Developer/CervellaSwarm && ./scripts/swarm/cleanup-logs.sh --execute
```

### Opzione 2: Monthly

```bash
# Primo giorno del mese alle 02:00
0 2 1 * * cd /Users/rafapra/Developer/CervellaSwarm && ./scripts/swarm/cleanup-logs.sh --execute
```

### Installazione

```bash
# Aggiungi a crontab
crontab -e

# Oppure usa launchd (macOS)
# Copia cron/cleanup-logs.plist in ~/Library/LaunchAgents/
```

---

## Log Operazioni

Lo script registra ogni esecuzione in:

```
.swarm/logs/cleanup.log
```

Formato:
```
[2026-02-04 12:00:00] Archived 17 files (retention: 30 days)
```

---

## Sicurezza

- ✅ **NON cancella mai** (solo move)
- ✅ Preserva struttura temporale (YYYY-MM)
- ✅ Dry-run default (previene errori)
- ✅ Validation parametri
- ✅ Log operazioni

---

## Retention Raccomandato

| Use Case | Days | Motivo |
|----------|------|--------|
| Produzione | 30 | Permette retrospettive mensili |
| Development | 14 | Più aggressivo, OK per dev |
| Debug intenso | 60 | Mantiene storia lunga |

**Default: 30 giorni** (bilanciato)

---

## Recupero File Archiviati

```bash
# Trova un file archiviato
find .swarm/archive -name "spawn.log"

# Ripristina
cp .swarm/archive/2026-01/spawn.log .swarm/logs/

# Lista archivio mese
ls -lh .swarm/archive/2026-01/
```

---

## Testing

```bash
# 1. Dry-run normale
./cleanup-logs.sh

# 2. Dry-run aggressivo
./cleanup-logs.sh --days 1

# 3. Esecuzione reale (attenzione!)
./cleanup-logs.sh --execute --days 60

# 4. Verifica archivio
ls .swarm/archive/
```

---

## Performance

**Dimensioni tipiche:**
- Pre-cleanup: ~200KB (.swarm/logs + .swarm/status)
- Post-cleanup: ~50KB (solo file recenti)
- Archivio: ~150KB per mese

**Tempo esecuzione:** < 1 secondo

---

## Note

- Script testato con retention 15/30/60 giorni
- Funziona su macOS e Linux
- Non richiede privilegi speciali
- Safe da eseguire manualmente

---

*Per domande: Cervella Backend*
*Ultima revisione: 2026-02-04*
