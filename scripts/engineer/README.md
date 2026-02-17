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

## Hook Post-Commit (FASE 10c)

L'Ingegnera include un hook automatico che analizza la codebase dopo ogni commit!

### Setup Hook

Il hook è già configurato in `~/.claude/hooks/post_commit_engineer.py`.

Verifica configurazione in `.claude/settings.json`:
```json
{
  "hooks": {
    "PostCommit": "~/.claude/hooks/post_commit_engineer.py"
  }
}
```

### Cosa Fa l'Hook

1. ✅ Si attiva automaticamente dopo ogni `git commit`
2. 🔍 Esegue `analyze_codebase.py` in background
3. 📊 Salva report in `reports/engineer_report_*.json`
4. 🚨 Se trova issues CRITICHE/ALTE → segnala immediatamente

### Esempio Output Hook

```bash
$ git commit -m "Add new feature"
[main abc1234] Add new feature
 3 files changed, 150 insertions(+)

🔍 Analisi codebase in corso...
   Progetto: ~/Developer/my-project
   Report: reports/engineer_report_20260101_120000.json

============================================================
🚨 ENGINEERING ISSUES TROVATE!
============================================================

🔴 CRITICO: File enormi (>1000 righe)
   Count: 2
   Files:
   - src/app.py
   - src/models.py

🟠 ALTO: Funzioni grandi (>50 righe)
   Count: 15
   Files:
   - src/utils.py
   - src/handlers.py

============================================================
💡 Raccomandazione: Esegui code review e refactoring!
============================================================
```

## PR Automatiche (FASE 10c)

Script per creare Pull Request automatiche di refactoring!

### Uso Base

```bash
# Crea PR per refactor specifici file
python3 scripts/engineer/create_auto_pr.py \
  --files "src/app.py,src/utils.py" \
  --title "Split app.py in moduli" \
  --description "Refactor app.py e utils.py per ridurre complessità"

# Dry-run (no actual changes)
python3 scripts/engineer/create_auto_pr.py \
  --files "src/app.py" \
  --title "Test PR" \
  --description "Test creazione PR" \
  --dry-run

# Da configurazione JSON
python3 scripts/engineer/create_auto_pr.py \
  --from-json refactor-plan.json
```

### Formato JSON

```json
{
  "files": ["src/app.py", "src/utils.py"],
  "title": "Split app.py",
  "description": "Refactor app.py in moduli più piccoli",
  "modification_type": "split"
}
```

### Workflow Automatico

Lo script esegue:
1. ✅ Crea branch: `refactor/auto-YYYYMMDD_HHMMSS`
2. ✅ Modifica i file specificati
3. ✅ Crea commit con messaggio standard
4. ✅ Pusha branch su remote
5. ✅ Crea PR con GitHub CLI (`gh`)

### Prerequisiti

```bash
# Installa GitHub CLI
brew install gh

# Autentica
gh auth login
```

### Output

```bash
============================================================
🔧 AUTO PR CREATOR - L'Ingegnera
============================================================

📌 Creo branch: refactor/auto-20260101_120000
📝 Modifico 2 file (refactor)...
   - src/app.py
   - src/utils.py
✅ Modifiche completate!
💾 Creo commit...
✅ Commit creato!
🚀 Push branch su remote...
✅ Branch pushato!
📋 Creo Pull Request...
✅ PR creata: https://github.com/user/repo/pull/123

============================================================
✅ WORKFLOW COMPLETATO!
============================================================
Branch: refactor/auto-20260101_120000
PR URL: https://github.com/user/repo/pull/123
============================================================

🎉 PR URL: https://github.com/user/repo/pull/123
```

## Roadmap Future

- [ ] Analisi AST completa (Python, JS)
- [ ] Complessità ciclomatica
- [ ] Code smells detection
- [ ] Metriche coverage
- [x] ~~Integrazione con git (hook post-commit)~~ ✅ FASE 10c
- [x] ~~PR automatiche~~ ✅ FASE 10c

## Versioning

```python
__version__ = "1.0.0"
__version_date__ = "2026-01-01"
```

---

**Creato da:** cervella-backend
**Per:** L'Ingegnera (FASE 10b + 10c)
**Progetto:** CervellaSwarm
