# RESEARCH: Parser Best Practices per C1.3
> **Data:** 26 Febbraio 2026
> **Ricercatrice:** Cervella Researcher
> **Scope:** Implementare `parser.py` per Lingua Universale v0.2
> **Fonti consultate:** 8 (CPython tokenize.py, Lark indenter.py, Ruff v0.4.0, Thunderseethe dev blog,
>   Python AST docs, Syrupy, inline-snapshot, Boolean World parser guide)
> **Codice esistente esaminato:** intent.py (649 LOC), spec.py (1242 LOC), grammar EBNF C1.2

---

## CONTESTO: Cosa Stiamo Costruendo

- Parser per Lingua Universale v0.2: 62 produzioni EBNF
- Indent-based (come Python), LL(1) quasi ovunque, LL(3) per `primary` e `step`
- Target: ~1200 LOC, Python puro, 0 dipendenze esterne
- Base: ~50-60% riuso da intent.py + spec.py (gia verificato)
- Output: AST -> usato da C2 (compilatore), constrained decoding export, round-trip render

---

## 1. TOKENIZER: L'Indent Stack Pattern Corretto

### Il Problema Attuale in intent.py / spec.py

Il tokenizer attuale emette N token `INDENT` per N livelli, e usa `_peek_indent_level()` /
`_count_indents()` per confrontare i livelli. Funziona, ma ha un problema fondamentale:
**non emette DEDENT**. Il parser deve invece confrontare livelli manualmente.

Questo va bene per grammatiche semplici. Per la nuova grammatica con 4 costrutti
top-level e nesting a 3+ livelli, serve l'approccio CPython/Lark: emettere DEDENT espliciti.

### Il Pattern Corretto (CPython + Lark)

La regola fondamentale documentata nel CPython tokenizer (e replicata in Lark indenter.py):

```
Stack: [0]  <- sempre inizia con 0

Per ogni nuova riga logica:
  col = indentazione misurata

  se col > stack[-1]:
    push(col)
    emit INDENT

  mentre col < stack[-1]:
    pop()
    se col != stack[-1]:  # ERROR: il dedent non allinea
      raise IndentationError
    emit DEDENT

  # se col == stack[-1]: nessun token, indentazione uguale

Fine file:
  mentre stack[-1] > 0:
    pop()
    emit DEDENT
```

### Implementazione Concreta per parser.py

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator
import re
import textwrap


class TokKind(Enum):
    # Valori strutturali
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()
    # Letterali
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    # Operatori e simboli
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    QUESTION = auto()
    PIPE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LPAREN = auto()
    RPAREN = auto()
    EQUALS = auto()
    GTE = auto()   # >=
    LTE = auto()   # <=
    EQ = auto()    # ==
    NEQ = auto()   # !=
    GT = auto()    # >
    LT = auto()    # <


@dataclass(frozen=True)
class Tok:
    """Token con posizione completa nel sorgente."""
    kind: TokKind
    value: str
    line: int       # 1-indexed
    col: int        # 0-indexed, colonna del primo carattere


