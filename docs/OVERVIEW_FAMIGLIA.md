# OVERVIEW FAMIGLIA - CervellaSwarm

> **Versione:** 1.0.0
> **Data:** 4 Gennaio 2026 - Sessione 81
> **"È il nostro team! La nostra famiglia digitale!"**

---

```
+------------------------------------------------------------------------------+
|                                                                              |
|   CERVELLASWARM - LA FAMIGLIA COMPLETA                                       |
|                                                                              |
|   17 membri | 4 livelli | 1 missione: LIBERTA GEOGRAFICA                    |
|                                                                              |
+------------------------------------------------------------------------------+
```

---

## LA GERARCHIA

```
                         +-------------------------+
                         |      LA REGINA          |
                         |    (Tu - Opus 4.5)      |
                         |                         |
                         | Coordina, DELEGA,       |
                         | MAI edit diretti!       |
                         +-----------+-------------+
                                     |
           +-------------------------+-------------------------+
           |                         |                         |
           v                         v                         v
   +---------------+         +---------------+         +---------------+
   | GUARDIANA     |         | GUARDIANA     |         | GUARDIANA     |
   |   QUALITA     |         |     OPS       |         |   RICERCA     |
   |    (Opus)     |         |    (Opus)     |         |    (Opus)     |
   |               |         |               |         |               |
   | Verifica code |         | Security +    |         | Verifica studi|
   | standard, test|         | deploy, infra |         | fonti, qualita|
   +---------------+         +---------------+         +---------------+
                                     |
                                     |
   +-------------------------------------------------------------------+
   |                        12 API WORKER (Sonnet)                      |
   +-------------------------------------------------------------------+
           |           |           |           |           |
           v           v           v           v           v
       Frontend    Backend     Tester    Reviewer   Researcher
           |           |           |           |           |
           v           v           v           v           v
    Scienziata  Ingegnera  Marketing   DevOps      Docs
           |           |
           v           v
        Data     Security
```

---

## LE 16 RAGAZZE - CHI FA COSA

| # | Nome | Model | Specializzazione | Quando Usarla |
|---|------|-------|------------------|---------------|
| 1 | **cervella-orchestrator** | Opus | La Regina, coordina tutto | Task complessi multi-team |
| 2 | **cervella-guardiana-qualita** | Opus | Verifica code/standard | Prima di merge |
| 3 | **cervella-guardiana-ops** | Opus | Security + infrastruttura | Deploy, audit sicurezza |
| 4 | **cervella-guardiana-ricerca** | Opus | Verifica studi | Validare ricerche |
| 5 | **cervella-frontend** | Sonnet | React, CSS, UI/UX | Componenti, styling |
| 6 | **cervella-backend** | Sonnet | Python, FastAPI, API | Endpoint, logica, DB |
| 7 | **cervella-tester** | Sonnet | Testing, Debug, QA | Scrivere test, trovare bug |
| 8 | **cervella-reviewer** | Sonnet | Code review | Review finale |
| 9 | **cervella-researcher** | Sonnet | Ricerca TECNICA | Prima di implementare |
| 10 | **cervella-scienziata** | Sonnet | Ricerca STRATEGICA | Mercato, competitor |
| 11 | **cervella-ingegnera** | Sonnet | Analisi codebase | Tech debt, refactoring |
| 12 | **cervella-marketing** | Sonnet | UX strategy, copy | Posizionamento UI |
| 13 | **cervella-devops** | Sonnet | Deploy, CI/CD | Infrastruttura |
| 14 | **cervella-docs** | Sonnet | Documentazione | README, guide |
| 15 | **cervella-data** | Sonnet | SQL, analytics | Query, database |
| 16 | **cervella-security** | Sonnet | Audit sicurezza | Vulnerabilita |

---

## STRUTTURA COMUNE AGENTI

Ogni agente ha la stessa struttura:

```
+-------------------------------------------------------------+
|  FRONTMATTER YAML                                           |
|  ---                                                        |
|  name: cervella-[nome]                                      |
|  version: 1.0.0                                             |
|  updated: 2026-01-02                                        |
|  description: [specializzazione]                            |
|  tools: [lista tools]                                       |
|  model: sonnet | opus                                       |
|  ---                                                        |
+-------------------------------------------------------------+
|  PRIMA DI TUTTO - LEGGI LA COSTITUZIONE                    |
|  @~/.claude/COSTITUZIONE.md                                |
+-------------------------------------------------------------+
|  REGOLA DECISIONE AUTONOMA                                 |
|  - PROCEDI SE: path chiaro, problema definito              |
|  - UNA DOMANDA SE: 2+ interpretazioni valide               |
|  - STOP SE: azione irreversibile                           |
+-------------------------------------------------------------+
|  DNA DI FAMIGLIA - CervellaSwarm                           |
|  - Chi siamo (Rafa = CEO, Cervella = Partner)              |
|  - Filosofia ("Lavoriamo in pace!")                        |
|  - Obiettivo (LIBERTA GEOGRAFICA)                          |
|  - Come parlo (FEMMINILE, calma, precisione)               |
+-------------------------------------------------------------+
|  OUTPUT ATTESO (COMPATTO!) - MAX 150 TOKENS!               |
|                                                             |
|  ## [Nome Task]                                             |
|  **Status**: OK | FAIL | BLOCKED                           |
|  **Fatto**: [1 frase max]                                  |
|  **File**: [lista, max 5]                                  |
|  **Next**: [SE serve]                                      |
+-------------------------------------------------------------+
```

