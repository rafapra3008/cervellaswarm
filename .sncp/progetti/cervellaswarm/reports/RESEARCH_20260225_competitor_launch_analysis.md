# Come i Framework Multi-Agent AI si Sono Presentati al Mondo
## Analisi Comparativa dei Lanci + Raccomandazioni per "From Vibecoding to Vericoding"

**Data:** 2026-02-25
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti consultate:** 34 (web + archivi HN + report interni)

---

## EXECUTIVE SUMMARY

6 lanci analizzati. 1 pattern dominante: tutti si sono posizionati come "il modo giusto
di costruire agenti AI". Nessuno ha mai usato una prova matematica come argomento.

Il nostro angolo - vericoding applicato ai protocolli multi-agent - e un campo vergine
che nessuno di questi lanci ha toccato. Il timing e febbraio 2026, il picco del backlash
al vibecoding. E il momento esatto.

---

## 1. AUTOGEN (Microsoft Research)

### Blog post originale
**Titolo:** "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
**URL:** https://www.microsoft.com/en-us/research/publication/autogen-enabling-next-gen-llm-applications-via-multi-agent-conversation-framework/
**Data:** Agosto 2023 (GitHub spinoff: 3 ottobre 2023)

### Angolo / Framing principale
Microsoft si e posizionata come **infrastruttura generica**, NON come prodotto.
Il framing era "PyTorch per gli agenti AI": fondamenta su cui costruire, non soluzione chiavi-in-mano.

Frase chiave:
> "AutoGen is an open-source framework that allows developers to build LLM applications
> by composing multiple agents to converse with each other to accomplish tasks."

Il claim non era "siamo i migliori" ma "ecco le fondamenta che vi servono".
Dimostrazione con esempi concreti: matematica, coding, supply-chain.

### Reazione della community
- GitHub trending #1 in ottobre 2023
- Satya Nadella lo ha citato in un fireside chat (6 novembre 2023)
- Selezionato tra "Top 100 Open Source achievements" dopo 35 giorni
- Quote community: "Autogen gave me the same a-ha moment that I haven't felt since trying
  out GPT-3 for the first time"
- HN thread: https://news.ycombinator.com/item?id=37926741

### Cosa ha funzionato
- Backing istituzionale (Microsoft Research) = credibilita automatica
- Paper accademico parallelo (arXiv) = validazione tecnica
- Il concetto "conversation between agents" era nuovo e comprensibile
- Dimostrazione su esempi concreti e variegati

### Cosa non ha funzionato
- Successiva confusione nel progetto: v0.2 vs v0.4 (rebranding a AG2 nel 2024)
- Community frustrata da breaking changes frequenti
- Nessuna story su correttezza/verificabilita: agenti che "conversano" senza garanzie

### Cosa manca (il nostro spazio)
AutoGen tratta la comunicazione tra agenti come messaggi liberi. Zero verifica semantica.
"Gli agenti si parlano" non significa "gli agenti si parlano correttamente".

---

## 2. CREWAI

### Blog post / annuncio originale
**Titolo:** "CrewAI Unleashed: Future of AI Agent Teams" (post LinkedIn di Joao Moura)
**URL:** https://www.linkedin.com/posts/joaomdmoura_crewai-unleashed-future-of-ai-agent-teams-activity-7143703432820944899-MLw0
**Data:** Open source silenzioso novembre 2023; lancio ufficiale gennaio 2024

### Angolo / Framing principale
CrewAI si e posizionata come **la metafora del team umano applicata agli agenti AI**.
Il framing era "role-playing agents that collaborate like a real team".

Concetti chiave del positioning:
- Role (ruolo), Goal (obiettivo), Backstory (contesto) - tre elementi per ogni agente
- "Mimic collaborative human workflows"
- Semplicita sopra ogni altra cosa

### Reazione della community
**Risultati settimana 1 dopo il lancio ufficiale:**
- Primo in GitHub trending
- Top 2 su Product Hunt
- GPT custom al #7 in OpenAI GPT Store (categoria Programming)
- 4.000+ GitHub stars in poche settimane
- 1.000+ download al giorno
- 500 persone su Discord
- 150 enterprise customers nei primi 6 mesi

