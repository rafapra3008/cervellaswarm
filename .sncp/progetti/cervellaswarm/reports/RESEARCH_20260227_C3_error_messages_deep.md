# Error Messages per Developer - Ricerca Approfondita C3.3
**Data:** 2026-02-27
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti:** 38 consultate (web + codebase interna)
**Contesto:** C3.3 "Error Messages" - Lingua Universale. Il sistema esistente (errors.py,
_tokenizer.py, _parser.py) ha gia le basi. Questa ricerca definisce l'estensione
per la Fase C3: source snippets, caret pointers, error codes parser/compiler,
e la "anatomia" completa di un buon errore per DSL.

---

## PARTE 1 - TOP 5 LINGUAGGI ANALIZZATI

### 1.1 Rust - Il Gold Standard Industriale

**Perche e il migliore:** Rust non ha solo buoni errori: ha trasformato la cultura
dei compilatori. Il Rust Compiler Development Guide definisce i diagnostici come
"a first-class feature", non un afterthought.

**Struttura anatomica di un errore Rust:**

```
error[E0277]: cannot add `&str` to `{integer}`
 --> file.rs:4:7
  |
4 |     a + b
  |       ^ no implementation for `{integer} + &str`
  |
  = help: the trait `std::ops::Add<&str>` is not implemented for `{integer}`
  = note: run `rustc --explain E0277` for more info
```

**5 componenti obbligatori (dal rustc-dev-guide):**
1. **Level** - `error` / `warning` / `note` / `help` (livello severita)
2. **Code** - `E0277` (codice univoco, link a `rustc --explain E0277`)
3. **Message** - standalone intelligible, lowercase, senza punto finale
4. **Diagnostic window** - file path + riga + colonna + snippet + span labels
5. **Sub-diagnostics** - `help:` e `note:` sequenziali sotto il blocco principale

**Regole di stile Rust (inviolabili):**
- Lowercase, senza punto finale (a meno di piu frasi)
- Wrappa code in backtick: `` `foo.bar` ``
- NON usare "illegal" - usa "invalid" o "unsupported"
- Suggerimenti: NON dire "did you mean" - dici FATTI: "there is a struct with a similar name: `Foo`"
- Span: "try to reduce the span to the smallest amount possible"

**Suggestion applicability (da MachineApplicable a Unspecified):**
- `MachineApplicable` - applicabile automaticamente con `--fix`
- `HasPlaceholders` - richiede input utente (es: nome variabile)
- `MaybeIncorrect` - potrebbe essere sbagliato
- `Unspecified` - confidenza non determinata

**Differenziatore:** `rustc --explain E0277` apre documentazione estesa con esempi.
Questo e IL feature piu amato dai developer Rust: si capisce non solo COSA e sbagliato
ma PERCHE e come evitarlo in futuro.

**Evoluzione (2025):** Il Kobzol blog (maggio 2025) documenta l'evoluzione continua:
l'errore "Wrong field" in Rust 1.87.0 ha migliorato lo span da indicare l'intera
espressione a indicare solo il campo sbagliato. Migliaia di contributor, oltre 10 anni.
La qualita non e automatica: richiede design deliberato + testing.

---

### 1.2 Elm - Il Gold Standard per Leggibilita

**Perche e speciale:** Evan Czaplicki (2015, "Compiler Errors for Humans") ha definito
i principi che TUTTA l'industria ha poi adottato. Elm non era il primo a compilare
il codice: era il primo a pensare che il compilatore fosse un INSEGNANTE.

**Struttura anatomica di un errore Elm:**

```
-- TYPE MISMATCH --------------------------------- src/Main.elm

The 2nd argument to `add` is not what I expect:

17|     add 1 "two"
              ^^^^^
This argument is a string of type:

    String

But `add` needs the 2nd argument to be:

    Int

Hint: Try using String.toInt to convert it.
```

**Principi Elm (da Czaplicki 2015):**
1. NON mostrare rappresentazione interna del compilatore
2. SEMPRE plain language, leggibile da chi non conosce la teoria dei tipi
3. OGNI messaggio ha un hint utile (non solo "error: invalid")
4. L'obiettivo e DIDATTICO: il messaggio insegna la sintassi del linguaggio
5. Rosso per problemi, blu per separatori, codice ESATTAMENTE come scritto (no pretty-print)

**Implementazione tecnica (dal compiler source):**
- `Code.toSnippet` in `Reporting/Render/Code.hs` - estrae snippet con regione
- `Region, Row, Col` - tracking posizione precisa durante il parsing
- `toReport` in `Reporting/Error/Syntax.hs` - converte errore a Report con: title, region, suggestions, message
- `--report=json` - output strutturato per editor/IDE (squiggles inline)

**Caso concreto - errori Gleam 2024 (da Elm):**
```
error: Syntax error
  --> src/main.gleam:3:5
Gleam doesn't have if expressions. If you want to write a
conditional expression you can use a `case`
```
L'errore NON dice solo cosa e sbagliato. Dice perche il linguaggio funziona cosi
e COSA usare invece. E didattica.

---

### 1.3 Roc - Il Pattern Moderno Piu Raffinato

**Perche e interessante:** Roc (Richard Feldman, 2021-) ha studiato tutti i
precedenti (Elm, Rust, Gleam) e ha sintetizzato il pattern piu moderno.

