# REPL Design per Lingua Universale - Ricerca C3.4
**Data:** 2026-02-27
**Status:** COMPLETA
**Fonti:** 20+ consultate (Python docs, PEP 762, Elixir IEx, Deno REPL, crafting interpreters, pytest docs, bernsteinbear.com)
**Preparato per:** Sessione C3.4 - REPLSession implementation

---

## 1. Python stdlib REPL Patterns

### `code.InteractiveConsole` / `InteractiveInterpreter`

Il modulo `code` della stdlib e la soluzione canonica per REPL custom in Python.

**Architettura a due livelli:**

```
InteractiveInterpreter   <-- core logic: namespace, exec(), exception handling
       |
InteractiveConsole       <-- aggiunge: prompt ps1/ps2, input buffering, push()
```

**Meccanismo multiline: `runsource()` return value**

Questo e il pattern chiave che dobbiamo REPLICARE per il nostro linguaggio:

```python
# InteractiveConsole.runsource() ritorna:
#   False -> input COMPLETO (eseguito o errore di sintassi definitivo)
#   True  -> input INCOMPLETO (servono piu linee -> mostra "...")

def push(self, line):
    self.buffer.append(line)
    source = "\n".join(self.buffer)
    more = self.runsource(source, self.filename)
    if not more:
        self.resetbuffer()
    return more
```

**Flusso tipico:**
```
User: "protocol Ping:"    -> push() -> runsource() -> True  (incompleto)
User: "  roles: a, b"    -> push() -> runsource() -> True  (incompleto)
User: ""                  -> push() -> runsource() -> False (completo, esegue)
```

**Perche NON usare `InteractiveConsole` direttamente:**
- `runsource()` e hardwired per Python (`compile()` builtin)
- Noi dobbiamo overridare con `check_source()` del nostro eval engine
- La struttura a classi e buona, ma l'implementazione va custom

**Pattern CORRETTO per noi: raw loop + readline**

```python
import readline  # solo importare abilita history + Emacs keybindings

while True:
    try:
        line = input(prompt)
    except EOFError:
        break
    result = session.push(line)
    prompt = "...  " if result.more else "lu>  "
```

### `cmd.Cmd` - Pro/Contro per il nostro caso

**PRO:**
- Dispatching automatico `do_*()` per comandi speciali (`:help`, `:quit`)
- Help system gratuito (docstring di `do_*()`)
- readline integration automatica
- `cmdqueue` per testing senza stdin reale

**CONTRO (decisivi per noi):**
- `cmd.Cmd` e pensato per comandi che iniziano con un keyword (`do_X`)
- Il nostro linguaggio ha sintassi propria: la maggior parte dell'input NON inizia con un "comando" riconoscibile
- `default()` dovrebbe gestire tutto il codice LU -> perde il vantaggio
- Multiline e NON supportato nativamente: va reimplementato comunque
- Overhead di abstraction per niente guadagnato

**VERDETTO: raw readline loop + classe REPLSession custom.**
`cmd.Cmd` va bene per shell-like (tipo `sftp>`). Per un linguaggio vero, raw loop e piu pulito.

---

## 2. IPython Architecture - Lezioni Chiave

IPython usa `prompt_toolkit` (dipendenza esterna, NON per noi). Ma l'architettura insegna:

**Separazione frontend/kernel:**
- Frontend: gestisce prompt, readline, history, colori
- Kernel: esegue codice, mantiene namespace

Per noi: `REPLSession` e il "kernel" (namespace + eval), il loop `_cmd_repl()` e il "frontend".

**Magic commands (pattern `%` / `%%`):**
IPython prefissa i comandi speciali con `%`. Noi usiamo `:` (stile IEx):
- `:help` invece di `%help`
- `:quit` invece di `%quit`
- `:check` per check inline
- `:run` per run file

Questo distingue chiaramente "comandi REPL" da "codice LU".

**Multiline detection automatica:**
IPython detecta automaticamente input incompleto tramite `compile()` con `symbol='single'`.
Noi facciamo lo stesso ma con `check_source()` che non fa execution.

---

## 3. Elixir IEx - Design Lessons

IEx e il REPL piu elegante per un linguaggio con sintassi a blocchi.

