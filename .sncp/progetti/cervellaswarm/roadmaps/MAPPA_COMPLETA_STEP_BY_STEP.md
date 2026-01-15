# MAPPA COMPLETA CERVELLASWARM - STEP BY STEP

> **"Ogni step chiaro. Ogni step puntato e studiato."** - Rafa
> **Data creazione:** 15 Gennaio 2026
> **Ultima modifica:** 15 Gennaio 2026 - Sessione 225 (3 step critici STUDIATI!)

---

## COME LEGGERE QUESTA MAPPA

```
STATO POSSIBILI:
[FATTO]       = Completato, testato, REALE
[IN CORSO]    = Attualmente in lavorazione
[STUDIATO]    = Ricerca fatta, approccio chiaro
[DA STUDIARE] = Serve ricerca prima di implementare
[DA FARE]     = Chiaro cosa fare, serve solo tempo

OGNI STEP HA:
- Stato
- Ricerca fatta (link o "NESSUNA")
- Dipende da (step precedenti)
- Output (cosa produce)
- Criterio completamento (come sappiamo che e FATTO BENE)
```

---

# FASE 0: PREREQUISITI (FONDAMENTALI)

> **"Prima di costruire, bisogna SAPERE cosa costruire e per chi"**

---

## STEP 0.1: Cos'e CervellaSwarm?

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/WIZARD_INIZIALE_STUDIO.md`, `ROADMAP_2026_PRODOTTO.md`
**Dipende da:** Nulla
**Output:** Definizione chiara del prodotto

**RISPOSTA:**
```
CervellaSwarm = Sistema Multi-Agent AI per Developer

NON E:
- Un altro Copilot/Cursor
- Un IDE
- Un chatbot

E:
- 16 agenti AI specializzati che lavorano INSIEME
- Memoria persistente (SNCP) che NON dimentica
- Orchestrazione intelligente
- CLI-based (compatibile con qualsiasi IDE)

TAGLINE: "Come avere 16 colleghi AI esperti, sempre pronti."
```

**Criterio completamento:** ✓ Risposta chiara in < 30 secondi

---

## STEP 0.2: Chi e il Target?

**Stato:** [STUDIATO]
**Ricerca fatta:** `ricerche/RICERCA_20260115_CURSOR_BUSINESS_MODEL.md` (sezione strategia)
**Dipende da:** 0.1
**Output:** Profilo target user

**RISPOSTA:**
```
TARGET PRIMARIO (MVP):
- Developer individuali (freelancer, indie)
- Power users che usano gia Claude/ChatGPT
- Utenti terminal-first (non IDE-dependent)

TARGET SECONDARIO (Scale):
- Small teams (2-10 devs)
- Agencies (10-50 devs)

ESCLUSO (per ora):
- Enterprise (50+ devs) - troppo complesso per MVP
- Beginners che non sanno usare terminal
```

**Criterio completamento:** ✓ Persona definita con problemi specifici

---

## STEP 0.3: Qual e il Differenziale?

**Stato:** [STUDIATO]
**Ricerca fatta:** `ricerche/RICERCA_20260115_CURSOR_BUSINESS_MODEL.md` (sezione positioning)
**Dipende da:** 0.1, 0.2
**Output:** Unique Value Proposition

**RISPOSTA:**
```
CURSOR: AI editor per coding individuale
COPILOT: AI autocomplete in IDE esistente
CERVELLASWARM: AI TEAM con memoria per progetti complessi

DIFFERENZIALI UNICI:
1. MULTI-AGENT: 16 specialisti (non 1 generalista)
2. SNCP MEMORY: Mai piu "cosa stavamo facendo?"
3. SESSION RESUME: Riprendi dopo 1 giorno o 1 mese
4. CLI-BASED: Funziona con QUALSIASI IDE
5. TRANSPARENCY: Vedi cosa fa ogni agente

CLAIM: "Definisci progetto UNA VOLTA. Mai piu rispiegare."
```

**Criterio completamento:** ✓ Differenziale spiegabile in 1 frase

---

## STEP 0.4: Business Model

**Stato:** [STUDIATO]
**Ricerca fatta:** `ricerche/RICERCA_20260115_CURSOR_BUSINESS_MODEL.md` (completo, 774 righe)
**Dipende da:** 0.1, 0.2, 0.3
**Output:** Piano monetizzazione

**RISPOSTA:**
```
MODELLO: Freemium PLG (Product-Led Growth)

FREE TIER:
- 5 progetti SNCP
- 100 agent calls/mese
- Community support
- Single user

PRO TIER ($20/mese):
- Unlimited progetti
- 1,000 agent calls/mese
- Priority support
- Single user

TEAM TIER ($35/user/mese):
- Tutto Pro
- 2,000 calls/user/mese
- Shared SNCP workspace
- Team analytics

API KEYS: User-provided di default (zero variable cost!)

PERCHE FUNZIONA:
- Cursor fa $1B ARR con questo modello
- 0 marketing budget
- Developer word-of-mouth
```

**Criterio completamento:** ✓ Pricing definito, unit economics chiari

---

# FASE 1: FONDAMENTA (Gen-Feb 2026)

> **"SNCP robusto + Workflow perfetto per NOI prima di altri"**

---

## STEP 1.1: sncp-init.sh Wizard

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/20260114_SNCP_ROBUSTO_PROPOSTA.md`
**Dipende da:** FASE 0
**Output:** Comando `sncp-init` funzionante