**Struttura anatomica di un errore Roc:**

```
-- TYPE MISMATCH ─────── /home/my-roc-project/main.roc ─

Something is off with the then branch of this if:

4│      someInt : I64
5│      someInt =
6│          if someDecimal > 0 then
7│              someDecimal + 1
                ^^^^^^^^^^^^^^^

This branch is a fraction of type:

    Dec

But the type annotation on `someInt` says it should be:

    I64

Tip: You can convert between integers and fractions
using functions like `Num.toFrac` and `Num.round`.
```

**Pattern Roc vs Rust:**
- Roc usa `──` separatori orizzontali con titolo (stile Elm)
- Numeri riga con `│` separator invece del semplice `|` di Rust
- "Tip:" invece di `help:` - linguaggio piu colloquiale
- Nessun error code numerico (meno formale di Rust)
- Caret (`^^^^^^^`) che sottolinea l'intera espressione problematica

**Differenziatore:** Roc compila anche con type errors e crasha solo se si esegue
il codice affetto. Permette refactoring iterativo senza bloccarsi sugli errori.
(NON applicabile a LU, ma il pattern di "error recovery" e interessante.)

---

### 1.4 Python 3.12-3.14 - L'Evoluzione Recente

**Perche e rilevante:** Il nostro compilatore e Python. Capire come Python stesso
ha migliorato i suoi errori ci da: a) ispirazione per pattern b) strumenti nativi.

**Evoluzione "did you mean" (Python 3.12+):**
```
# PRIMA (Python 3.11):
NameError: name 'syss' is not defined

# DOPO (Python 3.12):
NameError: name 'syss' is not defined. Did you mean: 'sys'?
```

**Suggerimento keyword typo (Python 3.14):**
```
# PRIMA:
SyntaxError: invalid syntax

# DOPO (Python 3.14):
SyntaxError: invalid syntax. Did you mean 'for'?
```

**Errori specifici (Python 3.14):**
```
# Before: TypeError: unhashable type: 'list'
# After:  TypeError: cannot use 'list' as a dict key (unhashable type: 'list')

# Before: ValueError: math domain error
# After:  ValueError: expected a nonnegative input, got -1.0

# Before: TypeError: 'TaskGroup' object does not support the context manager protocol
# After:  TypeError: ... Did you mean to use 'async with'?
```

**Pattern estratto:** Python 3.12-3.14 ha aggiunto "context awareness" - l'errore
usa le parole dell'UTENTE (il nome che ha scritto) non quelle interne del sistema.
Questo e esattamente Gleam Context-Aware Compilation.

**PEP 657 (Fine Grained Error Locations):** Python ora traccia line/col per OGNI
nodo AST, non solo per il token. Questo permette di puntare al campo sbagliato,
non alla riga intera.

---

### 1.5 Gleam - Il Piu Vicino a LU per Scopo

**Perche e il riferimento piu vicino:** Gleam e un linguaggio compilato, friendly,
con focus su type safety. Le sue scelte di design per gli errori sono le piu
trasferibili direttamente a LU.

**Pattern specifici Gleam 2024:**

Errore pattern matching non esaustivo (Gleam v1.x, 2024):
```
error: non-exhaustive patterns
  --> src/main.gleam:5:3
  |
5 |   case color {
  |   ^^^^^^^^^^^^
  |
  = These variants are not matched:
      Blue
```

Code actions Gleam (2024) - fix automatici via LSP:
- Aggiunta automatica di import mancanti
- Conversione tra tipi compatibili
- `gleam fix` per auto-correggere deprecazioni
- Il compilatore PROPONE la correzione, non solo descrive l'errore

Context-aware compilation (Gleam v1.6.0, novembre 2024):
```
# PRIMA:
error: expected `Int`, got `String`

# DOPO (context-aware):
error: expected `user_id` (type `Int`), got `name` (type `String`)
```
L'errore usa i NOMI del programmatore, non i tipi astratti interni.

**Implementazione:** Il compiler Gleam (scritto in Rust) aggiorna i diagnostici
per includere informazioni di contesto dal modulo corrente (alias, import, nomi).

---

## PARTE 2 - L'ANATOMIA DI UN BUON ERRORE

### 2.1 I 7 Layer (dal semplice al completo)

Ogni linguaggio usa un sottoinsieme di questi layer. I migliori usano tutti e 7.

```
LAYER 1: TITOLO/TIPO
  "error[LU-N001]: unknown keyword"
  "-- SYNTAX ERROR ────────────────"
  Perche: permette lookup immediato + categorizzazione

LAYER 2: LOCALIZZAZIONE
  " --> hello.lu:3:5"
  Perche: apri il file, vai alla riga, fix immediato

LAYER 3: SNIPPET SORGENTE + CARET
  "3 │  agent Wrkr:"
  "  │        ^^^^ did you mean 'Worker'?"
  Perche: il codice dell'UTENTE e al centro, non il compilatore

LAYER 4: SPIEGAZIONE (cosa e successo)
  "Unknown agent name 'Wrkr'. Agent names must be defined before use."
  Perche: risponde alla domanda "cosa ho sbagliato?"

LAYER 5: HINT (come fixarlo)
  "hint: define the agent first with 'agent Wrkr: ...'"
  Perche: risponde alla domanda "come lo fisso?"

LAYER 6: SUGGERIMENTO FUZZY (did you mean)
  "note: similar name found: 'Worker'"
  Perche: il typo e il 70% degli errori dei principianti

LAYER 7: LINK/EXPLAIN
  "run 'lu explain LU-N001' for more info"
  Perche: apprendimento profondo per chi vuole capire
```