def tokenize(source: str) -> list[Tok]:
    """Tokenizer indent-aware con INDENT/DEDENT espliciti.

    CHIAVE: emette sia INDENT che DEDENT (non solo INDENT come intent.py).
    Lo stack mantiene i livelli di indentazione come numeri di colonna.
    """
    source = textwrap.dedent(source)
    tokens: list[Tok] = []
    indent_stack: list[int] = [0]  # sempre inizia con 0
    paren_depth: int = 0           # disabilita INDENT/DEDENT dentro ()[]

    lines = source.split("\n")

    for line_no, raw_line in enumerate(lines, start=1):
        # Rifiuta tab (come intent.py - regola dell'esistente)
        if "\t" in raw_line:
            raise ParseError(
                "usa 4 spazi per indentare, non tab",
                line=line_no, col=0
            )

        stripped = raw_line.rstrip()

        # Riga vuota o commento: emetti NEWLINE logico se non dentro parens
        if not stripped or stripped.lstrip().startswith("#"):
            if paren_depth == 0 and tokens:
                # Non emettere NEWLINE doppio
                if tokens and tokens[-1].kind != TokKind.NEWLINE:
                    tokens.append(Tok(TokKind.NEWLINE, "\n", line_no, 0))
            continue

        # Misura indentazione
        leading = len(stripped) - len(stripped.lstrip())
        if leading % 4 != 0:
            raise ParseError(
                f"indentazione deve essere multiplo di 4 spazi (trovati {leading})",
                line=line_no, col=0
            )
        col_indent = leading  # numero di spazi (non livelli)

        # Gestisci INDENT/DEDENT solo se non dentro parentesi
        if paren_depth == 0:
            if col_indent > indent_stack[-1]:
                indent_stack.append(col_indent)
                tokens.append(Tok(TokKind.INDENT, "", line_no, 0))
            else:
                while col_indent < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(Tok(TokKind.DEDENT, "", line_no, 0))
                if col_indent != indent_stack[-1]:
                    raise ParseError(
                        "il rientro non corrisponde a nessun livello precedente",
                        line=line_no, col=0
                    )

        # Tokenizza contenuto della riga
        content = stripped.lstrip()
        pos = 0
        while pos < len(content):
            col = leading + pos  # colonna assoluta nel sorgente
            ch = content[pos]

            if ch == " ":
                pos += 1
                continue

            # Commento inline
            if ch == "#":
                break

            # Operatori multi-carattere (controlla prima di quelli singoli)
            two = content[pos:pos+2]
            if two == ">=":
                tokens.append(Tok(TokKind.GTE, ">=", line_no, col))
                pos += 2
                continue
            if two == "<=":
                tokens.append(Tok(TokKind.LTE, "<=", line_no, col))
                pos += 2
                continue
            if two == "==":
                tokens.append(Tok(TokKind.EQ, "==", line_no, col))
                pos += 2
                continue
            if two == "!=":
                tokens.append(Tok(TokKind.NEQ, "!=", line_no, col))
                pos += 2
                continue

            # Simboli singoli
            SINGLE = {
                ":": TokKind.COLON, ",": TokKind.COMMA, ".": TokKind.DOT,
                "?": TokKind.QUESTION, "|": TokKind.PIPE,
                "[": TokKind.LBRACKET, "]": TokKind.RBRACKET,
                "(": TokKind.LPAREN, ")": TokKind.RPAREN,
                "=": TokKind.EQUALS, ">": TokKind.GT, "<": TokKind.LT,
            }
            if ch in SINGLE:
                tok_kind = SINGLE[ch]
                tokens.append(Tok(tok_kind, ch, line_no, col))
                # Tracking parens per disabilitare INDENT/DEDENT
                if ch in "([":
                    paren_depth += 1
                elif ch in ")]":
                    paren_depth = max(0, paren_depth - 1)
                pos += 1
                continue

            # Stringa
            if ch in ('"', "'"):
                end = content.find(ch, pos + 1)
                if end == -1:
                    raise ParseError("stringa non chiusa", line=line_no, col=col)
                value = content[pos:end+1]
                tokens.append(Tok(TokKind.STRING, value, line_no, col))
                pos = end + 1
                continue

            # Numero
            if ch.isdigit():
                m = re.match(r"\d+(\.\d+)?", content[pos:])
                if m:
                    tokens.append(Tok(TokKind.NUMBER, m.group(), line_no, col))
                    pos += len(m.group())
                    continue

            # Identificatore o keyword
            m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", content[pos:])
            if m:
                tokens.append(Tok(TokKind.IDENT, m.group(), line_no, col))
                pos += len(m.group())
                continue

            raise ParseError(f"carattere inatteso: {ch!r}", line=line_no, col=col)

        # Fine riga logica (solo fuori da parens)
        if paren_depth == 0:
            tokens.append(Tok(TokKind.NEWLINE, "\n", line_no, leading + len(content)))

    # Fine file: emetti DEDENT per ogni livello aperto
    while indent_stack[-1] > 0:
        indent_stack.pop()
        tokens.append(Tok(TokKind.DEDENT, "", len(lines), 0))

    tokens.append(Tok(TokKind.EOF, "", len(lines), 0))
    return tokens
