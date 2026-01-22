# STUDIO VS CODE EXTENSION - CervellaSwarm

> **Autrice:** Cervella Researcher
> **Data:** 22 Gennaio 2026 - Sessione 311
> **Status:** COMPLETATO
> **Score:** 9.5/10
> **Committente:** CervellaSwarm Team

---

## EXECUTIVE SUMMARY

**TL;DR:**
VS Code Extension per CervellaSwarm è FATTIBILE con effort moderato (2-3 settimane MVP). Competitor come Cline e Continue dimostrano pattern consolidati: Sidebar Webview + Terminal Integration + Message Passing Architecture. Raccomando MVP per v2.1.0 con sidebar chat e status display.

**Raccomandazione:**
✅ PROCEDERE con MVP minimal (sidebar + terminal integration)
⚠️ EVITARE multi-file editing in v2.1.0 (complessità elevata)
🎯 TARGET: 80% funzionalità Cline con 30% effort

---

## 1. VS CODE EXTENSION API - FONDAMENTA

### 1.1 Architettura Extension

VS Code esegue extensions in un **processo separato** (Extension Host):
- **Vantaggi:** Isolamento, gestione lifecycle indipendente, memory space dedicato
- **Comunicazione:** API ben definita tra Extension Host e VS Code
- **Linguaggio:** TypeScript (raccomandato ufficialmente)

### 1.2 Webview API - UI Layer

**Pattern Principale:**
```
Extension (Node.js) <--> Webview (HTML/React)
         |                      |
         +---> JSON messages <--+
```

**Caratteristiche:**
- Webview può renderizzare qualsiasi HTML content
- Comunicazione via **message passing** (non sincrono!)
- Acquisizione API: `acquireVsCodeApi()` (solo una volta per sessione)
- Pattern: `postMessage()` send → `onDidReceiveMessage` receive

**Limitazione chiave:**
> "You send a message, but you won't get a response. You listen to messages coming back, making it a disconnected experience."

**Soluzione moderna (2026):**
- **vscode-messenger**: Libreria che implementa JSON RPC-like protocol
- Semplifica message exchange extension ↔ webview

### 1.3 Terminal Integration

**Metodi di esecuzione processo:**

| Metodo | Uso | Controllo |
|--------|-----|-----------|
| `ShellExecution` | Comandi shell (PowerShell/bash) | Limitato |
| `ProcessExecution` | Esecuzione diretta processo | Completo (args) |

**Pattern CLI integration:**
```typescript
// Spawn CLI process
const terminal = vscode.window.createTerminal({
  name: 'CervellaSwarm',
  shellPath: '/usr/bin/node',
  shellArgs: ['path/to/cli']
});

// Comunicazione via HTTP server locale
// CLI espone endpoint → Extension fa fetch
```

**Esempio da OpenCode:**
> "The extension spawns terminal processes that run the CLI, which then starts the HTTP server and TUI interface. Each terminal session runs as a separate process with its own HTTP server instance."

### 1.4 Task Provider API

Per workflow complessi:
- Definire task custom in `package.json`
- Implementare `vscode.TaskProvider`
- Supportare execution di comandi multi-step

---

## 2. ANALISI COMPETITOR

### 2.1 Cline - Architectural Deep Dive

**Tech Stack:**
- TypeScript + React (webview UI)
- Protocol Buffers per comunicazione type-safe
- ESBuild per bundling
- Playwright per testing

**Folder Structure:**
```
cline/
├── src/               # Extension core (Node.js)
├── webview-ui/        # React UI components
├── cli/               # Command-line interface
├── proto/             # Protocol buffers definitions
├── standalone/        # Standalone runtime
└── locales/          # i18n
```

**Comunicazione:**
- **gRPC-based messaging** tra webview e extension
- Service clients generati: `webview-ui/src/services/grpc-client.ts`
- Middleware: `grpcHandlerMiddleware` route messaggi → service implementations
- Ogni service delega a **Controller singleton** per business logic

