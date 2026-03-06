# Plan: TASK_E2 - IntentBridge Module Architecture

## Metadata
- **Task ID**: TASK_E2
- **Architect**: cervella-architect
- **Created**: 2026-03-06
- **Complexity**: High
- **Files Affected**: 5 new + 2 modified
- **Risk Score**: 0.4 (medium -- new module, but existing pipeline is stable)

---

## Phase 1: Understanding

### User Request
Design the `_intent_bridge.py` module for `packages/lingua-universale/` that provides a guided conversational interface to build protocols from natural language input, following the two-stage pattern (NL -> IntentDraft -> B.4 parse_intent() -> existing pipeline). Phase E.2 is GUIDED mode (no LLM), E.3 adds LLM later.

### Codebase Analysis

**Existing modules that IntentBridge will reuse:**
- `intent.py` (B.4): `parse_intent(source) -> IntentParseResult` -- deterministic parser for micro-language. Maps action verbs to `MessageKind` via `_ACTION_MAP`.
- `spec.py` (B.5): `parse_spec(source) -> ProtocolSpec`, `check_properties(protocol, spec) -> PropertyReport` -- static checker. `check_session(log, spec) -> PropertyReport` -- runtime checker.
- `codegen.py` (B.3): `generate_python(protocol) -> str`, `PythonGenerator` -- generates self-contained Python modules.
- `checker.py` (A.3): `SessionChecker` -- runtime enforcement. `ProtocolViolation`, `SessionComplete`, `MessageRecord`.
- `protocols.py`: `Protocol`, `ProtocolStep`, `ProtocolChoice` -- frozen dataclasses, the core data model.
- `errors.py` (B.6): i18n catalog pattern -- `MappingProxyType` dict with `"en"/"it"/"pt"` keys, each a `(message, suggestion)` tuple. Constants: `DEFAULT_LOCALE = "en"`, `SUPPORTED_LOCALES = frozenset({"en", "it", "pt"})`.
- `_cli.py`: argparse-based, `_build_parser()` returns `ArgumentParser` with subparsers, `_COMMAND_HANDLERS` dict dispatches.
- `_repl.py`: `REPLSession` class with injectable `input_fn`/`output_fn` for testability. Readline support. Colon-prefixed commands.
- `_colors.py`: shared `colors` singleton with `init_colors()`. Respects `NO_COLOR`/`FORCE_COLOR`.

**Key patterns observed:**
- P01: All value objects are `@dataclass(frozen=True)`.
- P04: Immutable mappings via `MappingProxyType`.
- ZERO external dependencies throughout.
- i18n done via in-module dict, not separate files.
- Tests have NO `__init__.py` in test directories (P17).
- CLI uses argparse stdlib, REPL uses injectable I/O for testing.

### Constraints
- ZERO external deps for core.
- Frozen dataclass for all value objects.
- Must reuse existing pipeline modules (intent.py, spec.py, codegen.py, checker.py).
- CLI via argparse, integrated into existing `_build_parser()`.
- i18n: dict-based, not file-based. Support it/pt/en.
- Tests without `__init__.py`.
- E.2 = guided mode (structured questions), NO LLM.
- E.3 = NL mode with optional `anthropic` dep (designed now, implemented later).

---

## Phase 2: Design

### 1. Architecture: Module Structure

IntentBridge is ONE new module `_intent_bridge.py` (private, prefixed with `_`) plus a thin CLI integration in `_cli.py`. All public API re-exported from `__init__.py`.

```
_intent_bridge.py     # Core: ChatSession, guided builder, i18n strings
                      # ~400-500 lines estimated

_cli.py               # Modified: add `lu chat` subcommand (~30 lines added)
__init__.py            # Modified: re-export IntentBridge public API (~10 lines added)
```

### 2. Data Model (all frozen dataclasses)

