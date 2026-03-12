# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Language Server Protocol implementation for Lingua Universale (D2 + D5).

Provides real-time diagnostics, hover, completion, and go-to-definition
in editors via LSP.
Uses pygls v2 as an optional dependency (``pip install cervellaswarm-lingua-universale[lsp]``).

Architecture (D2 - diagnostics):
    - textDocument/didOpen + didChange + didSave -> validate -> publish diagnostics
    - parse() -> catch TokenizeError | ParseError -> humanize() -> LSP Diagnostic
    - STDIO transport (launched via ``lu lsp``)

Architecture (D5 - advanced):
    - Symbol table built from AST on each parse (fast <5ms for typical .lu files)
    - Hover: token at cursor -> symbol table lookup -> Markdown content
    - Completion: context-aware (top-level keywords, agent clauses, trust tiers, etc.)
    - Go-to-definition: token at cursor -> symbol table -> definition Location
    - Pure functions separated from server handlers for testability

Coordinate mapping:
    - Lingua Universale: line is 1-indexed, col is 0-indexed
    - LSP Protocol:      line is 0-indexed, character is 0-indexed
    - Conversion:        lsp_line = lu_line - 1, lsp_char = lu_col
"""

from __future__ import annotations

import logging
import os
import re
import sys
import tempfile
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def _check_pygls_available() -> bool:
    """Check if pygls is installed."""
    try:
        import pygls  # noqa: F401
        return True
    except ImportError:
        return False


def _source_diagnostics(source: str) -> list:
    """Parse LU source and return a list of LSP Diagnostic objects.

    This is the core validation function, separated for testability.
    Returns an empty list if the source is valid.
    """
    from lsprotocol import types

    from ._parser import parse, ParseError
    from ._tokenizer import TokenizeError
    from .errors import humanize, ErrorSeverity

    diagnostics: list[types.Diagnostic] = []

    try:
        parse(source)
    except (TokenizeError, ParseError) as exc:
        # Humanize for rich error info (code, message, suggestion)
        try:
            herr = humanize(exc)
        except Exception:
            # Fallback if humanize fails
            herr = None

        # Extract location (1-indexed line, 0-indexed col)
        lu_line = getattr(exc, "line", 0) or 0
        lu_col = getattr(exc, "col", 0) or 0

        # Convert to LSP 0-indexed coordinates
        lsp_line = max(0, lu_line - 1)
        lsp_char = max(0, lu_col)

        # Build message
        if herr:
            msg_parts = [herr.message]
            if herr.suggestion:
                msg_parts.append(herr.suggestion)
            message = "\n".join(msg_parts)
            code = herr.code
            severity = (
                types.DiagnosticSeverity.Warning
                if herr.severity == ErrorSeverity.WARNING
                else types.DiagnosticSeverity.Error
            )
        else:
            message = str(exc)
            code = None
            severity = types.DiagnosticSeverity.Error

        diagnostics.append(
            types.Diagnostic(
                range=types.Range(
                    start=types.Position(line=lsp_line, character=lsp_char),
                    end=types.Position(line=lsp_line, character=lsp_char + 1),
                ),
                message=message,
                severity=severity,
                source="lingua-universale",
                code=code,
            )
        )
    except Exception as exc:
        # Catch-all for unexpected errors -- still report them
        diagnostics.append(
            types.Diagnostic(
                range=types.Range(
                    start=types.Position(line=0, character=0),
                    end=types.Position(line=0, character=1),
                ),
                message=f"Internal error: {exc}",
                severity=types.DiagnosticSeverity.Error,
                source="lingua-universale",
            )
        )

    return diagnostics


# ---------------------------------------------------------------------------
# D5: Symbol table
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SymbolEntry:
    """A symbol extracted from the AST for hover/completion/go-to-def."""

    name: str
    kind: str    # "variant_type" | "record_type" | "agent" | "protocol" | "module"
    loc: tuple[int, int]  # (line 1-indexed, col 0-indexed) -- plain tuple to avoid Loc import at top
    detail: str  # one-line summary
    doc: str     # Markdown hover content


def _type_expr_str(te) -> str:
    """Convert a TypeExpr AST node to a human-readable string."""
    from ._ast import SimpleType, GenericType

    if isinstance(te, SimpleType):
        return te.name + ("?" if te.optional else "")
    if isinstance(te, GenericType):
        return f"{te.name}[{_type_expr_str(te.arg)}]" + ("?" if te.optional else "")
    return str(te)  # pragma: no cover


def _regex_extract_symbols(source: str) -> dict[str, SymbolEntry]:
    """Fallback symbol extraction using regex for incomplete source.

    When the parser fails (user is typing), extract what we can from
    the raw text. Used primarily for completion in incomplete files.
    """
    table: dict[str, SymbolEntry] = {}

    for m in re.finditer(r"^type\s+(\w+)\s*=\s*(.+)$", source, re.MULTILINE):
        name = m.group(1)
        rest = m.group(2).strip()
        line_no = source[:m.start()].count("\n") + 1
        if "|" in rest:
            table[name] = SymbolEntry(
                name=name, kind="variant_type", loc=(line_no, 0),
                detail=f"type {name} = {rest}",
                doc=f"**type {name}** (variant)\n\n{rest}",
            )
        else:
            table[name] = SymbolEntry(
                name=name, kind="record_type", loc=(line_no, 0),
                detail=f"type {name}", doc=f"**type {name}** (record)",
            )

    for m in re.finditer(r"^agent\s+(\w+)\s*:", source, re.MULTILINE):
        name = m.group(1)
        line_no = source[:m.start()].count("\n") + 1
        table[name] = SymbolEntry(
            name=name, kind="agent", loc=(line_no, 0),
            detail=f"agent {name}", doc=f"**agent {name}**",
        )

    for m in re.finditer(r"^protocol\s+(\w+)\s*:", source, re.MULTILINE):
        name = m.group(1)
        line_no = source[:m.start()].count("\n") + 1
        table[name] = SymbolEntry(
            name=name, kind="protocol", loc=(line_no, 0),
            detail=f"protocol {name}", doc=f"**protocol {name}**",
        )

    for m in re.finditer(r"^use\s+python\s+([\w.]+)", source, re.MULTILINE):
        module = m.group(1)
        alias = module.split(".")[-1]
        line_no = source[:m.start()].count("\n") + 1
        table[alias] = SymbolEntry(
            name=alias, kind="module", loc=(line_no, 0),
            detail=f"use python {module}",
            doc=f"**use** python {module}\n\nPython module import",
        )

    return table


def _symbol_from_variant(decl, loc: tuple[int, int]) -> dict[str, SymbolEntry]:
    """Build symbol entries for a VariantTypeDecl (type + variant members)."""
    entries: dict[str, SymbolEntry] = {}
    variants_str = " | ".join(decl.variants)
    entries[decl.name] = SymbolEntry(
        name=decl.name,
        kind="variant_type",
        loc=loc,
        detail=f"type {decl.name} = {variants_str}",
        doc=f"**type {decl.name}** (variant)\n\n{variants_str}",
    )
    for v in decl.variants:
        entries[v] = SymbolEntry(
            name=v,
            kind="variant_member",
            loc=loc,
            detail=f"variant of {decl.name}",
            doc=f"Variant `{v}` of type `{decl.name}`",
        )
    return entries


def _symbol_from_record(decl, loc: tuple[int, int]) -> dict[str, SymbolEntry]:
    """Build symbol entry for a RecordTypeDecl."""
    fields = [(f.name, _type_expr_str(f.type_expr)) for f in decl.fields]
    fields_inline = ", ".join(f"{n}: {t}" for n, t in fields)
    fields_doc = "\n".join(f"- `{n}`: {t}" for n, t in fields)
    return {
        decl.name: SymbolEntry(
            name=decl.name,
            kind="record_type",
            loc=loc,
            detail=f"type {decl.name} = {{ {fields_inline} }}",
            doc=f"**type {decl.name}** (record)\n\n{fields_doc}",
        )
    }


def _symbol_from_agent(decl, loc: tuple[int, int]) -> dict[str, SymbolEntry]:
    """Build symbol entry for an AgentNode."""
    role = decl.role or "?"
    trust = decl.trust or "?"
    parts = [f"**agent {decl.name}**\n", f"role: {role} | trust: {trust}"]
    if decl.accepts:
        parts.append(f"accepts: {', '.join(decl.accepts)}")
    if decl.produces:
        parts.append(f"produces: {', '.join(decl.produces)}")
    return {
        decl.name: SymbolEntry(
            name=decl.name,
            kind="agent",
            loc=loc,
            detail=f"agent {decl.name} (role: {role}, trust: {trust})",
            doc="\n".join(parts),
        )
    }


def _symbol_from_protocol(decl, loc: tuple[int, int]) -> dict[str, SymbolEntry]:
    """Build symbol entries for a ProtocolNode (protocol + roles)."""
    from ._ast import AlwaysTerminates, NoDeadlock, AllParticipate

    entries: dict[str, SymbolEntry] = {}
    roles_str = ", ".join(decl.roles)
    props = []
    for p in decl.properties:
        if isinstance(p, AlwaysTerminates):
            props.append("always terminates")
        elif isinstance(p, NoDeadlock):
            props.append("no deadlock")
        elif isinstance(p, AllParticipate):
            props.append("all roles participate")
    parts = [f"**protocol {decl.name}**\n", f"roles: {roles_str}", f"steps: {len(decl.steps)}"]
    if props:
        parts.append(f"properties: {', '.join(props)}")
    entries[decl.name] = SymbolEntry(
        name=decl.name,
        kind="protocol",
        loc=loc,
        detail=f"protocol {decl.name} (roles: {roles_str})",
        doc="\n".join(parts),
    )
    for role_name in decl.roles:
        entries[role_name] = SymbolEntry(
            name=role_name,
            kind="role",
            loc=loc,
            detail=f"role in {decl.name}",
            doc=f"Role `{role_name}` in protocol `{decl.name}`",
        )
    return entries


def build_symbol_table(source: str) -> dict[str, SymbolEntry]:
    """Parse LU source and build a symbol table from all declarations.

    Returns an empty dict if the source has parse errors.
    This is a pure function, separated from the server for testability.
    """
    from ._parser import parse, ParseError
    from ._tokenizer import TokenizeError
    from ._ast import VariantTypeDecl, RecordTypeDecl, AgentNode, ProtocolNode, UseNode

    try:
        program = parse(source)
    except (TokenizeError, ParseError, Exception):
        return _regex_extract_symbols(source)

    table: dict[str, SymbolEntry] = {}

    for decl in program.declarations:
        loc = (decl.loc.line, decl.loc.col)

        if isinstance(decl, VariantTypeDecl):
            table.update(_symbol_from_variant(decl, loc))
        elif isinstance(decl, RecordTypeDecl):
            table.update(_symbol_from_record(decl, loc))
        elif isinstance(decl, AgentNode):
            table.update(_symbol_from_agent(decl, loc))
        elif isinstance(decl, ProtocolNode):
            entries = _symbol_from_protocol(decl, loc)
            for name, entry in entries.items():
                if entry.kind == "role" and name in table:
                    continue
                table[name] = entry
        elif isinstance(decl, UseNode):
            alias = decl.alias or decl.module.split(".")[-1]
            table[alias] = SymbolEntry(
                name=alias,
                kind="module",
                loc=loc,
                detail=f"use python {decl.module}" + (f" as {decl.alias}" if decl.alias else ""),
                doc=f"**use** python {decl.module}\n\nPython module import",
            )

    return table


# ---------------------------------------------------------------------------
# D5: Word-at-position helper
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _word_at_pos(source: str, line: int, character: int) -> tuple[str, int, int] | None:
    """Find the identifier at the given LSP position (0-indexed line and character).

    Returns (word, start_col, end_col) or None if no word at that position.
    """
    lines = source.splitlines()
    if line < 0 or line >= len(lines):
        return None
    text = lines[line]
    if character < 0 or character > len(text):
        return None
    # Find all words on this line and check if cursor is inside one
    for m in _WORD_RE.finditer(text):
        if m.start() <= character <= m.end():
            return (m.group(), m.start(), m.end())
    return None


# ---------------------------------------------------------------------------
# D5: Hover (pure function)
# ---------------------------------------------------------------------------


def _hover_info(source: str, line: int, character: int) -> tuple[str, int, int, int] | None:
    """Pure function: source + LSP position -> hover info.

    Returns (markdown, line, start_char, end_char) or None.
    """
    word_info = _word_at_pos(source, line, character)
    if not word_info:
        return None
    word, start_col, end_col = word_info

    table = build_symbol_table(source)
    entry = table.get(word)
    if not entry:
        return None

    return (entry.doc, line, start_col, end_col)


# ---------------------------------------------------------------------------
# D5: Go-to-definition (pure function)
# ---------------------------------------------------------------------------


def _goto_definition(source: str, line: int, character: int) -> tuple[int, int, int] | None:
    """Pure function: source + LSP position -> definition location.

    Returns (def_line_0indexed, def_col, name_len) or None.
    """
    word_info = _word_at_pos(source, line, character)
    if not word_info:
        return None
    word, _, _ = word_info

    table = build_symbol_table(source)
    entry = table.get(word)
    if not entry:
        return None

    # Convert LU 1-indexed line to LSP 0-indexed
    def_line = entry.loc[0] - 1
    def_col = entry.loc[1]
    return (def_line, def_col, len(entry.name))


# ---------------------------------------------------------------------------
# D5: Completion (pure function)
# ---------------------------------------------------------------------------

_TOP_LEVEL_KEYWORDS = [
    ("type", "Define a type (variant or record)"),
    ("agent", "Define an AI agent"),
    ("protocol", "Define a communication protocol"),
    ("use", "Import a Python module"),
]

_AGENT_CLAUSES = [
    ("role:", "Agent role (e.g. backend, guardiana)"),
    ("trust:", "Trust tier"),
    ("accepts:", "Message types this agent accepts"),
    ("produces:", "Message types this agent produces"),
    ("requires:", "Pre-conditions"),
    ("ensures:", "Post-conditions"),
]

_TRUST_TIERS = ["verified", "trusted", "standard", "untrusted"]

_CONFIDENCE_LEVELS = ["certain", "high", "medium", "low", "speculative"]

_PROPERTY_KEYWORDS = [
    ("always terminates", "Protocol always reaches completion"),
    ("no deadlock", "No deadlock possible"),
    ("all roles participate", "Every role sends at least one message"),
]

_ACTION_VERBS = ["asks", "returns", "tells", "proposes", "sends"]


def _completion_items(source: str, line: int, character: int) -> list:
    """Pure function: source + LSP position -> list of CompletionItem dicts.

    Returns a list of dicts with keys: label, kind, detail, insert_text, doc.
    The server handler converts these to lsprotocol CompletionItem objects.
    """
    lines = source.splitlines()
    if line < 0 or line >= len(lines):
        # Empty file or past end -> top-level keywords + defined names
        result = [{"label": kw, "kind": "keyword", "detail": desc}
                  for kw, desc in _TOP_LEVEL_KEYWORDS]
        table = build_symbol_table(source)
        for entry in table.values():
            if entry.kind in ("variant_type", "record_type", "agent", "protocol"):
                result.append({"label": entry.name, "kind": entry.kind, "detail": entry.detail})
        return result

    current_line = lines[line]
    text_before = current_line[:character].lstrip()
    indent = len(current_line) - len(current_line.lstrip())

    # Detect context by scanning backwards
    context = _detect_completion_context(lines, line, indent, text_before)

    items: list[dict] = []

    if context == "top_level":
        for kw, desc in _TOP_LEVEL_KEYWORDS:
            items.append({"label": kw, "kind": "keyword", "detail": desc})
        # Also suggest defined names
        table = build_symbol_table(source)
        for entry in table.values():
            if entry.kind in ("variant_type", "record_type", "agent", "protocol"):
                items.append({"label": entry.name, "kind": entry.kind, "detail": entry.detail})

    elif context == "agent_body":
        for clause, desc in _AGENT_CLAUSES:
            items.append({"label": clause, "kind": "property", "detail": desc})

    elif context == "trust_value":
        for tier in _TRUST_TIERS:
            items.append({"label": tier, "kind": "value", "detail": f"Trust: {tier}"})

    elif context == "confidence_value":
        for level in _CONFIDENCE_LEVELS:
            items.append({"label": level, "kind": "value", "detail": f"Confidence: {level}"})

    elif context == "protocol_body":
        # Suggest action verbs and defined role names
        for verb in _ACTION_VERBS:
            items.append({"label": verb, "kind": "keyword", "detail": f"Step action: {verb}"})
        table = build_symbol_table(source)
        for entry in table.values():
            if entry.kind == "role":
                items.append({"label": entry.name, "kind": "role", "detail": entry.detail})

    elif context == "properties_body":
        for prop, desc in _PROPERTY_KEYWORDS:
            items.append({"label": prop, "kind": "keyword", "detail": desc})

    elif context == "type_ref":
        # After accepts:/produces:/field type -> suggest defined type names
        table = build_symbol_table(source)
        for entry in table.values():
            if entry.kind in ("variant_type", "record_type"):
                items.append({"label": entry.name, "kind": entry.kind, "detail": entry.detail})

    else:
        # Fallback: top-level keywords + all defined names
        for kw, desc in _TOP_LEVEL_KEYWORDS:
            items.append({"label": kw, "kind": "keyword", "detail": desc})
        table = build_symbol_table(source)
        for entry in table.values():
            if entry.kind not in ("variant_member", "role"):
                items.append({"label": entry.name, "kind": entry.kind, "detail": entry.detail})

    return items


def _detect_completion_context(
    lines: list[str], current_line: int, indent: int, text_before: str,
) -> str:
    """Detect the completion context by analyzing the current line and surroundings."""
    # Trust value: "trust: " at cursor
    if re.match(r"trust:\s*$", text_before):
        return "trust_value"

    # Confidence value: "confidence >= " at cursor
    if re.match(r"confidence\s*>=\s*$", text_before):
        return "confidence_value"

    # Type reference: after "accepts:", "produces:" (including after comma for multiple types)
    if re.match(r"(accepts|produces):\s*(\w+\s*,\s*)*$", text_before):
        return "type_ref"

    # Top level: no indent
    if indent == 0 and not text_before:
        return "top_level"

    # Scan backwards to find enclosing block
    for i in range(current_line - 1, -1, -1):
        line = lines[i].rstrip()
        line_indent = len(line) - len(line.lstrip())
        stripped = line.lstrip()

        if line_indent < indent:
            # Found a less-indented line = potential block header
            if stripped.startswith("agent ") and stripped.endswith(":"):
                return "agent_body"
            if stripped.startswith("protocol ") and stripped.endswith(":"):
                return "protocol_body"
            if stripped == "properties:":
                return "properties_body"
            break

    if indent == 0:
        return "top_level"

    return "unknown"


def create_server():
    """Create and configure the Lingua Universale language server.

    Returns a pygls LanguageServer instance ready to be started.
    """
    from lsprotocol import types
    from pygls.lsp.server import LanguageServer

    from . import __version__

    server = LanguageServer(
        name="lingua-universale-lsp",
        version=__version__,
    )

    def _validate_and_publish(ls: LanguageServer, uri: str, source: str, version: int | None = None) -> None:
        """Validate source and publish diagnostics."""
        diagnostics = _source_diagnostics(source)
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=uri,
                version=version,
                diagnostics=diagnostics,
            )
        )

    @server.feature(types.TEXT_DOCUMENT_DID_OPEN)
    def did_open(ls: LanguageServer, params: types.DidOpenTextDocumentParams) -> None:
        """Validate document on open."""
        doc = ls.workspace.get_text_document(params.text_document.uri)
        _validate_and_publish(ls, doc.uri, doc.source, doc.version)

    @server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
    def did_change(ls: LanguageServer, params: types.DidChangeTextDocumentParams) -> None:
        """Validate document on change."""
        doc = ls.workspace.get_text_document(params.text_document.uri)
        _validate_and_publish(ls, doc.uri, doc.source, doc.version)

    @server.feature(types.TEXT_DOCUMENT_DID_SAVE)
    def did_save(ls: LanguageServer, params: types.DidSaveTextDocumentParams) -> None:
        """Validate document on save."""
        doc = ls.workspace.get_text_document(params.text_document.uri)
        _validate_and_publish(ls, doc.uri, doc.source, doc.version)

    @server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
    def did_close(ls: LanguageServer, params: types.DidCloseTextDocumentParams) -> None:
        """Clear diagnostics when document is closed."""
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=params.text_document.uri,
                diagnostics=[],
            )
        )

    # ---------------------------------------------------------------
    # D5: Hover
    # ---------------------------------------------------------------

    @server.feature(types.TEXT_DOCUMENT_HOVER)
    def hover(ls: LanguageServer, params: types.HoverParams) -> types.Hover | None:
        """Show type/agent/protocol info on hover."""
        doc = ls.workspace.get_text_document(params.text_document.uri)
        result = _hover_info(doc.source, params.position.line, params.position.character)
        if not result:
            return None
        markdown, line, start_col, end_col = result
        return types.Hover(
            contents=types.MarkupContent(
                kind=types.MarkupKind.Markdown,
                value=markdown,
            ),
            range=types.Range(
                start=types.Position(line=line, character=start_col),
                end=types.Position(line=line, character=end_col),
            ),
        )

    # ---------------------------------------------------------------
    # D5: Go-to-definition
    # ---------------------------------------------------------------

    @server.feature(types.TEXT_DOCUMENT_DEFINITION)
    def goto_def(ls: LanguageServer, params: types.DefinitionParams) -> types.Location | None:
        """Jump to the definition of a type, agent, or protocol."""
        doc = ls.workspace.get_text_document(params.text_document.uri)
        result = _goto_definition(doc.source, params.position.line, params.position.character)
        if not result:
            return None
        def_line, def_col, name_len = result
        return types.Location(
            uri=params.text_document.uri,
            range=types.Range(
                start=types.Position(line=def_line, character=def_col),
                end=types.Position(line=def_line, character=def_col + name_len),
            ),
        )

    # ---------------------------------------------------------------
    # D5: Completion
    # ---------------------------------------------------------------

    @server.feature(
        types.TEXT_DOCUMENT_COMPLETION,
        types.CompletionOptions(trigger_characters=[":", " "]),
    )
    def completion(ls: LanguageServer, params: types.CompletionParams) -> types.CompletionList:
        """Context-aware code completion."""
        doc = ls.workspace.get_text_document(params.text_document.uri)
        raw_items = _completion_items(doc.source, params.position.line, params.position.character)

        _KIND_MAP = {
            "keyword": types.CompletionItemKind.Keyword,
            "variant_type": types.CompletionItemKind.Enum,
            "record_type": types.CompletionItemKind.Class,
            "agent": types.CompletionItemKind.Class,
            "protocol": types.CompletionItemKind.Interface,
            "module": types.CompletionItemKind.Module,
            "property": types.CompletionItemKind.Property,
            "value": types.CompletionItemKind.Value,
            "role": types.CompletionItemKind.Variable,
            "variant_member": types.CompletionItemKind.EnumMember,
        }

        lsp_items = []
        for item in raw_items:
            lsp_items.append(
                types.CompletionItem(
                    label=item["label"],
                    kind=_KIND_MAP.get(item.get("kind", ""), types.CompletionItemKind.Text),
                    detail=item.get("detail", ""),
                )
            )

        return types.CompletionList(is_incomplete=False, items=lsp_items)

    return server


def start_lsp() -> int:
    """Start the language server via STDIO.

    Called by ``lu lsp``. Returns exit code.
    """
    if not _check_pygls_available():
        print(
            "Error: pygls is not installed.\n"
            "Install LSP support with: pip install cervellaswarm-lingua-universale[lsp]",
            file=sys.stderr,
        )
        return 1

    # Configure logging to file (CRITICAL: never write to stdout in STDIO mode)
    logging.basicConfig(
        filename=os.path.join(tempfile.gettempdir(), "lu-lsp.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    logger.info("Starting Lingua Universale LSP server (STDIO)")

    server = create_server()
    server.start_io()

    return 0
