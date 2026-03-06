# SNCP Evolution MC4 - Ricerca Stato dell'Arte Memoria AI Agents

> **Data:** 2026-03-06 - Sessione 431
> **Agente:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 8 consultate (docs ufficiali + web + file locali)

---

## 1. STATO DELL'ARTE - Memoria AI Agents 2026

### Le 4 Categorie Universali di Memoria

La comunita converge su una gerarchia a 4 livelli:

| Livello | Tipo | Durata | Limite |
|---------|------|--------|--------|
| L1 Working | Context window | Solo sessione | 128K-1M token |
| L2 Short-term | Storia sessione | Solo sessione | Accumula rumore (60%+) |
| L3 Long-term files | File markdown/DB | Cross-session | ~37% recall accuracy |
| L4 Vector/RAG | Semantic search | Cross-session | Scala fino a ~500K docs |

**Insight chiave:** Cross-session retention e l'hard problem del 2026. Il 37% di accuracy citato da Morph LLM conferma che nessuno lo ha risolto bene. SNCP con PROMPT_RIPRESA e auto-memory fa meglio della media.

### Pattern Dominanti nel 2026

1. **Files as memory** - Il pattern piu diffuso. Semplice, ispezionabile, versionabile con git. SNCP lo ha adottato correttamente.

2. **Progressive disclosure** - Carica solo il summary all'inizio, espande on-demand. SNCP 5.0 lo ha gia implementato (ClaudeMem, S327).

3. **Memory distillation** - Estrai segnali ad alto valore dalla conversazione, scrivi su file. Claude auto-memory fa questo automaticamente.

4. **Structured handoff** - Passa solo le informazioni necessarie (obiettivi, vincoli, decisioni prese), non il dump completo della storia.

---

## 2. CLAUDE CODE AUTO-MEMORY - Come Funziona Davvero

Dalla documentazione ufficiale letta oggi (code.claude.com/docs/en/memory):

### CLAUDE.md - Il Sistema Primario

- **Multi-layer:** managed policy > project > user > local
- **Load semantics:** I file CLAUDE.md nella gerarchia sopra la CWD vengono caricati COMPLETI all'avvio. Quelli in subdirectory vengono caricati on-demand quando Claude legge file in quelle directory.
- **Limite pratico:** Target sotto 200 righe per file. File piu lunghi consumano piu context e riducono l'aderenza.
- **Sopravvive a /compact:** CLAUDE.md viene riletto da disco dopo ogni compaction - questo e importante.

**Implicazione per noi:** I nostri 3 CLAUDE.md (global `~/.claude/CLAUDE.md`, project `CervellaSwarm/CLAUDE.md`, insiders `~/.claude-insiders/CLAUDE.md`) vengono tutti caricati. Stima: ~6KB totali = circa 1500 token solo di istruzioni fisse.

### Auto-Memory (`~/.claude-insiders/projects/.../memory/MEMORY.md`)

- **Prima 200 righe** di MEMORY.md vengono caricate ad ogni sessione automaticamente
- File topic separati (debugging.md, patterns.md) vengono caricati on-demand da Claude
- Machine-local: non sincronizzato tra macchine
- Claude scrive automaticamente quando scopre qualcosa di utile

**Conferma:** Il nostro MEMORY.md in `~/.claude-insiders/projects/-Users-rafapra-Developer-CervellaSwarm/memory/MEMORY.md` e già integrato con Claude auto-memory. Funziona in parallelo con SNCP.

### SubagentStart Hook

Dalla docs ufficiale: il hook SubagentStart puo iniettare `additionalContext` nel contesto del subagente. Il file `subagent_context_inject.py` menzionato nel CLAUDE.md non esiste piu come file attivo (trovato solo `subagent_start_costituzione.py.DISABLED`). E stato disabilitato in qualche sessione precedente.

---

## 3. CONFRONTO SNCP vs ALTERNATIVE

### SNCP (nostro sistema)

**Vantaggi confermati:**

- Markdown leggibile da umani e da AI
- Git-friendly: storia completa, diff chiari, rollback
- Zero dipendenze esterne (BM25 pure Python)
- Multi-progetto nativo (6 progetti distinti)
- Quality validation con quality-check.py
- Offline-first

**Limitazioni confermate:**

