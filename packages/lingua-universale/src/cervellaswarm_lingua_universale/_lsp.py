# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Language Server Protocol implementation for Lingua Universale (D2).

Provides real-time diagnostics (error reporting) in editors via LSP.
Uses pygls v2 as an optional dependency (``pip install cervellaswarm-lingua-universale[lsp]``).

Architecture:
    - textDocument/didOpen + didChange + didSave -> validate -> publish diagnostics
    - parse() -> catch TokenizeError | ParseError -> humanize() -> LSP Diagnostic
    - STDIO transport (launched via ``lu lsp``)

Coordinate mapping:
    - Lingua Universale: line is 1-indexed, col is 0-indexed
    - LSP Protocol:      line is 0-indexed, character is 0-indexed
    - Conversion:        lsp_line = lu_line - 1, lsp_char = lu_col
"""

from __future__ import annotations

import logging
import sys

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
        filename="/tmp/lu-lsp.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    logger.info("Starting Lingua Universale LSP server (STDIO)")

    server = create_server()
    server.start_io()

    return 0
