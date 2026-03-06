# Plan: C1.3.1 - Tokenizer Unificato per Lingua Universale v0.2

## Metadata
- **Task ID**: C1.3.1
- **Architect**: cervella-architect
- **Created**: 2026-02-26
- **Complexity**: Medium-High
- **Files Affected**: 2 (1 src + 1 test)
- **Risk Score**: 0.35
- **Dependencies**: EBNF grammar v0.2 (DESIGN_C1_2_SYNTAX_GRAMMAR.md)

---

## Phase 1: Understanding

### User Request

Creare un tokenizer unificato (`_tokenizer.py`) che sostituisca i due tokenizer duplicati in `intent.py` e `spec.py`, e che supporti tutti i token richiesti dalla grammatica EBNF v0.2 con 62 produzioni. Deve emettere INDENT/DEDENT espliciti con indent stack (come CPython), supportare paren depth tracking, e servire come fondamento per il parser unificato C1.3.

### Codebase Analysis

**File sorgente analizzati:**

| File | Path | LOC Tokenizer | Token Supportati |
|------|------|---------------|------------------|
| `intent.py` | `.../cervellaswarm_lingua_universale/intent.py` | ~70 (righe 140-228) | WORD, COLON, COMMA, NEWLINE, INDENT, EOF |
| `spec.py` | `.../cervellaswarm_lingua_universale/spec.py` | ~70 (righe 246-334) | WORD, COLON, GTE, NEWLINE, INDENT, EOF |

**Duplicazione misurata:** ~105 LOC identiche tra i due file (tokenizer base ~65 LOC + parser utility ~40 LOC).

**Pattern attuale (identico in entrambi):**
1. `textwrap.dedent(source)` all'inizio
2. Line-by-line processing con `source.split("\n")`
3. Tab rejection con errore esplicito
4. 4-space indent counting: `leading // 4` -> N token INDENT emessi per riga
5. Comment `#` e blank line skipping
6. Content tokenization con regex `[A-Za-z_][A-Za-z0-9_]*` per WORD
7. NEWLINE alla fine di ogni riga non vuota
8. EOF alla fine

**Limite critico del pattern attuale:** Non emette DEDENT. I parser compensano con `_peek_indent_level()` e `_count_indents()` per confrontare livelli manualmente. Funziona per 2 livelli di nesting ma non scala a 4+ livelli della grammatica v0.2.

### Constraints

1. **0 dipendenze esterne** -- solo Python stdlib (`re`, `textwrap`, `dataclasses`, `enum`)
2. **Backward compatibility** -- `intent.py` e `spec.py` continuano a funzionare con i LORO tokenizer interni. Il nuovo `_tokenizer.py` serve il NUOVO parser unificato. Nessun refactor dei file esistenti in questo step.
3. **Leading underscore** -- il file si chiama `_tokenizer.py` (privato al package). La public API sara `tokenize()` ma esportata solo dal futuro `parser.py`.
4. **Indent unit: 4 spazi** -- coerente con tutto il codebase esistente.
5. **Python >= 3.10** -- target del package (da `pyproject.toml`).

---

## Phase 2: Design

### Approach

1. **Un singolo file `_tokenizer.py`** con TokKind enum, Tok dataclass, e funzione `tokenize()`.
2. **Indent stack pattern da CPython** -- stack `[0]`, emette INDENT quando `col > stack[-1]`, emette DEDENT (anche multipli) quando `col < stack[-1]`, errore se dedent non allinea.
3. **Paren depth counter** -- dentro `()` e `[]` sopprime INDENT/DEDENT e NEWLINE (come Python e Lark).
4. **Keywords come IDENT** -- il tokenizer NON distingue keyword da identificatori. Il parser fara il dispatching. Motivazione sotto.
5. **Tok con (line, col)** -- per error messages precisi.
6. **Multi-char operators scan prima dei single-char** -- `>=` prima di `>`.

### Design Decisions

#### D1: Keywords come IDENT (non come token separati)

**Decisione:** Il tokenizer emette IDENT per tutte le parole (`protocol`, `agent`, `roles`, `when`, ecc.). Il parser confronta `tok.value` per distinguere keyword da nomi utente.

