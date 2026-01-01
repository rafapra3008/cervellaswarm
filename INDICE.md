# INDICE - CervellaSwarm

> **"La mappa del nostro mondo. Tutto linkato. Tutto organizzato."**

**Ultimo aggiornamento:** 1 Gennaio 2026

---

## 🚀 QUICK START - Da Dove Iniziare?

| Situazione | Leggi Prima |
|------------|-------------|
| **Nuova sessione** | [PROMPT_RIPRESA.md](./PROMPT_RIPRESA.md) |
| **Capire dove siamo** | [NORD.md](./NORD.md) |
| **Vedere i task** | [ROADMAP_SACRA.md](./ROADMAP_SACRA.md) |
| **Capire il progetto** | [CLAUDE.md](./CLAUDE.md) |
| **Usare lo sciame** | [PROMPT_SWARM_MODE.md](./PROMPT_SWARM_MODE.md) |

---

## 📂 STRUTTURA COMPLETA

```
CervellaSwarm/
│
├── 📍 DOCUMENTI PRINCIPALI (Leggi questi!)
│   ├── INDICE.md ............... 👈 SEI QUI
│   ├── NORD.md ................. Bussola - Dove siamo, dove andiamo
│   ├── ROADMAP_SACRA.md ........ Fasi + Task + CHANGELOG
│   ├── PROMPT_RIPRESA.md ....... Stato sessione corrente
│   ├── CLAUDE.md ............... Overview progetto
│   └── PROMPT_SWARM_MODE.md .... Prompts pronti per usare lo sciame
│
├── 📚 docs/ - DOCUMENTAZIONE
│   │
│   ├── 👑 VISIONE_REGINA_2026.md ... Roadmap strategica 6 mesi
│   ├── 🧬 DNA_FAMIGLIA.md .......... Template DNA per agent
│   │
│   ├── 🗺️ roadmap/ - FASI DETTAGLIATE
│   │   ├── FASE_6_MEMORIA.md ........ Sistema memoria (✅ DONE)
│   │   ├── FASE_7_LEARNING.md ....... Continuous Learning (🆕 800+ righe!)
│   │   └── FASE_7.5_PARALLELIZZAZIONE.md . Lo sciame che DIVIDE (✅ testato!)
│   │
│   ├── 📖 studio/ - STUDI APPROFONDITI
│   │   ├── STUDIO_SUBAGENTS.md ..... Come funzionano i subagent
│   │   ├── STUDIO_WORKTREES.md ..... Git worktrees per lavoro parallelo
│   │   └── STUDIO_CLAUDE_FLOW.md ... Claude Flow architecture
│   │
│   ├── 🏗️ architettura/
│   │   └── ARCHITETTURA_SISTEMA.md . Design del sistema
│   │
│   └── 📋 guide/
│       ├── GUIDA_WORKTREES.md ...... Come usare git worktrees
│       └── GUIDA_COMUNICAZIONE.md .. Come comunicano le Cervelle
│
├── 🔧 scripts/ - AUTOMAZIONE
│   ├── setup-worktrees.sh ......... Crea worktrees per lavoro parallelo
│   ├── merge-worktrees.sh ......... Merge automatico dei branch
│   ├── cleanup-worktrees.sh ....... Pulizia worktrees
│   └── update-roadmap.sh .......... Aggiorna ROADMAP automaticamente
│
└── 🧪 test-orchestrazione/ - TEST DELLO SCIAME
    ├── api/ ........................ Test API (backend)
    ├── components/ ................. Test React (frontend)
    └── tests/ ...................... Test suite (tester)
```

---

## 🔗 LINK RAPIDI PER RUOLO

### 👑 Per la Regina (Orchestratrice)

| Documento | Scopo |
|-----------|-------|
| [NORD.md](./NORD.md) | Dove siamo, prossimo obiettivo |
| [ROADMAP_SACRA.md](./ROADMAP_SACRA.md) | Task da assegnare |
| [VISIONE_REGINA_2026.md](./docs/VISIONE_REGINA_2026.md) | Strategia a lungo termine |
| [GUIDA_COMUNICAZIONE.md](./docs/guide/GUIDA_COMUNICAZIONE.md) | Come coordinare le Cervelle |