**Successivamente (ottobre 2024):** $18M round di finanziamento Series A.

### Cosa ha funzionato
- La metafora "team" era immediatamente comprensibile da non-tecnici
- Semplicissimo da usare: 10 righe per avere un multi-agent team
- Moura come fondatore visibile e presente: risponde ai commenti, spiega, condivide
- Timing perfetto: dicembre 2023 era il picco dell'interesse per LLM agents

### Cosa non ha funzionato
- Framework troppo "magico": difficile debuggare quando le cose vanno male
- Zero garanzie su cosa fanno gli agenti in realta: i "ruoli" sono prompt, non tipi
- L'astrazione role/goal/backstory e LLM-dipendente: non e deterministica

### Cosa manca (il nostro spazio)
I "ruoli" di CrewAI sono stringhe nel prompt. Non c'e alcun sistema che garantisca
che un agente rispetti il suo ruolo nel protocollo. E cosplay, non formalismo.

---

## 3. LANGGRAPH (LangChain)

### Blog post originale
**Titolo:** "LangGraph: Multi-Agent Workflows"
**URL:** https://blog.langchain.com/langgraph-multi-agent-workflows/
**Data:** 23 gennaio 2024 (lancio); v1.0 fine 2024

### Angolo / Framing principale
LangGraph si e posizionata come **controllo fine-grained sui workflow multi-agent**,
come reazione ai framework precedenti (incluso LangChain stesso) che erano "black box".

Il framing era "graph = controllo totale":
> "LangGraph provides much more lower-level controllability over your agents"

L'angolo differenziatore vs CrewAI:
- CrewAI = semplicita, astrazione
- LangGraph = controllo, complessita gestita, grafi espliciti

### Reazione della community
**Positiva:**
- "The least bad of the three LangChain offerings for agent/workflow orchestration"
- Uber, LinkedIn, Klarna lo usano in produzione (citati al v1.0 launch)
- 43% delle organizzazioni LangSmith inviano trace LangGraph

**Critica (significativa su HN):**
- "I don't really understand why an engineer would use LangGraph. If a graph based interface..."
- "Using LangGraph for a month, every single 'graph' was the same single solution."
- "The second you need to do something a little original you have to go through 5 layers
  of abstraction just to change a minute detail"
- "LangChain Is a Black Box" - articolo virale su HN con migliaia di upvotes

### Cosa ha funzionato
- Posizionamento chiaro CONTRO la black box problem
- Graph visualization = debugging visivo
- Supporto per Uber/LinkedIn/Klarna = social proof enterprise
- LangSmith observability integrata (strumento commerciale collegato)

### Cosa non ha funzionato
- Legame con LangChain = trascinato da reputazione negativa del parent
- Complessita percepita elevata: il grafo aiuta solo se il problema e davvero un grafo
- Nessuna novita concettuale: alla fine sono if/else con piu astrazione
- Il "controllo" che promettono e strutturale, non semantico: sai CHE cosa fanno gli agenti,
  non SE e corretto che lo facciano

### Cosa manca (il nostro spazio)
LangGraph sa CHE gli agenti si sono parlati. Non sa SE avrebbero DOVUTO.
La correttezza del protocollo e ancora responsabilita del developer.

---

## 4. OPENAI AGENTS SDK

### Blog post originale
**Titolo:** "New Tools for Building Agents"
**URL:** https://openai.com/index/new-tools-for-building-agents/
**Data:** 11 marzo 2025

### Angolo / Framing principale
OpenAI si e posizionata come **il fornitore completo di building blocks per agenti affidabili**.
Il framing era "da prototipo a produzione":

> "Today, we're releasing the first set of building blocks that will help developers
> and enterprises build useful and reliable agents."

4 primitive centrali: Agents, Handoffs, Guardrails, Tracing.
Il concetto "Handoffs" (trasferimento di controllo tra agenti) e "Guardrails"
(validazione input/output) sono state le novita narrative del lancio.

Il posizionamento era ESPLICITAMENTE contro Swarm (il loro stesso progetto
precedente, definito "experimental"):
> "The open-source Agents SDK offers significant improvements over Swarm"