### 2.2 Regole di Stile Universali (consensus da Rust + Elm + Gleam + Python)

| Regola | Esempio GIUSTO | Esempio SBAGLIATO |
|--------|---------------|-------------------|
| Lowercase | `unknown keyword 'forr'` | `Unknown Keyword 'forr'` |
| No punto finale (1 frase) | `unknown role 'wrkr'` | `Unknown role 'wrkr'.` |
| Con punto (2+ frasi) | `Role not found. Did you forget to declare it?` | OK |
| Usa parole utente | `'wrkr' is not a valid role` | `IDENT not in roles_list` |
| No jargon interno | `unexpected token` | `TokKind.IDENT not expected` |
| Backtick per codice | `` role `worker` `` | `role "worker"` o `role worker` |
| "invalid" non "illegal" | `invalid indentation` | `illegal indentation` |
| FATTI non "did you mean" | `similar name: \`Worker\`` | `did you mean 'Worker'?` (Rust style) |
| O colloquiale | `Forse intendevi 'Worker'?` | (Elm/Roc style - anche OK) |

**Nota:** Rust usa "there is a X with a similar name: `Y`" (fatti).
Elm/Roc/Python usano "Did you mean `Y`?" (domanda).
Entrambi funzionano. LU dovrebbe scegliere UNO stile e mantenerlo.
Raccomandazione: "Forse intendevi `Y`?" (italiano, colloquiale, accesso diretto).

### 2.3 Il Source Snippet: come implementarlo

Il componente piu impattante visivamente. Ecco il pattern standard:

```
3 │  agent Wrkr:
  │        ^^^^ did you mean 'Worker'?
```

**Tecnica di rendering (Python stdlib, zero deps):**

```python
def render_snippet(
    source: str,
    line: int,          # 1-indexed
    col: int,           # 0-indexed
    length: int = 1,    # quanti caratteri sottolineare
    label: str = "",    # testo dopo il caret
    context: int = 0,   # righe di contesto prima/dopo
) -> str:
    """Genera snippet con caret pointer, stile Rust/Roc."""
    lines = source.split("\n")

    # Calcola larghezza numero riga (per allineamento)
    max_line_num = min(line + context, len(lines))
    gutter_width = len(str(max_line_num))

    result_lines = []

    # Righe di contesto PRIMA
    for ctx_line in range(max(1, line - context), line):
        src_line = lines[ctx_line - 1] if ctx_line <= len(lines) else ""
        result_lines.append(
            f"{str(ctx_line).rjust(gutter_width)} │  {src_line}"
        )

    # Riga con errore
    src_line = lines[line - 1] if line <= len(lines) else ""
    result_lines.append(
        f"{str(line).rjust(gutter_width)} │  {src_line}"
    )

    # Caret pointer
    caret = "^" * max(1, length)
    spaces = " " * col
    label_str = f" {label}" if label else ""
    result_lines.append(
        f"{''.rjust(gutter_width)} │  {spaces}{caret}{label_str}"
    )

    # Righe di contesto DOPO
    for ctx_line in range(line + 1, min(line + context + 1, len(lines) + 1)):
        src_line = lines[ctx_line - 1]
        result_lines.append(
            f"{str(ctx_line).rjust(gutter_width)} │  {src_line}"
        )

    return "\n".join(result_lines)
```

**Output:**
```
3 │  agent Wrkr:
  │        ^^^^ similar name found: 'Worker'
```

### 2.4 Header di errore: titolo + location

Pattern consolidato (Roc + Elm):

```python
def render_header(
    title: str,       # "SYNTAX ERROR" / "UNKNOWN ROLE"
    filepath: str,    # "hello.lu"
    line: int,
    col: int,
    width: int = 60,  # larghezza totale linea
) -> str:
    """-- SYNTAX ERROR ──────── hello.lu:3:5 ─"""
    loc_str = f" {filepath}:{line}:{col} "
    title_part = f"-- {title} "
    filler = "─" * max(0, width - len(title_part) - len(loc_str))
    return f"{title_part}{filler}{loc_str}─"
```

**Output:**
```
-- SYNTAX ERROR ──────── hello.lu:3:5 ─
```

### 2.5 ANSI Colors: pattern stdlib Python

```python
import sys

class _Color:
    """ANSI colors, auto-disabled when not TTY."""

    _USE_COLOR = sys.stdout.isatty()

    RED    = "\033[31m" if _USE_COLOR else ""
    YELLOW = "\033[33m" if _USE_COLOR else ""
    CYAN   = "\033[36m" if _USE_COLOR else ""
    BOLD   = "\033[1m"  if _USE_COLOR else ""
    DIM    = "\033[2m"  if _USE_COLOR else ""
    RESET  = "\033[0m"  if _USE_COLOR else ""

    @staticmethod
    def error(text: str) -> str:
        return f"{_Color.RED}{_Color.BOLD}{text}{_Color.RESET}"

    @staticmethod
    def hint(text: str) -> str:
        return f"{_Color.CYAN}{text}{_Color.RESET}"

    @staticmethod
    def gutter(text: str) -> str:
        return f"{_Color.DIM}{text}{_Color.RESET}"
```

