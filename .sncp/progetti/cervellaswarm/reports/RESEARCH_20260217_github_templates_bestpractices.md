# .github/ Templates - Research & Piano Concreto
> **Data:** 2026-02-17 - Sessione 366
> **Ricercatore:** Cervella Researcher
> **Scopo:** F0.5 - .github/ templates per CervellaSwarm open source
> **Fonti:** 14 consultate (GitHub docs, CrewAI, LangGraph, Fiber, Codecov, shields.io)

---

## 1. VERDETTO PRINCIPALE: YAML vs Markdown per Issue Templates

**Usa YAML form-based (.yml). Sempre.**

### Perche YAML vince nel 2026

| Criterio | Markdown (.md) | YAML form (.yml) |
|----------|---------------|-----------------|
| UX contributor | Form libero (troppa variabilita) | Form strutturato con validazione |
| Campi obbligatori | Non applicabile | `required: true` funziona |
| Dropdown, checkboxes | No | Si (nativo) |
| Adozione big projects | Vecchio standard | CrewAI, LangGraph, tutti usano YAML |
| Blank issues disabilitabili | No | Si (config.yml) |

**Tutti e tre i competitor (CrewAI, LangGraph, Fiber) usano YAML.**
**config.yml con `blank_issues_enabled: false` disabilita le issue libere** -> costringe a usare i template.

---

## 2. ISSUE TEMPLATES - ANALISI COMPETITOR

### CrewAI (bug_report.yml) - Pattern migliore trovato

Campi raccolti:
- Descrizione bug
- Steps to reproduce
- Expected behavior
- Evidence (log, screenshot)
- OS (dropdown): Ubuntu 20.04-24.04, macOS, Windows, Other
- Python version (dropdown): 3.10, 3.11, 3.12
- CrewAI version (text)
- Virtual env type (dropdown): Venv, Conda, Poetry
- Screenshots/Code (optional)
- Possible solution (optional)
- Additional context (optional)

**Tutti i campi critici = `required: true`**

### LangGraph (bug-report.yml) - Pattern piu rigoroso

Approccio piu tecnico:
- Checklist pre-submit (7 checkbox obbligatorie): hai cercato su GitHub? Hai testato ultima versione? L'issue e nel codice di LangGraph, non nel tuo codice?
- Reproduction code (testo, non screenshot)
- Full error traceback
- System info: output di `python -m langchain_core.sys_info`

**Piu severo ma riduce drasticamente issue inutili.**

### Feature Request - Pattern CrewAI

- Feature Area (dropdown): Core functionality, Agent capabilities, Integration, Performance, Documentation, Other
- Bug relationship: link bug o "NA"
- Solution description (required)
- Contribution willingness (dropdown): "I will submit a PR" -> "Just suggesting"
- Alternatives (optional)
- Additional context (optional)

**Il campo "contribution willingness" e intelligente**: separa chi contribuisce da chi suggerisce.

---

## 3. PR TEMPLATE - ANALISI COMPETITOR

### LangGraph (PULL_REQUEST_TEMPLATE.md) - Formato consigliato

```
Title format: {TYPE}({SCOPE}): {DESCRIPTION}
Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
```

Checklist obbligatoria:
- [ ] Tests aggiunti/aggiornati
- [ ] `make format` passato
- [ ] `make lint` passato
- [ ] `make test` passato
- [ ] Documentazione aggiornata se necessario

**"We will not consider a PR unless these three are passing in CI."** - Esplicito e onesto.

### Fiber (pull_request_template.md) - Piu elaborato

Sezioni:
- Description (problema + soluzione + issues)
- Changes Introduced (checklist: performance, docs, changelog, migration guide)
- Type of Change (checkbox: feature, enhancement, docs, performance, consistency)
- Checklist pre-submit
- Commit formatting con emoji (overkill per CervellaSwarm)

---

## 4. GITHUB ACTIONS CI - ANALISI E RACCOMANDAZIONI

### Struttura CrewAI (11 workflow files)

```
.github/workflows/
├── tests.yml           # Test matrix Python 3.10-3.13
├── linter.yml          # Ruff/flake8
├── type-checker.yml    # mypy
├── codeql.yml          # Security scan
├── publish.yml         # PyPI release
├── stale.yml           # Auto-close stale issues
├── docs-broken-links.yml
├── build-uv-cache.yml
├── generate-tool-specs.yml
├── trigger-deployment-tests.yml
└── update-test-durations.yml
```

### Pattern tests.yml di CrewAI (da replicare)

