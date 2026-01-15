# STUDIO: Wizard Iniziale Perfetto per CervellaSwarm

**Data:** 15 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Obiettivo:** Studiare come creare il wizard iniziale che elimina il problema della "ri-spiegazione"

---

## EXECUTIVE SUMMARY

**TL;DR:** Il problema che viviamo noi (confusione su "cosa facciamo", dover rispiegare ogni sessione) è ESATTAMENTE quello che gli utenti NON devono vivere. Il wizard iniziale deve creare una "costituzione del progetto" così robusta che l'utente non deve MAI rispiegare.

**FINDING CHIAVE:** Il 61% degli utenti abbandona durante onboarding complesso. Context loss è il problema #1 nei CLI tools del 2025. La soluzione: Wizard robusto + Session Management + Progressive Disclosure.

**RACCOMANDAZIONE:** Implementare 3-Layer Onboarding System:
1. **Layer 1:** Wizard Iniziale (5-7 domande strategiche)
2. **Layer 2:** Session Management (project-specific context)
3. **Layer 3:** Progressive Re-engagement (quando serve)

---

## 1. IL PROBLEMA (Nostro e degli Utenti)

### 1.1 Il Problema che VIVIAMO

```
ESPERIENZA RAFA + CERVELLA (Prima SNCP robusto):
────────────────────────────────────────────────
Sessione 1: "Lavoriamo su X"
Sessione 2: "Cosa stavamo facendo?"
Sessione 3: "Perché avevamo deciso Y?"
Sessione 4: "Qual era l'obiettivo?"

RISULTATO: Tempo perso, frustrazione, momentum perso
```

### 1.2 Il Problema che gli Utenti VIVONO (Dati Reali)

**Onboarding Friction Statistics:**
- **61%** degli utenti abbandona durante onboarding complesso
- **40-60%** degli utenti usa l'app SOLO UNA VOLTA
- **40%** dei churned customers non ha mai adottato feature chiave

**Context Loss in CLI Tools (2025):**
- Claude Code Issue #2545: "Severe Session Memory Loss"
- Context Forge creato PROPRIO per risolvere questo problema
- Gemini CLI aggiunto session management come feature CRITICA nel 2025

**Cause Comuni:**
- Onboarding troppo generico (not personalized)
- Form fields complessi e non chiari
- Lack of clear guidance sui prossimi step
- Ogni restart = ri-spiegare tutto

### 1.3 IL DIFFERENZIALE DI CERVELLASWARM

> **"Il nostro wizard non è 'carino'. È NECESSITÀ ASSOLUTA."**

```
CURSOR (2023):
Wizard minimale perché IDE = visual + sempre aperto
Context loss basso (file sempre visibili)

CERVELLASWARM (2026):
CLI-based = context loss MASSIMO se non gestiamo
Session interruption = potenzialmente tutto perso
Multi-progetto = confusion 10x

QUINDI: Wizard robusto non è nice-to-have, è SURVIVAL.
```

---

## 2. BEST PRACTICES - WIZARD CHE FUNZIONANO

### 2.1 Node.js CLI Best Practices

