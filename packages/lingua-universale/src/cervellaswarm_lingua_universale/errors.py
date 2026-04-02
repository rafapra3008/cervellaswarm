# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Human-friendly error messages for Lingua Universale exceptions.

This module is a TRANSLATOR LAYER.  It converts cryptic technical
exceptions into messages that make sense to non-developers.
Inspired by Elm's compiler messages and Rust's diagnostic system.

Key design decisions:
- Existing exceptions are NOT modified (backward compatible).
- This layer is opt-in: call ``humanize(exc)`` when you want
  user-friendly output.
- Three locales supported: "en", "it", "pt".
- Fuzzy matching via ``difflib`` (stdlib, ZERO deps).
- Stable error codes (LU-T001, etc.) for documentation lookup.

Error code scheme:
    LU-T = types.py validation
    LU-P = protocols.py structure
    LU-R = checker.py runtime
    LU-D = dsl.py DSL parse
    LU-S = spec.py spec parse
    LU-I = intent.py intent parse
    LU-L = lean4_bridge.py Lean 4
    LU-G = codegen.py code gen
    LU-C = confidence.py + trust.py
    LU-A = integration.py agents
    LU-N = _tokenizer.py + _parser.py syntax (C1 pipeline)
    LU-X = unknown / fallback

Usage::

    from cervellaswarm_lingua_universale.errors import humanize, format_error

    try:
        checker.send("wrong_agent", "receiver", msg)
    except Exception as exc:
        err = humanize(exc, locale="it")
        print(format_error(err, verbose=True))
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Optional

from .checker import ProtocolViolation, SessionComplete
from .dsl import DSLParseError
from .intent import IntentParseError
from .spec import SpecParseError
from ._tokenizer import TokenizeError
from ._parser import ParseError


# ============================================================
# Public constants
# ============================================================

DEFAULT_LOCALE: str = "en"
SUPPORTED_LOCALES: frozenset[str] = frozenset({"en", "it", "pt"})


# ============================================================
# Enums
# ============================================================


class ErrorCategory(Enum):
    """Broad category of a Lingua Universale error."""

    VALIDATION = "validation"       # types.py, protocols.py
    PROTOCOL = "protocol"           # checker.py runtime
    PARSE = "parse"                 # dsl.py, spec.py, intent.py
    VERIFICATION = "verification"   # lean4_bridge.py
    CODEGEN = "codegen"             # codegen.py
    CONFIDENCE = "confidence"       # confidence.py, trust.py
    INTEGRATION = "integration"     # integration.py
    SYNTAX = "syntax"               # _tokenizer.py, _parser.py (C1 pipeline)