**PERCHE:**
- **La grammatica lo permette:** Tutte le keyword sono riconoscibili dal contesto sintattico. `protocol` appare solo all'inizio di `protocol_decl`, `roles` appare solo come prima parola dopo INDENT in `protocol_body`, ecc. Non c'e mai ambiguita.
- **Semplicita:** Un enum TokKind con 20+ valori (uno per keyword) rende il tokenizer complesso e fragile. Aggiungere una keyword futura richiederebbe modificare TokKind.
- **Precedente nel codebase:** intent.py usa WORD per tutto (anche per "protocol", "roles", "when", "asks", ecc.) e funziona perfettamente. spec.py idem.
- **Precedente nell'industria:** CPython, Go, e Rust usano tutti lookup post-tokenizzazione. Solo FORTRAN e COBOL avevano keyword come token separati.
- **Soft keywords:** In futuro `protocol` e `agent` potrebbero essere usati come nomi di variabile in contesti non-ambigui. Con IDENT sono gia pronti.

**Alternativa scartata:** Token separati per ogni keyword (KW_PROTOCOL, KW_AGENT, KW_ROLES, ...). Scartata perche aggiunge ~25 valori all'enum, rende il tokenizer un classificatore sintattico (non il suo ruolo), e non offre vantaggi per un parser recursive descent dove il dispatching e gia esplicito.

#### D2: Indent stack con colonne assolute (non livelli)

**Decisione:** Lo stack memorizza il numero di spazi (0, 4, 8, 12, ...), non il livello logico (0, 1, 2, 3).

**PERCHE:**
- **Pattern CPython:** CPython tokenize.py usa colonne assolute. E' il pattern piu testato al mondo per indent-based languages.
- **Flessibilita futura:** Se in v0.3 supportiamo 2-space indent (come YAML), lo stack funziona senza modifiche. Con livelli, servirebbe un moltiplicatore.
- **Error messages migliori:** "expected 8 spaces, got 6" e piu informativo di "expected indent level 2".

**Alternativa scartata:** Livelli logici (come fa intent.py attuale con `indent_level = leading // 4`). Scartata perche CPython e Lark usano colonne e il pattern e piu robusto.

#### D3: NEWLINE soppresso dentro parentesi

**Decisione:** Quando `paren_depth > 0`, non si emettono NEWLINE, INDENT, o DEDENT. Le righe dentro parentesi sono "continuazioni logiche".

**PERCHE:**
- **Grammatica v0.2:** `args ::= expr (',' expr)*` implica che gli argomenti possono stare su piu righe: `tests.pass(\n  80,\n  90\n)`. Senza soppressione NEWLINE, il parser vedrebbe NEWLINE dove non li aspetta.
- **Pattern Python:** Python fa esattamente questo. Dentro `()`, `[]`, `{}` non servono backslash per continuare.
- **Pattern Lark:** Lark indenter.py ha `paren_level` counter per lo stesso motivo.

#### D4: Blank lines producono zero token (non NEWLINE)

**Decisione:** Le righe vuote e le righe solo-commento non producono alcun token.

**PERCHE:**
- **Pattern attuale:** Sia intent.py che spec.py saltano blank lines (`if not stripped: continue`). Il parser non le vede mai.
- **Coerenza:** NEWLINE e un separatore di statement. Una blank line non separa nulla -- e solo whitespace visivo.
- **Fix F4 Guardiana:** Il report di design menziona il "double NEWLINE" bug. La soluzione corretta e non emettere NEWLINE per blank lines, cosi il parser non deve mai gestire NEWLINE consecutivi.

#### D5: String literals senza escape sequences (v0.2)

**Decisione:** Le stringhe supportano single e double quote ma NON escape sequences (`\"`, `\\`, ecc.) in v0.2.