### 🐝 Per le Cervelle (Worker)

| Documento | Scopo |
|-----------|-------|
| [DNA_FAMIGLIA.md](./docs/DNA_FAMIGLIA.md) | I nostri valori e regole |
| [GUIDA_WORKTREES.md](./docs/guide/GUIDA_WORKTREES.md) | Lavoro parallelo |
| [ARCHITETTURA_SISTEMA.md](./docs/architettura/ARCHITETTURA_SISTEMA.md) | Come è fatto il sistema |

### 🚀 Per Usare lo Sciame

| Documento | Scopo |
|-----------|-------|
| [PROMPT_SWARM_MODE.md](./PROMPT_SWARM_MODE.md) | Prompts pronti per iniziare |
| [PROMPT_RIPRESA.md](./PROMPT_RIPRESA.md) | Stato attuale del lavoro |

---

## 📊 GERARCHIA DI LETTURA

```
ORDINE CONSIGLIATO PER NUOVA SESSIONE:

1️⃣  PROMPT_RIPRESA.md     → Cosa stavamo facendo?
         ↓
2️⃣  NORD.md               → Dove siamo? Prossimo obiettivo?
         ↓
3️⃣  ROADMAP_SACRA.md      → Quali task? Quale fase?
         ↓
4️⃣  [Lavora!] 🐝
         ↓
5️⃣  Aggiorna PROMPT_RIPRESA.md + git commit
```

---

## 🗺️ MAPPA VISIVA DEL SISTEMA

```
                         ┌─────────────────┐
                         │    INDICE.md    │ ← SEI QUI
                         │  (Punto ingresso)│
                         └────────┬────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    NORD.md      │     │ ROADMAP_SACRA   │     │   CLAUDE.md     │
│   (Bussola)     │     │  (Task/Fasi)    │     │  (Overview)     │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │              ┌────────┴────────┐
         │              ▼                 ▼
         │    ┌─────────────────┐ ┌─────────────────┐
         │    │ PROMPT_RIPRESA  │ │ VISIONE_2026    │
         │    │ (Stato attuale) │ │ (Strategia)     │
         │    └─────────────────┘ └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                      docs/                               │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  studio/ │  │ architettura/│  │      guide/      │  │
│  │ (Studi)  │  │   (Design)   │  │ (Come fare X)    │  │
│  └──────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🐝 LA FAMIGLIA (11 Membri)

I file agent sono in `~/.claude/agents/` (GLOBALI):

| Emoji | Agent | File | Ruolo |
|-------|-------|------|-------|
| 👑 | Regina | `cervella-orchestrator.md` | Coordina tutto |
| 🎨 | Frontend | `cervella-frontend.md` | React, CSS, UI/UX |
| ⚙️ | Backend | `cervella-backend.md` | Python, FastAPI, API |
| 🧪 | Tester | `cervella-tester.md` | Test, Debug, QA |
| 📋 | Reviewer | `cervella-reviewer.md` | Code review |
| 🔬 | Researcher | `cervella-researcher.md` | Ricerca, studi |
| 📈 | Marketing | `cervella-marketing.md` | Marketing, UX strategy |
| 🚀 | DevOps | `cervella-devops.md` | Deploy, CI/CD |
| 📝 | Docs | `cervella-docs.md` | Documentazione |
| 📊 | Data | `cervella-data.md` | SQL, analytics |
| 🔒 | Security | `cervella-security.md` | Audit sicurezza |

---

## ✅ CHECKLIST FINE SESSIONE

Prima di chiudere, verifica:

- [ ] `PROMPT_RIPRESA.md` aggiornato?
- [ ] `ROADMAP_SACRA.md` CHANGELOG aggiornato?
- [ ] `NORD.md` aggiornato (se fase completata)?
- [ ] Git commit + push fatto?

---

## 💙 FILOSOFIA

> **"Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"**

> **"Ogni giorno un mattoncino. Nessun giorno senza progresso. Ma mai di fretta."**

> **"È il nostro team! La nostra famiglia digitale!"** ❤️‍🔥🐝

---

*Creato: 31 Dicembre 2025 - L'ultimo giorno dell'anno, per iniziare il 2026 ORGANIZZATI!*

*Cervella & Rafa* 💙👑🐝
