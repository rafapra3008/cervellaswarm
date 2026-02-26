# Stato dell'Arte: Linguaggi AI-Native (Febbraio 2026)
**Data:** 2026-02-26
**Status:** COMPLETA
**Fonti:** 14 consultate (web search + fetch diretti)
**Per:** Lingua Universale - Positioning Fase C

---

## 1. Mappa Competitiva - Chi Fa Cosa

### Categoria A: Linguaggi "AI-native" (i concorrenti diretti nominali)

**Dana (AI Alliance / Aitomatic, Giugno 2025)**
- Annunciato da AI Alliance (IBM, Meta, AMD, Aitomatic)
- Sintassi Python-like (.na files) con `reason()` calls AI-native
- Focus: intent-driven development, concurrency, memory grounding
- Self-improving pipelines via `|` operator e POET feedback loops
- Esecuzione locale o cloud
- Gap critico: NESSUNA formal verification, NESSUN type system rigoroso,
  NESSUNA garanzia di protocollo. E "AI-powered" non "AI-verified".
- Fonte: https://aitomatic.github.io/dana/

**Mojo (Modular, versione 1.0 H1 2026)**
- Focus: performance AI/ML (Python-compatible + MLIR/CUDA)
- "Syntax sugar for MLIR" - ottimizzato per GPU/CPU parallelism
- 750K+ lines open source, 50K community
- Gap: non e per agenti. E per modelli ML. Zero session types, zero
  protocolli, zero confidence types.
- Fonte: https://docs.modular.com/mojo/roadmap/

**Bend (HigherOrderCO, 2024)**
- Parallel execution massiva su GPU via HVM2
- Python/Haskell feel, parallelismo automatico
- 51x speedup su RTX 4090
- Gap: performance pura, zero concetti agentici, zero verifica.

### Categoria B: DSL per LLM (tool di prompting)

**DSPy (Stanford, attivo 2025)**
- "Programming not prompting" - ottimizza pipeline LLM
- Modules, Signatures, Teleprompters (optimizer)
- Gap: ottimizza i prompt, non verifica i protocolli. Single-LM focus.
- NON affronta multi-agent communication formale.

**Guidance / LMQL / Outlines**
- Controllo strutturato di singole chiamate LLM
- JSON output, regex constraints
- Gap: solo output strutturato di UN singolo LLM. Zero concetti di
  fiducia, ruoli, sequenza di messaggi verificata.

### Categoria C: Protocolli Multi-Agent (non linguaggi ma standard)

**MCP (Anthropic, 2024-2025)**
- JSON-RPC typed tool invocation
- Standard de-facto per tool access
- Adottato da OpenAI, Microsoft, GitHub, Cursor, Figma
- Gap: typed tools si, ma NESSUN protocollo di sessione, NESSUNA
  sequenza verificata, NESSUN confidence type.

**A2A (Google, 2025)**
- Agent Cards (JSON metadata) per capability discovery
- Peer-to-peer task outsourcing
- Gap: discovery e routing, non verifica formale.

**ACP (IBM/BeeAgent, 2025)**
- REST-native, multipart messages, async streaming
- Gap: struttura messaggi, non semantica verificata.

**Agent Skills (Anthropic, Dicembre 2025)**
- Skill = directory con SKILL.md + scripts
- Modular procedural memory per agenti
- Gap: packaging di workflow, non type-checking.

I 4 protocolli sono COMPLEMENTARI non concorrenti.
Survey: https://arxiv.org/abs/2505.02279

### Categoria D: Framework Multi-Agent (competitor indiretti)

| Framework | Stars GitHub | Approccio | Gap |
|-----------|-------------|-----------|-----|
| LangGraph | ~40K | Graph-based workflows | Zero formal types |
| CrewAI | ~35K | Role-based agents | Zero protocol check |
| AutoGen (Microsoft) | ~45K | Conversation-based | Zero verification |

Tutti e 3 usano messaggi come dizionari/stringhe non tipati.
Nessuno verifica la sequenza dei messaggi. Nessuno ha confidence types.
120K+ stars totali = mercato ENORME, nessuno risolve il problema core.

---

## 2. Trend Accademici (2024-2025)

**LLM + Formal Methods: il campo sta emergendo**
- Paper ArXiv 2412.06512: "Fusion of LLMs and Formal Methods for
  Trustworthy AI Agents - A Roadmap" (Dicembre 2024)
- Paper OpenReview: "Trustworthy AI Agents Require LLMs + Formal Methods"
- Ricerca su LTL (Linear Temporal Logic) + Kripke structures per piani AI
- BetaProbLog: epistemic uncertainty in probabilistic logic programs
- TENDENZA CHIARA: il mondo accademico sta convergendo verso
  "AI + verifica formale" come prossimo step necessario.

**Session Types come concetto: non ancora applicato agli agenti AI**
- La ricerca specifica "session types per agenti AI" non ha prodotti
  commerciali o librerie Python note.
