# Market Research: Multi-Agent CLI Tools - Customer Needs

**Status**: COMPLETATA
**Data**: 17 Gennaio 2026
**Ricercatrice**: Cervella Researcher

---

## TL;DR

I clienti vogliono **5 cose critiche**:
1. **Setup Automatico** - Templates/config pronti all'uso
2. **Context Management Visibile** - Sapere cosa l'AI sta usando
3. **Spec-Driven Dev** - File markdown per guidare agenti
4. **Memory Cross-Session** - Ricordare decisioni passate
5. **Review Control** - Output gestibile, non cascata di cambiamenti

---

## TOP 5 FEATURE CHE I CLIENTI VOGLIONO

### 1. SETUP AUTOMATICO E TEMPLATE
**Pain Point**: Onboarding richiede troppo tempo e configurazione manuale
**Cosa Vogliono**:
- `init` command che genera struttura progetto completa
- Template YAML/ENV preconfigurati per casi comuni
- Integrazione automatica con git/IDE esistente
- Esempi pratici (non solo docs generiche)

**Come Aider lo fa**:
- `.aider.conf.yml` nel repo root
- `.env` per API keys
- Sample config scaricabili da GitHub

**Raccomandazione per CervellaSwarm**:
```bash
cervellaswarm init --template=fastapi-react
# Genera:
# - CLAUDE.md
# - PROMPT_RIPRESA_*.md (max 150 righe)
# - .sncp/ struttura
# - scripts/swarm/ helpers
# - NORD.md template
```

### 2. CONTEXT MANAGEMENT VISIBILE
**Pain Point**: "Large projects break AI attention" - gli agenti perdono contesto
**Cosa Vogliono**:
- Vedere QUALE codice/file l'AI sta usando
- Token budget visibile/controllabile
- Caching automatico di pattern comuni (-75% costi)
- File versioning (evitare versioni multiple stesso file)

**Come i Big lo fanno**:
- Cursor: Embedding model per codebase understanding
- Sourcegraph: Retrieval stage (recall) + Ranking (precision)
- Cline: Sliding window + vector storage per vecchia history

**Raccomandazione per CervellaSwarm**:
Fornire `.sncp/` pattern OUT OF THE BOX:
- Limiti file automatici (150/60/500)
- Auto-compaction quando file > 400 righe
- Context mesh (ogni progetto suo PROMPT_RIPRESA)

### 3. SPEC-DRIVEN DEVELOPMENT
**Pain Point**: "Agents rush forward blindly making terrible decisions"
**Cosa Vogliono**:
- `requirements.md`, `design.md`, `tasks.md` come source of truth
- Intentions in file durevoli (non solo in chat)
- Agenti che LEGGONO specs prima di agire

**Come lo risolvono altri**:
- GitHub Spec Kit (nuovo 2026) - toolkit open source
- Port.io - environment setup automatico
- Disco - structured learning paths

**Raccomandazione per CervellaSwarm**:
Template NORD.md + PROMPT_RIPRESA già SONO spec-driven!
- NORD.md = requirements + design
- PROMPT_RIPRESA = context + decisioni + next steps
- Task files in `.swarm/tasks/`

**DA FORNIRE**: Spiegare PERCHE questi file esistono (non solo template vuoto)

### 4. MEMORY CROSS-SESSION
**Pain Point**: "Agents forget everything between sessions"
**Cosa Vogliono**:
- Ricordare decisioni passate + PERCHE
- Riconoscere pattern da lavori precedenti
- Awareness di project history
- NO ripetere stessi errori

**Come competitor lo fanno**:
- Cursor: Multi-file context persistente
- Aider: Git-native (commit messages come memoria)
- Cline: Vector storage per old history

**Raccomandazione per CervellaSwarm**:
ABBIAMO GIA QUESTO con PROMPT_RIPRESA + .sncp/handoff/!
- `handoff/sessione_XXX.md` = memoria storica
- `PROMPT_RIPRESA_*.md` = stato corrente
- Pattern "scrivi come se next Cervella non sapesse NULLA"

