"""Tests for Symbol dataclass (symbol_types.py).

Covers __repr__ method and default field values.

Author: Cervella Tester
Date: 2026-02-10
"""

from cervellaswarm_code_intelligence.symbol_types import Symbol


def test_symbol_repr():
    """Test Symbol __repr__ output format (line 52)."""
    symbol = Symbol(
        name="login", type="function",
        file="auth.py", line=42,
        signature="def login()"
    )
    result = repr(symbol)
    assert result == "<Symbol function 'login' at auth.py:42>"


def test_symbol_repr_class_type():
    """Test __repr__ with class type symbol."""
    symbol = Symbol(
        name="UserService", type="class",
        file="services/user.py", line=10,
        signature="class UserService:"
    )
    assert "class" in repr(symbol)
    assert "UserService" in repr(symbol)


def test_symbol_defaults():
    """Test Symbol default field values."""
    symbol = Symbol(
        name="test", type="class",
        file="test.py", line=1,
        signature="class Test:"
    )
    assert symbol.docstring == ""
    assert symbol.references == []


def test_symbol_with_all_fields():
    """Test Symbol with all fields populated."""
    symbol = Symbol(
        name="func", type="function",
        file="app.py", line=10,
        signature="def func(x: int) -> str",
        docstring="A function.",
        references=["other_func", "MyClass"]
    )
    assert symbol.name == "func"
    assert symbol.docstring == "A function."
    assert len(symbol.references) == 2


def test_symbol_references_independent():
    """Test that default references list is independent between instances."""
    s1 = Symbol("a", "function", "a.py", 1, "def a():")
    s2 = Symbol("b", "function", "b.py", 1, "def b():")
    s1.references.append("something")
    assert len(s2.references) == 0