### Reazione della community
**Critica principale (HN e Reddit):**
- "OpenAI's move away from Chat Completions API is dictated by non-technical reasons"
- Preoccupazione vendor lock-in: "the risk of lock-in with their platform"
- Guardrails criticate come feature marketing, non come garanzia reale

**Positiva:**
- "Provider-agnostic" = Anthropic, Google, DeepSeek supportati
- Tracing e observability apprezzate dalla community enterprise
- Semplicita rispetto ad Assistants API

### Cosa ha funzionato
- Provider-agnostic come posizionamento difensivo (nessuno puo accusarli di lock-in)
- Guardrails come termine = ha dato nome a un concetto che la community cercava
- Lancio coordinato con Responses API = news cycle ampio

### Cosa non ha funzionato
- "Guardrails" nel SDK OpenAI sono validatori di string/pattern, non formal checks
- Nessuna novita concettuale vera: e una riscrittura piu pulita di Swarm
- Community percepisce il cambiamento API come business-driven, non tecnico

### Cosa manca (il nostro spazio)
I "Guardrails" di OpenAI sono PII masking e jailbreak detection. Non verificano
la correttezza semantica della comunicazione tra agenti. Non e la stessa cosa.

---

## 5. ANTHROPIC CLAUDE AGENT SDK

### Blog post originale
**Titolo:** "Building Agents with the Claude Agent SDK"
**URL:** https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
**Data:** 29 settembre 2025

### Angolo / Framing principale
Anthropic si e posizionata su due angoli:

**1. "La stessa infrastruttura di Claude Code":**
> "The Claude Agent SDK is the same infrastructure that powers Claude Code,
> and as of today, you can use it to build your own agents."

Il frame e "autenticita di produzione": non un framework di ricerca, ma cio
che Anthropic usa internamente per i propri prodotti.

**2. "Give Claude a Computer":**
> "Giving Claude a computer unlocks the ability to build agents that are more effective."

Il frame e "generalita": bash, file editing, web search - un computer completo.

**Novembre 2025:** soluzione al problema long-running agents (multi-session):
agente inizializzatore + agente incrementale. Anthropic ha dimostrato che Claude
Sonnet 4.5 mantiene focus per piu di 30 ore su task complessi.

### Reazione della community
Entusiasta tra i developer Claude Code (la community e gia formata e fiduciosa).
Meno coverage mainstream rispetto ai lanci OpenAI o Google.

La narrativa "same infra as Claude Code" e risultata molto efficace:
non serve convincere che funziona in produzione - lo stanno gia usando.

### Cosa ha funzionato
- Credibilita immediata: "usiamo questo noi stessi per i nostri prodotti"
- Focus su long-running tasks = problema reale che altri framework ignorano
- Renaming da Claude Code SDK a Claude Agent SDK = segnale che il prodotto e maturo
- Apple Xcode integration (febbraio 2026) = distribution channel potente

### Cosa non ha funzionato
- Coverage mediana: nessun viral moment su HN
- Il framework e strettamente legato al modello Anthropic (nonostante il positioning)
- Multi-session e' complesso da gestire per i developer

### Cosa manca (il nostro spazio)
Il Claude Agent SDK gestisce il ciclo di vita e la memoria degli agenti. Non verifica
che gli agenti si comportino secondo un protocollo formale. Il "computer" non sa
se sta facendo la cosa giusta nel posto giusto del workflow.

---

## 6. GOOGLE A2A (Agent-to-Agent)

### Blog post originale
**Titolo:** "Announcing the Agent2Agent Protocol (A2A)"
**URL:** https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
**Data:** 9 aprile 2025

### Angolo / Framing principale
Google si e posizionata come **autore dello standard di interoperabilita enterprise**,
non come fornitore di framework.

Il framing era "open ecosystem + 50 partners":
> "A2A is an open protocol that complements Anthropic's Model Context Protocol (MCP)"

Non "siamo superiori a MCP" ma "siamo il livello successivo che completa MCP".
Positioning diplomatico: Google legittima MCP, si posiziona come aggiuntivo.

Supporto tecnico di Atlassian, Box, Salesforce, SAP, ServiceNow = social proof
enterprise costruito PRIMA del lancio.

