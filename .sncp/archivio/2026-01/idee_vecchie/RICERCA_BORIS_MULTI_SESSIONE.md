# Ricerca Boris Multi-Sessione - 9 Gennaio 2026

> **Sessione:** 134
> **Obiettivo:** Completare il quadro per LA NOSTRA STRADA finale

---

## COME BORIS GESTISCE MULTI-SESSIONE

### Setup di Boris

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   BORIS CHERNY (Creatore Claude Code):                          ║
║                                                                  ║
║   • 5 Claudes in terminal (tabs 1-5)                            ║
║   • 5-10 Claudes su claude.ai/code (browser)                    ║
║   • Sessioni mobile (iOS app)                                   ║
║   • --teleport per handoff local <-> web                        ║
║   • System notifications per sapere quando serve input          ║
║                                                                  ║
║   TOTALE: 10-15+ sessioni CONTEMPORANEE!                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Come Condivide Info tra Sessioni

**1. CLAUDE.md Condiviso (Git)**
- SINGOLO file per tutto il team
- In git, contribuito da tutti
- "Anytime Claude sbaglia, lo aggiungiamo"
- GitHub Action per aggiornamenti via PR

**2. One Session = One Context**
- Ogni sessione ha UN focus
- Evita token bloat
- Claude rimane concentrato su sub-task specifico

**3. Plan Mode SEMPRE**
- Shift+Tab x2 per entrare in Plan mode
- Va avanti e indietro finché il piano piace
- POI auto-accept edits mode
- "A good plan is really important!"

### Come Evita Conflitti

**Problema:** Multiple Claudes sullo stesso progetto = conflitti su stessi file

**Soluzioni Esistenti:**

| Soluzione | Come Funziona | Pro | Contro |
|-----------|---------------|-----|--------|
| **Git Worktrees** | Directory separate, storia condivisa | Isolamento totale | Bootstrap ogni worktree |
| **GitButler + Hooks** | Auto-sorting in branches separate | Zero worktrees | Richiede GitButler |
| **ccswitch** | CLI per gestire worktrees | Semplice | Setup manuale |
| **Separate Checkouts** | Clone separati | Semplice | Spazio disco |

### Come Fa il Merge

**Git Worktrees:**
- Ogni worktree = branch separato
- Merge normale via git
- "Fun new ability to create merge conflicts with yourself"

**GitButler:**
- Hooks creano branch automaticamente per ogni sessione
- Commit automatico con prompt usato
- Squash, reorder, split dopo

---

## STRUMENTI SCOPERTI

### 1. GitButler + Claude Code Hooks

```
COME FUNZIONA:
1. Hook pre-tool: GitButler sa che Claude sta per modificare
2. Hook post-tool: GitButler assegna modifiche a branch
3. Hook stop: Commit automatico

RISULTATO:
- 3 features in parallelo → 3 branches pulite
- Zero conflitti
- Zero worktrees
```

**Link:** https://blog.gitbutler.com/parallel-claude-code

### 2. ccswitch

```
CLI per gestire git worktrees per Claude Code.

COMANDI:
- ccswitch create <nome>  → Crea worktree
- ccswitch list           → Lista sessioni
- ccswitch cleanup        → Rimuovi worktrees

STORAGE:
~/.ccswitch/worktrees/repo-name/session-name
(progetto principale resta pulito)
```

**GitHub:** https://github.com/ksred/ccswitch

### 3. CCManager

```
Gestisce sessioni multiple per:
- Claude Code
- Gemini CLI
- Codex CLI
- Cursor Agent
- Copilot CLI

FEATURE SPECIALE:
Copia session data (conversation history, context)
quando crea nuovi worktrees!
```

**GitHub:** https://github.com/kbwo/ccmanager

### 4. Crystal

```
Desktop app per:
- Run multiple sessions (Claude Code + Codex)
- Commit automatico per ogni iterazione
- Compare approaches
```

**GitHub:** https://github.com/stravu/crystal

---

## BEST PRACTICES DALLA COMMUNITY

### 1. Isolamento

```
"Changes made in one worktree won't affect others,
 preventing Claude instances from interfering with each other."
```

### 2. Context Management

```
"Periodically reset or prune context during long sessions"
"Compress global state aggressively—store just the plan,
 key decisions, and the latest artifacts"
```

### 3. Document & Clear Pattern

```
1. Claude dumpa plan e progress in un .md
2. /clear lo stato
3. Nuova sessione legge il .md e continua
```

### 4. Parallel Scripting

```bash
# Per large-scale refactors:
claude -p "in /pathA change all refs from foo to bar" &
claude -p "in /pathB change all refs from foo to bar" &
wait
```

---

## FUTURO (2026)

```
"At a recent Claude Code Meetup in Tokyo, Anthropic engineers
 confirmed that Swarming capabilities will receive significant
 attention in 2026."
```

Async Subagents (v2.0.60):
- Parallel codebase exploration
- Concurrent code reviews
- Simultaneous search operations

---

## CONFRONTO CON IL NOSTRO PATTERN BORIS

| Aspetto | Boris | Noi (Pattern Boris) |
|---------|-------|---------------------|
| Isolamento | Git worktrees | Git clones separati |
| N. sessioni | 5-10+ | 2-3 (per ora) |
| Tool | iTerm2 + notifications | tmux + watcher |
| Context sharing | CLAUDE.md in git | CLAUDE.md + SNCP |
| Merge | Git merge | Git merge |

**DIFFERENZA CHIAVE:** Boris non ha una Regina che coordina!
Noi abbiamo IO che orchestro tutto.

---

## DOMANDE PER LA GUARDIANA

1. **GitButler vs Git Clones:** Vale la pena esplorare GitButler?
2. **ccswitch vs Nostro Pattern:** Usiamo ccswitch o manteniamo i clones?
3. **Quante sessioni parallele?** 2-3 bastano o scaliamo?
4. **Come integrare con Task Tool interno?** Ibrido?

---

## FONTI

- [Boris Cherny Workflow - VentureBeat](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are)
- [How Boris Uses Claude Code - Karo Zieminski](https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow)
- [GitButler Parallel Claude Code](https://blog.gitbutler.com/parallel-claude-code)
- [ccswitch GitHub](https://github.com/ksred/ccswitch)
- [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
- [CCManager GitHub](https://github.com/kbwo/ccmanager)
