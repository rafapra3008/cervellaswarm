# CervellaSwarm Reliability Patterns

> *"Apple Style = Liscio, Affidabile, Magico"*

Production-ready patterns for building resilient distributed systems. Zero external dependencies, fully type-hinted, extensively tested.

## Patterns Disponibili

### 1. Circuit Breaker
**File:** `circuit_breaker.py`
**Scopo:** Prevent cascade failures when external services fail

**Quick Start:**
```python
from patterns import circuit_breaker

@circuit_breaker(failure_threshold=3, recovery_timeout=60)
def call_external_api():
    return requests.get("https://api.example.com")
```

**How it works:**
- **CLOSED**: Normal operation, all calls go through
- **OPEN**: Too many failures, block all calls for `recovery_timeout` seconds
- **HALF_OPEN**: Testing if service recovered with single probe

**Configuration:**
- `failure_threshold`: Consecutive failures before opening (default: 5)
- `recovery_timeout`: Seconds to wait before retry (default: 60)

---

### 2. Retry with Exponential Backoff
**File:** `retry_backoff.py`
**Scopo:** Handle transient failures gracefully with increasing delays

**Quick Start:**
```python
from patterns import retry

@retry(max_retries=3, base_delay=1, max_delay=30)
def unstable_operation():
    return fetch_data_from_flaky_source()
```

**How it works:**
- Retry failed operations with exponential backoff: 1s, 2s, 4s, 8s...
- Optional jitter prevents thundering herd
- Configurable exception types to retry

**Configuration:**
- `max_retries`: Maximum retry attempts (default: 3)
- `base_delay`: Initial delay in seconds (default: 1.0)
- `max_delay`: Maximum delay cap (default: 60.0)
- `jitter`: Add randomness to delays (default: True)
- `exceptions`: Tuple of exceptions to catch (default: (Exception,))

**Advanced usage:**
```python
# Retry only specific exceptions
@retry(max_retries=5, exceptions=(ConnectionError, TimeoutError))
def network_operation():
    return api_call()
```

---

### 3. Structured Logging
**File:** `structured_logging.py`
**Scopo:** JSON-formatted logging for observability and analysis

**Quick Start:**
```python
from patterns import SwarmLogger

logger = SwarmLogger('backend-worker', task_id='task-001')
logger.info("Processing started", files=3, priority="high")
```

**Output format (JSONL):**
```json
{"timestamp": "2026-01-03T15:30:00", "level": "INFO", "agent": "backend-worker", "task_id": "task-001", "message": "Processing started", "extra": {"files": 3, "priority": "high"}}
```

**Features:**
- Dual output: JSON file + human-readable console
- Log rotation: One file per day (`logs/swarm_YYYY-MM-DD.jsonl`)
- Searchable: Filter by agent, level, task_id
- Structured: Every log is valid JSON

**Reading logs:**
```python
from patterns import read_logs, LogLevel

# Get all errors from backend-worker
errors = read_logs(
    Path("logs/swarm_2026-01-03.jsonl"),
    agent="backend-worker",
    level=LogLevel.ERROR
)
```

---

## Combined Usage

The real power comes from combining patterns:

```python
from patterns import circuit_breaker, retry, SwarmLogger

logger = SwarmLogger("api-client", task_id="job-001")

@circuit_breaker(failure_threshold=5, recovery_timeout=30)
@retry(max_retries=3, base_delay=1)
def resilient_api_call(data):
    logger.info("API call started", data=data)
    response = external_api.post(data)
    logger.info("API call succeeded", status=response.status)
    return response

# Now your function is:
# - Protected from cascade failures (circuit breaker)
# - Resilient to transient errors (retry)
# - Observable (structured logging)
```

---

## Design Principles

### Zero Dependencies
All patterns use only Python standard library. No pip install required.

### Type Safety
Full type hints for IDE autocomplete and static analysis:
```python
def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    ...
```

### Production Ready
- Thread-safe (circuit breaker uses locks)
- Tested (runnable doctests in each module)
- Documented (comprehensive docstrings)
- Observable (structured logging built-in)

---

## Examples

See `example_usage.py` for complete working examples:

```bash
python3 src/patterns/example_usage.py
```

This demonstrates:
1. Simple retry with logging
2. Circuit breaker for API calls
3. Combined patterns for maximum resilience
4. Task tracking with structured logs

---

## File Structure

```
src/patterns/
├── __init__.py              # Package exports
├── circuit_breaker.py       # Circuit Breaker pattern
├── retry_backoff.py         # Retry with backoff
├── structured_logging.py    # JSON logging
├── example_usage.py         # Working examples
└── README.md               # This file
```

---

## Quick Reference

| Pattern | Use When | Prevents |
|---------|----------|----------|
| Circuit Breaker | Calling external services | Cascade failures, wasted resources |
| Retry Backoff | Transient network/API errors | Immediate failures, thundering herd |
| Structured Logging | Need observability | Lost debugging info, unclear behavior |

---

## Testing

Each module has a `__main__` block for quick testing:

```bash
# Test circuit breaker
python3 src/patterns/circuit_breaker.py

# Test retry
python3 src/patterns/retry_backoff.py

# Test logging
python3 src/patterns/structured_logging.py
```

---

## Versioning

All modules use semantic versioning:

```python
__version__ = "1.0.0"
__version_date__ = "2026-01-03"
```

---

*Creato con calma e precisione da Cervella Backend* 🐍💙
*"Fatto BENE > Fatto VELOCE"*
