# E.3 NL Processing - Ricerca Strategica
> Cervella Researcher | 2026-03-11 | Sessione 441
> Status: COMPLETA
> Fonti consultate: 12 (docs ufficiali Anthropic, survey, articoli, tool comparisons)

---

## Scope della Ricerca

4 domande chiave per E.3 (NL Processing / LLM Integration):
1. Claude API structured output -- come forzare output JSON/dataclass deterministico
2. NL -> structured: come fanno Rasa, Dialogflow, LUIS (slot filling, disambiguazione)
3. Prompt engineering per protocol extraction (ruoli, messaggi, scelte, proprieta)
4. Testing LLM features senza chiamate API reali (mocking, metriche)

---

## 1. Claude API: Structured Output

### Due approcci, uno chiaro vincitore per noi

**Approccio A: `client.messages.parse()` con Pydantic (RACCOMANDATO)**

Disponibile nell'SDK Python (versione attuale: 0.84.0, feb 2026). Non richiede piu beta headers.

```python
from pydantic import BaseModel
import anthropic

class IntentDraftOut(BaseModel):
    protocol_name: str
    roles: list[str]
    messages: list[dict]   # {sender, receiver, action_key}
    choices: list[dict]    # {decider, branches}
    properties: list[str]

client = anthropic.Anthropic()
response = client.messages.parse(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="...",  # system prompt con istruzioni estrazione
    messages=[{"role": "user", "content": user_nl_text}],
    output_format=IntentDraftOut,
)
draft = response.parsed_output  # typed, validated
```

**Approccio B: `tool_use` con `tool_choice={"type": "tool", "name": "X"}`**

Forza il modello a chiamare SEMPRE lo stesso tool. Utile quando si vuole piu controllo
sul flusso (es: distinguere "ho estratto tutto" da "ho bisogno di chiarimenti").

```python
tools = [{
    "name": "extract_intent_draft",
    "description": "Extract protocol structure from natural language description.",
    "input_schema": {
        "type": "object",
        "properties": {
            "protocol_name": {"type": "string"},
            "roles": {"type": "array", "items": {"type": "string"}},
            "messages": {"type": "array", "items": {...}},
            "needs_clarification": {
                "type": "boolean",
                "description": "True if input is ambiguous and needs user clarification"
            },
            "clarification_question": {
                "type": "string",
                "description": "Question to ask user if needs_clarification is True"
            }
        },
        "required": ["protocol_name", "roles", "needs_clarification"],
        "additionalProperties": False,
    },
    "strict": True,
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_intent_draft"},
    ...
)
```

### Scelta per E.3: tool_use con `needs_clarification`

Il tool_use vince per noi perche:
- Permette di includere `needs_clarification` + `clarification_question` nello stesso output strutturato
- `strict: True` garantisce schema compliance senza retry logic
- Piu esplicito del parse() per gestire i rami "estratto ok" vs "chiedi chiarimento"
- Modelli supportati: tutti i claude-*-4-* (Haiku 4.5, Sonnet 4.5/4.6, Opus 4.5/4.6)

### Limitazioni JSON Schema da tenere a mente

- `minimum`, `maximum`, `minLength`, `maxLength` vengono rimossi automaticamente dall'SDK
  (la validazione rimane lato client, non lato modello)
- Gli array annidati complessi possono ridurre l'accuracy -- preferire strutture flat quando possibile
- `additionalProperties: false` viene aggiunto automaticamente (non problema, anzi utile)
- Streaming + structured output: accumula tutto prima di deserializzare, non si puo fare parse incrementale

### Optional dependency: pattern da seguire

Il package Anthropic stesso usa `[project.optional-dependencies]` in pyproject.toml.
Per il nostro caso (mantenere core ZERO DEPS):

```toml
# In packages/lingua-universale/pyproject.toml
[project.optional-dependencies]
dev = [...]
test = [...]
lsp = ["pygls>=2.0"]
nl = ["anthropic>=0.84.0"]   # <-- aggiungere questo
```

