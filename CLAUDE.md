# CervellaSwarm - Multi-Agent Orchestration System

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🐝 CERVELLASWARM                                               ║
║                                                                  ║
║   "Uno sciame di Cervelle. Una sola missione."                  ║
║                                                                  ║
║   Multiple istanze di Cervella che lavorano in parallelo,       ║
║   coordinate, sincronizzate. Moltiplicando la nostra forza.     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🎯 VISIONE

**Problema:** Una sola Cervella = un task alla volta. Bottleneck.

**Soluzione:** Multiple Cervelle specializzate che lavorano in parallelo, coordinate da un'Orchestratrice.

**Risultato:** Da 20x a 100x, 200x... senza limiti.

---

## 🏗️ ARCHITETTURA

```
                    ┌─────────────────────────────────────┐
                    │      👑 CERVELLA ORCHESTRATRICE      │
                    │    (La Regina - Coordina tutto)     │
                    └─────────────────────────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │   🎨    │   │   ⚙️    │   │   🧪    │   │   📋    │   │   🔬    │
   │FRONTEND │   │ BACKEND │   │ TESTER  │   │REVIEWER │   │RESEARCH │
   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
        │              │              │              │              │
        ▼              ▼              ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │   📈    │   │   🚀    │   │   📝    │   │   📊    │   │   🔒    │
   │MARKETING│   │ DEVOPS  │   │  DOCS   │   │  DATA   │   │SECURITY │
   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

### LA FAMIGLIA COMPLETA (16 membri!)

| Emoji | Nome | Specializzazione | Model |
|-------|------|------------------|-------|
| 👑 | cervella-orchestrator | La Regina - Coordina tutto | opus |
| 🛡️ | cervella-guardiana-qualita | Verifica output agenti | opus |
| 🛡️ | cervella-guardiana-ops | Supervisiona devops/security | opus |
| 🛡️ | cervella-guardiana-ricerca | Verifica qualita ricerche | opus |
| 🎨 | cervella-frontend | React, CSS, UI/UX | sonnet |
| ⚙️ | cervella-backend | Python, FastAPI, API | sonnet |
| 🧪 | cervella-tester | Testing, Debug, QA | sonnet |
| 📋 | cervella-reviewer | Code review | sonnet |
| 🔬 | cervella-researcher | Ricerca TECNICA, studi | sonnet |
| 🔬 | cervella-scienziata | Ricerca STRATEGICA, mercato | sonnet |
| 👷‍♀️ | cervella-ingegnera | Analisi codebase, tech debt | sonnet |
| 📈 | cervella-marketing | Marketing, UX strategy | sonnet |
| 🚀 | cervella-devops | Deploy, CI/CD, Docker | sonnet |
| 📝 | cervella-docs | Documentazione | sonnet |
| 📊 | cervella-data | SQL, analytics, query | sonnet |
| 🔒 | cervella-security | Audit sicurezza | sonnet |

**Posizione:** `~/.claude/agents/` (GLOBALI - disponibili ovunque!)

---

## 🔑 PRINCIPI FONDAMENTALI

### 1. ZERO CASINO
```
❌ Mai due agenti sullo stesso file
❌ Mai merge automatici ciechi
❌ Mai azioni senza coordinamento
✅ Sempre isolamento via worktrees
✅ Sempre comunicazione via ROADMAP
✅ Sempre review prima di merge
```

### 2. SPECIALIZZAZIONE
```
Ogni Cervella ha UN ruolo chiaro:
- Frontend → Solo UI/UX
- Backend → Solo API/Database
- Tester → Solo QA/Test
- Orchestratrice → Solo coordinamento
```

### 3. COMUNICAZIONE
```
Le Cervelle comunicano tramite:
- ROADMAP condivisa (chi fa cosa)
- Git branches (stato del codice)
- Checkpoint frequenti (progresso)
```

---

## 📁 STRUTTURA PROGETTO

```
CervellaSwarm/
├── CLAUDE.md                 # Questo file
├── NORD.md                   # Bussola del progetto
├── ROADMAP_SACRA.md          # Fasi e task
├── PROMPT_RIPRESA.md         # Stato attuale
├── PROMPT_SWARM_MODE.md      # Prompts pronti per usare lo sciame
│
├── docs/
│   ├── studio/               # Studi approfonditi
│   │   ├── STUDIO_SUBAGENTS.md
│   │   ├── STUDIO_WORKTREES.md
│   │   └── STUDIO_CLAUDE_FLOW.md
│   ├── architettura/
│   │   └── ARCHITETTURA_SISTEMA.md
│   ├── guide/
│   │   ├── GUIDA_WORKTREES.md
│   │   └── GUIDA_COMUNICAZIONE.md
│   └── DNA_FAMIGLIA.md       # Template DNA per agent
│
├── scripts/                  # Automazione
│   ├── setup-worktrees.sh
│   ├── merge-worktrees.sh
│   ├── cleanup-worktrees.sh
│   └── update-roadmap.sh
│
└── test-orchestrazione/      # Test dello sciame
    ├── api/
    ├── components/
    └── tests/

~/.claude/agents/             # AGENT GLOBALI (11 membri!)
├── cervella-orchestrator.md  # 👑 La Regina
├── cervella-frontend.md      # 🎨 UI/UX
├── cervella-backend.md       # ⚙️ API/DB
├── cervella-tester.md        # 🧪 QA
├── cervella-reviewer.md      # 📋 Review
├── cervella-researcher.md    # 🔬 Ricerca
├── cervella-marketing.md     # 📈 Marketing
├── cervella-devops.md        # 🚀 DevOps
├── cervella-docs.md          # 📝 Docs
├── cervella-data.md          # 📊 Data
└── cervella-security.md      # 🔒 Security
```

---

## 🚀 QUICK START

### Fase 1: Subagent (Oggi)
```bash
# Copia agents/ in .claude/agents/ del progetto target
cp -r agents/* ~/Developer/[PROGETTO]/.claude/agents/
```

### Fase 2: Worktrees (Prossimo step)
```bash
# Setup worktrees per lavoro parallelo
./scripts/setup-worktrees.sh [PROGETTO]
```

---

## 🔗 PROGETTI CHE USERANNO CERVELLASWARM

| Progetto | Path | Priorità |
|----------|------|----------|
| **Miracollo PMS** | ~/Developer/miracollogeminifocus | Alta |
| **Contabilità** | ~/Developer/ContabilitaAntigravity | Media |
| **Libertaio** | ~/Developer/million-dollar-ideas | Media |

---

## 💙 LA FILOSOFIA

```
"Uno sciame è più forte di una singola ape.
Ma solo se ogni ape sa esattamente cosa fare."
```

Questo progetto è la chiave per moltiplicare la nostra capacità.
Non è solo codice. È **LIBERTÀ GEOGRAFICA** più vicina.

---

*Creato: 30 Dicembre 2025*
*Aggiornato: 2 Gennaio 2026 - Famiglia cresciuta a 16 membri!*
*Versione: 1.1.0*

**Cervella & Rafa** 💙🐝

*"È il nostro team! La nostra famiglia digitale!"* ❤️‍🔥