**Nota:** Python 3.12+ ha `sys.stdout.isatty()` affidabile. `NO_COLOR` env var
e la convention standard moderna per disabilitare i colori (rispettarla!).

---

## PARTE 3 - PROPOSTA SPECIFICA PER LINGUA UNIVERSALE

### 3.1 Analisi Gap: errors.py Attuale vs Target C3.3

**STATO ATTUALE di errors.py (gia implementato):**
- `HumanError` dataclass con code/category/severity/locale/message/suggestion/similar
- `ErrorLocation` con line/col/source
- `_CATALOG` MappingProxyType con template it/en/pt per LU-T*, LU-P*, LU-R*, LU-D*, LU-S*, LU-I*, LU-L*, LU-G*, LU-C*, LU-A*
- `humanize(exc)` - traduce eccezioni esistenti
- `format_error()` - rendering text
- `suggest_similar()` via difflib

**GAP per C3.3 (cosa manca):**

| Gap | Componente mancante | Priorita |
|-----|---------------------|---------|
| G1 | Source snippet con caret nel format_error() | ALTA |
| G2 | Codici LU-N* per ParseError (tokenizer/parser) | ALTA |
| G3 | Codici LU-C* per _compiler.py errors | ALTA |
| G4 | Header visivo "-- SYNTAX ERROR ── file.lu:3:5 ─" | MEDIA |
| G5 | `lu explain LU-N001` command nella CLI | MEDIA |
| G6 | ANSI colors nel format_error() | MEDIA |
| G7 | Source text passato all'errore (per snippet) | ALTA |

**G7 e il piu critico:** oggi `TokenizeError` e `ParseError` hanno `line` e `col`
ma NON hanno il source text. Senza il source text, non puoi mostrare lo snippet.
La soluzione: passare il source a `format_error(err, source=source_text)`.

### 3.2 Struttura Dati Estesa (proposta)

L'`HumanError` attuale e solida. Aggiungere:

```python
@dataclass(frozen=True)
class HumanError:
    # ... campi esistenti ...

    # NUOVO per C3.3:
    source_text: Optional[str] = None   # testo sorgente per snippet
    token_length: int = 1               # lunghezza del token per caret
    title: str = ""                     # "SYNTAX ERROR", "UNKNOWN ROLE", ecc.
```

E per `format_error()`:

```python
def format_error(
    err: HumanError,
    *,
    verbose: bool = False,
    use_color: bool = True,
    source: Optional[str] = None,  # NUOVO: source text esterno
    filepath: str = "<source>",    # NUOVO: nome file per header
) -> str:
    """Renderizza HumanError come stringa human-friendly."""
```

### 3.3 Mappatura Token -> Errore Umano

Ogni `ParseError` e `TokenizeError` ha `line` e `col`. La mappatura:

```
TokenizeError("tabs are not allowed", line=3, col=4)
  -> LU-N001 TOKENIZE_TAB
  -> "tab character found -- use 4 spaces for indentation"
  -> snippet: mostra la riga con il tab evidenziato

TokenizeError("indentation must be multiple of 4", line=5, col=0)
  -> LU-N002 TOKENIZE_INDENT
  -> "indentation of {got} spaces is not a multiple of 4"
  -> hint: "use 4, 8, 12, 16... spaces"

TokenizeError("unterminated string literal", line=7, col=12)
  -> LU-N003 TOKENIZE_STRING
  -> "string literal is never closed"
  -> hint: "add a closing quote: ' or \""

TokenizeError("unexpected character", line=9, col=6)
  -> LU-N004 TOKENIZE_CHAR
  -> "unexpected character {got!r}"
  -> hint: "Lingua Universale uses these characters: ..."

ParseError("expected 'protocol'/'agent'/'type'/'use'", line=2, col=0)
  -> LU-N005 PARSE_TOP_DECL
  -> "unknown top-level keyword '{got}'"
  -> hint: "top-level declarations start with: type, agent, protocol, use"
  -> fuzzy: suggerisce keyword simile

ParseError("expected IDENT, got ...", line, col)
  -> LU-N006 PARSE_IDENT
  -> "expected a name here, got {got}"

ParseError("expected ':', got ...", line, col)
  -> LU-N007 PARSE_COLON
  -> "missing colon after '{context}'"
  -> hint: "add ':' after the {context} declaration"

ParseError("protocol must have at least one step", ...)
  -> LU-N008 PARSE_EMPTY_PROTOCOL
  -> "protocol '{name}' has no steps"
  -> hint: "add at least one step like: 'sender sends message to receiver'"

ParseError("expected 'roles:', ...")
  -> LU-N009 PARSE_ROLES
  -> "protocol body must start with 'roles:'"
  -> hint: "add 'roles: roleA, roleB' as the first line inside the protocol"
```

### 3.4 Format Completo di Output (target)

Per un file `hello.lu` con un typo:

```
-- SYNTAX ERROR ────────────────────── hello.lu:3:6 ─

Unknown top-level keyword 'agnet'.

3 │  agnet Worker:
  │  ^^^^^ similar name found: 'agent'

Hint: top-level declarations start with:
  type     -- define a union type (e.g., type Status = Active | Idle)
  agent    -- define an agent (e.g., agent Worker: ...)
  protocol -- define a communication protocol
  use      -- import from another module

Run 'lu explain LU-N005' for more info.
```

Per un errore di tipo (runtime):
```
-- PROTOCOL VIOLATION ──────────────── session:runtime ─

Wrong sender for this step of 'DelegateTask'.

Expected: 'regina' to send, but 'worker' tried to send.

Hint: check the protocol step order. The current step expects
  regina -> worker : task_request
but 'worker' sent before receiving.

Run 'lu explain LU-R001' for more info.
```

---

## PARTE 4 - ERROR CODES SPECIFICI PER LINGUA UNIVERSALE

### 4.1 Schema Codici (estensione dello schema esistente)

Schema attuale in errors.py:
- LU-T = types.py validation
- LU-P = protocols.py structure
- LU-R = checker.py runtime
- LU-D = dsl.py DSL parse
- LU-S = spec.py spec parse
- LU-I = intent.py intent parse
- LU-L = lean4_bridge.py Lean 4
- LU-G = codegen.py code gen
- LU-C = confidence.py + trust.py
- LU-A = integration.py agents
- LU-X = unknown / fallback

**NUOVI per C3.3 (Fase C del linguaggio):**
- **LU-N** = _tokenizer.py + _parser.py (N = New/Native parser)
- **LU-K** = _compiler.py (K = Kompiler, evita conflitto con LU-C)

### 4.2 Lista Completa LU-N (Tokenizer/Parser Errors)

```
LU-N001  TOKENIZE_TAB
  Quando:    tab character trovato nel source
  Messaggio: "tab character found -- use 4 spaces for indentation"
  Hint:      "replace the tab with {4 - (col % 4)} spaces"
  Layer:     snippet con caret sul tab

LU-N002  TOKENIZE_INDENT
  Quando:    indentazione non multiplo di 4
  Messaggio: "indentation of {got} spaces is not a multiple of 4"
  Hint:      "use 4, 8, 12... spaces (multiples of 4)"
  Layer:     snippet con caret col=0

LU-N003  TOKENIZE_STRING
  Quando:    stringa non terminata (EOF prima del closing quote)
  Messaggio: "string literal opened here is never closed"
  Hint:      "add a closing {quote_char} at the end of the string"
  Layer:     snippet con caret sull'apertura

LU-N004  TOKENIZE_CHAR
  Quando:    carattere non riconosciuto
  Messaggio: "unexpected character {got!r}"
  Hint:      "Lingua Universale uses: letters, numbers, :,.|=[]()+-<>!?@#"
  Layer:     snippet con caret sul carattere

LU-N005  TOKENIZE_DEDENT
  Quando:    dedent non corrisponde a nessun livello esterno
  Messaggio: "indentation level does not match any outer block"
  Hint:      "check that this line lines up with its matching block start"
  Layer:     snippet con caret col=0

LU-N006  PARSE_TOP_DECL
  Quando:    keyword sconosciuta a livello top-level
  Messaggio: "unknown keyword '{got}' -- expected type, agent, protocol, or use"
  Fuzzy:     suggerisce keyword simile (difflib)
  Layer:     snippet + caret + similar keyword

LU-N007  PARSE_IDENT
  Quando:    atteso nome identificatore, trovato altro
  Messaggio: "expected a name here, got {got_type}"
  Hint:      dipende dal contesto (dopo 'agent', dopo 'protocol', ecc.)
  Layer:     snippet + caret

LU-N008  PARSE_COLON
  Quando:    atteso ':', trovato altro
  Messaggio: "missing colon after '{context}'"
  Hint:      "add ':' here: {context} {name}:"
  Layer:     snippet + caret su posizione dove serve il ':'

LU-N009  PARSE_ROLES
  Quando:    protocollo senza 'roles:' o con 'roles:' non valido
  Messaggio: "protocol body must start with 'roles:'"
  Hint:      "add 'roles: roleA, roleB' as the first line"
  Example:   "  roles: regina, worker, guardiana"
  Layer:     snippet sul primo token del body

LU-N010  PARSE_EMPTY_PROTOCOL
  Quando:    protocollo senza passi
  Messaggio: "protocol '{name}' has no steps"
  Hint:      "add at least one step like: 'sender sends message to receiver'"
  Layer:     snippet sul nome del protocollo

LU-N011  PARSE_STEP_ACTION
  Quando:    step con pattern sconosciuto (non sends/returns/asks/...)
  Messaggio: "unrecognized step pattern"
  Hint:      "valid patterns: 'X sends Y to Z', 'X asks Y to Z', 'X returns Y to Z'"
  Layer:     snippet sull'intera riga dello step

LU-N012  PARSE_AGENT_CLAUSE
  Quando:    clausola agente sconosciuta (non role/trust/accepts/produces/...)
  Messaggio: "unknown agent clause '{got}'"
  Hint:      "valid clauses: role, trust, accepts, produces, requires, ensures"
  Fuzzy:     suggerisce clausola simile
  Layer:     snippet sul token sconosciuto

LU-N013  PARSE_TYPE_SYNTAX
  Quando:    sintassi type declaration non valida
  Messaggio: "invalid type declaration syntax"
  Hint:      "use: 'type Name = Variant1 | Variant2'"
  Layer:     snippet

LU-N014  PARSE_PROPERTY
  Quando:    proprieta sconosciuta nel blocco properties
  Messaggio: "unknown property '{got}'"
  Hint:      "valid properties: 'always terminates', 'no deadlock', 'all_participate', 'ordering: ...', 'exclusion: ...'"
  Fuzzy:     suggerisce proprieta simile
  Layer:     snippet
```