```python
class ChatPhase(Enum):
    """Phases of the guided conversation."""
    WELCOME = "welcome"       # Initial greeting
    DESCRIBE = "describe"     # User describes what they want
    ROLES = "roles"           # Clarify roles
    MESSAGES = "messages"     # Clarify message flow
    CHOICES = "choices"       # Clarify branching (optional)
    PROPERTIES = "properties" # Clarify safety properties
    CONFIRM = "confirm"       # Show draft, ask for confirmation
    VERIFY = "verify"         # Run spec checker
    CODEGEN = "codegen"       # Generate code
    SIMULATE = "simulate"     # Run simulation
    DONE = "done"             # Session complete


@dataclass(frozen=True)
class IntentDraft:
    """Intermediate representation between NL and B.4 micro-language.

    This is the "OnionL" equivalent from Req2LTL: a structured
    intermediate that maps deterministically to intent notation.
    """
    protocol_name: str
    roles: tuple[str, ...]                              # ("Cuoco", "Dispensa")
    messages: tuple[DraftMessage, ...]                   # ordered message specs
    choices: tuple[DraftChoice, ...] = ()                # branching points
    properties: tuple[str, ...] = ()                     # ("always_terminates", ...)
    confidence: str = "high"                             # confidence level label


@dataclass(frozen=True)
class DraftMessage:
    """A single message in the draft."""
    sender: str          # role name
    receiver: str        # role name
    action: str          # B.4 action verb key (e.g., "asks_to_do_task")
    description: str = ""


@dataclass(frozen=True)
class DraftChoice:
    """A branching point in the draft."""
    decider: str                                         # role name
    branches: tuple[tuple[str, tuple[DraftMessage, ...]], ...]  # (label, messages)


@dataclass(frozen=True)
class Turn:
    """A single turn in the conversation."""
    speaker: str         # "user" or "system"
    text: str
    phase: ChatPhase


@dataclass(frozen=True)
class ChatResult:
    """Final result of a completed chat session."""
    draft: IntentDraft
    intent_source: str                  # Generated B.4 intent notation text
    parse_result: IntentParseResult     # From intent.py
    property_report: PropertyReport     # From spec.py
    generated_code: str                 # From codegen.py
    simulation_log: tuple[MessageRecord, ...] = ()
```

### 3. ChatSession (mutable, like REPLSession)

```python
class ChatSession:
    """Stateful guided conversation for building protocols.

    Injectable I/O for testability (same pattern as REPLSession).
    """
    def __init__(
        self,
        *,
        lang: str = "en",
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[..., None] | None = None,
    ) -> None: ...

    # Public API
    def run(self) -> ChatResult | None: ...        # Main loop (blocking)
    def process_input(self, text: str) -> str: ... # Single-turn (for testing/bots)

    # Properties
    @property
    def phase(self) -> ChatPhase: ...
    @property
    def draft(self) -> IntentDraft | None: ...
    @property
    def turns(self) -> list[Turn]: ...
    @property
    def lang(self) -> str: ...
```

**Design rationale:** `ChatSession` is mutable (like `REPLSession` and `SessionState`) because it tracks conversation state. The *results* it produces (`IntentDraft`, `ChatResult`, `Turn`) are all frozen.

### 4. Guided Builder (E.2 core logic)

The guided builder is a state machine inside `ChatSession`. Each phase has:
- A **prompt function** that generates the question to ask the user
- A **parse function** that interprets the user's answer
- A **transition function** that decides the next phase

```python
# Phase transition table (internal)
_TRANSITIONS: dict[ChatPhase, ChatPhase] = {
    ChatPhase.WELCOME:    ChatPhase.DESCRIBE,
    ChatPhase.DESCRIBE:   ChatPhase.ROLES,
    ChatPhase.ROLES:      ChatPhase.MESSAGES,
    ChatPhase.MESSAGES:   ChatPhase.CHOICES,
    ChatPhase.CHOICES:    ChatPhase.PROPERTIES,
    ChatPhase.PROPERTIES: ChatPhase.CONFIRM,
    ChatPhase.CONFIRM:    ChatPhase.VERIFY,    # on "yes"
    # CONFIRM -> ROLES on "no" (back to editing)
    ChatPhase.VERIFY:     ChatPhase.CODEGEN,
    ChatPhase.CODEGEN:    ChatPhase.SIMULATE,
    ChatPhase.SIMULATE:   ChatPhase.DONE,
}
```

**Each phase handler is a private method** `_handle_{phase}(user_input: str) -> str` that:
1. Parses user input
2. Updates internal state (builds `IntentDraft` incrementally)
3. Transitions to next phase
4. Returns the system response string

### 5. IntentDraft -> B.4 Source Generation

The key function that bridges guided input to the existing pipeline:

```python
def render_intent_source(draft: IntentDraft) -> str:
    """Convert an IntentDraft to B.4 intent notation source text.

    This is the DETERMINISTIC bridge: structured data -> text that
    parse_intent() can parse. No LLM, no heuristics.

    Example output:
        protocol GestioneRicette:
            roles: Cuoco, Dispensa

            Cuoco asks Dispensa to do task
            Dispensa returns result to Cuoco
            when Cuoco decides:
                cucinare:
                    Cuoco sends message to Dispensa
                aggiungere:
                    Cuoco sends message to Dispensa
    """
```

**Action mapping for guided mode**: The user picks from a menu of action types in their language. Each maps to a B.4 action verb tuple:

```python
_GUIDED_ACTIONS: dict[str, dict[str, tuple[str, ...]]] = {
    "it": {
        "chiede di fare":     ("asks", "to", "do", "task"),
        "restituisce":        ("returns", "result", "to"),
        "chiede di verificare": ("asks", "to", "verify"),
        "propone":            ("proposes", "plan", "to"),
        "invia messaggio":    ("sends", "message", "to"),
        ...
    },
    "pt": { ... },
    "en": { ... },
}
```

### 6. Pipeline Integration (flow)

```
User types description
    |
    v
[ChatSession._handle_describe()]
    | Extracts protocol name, initial role guesses
    v
[ChatSession._handle_roles()]
    | User confirms/edits roles (min 2)
    v
[ChatSession._handle_messages()]
    | User builds message sequence step by step
    | System offers action menu in user's language
    v
[ChatSession._handle_choices()]
    | Optional: "Does any role make decisions?" yes/no
    | If yes: user defines branches
    v
[ChatSession._handle_properties()]
    | System suggests defaults (always_terminates, no_deadlock)
    | User can add: ordering, exclusion, confidence, trust
    v
[ChatSession._handle_confirm()]
    | System calls render_intent_source(draft) -> source text
    | Shows formatted protocol box to user
    | User says yes/no
    v
[render_intent_source(draft)] -> source: str
    |
    v
[intent.parse_intent(source)] -> IntentParseResult  (EXISTING B.4)
    |
    v
[spec.check_properties(protocol, spec)] -> PropertyReport  (EXISTING B.5)
    |
    v
[codegen.generate_python(protocol)] -> code: str  (EXISTING B.3)
    |
    v
[Simulation via checker.SessionChecker]  (EXISTING A.3)
    | System creates a SessionChecker, runs a sample scenario
    | Shows step-by-step narrative in user's language
    v
ChatResult (frozen, returned)
```

### 7. CLI Integration

Add `lu chat` subcommand to `_cli.py`:

```python
# In _build_parser():
p_chat = subparsers.add_parser(
    "chat",
    help="Interactive guided protocol builder",
)
p_chat.add_argument(
    "--lang",
    choices=["it", "pt", "en"],
    default="en",
    help="Interface language (default: en)",
)
p_chat.add_argument(
    "-o", "--output",
    help="Save generated Python to file",
)
```

Handler:
```python
def _cmd_chat(args: argparse.Namespace) -> int:
    from ._intent_bridge import ChatSession
    session = ChatSession(lang=args.lang)
    result = session.run()
    if result and args.output:
        Path(args.output).write_text(result.generated_code, encoding="utf-8")
    return 0
```

### 8. Internationalization (i18n) Strategy

All user-facing strings in a single `_STRINGS` dict inside `_intent_bridge.py`:

```python
_STRINGS: MappingProxyType = MappingProxyType({
    "welcome": MappingProxyType({
        "en": (
            'Lingua Universale - Interactive Chat\n'
            '"Tell me what you want to create and I\'ll build it, with proof it works."\n\n'
            'Languages: italiano | portugues | english\n'
            'Type "help" for help. "exit" to quit.'
        ),
        "it": (
            'Lingua Universale - Chat Interattiva\n'
            '"Dimmi cosa vuoi creare e io lo costruisco, con la prova che funziona."\n\n'
            'Lingue: italiano | portugues | english\n'
            'Digita "aiuto" per la guida. "esci" per uscire.'
        ),
        "pt": (
            'Lingua Universale - Chat Interativo\n'
            '"Diga-me o que voce quer criar e eu construo, com a prova que funciona."\n\n'
            'Idiomas: italiano | portugues | english\n'
            'Digite "ajuda" para ajuda. "sair" para sair.'
        ),
    }),
    "ask_describe": MappingProxyType({ ... }),
    "ask_roles": MappingProxyType({ ... }),
    "ask_messages": MappingProxyType({ ... }),
    "verify_progress": MappingProxyType({ ... }),
    "all_proved": MappingProxyType({ ... }),
    "code_ready": MappingProxyType({ ... }),
    "sim_success": MappingProxyType({ ... }),
    "sim_violation": MappingProxyType({ ... }),
    # ... ~25-30 string keys total
})
```

