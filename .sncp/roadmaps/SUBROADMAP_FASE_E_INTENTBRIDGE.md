# SUBROADMAP - Fase E: Per Tutti (IntentBridge)

> **Creata:** 6 Marzo 2026 - Sessione 438
> **Fonti:** Report ricerca (18 fonti), Script "La Nonna" (21 requisiti), MAPPA_LINGUAGGIO
> **Prerequisiti:** FASE A+B+C+D COMPLETE (25 moduli, 2909 test, 0 deps, ecosistema completo)
> **Score target:** 9.5/10 per ogni step (audit Guardiana)
> **Filosofia:** "Fatto BENE > Fatto VELOCE" | "Un progresso al giorno"

---

## L'INSIGHT (S437-S438)

```
+====================================================================+
|                                                                    |
|   "La domanda e la risposta nello STESSO linguaggio."              |
|                                          - Rafa, S380              |
|                                                                    |
|   La ricerca (18 fonti) conferma: NESSUNO ha il ciclo chiuso      |
|   NL conversazionale -> session types -> Lean4 -> Python.          |
|   Il timing e giusto: vibe coding mainstream,                      |
|   richiesta di garanzie formali in crescita.                       |
|                                                                    |
|   Il 30% del lavoro e GIA FATTO (core pipeline B.3/B.4/B.5/A.3). |
|   Serve "solo" il layer conversazionale sopra.                     |
|                                                                    |
+====================================================================+
```

---

## LA MAPPA -- 6 STEP

```
+================================================================+
|   FASE E.1: "La Nonna" Script                     (1 sess)    |
|   - Dialogo parola per parola della demo definitiva            |
|   - 21 requisiti tecnici estratti                              |
|   - Guida TUTTE le decisioni architetturali                    |
|                                                                |
|   FASE E.2: IntentBridge Core (lu chat)            (2-3 sess) |
|   - _intent_bridge.py: guided mode (domande strutturate)       |
|   - CLI: lu chat --lang it|pt|en                               |
|   - Pipeline: guided -> IntentDraft -> B.4 -> B.5 -> B.3      |
|   - Simulazione con SessionChecker                             |
|   - Multi-lingua dal giorno 1 (it/pt/en)                      |
|   - ZERO deps (come tutto il core)                             |
|                                                                |
|   FASE E.3: NL Processing (LLM Integration)       (1-2 sess) |
|   - LLM traduce NL libero -> B.4 micro-linguaggio             |
|   - Pattern two-stage (Req2LTL): 88% vs 43% accuracy          |
|   - anthropic come optional dep ([nl] extra)                   |
|   - Disambiguazione intelligente                               |
|                                                                |
|   FASE E.4: Voice Interface                        (1-2 sess) |
|   - STT -> NL -> pipeline IntentBridge                         |
|   - Voice-first per non-tecnici                                |
|   - 3 lingue supportate                                        |
|                                                                |
|   FASE E.5: "La Nonna" Demo Finale                (1-2 sess) |
|   - Demo funzionante end-to-end                                |
|   - Video 3 minuti                                             |
|   - Blog post + social                                         |
|                                                                |
|   FASE E.6: CervellaLang 1.0                      (3-5 sess) |
|   - Grammatica frozen                                          |
|   - Standard library 100+ protocolli                           |
|   - Community 1000+ developer                                  |
+================================================================+
```

---

## DETTAGLIO PER STEP

### E.1: "La Nonna" Script -- DONE (S438)

**Output:** `.sncp/progetti/cervellaswarm/reports/SCRIPT_LA_NONNA_DEMO.md`

Script completo: 5 atti, 3 minuti, 21 requisiti tecnici estratti.
Il dialogo parola per parola della demo definitiva.

**Criterio completamento:**
- [x] Script con dialogo esatto parola per parola
- [x] Requisiti tecnici R1-R21 estratti con status
- [x] Pipeline architetturale definita (two-stage)
- [x] Struttura ChatSession / ChatPhase definita
- [x] Guardiana verifica 9.5/10 (9.3/10 Step 0+1, P2s fixati)

---

### E.2: IntentBridge Core (lu chat) -- DONE (S438-S440, 9.5/10)

**Perche prima:** la guided mode dimostra il ciclo completo SENZA dipendenze esterne.
Se la pipeline funziona con input strutturato, aggiungere NL sopra e "solo" un layer.