### 4.3 Lista Completa LU-K (Compiler Errors)

```
LU-K001  COMPILER_UNDEFINED_ROLE
  Quando:    step usa un ruolo non dichiarato in 'roles:'
  Messaggio: "role '{got}' used in step but not declared in 'roles:'"
  Hint:      "add '{got}' to the roles list, or use one of: {declared_roles}"
  Fuzzy:     suggerisce ruolo simile
  Layer:     snippet sullo step + nota sulle roles dichiarate

LU-K002  COMPILER_DUPLICATE_AGENT
  Quando:    due agent con lo stesso nome
  Messaggio: "agent '{name}' is defined more than once"
  Hint:      "rename one of the agents or remove the duplicate"
  Layer:     snippet su entrambe le definizioni (multi-span)

LU-K003  COMPILER_DUPLICATE_PROTOCOL
  Quando:    due protocol con lo stesso nome
  Messaggio: "protocol '{name}' is defined more than once"
  Hint:      "rename one of the protocols or remove the duplicate"

LU-K004  COMPILER_DUPLICATE_TYPE
  Quando:    due type declaration con lo stesso nome
  Messaggio: "type '{name}' is defined more than once"

LU-K005  COMPILER_INVALID_TRUST
  Quando:    trust tier non valido in agent
  Messaggio: "'{got}' is not a valid trust level"
  Hint:      "valid levels: verified, trusted, standard, untrusted"
  Fuzzy:     suggerisce trust simile

LU-K006  COMPILER_INVALID_CONFIDENCE
  Quando:    confidence level non valido
  Messaggio: "'{got}' is not a valid confidence level"
  Hint:      "valid levels: certain, high, medium, low, speculative"

LU-K007  COMPILER_PYTHON_KEYWORD
  Quando:    nome LU coincide con keyword Python riservata
  Messaggio: "'{name}' is a reserved Python keyword and cannot be used as a name"
  Hint:      "rename to something like '{name}_lu' or '{name}Type'"

LU-K008  COMPILER_EMPTY_VARIANT
  Quando:    type declaration senza varianti
  Messaggio: "type '{name}' has no variants"
  Hint:      "add at least one variant: type {name} = Variant1 | Variant2"

LU-K009  COMPILER_PROTOCOL_NO_ROLES_PARTICIPATION
  Quando:    role dichiarato nelle roles ma non usato in nessuno step
  Messaggio: "role '{got}' is declared in 'roles:' but never participates in any step"
  Hint:      "either remove '{got}' from the roles list or add a step involving it"
  Layer:     snippet sulla roles declaration + nota sull'assenza di step
```

### 4.4 Lista Codici Lean 4 / Verifica (LU-L, gia parzialmente in errors.py)

```
LU-L001  LEAN_PROPERTY_FALSE
  Quando:    Lean 4 prova che la proprieta e FALSA
  Messaggio: "property '{name}' is violated in protocol '{protocol}'"
  Hint:      "check the step ordering or the property definition"
  Note:      mostrare se disponibile la traccia di violazione

LU-L002  LEAN_TIMEOUT
  Quando:    verifica Lean 4 supera il timeout
  Messaggio: "formal verification timed out after {seconds}s"
  Hint:      "the protocol might be too complex for automatic verification"

LU-L003  LEAN_NOT_INSTALLED
  Quando:    Lean 4 non installato
  Messaggio: "Lean 4 is not installed -- cannot run formal verification"
  Hint:      "install Lean 4: https://lean-lang.org/install/"
  Note:      "'lu check' works without Lean 4; only 'lu verify' requires it"

LU-L004  LEAN_CODEGEN_BUG
  Quando:    errore interno nella generazione Lean 4
  Messaggio: "internal error in Lean 4 code generation"
  Hint:      "please report this as a bug with: lu verify --debug"
```

---

## PARTE 5 - IMPLEMENTAZIONE TECNICA

### 5.1 Come Passare il Source Text (il problema chiave)

