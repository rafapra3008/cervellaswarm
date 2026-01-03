"""Circuit Breaker Pattern for preventing cascade failures.

This module provides a Circuit Breaker implementation that prevents calling
a failing service repeatedly. It transitions between CLOSED, OPEN, and HALF_OPEN
states based on failure rates.

Usage:
    @circuit_breaker(failure_threshold=3, recovery_timeout=60)
    def call_external_api():
        # Your code here
        pass
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-03"

import logging
import time
from enum import Enum
from functools import wraps
from typing import Callable, Any, TypeVar, Optional
from threading import Lock

logger = logging.getLogger(__name__)

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit Breaker states."""
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Blocking calls due to failures
    HALF_OPEN = "HALF_OPEN"  # Testing if service recovered


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is OPEN."""
    pass


class CircuitBreaker:
    """Circuit Breaker implementation.

    Attributes:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before attempting recovery
        state: Current circuit state
        failure_count: Current number of consecutive failures
        last_failure_time: Timestamp of last failure
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60
    ):
        """Initialize Circuit Breaker.

        Args:
            failure_threshold: Consecutive failures before opening circuit
            recovery_timeout: Seconds to wait in OPEN state before HALF_OPEN
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self._lock = Lock()

    def _transition_to_open(self) -> None:
        """Transition to OPEN state."""
        old_state = self.state
        self.state = CircuitState.OPEN
        self.last_failure_time = time.time()
        logger.warning(
            f"Circuit Breaker transitioned: {old_state.value} -> OPEN "
            f"(failures: {self.failure_count}/{self.failure_threshold})"
        )

    def _transition_to_half_open(self) -> None:
        """Transition to HALF_OPEN state."""
        old_state = self.state
        self.state = CircuitState.HALF_OPEN
        logger.info(f"Circuit Breaker transitioned: {old_state.value} -> HALF_OPEN")

    def _transition_to_closed(self) -> None:
        """Transition to CLOSED state."""
        old_state = self.state
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        logger.info(f"Circuit Breaker transitioned: {old_state.value} -> CLOSED")

    def _check_recovery_timeout(self) -> None:
        """Check if recovery timeout has passed and transition to HALF_OPEN."""
        if (
            self.state == CircuitState.OPEN
            and self.last_failure_time is not None
            and time.time() - self.last_failure_time >= self.recovery_timeout
        ):
            self._transition_to_half_open()

    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function with circuit breaker protection.

        Args:
            func: Function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            CircuitBreakerError: If circuit is OPEN
            Exception: Any exception raised by func
        """
        with self._lock:
            self._check_recovery_timeout()

            if self.state == CircuitState.OPEN:
                raise CircuitBreakerError(
                    f"Circuit breaker is OPEN. "
                    f"Retry after {self.recovery_timeout}s from last failure."
                )

        try:
            result = func(*args, **kwargs)

            with self._lock:
                if self.state == CircuitState.HALF_OPEN:
                    self._transition_to_closed()
                elif self.state == CircuitState.CLOSED:
                    # Reset failure count on success
                    if self.failure_count > 0:
                        self.failure_count = 0

            return result

        except Exception as e:
            with self._lock:
                self.failure_count += 1
                logger.error(
                    f"Circuit Breaker recorded failure ({self.failure_count}/"
                    f"{self.failure_threshold}): {e}"
                )

                if self.state == CircuitState.HALF_OPEN:
                    # Failed during recovery test -> back to OPEN
                    self._transition_to_open()
                elif self.failure_count >= self.failure_threshold:
                    self._transition_to_open()

            raise


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: int = 60
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for circuit breaker pattern.

    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before attempting recovery

    Returns:
        Decorated function with circuit breaker protection

    Example:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=60)
        ... def call_external_api():
        ...     # API call that might fail
        ...     return requests.get("https://api.example.com")
    """
    breaker = CircuitBreaker(failure_threshold, recovery_timeout)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return breaker.call(func, *args, **kwargs)

        # Expose breaker for inspection/testing
        wrapper.circuit_breaker = breaker  # type: ignore
        return wrapper

    return decorator


if __name__ == "__main__":
    # Simple test
    import random

    @circuit_breaker(failure_threshold=3, recovery_timeout=5)
    def flaky_service():
        """Simulate a flaky service."""
        if random.random() < 0.7:  # 70% failure rate
            raise Exception("Service unavailable")
        return "Success"

    logging.basicConfig(level=logging.INFO)

    for i in range(10):
        try:
            result = flaky_service()
            print(f"Call {i+1}: {result}")
        except CircuitBreakerError as e:
            print(f"Call {i+1}: Circuit OPEN - {e}")
        except Exception as e:
            print(f"Call {i+1}: Failed - {e}")

        time.sleep(1)