**Fonte:** [Node.js CLI Apps Best Practices (Lirantal)](https://github.com/lirantal/nodejs-cli-apps-best-practices)

**Principi Chiave:**

**1. Build Empathic CLIs**
- Guide users verso successo proattivamente
- Prompt quando mancano dati, non fallire silenziosamente
- "Put workflows in place that assist the user"

**2. Zero Configuration (quando possibile)**
- Auto-detect environment variables
- Work out-of-the-box
- Prompt SOLO quando interaction è essenziale

**3. Rich Interactions**
- Dropdown selects > text-only prompts
- Progress bars per operazioni async
- Auto-complete dove possibile
- **"Don't force parameters users can work out automatically"**

**4. Stateful Data Handling**
- Remember user preferences tra invocazioni
- Store config seguendo XDG Base Directory Specification
- Use libraries: `configstore` o `conf`

**5. Configuration Precedence**
```
CLI args → ENV vars → Project config → User config → System config
```

### 2.2 Inquirer.js / Prompts (Interactive CLI Pattern)

**Fonte:** [@inquirer/prompts (2025 rewrite)](https://www.npmjs.com/package/@inquirer/prompts)

**Prompt Types Disponibili:**
- `input` - Text input
- `select` - Choose from list (arrow keys)
- `checkbox` - Multi-select
- `confirm` - Yes/No
- `password` - Hidden input
- `editor` - Open editor per testo lungo

**Pattern Moderno (2025):**
```javascript
import { input, select, checkbox } from '@inquirer/prompts';

const projectName = await input({
  message: 'Project name:',
  default: 'my-project'
});

const projectType = await select({
  message: 'Project type:',
  choices: [
    { name: 'Web App', value: 'webapp' },
    { name: 'API', value: 'api' },
    { name: 'CLI Tool', value: 'cli' }
  ]
});
```

**Utilizzato da:** eslint, webpack, yarn, pm2, pnpm, Cypress, Google Lighthouse, AWS Amplify, GitHub Actions Toolkit

### 2.3 Rails Wizard Pattern

**Fonte:** [Wicked gem - Rails wizards](https://github.com/zombocom/wicked)

**Principi Architetturali:**

**1. Controller Architecture:**
- UNO controller per navigare tutti gli step
- Evitare controller per ogni step (code duplication)
- Controller = routing, Wizard = business logic

**2. Separation of Concerns:**
- Wizard separato dal controller
- Riusabile in contesti diversi
- Journey definito centralmente

**3. State Persistence Strategies:**
- **Server-side:** Persist partial data, user può refresh
- **Client-side:** Batch in memory, POST alla fine
- **Hybrid:** Persist per-step behind the scenes

**4. Design Considerations:**
- Reset state a inizio e fine journey
- Controller agnostic
- Every step visible in ONE place

### 2.4 Onboarding UX Best Practices

**Fonte:** [Multiple UX Research 2025](https://www.eleken.co/blog-posts/wizard-ui-pattern-explained)

**Progressive Disclosure:**
```
❌ SBAGLIATO: Bombardare utente con 50 domande upfront
✅ CORRETTO: Introdurre informazioni step-by-step

Esempio: Hiking guide
- Insegna mentre cammini
- Tooltips quando hover su button
- Hints solo quando feature first used
```

**Allow Re-access:**
- Onboarding può essere ri-triggered
- User può tornare quando serve
- Resource Centre con guide always accessible
- **"Give users a way BACK into guides"**

**Keep Content Brief:**
- Start con domande semplici (closed questions)
- Poi open-ended quando utente è comfortable
- Brief patterns + "additional help if needed"

**Provide Skip Options:**
- Progress indication sempre visibile
- Exit/skip option se onboarding > 4 screens
- **"Skip button can make a world of difference"**

**Avoid Generalized Experience:**
- Cater to specific user personas
- Not one-size-fits-all
- Customize basato su user answers

---

## 3. SESSION MANAGEMENT - STATE OF THE ART (2025)

### 3.1 Claude Code Session Management

**Fonte:** [Claude Code Documentation](https://stevekinney.com/courses/ai-development/claude-code-session-management)

**Features:**
- Sophisticated session persistence beyond conversation history
- Maintains: background processes, file contexts, permissions, working directories
- Commands:
  - `claude -c` / `claude --continue` → most recent
  - `claude -r "abc123"` → specific session by ID
  - `claude --resume` → list recent conversations
- **Session forking** per experimentation
- **Background task persistence** across sessions

**Problema Risolto:** "Context loss durante restart"

### 3.2 Gemini CLI Session Management

**Fonte:** [Google Developers Blog - Gemini CLI Sessions](https://developers.googleblog.com/pick-up-exactly-where-you-left-off-with-session-management-in-gemini-cli/)

**Game-Changer Feature (v0.20.0+):**

**1. Automatic Saving:**
- Sessions saved automaticamente
- NO user action required

**2. Project-Specific Context:**
```
Se switch directories → Gemini CLI AUTOMATICALLY switches context
Project A folder → History Project A
Project B folder → History Project B

ZERO confusion cross-project!
```

**3. Session Browser:**
- Type `/resume` to open browser
- Chronologically sorted conversations
- Preview summaries
- Search by ID o keywords
- Select one to restore

**4. Resume Commands:**
```bash
gemini --resume                # Most recent
gemini --resume 5              # Specific by number
gemini --resume <UUID>         # Specific by ID
gemini --list-sessions         # Show all
```

**5. History Management:**
- Config in `settings.json`
- `maxAge: "30d"` → auto-cleanup vecchie
- `maxCount: 100` → limit number stored

**What Gets Captured:**
- Conversation prompts + responses
- Tool execution details (inputs/outputs)
- Token usage metrics
- Assistant reasoning

**LESSON:** Project-specific context switching è GAME CHANGER!

### 3.3 GitHub Copilot CLI

**Fonte:** [DeepWiki - Copilot CLI Sessions](https://deepwiki.com/github/copilot-cli/3.3-session-management-and-history)

**Features:**
- Session lifecycle management
- Conversation state maintained across CLI launches
- Pause and resume work seamlessly
- Each session = unique sessionId
- Complete conversation history saved

**LESSON:** Persistence è STANDARD nel 2025, non optional!

---

## 4. PROJECT "CONSTITUTION" PATTERN

### 4.1 Project Manifesto Concept

**Fonte:** [Antonio Nieto-Rodriguez - Project Manifesto](https://antonionietorodriguez.com/project-manifesto/)

**Cosa è un Project Manifesto:**
> "Defines the aims and presents an image of a project management approach"

**12 Guiding Principles:**
1. Clear purpose aligned con strategic objectives
2. Define project scope (what, who, when, where, how, why)
3. Core values espliciti
4. Purpose and inspirations documentati
5. Objectives chiari
6. Solutions pathway definito
7. Simplification processes
8. Collaboration emphasis
9. Effective communication
10. Reduce bureaucracy
11. Accessible to experts AND non-experts
12. Adaptable to context

**Inspirato da:** Agile Manifesto (2001)

**APPLICAZIONE PER NOI:**
Ogni progetto CervellaSwarm = ha suo "manifesto"
Creato dal wizard iniziale
Mai più "cosa stavamo facendo?"

### 4.2 Setup Wizard Questions Best Practices

**Fonte:** [Setup Wizards Design](https://www.kryshiggins.com/the-design-of-setup-wizards/)

**Core Principles:**

**1. Set Expectations Upfront:**
```
Prima di wizard → Tell user:
- Quanto tempo richiede
- Cosa sarà chiesto
- Valore di completare setup
```

**2. Only Ask If Necessary:**
```
❌ Ask "What's your timezone?" se puoi auto-detect
✅ Ask "What's your timezone?" solo se auto-detect fails

"Set up as much as possible automatically"
```

**3. Check Preconditions:**
```
Prima di iniziare wizard:
- Necessary dependencies installed?
- Permissions available?
- Network reachable?

Se NO → Guide user verso fixing
```

**4. Action Over Information:**
```
❌ "Here's 10 pages explaining features"
✅ "Let's set up your first project"

Focus on DO, not READ
```

**5. Every Step Clear:**
```
User must understand:
- What wizard is asking
- Why it's asking
- Enough info to make decision
- What happens after answer
```

---

## 5. PROPOSTA DETTAGLIATA - NOSTRO WIZARD

### 5.1 Wizard Iniziale - Le Domande Strategiche

**Obiettivo:** Creare la "Costituzione del Progetto" in 5-7 minuti

**SEZIONE 1: IDENTITÀ PROGETTO (2-3 min)**

```
1. Project Name:
   [input con validation: no spaces, lowercase, alphanumeric]
   Default: cwd basename

   Why: Nome univoco per SNCP folder structure

2. Project Description:
   [text input, 1-2 frasi]
   Placeholder: "A web app that helps users..."

   Why: Context per AI, README seed

3. Project Type:
   [select]
   Options:
   - Web Application (frontend + backend)
   - API/Backend Service
   - CLI Tool
   - Library/Package
   - Data Analysis
   - Mobile App
   - Other (specify)

   Why: Determina quali agenti attivare, templates applicare
```

**SEZIONE 2: OBIETTIVO E SCOPE (2-3 min)**

```
4. Main Goal:
   [editor - opens text editor per risposta più lunga]
   Prompt: "What problem does this project solve? What's the end goal?"

   Example shown:
   "Build a task manager that helps developers track work across
   multiple projects without context switching overhead."

   Why: Diventa NORTH STAR del progetto

5. Success Criteria:
   [checkbox - multiple]
   "How will you know the project succeeded? (select all that apply)"
   Options:
   - [ ] Users actively using it
   - [ ] Revenue/profit generated
   - [ ] Problem personally solved
   - [ ] Portfolio/learning completed
   - [ ] Open source adoption
   - [ ] Other: ___________

   Why: Metrics chiari, evita scope creep

6. Timeline:
   [select]
   Options:
   - Quick prototype (1-2 weeks)
   - MVP (1-3 months)
   - Full product (3-6 months)
   - Long-term project (6+ months)
   - No deadline (exploratory)

   Why: Imposta aspettative, velocity dello sciame
```

**SEZIONE 3: TECH & TEAM (1-2 min)**

```
7. Tech Stack Known?
   [confirm] "Do you already know what technologies you'll use?"

   If YES:
     7a. [checkbox] Select all:
         - [ ] Frontend (React, Vue, Angular, ...)
         - [ ] Backend (Node, Python, Ruby, Go, ...)
         - [ ] Database (PostgreSQL, MongoDB, ...)
         - [ ] Other: ___________

   If NO:
     7a. [select] "What's your comfort level?"
         - Beginner (need recommendations)
         - Intermediate (open to suggestions)
         - Expert (I'll decide as I go)

   Why: Determina level di guidance da fornire

8. Working Mode:
   [select]
   - Solo (just you + swarm)
   - Small team (2-5 people)
   - Larger team (5+ people)

   Why: Coordination strategy, git workflow suggestions
```

**SEZIONE 4: PREFERENCES (30 sec - 1 min)**

```
9. Session Length Preference:
   [select]
   - Short sessions (30-60 min)
   - Medium sessions (1-3 hours)
   - Long sessions (3+ hours)
   - Variable (depends on task)

   Why: Auto-checkpoint timing, break suggestions

10. Notification Style:
    [select]
    - Minimal (errors only)
    - Standard (important updates)
    - Verbose (every step visible)

    Why: Logging level, UI verbosity
```

**FINALE: CONFERMA**

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   PROJECT CONSTITUTION PREVIEW                       ║
║                                                      ║
║   Name:        {project_name}                        ║
║   Goal:        {first_50_chars}...                   ║
║   Type:        {project_type}                        ║
║   Timeline:    {timeline}                            ║
║   Stack:       {tech_stack_summary}                  ║
║                                                      ║
║   This will be saved to:                             ║
║   .sncp/progetti/{name}/COSTITUZIONE.md              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

[E] Edit answers  [C] Confirm and initialize  [Q] Quit
```

### 5.2 Cosa Viene Creato dal Wizard

**File 1: `.sncp/progetti/{name}/COSTITUZIONE.md`**

```markdown
# Costituzione Progetto: {Name}

> Creato: {date}
> Ultima revisione: {date}

## Identità

**Nome:** {project_name}
**Tipo:** {project_type}
**Descrizione:** {description}

## Obiettivo Finale

{main_goal - testo completo user}

## Criteri di Successo

- [x] {criterion_1}
- [x] {criterion_2}
- [x] {criterion_3}

## Scope e Timeline

**Timeline target:** {timeline}
**Working mode:** {working_mode}

## Tech Stack

{tech_stack_details o "To be determined"}

## Preferenze Team

**Session length:** {session_pref}
**Notifications:** {notification_style}

---

*Questa costituzione è il NORTH STAR del progetto.*
*Se mai ci sentiamo persi, torniamo QUI.*
```

**File 2: `.sncp/progetti/{name}/stato.md`**

```markdown
# Stato {Project Name}

> Ultimo aggiornamento: {date}

## TL;DR

Progetto appena inizializzato! Ready to start.

## Next Steps

1. [ ] Define initial architecture
2. [ ] Set up development environment
3. [ ] First implementation spike

## Note

Wizard completato: {timestamp}
```

**File 3: `.sncp/progetti/{name}/PROMPT_RIPRESA_{name}.md`**

```markdown
# PROMPT RIPRESA - {Project Name}

> Ultimo aggiornamento: {date}

## Progetto

{Copia delle info essenziali da COSTITUZIONE}

## Dove Siamo

Appena iniziato! Prima sessione.

## Prossimi Step

{Dipende dal project_type}

Per web app:
1. Setup project structure
2. Initialize git repo
3. Create frontend boilerplate

Per API:
1. Define API contracts
2. Setup backend framework
3. Database schema design

etc...
```

**File 4: `.sncp/progetti/{name}/roadmap/ROADMAP.md`**

```markdown
# Roadmap {Project Name}

(Template basato su project_type + timeline)

## Phase 1: Setup (Week 1)
- [ ] Environment configuration
- [ ] Dependencies installed
- [ ] First "Hello World"

## Phase 2: Core Features (Weeks 2-4)
...

(Auto-generated basato su risposte wizard)
```

**Cartelle Create:**

```
.sncp/progetti/{name}/
├── COSTITUZIONE.md          ← NORTH STAR
├── stato.md                 ← Current state
├── PROMPT_RIPRESA_{name}.md ← Session resume
├── idee/                    ← Ideas & research
├── decisioni/               ← Decisions with WHY
├── reports/                 ← Test reports, audits
├── roadmap/
│   └── ROADMAP.md           ← Auto-generated roadmap
└── workflow/                ← Custom protocols
```

### 5.3 Flusso Prima Sessione - EXACTLY

**STEP 1: User runs command**

```bash
$ cervella-swarm init

╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🧠 CervellaSwarm Project Initialization            ║
║                                                      ║
║   Let's create your project constitution.            ║
║   This takes ~5 minutes and prevents you from        ║
║   ever having to re-explain your project.            ║
║                                                      ║
║   (Press Ctrl+C anytime to cancel)                   ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

Press Enter to start...
```

**STEP 2: Wizard questions (5-7 min)**

```
[Progress: 1/10]
━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? Project name: › my-awesome-app

[Validating... ✓]

[Progress: 2/10]
━━━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? Brief description: › A task manager for developers

...
(continue through 10 questions)
```

**STEP 3: Confirmation & Creation**

```
[Progress: 10/10]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ All questions answered!

Generating your project constitution...

✓ Created .sncp/progetti/my-awesome-app/
✓ Generated COSTITUZIONE.md
✓ Generated PROMPT_RIPRESA_my-awesome-app.md
✓ Generated roadmap template
✓ Initialized git (optional)

╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🎉 Project initialized successfully!               ║
║                                                      ║
║   Your project constitution is ready.                ║
║   You'll never need to re-explain your goals.        ║
║                                                      ║
║   Next: Start your first work session                ║
║   $ cervella-swarm start                             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

**STEP 4: First Work Session**

```bash
$ cervella-swarm start

Loading project: my-awesome-app...

✓ Constitution loaded
✓ 16 agents ready
✓ Context initialized

╔══════════════════════════════════════════════════════╗
║   Project: My Awesome App                            ║
║   Goal: A task manager for developers                ║
║   Session: #1                                        ║
╚══════════════════════════════════════════════════════╝

Regina: Ciao! Ho letto la costituzione del progetto.
        So che vogliamo costruire un task manager.
        Cosa vuoi fare oggi?

You: Let's design the database schema

Regina: Perfetto! Lancio cervella-data per schema design.
        Ti tengo aggiornato...

[Work happens...]

You: Done for today

Regina: Ottimo lavoro! Salvo tutto...

✓ stato.md updated
✓ PROMPT_RIPRESA updated
✓ Session saved

Arrivederci! 👋
```

**STEP 5: Second Session (Il giorno dopo)**

```bash
$ cervella-swarm start

Loading project: my-awesome-app...

✓ Constitution loaded
✓ Previous session found (#1)
✓ Context restored

╔══════════════════════════════════════════════════════╗
║   Project: My Awesome App                            ║
║   Goal: A task manager for developers                ║
║   Session: #2                                        ║
║   Last session: Yesterday, 14:30                     ║
╚══════════════════════════════════════════════════════╝

Regina: Ciao! Ieri abbiamo lavorato sul database schema.
        cervella-data ha creato 5 tabelle.
        Vuoi continuare da lì o fare altro?

[R] Resume from yesterday  [N] New task  [S] Show status

You: r

Regina: Ok! Riprendo dove abbiamo lasciato...
```

**MAGIC MOMENT:**

```
L'utente NON ha dovuto dire:
- ❌ "Sto costruendo un task manager"
- ❌ "Il goal è X"
- ❌ "Ieri stavamo lavorando su Y"

La Regina SA TUTTO perché:
✓ COSTITUZIONE.md ha il context
✓ PROMPT_RIPRESA ha ultimo stato
✓ stato.md ha details
✓ Session #1 saved completamente

ZERO ri-spiegazione!
```

### 5.4 Flusso Terza Sessione (Una settimana dopo)

```bash
$ cervella-swarm start

Loading project: my-awesome-app...

⚠️  Last session was 7 days ago

╔══════════════════════════════════════════════════════╗
║   Welcome back!                                      ║
║                                                      ║
║   It's been a week since your last session.          ║
║   Would you like a quick recap?                      ║
║                                                      ║
║   [Y] Yes, show me where we are                      ║
║   [N] No, I remember                                 ║
║   [D] Detailed status report                         ║
╚══════════════════════════════════════════════════════╝

You: y

Regina: Ecco un quick recap:

PROJECT: My Awesome App (Task manager for developers)

PROGRESS:
✓ Database schema designed (5 tables)
✓ Backend API structure planned
⚠ Frontend not started yet

LAST WORKED ON:
- Session #2 (7 days ago): API endpoint definitions

NEXT LOGICAL STEPS:
1. Implement first API endpoints
2. Set up authentication
3. Start frontend boilerplate

What would you like to do?
```

**AGAIN:**
- ❌ User NON ha dovuto spiegare tutto
- ✓ System SA context completo
- ✓ Suggestions intelligenti basate su stato
- ✓ Frictionless re-engagement

---

## 6. MECCANISMO DI RIPRESA ROBUSTO

### 6.1 Session Management Architecture

**Inspired by:** Gemini CLI + Claude Code patterns

**COMPONENTS:**

**1. Session Store** (`.sncp/progetti/{name}/sessions/`)

```
sessions/
├── session_001.json
├── session_002.json
├── session_003.json
└── current -> session_003.json (symlink)
```

**Session File Structure:**

```json
{
  "id": "sess_20260115_143022",
  "number": 3,
  "started": "2026-01-15T14:30:22Z",
  "ended": "2026-01-15T16:45:10Z",
  "duration_minutes": 135,
  "tasks_completed": [
    {
      "description": "Design database schema",
      "agent": "cervella-data",
      "files_modified": ["schema.sql", "models.py"],
      "result": "success"
    }
  ],
  "decisions_made": [
    {
      "what": "Use PostgreSQL instead of MongoDB",
      "why": "Need relational integrity for task dependencies",
      "who": "Regina + cervella-data",
      "when": "2026-01-15T14:45:00Z"
    }
  ],
  "next_suggested": [
    "Implement authentication endpoints",
    "Set up database migrations",
    "Design user model"
  ],
  "context_snapshot": {
    "files_in_focus": ["backend/models/", "backend/routes/"],
    "agents_used": ["cervella-data", "cervella-backend"],
    "mood": "productive"
  }
}
```

**2. Project Context Manager**

```python
class ProjectContext:
    def __init__(self, project_name):
        self.constitution = self.load_constitution(project_name)
        self.stato = self.load_stato(project_name)
        self.prompt_ripresa = self.load_prompt_ripresa(project_name)
        self.sessions = self.load_sessions(project_name)
        self.last_session = self.get_last_session()

    def get_resume_summary(self, detail_level='quick'):
        """Generate resumption context based on detail level"""
        if detail_level == 'quick':
            return self._quick_recap()
        elif detail_level == 'detailed':
            return self._detailed_status()
        elif detail_level == 'full':
            return self._full_context()

    def _quick_recap(self):
        """Last session + next steps"""
        return {
            'project_goal': self.constitution['main_goal'],
            'last_worked': self.last_session['ended'],
            'last_tasks': self.last_session['tasks_completed'][-3:],
            'next_suggested': self.last_session['next_suggested']
        }
```

**3. Session Resumption Flow**

```python
def resume_session(project_name):
    ctx = ProjectContext(project_name)

    days_since_last = (now() - ctx.last_session['ended']).days

    if days_since_last == 0:
        # Same day - likely remember everything
        print("Welcome back! Continuing from earlier...")
        return ctx.get_resume_summary('quick')

    elif days_since_last <= 3:
        # Few days - might need quick reminder
        print(f"Welcome back! It's been {days_since_last} days.")
        return ctx.get_resume_summary('quick')

    elif days_since_last <= 7:
        # Week - offer recap
        print(f"Welcome back! It's been {days_since_last} days.")
        if confirm("Show recap?"):
            return ctx.get_resume_summary('detailed')

    else:
        # Long time - definitely show recap
        print(f"Welcome back! It's been {days_since_last} days.")
        return ctx.get_resume_summary('detailed')
```

### 6.2 Progressive Re-engagement

**Inspired by:** Onboarding UX research - progressive disclosure

**LEVELS OF CONTEXT:**

**Level 0: Instant (< 1 hour since last)**
```
No recap needed. Just continue.
```

**Level 1: Same Day (< 24 hours)**
```
╔═══════════════════════════════════════╗
║ Last: 2 hours ago                     ║
║ Task: API design                      ║
╚═══════════════════════════════════════╝
```

**Level 2: Recent (1-3 days)**
```
╔═══════════════════════════════════════╗
║ Last session: 2 days ago              ║
║                                       ║
║ Completed:                            ║
║ ✓ Database schema                     ║
║ ✓ User model                          ║
║                                       ║
║ Next: API endpoints                   ║
╚═══════════════════════════════════════╝
```

**Level 3: Medium Gap (4-7 days)**
```
╔═══════════════════════════════════════╗
║ PROJECT: My Awesome App               ║
║ Goal: Task manager for developers     ║
║                                       ║
║ Last session: 5 days ago              ║
║                                       ║
║ Progress:                             ║
║ ▓▓▓▓▓▓▓░░░░░░░░ 35%                  ║
║                                       ║
║ Completed:                            ║
║ ✓ Database design                     ║
║ ✓ Backend structure                   ║
║                                       ║
║ In Progress:                          ║
║ ⚡ API implementation                  ║
║                                       ║
║ Next suggested:                       ║
║ 1. Complete auth endpoints            ║
║ 2. Set up testing framework           ║
║ 3. Start frontend                     ║
╚═══════════════════════════════════════╝

[D] Detailed report  [C] Continue  [H] Help
```

**Level 4: Long Gap (7+ days)**
```
╔═══════════════════════════════════════╗
║ 🧠 FULL PROJECT RECAP                 ║
╚═══════════════════════════════════════╝

PROJECT CONSTITUTION:
─────────────────────
Name: My Awesome App
Goal: Build a task manager that helps
      developers track work across multiple
      projects without context switching.

Success Criteria:
✓ Solve personal pain point
✓ Open source adoption
□ 100+ active users

PROGRESS SUMMARY:
─────────────────
Timeline: MVP (1-3 months)
Started: 3 weeks ago
Sessions: 7 total
Time invested: 18 hours

WHAT'S DONE:
─────────────
✓ Database schema (PostgreSQL)
  - users, projects, tasks, tags, task_deps
✓ Backend API structure (FastAPI)
  - Authentication planned
  - CRUD endpoints designed
✓ Git repo initialized

WHAT'S IN PROGRESS:
───────────────────
⚡ API Implementation (50% done)
  - User endpoints: ✓ Done
  - Project endpoints: 🚧 In progress
  - Task endpoints: ⏳ Not started

LAST WORKED ON:
───────────────
Session #7 (12 days ago)
Task: Implemented user registration + login
Agent: cervella-backend
Result: Working authentication flow

BLOCKERS/ISSUES:
────────────────
None currently!

NEXT STEPS:
───────────
1. Complete project CRUD endpoints
2. Start task endpoints
3. Set up testing (pytest)
4. Frontend boilerplate (React)

Ready to continue? [Y/n]
```

### 6.3 Re-access Mechanism

**Inspired by:** "Allow users to re-access guidance"

**COMMANDS ALWAYS AVAILABLE:**

```bash
# During any session:

/status          # Quick status (Level 2 recap)
/recap           # Full recap (Level 4)
/constitution    # Show project constitution
/sessions        # List all sessions
/session 5       # Show specific session details
/decisions       # Show all decisions made with WHY
/progress        # Visual progress dashboard
/help            # Context-sensitive help
```

**Example `/progress` Output:**

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   MY AWESOME APP - PROGRESS DASHBOARD                ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   PHASE 1: SETUP                        ✓ 100%      ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                              ║
║                                                      ║
║   PHASE 2: BACKEND                      ⚡ 60%       ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░                              ║
║   • Database schema       ✓ Done                     ║
║   • API structure         ✓ Done                     ║
║   • Authentication        ✓ Done                     ║
║   • CRUD endpoints        🚧 60%                     ║
║   • Testing framework     ⏳ Not started              ║
║                                                      ║
║   PHASE 3: FRONTEND                     ⏳ 0%        ║
║   ░░░░░░░░░░░░░░░░░░░░                              ║
║                                                      ║
║   OVERALL PROGRESS:       35% complete               ║
║   Sessions: 7  |  Hours: 18  |  Days active: 21     ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

Type /sessions to see session history
Type /recap for detailed status
```

---

## 7. ANTI-PATTERNS DA EVITARE

### 7.1 Lezioni dal Research

**Cosa NON Fare:**

**❌ 1. Wizard Troppo Lungo**
```
PROBLEMA: 61% drop-off se troppo complesso
LIMITE: Max 10 domande, max 7 minuti
SKIP: Offer skip per advanced users
```

**❌ 2. Domande Generiche**
```
PROBLEMA: Generalized onboarding = poor fit
SBAGLIATO: "What kind of project?" (troppo vago)
CORRETTO: "What kind of project?" + smart defaults per type
```

**❌ 3. No Way Back**
```
PROBLEMA: User fa errore, deve rifare tutto
SOLUZIONE: [E] Edit sempre disponibile
          /constitution edit command
```

**❌ 4. Form Overload**
```
PROBLEMA: Ogni campo extra = chance to drop off
REGOLA: "Does this NEED to be asked now?"
        Se può aspettare → NON chiedere
```

**❌ 5. No Progress Indication**
```
PROBLEMA: User non sa quanto manca
SOLUZIONE: [Progress: 3/10] sempre visibile
```

**❌ 6. Fail Silently**
```
PROBLEMA: Validation error, user confused
SOLUZIONE: Immediate feedback con fix suggestions
```

**❌ 7. One-Size-Fits-All**
```
PROBLEMA: Expert users annoyed, beginners lost
SOLUZIONE: Detect expertise level, adjust accordingly
```

### 7.2 Context Loss Anti-Patterns

**Cosa NON Fare:**

**❌ 1. Assume User Remembers**
```
SBAGLIATO:
  Regina: "Ready to continue?"
  (User dopo 2 settimane: Continue WHAT?!)

CORRETTO:
  Regina: "Last time we worked on X.
           Want to continue with Y?"
```

**❌ 2. Context in Memory Only**
```
SBAGLIATO: Tenere tutto in memory corrente
           Restart = tutto perso

CORRETTO: Persist to disk ALWAYS
          .sncp/progetti/{name}/sessions/
```

**❌ 3. No Project Switching Support**
```
SBAGLIATO: User switch project → confusion

CORRETTO: Automatic context switch basato su cwd
          (Gemini CLI pattern!)
```

**❌ 4. Generic Error Messages**
```
SBAGLIATO: "Error loading project"
CORRETTO: "Project 'X' not found.
           Did you mean 'Y'?
           Or run: cervella-swarm init"
```

---

## 8. IMPLEMENTATION ROADMAP

### 8.1 Phase 1: Core Wizard (Week 1-2)

**Priority 1:**
- [ ] Implement `cervella-swarm init` command
- [ ] 10 strategic questions with inquirer.js
- [ ] Generate COSTITUZIONE.md
- [ ] Generate initial PROMPT_RIPRESA
- [ ] Create folder structure

**Tech:**
- Node.js script
- @inquirer/prompts library
- Template engine (Handlebars?)
- File system operations

**Success Criteria:**
- Can initialize new project in < 7 minutes
- All 10 questions have smart defaults
- Generated files are human-readable
- Skip option available for advanced users

### 8.2 Phase 2: Session Management (Week 3-4)

**Priority 2:**
- [ ] Session recording (JSON format)
- [ ] `cervella-swarm start` with context loading
- [ ] Session history (`/sessions` command)
- [ ] Resume flow with recap levels
- [ ] Project auto-detection (based on cwd)

**Tech:**
- Session store in `.sncp/progetti/{name}/sessions/`
- ProjectContext manager class
- Resume logic with time-based recap levels

**Success Criteria:**
- Can resume session after restart
- Correct recap level shown based on gap
- Zero context loss
- Project switching works automatically

### 8.3 Phase 3: Progressive Re-engagement (Week 5-6)

**Priority 3:**
- [ ] In-session commands (`/status`, `/recap`, etc.)
- [ ] Progress dashboard visualization
- [ ] Decision tracking and display
- [ ] Re-edit constitution command

**Tech:**
- Command parser for `/commands`
- ASCII art dashboard
- Markdown rendering in terminal

**Success Criteria:**
- User can check status anytime
- Decisions are traceable
- Constitution is editable post-init
- Help is context-sensitive

### 8.4 Phase 4: Polish & Testing (Week 7-8)

**Priority 4:**
- [ ] Error handling & validation
- [ ] Help system comprehensive
- [ ] Templates for common project types
- [ ] Migration tool for existing projects
- [ ] Documentation complete

**Tech:**
- Error recovery flows
- Help content database
- Project templates (web-app, api, cli, etc.)

**Success Criteria:**
- New user can complete wizard without confusion
- Existing SNCP projects can migrate
- Error messages are helpful not cryptic
- Documentation covers all flows

---

## 9. METRICS & VALIDATION

### 9.1 Success Metrics

**Wizard Completion:**
- **Target:** >80% of users complete wizard
- **Measure:** Track started vs completed
- **Red flag:** >30% drop-off at any single question

**Session Resumption:**
- **Target:** <30 seconds to resume context
- **Measure:** Time from `start` to "ready to work"
- **Red flag:** User asks "what was I doing?"

**Re-explanation Frequency:**
- **Target:** <5% of sessions start with user re-explaining
- **Measure:** Count times user says "I'm working on X" when X is in constitution
- **Red flag:** >15% re-explanation rate

**Long-term Engagement:**
- **Target:** Users return after 7+ day gap
- **Measure:** Sessions after 1 week inactive
- **Red flag:** <20% return rate after gap

### 9.2 User Testing Protocol

**Phase 1: Internal (Rafa + Cervella)**
1. Use wizard on 3 different project types
2. Test session resume after 1 day, 3 days, 7 days
3. Deliberately break flow, test error recovery
4. Document every friction point

**Phase 2: Alpha (5-10 developers)**
1. Give wizard with minimal explanation
2. Track completion time and drop-offs
3. Survey: "Did you have to re-explain your project?"
4. Iterate based on feedback

**Phase 3: Beta (50-100 developers)**
1. Public release
2. Anonymous usage metrics
3. In-app feedback prompts
4. Monitor support requests

---

## 10. FINAL RECOMMENDATIONS

### 10.1 Top Priorities

**DO FIRST:**
1. ✅ **Implement Core Wizard** - 10 questions, generates constitution
2. ✅ **Session Save/Restore** - Basic persistence
3. ✅ **Project Auto-Detection** - Switch projects = switch context

**DO SECOND:**
4. ✅ **Time-Based Recaps** - Smart resumption based on gap
5. ✅ **In-Session Commands** - `/status`, `/recap`, `/help`
6. ✅ **Progress Dashboard** - Visual feedback

**DO THIRD:**
7. ✅ **Templates** - Common project types
8. ✅ **Migration Tool** - For existing projects
9. ✅ **Polish** - Error messages, help system

### 10.2 Decision Matrix

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| Core Wizard (10 Q) | **CRITICAL** | Medium | **P0** |
| Constitution Generation | **CRITICAL** | Low | **P0** |
| Session Persistence | **CRITICAL** | Medium | **P0** |
| Project Auto-Detection | **HIGH** | Low | **P1** |
| Time-Based Recaps | **HIGH** | Medium | **P1** |
| In-Session Commands | **MEDIUM** | Medium | **P2** |
| Progress Dashboard | **MEDIUM** | High | **P2** |
| Project Templates | **LOW** | Medium | **P3** |
| Migration Tool | **LOW** | High | **P3** |

### 10.3 The Killer Feature

> **"You define your project ONCE. Never re-explain."**

Questo è il nostro differenziale. Cursor non ha questo perché IDE = sempre visibile. Noi CLI = context loss risk MASSIMO. Quindi wizard robusto è SURVIVAL.

**Marketing Angle:**
```
"Other AI tools forget your project every time.
CervellaSwarm remembers forever.

Define your goal once. Work for months.
Never re-explain what you're building."
```

### 10.4 Success Scenario (3 Months In)

```
User Story:

Day 1: Run `cervella-swarm init`
       Answer 10 questions (6 minutes)
       "Cool! Let's start working."

Day 3: Run `cervella-swarm start`
       "Welcome back! Continuing API work..."
       "Perfect, no re-explaining needed!"

Day 15: Run `cervella-swarm start`
        "It's been 2 weeks. Quick recap?"
        Shows recap. "Ah yes! Let's continue."

Day 60: Run `cervella-swarm start`
        Full recap shown automatically.
        "Oh right! We were building X. Let's go!"

Review: "I've never used a tool that REMEMBERS
         like this. I can take breaks and come
         back without losing momentum. 10/10."
```

---

## 11. SOURCES

### CLI Best Practices
- [Node.js CLI Apps Best Practices](https://github.com/lirantal/nodejs-cli-apps-best-practices) - Lirantal
- [Best practices for building CLI and publishing to NPM](https://webbylab.com/blog/best-practices-for-building-cli-and-publishing-it-to-npm/)

### Interactive Prompts
- [@inquirer/prompts](https://www.npmjs.com/package/@inquirer/prompts) - Modern inquirer.js rewrite
- [Enquirer](https://github.com/enquirer/enquirer) - Stylish CLI prompts
- [How To Create Interactive Command-line Prompts with Inquirer.js](https://www.digitalocean.com/community/tutorials/nodejs-interactive-command-line-prompts)

### Wizard Patterns
- [Wicked gem - Rails wizards](https://github.com/zombocom/wicked)
- [Wizards in Ruby on Rails](https://ollie.treend.uk/posts/wizards/)
- [Wizard UI Pattern Explained](https://www.eleken.co/blog-posts/wizard-ui-pattern-explained)

### Onboarding UX
- [Airtable Onboarding Wizard Best Practices](https://www.candu.ai/blog/airtables-best-wizard-onboarding-flow)
- [19 Onboarding UX Examples](https://userpilot.com/blog/onboarding-ux-examples/)
- [UX Onboarding Best Practices 2025](https://www.uxdesigninstitute.com/blog/ux-onboarding-best-practices-guide/)
- [I studied 200+ onboarding flows](https://designerup.co/blog/i-studied-the-ux-ui-of-over-200-onboarding-flows-heres-everything-i-learned/)

### Session Management
- [Pick up where you left off - Gemini CLI](https://developers.googleblog.com/pick-up-exactly-where-you-left-off-with-session-management-in-gemini-cli/)
- [Claude Code Session Management](https://stevekinney.com/courses/ai-development/claude-code-session-management)
- [How I Solved Claude Code's Context Loss Problem](https://dev.to/kaz123/how-i-solved-claude-codes-context-loss-problem-with-a-lightweight-session-manager-265d)

### Context Loss Problems
- [Severe Session Memory Loss - Claude Code Issue #2545](https://github.com/anthropics/claude-code/issues/2545)
- [Context Loss during Updates - Cursor Forum](https://forum.cursor.com/t/critical-bug-ai-session-context-loss-during-mandatory-updates/148192)
- [Session Resumption Feature Request - Claude Code #1340](https://github.com/anthropics/claude-code/issues/1340)

### Project Manifesto
- [Project Manifesto - Antonio Nieto-Rodriguez](https://antonionietorodriguez.com/project-manifesto/)
- [Draft a Project Manifesto](https://kristofberg.medium.com/draft-a-project-manifesto-c006dadbc3ac)

### Setup Wizards
- [The design of setup wizards](https://www.kryshiggins.com/the-design-of-setup-wizards/)
- [Creating a setup wizard (and when you shouldn't)](https://blog.logrocket.com/ux-design/creating-setup-wizard-when-you-shouldnt/)
- [Setup Wizards - Sentry](https://develop.sentry.dev/sdk/expected-features/setup-wizards/)

### Statistics & Research
- [Frictionless Customer Onboarding](https://userpilot.com/blog/frictionless-customer-onboarding/)
- [How to Identify & Fix User Friction](https://whatfix.com/blog/user-friction/)
- [Fintech onboarding: 6 UX practices that reduce drop-off](https://www.eleken.co/blog-posts/fintech-onboarding-simplification)

---

## 12. CONSTITUTION APPLICATION

**COSTITUZIONE-APPLIED:** SI

**Principio usato:** "Nulla è complesso - solo non ancora studiato!"

**Come applicato:**
Il problema sembrava complesso: "Come evitiamo che utenti debbano ri-spiegare?"

Ma studiando:
- CLI tools best practices
- Gemini/Claude Code session management
- Onboarding UX research
- Wizard design patterns

Ho scoperto che:
1. È un problema NOTO (61% drop-off, context loss issue #1 nel 2025)
2. Esistono SOLUZIONI validate (session management, project manifesto)
3. Abbiamo già VANTAGGIO (SNCP = perfect foundation)

**Risultato:** Da "complesso e vago" a "roadmap chiara in 8 settimane"

**Altri principi applicati:**
- "Studiare prima di agire" → 45 minuti ricerca → proposta solida
- "I player grossi hanno già risolto" → Gemini CLI, Claude Code studiati
- "Non reinventiamo la ruota" → Adaptiamo pattern esistenti

---

**Ricerca completata:** 15 Gennaio 2026
**Tempo impiegato:** ~60 minuti
**Fonti consultate:** 30+ articoli, documentazione, papers
**Confidenza findings:** ALTA - Multiple fonti concordanti

*"Il wizard non è un extra. È la fondazione dell'intera UX."* 🔬

---

**PROSSIMA AZIONE:** Review con Regina per approvazione approccio e decisione su timeline implementazione.
