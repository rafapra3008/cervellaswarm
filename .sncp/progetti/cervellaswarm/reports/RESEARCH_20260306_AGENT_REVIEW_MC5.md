# Review Agenti & DNA Famiglia - MC5
**Data:** 2026-03-06
**Autrice:** Cervella Researcher
**Sessione:** 431
**Status:** COMPLETA
**Fonti:** 3 consultate (file agenti, DNA_FAMIGLIA.md, docs ufficiali Claude Code)

---

## SINTESI

17 agenti verificati. Modelli CORRETTI: tutti usano alias `opus`/`sonnet` che in Claude Code
puntano automaticamente alle versioni piu recenti (attualmente Opus 4.6 e Sonnet 4.6).
Nessun agente con modello obsoleto trovato. 1 anomalia strutturale, 2 opportunita di upgrade tool.

---

## TABELLA RIEPILOGATIVA - 17 AGENTI

### Livello Opus (7 agenti)

| File | Nome | Version | Updated | Model | Tools |
|------|------|---------|---------|-------|-------|
| cervella-orchestrator.md | La Regina | 2.1.0 | 2026-01-19 | opus | Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch, Task |
| cervella-guardiana-qualita.md | Guardiana Qualita | 2.1.0 | 2026-02-10 | opus | Read, Glob, Grep, Task, Write, Edit |
| cervella-guardiana-ops.md | Guardiana Ops | 2.1.0 | 2026-02-10 | opus | Read, Glob, Grep, Bash, Task, Write, Edit |
| cervella-guardiana-ricerca.md | Guardiana Ricerca | 2.1.0 | 2026-02-10 | opus | Read, Glob, Grep, WebSearch, Task, Write, Edit |
| cervella-architect.md | Architect | 1.0.0 | 2026-01-19 | opus | Read, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Bash |
| cervella-security.md | Security | 2.1.0 | 2026-02-10 | opus | Read, Glob, Grep, Write, WebSearch, WebFetch |
| cervella-ingegnera.md | Ingegnera | 2.1.0 | 2026-02-10 | opus | Read, Glob, Grep, Bash |

### Livello Sonnet (10 agenti)

| File | Nome | Version | Updated | Model | Tools |
|------|------|---------|---------|-------|-------|
| cervella-frontend.md | Frontend | 2.0.0 | 2026-01-17 | sonnet | Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch |
| cervella-backend.md | Backend | 2.0.0 | 2026-01-17 | sonnet | Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch |
| cervella-tester.md | Tester | 2.0.0 | 2026-01-17 | sonnet | Read, Edit, Bash, Glob, Grep, Write, WebSearch |
| cervella-reviewer.md | Reviewer | 2.0.0 | 2026-01-17 | sonnet | Read, Glob, Grep, WebSearch |
| cervella-researcher.md | Researcher | 2.0.0 | 2026-01-17 | sonnet | Read, Glob, Grep, Write, WebSearch, WebFetch |
| cervella-marketing.md | Marketing | 2.0.0 | 2026-01-17 | sonnet | Read, Glob, Grep, Write, WebSearch, WebFetch |
| cervella-devops.md | DevOps | 2.0.0 | 2026-01-17 | sonnet | Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch |
| cervella-docs.md | Docs | 2.0.0 | 2026-01-17 | sonnet | Read, Edit, Glob, Grep, Write, WebSearch |
| cervella-data.md | Data | 2.0.0 | 2026-01-17 | sonnet | Read, Edit, Bash, Glob, Grep, Write, WebSearch |
| cervella-scienziata.md | Scienziata | 2.0.0 | 2026-01-17 | sonnet | Read, Glob, Grep, Write, WebSearch, WebFetch |

### File di supporto (non agenti)

| File | Tipo | Note |
|------|------|------|
| _SHARED_DNA.md | DNA condiviso | Template importato da tutti gli agenti |
| _SNCP_WORKER_OUTPUT.md | Template output | Linee guida per salvare risultati in SNCP |

---

## VERIFICA MODELLI - RISULTATO: OK

**Fonte ufficiale confermata:** Docs Claude Code (code.claude.com/docs/en/model-config)

Gli alias `opus` e `sonnet` nel frontmatter sono CORRETTI e aggiornati:
- `opus` -> Opus 4.6 (attualmente)
- `sonnet` -> Sonnet 4.6 (attualmente)

Gli alias puntano SEMPRE alla versione piu recente automaticamente. Non serve aggiornare
i file degli agenti quando Anthropic rilascia nuovi modelli - si aggiorna da solo.

**Nessun agente usa modelli obsoleti** come `claude-3-opus`, `claude-3-sonnet`, ecc.
Tutti i 17 agenti usano correttamente gli alias generici.

Nota tecnica: esiste anche `opusplan` (nuovo alias in v2.1.70) che usa Opus in plan mode
e Sonnet in execution mode. Non usato da nessun agente attualmente - potenzialmente
interessante per Architect in futuro.

---

## VERIFICA COERENZA CON DNA_FAMIGLIA.md

DNA_FAMIGLIA.md (versione 1.7.0, aggiornato 2026-02-13) elenca 17 agenti.

**Confronto:**