Key points osservati:
- **Matrix: Python 3.10, 3.11, 3.12, 3.13**
- **Parallel test groups: 8 gruppi** (crewai ha suite larga)
- **Timeout per job: 15 minuti**
- **Fail-fast: true** (se un job fallisce, stop tutti)
- **Cache UV packages** con hash del lockfile
- **Read-only permissions** (best practice sicurezza)

### Trigger consigliati per CervellaSwarm

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Lunedi mezzanotte = settimana nuova
```

**NOTA:** Non triggerare su OGNI push a OGNI branch. Solo main + PR verso main.

### Matrix Python per CervellaSwarm

CervellaSwarm usa Python + TypeScript (monorepo). Raccomandazione:

```yaml
strategy:
  fail-fast: false  # false: vedi tutti i fallimenti, non solo il primo
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
    # 3.13: opzionale, aggiungilo quando stable per 6+ mesi
    os: [ubuntu-latest]  # Solo ubuntu: piu veloce, meno costo
    # Windows/macOS: aggiungi solo se il progetto li supporta esplicitamente
```

**Python 3.10 obbligatorio**: e il minimo dichiarato.
**3.13**: non ancora universalmente stabile su tutte le dipendenze (tree-sitter incluso). Aggiungi in F1.

### TypeScript nel monorepo

Per il package `@cervellaswarm/mcp-server`:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'  # LTS 2025-2026
    cache: 'npm'
    cache-dependency-path: packages/mcp-server/package-lock.json

- name: Install and test
  working-directory: packages/mcp-server
  run: |
    npm ci
    npm test
    npm run build
```

**Triggers per monorepo**: usa `paths:` filter per non runnare Python CI quando cambi solo TypeScript e viceversa.

---

## 5. BADGE DINAMICI - RACCOMANDAZIONE

### Opzione A: Codecov (consigliata per open source)

Pro:
- Free per progetti open source
- Badge dinamici automatici
- PR comments con coverage diff
- Integrazione diretta GitHub

Setup:
1. Registrarsi su codecov.io con GitHub
2. Aggiungere `CODECOV_TOKEN` come GitHub secret
3. Nel workflow: `codecov/codecov-action@v4`
4. Badge: `https://codecov.io/gh/cervellaswarm/cervellaswarm/branch/main/graph/badge.svg`

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage.xml
    fail_ci_if_error: true
```

### Opzione B: Self-hosted (no dipendenza esterna)

Usa `tj-actions/coverage-badge-py`:
- Genera badge SVG in-repo
- Commit automatico nel branch
- Zero dipendenze esterne
- Limite: badge non aggiornato in tempo reale su fork

**Per CervellaSwarm: Opzione A (Codecov) consigliata.** Gratuita, affidabile, standard nei grandi progetti.

### Badge test count (statico -> dinamico)

Il README ha "1,032 tests" hardcodato. Per renderlo dinamico:
- Genera un file `test-count.txt` nel CI
- Usa `shields.io` endpoint custom con gist (dinamicbadges-action)
- OPPURE: accetta che sia semi-statico e aggiornalo manualmente ogni sessione

**Raccomandazione:** non over-engineerare. Codecov badge per coverage + GitHub Actions badge per CI status sono sufficienti.

---

## 6. DEPENDABOT - CONFIG RACCOMANDATA

### CrewAI usa solo `uv` (1 entry). LangGraph usa uv + npm in multipli path.

Per CervellaSwarm (pip + npm, monorepo):

```yaml
version: 2
updates:
  # GitHub Actions - mantieni actions aggiornate
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      security-updates:
        patterns: ["*"]
        update-types: ["minor", "patch"]

  # npm per mcp-server
  - package-ecosystem: "npm"
    directory: "/packages/mcp-server"
    schedule:
      interval: "weekly"
    groups:
      security-updates:
        patterns: ["*"]
        update-types: ["minor", "patch"]