Pattern import con fallback (stesso pattern di `lsp` per pygls):

```python
# In _nl_processor.py (nuovo file E.3)
try:
    import anthropic as _anthropic
    _HAS_ANTHROPIC = True
except ImportError:
    _HAS_ANTHROPIC = False

def _require_anthropic() -> None:
    if not _HAS_ANTHROPIC:
        raise ImportError(
            "NL mode requires anthropic. "
            "Install with: pip install cervellaswarm-lingua-universale[nl]"
        )
```

---

## 2. NL -> Structured: Come Fanno Rasa, Dialogflow, LUIS

### Pattern comune: Intent + Entities + Slots

Tutti e tre usano lo stesso schema concettuale:
1. **Intent classification**: capire COSA vuole l'utente (es: `create_protocol`, `add_message`)
2. **Entity extraction**: estrarre i VALORI concreti (es: `Cook`, `Pantry`, `ask_task`)
3. **Slot filling**: mappare le entities negli slot del form (es: `roles = ["Cook", "Pantry"]`)

**Dialogflow CX** aggiunge:
- Confidence score (0.0 - 1.0) per ogni intent match
- Threshold configurabile (sotto threshold -> `no-match` event -> fallback)
- Alternate intents quando piu intent hanno score simile

**Rasa** aggiunge:
- NLUCommandAdapter: converte intent+entities -> `SetSlot` commands automaticamente
- Threshold configurabile per fallback
- `FallbackClassifier` quando confidence < threshold

**Lezione per E.3**: non serve replicare questa architettura complessita. Con LLM (Claude)
otteniamo intent + entities + slot filling in un unico call. La confidenza si ottiene via
il campo `needs_clarification` (il LLM sa quando e ambiguo).

### Pattern "slot filling" adatto a IntentDraft

IntentDraft ha 5 "slot" da riempire:
- `protocol_name` (string, obbligatorio, facile)
- `roles` (array di stringhe, obbligatorio)
- `messages` (array di oggetti con sender/receiver/action_key, il piu difficile)
- `choices` (array, opzionale, spesso assente in protocolli semplici)
- `properties` (array con default `["always_terminates", "no_deadlock"]`)

Strategia: default sensati per i campi opzionali riducono il carico sul LLM.
`choices=[]` e `properties=["always_terminates","no_deadlock"]` sono default validi
per l'80% dei casi. Il LLM deve solo estrarli quando esplicitamente menzionati.

### Disambiguazione: pattern da Dialogflow

Quando confidence < threshold, Dialogflow chiede un clarification question.
Per noi, il LLM include `needs_clarification=True` + `clarification_question="..."`.
La ChatSession gestisce il loop:

```
NL input -> LLM extract -> needs_clarification?
  YES -> mostra clarification_question -> aspetta risposta -> retry con context
  NO  -> IntentDraft -> pipeline B.4 -> ... (identico a E.2)
```

Max 2-3 round di clarification prima di fallback a guided mode (evita loop infiniti).

---

## 3. Prompt Engineering per Protocol Extraction

### Architettura system prompt

**Tre componenti obbligatori**:
1. Ruolo e contesto ("Sei un estrattore di protocolli di comunicazione...")
2. Vocabolario vincolato (lista esplicita delle 10 action_keys valide)
3. Esempi few-shot (2-3 esempi NL -> JSON)

**Lingua: un singolo prompt multilingue o tre prompt?**

Ricerca (ACM FSE 2025, studi multilinguali LLM 2025) indica che i LLM moderni
(Claude Sonnet 4.x) gestiscono it/pt/en in modo comparabile con istruzioni in inglese.
Raccomandazione: system prompt in inglese, examples in lingua target, output sempre in inglese.

Questo perche:
- Le action_keys sono in inglese (ask_task, return_result, etc.) -- devono rimanere tali
- La coerenza dell'IR (IntentDraft) non deve dipendere dalla lingua dell'input
- Piu semplice da mantenere (un prompt, non tre)