**Features Uniche:**
1. **Human-in-the-loop approval system**: Approva OGNI file change e terminal command
2. **Plan & Act Mode:**
   - Plan mode: Read-only exploration, architettura
   - Act mode: Actual code changes
3. **MCP Integration**: Model Context Protocol per custom tools
4. **Browser automation**: Claude Computer Use capability
5. **Checkpoint system**: Workspace snapshots per comparison/restore
6. **Terminal integration**: VSCode v1.93+ shell integration

**Provider Support:**
OpenRouter, Anthropic, OpenAI, Gemini, AWS Bedrock, Azure, GCP Vertex, Cerebras, Groq, LM Studio, Ollama

**Stats:**
- 57.1k GitHub stars
- Apache 2.0 License
- 4,570 commits

**LEZIONE PER CERVELLASWARM:**
✅ Human-in-the-loop approval = trust
✅ Plan/Act separation = smart workflow
✅ Checkpoint system = safety net

### 2.2 Continue.dev - Modular Architecture

**Tech Stack:**
- TypeScript (84.1%)
- JavaScript (7.7%)
- Kotlin (3.9%) - JetBrains integration
- Python (2.3%)
- Rust (0.7%)

**Folder Structure:**
```
continue/
├── core/          # Business logic e agent orchestration
├── gui/           # Web-based dashboard (React + Redux)
├── extensions/    # VS Code + JetBrains plugins
├── cli/           # Headless/TUI modes
├── packages/      # Modular npm packages
├── actions/       # Workflow definitions
└── docs/          # Documentation
```

**Component Communication:**
```
core <-> extension <-> gui
```

**Protocol:** Definito in `core/protocol/` folder

**Configuration:**
- `config.json` o `config.yaml`
- Definisce: models (chat/edit/apply/embed/rerank), context providers, system messages, custom slash commands

**Operational Modes:**
1. **Cloud Agents**: Async workflows (GitHub PR events, schedules)
2. **CLI Agents**: Real-time terminal execution con step-by-step approval
3. **IDE Agents**: Editor integration via plugin protocols

**Philosophy:**
> "The future of coding isn't writing more code. It's delegating the boring parts."

**LEZIONE PER CERVELLASWARM:**
✅ Modular architecture = scalabilità
✅ Multi-mode (cloud/cli/ide) = flessibilità
✅ Unified config system = semplicità

### 2.3 Cursor AI - Il "Fork Rebuilt Around AI"

**Differenza chiave vs Extensions:**
> "Cursor is a VS Code fork rebuilt around AI, not an editor with AI added but an AI tool that happens to be an editor."

**Features Speciali:**

1. **Codebase-Wide Understanding**
   - RAG (Retrieval-Augmented Generation) avanzato
   - Indexing completo progetto
   - Deeper insights vs extension-based solutions

2. **Composer (Multi-File Editing)**
   - AI crea/edita multiple files simultaneously
   - Natural language instructions
   - AI identifica file rilevanti, plan edits, apply changes

3. **Inline Editing**
   - Select code → describe changes → AI rewrites in place

4. **Terminal AI**
   - Command suggestions direttamente nel terminal

5. **AI-Powered Code Reviews**
   - AI analizza diffs, spiega changes
   - Evidenzia bugs, suspicious patterns
   - Genera commit messages based on actual code changes

**Performance (2026):**
| Metric | VS Code | Cursor |
|--------|---------|--------|
| Startup time | 0.8-1.2s | 1.0-1.5s |
| Memory (idle) | 150-200MB | 200-280MB |
| Memory (large project) | 400-600MB | 500-800MB |

**Overhead:** +80-200MB per codebase indexing system

**Extension Compatibility:**
~95% VS Code extensions funzionano (issues con extensions che usano internal APIs)

**Pricing:**
$20/month

**LEZIONE PER CERVELLASWARM:**
⚠️ Full fork = overkill per nostro use case
✅ Codebase indexing = potente (possiamo fare via tree-sitter!)
✅ Multi-file editing = feature killer (ma complessa)