```

**Note:**
- `groups`: raggruppa tutti gli aggiornamenti in 1 PR (non 20 PR separate)
- `github-actions`: aggiorna automaticamente `actions/checkout@v3` -> `@v4` ecc
- `interval: weekly` standard. Monthly se non vuoi PR continue.

---

## 7. CODEOWNERS - VALE PER 1 MAINTAINER?

**Si, vale. Per due motivi:**

1. **Code review automatica**: quando qualcuno apre una PR, GitHub assegna automaticamente il reviewer. Con 1 maintainer, GitHub aggiunge te come required reviewer di default.

2. **Segnale di professionalita**: i contributor vedono che c'e ownership chiara. E un signal di progetto serio.

**Config minimale (pattern Fiber):**

```
# .github/CODEOWNERS
* @rafapra3008
```

Un singolo wildcard e sufficiente. Se aggiungi maintainer in futuro, aggiungi qui.

---

## 8. FUNDING.yml - GitHub Sponsors o altro?

**GitHub Sponsors e il piu semplice e nativo per un progetto GitHub.**

Pattern da Fiber:
```yaml
github: [cervellaswarm]  # username GitHub dell'account sponsor
```

**Prerequisito:** devi attivare GitHub Sponsors sul tuo account (github.com/sponsors).

**Alternativa che ho visto in grandi progetti:** Open Collective + GitHub Sponsors in parallelo. Per ora basta GitHub Sponsors.

---

## 9. PIANO CONCRETO - FILE DA CREARE

### Struttura finale raccomandata

```
.github/
├── ISSUE_TEMPLATE/
│   ├── config.yml              # Disabilita blank issues
│   ├── bug_report.yml          # Form YAML
│   └── feature_request.yml    # Form YAML
├── workflows/
│   ├── ci.yml                  # Test + lint (Python + TypeScript)
│   └── stale.yml               # Auto-close vecchie issues
├── PULL_REQUEST_TEMPLATE.md
├── dependabot.yml
├── CODEOWNERS
└── FUNDING.yml
```

**NOTA:** Non serve CodeQL per ora (aggiungi in F2 quando pubblico). Non serve `release-drafter` (aggiungi in F4 pre-launch).

---

## 10. CONTENUTO RACCOMANDATO PER OGNI FILE

### .github/ISSUE_TEMPLATE/config.yml

```yaml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://github.com/cervellaswarm/cervellaswarm/wiki
    about: Check the docs before opening an issue
  - name: Discussions
    url: https://github.com/cervellaswarm/cervellaswarm/discussions
    about: For questions and general discussion
```

### .github/ISSUE_TEMPLATE/bug_report.yml

```yaml
name: Bug Report
description: Something isn't working as expected
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report a bug.
        Please fill in as much detail as possible.

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Step-by-step instructions to reproduce the behavior
      placeholder: |
        1. Run `cervellaswarm ...`
        2. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened? Include full error message and stack trace.
    validations:
      required: true

  - type: dropdown
    id: python-version
    attributes:
      label: Python Version
      options:
        - "3.10"
        - "3.11"
        - "3.12"
        - "3.13"
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      options:
        - macOS
        - Ubuntu / Debian
        - Windows
        - Other Linux
        - Other
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: CervellaSwarm Version
      placeholder: "e.g. 0.1.0"
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Anything else that might be relevant (config files, environment, etc.)
    validations:
      required: false
```

### .github/ISSUE_TEMPLATE/feature_request.yml

```yaml
name: Feature Request
description: Suggest a new feature or improvement
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a feature!
        Search existing issues and discussions before submitting.

  - type: dropdown
    id: area
    attributes:
      label: Feature Area
      options:
        - Agent orchestration
        - Session continuity (SNCP)
        - Hook system
        - CLI
        - MCP server
        - Documentation
        - Testing / DX
        - Other
    validations:
      required: true

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this solve? What is the current limitation?
      placeholder: "As a user, I find it difficult to..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How would you like this to work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Other approaches you thought of
    validations:
      required: false

  - type: dropdown
    id: contribution
    attributes:
      label: Willing to Contribute?
      options:
        - "Yes - I will submit a PR"
        - "Maybe - I can help if guided"
        - "No - just suggesting"
    validations:
      required: true
```

### .github/PULL_REQUEST_TEMPLATE.md

```markdown
## Summary

<!-- What does this PR do? Why? Link related issues with "Closes #xxx" -->

## Type of Change

- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change (requires version bump)
- [ ] Documentation update
- [ ] Refactor / internal improvement
- [ ] CI / tooling

## Test Plan

<!-- How was this tested? -->

- [ ] Added unit tests covering the change
- [ ] Existing tests pass (`python -m pytest tests/ -q`)
- [ ] TypeScript tests pass (`npm test` in relevant package)

## Checklist