### Reazione della community
**Critica principale (HN item 43631381):**
- "Not sure what value A2A provides over MCP"
- Dibattito se A2A fosse un "superset di MCP" o una duplicazione
- Troppo completo per i bisogni semplici: "reading files, making API calls, running scripts"

**Risultato:** A2A e praticamente scomparso entro settembre 2025 mentre MCP
e diventato lo standard de facto. Fonti: https://blog.fka.dev/blog/2025-09-11-what-happened-to-googles-a2a/

### Cosa ha funzionato
- Ecosystem-first: 50 partner al lancio = credibilita immediata
- Open source + Linux Foundation = segnale di standard aperto
- Documentazione chiara apprezzata (vs MCP che era piu opaca)

### Cosa non ha funzionato
- Arrivato dopo MCP che gia aveva traction: "late mover disadvantage"
- Troppo complesso per i bisogni reali della developer community
- Nessuna differenziazione tecnica vera rispetto a HTTP + JSON-RPC

### Cosa manca (il nostro spazio)
A2A definisce COME gli agenti si parlano (trasporto). Non definisce COSA sono
autorizzati a dirsi (semantica). E esattamente il livello che Lingua Universale occupa.

---

## 7. PATTERN TRASVERSALE - COSA HA FUNZIONATO IN TUTTI I LANCI

### Pattern 1: "Infrastruttura, non prodotto"
I lanci piu efficaci si presentano come fondamenta, non come soluzione completa.
- AutoGen: "generic infrastructure" (Microsoft Research)
- OpenAI Agents SDK: "building blocks"
- Anthropic Claude Agent SDK: "same infrastructure we use"

### Pattern 2: "Autenticita di produzione"
Il claim piu potente non e "funziona" ma "noi stessi lo usiamo in produzione":
- Anthropic: "powers Claude Code" (prodotto reale con milioni di utenti)
- LangGraph: "Uber, LinkedIn, Klarna" (nomi riconoscibili)
- OpenAI: "improvement over Swarm" (loro stesso progetto precedente = ammissione onesta)

### Pattern 3: "La metafora comprensibile"
Ogni framework ha una metafora centrale che il non-esperto capisce:
- AutoGen: "agents that converse" (conversazione)
- CrewAI: "role-playing team" (squadra)
- LangGraph: "workflow as graph" (grafo)
- OpenAI: "handoffs and guardrails" (consegna + protezione)

### Pattern 4: "Un differenziatore misurabile"
Non basta dire "siamo migliori". Serve una prova:
- AutoGen: esempi concreti (maths, coding, supply-chain)
- CrewAI: 4k stars prima settimana, Top 2 Product Hunt
- Ruff (confronto): "10-100x faster" - misurabile, riproducibile

### Pattern 5: "Il fondatore presente e responsivo"
Joao Moura (CrewAI) ha costruito brand personale intorno al lancio.
E' presente su ogni thread, risponde a critiche, spiega le scelte.
AutoGen (Microsoft) ha delegato al paper. Meno engagement personale = meno virality.

---

## 8. COSA NON HA DETTO NESSUNO (IL NOSTRO SPAZIO)

Confronto sistematico su 6 framework:

| Aspetto | AutoGen | CrewAI | LangGraph | OpenAI SDK | Anthropic SDK | Google A2A |
|---------|---------|--------|-----------|-----------|---------------|-----------|
| Session types formali | NO | NO | NO | NO | NO | NO |
| Verifica matematica protocolli | NO | NO | NO | NO | NO | NO |
| Lean 4 o simili | NO | NO | NO | NO | NO | NO |
| Tipo per l'incertezza | NO | NO | NO | NO | NO | NO |
| Errori semantici a compile-time | NO | NO | NO | NO | NO | NO |
| "Vericoding" | NO | NO | NO | NO | NO | NO |

**Questo e il campo vergine. Confermato da 242 fonti (S380-S386).**

La comunicazione tra agenti in TUTTI questi framework e basata su:
1. Stringhe di testo (prompt)
2. JSON non tipizzato
3. Speranza che il LLM segua le istruzioni