- Token cost: tutto il contesto iniettato dal hook va nella context window
- No semantic search (BM25 e keyword-only)
- Reports vecchi accumulati: il git status mostra 30+ file report eliminati ma ancora tracciati

### Claude Auto-Memory (integrato)

**Vantaggi:**

- Zero sforzo: Claude scrive da solo
- Integrato nativamente: nessun hook da mantenere
- 200 righe caricate automaticamente

**Limitazioni:**

- Machine-local: non sincronizzato
- Nessun controllo su cosa scrive
- Non multi-progetto (una directory per repo)

### Confronto diretto

| Aspetto | SNCP | Auto-Memory | CLAUDE.md |
|---------|------|-------------|-----------|
| Chi scrive | Cervella (manuale) | Claude (auto) | Noi + regole fisse |
| Cosa contiene | Stato progetto, decisioni | Pattern scoperti | Regole operative |
| Scope | Multi-progetto | Per-repo | Global/project |
| Token cost | Controllabile | ~200 righe fisso | ~200 righe fisso |
| Ispezionabile | Si | Si | Si |
| Git-synced | Si | No (machine-local) | Si |

**Conclusione del confronto:** I tre sistemi sono COMPLEMENTARI, non concorrenti. SNCP gestisce lo stato del progetto (COSA stiamo facendo, decisioni prese). Auto-memory gestisce pattern tecnici (COME funziona la codebase). CLAUDE.md gestisce le regole operative (CHI siamo, come lavoriamo).

---

## 4. ANALISI SNCP ATTUALE - Cosa Funziona, Cosa Migliorare

### Cosa Funziona Bene (da non toccare)

1. **PROMPT_RIPRESA con limite 150 righe** - Il limite e corretto. Il nostro PROMPT_RIPRESA cervellaswarm e a 119 righe. Sano.

2. **Session hook snello** - Il `session_start_swarm.py` v3.1.0 inietta solo ~600 chars (era ~4800). Riduzione 87%. Questo e ottimo.

3. **PROMPT_RIPRESA_MASTER come index** - Un file di puntatori a 53 righe che rimanda ai specifici. Pattern efficiente.

4. **Archivio con struttura temporale** - `.sncp/archivio/2026-01/` categorizza lezioni, ricerche, idee obsolete. Corretto.

5. **SNCP 5.0 gia implementato** - Progressive disclosure (S327), Consolidation Scheduler (S328), Explainable Search, Memory Ontology 5 types. Queste feature sono gia live.

### Problemi Identificati

**P1 - Reports nel limbo (git status):**
Il git status mostra 30+ file in `.sncp/progetti/cervellaswarm/reports/` marcati come `D` (deleted). Questi file esistono nel repo git ma sono stati eliminati localmente senza commit. Sono inutili: il contenuto e in sessioni passate (gennaio-febbraio 2026) e gia archiviate. Il problema e che appaiono nel git status ad ogni sessione creando rumore.
- **Soluzione:** `git add -A .sncp/progetti/cervellaswarm/reports/ && git commit -m "cleanup: remove old session reports"` nella prossima sessione con la Regina.

**P2 - subagent_context_inject.py mancante:**
Il file `subagent_context_inject.py` e menzionato in `CervellaSwarm/CLAUDE.md` come hook attivo ma non esiste. Esiste solo `subagent_start_costituzione.py.DISABLED`. Il CLAUDE.md dice "Hook Attivi" ma uno degli hook e disabilitato/rimosso. Crea aspettative false.
- **Soluzione:** Aggiornare `CervellaSwarm/CLAUDE.md` per riflettere gli hook realmente attivi (session_start_swarm.py, memory_flush_auto.py, subagent_stop.py).

**P3 - PROMPT_RIPRESA_MASTER non aggiornato:**
Il MASTER dice "Ultimo aggiornamento: 21 Febbraio 2026 - Sessione 384" e la entry di CervellaSwarm cita S385. Siamo alla S430. E desincronizzato di 46 sessioni.
- **Soluzione:** Alla prossima sessione, aggiornare la entry CervellaSwarm nel MASTER.

**P4 - Token cost dei CLAUDE.md multipli:**
Con 3 CLAUDE.md caricati (global + project + insiders) + auto-memory (200 righe) + hook session start, stimiamo 3000-4000 token usati solo per il contesto fisso prima di qualsiasi lavoro. La docs Claude Code dice "target under 200 lines per file". Il nostro global CLAUDE.md e a ~200 righe, il project e a ~80 righe. Siamo nel range corretto.

