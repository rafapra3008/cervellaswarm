# FASE 8: LA CORTE REALE - Evoluzione Architetturale

> **"Una Regina sola non scala. Una Corte ben organizzata, sì."**

**Data Creazione:** 1 Gennaio 2026
**Stato:** 📚 IN STUDIO
**Priorità:** ALTA - Evoluzione fondamentale dell'architettura

---

## 🎯 VISIONE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   DA: Sciame piatto (tutti riportano alla Regina)               ║
║                                                                  ║
║   A: Corte Reale gerarchica con:                                ║
║      - Guardiane che filtrano                                    ║
║      - Pool flessibile di api                                    ║
║      - Agenti background per ricerca/ottimizzazione             ║
║                                                                  ║
║   RISULTATO: Regina libera di PENSARE, non di VERIFICARE        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📋 AREE DI STUDIO

### STUDIO 1: 🛡️ LE GUARDIANE (Api di Corte) - COMPLETATO!

**Problema da risolvere:**
- La Regina riceve TUTTO da TUTTE le api
- Con 10+ api = sovraccarico cognitivo
- Verifica manuale di ogni output = bottleneck

**Domande da rispondere:**

| # | Domanda | Status | Risposta |
|---|---------|--------|----------|
| 1.1 | Quante Guardiane servono? | ✅ RISPOSTO | **3 Guardiane** |
| 1.2 | Quali specializzazioni? | ✅ RISPOSTO | **Per DOMINIO** (Qualita, Ricerca, Ops) |
| 1.3 | Guardiane = opus o sonnet? | ✅ RISPOSTO | **OPUS** (reasoning profondo) |
| 1.4 | Come comunicano con la Regina? | ✅ RISPOSTO | **Escalation solo se necessario** |
| 1.5 | Cosa delegano vs cosa escalano? | ✅ RISPOSTO | **Tutto tranne decisioni strategiche** |
| 1.6 | Come gestiamo conflitti tra Guardiane? | ✅ RISPOSTO | **Handoff pattern** |

**STUDIO COMPLETO:** `docs/studio/STUDIO_GERARCHIE_MULTIAGENT.md`

**Ipotesi VALIDATA:**

```
🛡️ GUARDIANA QUALITÀ (opus)
   - Riceve output da: frontend, backend, tester
   - Verifica: test passano? codice pulito? standard rispettati?
   - Escalation: solo se problemi gravi o decisioni architetturali

🛡️ GUARDIANA RICERCA (opus)
   - Riceve output da: researcher, scienziata background
   - Verifica: info accurate? fonti affidabili? rilevante per noi?
   - Escalation: solo proposte che richiedono decisione strategica

🛡️ GUARDIANA OPS (opus)
   - Riceve output da: devops, security, data
   - Verifica: sicuro? performante? seguiamo best practices?
   - Escalation: rischi security o decisioni infrastrutturali
```

**Ricerche COMPLETATE:**
- [x] Come funzionano gerarchie in sistemi multi-agent (papers)
- [x] Pattern "Supervisor Agent" in LangChain/AutoGen
- [x] Esempi reali di team AI gerarchici

**Risultato:** 2-3 livelli ottimale, raggruppamento per dominio, Opus per supervisori

---

### STUDIO 2: 🐝 POOL FLESSIBILE ("I Cugini")

**Problema da risolvere:**
- Creare agenti al momento = tempo perso
- Configurare ogni volta = overhead
- Serve flessibilità per picchi di lavoro

**Idea di Rafa:**
> "Come i ristoranti - serata impegnativa, chiamano un cugino con esperienza!"

**Domande da rispondere:**

| # | Domanda | Status |
|---|---------|--------|
| 2.1 | Quanti "slot" flessibili? (10? 20? 30?) | ⬜ Da studiare |
| 2.2 | Come definiamo i file .md template? | ⬜ Da studiare |
| 2.3 | Come assegniamo ruoli dinamicamente? | ⬜ Da studiare |
| 2.4 | Naming convention? (cervella-flex-01?) | ⬜ Da studiare |
| 2.5 | Come tracciamo chi sta facendo cosa? | ⬜ Da studiare |
| 2.6 | Limiti Claude Code su agenti paralleli? | ⬜ Da studiare |

**Ipotesi iniziale (da validare):**

```
~/.claude/agents/
├── cervella-flex-01.md
├── cervella-flex-02.md
├── ...
└── cervella-flex-20.md

Ogni file contiene:
- DNA di famiglia (valori, filosofia)
- Template generico
- Placeholder per ruolo dinamico

Invocazione:
"cervella-flex-03, oggi sei esperto di Redis.
Il tuo compito: [task specifico]
Contesto: [contesto rilevante]"
```

