# @cervellaswarm/core

> Core utilities for CervellaSwarm - shared between CLI and MCP Server

## Installation

```bash
npm install @cervellaswarm/core
```

## Modules

### Client Utilities

Retry logic, timeout handling, and error management.

```typescript
import {
  withRetry,
  withTimeout,
  parseError,
  CervellaSwarmError
} from '@cervellaswarm/core/client';

// Retry API calls with exponential backoff
const result = await withRetry(
  () => anthropicClient.messages.create(...),
  { maxRetries: 3 }
);

// Add timeout to operations
const result = await withTimeout(
  () => longOperation(),
  30000 // 30 seconds
);

// Parse errors to user-friendly format
try {
  await apiCall();
} catch (error) {
  const info = parseError(error);
  console.log(info.message);
  console.log(info.retryable);
}
```

### Workers

Worker types and registry.

```typescript
import {
  getAvailableWorkers,
  isValidWorker,
  type WorkerType
} from '@cervellaswarm/core/workers';

// Get all worker types
const workers = getAvailableWorkers();
// ['backend', 'frontend', 'tester', ...]

// Validate worker type
if (isValidWorker('backend')) {
  // Type-safe: backend is WorkerType
}
```

### Config (Coming Soon)

Configuration management utilities.

```typescript
import { getConfigVersion } from '@cervellaswarm/core/config';
```

## Version

This package is in alpha. API may change.

- v1.0.0-alpha.1: Initial release with client utilities

## License

Apache 2.0

---

*Part of [CervellaSwarm](https://github.com/rafapra3008/CervellaSwarm)*