---

## 5. PATTERN COMUNITA - Cosa Fanno i Big Team

### Path-specific rules (novita 2026)

Claude Code supporta ora `.claude/rules/*.md` con YAML frontmatter `paths:` per caricare regole SOLO quando si lavora su certi file. Esempio:

```yaml
---
paths:
  - "packages/lingua-universale/**/*.py"
---
# Regole LU Development
- Sempre aggiungere test per ogni modulo
```

Questo e utile per noi: le regole specifiche per i package LU potrebbero caricarsi solo quando lavoriamo su quei file invece di essere sempre in context.

### Skills vs Rules

Claude Code ha una distinzione importante:
- **Rules** (.claude/rules/): caricate ogni sessione o quando file matching vengono aperti
- **Skills** (se supportati): caricano on-demand solo quando invocati

Per SNCP questo suggerisce che le roadmap e i report non dovrebbero mai essere caricate via hook. Dovrebbero essere lette on-demand (Read tool) quando servono.

### SubagentStart per contesto specifico degli agenti

Il hook SubagentStart puo iniettare contesto diverso per agenti diversi. Esempio: il Researcher riceve solo documentazione di ricerca, il Backend solo info architettura. Questo e il pattern che avevamo implementato con `subagent_start_costituzione.py` prima di disabilitarlo.

**Considerazione:** Vale la pena rivalutare un SubagentStart hook leggero (~200 chars) che inietti il ruolo dell'agente. Il `_SHARED_DNA.md` gia presente svolge questa funzione via CLAUDE.md.

---

## 6. RACCOMANDAZIONI CONCRETE

### Immediato (prossima sessione Regina)

1. **Committare i file deleted del reports:** Rimuovere i 30+ report obsoleti dal tracking git. Sono noise puro.

2. **Aggiornare CervellaSwarm/CLAUDE.md:** Togliere `subagent_context_inject.py` dalla lista hook attivi. Aggiungere `subagent_stop.py`.

3. **Aggiornare PROMPT_RIPRESA_MASTER:** Entry CervellaSwarm aggiornata a S430.

### Breve termine (MC4 o MC5)

4. **Esplorare .claude/rules/ con path-specific:** Per le regole specifiche dei package LU. Riduce il contesto globale.

5. **Rivalutare SubagentStart hook:** Un hook leggero che inietti l'agent type e il progetto corrente. Il `subagent_stop.py` gia registra il completion, avrebbe senso avere il corrispondente start.

### Da NON fare

- NON migrare SNCP a database: il vantaggio e la leggibilita markdown + git
- NON aggiungere vector search: BM25 e sufficiente per le nostre dimensioni
- NON rimuovere il limite 150 righe PROMPT_RIPRESA: e la protezione piu importante
- NON centralizzare tutta la memoria in un unico file: la separazione per progetto e corretta

---

## 7. VALUTAZIONE SNCP ATTUALE

| Dimensione | Score | Note |
|------------|-------|------|
| Struttura | 9.5/10 | Multi-progetto, archivio, limiti applicati |
| Token efficiency | 8.5/10 | Hook snello (v3.1.0), ma 3 CLAUDE.md pesano |
| Completezza | 9.0/10 | SNCP 5.0 implementato (progressive disclosure, consolidation) |
| Manutenzione | 7.5/10 | 3 problemi identificati (reports, hook doc, master stale) |
| Allineamento industry | 9.0/10 | Pattern corretti: files-as-memory, progressive disclosure |

**Score globale: 8.7/10** (era 8.8/10 prima di SNCP 5.0, ora leggermente giu per i 3 problemi di manutenzione)

---

## 8. DOMANDE APERTE PER LA REGINA

1. Il `memory_flush_auto.py` - cosa fa esattamente? (non lo abbiamo analizzato in questa sessione)
2. Il database `swarm_memory.db` popolato da `subagent_stop.py` - viene mai letto? Da chi?
3. Vale la pena riabilitare un SubagentStart hook? Il DNA viene iniettato via CLAUDE.md degli agenti, un hook aggiungerebbe solo il progetto corrente.

---

*"Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*
*Cervella Researcher - S431 - 2026-03-06*
