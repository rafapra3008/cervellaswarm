# Ricerca: Git Commit in AI Coding Tools

**Data:** 19 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Contesto:** Decidere strategia auto-commit per CervellaSwarm workers

---

## TL;DR

**AIDER**: Auto-commit **ATTIVO di default**, disattivabile con flag
**CURSOR**: **SOLO genera messaggi**, utente commita manualmente
**CLAUDE CODE**: **NO auto-commit**, l'utente chiede e Claude esegue

**Raccomandazione:** Approccio AIDER con flag opt-out (`--no-auto-commit`)

---

## 1. AIDER - Auto-commit di Default

### Comportamento Standard

```
✅ Auto-commit ATTIVO per default
✅ Ogni edit → commit automatico
✅ Pre-commit di modifiche esistenti (separa lavoro AI/umano)
✅ Attribution automatica: "(aider)" in git metadata
✅ Commit messages con Conventional Commits
```

### Controllo Utente

| Flag | Effetto |
|------|---------|
| `--no-auto-commits` | Disabilita auto-commit |
| `--no-dirty-commits` | Non commita pre-existing changes |
| `--no-git` | Disabilita git completamente |
| `--commit-prompt` | Personalizza template commit message |

### Attribution Mechanism

```bash
# Git metadata modificato:
Author: "John Doe (aider)"
Committer: "John Doe (aider)"

# Opzionalmente:
- Prefisso messaggio: "aider: Fix bug in parser"
- Co-authored-by: trailer standard GitHub
```

### Filosofia AIDER

> "Ogni edit dell'AI deve essere tracciabile e facilmente revertibile"

Commit automatico permette:
- Atomic rollback (git revert)
- Storia chiara AI vs umano
- Review granulare delle modifiche AI

