# RICERCA: Onboarding Best Practices - AI Agent Systems

> **Researcher:** Cervella Researcher
> **Data:** 3 Febbraio 2026
> **Scope:** Best practices onboarding per sistemi AI multi-agent

---

## EXECUTIVE SUMMARY

**TL;DR:** Il mercato 2026 ha standardizzato su:
- File configurazione in **root progetto** (CLAUDE.md, .cursorrules, AGENTS.md)
- **Onboarding progressivo** (non wizard massivo)
- **Context hierarchy** (global → project → folder)
- **Persistent memory** come differenziatore competitivo

**Raccomandazione:** SNCP è **AVANTI** rispetto al mercato su memoria persistente, ma deve migliorare UX onboarding iniziale.

---

## 1. COMPETITOR ANALYSIS

### 1.1 Claude Code

**File Configurazione:**
- `CLAUDE.md` - Root progetto (standard de facto)
- `~/.claude/CLAUDE.md` - Configurazione globale
- `.claude/commands/` - Comandi custom
- `.claude/skills/` - Skills riutilizzabili

**Onboarding:**
- Comando `/init` genera CLAUDE.md automatico analizzando codebase
- CLAUDE.md letto all'inizio di OGNI conversazione
- Hook system per automazioni

**Best Practices:**
- **Brevità:** < 500 righe per CLAUDE.md (consumano context!)
- **Hierarchy:** Global → Project → Subfolders
- **Skills:** File separati per logica riutilizzabile
- **Anti-pattern:** Over-specification (troppi dettagli = rumore)