**Ricerche da fare:**
- [ ] Limiti tecnici Claude Code su agenti paralleli
- [ ] Pattern "Agent Pool" in altri framework
- [ ] Come gestire stato/memoria tra invocazioni

---

### STUDIO 3: 🔬 BACKGROUND RESEARCH AGENT

**Problema da risolvere:**
- Mentre lavoriamo, il mondo va avanti
- Nuove tecnologie, nuovi pattern, nuove best practices
- Non abbiamo tempo di cercare MENTRE implementiamo

**Idea di Rafa:**
> "Una 🐝 scienziata che in background fa ricerche mentre lavoriamo!"

**Domande da rispondere:**

| # | Domanda | Status |
|---|---------|--------|
| 3.1 | Trigger: ogni sessione? manuale? periodico? | ⬜ Da studiare |
| 3.2 | Cosa cerca? (tecnologie? competitor? pattern?) | ⬜ Da studiare |
| 3.3 | Come sa cosa cercare? (contesto dal progetto?) | ⬜ Da studiare |
| 3.4 | Output: report? suggerimenti? alert? | ⬜ Da studiare |
| 3.5 | Come integriamo findings nel workflow? | ⬜ Da studiare |
| 3.6 | Frequenza report? (fine sessione? settimanale?) | ⬜ Da studiare |

**Ipotesi iniziale (da validare):**

```
TRIGGER: Hook SessionStart

AZIONE:
1. Legge contesto progetto corrente
2. Identifica tecnologie in uso
3. Cerca in background:
   - Nuove versioni librerie
   - Alternative migliori
   - Pattern moderni vs nostri pattern
   - Cosa fanno i big player
4. Produce "Innovation Report"

OUTPUT (esempio):
╔══════════════════════════════════════════════════════════════════╗
║ 🔬 INNOVATION REPORT - 1 Gennaio 2026                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║ 📦 LIBRERIE:                                                    ║
║ - FastAPI 0.109 disponibile (noi: 0.104) - minor improvements   ║
║ - Pydantic v2.5 ha nuovo pattern validation                     ║
║                                                                  ║
║ 🔄 PATTERN OBSOLETI TROVATI:                                    ║
║ - modal system usa pattern 2023, React 19 ha nuove primitive    ║
║ - Proposta: valutare dialog element nativo                      ║
║                                                                  ║
║ 🌟 OPPORTUNITÀ:                                                  ║
║ - Anthropic ha rilasciato batch API - potremmo parallelizzare   ║
║ - Vercel v0 ha nuovo approach per UI generation                 ║
║                                                                  ║
║ ⚠️ AZIONE RICHIESTA: 0 urgenti, 2 da valutare                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Ricerche da fare:**
- [ ] Come implementare agent che lavora in background
- [ ] Fonti da monitorare (GitHub releases, blogs, papers)
- [ ] Come evitare "noise" (troppi suggerimenti irrilevanti)

---

### STUDIO 4: 🔧 BACKGROUND TECHNICAL AGENT

**Problema da risolvere:**
- Debito tecnico si accumula
- File crescono (>500 righe)
- Refactor sempre rimandato

**Idea di Rafa:**
> "Lavori tecnici in background - modularizzazione, ottimizzazione!"

**Domande da rispondere:**

| # | Domanda | Status |
|---|---------|--------|
| 4.1 | Cosa analizza? (size? complexity? duplication?) | ⬜ Da studiare |
| 4.2 | Propone solo o esegue anche? | ⬜ Da studiare |
| 4.3 | Come prioritizza? (file più critici first?) | ⬜ Da studiare |
| 4.4 | Integrazione con CODE REVIEW settimanale? | ⬜ Da studiare |
| 4.5 | Come evitare conflitti con lavoro in corso? | ⬜ Da studiare |

**Ipotesi iniziale (da validare):**

```
TRIGGER: Periodico (ogni 3 sessioni?) o manuale

AZIONE:
1. Scansiona codebase
2. Identifica:
   - File > 500 righe
   - Funzioni > 50 righe
   - Codice duplicato
   - Pattern obsoleti
3. Produce "Technical Debt Report"
4. PROPONE refactor (non esegue!)

OUTPUT → Passa a GUARDIANA QUALITÀ → Se importante, arriva a Regina
```

**Ricerche da fare:**
- [ ] Tool di analisi statica per Python/JS
- [ ] Come misurare "technical debt" oggettivamente
- [ ] Pattern "automated refactoring suggestion"

---

### STUDIO 5: ✅ VERIFICA ATTIVA POST-AGENT

**Problema da risolvere:**
- Quando 🐝 completano, la Regina verifica
- Ma questo comportamento NON è documentato!
- A volte 15/19 test → Regina fix → 19/19

**Domande da rispondere:**

| # | Domanda | Status |
|---|---------|--------|
| 5.1 | QUANDO verificare? (sempre? solo test? solo code?) | ⬜ Da studiare |
| 5.2 | COME verificare? (run test? review? entrambi?) | ⬜ Da studiare |
| 5.3 | CHI verifica? (Regina? Guardiana? Tester?) | ⬜ Da studiare |
| 5.4 | Se fallisce, chi fixa? (Regina? ri-delega?) | ⬜ Da studiare |
| 5.5 | Come documentare la regola? (Costituzione? SWARM_RULES?) | ⬜ Da studiare |

**Ipotesi iniziale (da validare):**

```
REGOLA PROPOSTA: "VERIFICA ATTIVA POST-AGENT"