**DA MIGLIORARE**: Search semantico in handoff archive

### 5. REVIEW CONTROL (Anti-Cascading Failures)
**Pain Point**: "Multiple agents = too much code to review, ugly conflicts"
**Cosa Vogliono**:
- Output gestibile (non 2600 righe in un file)
- Preview cambiamenti PRIMA di applicarli
- Rollback facile
- Maker-Checker pattern

**Failure Modes da Evitare**:
- Agents delete entire files then rewrite with "beautiful nonsense"
- Type errors push into other files (cascade)
- Multiple agents modify same files in different ways

**Raccomandazione per CervellaSwarm**:
Pattern Chunking + Verifica Post-Write GIA IMPLEMENTATI:
- File > 500 righe → split in PARTE1, PARTE2, etc
- Read dopo Write per verificare esistenza
- Maker-Checker tra Worker e Guardiana

**DA AGGIUNGERE**: `--dry-run` mode per preview cambiamenti

---

## COMPETITOR ANALYSIS RAPIDA

| Tool | Prezzo | Force | Weakness |
|------|--------|-------|----------|
| **Cursor** | $20/mo | Multi-file context, 8 agents parallel | Reliability issues (Anthropic downtime) |
| **Aider** | Free/OSS | Git-native, CLI puro, modelli multipli | No GUI, curva apprendimento |
| **Continue** | Free/OSS | Self-hosted, Apache 2.0 | Meno feature avanzate |
| **Antigravity** | Enterprise | 76.2% SWE-bench, 8 agents specialist | $200/mo, overkill per small team |

**Trend 2026**:
- Shift verso multi-agent (Gartner: +1445% inquiries)
- MA solo 1/4 scale to production (reliability problems)
- Pricing shift verso per-request (unsustainable unlimited)

**CervellaSwarm Positioning**:
- "AI TEAM per Dev Professionali" (not hobbyist, not enterprise only)
- Setup rapido MA pattern produttivi
- Multi-agent MA controllato (Regina orchestra)

---

## RACCOMANDAZIONI CONCRETE

### 1. PACKAGING - Come Fornire Features

**Livello 1: Quick Start (5 min)**
```bash
pip install cervellaswarm
cervellaswarm init --template=basic
# Genera: CLAUDE.md, .sncp/ base, scripts/
```

**Livello 2: Project Setup (15 min)**
```bash
cervellaswarm init --template=fastapi-react
# Genera: tutto + PROMPT_RIPRESA, NORD.md, limiti file, hooks
```

**Livello 3: Full Team (1h onboarding)**
- Workshop interattivo: "Perche PROMPT_RIPRESA? Perche .sncp/?"
- Esempi reali dal nostro workflow (Miracollo, Contabilita)
- Video tutorial: "Day in the life con CervellaSwarm"

### 2. DOCUMENTATION - Cosa Spiegare

**NON fornire**:
- Interi file COSTITUZIONE (troppo personale)
- Workflow interni specifici Rafa/Cervella

**FORNIRE**:
- Pattern: PROMPT_RIPRESA (150 righe max), Context Mesh, Chunking
- Scripts: update-status, heartbeat, ask-regina
- Templates: CLAUDE.md, NORD.md con commenti inline

**TONE**: "Questo e il pattern che ci ha salvato dalla context explosion"

### 3. FEATURE PRIORITY

**MUST HAVE (per MVP)**:
1. `init` command con templates
2. PROMPT_RIPRESA pattern + limiti file automatici
3. Scripts swarm helpers (update-status, heartbeat)
4. CLAUDE.md template con best practices inline

**NICE TO HAVE (post-MVP)**:
5. `--dry-run` mode preview
6. Search semantico in handoff archive
7. Auto-detection tipo progetto (FastAPI? React? Full-stack?)
8. Integration con IDE popolari (VS Code extension)