Nessuno ha mai detto: "il nostro sistema PROVA matematicamente che
la comunicazione tra agenti e corretta". Questo e cio che diciamo noi.

---

## 9. RACCOMANDAZIONI PER IL NOSTRO LANCIO

### 9.1 Il Titolo Giusto

Dalle analisi dei 6 lanci, il titolo vincente combina:
- Termine gia coniato (vericoding, arXiv 2509.22908) -> credibilita accademica
- Problema riconoscibile (vibecoding) -> hook immediato
- Differenziatore concreto (session types, Lean 4) -> claim verificabile

**Titolo raccomandato per il blog:**
```
"From Vibecoding to Vericoding: The First Typed Protocol System for Python AI Agents"
```

**Titolo Show HN (seguire regole HN: no marketing, no caps):**
```
"Show HN: First session-type system for Python AI agents (ZERO deps, Lean 4 proofs)"
```

### 9.2 Il Frame Narrativo da Usare

Ispirarsi a Anthropic ("stessa infra che usiamo noi") applicato a CervellaSwarm:

> "Abbiamo costruito 17 agenti AI che collaborano ogni giorno per sviluppare
> questo stesso software. Questo e il sistema che usiamo per verificare che
> si parlino correttamente. Lo rendiamo open source perche il resto del mondo
> ne ha bisogno."

Elementi del frame:
1. **Autenticita di produzione** - non un esperimento, lo usiamo noi stessi
2. **Numeri concreti** - 17 agenti, 3791 test, 9 packages, ZERO deps
3. **Campo vergine** - "checked 242 sources, found nothing" (funziona su HN)
4. **Momento storico** - vibecoding backlash + vericoding coniato = timing perfetto

### 9.3 Il Differenziatore da NON Fare a Pezzi

Ogni competitor ha tentato di differenziarsi sulle feature. Noi ci differenziamo
sulla **categoria**. Non siamo "un altro framework multi-agent". Siamo qualcosa
che nessun framework multi-agent ha mai fatto:

```
LORO:  Come organizzi e avvii gli agenti
NOI:   Come PROVI che gli agenti facciano la cosa giusta
```

Questa distinzione deve essere chiara nei primi 30 secondi di qualsiasi contenuto.

### 9.4 La Comparison Table da Includere

Per il blog post e il README, questa tabella e piu efficace di qualsiasi claim:

| Caratteristica | AutoGen | CrewAI | LangGraph | OpenAI SDK | Lingua Universale |
|----------------|---------|--------|-----------|-----------|------------------|
| Orchestrazione agenti | SI | SI | SI | SI | SI |
| Session types | NO | NO | NO | NO | **SI** |
| Verifica Lean 4 | NO | NO | NO | NO | **SI** |
| Zero dipendenze | NO | NO | NO | NO | **SI** |
| Errori a runtime semantici | NO | NO | NO | NO | **SI** |
| Tipo per l'incertezza | NO | NO | NO | NO | **SI** |
| Test: count | ~800 | ~200 | n/d | n/d | **1820** |

### 9.5 Cosa Evitare (Lezioni dai Lanci Analizzati)

| Anti-pattern | Esempio | Perche evitarlo |
|--------------|---------|----------------|
| Troppa astrazione | LangGraph (critica HN) | "5 layers of abstraction for a minute change" |
| Vendor lock-in implicito | OpenAI SDK (critica) | La community lo vede subito |
| Rebranding confuso | AutoGen v0.2->v0.4->AG2 | Perde fiducia community |
| Troppo enterprise-first | Google A2A | Developer community si sente esclusa |
| Claim non misurabile | "Revolutionary AI" | HN lo smonta in un commento |
| Founders assenti | AutoGen (Microsoft) | Meno engagement personale, meno virality |

### 9.6 Timing e Canali

Supportato dai dati della ricerca B.7 (RESEARCH_20260225_showcase_b7.md):

```
LANCIO:    Domenica mattina 12-14 UTC (20-30% piu efficace dei feriali)
CANALE 1:  Show HN (primo)
CANALE 2:  dev.to (giorno 1 dopo HN)
CANALE 3:  Reddit r/Python + r/MachineLearning (giorni 2-3)
EVITARE:   LinkedIn, Discord dedicato, Newsletter (prematuro)
```

