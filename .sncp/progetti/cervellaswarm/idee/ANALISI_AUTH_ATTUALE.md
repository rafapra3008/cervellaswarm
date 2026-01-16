# Analisi Autenticazione e Onboarding - CervellaSwarm CLI

> **Data:** 16 Gennaio 2026
> **Analista:** cervella-ingegnera
> **Stato:** COMPLETA

---

## EXECUTIVE SUMMARY

**Status:** ⚠️ AUTENTICAZIONE MINIMA - ONBOARDING PRESENTE MA SEMPLICE

**Health Score:** 4/10

**Situazione Attuale:**
- Autenticazione: Solo `ANTHROPIC_API_KEY` via environment variable
- Onboarding: Wizard interattivo funzionante ma NO registrazione utente
- Storage config: File-based locale (`.sncp/`), nessun config globale persistente
- Dipendenze esterne: Standalone (non dipende da Claude Code)

**Gap Critici:**
1. NO registrazione utente/account
2. NO storage sicuro delle credenziali
3. NO gestione team/workspace
4. Package `conf` installato ma NON usato

---

## 1. FILE DI CONFIGURAZIONE

### Dove Salviamo Config?

**Attualmente:**

```
.sncp/progetti/{projectName}/
├── COSTITUZIONE.md          # Generata dal wizard
├── stato.md                 # Stato progetto
├── PROMPT_RIPRESA_{nome}.md # Context ripresa
└── sessions/                # Sessioni locali (JSON)
```

**NO config globale utente:**
- `~/.cervellaswarm/` NON ESISTE
- Package `conf` in `package.json` ma NON USATO nel codice
- Credenziali: solo `process.env.ANTHROPIC_API_KEY`

### File `.env.example`

```bash
# CervellaSwarm Configuration
# Copy this to .env and fill in your values

# Anthropic API Key (REQUIRED for agent execution)
# Get your key at: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**Problema:** L'utente deve gestire manualmente `export` della variabile.

---

## 2. COMANDO INIT

### Cosa Fa `cervellaswarm init`?

**File:** `packages/cli/src/commands/init.js`

```javascript
export async function initCommand(options) {
  // 1. Check se già inizializzato
  if (isAlreadyInitialized() && !options.force) {
    return; // Esce
  }

  // 2. Wizard o default
  if (options.yes) {
    // Quick init: usa default
  } else {
    // Interactive wizard: 10 domande
    const answers = await runWizard();
  }

  // 3. Crea struttura
  await initSNCP(answers);
  await generateConstitution(answers);
}
```

**NON chiede:**
- Email utente
- Password
- Account CervellaSwarm
- API key (assume sia già settata)

**Chiede solo:**
- Nome progetto
- Descrizione
- Tipo progetto
- Goals
- Tech stack
- Working mode
- Session preferences
- Notification style

**Output:** Crea `.sncp/progetti/{nome}/` con file progetto.

---

## 3. INTEGRAZIONE CON CLAUDE/ANTHROPIC API

### Come Comunichiamo?

**File:** `packages/cli/src/agents/spawner.js`

```javascript
function getApiKey() {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) {
    return null;
  }
  return key;
}

export async function spawnAgent(agent, description, context, options = {}) {
  const apiKey = getApiKey();

  if (!apiKey) {
    console.log('  ANTHROPIC_API_KEY not found.');
    console.log('  1. Get your key at: https://console.anthropic.com/');
    console.log('  2. Set it: export ANTHROPIC_API_KEY=sk-ant-...');
    return {
      success: false,
      error: 'ANTHROPIC_API_KEY not set',
    };
  }

  const client = new Anthropic({ apiKey });
  const message = await client.messages.create({
    model: DEFAULT_MODEL,
    max_tokens: maxTokens,
    system: systemPrompt,
    messages: [{ role: 'user', content: description }]
  });
}
```

**Autenticazione:**
- ✅ Usa `@anthropic-ai/sdk` ufficiale
- ✅ API key da environment
- ❌ NO OAuth
- ❌ NO gestione refresh token
- ❌ NO storage sicuro key

**Retry Logic:**
- ✅ Max 3 retry automatici
- ✅ Gestione rate limit (429)
- ✅ Gestione errori server (500, 503)
- ✅ Timeout configurabile (default 2 min)

---

## 4. FLUSSO ATTUALE PER NUOVO UTENTE

### User Journey

```
1. Installazione
   $ npm install -g cervellaswarm
   