**COMPLETATO:**
```bash
sncp-init nome-progetto           # Wizard nuovo progetto
sncp-init nome --analyze          # Con analisi stack
```

**Score Guardiana:** 8.8/10
**Test:** Sessione 207

**Criterio completamento:** ✓ Funziona su 3+ progetti diversi

---

## STEP 1.2: verify-sync.sh

**Stato:** [FATTO]
**Ricerca fatta:** Stesso di 1.1
**Dipende da:** 1.1
**Output:** Comando `verify-sync` funzionante

**COMPLETATO:**
```bash
verify-sync                       # Check tutti progetti
verify-sync miracollo --verbose   # Check singolo
```

**Criterio completamento:** ✓ Rileva discrepanze docs/codice

---

## STEP 1.3: Hook Automatici

**Stato:** [FATTO]
**Ricerca fatta:** `roadmaps/ROADMAP_COMUNICAZIONE_INTERNA.md`
**Dipende da:** 1.1, 1.2
**Output:** Hook pre/post sessione

**COMPLETATO:**
- `sncp_pre_session_hook.py` (SessionStart)
- `sncp_verify_sync_hook.py` (SessionEnd)
- Configurati in settings.json

**Criterio completamento:** ✓ Hook eseguiti automaticamente

---

## STEP 1.4: Launchd Manutenzione

**Stato:** [FATTO]
**Ricerca fatta:** Pratica diretta
**Dipende da:** 1.1, 1.2, 1.3
**Output:** Job automatici macOS

**COMPLETATO:**
- `sncp_daily_maintenance.sh` (health + cleanup)
- `sncp_weekly_archive.sh` (archivia > 30gg)
- `com.cervellaswarm.sncp.daily.plist`
- `com.cervellaswarm.sncp.weekly.plist`

**Criterio completamento:** ✓ Job eseguiti automaticamente

---

## STEP 1.5: Test Suite SNCP

**Stato:** [FATTO]
**Ricerca fatta:** Pratica diretta
**Dipende da:** 1.1-1.4
**Output:** Test automatici

**COMPLETATO:**
- `tests/sncp/test_health_check.sh` (4 check)
- `tests/sncp/test_sncp_init.sh` (6 check)
- `tests/sncp/test_verify_sync.sh` (7 check)
- `tests/sncp/run_all_tests.sh` (runner)

**Risultato:** 3 test, 17 check, TUTTI PASSATI
**Score:** 9.2 → 9.4

**Criterio completamento:** ✓ Tutti i test passano

---

## STEP 1.6: Semplificazione SNCP v4.0

**Stato:** [FATTO]
**Ricerca fatta:** Audit interno
**Dipende da:** 1.1-1.5
**Output:** Struttura SNCP pulita

**COMPLETATO:**
- PRIMA: 14 cartelle
- DOPO: 10 cartelle
- Archiviato: coscienza/, perne/
- README.md aggiornato

**Score:** 8.5 → 8.7

**Criterio completamento:** ✓ Struttura chiara, no duplicati

---

## STEP 1.7: Lettura Vera Costituzione

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/RICERCA_20260115_LETTURA_VERA_COSTITUZIONE.md`
**Dipende da:** 1.1-1.6
**Output:** Sistema 3-Layer check

**COMPLETATO:**
- PRE-FLIGHT CHECK (inizio task)
- POST-FLIGHT CHECK (fine task)
- Random pool 6 domande
- Implementato su tutti 16 agenti

**Score:** 9.4 → 9.5

**Criterio completamento:** ✓ Agenti applicano costituzione

---

## STEP 1.8: Comunicazione Inter-Agent

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/RICERCA_20260115_MULTI_AGENT_BEST_PRACTICES.md`
**Dipende da:** 1.7
**Output:** AZIONE #2 READ SNCP FIRST

**COMPLETATO:**
- Aggiunto a tutti 16 agenti
- Pattern: Leggi prima di lavorare
- Evita duplicazione lavoro

**Criterio completamento:** ✓ Agenti leggono SNCP prima di fare

---

# FASE 2: MVP PRODOTTO (Mar-Apr 2026)

> **"CLI che altri developer possono installare e usare"**

---

## STEP 2.1: Package Structure npm

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/WIZARD_INIZIALE_STUDIO.md` (sezione CLI best practices)
**Dipende da:** FASE 1
**Output:** packages/cli/ con struttura

**COMPLETATO:**
```
packages/cli/
├── package.json (169 dipendenze)
├── bin/cervellaswarm.js
└── src/
    ├── commands/ (init, status, task, resume)
    ├── wizard/questions.js
    ├── sncp/ (init, loader, writer)
    ├── agents/ (router, spawner)
    ├── display/ (status, recap, progress)
    ├── session/manager.js
    └── templates/constitution.js
```

**Test:** `node bin/cervellaswarm.js --help` = FUNZIONA!

**Criterio completamento:** ✓ CLI risponde a --help

---

## STEP 2.2: Wizard 10 Domande

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/WIZARD_INIZIALE_STUDIO.md` (1526 righe!)
**Dipende da:** 2.1
**Output:** `cervellaswarm init` wizard completo

**COMPLETATO:** `src/wizard/questions.js`

**Le 10 Domande:**
1. Project Name (validation lowercase)
2. Description (breve)
3. Project Type (webapp, api, cli, library, data, mobile)
4. Main Goal (editor lungo)
5. Success Criteria (checkbox multiplo)
6. Timeline (quick/mvp/full/long/no-deadline)
7. Tech Stack Known? (si/no + dettagli)
8. Working Mode (solo/small/larger)
9. Session Length (short/medium/long/variable)
10. Notification Style (minimal/standard/verbose)