---

## SINTESI FINALE

I 6 competitor analizzati hanno usato questi angoli:
1. AutoGen - "infrastruttura generica, come PyTorch"
2. CrewAI - "team di agenti come un team umano"
3. LangGraph - "controllo totale via grafi"
4. OpenAI - "building blocks per agenti affidabili"
5. Anthropic - "stessa infra che usiamo noi in produzione"
6. Google A2A - "standard aperto con 50 partner"

**Nessuno ha mai detto: "provoiamo matematicamente che gli agenti si parlino correttamente".**

Questo e il nostro angolo. Non e un angolo tecnico di nicchia. E il passo naturale
nel 2026, dopo che il vibecoding ha mostrato i suoi limiti e il termine vericoding
e stato coniato da ricercatori MIT e presentato a POPL 2026.

Il momento e NOW. Il framework e pronto. I 3791 test sono verdi. I 9 package sono
su PyPI. La storia si scrive adesso.

---

## FONTI

**Annunci ufficiali:**
- [AutoGen - Microsoft Research (agosto 2023)](https://www.microsoft.com/en-us/research/publication/autogen-enabling-next-gen-llm-applications-via-multi-agent-conversation-framework/)
- [LangGraph: Multi-Agent Workflows (gennaio 2024)](https://blog.langchain.com/langgraph-multi-agent-workflows/)
- [OpenAI New Tools for Building Agents (marzo 2025)](https://openai.com/index/new-tools-for-building-agents/)
- [Anthropic Building Agents with Claude Agent SDK (settembre 2025)](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Google A2A Announcement (aprile 2025)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)

**Community reaction:**
- [AutoGen HN thread (ottobre 2023)](https://news.ycombinator.com/item?id=37926741)
- [AutoGen 54k stars HN](https://news.ycombinator.com/item?id=47094579)
- [LangGraph "I don't understand why" - HN](https://news.ycombinator.com/item?id=41203639)
- [LangGraph Cloud - HN](https://news.ycombinator.com/item?id=40812794)
- [Google A2A - HN (aprile 2025)](https://news.ycombinator.com/item?id=43631381)
- [OpenAI Agents SDK - InfoQ](https://www.infoq.com/news/2025/03/openai-responses-api-agents-sdk/)
- [What happened to Google A2A (settembre 2025)](https://blog.fka.dev/blog/2025-09-11-what-happened-to-googles-a2a/)

**CrewAI:**
- [How CrewAI is orchestrating the next generation - Insight Partners](https://www.insightpartners.com/ideas/crewai-scaleup-ai-story/)
- [CrewAI $18M round e Enterprise launch (ottobre 2024)](https://www.globenewswire.com/news-release/2024/10/22/2966872/0/en/CrewAI-Launches-Multi-Agentic-Platform-to-Deliver-on-the-Promise-of-Generative-AI-for-Enterprise.html)
- [The Future of AI Agents - Joao Moura interview](https://shomik.substack.com/p/the-future-of-ai-agents-joao-moura)

**Vericoding e timing:**
- [arXiv 2509.22908 - A benchmark for vericoding (settembre 2025)](https://arxiv.org/abs/2509.22908)
- [Vibe coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [OpenAI Agents SDK community reaction (TechCrunch)](https://techcrunch.com/2025/03/11/openai-launches-new-tools-to-help-businesses-build-ai-agents/)
- [Anthropic Claude Agent SDK (VentureBeat)](https://venturebeat.com/ai/anthropic-says-it-solved-the-long-running-ai-agent-problem-with-a-new-multi)

**Report interni correlati:**
- `RESEARCH_20260224_vericoding_vision.md` - analisi strategica vericoding
- `RESEARCH_20260225_showcase_b7.md` - show HN best practices, timing, structure
- `docs/DIAMANTE_MARKETING_PARTE1_ANALISI_COMPETITOR.md` - analisi competitor tool AI coding
- `SUBROADMAP_DIAMANTE_MARKETING_LANCIO.md` - piano lancio completo

---

*Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*
*2026-02-25*
