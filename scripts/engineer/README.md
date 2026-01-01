# 🔧 L'Ingegnera - Analisi Codebase Automatica

**Versione:** 1.0.0
**Data:** 1 Gennaio 2026

## Cosa Fa

L'Ingegnera analizza automaticamente una codebase e trova:

- 📏 **File Grandi** (> 500 righe)
- 🔍 **Funzioni Grandi** (> 50 righe)
- 📝 **TODO/FIXME Vecchi**
- 📋 **File Duplicati** (stesso contenuto)

E genera un report prioritizzato con suggerimenti di refactoring!

## Installazione

Nessuna installazione necessaria! Usa solo la libreria standard Python.

**Opzionale:** Installa `rich` per progress bar migliore:
```bash
pip install rich
```

## Uso Base

```bash
# Analizza progetto corrente
python3 scripts/engineer/analyze_codebase.py .

# Analizza altro progetto
python3 scripts/engineer/analyze_codebase.py /path/to/project

# Salva report in file
python3 scripts/engineer/analyze_codebase.py . --output report.md

# Output JSON invece di Markdown
python3 scripts/engineer/analyze_codebase.py . --json --output report.json
```

## Output

### Report Markdown

```markdown
# 🔧 ENGINEERING REPORT - 01/01/2026 18:56
## Progetto: /path/to/project

### 📊 Summary
- File analizzati: 80
- Righe totali: 23032
- Issues trovate: 51

### 🔴 CRITICO
File > 1000 righe

### 🟠 ALTO
File > 500 righe, funzioni > 50 righe

### 🟡 MEDIO
TODO/FIXME trovati

### 🟢 BASSO
File duplicati

### 💡 Raccomandazioni
1. [ ] Priorità 1: ...
2. [ ] Priorità 2: ...
```

### Report JSON

```json
{
  "timestamp": "01/01/2026 18:56",
  "project": "/path/to/project",
  "results": {
    "large_files": [...],
    "large_functions": [...],
    "todos": [...],
    "duplicates": [...],
    "stats": {
      "total_files": 80,
      "total_lines": 23032,
      "total_issues": 51
    }
  }
}
```

## Esempio Reale

Analisi di CervellaSwarm:

```bash
$ python3 scripts/engineer/analyze_codebase.py . --output engineering_report.md

🔧 L'Ingegnera - Analisi Codebase v1.0.0
📂 Progetto: .

🔍 Analizzo 80 file...

Analisi in corso... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

✅ Report salvato: engineering_report.md

📊 Analisi completata!
   File: 80
   Issues: 51
```

Risultato:
- 9 file grandi da splittare
- 41 funzioni grandi da refactorare
- 1 TODO da completare

## Esclusioni Automatiche

Lo script salta automaticamente:

**Directory:**
- `node_modules/`
- `.git/`
- `__pycache__/`
- `venv/`, `.venv/`
- `dist/`, `build/`
- `.next/`, `.nuxt/`
- `coverage/`

**File:**
- `*.min.js`, `*.min.css`
- `*.map`
- `package-lock.json`, `yarn.lock`

## Estensioni Analizzate

- Python: `.py`
- JavaScript/TypeScript: `.js`, `.jsx`, `.ts`, `.tsx`
- Markup: `.md`, `.html`
- Styles: `.css`

## Soglie

| Metrica | Soglia | Livello |
|---------|--------|---------|
| File enorme | > 1000 righe | 🔴 CRITICO |
| File grande | > 500 righe | 🟠 ALTO |
| Funzione grande | > 50 righe | 🟠 ALTO |
| TODO/FIXME | Tutti | 🟡 MEDIO |
| Duplicati | Tutti | 🟢 BASSO |

## Integrazione con Workflow

### Come L'Ingegnera

```bash
# 1. Analizza progetto
python3 scripts/engineer/analyze_codebase.py ~/Developer/MioProgetto \
  --output engineering_report.md

# 2. Leggi report
cat engineering_report.md

# 3. Crea task da raccomandazioni
# (manualmente o via script)
```

### In Code Review Settimanale

```bash
# Genera report pre-review
python3 scripts/engineer/analyze_codebase.py . \
  --output docs/reviews/$(date +%Y-%m-%d)-engineering.md

# Poi analizza con cervella-reviewer
```

## Limitazioni v1.0.0

- Analisi funzioni è approssimativa (non usa AST)
- Import non usati: solo Python, analisi base
- Non rileva code smells complessi
- Non misura complessità ciclomatica

## Roadmap Future

- [ ] Analisi AST completa (Python, JS)
- [ ] Complessità ciclomatica
- [ ] Code smells detection
- [ ] Metriche coverage
- [ ] Integrazione con git (file modificati recentemente)

## Versioning

```python
__version__ = "1.0.0"
__version_date__ = "2026-01-01"
```

---

**Creato da:** cervella-backend
**Per:** L'Ingegnera (FASE 10b)
**Progetto:** CervellaSwarm
