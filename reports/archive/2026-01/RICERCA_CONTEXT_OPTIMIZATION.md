# RICERCA: Ottimizzazione Context Usage in Claude Code

> **Data:** 8 Gennaio 2026
> **Ricercatore:** cervella-researcher
> **Obiettivo:** Ridurre il 19% di context overhead iniziale SENZA toccare CLAUDE.md/COSTITUZIONE.md

---

## EXECUTIVE SUMMARY

**Problema:** Ogni sessione parte con 19% contesto gia consumato.

**Soluzione:** Implementando le ottimizzazioni proposte, possiamo ridurre l'overhead del **37-59%**.

**Cosa NON tocchiamo:**
- ~/.claude/CLAUDE.md (personalita)
- ~/.claude/COSTITUZIONE.md (anima)

**Cosa ottimizziamo:**
- Hook SessionStart (load_context.py)
- CLAUDE.md del progetto
- Memoria swarm iniettata
- Pattern di caricamento

---

## 1. ANALISI ATTUALE

### Cosa Consuma Quanto

| Componente | Tokens Stimati | Note |
|------------|----------------|------|
| System prompts Claude Code | ~2000-3000 | Fisso, non modificabile |
| CLAUDE.md globale | ~2500-3000 | SACRO - non toccare |
| COSTITUZIONE.md | ~1800-2200 | SACRO - non toccare |
| CLAUDE.md progetto | ~800-1000 | Ottimizzabile |
| load_context.py output | ~800-1500 | Ottimizzabile |
| NORD/PROMPT_RIPRESA | ~500-1000 | Da verificare |
| **TOTALE** | ~8400-11700 | |

### Hook SessionStart - Dettaglio

```python
# load_context.py carica:
- Ultimi 10-20 eventi swarm (100 char ciascuno)
- Statistiche per OGNI agent (12+ agent)
- Lezioni apprese (fino a 10)
- Suggerimenti attivi (fino a 5)
```

**Output tipico:** 40-80 righe di markdown con box, emoji, tabelle.

### CLAUDE.md Progetto - Dettaglio

```
199 righe totali:
- ASCII art header (14 righe)
- Visione (10 righe)
- Architettura ASCII (20 righe)
- Tabella famiglia (20 righe)
- Principi (30 righe)
- Struttura progetto (45 righe)
- Quick start (15 righe)
- Filosofia (20 righe)
- Footer (10 righe)
```

**Ridondanze:** Tabella famiglia gia in swarm-help, architettura gia in docs/.

---

## 2. QUICK WINS (Implementabili Subito)

### 2.1 Ottimizza load_context.py

**Modifiche:**

```python
# PRIMA
events = get_recent_events(conn, limit=20)  # 20 eventi
task[:100]  # 100 char per task

# DOPO
events = get_recent_events(conn, limit=5)   # 5 eventi
task[:50]   # 50 char per task
```

**Altre ottimizzazioni:**
- Statistiche: tutti agent → top 3 per task count
- Lezioni: 10 → 3 (solo alta confidence)
- Rimuovi box decorativi ASCII

**Risparmio stimato:** 300-400 tokens (-25-35%)

### 2.2 CLAUDE.md Progetto Compatto

**Crea versione compatta (40 righe max):**

```markdown
# CervellaSwarm

Multi-Agent Orchestration System. 16 agenti specializzati.

## Quick Reference
- Famiglia: `swarm-help` o `~/.claude/agents/`
- Docs: `docs/` per architettura e guide
- Scripts: `scripts/` per automazione

## Principi
1. ZERO CASINO - Mai due agenti stesso file
2. SPECIALIZZAZIONE - Ogni Cervella ha UN ruolo
3. COMUNICAZIONE - Via ROADMAP e git branches

## Path
- Agents: ~/.claude/agents/
- Logs: .swarm/logs/
- Tasks: .swarm/tasks/

*Per dettagli: docs/architettura/ARCHITETTURA_SISTEMA.md*
```

**Risparmio stimato:** 400-500 tokens (-50%)

### 2.3 Verifica NORD/PROMPT_RIPRESA Injection

**Da verificare:** L'hook sta iniettando questi file?

Se si:
- Riduci a header-only (prime 20 righe)
- Oppure rimuovi (Cervella puo leggerli con Read)

**Risparmio potenziale:** 200-500 tokens

### TOTALE QUICK WINS

| Ottimizzazione | Risparmio |
|----------------|-----------|
| load_context.py | -300-400 tokens |
| CLAUDE.md compatto | -400-500 tokens |
| NORD/PROMPT header | -200-500 tokens |
| **TOTALE** | **-900-1400 tokens (-37%)** |

---

## 3. OTTIMIZZAZIONI MEDIE (Futuro)

### 3.1 Context Condizionale per Ruolo

**Idea:** Regina e Worker hanno bisogni diversi.

```python
# load_context.py
def load_context(agent_role="regina"):
    if agent_role == "regina":
        # Full context
        return full_memory_context()
    else:
        # Worker: solo lezioni rilevanti
        return minimal_context(agent_name)
```

