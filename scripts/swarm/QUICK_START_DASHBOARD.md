# Dashboard - Quick Start

## 5-Second Start

```bash
cd scripts/swarm/
./dashboard.sh
```

## Watch Mode (Monitoring Continuo)

```bash
./dashboard.sh --watch
```

Press `Ctrl+C` to exit.

## Try the Demo

```bash
./demo_dashboard.sh
```

Crea task di esempio e mostra la dashboard in azione.

## Common Commands

```bash
# Snapshot singolo
./dashboard.sh

# Watch con intervallo personalizzato (5 secondi)
./dashboard.sh --watch --interval 5

# Export JSON
./dashboard.sh --json > snapshot.json

# Help
./dashboard.sh --help
```

## What You'll See

- **17 Workers** - Status di ogni worker (ACTIVE/READY/IDLE)
- **Task Queue** - Pending, In Progress, Completed
- **Metrics** - Stats generali
- **Last Activity** - Ultimi 5 eventi

## Integration Examples

```bash
# Check if swarm is active
if ./dashboard.sh --json | jq -e '.workers[] | select(.status == "active")' > /dev/null; then
    echo "Sciame attivo!"
fi

# Count active workers
./dashboard.sh --json | jq '[.workers[] | select(.status == "active")] | length'

# Export daily snapshot
./dashboard.sh --json > ~/logs/swarm_$(date +%Y%m%d).json
```

---

**Need more info?** See `README_DASHBOARD.md`