**Helper:**
```python
def _t(key: str, lang: str, **kwargs: str) -> str:
    """Translate a string key to the given language."""
    entry = _STRINGS.get(key, {})
    template = entry.get(lang, entry.get("en", key))
    return template.format_map(_SafeDict(kwargs))
```

This reuses the exact `_SafeDict` pattern from `errors.py`.

### 9. E.3 NL Mode Extension Point (design now, implement later)

The `ChatSession` constructor accepts an optional `nl_processor`:

```python
class ChatSession:
    def __init__(
        self,
        *,
        lang: str = "en",
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[..., None] | None = None,
        nl_processor: NLProcessor | None = None,  # E.3: optional LLM layer
    ) -> None: ...
```

Where `NLProcessor` is a Protocol (typing.Protocol, not our Protocol):

```python
class NLProcessor(typing.Protocol):
    """Interface for NL -> IntentDraft conversion (E.3).

    Implementations may use Claude, GPT, or any LLM.
    The guided mode is the fallback when nl_processor is None.
    """
    def process(self, text: str, lang: str, context: list[Turn]) -> IntentDraft: ...
```

When `nl_processor is not None`, the DESCRIBE phase sends user text to the LLM instead of asking structured questions. Everything after IntentDraft is the same pipeline.

This means E.3 is a **single new file** `_nl_processor.py` with `anthropic` as optional dep, and a one-line change in `ChatSession.__init__`.

### 10. Critical Files

| File | Action | Risk |
|------|--------|------|
| `_intent_bridge.py` | **CREATE** (~450 lines) | Low (new, no breaking) |
| `_cli.py` | MODIFY (add `chat` subcommand, ~30 lines) | Low (additive) |
| `__init__.py` | MODIFY (re-export new public API, ~10 lines) | Low (additive) |
| `tests/test_intent_bridge_core.py` | **CREATE** (~200 lines) | None |
| `tests/test_intent_bridge_cli.py` | **CREATE** (~100 lines) | None |

**Files NOT modified:**
- `intent.py` -- used as-is
- `spec.py` -- used as-is
- `codegen.py` -- used as-is
- `checker.py` -- used as-is
- `protocols.py` -- used as-is
- `errors.py` -- used as-is (i18n pattern copied, not extended)

### 11. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| B.4 `_ACTION_MAP` does not cover all user scenarios | Medium | Medium | Map guided actions to existing ACTION_MAP keys only. Document which MessageKind values are available. Users can always edit the generated source. |
| Role names with spaces/special chars | Low | Low | Validate role names with `_WORD_RE` from intent.py (already enforces `[A-Za-z_][A-Za-z0-9_]*`). Show clear error if invalid. |
| Guided mode feels too rigid (too many questions) | Medium | Medium | Design phases to be skippable. Default properties auto-applied. Minimum viable: 3-4 turns (describe -> roles -> messages -> confirm). |
| `render_intent_source()` generates invalid B.4 syntax | High | Low | Unit test every code path. Round-trip test: render -> parse_intent -> compare protocol. |
| i18n strings bloat the module | Low | Low | ~30 keys x 3 locales x ~50 chars = ~4.5KB. Acceptable for MVP. |
| ChatSession state machine complexity | Medium | Low | Linear phase transitions. Only CONFIRM has a backward edge (-> ROLES for re-editing). State machine is simple by design. |

---

## Phase 3: Review

### Assumptions
- [x] B.4 `parse_intent()` handles arbitrary role names (confirmed: uses `_WORD_RE = [A-Za-z_][A-Za-z0-9_]*`)
- [x] B.5 `check_properties()` works with any Protocol object (confirmed: takes Protocol + ProtocolSpec, no CervellaSwarm-specific coupling)
- [x] B.3 `generate_python()` works with user-defined protocols (confirmed: generates from any Protocol)
- [x] Existing tests pass without modification (new module is additive only)
- [x] `_ACTION_MAP` in intent.py covers enough message types for general-purpose protocols (14 action verbs available)
- [x] CLI `_build_parser()` supports adding new subcommands (confirmed: uses `subparsers.add_parser()`)