class ErrorSeverity(Enum):
    """How serious the error is."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


# ============================================================
# Data types
# ============================================================


@dataclass(frozen=True)
class ErrorLocation:
    """Optional location information within source text."""

    line: Optional[int] = None
    col: Optional[int] = None
    source: Optional[str] = None  # e.g., "spec", "intent", "dsl"


@dataclass(frozen=True)
class HumanError:
    """A human-friendly representation of a Lingua Universale error.

    Attributes:
        code:       Stable error code (e.g., "LU-T001") for docs lookup.
        category:   Which subsystem produced the error.
        severity:   How serious the error is.
        locale:     Language of the human-readable fields.
        message:    Main message, intelligible on its own.
        suggestion: Actionable hint: how to fix it.
        technical:  Original exception message (for verbose mode).
        location:   Optional source location.
        got:        What the user wrote / provided.
        expected:   What was expected.
        similar:    Fuzzy-matched alternatives ("did you mean?").
    """

    code: str
    category: ErrorCategory
    severity: ErrorSeverity
    locale: str
    message: str
    suggestion: str
    technical: str
    location: Optional[ErrorLocation] = None
    got: Optional[str] = None
    expected: Optional[str] = None
    similar: tuple[str, ...] = ()


# ============================================================
# Snippet renderer
# ============================================================


def render_snippet(
    source: str,
    line: int,
    col: int,
    length: int = 1,
    label: str = "",
    context_lines: int = 1,
) -> str:
    """Generate a source code snippet with caret pointing to the error.

    Inspired by Rust and Elm compiler diagnostics.

    Args:
        source:        Full source text.
        line:          1-indexed line number of the error.
        col:           0-indexed column of the error.
        length:        Number of characters to underline.
        label:         Label to show next to the caret (e.g., "expected ':'").
        context_lines: Number of lines to show before and after the error.

    Returns:
        Multi-line string with line numbers, source, and caret indicator.
    """
    src_lines = source.splitlines() or [""]
    if line < 1 or line > len(src_lines):
        return ""

    start = max(1, line - context_lines)
    end = min(len(src_lines), line + context_lines)
    gutter_w = len(str(end))

    result: list[str] = []

    for ln in range(start, end + 1):
        src = src_lines[ln - 1]
        prefix = f"{str(ln).rjust(gutter_w)} |  "
        result.append(f"{prefix}{src}")

        if ln == line:
            # Caret line -- clamp col to line length
            safe_col = min(col, len(src))
            caret = "^" * max(1, length)
            padding = " " * safe_col
            gutter_pad = " " * gutter_w + " |  "
            label_str = f" {label}" if label else ""
            result.append(f"{gutter_pad}{padding}{caret}{label_str}")

    return "\n".join(result)


# ============================================================
# Internal helpers
# ============================================================


class _SafeDict(dict):  # type: ignore[type-arg]
    """A dict whose missing keys return '{key}' for str.format_map().

    Prevents KeyError when a template references a variable not in
    the context.
    """

    def __missing__(self, key: str) -> str:
        return f"{{{key}}}"


# Each catalog entry: code -> {locale -> (message_template, suggestion_template)}
# Templates use {name}, {value}, {got}, {expected}, etc.
# A _SafeDict is used during substitution so missing keys are harmless.

_CATALOG: MappingProxyType = MappingProxyType({

    # ------------------------------------------------------------------
    # LU-T - types.py validation errors
    # ------------------------------------------------------------------

    "LU-T001": MappingProxyType({
        "en": (
            "'{field}' cannot be empty.",
            "Provide a non-empty string for '{field}'.",
        ),
        "it": (
            "'{field}' non puo essere vuoto.",
            "Fornisci una stringa non vuota per '{field}'.",
        ),
        "pt": (
            "'{field}' nao pode estar vazio.",
            "Forneca uma string nao-vazia para '{field}'.",
        ),
    }),

    "LU-T002": MappingProxyType({
        "en": (
            "Score out of range: got {got}, expected 0.0-10.0.",
            "Use a value between 0.0 and 10.0 for the score.",
        ),
        "it": (
            "Punteggio fuori intervallo: ricevuto {got}, atteso 0.0-10.0.",
            "Usa un valore tra 0.0 e 10.0 per il punteggio.",
        ),
        "pt": (
            "Pontuacao fora do intervalo: recebido {got}, esperado 0.0-10.0.",
            "Use um valor entre 0.0 e 10.0 para a pontuacao.",
        ),
    }),

    "LU-T003": MappingProxyType({
        "en": (
            "Summary is too long: {got} characters (max 200).",
            "Shorten the summary to at most 200 characters.",
        ),
        "it": (
            "Il riepilogo e troppo lungo: {got} caratteri (max 200).",
            "Abbrevia il riepilogo a massimo 200 caratteri.",
        ),
        "pt": (
            "Resumo muito longo: {got} caracteres (max 200).",
            "Encurte o resumo para no maximo 200 caracteres.",
        ),
    }),

    "LU-T004": MappingProxyType({
        "en": (
            "Task is BLOCKED but no blockers were provided.",
            "Set the 'blockers' field to explain what is blocking the task.",
        ),
        "it": (
            "Il task e BLOCKED ma non sono stati forniti blockers.",
            "Imposta il campo 'blockers' per spiegare cosa blocca il task.",
        ),
        "pt": (
            "A tarefa esta BLOCKED mas nenhum bloqueador foi fornecido.",
            "Defina o campo 'blockers' para explicar o que bloqueia a tarefa.",
        ),
    }),

    "LU-T005": MappingProxyType({
        "en": (
            "Plan was rejected but no feedback was provided.",
            "Set the 'feedback' field when rejecting a plan.",
        ),
        "it": (
            "Il piano e stato rifiutato ma non e stato fornito feedback.",
            "Imposta il campo 'feedback' quando rifiuti un piano.",
        ),
        "pt": (
            "O plano foi rejeitado mas nenhum feedback foi fornecido.",
            "Defina o campo 'feedback' ao rejeitar um plano.",
        ),
    }),

    "LU-T006": MappingProxyType({
        "en": (
            "Risk score out of range: got {got}, expected 0.0-1.0.",
            "Use a value between 0.0 and 1.0 for the risk score.",
        ),
        "it": (
            "Punteggio di rischio fuori intervallo: ricevuto {got}, atteso 0.0-1.0.",
            "Usa un valore tra 0.0 e 1.0 per il punteggio di rischio.",
        ),
        "pt": (
            "Pontuacao de risco fora do intervalo: recebido {got}, esperado 0.0-1.0.",
            "Use um valor entre 0.0 e 1.0 para a pontuacao de risco.",
        ),
    }),

    "LU-T007": MappingProxyType({
        "en": (
            "'{field}' must be positive, got {got}.",
            "Use a value >= 1 for '{field}'.",
        ),
        "it": (
            "'{field}' deve essere positivo, ricevuto {got}.",
            "Usa un valore >= 1 per '{field}'.",
        ),
        "pt": (
            "'{field}' deve ser positivo, recebido {got}.",
            "Use um valor >= 1 para '{field}'.",
        ),
    }),

    "LU-T008": MappingProxyType({
        "en": (
            "'{field}' cannot be negative, got {got}.",
            "Use 0 or a positive value for '{field}'.",
        ),
        "it": (
            "'{field}' non puo essere negativo, ricevuto {got}.",
            "Usa 0 o un valore positivo per '{field}'.",
        ),
        "pt": (
            "'{field}' nao pode ser negativo, recebido {got}.",
            "Use 0 ou um valor positivo para '{field}'.",
        ),
    }),

    "LU-T009": MappingProxyType({
        "en": (
            "Audit score out of range: got {got}, expected 0.0-10.0.",
            "Use a value between 0.0 and 10.0 for the audit score.",
        ),
        "it": (
            "Punteggio audit fuori intervallo: ricevuto {got}, atteso 0.0-10.0.",
            "Usa un valore tra 0.0 e 10.0 per il punteggio audit.",
        ),
        "pt": (
            "Pontuacao de auditoria fora do intervalo: recebido {got}, esperado 0.0-10.0.",
            "Use um valor entre 0.0 e 10.0 para a pontuacao de auditoria.",
        ),
    }),

    "LU-T010": MappingProxyType({
        "en": (
            "Checked items cannot be empty for an AuditVerdict.",
            "Provide at least one item in the 'checked' tuple.",
        ),
        "it": (
            "Gli elementi verificati non possono essere vuoti per AuditVerdict.",
            "Fornisci almeno un elemento nella tupla 'checked'.",
        ),
        "pt": (
            "Os itens verificados nao podem estar vazios em AuditVerdict.",
            "Forneca pelo menos um item na tupla 'checked'.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-P - protocols.py structural errors
    # ------------------------------------------------------------------

    "LU-P001": MappingProxyType({
        "en": (
            "Sender and receiver cannot be the same role: '{got}'.",
            "A step must connect two different roles.",
        ),
        "it": (
            "Mittente e destinatario non possono essere lo stesso ruolo: '{got}'.",
            "Un passo deve collegare due ruoli diversi.",
        ),
        "pt": (
            "Remetente e destinatario nao podem ser o mesmo papel: '{got}'.",
            "Um passo deve conectar dois papeis diferentes.",
        ),
    }),

    "LU-P002": MappingProxyType({
        "en": (
            "Protocol must have at least 2 roles, got {got}.",
            "Add more roles to the protocol definition.",
        ),
        "it": (
            "Il protocollo deve avere almeno 2 ruoli, ricevuto {got}.",
            "Aggiungi altri ruoli alla definizione del protocollo.",
        ),
        "pt": (
            "O protocolo deve ter pelo menos 2 papeis, recebido {got}.",
            "Adicione mais papeis a definicao do protocolo.",
        ),
    }),

    "LU-P003": MappingProxyType({
        "en": (
            "Duplicate roles in protocol: {got}.",
            "Each role name must appear exactly once in the roles list.",
        ),
        "it": (
            "Ruoli duplicati nel protocollo: {got}.",
            "Ogni nome di ruolo deve apparire esattamente una volta nella lista ruoli.",
        ),
        "pt": (
            "Papeis duplicados no protocolo: {got}.",
            "Cada nome de papel deve aparecer exatamente uma vez na lista de papeis.",
        ),
    }),

    "LU-P004": MappingProxyType({
        "en": (
            "max_repetitions must be at least 1, got {got}.",
            "Set max_repetitions to 1 or higher.",
        ),
        "it": (
            "max_repetitions deve essere almeno 1, ricevuto {got}.",
            "Imposta max_repetitions a 1 o superiore.",
        ),
        "pt": (
            "max_repetitions deve ser pelo menos 1, recebido {got}.",
            "Defina max_repetitions como 1 ou maior.",
        ),
    }),

    "LU-P005": MappingProxyType({
        "en": (
            "Role '{got}' is not declared in the protocol roles.",
            "Add '{got}' to the roles list, or correct the typo.",
        ),
        "it": (
            "Il ruolo '{got}' non e dichiarato nei ruoli del protocollo.",
            "Aggiungi '{got}' alla lista ruoli, oppure correggi il typo.",
        ),
        "pt": (
            "O papel '{got}' nao esta declarado nos papeis do protocolo.",
            "Adicione '{got}' a lista de papeis, ou corrija o erro de digitacao.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-R - checker.py runtime errors
    # ------------------------------------------------------------------

    "LU-R001": MappingProxyType({
        "en": (
            "Wrong sender at step {step}: expected {expected}, got {got}.",
            "Check which agent should send this message according to the protocol.",
        ),
        "it": (
            "Mittente errato al passo {step}: atteso {expected}, ricevuto {got}.",
            "Verifica quale agente deve inviare questo messaggio secondo il protocollo.",
        ),
        "pt": (
            "Remetente errado no passo {step}: esperado {expected}, recebido {got}.",
            "Verifique qual agente deve enviar esta mensagem conforme o protocolo.",
        ),
    }),

    "LU-R002": MappingProxyType({
        "en": (
            "Wrong receiver at step {step}: expected {expected}, got {got}.",
            "Check which agent should receive this message according to the protocol.",
        ),
        "it": (
            "Destinatario errato al passo {step}: atteso {expected}, ricevuto {got}.",
            "Verifica quale agente deve ricevere questo messaggio secondo il protocollo.",
        ),
        "pt": (
            "Destinatario errado no passo {step}: esperado {expected}, recebido {got}.",
            "Verifique qual agente deve receber esta mensagem conforme o protocolo.",
        ),
    }),

    "LU-R003": MappingProxyType({
        "en": (
            "Wrong message kind at step {step}: expected {expected}, got {got}.",
            "Send the correct message type as specified by the protocol.",
        ),
        "it": (
            "Tipo di messaggio errato al passo {step}: atteso {expected}, ricevuto {got}.",
            "Invia il tipo di messaggio corretto come specificato dal protocollo.",
        ),
        "pt": (
            "Tipo de mensagem errado no passo {step}: esperado {expected}, recebido {got}.",
            "Envie o tipo de mensagem correto conforme especificado pelo protocolo.",
        ),
    }),

    "LU-R004": MappingProxyType({
        "en": (
            "Not at a choice point: cannot call choose_branch() here.",
            "Only call choose_branch() when the session is at a ProtocolChoice.",
        ),
        "it": (
            "Non siamo a un punto di scelta: non si puo chiamare choose_branch() qui.",
            "Chiama choose_branch() solo quando la sessione e a un ProtocolChoice.",
        ),
        "pt": (
            "Nao esta em um ponto de escolha: nao e possivel chamar choose_branch() aqui.",
            "Chame choose_branch() apenas quando a sessao esta em um ProtocolChoice.",
        ),
    }),

    "LU-R005": MappingProxyType({
        "en": (
            "Branch '{got}' not found. Available branches: {expected}.",
            "Use one of the valid branch names listed above.",
        ),
        "it": (
            "Branch '{got}' non trovato. Branch disponibili: {expected}.",
            "Usa uno dei nomi di branch validi elencati sopra.",
        ),
        "pt": (
            "Branch '{got}' nao encontrado. Branches disponiveis: {expected}.",
            "Use um dos nomes de branch validos listados acima.",
        ),
    }),

    "LU-R006": MappingProxyType({
        "en": (
            "At a choice point: call choose_branch() before sending a message.",
            "The protocol requires you to choose a branch before proceeding.",
        ),
        "it": (
            "Siamo a un punto di scelta: chiama choose_branch() prima di inviare.",
            "Il protocollo richiede di scegliere un branch prima di procedere.",
        ),
        "pt": (
            "Em um ponto de escolha: chame choose_branch() antes de enviar uma mensagem.",
            "O protocolo requer que voce escolha um branch antes de continuar.",
        ),
    }),

    "LU-R007": MappingProxyType({
        "en": (
            "Protocol session '{session}' is already complete.",
            "Start a new session or check your loop logic.",
        ),
        "it": (
            "La sessione di protocollo '{session}' e gia completata.",
            "Avvia una nuova sessione o controlla la tua logica di loop.",
        ),
        "pt": (
            "A sessao de protocolo '{session}' ja esta completa.",
            "Inicie uma nova sessao ou verifique sua logica de loop.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-D - dsl.py parse errors
    # ------------------------------------------------------------------

    "LU-D001": MappingProxyType({
        "en": (
            "Unexpected character in DSL source: {got}.",
            "Remove or replace the unexpected character.",
        ),
        "it": (
            "Carattere imprevisto nella sorgente DSL: {got}.",
            "Rimuovi o sostituisci il carattere imprevisto.",
        ),
        "pt": (
            "Caractere inesperado na fonte DSL: {got}.",
            "Remova ou substitua o caractere inesperado.",
        ),
    }),

    "LU-D002": MappingProxyType({
        "en": (
            "Syntax error: expected {expected}, got {got}.",
            "Fix the DSL syntax at the indicated location.",
        ),
        "it": (
            "Errore di sintassi: atteso {expected}, ricevuto {got}.",
            "Correggi la sintassi DSL nella posizione indicata.",
        ),
        "pt": (
            "Erro de sintaxe: esperado {expected}, recebido {got}.",
            "Corrija a sintaxe DSL no local indicado.",
        ),
    }),

    "LU-D003": MappingProxyType({
        "en": (
            "Unknown message type: '{got}'.",
            "Use a valid PascalCase message type (e.g., TaskRequest, AuditVerdict).",
        ),
        "it": (
            "Tipo di messaggio sconosciuto: '{got}'.",
            "Usa un tipo di messaggio PascalCase valido (es. TaskRequest, AuditVerdict).",
        ),
        "pt": (
            "Tipo de mensagem desconhecido: '{got}'.",
            "Use um tipo de mensagem PascalCase valido (ex. TaskRequest, AuditVerdict).",
        ),
    }),

    "LU-D004": MappingProxyType({
        "en": (
            "Duplicate branch label: '{got}'.",
            "Each branch in a choice must have a unique label.",
        ),
        "it": (
            "Etichetta di branch duplicata: '{got}'.",
            "Ogni branch in una scelta deve avere un'etichetta unica.",
        ),
        "pt": (
            "Rotulo de branch duplicado: '{got}'.",
            "Cada branch em uma escolha deve ter um rotulo unico.",
        ),
    }),

    "LU-D005": MappingProxyType({
        "en": (
            "Empty choice or branch: a choice must have at least one non-empty branch.",
            "Add at least one step inside each branch.",
        ),
        "it": (
            "Scelta o branch vuoto: una scelta deve avere almeno un branch non vuoto.",
            "Aggiungi almeno un passo all'interno di ogni branch.",
        ),
        "pt": (
            "Escolha ou branch vazio: uma escolha deve ter pelo menos um branch nao-vazio.",
            "Adicione pelo menos um passo dentro de cada branch.",
        ),
    }),

    "LU-D006": MappingProxyType({
        "en": (
            "No protocols found in DSL source.",
            "Define at least one protocol block: 'protocol Name {{ ... }}'.",
        ),
        "it": (
            "Nessun protocollo trovato nella sorgente DSL.",
            "Definisci almeno un blocco protocollo: 'protocol Nome {{ ... }}'.",
        ),
        "pt": (
            "Nenhum protocolo encontrado na fonte DSL.",
            "Defina pelo menos um bloco de protocolo: 'protocol Nome {{ ... }}'.",
        ),
    }),

    "LU-D007": MappingProxyType({
        "en": (
            "Unexpected end of input in DSL: expected '}}'.",
            "Add the missing closing brace '}}'.",
        ),
        "it": (
            "Fine inattesa dell'input DSL: attesa '}}'.",
            "Aggiungi la parentesi graffa di chiusura '}}'.",
        ),
        "pt": (
            "Fim inesperado do input DSL: esperado '}}'.",
            "Adicione a chave de fechamento '}}'.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-S - spec.py parse errors
    # ------------------------------------------------------------------

    "LU-S001": MappingProxyType({
        "en": (
            "Tabs are not allowed in spec source (line {line}).",
            "Replace tabs with 4 spaces for indentation.",
        ),
        "it": (
            "I tab non sono permessi nella sorgente spec (riga {line}).",
            "Sostituisci i tab con 4 spazi per l'indentazione.",
        ),
        "pt": (
            "Tabs nao sao permitidos na fonte spec (linha {line}).",
            "Substitua tabs por 4 espacos para indentacao.",
        ),
    }),

    "LU-S002": MappingProxyType({
        "en": (
            "Indentation must be a multiple of 4 spaces, got {got} (line {line}).",
            "Use exactly 4 spaces per indentation level.",
        ),
        "it": (
            "L'indentazione deve essere multipla di 4 spazi, ricevuto {got} (riga {line}).",
            "Usa esattamente 4 spazi per ogni livello di indentazione.",
        ),
        "pt": (
            "A indentacao deve ser multipla de 4 espacos, recebido {got} (linha {line}).",
            "Use exatamente 4 espacos por nivel de indentacao.",
        ),
    }),

    "LU-S003": MappingProxyType({
        "en": (
            "Unknown message kind: '{got}' (line {line}).",
            "Use a valid snake_case message kind (e.g., task_request, audit_verdict).",
        ),
        "it": (
            "Tipo di messaggio sconosciuto: '{got}' (riga {line}).",
            "Usa un tipo di messaggio snake_case valido (es. task_request, audit_verdict).",
        ),
        "pt": (
            "Tipo de mensagem desconhecido: '{got}' (linha {line}).",
            "Use um tipo de mensagem snake_case valido (ex. task_request, audit_verdict).",
        ),
    }),

    "LU-S004": MappingProxyType({
        "en": (
            "Unknown confidence level: '{got}' (line {line}).",
            "Valid levels are: certain, high, medium, low, speculative.",
        ),
        "it": (
            "Livello di confidenza sconosciuto: '{got}' (riga {line}).",
            "I livelli validi sono: certain, high, medium, low, speculative.",
        ),
        "pt": (
            "Nivel de confianca desconhecido: '{got}' (linha {line}).",
            "Os niveis validos sao: certain, high, medium, low, speculative.",
        ),
    }),

    "LU-S005": MappingProxyType({
        "en": (
            "Unknown trust tier: '{got}' (line {line}).",
            "Valid tiers are: verified, trusted, standard, untrusted.",
        ),
        "it": (
            "Livello di fiducia sconosciuto: '{got}' (riga {line}).",
            "I livelli validi sono: verified, trusted, standard, untrusted.",
        ),
        "pt": (
            "Nivel de confianca desconhecido: '{got}' (linha {line}).",
            "Os niveis validos sao: verified, trusted, standard, untrusted.",
        ),
    }),

    "LU-S006": MappingProxyType({
        "en": (
            "ORDERING property: 'a' and 'b' must be different message kinds.",
            "Use two distinct message kinds in an ordering property.",
        ),
        "it": (
            "Proprieta ORDERING: 'a' e 'b' devono essere tipi di messaggio diversi.",
            "Usa due tipi di messaggio distinti in una proprieta di ordinamento.",
        ),
        "pt": (
            "Propriedade ORDERING: 'a' e 'b' devem ser tipos de mensagem diferentes.",
            "Use dois tipos de mensagem distintos em uma propriedade de ordenamento.",
        ),
    }),

    "LU-S007": MappingProxyType({
        "en": (
            "Spec syntax error: expected {expected}, got {got} (line {line}).",
            "Fix the spec syntax at the indicated line.",
        ),
        "it": (
            "Errore di sintassi spec: atteso {expected}, ricevuto {got} (riga {line}).",
            "Correggi la sintassi spec alla riga indicata.",
        ),
        "pt": (
            "Erro de sintaxe spec: esperado {expected}, recebido {got} (linha {line}).",
            "Corrija a sintaxe spec na linha indicada.",
        ),
    }),

    "LU-S008": MappingProxyType({
        "en": (
            "Spec block must have at least one property.",
            "Add at least one property declaration inside the spec block.",
        ),
        "it": (
            "Il blocco spec deve avere almeno una proprieta.",
            "Aggiungi almeno una dichiarazione di proprieta all'interno del blocco spec.",
        ),
        "pt": (
            "O bloco spec deve ter pelo menos uma propriedade.",
            "Adicione pelo menos uma declaracao de propriedade dentro do bloco spec.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-I - intent.py parse errors
    # ------------------------------------------------------------------

    "LU-I001": MappingProxyType({
        "en": (
            "Tabs are not allowed in intent source (line {line}).",
            "Replace tabs with 4 spaces for indentation.",
        ),
        "it": (
            "I tab non sono permessi nella sorgente intent (riga {line}).",
            "Sostituisci i tab con 4 spazi per l'indentazione.",
        ),
        "pt": (
            "Tabs nao sao permitidos na fonte intent (linha {line}).",
            "Substitua tabs por 4 espacos para indentacao.",
        ),
    }),

    "LU-I002": MappingProxyType({
        "en": (
            "Indentation must be a multiple of 4 spaces, got {got} (line {line}).",
            "Use exactly 4 spaces per indentation level.",
        ),
        "it": (
            "L'indentazione deve essere multipla di 4 spazi, ricevuto {got} (riga {line}).",
            "Usa esattamente 4 spazi per ogni livello di indentazione.",
        ),
        "pt": (
            "A indentacao deve ser multipla de 4 espacos, recebido {got} (linha {line}).",
            "Use exatamente 4 espacos por nivel de indentacao.",
        ),
    }),

    "LU-I003": MappingProxyType({
        "en": (
            "Cannot parse action: unknown verb phrase '{got}' (line {line}).",
            "Use a recognized action phrase such as 'asks ... to do task' or "
            "'returns result to'.",
        ),
        "it": (
            "Impossibile analizzare l'azione: frase verbale sconosciuta '{got}' (riga {line}).",
            "Usa una frase di azione riconosciuta come 'asks ... to do task' o "
            "'returns result to'.",
        ),
        "pt": (
            "Nao e possivel analisar a acao: frase verbal desconhecida '{got}' (linha {line}).",
            "Use uma frase de acao reconhecida como 'asks ... to do task' ou "
            "'returns result to'.",
        ),
    }),

    "LU-I004": MappingProxyType({
        "en": (
            "Expected indented 'roles:' declaration (line {line}).",
            "Add 'roles: role1, role2' indented by 4 spaces after the protocol header.",
        ),
        "it": (
            "Attesa la dichiarazione 'roles:' indentata (riga {line}).",
            "Aggiungi 'roles: ruolo1, ruolo2' indentato di 4 spazi dopo l'intestazione.",
        ),
        "pt": (
            "Esperada declaracao 'roles:' indentada (linha {line}).",
            "Adicione 'roles: papel1, papel2' indentado por 4 espacos apos o cabecalho.",
        ),
    }),

    "LU-I005": MappingProxyType({
        "en": (
            "Intent syntax error: expected {expected}, got {got} (line {line}).",
            "Fix the intent syntax at the indicated line.",
        ),
        "it": (
            "Errore di sintassi intent: atteso {expected}, ricevuto {got} (riga {line}).",
            "Correggi la sintassi intent alla riga indicata.",
        ),
        "pt": (
            "Erro de sintaxe intent: esperado {expected}, recebido {got} (linha {line}).",
            "Corrija a sintaxe intent na linha indicada.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-L - lean4_bridge.py errors
    # ------------------------------------------------------------------

    "LU-L001": MappingProxyType({
        "en": (
            "Cannot create Lean 4 identifier from empty string.",
            "Provide a non-empty name before calling the Lean 4 generator.",
        ),
        "it": (
            "Impossibile creare un identificatore Lean 4 da una stringa vuota.",
            "Fornisci un nome non vuoto prima di chiamare il generatore Lean 4.",
        ),
        "pt": (
            "Nao e possivel criar identificador Lean 4 a partir de string vazia.",
            "Forneca um nome nao-vazio antes de chamar o gerador Lean 4.",
        ),
    }),

    "LU-L002": MappingProxyType({
        "en": (
            "Invalid Lean 4 identifier: '{got}'.",
            "Identifiers must match [A-Za-z_][A-Za-z0-9_]*.",
        ),
        "it": (
            "Identificatore Lean 4 non valido: '{got}'.",
            "Gli identificatori devono corrispondere a [A-Za-z_][A-Za-z0-9_]*.",
        ),
        "pt": (
            "Identificador Lean 4 invalido: '{got}'.",
            "Identificadores devem corresponder a [A-Za-z_][A-Za-z0-9_]*.",
        ),
    }),

    "LU-L003": MappingProxyType({
        "en": (
            "Lean 4 is not installed or not on PATH.",
            "Install Lean 4 (https://leanprover.github.io/) or use the generator "
            "without verification.",
        ),
        "it": (
            "Lean 4 non e installato o non e nel PATH.",
            "Installa Lean 4 (https://leanprover.github.io/) o usa il generatore "
            "senza verifica.",
        ),
        "pt": (
            "Lean 4 nao esta instalado ou nao esta no PATH.",
            "Instale o Lean 4 (https://leanprover.github.io/) ou use o gerador "
            "sem verificacao.",
        ),
    }),

    "LU-L004": MappingProxyType({
        "en": (
            "Lean 4 verification timed out.",
            "Increase the timeout or simplify the protocol.",
        ),
        "it": (
            "La verifica Lean 4 e andata in timeout.",
            "Aumenta il timeout o semplifica il protocollo.",
        ),
        "pt": (
            "A verificacao Lean 4 excedeu o tempo limite.",
            "Aumente o timeout ou simplifique o protocolo.",
        ),
    }),

    "LU-L005": MappingProxyType({
        "en": (
            "Protocol list for Lean 4 generation cannot be empty.",
            "Provide at least one protocol to generate_lean4_multi().",
        ),
        "it": (
            "La lista di protocolli per la generazione Lean 4 non puo essere vuota.",
            "Fornisci almeno un protocollo a generate_lean4_multi().",
        ),
        "pt": (
            "A lista de protocolos para geracao Lean 4 nao pode estar vazia.",
            "Forneca pelo menos um protocolo a generate_lean4_multi().",
        ),
    }),

    "LU-L006": MappingProxyType({
        "en": (
            "Duplicate protocol names in Lean 4 generation: {got}.",
            "Each protocol must have a unique name.",
        ),
        "it": (
            "Nomi di protocollo duplicati nella generazione Lean 4: {got}.",
            "Ogni protocollo deve avere un nome unico.",
        ),
        "pt": (
            "Nomes de protocolo duplicados na geracao Lean 4: {got}.",
            "Cada protocolo deve ter um nome unico.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-G - codegen.py errors
    # ------------------------------------------------------------------

    "LU-G001": MappingProxyType({
        "en": (
            "Cannot create Python identifier from empty string.",
            "Provide a non-empty name before calling the Python code generator.",
        ),
        "it": (
            "Impossibile creare un identificatore Python da una stringa vuota.",
            "Fornisci un nome non vuoto prima di chiamare il generatore di codice Python.",
        ),
        "pt": (
            "Nao e possivel criar identificador Python a partir de string vazia.",
            "Forneca um nome nao-vazio antes de chamar o gerador de codigo Python.",
        ),
    }),

    "LU-G002": MappingProxyType({
        "en": (
            "Protocol name '{got}' cannot be used as a Python identifier.",
            "Use a name that can be safely converted to a Python constant.",
        ),
        "it": (
            "Il nome del protocollo '{got}' non puo essere usato come identificatore Python.",
            "Usa un nome che possa essere convertito in modo sicuro in una costante Python.",
        ),
        "pt": (
            "O nome do protocolo '{got}' nao pode ser usado como identificador Python.",
            "Use um nome que possa ser convertido com seguranca em uma constante Python.",
        ),
    }),

    "LU-G003": MappingProxyType({
        "en": (
            "Protocol list for Python code generation cannot be empty.",
            "Provide at least one protocol to generate_python_multi().",
        ),
        "it": (
            "La lista di protocolli per la generazione di codice Python non puo essere vuota.",
            "Fornisci almeno un protocollo a generate_python_multi().",
        ),
        "pt": (
            "A lista de protocolos para geracao de codigo Python nao pode estar vazia.",
            "Forneca pelo menos um protocolo a generate_python_multi().",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-C - confidence.py + trust.py errors
    # ------------------------------------------------------------------

    "LU-C001": MappingProxyType({
        "en": (
            "Confidence value out of range: got {got}, expected 0.0-1.0.",
            "Use a value between 0.0 (no confidence) and 1.0 (full confidence).",
        ),
        "it": (
            "Valore di confidenza fuori intervallo: ricevuto {got}, atteso 0.0-1.0.",
            "Usa un valore tra 0.0 (nessuna confidenza) e 1.0 (piena confidenza).",
        ),
        "pt": (
            "Valor de confianca fora do intervalo: recebido {got}, esperado 0.0-1.0.",
            "Use um valor entre 0.0 (sem confianca) e 1.0 (confianca total).",
        ),
    }),

    "LU-C002": MappingProxyType({
        "en": (
            "Cannot compose an empty collection of confidence scores.",
            "Provide at least one ConfidenceScore to compose_scores().",
        ),
        "it": (
            "Impossibile comporre una collezione vuota di punteggi di confidenza.",
            "Fornisci almeno un ConfidenceScore a compose_scores().",
        ),
        "pt": (
            "Nao e possivel compor uma colecao vazia de pontuacoes de confianca.",
            "Forneca pelo menos um ConfidenceScore a compose_scores().",
        ),
    }),

    "LU-C003": MappingProxyType({
        "en": (
            "Trust value out of range: got {got}, expected 0.0-1.0.",
            "Use a value between 0.0 (no trust) and 1.0 (full trust).",
        ),
        "it": (
            "Valore di fiducia fuori intervallo: ricevuto {got}, atteso 0.0-1.0.",
            "Usa un valore tra 0.0 (nessuna fiducia) e 1.0 (fiducia piena).",
        ),
        "pt": (
            "Valor de confianca fora do intervalo: recebido {got}, esperado 0.0-1.0.",
            "Use um valor entre 0.0 (sem confianca) e 1.0 (confianca total).",
        ),
    }),

    "LU-C004": MappingProxyType({
        "en": (
            "Attenuation factor out of range: got {got}, expected 0.0-1.0.",
            "Use a factor between 0.0 and 1.0 for trust attenuation.",
        ),
        "it": (
            "Fattore di attenuazione fuori intervallo: ricevuto {got}, atteso 0.0-1.0.",
            "Usa un fattore tra 0.0 e 1.0 per l'attenuazione della fiducia.",
        ),
        "pt": (
            "Fator de atenuacao fora do intervalo: recebido {got}, esperado 0.0-1.0.",
            "Use um fator entre 0.0 e 1.0 para atenuacao de confianca.",
        ),
    }),

    "LU-C005": MappingProxyType({
        "en": (
            "Cannot compose an empty trust chain.",
            "Provide at least one TrustScore to compose_chain().",
        ),
        "it": (
            "Impossibile comporre una catena di fiducia vuota.",
            "Fornisci almeno un TrustScore a compose_chain().",
        ),
        "pt": (
            "Nao e possivel compor uma cadeia de confianca vazia.",
            "Forneca pelo menos um TrustScore a compose_chain().",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-A - integration.py errors
    # ------------------------------------------------------------------

    "LU-A001": MappingProxyType({
        "en": (
            "Binding role '{got}' is not in the protocol roles.",
            "Only bind roles that are declared in the protocol.",
        ),
        "it": (
            "Il ruolo di binding '{got}' non e nei ruoli del protocollo.",
            "Esegui il binding solo di ruoli dichiarati nel protocollo.",
        ),
        "pt": (
            "O papel de binding '{got}' nao esta nos papeis do protocolo.",
            "Vincule apenas papeis declarados no protocolo.",
        ),
    }),

    "LU-A002": MappingProxyType({
        "en": (
            "Unknown agent name: '{got}'.",
            "Use a valid agent name from the AGENT_CATALOG "
            "(e.g., 'cervella-backend', 'cervella-orchestrator').",
        ),
        "it": (
            "Nome agente sconosciuto: '{got}'.",
            "Usa un nome agente valido dall'AGENT_CATALOG "
            "(es. 'cervella-backend', 'cervella-orchestrator').",
        ),
        "pt": (
            "Nome de agente desconhecido: '{got}'.",
            "Use um nome de agente valido do AGENT_CATALOG "
            "(ex. 'cervella-backend', 'cervella-orchestrator').",
        ),
    }),

    "LU-A003": MappingProxyType({
        "en": (
            "Agent '{got}' cannot play this protocol role.",
            "Check agent_by_name() to see which roles this agent supports.",
        ),
        "it": (
            "L'agente '{got}' non puo svolgere questo ruolo di protocollo.",
            "Controlla agent_by_name() per vedere quali ruoli supporta questo agente.",
        ),
        "pt": (
            "O agente '{got}' nao pode desempenhar este papel de protocolo.",
            "Verifique agent_by_name() para ver quais papeis este agente suporta.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-N - C1 pipeline: tokenizer + parser syntax errors
    # ------------------------------------------------------------------

    "LU-N001": MappingProxyType({
        "en": (
            "tab characters are not allowed; use spaces.",
            "Replace tabs with spaces (4 spaces per indent level).",
        ),
        "it": (
            "i caratteri tab non sono permessi; usa spazi.",
            "Sostituisci i tab con spazi (4 spazi per livello di indentazione).",
        ),
        "pt": (
            "caracteres tab nao sao permitidos; use espacos.",
            "Substitua tabs por espacos (4 espacos por nivel de indentacao).",
        ),
    }),

    "LU-N002": MappingProxyType({
        "en": (
            "indentation must be a multiple of 4 spaces (got {got}).",
            "Adjust indentation to a multiple of 4 spaces.",
        ),
        "it": (
            "l'indentazione deve essere un multiplo di 4 spazi (ricevuto {got}).",
            "Correggi l'indentazione a un multiplo di 4 spazi.",
        ),
        "pt": (
            "a indentacao deve ser um multiplo de 4 espacos (recebido {got}).",
            "Ajuste a indentacao para um multiplo de 4 espacos.",
        ),
    }),

    "LU-N003": MappingProxyType({
        "en": (
            "unterminated string literal.",
            "Close the string with a matching quote.",
        ),
        "it": (
            "stringa non terminata.",
            "Chiudi la stringa con le virgolette corrispondenti.",
        ),
        "pt": (
            "string nao terminada.",
            "Feche a string com as aspas correspondentes.",
        ),
    }),

    "LU-N004": MappingProxyType({
        "en": (
            "unexpected character: `{got}`.",
            "Remove or replace this character.",
        ),
        "it": (
            "carattere inaspettato: `{got}`.",
            "Rimuovi o sostituisci questo carattere.",
        ),
        "pt": (
            "caractere inesperado: `{got}`.",
            "Remova ou substitua este caractere.",
        ),
    }),

    "LU-N005": MappingProxyType({
        "en": (
            "dedent does not match any outer indentation level.",
            "Align the line with a previous indentation level.",
        ),
        "it": (
            "la dedentazione non corrisponde a nessun livello esterno.",
            "Allinea la riga con un livello di indentazione precedente.",
        ),
        "pt": (
            "a deindentacao nao corresponde a nenhum nivel externo.",
            "Alinhe a linha com um nivel de indentacao anterior.",
        ),
    }),

    "LU-N006": MappingProxyType({
        "en": (
            "unknown top-level keyword `{got}`.",
            "Top-level declarations start with: type, agent, protocol, use.",
        ),
        "it": (
            "keyword top-level sconosciuta `{got}`.",
            "Le dichiarazioni top-level iniziano con: type, agent, protocol, use.",
        ),
        "pt": (
            "palavra-chave top-level desconhecida `{got}`.",
            "Declaracoes top-level comecam com: type, agent, protocol, use.",
        ),
    }),

    "LU-N007": MappingProxyType({
        "en": (
            "expected {expected}, got `{got}`.",
            "Check the syntax at this position.",
        ),
        "it": (
            "atteso {expected}, ricevuto `{got}`.",
            "Controlla la sintassi in questa posizione.",
        ),
        "pt": (
            "esperado {expected}, recebido `{got}`.",
            "Verifique a sintaxe nesta posicao.",
        ),
    }),

    "LU-N008": MappingProxyType({
        "en": (
            "expected `:` after declaration name.",
            "Add a colon after the name: `protocol MyProto:`",
        ),
        "it": (
            "atteso `:` dopo il nome della dichiarazione.",
            "Aggiungi i due punti dopo il nome: `protocol MioProto:`",
        ),
        "pt": (
            "esperado `:` apos o nome da declaracao.",
            "Adicione dois-pontos apos o nome: `protocol MeuProto:`",
        ),
    }),

    "LU-N009": MappingProxyType({
        "en": (
            "protocol must have at least one step.",
            "Add at least one message step (e.g., `a sends message to b`).",
        ),
        "it": (
            "il protocollo deve avere almeno un passo.",
            "Aggiungi almeno un passo (es: `a sends message to b`).",
        ),
        "pt": (
            "o protocolo deve ter pelo menos um passo.",
            "Adicione pelo menos um passo (ex: `a sends message to b`).",
        ),
    }),

    "LU-N010": MappingProxyType({
        "en": (
            "cannot parse step action `{got}`.",
            "Valid actions: asks, returns, sends, tells, proposes.",
        ),
        "it": (
            "impossibile analizzare l'azione del passo `{got}`.",
            "Azioni valide: asks, returns, sends, tells, proposes.",
        ),
        "pt": (
            "nao foi possivel analisar a acao do passo `{got}`.",
            "Acoes validas: asks, returns, sends, tells, proposes.",
        ),
    }),

    "LU-N011": MappingProxyType({
        "en": (
            "unknown property `{got}`.",
            "Valid properties: always terminates, no deadlock, all roles participate, "
            "confidence >= level, trust >= tier, X before Y, X cannot send Y.",
        ),
        "it": (
            "proprieta sconosciuta `{got}`.",
            "Proprieta valide: always terminates, no deadlock, all roles participate, "
            "confidence >= level, trust >= tier, X before Y, X cannot send Y.",
        ),
        "pt": (
            "propriedade desconhecida `{got}`.",
            "Propriedades validas: always terminates, no deadlock, all roles participate, "
            "confidence >= level, trust >= tier, X before Y, X cannot send Y.",
        ),
    }),

    "LU-N012": MappingProxyType({
        "en": (
            "unknown agent clause `{got}`.",
            "Valid clauses: role, trust, accepts, produces, requires, ensures.",
        ),
        "it": (
            "clausola agent sconosciuta `{got}`.",
            "Clausole valide: role, trust, accepts, produces, requires, ensures.",
        ),
        "pt": (
            "clausula de agente desconhecida `{got}`.",
            "Clausulas validas: role, trust, accepts, produces, requires, ensures.",
        ),
    }),

    "LU-N013": MappingProxyType({
        "en": (
            "invalid trust tier `{got}`.",
            "Valid trust tiers: verified, trusted, standard, untrusted.",
        ),
        "it": (
            "livello di trust non valido `{got}`.",
            "Livelli validi: verified, trusted, standard, untrusted.",
        ),
        "pt": (
            "nivel de confianca invalido `{got}`.",
            "Niveis validos: verified, trusted, standard, untrusted.",
        ),
    }),

    "LU-N014": MappingProxyType({
        "en": (
            "invalid confidence level `{got}`.",
            "Valid levels: certain, high, medium, low, speculative.",
        ),
        "it": (
            "livello di confidence non valido `{got}`.",
            "Livelli validi: certain, high, medium, low, speculative.",
        ),
        "pt": (
            "nivel de certeza invalido `{got}`.",
            "Niveis validos: certain, high, medium, low, speculative.",
        ),
    }),

    # ------------------------------------------------------------------
    # LU-X - unknown / fallback
    # ------------------------------------------------------------------

    "LU-X001": MappingProxyType({
        "en": (
            "An unexpected error occurred in Lingua Universale.",
            "Check the technical details below for more information.",
        ),
        "it": (
            "Si e verificato un errore imprevisto in Lingua Universale.",
            "Controlla i dettagli tecnici di seguito per ulteriori informazioni.",
        ),
        "pt": (
            "Ocorreu um erro inesperado em Lingua Universale.",
            "Verifique os detalhes tecnicos abaixo para mais informacoes.",
        ),
    }),
})


# ============================================================
# ValueError substring matchers
# Maps substring patterns to (error_code, field_extractor_hint)
# ============================================================
#
# Order matters: more specific patterns first.
# Each entry is (substring, code).
# humanize() iterates this list and uses the FIRST match.

_VALUE_ERROR_MATCHERS: tuple[tuple[str, str], ...] = (
    # types.py - empty field patterns
    ("task_id cannot be empty", "LU-T001"),
    ("description cannot be empty", "LU-T001"),
    ("summary cannot be empty", "LU-T001"),
    ("audit_id cannot be empty", "LU-T001"),
    ("target cannot be empty", "LU-T001"),
    ("plan_id cannot be empty", "LU-T001"),
    ("task_description cannot be empty", "LU-T001"),
    ("query_id cannot be empty", "LU-T001"),
    ("topic cannot be empty", "LU-T001"),
    ("protocol_name cannot be empty", "LU-T001"),
    ("property_name cannot be empty", "LU-T001"),
    ("lean_theorem cannot be empty", "LU-T001"),
    ("lean_code cannot be empty", "LU-T001"),
    ("source cannot be empty", "LU-T001"),
    ("protocol name cannot be empty", "LU-T001"),
    ("agent_name cannot be empty", "LU-T001"),
    ("protocol_roles cannot be empty", "LU-T001"),
    ("checked items cannot be empty", "LU-T010"),
    # types.py - score/range patterns
    ("score must be 0.0-10.0", "LU-T002"),
    ("audit score must be 0.0-10.0", "LU-T009"),
    ("risk_score must be 0.0-1.0", "LU-T006"),
    ("summary must be <= 200", "LU-T003"),
    ("blockers required when status is BLOCKED", "LU-T004"),
    ("feedback required when rejecting", "LU-T005"),
    ("max_file_lines must be positive", "LU-T007"),
    ("min_sources must be positive", "LU-T007"),
    ("sources_consulted must be at least 1", "LU-T007"),
    ("files_affected cannot be negative", "LU-T008"),
    # protocols.py
    ("sender and receiver cannot be the same", "LU-P001"),
    ("sender cannot be empty", "LU-T001"),
    ("receiver cannot be empty", "LU-T001"),
    ("decider cannot be empty", "LU-T001"),
    ("branches cannot be empty", "LU-P002"),
    ("protocol must have at least 2 roles", "LU-P002"),
    ("duplicate roles:", "LU-P003"),
    ("max_repetitions must be at least 1", "LU-P004"),
    ("not in protocol roles", "LU-P005"),
    # lean4_bridge.py
    ("cannot create Lean 4 identifier from empty string", "LU-L001"),
    ("is not a valid Lean 4 identifier", "LU-L002"),
    ("duplicate protocol names", "LU-L006"),
    ("protocols cannot be empty", "LU-L005"),
    # codegen.py
    ("cannot create Python identifier from empty string", "LU-G001"),
    ("cannot be used as a Python identifier", "LU-G002"),
    ("protocol name cannot be used as Python identifier", "LU-G002"),
    # confidence.py
    ("confidence must be 0.0-1.0", "LU-C001"),
    ("cannot compose empty scores", "LU-C002"),
    # trust.py
    ("trust must be 0.0-1.0", "LU-C003"),
    ("attenuation factor must be 0.0-1.0", "LU-C004"),
    ("cannot compose empty trust chain", "LU-C005"),
    # integration.py
    ("binding role", "LU-A001"),
    ("unknown agent name", "LU-A002"),
    ("cannot play", "LU-A003"),
)


# ============================================================
# Public API
# ============================================================


def suggest_similar(
    got: str,
    valid_options: list[str],
    n: int = 3,
    cutoff: float = 0.6,
) -> tuple[str, ...]:
    """Suggest similar valid options using fuzzy matching.

    Uses ``difflib.get_close_matches()`` from the standard library
    (ZERO extra dependencies).

    Args:
        got:           The string the user provided.
        valid_options: List of valid alternatives to match against.
        n:             Maximum number of suggestions to return.
        cutoff:        Similarity threshold (0.0-1.0).

    Returns:
        A tuple of up to *n* similar strings from *valid_options*.
    """
    if not got or not valid_options:
        return ()
    matches = difflib.get_close_matches(got, valid_options, n=n, cutoff=cutoff)
    return tuple(matches)


def humanize(
    exc: Exception,
    locale: str = DEFAULT_LOCALE,
    context: Optional[dict[str, str]] = None,
) -> HumanError:
    """Translate any Lingua Universale exception to a human-friendly message.

    The chain of matchers (most specific first):
    1. C1 pipeline errors (TokenizeError, ParseError).
    2. Custom exception types (ProtocolViolation, SessionComplete,
       DSLParseError, SpecParseError, IntentParseError).
    3. ValueError message substring matching.
    4. RuntimeError / TimeoutError for Lean 4.
    5. Fallback: LU-X001.

    Args:
        exc:     The exception to translate.
        locale:  Target locale ("en", "it", "pt"). Falls back to "en".
        context: Optional extra substitution variables for message templates.

    Returns:
        A :class:`HumanError` with locale-appropriate messages.
    """
    # Validate and normalise locale
    _locale = locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE

    # Defensive copy of context (P11)
    _ctx: dict[str, str] = dict(context) if context else {}

    # ------------------------------------------------------------------
    # 1. Custom exception types
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # C1 pipeline: tokenizer errors
    # ------------------------------------------------------------------

    if isinstance(exc, TokenizeError):
        code, ctx_extra = _classify_tokenize_error(exc)
        loc = ErrorLocation(line=exc.line, col=exc.col, source="tokenizer")
        ctx_merged = {**_ctx, **ctx_extra}
        return _build(
            code=code,
            category=ErrorCategory.SYNTAX,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx=ctx_merged,
            got=ctx_extra.get("got"),
            expected=ctx_extra.get("expected"),
            location=loc,
        )

    # ------------------------------------------------------------------
    # C1 pipeline: parser errors
    # ------------------------------------------------------------------

    if isinstance(exc, ParseError):
        code, ctx_extra = _classify_parse_error(exc)
        loc = ErrorLocation(line=exc.line, col=exc.col, source="parser")
        ctx_merged = {**_ctx, **ctx_extra}
        similar = _parser_similar(code, ctx_extra.get("got", ""))
        return _build(
            code=code,
            category=ErrorCategory.SYNTAX,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx=ctx_merged,
            got=ctx_extra.get("got"),
            expected=ctx_extra.get("expected"),
            location=loc,
            similar=similar,
        )

    if isinstance(exc, SessionComplete):
        return _build(
            code="LU-R007",
            category=ErrorCategory.PROTOCOL,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx={**_ctx, "session": exc.session_id, "protocol": exc.protocol},
            got=exc.session_id,
        )

    if isinstance(exc, ProtocolViolation):
        code = _classify_protocol_violation(exc)
        loc = ErrorLocation(source="checker")
        return _build(
            code=code,
            category=ErrorCategory.PROTOCOL,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx={
                **_ctx,
                "step": str(exc.step),
                "expected": exc.expected,
                "got": exc.got,
                "session": exc.session_id,
                "protocol": exc.protocol,
            },
            got=exc.got,
            expected=exc.expected,
            location=loc,
        )

    if isinstance(exc, DSLParseError):
        code, ctx_extra = _classify_dsl_error(exc)
        loc = ErrorLocation(line=exc.line if exc.line else None, source="dsl")
        ctx_merged = {**_ctx, "line": str(exc.line), **ctx_extra}
        return _build(
            code=code,
            category=ErrorCategory.PARSE,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx=ctx_merged,
            got=ctx_extra.get("got"),
            expected=ctx_extra.get("expected"),
            location=loc,
            similar=_dsl_similar(code, ctx_extra.get("got", "")),
        )

    if isinstance(exc, SpecParseError):
        code, ctx_extra = _classify_spec_error(exc)
        loc = ErrorLocation(line=exc.line if exc.line else None, source="spec")
        ctx_merged = {**_ctx, "line": str(exc.line), **ctx_extra}
        return _build(
            code=code,
            category=ErrorCategory.PARSE,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx=ctx_merged,
            got=ctx_extra.get("got"),
            expected=ctx_extra.get("expected"),
            location=loc,
            similar=_spec_similar(code, ctx_extra.get("got", "")),
        )

    if isinstance(exc, IntentParseError):
        code, ctx_extra = _classify_intent_error(exc)
        loc = ErrorLocation(line=exc.line if exc.line else None, source="intent")
        ctx_merged = {**_ctx, "line": str(exc.line), **ctx_extra}
        return _build(
            code=code,
            category=ErrorCategory.PARSE,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx=ctx_merged,
            got=ctx_extra.get("got"),
            expected=ctx_extra.get("expected"),
            location=loc,
        )

    # ------------------------------------------------------------------
    # 2. ValueError - substring matching
    # ------------------------------------------------------------------

    if isinstance(exc, ValueError):
        msg = str(exc)
        for substring, code in _VALUE_ERROR_MATCHERS:
            if substring in msg:
                ctx_extra = _extract_value_error_ctx(msg, code)
                category = _category_for_code(code)
                return _build(
                    code=code,
                    category=category,
                    severity=ErrorSeverity.ERROR,
                    locale=_locale,
                    technical=msg,
                    ctx={**_ctx, **ctx_extra},
                    got=ctx_extra.get("got"),
                )
        # No match - use fallback
        return _build_fallback(_locale, str(exc), ErrorCategory.VALIDATION)

    # ------------------------------------------------------------------
    # 3. RuntimeError / TimeoutError for Lean 4
    # ------------------------------------------------------------------

    if isinstance(exc, TimeoutError):
        return _build(
            code="LU-L004",
            category=ErrorCategory.VERIFICATION,
            severity=ErrorSeverity.ERROR,
            locale=_locale,
            technical=str(exc),
            ctx=_ctx,
        )

    if isinstance(exc, RuntimeError):
        msg = str(exc)
        if "lean" in msg.lower() or "not installed" in msg.lower():
            return _build(
                code="LU-L003",
                category=ErrorCategory.VERIFICATION,
                severity=ErrorSeverity.ERROR,
                locale=_locale,
                technical=msg,
                ctx=_ctx,
            )
        return _build_fallback(_locale, msg, ErrorCategory.VERIFICATION)

    # ------------------------------------------------------------------
    # 4. Fallback
    # ------------------------------------------------------------------

    return _build_fallback(_locale, str(exc), ErrorCategory.VALIDATION)


def format_error(error: HumanError, verbose: bool = False, source: str = "") -> str:
    """Format a HumanError for terminal display.

    Output style is inspired by Elm and Rust compiler diagnostics:
    compact, actionable, and kind.

    Args:
        error:   The :class:`HumanError` to format.
        verbose: If True, include the original technical message.
        source:  Optional full source text for snippet rendering.

    Returns:
        A multi-line string ready for ``print()``.
    """
    lines: list[str] = []

    # Header line: [CODE] Short description
    lines.append(f"[{error.code}] {error.message}")

    # Location
    if error.location is not None:
        loc_parts: list[str] = []
        if error.location.line is not None:
            loc_parts.append(f"Line {error.location.line}")
        if error.location.col is not None:
            loc_parts.append(f"Col {error.location.col}")
        if loc_parts:
            lines.append(f"  {', '.join(loc_parts)}")

    # Source snippet
    if source and error.location and error.location.line:
        snippet = render_snippet(
            source,
            error.location.line,
            error.location.col or 0,
            label=error.message[:60] if len(error.message) > 60 else error.message,
        )
        if snippet:
            lines.append("")
            lines.append(snippet)
            lines.append("")

    # Got / expected
    if error.got is not None and error.expected is not None:
        lines.append(f"  Got:      {error.got}")
        lines.append(f"  Expected: {error.expected}")
    elif error.got is not None:
        lines.append(f"  Got: {error.got}")
    elif error.expected is not None:
        lines.append(f"  Expected: {error.expected}")

    # Fuzzy suggestions
    if error.similar:
        suggestions = ", ".join(error.similar)
        lines.append(f"  Did you mean: {suggestions}?")

    # Suggestion line
    if error.suggestion:
        lines.append(f"  Hint: {error.suggestion}")

    # Verbose: technical details
    if verbose and error.technical:
        lines.append(f"  [technical] {error.technical}")

    return "\n".join(lines)


# ============================================================
# Internal builders
# ============================================================


def _build(
    *,
    code: str,
    category: ErrorCategory,
    severity: ErrorSeverity,
    locale: str,
    technical: str,
    ctx: dict[str, str],
    got: Optional[str] = None,
    expected: Optional[str] = None,
    location: Optional[ErrorLocation] = None,
    similar: tuple[str, ...] = (),
) -> HumanError:
    """Build a HumanError from catalog entry + context dict."""
    entry = _CATALOG.get(code, _CATALOG["LU-X001"])
    locale_entry = entry.get(locale, entry.get(DEFAULT_LOCALE, ("", "")))
    msg_tmpl, sug_tmpl = locale_entry

    safe = _SafeDict(ctx)
    message = msg_tmpl.format_map(safe)
    suggestion = sug_tmpl.format_map(safe)

    return HumanError(
        code=code,
        category=category,
        severity=severity,
        locale=locale,
        message=message,
        suggestion=suggestion,
        technical=technical,
        location=location,
        got=got,
        expected=expected,
        similar=similar,
    )


def _build_fallback(
    locale: str,
    technical: str,
    category: ErrorCategory,
) -> HumanError:
    """Build a LU-X001 fallback error."""
    return _build(
        code="LU-X001",
        category=category,
        severity=ErrorSeverity.ERROR,
        locale=locale,
        technical=technical,
        ctx={},
    )


# ============================================================
# Classifiers for custom exception types
# ============================================================


def _classify_tokenize_error(exc: TokenizeError) -> tuple[str, dict[str, str]]:
    """Determine LU-N00X code from a TokenizeError."""
    raw = str(exc)
    msg = raw.split(": ", 1)[-1] if ": " in raw else raw

    if "tabs" in msg.lower() or "tab" in msg.lower():
        return "LU-N001", {}

    if "indentation must be" in msg:
        got = _extract_parenthesized(msg) or ""
        return "LU-N002", {"got": got}

    if "unterminated string" in msg:
        return "LU-N003", {}

    if "unexpected character" in msg:
        got = _extract_quoted(msg) or ""
        return "LU-N004", {"got": got}

    if "dedent" in msg:
        return "LU-N005", {}

    # Generic tokenizer error
    return "LU-N007", _extract_expected_got(msg)


_PARSE_EXACT: list[tuple[str, str, str]] = [
    # (substring, code, extractor_key)
    # extractor_key: "eg" = _extract_expected_got, "q" = _extract_quoted->got, "qm" = quoted or msg, "" = no ctx
    ("expected COLON", "LU-N008", "eg"),
    ("protocol must have at least one step", "LU-N009", ""),
    ("cannot parse action", "LU-N010", "qm"),
    ("unknown action", "LU-N010", "qm"),
    ("unknown property", "LU-N011", "q"),
    ("unknown agent clause", "LU-N012", "q"),
    ("invalid trust tier", "LU-N013", "q"),
    ("invalid confidence level", "LU-N014", "q"),
]


def _classify_parse_error(exc: ParseError) -> tuple[str, dict[str, str]]:
    """Determine LU-N00X code from a ParseError."""
    raw = str(exc)
    msg = raw.split(": ", 1)[-1] if ": " in raw else raw

    if "expected 'protocol'" in msg and "'agent'" in msg and "'type'" in msg:
        m = re.search(r"got\s+'([^']+)'", msg)
        got = m.group(1) if m else (_extract_quoted(msg) or "")
        return "LU-N006", {"got": got}

    for substr, code, ext in _PARSE_EXACT:
        if substr in msg:
            if ext == "eg":
                return code, _extract_expected_got(msg)
            if ext == "qm":
                return code, {"got": _extract_quoted(msg) or msg}
            if ext == "q":
                return code, {"got": _extract_quoted(msg) or ""}
            return code, {}

    return "LU-N007", _extract_expected_got(msg)


def _parser_similar(code: str, got: str) -> tuple[str, ...]:
    """Build fuzzy suggestions for parser errors."""
    if code == "LU-N006" and got:
        return suggest_similar(got, ["type", "agent", "protocol", "use"])
    if code == "LU-N010" and got:
        return suggest_similar(got, ["asks", "returns", "sends", "tells", "proposes"])
    if code == "LU-N011" and got:
        return suggest_similar(
            got, ["always terminates", "no deadlock", "all roles participate",
                  "confidence", "trust", "before", "cannot send"]
        )
    if code == "LU-N012" and got:
        return suggest_similar(
            got, ["role", "trust", "accepts", "produces", "requires", "ensures"]
        )
    if code == "LU-N013" and got:
        return suggest_similar(
            got, ["verified", "trusted", "standard", "untrusted"]
        )
    if code == "LU-N014" and got:
        return suggest_similar(
            got, ["certain", "high", "medium", "low", "speculative"]
        )
    return ()


def _classify_protocol_violation(exc: ProtocolViolation) -> str:
    """Determine LU-R00X code from the violation's expected/got strings."""
    expected = exc.expected
    got = exc.got

    if "not at a choice point" in got:
        return "LU-R004"
    if "branch selection" in expected:
        return "LU-R006"
    if expected.startswith("branch in"):
        return "LU-R005"
    if expected.startswith("sender="):
        return "LU-R001"
    if expected.startswith("receiver="):
        return "LU-R002"
    if expected.startswith("message="):
        return "LU-R003"
    # Default to generic protocol violation
    return "LU-R003"


