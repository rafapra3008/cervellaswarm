# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _interop.py (C2.3.3 -- compile_file + save_module).

Test structure:
  - InteropError: attributes, message, subclass
  - compile_file: happy path, encoding, source_name override, file not found,
    unreadable, parse error, round-trip exec
  - save_module: happy path, overwrite=False, overwrite=True, parent missing,
    content verification
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._compiler import ASTCompiler, CompiledModule
from cervellaswarm_lingua_universale._interop import (
    InteropError,
    compile_file,
    save_module,
)


# ============================================================
# Sample .lu sources (reusable)
# ============================================================

SIMPLE_VARIANT = textwrap.dedent("""\
    type Status = Active | Inactive | Pending
""")

AGENT_WITH_CONTRACTS = textwrap.dedent("""\
    type TaskStatus = Pending | Done

    agent Worker:
        role: executor
        accepts: task_request
        requires: priority > 0
        ensures: result.valid
""")

MIXED_PROGRAM = textwrap.dedent("""\
    use python math

    type Color = Red | Green | Blue

    agent Painter:
        role: creator
        accepts: paint_request
""")


# ============================================================
# InteropError
# ============================================================


class TestInteropError:
    """Tests for the InteropError exception class."""

    def test_is_runtime_error(self) -> None:
        assert issubclass(InteropError, RuntimeError)

    def test_basic_message(self) -> None:
        err = InteropError("something failed")
        assert str(err) == "something failed"

    def test_attributes_default(self) -> None:
        err = InteropError("fail")
        assert err.path == ""
        assert err.operation == ""

    def test_attributes_custom(self) -> None:
        err = InteropError("fail", path="/tmp/x.lu", operation="compile_file:read")
        assert err.path == "/tmp/x.lu"
        assert err.operation == "compile_file:read"

    def test_catchable_as_runtime_error(self) -> None:
        with pytest.raises(RuntimeError, match="test"):
            raise InteropError("test")


# ============================================================
# compile_file
# ============================================================


