# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the unified Lingua Universale tokenizer.

Groups:
    1. TestBasicTokens        - individual token kinds
    2. TestIndentDedent       - indent stack, INDENT/DEDENT emission
    3. TestParenDepth         - line-continuation suppression
    4. TestCommentsAndBlanks  - comment and blank-line handling
    5. TestTokenizeErrors     - error cases with correct line/col
    6. TestCanonicalExamples  - all 10 design-document examples

NOTE: No __init__.py in this directory (Package Shadowing Fix).
"""

import pytest

from cervellaswarm_lingua_universale._tokenizer import (
    Tok,
    TokKind,
    TokenizeError,
    tokenize,
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def kinds(toks: list[Tok]) -> list[TokKind]:
    """Return only the kinds from a token list."""
    return [t.kind for t in toks]


def values(toks: list[Tok]) -> list[str]:
    """Return only the values from a token list."""
    return [t.value for t in toks]


def assert_indent_dedent_balanced(tokens: list[Tok]) -> None:
    """Every INDENT must have a matching DEDENT before EOF."""
    depth = 0
    for tok in tokens:
        if tok.kind == TokKind.INDENT:
            depth += 1
        elif tok.kind == TokKind.DEDENT:
            depth -= 1
            assert depth >= 0, (
                f"DEDENT without matching INDENT at line {tok.line}"
            )
    assert depth == 0, f"Unmatched INDENT: {depth} level(s) still open at EOF"


# ---------------------------------------------------------------------------
# Group 1: Basic Tokens
# ---------------------------------------------------------------------------


class TestBasicTokens:
    def test_ident_simple(self):
        toks = tokenize("hello")
        assert kinds(toks) == [TokKind.IDENT, TokKind.NEWLINE, TokKind.EOF]
        assert toks[0].value == "hello"

    def test_ident_with_underscore(self):
        toks = tokenize("my_var")
        assert toks[0].kind == TokKind.IDENT
        assert toks[0].value == "my_var"

    def test_ident_with_digits(self):
        toks = tokenize("var123")
        assert toks[0].kind == TokKind.IDENT
        assert toks[0].value == "var123"

    def test_ident_leading_underscore(self):
        toks = tokenize("_private")
        assert toks[0].kind == TokKind.IDENT
        assert toks[0].value == "_private"

    def test_number_integer(self):
        toks = tokenize("42")
        assert toks[0].kind == TokKind.NUMBER
        assert toks[0].value == "42"

    def test_number_float(self):
        toks = tokenize("3.14")
        assert toks[0].kind == TokKind.NUMBER
        assert toks[0].value == "3.14"

    def test_number_zero(self):
        toks = tokenize("0")
        assert toks[0].kind == TokKind.NUMBER
        assert toks[0].value == "0"

    def test_string_double_quote(self):
        toks = tokenize('"hello"')
        assert toks[0].kind == TokKind.STRING
        assert toks[0].value == '"hello"'

    def test_string_single_quote(self):
        toks = tokenize("'world'")
        assert toks[0].kind == TokKind.STRING
        assert toks[0].value == "'world'"

    def test_colon(self):
        toks = tokenize(":")
        assert kinds(toks) == [TokKind.COLON, TokKind.NEWLINE, TokKind.EOF]

    def test_comma(self):
        toks = tokenize("a, b")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.COMMA,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_all_comparison_operators(self):
        toks = tokenize(">= <= == != > <")
        k = kinds(toks)
        assert k[0] == TokKind.GTE
        assert k[1] == TokKind.LTE
        assert k[2] == TokKind.EQ
        assert k[3] == TokKind.NEQ
        assert k[4] == TokKind.GT
        assert k[5] == TokKind.LT

    def test_brackets(self):
        toks = tokenize("List[String]")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.LBRACKET,
            TokKind.IDENT,
            TokKind.RBRACKET,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_parens(self):
        toks = tokenize("f(x)")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.LPAREN,
            TokKind.IDENT,
            TokKind.RPAREN,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_pipe(self):
        toks = tokenize("a | b")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.PIPE,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_question(self):
        toks = tokenize("String?")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.QUESTION,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_dot(self):
        toks = tokenize("task.done")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.DOT,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_equals(self):
        # type X = a  (assignment, not equality ==)
        toks = tokenize("type X = a")
        assert kinds(toks) == [
            TokKind.IDENT,
            TokKind.IDENT,
            TokKind.EQUALS,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_equals_vs_eq(self):
        # '=' and '==' are different tokens
        toks = tokenize("a = b == c")
        k = kinds(toks)
        assert TokKind.EQUALS in k
        assert TokKind.EQ in k

    def test_token_line_numbers(self):
        toks = tokenize("a\nb")
        # first IDENT is on line 1
        assert toks[0].line == 1
        # second IDENT is on line 2
        ident_toks = [t for t in toks if t.kind == TokKind.IDENT]
        assert ident_toks[0].line == 1
        assert ident_toks[1].line == 2

    def test_token_col_zero_indexed(self):
        toks = tokenize("abc")
        assert toks[0].col == 0

    def test_token_col_offset(self):
        toks = tokenize("a b")
        assert toks[0].col == 0  # 'a'
        assert toks[1].col == 2  # 'b'

    def test_empty_source(self):
        toks = tokenize("")
        assert kinds(toks) == [TokKind.EOF]

    def test_only_whitespace(self):
        toks = tokenize("   ")
        assert kinds(toks) == [TokKind.EOF]


# ---------------------------------------------------------------------------
# Group 2: Indent / Dedent
# ---------------------------------------------------------------------------


class TestIndentDedent:
    def test_single_indent(self):
        src = "a:\n    b"
        toks = tokenize(src)
        k = kinds(toks)
        assert TokKind.INDENT in k
        assert TokKind.DEDENT in k
        assert_indent_dedent_balanced(toks)

    def test_single_indent_order(self):
        # a: NEWLINE INDENT b NEWLINE DEDENT EOF
        src = "a:\n    b"
        toks = tokenize(src)
        k = kinds(toks)
        assert k == [
            TokKind.IDENT,
            TokKind.COLON,
            TokKind.NEWLINE,
            TokKind.INDENT,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.DEDENT,
            TokKind.EOF,
        ]

    def test_indent_dedent_pair_with_continuation(self):
        src = "a:\n    b\nc"
        toks = tokenize(src)
        k = kinds(toks)
        # DEDENT appears before IDENT("c")
        dedent_idx = k.index(TokKind.DEDENT)
        c_ident_idx = next(
            i for i, t in enumerate(toks)
            if t.kind == TokKind.IDENT and t.value == "c"
        )
        assert dedent_idx < c_ident_idx
        assert_indent_dedent_balanced(toks)

    def test_double_indent(self):
        src = "a:\n    b:\n        c"
        toks = tokenize(src)
        k = kinds(toks)
        assert k.count(TokKind.INDENT) == 2
        assert k.count(TokKind.DEDENT) == 2
        assert_indent_dedent_balanced(toks)

    def test_triple_indent(self):
        src = "a:\n    b:\n        c:\n            d"
        toks = tokenize(src)
        k = kinds(toks)
        assert k.count(TokKind.INDENT) == 3
        assert k.count(TokKind.DEDENT) == 3
        assert_indent_dedent_balanced(toks)

    def test_multiple_dedent_at_once(self):
        # Going from depth 2 back to depth 0 emits 2 DEDENTs
        src = "a:\n    b:\n        c\nd"
        toks = tokenize(src)
        k = kinds(toks)
        assert k.count(TokKind.INDENT) == 2
        assert k.count(TokKind.DEDENT) == 2
        assert_indent_dedent_balanced(toks)

    def test_same_level_no_indent_token(self):
        src = "a\nb"
        toks = tokenize(src)
        k = kinds(toks)
        assert TokKind.INDENT not in k
        assert TokKind.DEDENT not in k

    def test_eof_closes_all_indents(self):
        # Source ends without returning to level 0
        src = "a:\n    b"
        toks = tokenize(src)
        # Last meaningful token before EOF should be DEDENT
        non_eof = [t for t in toks if t.kind != TokKind.EOF]
        assert non_eof[-1].kind == TokKind.DEDENT
        assert_indent_dedent_balanced(toks)

    def test_eof_closes_multiple_indents(self):
        src = "a:\n    b:\n        c"
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        # Two DEDENTs emitted at EOF
        assert kinds(toks).count(TokKind.DEDENT) == 2

    def test_indent_must_be_4_spaces(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n  b")
        assert "multiple of 4" in str(exc_info.value)

    def test_indent_6_spaces_error(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n      b")
        assert "multiple of 4" in str(exc_info.value)

    def test_indent_8_spaces_valid(self):
        # 8 spaces is valid (double indent)
        src = "a:\n    b:\n        c"
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)

    def test_misaligned_dedent_error(self):
        # Dedent to 6 spaces: not on the stack (0, 4, 8 are valid)
        src = "a:\n    b:\n        c\n      d"
        with pytest.raises(TokenizeError):
            tokenize(src)

    def test_tab_rejected(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n\tb")
        assert "tab" in str(exc_info.value).lower()

    def test_multiple_statements_same_level(self):
        src = "a:\n    x\n    y\n    z"
        toks = tokenize(src)
        # Only one INDENT going in and one DEDENT coming out
        k = kinds(toks)
        assert k.count(TokKind.INDENT) == 1
        assert k.count(TokKind.DEDENT) == 1
        assert_indent_dedent_balanced(toks)


# ---------------------------------------------------------------------------
# Group 3: Paren Depth
# ---------------------------------------------------------------------------


class TestParenDepth:
    def test_no_newline_inside_parens(self):
        src = "f(\n    x\n)"
        toks = tokenize(src)
        k = kinds(toks)
        # The only NEWLINE should be after the closing paren
        newlines = [i for i, k_ in enumerate(k) if k_ == TokKind.NEWLINE]
        rparen_idx = k.index(TokKind.RPAREN)
        assert all(nl > rparen_idx for nl in newlines)

    def test_no_indent_inside_parens(self):
        src = "f(\n    x\n)"
        toks = tokenize(src)
        k = kinds(toks)
        assert TokKind.INDENT not in k
        assert TokKind.DEDENT not in k

    def test_no_newline_inside_brackets(self):
        src = "List[\n    String\n]"
        toks = tokenize(src)
        k = kinds(toks)
        rbracket_idx = k.index(TokKind.RBRACKET)
        newlines = [i for i, k_ in enumerate(k) if k_ == TokKind.NEWLINE]
        assert all(nl > rbracket_idx for nl in newlines)

    def test_nested_parens(self):
        src = "f(g(\n    x\n))"
        toks = tokenize(src)
        k = kinds(toks)
        assert TokKind.INDENT not in k
        assert TokKind.DEDENT not in k
        # Two LPARENs, two RPARENs
        assert k.count(TokKind.LPAREN) == 2
        assert k.count(TokKind.RPAREN) == 2

    def test_mixed_parens_and_brackets(self):
        src = "f([a,\n    b])"
        toks = tokenize(src)
        k = kinds(toks)
        assert TokKind.INDENT not in k
        assert TokKind.DEDENT not in k

    def test_normal_newline_after_close_paren(self):
        src = "f(x)\na"
        toks = tokenize(src)
        k = kinds(toks)
        # NEWLINE appears after RPAREN
        rparen_idx = k.index(TokKind.RPAREN)
        first_newline = k.index(TokKind.NEWLINE)
        assert first_newline > rparen_idx

    def test_indent_resumes_after_close_paren(self):
        # After paren closes back to depth 0, subsequent indentation works
        src = "outer:\n    inner(\n        x\n    )\n    next"
        toks = tokenize(src)
        k = kinds(toks)
        assert_indent_dedent_balanced(toks)
        # There is exactly one INDENT (outer -> inner) and one DEDENT
        assert k.count(TokKind.INDENT) == 1
        assert k.count(TokKind.DEDENT) == 1

    def test_unmatched_close_paren_still_token(self):
        # ')' emits RPAREN even when paren_depth is 0 (parser handles error)
        toks = tokenize(")")
        assert toks[0].kind == TokKind.RPAREN

    def test_multiline_args_no_structural_tokens(self):
        src = "tests.pass(\n    80,\n    90\n)"
        toks = tokenize(src)
        k = kinds(toks)
        assert TokKind.INDENT not in k
        assert TokKind.DEDENT not in k
        # Verify the numbers are present
        num_toks = [t for t in toks if t.kind == TokKind.NUMBER]
        assert [t.value for t in num_toks] == ["80", "90"]


# ---------------------------------------------------------------------------
# Group 4: Comments and Blank Lines
# ---------------------------------------------------------------------------


class TestCommentsAndBlanks:
    def test_blank_line_produces_no_tokens(self):
        src = "a\n\nb"
        toks = tokenize(src)
        k = kinds(toks)
        # Should be: IDENT NEWLINE IDENT NEWLINE EOF (no double NEWLINE)
        assert k.count(TokKind.NEWLINE) == 2
        assert k == [
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_comment_line_skipped(self):
        src = "# comment\na"
        toks = tokenize(src)
        k = kinds(toks)
        assert k == [TokKind.IDENT, TokKind.NEWLINE, TokKind.EOF]

    def test_inline_comment(self):
        src = "a  # comment"
        toks = tokenize(src)
        k = kinds(toks)
        assert k == [TokKind.IDENT, TokKind.NEWLINE, TokKind.EOF]

    def test_comment_after_colon(self):
        src = "roles: a, b  # lista ruoli"
        toks = tokenize(src)
        k = kinds(toks)
        assert k == [
            TokKind.IDENT,
            TokKind.COLON,
            TokKind.IDENT,
            TokKind.COMMA,
            TokKind.IDENT,
            TokKind.NEWLINE,
            TokKind.EOF,
        ]

    def test_multiple_blank_lines(self):
        src = "a\n\n\n\nb"
        toks = tokenize(src)
        k = kinds(toks)
        # No double NEWLINE from the blank lines
        assert k.count(TokKind.NEWLINE) == 2

    def test_comment_only_source(self):
        src = "# just a comment"
        toks = tokenize(src)
        assert kinds(toks) == [TokKind.EOF]

    def test_comment_between_indented_blocks(self):
        src = "a:\n    # mid-block comment\n    b"
        toks = tokenize(src)
        k = kinds(toks)
        # Comment does not break INDENT/DEDENT
        assert TokKind.INDENT in k
        assert TokKind.DEDENT in k
        assert_indent_dedent_balanced(toks)


# ---------------------------------------------------------------------------
# Group 5: Error Cases
# ---------------------------------------------------------------------------


class TestTokenizeErrors:
    def test_tab_error(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("\ta")
        err = exc_info.value
        assert err.line == 1

    def test_tab_inside_source(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n\tb")
        err = exc_info.value
        assert err.line == 2

    def test_bad_indent_2_spaces(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n  b")
        assert "multiple of 4" in str(exc_info.value)

    def test_bad_indent_3_spaces(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n   b")
        assert "multiple of 4" in str(exc_info.value)

    def test_bad_indent_5_spaces(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n     b")
        assert "multiple of 4" in str(exc_info.value)

    def test_unterminated_string_double(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize('"hello')
        err = exc_info.value
        assert "unterminated" in str(err).lower()
        assert err.line == 1

    def test_unterminated_string_single(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("'hello")
        err = exc_info.value
        assert "unterminated" in str(err).lower()

    def test_unexpected_character_at(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("@")
        err = exc_info.value
        assert "unexpected" in str(err).lower()
        assert "@" in str(err)

    def test_unexpected_character_hash_in_content(self):
        # Hash starts inline comment, does NOT cause an error
        toks = tokenize("a # ok")
        assert toks[0].kind == TokKind.IDENT

    def test_error_has_line_info(self):
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a\nb\n@bad")
        err = exc_info.value
        assert err.line == 3

    def test_error_has_col_info(self):
        # "a @" - '@' is at col 2 in the content (after 'a' and space)
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a @b")
        err = exc_info.value
        assert err.col == 2  # '@' is at col 2 (0-indexed)

    def test_misaligned_dedent(self):
        # Indent stack is [0, 8] (jumped by 8 from level 0).
        # Dedent to 4 is a valid multiple of 4 but NOT on the stack [0, 8].
        # This must raise TokenizeError about misaligned dedent.
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("a:\n        b\n    c")
        assert "dedent" in str(exc_info.value).lower()

    def test_tab_mid_line(self):
        # Tab embedded in content (not just at indent) must also be rejected
        with pytest.raises(TokenizeError):
            tokenize("a\tb")

    def test_exclamation_alone(self):
        # '!' alone is not a valid operator (only '!=' is)
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("!")
        assert "unexpected" in str(exc_info.value).lower()

    def test_tokenize_error_string_representation(self):
        # Error message includes location
        with pytest.raises(TokenizeError) as exc_info:
            tokenize("@")
        assert "line 1" in str(exc_info.value)
        assert "col" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Group 6: Canonical Examples
# ---------------------------------------------------------------------------


class TestCanonicalExamples:
    """Tokenize all 10 examples from DESIGN_C1_2_SYNTAX_GRAMMAR.md.

    Each test verifies:
    - No TokenizeError is raised
    - INDENT/DEDENT are balanced
    - Key structural tokens are present with correct values
    """

    def test_example_1_delegate_task(self):
        src = """\
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    task_request before task_result
                    all roles participate
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # Must have IDENT tokens (not WORD -- old tokenizer)
        assert TokKind.IDENT in k
        # Must have structural tokens
        assert TokKind.COLON in k
        assert TokKind.COMMA in k
        # Check first IDENT is "protocol"
        first_ident = next(t for t in toks if t.kind == TokKind.IDENT)
        assert first_ident.value == "protocol"

    def test_example_2_plan_and_build(self):
        src = """\
            protocol PlanAndBuild:
                roles: regina, architect, worker, guardiana

                regina asks architect to plan
                architect returns plan to regina

                when regina decides:
                    approve:
                        regina tells architect decision
                        regina asks worker to do task
                        worker returns result to regina
                        regina asks guardiana to verify
                        guardiana returns verdict to regina
                    reject:
                        regina tells architect decision
                        architect returns plan to regina

                properties:
                    always terminates
                    no deadlock
                    confidence >= high
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # 'when' introduces choice block -> INDENT
        assert TokKind.INDENT in k
        # GTE for '>=' in confidence >= high
        assert TokKind.GTE in k

    def test_example_3_agent_with_contracts(self):
        src = """\
            agent Worker:
                role: backend
                trust: standard

                accepts: TaskRequest, PlanDecision
                produces: TaskResult

                requires:
                    task.well_defined
                    context.sufficient

                ensures:
                    output.compiles
                    tests.pass(80)
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # tests.pass(80): IDENT DOT IDENT LPAREN NUMBER RPAREN
        dot_idx = [i for i, kind in enumerate(k) if kind == TokKind.DOT]
        assert len(dot_idx) >= 1
        assert TokKind.LPAREN in k
        assert TokKind.RPAREN in k
        # NUMBER "80"
        num_toks = [t for t in toks if t.kind == TokKind.NUMBER]
        assert any(t.value == "80" for t in num_toks)

    def test_example_4_type_record(self):
        src = """\
            type AnalysisResult =
                conclusion: String
                confidence: Confident[String]
                evidence: List[String]
                alternative: String?
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # EQUALS for '='
        assert TokKind.EQUALS in k
        # LBRACKET / RBRACKET for Confident[String] and List[String]
        assert TokKind.LBRACKET in k
        assert TokKind.RBRACKET in k
        # QUESTION for 'String?'
        assert TokKind.QUESTION in k

    def test_example_5_type_variant(self):
        src = """\
            type TaskStatus = ok | fail | blocked

            type AuditVerdict = approved | blocked | needs_revision

            type Priority = critical | high | medium | low
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # type X = ok | fail | blocked  -> IDENT IDENT EQUALS IDENT PIPE IDENT PIPE IDENT NEWLINE
        assert TokKind.EQUALS in k
        assert TokKind.PIPE in k
        # Three PIPE tokens for first line alone (ok | fail | blocked)
        pipe_count = k.count(TokKind.PIPE)
        assert pipe_count >= 3

    def test_example_6_use_python(self):
        src = """\
            use python math
            use python datetime as dt
            use python pandas as pd

            agent DataAnalyst:
                role: data
                trust: standard

                requires:
                    pd.version >= "2.0"

                ensures:
                    output.format == "dataframe"
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # use python math -> IDENT IDENT IDENT NEWLINE
        ident_vals = [t.value for t in toks if t.kind == TokKind.IDENT]
        assert "use" in ident_vals
        assert "python" in ident_vals
        assert "math" in ident_vals
        assert "as" in ident_vals
        # "2.0" is a STRING
        str_toks = [t for t in toks if t.kind == TokKind.STRING]
        assert any("2.0" in t.value for t in str_toks)
        # >= and == operators
        assert TokKind.GTE in k
        assert TokKind.EQ in k

    def test_example_7_trust_properties(self):
        src = """\
            protocol SecureAudit:
                roles: regina, guardiana, backend

                regina asks backend to do task
                backend returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    trust >= trusted
                    backend cannot send audit_verdict
                    confidence >= high
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # trust >= trusted -> GTE
        assert TokKind.GTE in k
        ident_vals = [t.value for t in toks if t.kind == TokKind.IDENT]
        assert "trust" in ident_vals
        assert "trusted" in ident_vals
        assert "confidence" in ident_vals

    def test_example_8_recipe_app(self):
        src = """\
            protocol RecipeApp:
                roles: regina, chef, guardiana

                regina asks chef to do task
                chef returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    all roles participate

            agent Chef:
                role: backend
                trust: standard

                requires:
                    user.authenticated

                ensures:
                    no_recipe_deleted_by_accident
                    recipes.saved
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # Both protocol and agent blocks
        ident_vals = [t.value for t in toks if t.kind == TokKind.IDENT]
        assert "protocol" in ident_vals
        assert "agent" in ident_vals
        assert "Chef" in ident_vals

    def test_example_9_deep_research(self):
        src = """\
            type ResearchResult =
                findings: Confident[String]
                sources: List[String]
                methodology: String

            protocol DeepResearch:
                roles: regina, researcher, guardiana

                regina asks researcher to research
                researcher returns report to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    confidence >= medium
                    trust >= standard
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)
        # type block uses LBRACKET/RBRACKET
        assert TokKind.LBRACKET in k
        assert TokKind.RBRACKET in k
        # Two GTE for confidence >= medium and trust >= standard
        assert k.count(TokKind.GTE) >= 2

    def test_example_10_full_program(self):
        src = """\
            use python logging

            type Priority = critical | high | medium | low

            type CodeResult =
                code: Confident[String]
                tests_passed: Number
                coverage: Number

            protocol CodeReview:
                roles: regina, backend, tester, guardiana

                regina asks backend to do task
                backend returns result to regina
                regina asks tester to verify
                tester returns verdict to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina

                properties:
                    always terminates
                    no deadlock
                    task_request before task_result
                    backend cannot send audit_verdict
                    tester cannot send task_result
                    trust >= standard
                    all roles participate

            agent CodeBackend:
                role: backend
                trust: standard

                accepts: TaskRequest
                produces: TaskResult

                requires:
                    task.well_defined
                    task.priority != critical or regina.approved

                ensures:
                    output.compiles
                    tests.pass(80)
                    coverage >= 70

            agent CodeTester:
                role: tester
                trust: trusted

                accepts: AuditRequest
                produces: AuditVerdict

                requires:
                    code.compiles

                ensures:
                    all_tests.executed
                    report.complete
        """
        toks = tokenize(src)
        assert_indent_dedent_balanced(toks)
        k = kinds(toks)

        # Token count sanity: a full program should be substantial
        assert len(toks) > 100

        # All structural token types present
        assert TokKind.IDENT in k
        assert TokKind.COLON in k
        assert TokKind.COMMA in k
        assert TokKind.NEWLINE in k

        # Operators used in conditions/properties
        assert TokKind.GTE in k       # coverage >= 70, trust >= standard
        assert TokKind.NEQ in k       # task.priority != critical
        assert TokKind.PIPE in k      # type Priority variants
        assert TokKind.LBRACKET in k  # Confident[String], List[String]
        assert TokKind.LPAREN in k    # tests.pass(80)
        assert TokKind.DOT in k       # task.well_defined, tests.pass

        # Verify the NUMBER tokens
        num_toks = [t for t in toks if t.kind == TokKind.NUMBER]
        num_values = [t.value for t in num_toks]
        assert "80" in num_values
        assert "70" in num_values

        # Verify key identifiers
        ident_vals = {t.value for t in toks if t.kind == TokKind.IDENT}
        for kw in ("use", "python", "type", "protocol", "agent",
                   "requires", "ensures", "properties"):
            assert kw in ident_vals, f"Expected keyword '{kw}' as IDENT"