**Pattern multiline di IEx:**
- Il parser riceve input come charlist
- Ritorna `{:ok, expr, state}` o `{:incomplete, state}`
- Lo stato viene accumulato tra le linee
- `#iex:break` forza reset dello stato (nostro equivalente: linea vuota doppia)

**Helper commands (`:h`, `:v`, `:c`):**
IEx ha comandi speciali prefissati. Pattern diretto per noi:

```
:help        -- mostra comandi disponibili
:quit / :q   -- esce
:check       -- check_source() sull'input corrente
:run <file>  -- run_file()
:clear       -- pulisce schermo
:reset       -- resetta namespace sessione
:history     -- mostra history
```

**Stateful session:**
IEx mantiene variabili tra comandi. Il nostro `REPLSession.namespace` fa lo stesso.

**Break out of multiline:**
IEx usa `#iex:break` su una riga da sola. Noi: linea vuota su riga da sola quando si e in modalita continuation.

---

## 4. Gleam REPL - Situazione Attuale

Gleam 1.0 (2024) non ha un REPL tradizionale. Ha scelto diversamente:
- Language Tour interattivo nel browser (via WebAssembly)
- Nessun `gleam repl` da CLI

**Lezione:** Un linguaggio typed con AST ricco puo scegliere di non avere REPL classico. Ma Gleam compila a Erlang/JS - noi vogliamo eval incremental che e diverso.

**Cosa Gleam fa bene con i suoi error messages** (applicabile a noi):
- Errori contestualizzati con source snippet (gia fatto in C3.3)
- Suggerimenti "did you mean?" (gia fatto con `_parser_similar()`)

---

## 5. Deno REPL - Pattern Utili

Deno REPL (`deno repl`) ha caratteristiche rilevanti:

**`_` e `_error` variables:**
```
lu> agent Worker:         -- definisco qualcosa
lu> _last                 -- vedo l'ultimo risultato
lu> _error                -- vedo l'ultimo errore
```
Questo e un pattern utile: `REPLSession` dovrebbe mantenere `_last_result` e `_last_error`.

**`--eval` flag equivalente:**
`lu repl --eval "type Color = Red | Green"` -> pre-carica definizioni prima di entrare nel REPL.

**History persistence:**
Deno salva history in `deno_history.txt` in `DENO_DIR`.
Per noi: `~/.lu_history` (oppure `$LU_HISTORY` env var), con `readline.write_history_file()`.

**Exit via Ctrl+D:**
Pattern standard POSIX: Ctrl+D genera `EOFError` -> REPL esce pulitamente.

---

## 6. `cmd.Cmd` vs Raw Readline - Decisione Finale

| Criterio | cmd.Cmd | Raw readline loop |
|---|---|---|
| Multiline support | NO (da reimplementare) | SI (implementazione diretta) |
| Command dispatch | Automatico via do_* | Manuale (switch su prefix `:`) |
| Testing | cmdqueue lista | StringIO su stdin |
| Overhead | Alto per linguaggio custom | Zero |
| Control | Limitato da class API | Totale |
| Fitting al nostro caso | Scarso | Ottimo |

**DECISIONE: Raw readline loop.**

Il pattern corretto:

```python
import readline
import os

def _setup_readline(history_file: str) -> None:
    """Abilita readline history e tab completion."""
    if os.path.exists(history_file):
        readline.read_history_file(history_file)
    readline.set_history_length(1000)
    # Tab completion per keywords LU
    readline.parse_and_bind("tab: complete")
    readline.set_completer(lu_completer)

def _save_readline(history_file: str) -> None:
    readline.write_history_file(history_file)
```

---

## 7. Multiline Input Detection

Questa e la parte piu critica per un linguaggio con sintassi a blocchi come LU.

**Il problema:** Come sapere se l'utente sta ancora scrivendo o ha finito?

```
lu> protocol Ping:       <- INCOMPLETO: manca body
...   roles: a, b        <- ancora...
...   a sends msg to b   <- ancora...
...                      <- linea vuota -> COMPLETO
```

**Strategia raccomandata per LU: "parse-and-check"**

Usa `check_source()` direttamente:

