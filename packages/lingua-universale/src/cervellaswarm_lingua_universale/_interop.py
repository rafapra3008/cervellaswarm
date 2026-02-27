# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Python interop layer for compiled Lingua Universale modules (C2.3).

Provides file I/O and runtime operations on top of the pure-string compiler:

  - ``compile_file()`` -- read a ``.lu`` file, parse, and compile to a
    ``CompiledModule``.
  - ``save_module()`` -- write a ``CompiledModule``'s Python source to disk.
  - ``load_module()`` -- execute a ``CompiledModule`` into a live Python module.
  - ``load_file()``   -- convenience: .lu -> live module in one step.

Architecture (STUDIO C2.3):
  - ``_compiler.py`` = pure string generation (no I/O, no importlib).
  - ``_interop.py``  = I/O and runtime module management.

Security:
  ``load_module`` and ``load_file`` execute generated Python code via ``exec()``.
  Do not load untrusted ``.lu`` files without review.
"""

from __future__ import annotations

import types
from pathlib import Path

from ._compiler import ASTCompiler, CompiledModule
from ._parser import parse


class InteropError(RuntimeError):
    """Raised when a Lingua Universale interop operation fails.

    Wraps lower-level errors (I/O, parse, compile) with context about
    which file or operation was involved.

    Attributes:
        path: The file path involved in the failed operation (may be empty).
        operation: Short description of the operation that failed.
    """

    __slots__ = ("path", "operation")

    def __init__(
        self,
        message: str,
        *,
        path: str = "",
        operation: str = "",
    ) -> None:
        self.path = path
        self.operation = operation
        super().__init__(message)


# ============================================================
# compile_file
# ============================================================


def compile_file(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    source_name: str | None = None,
) -> CompiledModule:
    """Read a ``.lu`` file, parse it, and compile to a ``CompiledModule``.

    Args:
        path: Path to the ``.lu`` source file.
        encoding: File encoding (default ``"utf-8"``).
        source_name: Override for the ``source_file`` field in the result.
            Defaults to the file's name (e.g. ``"example.lu"``).

    Returns:
        A ``CompiledModule`` with the compiled Python source and metadata.

    Raises:
        InteropError: If the file cannot be read, parsed, or compiled.

    Example::

        from cervellaswarm_lingua_universale._interop import compile_file

        module = compile_file("protocols/delegate.lu")
        print(module.python_source)
    """
    file_path = Path(path)

    # Resolve source_name: default to filename
    effective_name = source_name if source_name is not None else file_path.name

    # 1. Read file
    try:
        source = file_path.read_text(encoding=encoding)
    except FileNotFoundError:
        raise InteropError(
            f"File not found: {file_path}",
            path=str(file_path),
            operation="compile_file:read",
        ) from None
    except LookupError as exc:
        raise InteropError(
            f"Unknown encoding {encoding!r} for {file_path}: {exc}",
            path=str(file_path),
            operation="compile_file:read",
        ) from None
    except OSError as exc:
        raise InteropError(
            f"Cannot read file: {file_path}: {exc}",
            path=str(file_path),
            operation="compile_file:read",
        ) from exc

    # 2. Parse
    try:
        program = parse(source)
    except Exception as exc:
        raise InteropError(
            f"Parse error in {file_path}: {exc}",
            path=str(file_path),
            operation="compile_file:parse",
        ) from exc

    # 3. Compile
    try:
        compiler = ASTCompiler()
        return compiler.compile(program, source_file=effective_name)
    except Exception as exc:
        raise InteropError(
            f"Compile error in {file_path}: {exc}",
            path=str(file_path),
            operation="compile_file:compile",
        ) from exc


# ============================================================
# save_module
# ============================================================


def save_module(
    compiled: CompiledModule,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a ``CompiledModule``'s Python source to a file on disk.

    Args:
        compiled: The compiled module to save.
        output_path: Destination path for the ``.py`` file.
        overwrite: If ``False`` (default), raise ``InteropError`` when the
            target file already exists.  If ``True``, overwrite silently.

    Returns:
        The resolved ``Path`` of the written file.

    Raises:
        InteropError: If the file already exists (and ``overwrite=False``),
            the parent directory does not exist, or an I/O error occurs.

    Example::

        from cervellaswarm_lingua_universale._interop import (
            compile_file, save_module,
        )

        module = compile_file("protocols/delegate.lu")
        save_module(module, "generated/delegate.py")
    """
    out = Path(output_path)

    # Check parent directory exists
    if not out.parent.exists():
        raise InteropError(
            f"Parent directory does not exist: {out.parent}",
            path=str(out),
            operation="save_module:directory",
        )

    # Check overwrite policy
    if not overwrite and out.exists():
        raise InteropError(
            f"File already exists (use overwrite=True to replace): {out}",
            path=str(out),
            operation="save_module:exists",
        )

    # Write atomically via 'x' mode when not overwriting (F4 finding)
    try:
        if overwrite:
            out.write_text(compiled.python_source, encoding="utf-8")
        else:
            # 'x' mode: exclusive creation -- fails if file was created
            # between our exists() check and this open() call.
            with open(out, "x", encoding="utf-8") as f:
                f.write(compiled.python_source)
    except FileExistsError:
        raise InteropError(
            f"File already exists (race condition): {out}",
            path=str(out),
            operation="save_module:write",
        ) from None
    except OSError as exc:
        raise InteropError(
            f"Cannot write file: {out}: {exc}",
            path=str(out),
            operation="save_module:write",
        ) from exc

    return out.resolve()