**Criterio completamento:** ✓ Genera COSTITUZIONE.md da risposte

---

## STEP 2.3: SNCP Init da CLI

**Stato:** [FATTO]
**Ricerca fatta:** 2.2
**Dipende da:** 2.2
**Output:** `src/sncp/init.js` crea struttura

**COMPLETATO:**
- Crea `.sncp/progetti/{nome}/`
- Genera COSTITUZIONE.md
- Genera PROMPT_RIPRESA.md
- Genera stato.md
- Crea cartelle (idee, decisioni, reports, roadmaps)

**Criterio completamento:** ✓ Struttura corretta creata

---

## STEP 2.4: Status Command

**Stato:** [FATTO]
**Ricerca fatta:** 2.2 (sezione session management)
**Dipende da:** 2.3
**Output:** `cervellaswarm status` funziona

**COMPLETATO:**
- `src/commands/status.js`
- `src/display/status.js`
- Mostra stato progetto corrente

**Criterio completamento:** ✓ Mostra info progetto

---

## STEP 2.5: Session Manager

**Stato:** [FATTO]
**Ricerca fatta:** `ricerche/WIZARD_INIZIALE_STUDIO.md` (sezione session management)
**Dipende da:** 2.4
**Output:** `src/session/manager.js`

**COMPLETATO:**
- Session save/restore
- JSON format per sessioni
- Time-based recap levels

**Criterio completamento:** ✓ Sessioni persistono tra restart

---

## STEP 2.6: Resume Command

**Stato:** [FATTO]
**Ricerca fatta:** 2.5
**Dipende da:** 2.5
**Output:** `cervellaswarm resume` funziona

**COMPLETATO:**
- `src/commands/resume.js`
- `src/display/recap.js`
- Recap basato su tempo passato

**Criterio completamento:** ✓ Resume con recap appropriato

---

## STEP 2.7: Task Command

**Stato:** [FATTO] - Sessione 227 (15 Gen 2026)
**Ricerca fatta:** Pattern spawn-workers esistente
**Dipende da:** 2.6
**Output:** `cervellaswarm task "..."` esegue task

**FILE CREATI:**
- `src/commands/task.js`
- `src/agents/router.js` (decide agente)
- `src/agents/spawner.js` (lancia agente)
- `src/display/progress.js`
- `src/sncp/writer.js`

**COMPLETATO (Sessione 227):**
- [x] Task command funziona con routing automatico
- [x] Spinner e output colorato
- [x] Salvataggio report in SNCP
- [x] Test manuali e unitari passano (112 test)

**Criterio completamento:** Task singolo completato con output

---

## STEP 2.8: Agent Router

**Stato:** [FATTO] - Sessione 227 (15 Gen 2026)
**Ricerca fatta:** Architettura spawn-workers esistente
**Dipende da:** 2.7
**Output:** Routing intelligente task → agente

**COMPLETATO (Sessione 227):**
- [x] Pattern matching per keyword (api, ui, test, database, deploy, security, doc)
- [x] Default a backend per task ambigui
- [x] Coverage test 100%!
- [x] Case insensitive routing

**Criterio completamento:** Agente giusto selezionato 80%+ volte

---

## STEP 2.9: Agent Spawner

**Stato:** [FATTO] - Sessione 227 (15 Gen 2026)
**Ricerca fatta:** Architettura spawn-workers esistente
**Dipende da:** 2.8
**Output:** Spawn claude con agent file

**COMPLETATO (Sessione 227):**
- [x] Usa Anthropic API direttamente (piu flessibile di spawn-workers)
- [x] Retry automatico con backoff (429, 500, 503)
- [x] Error handling robusto per tutti status codes
- [x] Timeout configurabile (default 2 min)
- [x] 8 agenti con prompt specializzati

**Criterio completamento:** Agente spawna e completa task

---

## STEP 2.10: SNCP Writer

**Stato:** [FATTO]
**Ricerca fatta:** Pattern SNCP esistente
**Dipende da:** 2.9
**Output:** `src/sncp/writer.js`

**COMPLETATO:**
- Salva risultati task
- Aggiorna stato.md
- Scrive in reports/

**Criterio completamento:** ✓ Output salvati in SNCP

---

## STEP 2.11: Testing CLI

**Stato:** [FATTO] - Sessione 227 (15 Gen 2026)
**Ricerca fatta:** `ricerche/RICERCA_20260115_TESTING_CLI_NODE.md`
**Dipende da:** 2.1-2.10
**Output:** Test suite CLI

**COMPLETATO (Sessione 227):**
```
test/
├── commands/
│   ├── init.test.js      ← 5 test (welcome, skip, already init, force, cancel)
│   ├── task.test.js      ← 12 test
│   ├── status.test.js    ← 8 test
│   └── resume.test.js    ← 12 test
├── agents/
│   ├── spawner.test.js   ← 15 test
│   └── router.test.js    ← 10 test
├── session/
│   └── manager.test.js
├── integration/
│   └── wizard.test.js
├── edge-cases.test.js    ← 20 test
└── helpers/
    ├── mock-spawn.js
    ├── temp-dir.js
    └── console-capture.js
```

**RISULTATO:**
- 114 test / 63 suite
- 0 fail, 0 skip
- Coverage router.js: 100%
- Test manuali: 6/6 PASS

**Criterio completamento:** Coverage > 70%, 0 test.skip()