### Template system prompt raccomandato

```python
SYSTEM_PROMPT = """You are a protocol extraction assistant for the CervellaSwarm Lingua Universale system.

Your task: extract a structured protocol definition from a natural language description.

## Valid action_keys (use ONLY these exact strings):
- ask_task: one role asks another to do a task
- return_result: one role returns a result to another
- ask_verify: one role asks another to verify something
- return_verdict: one role returns a verdict
- ask_plan: one role asks another to plan
- propose_plan: one role proposes a plan
- ask_research: one role asks another to research
- return_report: one role returns a report
- tell_decision: one role tells a decision
- send_message: one role sends a generic message

## Valid properties (use ONLY these):
- always_terminates: the protocol always ends
- no_deadlock: no deadlock can occur
- no_starvation: no role is starved of turns
- eventually_responds: a response eventually comes

## Rules:
- roles: extract all named participants, normalize to PascalCase (e.g. "Cook", "Pantry")
- messages: extract each communication step as {sender, receiver, action_key}
- choices: only include if a branching decision is explicitly described
- properties: default to ["always_terminates", "no_deadlock"] unless others mentioned
- If the description is ambiguous, set needs_clarification=True and provide a specific question
- Do NOT invent roles or messages not mentioned in the input

## Example (Italian input):
Input: "Voglio un sistema dove il cuoco chiede alla dispensa gli ingredienti e la dispensa li restituisce"
Output:
{
  "protocol_name": "RecipeExchange",
  "roles": ["Cook", "Pantry"],
  "messages": [
    {"sender": "Cook", "receiver": "Pantry", "action_key": "ask_task"},
    {"sender": "Pantry", "receiver": "Cook", "action_key": "return_result"}
  ],
  "choices": [],
  "properties": ["always_terminates", "no_deadlock"],
  "needs_clarification": false,
  "clarification_question": null
}
"""
```

### Few-shot: quanti esempi?

- 1 esempio (one-shot): sufficiente per pattern semplici (2 ruoli, messaggi lineari)
- 3 esempi (few-shot): raccomandato per coprire: lineare, con choice, multi-ruolo
- I 3 protocolli di E.2 (RecipeExchange, TaskDelegation, DataPipeline) sono i candidati naturali

### Chain-of-thought: utile o overhead?

Per extraction tasks strutturati, il CoT (chain-of-thought) non migliora significativamente
l'accuracy ma aumenta i token. Raccomandazione: NO CoT nel system prompt, ma aggiungere
`"description": "think step by step to identify all roles mentioned"` nei field descriptions
del tool schema dove necessario.

### Gestione multilingue in pratica

```python
def build_user_message(text: str, lang: str) -> str:
    lang_hint = {"it": "Italian", "pt": "Portuguese", "en": "English"}
    return f"[Input language: {lang_hint.get(lang, 'English')}]\n\n{text}"
```

Il language hint nel user message e sufficiente. Il LLM normalizza automaticamente
i nomi dei ruoli (es: "cuoco" -> "Cook", "despensa" -> "Pantry").

---

## 4. Testing LLM Features: Pattern Deterministici

### La piramide dei test per E.3

```
Layer 6 (Evals live)     -- SKIP per ora (costo, ci vuole dataset)
Layer 5 (Behavioral)     -- contracts su tool arguments
Layer 4 (Integration)    -- full stack con LLM mockato
Layer 3 (Component)      -- NLProcessor mockato
Layer 2 (Property-based) -- invarianti sul parsing
Layer 1 (Unit)           -- logica deterministica pura (ZERO mock)
```

### Layer 1: Unit tests ZERO mock (la maggior parte dei 50+ test)