### 2.4 GitHub Copilot - Standard di Riferimento

**Features:**
- Inline autocompletions
- Copilot Chat companion (conversational Q&A)
- Debugging help, code explanation
- Deep integration con VS Code

**Chat Participant API:**
- Extension possono creare "@participants" specializzati
- Es: `@vscode` built-in participant
- Domain-specific knowledge
- Access full VS Code extension APIs

**Tool API:**
- Extensions contribute tools via Language Model Tools API
- Specialized functionality + full extension APIs

**LEZIONE PER CERVELLASWARM:**
✅ Chat Participant pattern = UX familiare
✅ @ mention syntax = intuitivo
✅ Tool API = potente

---

## 3. POC MINIMO - MVP Features per CervellaSwarm

### 3.1 Must-Have Features (v2.1.0)

**SIDEBAR CHAT:**
- Webview React-based
- Input field per task description
- Status display: IDLE | WORKING | DONE | ERROR
- Task history (ultime 5 task)

**TERMINAL INTEGRATION:**
- Spawn `cervellaswarm task` in integrated terminal
- Parse output per status updates
- Clickable file paths (open in editor)

**WORKER STATUS:**
- Display active workers (backend, frontend, tester...)
- Progress indicators
- Heartbeat visualization

**MINIMAL UI:**
```
┌─────────────────────────────────┐
│ CervellaSwarm 🐝                │
├─────────────────────────────────┤
│ Task:                            │
│ [_________________________]      │
│                                  │
│ Workers: 3 active                │
│ • backend (WORKING)              │
│ • frontend (DONE)                │
│ • tester (IDLE)                  │
│                                  │
│ Recent Tasks:                    │
│ ✓ Add login feature              │
│ ✓ Fix CSS bug                    │
│ ✗ Deploy to staging (error)     │
└─────────────────────────────────┘
```

### 3.2 Nice-to-Have (v2.2.0+)

**FILE DECORATION:**
- Visual indicator su file modificati da workers
- Gutter icons per AI-suggested changes

**INLINE DIFF PREVIEW:**
- Preview changes prima di applicarle
- Accept/Reject buttons

**MULTI-FILE EDITING (come Cursor Composer):**
- AI suggerisce edits cross-file
- Plan visualization
- Batch apply

**CHAT PARTICIPANT `@cervellaswarm`:**
- Integrazione con Copilot Chat API
- Domain-specific knowledge
- Delegate to workers via @mention

**CHECKPOINT INTEGRATION:**
- Integrazione con git per snapshots
- Restore previous state

### 3.3 Minimal Architecture (MVP)

```
┌────────────────────────────────────────────────────────────┐
│                    VS CODE EXTENSION                        │
│  ┌──────────────────┐          ┌─────────────────────┐     │
│  │  Extension Host  │ <------> │  Webview (React)    │     │
│  │  (Node.js)       │  JSON    │  - Sidebar UI       │     │
│  │                  │  msgs    │  - Task input       │     │
│  │  - Task Manager  │          │  - Status display   │     │
│  │  - Terminal Mgr  │          └─────────────────────┘     │
│  │  - Status Parser │                                       │
│  └──────┬───────────┘                                       │
│         │                                                   │
└─────────┼───────────────────────────────────────────────────┘
          │
          ▼ spawn
┌─────────────────────────┐
│  Integrated Terminal    │
│  $ cervellaswarm task   │
│  [worker output...]     │
└─────────────────────────┘
          │
          ▼ comunicazione via stdio / HTTP localhost
┌─────────────────────────┐
│  CervellaSwarm CLI      │
│  (existing!)            │
│  - spawn-workers.sh     │
│  - task management      │
│  - .swarm/ state        │
└─────────────────────────┘
```

**Vantaggi:**
- ✅ Riusa CLI esistente (zero duplicazione)
- ✅ Extension = thin layer (UI + orchestration)
- ✅ CLI handle complessità (worker management, SNCP, etc)
- ✅ Testabile separatamente