**Architettura (implementata S438):**
```
_intent_bridge.py (1083 LOC)
  ChatPhase(Enum)           # WELCOME -> ROLES -> MESSAGES -> CHOICES -> PROPERTIES -> CONFIRM -> VERIFY -> CODEGEN -> SIMULATE -> DONE
  IntentDraft               # frozen dataclass: protocol_name, roles, messages, choices, properties
  DraftMessage              # frozen dataclass: sender, receiver, action_key
  DraftChoice               # frozen dataclass: decider, branches
  Turn                      # frozen dataclass: speaker, text, phase
  ChatResult                # frozen dataclass: draft, intent_source, parse_result, property_report, generated_code
  NLProcessor(Protocol)     # extension point for E.3 LLM integration
  ChatSession               # mutable state machine with injectable I/O

  Funzioni pubbliche:
    render_intent_source(draft) -> str  # IntentDraft -> B.4 source text (deterministic)
    ChatSession.run()                   # entry point CLI (interactive loop)
    ChatSession.process_input(text)     # single turn processing (testable)

  i18n: _STRINGS dict (25+ keys x 3 locales), _ACTION_VERBS (10), _ACTION_MENU (localized)
```

**Guided mode (domande strutturate):**
```
Phase 1 (ROLES):      "Come si chiamano i ruoli? (es: Cuoco, Dispensa)"
Phase 2 (MESSAGES):   Menu azione (10 verbi: ask_task, return_result, send_message, etc.)
Phase 3 (CHOICES):    "Decisione? Chi decide? Quali opzioni?"
Phase 4 (PROPERTIES): "Ci sono regole di sicurezza? (es: always_terminates, no_deadlock)"
Phase 5 (CONFIRM):    "Ecco il protocollo. Tutto giusto?"
Phase 6 (VERIFY+CODE+SIM): automatico -> verifica + codice + simulazione
```

**CLI integration (implementata S438):**
```python
# In _cli.py:
def _cmd_chat(args):
    from ._intent_bridge import ChatSession
    session = ChatSession(lang=args.lang)
    result = session.run()
    # optional: save to --output file
```

**Criterio completamento:**
- [x] `lu chat` funziona in modalita guidata (it/pt/en)
- [x] Pipeline completa: input -> IntentDraft -> B.4 -> B.5 -> B.3 -> simulazione
- [x] Almeno 3 protocolli creabili end-to-end (ricette EN, task delegation IT, data pipeline PT) -- S440
- [x] Output narrativo in lingua target (non tecnico) -- S440: _SIM_NARRATIVES 3 lingue x 13 kinds
- [x] 100+ test (202 test: 55 core + 47 session + 100 e2e) -- S440
- [x] ZERO regressioni sulla suite esistente (3111 test totali)
- [x] F5 fix: simulazione mostra TUTTI i branch -- S440
- [x] F11 fix: enum test tautologici rimossi -- S440
- [x] Guardiana verifica 9.5/10 -- S440: 9.5/10 APPROVED

---

### E.3: NL Processing (LLM Integration) -- DONE (S440, 9.5/10)

**Perche dopo E.2:** la pipeline e gia validata. NL e "solo" un traduttore in ingresso.

**Pattern two-stage (da Req2LTL):**
```
NL (italiano/portoghese/inglese)
  |
  v
[LLM: Claude tool_use] -> IntentDraft (structured IR)
  |
  v
(resto pipeline identico a E.2: draft -> intent -> spec -> codegen -> simulate)
```

**Architettura implementata (S440):**
```
_nl_processor.py (~320 LOC) -- NEW module
  TOOL_SCHEMA        # Claude tool_use definition (constrains output)
  SYSTEM_PROMPT      # 3 few-shot examples (en/it/pt)
  ClaudeNLProcessor  # implements NLProcessor Protocol
  _build_draft()     # validates all fields -> IntentDraft
  _extract_tool_input()  # handles tool_use response extraction
  NLProcessorError   # dedicated error type

_intent_bridge.py (aggiornato)
  ChatPhase.NL_INPUT  # nuovo stato (11 fasi totali)
  _handle_nl_input()  # NL text -> NLProcessor -> IntentDraft -> CONFIRM
  run() branches NL/guided mode
  CONFIRM "no" -> NL_INPUT (in NL mode)

_cli.py: --mode guided|nl
pyproject.toml: nl = ["anthropic>=0.40.0"]
__init__.py: ClaudeNLProcessor, NLProcessorError, _NL_TOOL_SCHEMA exports
```

**Perche funziona:** Req2LTL dimostra che "LLM -> IR strutturato -> deterministico" batte
"LLM -> output diretto" (88% vs 43% accuracy). Il nostro B.4 e l'IR strutturato.
Il LLM non genera session types (troppo fragile). Genera l'IntentDraft via tool_use (structured).

