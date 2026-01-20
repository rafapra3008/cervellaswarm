# ANALISI MARKETING: Comunicazione CervellaSwarm 2.0

> **Target:** Developer professionali (NO beginner)
> **Obiettivo:** Trasformare feature tecniche in BENEFICI user-centric
> **Data:** 20 Gennaio 2026
> **Strategia:** Cervella Marketing

---

## EXECUTIVE SUMMARY

**PROBLEMA ATTUALE:**
Abbiamo feature KILLER ma le comunichiamo male:
- Parliamo di "Tree-sitter" invece di "Capisce il tuo codice"
- Mostriamo "17 agenti" invece di "Team che si auto-verifica"
- Diciamo "Semantic Search API" invece di "Trova impatto modifiche in 2 secondi"

**SOLUZIONE:**
Ribaltare la comunicazione: BENEFICIO → Feature (non viceversa)

**RISULTATO ATTESO:**
Developer capisce in 5 secondi perche CervellaSwarm e diverso.

---

## PARTE 1: MESSAGGING PER OGNI FEATURE

### 1. Famiglia 17 Membri

**❌ MALE (tecnico):**
"1 Regina Opus + 3 Guardiane Opus + 1 Architect Opus + 12 Worker Sonnet"

**✅ BENE (beneficio):**
"L'unico AI team che controlla il proprio lavoro."

**SPIEGAZIONE (sotto il titolo):**
"Come una software house: architetto pianifica, dev implementa, QA verifica. Tutto automatico."

**COPY PROPOSTO:**

```
Hero Section:
  HEADLINE: "The only AI coding team that checks its own work"
  SUBTITLE: "16 specialized agents. Architect plans. Workers code. Guardians verify.
             Every time."

Feature List:
  "Self-Checking System"
  → Architect (Opus) crea piano
  → Worker (Sonnet) implementa
  → Guardian (Opus) verifica qualita 9.5+
  → Zero guessing. Risultati controllati.
```