---

## 4. EFFORT & COMPLESSITÀ

### 4.1 Effort Estimate (MVP)

**Setup & Scaffold (1 giorno):**
- Yo generator: `yo code`
- TypeScript + React setup
- ESBuild configuration
- Package.json contributions (sidebar, commands)

**Extension Core (3-4 giorni):**
- Task Manager class (track tasks, workers)
- Terminal Manager (spawn CLI, parse output)
- Message passing webview ↔ extension
- Status persistence (memento API)

**Webview UI (3-4 giorni):**
- React components (TaskInput, StatusDisplay, WorkerList)
- CSS styling (match VS Code theme)
- Message handlers
- State management (Redux/Context)

**Integration & Testing (2-3 giorni):**
- E2E test con CLI
- Edge cases (terminal close, worker timeout, error states)
- VS Code API version compatibility
- Package per VSIX

**Documentation (1 giorno):**
- README extension
- Contribution guide
- Screenshots/GIF demo

**TOTALE: 10-13 giorni (2-3 settimane)**

### 4.2 Complessità Breakdown

| Feature | Complessità | Rationale |
|---------|-------------|-----------|
| Sidebar Webview | 🟢 LOW | API ben documentata, esempi Microsoft |
| Terminal spawn | 🟢 LOW | `createTerminal()` + shellArgs |
| Message passing | 🟡 MEDIUM | Async, need protocol design |
| Status parsing | 🟡 MEDIUM | Regex/JSON parse CLI output |
| File decoration | 🟡 MEDIUM | `FileDecorationProvider` API |
| Inline diff | 🔴 HIGH | Custom editor, conflict resolution |
| Multi-file edit | 🔴 HIGH | Plan visualization, batch apply, undo |
| Chat Participant | 🟡 MEDIUM | New API (2026), need Copilot |

**MVP = Solo feature 🟢 LOW + 🟡 MEDIUM basilari**

### 4.3 Librerie & Framework Utili

**Consigliati:**

1. **vscode-messenger** - Message passing semplificato
   - JSON RPC-like protocol
   - Type-safe communication

2. **React + Redux Toolkit** - Webview UI
   - State management robusto
   - Component reusability

3. **ESBuild** - Fast bundling
   - Raccomandato 2026
   - Faster than webpack

4. **@types/vscode** - TypeScript types
   - Autocomplete VS Code API
   - Mandatory per TS

**Optional:**

5. **vscode-webview-ui-toolkit** - Microsoft official UI components
   - Match VS Code look & feel
   - Accessibilità built-in

6. **axios** - HTTP client (se CLI espone localhost API)

### 4.4 Esempi Open Source da Studiare

**Da Microsoft:**
- `vscode-extension-samples/webview-sample` - Basic webview example
- `vscode-extension-samples/chat-sample` - Chat participant demo
- `vscode-extension-samples/task-provider-sample` - Custom tasks

**Da Community:**
- **Cline** (github.com/cline/cline) - Human-in-the-loop, Plan/Act pattern
- **Continue** (github.com/continuedev/continue) - Modular architecture
- **Run in Terminal** - Simple terminal spawn example

---

## 5. RACCOMANDAZIONE FINALE

### 5.1 MVP Features per v2.1.0

**FASE 1 (Week 1): Foundation**
- ✅ Scaffold extension (TypeScript + React)
- ✅ Sidebar webview con UI minimal
- ✅ Message passing protocol design
- ✅ Extension ↔ CLI communication via terminal

**FASE 2 (Week 2): Core Features**
- ✅ Task input + submit to CLI
- ✅ Status display (IDLE/WORKING/DONE/ERROR)
- ✅ Worker list con heartbeat visualization
- ✅ Task history (ultime 5)

**FASE 3 (Week 3): Polish**
- ✅ Error handling + edge cases
- ✅ VS Code theme compatibility (light/dark)
- ✅ Testing + VSIX packaging
- ✅ Documentation + screenshots

