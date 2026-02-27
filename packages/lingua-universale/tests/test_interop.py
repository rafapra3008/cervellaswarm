# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _interop.py (C2.3.3 + C2.3.4).

Test structure:
  - InteropError: attributes, message, subclass
  - compile_file: happy path, encoding, source_name override, file not found,
    unreadable, parse error, round-trip exec
  - save_module: happy path, overwrite=False, overwrite=True, parent missing,
    content verification
  - load_module: module attributes, __name__, __file__, __spec__, not in
    sys.modules, exec error, GC, variant/agent/contract access
  - load_file: convenience wrapper, full pipeline
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._compiler import ASTCompiler, CompiledModule
from cervellaswarm_lingua_universale._interop import (
    InteropError,
    compile_file,
    load_file,
    load_module,
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


# ============================================================
# load_module (C2.3.4)
# ============================================================


class TestLoadModule:
    """Tests for load_module()."""

    def test_returns_module_type(self, tmp_path: Path) -> None:
        """load_module returns a types.ModuleType instance."""
        import types

        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert isinstance(mod, types.ModuleType)

    def test_module_name_from_source_file(self, tmp_path: Path) -> None:
        """__name__ defaults to source file stem."""
        lu_file = tmp_path / "my_types.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert mod.__name__ == "my_types"

    def test_module_name_override(self, tmp_path: Path) -> None:
        """module_name parameter overrides default."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled, module_name="custom_mod")
        assert mod.__name__ == "custom_mod"

    def test_module_file_attribute(self, tmp_path: Path) -> None:
        """__file__ is set to compiled.source_file."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert mod.__file__ == "variant.lu"

    def test_module_spec_is_none(self, tmp_path: Path) -> None:
        """__spec__ is None (not loaded via importlib)."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert mod.__spec__ is None

    def test_module_loader_is_none(self, tmp_path: Path) -> None:
        """__loader__ is None."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert mod.__loader__ is None

    def test_not_in_sys_modules(self, tmp_path: Path) -> None:
        """Loaded module is NOT registered in sys.modules."""
        import sys

        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled, module_name="lu_test_not_registered")
        assert "lu_test_not_registered" not in sys.modules

    def test_variant_type_accessible(self, tmp_path: Path) -> None:
        """Variant type is accessible as a module attribute."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert hasattr(mod, "Status")
        assert mod.__lu_version__ == "0.2"

    def test_agent_class_accessible(self, tmp_path: Path) -> None:
        """Agent class is accessible and instantiable."""
        lu_file = tmp_path / "agent.lu"
        lu_file.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert hasattr(mod, "Worker")
        worker = mod.Worker()
        assert worker.__lu_role__ == "executor"

    def test_agent_contracts_enforced(self, tmp_path: Path) -> None:
        """Contract violations raise ContractViolation at runtime."""
        from cervellaswarm_lingua_universale._contracts import ContractViolation

        lu_file = tmp_path / "contracts.lu"
        lu_file.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        worker = mod.Worker()
        with pytest.raises(ContractViolation, match="requires violated"):
            worker.process(priority=0, result=None)

    def test_mixed_program_attributes(self, tmp_path: Path) -> None:
        """Mixed program: imports, types, agents all accessible."""
        lu_file = tmp_path / "mixed.lu"
        lu_file.write_text(MIXED_PROGRAM, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert hasattr(mod, "Color")
        assert hasattr(mod, "Painter")
        assert hasattr(mod, "math")
        assert hasattr(mod, "__all__")
        assert mod.__all__ == ["Color", "Painter"]

    def test_all_attribute_matches_exports(self, tmp_path: Path) -> None:
        """Module __all__ matches CompiledModule.exports."""
        lu_file = tmp_path / "exports.lu"
        lu_file.write_text(MIXED_PROGRAM, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert list(mod.__all__) == list(compiled.exports)

    def test_exec_error_wrapped(self) -> None:
        """InteropError wraps exec() failures."""
        broken = CompiledModule(
            source_file="broken.lu",
            python_source="raise ValueError('boom')\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        with pytest.raises(InteropError, match="Failed to execute") as exc_info:
            load_module(broken)
        assert exc_info.value.operation == "load_module:exec"
        assert exc_info.value.path == "broken.lu"

    def test_exec_syntax_error_wrapped(self) -> None:
        """InteropError wraps SyntaxError in generated code."""
        broken = CompiledModule(
            source_file="syntax.lu",
            python_source="def (invalid syntax\n",
            agents=(),
            protocols=(),
            imports=(),
        )
        with pytest.raises(InteropError, match="Failed to execute"):
            load_module(broken)

    def test_gc_no_leak(self, tmp_path: Path) -> None:
        """Module is garbage-collectable when reference is dropped."""
        import gc
        import weakref

        lu_file = tmp_path / "gc.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        ref = weakref.ref(mod)
        del mod
        gc.collect()
        assert ref() is None

    def test_multiple_loads_independent(self, tmp_path: Path) -> None:
        """Loading same CompiledModule twice gives independent modules."""
        lu_file = tmp_path / "multi.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod1 = load_module(compiled, module_name="mod1")
        mod2 = load_module(compiled, module_name="mod2")
        assert mod1 is not mod2
        assert mod1.__name__ == "mod1"
        assert mod2.__name__ == "mod2"

    def test_lu_source_attribute(self, tmp_path: Path) -> None:
        """Module has __lu_source__ from generated code."""
        lu_file = tmp_path / "source.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        compiled = compile_file(lu_file)
        mod = load_module(compiled)
        assert mod.__lu_source__ == "source.lu"


# ============================================================
# load_file (C2.3.4)
# ============================================================


class TestLoadFile:
    """Tests for load_file() -- convenience wrapper."""

    def test_simple_variant(self, tmp_path: Path) -> None:
        """Load a variant type directly from .lu file."""
        import types

        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        mod = load_file(lu_file)
        assert isinstance(mod, types.ModuleType)
        assert hasattr(mod, "Status")

    def test_module_name_override(self, tmp_path: Path) -> None:
        """module_name is passed through to load_module."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        mod = load_file(lu_file, module_name="my_variant")
        assert mod.__name__ == "my_variant"

    def test_module_name_defaults_to_stem(self, tmp_path: Path) -> None:
        """Default module name is the file stem."""
        lu_file = tmp_path / "my_types.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        mod = load_file(lu_file)
        assert mod.__name__ == "my_types"

    def test_string_path(self, tmp_path: Path) -> None:
        """Accept string path."""
        lu_file = tmp_path / "variant.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="utf-8")

        mod = load_file(str(lu_file))
        assert hasattr(mod, "Status")

    def test_encoding_passthrough(self, tmp_path: Path) -> None:
        """Encoding is passed to compile_file."""
        lu_file = tmp_path / "latin.lu"
        lu_file.write_text(SIMPLE_VARIANT, encoding="latin-1")

        mod = load_file(lu_file, encoding="latin-1")
        assert hasattr(mod, "Status")

    def test_file_not_found_propagates(self, tmp_path: Path) -> None:
        """InteropError propagates from compile_file."""
        missing = tmp_path / "missing.lu"

        with pytest.raises(InteropError, match="File not found"):
            load_file(missing)

    def test_full_pipeline_with_contracts(self, tmp_path: Path) -> None:
        """Full pipeline: .lu -> load_file -> use agent with contracts."""
        from cervellaswarm_lingua_universale._contracts import ContractViolation

        lu_file = tmp_path / "worker.lu"
        lu_file.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu_file)
        worker = mod.Worker()
        # Valid contract
        assert worker.__lu_role__ == "executor"
        # Invalid contract
        with pytest.raises(ContractViolation):
            worker.process(priority=-1, result=None)