```

**Differenza chiave da intent.py:** Il tokenizer ora emette DEDENT espliciti.
Il parser puo usare `expect(TokKind.INDENT)` e `expect(TokKind.DEDENT)` invece
di confrontare livelli manualmente. Molto piu leggibile e corretto.

**Il tracking paren_depth:** Dentro `()` o `[]`, il INDENT/DEDENT e disabilitato.
Questo permette espressioni multi-riga nelle args: `tests.pass(80,\n  90)` sarebbe
valido (anche se la grammatica v0.2 non lo usa ancora).

---

## 2. PARSER RECURSIVE DESCENT: Struttura Pulita

### Il Pattern Base (identico a intent.py / spec.py - riusa)

```python
class Parser:
    """Recursive descent parser per Lingua Universale v0.2.

    Pattern IDENTICO a _IntentParser e _SpecParser esistenti.
    Riusa le stesse utility: _peek, _advance, _expect, _expect_word.
    """

    def __init__(self, tokens: list[Tok]) -> None:
        self._tokens = tokens
        self._pos = 0

    # --- Utility identiche a intent.py / spec.py ---

    def _peek(self) -> Tok:
        return self._tokens[self._pos]

    def _peek_at(self, offset: int) -> Tok:
        """Lookahead senza consumare - per LL(3)."""
        idx = self._pos + offset
        if idx >= len(self._tokens):
            return self._tokens[-1]  # EOF
        return self._tokens[idx]

    def _advance(self) -> Tok:
        tok = self._tokens[self._pos]
        if tok.kind != TokKind.EOF:
            self._pos += 1
        return tok

    def _expect(self, kind: TokKind) -> Tok:
        tok = self._peek()
        if tok.kind != kind:
            raise ParseError(
                f"atteso {kind.name}, trovato {tok.kind.name} ({tok.value!r})",
                line=tok.line, col=tok.col
            )
        return self._advance()

    def _expect_word(self, value: str | None = None) -> Tok:
        tok = self._peek()
        if tok.kind != TokKind.IDENT:
            expected = f"'{value}'" if value else "un identificatore"
            raise ParseError(
                f"atteso {expected}, trovato {tok.kind.name} ({tok.value!r})",
                line=tok.line, col=tok.col
            )
        if value is not None and tok.value != value:
            raise ParseError(
                f"atteso '{value}', trovato '{tok.value}'",
                line=tok.line, col=tok.col
            )
        return self._advance()

    def _skip_newlines(self) -> None:
        while self._peek().kind == TokKind.NEWLINE:
            self._advance()

    def _at(self, *kinds: TokKind) -> bool:
        """True se il token corrente e uno dei kinds. Non consuma."""
        return self._peek().kind in kinds

    def _at_word(self, *values: str) -> bool:
        """True se IDENT con uno dei values. Non consuma."""
        tok = self._peek()
        return tok.kind == TokKind.IDENT and tok.value in values
```

### Il LL(3) Lookahead per primary

La grammatica ha `primary` che richiede LL(3):
```
primary ::= IDENT '.' IDENT '(' args? ')'   # LL(3): vedi IDENT DOT IDENT LPAREN
           | IDENT '.' IDENT                  # LL(3): vedi IDENT DOT IDENT
           | IDENT
```

Pattern concreto con `_peek_at`:

```python
def _parse_primary(self) -> ASTNode:
    """Parse primary expression. LL(3) per dotted access."""
    tok = self._peek()

    if tok.kind == TokKind.IDENT:
        # Lookahead: IDENT DOT IDENT?
        if self._peek_at(1).kind == TokKind.DOT:
            # Lookahead: IDENT DOT IDENT LPAREN?
            if self._peek_at(3).kind == TokKind.LPAREN:
                # IDENT '.' IDENT '(' args? ')'  -> method call
                obj = self._advance()    # IDENT
                self._advance()          # DOT
                attr = self._advance()   # IDENT
                self._advance()          # LPAREN
                args = self._parse_args_opt()
                rparen = self._expect(TokKind.RPAREN)
                return MethodCallExpr(
                    obj=obj.value, attr=attr.value, args=args,
                    loc=Loc(obj.line, obj.col)
                )
            else:
                # IDENT '.' IDENT  -> attribute access
                obj = self._advance()    # IDENT
                self._advance()          # DOT
                attr = self._advance()   # IDENT
                return AttrExpr(
                    obj=obj.value, attr=attr.value,
                    loc=Loc(obj.line, obj.col)
                )
        else:
            # IDENT semplice
            tok = self._advance()
            return IdentExpr(name=tok.value, loc=Loc(tok.line, tok.col))

    if tok.kind == TokKind.NUMBER:
        tok = self._advance()
        return NumberExpr(value=tok.value, loc=Loc(tok.line, tok.col))

    if tok.kind == TokKind.STRING:
        tok = self._advance()
        return StringExpr(value=tok.value, loc=Loc(tok.line, tok.col))

    if tok.kind == TokKind.LPAREN:
        self._advance()  # consuma (
        expr = self._parse_expr()
        self._expect(TokKind.RPAREN)
        return expr

    raise ParseError(
        f"attesa un'espressione, trovato {tok.kind.name} ({tok.value!r})",
        line=tok.line, col=tok.col
    )