```python
# Test deterministici: tutto cio che NON tocca il LLM
def test_intent_draft_to_b4_roundtrip():
    draft = IntentDraft(protocol_name="Test", roles=("A", "B"), ...)
    source = render_intent_source(draft)
    result = parse_intent(source)
    assert result.protocol.name == "Test"

def test_nl_processor_fallback_when_no_anthropic(monkeypatch):
    # Simula anthropic non installato
    monkeypatch.setattr("cervellaswarm_lingua_universale._nl_processor._HAS_ANTHROPIC", False)
    with pytest.raises(ImportError, match="pip install.*\\[nl\\]"):
        session = ChatSession(lang="en", mode="nl")
        session.run()
```

### Layer 3: Component tests con NLProcessor mockato

Questo e il pattern CHIAVE per E.3. Il `NLProcessor` e gia definito come `Protocol`
con `process(text, lang, context) -> IntentDraft`. Si crea un fake deterministico:

```python
# In tests/test_nl_processor.py
class FakeNLProcessor:
    """Deterministic fake: restituisce sempre un IntentDraft fisso per input fisso."""
    def __init__(self, mapping: dict[str, IntentDraft]):
        self._mapping = mapping

    def process(self, text: str, lang: str, context: list) -> IntentDraft:
        key = text.strip().lower()[:40]  # prime 40 char come chiave
        if key not in self._mapping:
            raise ValueError(f"FakeNLProcessor: unexpected input: {text!r}")
        return self._mapping[key]

@pytest.fixture
def recipe_nl_processor():
    return FakeNLProcessor({
        "voglio un sistema dove il cuoco chiede alla di": IntentDraft(
            protocol_name="RecipeExchange",
            roles=("Cook", "Pantry"),
            messages=(
                DraftMessage("Cook", "Pantry", "ask_task"),
                DraftMessage("Pantry", "Cook", "return_result"),
            ),
        )
    })

def test_nl_mode_full_pipeline(recipe_nl_processor):
    inputs = iter([
        "Voglio un sistema dove il cuoco chiede alla dispensa gli ingredienti",
        "yes",  # confirm
    ])
    session = ChatSession(
        lang="it",
        mode="nl",
        nl_processor=recipe_nl_processor,
        input_fn=lambda p: next(inputs),
        output_fn=lambda *a, **kw: None,
    )
    result = session.run()
    assert result.draft.protocol_name == "RecipeExchange"
    assert len(result.draft.roles) == 2
```

### Layer 4: Integration con mock Anthropic SDK

Per i test che verificano la chiamata API reale (formato, parametri):

```python
from unittest.mock import MagicMock, patch

def make_mock_tool_response(draft_dict: dict):
    """Costruisce una risposta Anthropic SDK mockata con tool_use."""
    tool_use_block = MagicMock()
    tool_use_block.type = "tool_use"
    tool_use_block.name = "extract_intent_draft"
    tool_use_block.input = draft_dict
    response = MagicMock()
    response.content = [tool_use_block]
    response.stop_reason = "tool_use"
    return response

@patch("cervellaswarm_lingua_universale._nl_processor._anthropic")
def test_claude_nl_processor_calls_api(mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.Anthropic.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_tool_response({
        "protocol_name": "TestProtocol",
        "roles": ["Alice", "Bob"],
        "messages": [{"sender": "Alice", "receiver": "Bob", "action_key": "ask_task"}],
        "choices": [],
        "properties": ["always_terminates", "no_deadlock"],
        "needs_clarification": False,
        "clarification_question": None,
    })

    processor = ClaudeNLProcessor(api_key="test-key")
    draft = processor.process("Alice asks Bob something", "en", [])

    assert draft.protocol_name == "TestProtocol"
    mock_client.messages.create.assert_called_once()
    call_kwargs = mock_client.messages.create.call_args[1]
    assert call_kwargs["tool_choice"] == {"type": "tool", "name": "extract_intent_draft"}
```

### Metriche accuracy per NL -> structured (target 80%+)