**PERCHE:**
- **Uso attuale nella grammatica:** Le uniche stringhe negli esempi canonici sono: `"2.0"`, `"dataframe"`. Nessuna contiene virgolette interne o escape.
- **YAGNI:** Aggiungere escape sequences complica il tokenizer (~20 LOC) senza use case concreto.
- **Estensione futura:** In v0.3 si puo aggiungere escape handling senza breaking changes (e' puramente additivo).

#### D6: Number literals: int e float, no negative, no scientific

**Decisione:** Il tokenizer riconosce `[0-9]+(\.[0-9]+)?`. Nessun supporto per numeri negativi nel tokenizer (il parser puo gestirli come unary minus), ne per notazione scientifica.

**PERCHE:**
- **Uso attuale:** `tests.pass(80)`, `coverage >= 70`, `pd.version >= "2.0"`. Tutti interi o float semplici.
- **Coerenza:** Python stesso non ha "negative number literals" -- `-5` e unary minus applicato a `5`.

#### D7: Errore TokenizeError separato da ParseError

**Decisione:** Il tokenizer alza `TokenizeError` (sottoclasse di `Exception`), NON il `ParseError` generico che sara usato dal parser.

**PERCHE:**
- **Fase diversa:** Un errore nel tokenizer ("carattere inatteso", "tab non permessi", "stringa non chiusa") e qualitativamente diverso da un errore nel parser ("expected 'roles:', found 'asks'"). Il chiamante potrebbe volerli distinguere.
- **Pattern esistente:** intent.py ha `IntentParseError`, spec.py ha `SpecParseError`. Il nuovo sistema avra `TokenizeError` per la fase di tokenizzazione.
- **Compatibilita futura:** In C1.3.2+ il `ParseError` estendera errors.py con codici di errore (LU-T per tokenizer, LU-P per parser). Avere classi separate facilita questo.

### Critical Files

| File | Path Assoluto | Modifica | Rischio |
|------|---------------|----------|---------|
| `_tokenizer.py` (NUOVO) | `/Users/rafapra/Developer/CervellaSwarm/packages/lingua-universale/src/cervellaswarm_lingua_universale/_tokenizer.py` | Creare da zero | Low -- file nuovo, zero impatto su esistente |
| `test_tokenizer.py` (NUOVO) | `/Users/rafapra/Developer/CervellaSwarm/packages/lingua-universale/tests/test_tokenizer.py` | Creare da zero | Low -- file nuovo |

**File NON toccati (backward compat):**
- `intent.py` -- mantiene il suo tokenizer inline `_tokenize_intent()`
- `spec.py` -- mantiene il suo tokenizer inline `_tokenize_spec()`
- `__init__.py` -- nessuna nuova export (il tokenizer e privato)

### Risks

| Rischio | Probabilita | Mitigazione |
|---------|-------------|-------------|
| INDENT/DEDENT generati in modo errato per nesting profondo (3+ livelli) | Bassa | Test espliciti con 4 livelli (Esempio 10 canonico ha 3 livelli: protocol > choice > branch) |
| Paren depth non bilanciato causa token stream corrotto | Bassa | Test con parentesi sbilanciate. Il tokenizer segnala errore su `paren_depth < 0` come carattere inatteso `)` |
| Regressione su source con `textwrap.dedent` (triple-quoted strings) | Media | Copiare i test da intent.py che usano triple-quoted strings con base indentation |
| Confusione con `=` (EQUALS) vs `==` (EQ) | Bassa | Multi-char scan PRIMA di single-char. Test esplicito `a == b` e `type X = ...` |

---

## Phase 3: Review

### Assumptions

- [x] Il tokenizer non deve riconoscere keyword -- confermato dal pattern intent.py/spec.py
- [x] 4 spazi per livello di indentazione -- confermato da tutti i file del codebase
- [x] Tab rifiutati con errore -- confermato da intent.py riga 173 e spec.py riga 279
- [x] `textwrap.dedent` applicato prima di tokenizzare -- confermato da intent.py riga 169
- [x] Commenti `#` trattati come blank lines -- confermato da intent.py riga 180
- [x] Il file `_tokenizer.py` con underscore e' la convenzione per moduli privati -- confermato dal pattern Python standard

### Questions

Nessuna domanda per l'utente. Tutte le decisioni sono motivate dal codebase esistente e dai report di ricerca.

---

## Phase 4: Final Plan

### Architettura del File `_tokenizer.py`

```
_tokenizer.py (~180-200 LOC)
|
+-- class TokKind(Enum)          # ~25 LOC - tutti i token kinds
+-- @dataclass class Tok          # ~8 LOC - frozen, con kind/value/line/col
+-- class TokenizeError           # ~12 LOC - errore con line/col
+-- def tokenize(source) -> list  # ~130-150 LOC - la funzione principale
     |
     +-- textwrap.dedent
     +-- line-by-line loop
     |    +-- tab check
     |    +-- blank/comment skip
     |    +-- indent measurement
     |    +-- indent stack logic (INDENT/DEDENT)
     |    +-- content tokenization
     |    |    +-- multi-char operators (>=, <=, ==, !=)
     |    |    +-- single-char symbols (:, ,, ., ?, |, [, ], (, ), =, >, <)
     |    |    +-- paren depth tracking
     |    |    +-- string literals
     |    |    +-- number literals
     |    |    +-- identifiers (regex)
     |    |    +-- inline comments
     |    +-- NEWLINE emission (se paren_depth == 0)
     +-- final DEDENT emission
     +-- EOF emission
```

### TokKind Enum (completo)

```python
class TokKind(Enum):
    # --- Strutturali ---
    INDENT   = auto()   # Aumento indentazione (1 token per aumento)
    DEDENT   = auto()   # Diminuzione indentazione (1 token per livello chiuso)
    NEWLINE  = auto()   # Fine riga logica
    EOF      = auto()   # Fine sorgente

    # --- Letterali ---
    IDENT    = auto()   # Identificatori e keyword (parser distingue)
    NUMBER   = auto()   # Numeri interi e float: 80, 3.14
    STRING   = auto()   # Stringhe: "hello", 'world'

    # --- Operatori di confronto (multi-char prima) ---
    GTE      = auto()   # >=
    LTE      = auto()   # <=
    EQ       = auto()   # ==
    NEQ      = auto()   # !=
    GT       = auto()   # >
    LT       = auto()   # <

    # --- Simboli singoli ---
    COLON    = auto()   # :
    COMMA    = auto()   # ,
    DOT      = auto()   # .
    QUESTION = auto()   # ?
    PIPE     = auto()   # |
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    LPAREN   = auto()   # (
    RPAREN   = auto()   # )
    EQUALS   = auto()   # =
```

**Totale: 22 token kinds** (4 strutturali + 3 letterali + 6 confronto + 9 simboli).

PERCHE questi e non altri:
- Ogni token kind corrisponde a un terminale nella grammatica EBNF v0.2.
- Non c'e ARROW (`->`) perche v0.2 non la usa (era in dsl.py).
- Non c'e LBRACE/RBRACE/SEMICOLON perche v0.2 e indent-based, non brace-based.
- Non c'e HASH (`#`) perche i commenti sono gestiti dal tokenizer, non passati al parser.

### Tok Dataclass

```python
@dataclass(frozen=True)
class Tok:
    kind: TokKind
    value: str    # Testo originale del token (es. "protocol", "80", ">=")
    line: int     # 1-indexed (riga nel sorgente)
    col: int      # 0-indexed (colonna del primo carattere)
```

PERCHE `frozen=True`: Coerente con il pattern del codebase (IntentParseResult, PropertySpec, ProtocolStep sono tutti frozen). Immutabile = sicuro per caching e set.

PERCHE `col` 0-indexed: Convenzione CPython `ast.col_offset`. Permette di puntare direttamente al carattere nella stringa sorgente con `line[col]`.

PERCHE `value` e sempre la stringa originale: Per IDENT e' il nome (`"protocol"`), per NUMBER e' la rappresentazione (`"80"`, `"3.14"`), per STRING include le virgolette (`'"hello"'`), per INDENT/DEDENT/NEWLINE/EOF e' stringa vuota `""`. Il parser interpretera i valori (es. `int(tok.value)` per numeri).

### TokenizeError

```python
class TokenizeError(Exception):
    def __init__(self, message: str, line: int = 0, col: int = 0) -> None:
        self.line = line
        self.col = col
        loc = f"line {line}, col {col}" if line else "unknown location"
        super().__init__(f"{loc}: {message}")
```

### Pseudocodice: Indent Stack (parte critica)

```python
indent_stack: list[int] = [0]   # sempre inizia con 0

for line_no, raw_line in enumerate(lines, start=1):
    stripped = raw_line.rstrip()
    if is_blank_or_comment(stripped):
        continue

    leading_spaces = len(stripped) - len(stripped.lstrip())

    # Validate: must be multiple of 4
    if leading_spaces % 4 != 0:
        raise TokenizeError(
            f"indentation must be a multiple of 4 spaces (got {leading_spaces})",
            line=line_no, col=0
        )

    # INDENT/DEDENT logic (only when paren_depth == 0)
    if paren_depth == 0:
        if leading_spaces > indent_stack[-1]:
            # Deeper: push and emit ONE INDENT
            indent_stack.append(leading_spaces)
            tokens.append(Tok(TokKind.INDENT, "", line_no, 0))

        elif leading_spaces < indent_stack[-1]:
            # Shallower: pop and emit DEDENT for EACH level closed
            while leading_spaces < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(Tok(TokKind.DEDENT, "", line_no, 0))
            # After popping, the top must match exactly
            if leading_spaces != indent_stack[-1]:
                raise TokenizeError(
                    "dedent does not match any outer indentation level",
                    line=line_no, col=0
                )
        # else: leading_spaces == indent_stack[-1] -> same level, no token

    # ... tokenize content ...
    # ... emit NEWLINE if paren_depth == 0 ...

# After all lines: close all open indentation levels
while indent_stack[-1] > 0:
    indent_stack.pop()
    tokens.append(Tok(TokKind.DEDENT, "", last_line, 0))

tokens.append(Tok(TokKind.EOF, "", last_line, 0))
```

**Proprieta garantite dall'indent stack:**
1. Ogni INDENT ha esattamente un DEDENT corrispondente (bilanciato).
2. Il parser puo usare `_expect(TokKind.INDENT)` e `_expect(TokKind.DEDENT)` senza mai confrontare livelli manualmente.
3. Nesting multiplo: `protocol > choice > branch` produce: INDENT, INDENT, INDENT -> DEDENT, DEDENT, DEDENT.

### Pseudocodice: Paren Depth (parte critica)

```python
paren_depth: int = 0

# Dentro il loop di tokenizzazione del contenuto:
if ch in "([":
    paren_depth += 1
    tokens.append(Tok(LPAREN_or_LBRACKET, ch, line_no, col))
elif ch in ")]":
    if paren_depth > 0:
        paren_depth -= 1
    tokens.append(Tok(RPAREN_or_RBRACKET, ch, line_no, col))

# A fine riga:
if paren_depth == 0:
    tokens.append(Tok(TokKind.NEWLINE, "", line_no, end_col))
# Se paren_depth > 0: niente NEWLINE, la riga successiva e' continuazione
```

**Effetto:** Dentro `tests.pass(\n  80\n)` il tokenizer emette:
```
IDENT("tests") DOT IDENT("pass") LPAREN NUMBER("80") RPAREN
```
Senza NEWLINE ne INDENT/DEDENT tra le righe.

### Pseudocodice: Content Tokenization (parte critica)

```python
# Ordine di scan -- IMPORTANTE: multi-char prima di single-char

content = stripped.lstrip()
pos = 0
while pos < len(content):
    col = leading_spaces + pos
    ch = content[pos]

    # 1. Skip spaces
    if ch == " ":
        pos += 1; continue

    # 2. Inline comment -> stop line
    if ch == "#":
        break

    # 3. Multi-char operators (MUST be before single-char)
    two = content[pos:pos+2]
    if two in (">=", "<=", "==", "!="):
        kind = {">=": GTE, "<=": LTE, "==": EQ, "!=": NEQ}[two]
        tokens.append(Tok(kind, two, line_no, col))
        pos += 2; continue

    # 4. Single-char symbols
    if ch in SINGLE_CHAR_MAP:  # : , . ? | [ ] ( ) = > <
        tokens.append(Tok(SINGLE_CHAR_MAP[ch], ch, line_no, col))
        # Track parens
        if ch in "([": paren_depth += 1
        elif ch in ")]": paren_depth = max(0, paren_depth - 1)
        pos += 1; continue

    # 5. String literal
    if ch in ('"', "'"):
        end = content.find(ch, pos + 1)
        if end == -1:
            raise TokenizeError("unterminated string literal", line_no, col)
        value = content[pos:end+1]  # includes quotes
        tokens.append(Tok(TokKind.STRING, value, line_no, col))
        pos = end + 1; continue

    # 6. Number literal
    if ch.isdigit():
        m = _NUMBER_RE.match(content, pos)  # r"\d+(\.\d+)?"
        tokens.append(Tok(TokKind.NUMBER, m.group(), line_no, col))
        pos = m.end(); continue

    # 7. Identifier (word)
    m = _IDENT_RE.match(content, pos)  # r"[A-Za-z_][A-Za-z0-9_]*"
    if m:
        tokens.append(Tok(TokKind.IDENT, m.group(), line_no, col))
        pos = m.end(); continue

    # 8. Unknown character
    raise TokenizeError(f"unexpected character: {ch!r}", line_no, col)
```

### API Pubblica

```python
def tokenize(source: str) -> list[Tok]:
    """Tokenize Lingua Universale source into a flat token list.

    Indent-aware: emits explicit INDENT and DEDENT tokens using an
    indent stack (CPython pattern). Inside () and [], INDENT/DEDENT
    and NEWLINE are suppressed.

    The source is textwrap.dedent()-ed first, so triple-quoted strings
    with arbitrary base indentation work naturally.

    Args:
        source: The source text to tokenize.

    Returns:
        A list of Tok objects, always ending with EOF.
        Every INDENT has a matching DEDENT.

    Raises:
        TokenizeError: On lexical errors (tabs, bad indent, unterminated
            string, unexpected character).
    """
```

### Execution Order

| Step | Azione | Files | Worker | Perche quest'ordine |
|------|--------|-------|--------|---------------------|
| 1 | Creare `_tokenizer.py` con TokKind, Tok, TokenizeError | `_tokenizer.py` | backend | Fondamento: tutto il resto dipende da questi tipi |
| 2 | Implementare `tokenize()` - indent stack + content scan | `_tokenizer.py` | backend | Cuore del tokenizer |
| 3 | Creare `test_tokenizer.py` - basic tokens | `test_tokenizer.py` | backend/tester | Verifica fondamentali |
| 4 | Test indent/dedent con indent stack | `test_tokenizer.py` | backend/tester | Verifica la parte piu critica |
| 5 | Test paren depth, comments, errors | `test_tokenizer.py` | backend/tester | Verifica edge cases |
| 6 | Test con i 10 esempi canonici tokenizzati | `test_tokenizer.py` | backend/tester | Accettazione vs grammar design |

### Test Strategy

#### Gruppo 1: Basic Tokens (~15 test)

```python
class TestBasicTokens:
    def test_ident_simple(self):
        # "hello" -> [IDENT("hello"), NEWLINE, EOF]
    def test_ident_with_underscore(self):
        # "my_var" -> [IDENT("my_var"), NEWLINE, EOF]
    def test_ident_with_digits(self):
        # "var123" -> [IDENT("var123"), NEWLINE, EOF]
    def test_number_integer(self):
        # "42" -> [NUMBER("42"), NEWLINE, EOF]
    def test_number_float(self):
        # "3.14" -> [NUMBER("3.14"), NEWLINE, EOF]
    def test_string_double_quote(self):
        # '"hello"' -> [STRING('"hello"'), NEWLINE, EOF]
    def test_string_single_quote(self):
        # "'world'" -> [STRING("'world'"), NEWLINE, EOF]
    def test_colon(self):
        # ":" -> [COLON, NEWLINE, EOF]
    def test_comma(self):
        # "a, b" -> [IDENT, COMMA, IDENT, NEWLINE, EOF]
    def test_all_comparison_operators(self):
        # ">= <= == != > <" -> [GTE, LTE, EQ, NEQ, GT, LT, NEWLINE, EOF]
    def test_brackets(self):
        # "List[String]" -> [IDENT, LBRACKET, IDENT, RBRACKET, NEWLINE, EOF]
    def test_parens(self):
        # "f(x)" -> [IDENT, LPAREN, IDENT, RPAREN, NEWLINE, EOF]
    def test_pipe(self):
        # "a | b" -> [IDENT, PIPE, IDENT, NEWLINE, EOF]
    def test_question(self):
        # "String?" -> [IDENT, QUESTION, NEWLINE, EOF]
    def test_dot(self):
        # "task.done" -> [IDENT, DOT, IDENT, NEWLINE, EOF]
    def test_equals(self):
        # "type X = a" -> [IDENT, IDENT, EQUALS, IDENT, NEWLINE, EOF]
```

#### Gruppo 2: Indent/Dedent (~12 test)

```python
class TestIndentDedent:
    def test_single_indent(self):
        # "a:\n    b" -> [IDENT, COLON, NEWLINE, INDENT, IDENT, NEWLINE, DEDENT, EOF]
    def test_indent_dedent_pair(self):
        # "a:\n    b\nc" -> [..., INDENT, ..., DEDENT, IDENT, ...]
    def test_double_indent(self):
        # "a:\n    b:\n        c" -> [INDENT, ..., INDENT, ..., DEDENT, DEDENT, EOF]
    def test_triple_indent(self):
        # 3 levels deep (protocol > choice > branch)
    def test_multiple_dedent_at_once(self):
        # "a:\n    b:\n        c\nd" -> emits 2 DEDENT before IDENT("d")
    def test_same_level_no_indent_token(self):
        # "a\nb" -> no INDENT or DEDENT between them
    def test_eof_closes_all_indents(self):
        # "a:\n    b" -> DEDENT emitted before EOF
    def test_eof_closes_multiple_indents(self):
        # "a:\n    b:\n        c" -> 2 DEDENT before EOF
    def test_indent_must_be_4_spaces(self):
        # "a:\n  b" -> TokenizeError (2 spaces)
    def test_indent_6_spaces_error(self):
        # "a:\n      b" -> TokenizeError (6 spaces)
    def test_misaligned_dedent_error(self):
        # "a:\n        b:\n            c\n      d" -> TokenizeError (6 not on stack)
    def test_tab_rejected(self):
        # "a:\n\tb" -> TokenizeError
```

#### Gruppo 3: Paren Depth (~8 test)

```python
class TestParenDepth:
    def test_no_newline_inside_parens(self):
        # "f(\n  x\n)" -> [IDENT, LPAREN, IDENT, RPAREN, NEWLINE, EOF]
        # (no NEWLINE or INDENT between lines inside parens)
    def test_no_indent_inside_parens(self):
        # Verify no INDENT/DEDENT inside ()
    def test_no_newline_inside_brackets(self):
        # "List[\n  String\n]" -> [IDENT, LBRACKET, IDENT, RBRACKET, NEWLINE, EOF]
    def test_nested_parens(self):
        # "f(g(\n  x\n))" -> paren_depth goes 0->1->2->1->0
    def test_mixed_parens_and_brackets(self):
        # "f([a,\n  b])" -> all correct
    def test_normal_newline_after_close_paren(self):
        # NEWLINE resumes after paren closes
    def test_indent_resumes_after_close_paren(self):
        # INDENT/DEDENT tracking resumes after paren_depth returns to 0
    def test_unmatched_close_paren_is_token(self):
        # ")" still emits RPAREN even if paren_depth is 0
        # (parser handles the error, not tokenizer)
```

#### Gruppo 4: Comment and Blank Line Handling (~6 test)

```python
class TestCommentsAndBlanks:
    def test_blank_line_produces_no_tokens(self):
        # "a\n\nb" -> [IDENT, NEWLINE, IDENT, NEWLINE, EOF] (no double NEWLINE)
    def test_comment_line_skipped(self):
        # "# comment\na" -> [IDENT, NEWLINE, EOF]
    def test_inline_comment(self):
        # "a  # comment" -> [IDENT, NEWLINE, EOF]
    def test_comment_after_colon(self):
        # "roles: a, b  # lista ruoli" -> [IDENT, COLON, IDENT, COMMA, IDENT, NEWLINE, EOF]
    def test_multiple_blank_lines(self):
        # "a\n\n\n\nb" -> no double NEWLINE
    def test_comment_only_source(self):
        # "# just a comment" -> [EOF]
```

#### Gruppo 5: Error Cases (~8 test)

```python
class TestTokenizeErrors:
    def test_tab_error(self):
        # Tabs rejected with clear message
    def test_bad_indent_not_multiple_of_4(self):
        # 2 spaces, 3 spaces, 5 spaces, etc.
    def test_unterminated_string_double(self):
        # '"hello' -> TokenizeError
    def test_unterminated_string_single(self):
        # "'hello" -> TokenizeError
    def test_unexpected_character(self):
        # "@" -> TokenizeError
    def test_error_has_line_info(self):
        # Verify error.line is correct
    def test_error_has_col_info(self):
        # Verify error.col points to the problem character
    def test_misaligned_dedent(self):
        # Dedent to a level not on the stack
```

#### Gruppo 6: Canonical Examples Tokenized (~10 test)

```python
class TestCanonicalExamples:
    def test_example_1_delegate_task(self):
        # Tokenize Example 1 (basic protocol with properties)
        # Verify: correct count of INDENT/DEDENT pairs
        # Verify: no WORD -- all identifiers are IDENT
    def test_example_2_plan_and_build(self):
        # Choice block: when X decides -> INDENT branches DEDENT
    def test_example_3_agent_with_contracts(self):
        # agent Worker: -> INDENT clauses with requires/ensures DEDENT
        # tests.pass(80) -> IDENT DOT IDENT LPAREN NUMBER RPAREN
    def test_example_4_type_record(self):
        # type AnalysisResult = NEWLINE INDENT fields DEDENT
        # Confident[String] -> IDENT LBRACKET IDENT RBRACKET
        # String? -> IDENT QUESTION
    def test_example_5_type_variant(self):
        # type TaskStatus = ok | fail | blocked
        # -> IDENT IDENT EQUALS IDENT PIPE IDENT PIPE IDENT NEWLINE
    def test_example_6_use_python(self):
        # use python math -> IDENT IDENT IDENT NEWLINE
        # use python datetime as dt -> IDENT IDENT IDENT IDENT IDENT NEWLINE
    def test_example_7_trust_properties(self):
        # trust >= trusted -> IDENT GTE IDENT
    def test_example_8_recipe_app(self):
        # Combined protocol + agent
    def test_example_9_deep_research(self):
        # Type + protocol together
    def test_example_10_full_program(self):
        # The big one: use + 2 types + protocol + 2 agents
        # Verify total token count is reasonable
        # Verify every INDENT has a matching DEDENT
```

#### Test Helper: INDENT/DEDENT Balance Check

```python
def assert_indent_dedent_balanced(tokens: list[Tok]) -> None:
    """Every INDENT must have a matching DEDENT."""
    depth = 0
    for tok in tokens:
        if tok.kind == TokKind.INDENT:
            depth += 1
        elif tok.kind == TokKind.DEDENT:
            depth -= 1
        assert depth >= 0, f"DEDENT without matching INDENT at line {tok.line}"
    assert depth == 0, f"Unmatched INDENT: {depth} levels still open at EOF"
```

Questo helper va usato in OGNI test dei canonical examples.

### Success Criteria

- [ ] `_tokenizer.py` creato con TokKind (22 valori), Tok (frozen dataclass), TokenizeError, `tokenize()`
- [ ] Tutti i 22 token kinds emessi correttamente per i rispettivi caratteri/pattern
- [ ] INDENT/DEDENT bilanciati per qualsiasi input valido (proprieta invariante)
- [ ] Paren depth disabilita INDENT/DEDENT/NEWLINE dentro `()` e `[]`
- [ ] Tab rifiutati con errore
- [ ] Indentazione non multipla di 4 rifiutata con errore
- [ ] Stringhe non chiuse segnalate con errore + line/col
- [ ] Commenti `#` (full-line e inline) gestiti senza produrre token
- [ ] Blank lines non producono NEWLINE
- [ ] `textwrap.dedent` applicato prima (triple-quoted strings funzionano)
- [ ] Tutti i 10 esempi canonici tokenizzano senza errori
- [ ] ~60 test passano in `test_tokenizer.py`
- [ ] 0 dipendenze esterne (solo stdlib)
- [ ] Coverage >= 95% su `_tokenizer.py`

### Estimated LOC

| Sezione | LOC Stimate |
|---------|-------------|
| TokKind enum | ~25 |
| Tok dataclass | ~8 |
| TokenizeError class | ~12 |
| `tokenize()` function | ~130-150 |
| Module docstring + imports | ~15 |
| **Totale `_tokenizer.py`** | **~190-210** |
| | |
| Test basic tokens | ~80 |
| Test indent/dedent | ~100 |
| Test paren depth | ~60 |
| Test comments/blanks | ~40 |
| Test errors | ~50 |
| Test canonical examples | ~120 |
| Test helpers | ~20 |
| **Totale `test_tokenizer.py`** | **~470-500** |

### Estimated Worker Effort

- **Backend Worker**: 1 sessione per `_tokenizer.py` + test. Il 60% del codice del tokenizer e' riuso diretto del pattern intent.py/spec.py.

---

**Status**: WAITING_APPROVAL