```

### Il Pattern per step (pattern matching, non LL(k) puro)

```python
# Tabella action (come _ACTION_MAP in intent.py - riusa quasi identico)
# La chiave e una tupla di keyword, il valore e il tipo di azione
_STEP_ACTIONS: dict[tuple[str, ...], str] = {
    ("asks", "to", "do", "task"): "TASK_REQUEST",
    ("returns", "result", "to"): "TASK_RESULT",
    ("asks", "to", "verify"): "AUDIT_REQUEST",
    # ... (come intent.py, aggiungere "proposes")
}

def _parse_step(self) -> StepNode:
    """Parse step: IDENT action NEWLINE.

    Il receiver e estratto dalla sequenza di parole per pattern matching.
    RIUSA _resolve_step da intent.py quasi identicamente.
    """
    sender_tok = self._expect(TokKind.IDENT)

    # Colleziona tutti i WORD fino al NEWLINE
    words: list[str] = []
    word_toks: list[Tok] = []
    while self._peek().kind == TokKind.IDENT:
        t = self._advance()
        words.append(t.value)
        word_toks.append(t)

    self._expect(TokKind.NEWLINE)

    # Pattern matching (stesso algoritmo di _resolve_step in intent.py)
    action_kind, receiver = self._resolve_step_action(
        words, sender_tok.line
    )

    return StepNode(
        sender=sender_tok.value,
        receiver=receiver,
        action=action_kind,
        loc=Loc(sender_tok.line, sender_tok.col)
    )
```

---

## 3. AST DESIGN: Frozen Dataclass con SourceLocation

### Pattern Raccomandato: frozen dataclass + Loc separata

```python
@dataclass(frozen=True)
class Loc:
    """Source location di un nodo AST.

    Ispirato a CPython ast.py: lineno, col_offset.
    Aggiunto col_end per messaggi di errore precisi.
    """
    line: int     # 1-indexed
    col: int      # 0-indexed
    end_line: int = 0   # 0 = non specificato
    end_col: int = 0    # 0 = non specificato

    def __str__(self) -> str:
        return f"line {self.line}, col {self.col}"


# Nodi AST - tutti frozen=True per immutabilita
@dataclass(frozen=True)
class ProgramNode:
    declarations: tuple["DeclNode", ...]
    loc: Loc


@dataclass(frozen=True)
class ProtocolNode:
    name: str
    roles: tuple[str, ...]
    steps: tuple["StepOrChoiceNode", ...]
    properties: tuple["PropertyNode", ...] = ()
    loc: Loc = Loc(0, 0)


@dataclass(frozen=True)
class AgentNode:
    name: str
    clauses: tuple["AgentClauseNode", ...]
    loc: Loc = Loc(0, 0)


@dataclass(frozen=True)
class TypeDeclNode:
    name: str
    body: "VariantTypeNode | RecordTypeNode"
    loc: Loc = Loc(0, 0)


@dataclass(frozen=True)
class UseNode:
    module: str       # "math", "datetime", "pandas"
    alias: str | None  # None se no 'as'
    loc: Loc = Loc(0, 0)


@dataclass(frozen=True)
class StepNode:
    sender: str
    receiver: str
    action: str    # es. "TASK_REQUEST"
    loc: Loc = Loc(0, 0)