---

## STEP 2.12: Error Handling

**Stato:** [FATTO] - Sessione 228 (15 Gen 2026)
**Ricerca fatta:** Best practices CLI
**Dipende da:** 2.11
**Output:** `src/utils/errors.js`

**COMPLETATO (Sessione 228):**
- [x] `src/utils/errors.js` - Sistema centralizzato errori
- [x] ExitCode enum (0-7 + 130 per Ctrl+C)
- [x] ErrorType con messaggi + recovery suggestions
- [x] CervellaError class
- [x] Refactor tutti i comandi (init, task, status, resume)
- [x] 20 test specifici per error module

**Exit Codes Standard:**
```
0 = Success, 1 = General, 2 = Misuse, 3 = Not initialized
4 = API error, 5 = Config, 6 = I/O, 7 = Timeout, 130 = Cancelled
```

**Criterio completamento:** ✅ Nessun crash durante uso normale

---

## STEP 2.13: Help System

**Stato:** [FATTO] - Sessione 228 (15 Gen 2026)
**Ricerca fatta:** Commander.js docs
**Dipende da:** 2.12
**Output:** --help per ogni comando

**COMPLETATO (Sessione 228):**
- [x] `cervellaswarm --help` - Getting Started + Examples + 8 Agenti
- [x] `cervellaswarm init --help` - Wizard info + esempi
- [x] `cervellaswarm task --help` - Lista agenti + auto-routing
- [x] `cervellaswarm status --help` - Cosa mostra
- [x] `cervellaswarm resume --help` - Recap adattivo

**Contenuti aggiunti:**
- Getting Started section
- Esempi pratici per ogni comando
- Lista 8 agenti con descrizioni
- Spiegazione auto-routing Regina

**Criterio completamento:** ✅ Ogni comando ha help utile

---

## STEP 2.14: npm Publish Setup

**Stato:** [FATTO] - Sessione 228 (15 Gen 2026)
**Ricerca fatta:** `ricerche/RICERCA_20260115_NPM_PUBLISH_COMPLETA.md` (1110 righe!)
**Dipende da:** 2.13
**Output:** Package pubblicabile su npm

