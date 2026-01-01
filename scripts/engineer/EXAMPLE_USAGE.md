# Esempio Uso: L'Ingegnera

## Scenario 1: Analisi Progetto Miracollo

```bash
# 1. Analizza
python3 scripts/engineer/analyze_codebase.py \
  ~/Developer/miracollogeminifocus \
  --output miracollo_engineering.md

# 2. Leggi report
cat miracollo_engineering.md
```

**Output Atteso:**
```markdown
# 🔧 ENGINEERING REPORT - 01/01/2026 19:00
## Progetto: /Users/rafapra/Developer/miracollogeminifocus

### 📊 Summary
- File analizzati: 156
- Righe totali: 45000
- Issues trovate: 89

### 🔴 CRITICO
#### File Enormi (> 1000 righe)
| File | Righe | Suggerimento |
|------|-------|-------------|
| components/Dashboard.jsx | 1247 | Split in componenti separati |

### 🟠 ALTO
#### File Grandi (> 500 righe)
| File | Righe | Suggerimento |
|------|-------|-------------|
| api/projects.py | 876 | Split in moduli separati |
| components/TaskList.jsx | 654 | Split in componenti separati |

### 💡 Raccomandazioni
1. [ ] CRITICO: Split 1 file enormi (>1000 righe)
2. [ ] Refactor 12 file grandi (>500 righe)
3. [ ] Split 34 funzioni grandi (>50 righe)
4. [ ] Risolvere 8 FIXME trovati
5. [ ] Completare o rimuovere 34 TODO
```

---

## Scenario 2: Prompt per Orchestratrice

**Input a cervella-orchestrator:**

```
Rafa: Analizza il progetto Miracollo e crea task di refactoring

Orchestratrice: 👑 Perfetto! Delego a L'Ingegnera:

@engineer analizza /Users/rafapra/Developer/miracollogeminifocus

[L'Ingegnera esegue analyze_codebase.py]

Risultati:
- 1 file CRITICO (>1000 righe)
- 12 file ALTO (>500 righe)
- 34 funzioni grandi
- 8 FIXME da risolvere

Consiglio:

1. PRIORITÀ 1: Split Dashboard.jsx (1247 righe)
   → Delego a @frontend:
   "Split Dashboard.jsx in:
   - DashboardHeader.jsx
   - DashboardStats.jsx
   - DashboardCharts.jsx
   - DashboardActivity.jsx"

2. PRIORITÀ 2: Refactor api/projects.py (876 righe)
   → Delego a @backend:
   "Split projects.py in:
   - projects/routes.py
   - projects/models.py
   - projects/service.py"

3. PRIORITÀ 3: Risolvere 8 FIXME
   → Delego a @tester:
   "Review e risolvi FIXME in:
   - auth.py:42
   - tasks.py:156
   ..."

Vuoi che procediamo?
```

---

## Scenario 3: Code Review Settimanale

**Workflow automatico ogni Lunedì/Venerdì:**

```bash
#!/bin/bash
# scripts/weekly-engineering-check.sh

PROJECT=$1
DATE=$(date +%Y-%m-%d)

echo "🔧 Engineering Check - $DATE"

# 1. Analizza
python3 scripts/engineer/analyze_codebase.py "$PROJECT" \
  --output "docs/reviews/$DATE-engineering.md"

# 2. Se issues CRITICHE → notifica
CRITICAL=$(grep -c "🔴 CRITICO" "docs/reviews/$DATE-engineering.md" || true)

if [ "$CRITICAL" -gt 0 ]; then
  echo "⚠️ ATTENZIONE: $CRITICAL issues CRITICHE trovate!"
  echo "Vedi: docs/reviews/$DATE-engineering.md"
fi

# 3. Crea branch per refactoring
git checkout -b "refactor/engineering-$DATE"

echo "✅ Report creato: docs/reviews/$DATE-engineering.md"
echo "📋 Branch creato: refactor/engineering-$DATE"
```

**Uso:**
```bash
./scripts/weekly-engineering-check.sh ~/Developer/miracollogeminifocus
```

---

## Scenario 4: Integrazione con Sprint

**Task Sprint 10.1b - Engineering Check:**

```markdown
## Sprint 10.1b - Engineering Audit
**Owner:** L'Ingegnera
**Effort:** 30 min

### Checklist
- [ ] Esegui analisi codebase
- [ ] Identifica file CRITICI (>1000 righe)
- [ ] Identifica FIXME urgenti
- [ ] Crea task refactoring prioritizzati
- [ ] Assegna task a specialisti giusti

### Command
```bash
python3 scripts/engineer/analyze_codebase.py . \
  --output docs/engineering/audit-$(date +%Y%m%d).md
```

### Output Atteso
- Report engineering audit
- Lista task prioritizzati
- Assignment specialisti
```

---

## Scenario 5: JSON per Automazione

**Genera JSON per processing automatico:**

```bash
# Genera JSON
python3 scripts/engineer/analyze_codebase.py . \
  --json --output /tmp/analysis.json

# Processa con jq
jq '.results.large_files[] | select(.lines > 1000)' /tmp/analysis.json

# Output:
{
  "file": "components/Dashboard.jsx",
  "lines": 1247,
  "suggestion": "Split in componenti separati"
}
```

**Script Automazione:**

```bash
#!/bin/bash
# create-refactoring-tasks.sh

# 1. Analizza
python3 scripts/engineer/analyze_codebase.py . --json --output /tmp/analysis.json

# 2. Estrai file critici
CRITICAL_FILES=$(jq -r '.results.large_files[] | select(.lines > 1000) | .file' /tmp/analysis.json)

# 3. Crea task per ogni file
for FILE in $CRITICAL_FILES; do
  echo "Creating task for: $FILE"
  # Qui potresti creare issue su GitHub, Jira, etc.
done
```

---

## Tips & Tricks

### 1. Focus su Specifico

```bash
# Solo file grandi
python3 scripts/engineer/analyze_codebase.py . | grep "File Grandi"

# Solo TODOs
python3 scripts/engineer/analyze_codebase.py . | grep -A 20 "TODO/FIXME"
```

### 2. Diff tra Analisi

```bash
# Analisi oggi
python3 scripts/engineer/analyze_codebase.py . \
  --output /tmp/today.md

# Confronta con settimana scorsa
diff docs/reviews/2025-12-25-engineering.md /tmp/today.md
```

### 3. Metriche nel Tempo

```bash
# Traccia evoluzione
echo "$(date +%Y-%m-%d),$(grep 'Issues trovate:' /tmp/today.md | grep -o '[0-9]*')" \
  >> metrics/engineering-trend.csv
```

---

**Creato da:** cervella-backend
**Data:** 1 Gennaio 2026
**Versione:** 1.0.0
