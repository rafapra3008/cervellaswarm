# Task: Creare swarm-report Centralizzato

**Assegnato a:** cervella-backend
**Priorita:** MEDIA
**Stato:** ready

---

## Obiettivo

Creare comando `swarm-report` che genera report giornaliero di TUTTI i task completati.

## Problema Attuale

- Output sparsi in tanti file _output.md
- Difficile trovare cosa e' stato fatto
- Nessuna vista aggregata

## Soluzione

Comando che:
1. Scansiona .swarm/tasks/*.done
2. Legge tutti i _output.md
3. Genera report aggregato
4. Mostra statistiche

## Implementazione

### Script swarm-report

Crea in `~/.claude/scripts/swarm-report`:

```bash
#!/bin/bash
#
# swarm-report - Report centralizzato task completati
#
# Uso:
#   swarm-report           # Report di oggi
#   swarm-report --week    # Report ultima settimana
#   swarm-report --all     # Tutti i task

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directory
TASKS_DIR=".swarm/tasks"
REPORT_DIR=".swarm/reports"

# Crea report dir se non esiste
mkdir -p "$REPORT_DIR"

# Data
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/report_${TODAY}.md"

echo -e "${BLUE}=== SWARM REPORT ===${NC}"
echo ""

# Conta task
TOTAL_DONE=$(find "$TASKS_DIR" -name "*.done" 2>/dev/null | wc -l | tr -d ' ')
TOTAL_PENDING=$(find "$TASKS_DIR" -name "*.ready" 2>/dev/null | wc -l | tr -d ' ')

echo -e "${GREEN}Task completati:${NC} $TOTAL_DONE"
echo -e "${YELLOW}Task pending:${NC} $TOTAL_PENDING"
echo ""

# Genera report markdown
cat > "$REPORT_FILE" << EOF
# Swarm Report - $TODAY

## Statistiche

| Metrica | Valore |
|---------|--------|
| Task completati | $TOTAL_DONE |
| Task pending | $TOTAL_PENDING |

## Task Completati

EOF

# Lista task completati
for done_file in "$TASKS_DIR"/*.done; do
    [ -f "$done_file" ] || continue

    task_name=$(basename "$done_file" .done)
    output_file="$TASKS_DIR/${task_name}_output.md"

    echo "### $task_name" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    if [ -f "$output_file" ]; then
        # Estrai prime 10 righe di output
        echo '```' >> "$REPORT_FILE"
        head -20 "$output_file" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    else
        echo "_Nessun output trovato_" >> "$REPORT_FILE"
    fi

    echo "" >> "$REPORT_FILE"
done

echo "---" >> "$REPORT_FILE"
echo "*Report generato: $(date)*" >> "$REPORT_FILE"

echo -e "${GREEN}Report salvato:${NC} $REPORT_FILE"
echo ""

# Mostra anteprima
echo "=== ANTEPRIMA ==="
head -50 "$REPORT_FILE"
```

### Funzionalita Aggiuntive

1. **--week**: Filtra per ultima settimana
2. **--project [nome]**: Filtra per progetto
3. **--agent [tipo]**: Filtra per tipo agente
4. **--json**: Output in JSON per integrazione

### Esempio Output

```
=== SWARM REPORT ===

Task completati: 15
Task pending: 3

=== ANTEPRIMA ===
# Swarm Report - 2026-01-06

## Statistiche
| Metrica | Valore |
|---------|--------|
| Task completati | 15 |
| Task pending | 3 |

## Task Completati

### TASK_GOLD_BACKEND
```
Output del task backend...
```

### TASK_GOLD_FRONTEND
```
Output del task frontend...
```
```

## Output Atteso

1. Script `swarm-report` in ~/.claude/scripts/
2. Chmod +x e link in PATH
3. Funziona con flag --week, --all
4. Genera file .md in .swarm/reports/
5. Documentazione uso

## Bonus

Aggiungere opzione `--html` che genera pagina HTML bella da vedere.

---

*"Visibilita totale = controllo totale!"*
