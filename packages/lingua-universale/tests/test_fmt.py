# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the _fmt.py module -- Lingua Universale auto-formatter (B6).

Covers:
  TestFormatting    - Core formatting: steps, properties, agents, types, choices
  TestIdempotency   - format(format(x)) == format(x), stdlib parametrized
  TestComments      - File-level and inter-declaration comment preservation
  TestEdgeCases     - Empty program, zero steps, minimal agent, multi-property
  TestPublicAPI     - format_source(), format_file() contracts
  TestCLI           - lu fmt, --check, --diff, --stdout
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._fmt import format_file, format_source


# ============================================================
# Helpers
# ============================================================

_STDLIB_DIR = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "cervellaswarm_lingua_universale"
    / "stdlib"
)


def _fmt(source: str) -> str:
    """Convenience wrapper: dedent + format_source."""
    return format_source(textwrap.dedent(source))


# ============================================================
# TestFormatting
# ============================================================


class TestFormatting:
    """Core formatting behaviour: steps, properties, agents, types, choices."""

    # --- simple protocol ---

    def test_simple_protocol_round_trip(self):
        """A minimal valid protocol formats to canonical form."""
        source = textwrap.dedent("""\
            protocol TaskRequest:
                roles: client, server

                client asks server to do task
                server returns result to client

                properties:
                    always terminates
                    no deadlock
        """)
        result = format_source(source)
        assert "protocol TaskRequest:" in result
        assert "roles: client, server" in result
        assert "client asks server to do task" in result
        assert "server returns result to client" in result
        assert "properties:" in result
        assert "always terminates" in result
        assert "no deadlock" in result

    def test_blank_line_between_roles_and_first_step(self):
        """Formatter inserts blank line between roles declaration and first step."""
        source = textwrap.dedent("""\
            protocol Ping:
                roles: checker, service
                checker sends ping to service
                properties:
                    always terminates
        """)
        result = format_source(source)
        lines = result.splitlines()
        roles_idx = next(i for i, l in enumerate(lines) if "roles:" in l)
        step_idx = next(i for i, l in enumerate(lines) if "checker sends" in l)
        # There must be exactly one blank line between roles and first step
        assert lines[roles_idx + 1] == ""
        assert step_idx == roles_idx + 2

    def test_blank_line_before_properties_block(self):
        """Formatter inserts blank line before properties block."""
        source = textwrap.dedent("""\
            protocol TaskRequest:
                roles: client, server
                client asks server to do task
                server returns result to client
                properties:
                    always terminates
        """)
        result = format_source(source)
        lines = result.splitlines()
        props_idx = next(i for i, l in enumerate(lines) if "properties:" in l)
        assert lines[props_idx - 1] == ""

    # --- all 5 action types ---

    def test_action_asks_format(self):
        """'asks' action formats as: sender asks receiver to payload."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice asks bob to do task
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    alice asks bob to do task" in result

    def test_action_returns_format(self):
        """'returns' action formats as: sender returns payload to receiver."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice asks bob to process
                bob returns result to alice
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    bob returns result to alice" in result

    def test_action_tells_format(self):
        """'tells' action formats as: sender tells receiver payload."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: coord, worker
                coord asks worker to start
                coord tells worker stop now
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    coord tells worker stop now" in result

    def test_action_proposes_format(self):
        """'proposes' action formats as: sender proposes payload to receiver."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice proposes plan to bob
                bob returns answer to alice
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    alice proposes plan to bob" in result

    def test_action_sends_format(self):
        """'sends' action formats as: sender sends payload to receiver."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice sends ping to bob
                bob sends pong to alice
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    alice sends ping to bob" in result

    # --- properties canonical ordering ---

    def test_properties_canonical_order(self):
        """Properties are sorted: terminates, deadlock, deletion, participate, confidence, trust, ordering, exclusion, role_exclusive."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: client, server
                client asks server to do task
                server returns result to client
                properties:
                    trust >= verified
                    no deadlock
                    always terminates
                    confidence >= high
                    no deletion
                    all roles participate
        """)
        result = format_source(source)
        lines = result.splitlines()
        # Extract lines inside the properties block
        props_start = next(i for i, l in enumerate(lines) if "properties:" in l)
        prop_lines = [l.strip() for l in lines[props_start + 1:] if l.strip()]
        expected_order = [
            "always terminates",
            "no deadlock",
            "no deletion",
            "all roles participate",
            "confidence >= high",
            "trust >= verified",
        ]
        assert prop_lines == expected_order

    def test_ordering_prop_before_after(self):
        """OrderingProp formats as: X before Y."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice sends ping to bob
                bob sends pong to alice
                properties:
                    always terminates
                    alice before bob
        """)
        result = format_source(source)
        assert "alice before bob" in result

    def test_exclusion_prop_cannot_send(self):
        """ExclusionProp formats as: role cannot send message."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice sends ping to bob
                bob sends pong to alice
                properties:
                    always terminates
                    alice cannot send pong
        """)
        result = format_source(source)
        assert "alice cannot send pong" in result

    def test_role_exclusive_prop(self):
        """RoleExclusiveProp formats as: role exclusive message."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: approver, requester
                requester asks approver to review
                approver returns decision to requester
                properties:
                    always terminates
                    approver exclusive decision
        """)
        result = format_source(source)
        assert "approver exclusive decision" in result

    # --- agent canonical ordering ---

    def test_agent_clause_canonical_order(self):
        """Agent clauses: role, trust, accepts, produces, requires, ensures."""
        source = textwrap.dedent("""\
            agent MyAgent:
                ensures: response.sent
                requires: request.valid
                trust: standard
                role: client
                produces: Response
                accepts: Request
        """)
        result = format_source(source)
        lines = result.splitlines()
        agent_idx = next(i for i, l in enumerate(lines) if "agent MyAgent:" in l)
        clause_lines = [l.strip() for l in lines[agent_idx + 1:] if l.strip()]
        # Check canonical ordering
        keys = [cl.split(":")[0] for cl in clause_lines]
        assert keys == ["role", "trust", "accepts", "produces", "requires", "ensures"]

    def test_agent_role_only(self):
        """Agent with only role clause formats correctly."""
        source = textwrap.dedent("""\
            agent MinimalAgent:
                role: worker
        """)
        result = format_source(source)
        assert "agent MinimalAgent:" in result
        assert "    role: worker" in result

    # --- use statements sorted ---

    def test_use_statements_sorted_alphabetically(self):
        """use statements are sorted by module name."""
        source = textwrap.dedent("""\
            use python zebra
            use python alpha
            use python math
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        lines = result.splitlines()
        use_lines = [l for l in lines if l.startswith("use python")]
        modules = [l.split()[-1] for l in use_lines]
        assert modules == sorted(modules)

    # --- type declarations ---

    def test_variant_type_one_line(self):
        """Variant type formats on a single line with ' | ' separator."""
        source = textwrap.dedent("""\
            type Status = Active | Inactive | Pending
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "type Status = Active | Inactive | Pending" in result

    def test_record_type_indented_fields(self):
        """Record type fields are indented under the type declaration."""
        source = textwrap.dedent("""\
            type Request =
                id: String
                payload: String
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "type Request =" in result
        assert "    id: String" in result
        assert "    payload: String" in result

    # --- choices ---

    def test_choice_blank_line_before(self):
        """A blank line appears before 'when X decides:' when preceded by a step."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice asks bob to start
                when bob decides:
                    yes:
                        bob returns ok to alice
                    no:
                        bob returns fail to alice
                properties:
                    always terminates
        """)
        result = format_source(source)
        lines = result.splitlines()
        step_idx = next(i for i, l in enumerate(lines) if "alice asks bob to start" in l)
        when_idx = next(i for i, l in enumerate(lines) if "when bob decides:" in l)
        # blank line must exist between the step and the when
        assert lines[step_idx + 1] == ""
        assert when_idx == step_idx + 2

    def test_choice_blank_line_between_branches(self):
        """Blank line separates branches inside a choice block."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                when alice decides:
                    approve:
                        alice returns ok to bob
                    reject:
                        alice returns fail to bob
                properties:
                    always terminates
        """)
        result = format_source(source)
        lines = result.splitlines()
        approve_idx = next(i for i, l in enumerate(lines) if "approve:" in l)
        reject_idx = next(i for i, l in enumerate(lines) if "reject:" in l)
        # There must be a blank line between the last line of approve branch and reject:
        between = lines[approve_idx + 1:reject_idx]
        assert "" in between

    def test_nested_choice_formats_correctly(self):
        """Nested choices (LU 1.1) format with correct indentation."""
        source = textwrap.dedent("""\
            protocol SagaOrder:
                roles: coordinator, payment, inventory
                coordinator asks payment to charge order
                when payment decides:
                    success:
                        payment returns confirmation to coordinator
                        coordinator asks inventory to reserve items
                        when inventory decides:
                            reserved:
                                inventory returns reservation to coordinator
                            out_of_stock:
                                inventory returns error to coordinator
                    failure:
                        payment returns error to coordinator
                properties:
                    always terminates
                    no deadlock
        """)
        result = format_source(source)
        # Outer choice
        assert "    when payment decides:" in result
        # Inner choice indented further
        assert "        when inventory decides:" in result
        # Innermost branch labels
        assert "            reserved:" in result
        assert "            out_of_stock:" in result

    def test_choice_format_structure(self):
        """when X decides: / label: / steps structure is emitted correctly."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                when alice decides:
                    yes:
                        alice returns ok to bob
                    no:
                        alice returns fail to bob
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    when alice decides:" in result
        assert "        yes:" in result
        assert "            alice returns ok to bob" in result
        assert "        no:" in result
        assert "            alice returns fail to bob" in result


# ============================================================
# TestIdempotency
# ============================================================


class TestIdempotency:
    """format(format(x)) == format(x) for any valid LU source."""

    def test_idempotent_simple_protocol(self):
        """Formatting a simple protocol twice yields the same result."""
        source = textwrap.dedent("""\
            protocol TaskRequest:
                roles: client, server

                client asks server to do task
                server returns result to client

                properties:
                    always terminates
                    no deadlock
        """)
        first = format_source(source)
        second = format_source(first)
        assert first == second

    def test_idempotent_with_choice(self):
        """Formatting a protocol with choices is idempotent."""
        source = textwrap.dedent("""\
            protocol ApprovalWorkflow:
                roles: requester, approver, notifier

                requester asks approver to review request
                when approver decides:
                    approve:
                        approver returns approval to requester
                        approver sends approval notice to notifier
                    reject:
                        approver returns rejection to requester

                properties:
                    always terminates
                    no deadlock
                    approver exclusive decision
        """)
        first = format_source(source)
        second = format_source(first)
        assert first == second

    def test_idempotent_with_types_and_agents(self):
        """Formatting a file with types and agents is idempotent."""
        source = textwrap.dedent("""\
            type Status = Active | Inactive

            type Request =
                id: String
                payload: String

            agent ClientAgent:
                role: client
                trust: standard
                accepts: Response
                produces: Request
                requires: request.valid
                ensures: request.sent

            protocol RequestResponse:
                roles: client, server

                client asks server to process request
                server returns response to client

                properties:
                    always terminates
                    no deadlock
        """)
        first = format_source(source)
        second = format_source(first)
        assert first == second

    def test_idempotent_with_nested_choice(self):
        """Formatting nested choices is idempotent."""
        source = textwrap.dedent("""\
            protocol SagaOrder:
                roles: coordinator, payment, inventory

                coordinator asks payment to charge order
                when payment decides:
                    success:
                        payment returns confirmation to coordinator
                        coordinator asks inventory to reserve items
                        when inventory decides:
                            reserved:
                                inventory returns reservation to coordinator
                            out_of_stock:
                                inventory returns error to coordinator
                                coordinator tells payment refund order
                    failure:
                        payment returns error to coordinator

                properties:
                    always terminates
                    no deadlock
                    coordinator before payment
        """)
        first = format_source(source)
        second = format_source(first)
        assert first == second

    @pytest.fixture(
        params=sorted(_STDLIB_DIR.rglob("*.lu")),
        ids=lambda p: p.stem,
    )
    def stdlib_file(self, request):
        return request.param

    def test_stdlib_idempotent(self, stdlib_file):
        """Formatting any stdlib .lu file twice yields the same result."""
        source = stdlib_file.read_text(encoding="utf-8")
        first = format_source(source, source_file=str(stdlib_file))
        second = format_source(first, source_file=str(stdlib_file))
        assert first == second, (
            f"{stdlib_file.name} is not idempotent after formatting"
        )


# ============================================================
# TestComments
# ============================================================


class TestComments:
    """Comment preservation during formatting."""

    def test_file_level_header_comments_preserved(self):
        """Comments before any declaration are preserved as a header block."""
        source = textwrap.dedent("""\
            # SPDX-License-Identifier: Apache-2.0
            # My protocol file

            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "# SPDX-License-Identifier: Apache-2.0" in result
        assert "# My protocol file" in result
        # Header must appear before the protocol declaration
        header_idx = result.index("# SPDX-License-Identifier")
        proto_idx = result.index("protocol Test:")
        assert header_idx < proto_idx

    def test_empty_file_trailing_newline(self):
        """Formatting an empty source returns a single trailing newline."""
        result = format_source("")
        assert result == "\n"

    def test_file_with_only_comments_preserved(self):
        """A file with only comments (no declarations) returns comments + newline."""
        source = "# just a comment\n"
        result = format_source(source)
        assert "# just a comment" in result
        assert result.endswith("\n")

    def test_stdlib_spdx_header_preserved(self):
        """Formatting request_response.lu preserves its SPDX comment header."""
        lu_file = (
            _STDLIB_DIR / "communication" / "request_response.lu"
        )
        source = lu_file.read_text(encoding="utf-8")
        result = format_source(source, source_file=str(lu_file))
        assert "# SPDX-License-Identifier: Apache-2.0" in result