- [ ] Self-reviewed the diff
- [ ] Added comments on non-obvious code
- [ ] Updated documentation if behavior changed
- [ ] No hardcoded personal paths or secrets
```

### .github/workflows/ci.yml (Python + TypeScript)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  python-tests:
    name: Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    timeout-minutes: 20

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests with coverage
        run: |
          python -m pytest tests/common/ tests/swarm/ tests/memory/ tests/sncp/ \
            tests/utils/ tests/tools/ \
            -q --tb=short \
            --cov=scripts --cov=cervella \
            --cov-report=xml \
            --cov-report=term-missing

      - name: Upload coverage to Codecov
        if: matrix.python-version == '3.11'  # Upload solo una volta
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          fail_ci_if_error: false  # Non blocca CI se Codecov e down

  typescript-tests:
    name: TypeScript (Node 20)
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: packages/mcp-server/package-lock.json

      - name: Install and test MCP server
        working-directory: packages/mcp-server
        run: |
          npm ci
          npm test
          npm run build

  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: 'pip'

      - name: Install ruff
        run: pip install ruff

      - name: Run ruff
        run: ruff check . --output-format=github
```

### .github/workflows/stale.yml

```yaml
name: Close Stale Issues

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: >
            This issue has been inactive for 60 days.
            It will be closed in 7 days if there is no activity.
            If this is still relevant, please comment.
          days-before-stale: 60
          days-before-close: 7
          stale-issue-label: 'stale'
          exempt-issue-labels: 'pinned,security,roadmap'
```

### .github/dependabot.yml

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      python-deps:
        patterns: ["*"]
        update-types: ["minor", "patch"]

  - package-ecosystem: "npm"
    directory: "/packages/mcp-server"
    schedule:
      interval: "weekly"
    groups:
      npm-deps:
        patterns: ["*"]
        update-types: ["minor", "patch"]
```

### .github/CODEOWNERS

```
# All files -> maintainer review required
* @rafapra3008
```

### .github/FUNDING.yml

```yaml
github: [cervellaswarm]
```

**Prerequisito:** attivare GitHub Sponsors su account `cervellaswarm` o `rafapra3008`.

---

## 11. NOTA SU CONTENT SCANNER

Il content scanner v3.1 dovra verificare che i file `.github/` non contengano:
- Path interni (`/Users/rafapra/`)
- Termini blacklistati (`SNCP_DIR`, `REGINA`, ecc.)
- Riferimenti a repo privato

I file sopra sono gia stati scritti pensando al pubblico.

---

## PRIORITA DI IMPLEMENTAZIONE

| Priorita | File | Effort | Impatto |
|----------|------|--------|---------|
| P0 | `ISSUE_TEMPLATE/config.yml` | 5 min | Blocca blank issues |
| P0 | `ISSUE_TEMPLATE/bug_report.yml` | 15 min | Struttura reports |
| P0 | `ISSUE_TEMPLATE/feature_request.yml` | 10 min | Struttura feature req |
| P0 | `PULL_REQUEST_TEMPLATE.md` | 10 min | Guida contributors |
| P1 | `workflows/ci.yml` | 30 min + Codecov setup | Badge dinamici CI |
| P1 | `dependabot.yml` | 10 min | Security auto-updates |
| P2 | `CODEOWNERS` | 2 min | Pro signal |
| P2 | `FUNDING.yml` | 2 min | Monetizzazione futura |
| P3 | `workflows/stale.yml` | 5 min | Manutenzione automatica |

**Stima totale: ~90 minuti per implementazione completa.**

---

## SINTESI DECISIONI CHIAVE

| Decisione | Raccomandazione | Perche |
|-----------|----------------|--------|
| Issue format | YAML form-based | Strutturato, validazione, tutti i grandi usano questo |
| Blank issues | Disabilitati | config.yml `blank_issues_enabled: false` |
| Python matrix | 3.10, 3.11, 3.12 | 3.13 troppo nuovo per tree-sitter |
| OS matrix | Solo ubuntu-latest | Costo/velocita: Windows/macOS non necessari ora |
| Coverage upload | Codecov | Free OSS, PR comments, badge automatici |
| CI trigger | push main + PR | Non ogni branch per risparmiare minuti Actions |
| Dependabot | Gruppi settimanali | 1 PR raggruppata, non 20 separate |
| CODEOWNERS | Si, anche con 1 maintainer | Signal professionalita + auto-assign review |
| FUNDING | GitHub Sponsors | Piu semplice, nativo GitHub |
| TypeScript | Node 20 LTS | Stabile, supportato fino 2026 |

---

*Report generato da Cervella Researcher - S366 - 2026-02-17*
*Fonti: GitHub Docs, CrewAI .github/, LangGraph .github/, Fiber .github/, Codecov docs*