```python
def _is_complete(buffer: list[str]) -> tuple[bool, bool]:
    """
    Returns (is_complete, has_error).
    - (True, False)  -> input valido e completo, procedi con eval
    - (True, True)   -> errore sintattico definitivo, mostra errore
    - (False, False) -> input incompleto, chiedi altra linea
    """
    source = "\n".join(buffer)
    result = check_source(source)
    if result.ok:
        return True, False
    # Distingui errore "incompleto" da errore "definitivo"
    error_text = result.errors[0] if result.errors else ""
    if _looks_incomplete(source, error_text):
        return False, False
    return True, True
```

**`_looks_incomplete()` - euristiche:**

```python
_INCOMPLETE_SIGNALS = [
    "unexpected EOF",
    "expected INDENT",
    "unterminated",
    "LU-N003",  # unterminated string
]

def _looks_incomplete(source: str, error_text: str) -> bool:
    """Euristiche per distinguere errore 'incompleto' da 'definitivo'."""
    # 1. Linea finisce con ":" -> blocco aperto
    stripped = source.rstrip()
    if stripped.endswith(":"):
        return True
    # 2. L'ultimo token e INDENT senza DEDENT (aperto)
    # 3. Error message contiene segnali di incompletezza
    for signal in _INCOMPLETE_SIGNALS:
        if signal in error_text:
            return True
    # 4. Indentazione aperta: l'ultima linea e piu indentata della prima
    lines = [l for l in source.split("\n") if l.strip()]
    if lines and lines[-1].startswith("    "):
        return True
    return False
```

**Escape hatch: linea vuota doppia**
Se l'utente vuole forzare l'esecuzione anche con input incompleto (o uscire dalla modalita continuation):

```python
if not line and buffer and buffer[-1] == "":
    # Due righe vuote consecutive -> forza esecuzione o reset
    break
```