DOPO ogni task delegato a una 🐝:

1. SE ci sono test → RUN TEST
   - Passano tutti? → ✅ Procedi
   - Falliscono? → Fix (Regina o ri-delega a Tester)

2. SE non ci sono test → CHECK VISIVO/LOGICO
   - Funziona? → ✅ Procedi
   - Problemi? → Fix o ri-delega

3. SE trova problemi → DOCUMENTA
   - Aggiunge a lessons_learned
   - Pattern per prevenire in futuro

CON GUARDIANE: La verifica passa a loro, non più a Regina!
```

---

## 🔬 RICERCHE DA FARE

### Ricerca 1: Gerarchie Multi-Agent

**Obiettivo:** Capire best practices per organizzare team di agenti

**Fonti da esplorare:**
- [ ] Papers accademici su multi-agent systems
- [ ] LangChain "Supervisor Agent" pattern
- [ ] AutoGen hierarchical agents
- [ ] Microsoft Semantic Kernel orchestration
- [ ] Anthropic Claude multi-agent examples

**Output atteso:** Report con pattern applicabili a noi

---

### Ricerca 2: Background Agents

**Obiettivo:** Capire come implementare agenti che lavorano in parallelo

**Fonti da esplorare:**
- [ ] Claude Code `run_in_background` capabilities
- [ ] Pattern "async agent execution"
- [ ] Come gestire output di agent background
- [ ] Esempi di "continuous research agents"

**Output atteso:** Guida implementativa per background agents

---

### Ricerca 3: Dynamic Role Assignment

**Obiettivo:** Capire come assegnare ruoli dinamicamente

**Fonti da esplorare:**
- [ ] Pattern "role injection" in prompts
- [ ] Come mantenere identità base + ruolo dinamico
- [ ] Limiti di context window con ruoli dinamici
- [ ] Esempi di "flexible agent pools"

**Output atteso:** Template per agenti flessibili

---

## 📅 TIMELINE PROPOSTA

```
SETTIMANA 1 (1-7 Gennaio):
├── Studio 1-2: Guardiane + Pool Flessibile
├── Ricerca 1: Gerarchie Multi-Agent
└── Prima bozza architettura

SETTIMANA 2 (8-14 Gennaio):
├── Studio 3-4: Background Agents
├── Ricerca 2-3: Background + Dynamic Roles
└── Prototipo minimo

SETTIMANA 3 (15-21 Gennaio):
├── Studio 5: Verifica Attiva
├── Integrazione tutti gli studi
└── Proposta finale architettura v2.0

SETTIMANA 4 (22-31 Gennaio):
├── Implementazione prima Guardiana
├── Implementazione primo Background Agent
└── Test su progetto reale (Miracollo?)
```

---

## 💎 PRINCIPIO GUIDA

> **"Una Regina saggia non fa tutto da sola. Costruisce una Corte che la supporta."**

---

## 📝 NOTE E IDEE

*Spazio per aggiungere pensieri durante lo studio...*

### Idea di Rafa: "I Cugini" 🐝
> "Come fanno i ristoranti - serata impegnativa, chiamano uno con esperienza!"

Metafora perfetta per il Pool Flessibile!

### Idea di Rafa: "Scienziata in Background" 🔬
> "Mentre lavoriamo, lei cerca nuove funzioni, studi dei big players..."

Potrebbe essere il nostro "Innovation Engine"!

---

## 🔗 FILE CORRELATI

| File | Scopo |
|------|-------|
| FASE_7_LEARNING.md | Continuous Learning (prerequisito) |
| FASE_7.5_PARALLELIZZAZIONE.md | Parallelizzazione (prerequisito) |
| SWARM_RULES.md | Regole attuali dello sciame |
| DNA_FAMIGLIA.md | Template DNA per nuovi agenti |

---

## 📅 CHANGELOG

| Data | Modifica |
|------|----------|
| 1 Gen 2026 | Creazione documento - Brainstorm con Rafa! |

---

*"La Corte Reale: dove ogni ape sa il suo posto, e la Regina può finalmente PENSARE."* 👑🛡️🐝

*"È il nostro team! La nostra famiglia digitale!"* ❤️‍🔥