# ============================================================
# TestEdgeCases
# ============================================================


class TestEdgeCases:
    """Edge cases: empty inputs, minimal declarations, multi-property."""

    def test_empty_program_no_declarations(self):
        """A source with no declarations produces a trailing newline."""
        result = format_source("")
        assert result == "\n"

    def test_protocol_with_single_step_and_no_choice(self):
        """A protocol with exactly one step (no choice) formats without crashing."""
        source = textwrap.dedent("""\
            protocol Ping:
                roles: client, server
                client asks server to ping
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "protocol Ping:" in result
        assert "roles: client, server" in result
        assert "client asks server to ping" in result
        assert "always terminates" in result

    def test_agent_with_only_role_no_other_clauses(self):
        """An agent with only a role clause formats correctly without extra lines."""
        source = textwrap.dedent("""\
            agent Bare:
                role: worker
        """)
        result = format_source(source)
        assert "agent Bare:" in result
        assert "    role: worker" in result
        # Must not have trust/accepts/produces/requires/ensures lines
        assert "trust:" not in result
        assert "accepts:" not in result
        assert "produces:" not in result

    def test_multiple_properties_of_same_type_all_emitted(self):
        """Multiple ordering properties (same type, different values) are all emitted."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob, carol
                alice sends msg to bob
                bob sends msg to carol
                properties:
                    always terminates
                    alice before bob
                    bob before carol
        """)
        result = format_source(source)
        assert "alice before bob" in result
        assert "bob before carol" in result

    def test_output_ends_with_single_newline(self):
        """Formatted output always ends with exactly one newline."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: alice, bob
                alice asks bob to do task
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert result.endswith("\n")
        assert not result.endswith("\n\n")

    def test_generic_optional_type_expr(self):
        """Generic and optional type expressions format correctly."""
        source = textwrap.dedent("""\
            type Order =
                id: String
                items: List[String]
                note: String?
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "    id: String" in result
        assert "    items: List[String]" in result
        assert "    note: String?" in result

    def test_use_with_alias(self):
        """use ... as alias formats correctly."""
        source = textwrap.dedent("""\
            use python datetime as dt
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert "use python datetime as dt" in result


# ============================================================
# TestPublicAPI
# ============================================================


class TestPublicAPI:
    """Tests for format_source() and format_file() contracts."""

    def test_format_source_returns_string(self):
        """format_source() returns a str."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source)
        assert isinstance(result, str)

    def test_format_source_accepts_source_file_kwarg(self):
        """format_source() accepts source_file= as keyword arg without raising."""
        source = textwrap.dedent("""\
            protocol Test:
                roles: a, b
                a asks b to go
                properties:
                    always terminates
        """)
        result = format_source(source, source_file="myfile.lu")
        assert isinstance(result, str)

    def test_format_file_returns_changed_true_when_different(self, tmp_path):
        """format_file() returns (formatted, True) when file is not yet canonical."""
        # Write a file with wrong property order so formatting changes it
        lu_file = tmp_path / "test.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol Test:
                    roles: a, b
                    a asks b to go
                    b returns result to a
                    properties:
                        no deadlock
                        always terminates
            """),
            encoding="utf-8",
        )
        formatted, changed = format_file(lu_file)
        assert changed is True
        assert isinstance(formatted, str)

    def test_format_file_returns_changed_false_when_already_canonical(self, tmp_path):
        """format_file() returns (formatted, False) when file is already canonical."""
        # Write a file that is already in canonical form
        source = textwrap.dedent("""\
            protocol Test:
                roles: a, b

                a asks b to go
                b returns result to a

                properties:
                    always terminates
                    no deadlock
        """)
        lu_file = tmp_path / "canonical.lu"
        # Format once to get canonical form, write that
        canonical = format_source(source)
        lu_file.write_text(canonical, encoding="utf-8")
        formatted, changed = format_file(lu_file)
        assert changed is False
        assert formatted == canonical

    def test_format_file_raises_file_not_found(self, tmp_path):
        """format_file() raises FileNotFoundError for a missing file."""
        missing = tmp_path / "does_not_exist.lu"
        with pytest.raises(FileNotFoundError):
            format_file(missing)

    def test_format_file_accepts_str_path(self, tmp_path):
        """format_file() accepts a str path, not just Path."""
        lu_file = tmp_path / "str.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol Test:
                    roles: a, b
                    a asks b to go
                    properties:
                        always terminates
            """),
            encoding="utf-8",
        )
        formatted, changed = format_file(str(lu_file))
        assert isinstance(formatted, str)


# ============================================================
# TestCLI
# ============================================================


class TestCLI:
    """Tests for the lu fmt CLI subcommand."""

    def _run_lu(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "cervellaswarm_lingua_universale", *args],
            capture_output=True,
            text=True,
        )

    def _canonical_file(self, tmp_path) -> Path:
        """Write and return a file already in canonical form."""
        source = textwrap.dedent("""\
            protocol TaskRequest:
                roles: client, server

                client asks server to do task
                server returns result to client

                properties:
                    always terminates
                    no deadlock
        """)
        lu_file = tmp_path / "canonical.lu"
        # Use format_source to get the exact canonical form
        canonical = format_source(source)
        lu_file.write_text(canonical, encoding="utf-8")
        return lu_file

    def _unformatted_file(self, tmp_path) -> Path:
        """Write and return a file NOT in canonical form (wrong property order)."""
        lu_file = tmp_path / "unformatted.lu"
        lu_file.write_text(
            textwrap.dedent("""\
                protocol TaskRequest:
                    roles: client, server
                    client asks server to do task
                    server returns result to client
                    properties:
                        no deadlock
                        always terminates
            """),
            encoding="utf-8",
        )
        return lu_file

    def test_fmt_in_place_writes_file(self, tmp_path):
        """lu fmt <file> rewrites the file to canonical form."""
        lu_file = self._unformatted_file(tmp_path)
        original = lu_file.read_text(encoding="utf-8")
        result = self._run_lu("fmt", str(lu_file))
        assert result.returncode == 0
        new_content = lu_file.read_text(encoding="utf-8")
        # File must have changed
        assert new_content != original
        # Now it must be idempotent
        second_fmt = format_source(new_content)
        assert second_fmt == new_content

    def test_fmt_in_place_already_formatted_exit_0(self, tmp_path):
        """lu fmt exits 0 for a file already in canonical form and does not change it."""
        lu_file = self._canonical_file(tmp_path)
        original = lu_file.read_text(encoding="utf-8")
        result = self._run_lu("fmt", str(lu_file))
        assert result.returncode == 0
        assert lu_file.read_text(encoding="utf-8") == original

    def test_fmt_check_already_formatted_exit_0(self, tmp_path):
        """lu fmt --check exits 0 if file is already formatted."""
        lu_file = self._canonical_file(tmp_path)
        result = self._run_lu("fmt", "--check", str(lu_file))
        assert result.returncode == 0

    def test_fmt_check_would_reformat_exit_1(self, tmp_path):
        """lu fmt --check exits 1 if file would be reformatted."""
        lu_file = self._unformatted_file(tmp_path)
        result = self._run_lu("fmt", "--check", str(lu_file))
        assert result.returncode == 1

    def test_fmt_check_does_not_modify_file(self, tmp_path):
        """lu fmt --check never writes to disk even when file would change."""
        lu_file = self._unformatted_file(tmp_path)
        original = lu_file.read_text(encoding="utf-8")
        self._run_lu("fmt", "--check", str(lu_file))
        assert lu_file.read_text(encoding="utf-8") == original

    def test_fmt_diff_shows_diff_output(self, tmp_path):
        """lu fmt --diff prints unified diff and exits 1 when file would change."""
        lu_file = self._unformatted_file(tmp_path)
        result = self._run_lu("fmt", "--diff", str(lu_file))
        assert result.returncode == 1  # CI-friendly: exit 1 when files need reformatting
        # unified diff markers
        assert "---" in result.stdout or "+++" in result.stdout

    def test_fmt_diff_no_change_exit_0(self, tmp_path):
        """lu fmt --diff exits 0 and produces no diff for an already-formatted file."""
        lu_file = self._canonical_file(tmp_path)
        result = self._run_lu("fmt", "--diff", str(lu_file))
        assert result.returncode == 0

    def test_fmt_stdout_prints_formatted(self, tmp_path):
        """lu fmt --stdout prints formatted source to stdout without modifying file."""
        lu_file = self._unformatted_file(tmp_path)
        original = lu_file.read_text(encoding="utf-8")
        result = self._run_lu("fmt", "--stdout", str(lu_file))
        assert result.returncode == 0
        # File must be unchanged
        assert lu_file.read_text(encoding="utf-8") == original
        # stdout must contain formatted protocol
        assert "protocol TaskRequest:" in result.stdout
        assert "always terminates" in result.stdout

    def test_fmt_missing_file_exit_1(self, tmp_path):
        """lu fmt exits 1 and prints an error for a missing file."""
        missing = tmp_path / "nope.lu"
        result = self._run_lu("fmt", str(missing))
        assert result.returncode == 1
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "error" in output.lower()


# ============================================================
# Guardiana F6: Inter-declaration comments preserved
# ============================================================


class TestInterDeclarationComments:
    """F6: Comments placed between declarations must be preserved."""

    def test_comment_between_agent_and_protocol(self):
        source = textwrap.dedent("""\
            agent Worker:
                role: backend
                trust: standard

            # This protocol coordinates the work
            protocol SimpleWork:
                roles: client, server
                client asks server to do task
                server returns result to client
                properties:
                    always terminates
        """)
        formatted = format_source(source)
        assert "# This protocol coordinates the work" in formatted
        assert "protocol SimpleWork:" in formatted

    def test_comment_between_types(self):
        source = textwrap.dedent("""\
            type Status = Active | Inactive

            # Request carries the payload
            type Request =
                id: String
                payload: String
        """)
        formatted = format_source(source)
        assert "# Request carries the payload" in formatted


# ============================================================
# Guardiana F7: Parse error handling
# ============================================================


class TestParseError:
    """F7: format_source raises on invalid LU input."""

    def test_format_source_raises_on_invalid_input(self):
        with pytest.raises(Exception):
            format_source("this is not valid lu at all")
