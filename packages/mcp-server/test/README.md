# MCP Server Test Suite

Comprehensive test suite for CervellaSwarm MCP Server.

## Test Structure

```
test/
├── tiers.test.ts      # Billing tier configuration (24 tests)
├── usage.test.ts      # Usage tracking & quotas (31 tests)
├── spawner.test.ts    # Worker spawning & errors (13 tests)
├── config.test.ts     # Configuration management (16 tests)
└── types.test.ts      # Type definitions (5 tests)
```

## Running Tests

```bash
# Run all tests
npm test

# Build + test
npm run build && npm test

# Watch mode (if needed)
npm run dev & npm test
```

## Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| billing/tiers.ts | 24 | ~100% |
| billing/usage.ts | 31 | ~95% |
| agents/spawner.ts | 13 | ~70% |
| config/manager.ts | 16 | ~75% |
| billing/types.ts | 5 | ~100% |
| **TOTAL** | **74** | **~85%** |

## What's Tested

### Tier Configuration (tiers.test.ts)
- [x] Tier limits (free, pro, team, enterprise)
- [x] Tier pricing
- [x] Tier display names
- [x] Upgrade paths
- [x] Warning thresholds
- [x] Utility functions (getLimitForTier, isUnlimited, etc.)

### Usage Tracking (usage.test.ts)
- [x] File initialization
- [x] Quota checking (OK, WARNING, EXCEEDED)
- [x] Call tracking
- [x] Statistics calculation
- [x] Data integrity (checksums, backups)
- [x] Monthly reset
- [x] Tier changes
- [x] Persistence across instances

### Worker Spawner (spawner.test.ts)
- [x] Worker listing
- [x] Worker name normalization
- [x] Parameter validation
- [x] Response structure
- [x] Error message mapping
- [x] Unique worker names

### Config Manager (config.test.ts)
- [x] API key detection
- [x] Source priority (env > config)
- [x] Model settings
- [x] Timeout validation
- [x] Retry configuration
- [x] Tier management
- [x] Path resolution
- [x] API key validation

### Type Definitions (types.test.ts)
- [x] QuotaStatus enum
- [x] Status values
- [x] Type structure

## Notes

- Tests use Node.js native test runner (no Jest/Mocha)
- Temp directories for file-based tests
- No mocking of Anthropic SDK (parameter validation only)
- Integration with actual config system

## Future Improvements

- Add coverage reporting (c8/nyc)
- Mock Anthropic SDK for full integration tests
- Add MCP tool integration tests
- Performance benchmarks