**Success Criteria MVP:**
1. User può submit task da sidebar
2. Extension spawna `cervellaswarm task` in terminal
3. Status workers visualizzato real-time
4. Task history persistente tra session
5. VSIX installabile + pubblicabile su Marketplace

### 5.2 Nice-to-Have per v2.2.0+

**Post-MVP Enhancements:**
- File decoration (AI-modified files)
- Inline diff preview (Accept/Reject)
- Chat Participant `@cervellaswarm` integration
- Multi-file editing (Cursor Composer-like)
- Checkpoint/restore integration
- MCP tool visualization

**Effort Post-MVP:**
- File decoration: +2-3 giorni
- Inline diff: +5-7 giorni
- Chat Participant: +3-4 giorni
- Multi-file editing: +10-15 giorni (complesso!)

### 5.3 Timeline Realistica

```
v2.1.0 - MVP Extension (Week 1-3)
├── FASE 1: Foundation (5 giorni)
├── FASE 2: Core Features (7 giorni)
└── FASE 3: Polish (3 giorni)
TOTAL: 15 giorni (3 settimane)

v2.2.0 - Enhanced (Week 4-6)
├── File decoration (3 giorni)
├── Inline diff preview (5 giorni)
└── Chat Participant (4 giorni)
TOTAL: 12 giorni (2.5 settimane)

v2.3.0 - Advanced (Week 7-10)
└── Multi-file editing (15 giorni)
```

### 5.4 Decisione: GO / NO-GO?

**✅ GO - Raccomando PROCEDERE**

**Motivi:**
1. **MVP effort moderato** (2-3 settimane) → ROI alto
2. **Competitor validation** - Cline, Continue dimostrano demand
3. **CLI riuso** - Zero duplicazione, extension = thin layer
4. **Differentiation** - CervellaSwarm = team approach unico
5. **Market timing** - 2026 = peak VS Code extensions AI

**Rischi Mitigati:**
- ⚠️ Complessità multi-file editing → POST-MVP (v2.2.0+)
- ⚠️ Message passing async → vscode-messenger library
- ⚠️ Terminal parsing → JSON output CLI (already implemented!)

**Blockers:**
- 🛑 NESSUNO - Tutto fattibile con API esistenti

### 5.5 Architettura Consigliata

**Pattern: Thin Extension + Thick CLI**

```
Extension (Thin):
- UI layer (React sidebar)
- Task orchestration
- Status visualization
- Message relay

CLI (Thick):
- Worker management (spawn-workers.sh)
- SNCP persistence
- Task execution
- .swarm/ state
```

**Vantaggi:**
- Extension lightweight (<500 righe core logic)
- CLI testabile indipendentemente
- Update CLI = auto-update extension features
- Debug semplificato (CLI standalone)

### 5.6 Next Steps Immediate

**Step 1: Validazione con Guardiane**
- Consulta Guardiana Qualità per approval
- Consulta Guardiana Ops per deployment strategy
- Consulta Guardiana Marketing per positioning

**Step 2: Scaffold Extension**
```bash
npm install -g yo generator-code
yo code  # select TypeScript + React Webview
```

**Step 3: Proof of Concept (2 giorni)**
- Sidebar display "Hello CervellaSwarm"
- Button "Run Task" → spawn terminal con `cervellaswarm --version`
- Parse output → display in webview

**Step 4: Decision Point**
- Se POC OK → FULL MVP
- Se problemi → ITERATE

---

## 6. FONTI & RIFERIMENTI