def _classify_dsl_error(exc: DSLParseError) -> tuple[str, dict[str, str]]:
    """Determine LU-D00X code and context from a DSLParseError."""
    raw = str(exc)
    # Strip location prefix "line N, col M: ..."
    msg = raw.split(": ", 1)[-1] if ": " in raw else raw

    if "unexpected character" in msg:
        # e.g. "unexpected character: '@'"
        got = _extract_quoted(msg) or ""
        return "LU-D001", {"got": got}

    if "unknown message type" in msg or "unknown message kind" in msg:
        got = _extract_quoted(msg) or ""
        return "LU-D003", {"got": got}

    if "duplicate branch label" in msg:
        got = _extract_quoted(msg) or ""
        return "LU-D004", {"got": got}

    if "empty" in msg and ("choice" in msg or "branch" in msg):
        return "LU-D005", {}

    if "no protocols found" in msg:
        return "LU-D006", {}

    if "unexpected end of input" in msg:
        return "LU-D007", {}

    # Generic: expected X, got Y
    parts = _extract_expected_got(msg)
    return "LU-D002", parts


_SPEC_EXACT: list[tuple[str, str, str]] = [
    ("tabs are not allowed", "LU-S001", ""),
    ("indentation must be a multiple of 4", "LU-S002", "p"),
    ("unknown message kind", "LU-S003", "q"),
    ("unknown confidence level", "LU-S004", "q"),
    ("unknown trust tier", "LU-S005", "q"),
    ("a and b must differ", "LU-S006", ""),
    ("at least one property", "LU-S008", ""),
    ("must have at least one property", "LU-S008", ""),
]


