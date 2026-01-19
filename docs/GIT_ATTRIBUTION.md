# Git Attribution System

> CervellaSwarm 2.0 - Tracciabilita commits per AI team

---

## Overview

Il sistema di Git Attribution permette di tracciare chi (quale agente) ha fatto cosa nel codebase. Ogni commit include una firma che identifica il worker responsabile.

```
feat(api): Add user authentication

Co-authored-by: CervellaSwarm (backend-worker/claude-sonnet-4-5) <noreply@cervellaswarm.com>
```

---

## Componenti

| File | Versione | Scopo |
|------|----------|-------|
| `scripts/utils/git_worker_commit.sh` | v1.2.2 | Script commit con attribution |
| `scripts/utils/worker_attribution.json` | v1.1.0 | Mapping worker → attribution |
| `scripts/swarm/spawn-workers.sh` | v3.6.0 | Integrazione --auto-commit |

---

## Uso Base

### Commit Manuale con Attribution

```bash
# Commit esplicito
./scripts/utils/git_worker_commit.sh \
  --worker backend \
  --type feat \
  --scope api \
  --message "Add login endpoint"

# Con auto-detect di type e scope
./scripts/utils/git_worker_commit.sh \
  --worker frontend \
  --auto \
  --message "Fix button alignment"
```

### Auto-Commit con spawn-workers

```bash
# Spawna worker CON auto-commit
spawn-workers --backend --auto-commit

# Default (senza auto-commit)
spawn-workers --backend
```

---

## Conventional Commits

Il sistema usa [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <message>
```

### Types Supportati

| Type | Quando |
|------|--------|
| `feat` | Nuova funzionalita |
| `fix` | Bug fix |
| `docs` | Solo documentazione |
| `style` | Formattazione (no logic) |
| `refactor` | Refactoring (no feat/fix) |
| `test` | Aggiunta/fix test |
| `chore` | Build, config, etc |

### Auto-Detection Type

Lo script rileva il tipo dai file modificati:

| Pattern | Type Rilevato |
|---------|---------------|
| `*.md`, `docs/*` | docs |
| `*test*`, `tests/*` | test |
| `*.css`, `*.scss` | style |
| `package*.json`, `*.config.*` | chore |
| Altri | feat |

### Scope Patterns (13 totali)

| Pattern | Scope |
|---------|-------|
| `scripts/*` | scripts |
| `docs/*` | docs |
| `api/*`, `routes/*` | api |
| `components/*`, `ui/*` | ui |
| `tests/*`, `test/*` | test |
| `hooks/*` | hooks |
| `config/*` | config |
| `db/*`, `database/*` | db |
| `.sncp/*` | sncp |
| `reports/*` | reports |
| `src/*` | src |
| Altri | general |

---

## Worker Attribution

### 16 Agenti Tracciabili

**Workers (Sonnet):**
- backend, frontend, tester, docs, reviewer
- devops, researcher, data, security
- scienziata, ingegnera, marketing

**Guardiane (Opus):**
- guardiana-qualita, guardiana-ops, guardiana-ricerca

**Special:**
- regina, orchestrator, auto-save

### Formato Attribution

```
Co-authored-by: CervellaSwarm ({role}/{model}) <noreply@cervellaswarm.com>
```

Esempio:
```
Co-authored-by: CervellaSwarm (backend-worker/claude-sonnet-4-5) <noreply@cervellaswarm.com>
```

---

## Comandi Avanzati

### Save User Work

Prima che un worker modifichi file, salva il lavoro dell'utente:

```bash
./scripts/utils/git_worker_commit.sh --save-user-work
```

### Check Dirty

Verifica se ci sono modifiche non committate:

```bash
./scripts/utils/git_worker_commit.sh --check-dirty
```

### Dry Run

Preview del commit senza eseguirlo:

```bash
./scripts/utils/git_worker_commit.sh \
  --worker backend \
  --type feat \
  --message "Test" \
  --dry-run
```

### Undo Last Commit

Annulla l'ultimo commit (preserva modifiche staged):

```bash
./scripts/utils/git_worker_commit.sh --undo
```

---

## Flags Reference

| Flag | Descrizione |
|------|-------------|
| `--worker NAME` | Nome del worker (obbligatorio) |
| `--type TYPE` | Tipo commit (feat/fix/docs/...) |
| `--scope SCOPE` | Scope del commit |
| `--message MSG` | Messaggio commit (obbligatorio) |
| `--auto` | Auto-detect type e scope |
| `--dry-run` | Preview senza commit |
| `--allow-hooks` | Esegue pre-commit hooks |
| `--staged-only` | Committa solo staged files |
| `--save-user-work` | Salva dirty files utente |
| `--check-dirty` | Verifica uncommitted changes |
| `--undo` | Annulla ultimo commit (soft) |

---

## Configurazione

### Attribution JSON

Il file `scripts/utils/worker_attribution.json` e la single source of truth per le attribution. Struttura:

```json
{
  "workers": {
    "backend": {
      "role": "backend-worker",
      "model": "claude-sonnet-4-5",
      "specialization": "Python, FastAPI, Database, API REST"
    }
  }
}
```

Per aggiungere un worker, editare il JSON.

### Requisiti

- `jq` per parsing JSON (fallback se non disponibile)
- Git configurato
- Bash 4+

---

## Workflow Raccomandato

```
1. spawn-workers --backend --auto-commit
2. Worker fa le modifiche
3. Auto-commit con attribution ← automatico!
4. Regina verifica il lavoro
5. Push su origin (privato)
```

---

## Troubleshooting

### "Worker non valido"

Verifica che il nome sia nella lista:
```bash
./scripts/utils/git_worker_commit.sh --help
```

### "jq non installato"

```bash
brew install jq  # macOS
apt install jq   # Linux
```

### "Nothing to commit"

Verifica che ci siano modifiche:
```bash
git status
```

---

*Documentazione creata: Sessione 273 - 19 Gennaio 2026*
*CervellaSwarm Git Flow v1.2.2*