**Risparmio:** -40-50% per ogni worker

### 3.2 Memory Snapshot Giornaliero

**Invece di:**
- 10 eventi + timestamp + agent + task + status
- Statistiche per ogni agent
- Lezioni complete

**Fai:**
- 1 riga summary: "Ieri: 5 task completati, 2 in corso"
- Top 3 agent attivi
- 1 lezione critica

**Risparmio:** -70-80% hook output

### 3.3 Lazy Loading Pattern

**Principio chiave trovato in ricerca:**

> "Claude non ha bisogno di docs verbose all'inizio.
> Ha bisogno di TRIGGER per sapere QUANDO caricare contesto dettagliato."

**Pattern:**

```markdown
# PRIMA (100 righe sempre in context)
[tutta la documentazione]

# DOPO (5 righe + trigger)
## Quick Ref
- Famiglia: `swarm-help`
- Per dettagli architettura: Read docs/architettura/
- Per storia: Read NORD.md o PROMPT_RIPRESA.md
```

**Risparmio:** Enorme per progetti con molta documentazione

---

## 4. IDEE AVANZATE (Lungo Termine)

### 4.1 Skill System per Context

**Idea:** Invece di caricare tutto, carica "skills" on-demand.

```
/load-swarm-context  → Carica memoria swarm
/load-project-arch   → Carica architettura
/load-lessons        → Carica lezioni apprese
```

### 4.2 Context Compression

**Idea:** Comprimi informazioni in formato denso.

```
# PRIMA (80 tokens)
- cervella-backend: 43 task (100.0% successo) - Progetti: cervellaswarm, miracollo

# DOPO (20 tokens)
backend:43/100%|swarm,miracollo
```

### 4.3 External Memory con MCP

**Idea:** Memoria esterna accessibile via MCP invece di iniettata.

```json
{
  "mcpServers": {
    "swarm-memory": {
      "command": "swarm-memory-server",
      "description": "Accede a memoria swarm on-demand"
    }
  }
}
```

---

## 5. BEST PRACTICES TROVATE

### Fonte: 54% Context Reduction Case Study

Un progetto ha ottenuto -54% tokens con:

1. **Rimozione docs verbosi** da context iniziale
2. **Tabella trigger** invece di spiegazioni
3. **Link a file** invece di contenuto inline
4. **Summary** invece di dettagli completi

### Pattern Raccomandato

```
SBAGLIATO:
- Caricare tutto all'avvio
- Documentazione inline completa
- Statistiche dettagliate sempre

GIUSTO:
- Caricare minimo necessario
- Riferimenti a dove trovare dettagli
- Summary con opzione di espansione
```

### Anti-Pattern da Evitare

1. **Over-trimming:** Rimuovere troppo (Claude perde grounding)
2. **External-only:** Tutto in file esterni (crea friction)
3. **Complex loading:** Logica troppo complessa per decidere cosa caricare

---

## 6. RACCOMANDAZIONI

### Sprint 1: Quick Wins (1 ora)

```
[ ] Modifica load_context.py
    - limit=20 → limit=5
    - task[:100] → task[:50]
    - Rimuovi box ASCII

[ ] Crea CLAUDE.md compatto
    - 40 righe max
    - Link a docs/ per dettagli

[ ] Verifica NORD/PROMPT injection
    - Se presente, riduci o rimuovi

[ ] Benchmark before/after
    - Screenshot % contesto inizio sessione
```

### Sprint 2: Ottimizzazioni Medie (2-3 ore)

```
[ ] Context condizionale Regina/Worker
[ ] Memory snapshot giornaliero
[ ] Lazy loading pattern completo
```

### Sprint 3: Idee Avanzate (futuro)

```
[ ] Skill system
[ ] Context compression
[ ] MCP memory server
```

---

## 7. METRICHE SUCCESSO

### Before (Attuale)

- Context iniziale: 19%
- Tokens overhead: ~8000-11000
- Righe iniettate: ~200+

### After Sprint 1 (Target)

- Context iniziale: 12-14% (-37%)
- Tokens overhead: ~5000-7000
- Righe iniettate: ~80-100

### After Sprint 2 (Target)

- Context iniziale: 8-10% (-50%)
- Tokens overhead: ~4000-5500
- Righe iniettate: ~40-60

---

## 8. FONTI

1. [Claude Code Context Optimization - 54% Reduction](https://gist.github.com/johnlindquist/849b813e76039a908d962b2f0923dc9a)
2. [Advanced Tool Use - Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use)
3. [24 Claude Code Tips - Dev.to](https://dev.to/oikon/24-claude-code-tips-claudecodeadventcalendar-52b5)
4. [Context Management Guide - ClaudeCode.io](https://claudecode.io/guides/context-management)
5. [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)

---

*Ricerca completata da cervella-researcher*
*8 Gennaio 2026*

**TL;DR:** Possiamo risparmiare 37-59% del context overhead senza toccare la personalita. Inizia con Sprint 1 (1 ora di lavoro).