---

## GLI SCRIPTS PRINCIPALI

### spawn-workers.sh (v1.4.0) - LA MAGIA!

Apre finestre worker AUTOMATICAMENTE!

```bash
# Worker singoli
./spawn-workers.sh --backend
./spawn-workers.sh --frontend
./spawn-workers.sh --tester

# Combinazioni
./spawn-workers.sh --backend --frontend
./spawn-workers.sh --all                  # backend + frontend + tester

# Guardiane (Opus)
./spawn-workers.sh --guardiana-qualita
./spawn-workers.sh --guardiana-ops
./spawn-workers.sh --guardiana-ricerca
./spawn-workers.sh --guardiane            # Tutte e 3

# Lista
./spawn-workers.sh --list
```

**TUTTI I WORKER:**
`--backend, --frontend, --tester, --docs, --reviewer, --devops, --researcher, --data, --security, --scienziata, --ingegnera`

**FEATURE:**
- Auto-close quando nessun task
- Notifiche macOS (Glass sound)
- Prompt automatico iniettato
- Worker cerca task in .swarm/tasks/

---

### anti-compact.sh (v1.6.0) - SALVAVITA!

Quando il contesto sta finendo:

```bash
./anti-compact.sh                     # Checkpoint + spawn nuova finestra
./anti-compact.sh --no-spawn          # Solo checkpoint
./anti-compact.sh --message "testo"   # Con messaggio custom
```

**COSA FA:**
1. FERMA tutto
2. SALVA (git add + commit + push)
3. AGGIORNA PROMPT_RIPRESA.md con istruzioni
4. APRE nuova finestra VS Code (con task automatico)

---

### triple-ack.sh (v2.0.0) - Pattern Apple Style

3 step per confermare task:

```bash
./triple-ack.sh received TASK_001     # "Ho ricevuto"
./triple-ack.sh understood TASK_001   # "Ho capito"
./triple-ack.sh status TASK_001       # Mostra stato
```

---

### Altri scripts

| Script | Cosa fa |
|--------|---------|
| `task_manager.py` | Gestione task (list, ready, working, done) |
| `monitor-status.sh` | Monitoraggio stato .swarm/ |
| `dashboard.sh/.py` | Dashboard ASCII |
| `shutdown-sequence.sh` | Chiusura graceful |
| `checklist-pre-merge.sh` | Checklist prima merge |

---

## IL FLUSSO DI LAVORO

```
1. RAFA -> da task alla REGINA

2. REGINA -> analizza, divide in sub-task

3. REGINA -> scrive task in .swarm/tasks/TASK_XXX.md

4. REGINA -> spawna worker: ./spawn-workers.sh --backend

5. WORKER -> legge task, crea .working, lavora

6. WORKER -> finisce, crea .done + _output.md

7. GUARDIANA -> verifica qualita (se Livello 2-3)

8. REGINA -> raccoglie risultati, riporta a Rafa
```

---

## I 3 LIVELLI DI RISCHIO

| Livello | Tipo | Esempio | Chi Verifica |
|---------|------|---------|--------------|
| **1 BASSO** | docs, commenti, styling | README, CSS | Regina |
| **2 MEDIO** | feature nuove, refactoring | Nuovo endpoint | Guardiana Qualita |
| **3 ALTO** | deploy, auth, dati sensibili | Production deploy | Guardiana Ops + Rafa |

---

## STRUTTURA .swarm/

```
.swarm/
+-- tasks/              # Task per i worker
|   +-- TASK_001.md     # Il task
|   +-- TASK_001.ready  # Pronto per essere preso
|   +-- TASK_001.working # In lavorazione
|   +-- TASK_001.done   # Completato
|   +-- TASK_001_output.md # Output del worker
|
+-- status/             # Stato globale
+-- logs/               # Log spawn/attivita
+-- handoff/            # Comunicazione Regina <-> Worker
+-- prompts/            # Prompt iniettati ai worker
+-- runners/            # Script runner per ogni worker
+-- archive/            # Task archiviati
```

---

## FILE AGENTI

Tutti in: `~/.claude/agents/`

```
cervella-orchestrator.md      # La Regina (Opus)
cervella-guardiana-qualita.md # Guardiana (Opus)
cervella-guardiana-ops.md     # Guardiana (Opus)
cervella-guardiana-ricerca.md # Guardiana (Opus)
cervella-frontend.md          # Worker (Sonnet)
cervella-backend.md           # Worker (Sonnet)
cervella-tester.md            # Worker (Sonnet)
cervella-reviewer.md          # Worker (Sonnet)
cervella-researcher.md        # Worker (Sonnet)
cervella-scienziata.md        # Worker (Sonnet)
cervella-ingegnera.md         # Worker (Sonnet)
cervella-marketing.md         # Worker (Sonnet)
cervella-devops.md            # Worker (Sonnet)
cervella-docs.md              # Worker (Sonnet)
cervella-data.md              # Worker (Sonnet)
cervella-security.md          # Worker (Sonnet)
```

---

*"E il nostro team! La nostra famiglia digitale!"*

*Creato: 4 Gennaio 2026 - Sessione 81*
*Cervella & Rafa*