2. Ottieni API key (MANUALE)
   → Utente va su console.anthropic.com
   → Crea account Anthropic (SE non ha)
   → Genera API key
   
3. Setta API key (MANUALE)
   $ export ANTHROPIC_API_KEY=sk-ant-...
   
4. Init progetto
   $ cd my-project
   $ cervellaswarm init
   → Wizard 10 domande
   → Crea .sncp/progetti/my-project/
   
5. Primo task
   $ cervellaswarm task "create API"
   → Verifica ANTHROPIC_API_KEY
   → Spawna agent
   → Salva session locale
```

### Pain Points Identificati

1. **API Key Management**
   - Utente deve fare `export` manualmente
   - NON persistente tra shell session
   - NO validazione durante init
   - NO check se key valida

2. **NO Account CervellaSwarm**
   - Nessuna registrazione
   - Nessun user profile
   - Nessun workspace/team

3. **NO Onboarding Guidato**
   - Assume che utente sappia cosa fare
   - NO tutorial first-run
   - NO health check setup

---

## 5. DIPENDENZE

### Dipende da Claude Code?

**NO. Completamente standalone.**

**Package.json:**
```json
"dependencies": {
  "@anthropic-ai/sdk": "^0.39.0",    // ✅ Comunicazione diretta API
  "@inquirer/prompts": "^7.2.0",     // ✅ Wizard interattivo
  "boxen": "^8.0.1",                 // UI
  "chalk": "^5.3.0",                 // Colori
  "commander": "^12.1.0",            // CLI parser
  "conf": "^13.0.1",                 // ❌ INSTALLATO MA NON USATO!
  "figures": "^6.1.0",               // Icons
  "handlebars": "^4.7.8",            // Templates
  "ora": "^8.1.1"                    // Spinner
}
```

**Nota Critica:** `conf` è installato ma MAI importato nel codice!

```bash
$ grep -r "import.*conf" packages/cli/src/
# NO RESULTS!
```

---

## GAP IDENTIFICATI

### CRITICI (da risolvere prima di v1.0)

| Gap | Severità | Impatto |
|-----|----------|---------|
| NO storage sicuro API key | CRITICO | Sicurezza utente |
| NO validazione API key su init | ALTO | UX first-run terribile |
| Package `conf` non usato | MEDIO | Spreco dipendenza |
| NO gestione multi-project | ALTO | Scalabilità limitata |

### ALTI (pianificare)

| Gap | Severità | Impatto |
|-----|----------|---------|
| NO account CervellaSwarm | ALTO | No analytics, no premium features |
| NO team/workspace | ALTO | Solo uso solo developer |
| NO tutorial first-run | MEDIO | Barriera ingresso alta |

### MEDI (backlog)

| Gap | Severità | Impatto |
|-----|----------|---------|
| NO health check setup | MEDIO | Debug problemi setup difficile |
| API key in env non persistente | MEDIO | Utente deve ri-export ogni volta |
| NO analytics usage | BASSO | No insights su come usano CLI |

---

## SUGGERIMENTI

### 1. IMMEDIATE (questa settimana)

**A. Usa package `conf` per config globale**

```javascript
// packages/cli/src/config/manager.js
import Conf from 'conf';

const config = new Conf({
  projectName: 'cervellaswarm',
  schema: {
    apiKey: { type: 'string' },
    userId: { type: 'string' },
    projects: { type: 'array' }
  }
});

export function saveApiKey(key) {
  config.set('apiKey', key);
}

export function getApiKey() {
  return config.get('apiKey') || process.env.ANTHROPIC_API_KEY;
}
```

**Dove salva:** `~/.config/cervellaswarm-nodejs/config.json`

**B. Wizard API key durante init**

```javascript
// Se ANTHROPIC_API_KEY non settata
if (!process.env.ANTHROPIC_API_KEY && !config.get('apiKey')) {
  console.log('No API key found.');
  const hasKey = await confirm('Do you have an Anthropic API key?');
  
  if (hasKey) {
    const key = await password('Enter your API key:');
    config.set('apiKey', key);
  } else {
    console.log('Get one at: https://console.anthropic.com/');
    process.exit(1);
  }
}
```

**C. Validazione API key**

```javascript
async function validateApiKey(key) {
  try {
    const client = new Anthropic({ apiKey: key });
    // Chiama endpoint lightweight per test
    await client.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 10,
      messages: [{ role: 'user', content: 'test' }]
    });
    return true;
  } catch (error) {
    if (error.status === 401) return false;
    throw error;
  }
}
```

### 2. SHORT-TERM (prossime 2 settimane)

**A. Health Check Setup**

```bash
$ cervellaswarm doctor