@dataclass(frozen=True)
class ChoiceNode:
    decider: str
    branches: tuple[tuple[str, tuple[StepNode, ...]], ...]
    loc: Loc = Loc(0, 0)


# Espressioni (per requires/ensures)
@dataclass(frozen=True)
class IdentExpr:
    name: str
    loc: Loc = Loc(0, 0)

@dataclass(frozen=True)
class AttrExpr:
    obj: str
    attr: str
    loc: Loc = Loc(0, 0)

@dataclass(frozen=True)
class MethodCallExpr:
    obj: str
    attr: str
    args: tuple["Expr", ...]
    loc: Loc = Loc(0, 0)

@dataclass(frozen=True)
class BinOpExpr:
    op: str       # "or", "and", "==", "!=", "<", ">", "<=", ">="
    left: "Expr"
    right: "Expr"
    loc: Loc = Loc(0, 0)

@dataclass(frozen=True)
class NotExpr:
    operand: "Expr"
    loc: Loc = Loc(0, 0)

@dataclass(frozen=True)
class NumberExpr:
    value: str  # stringa per preservare "80" vs "80.0"
    loc: Loc = Loc(0, 0)

@dataclass(frozen=True)
class StringExpr:
    value: str
    loc: Loc = Loc(0, 0)
```

### Perche frozen=True

- Hashable automaticamente (si usa in set e dict per analisi)
- Immutabile: il compilatore (C2) puo fare caching sicuro
- Coerente con i dataclass esistenti nel progetto (protocols.py, spec.py usano gia frozen=True)
- Pattern validato internamente: `IntentParseResult`, `PropertySpec`, `ProtocolSpec` sono tutti frozen

### Visitor Pattern per il Compilatore (C2)

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class ASTVisitor(Generic[T]):
    """Visitor base per traversal AST.

    Ogni metodo visit_X riceve il nodo e restituisce T.
    Per il compilatore (C2), T sara il codice Python generato.
    Per il checker, T sara PropertyResult.
    """

    def visit(self, node: object) -> T:
        """Dispatch al metodo visit_ClassName."""
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.visit_default)
        return visitor(node)

    def visit_default(self, node: object) -> T:
        """Fallback: visita tutti i figli."""
        raise NotImplementedError(
            f"Nessun visitor per {type(node).__name__}"
        )

    def visit_children(self, node: object) -> list[T]:
        """Visita tutti i campi che sono nodi o tuple di nodi."""
        results = []
        for field_val in vars(node).values():
            if isinstance(field_val, tuple):
                for item in field_val:
                    if hasattr(item, "__dataclass_fields__"):
                        results.append(self.visit(item))
            elif hasattr(field_val, "__dataclass_fields__"):
                results.append(self.visit(field_val))
        return results


# Esempio di uso per render (round-trip test)
class ASTRenderer(ASTVisitor[str]):
    """Renderizza l'AST in sorgente Lingua Universale."""

    def visit_ProtocolNode(self, node: ProtocolNode) -> str:
        roles = ", ".join(node.roles)
        steps = "\n".join(
            "    " + self.visit(s) for s in node.steps
        )
        return f"protocol {node.name}:\n    roles: {roles}\n{steps}"

    def visit_StepNode(self, node: StepNode) -> str:
        # Inverti action -> frase naturale
        phrase = _ACTION_TO_PHRASE.get(node.action, node.action)
        return f"{node.sender} {phrase.format(r=node.receiver)}"
```

---

## 4. ERROR RECOVERY: Panic Mode con Anchor Set

### Strategia Raccomandata per il Nostro Caso

Per un parser ~1200 LOC con target "errori umani", la strategia ottimale
(da Thunderseethe 2024 e Ruff v0.4.0) e il **panic mode con anchor set**.

Non serve full error recovery (lascia quello a C3). Serve:
1. Buoni messaggi di errore al PRIMO errore
2. Non crashare con stack trace Python
3. Puntare esattamente alla riga/colonna sbagliata

