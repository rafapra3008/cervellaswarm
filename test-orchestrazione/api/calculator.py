"""
Calculator module - Mathematical operations for CervellaSwarm.

Created by: cervella-backend
Task: TASK_GOLD_BACKEND
"""


def add(a: float, b: float) -> float:
    """
    Sum two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.

    Example:
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
    """
    return a + b


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The product of a and b.

    Example:
        >>> multiply(4, 5)
        20
        >>> multiply(-2, 3)
        -6
    """
    return a * b


def power(base: float, exp: float) -> float:
    """
    Calculate base raised to the power of exp.

    Args:
        base: The base number.
        exp: The exponent.

    Returns:
        base raised to the power of exp.

    Example:
        >>> power(2, 3)
        8
        >>> power(5, 0)
        1
    """
    return base ** exp