**Fonti:**
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [CLAUDE.md Initialization Guide](https://egghead.io/claude-md-initialization-and-best-practices-in-claude-code~jae0x)
- [Creating Perfect CLAUDE.md](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/)

### 1.2 Cursor

**File Configurazione:**
- `.cursorrules` - File singolo (deprecato)
- `.cursor/rules/` - Cartella con file `.mdc` (modern approach 2026)
- Supporto scoped rules per folder specifiche

**Onboarding:**
- Command Palette: "Cursor Rules: Add .cursorrules"
- Auto-detect configurazione esistente
- Community templates (awesome-cursorrules repo)

**Best Practices:**
- **Modular rules:** File separati per scope diversi
- **Community-driven:** Riuso template esistenti
- **ROI:** 63% faster onboarding, 41% meno code review iterations

**Fonti:**
- [Mastering Cursor Rules](https://dev.to/anshul_02/mastering-cursor-rules-your-complete-guide-to-ai-powered-coding-excellence-2j5h)
- [Cursor AI Integration 2026](https://monday.com/blog/rnd/cursor-ai-integration/)
- [Awesome Cursorrules](https://github.com/PatrickJS/awesome-cursorrules)

### 1.3 Aider

**File Configurazione:**
- `.aider.conf.yml` - Main config
- `.aider.model.settings.yml` - Model settings
- `.aider.model.metadata.json` - Context windows
- `.env` - API keys
- `.aiderignore` - File ignore

**Onboarding:**
- Config file discovery: Home → Git Root → Current dir
- Priority: Last loaded wins
- Convention files auto-loaded

**Best Practices:**
- **Multi-location:** Cascading config (global → project)
- **Environment vars:** AIDER_xxx format
- **Conventions:** Auto-load CONVENTIONS.md

**Fonti:**
- [Aider Configuration](https://aider.chat/docs/config.html)
- [YAML Config File](https://aider.chat/docs/config/aider_conf.html)
- [Coding Conventions](https://aider.chat/docs/usage/conventions.html)

### 1.4 GitHub Copilot

**File Configurazione:**
- `.github/copilot-instructions.md` - Repo-level
- `.github/instructions/*.instructions.md` - Scoped instructions
- JSON-based config templates

**Onboarding:**
- Phased onboarding plan (Phase 1: Setup, Phase 2: Exploration)
- Copilot Coding Agent esplora codebase automaticamente
- CLI con specialized agents (Explore, Task)

**Status 2026:**
- Copilot Workspace sunset (May 2025)
- Focus su Coding Agents + CLI + MCP integration

**Fonti:**
- [Onboarding AI Peer Programmer](https://github.blog/ai-and-ml/github-copilot/onboarding-your-ai-peer-programmer-setting-up-github-copilot-coding-agent-for-success/)
- [Onboarding Plan Prompts](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/onboarding-plan)
- [GitHub Copilot CLI 2026](https://github.blog/changelog/2026-01-14-github-copilot-cli-enhanced-agents-context-management-and-new-ways-to-install/)

---

## 2. NAMING CONVENTIONS MERCATO

### Standard Emergenti 2026

| File Name | Standard | Tool | Purpose |
|-----------|----------|------|---------|
| `AGENTS.md` | **OPEN STANDARD** | Multi-tool | Tool-agnostic convention |
| `CLAUDE.md` | Claude-specific | Claude Code | Project context |
| `.cursorrules` | Legacy | Cursor | Deprecato |
| `.cursor/rules/` | Modern | Cursor | Modular rules |
| `.aider.conf.yml` | Aider-specific | Aider | Main config |
| `.github/copilot-instructions.md` | GitHub | Copilot | Repo instructions |
| `.aiassistant/rules/` | JetBrains | AI Assistant | Project rules |

### Convenzioni Generiche

- `AI.md` / `AI_INSTRUCTIONS.md` - General-purpose
- `CONTRIBUTING.md` - Respected by most LLMs (training data)
- `README.ai.md` - AI-focused readme separato
- `STYLEGUIDE.md` - Code style customization

### Hierarchical Patterns

**Esempio OpenAI repo:** 88 nested AGENTS.md files!

```
/AGENTS.md              # Root-level global guidance
/frontend/AGENTS.md     # Frontend-specific overrides
/backend/AGENTS.md      # Backend-specific rules
~/.agents.md            # Personal preferences
```

**Discovery:** Nearest file in tree wins (cascading override)

**Fonti:**
- [AI Agent File Naming Conventions](https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6)
- [Instruction Files Overview](https://aruniyer.github.io/blog/agents-md-instruction-files.html)
- [JetBrains AI Guidelines](https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/)

---

## 3. ONBOARDING UX PRINCIPLES

### 3.1 Modern Onboarding Flow (2026)

**TREND:** Wizard tradizionali → Interactive flows

**Limitazioni Wizards:**
- Limited functionality (solo setup tecnico)
- No hands-on learning (click "Next" senza capire)
- Low personalization (one-size-fits-all)
- High interaction cost (tedious)

**Modern Approach:**
- **Progressive disclosure:** Mostra solo ciò che serve
- **Contextual guidance:** Tooltip, hotspot, dialog in-app
- **Adaptive flows:** Basati su comportamento utente
- **Hands-on:** Esplorare facendo, non leggendo

**Fonti:**
- [Old vs New Onboarding](https://userpilot.com/blog/onboarding-wizard/)
- [Wizard UI Pattern](https://www.eleken.co/blog-posts/wizard-ui-pattern-explained)

### 3.2 CLI Onboarding Best Practices

**Golden Rules:**

1. **Show first command upfront**
   - "What's the command they'll use first?"
   - Don't hide behind 10 pages of docs

2. **Use CLI itself for onboarding**
   - Interactive prompts
   - Validation real-time
   - Feedback immediato

3. **Configuration patterns:**
   - Dot files (`.toolname`) per account/project
   - System-wide defaults overridable per-project
   - Environment variables come fallback

4. **Visual feedback:**
   - Colors (magenta, cyan, blue, green, gray)
   - Yellow/red per warnings/errors
   - Progress indicators

5. **Human-first design:**
   - Text-based UI, non cryptic commands
   - Help sempre accessibile
   - Error messages actionable

**Fonti:**
- [UX Patterns for CLI Tools](https://lucasfcosta.com/2022/06/01/ux-patterns-cli-tools.html)
- [3 Steps Awesome CLI UX](https://opensource.com/article/22/7/awesome-ux-cli-application)
- [CLI Design Best Practices](https://codyaray.com/2020/07/cli-design-best-practices)

### 3.3 Developer Onboarding Metrics

**Structured onboarding delivers:**
- Faster time-to-productivity
- Reduced learning curve
- Better knowledge retention
- Consistent quality

**Key Focus Areas:**
- Local dev setup (Docker, IDE)
- Testing frameworks
- Code quality tools
- Workflow documentation

**Fonti:**
- [Developer Onboarding Guide](https://www.cortex.io/post/developer-onboarding-guide)
- [Developer Onboarding Checklist](https://www.port.io/blog/developer-onboarding-checklist)

---

## 4. PERSISTENT MEMORY & MULTI-PROJECT CONTEXT

### 4.1 Problema Chiave Mercato

**LLMs tradizionali = STATELESS**
- Ogni conversazione riparte da zero
- No memory across sessions
- Context mixing tra progetti

### 4.2 Soluzioni Emergenti 2026

**ALMA-memory:**
- Persistent memory per AI agents
- Progress tracking progetti
- Multi-agent sharing
- Anti-patterns detection

**MCP (Model Context Protocol):**
- Memory across sessions
- **PROBLEMA:** Context separation progetti debole
- **ISSUE:** Data overlap su progetti simili

**Agentic Project Management (APM):**
- Real-world PM principles
- Context retention techniques
- Smooth transition quando context window pieno
- Specialized agents coordination

**Lindy Societies:**
- Shared memory across agents
- One agent learns → others benefit

### 4.3 Technical Architecture

**Standard Pattern:**
- Embeddings in vector database
- Semantic similarity search
- Context engineering as discipline

**Fonti:**
- [ALMA-memory](https://github.com/RBKunnela/ALMA-memory)
- [Memory MCP 2026](https://research.aimultiple.com/memory-mcp/)
- [Memory in Age of AI Agents](https://arxiv.org/abs/2512.13564)
- [Context-Aware Multi-Agent](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)

---

## 5. COMPETITIVE ADVANTAGES 2026

### 5.1 Cosa Differenzia Un AI Assistant

**Memory & Context (Top Priority):**
- Persistent memory across sessions
- Context windows 1M+ tokens
- Entire codebase in memory
- No forgetting previous steps

**Enterprise Features:**
- Context as competitive advantage
- Large-context = mission-critical work
- Trust & quality over speed alone

**Developer Productivity:**
- 75%+ developers use AI tools
- Competitive advantage = effective usage
- Balance speed/quality/trust

### 5.2 Unique Features Examples

**Cursor:**
- Composer mode (multi-file diffs)
- Semantic code search (entire codebase)
- Inline Tab-completions

**Claude:**
- Enterprise-grade large-context
- Mission-critical code analysis
- Data analysis at scale

**CodeConductor:**
- Context across workflows/tasks/iterations
- Remembers previous steps

**Fonti:**
- [AI Coding Assistants 2026 Trends](https://medium.com/@eitbiz/ai-coding-assistants-in-2026-transforming-modern-software-development-workflows-68a8ad5ed8fd)
- [Cursor vs Codex vs Claude](https://digitalstrategy-ai.com/2026/01/28/ai-software-development-2/)
- [Best AI Coding Assistants 2026](https://learn.ryzlabs.com/ai-coding-assistants/best-ai-coding-assistants-of-2026-what-developers-need-to-know)

---

## 6. RACCOMANDAZIONI PER CERVELLASWARM

### 6.1 Cosa SNCP Fa Bene (Keep)

✅ **Persistent Memory:**
- PROMPT_RIPRESA_*.md = Memory across sessions
- Multi-progetto NATIVO (.sncp/progetti/)
- Handoff system per session continuity

✅ **Hierarchical Context:**
- Global (.sncp/PROMPT_RIPRESA_MASTER.md)
- Per-progetto (PROMPT_RIPRESA_{progetto}.md)
- NORD.md per direzione

✅ **Multi-Agent Coordination:**
- 17 agents specialized
- Swarm rules chiare
- Task delegation framework

### 6.2 Gap da Colmare (Improve)

⚠️ **Onboarding UX:**
- NO comando `/init` automatico
- Setup manuale (error-prone)
- Documentazione scattered

⚠️ **File Limits Enforcement:**
- 150/500 righe - difficile rispettare
- Hook warn ma non prevengono
- Archivio manuale

⚠️ **Context Separation:**
- Progetti simili potrebbero mescolarsi
- Nessun namespace enforcement
- Rely on naming conventions

### 6.3 Azioni Concrete

**IMMEDIATE (Quick Wins):**

1. **Comando `/sncp-init`**
   - Analizza progetto corrente
   - Genera NORD.md + PROMPT_RIPRESA template
   - Setup .sncp/ structure automatico

2. **Onboarding Interactive**
   - Wizard: Nome progetto → Tipo → Stack
   - Output: File configurati pronti all'uso
   - Validation step-by-step

3. **File Limits Auto-Enforce**
   - Hook preventivo (block write se > limiti)
   - Auto-archivio quando threshold
   - Warning progressivo (70%, 85%, 95%)

**MEDIUM (Enhancement):**

4. **Context Namespace**
   - Project ID embedded in memory
   - Semantic search scoped by project
   - Prevent cross-project pollution

5. **Skills Library**
   - `.sncp/skills/` - Riutilizzabili
   - Per-project skills override
   - Swarm-wide skills sharing

6. **Documentation Hub**
   - Single page: "Getting Started with SNCP"
   - Video walkthrough
   - Example projects

**LONG-TERM (Innovation):**

7. **SNCP Protocol Spec**
   - Open standard come AGENTS.md
   - Tool-agnostic memory format
   - Community adoption

8. **Multi-Agent Memory Sharing**
   - What Researcher learns → available to Backend
   - Semantic memory pool
   - Anti-duplication

---

## 7. NOSTRI DIFFERENZIATORI

### Cosa Rende SNCP Unico

**1. NATIVE MULTI-PROJECT**
- Competitor: Single project o weak separation
- SNCP: First-class multi-project architecture

**2. SWARM COORDINATION**
- Competitor: Single agent o loosely coupled
- SNCP: 17 agents orchestrated by Regina

**3. PERSISTENT MEMORY DESIGN**
- Competitor: Vector DB bolt-on
- SNCP: File-based, human-readable, git-trackable

**4. ФИЛОСОФИЯ ITALIANA**
- "Lavoriamo in pace! Senza casino!"
- Focus on quality > speed
- Partnership model (Regina + Rafa)

### Come Comunicarlo

**Onboarding Message:**
```
CervellaSwarm non è "un altro AI assistant".

È una FAMIGLIA di 17 esperti che:
- RICORDANO tutto (memoria persistente)
- COLLABORANO tra loro (swarm coordination)
- CRESCONO con te (multi-project learning)

Mentre altri AI dimenticano dopo ogni sessione,
CervellaSwarm costruisce un CERVELLO per i tuoi progetti.
```

---

## 8. ERRORI COMUNI DA EVITARE

**Da Competitor Analysis:**

❌ **Over-specification** (Claude)
- Config file troppo lunghi
- Noise overwhelms signal
- Soluzione: Ruthless pruning

❌ **One-size-fits-all** (Wizards)
- No personalization
- Tedious for experts
- Soluzione: Adaptive flows

❌ **Context Mixing** (MCP)
- Projects blend together
- Data overlap
- Soluzione: Namespace enforcement

❌ **Stateless Design** (Traditional LLMs)
- No memory
- Repeat same questions
- Soluzione: Persistent storage

❌ **Documentation Overload**
- 10 pages before first command
- Lost users
- Soluzione: Show, don't tell

---

## 9. PROSSIMI STEP

**Per Ricerca Completa:**

1. [ ] Deep dive su MCP protocol specifics
2. [ ] Analyze ALMA-memory implementation
3. [ ] Study APM framework architecture
4. [ ] Review semantic search patterns
5. [ ] Benchmark context window usage SNCP vs competitors

**Per Implementazione:**

1. [ ] Draft `/sncp-init` command spec
2. [ ] Design onboarding wizard flow
3. [ ] Prototype file limits auto-enforcement
4. [ ] Define SNCP Protocol v1.0 spec
5. [ ] Create "Getting Started" guide

---

## 10. CONCLUSIONI

**SNCP è AVANTI sul mercato in:**
- Persistent memory (PROMPT_RIPRESA)
- Multi-project nativo
- Swarm coordination

**SNCP deve MIGLIORARE su:**
- Onboarding UX (wizard/init command)
- File limits enforcement (auto-archivio)
- Documentation accessibility

**OPPORTUNITÀ STRATEGICA:**
Open-source SNCP protocol → diventare lo **standard de facto** per multi-project AI memory.

**NEXT ACTION:**
Implementare `/sncp-init` command per abbattere barriera ingresso nuovi utenti.

---

*Ricerca completata: 3 Febbraio 2026*
*Cervella Researcher - CervellaSwarm*

**"Un'ora di ricerca risparmia dieci ore di codice sbagliato."**