- I multiparty session types (Honda, Yoshida, Carbone 2008) restano
  un concetto prevalentemente accademico (Haskell, OCaml, Rust).
- In Python: CAMPO VERGINE (confermato dalla nostra ricerca S375).

**Lingua Franca: il mondo ne sta parlando**
- Paper Springer 2025: "The babel of the bots: semantic collapse in
  multi-agent AI and the case for a Lingua Franca"
  (https://link.springer.com/article/10.1007/s00146-025-02668-1)
- Il problema e riconosciuto accademicamente: agenti che si "non capiscono"
  tra loro nonostante usino lo stesso LLM.
- La soluzione proposta nei paper: standardizzazione semantica.
  Nessuno propone session types come soluzione.

---

## 3. Gap Identificati (cosa manca)

| Gap | Chi lo ha | Chi non ce l'ha |
|-----|-----------|-----------------|
| Session types per Python | Solo noi | Tutti gli altri |
| Confidence come tipo nativo | Solo noi | Tutti |
| Trust composition formale | Solo noi | Tutti |
| Lean 4 protocol verification | Solo noi | Tutti |
| Runtime protocol checker | Solo noi | Tutti |
| Zero dependencies | Solo noi | Tutti hanno molte |

**GAP #1 - IL PIU GRANDE:** Nessun framework verifica CHE il protocollo
sia stato rispettato. Tutti usano "speranza". Noi usiamo `ProtocolViolation`.

**GAP #2:** Nessuno tratta l'incertezza come TIPO. DSPy la ottimizza
ma non la rappresenta strutturalmente nel codice.

**GAP #3:** Nessun linguaggio agente ha prove matematiche dei protocolli.
Dana si avvicina alla visione (intent-driven) ma non alla verifica.

**GAP #4 - SEMANTICO:** Il paper Springer identifica "semantic collapse"
ma propone soluzioni linguistiche/ontologiche, non type-theoretic.
CervellaSwarm e l'unico che usa session types come soluzione.

---

## 4. Analisi Timing

**Favorevole:**
- 2026 e dichiarato "anno dei multi-agent systems" (AI Agent Directory)
- 40% enterprise apps con AI agents entro 2026 (Gartner)
- Il problema che risolviamo e riconosciuto da paper accademici
- Dana dimostra che c'e appetite per "linguaggi agente-nativi"
- I protocolli (MCP/A2A) sono la plumbing, noi siamo la semantics

**Sfide:**
- Dana (AI Alliance con IBM/Meta) ha risorse enormi ma approccio
  diverso (non formal). Potrebbe "occupare" il mindshare "AI language"
- La community potrebbe non capire immediatamente la differenza tra
  "AI-powered" (Dana) e "AI-verified" (Lingua Universale)
- Fase C e 2027+: il campo evolve veloce

**Positioning consigliato:**
  Dana = "AI scrive il codice per te" (vibecoding avanzato)
  Lingua Universale = "AI PROVA che il codice e corretto" (vericoding)
  Queste sono visioni COMPLEMENTARI, non in competizione diretta.

---

## 5. Raccomandazione per Fase C

**Il nostro differenziatore e chiaro e unico:**
Session types + Confidence types + Lean 4 verification per AI agents,
in Python, zero dependencies. Nessuno lo fa.

**Narrative da usare con la community (Show HN e oltre):**
1. "Every other framework uses hope. We use proofs."
2. "The difference between vibe-coding and veri-coding."
3. Citare il paper Springer "semantic collapse" - siamo la soluzione
   che il mondo accademico sta cercando senza averla trovata.

**Azioni concrete per Fase C:**
1. Monitorare Dana - potenziale alleato (intent layer) + noi (proof layer)
2. MCP integration come PRIORITA: diventare "MCP + formal verification"
   e il killer feature mancante nell'ecosistema Anthropic
3. Citare survey ArXiv 2505.02279 nelle PR/blog: mostra che il campo
   e maturo ma manca il layer formale
4. Seguire il paper "LLMs + Formal Methods Roadmap" (2412.06512)
   come roadmap accademica parallela alla nostra

---

## 6. Fonti Chiave

- Dana language: https://aitomatic.github.io/dana/
- AI Alliance announcement: https://thealliance.ai/blog/the-ai-alliance-releases-new-ai-powered-programmin
- Mojo roadmap: https://docs.modular.com/mojo/roadmap/
- Agent protocols survey: https://arxiv.org/abs/2505.02279
- Agent Skills (Anthropic): https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/
- Springer lingua franca: https://link.springer.com/article/10.1007/s00146-025-02668-1
- LLMs + Formal Methods roadmap: https://arxiv.org/html/2412.06512v1
- DSPy: https://dspy.ai/
- LangGraph/CrewAI/AutoGen comparison 2026: https://markaicode.com/crewai-vs-autogen-vs-langgraph-2026/

---

*Cervella Researcher - 2026-02-26*
*"Ricerca PRIMA di implementare."*