def _classify_spec_error(exc: SpecParseError) -> tuple[str, dict[str, str]]:
    """Determine LU-S00X code and context from a SpecParseError."""
    raw = str(exc)
    msg = raw.split(": ", 1)[-1] if ": " in raw else raw

    if "ORDERING" in msg and "must differ" in msg:
        return "LU-S006", {}

    for substr, code, ext in _SPEC_EXACT:
        if substr in msg:
            if ext == "p":
                return code, {"got": _extract_parenthesized(msg) or ""}
            if ext == "q":
                return code, {"got": _extract_quoted(msg) or ""}
            return code, {}

    return "LU-S007", _extract_expected_got(msg)


def _classify_intent_error(exc: IntentParseError) -> tuple[str, dict[str, str]]:
    """Determine LU-I00X code and context from an IntentParseError."""
    raw = str(exc)
    msg = raw.split(": ", 1)[-1] if ": " in raw else raw

    if "tabs are not allowed" in msg:
        return "LU-I001", {}

    if "indentation must be a multiple of 4" in msg:
        got = _extract_parenthesized(msg) or ""
        return "LU-I002", {"got": got}

    if "expected indented 'roles'" in msg or "expected indented" in msg:
        return "LU-I004", {}

    if "cannot parse action" in msg or "unknown verb" in msg:
        got = _extract_quoted(msg) or msg
        return "LU-I003", {"got": got}

    # Generic
    parts = _extract_expected_got(msg)
    return "LU-I005", parts