Metrica standard per questo tipo di task: **slot accuracy** (per ogni campo dell'IR):
- `protocol_name_exact_match`: % casi dove il nome estratto e corretto
- `roles_f1`: precision/recall sui ruoli estratti
- `messages_exact_match`: % casi dove TUTTI i messaggi sono estratti correttamente
- `action_key_accuracy`: % action_keys corrette sul totale dei messaggi

Per costruire il dataset di eval (necessario prima di go-live):
- Usare i 3 protocolli di E.2 come golden set iniziale
- Aggiungere varianti linguistiche (10-15 riformulazioni per protocollo)
- Target: 30-50 esempi annotati per lingua = 90-150 esempi totali

Strumenti open source: `deepeval` (specialized pytest for LLM evals), oppure
script custom con json comparison. Dato che abbiamo gia il framework pytest,
raccomando script custom per mantenere ZERO deps extra nel test suite.

---

## Sintesi Decisioni per E.3

### Architettura ClaudeNLProcessor

```
_nl_processor.py (nuovo file, optional dep)
  ClaudeNLProcessor(NLProcessor)  # implementa il Protocol gia definito
    __init__(api_key=None, model="claude-sonnet-4-6", lang="en")
    process(text, lang, context) -> IntentDraft
      1. build_messages(text, lang, context) -> list[dict]
      2. client.messages.create(tools=[EXTRACT_TOOL], tool_choice=FORCE, ...)
      3. parse_tool_response(response) -> IntentDraft | ClarificationNeeded
      4. Se needs_clarification -> raise ClarificationNeeded(question)
      5. map_to_intent_draft(tool_output) -> IntentDraft

  EXTRACT_TOOL: dict  # schema JSON fisso, modulo-level constant
  SYSTEM_PROMPT: str  # con few-shot examples, modulo-level constant
```

### Modifiche a ChatSession (E.2 -> E.3)

`ChatSession` gia ha `nl_processor: NLProcessor | None`. In E.3:
- Aggiungere `mode: Literal["guided", "nl"] = "guided"` a `__init__`
- Quando `mode="nl"` e `nl_processor` e `None`: raise con istruzione install
- Quando `mode="nl"` e `nl_processor` e presente: fase ROLES accetta NL libero
- Il resto della pipeline (CONFIRM -> VERIFY -> CODEGEN -> SIMULATE) e identico

### CLI integration

```python
# _cli.py: aggiungere --mode nl
lu chat --mode nl --lang it     # usa ClaudeNLProcessor con ANTHROPIC_API_KEY dall'env
lu chat --mode nl --lang it --api-key sk-...  # override API key
lu chat                          # guided mode (default, ZERO DEPS)
```

### Fallback chain

```
--mode nl + ANTHROPIC_API_KEY presente -> ClaudeNLProcessor
--mode nl + ANTHROPIC_API_KEY assente  -> errore esplicito con istruzioni
--mode guided (default)                -> guided mode E.2 (ZERO DEPS, sempre disponibile)
```

---

## 3 Raccomandazioni Chiave

### Raccomandazione 1: tool_use con campo `needs_clarification` (NON parse())

`tool_choice={"type": "tool", "name": "extract_intent_draft"}` forza sempre lo stesso
output strutturato. Il campo `needs_clarification: bool` dentro lo schema gestisce
la disambiguazione in modo elegante senza secondo round-trip.
Evidenza: pattern validato da Dialogflow/LUIS (confidence threshold -> clarification).

### Raccomandazione 2: FakeNLProcessor come layer di test primario

Il `NLProcessor` Protocol gia esistente e il punto di iniezione perfetto.
80%+ dei test E.3 devono usare `FakeNLProcessor`, non mock Anthropic SDK.
Questo mantiene i test veloci, deterministici, senza costo API.
Solo 5-10 test di Layer 4 usano mock SDK per verificare il formato delle chiamate.

### Raccomandazione 3: System prompt con few-shot in lingua + vocabolario vincolato

I 10 action_keys devono essere elencati esplicitamente nel system prompt.
Senza questa lista, il LLM inventa varianti ("request_task", "ask_ingredient", etc.)
che rompono il mapping verso B.4.
I 3 protocolli di E.2 sono i few-shot examples naturali (uno per lingua).

---

## Effort Stimato E.3

```
Step 1: _nl_processor.py (ClaudeNLProcessor, EXTRACT_TOOL, SYSTEM_PROMPT)  -- 0.5 sess
Step 2: Integrazione ChatSession (mode="nl", fallback, CLI --mode nl)       -- 0.5 sess
Step 3: Test suite 50+ (FakeNLProcessor unit, mock SDK integration)         -- 0.5 sess
Step 4: Guardiana audit 9.5/10                                               -- 0.5 sess
TOTALE: 2 sessioni (stima conservativa, nel range subroadmap 1-2 sess)
```

---

## Fonti Consultate

1. [Structured outputs - Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) -- approcci, Pydantic, output_config
2. [How to implement tool use - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use) -- tool_choice, force tool, best practices
3. [anthropic PyPI](https://pypi.org/project/anthropic/) -- versione 0.84.0, extras pattern
4. [Rasa NLU Slots](https://rasa.com/docs/reference/primitives/slots/) -- slot filling mechanism
5. [Rasa Intents and Entities](https://rasa.com/docs/reference/primitives/intents-and-entities/) -- intent classification
6. [Dialogflow ES Intent Matching](https://docs.cloud.google.com/dialogflow/es/docs/intents-matching) -- confidence scores, threshold, fallback
7. [Req2LTL paper](https://arxiv.org/html/2512.17334) -- two-stage pattern (gia nel report S437)
8. [Langfuse LLM Testing Guide](https://langfuse.com/blog/2025-10-21-testing-llm-applications) -- testing strategies (non deterministiche)
9. [Testing Pyramid for AI Agent](https://dev.to/aashmawy/how-i-test-an-ai-support-agent-a-practical-testing-pyramid-3iik) -- 6 layer pyramid, mocking patterns
10. [Mocking External APIs - Scenario](https://langwatch.ai/scenario/testing-guides/mocks/) -- dependency injection per mock LLM
11. [Few-Shot Prompting Guide](https://www.promptingguide.ai/techniques/fewshot) -- few-shot per structured extraction
12. [deepeval - LLM Evaluation Framework](https://github.com/confident-ai/deepeval) -- metriche accuracy

---

## Output Header (per la Regina)

```
## E.3 NL Processing - Ricerca
Status: COMPLETA
Fonti: 12 consultate

Sintesi:
- Claude API: tool_use con tool_choice=force + needs_clarification field e l'approccio
  migliore. Niente beta headers, modello supportato: claude-sonnet-4-6. SDK v0.84.0.
- Optional dep: [nl] = ["anthropic>=0.84.0"] in pyproject.toml. Pattern import/fallback
  identico al pattern [lsp]/pygls gia in uso.
- Rasa/Dialogflow/LUIS: tutti usano intent+entities+slots+confidence. Con LLM tutto
  in un unico call. needs_clarification=True sostituisce il "confidence threshold fallback".
- Prompt engineering: system prompt EN con vocabolario vincolato (10 action_keys), few-shot
  in lingua target (i 3 protocolli E.2 sono gli esempi naturali), language hint nel user msg.
- Testing: FakeNLProcessor come layer primario (80%+ dei test), mock SDK solo per
  verificare formato chiamate API (10-15 test). Test deterministici senza costo API.

Raccomandazione:
  1. tool_use + needs_clarification (NON parse()) -- gestisce estrazione + disambiguazione
  2. FakeNLProcessor come punto di iniezione test (Protocol gia definito in E.2)
  3. System prompt con 10 action_keys esplicite + 3 few-shot examples (una per lingua)

Report: .sncp/progetti/cervellaswarm/reports/RESEARCH_20260311_E3_NL_PROCESSING.md
```

---

*"Ricerca PRIMA di implementare."*
*"Non inventare, studia come fanno i big."*

*Cervella Researcher - CervellaSwarm S441*