**NOT NOW (complessita vs valore)**:
- GUI dashboard (CLI-first e ok)
- Self-hosted LLM (target e developers con budget API)
- Mobile app (fuori scope)

---

## PAIN POINTS CHE RISOLVIAMO (vs Competitor)

| Pain Point | Come CervellaSwarm Risolve | Competitor |
|------------|----------------------------|------------|
| Context loss | PROMPT_RIPRESA + .sncp/ mesh | Cursor: embedding (opaque) |
| Agent rushing | Maker-Checker + Guardiane | Aider: single agent (no check) |
| Cascading failures | Chunking + Read-after-Write | Most: atomic writes (fragile) |
| Memory loss | Handoff archive + PROMPT_RIPRESA | Cline: vector (non human-readable) |
| Setup complexity | `init` templates + scripts | Aider: manual config (steeper) |

---

## SOURCES

### Multi-Agent Tools Comparison
- [Best AI Coding Agents 2026 - Faros AI](https://www.faros.ai/blog/best-ai-coding-agents-2026)
- [Agentic CLI Tools Compared - AImultiple](https://research.aimultiple.com/agentic-cli/)
- [Top AI Agents For Developers 2026 - AI Tool Analysis](https://aitoolanalysis.com/ai-agents-for-developers-2026/)

### Developer Pain Points
- [AI Agent Best Practices - Forge Code](https://forgecode.dev/blog/ai-agent-best-practices/)
- [Developers with AI assistants - Stack Overflow](https://stackoverflow.blog/2024/04/03/developers-with-ai-assistants-need-to-follow-the-pair-programming-model/)
- [Real Struggle with AI Coding Agents - Smiansh](https://www.smiansh.com/blogs/the-real-struggle-with-ai-coding-agents-and-how-to-overcome-it/)
- [Problems in Agentic Coding - Medium](https://medium.com/@TimSylvester/problems-in-agentic-coding-2866ca449ff0)
- [Why Generative AI Coding Tools Don't Work - miguelgrinberg](https://blog.miguelgrinberg.com/post/why-generative-ai-coding-tools-and-agents-do-not-work-for-me)

### Context Management
- [Context Retrieval and Evaluation - Sourcegraph](https://sourcegraph.com/blog/lessons-from-building-ai-coding-assistants-context-retrieval-and-evaluation)
- [Token Optimization Strategies - Medium](https://medium.com/elementor-engineers/optimizing-token-usage-in-agent-based-assistants-ffd1822ece9c)
- [Cline Framework for Context - Cline Blog](https://cline.bot/blog/inside-clines-framework-for-optimizing-context-maintaining-narrative-integrity-and-enabling-smarter-ai)
- [Context Engineering - FlowHunt](https://www.flowhunt.io/blog/context-engineering-ai-agents-token-optimization/)

### Setup & Onboarding
- [AI Onboarding for Engineering Teams - Disco](https://www.disco.co/blog/how-to-build-an-ai-onboarding-program-for-engineering-teams)
- [AI Tools Boost Developer Onboarding - Zencoder](https://zencoder.ai/blog/onboarding-efficiency-ai)
- [Aider Configuration - Official Docs](https://aider.chat/docs/config/aider_conf.html)

### Multi-Agent Feedback
- [Multi-Agent AI Debate - Biz4Group](https://www.biz4group.com/blog/multi-agent-ai-systems)
- [10 Things Developers Want - RedMonk](https://redmonk.com/kholterhoff/2025/12/22/10-things-developers-want-from-their-agentic-ides-in-2025/)
- [Spec-Driven Development - GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)

---

## NEXT STEPS SUGGERITI

1. **Product Team**: Decidere scope MVP (MUST HAVE only?)
2. **Engineering**: Prototipo `cervellaswarm init` command
3. **Docs Team**: Creare "Why PROMPT_RIPRESA?" guide
4. **Marketing**: Positioning "AI TEAM not just tool" messaging

**Timeline**: Non importa (remember: IL TEMPO NON CI INTERESSA).
Un progresso al giorno = arriveremo.