# ============================================================
# load_module
# ============================================================


def load_module(
    compiled: CompiledModule,
    *,
    module_name: str | None = None,
) -> types.ModuleType:
    """Execute a ``CompiledModule`` and return a live Python module.

    The generated Python source is executed via ``exec()`` into a fresh
    ``types.ModuleType`` namespace.  The resulting module has proper
    ``__name__``, ``__file__``, and ``__spec__`` attributes but is
    **not** registered in ``sys.modules`` -- it exists only as long as
    the caller holds a reference.

    .. warning::

       This function executes generated code via ``exec()``.  Do not
       load untrusted ``.lu`` files without review.

    Args:
        compiled: The compiled module to load.
        module_name: Name for the module's ``__name__`` attribute.
            Defaults to the source file stem (e.g. ``"example"`` for
            ``"example.lu"``).

    Returns:
        A live ``types.ModuleType`` containing the compiled declarations.

    Raises:
        InteropError: If execution of the generated code fails.

    Example::

        from cervellaswarm_lingua_universale._interop import (
            compile_file, load_module,
        )

        compiled = compile_file("protocols/delegate.lu")
        mod = load_module(compiled)
        print(mod.DelegateTaskSession)
    """
    # Derive module name from source_file if not given
    if module_name is None:
        module_name = Path(compiled.source_file).stem

    # Create module object
    mod = types.ModuleType(module_name)
    mod.__file__ = compiled.source_file
    mod.__spec__ = None  # Not loaded via importlib
    mod.__loader__ = None

    # Execute generated code into module namespace
    try:
        code = compile(compiled.python_source, compiled.source_file, "exec")
        exec(code, mod.__dict__)  # noqa: S102
    except Exception as exc:
        raise InteropError(
            f"Failed to execute compiled module "
            f"{compiled.source_file!r}: {exc}",
            path=compiled.source_file,
            operation="load_module:exec",
        ) from exc

    return mod


# ============================================================
# load_file
# ============================================================


def load_file(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    module_name: str | None = None,
) -> types.ModuleType:
    """Compile a ``.lu`` file and return a live Python module.

    Convenience function combining ``compile_file()`` + ``load_module()``.

    .. warning::

       This function executes generated code via ``exec()``.  Do not
       load untrusted ``.lu`` files without review.

    Args:
        path: Path to the ``.lu`` source file.
        encoding: File encoding (default ``"utf-8"``).
        module_name: Name for the module's ``__name__`` attribute.
            Defaults to the source file stem.

    Returns:
        A live ``types.ModuleType`` containing the compiled declarations.

    Raises:
        InteropError: If the file cannot be read, parsed, compiled, or
            executed.

    Example::

        from cervellaswarm_lingua_universale._interop import load_file

        mod = load_file("protocols/delegate.lu")
        session = mod.DelegateTaskSession()
    """
    compiled = compile_file(path, encoding=encoding)
    return load_module(compiled, module_name=module_name)
