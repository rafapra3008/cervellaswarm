# Ricerca: Best Practices Metering/Usage Tracking MCP Server

**Data:** 16 Gennaio 2026
**Researcher:** Cervella Researcher
**Richiesta:** Rafa

---

## TL;DR

**Schema raccomandato:** JSON file con tracking per user+month, auto-reset mensile via timestamp check
**Counting policy:** Conta SOLO chiamate API successful (status 2xx), retry NON conta se fail
**Edge cases:** Idempotency keys per evitare duplicati, timeout handling, graceful degradation
**User Experience:** Warning a 80%, block a 100%, upgrade prompt con CTA chiaro

---

## 1. SCHEMA DATI RACCOMANDATO

### File Structure (usando `conf` package)

```typescript
// config/usage-schema.ts
export interface UsageSchema {
  users: {
    [userId: string]: UserUsage;
  };
  settings: {
    resetDay: number; // 1 = primo del mese
    lastGlobalReset: number; // timestamp
  };
}

export interface UserUsage {
  plan: 'free' | 'pro' | 'team';
  currentPeriod: {
    start: number; // timestamp inizio periodo
    end: number; // timestamp fine periodo
    calls: number; // chiamate effettuate
    limit: number; // limite del piano (50/500/1000)
  };
  history: Array<{
    period: string; // "2026-01"
    calls: number;
    plan: string;
  }>;
  lastCallTimestamp: number;
  metadata: {
    createdAt: number;
    upgradedAt?: number;
    downgradedAt?: number;
  };
}
```

### Esempio JSON Storage

```json
{
  "users": {
    "user_123": {
      "plan": "free",
      "currentPeriod": {
        "start": 1704067200000,
        "end": 1706745599999,
        "calls": 42,
        "limit": 50
      },
      "history": [
        { "period": "2025-12", "calls": 48, "plan": "free" }
      ],
      "lastCallTimestamp": 1706123456789,
      "metadata": {
        "createdAt": 1701388800000
      }
    }
  },
  "settings": {
    "resetDay": 1,
    "lastGlobalReset": 1704067200000
  }
}
```

---

## 2. GESTIONE RESET MENSILE

### Pattern Raccomandato: Lazy Reset on Access

```typescript
class UsageTracker {
  private conf: Conf<UsageSchema>;

  async checkAndResetIfNeeded(userId: string): Promise<void> {
    const user = this.conf.get(`users.${userId}`);
    const now = Date.now();

    // Check se periodo scaduto
    if (now > user.currentPeriod.end) {
      // Archivia periodo precedente
      const prevPeriod = {
        period: this.formatPeriod(user.currentPeriod.start),
        calls: user.currentPeriod.calls,
        plan: user.plan
      };

      // Limita history a ultimi 12 mesi
      const history = [...user.history, prevPeriod].slice(-12);

      // Reset periodo corrente
      const { start, end } = this.getNextPeriodBounds();

      this.conf.set(`users.${userId}`, {
        ...user,
        currentPeriod: {
          start,
          end,
          calls: 0,
          limit: this.getLimitForPlan(user.plan)
        },
        history
      });
    }
  }

  private getNextPeriodBounds(): { start: number; end: number } {
    const now = new Date();
    const start = new Date(now.getFullYear(), now.getMonth(), 1);
    const end = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999);

    return {
      start: start.getTime(),
      end: end.getTime()
    };
  }
}
```

**Perché lazy reset?**
- Nessun cronjob necessario
- Reset automatico al primo accesso del nuovo mese
- Semplice, affidabile, zero dipendenze esterne

---

## 3. CONTEGGIO CHIAMATE API - BEST PRACTICES

### Regola d'Oro: Conta SOLO Successi

```typescript
async trackApiCall(
  userId: string,
  operation: () => Promise<ApiResponse>
): Promise<ApiResponse> {
  // 1. Verifica quota PRIMA di chiamare
  await this.checkAndResetIfNeeded(userId);
  const usage = this.getUsage(userId);

  if (usage.currentPeriod.calls >= usage.currentPeriod.limit) {
    throw new QuotaExceededError({
      current: usage.currentPeriod.calls,
      limit: usage.currentPeriod.limit,
      plan: usage.plan,
      resetsAt: usage.currentPeriod.end
    });
  }

  // 2. Esegui chiamata API
  let response: ApiResponse;
  try {
    response = await operation();
  } catch (error) {
    // IMPORTANTE: Errori NON contano nel quota!
    // - Network timeout
    // - Server 5xx
    // - Request malformed
    throw error;
  }

  // 3. Conta SOLO se successful (2xx)
  if (response.status >= 200 && response.status < 300) {
    await this.incrementUsage(userId);
  }

  return response;
}
```