# ============================================================
# Context extractors
# ============================================================


def _extract_quoted(text: str) -> Optional[str]:
    """Extract first single- or double-quoted token from text."""
    m = re.search(r"['\"]([^'\"]+)['\"]", text)
    return m.group(1) if m else None


def _extract_parenthesized(text: str) -> Optional[str]:
    """Extract first parenthesized number from text, e.g. '(got 6)'."""
    m = re.search(r"\(got\s+([^\)]+)\)", text)
    if m:
        return m.group(1)
    # Fallback: any number in parentheses
    m2 = re.search(r"\((\d+)\)", text)
    return m2.group(1) if m2 else None


def _extract_expected_got(text: str) -> dict[str, str]:
    """Extract 'expected X, got Y' substrings from an error message."""
    result: dict[str, str] = {}
    m_exp = re.search(r"expected\s+([^,]+)", text)
    if m_exp:
        result["expected"] = m_exp.group(1).strip()
    m_got = re.search(r"got\s+(.+?)(?:\s*$|\s*\()", text)
    if m_got:
        result["got"] = m_got.group(1).strip()
    return result


def _extract_value_error_ctx(msg: str, code: str) -> dict[str, str]:
    """Extract substitution context from a ValueError message string."""
    ctx: dict[str, str] = {}

    # Pattern: "X cannot be empty" -> field = X
    m_empty = re.match(r"(\w+) cannot be empty", msg)
    if m_empty:
        ctx["field"] = m_empty.group(1)
        return ctx

    # Pattern: "... must be ..., got N" or similar
    m_got = re.search(r"got\s+([\d.\-]+)", msg)
    if m_got:
        ctx["got"] = m_got.group(1)

    # Pattern: "X must be positive" -> field
    m_pos = re.match(r"(\w+) must be positive", msg)
    if m_pos:
        ctx["field"] = m_pos.group(1)

    # Pattern: "X cannot be negative, got N" -> field
    m_neg = re.match(r"(\w+) cannot be negative", msg)
    if m_neg:
        ctx["field"] = m_neg.group(1)

    # Pattern: "sender and receiver cannot be the same: 'X'"
    m_same = re.search(r"cannot be the same:\s*'([^']+)'", msg)
    if m_same:
        ctx["got"] = m_same.group(1)

    # Pattern: "duplicate roles: [...]"
    m_dup = re.search(r"duplicate roles:\s*(.+)", msg)
    if m_dup:
        ctx["got"] = m_dup.group(1).strip()

    # Pattern: "'X' not in protocol roles"
    m_role = re.search(r"'([^']+)' not in protocol roles", msg)
    if m_role:
        ctx["got"] = m_role.group(1)

    # Pattern: "unknown agent name 'X'"
    m_agent = re.search(r"unknown agent name '([^']+)'", msg)
    if m_agent:
        ctx["got"] = m_agent.group(1)

    # Pattern: "binding role 'X' not in"
    m_binding = re.search(r"binding role '([^']+)'", msg)
    if m_binding:
        ctx["got"] = m_binding.group(1)

    # Pattern: "agent 'X' ... cannot play"
    m_play = re.search(r"agent '([^']+)'.*cannot play", msg)
    if m_play:
        ctx["got"] = m_play.group(1)

    # Pattern: "duplicate protocol names ... (X)"
    m_dup_p = re.search(r"duplicate.*names.*:?\s*(.+)", msg)
    if m_dup_p and code == "LU-L006":
        ctx["got"] = m_dup_p.group(1).strip()

    # Pattern: "'X' cannot be used as a Python identifier"
    m_pyid = re.search(r"'([^']+)' cannot be used as a Python identifier", msg)
    if m_pyid:
        ctx["got"] = m_pyid.group(1)

    return ctx