```python
@dataclass(frozen=True)
class ParseError(Exception):
    """Errore di parsing con posizione precisa.

    Estende errors.py esistente in C3. Per ora: autonomo.
    """
    message: str
    line: int = 0
    col: int = 0

    def __str__(self) -> str:
        if self.line:
            return f"riga {self.line}, colonna {self.col}: {self.message}"
        return self.message

    def format_with_source(self, source_lines: list[str]) -> str:
        """Formatta con il contesto della riga sorgente."""
        if not self.line or self.line > len(source_lines):
            return str(self)

        source_line = source_lines[self.line - 1]
        pointer = " " * self.col + "^"
        return (
            f"riga {self.line}: {self.message}\n"
            f"  {source_line}\n"
            f"  {pointer}"
        )


# Anchor set per ogni costrutto
_TOP_LEVEL_ANCHORS = {"protocol", "agent", "type", "use"}

# Negli error handler: skip fino all'anchor
def _skip_to_next_declaration(self) -> None:
    """Panic mode: salta fino alla prossima dichiarazione top-level."""
    while not self._at(TokKind.EOF):
        tok = self._peek()
        if tok.kind == TokKind.IDENT and tok.value in _TOP_LEVEL_ANCHORS:
            break
        self._advance()
```

### I 3 Tipi di Errore da Gestire Bene

```python
# TIPO 1: Token inatteso (il piu comune)
# SBAGLIATO: "unexpected token at line 5"
# CORRETTO:
raise ParseError(
    f"atteso 'roles:', trovato '{tok.value}'. "
    f"Ogni protocollo deve iniziare con 'roles: ...'",
    line=tok.line, col=tok.col
)

# TIPO 2: Indentazione sbagliata (freccia al problema esatto)
raise ParseError(
    f"l'indentazione non corrisponde a nessun livello precedente "
    f"(trovati {col_indent} spazi, attesi {indent_stack[-1]})",
    line=line_no, col=0
)

# TIPO 3: Keyword sconosciuta nel contesto
raise ParseError(
    f"azione sconosciuta: '{sender} {' '.join(words)}'. "
    f"Azioni valide: 'asks ... to do task', 'returns result to ...', ecc.",
    line=sender_tok.line, col=sender_tok.col
)
```

---

## 5. TESTING STRATEGY: Concreta per il Nostro Caso

### A) Test dei 10 Esempi Canonici (OBBLIGATORIO)

Ogni esempio da C1.2 deve passare. Questi sono i test di accettazione:

```python
import pytest
from .parser import parse

# Tutti e 10 gli esempi da DESIGN_C1_2_SYNTAX_GRAMMAR.md
CANONICAL_EXAMPLES = [
    ("esempio_1_basic", """
protocol DelegateTask:
    roles: regina, worker, guardiana

    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

    properties:
        always terminates
        no deadlock
"""),
    # ... tutti e 10
]

@pytest.mark.parametrize("name,source", CANONICAL_EXAMPLES)
def test_canonical_example_parses(name: str, source: str) -> None:
    """Tutti gli esempi del design devono parsare senza errori."""
    result = parse(source)
    assert result is not None, f"esempio {name} ha fallito"
```

### B) Test AST con Snapshot (Syrupy)

Per verificare che l'AST abbia la struttura corretta senza scrivere assertion complesse:

```python
# pip install syrupy (solo in dev, non in prod)
# Lo snapshot e generato al primo run con: pytest --snapshot-update

from syrupy import SnapshotAssertion

def test_protocol_ast_snapshot(snapshot: SnapshotAssertion) -> None:
    source = """
protocol DelegateTask:
    roles: regina, worker

    regina asks worker to do task
    worker returns result to regina
"""
    result = parse(source)
    # Il primo run crea il file .ambr, i successivi verificano
    assert result == snapshot


# ALTERNATIVA SENZA DIPENDENZE: assert su struttura specifica
def test_protocol_ast_structure() -> None:
    result = parse("""
protocol Simple:
    roles: a, b
    a asks b to do task
""")
    assert isinstance(result, ProgramNode)
    assert len(result.declarations) == 1
    proto = result.declarations[0]
    assert isinstance(proto, ProtocolNode)
    assert proto.name == "Simple"
    assert proto.roles == ("a", "b")
    assert len(proto.steps) == 1
    step = proto.steps[0]
    assert step.sender == "a"
    assert step.receiver == "b"
    assert step.action == "TASK_REQUEST"
```

