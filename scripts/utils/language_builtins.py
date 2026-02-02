"""Built-in symbol sets for reference filtering.

This module defines sets of built-in symbols for Python and TypeScript/JavaScript
that should be filtered out during reference extraction. These are standard
library and language primitives that don't represent user-defined dependencies.

Usage:
    from builtins import PYTHON_BUILTINS, TS_BUILTINS

    if symbol_name in PYTHON_BUILTINS:
        # Skip this reference
        pass

Author: Cervella Backend (F1.1 Tech Debt Cleanup)
Version: 1.0.0
Date: 2026-02-02
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-02"

# Python builtins to ignore in reference extraction
# Includes: functions, constants, special names, common typing
PYTHON_BUILTINS = frozenset({
    # Built-in functions
    "abs", "all", "any", "ascii", "bin", "bool", "breakpoint", "bytearray",
    "bytes", "callable", "chr", "classmethod", "compile", "complex",
    "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec",
    "filter", "float", "format", "frozenset", "getattr", "globals",
    "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance",
    "issubclass", "iter", "len", "list", "locals", "map", "max",
    "memoryview", "min", "next", "object", "oct", "open", "ord", "pow",
    "print", "property", "range", "repr", "reversed", "round", "set",
    "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super",
    "tuple", "type", "vars", "zip",
    # Constants
    "True", "False", "None", "Ellipsis", "NotImplemented",
    # Special names
    "self", "cls", "__init__", "__new__", "__del__", "__repr__", "__str__",
    "__bytes__", "__format__", "__lt__", "__le__", "__eq__", "__ne__",
    "__gt__", "__ge__", "__hash__", "__bool__", "__getattr__", "__setattr__",
    "__delattr__", "__dir__", "__get__", "__set__", "__delete__",
    "__call__", "__len__", "__getitem__", "__setitem__", "__delitem__",
    "__iter__", "__next__", "__contains__", "__add__", "__sub__", "__mul__",
    "__enter__", "__exit__", "__await__", "__aiter__", "__anext__",
    # Common typing
    "Any", "Union", "Optional", "List", "Dict", "Set", "Tuple", "Type",
    "Callable", "Iterable", "Iterator", "Generator", "Sequence", "Mapping",
})

# TypeScript/JavaScript builtins to ignore in reference extraction
# Includes: global objects, constructors, DOM types, React hooks
TS_BUILTINS = frozenset({
    # Global objects
    "console", "document", "window", "navigator", "location", "history",
    "localStorage", "sessionStorage", "fetch", "XMLHttpRequest",
    "URL", "URLSearchParams", "FormData",
    # Fetch API
    "Response", "Request", "Headers",
    # File API
    "File", "Blob", "FileReader", "FileList",
    # Built-in constructors
    "Array", "Object", "String", "Number", "Boolean", "Symbol", "BigInt",
    "Function", "Map", "Set", "WeakMap", "WeakSet", "WeakRef", "Date",
    "RegExp", "Error", "TypeError", "ReferenceError", "SyntaxError", "RangeError",
    "Promise", "Proxy", "Reflect", "JSON", "Math", "Intl",
    "Atomics", "FinalizationRegistry",
    "ArrayBuffer", "SharedArrayBuffer", "DataView",
    "Int8Array", "Uint8Array", "Uint8ClampedArray",
    "Int16Array", "Uint16Array", "Int32Array", "Uint32Array",
    "Float32Array", "Float64Array", "BigInt64Array", "BigUint64Array",
    # Built-in functions
    "parseInt", "parseFloat", "isNaN", "isFinite", "encodeURI", "decodeURI",
    "encodeURIComponent", "decodeURIComponent", "eval", "alert", "confirm",
    "prompt", "setTimeout", "setInterval", "clearTimeout", "clearInterval",
    "requestAnimationFrame", "cancelAnimationFrame", "queueMicrotask",
    # Primitive types (TypeScript)
    "string", "number", "boolean", "void", "null", "undefined", "never",
    "any", "unknown", "object", "symbol", "bigint",
    # Utility types (TypeScript)
    "Partial", "Required", "Readonly", "Record", "Pick", "Omit", "Exclude",
    "Extract", "NonNullable", "Parameters", "ConstructorParameters",
    "ReturnType", "InstanceType", "ThisParameterType", "OmitThisParameter",
    "ThisType", "Uppercase", "Lowercase", "Capitalize", "Uncapitalize",
    "Awaited", "NoInfer",
    # Special keywords
    "this", "super", "arguments", "globalThis",
    # Common globals
    "process", "module", "exports", "require", "__dirname", "__filename",
    "Buffer", "global",
    # React common (filtered because ubiquitous)
    "React", "Component", "PureComponent", "Fragment",
    "useState", "useEffect", "useContext", "useReducer", "useCallback",
    "useMemo", "useRef", "useImperativeHandle", "useLayoutEffect",
    "useDebugValue", "useDeferredValue", "useTransition", "useId",
    "createElement", "cloneElement", "isValidElement", "Children",
    # Event types (common DOM)
    "Event", "MouseEvent", "KeyboardEvent", "TouchEvent", "FocusEvent",
    "InputEvent", "ChangeEvent", "FormEvent", "DragEvent", "WheelEvent",
    # DOM types
    "Element", "HTMLElement", "HTMLDivElement", "HTMLInputElement",
    "HTMLButtonElement", "HTMLFormElement", "HTMLAnchorElement",
    "Node", "NodeList", "Document", "Window",
})