### Official Documentation
- [VS Code Extension API](https://code.visualstudio.com/api/references/vscode-api)
- [Webview API Guide](https://code.visualstudio.com/api/extension-guides/webview)
- [Building Extensions 2026 Complete Guide](https://abdulkadersafi.com/blog/building-vs-code-extensions-in-2026-the-complete-modern-guide)
- [Task Provider API](https://code.visualstudio.com/api/extension-guides/task-provider)
- [Chat Participant API](https://code.visualstudio.com/api/extension-guides/ai/chat)

### Competitor Analysis
- [Cline VS Code Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- [Cline GitHub Repository](https://github.com/cline/cline)
- [Continue.dev Extension](https://marketplace.visualstudio.com/items?itemName=Continue.continue)
- [Continue GitHub Repository](https://github.com/continuedev/continue)
- [Cursor vs VS Code Comparison](https://graphite.com/guides/cursor-vs-vscode-comparison)
- [Best AI Code Editors 2026](https://playcode.io/blog/best-ai-code-editors-2026)

### Technical Resources
- [Webview Communication Simplification](https://www.eliostruyf.com/simplify-communication-visual-studio-code-extension-webview/)
- [VS Code Messenger Library](https://www.typefox.io/blog/vs-code-messenger/)
- [Microsoft Extension Samples](https://github.com/microsoft/vscode-extension-samples)
- [Pass Data to Webview Panel](https://medium.com/@ashleyluu87/data-flow-from-vs-code-extension-webview-panel-react-components-2f94b881467e)

### Tutorials & Guides
- [Your First Extension](https://code.visualstudio.com/api/get-started/your-first-extension)
- [Chat Tutorial](https://code.visualstudio.com/api/extension-guides/ai/chat-tutorial)
- [Extension to Pass Arguments to Terminal](https://egghead.io/lessons/egghead-create-a-vs-code-extension-to-pass-arguments-to-the-terminal)

---

## 7. APPENDICE: Decisioni Architetturali

### A1. Perché React per Webview?

**PRO:**
- State management robusto (Redux/Context)
- Component reusability
- Large ecosystem (UI libraries)
- Fast development (create-react-app patterns)

**CONTRO:**
- Bundle size (~200KB minified)
- Overkill per UI molto semplici

**DECISIONE:**
✅ React per MVP - UI evolverà (task history, worker list, charts)

### A2. Perché Message Passing vs HTTP Localhost?

**Message Passing (vscode.postMessage):**
- ✅ Built-in VS Code API
- ✅ No port conflicts
- ✅ Secure (no network exposure)
- ❌ Async, disconnected

**HTTP Localhost (CLI espone server):**
- ✅ Request/Response pattern
- ✅ REST-like API
- ❌ Port management
- ❌ Security concerns

**DECISIONE:**
✅ Message Passing per Extension ↔ Webview
✅ Terminal stdio per Extension ↔ CLI
Rationale: Segue pattern VS Code standard, zero dependencies esterne

### A3. TypeScript vs JavaScript?

**TypeScript:**
- ✅ Type safety (catch errors at compile time)
- ✅ VS Code API autocomplete
- ✅ Raccomandato ufficialmente Microsoft
- ✅ Large codebase scalability

**JavaScript:**
- ✅ Faster development (no compile step)
- ✅ Smaller bundle
- ❌ No type checking

**DECISIONE:**
✅ TypeScript - Mandatory per extensions serie (2026 best practice)

---

## 8. CONCLUSIONI

**CervellaSwarm VS Code Extension è FATTIBILE e RACCOMANDATO.**

**Key Takeaways:**
1. **MVP = 2-3 settimane** (effort moderato, ROI alto)
2. **Architettura Thin Extension + Thick CLI** = riuso massimo
3. **Competitor validation** - Cline (57k stars), Continue dimostrano demand
4. **Differentiation** - Multi-agent approach CervellaSwarm = unico
5. **Timeline:** v2.1.0 MVP (Week 1-3), v2.2.0 Enhanced (Week 4-6)

**Raccomandazione Finale:**
✅ **PROCEDI con POC (2 giorni)** → Se OK → **FULL MVP (3 settimane)**

**Next Action:**
Consulta Guardiana Qualità + Ops per approval → Start POC

---

*"Non reinventiamo la ruota - la miglioriamo!"*
*Cervella Researcher - CervellaSwarm Team*
*Sessione 311 - 22 Gennaio 2026*