class TestCompileFile:
    """Tests for compile_file()."""

    def test_simple_variant(self, tmp_path: Path) -> None:
        """Compile a simple variant type from a .lu file."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file)

        assert isinstance(result, CompiledModule)
        assert result.source_file == "variant.lu"
        assert "Status" in result.types
        assert "Literal" in result.python_source

    def test_source_name_defaults_to_filename(self, tmp_path: Path) -> None:
        """source_file should be the filename, not the full path."""
        lu_file = tmp_path / "my_protocol.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file)
        assert result.source_file == "my_protocol.lu"

    def test_source_name_override(self, tmp_path: Path) -> None:
        """source_name parameter overrides the default."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file, source_name="custom.lu")
        assert result.source_file == "custom.lu"

    def test_string_path(self, tmp_path: Path) -> None:
        """Accept string path (not just Path objects)."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(str(lu_file))
        assert isinstance(result, CompiledModule)
        assert result.source_file == "variant.lu"

    def test_agent_with_contracts(self, tmp_path: Path) -> None:
        """Compile an agent with requires/ensures contracts."""
        lu_file = tmp_path / "worker.lu"
        lu_file.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        result = compile_file(lu_file)
        assert "Worker" in result.agents
        assert "TaskStatus" in result.types
        assert "ContractViolation" in result.python_source

    def test_mixed_program(self, tmp_path: Path) -> None:
        """Compile a program with use + type + agent."""
        lu_file = tmp_path / "mixed.lu"
        lu_file.write_text(MIXED_PROGRAM, encoding="utf-8")

        result = compile_file(lu_file)
        assert result.imports == ("math",)
        assert result.types == ("Color",)
        assert result.agents == ("Painter",)

    def test_metadata_in_output(self, tmp_path: Path) -> None:
        """Generated code includes __lu_version__ and __lu_source__."""
        lu_file = tmp_path / "meta.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file)
        assert '__lu_version__' in result.python_source
        assert '__lu_source__ = "meta.lu"' in result.python_source

    def test_all_in_output(self, tmp_path: Path) -> None:
        """Generated code includes __all__."""
        lu_file = tmp_path / "all.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file)
        assert "__all__" in result.python_source
        assert result.exports == ("Status",)

    def test_roundtrip_exec(self, tmp_path: Path) -> None:
        """Compiled output is executable Python."""
        lu_file = tmp_path / "exec.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file)
        ns: dict = {}
        exec(compile(result.python_source, result.source_file, "exec"), ns)  # noqa: S102
        assert ns["Status"] is not None

    def test_encoding_latin1(self, tmp_path: Path) -> None:
        """Read a file with non-UTF-8 encoding."""
        lu_file = tmp_path / "latin.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="latin-1")

        result = compile_file(lu_file, encoding="latin-1")
        assert result.source_file == "latin.lu"

    def test_file_not_found(self, tmp_path: Path) -> None:
        """InteropError for missing file."""
        missing = tmp_path / "does_not_exist.lu"

        with pytest.raises(InteropError, match="File not found") as exc_info:
            compile_file(missing)
        assert exc_info.value.operation == "compile_file:read"
        assert "does_not_exist.lu" in exc_info.value.path

    def test_parse_error(self, tmp_path: Path) -> None:
        """InteropError wraps parse errors."""
        lu_file = tmp_path / "bad.lu"
        lu_file.write_text("this is not valid lu syntax @@@\n", encoding="utf-8")

        with pytest.raises(InteropError, match="Parse error") as exc_info:
            compile_file(lu_file)
        assert exc_info.value.operation == "compile_file:parse"

    def test_empty_file(self, tmp_path: Path) -> None:
        """Empty .lu file produces empty module."""
        lu_file = tmp_path / "empty.lu"
        lu_file.write_text("", encoding="utf-8")

        result = compile_file(lu_file)
        assert result.agents == ()
        assert result.protocols == ()
        assert result.types == ()

    def test_invalid_encoding(self, tmp_path: Path) -> None:
        """InteropError for unknown encoding."""
        lu_file = tmp_path / "enc.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        with pytest.raises(InteropError, match="Unknown encoding") as exc_info:
            compile_file(lu_file, encoding="nope")
        assert exc_info.value.operation == "compile_file:read"

    def test_compile_error_wrapped(self, tmp_path: Path) -> None:
        """InteropError wraps internal compiler errors."""
        import unittest.mock as mock

        lu_file = tmp_path / "err.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        with mock.patch.object(
            ASTCompiler, "compile", side_effect=TypeError("test boom")
        ):
            with pytest.raises(InteropError, match="Compile error") as exc_info:
                compile_file(lu_file)
            assert exc_info.value.operation == "compile_file:compile"


# ============================================================
# save_module
# ============================================================


class TestSaveModule:
    """Tests for save_module()."""

    @pytest.fixture()
    def sample_module(self) -> CompiledModule:
        """A minimal CompiledModule for testing save_module."""
        return CompiledModule(
            source_file="test.lu",
            python_source='"""Generated."""\n__lu_version__ = "0.2"\n',
            agents=(),
            protocols=(),
            imports=(),
            types=(),
            exports=(),
        )

    def test_save_creates_file(self, tmp_path: Path, sample_module: CompiledModule) -> None:
        """save_module creates a .py file with the correct content."""
        out = tmp_path / "output.py"
        result = save_module(sample_module, out)

        assert out.exists()
        assert out.read_text(encoding="utf-8") == sample_module.python_source
        assert result == out.resolve()

    def test_save_returns_resolved_path(self, tmp_path: Path, sample_module: CompiledModule) -> None:
        """Returned path is always resolved (absolute)."""
        out = tmp_path / "output.py"
        result = save_module(sample_module, out)
        assert result.is_absolute()

    def test_save_string_path(self, tmp_path: Path, sample_module: CompiledModule) -> None:
        """Accept string path (not just Path objects)."""
        out = tmp_path / "string_path.py"
        result = save_module(sample_module, str(out))
        assert out.exists()
        assert isinstance(result, Path)

    def test_save_no_overwrite_raises(self, tmp_path: Path, sample_module: CompiledModule) -> None:
        """Refuse to overwrite existing file by default."""
        out = tmp_path / "existing.py"
        out.write_text("# old content\n")

        with pytest.raises(InteropError, match="already exists") as exc_info:
            save_module(sample_module, out)
        assert exc_info.value.operation == "save_module:exists"

    def test_save_overwrite_true(self, tmp_path: Path, sample_module: CompiledModule) -> None:
        """overwrite=True replaces existing file."""
        out = tmp_path / "overwrite.py"
        out.write_text("# old content\n")

        save_module(sample_module, out, overwrite=True)
        assert out.read_text(encoding="utf-8") == sample_module.python_source

    def test_save_parent_missing(self, tmp_path: Path, sample_module: CompiledModule) -> None:
        """InteropError when parent directory does not exist."""
        out = tmp_path / "nonexistent_dir" / "output.py"

        with pytest.raises(InteropError, match="Parent directory") as exc_info:
            save_module(sample_module, out)
        assert exc_info.value.operation == "save_module:directory"

    def test_save_content_matches_compiled(self, tmp_path: Path) -> None:
        """Saved content matches compile_file output exactly."""
        lu_file = tmp_path / "roundtrip.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        module = compile_file(lu_file)
        out = tmp_path / "roundtrip.py"
        save_module(module, out)

        saved = out.read_text(encoding="utf-8")
        assert saved == module.python_source

    def test_full_roundtrip_compile_save_exec(self, tmp_path: Path) -> None:
        """Full pipeline: .lu -> compile_file -> save_module -> exec saved .py."""
        lu_file = tmp_path / "full.lu"
        lu_file.write_text(MIXED_PROGRAM, encoding="utf-8")

        module = compile_file(lu_file)
        py_file = tmp_path / "full.py"
        save_module(module, py_file)

        saved_source = py_file.read_text(encoding="utf-8")
        ns: dict = {}
        exec(compile(saved_source, "full.py", "exec"), ns)  # noqa: S102
        assert "Painter" in ns
        assert ns["__all__"] == ["Color", "Painter"]


# ============================================================
# Edge cases
# ============================================================


class TestInteropEdgeCases:
    """Edge cases and integration between compile_file + save_module."""

    def test_compile_file_preserves_exports(self, tmp_path: Path) -> None:
        """exports field matches the __all__ in the generated source."""
        lu_file = tmp_path / "exports.lu"
        lu_file.write_text(MIXED_PROGRAM, encoding="utf-8")

        module = compile_file(lu_file)
        assert "Color" in module.exports
        assert "Painter" in module.exports

    def test_source_name_with_backslash(self, tmp_path: Path) -> None:
        """source_name with backslash is properly escaped in output."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file, source_name="path\\to\\file.lu")
        # Should not break the generated Python
        ns: dict = {}
        exec(compile(result.python_source, "test", "exec"), ns)  # noqa: S102
        assert ns["__lu_source__"] == "path\\to\\file.lu"

    def test_compile_file_oserror(self, tmp_path: Path) -> None:
        """InteropError wraps OSError (e.g. permission denied)."""
        lu_file = tmp_path / "unreadable.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")
        lu_file.chmod(0o000)
        try:
            with pytest.raises(InteropError, match="Cannot read file") as exc_info:
                compile_file(lu_file)
            assert exc_info.value.operation == "compile_file:read"
        finally:
            lu_file.chmod(0o644)

    def test_save_oserror_write(self, tmp_path: Path) -> None:
        """InteropError wraps OSError when write fails (e.g. read-only dir)."""
        ro_dir = tmp_path / "readonly"
        ro_dir.mkdir()
        out = ro_dir / "output.py"
        ro_dir.chmod(0o555)
        module = CompiledModule(
            source_file="test.lu",
            python_source="# test\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        try:
            with pytest.raises(InteropError, match="Cannot write file") as exc_info:
                save_module(module, out)
            assert exc_info.value.operation == "save_module:write"
        finally:
            ro_dir.chmod(0o755)

    def test_save_race_condition_file_exists(self, tmp_path: Path) -> None:
        """FileExistsError from 'x' mode open is caught as InteropError."""
        import unittest.mock as mock

        out = tmp_path / "race.py"
        module = CompiledModule(
            source_file="test.lu",
            python_source="# test\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        # Simulate: exists() returns False but open('x') raises FileExistsError
        with mock.patch("builtins.open", side_effect=FileExistsError("race")):
            with pytest.raises(InteropError, match="race condition") as exc_info:
                save_module(module, out)
            assert exc_info.value.operation == "save_module:write"

    def test_source_name_with_quotes(self, tmp_path: Path) -> None:
        """source_name with double quotes is properly escaped."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        result = compile_file(lu_file, source_name='file"with"quotes.lu')
        ns: dict = {}
        exec(compile(result.python_source, "test", "exec"), ns)  # noqa: S102
        assert ns["__lu_source__"] == 'file"with"quotes.lu'