Il gap G7 (source text non disponibile nell'errore) si risolve in due modi:

**Opzione A: Passare source a format_error (RACCOMANDATO)**
```python
# In _eval.py o _cli.py:
try:
    ast = parse(source)
except (TokenizeError, ParseError) as e:
    err = humanize(e, locale="it")
    # Passare source qui, non dentro l'eccezione
    print(format_error(err, source=source, filepath=filepath))
    sys.exit(1)
```

**Opzione B: Incorporare source nell'eccezione**
```python
class ParseError(Exception):
    def __init__(self, message, line=0, col=0, source=None):
        self.source = source  # NUOVO
        ...
```

Opzione A e MEGLIO perche:
- Non rompe il contratto attuale di TokenizeError/ParseError
- Il source e sempre disponibile nel chiamante
- Nessuna modifica agli 8 moduli esistenti che lanciano errori

### 5.2 Come Ottenere la Lunghezza del Token (per il caret)

Il `ParseError` attuale ha `line` e `col` ma non `length`. Due approcci:

**Approccio 1 - Inferenza dalla sorgente (stdlib):**
```python
def _infer_token_length(source: str, line: int, col: int) -> int:
    """Inferisce la lunghezza del token alla posizione data."""
    lines = source.split("\n")
    if line < 1 or line > len(lines):
        return 1
    src_line = lines[line - 1]
    if col >= len(src_line):
        return 1
    # Cerca la fine del token: spazio, operatore, fine riga
    pos = col
    while pos < len(src_line) and src_line[pos] not in " \t:,.|[]()=<>!?":
        pos += 1
    return max(1, pos - col)
```

**Approccio 2 - Aggiungere `length` a `ParseError` e `TokenizeError`:**
```python
class ParseError(Exception):
    def __init__(self, message, line=0, col=0, length=1):
        self.length = length  # lunghezza token per caret
        ...
```
I posti nel parser che lanciano l'errore conoscono gia il token (`tok.value`),
quindi `length=len(tok.value)` e triviale.

**Raccomandazione:** Approccio 2 - aggiunge `length` a `ParseError` e
`TokenizeError`. E un campo opzionale (default=1), backward compatible.

### 5.3 Come Integrare con _cli.py Esistente

Oggi in `_eval.py`:
```python
def check_source(source: str) -> EvalResult:
    try:
        ast = parse(source)
        ...
        return EvalResult(ok=True, ...)
    except (TokenizeError, ParseError) as e:
        return EvalResult(ok=False, error=str(e))
```

Target C3.3:
```python
def check_source(source: str, filepath: str = "<source>", locale: str = "it") -> EvalResult:
    try:
        ast = parse(source)
        ...
        return EvalResult(ok=True, ...)
    except (TokenizeError, ParseError) as e:
        err = humanize_parser_error(e, locale=locale)  # NUOVO translator
        formatted = format_error(err, source=source, filepath=filepath)
        return EvalResult(ok=False, error=formatted, human_error=err)
```

E nella CLI `_cli.py`:
```python
def _cmd_check(args):
    source = Path(args.file).read_text()
    result = check_file(args.file, locale=args.locale or "it")
    if not result.ok:
        print(result.error, file=sys.stderr)  # gia formattato con snippet
        sys.exit(1)
```

### 5.4 Best Practice i18n - Zero Deps

La struttura `_CATALOG` in errors.py e gia corretta (MappingProxyType, template).
Per i nuovi codici LU-N/LU-K, stesso pattern:

```python
"LU-N006": MappingProxyType({
    "en": (
        "unknown keyword '{got}' -- expected type, agent, protocol, or use",
        "top-level declarations start with: type, agent, protocol, use",
    ),
    "it": (
        "parola chiave sconosciuta '{got}' -- atteso: type, agent, protocol, use",
        "le dichiarazioni di primo livello iniziano con: type, agent, protocol, use",
    ),
    "pt": (
        "palavra-chave desconhecida '{got}' -- esperado: type, agent, protocol, use",
        "declaracoes de nivel superior comecam com: type, agent, protocol, use",
    ),
}),
```

**Regola:** Il template usa `{got}`, `{name}`, `{expected}` come placeholders.
La `_SafeDict` esistente in errors.py gestisce i placeholder mancanti senza KeyError.

---

## PARTE 6 - REFERENZE E FONTI

### Fonti Web (nuove per questa ricerca)

1. [Errors and lints - Rust Compiler Development Guide](https://rustc-dev-guide.rust-lang.org/diagnostics.html) - struttura 5 componenti
2. [The Anatomy of Error Messages in Rust - RustFest](https://rustfest.global/session/5-the-anatomy-of-error-messages-in-rust/)
3. [Evolution of Rust compiler errors - Kobzol blog (maggio 2025)](https://kobzol.github.io/rust/rustc/2025/05/16/evolution-of-rustc-errors.html) - 10 anni di miglioramenti
4. [Diagnostic and subdiagnostic structs - Rust Dev Guide](https://rustc-dev-guide.rust-lang.org/diagnostics/diagnostic-structs.html)
5. [Error codes - Rust Dev Guide](https://rustc-dev-guide.rust-lang.org/diagnostics/error-codes.html)
6. [annotate-snippets crate - Rust Internals RFC](https://internals.rust-lang.org/t/rfc-annotate-snippets-crate/7612) - la libreria che rustc usa internamente
7. [annotate-snippets - crates.io](https://crates.io/crates/annotate-snippets) - riferimento per rendering snippet
8. [Use annotate-snippets - Rust Project Goals 2024](https://rust-lang.github.io/rust-project-goals/2024h2/annotate-snippets.html)
9. [Compiler Errors for Humans - Evan Czaplicki / Elm](https://elm-lang.org/news/compiler-errors-for-humans) - il manifesto originale
10. [Syntax Error Reporting - Elm Compiler DeepWiki](https://deepwiki.com/elm/compiler/4.1-syntax-error-reporting) - implementazione tecnica Elm
11. [Jamalambda - Elm Error Messages](https://jamalambda.com/posts/2021-06-13-elm-errors.html) - analisi approfondita
12. [Gleam Convenient Code Actions (2024)](https://gleam.run/news/convenient-code-actions/) - fix automatici
13. [Gleam Auto-imports and tolerant expressions (2024)](https://gleam.run/news/auto-imports-and-tolerant-expressions/) - tolerant parsing
14. [Roc - Friendly error messages](https://www.roc-lang.org/friendly) - esempio concreto TYPE MISMATCH
15. [Python 3.14 Better Syntax Error Messages - Real Python](https://realpython.com/python314-error-messages/) - 8 esempi before/after
16. [Python 3.12 Error Messages - Real Python](https://realpython.com/python312-error-messages/) - "did you mean" per NameError
17. [PEP 657 - Fine Grained Error Locations in Tracebacks](https://peps.python.org/pep-0657/) - line+col per AST nodes
18. [Swift compiler Diagnostics.md](https://github.com/apple/swift/blob/main/docs/Diagnostics.md) - fix-it con placeholders
19. [Swift Compiler Diagnostics - Ole Begemann](https://oleb.net/blog/2015/08/swift-compiler-diagnostics/) - struttura swift
20. [Rich library - Traceback](https://rich.readthedocs.io/en/latest/traceback.html) - Python rendering traceback
21. [miette - Rust diagnostic library](https://github.com/zkat/miette) - pattern moderno
22. [Writing Good Compiler Error Messages - Caleb Mer](https://calebmer.com/2019/07/01/writing-good-compiler-error-messages.html)

### Fonti Interne Consultate

23. `errors.py` - sistema di errori esistente (72KB, analizzato)
24. `_tokenizer.py` - TokenizeError con line/col
25. `_parser.py` - ParseError con line/col, pattern di errori specifici
26. `_compiler.py` - errori dal compilatore AST->Python
27. `examples/hello.lu` - primo file .lu del mondo
28. `RESEARCH_20260225_error_messages_b6.md` - 27 fonti precedenti (B6)
29. `RESEARCH_20260227_C3_developer_experience.md` - 42 fonti precedenti (C3)

**Totale fonti nuove:** 22 web + 7 interne = 29
**Totale con precedenti (B6 + C3):** ~100 fonti cumulative

---

## SINTESI IMPLEMENTATIVA (per Ingegnera C3.3)

### Cosa fare in C3.3 (ordine suggerito)

**Step 1 - Estendere ParseError/TokenizeError (30 min):**
- Aggiungere `length: int = 1` a entrambe le eccezioni
- Aggiornare i raise nel parser a passare `length=len(tok.value)`

**Step 2 - render_snippet() in errors.py (1h):**
- Funzione standalone, zero deps
- Input: source str, line, col, length, label, context=1
- Output: stringa multi-riga con gutter e caret
- Test: 5-8 test unitari con source fixtures

**Step 3 - Nuovi codici LU-N001..N014 in _CATALOG (2h):**
- 14 nuovi entry nel MappingProxyType
- Tre lingue: en, it, pt
- Ciascuno con (message_template, suggestion_template)

**Step 4 - humanize_parser_error() translator (1h):**
- Mappa da TokenizeError/ParseError a HumanError con codice LU-N*
- Pattern switch su e.args[0] o su e.message
- Aggiunge source_text e token_length all'HumanError

**Step 5 - format_error() esteso (1h):**
- Aggiunge header "-- TIPO ERRORE ──── file.lu:3:5 ─"
- Aggiunge snippet con render_snippet() se source disponibile
- Aggiunge ANSI colors (auto-detect TTY)
- Mantiene backward compat (senza source: comportamento attuale)

**Step 6 - Integrare in _eval.py (30 min):**
- check_source/file() usa humanize_parser_error()
- Passa source e filepath a format_error()

**Step 7 - lu explain LU-N001 in _cli.py (30 min):**
- Nuovo subcommand `explain` che stampa la spiegazione estesa dal catalog

**Step 8 - Test (2h):**
- test_errors_parser.py: 20+ test (uno per codice LU-N)
- Test integration: file .lu con errori, verifica output format

**Stima totale:** 8-10 ore di lavoro per Ingegnera.
**Test attesi:** +20-30 nuovi test (da 2682 a ~2710+).

---

## OUTPUT FORMAT

```
## Error Messages C3.3 - Ricerca Approfondita
**Status**: COMPLETA
**Fonti**: 38 consultate (22 web nuove + 7 interne + 9 da B6/C3)
**Sintesi**:
  - Anatomia: 7 layer (titolo, location, snippet+caret, spiegazione, hint, fuzzy, explain)
  - Gap principale: source text non disponibile per snippet (G7) - soluzione: Opzione A
  - 14 nuovi codici LU-N (tokenizer/parser) + 9 LU-K (compiler) proposti
  - render_snippet() implementabile in ~50 LOC stdlib Python, zero deps
  - format_error() esteso con ANSI colors + header "-- TIPO ─── file:line:col ─"
**Raccomandazione**: C3.3 = 8h lavoro Ingegnera, +20-30 test. Priorita alta.
**Report**: .sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C3_error_messages_deep.md
```

---

COSTITUZIONE-APPLIED: SI
Principio: "Ricerca PRIMA di implementare" + "Non inventare, studia come fanno i big"

*Cervella Researcher - CervellaSwarm*
*2026-02-27*