# ============================================================
# Fuzzy suggestion helpers
# ============================================================

_VALID_MESSAGE_KINDS: tuple[str, ...] = (
    "task_request", "task_result", "audit_request", "audit_verdict",
    "plan_request", "plan_proposal", "plan_decision",
    "research_query", "research_report",
    "dm", "broadcast", "shutdown_request", "shutdown_ack", "context_inject",
)

_VALID_PASCAL_MESSAGE_KINDS: tuple[str, ...] = (
    "TaskRequest", "TaskResult", "AuditRequest", "AuditVerdict",
    "PlanRequest", "PlanProposal", "PlanDecision",
    "ResearchQuery", "ResearchReport",
    "DirectMessage", "Broadcast", "ShutdownRequest", "ShutdownAck",
    "ContextInject",
)


def _dsl_similar(code: str, got: str) -> tuple[str, ...]:
    """Build fuzzy suggestions for DSL errors."""
    if code == "LU-D003" and got:
        return suggest_similar(got, list(_VALID_PASCAL_MESSAGE_KINDS))
    return ()


def _spec_similar(code: str, got: str) -> tuple[str, ...]:
    """Build fuzzy suggestions for spec errors."""
    if code == "LU-S003" and got:
        return suggest_similar(got, list(_VALID_MESSAGE_KINDS))
    if code == "LU-S004" and got:
        return suggest_similar(
            got, ["certain", "high", "medium", "low", "speculative"]
        )
    if code == "LU-S005" and got:
        return suggest_similar(
            got, ["verified", "trusted", "standard", "untrusted"]
        )
    return ()


# ============================================================
# Category lookup helper
# ============================================================

_CODE_CATEGORY: MappingProxyType = MappingProxyType({
    "LU-T": ErrorCategory.VALIDATION,
    "LU-P": ErrorCategory.VALIDATION,
    "LU-R": ErrorCategory.PROTOCOL,
    "LU-D": ErrorCategory.PARSE,
    "LU-S": ErrorCategory.PARSE,
    "LU-I": ErrorCategory.PARSE,
    "LU-L": ErrorCategory.VERIFICATION,
    "LU-G": ErrorCategory.CODEGEN,
    "LU-C": ErrorCategory.CONFIDENCE,
    "LU-A": ErrorCategory.INTEGRATION,
    "LU-N": ErrorCategory.SYNTAX,
    "LU-X": ErrorCategory.VALIDATION,
})


def _category_for_code(code: str) -> ErrorCategory:
    """Return the ErrorCategory for a given error code."""
    prefix = code[:4]  # "LU-T", "LU-P", etc.
    return _CODE_CATEGORY.get(prefix, ErrorCategory.VALIDATION)