**Fonte:** [Aider Git Integration](https://aider.chat/docs/git.html)

---

## 2. CURSOR - Solo Generazione Messaggi

### Comportamento Standard

```
❌ NO auto-commit
✅ Genera SOLO messaggi commit
👤 Utente esegue commit manualmente
```

### Workflow Utente

```
1. Stage files (manuale)
2. Click sparkle icon → genera messaggio AI
3. Revisiona messaggio
4. Commit manuale
5. Push manuale
```

### Features

- Adatta stile ai commit esistenti (Conventional Commits detection)
- Usa staged changes + git history per contesto
- Può essere automatizzato con shortcuts custom (chain comandi)

### Filosofia CURSOR

> "L'AI assiste, l'umano controlla"

Commit rimane decisione esplicita dell'utente.
AI riduce friction ma non toglie controllo.

**Fonte:** [Cursor AI Commit Message](https://cursor.com/docs/more/ai-commit-message)

---

## 3. CLAUDE CODE - Natural Language Git

### Comportamento Standard

```
❌ NO auto-commit
💬 Utente chiede: "Commit these changes"
🤖 Claude esegue: git add + git commit
```

### Workflow

```
User: "Commit the API fixes with a good message"
Claude: [analyzes changes]
        [generates message]
        [executes git commit]
        "Committed: feat(api): Add error handling for timeout scenarios"
```

### Attribution

```bash
# GitHub Co-authored-by trailer:
Co-authored-by: Claude <claude@anthropic.com>

# Appare in GitHub come co-autore
```

Disattivabile via CLAUDE.md o git hooks.

### Filosofia CLAUDE CODE

> "Conversazione naturale, zero config"

Git è uno strumento come gli altri.
Nessuna modalità speciale, solo linguaggio naturale.

**Fonti:**
- [How to Use Git with Claude Code](https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution)
- [AI-Powered Git Commits with Claude Code](https://susomejias.dev/ai-powered-git-commits-with-claude-code/)

---

## 4. Pattern nel Settore

### Spectrum Automazione

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Manuale          Semi-Auto           Auto
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CURSOR       CLAUDE CODE         AIDER
(genera)     (su richiesta)   (default on)
```

### Best Practices Identificate

| Pratica | Tool | Rationale |
|---------|------|-----------|
| **Attribution obbligatoria** | Tutti | Tracciare lavoro AI vs umano |
| **Conventional Commits** | Aider, Cursor | Standard industria |
| **Opt-out disponibile** | Aider | Rispettare workflow utente |
| **Commit atomici** | Aider | Facilita rollback |
| **Separazione pre-existing** | Aider | Chiarezza storia git |

### Consensus Emergente (2026)

Dall'analisi dei tool e degli articoli:

1. **Attribution è standard** - Tutti implementano tracking AI
2. **Auto-commit è controverso** - Ma tools di successo lo offrono
3. **Opt-out cruciale** - Flag per disabilitare è fondamentale
4. **Atomicità vince** - Commit granulari > grossi batch

**Fonte:** [Git Best Practices and AI-Driven Development](https://medium.com/@FrankGoortani/git-best-practices-and-ai-driven-development-rethinking-documentation-and-coding-standards-bca75567566a)

---

## 5. Pro/Contro per CervellaSwarm

### Opzione A: Auto-commit Sempre (modello AIDER)

**PRO:**
- ✅ Storia git granulare e pulita
- ✅ Ogni worker edit = atomic commit
- ✅ Rollback preciso e facile
- ✅ Zero friction per worker (focus su task)
- ✅ Attribution automatica già implementata
- ✅ Segue best practice del leader (Aider)

**CONTRO:**
- ⚠️ Può generare molti commit (ma squash facile)
- ⚠️ Utente perde controllo pre-push
- ⚠️ Richiede trust nel sistema

### Opzione B: Commit Manuale (modello CURSOR)

**PRO:**
- ✅ Controllo totale utente
- ✅ Review prima del commit
- ✅ Flessibilità massima

**CONTRO:**
- ❌ Friction alto per Rafa
- ❌ Workers creano files ma utente deve committare
- ❌ Rompe automazione del sistema
- ❌ Rafa fa operazioni tecniche (CONTRO Costituzione!)

### Opzione C: Flag --auto-commit (default OFF)

**PRO:**
- ✅ Flessibilità configurabile
- ✅ Default safe (nessuna sorpresa)
- ✅ Opt-in quando pronto

**CONTRO:**
- ⚠️ Richiede configurazione esplicita
- ⚠️ Default pessimo per uso swarm (friction alta)
- ⚠️ Utente deve ricordare di attivare flag

---

## 6. RACCOMANDAZIONE

### Strategia Proposta: "AIDER-Inspired + Regina Control"

```bash
# Default per worker spawns:
AUTO_COMMIT=true (come Aider)

# Con override globale:
export CERVELLASWARM_AUTO_COMMIT=false  # disabilita per tutti

# Con override per spawn:
spawn-workers --backend --no-auto-commit  # opt-out specifico
```

### Implementazione in 3 Livelli

**LIVELLO 1: Worker (default ON)**
```bash
# In git_worker_commit.sh
AUTO_COMMIT=${AUTO_COMMIT:-true}  # default true come Aider

if [ "$AUTO_COMMIT" = "true" ]; then
  git add .
  git commit --author="Worker Name (CervellaSwarm) <...>"
fi
```

**LIVELLO 2: Regina Override**
```bash
# Regina può disabilitare prima di spawn
export AUTO_COMMIT=false
spawn-workers --backend
```

**LIVELLO 3: User Global Config**
```bash
# In ~/.config/cervellaswarm/config
AUTO_COMMIT=false  # utente decide default
```

### Rationale

1. **Default ON come Aider** - Tool di maggior successo usa questa strategia
2. **Attribution già implementata** - `git_worker_commit.sh` già pronto
3. **Override a 3 livelli** - Flessibilità totale
4. **Zero friction per Rafa** - Workers committano automaticamente
5. **Allineato a Costituzione** - Rafa MAI operazioni tecniche

### Commit Message Strategy

Seguire Aider:
```bash
# Worker genera messaggio con context:
# - File modificati
# - Task description
# - Chat history se rilevante

# Formato Conventional Commits:
"feat(api): Add SSE endpoint for real-time updates

Implemented by: cervella-backend-dev
Task: #TASK_042
Context: Dashboarding sprint"
```

---

## 7. Prossimi Step

### Implementazione Suggerita

1. **Modificare `git_worker_commit.sh`**
   - Aggiungere flag `AUTO_COMMIT` con default `true`
   - Implementare commit message generation migliore

2. **Aggiornare `spawn-workers`**
   - Passare env var `AUTO_COMMIT` ai worker
   - Flag CLI: `--no-auto-commit` per override

3. **Documentare in DNA**
   - Aggiornare DNA worker con policy commit
   - Esempi uso in docs/

4. **Test Phase**
   - Provare con 1-2 task piccoli
   - Verificare git history risultante
   - Adjust se necessario

### Metriche Success

- ✅ Zero richieste "Rafa, committa questo"
- ✅ Git history pulita e comprensibile
- ✅ Attribution sempre presente
- ✅ Rollback funziona a livello granulare

---

## Fonti

- [Aider Git Integration](https://aider.chat/docs/git.html)
- [Cursor AI Commit Message](https://cursor.com/docs/more/ai-commit-message)
- [How to Use Git with Claude Code](https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution)
- [AI-Powered Git Commits with Claude Code](https://susomejias.dev/ai-powered-git-commits-with-claude-code/)
- [Git Best Practices and AI-Driven Development](https://medium.com/@FrankGoortani/git-best-practices-and-ai-driven-development-rethinking-documentation-and-coding-standards-bca75567566a)
- [GitHub - Aider-AI/aider](https://github.com/Aider-AI/aider)
- [Learn Cursor - Git Commit](https://learn-cursor.com/en/blog/posts/cursor-git-commit)

---

*Ricerca completata: 19 Gennaio 2026*
*Next: Discussione con Regina per decisione finale*