### C) Test Error Messages (FONDAMENTALE per il target)

```python
@pytest.mark.parametrize("bad_source,expected_fragment", [
    # Tab invece di spazi
    ("protocol X:\n\treges: a, b", "tab"),
    # Indentazione non multiplo di 4
    ("protocol X:\n  roles: a, b", "multiplo di 4"),
    # Keyword sconosciuta
    ("protocol X:\n    roles: a, b\n    a jumps b", "azione sconosciuta"),
    # Roles mancante
    ("protocol X:\n    a asks b to do task", "'roles:'"),
])
def test_error_message_contains(bad_source: str, expected_fragment: str) -> None:
    """I messaggi di errore devono essere comprensibili."""
    with pytest.raises(ParseError) as exc_info:
        parse(bad_source)
    error_msg = str(exc_info.value)
    assert expected_fragment.lower() in error_msg.lower(), (
        f"Messaggio di errore '{error_msg}' non contiene '{expected_fragment}'"
    )

def test_error_has_line_info() -> None:
    """Ogni errore deve avere informazione di riga."""
    with pytest.raises(ParseError) as exc_info:
        parse("protocol X:\n    roles: a\n\tjumps")
    assert exc_info.value.line > 0
    assert exc_info.value.col >= 0
```

### D) Property-Based Testing con Hypothesis (per fuzzing)

```python
from hypothesis import given, settings
from hypothesis import strategies as st

# Genera sorgenti valide dalla grammatica (strat custom)
@st.composite
def valid_step(draw: st.DrawFn) -> str:
    sender = draw(st.sampled_from(["regina", "worker", "guardiana"]))
    actions = [
        ("asks {r} to do task", "worker"),
        ("returns result to {r}", "regina"),
        ("asks {r} to verify", "guardiana"),
    ]
    template, receiver = draw(st.sampled_from(actions))
    return f"{sender} {template.format(r=receiver)}"


@st.composite
def valid_protocol(draw: st.DrawFn) -> str:
    name = draw(st.from_regex(r"[A-Z][A-Za-z]{2,10}", fullmatch=True))
    n_steps = draw(st.integers(min_value=1, max_value=4))
    steps = [draw(valid_step()) for _ in range(n_steps)]
    steps_str = "\n    ".join(steps)
    return f"protocol {name}:\n    roles: regina, worker\n\n    {steps_str}\n"


@given(source=valid_protocol())
@settings(max_examples=200)
def test_valid_protocol_always_parses(source: str) -> None:
    """Qualsiasi protocollo valido generato deve parsare."""
    result = parse(source)
    assert result is not None
    assert len(result.declarations) == 1
```

### E) Round-Trip Test (parse -> render -> parse)

```python
def test_round_trip(example_source: str) -> None:
    """Parse -> render deve produrre sorgente equivalente."""
    ast1 = parse(example_source)
    rendered = render(ast1)  # ASTRenderer
    ast2 = parse(rendered)
    # Non confrontiamo stringhe (whitespace), confrontiamo AST
    assert ast1 == ast2
```

---

## 6. RIFERIMENTI CONCRETI ESAMINATI

### CPython tokenize.py
- **Path:** `Lib/tokenize.py` nel repo CPython
- **Pattern chiave:** Indent stack `[0]`, DEDENT multipli per ogni livello
- **Rilevante per noi:** L'algoritmo esatto di confronto `col vs stack[-1]`

### Lark indenter.py
- **Path:** `lark/indenter.py` nel repo lark-parser
- **Pattern chiave:** `paren_level` counter per disabilitare INDENT/DEDENT
- **Rilevante per noi:** Il counter paren_depth (adottato nel nostro tokenizer)
- **Nota:** Lark e una dipendenza esterna che NON usiamo, ma l'algoritmo e riproducibile

### Ruff v0.4.0 (Astral)
- **Approccio:** Hand-written recursive descent, >2x veloce vs generated
- **Error recovery:** Panic mode con skip intelligente (non necessario per noi in C1.3)
- **Lezione:** "Parser e linter hanno AST ideali diversi" - il nostro AST deve servire
  sia il compilatore (C2) che il constrained decoding export (C2.4)