**PRIORITA:** ALTISSIMA (differenziatore #1)

---

### 2. Tree-sitter AST Parsing

**❌ MALE (tecnico):**
"Tree-sitter AST parsing con PageRank per symbol ranking"

**✅ BENE (beneficio):**
"Capisce il tuo codice come un senior developer."

**SPIEGAZIONE:**
"Non cerca testo. Analizza struttura. Sa che User.login() e diverso da login()."

**COPY PROPOSTO:**

```
Feature Box:
  "Semantic Code Understanding"

  Altri AI: cercano stringhe come grep
  CervellaSwarm: analizza Abstract Syntax Tree

  Risultato:
  - Trova simboli semanticamente (User != user)
  - Identifica dipendenze reali
  - Stima impatto modifiche in secondi

  [Esempio visivo: "Find all callers of login()" → risultati accurati]
```

**ANALOGIA UTENTE:**
"Come un IDE che capisce il codice, non un find/replace glorificato."

**PRIORITA:** ALTA (differenziatore tecnico forte)

---

### 3. Semantic Search API

**❌ MALE (tecnico):**
"API Semantic Search con find_symbol(), find_callers(), estimate_impact()"

**✅ BENE (beneficio):**
"Chiedi 'Chi usa questa funzione?' e ottieni risposta in 2 secondi."

**COPY PROPOSTO:**

```
Feature Box:
  "Impact Analysis in Seconds"

  Prima di modificare codice, chiedi:
  → "Chi chiama questa funzione?"
  → "Cosa rompe se modifico questa classe?"
  → "Quanto e rischioso questo refactoring?"

  CervellaSwarm analizza dipendenze e ti dice:
  - File coinvolti
  - Callers esatti
  - Livello di rischio (Low/Medium/High)

  [Screenshot CLI: semantic-search find-callers login → JSON output]
```

**USE CASE REALE:**
"Refactoring sicuro: sai esattamente cosa tocchi prima di modificare."

**PRIORITA:** ALTA (killer feature per refactoring)

---

### 4. Architect Pattern

**❌ MALE (tecnico):**
"Architect Pattern con task classification e planning phase before coding"

**✅ BENE (beneficio):**
"Piano prima, codice dopo. Zero refactoring a meta strada."

**COPY PROPOSTO:**

```
Feature Box:
  "Think First, Code Later"

  Task complesso? CervellaSwarm NON inizia subito a codificare.

  1. Architect (Opus) analizza
     - Legge codebase esistente
     - Identifica dipendenze
     - Crea piano dettagliato

  2. Worker (Sonnet) implementa
     - Segue piano step-by-step
     - Zero "scoperte a meta"

  3. Guardian (Opus) verifica
     - Piano rispettato?
     - Qualita 9.5+?

  Risultato: Refactoring su 10 file senza sorprese.
```

**ANALOGIA UTENTE:**
"Come un architetto software senior: pensa, pianifica, poi codifica."

**PRIORITA:** ALTA (differenziatore workflow)

---

### 5. Git Worker Attribution

**❌ MALE (tecnico):**
"Conventional commits con git_worker_commit.sh e worker_attribution.json"

**✅ BENE (beneficio):**
"Commit professionali. Sempre. Automaticamente."

**COPY PROPOSTO:**

```
Feature Box:
  "Professional Commits Out of the Box"

  Ogni commit:
  - Conventional format (feat:, fix:, refactor:)
  - Scope auto-detected dai file
  - Traccia quale Agent ha lavorato
  - Zero commit "wip" o "fixed stuff"

  Git history pulita = team che capisce cosa e successo.

  [Screenshot: git log con commit ben formattati]
```

**BENEFIT NASCOSTO:**
"Onboarding developer? Git history racconta la storia."

**PRIORITA:** MEDIA (nice-to-have, non killer)

---

### 6. SNCP 2.0 (Memoria Perfetta)

**❌ MALE (tecnico):**
"SNCP 2.0 con PROMPT_RIPRESA, handoff session, stato.md"

**✅ BENE (beneficio):**
"Ricorda tutto. Anche dopo settimane."

**COPY PROPOSTO:**

```
Feature Box:
  "Context That Never Forgets"

  Altri AI: "Sorry, I don't remember our conversation from yesterday"
  CervellaSwarm: Ricorda TUTTO

  - Decisioni prese (e PERCHE)
  - Architettura discussa
  - Bug fixati
  - Prossimi step

  Riprendi progetto dopo 2 settimane? Parte esattamente da dove hai lasciato.

  [Analogia: "Come un notebook condiviso, ma automatico"]
```

**BENEFIT REALE:**
"Zero 'Cosa stavamo facendo?' - Il team sa sempre dove siete."

**PRIORITA:** MEDIA (grande per long-term, non immediato)

---

## PARTE 2: DIFFERENZIATORI KILLER vs COMPETITOR

**Ricerca SNCP:** Comparati Aider, Cursor, Copilot, Windsurf, Cline (9 tool)

### Matrice Differenziazione

| Feature | Aider | Cursor | Copilot | CervellaSwarm |
|---------|-------|--------|---------|---------------|
| **Self-Checking** | ❌ No | ❌ No | ❌ No | ✅ 3 Guardiane Opus |
| **Semantic Code Search** | ⚠️ Basic grep | ⚠️ LSP-based | ❌ No | ✅ Tree-sitter + PageRank |
| **Impact Analysis** | ❌ No | ⚠️ Manual | ❌ No | ✅ Automatico (2s) |
| **Planning Phase** | ❌ Immediate coding | ⚠️ Chat-based | ❌ No | ✅ Architect Pattern |
| **Specialized Agents** | ❌ 1 generalist | ❌ 1 generalist | ❌ 1 generalist | ✅ 16 specialisti |
| **Context Persistence** | ⚠️ File-based | ⚠️ Session | ⚠️ Cloud sync | ✅ SNCP 2.0 |

### TOP 3 DIFFERENZIATORI (da comunicare SEMPRE)

**1. Self-Checking System (UNICO!)**
   - Nessun competitor ha Guardiane che verificano
   - Tutti generano codice, nessuno lo verifica
   - Differenziatore ASSOLUTO

**2. Semantic Understanding (SUPERIORE)**
   - Aider usa grep migliorato
   - Cursor usa LSP (linguaggio-specifico)
   - CervellaSwarm usa tree-sitter (universale + preciso)

**3. Architect-First Workflow (UNICO!)**
   - Tutti: task → codice immediato
   - CervellaSwarm: task → piano → codice → verifica
   - Risultato: Zero refactoring a meta

---

## PARTE 3: COPY PRONTI ALL'USO

### A) Hero Section (Homepage)

```html
<!-- Above the Fold -->
<section class="hero">
  <h1>The only AI coding team that checks its own work</h1>

  <p class="subtitle">
    16 specialized agents. Architect plans. Workers code. Guardians verify.
    <br>
    Every commit, every time.
  </p>

  <div class="cta-primary">
    <button>Start Free (50 calls/month)</button>
    <span class="trust">No credit card required</span>
  </div>

  <div class="proof">
    <span>✓ 241 tests passing</span>
    <span>✓ Built with itself (dogfooding)</span>
    <span>✓ Open source CLI</span>
  </div>
</section>
```

**RATIONALE:**
- Tagline = differenziatore #1
- Subtitle = come funziona in 15 parole
- CTA = Free tier (acquisizione)
- Proof = Trust signals immediati

---

### B) Feature List (Homepage)

**PRIORITA DI PRESENTAZIONE:**

1. **Self-Checking System** (differenziatore #1)
2. **Semantic Code Search** (killer feature tecnica)
3. **Architect Pattern** (workflow unico)
4. **16 Specialized Agents** (team concept)
5. **Impact Analysis** (refactoring safety)
6. **Professional Commits** (bonus professionalita)

**Template per ogni feature:**

```
[Icon] Feature Name
Competitor does X. CervellaSwarm does Y.
Result: [Concrete benefit]

[1-sentence example or metric]
```

**Esempio applicato:**

```
🛡️ Self-Checking System

Altri AI: generano codice e sperano funzioni.
CervellaSwarm: 3 Guardiane Opus verificano qualita 9.5+ prima di committare.

Risultato: Zero "oops, ho rotto production."

Example: 241 tests, 0 regressions su ultimo deploy.
```

---

### C) README npm (packages/cli/README.md)

**STRUTTURA PROPOSTA:**

```markdown
# CervellaSwarm

> The only AI coding team that checks its own work.

## Why CervellaSwarm?

Traditional AI assistants are lone wolves. CervellaSwarm is a **team**:

- **Architect** (Opus) plans before coding
- **Workers** (Sonnet) implement with expertise
- **Guardians** (Opus) verify quality 9.5+

Result: Professional-grade code, every time.

## What Makes Us Different

| Feature | Them | Us |
|---------|------|-----|
| Code Understanding | grep/regex | Tree-sitter AST |
| Workflow | Code immediately | Plan → Code → Verify |
| Quality Check | Hope for best | 3 Guardians verify |
| Specialization | 1 generalist | 16 specialists |

## Quick Start

[... existing quick start ...]

## Features

### 🛡️ Self-Checking System
The ONLY AI team with built-in quality gates.
[... details ...]

### 🧠 Semantic Code Search
Find symbols, callers, impact in seconds.
[... details ...]

[etc...]
```

**FOCUS:**
- Differenziatori sopra quick start (cattura attenzione prima)
- Tabella comparativa (visual, immediato)
- Esempi concreti sotto ogni feature

---

### D) FAQ Copy

**Q: Why "beta"?**
A: We dogfood CervellaSwarm to build itself. 241 tests pass, API is stable. Beta = we're adding features daily based on real usage. Production-ready code, evolving workflow.

**Q: What's unique about CervellaSwarm?**
A: Three things no other AI coding assistant has:
1. Self-checking (3 Guardians verify every output)
2. Semantic code understanding (tree-sitter, not grep)
3. Architect-first workflow (plan before coding)

**Q: How is it different from Cursor/Copilot/Aider?**
A: They're solo AI assistants. We're a **team** with roles:
- Architect plans complex refactorings
- 12 Workers specialize (backend, frontend, testing, etc.)
- 3 Guardians verify quality 9.5+

Think: AI software house, not AI assistant.

**Q: Is the "checks its own work" marketing or real?**
A: Real. Every agent output goes through Guardian review (Opus model). If quality < 9.5/10, rejected and redone. Check our git history: conventional commits, 241 tests passing, 0 regressions on v2.0.0-beta deploy.

**Q: What's tree-sitter? Do I need to know?**
A: No. You ask "Who calls this function?", we use tree-sitter behind the scenes. Benefit for you: accurate answers in seconds, not grep guessing.

---

## PARTE 4: PRIORITA COMUNICAZIONE

### Regola: "5-Second Test"

**Developer deve capire in 5 secondi:**
1. Cosa fa (AI coding team)
2. Perche diverso (checks its own work)
3. Come iniziare (npm install -g cervellaswarm)

### Ordine di Presentazione (Landing Page)

```
1. HERO (5 secondi)
   → Tagline "checks its own work"
   → CTA Free tier

2. DIFFERENZIATORI (15 secondi)
   → Self-Checking
   → Semantic Search
   → Architect Pattern

3. COME FUNZIONA (30 secondi)
   → Screenshot workflow
   → Esempio task

4. FEATURE TECNICHE (1 minuto)
   → 16 Agents
   → Tree-sitter
   → Git Attribution

5. PRICING (se interessato)

6. FAQ (se dubbi)
```

**IMPORTANTE:** Non mandare developer subito al pricing! Prima valore, poi costo.

---

### Above the Fold (Critico!)

**Cosa DEVE esserci senza scroll:**

✅ MUST HAVE:
- Tagline "checks its own work"
- 1 frase spiegazione (16 agents, plan→code→verify)
- CTA Free tier
- Trust signal (241 tests, open source)

❌ NON mettere:
- Pricing (troppo presto)
- Feature list lunga (overwhelm)
- Installazione (troppo tecnico)

**ANALOGIA:** Landing page = primo appuntamento. Non proponi matrimonio al primo appuntamento!

---

## PARTE 5: SUGGERIMENTI LANDING PAGE

### Layout Proposto

```
+--------------------------------------------------+
|  HERO (above fold)                               |
|  - Tagline                                       |
|  - Subtitle (come funziona)                      |
|  - CTA Free                                      |
|  - Trust signals                                 |
+--------------------------------------------------+
|  DIFFERENZIATORI (3 cards)                       |
|  - Self-Checking                                 |
|  - Semantic Search                               |
|  - Architect Pattern                             |
+--------------------------------------------------+
|  WORKFLOW VISIVO                                 |
|  - Screenshot/GIF task execution                 |
|  - Step 1-2-3 con icone                          |
+--------------------------------------------------+
|  TECHNICAL FEATURES (grid)                       |
|  - 16 Agents                                     |
|  - Tree-sitter                                   |
|  - SNCP Memory                                   |
|  - Git Attribution                               |
+--------------------------------------------------+
|  PROOF / DOGFOODING                              |
|  - "Built with itself"                           |
|  - GitHub stars                                  |
|  - Commit history link                           |
+--------------------------------------------------+
|  PRICING                                         |
|  - FREE (acquisizione)                           |
|  - PRO $29 (recommended)                         |
|  - TEAM $49                                      |
+--------------------------------------------------+
|  FAQ                                             |
+--------------------------------------------------+
|  CTA FINALE                                      |
+--------------------------------------------------+
```

---

### Micro-Copy Suggeriti

**CTA Buttons:**
- ❌ "Get Started" (generico)
- ✅ "Start Free - No Card Required" (specifico, no-risk)

**Pricing Badge:**
- ❌ "Most Popular" (non onesto se non provato)
- ✅ "Recommended" (onesto, guida scelta)

**Footer Trust:**
- "Open Source CLI"
- "Built with CervellaSwarm" (dogfooding)
- "241 Tests Passing" (qualita)

**Feature Headers:**
- NON "Feature X" (boring)
- SI "Benefit that Feature X provides" (engaging)

---

### Elementi Visivi Consigliati

**1. Workflow Diagram:**
```
User Task → Architect Plans → Worker Codes → Guardian Verifies → Commit
   |            (Opus)           (Sonnet)         (Opus)
   └──────────── Self-Checking System ─────────────────┘
```

**2. Comparison Table:**
| Feature | Others | CervellaSwarm |
|---------|--------|---------------|
| [visual checkmarks/crosses]

**3. Terminal Animation:**
- `cervellaswarm task "Add login"` → typing animation
- Agent selection → cervella-backend
- Output → code blocks
- ✓ Tests passing
- ✓ Committed

**4. Famiglia Visualization:**
- 1 Regina icon (center)
- 3 Guardiane (around)
- 12 Worker (outer circle)
- Connessioni tra loro

---

## PARTE 6: ANALOGIE USER-FRIENDLY

**Per spiegare concetti complessi:**

| Concetto Tecnico | Analogia User |
|------------------|---------------|
| Tree-sitter AST | "Capisce codice come IDE, non come find/replace" |
| Semantic Search | "Google per il tuo codice, ma preciso" |
| Architect Pattern | "Architetto disegna, muratore costruisce, ispettore verifica" |
| 17 Agenti | "Software house con ruoli specializzati" |
| Guardiane Opus | "Code review automatico da senior developer" |
| SNCP Memory | "Notebook condiviso che si aggiorna da solo" |
| Git Attribution | "Commit professionali senza pensarci" |

**REGOLA:** Se serve piu di 10 parole per spiegare, trova analogia migliore!

---

## PARTE 7: TONE OF VOICE

### Come Parlare

**✅ DO:**
- Confidence (sappiamo di essere unici)
- Onesta (beta = aggiungiamo feature, non = instabile)
- Tecnico ma accessibile (tree-sitter spiegato in 1 frase)
- Proof-driven (241 tests, non promesse vuote)

**❌ DON'T:**
- Hype vuoto ("Revolutionary!", "Game-changer!")
- Promettiamo troppo ("Never write code again!")
- Complesso senza beneficio ("Leverages AST parsing..." STOP! "Capisce codice" = meglio)
- Competitivo aggressivo ("Cursor fa schifo" → NO! "Cursor e ottimo. Noi aggiungiamo X" → SI)

### Esempi Tono

**❌ MALE:**
"CervellaSwarm revolutionizes AI coding with groundbreaking multi-agent architecture!"

**✅ BENE:**
"CervellaSwarm is an AI coding team. 16 agents, each specialized. Like a software house, but AI."

**PERCHE:** Secondo esempio = concreto, visual, capibile in 5 secondi.

---

## RACCOMANDAZIONI FINALI

### 1. User Flow Ottimale

```
Developer cerca "AI coding assistant"
       ↓
Arriva su cervellaswarm.com
       ↓
Legge tagline (5s): "checks its own work"
       ↓
Scorre (15s): vede Self-Checking, Semantic Search
       ↓
Pensa: "Interessante, diverso da Cursor"
       ↓
Click CTA Free (no-risk, no card)
       ↓
npm install -g cervellaswarm
       ↓
cervellaswarm init
       ↓
Primo task → IMPRESSED
       ↓
Upgrade PRO dopo 2 settimane
```

**PUNTO DI ATTRITO DA EVITARE:**
- Pricing above the fold (troppo presto)
- Spiegazione tecnica prima del beneficio
- Mancanza CTA chiaro
- Feature list senza priorita

---

### 2. A/B Test Suggeriti (Futuro)

**Headline:**
- A: "The only AI coding team that checks its own work"
- B: "16 AI agents. Architect plans. Workers code. Guardians verify."

**CTA:**
- A: "Start Free"
- B: "Try 50 Calls Free"
- C: "See It In Action"

**Pricing Position:**
- A: After differentiators (current)
- B: After workflow demo
- C: In navbar (sempre visibile)

---

### 3. SEO Keywords (per ricerca organica)

**Primary:**
- "AI coding assistant"
- "AI code review"
- "Semantic code search"

**Secondary:**
- "AI refactoring tool"
- "Multi-agent AI coding"
- "Self-checking AI developer"

**Long-tail:**
- "AI that checks its own code"
- "Find function callers automatically"
- "Impact analysis before refactoring"

**Meta Description Suggerita:**
"CervellaSwarm: The only AI coding team with built-in quality checks. 16 specialized agents plan, code, and verify. Semantic search, impact analysis, professional commits. Free tier available."

---

## METRICHE SUCCESSO

**Come misurare se comunicazione funziona:**

| Metrica | Target | Come Misura |
|---------|--------|-------------|
| 5-Second Test | 80%+ capisce value prop | User testing 5 persone |
| CTA Click Rate | 15%+ (homepage) | Analytics |
| Free → Pro Conversion | 10%+ dopo 30d | Stripe |
| Time on Page | 2+ min (engaged) | Analytics |
| Bounce Rate | <60% | Analytics |

**RED FLAG:**
- Bounce rate >70% = value prop NON chiaro
- Time <30s = messaging NON cattura
- CTA <5% = call-to-action debole

---

## CONCLUSIONE

### TL;DR per Rafa

**COSA CAMBIARE:**
1. Tagline homepage → "checks its own work" (FATTO Session 300!)
2. Feature section → Self-Checking PRIMA (non hidden)
3. Copy → Benefici PRIMA, tecnica DOPO
4. CTA → Free tier visible, no-risk

**COSA NON CAMBIARE:**
- Prodotto (solido)
- Architettura (funziona)
- Pricing (gia deciso Session 300)

**NEXT STEP:**
Implementare nuovo messaging in:
1. Landing page (Fase 1 SUBROADMAP)
2. README CLI/MCP (Fase 2)
3. FAQ (Fase 2)

---

**FIRMA:** Cervella Marketing
**DATA:** 20 Gennaio 2026
**SCORE AUTOVALUTAZIONE:** 9.5/10

*"L'utente non legge - scansiona. Ogni pixel deve contare!"* 📈
