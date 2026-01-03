"""CervellaSwarm Reliability Patterns.

Production-ready patterns for building resilient distributed systems.
All modules are dependency-free (stdlib only) and fully type-hinted.

Modules:
    circuit_breaker: Prevent cascade failures
    retry_backoff: Handle transient errors gracefully
    structured_logging: JSON logging for observability
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-03"

from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
    circuit_breaker
)

from .retry_backoff import (
    retry,
    RetryContext,
    calculate_backoff
)

from .structured_logging import (
    SwarmLogger,
    LogLevel,
    read_logs
)

__all__ = [
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerError",
    "CircuitState",
    "circuit_breaker",
    # Retry
    "retry",
    "RetryContext",
    "calculate_backoff",
    # Logging
    "SwarmLogger",
    "LogLevel",
    "read_logs",
]