**Fonti:**
- [Best Practices on API Retries](https://medium.com/@majnun.abdurahmanov/best-practices-on-api-retries-8c0ea4babf4e)
- [Scalable API Rate Limiting System](https://medium.com/@hafeez.fijur/scalable-api-rate-limiting-system-quota-management-system-f936e827ae53)

---

## 4. EDGE CASES DA GESTIRE

### A. Chiamata Fallita - Non Conta

```typescript
// ❌ SBAGLIATO: Conta tutto
calls++;
await callAnthropicAPI();

// ✅ CORRETTO: Conta solo success
const result = await callAnthropicAPI();
if (result.status === 200) {
  calls++;
}
```

**Razionale:** L'utente non ha ricevuto valore, non deve pagare.

---

### B. Retry - Conta Solo Finale Success

```typescript
async callWithRetry(userId: string, maxRetries = 3): Promise<ApiResponse> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      // trackApiCall già gestisce il counting corretto
      return await this.trackApiCall(userId, () => callAnthropicAPI());
    } catch (error) {
      if (error instanceof QuotaExceededError) {
        throw error; // Non retry se quota exceeded
      }

      lastError = error;

      // Exponential backoff
      await sleep(Math.pow(2, attempt) * 1000);
    }
  }

  throw lastError;
}
```

**Policy:**
- Retry automatici NON contano come chiamate separate
- Solo la chiamata successful finale conta
- Quota exceeded = stop immediato, no retry

**Fonti:**
- [Best Practice: Implementing Retry Logic](https://api4.ai/blog/best-practice-implementing-retry-logic-in-http-api-clients)
- [Retry Policy Recommendations](https://developers.liveperson.com/retry-policy-recommendations.html)

---

### C. Idempotency Keys (Evitare Duplicati)

```typescript
interface CallOptions {
  idempotencyKey?: string;
}

async trackApiCall(
  userId: string,
  operation: () => Promise<ApiResponse>,
  options?: CallOptions
): Promise<ApiResponse> {
  // Check idempotency key cache
  if (options?.idempotencyKey) {
    const cached = this.idempotencyCache.get(options.idempotencyKey);
    if (cached) {
      return cached; // Return cached, NON conta di nuovo
    }
  }

  const response = await this.executeAndCount(userId, operation);

  // Cache per 24h
  if (options?.idempotencyKey && response.status === 200) {
    this.idempotencyCache.set(
      options.idempotencyKey,
      response,
      { ttl: 86400 }
    );
  }

  return response;
}
```

**Use case:** Client retry dopo network timeout - evita doppio conteggio.

**Fonte:**
- [Retry failed API requests - LINE Developers](https://developers.line.biz/en/docs/messaging-api/retrying-api-request/)

---

### D. Timeout Handling

```typescript
async callWithTimeout(
  userId: string,
  timeoutMs = 30000
): Promise<ApiResponse> {
  const timeoutPromise = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new TimeoutError()), timeoutMs)
  );

  try {
    return await Promise.race([
      this.trackApiCall(userId, () => callAnthropicAPI()),
      timeoutPromise
    ]);
  } catch (error) {
    if (error instanceof TimeoutError) {
      // Timeout NON conta nel quota
      // Ma logga per monitoring
      logger.warn('API call timeout', { userId, timeoutMs });
    }
    throw error;
  }
}
```

**Importante:** Timeout significa risposta non ricevuta = nessun valore = non conta.

---

### E. Concurrent Calls Race Condition

```typescript
// PROBLEMA: Due chiamate simultanee potrebbero entrambe vedere "49/50" e passare
async incrementUsage(userId: string): Promise<void> {
  // ❌ UNSAFE: Read-modify-write race
  const current = this.conf.get(`users.${userId}.currentPeriod.calls`);
  this.conf.set(`users.${userId}.currentPeriod.calls`, current + 1);
}

// ✅ SOLUZIONE: Atomic increment con lock
import pMutex from 'p-mutex';

private userLocks = new Map<string, Mutex>();

async incrementUsage(userId: string): Promise<void> {
  const lock = this.getUserLock(userId);

  await lock.runExclusive(() => {
    const current = this.conf.get(`users.${userId}.currentPeriod.calls`);
    this.conf.set(`users.${userId}.currentPeriod.calls`, current + 1);
    this.conf.set(`users.${userId}.lastCallTimestamp`, Date.now());
  });
}
```

**Alternative (se single process):** `conf` package già fa atomic writes su file system.

---

## 5. USER EXPERIENCE - UPGRADE PROMPTS

### Pattern: Progressive Warnings

```typescript
enum QuotaStatus {
  OK = 'ok',           // < 80%
  WARNING = 'warning', // 80-100%
  EXCEEDED = 'exceeded' // >= 100%
}

function getQuotaStatus(usage: UserUsage): QuotaStatus {
  const percentage = (usage.currentPeriod.calls / usage.currentPeriod.limit) * 100;

  if (percentage >= 100) return QuotaStatus.EXCEEDED;
  if (percentage >= 80) return QuotaStatus.WARNING;
  return QuotaStatus.OK;
}

// User-friendly messages
const MESSAGES = {
  [QuotaStatus.WARNING]: {
    title: "You're running low on API calls",
    message: "You've used {used} of {limit} calls this month. Consider upgrading to Pro for 500 calls/month.",
    action: "Upgrade to Pro",
    style: "warning"
  },
  [QuotaStatus.EXCEEDED]: {
    title: "Monthly limit reached",
    message: "You've used all {limit} calls for {plan} plan. Upgrade now to continue or wait until {resetDate}.",
    action: "Upgrade Now",
    style: "error"
  }
};
```

### Response Headers (per monitoring client-side)

```typescript
function addUsageHeaders(response: Response, usage: UserUsage): void {
  response.headers.set('X-RateLimit-Limit', usage.currentPeriod.limit.toString());
  response.headers.set('X-RateLimit-Remaining',
    Math.max(0, usage.currentPeriod.limit - usage.currentPeriod.calls).toString()
  );
  response.headers.set('X-RateLimit-Reset',
    new Date(usage.currentPeriod.end).toISOString()
  );

  const status = getQuotaStatus(usage);
  if (status !== QuotaStatus.OK) {
    response.headers.set('X-RateLimit-Status', status);
  }
}
```

**Fonte:**
- [API Governance using Quota - KrakenD](https://www.krakend.io/docs/enterprise/governance/quota/)

---

## 6. IMPLEMENTAZIONE COMPLETA

### File: `src/usage-tracker.ts`

```typescript
import Conf from 'conf';
import { Mutex } from 'async-mutex';

export class UsageTracker {
  private conf: Conf<UsageSchema>;
  private userLocks = new Map<string, Mutex>();

  constructor(configPath?: string) {
    this.conf = new Conf<UsageSchema>({
      projectName: 'mcp-usage',
      configName: 'usage',
      cwd: configPath,
      schema: {
        users: { type: 'object' },
        settings: {
          type: 'object',
          properties: {
            resetDay: { type: 'number', default: 1 },
            lastGlobalReset: { type: 'number' }
          }
        }
      }
    });
  }

  async trackCall(userId: string, operation: () => Promise<ApiResponse>): Promise<ApiResponse> {
    // 1. Check & reset if needed
    await this.checkAndResetIfNeeded(userId);

    // 2. Verify quota
    const usage = this.getUsage(userId);
    if (usage.currentPeriod.calls >= usage.currentPeriod.limit) {
      throw new QuotaExceededError(this.buildQuotaError(usage));
    }

    // 3. Execute operation
    let response: ApiResponse;
    try {
      response = await operation();
    } catch (error) {
      // Failed calls don't count
      throw error;
    }

    // 4. Count only successful calls
    if (response.status >= 200 && response.status < 300) {
      await this.incrementUsage(userId);
    }

    return response;
  }

  private async checkAndResetIfNeeded(userId: string): Promise<void> {
    const lock = this.getUserLock(userId);

    await lock.runExclusive(() => {
      const user = this.conf.get(`users.${userId}`);
      if (!user) {
        this.initializeUser(userId);
        return;
      }

      const now = Date.now();
      if (now > user.currentPeriod.end) {
        this.resetUserPeriod(userId, user);
      }
    });
  }

  private async incrementUsage(userId: string): Promise<void> {
    const lock = this.getUserLock(userId);

    await lock.runExclusive(() => {
      const calls = this.conf.get(`users.${userId}.currentPeriod.calls`);
      this.conf.set(`users.${userId}.currentPeriod.calls`, calls + 1);
      this.conf.set(`users.${userId}.lastCallTimestamp`, Date.now());
    });
  }

  private getUserLock(userId: string): Mutex {
    if (!this.userLocks.has(userId)) {
      this.userLocks.set(userId, new Mutex());
    }
    return this.userLocks.get(userId)!;
  }

  getUsage(userId: string): UserUsage {
    return this.conf.get(`users.${userId}`);
  }

  getQuotaStatus(userId: string): QuotaStatus {
    const usage = this.getUsage(userId);
    const percentage = (usage.currentPeriod.calls / usage.currentPeriod.limit) * 100;

    if (percentage >= 100) return QuotaStatus.EXCEEDED;
    if (percentage >= 80) return QuotaStatus.WARNING;
    return QuotaStatus.OK;
  }

  // ... altri metodi helper
}
```

---

## 7. MONITORING & LOGGING

### Metriche da Tracciare

```typescript
interface UsageMetrics {
  // Per user
  callsPerUser: Record<string, number>;
  quotaExceededCount: Record<string, number>;

  // Globali
  totalCallsToday: number;
  totalCallsMonth: number;
  uniqueUsersToday: number;

  // Per plan
  callsByPlan: {
    free: number;
    pro: number;
    team: number;
  };

  // Performance
  avgResponseTime: number;
  errorRate: number; // % chiamate fallite
  retryRate: number; // % chiamate con retry
}
```

### Logging Best Practices

```typescript
logger.info('API call tracked', {
  userId,
  callsRemaining: usage.currentPeriod.limit - usage.currentPeriod.calls,
  plan: usage.plan,
  responseTime: endTime - startTime,
  status: response.status
});

// Alert se quota exceeded frequente
if (quotaExceededCount > threshold) {
  logger.warn('High quota exceeded rate', {
    userId,
    count: quotaExceededCount,
    plan: usage.plan,
    suggestion: 'Consider reaching out for upgrade'
  });
}
```

**Fonte:**
- [MCP Server Monitoring Lessons Learned](https://huggingface.co/blog/mclenhard/mcp-monitoring)
- [Unlocking User Insights: MCP Server Monitoring](https://www.arsturn.com/blog/unlocking-user-insights-monitoring-and-enhancing-your-mcp-server-experience)

---

## 8. TESTING CHECKLIST

### Unit Tests

```typescript
describe('UsageTracker', () => {
  it('should count only successful calls', async () => {
    const tracker = new UsageTracker();

    // Failed call - should NOT count
    await expect(tracker.trackCall('user1', () => Promise.reject())).rejects.toThrow();
    expect(tracker.getUsage('user1').currentPeriod.calls).toBe(0);

    // Successful call - should count
    await tracker.trackCall('user1', () => Promise.resolve({ status: 200 }));
    expect(tracker.getUsage('user1').currentPeriod.calls).toBe(1);
  });

  it('should auto-reset at month boundary', async () => {
    const tracker = new UsageTracker();

    // Set usage in previous month
    tracker.conf.set('users.user1.currentPeriod', {
      start: Date.parse('2025-12-01'),
      end: Date.parse('2025-12-31 23:59:59'),
      calls: 45,
      limit: 50
    });

    // Check in January - should auto-reset
    await tracker.checkAndResetIfNeeded('user1');
    expect(tracker.getUsage('user1').currentPeriod.calls).toBe(0);
  });

  it('should handle concurrent increments correctly', async () => {
    const tracker = new UsageTracker();

    // Simulate 10 concurrent calls
    await Promise.all(
      Array(10).fill(null).map(() =>
        tracker.trackCall('user1', () => Promise.resolve({ status: 200 }))
      )
    );

    expect(tracker.getUsage('user1').currentPeriod.calls).toBe(10);
  });
});
```

---

## 9. RACCOMANDAZIONI FINALI

### DO ✅

1. **Conta solo success (2xx)** - utente riceve valore
2. **Reset automatico lazy** - primo accesso nuovo mese
3. **Lock atomic per incrementi** - evita race conditions
4. **Idempotency keys** - client retry sicuro
5. **History 12 mesi** - analytics e compliance
6. **Headers X-RateLimit-*** - client monitoring
7. **Warning progressivi (80%)** - UX non aggressiva
8. **Logging dettagliato** - debug e analytics

### DON'T ❌

1. **Non contare fails/timeouts** - utente non riceve valore
2. **Non contare retry multipli** - solo final success
3. **Non cronjob per reset** - lazy reset più semplice
4. **Non block senza warning** - frustrazione utente
5. **Non perdere history** - importante per upgrade decision
6. **Non race conditions** - usa lock
7. **Non hard-code limiti** - usa config per plan

---

## 10. PROSSIMI STEP SUGGERITI

### Implementazione Base (MVP)

1. Setup `conf` package con schema
2. Implementa `UsageTracker` class base
3. Integra in MCP handler spawn agents
4. Test unit per edge cases
5. Logging basic

### Enhancement Fase 2

1. Dashboard usage per user
2. Email notification a 80% quota
3. Analytics: trend usage per plan
4. Auto-suggest upgrade basato su pattern
5. Export usage per billing

### Fase 3 (Scalabilità)

1. Migrazione da file JSON a Redis (se multi-instance)
2. Distributed locks (se cluster)
3. Real-time metrics dashboard
4. A/B test pricing tiers

---

## FONTI PRINCIPALI

### MCP Monitoring & Best Practices
- [MCP Server Best Practices for 2026](https://www.cdata.com/blog/mcp-server-best-practices-2026)
- [Monitor your MCP server | Speakeasy](https://www.speakeasy.com/mcp/monitoring-mcp-servers)
- [MCP Server Monitoring Lessons Learned](https://huggingface.co/blog/mclenhard/mcp-monitoring)
- [How to Setup Observability for MCP Server with Moesif](https://www.moesif.com/blog/monitoring/model-context-protocol/How-to-Setup-Observability-For-Your-MCP-Server-with-Moesif/)

### Rate Limiting & Usage Tracking
- [Scalable API Rate Limiting System & Quota Management](https://medium.com/@hafeez.fijur/scalable-api-rate-limiting-system-quota-management-system-f936e827ae53)
- [API Governance using Quota - KrakenD](https://www.krakend.io/docs/enterprise/governance/quota/)
- [rate-limiter-flexible - npm](https://www.npmjs.com/package/rate-limiter-flexible)
- [express-rate-limit - npm](https://www.npmjs.com/package/express-rate-limit)

### Retry Logic & Edge Cases
- [Best Practice: Implementing Retry Logic in HTTP API Clients](https://api4.ai/blog/best-practice-implementing-retry-logic-in-http-api-clients)
- [Best Practices on API Retries](https://medium.com/@majnun.abdurahmanov/best-practices-on-api-retries-8c0ea4babf4e)
- [Retry failed API requests | LINE Developers](https://developers.line.biz/en/docs/messaging-api/retrying-api-request/)
- [Retry Policy Recommendations | LivePerson](https://developers.liveperson.com/retry-policy-recommendations.html)

### File Storage TypeScript
- [conf - npm](https://www.npmjs.com/package/conf)
- [node-json-db - npm](https://www.npmjs.com/package/node-json-db)

---

## RIEPILOGO DECISIONI

| Aspetto | Scelta | Motivazione |
|---------|--------|-------------|
| **Storage** | File JSON via `conf` | Semplice, atomic writes, schema validation |
| **Reset** | Lazy on access | No cronjob, self-healing |
| **Counting** | Solo 2xx success | Utente riceve valore solo se success |
| **Retry** | Non conta multipli | Solo final success conta |
| **Concurrency** | Mutex lock | Evita race conditions increment |
| **Idempotency** | Key cache 24h | Client retry safe |
| **UX** | Warning 80%, block 100% | Progressive, non aggressivo |
| **History** | 12 mesi | Analytics + compliance |

---

*Ricerca completata: 16 Gennaio 2026*
*Tempo ricerca: ~15 minuti*
*Fonti consultate: 25+*
*Confidenza raccomandazioni: ALTA (basato su industry best practices)*