### Design Decisions (for Rafa's approval)

1. **Guided mode uses menus, not free text.** In E.2, the user picks from numbered options (action types, property types). This is deterministic and needs no LLM. E.3 adds free text via `NLProcessor`.

2. **IntentDraft is a NEW dataclass, not a Protocol.** It's the intermediate representation between the user's input and B.4 syntax. This follows the Req2LTL "two-stage" pattern that achieved 88% vs 43% accuracy.

3. **One module, not three.** `_intent_bridge.py` contains everything (data model, session, builder, i18n strings). Splitting into multiple files is premature for ~450 lines. Can be split later if it grows.

4. **Simulation uses hardcoded sample data.** The simulation in E.2 generates a sample scenario (like "Cuoco chiede ingredienti") with placeholder payloads. Full simulation with user-provided data is E.3+.

---

## Phase 4: Final Plan

### Execution Order

1. **Create `_intent_bridge.py`** - Worker: backend
   - Files: `packages/lingua-universale/src/cervellaswarm_lingua_universale/_intent_bridge.py`
   - Content: ChatPhase enum, IntentDraft/DraftMessage/DraftChoice/Turn/ChatResult frozen dataclasses, `render_intent_source()` function, `_STRINGS` i18n dict, `_t()` helper, `_GUIDED_ACTIONS` mapping, `ChatSession` class with all `_handle_*` phase methods, `NLProcessor` typing.Protocol
   - Why first: core module, everything else depends on it

2. **Create tests for `_intent_bridge.py`** - Worker: tester
   - Files: `packages/lingua-universale/tests/test_intent_bridge_core.py`
   - Test categories:
     - Data model: frozen dataclass creation, validation
     - `render_intent_source()`: round-trip test (render -> parse_intent -> check protocol matches draft)
     - `ChatSession.process_input()`: unit test each phase with injected I/O
     - i18n: all 3 locales render without error, all string keys exist in all locales
     - Edge cases: empty roles, single message, no choices, all properties
   - Why second: validate core before CLI integration

3. **Modify `_cli.py`** - Worker: backend
   - Files: `packages/lingua-universale/src/cervellaswarm_lingua_universale/_cli.py`
   - Changes: add `chat` subparser with `--lang` and `-o` args, add `_cmd_chat` handler, add to `_COMMAND_HANDLERS`
   - Why third: depends on #1

4. **Create CLI tests** - Worker: tester
   - Files: `packages/lingua-universale/tests/test_intent_bridge_cli.py`
   - Test: `lu chat --help` works, `_cmd_chat` with injected I/O produces result
   - Why fourth: depends on #3

5. **Modify `__init__.py`** - Worker: backend
   - Files: `packages/lingua-universale/src/cervellaswarm_lingua_universale/__init__.py`
   - Changes: import and re-export `ChatSession`, `ChatResult`, `IntentDraft`, `ChatPhase`, `render_intent_source` from `._intent_bridge`
   - Why last: public API, only after everything works

### Success Criteria
- [ ] `render_intent_source()` round-trip: IntentDraft -> source -> `parse_intent(source)` -> Protocol matches draft (roles, elements count, message kinds)
- [ ] `ChatSession` with injected I/O completes full guided flow (WELCOME -> DONE) producing a valid `ChatResult`
- [ ] `ChatResult.property_report.all_passed == True` for a well-formed protocol
- [ ] `lu chat --lang it --help` works
- [ ] All 3 locales (en/it/pt): every `_STRINGS` key has a translation, no KeyError
- [ ] Zero new external dependencies
- [ ] All existing 2909 LU tests still pass
- [ ] New test count: ~80-120 tests across 2 test files
- [ ] Guardiana audit: >= 9.0/10

### Estimated Worker Effort
- Backend worker: 1.5 sessions (1 for core module + CLI, 0.5 for polish)
- Tester worker: 0.5 sessions (tests are straightforward with injected I/O)
- Guardiana: 0.5 sessions (audit)
- **Total: ~2-3 sessions for E.2 complete**

---
**Status**: WAITING_APPROVAL