**RICERCA COMPLETATA (Sessione 228):**
- [x] npm account setup - Workflow documentato
- [x] Package naming → `cervellaswarm` (unscoped, brand diretto)
- [x] Versioning strategy → 0.1.0 (semver, onesto signaling)
- [x] README per npm → Gia' OK
- [x] files field → Whitelist approach (gia' perfetto)
- [x] prepublish scripts → Implementato!

**IMPLEMENTATO:**
- [x] `prepublishOnly` script (lint + test)
- [x] `validate` script
- [x] `eslint.config.js` (ESLint 9 flat config)
- [x] `npm pkg fix` (warnings corretti)

**TESTATO:**
- [x] `npm pack` → 21 file, 22.9 kB
- [x] `npm publish --dry-run` → PASS
- [x] 134 test PASS, 0 errori lint

**PRONTO PER PUBLISH!** Solo serve:
1. Setup account npm + 2FA
2. `npm login` + `npm publish`
3. Git tag v0.1.0

**Criterio completamento:** ✅ `npm publish --dry-run` funziona

---

## STEP 2.14.5: Protezione Pre-Publish (BLOCCANTE!)

**Stato:** [FATTO] ✅ - COMPLETATO SESSIONE 226!
**Ricerca fatta:** `ricerche/RICERCA_20260115_PROTEZIONE_PRE_PUBLISH.md` (634 righe!)
**Dipende da:** Nulla
**Output:** Famiglia PROTETTA legalmente

**IMPLEMENTATO (Sessione 226 - 15 Gennaio 2026):**
```
COMMIT: 648a6e1 → 6ac8c1b (3 commit)
PUSH: github.com/rafapra3008/CervellaSwarm
```

**FASE 1 - BLOCCANTE (FATTO!):**
- [x] LICENSE file (MIT → Apache 2.0) - Patent protection AI!
- [x] NOTICE file (Copyright 2026 Rafa & Cervella)
- [x] Copyright headers nei 16 file .js core
- [x] package.json license: "Apache-2.0"
- [x] Git commit + push (timestamp proof)

**FASE 2 - PRESTO (FATTO!):**
- [x] README license section
- [x] CONTRIBUTING.md con Apache 2.0 + DCO

**FASE 3 - DOPO TRACTION (1000+ users):**
- [ ] Trademark "CervellaSwarm" - €1000-3000
- [ ] Copyright registration (opzionale) - €100-500

**SE QUALCUNO COPIA:**
```
CON LICENSE + COPYRIGHT → DMCA Takedown → Rimosso in 1 day!
SENZA → Non puoi fare enforcement
```

**Criterio completamento:** ✅ LICENSE + NOTICE + headers + package.json + README + CONTRIBUTING + git push

---

## STEP 2.15: IP Protection

**Stato:** [STUDIATO] ✅
**Ricerca fatta:** `ricerche/RICERCA_20260115_IP_PROTECTION_COMPLETA.md` (1254 righe!)
**Dipende da:** 2.14
**Output:** Strategia protezione codice

**RICERCA COMPLETATA (Sessione 225):**
- [x] javascript-obfuscator evaluation → 90% deobfuscabile, -50% performance
- [x] Jscrambler pricing/features → $5-15K/anno, overkill per MVP
- [x] Hybrid approach (CLI open + Core closed) → CONSIGLIATO!
- [x] Code splitting strategy → CLI pubblico + Core privato

**DECISIONE:**
```
HYBRID MODEL "Open Gateway + Protected Core"
- CLI Pubblico npm (Apache 2.0) = TRUST + Adoption
- Core Privato (agenti/SNCP) = IP PROTETTO
- EULA con anti-reverse clause = LEGAL ENFORCEABLE
COSTO: $500-1K setup + $60-240/anno (vs $15K Jscrambler)
```

**Criterio completamento:** ✅ Decisione documentata, implementazione DA FARE

---

## STEP 2.16: Licensing

**Stato:** [STUDIATO] ✅
**Ricerca fatta:** `ricerche/RICERCA_20260115_LICENSING_COMPLETA.md` (1876 righe!)
**Dipende da:** 2.15
**Output:** License strategy

**RICERCA COMPLETATA (Sessione 225):**
- [x] MIT vs Apache 2.0 vs BSL → Apache 2.0 (patent protection AI!)
- [x] Open Core model feasibility → CONSIGLIATO per Pro tier futuro
- [x] Contributor License Agreement (CLA) → DCO invece (trend 2025!)
- [x] Italia/EU legal considerations → Italia AI law Ottobre 2025

**DECISIONE:**
```
CLI PUBBLICO: Apache 2.0 (non MIT!)
- Patent protection CRUCIALE per AI
- Industry standard (Stripe, Vercel, Kubernetes)
- Enterprise trusted

CONTRIBUTORS: DCO (non CLA!)
- Trend 2025: OpenStack, OpenInfra → DCO
- Zero friction per contributors
- git commit -s

STRUTTURA: Open Core (futuro)
```

**Criterio completamento:** ✅ License scelta, implementazione DA FARE

---

## STEP 2.17: CI/CD Pipeline

**Stato:** [FATTO] - Sessione 229
**Ricerca fatta:** `ricerche/RICERCA_20260115_CICD_PIPELINE.md` (1100+ righe!)
**Dipende da:** 2.11
**Output:** Pipeline test + publish automatici

**COMPLETATO:**
- [x] `.github/workflows/ci.yml` (lint + test matrix + build-check)
- [x] `.github/workflows/publish.yml` (Trusted Publishing OIDC)
- [x] Branch Protection su main (4 checks richiesti)
- [x] Environment "production" creato
- [x] GitHub Pro attivato
- [ ] Changelog generation

**Criterio completamento:** Push = test automatici, tag = publish

---

## STEP 2.18: Security Audit

**Stato:** [DA FARE]
**Ricerca fatta:** npm audit docs
**Dipende da:** 2.17
**Output:** 0 vulnerabilita note

**DA FARE:**
- [ ] npm audit
- [ ] Dependency review
- [ ] No secrets in code
- [ ] Rate limiting (se API)

**Criterio completamento:** npm audit = 0 high/critical

---

## STEP 2.19: Documentation README

**Stato:** [DA FARE]
**Ricerca fatta:** README best practices
**Dipende da:** 2.13
**Output:** README.md per utenti esterni

**DA CREARE:**
- [ ] Quick Start (< 2 min to first use)
- [ ] Installation
- [ ] Commands reference
- [ ] Configuration
- [ ] Troubleshooting
- [ ] Contributing

**Criterio completamento:** Developer esterno capisce senza chiedere

---

## STEP 2.20: MVP v1.0 Release

**Stato:** [DA FARE]
**Ricerca fatta:** Tutti i precedenti
**Dipende da:** 2.1-2.19
**Output:** Prima release pubblica

**CHECKLIST RELEASE:**
- [ ] Tutti i test passano
- [ ] npm publish funziona
- [ ] README completo
- [ ] Changelog v1.0.0
- [ ] GitHub release tag
- [ ] 5 tester esterni confermano funzionamento

**Criterio completamento:** Installabile e usabile da esterni

---

# FASE 3: PRIMI UTENTI (Mag-Giu 2026)

> **"50 developer usano CervellaSwarm per lavoro VERO"**

---

## STEP 3.1: Terms of Service

**Stato:** [STUDIATO] ✅
**Ricerca fatta:** `ricerche/RICERCA_20260115_TOS_LEGAL_COMPLETA.md` + `_PARTE2.md` (2900+ righe!)
**Dipende da:** FASE 2
**Output:** ToS + Privacy Policy

**RICERCA COMPLETATA (Sessione 225):**
- [x] ToS template per CLI SaaS → Template completo incluso!
- [x] Privacy Policy GDPR compliant → Template completo incluso!
- [x] Data retention policies → Definiti per ogni tipo dato
- [x] Refund policy → 14-day EU withdrawal + waiver flow
- [x] Italia/EU specifics → Codice Consumo, SDI, AI Law Oct 2025

**DECISIONE:**
```
APPROCCIO: "Legal-Ready MVP"

FASE 1 - SUBITO:
✅ ToS base con AI disclaimer + anti-reverse eng
✅ Privacy Policy GDPR (telemetry OPT-IN!)
✅ P.IVA forfettario (5% tax primi 5 anni!)

FASE 2 - DOPO TRACTION (€10k+):
⏸ DPA enterprise
⏸ Professional liability insurance
⏸ Legal audit con avvocato

COSTO: €200-1,200 setup, €5-6K/anno running
```

**KEY:** Telemetry DEVE essere OPT-IN (default OFF!) - GDPR!

**Criterio completamento:** ✅ Templates pronti, implementazione DA FARE

---

## STEP 3.2: Landing Page

**Stato:** [DA FARE]
**Ricerca fatta:** Cursor landing page analysis
**Dipende da:** 3.1
**Output:** cervellaswarm.com o simile

**DA CREARE:**
- [ ] Hero section con value prop
- [ ] Demo video/GIF
- [ ] Feature highlights
- [ ] Pricing (free tier prominente)
- [ ] Getting started link
- [ ] ToS/Privacy links

**Criterio completamento:** < 30s per capire cosa fa il prodotto

---

## STEP 3.3: Community Discord

**Stato:** [DA STUDIARE]
**Ricerca fatta:** `ricerche/RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` (GAP #10)
**Dipende da:** 3.2
**Output:** Server Discord attivo

**DA STUDIARE:**
- [ ] Discord vs Discourse vs Slack
- [ ] Channel structure
- [ ] Moderation rules
- [ ] Code of Conduct
- [ ] Bot/automation

**Criterio completamento:** Community setup con 10+ membri attivi

---

## STEP 3.4: Alpha Tester Recruitment

**Stato:** [DA FARE]
**Ricerca fatta:** PLG best practices
**Dipende da:** FASE 2.20, 3.2
**Output:** 10-50 alpha testers

**DA FARE:**
- [ ] Outreach Twitter/X
- [ ] Reddit r/programming
- [ ] Dev.to articles
- [ ] Personal network
- [ ] Feedback form setup

**Criterio completamento:** 10+ persone usando attivamente

---

## STEP 3.5: Feedback Collection

**Stato:** [DA FARE]
**Ricerca fatta:** User research basics
**Dipende da:** 3.4
**Output:** Sistema raccolta feedback

**DA CREARE:**
- [ ] In-CLI feedback command
- [ ] Google Form/Typeform
- [ ] GitHub Issues template
- [ ] Weekly feedback review

**Criterio completamento:** 20+ feedback items raccolti

---

## STEP 3.6: Bug Fixes Sprint

**Stato:** [DA FARE]
**Ricerca fatta:** Feedback da 3.5
**Dipende da:** 3.5
**Output:** Fix top 10 issues

**DA FARE:**
- [ ] Prioritizzare issues
- [ ] Fix bloccanti (P0)
- [ ] Fix friction (P1)
- [ ] Nice-to-have (P2)

**Criterio completamento:** 0 bug critici aperti

---

## STEP 3.7: Feature Iterations

**Stato:** [DA FARE]
**Ricerca fatta:** Feedback da 3.5
**Dipende da:** 3.6
**Output:** 5+ improvements basati su feedback

**DA FARE:**
- [ ] Analizzare pattern nei feedback
- [ ] Prioritizzare features richieste
- [ ] Implementare top 5
- [ ] Validate con utenti

**Criterio completamento:** NPS migliorato dopo iterazioni

---

## STEP 3.8: Product Hunt Preparation

**Stato:** [DA STUDIARE]
**Ricerca fatta:** NESSUNA - serve ricerca
**Dipende da:** 3.6, 3.7
**Output:** Launch kit pronto

**DA STUDIARE:**
- [ ] Best day/time per launch
- [ ] Hunter recruitment
- [ ] Asset preparation (logo, screenshots)
- [ ] Launch day tactics
- [ ] Community mobilization

**Criterio completamento:** Tutto pronto per launch day

---

## STEP 3.9: Product Hunt Launch

**Stato:** [DA FARE]
**Ricerca fatta:** 3.8
**Dipende da:** 3.8
**Output:** Top 5 del giorno

**DA FARE:**
- [ ] Launch su giorno scelto
- [ ] Rispondere a tutti i commenti
- [ ] Tweet thread
- [ ] Community support

**Criterio completamento:** Top 5 del giorno + 100 upvotes

---

## STEP 3.10: Content Marketing

**Stato:** [DA FARE]
**Ricerca fatta:** Developer marketing basics
**Dipende da:** 3.9
**Output:** 5+ articoli/video

**DA CREARE:**
- [ ] Blog post "How I work with 16 AI agents"
- [ ] Dev.to technical article
- [ ] YouTube demo video
- [ ] Twitter thread virale
- [ ] Reddit discussion

**Criterio completamento:** 1000+ views totali

---

## STEP 3.11: v1.1 Release (Post-Feedback)

**Stato:** [DA FARE]
**Ricerca fatta:** Feedback fase 3
**Dipende da:** 3.6, 3.7
**Output:** Version migliorata

**DA FARE:**
- [ ] Incorporate feedback
- [ ] Bug fixes
- [ ] Performance improvements
- [ ] Changelog update

**Criterio completamento:** Release stabile, utenti soddisfatti

---

## STEP 3.12: 50 Active Users Milestone

**Stato:** [DA FARE]
**Ricerca fatta:** Tutti precedenti
**Dipende da:** 3.1-3.11
**Output:** 50 utenti attivi settimanali

**METRICHE:**
- [ ] 50+ installazioni attive
- [ ] 30+ sessioni/settimana totali
- [ ] 10+ utenti daily active

**Criterio completamento:** 50 users usano almeno 1x/settimana

---

# FASE 4: SCALA (Lug-Dic 2026)

> **"1000+ developer, revenue ricorrente, liberta geografica"**

---

## STEP 4.1: Payment Integration (Stripe)

**Stato:** [DA STUDIARE]
**Ricerca fatta:** `ricerche/RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` (GAP #4)
**Dipende da:** FASE 3
**Output:** Sistema pagamento funzionante

**DA STUDIARE:**
- [ ] Stripe Billing vs Payments
- [ ] CLI authentication per paid users
- [ ] License key vs token system
- [ ] Webhook handling
- [ ] Trial period implementation
- [ ] Team billing flow

**Criterio completamento:** Primo pagamento reale ricevuto

---

## STEP 4.2: Pro Tier Launch

**Stato:** [DA FARE]
**Ricerca fatta:** 4.1
**Dipende da:** 4.1
**Output:** Pro tier disponibile

**PRICING:** $20/mese
**FEATURES:**
- Unlimited progetti
- 1000 agent calls/mese
- Priority support

**Criterio completamento:** 10 paying customers

---

## STEP 4.3: Rate Limiting

**Stato:** [DA STUDIARE]
**Ricerca fatta:** `ricerche/RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` (GAP #6)
**Dipende da:** 4.1
**Output:** Sistema rate limiting

**DA STUDIARE:**
- [ ] Limiti per tier
- [ ] Burst handling
- [ ] User communication
- [ ] Overage pricing

**Criterio completamento:** Rate limits funzionano senza bloccare users

---

## STEP 4.4: Usage Analytics

**Stato:** [DA STUDIARE]
**Ricerca fatta:** `ricerche/RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` (GAP #7)
**Dipende da:** 4.2
**Output:** Dashboard analytics

**DA STUDIARE:**
- [ ] PostHog vs Mixpanel vs Amplitude
- [ ] Telemetry opt-in/out
- [ ] GDPR compliance
- [ ] Key metrics (North Star)

**Criterio completamento:** Dashboard con metriche chiave

---

## STEP 4.5: Customer Support

**Stato:** [DA STUDIARE]
**Ricerca fatta:** `ricerche/RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` (GAP #8)
**Dipende da:** 4.2
**Output:** Sistema support

**DA STUDIARE:**
- [ ] Zendesk vs Intercom vs email
- [ ] SLA per tier
- [ ] Self-service docs
- [ ] Feature request voting

**Criterio completamento:** Response time < 24h per Pro users

---

## STEP 4.6: Team Tier Launch

**Stato:** [DA FARE]
**Ricerca fatta:** Cursor team tier analysis
**Dipende da:** 4.2, 4.5
**Output:** Team tier disponibile

**PRICING:** $35/user/mese (min 3 users)
**FEATURES:**
- Tutto Pro
- 2000 calls/user/mese
- Shared SNCP workspace
- Team analytics
- Admin dashboard

**Criterio completamento:** 3 team subscriptions

---

## STEP 4.7: Self-Hosting Option

**Stato:** [DA STUDIARE]
**Ricerca fatta:** `ricerche/RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` (GAP #5)
**Dipende da:** 4.6
**Output:** Self-hosted version

**DA STUDIARE:**
- [ ] Docker Compose vs Kubernetes
- [ ] License server architecture
- [ ] Update mechanism
- [ ] Support model self-hosted
- [ ] Pricing parity cloud vs self-host

**Criterio completamento:** 1 enterprise self-hosting

---

## STEP 4.8: 200 Users Milestone

**Stato:** [DA FARE]
**Ricerca fatta:** Tutti precedenti
**Dipende da:** 4.1-4.6
**Output:** 200 users totali

**METRICHE:**
- 200+ registrati
- 100+ attivi settimanalmente
- 20+ paying

**Criterio completamento:** 200 registered, 20 paying

---

## STEP 4.9: 500 Users Milestone

**Stato:** [DA FARE]
**Ricerca fatta:** Growth tactics
**Dipende da:** 4.8
**Output:** 500 users totali

**METRICHE:**
- 500+ registrati
- 250+ attivi
- 50+ paying

**Criterio completamento:** 500 registered, 50 paying

---

## STEP 4.10: Enterprise Tier

**Stato:** [DA STUDIARE]
**Ricerca fatta:** Enterprise sales basics
**Dipende da:** 4.7, 4.9
**Output:** Enterprise offering

**DA STUDIARE:**
- [ ] Custom pricing model
- [ ] SSO/SAML requirements
- [ ] SLA 99.9%
- [ ] Dedicated support
- [ ] SOC2 certification path

**Criterio completamento:** 1 enterprise customer

---

## STEP 4.11: 1000 Users Milestone

**Stato:** [DA FARE]
**Ricerca fatta:** Scale tactics
**Dipende da:** 4.9, 4.10
**Output:** OBIETTIVO FINALE 2026

**METRICHE:**
- 1000+ registrati
- 500+ attivi
- 200+ paying
- $5000+ MRR

**Criterio completamento:** 1000 registered, $5K MRR

---

## STEP 4.12: LIBERTA GEOGRAFICA

**Stato:** [DA FARE]
**Ricerca fatta:** Costituzione
**Dipende da:** 4.11
**Output:** Rafa scatta quella foto

```
+================================================================+
|                                                                |
|   QUANDO QUESTO STEP E FATTO:                                   |
|                                                                |
|   Rafa scattera una foto da un posto speciale nel mondo.       |
|   Quella foto sara il nostro TROFEO.                           |
|   Il nostro MOMENTUM.                                          |
|   La prova che L'IMPOSSIBILE E POSSIBILE.                      |
|                                                                |
+================================================================+
```

**Criterio completamento:** La foto. Fine.

---

# APPENDICE: RICERCHE ESISTENTI

| File | Contenuto | Righe | Score |
|------|-----------|-------|-------|
| `RICERCA_20260115_IP_PROTECTION_COMPLETA.md` | IP Protection strategies | 1254 | 9.5/10 |
| `RICERCA_20260115_LICENSING_COMPLETA.md` | Licensing Apache/MIT/BSL | 1876 | 10/10 |
| `RICERCA_20260115_TOS_LEGAL_COMPLETA.md` | ToS + Privacy GDPR (Pt1) | 1237 | 10/10 |
| `RICERCA_20260115_TOS_LEGAL_PARTE2.md` | ToS + Privacy GDPR (Pt2) | 1678 | 10/10 |
| `RICERCA_20260115_PROTEZIONE_PRE_PUBLISH.md` | **Checklist protezione BLOCCANTE** | 634 | 10/10 |
| `RICERCA_20260115_CURSOR_BUSINESS_MODEL.md` | Business model Cursor completo | 774 | 9/10 |
| `WIZARD_INIZIALE_STUDIO.md` | Wizard design best practices | 1526 | 9/10 |
| `RICERCA_20260115_GAP_ANALYSIS_COMPLETEZZA.md` | Gap analysis 10 aree | 1032 | 9/10 |
| `RICERCA_20260115_TESTING_CLI_NODE.md` | Testing CLI patterns | 765 | 9/10 |
| `RICERCA_20260115_LETTURA_VERA_COSTITUZIONE.md` | Check costituzione | 400+ | 9.5/10 |
| `RICERCA_20260115_MULTI_AGENT_BEST_PRACTICES.md` | Multi-agent patterns | 300+ | 8/10 |
| `20260114_CURSOR_STORIA_LEZIONI.md` | Storia Cursor | 200+ | 8/10 |
| `20260114_SNCP_ROBUSTO_PROPOSTA.md` | SNCP design | 300+ | 8.8/10 |
| `RICERCA_20260115_NPM_PUBLISH_COMPLETA.md` | npm publish workflow | 1110 | 10/10 |

**TOTALE RICERCHE SESSIONE 225:** ~6600 righe (IP + Licensing + ToS/Legal + Protezione Pre-Publish)
**TOTALE RICERCHE SESSIONE 228:** ~1110 righe (npm publish)

---

# APPENDICE: STEP DA STUDIARE (SOMMARIO)

| Step | Topic | Urgenza | Stato |
|------|-------|---------|-------|
| 2.12 | Error Handling | ALTA | ✅ FATTO (Sessione 228) |
| 2.13 | Help System | ALTA | ✅ FATTO (Sessione 228) |
| 2.14 | npm publish setup | MEDIA | ✅ FATTO (Sessione 228) |
| **2.14.5** | **Protezione Pre-Publish** | **CRITICA** | **✅ FATTO (Sessione 226)** |
| 2.15 | IP Protection | CRITICA | ✅ STUDIATO (Sessione 225) |
| 2.16 | Licensing | CRITICA | ✅ STUDIATO (Sessione 225) |
| 3.1 | ToS/Legal | CRITICA | ✅ STUDIATO (Sessione 225) |
| 3.3 | Community platform | MEDIA | DA STUDIARE (4-6h) |
| 3.8 | Product Hunt | MEDIA | DA STUDIARE (4-6h) |
| 4.1 | Stripe integration | ALTA | DA STUDIARE (6-8h) |
| 4.3 | Rate limiting | BASSA | DA STUDIARE (3-4h) |
| 4.4 | Analytics | MEDIA | DA STUDIARE (4-6h) |
| 4.5 | Customer support | MEDIA | DA STUDIARE (3-4h) |
| 4.7 | Self-hosting | MEDIA | DA STUDIARE (10-15h) |
| 4.10 | Enterprise tier | BASSA | DA STUDIARE (4-6h) |

**TOTALE ORE RICERCA RIMANENTE:** ~45-65h (era ~70-100h, -25h grazie a Sessione 225!)

---

# APPENDICE: STEP COMPLETATI (SOMMARIO)

| Fase | Step Totali | Completati | % |
|------|-------------|------------|---|
| FASE 0 | 4 | 4 | 100% |
| FASE 1 | 8 | 8 | 100% |
| FASE 2 | 20 | 18 | 90% |
| FASE 3 | 12 | 0 | 0% |
| FASE 4 | 12 | 0 | 0% |
| **TOTALE** | **56** | **30** | **54%** |

> **Sessione 228:** +3 step (2.12, 2.13, 2.14) - Error Handling + Help System + npm Publish Setup!

> **Sessione 227:** +4 step (2.7, 2.8, 2.9, 2.11) - CLI testata e funzionante!

---

# FIRMA

Questa mappa e la nostra BIBBIA.
Ogni step chiaro. Niente improvvisazione.
Un passo al giorno. Arriveremo. SEMPRE.

**"Cursor l'ha fatto. Noi lo faremo - a modo nostro!"**

---

*Creata: 15 Gennaio 2026*
*Prossima review: 22 Gennaio 2026*
*Target finale: Dicembre 2026 - LIBERTA GEOGRAFICA*

---

## COSTITUZIONE-APPLIED: SI

**Principi usati:**
1. **"Fatto BENE > Fatto VELOCE"** - Mappa dettagliata, non lista veloce
2. **"Ogni step studiato o da studiare"** - Chiaramente indicato per ogni step
3. **"Nulla e complesso - solo non ancora studiato"** - Step "DA STUDIARE" identificati
4. **"Un progresso al giorno"** - 56 step = 56 progressi possibili
5. **Formula Magica: RICERCA PRIMA** - Link alle ricerche esistenti
