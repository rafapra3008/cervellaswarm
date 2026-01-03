"""Example usage of CervellaSwarm reliability patterns.

This file demonstrates how to use circuit_breaker, retry, and structured_logging
together to build resilient worker processes.
"""

import time
import random
from pathlib import Path

from circuit_breaker import circuit_breaker, CircuitBreakerError
from retry_backoff import retry
from structured_logging import SwarmLogger


# Example 1: Simple retry with logging
def example_retry_with_logging():
    """Example: Retry pattern with structured logging."""
    logger = SwarmLogger("example-worker", task_id="demo-001")

    @retry(max_retries=3, base_delay=0.5, max_delay=5)
    def flaky_operation():
        logger.info("Attempting operation")
        if random.random() < 0.7:  # 70% failure rate
            logger.warning("Operation failed, will retry")
            raise ConnectionError("Simulated failure")
        logger.info("Operation succeeded")
        return "Success!"

    try:
        result = flaky_operation()
        logger.info("Task completed", result=result)
        return result
    except Exception as e:
        logger.error("Task failed after all retries", error=str(e))
        raise


# Example 2: Circuit breaker for external API
def example_circuit_breaker():
    """Example: Circuit breaker for external service."""
    logger = SwarmLogger("api-client", task_id="demo-002")

    @circuit_breaker(failure_threshold=3, recovery_timeout=10)
    def call_external_api():
        logger.info("Calling external API")
        if random.random() < 0.5:  # 50% failure rate
            logger.warning("API call failed")
            raise Exception("API Error")
        logger.info("API call succeeded")
        return {"status": "ok"}

    # Simulate multiple calls
    for i in range(10):
        try:
            result = call_external_api()
            logger.info(f"Call {i+1} succeeded", result=result)
        except CircuitBreakerError as e:
            logger.warning(f"Call {i+1} blocked by circuit breaker", error=str(e))
        except Exception as e:
            logger.error(f"Call {i+1} failed", error=str(e))

        time.sleep(0.5)


# Example 3: Combining retry + circuit breaker + logging
def example_combined():
    """Example: All patterns combined for maximum resilience."""
    logger = SwarmLogger("resilient-worker", task_id="demo-003")

    @circuit_breaker(failure_threshold=5, recovery_timeout=15)
    @retry(max_retries=2, base_delay=1, max_delay=10)
    def resilient_operation(data: str):
        logger.info("Processing data", data=data)

        # Simulate random failures
        rand = random.random()
        if rand < 0.3:  # 30% immediate failure
            logger.warning("Immediate failure", failure_type="network")
            raise ConnectionError("Network issue")
        elif rand < 0.5:  # 20% timeout
            logger.warning("Timeout detected", failure_type="timeout")
            raise TimeoutError("Operation timeout")

        # Success
        logger.info("Data processed successfully", data=data)
        return f"Processed: {data}"

    # Process multiple items
    items = [f"item-{i}" for i in range(20)]
    results = []

    for item in items:
        try:
            result = resilient_operation(item)
            results.append(result)
            logger.info("Item processed", item=item, total_processed=len(results))
        except CircuitBreakerError:
            logger.error("Circuit breaker OPEN, skipping item", item=item)
        except Exception as e:
            logger.error("Item failed after retries", item=item, error=str(e))

    logger.info(
        "Batch processing completed",
        total_items=len(items),
        successful=len(results),
        failed=len(items) - len(results)
    )

    return results


# Example 4: Using structured logging for task tracking
def example_task_tracking():
    """Example: Track task progress with structured logging."""
    logger = SwarmLogger("task-worker")

    tasks = ["task-001", "task-002", "task-003"]

    for task_id in tasks:
        logger.set_task_id(task_id)
        logger.info("Task started", priority="high")

        # Simulate work
        steps = ["validate", "process", "save"]
        for step in steps:
            logger.debug("Executing step", step=step)
            time.sleep(0.1)

        logger.info("Task completed", steps_count=len(steps))

    logger.info("All tasks completed", total_tasks=len(tasks))


if __name__ == "__main__":
    print("=" * 60)
    print("CervellaSwarm Reliability Patterns - Examples")
    print("=" * 60)

    print("\n[1] Retry with Logging")
    print("-" * 60)
    try:
        example_retry_with_logging()
    except Exception as e:
        print(f"Example 1 failed: {e}")

    print("\n[2] Circuit Breaker")
    print("-" * 60)
    example_circuit_breaker()

    print("\n[3] Combined Patterns (Retry + Circuit Breaker + Logging)")
    print("-" * 60)
    results = example_combined()
    print(f"Processed {len(results)} items successfully")

    print("\n[4] Task Tracking")
    print("-" * 60)
    example_task_tracking()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("Check logs/ directory for structured logs")
    print("=" * 60)