### Thunderseethe Devlog (2024)
- **Pattern:** anchor set per sincronizzazione post-errore
- **Rilevante per noi:** Semplificato come `_TOP_LEVEL_ANCHORS` (solo in C3)

---

## RACCOMANDAZIONI CONCRETE PER C1.3

### Struttura File Suggerita

```
packages/lingua-universale/src/.../
    parser.py           # NUOVO: ~1200 LOC
        - class Tok + TokKind
        - class Loc
        - class ParseError
        - def tokenize() -> list[Tok]
        - Nodi AST (dataclass frozen)
        - class Parser (recursive descent)
        - def parse(source) -> ProgramNode

tests/
    test_parser_canonical.py   # 10 esempi C1.2
    test_parser_errors.py      # error messages
    test_parser_structure.py   # AST structure assertions
    test_parser_roundtrip.py   # parse -> render -> parse
    test_parser_property.py    # hypothesis (se Hypothesis installato)
```

### Ordine di Implementazione Suggerito

1. **TokKind + Tok + Loc + ParseError** (~30 LOC) - basi
2. **tokenize()** (~120 LOC) - con INDENT/DEDENT espliciti. Test: tutti gli esempi tokenizzano
3. **Nodi AST** (~150 LOC) - frozen dataclass, un nodo per regola grammaticale
4. **Parser utility** (_peek, _advance, _expect, _skip_newlines, _peek_at) (~60 LOC)
5. **parse_program / parse_declaration** - dispatch ai 4 costrutti top-level (~40 LOC)
6. **parse_protocol** - il piu complesso, con INDENT/DEDENT espliciti (~200 LOC)
7. **parse_agent** (~80 LOC)
8. **parse_type_decl** (~60 LOC)
9. **parse_use_decl** (~30 LOC)
10. **parse_expr / or_expr / and_expr / not_expr / comparison / primary** (~200 LOC)
11. **ASTRenderer** per round-trip (~150 LOC)
12. **test_parser_canonical.py** in parallelo con sviluppo

### Riuso da Codice Esistente (50-60% stimato Ingegnera)

| Da | Cosa riusare | Come |
|----|-------------|------|
| intent.py | `_ACTION_MAP`, `_try_match_action`, `_resolve_step`, `_format_valid_actions` | Copia + adatta nomi |
| intent.py | Pattern `_peek`, `_advance`, `_expect`, `_skip_newlines` | Copia identico |
| intent.py | Logica `_parse_choice`, `_parse_elements` | Adatta per INDENT/DEDENT espliciti |
| spec.py | `_parse_property_body`, tutti i `_parse_*` per properties | Copia + integra |
| spec.py | `_CONFIDENCE_LEVELS`, `_TRUST_TIER_MAP` | Importa direttamente |
| protocols.py | `ProtocolStep`, `ProtocolChoice` | Estendi o mantieni per backward compat |

### Decisione Critica: Nuovi Nodi vs Compatibilita

Due opzioni per l'AST:
- **A) Estendi** i dataclass esistenti (Protocol, ProtocolStep) con i nuovi campi
- **B) Nuovi nodi** puliti (ProgramNode, ProtocolNode, AgentNode, ecc.)

**Raccomandazione: Opzione B** (nuovi nodi). Motivazione:
- L'AST del nuovo linguaggio deve servire C2 (compilatore) e C2.4 (constrained decoding)
- I nodi esistenti (Protocol, ProtocolStep) sono tie ai moduli runtime (checker.py, monitor.py)
- Un AST pulito evita coupling tra "AST del linguaggio" e "runtime del framework"
- Backward compat: `parse_intent()` e `parse_spec()` continuano a funzionare, il nuovo
  `parse()` produce ProgramNode -> che C2 compila in Protocol + checker objects

---

## METRICHE ATTESE

```
File:          parser.py
LOC stimate:   1200 (tokenizer 150, AST nodes 200, parser 600, renderer 150, utility 100)
Riuso:         50-60% da intent.py + spec.py
Test:          ~700 LOC (stima Ingegnera)
Coverage:      >= 95% (target C1.3)
Sessioni:      5-6 (stima Ingegnera)
```

---

*Cervella Researcher - CervellaSwarm S409*
*Ricerca PRIMA di implementare. Non inventare, studia come fanno i big.*
