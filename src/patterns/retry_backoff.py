"""Retry Pattern with Exponential Backoff.

This module provides a retry mechanism with exponential backoff to handle
transient failures gracefully. Includes optional jitter to prevent thundering herd.

Usage:
    @retry(max_retries=3, base_delay=1, max_delay=30)
    def unstable_operation():
        # Your code here
        pass
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-03"

import logging
import time
import random
from functools import wraps
from typing import Callable, TypeVar, Tuple, Type, Optional, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')


def calculate_backoff(
    attempt: int,
    base_delay: float,
    max_delay: float,
    jitter: bool = True
) -> float:
    """Calculate exponential backoff delay.

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter

    Returns:
        Delay in seconds
    """
    # Exponential: base_delay * 2^attempt
    delay = min(base_delay * (2 ** attempt), max_delay)

    if jitter:
        # Add jitter: random value between 0 and delay
        delay = random.uniform(0, delay)

    return delay


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retry with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for first retry
        max_delay: Maximum delay in seconds
        jitter: Add random jitter to prevent thundering herd
        exceptions: Tuple of exception types to catch and retry

    Returns:
        Decorated function with retry logic

    Example:
        >>> @retry(max_retries=3, base_delay=1, max_delay=30)
        ... def unstable_operation():
        ...     # Operation that might fail transiently
        ...     return external_api_call()

        >>> # Retry only specific exceptions
        >>> @retry(max_retries=5, exceptions=(ConnectionError, TimeoutError))
        ... def network_operation():
        ...     return fetch_data()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        logger.info(
                            f"Retry attempt {attempt}/{max_retries} "
                            f"for {func.__name__}"
                        )

                    result = func(*args, **kwargs)

                    if attempt > 0:
                        logger.info(
                            f"Success on retry attempt {attempt} "
                            f"for {func.__name__}"
                        )

                    return result

                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        delay = calculate_backoff(
                            attempt,
                            base_delay,
                            max_delay,
                            jitter
                        )

                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed "
                            f"for {func.__name__}: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed "
                            f"for {func.__name__}: {e}"
                        )

            # All retries exhausted
            if last_exception:
                raise last_exception
            else:
                # Should never happen, but satisfies type checker
                raise RuntimeError("Retry loop exited unexpectedly")

        return wrapper

    return decorator


class RetryContext:
    """Context manager for retry with exponential backoff.

    Alternative to decorator for more explicit control.

    Example:
        >>> retry_ctx = RetryContext(max_retries=3, base_delay=1)
        >>> for attempt in retry_ctx:
        ...     try:
        ...         result = unstable_operation()
        ...         retry_ctx.success()
        ...         break
        ...     except Exception as e:
        ...         if not retry_ctx.should_retry(e):
        ...             raise
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True,
        exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        """Initialize retry context.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            jitter: Add random jitter
            exceptions: Exception types to retry on
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.exceptions = exceptions
        self.attempt = 0
        self._success = False

    def __iter__(self):
        """Iterate through retry attempts."""
        self.attempt = 0
        self._success = False
        return self

    def __next__(self) -> int:
        """Get next retry attempt.

        Returns:
            Current attempt number

        Raises:
            StopIteration: When all retries exhausted or success called
        """
        if self._success or self.attempt > self.max_retries:
            raise StopIteration

        current = self.attempt
        self.attempt += 1
        return current

    def success(self) -> None:
        """Mark operation as successful and stop retrying."""
        self._success = True

    def should_retry(self, exception: Exception) -> bool:
        """Check if should retry after this exception.

        Args:
            exception: Exception that was raised

        Returns:
            True if should retry, False otherwise
        """
        if not isinstance(exception, self.exceptions):
            return False

        if self.attempt > self.max_retries:
            logger.error(
                f"All {self.max_retries + 1} attempts exhausted: {exception}"
            )
            return False

        delay = calculate_backoff(
            self.attempt - 1,  # -1 because attempt was already incremented
            self.base_delay,
            self.max_delay,
            self.jitter
        )

        logger.warning(
            f"Attempt {self.attempt}/{self.max_retries + 1} failed: {exception}. "
            f"Retrying in {delay:.2f}s..."
        )

        time.sleep(delay)
        return True


if __name__ == "__main__":
    # Simple test
    import random

    @retry(max_retries=5, base_delay=0.5, max_delay=5)
    def flaky_operation():
        """Simulate a flaky operation."""
        if random.random() < 0.6:  # 60% failure rate
            raise ConnectionError("Temporary connection issue")
        return "Success!"

    logging.basicConfig(level=logging.INFO)

    try:
        result = flaky_operation()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after all retries: {e}")