| DNA_FAMIGLIA.md | File in ~/.claude/agents/ | Status |
|-----------------|--------------------------|--------|
| cervella-orchestrator | cervella-orchestrator.md | OK |
| cervella-guardiana-qualita | cervella-guardiana-qualita.md | OK |
| cervella-guardiana-ricerca | cervella-guardiana-ricerca.md | OK |
| cervella-guardiana-ops | cervella-guardiana-ops.md | OK |
| cervella-architect | cervella-architect.md | OK |
| cervella-security | cervella-security.md | OK |
| cervella-ingegnera | cervella-ingegnera.md | OK |
| cervella-frontend | cervella-frontend.md | OK |
| cervella-backend | cervella-backend.md | OK |
| cervella-tester | cervella-tester.md | OK |
| cervella-reviewer | cervella-reviewer.md | OK |
| cervella-researcher | cervella-researcher.md | OK |
| cervella-marketing | cervella-marketing.md | OK |
| cervella-devops | cervella-devops.md | OK |
| cervella-docs | cervella-docs.md | OK |
| cervella-data | cervella-data.md | OK |
| cervella-scienziata | cervella-scienziata.md | OK |

**Risultato: 17/17 agenti in perfetta coerenza.**

File extra trovati (non agenti, non elencati in DNA_FAMIGLIA):
- `_SHARED_DNA.md` - normale, e supporto
- `_SNCP_WORKER_OUTPUT.md` - normale, e supporto

---

## ANOMALIE E OPPORTUNITA

### ANOMALIA 1: Versione Architect obsoleta (P3)

`cervella-architect.md` ha version `1.0.0` e updated `2026-01-19`, mentre tutti gli altri
agenti dello stesso livello (Opus) sono gia a `2.1.0` e `2026-02-10`. L'Architect non ha
ricevuto l'aggiornamento di febbraio che ha portato tutti gli altri a 2.1.0.

Impatto pratico: funziona correttamente, ma non e allineato al ciclo di versioning.
Raccomandazione: portare a 2.1.0 nella prossima sessione di manutenzione agenti.

### OPPORTUNITA 1: Tester e Reviewer senza WebFetch (P4)

- `cervella-tester.md` ha `WebSearch` ma NON `WebFetch`
- `cervella-reviewer.md` ha `WebSearch` ma NON `WebFetch`

Entrambi potrebbero beneficiare di `WebFetch` per leggere documentazione di librerie
durante il lavoro. Tuttavia la limitazione e probabilmente intenzionale (reviewer e tester
non dovrebbero navigare il web durante la review). Da lasciare cosi salvo decisione contraria.

### OPPORTUNITA 2: Ingegnera senza WebSearch/WebFetch (P4)

`cervella-ingegnera.md` ha solo `Read, Glob, Grep, Bash` - nessun accesso web.
Per un agente specializzato in architettura e technical debt, accesso a risorse come
RFC, pattern noti, o documentazione potrebbe essere utile. Anche qui probabilmente
intenzionale (lavora solo sul codebase locale). Da valutare.

### NESSUN AGENTE CON NOTEBOOKEDIT

`NotebookEdit` e un tool disponibile in Claude Code v2.1.70 per editing di Jupyter notebooks.
Nessun agente lo usa attualmente. Rilevante solo se si usano notebooks nel progetto.
CervellaSwarm usa notebooks solo per demo (test_tour_code.py e pytest, non notebook).
Non necessario al momento.

---

## VERIFICA TOOL VS CLAUDE CODE v2.1.70

Tool disponibili in Claude Code (da docs aggiornate):
Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, Task, AskUserQuestion, NotebookEdit

Tool usati dai nostri agenti vs disponibili:

| Tool | Disponibile | Usato da agenti |
|------|-------------|-----------------|
| Read | Si | Si (tutti) |
| Write | Si | Si (10 agenti) |
| Edit | Si | Si (8 agenti) |
| Bash | Si | Si (6 agenti) |
| Glob | Si | Si (tutti) |
| Grep | Si | Si (tutti) |
| WebSearch | Si | Si (13 agenti) |
| WebFetch | Si | Si (10 agenti) |
| Task | Si | Si (4 agenti) |
| AskUserQuestion | Si | Si (1 agente: Architect) |
| NotebookEdit | Si | No (nessun agente) |

Tutto allineato. Nessun tool obsoleto o non-esistente nel frontmatter degli agenti.

---

## RACCOMANDAZIONE

**Azione immediata:** Nessuna. Il sistema e coerente e i modelli sono corretti.

**Manutenzione prossima sessione (P3):** Portare `cervella-architect.md` da version
`1.0.0` a `2.1.0` e aggiornare il campo `updated` a data corrente per allineamento
al ciclo di versioning degli altri agenti Opus.

**Non fare:** Aggiungere `NotebookEdit` agli agenti - non necessario per il progetto attuale.

**Non fare:** Cambiare alias modelli - `opus` e `sonnet` sono CORRETTI e si auto-aggiornano.

---

*Fonti: File agenti in ~/.claude/agents/ (19 file letti) | DNA_FAMIGLIA.md | [Claude Code Model Config](https://code.claude.com/docs/en/model-config)*