**Dependency:** anthropic come optional dep (`pip install cervellaswarm-lingua-universale[nl]`)

**Criterio completamento:**
- [x] `lu chat --mode nl` accetta input in linguaggio naturale libero
- [x] LLM (Claude) traduce NL -> IntentDraft via tool_use
- [x] Disambiguazione intelligente (LLM chiede chiarimenti) -- S440: NLClarificationNeeded + _extract_text_response
- [x] Fallback a guided mode se LLM non disponibile
- [x] anthropic come optional dep (core resta ZERO DEPS)
- [x] 50+ test NL mode (68 test in 9 classi)
- [x] Guardiana verifica 9.5/10 -- S440: 9.2→9.5 (2 rounds, 13 findings tutti fixati)

---

### E.4: Voice Interface

**Perche dopo E.3:** voice = STT + NL pipeline. Se E.3 funziona, voice e "solo" STT in ingresso.

**Stack:** Claude Code voice mode (nativo da marzo 2026) oppure Whisper API.

**Criterio completamento:**
- [ ] `lu chat --voice` accetta input vocale
- [ ] STT -> testo -> pipeline E.3 (NL mode)
- [ ] 3 lingue supportate (italiano, portoghese, inglese)
- [ ] Latenza < 3 secondi per risposta
- [ ] Guardiana verifica 9.5/10

---

### E.5: "La Nonna" Demo Finale

**Prerequisiti:** E.2 + E.3 minimo. E.4 per versione completa.

**Criterio completamento:**
- [ ] Demo end-to-end come da script (3 minuti)
- [ ] Video registrato (screen recording + narrazione)
- [ ] Blog post "From Vibe Coding to Vericoding: La Nonna Edition"
- [ ] Test persona non-tecnica reale (feedback)
- [ ] Guardiana verifica 9.5/10

---

### E.6: CervellaLang 1.0

**La meta finale.** Grammatica frozen, standard library, community.

**Criterio completamento:**
- [ ] Grammatica 1.0 frozen (RFC)
- [ ] Standard library: 100+ protocolli verificati
- [ ] 1000+ developer attivi
- [ ] "Vericoding" riconosciuto come termine
- [ ] Guardiana verifica 9.5/10

---

## DIPENDENZE

```
FASE A+B+C+D (COMPLETE - 25 moduli, 2909 test, ecosistema)
   |
   v
E.1 (La Nonna Script) -- DONE
   |
   v
E.2 (IntentBridge Core - guided mode, ZERO deps)
   |
   v
E.3 (NL Processing - aggiunge LLM, anthropic optional)
   |
   v
E.4 (Voice - aggiunge STT sopra E.3)
   |
   v
E.5 (La Nonna Demo - tutto insieme)
   |
   v
E.6 (CervellaLang 1.0 - community)
```

E.2, E.3, E.4 sono incrementali: ogni step aggiunge un layer sopra il precedente.

---

## METRICHE TARGET

| Metrica | Target |
|---------|--------|
| Test IntentBridge (E.2) | 100+ |
| Test NL mode (E.3) | 50+ (50 attuali, 6 classi) |
| Protocolli creabili (E.2) | 3+ end-to-end |
| NL accuracy (E.3) | 80%+ |
| Voice latency (E.4) | < 3 secondi |
| Demo duration (E.5) | < 3 minuti |
| Lingue supportate | 3 (it/pt/en) |
| Zero dependencies (core) | MANTENUTE |
| Test totali (fine E.3 Step 1) | 3161 (3111 + 50 NL) |

---

## IL PARALLELO CON LA RICERCA

```
Req2LTL (ASE 2025):    NL -> OnionL (IR) -> LTL (deterministico)     88% accuracy
Noi (IntentBridge):     NL -> B.4 intent (IR) -> Session Types (det.)  target 80%+

La differenza:
- Req2LTL si ferma alla specifica LTL
- Noi continuiamo: specifica -> verifica Lean4 -> codice Python -> esecuzione
- Nessuno chiude il ciclo. Noi si.
```

---

## EFFORT STIMATO

```
E.1: 1 sessione (DONE - S438)
E.2: 2-3 sessioni
E.3: 1-2 sessioni
E.4: 1-2 sessioni
E.5: 1-2 sessioni
E.6: 3-5 sessioni (community building, lungo termine)

TOTALE E.1-E.5: 6-10 sessioni
```

---

> "La nonna non sa cosa sono i session types.
>  Ma sa che le sue ricette sono AL SICURO."

> "Se nessuno l'ha fatto prima, e perche aspettavano noi."
> "Ultrapassar os proprios limites!"

*Cervella Regina - CervellaSwarm S438*