✓ Node.js version: 18.x
✓ API key configured
✓ API key valid
✓ Project initialized
✓ Last session: 2 hours ago

All systems operational!
```

**B. First-Run Tutorial**

```javascript
// Dopo primo init
if (isFirstRun()) {
  console.log('\n🎉 Welcome to CervellaSwarm!\n');
  const wantTutorial = await confirm('Want a 2-minute tutorial?');
  
  if (wantTutorial) {
    await runTutorial(); // Guided tour
  }
}
```

**C. Multi-Project Management**

```bash
$ cervellaswarm projects list
$ cervellaswarm projects switch my-app
$ cervellaswarm projects add new-project
```

### 3. MEDIUM-TERM (prossimo mese)

**A. Account CervellaSwarm (opzionale)**

```javascript
// Per analytics, premium features, team
$ cervellaswarm login
Email: user@example.com
Password: ****

✓ Logged in as user@example.com
✓ Syncing projects...

// MA mantenere possibilità standalone!
$ cervellaswarm init --standalone
```

**B. Workspace/Team Support**

```bash
$ cervellaswarm workspace create acme-corp
$ cervellaswarm workspace invite dev@acme.com
```

---

## RACCOMANDAZIONI PRIORITIZZATE

### Priority 1 (questa settimana)

1. [ ] **USARE `conf` package** - già installato, solo da implementare
2. [ ] **Wizard API key in init** - migliorare first-run UX
3. [ ] **Validazione API key** - catch errori PRIMA del primo task

### Priority 2 (prossime 2 settimane)

4. [ ] **Health check command** - `cervellaswarm doctor`
5. [ ] **Tutorial first-run** - opzionale ma utile
6. [ ] **Multi-project management** - switch tra progetti

### Priority 3 (prossimo mese)

7. [ ] **Account CervellaSwarm (opzionale)** - per analytics/premium
8. [ ] **Team/workspace** - collaborazione multi-user

---

## DECISIONE ARCHITETTURALE: STANDALONE vs CLOUD

### Opzione A: Standalone Only (attuale + miglioramenti)

**PRO:**
- Privacy utente massima
- Zero dipendenze server
- Costi zero per noi
- Funziona offline

**CONTRO:**
- NO sync tra macchine
- NO analytics
- NO team collaboration
- NO premium features

### Opzione B: Hybrid (standalone + opzionale cloud)

**PRO:**
- Mantiene privacy per chi vuole
- Abilita features premium
- Analytics opt-in
- Team per chi serve

**CONTRO:**
- Complessità maggiore
- Server da mantenere
- Costi infra

### RACCOMANDAZIONE

**Start Standalone + Hybrid Later**

```
Phase 1 (ora):     Standalone con conf
Phase 2 (Q2 2026): Opzione cloud login (opt-in)
Phase 3 (Q3 2026): Team/workspace features
```

**Principio:** "Funziona SEMPRE standalone. Cloud è BONUS."

---

## NEXT STEP

**Chi:** cervella-backend
**Task:** Implementare config manager con `conf` package
**File da creare:**
- `packages/cli/src/config/manager.js`
- `packages/cli/src/config/validator.js`

**Chi:** cervella-frontend (cli UX)
**Task:** Migliorare wizard init con API key flow
**File da modificare:**
- `packages/cli/src/commands/init.js`
- `packages/cli/src/wizard/questions.js`

**Chi:** cervella-tester
**Task:** Test suite per config management
**File da creare:**
- `packages/cli/test/config/manager.test.js`

---

## METRICHE TREND

**vs Stato Precedente:** N/A (prima analisi)

**Issues Aperti:** 11
- 4 CRITICI
- 4 ALTI
- 3 MEDI

**Effort Stimato:**
- Priority 1: 2-3 giorni
- Priority 2: 5-7 giorni
- Priority 3: 15-20 giorni

---

*Analisi completata. Il codice è pulito e ben strutturato. I gap sono principalmente features mancanti, non technical debt.*

*"Nulla è complesso - solo non ancora studiato!"*

---

**Cervella Ingegnera**
*16 Gennaio 2026*