**Alternative considerate (dalla discussione craftinginterpreters #799):**
1. Exception speciale dal parser (complessa, accoppia parser a REPL)
2. Bracket matching (funziona per C-like, non per indent-based)
3. Doppia newline come trigger (IEx pattern) -> SCELTO

---

## 8. Testing del REPL con pytest

**Pattern 1: Test del loop tramite dependency injection**

Il pattern migliore non e mockare stdin direttamente, ma iniettare `input_fn` e `output_fn`:

```python
class REPLSession:
    def __init__(self, *, input_fn=input, output_fn=print):
        self._input_fn = input_fn   # iniettabile per test
        self._output_fn = output_fn  # iniettabile per test
        self._namespace: dict = {}
        self._history: list[str] = []
```

**Test con lista di input:**

```python
def test_repl_single_line(capsys):
    inputs = iter(["type Color = Red | Green", ":quit"])
    session = REPLSession(input_fn=lambda prompt: next(inputs))
    session.run()
    captured = capsys.readouterr()
    assert "Color" in captured.out

def test_repl_multiline(capsys):
    inputs = iter([
        "protocol Ping:",
        "  roles: a, b",
        "  a sends msg to b",
        "",          # chiude il blocco
        ":quit"
    ])
    session = REPLSession(input_fn=lambda prompt: next(inputs))
    session.run()
    captured = capsys.readouterr()
    assert "Ping" in captured.out
```

**Pattern 2: Test dello stato della sessione**

Testa `REPLSession` come oggetto, non il loop:

```python
def test_session_state():
    session = REPLSession()
    r1 = session.eval("type Color = Red | Green | Blue")
    assert r1.ok
    assert "Color" in session.namespace

def test_session_error_doesnt_corrupt_state():
    session = REPLSession()
    session.eval("type Color = Red")
    r = session.eval("invalid syntax here")
    assert not r.ok
    assert "Color" in session.namespace  # stato precedente intatto
```

**Pattern 3: Test dei comandi speciali**

```python
def test_help_command(capsys):
    session = REPLSession()
    session.handle_command(":help")
    captured = capsys.readouterr()
    assert ":quit" in captured.out
    assert ":check" in captured.out

def test_quit_command():
    session = REPLSession()
    result = session.handle_command(":quit")
    assert result.should_exit is True
```

**Pattern 4: monkeypatch stdin per test di integrazione**

```python
from io import StringIO

def test_repl_integration(monkeypatch, capsys):
    fake_input = StringIO("type X = A | B\n:quit\n")
    monkeypatch.setattr("sys.stdin", fake_input)
    # Chiamata al main del REPL...
```

**ATTENZIONE:** readline.read_history_file() / write_history_file() crashano in test
perche readline non funziona senza TTY reale. Wrappare con try/except:

```python
def _safe_readline_setup(history_file: str) -> None:
    try:
        import readline
        if os.path.exists(history_file):
            readline.read_history_file(history_file)
        readline.set_history_length(1000)
    except (ImportError, OSError):
        pass  # Windows senza pyreadline, o in test environment
```

---

## 9. TTY Detection + Colori

Il pattern esiste GIA in `_cli.py` e va RIUSATO verbatim:

```python
# Da _cli.py (linee 32-51) -- pattern gia validato
_RESET = ""
_BOLD = ""
_RED = ""
_GREEN = ""
_YELLOW = ""
_CYAN = ""

def _init_colors() -> None:
    global _RESET, _BOLD, _RED, _GREEN, _YELLOW, _CYAN
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        _RESET = "\033[0m"
        _BOLD = "\033[1m"
        _RED = "\033[31m"
        _GREEN = "\033[32m"
        _YELLOW = "\033[33m"
        _CYAN = "\033[36m"
```

**Miglioramento suggerito rispetto a _cli.py:**
Aggiungere supporto `NO_COLOR` e `FORCE_COLOR` (standard de-facto 2024):

```python
def _init_colors() -> None:
    global _RESET, _BOLD, _RED, _GREEN, _YELLOW, _CYAN
    import os
    if os.environ.get("NO_COLOR"):
        return  # Nessun colore (sempre)
    force = os.environ.get("FORCE_COLOR") or os.environ.get("CLICOLOR_FORCE")
    is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    if force or is_tty:
        _RESET = "\033[0m"
        _BOLD = "\033[1m"
        _RED = "\033[31m"
        _GREEN = "\033[32m"
        _YELLOW = "\033[33m"
        _CYAN = "\033[36m"
```

**Colori specifici REPL:**
- Prompt `lu>` -> `_CYAN` + `_BOLD`
- Continuation `...` -> `_CYAN` (no bold)
- OK output -> `_GREEN`
- Error -> `_RED`
- Info (`:help`, `:history`) -> `_YELLOW`

---

## 10. Session State Management

**Design REPLSession.namespace:**

Il namespace accumula dichiarazioni LU tra comandi. Ogni `eval()` riuscito aggiorna lo stato.

**Problema:** Il nostro `run_source()` crea un `types.ModuleType` isolato ogni volta.
Per accumulare stato, dobbiamo FONDERE i moduli o tenere un namespace condiviso.

**Opzione A: Namespace Python condiviso (raccomandato)**
```python
class REPLSession:
    def __init__(self):
        self._namespace: dict[str, object] = {}
        self._source_history: list[str] = []  # per :history
        self._compiled_history: list[str] = []  # sorgente accu

    def eval(self, source: str) -> EvalResult:
        result = run_source(source)
        if result.ok and result.module:
            # Fonde gli attributi pubblici del modulo nel namespace
            for name in dir(result.module):
                if not name.startswith("_"):
                    self._namespace[name] = getattr(result.module, name)
            self._source_history.append(source)
        return result
```

**Opzione B: Source accumulation (piu fedele al linguaggio)**
```python
def eval(self, source: str) -> EvalResult:
    # Testa prima il singolo input
    test_result = check_source(source)
    if not test_result.ok:
        return test_result
    # Ricompila tutto insieme per coerenza
    accumulated = "\n\n".join(self._source_history + [source])
    full_result = run_source(accumulated)
    if full_result.ok:
        self._source_history.append(source)
    return full_result
```

**Opzione A e raccomandata** perche:
- Performance O(1) invece di O(n) per sessioni lunghe
- Compatibile con la struttura di `load_module()` in `_interop.py`
- Namespace chiari per l'utente

**Variabili speciali automatiche:**
```python
self._namespace["_"] = last_result      # come Python REPL
self._namespace["_error"] = last_error  # come Deno REPL
```

---

## Design Suggerito: REPLSession Class

```python
# packages/lingua-universale/src/cervellaswarm_lingua_universale/_repl.py

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Callable

from ._eval import check_source, run_source, EvalResult


@dataclass
class REPLCommandResult:
    """Risultato di un comando REPL (non LU code)."""
    should_exit: bool = False
    output: str = ""


class REPLSession:
    """Sessione REPL stateful per Lingua Universale.

    Design decisions (C3.4):
    - D2: stdlib REPL (readline/cmd, ZERO deps esterne)
    - D4: REPLSession class stateful
    - Namespace Python condiviso tra comandi
    - Comandi speciali prefissati con ":"
    - Multiline via "parse-and-check" euristico

    Usage::

        session = REPLSession()
        session.run()  # loop interattivo

    For testing::

        inputs = iter(["type X = A | B", ":quit"])
        session = REPLSession(input_fn=lambda p: next(inputs))
        session.run()
    """

    PROMPT = "lu>  "
    PROMPT_CONT = "...  "
    HISTORY_FILE = os.path.expanduser("~/.lu_history")

    def __init__(
        self,
        *,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[..., None] = print,
    ) -> None:
        self._input_fn = input_fn
        self._output_fn = output_fn
        self._namespace: dict[str, object] = {}
        self._source_history: list[str] = []
        self._last_error: str | None = None
        self._colors_initialized = False

    def run(self) -> None:
        """Loop REPL principale. Blocca fino a :quit o Ctrl+D."""
        self._init_colors()
        self._setup_readline()
        self._print_banner()

        buffer: list[str] = []

        while True:
            prompt = self.PROMPT_CONT if buffer else self.PROMPT
            prompt_colored = f"{_CYAN}{_BOLD}{prompt}{_RESET}"

            try:
                line = self._input_fn(prompt_colored)
            except EOFError:
                self._output_fn()  # newline finale
                break
            except KeyboardInterrupt:
                self._output_fn()
                buffer = []
                continue

            # Comandi speciali (solo su riga vuota buffer)
            stripped = line.strip()
            if not buffer and stripped.startswith(":"):
                result = self._handle_command(stripped)
                if result.should_exit:
                    break
                if result.output:
                    self._output_fn(result.output)
                continue

            buffer.append(line)

            # Linea vuota -> tenta esecuzione
            if not stripped:
                if len(buffer) == 1:
                    buffer = []  # riga vuota su buffer vuoto -> ignora
                    continue
                source = "\n".join(buffer).strip()
                if source:
                    self._execute(source)
                buffer = []
                continue

            # Controlla se input e completo
            source = "\n".join(buffer)
            complete, has_error = self._is_complete(source)
            if complete:
                if has_error:
                    # Errore definitivo, non incompleto
                    self._execute(source)
                    buffer = []
                elif not source.endswith(":"):
                    # Input completo e valido senza blocco aperto
                    self._execute(source)
                    buffer = []
                # else: blocco aperto, continua ad accumulare

        self._save_readline()

    def eval(self, source: str) -> EvalResult:
        """Evalua sorgente LU e aggiorna namespace. Per uso programmatico."""
        result = run_source(source)
        if result.ok and result.module:
            for name in dir(result.module):
                if not name.startswith("_"):
                    self._namespace[name] = getattr(result.module, name)
            self._source_history.append(source)
            self._last_error = None
        else:
            self._last_error = result.errors[0] if result.errors else None
        return result

    def _execute(self, source: str) -> None:
        """Esegue source e stampa risultato."""
        result = self.eval(source)
        if result.ok:
            if result.compiled:
                parts = []
                if result.compiled.agents:
                    parts.append(f"{len(result.compiled.agents)} agent(s)")
                if result.compiled.protocols:
                    parts.append(f"{len(result.compiled.protocols)} protocol(s)")
                if result.compiled.types:
                    parts.append(f"{len(result.compiled.types)} type(s)")
                if parts:
                    self._output_fn(f"{_GREEN}OK{_RESET}  {', '.join(parts)}")
        else:
            for err in result.errors:
                self._output_fn(f"{_RED}{err}{_RESET}", file=sys.stderr)

    def _handle_command(self, cmd: str) -> REPLCommandResult:
        """Gestisce comandi speciali :cmd."""
        parts = cmd.split(None, 1)
        name = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if name in (":quit", ":q", ":exit"):
            return REPLCommandResult(should_exit=True)
        elif name == ":help":
            return REPLCommandResult(output=_HELP_TEXT)
        elif name == ":history":
            lines = [f"  {i+1}: {s[:60]}" for i, s in enumerate(self._source_history)]
            return REPLCommandResult(output="\n".join(lines) or "  (empty)")
        elif name == ":reset":
            self._namespace.clear()
            self._source_history.clear()
            return REPLCommandResult(output=f"{_GREEN}Session reset.{_RESET}")
        elif name == ":check" and arg:
            result = check_source(arg)
            if result.ok:
                return REPLCommandResult(output=f"{_GREEN}OK{_RESET}")
            return REPLCommandResult(output=f"{_RED}{result.errors[0]}{_RESET}")
        else:
            return REPLCommandResult(output=f"{_RED}Unknown command: {cmd}{_RESET}  Try :help")

    def _is_complete(self, source: str) -> tuple[bool, bool]:
        """(is_complete, has_error)."""
        result = check_source(source)
        if result.ok:
            return True, False
        error_text = result.errors[0] if result.errors else ""
        if _looks_incomplete(source, error_text):
            return False, False
        return True, True

    def _print_banner(self) -> None:
        from . import __version__
        self._output_fn(
            f"{_CYAN}{_BOLD}Lingua Universale v{__version__}{_RESET}  "
            f"-- the first language native to AI"
        )
        self._output_fn(f"Type {_BOLD}:help{_RESET} for commands, "
                        f"{_BOLD}Ctrl+D{_RESET} to exit.")

    def _init_colors(self) -> None:
        """Abilita colori se TTY o FORCE_COLOR."""
        global _RESET, _BOLD, _RED, _GREEN, _YELLOW, _CYAN  # noqa: PLW0603
        if os.environ.get("NO_COLOR"):
            return
        force = os.environ.get("FORCE_COLOR") or os.environ.get("CLICOLOR_FORCE")
        is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        if force or is_tty:
            _RESET = "\033[0m"
            _BOLD = "\033[1m"
            _RED = "\033[31m"
            _GREEN = "\033[32m"
            _YELLOW = "\033[33m"
            _CYAN = "\033[36m"

    def _setup_readline(self) -> None:
        try:
            import readline as rl
            if os.path.exists(self.HISTORY_FILE):
                rl.read_history_file(self.HISTORY_FILE)
            rl.set_history_length(1000)
        except (ImportError, OSError):
            pass

    def _save_readline(self) -> None:
        try:
            import readline as rl
            rl.write_history_file(self.HISTORY_FILE)
        except (ImportError, OSError):
            pass


# ============================================================
# Module-level color state (come _cli.py)
# ============================================================

_RESET = ""
_BOLD = ""
_RED = ""
_GREEN = ""
_YELLOW = ""
_CYAN = ""

_HELP_TEXT = """\
Lingua Universale REPL commands:
  :help          Show this help
  :quit  :q      Exit the REPL
  :reset         Clear session state (all definitions)
  :history       Show input history
  :check <src>   Check a single-line source without executing

Keyboard shortcuts:
  Ctrl+D         Exit
  Ctrl+C         Cancel current input
  Up/Down        Navigate history
  Ctrl+R         Reverse history search

Multiline input:
  End line with ':' to start a block.
  Press Enter on empty line to execute accumulated input.
  Two empty lines in a row forces reset of input buffer.
"""


def _looks_incomplete(source: str, error_text: str) -> bool:
    """Euristiche per distinguere errore incompleto da definitivo."""
    _INCOMPLETE_SIGNALS = [
        "unexpected EOF",
        "expected INDENT",
        "unterminated",
        "LU-N003",
        "LU-N009",  # empty protocol
    ]
    stripped = source.rstrip()
    if stripped.endswith(":"):
        return True
    lines = [l for l in source.split("\n") if l.strip()]
    if len(lines) > 1 and lines[-1].startswith("    "):
        return True
    for signal in _INCOMPLETE_SIGNALS:
        if signal in error_text:
            return True
    return False
```

---

## Pattern di Test Suggerito

**File:** `tests/test_repl.py`

**Struttura classi:**

```python
class TestREPLSessionEval:
    """Test eval() diretto senza loop."""

class TestREPLMultiline:
    """Test detection multiline."""

class TestREPLCommands:
    """Test comandi : (handle_command)."""

class TestREPLLoop:
    """Test run() con input_fn iniettato."""

class TestREPLColors:
    """Test TTY detection e NO_COLOR."""

class TestREPLState:
    """Test accumulo namespace tra eval()."""
```

**Test essenziali (priorita massima per Guardiana):**

```python
# 1. Single-line eval
def test_eval_type_decl():
    session = REPLSession()
    r = session.eval("type Color = Red | Green | Blue")
    assert r.ok

# 2. Namespace accumulation
def test_namespace_accumulates():
    session = REPLSession()
    session.eval("type X = A | B")
    assert "X" in session._namespace or session._source_history

# 3. Error doesn't corrupt state
def test_error_preserves_state():
    session = REPLSession()
    session.eval("type Color = Red")
    r = session.eval("this is not valid LU syntax here !!")
    assert not r.ok
    # Color deve essere ancora noto
    assert session._source_history  # history non cancellata

# 4. Quit command
def test_quit_exits():
    inputs = iter([":quit"])
    session = REPLSession(input_fn=lambda p: next(inputs))
    session.run()  # deve terminare senza StopIteration

# 5. Multiline protocol
def test_multiline_block(capsys):
    inputs = iter([
        "protocol Ping:",
        "  roles: a, b",
        "  a sends msg to b",
        "",       # esegue
        ":quit"
    ])
    session = REPLSession(input_fn=lambda p: next(inputs))
    session.run()
    captured = capsys.readouterr()
    assert "OK" in captured.out or "Ping" in captured.out

# 6. Ctrl+D (EOFError) exits gracefully
def test_ctrl_d_exits():
    def raise_eof(prompt):
        raise EOFError
    session = REPLSession(input_fn=raise_eof)
    session.run()  # non deve sollevare

# 7. Help command
def test_help_command():
    session = REPLSession()
    result = session._handle_command(":help")
    assert ":quit" in result.output
    assert not result.should_exit

# 8. NO_COLOR disables colors
def test_no_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    session = REPLSession()
    session._init_colors()
    assert _RESET == ""  # o verifica che i globali siano vuoti

# 9. is_complete detection
def test_is_complete_open_block():
    session = REPLSession()
    complete, has_error = session._is_complete("protocol Ping:")
    assert not complete  # blocco aperto, incompleto

def test_is_complete_valid_type():
    session = REPLSession()
    complete, has_error = session._is_complete("type X = A | B")
    assert complete
    assert not has_error
```

---

## Rischi e Mitigazioni

| Rischio | Probabilita | Impatto | Mitigazione |
|---|---|---|---|
| readline non disponibile (Windows) | Media | Basso | try/except ImportError, degradazione graceful |
| `_is_complete()` falso positivo (esegue prematuro) | Media | Medio | Test exhaustivi, regola "`:` finale = sempre incompleto" |
| `_is_complete()` falso negativo (accumula all'infinito) | Bassa | Alto | Escape hatch: doppia riga vuota forza reset buffer |
| Namespace accumulation O(n) per sessioni lunghe | Bassa | Basso | Opzione A (merge moduli) e O(1) per sessione |
| readline.write_history_file() crash in CI | Alta | Basso | try/except OSError gia nel design |
| Colori che escono su pipe/redirect | Media | Basso | isatty() gia gestito, NO_COLOR standard |
| REPL "mangia" eccezioni interne | Media | Alto | `_execute()` non usa bare except, usa pattern EvalResult |

---

## Raccomandazione Finale

**Architettura C3.4:**

1. File nuovo: `_repl.py` con `REPLSession` class
2. Aggiunta a `_cli.py`: subcommand `repl` -> chiama `REPLSession().run()`
3. `_cli.py` `_build_parser()`: aggiunge `subparsers.add_parser("repl")`
4. `_COMMAND_HANDLERS["repl"] = _cmd_repl`
5. Test in `tests/test_repl.py` separato

**Ordine implementazione:**
1. `REPLSession.eval()` + `_is_complete()` (core, testabile senza loop)
2. `_handle_command()` (comandi speciali)
3. `run()` loop principale
4. `_cmd_repl()` in `_cli.py`
5. Test suite

**Stima complessita:** Media. Non e la parte piu difficile - il difficile (multiline detection) e gia risolto dalla strategia "parse-and-check" che delega al nostro `check_source()` esistente.

---

*Ricerca completata da Cervella Researcher - Sessione 422 - 2026-02-27*
*Fonti: 20+ (Python docs, PEP 762, Elixir IEx hexdocs, Deno REPL docs, craftinginterpreters #799, bernsteinbear.com, pytest docs)*
