# Output: Test API CervellaSwarm

## Risultato
✅ Test suite API completata e funzionante

## File Creati

### Struttura Test
```
packages/api/test/
├── helpers/
│   ├── mock-stripe.js      # Mock Stripe SDK + webhook signature
│   └── mock-express.js     # Mock Express req/res
├── webhooks.test.js        # 22 test webhook handler
├── checkout.test.js        # 12 test checkout route
└── README.md               # Documentazione suite
```

### package.json
```json
"test": "node --test test/*.test.js",
"test:watch": "node --test --watch test/*.test.js"
```

## Test Coverage

### webhooks.test.js (22 test)
- ✅ Signature verification (valid/invalid/missing)
- ✅ checkout.session.completed handler
- ✅ invoice.paid handler
- ✅ invoice.payment_failed handler
- ✅ customer.subscription.created handler
- ✅ customer.subscription.updated handler
- ✅ customer.subscription.deleted handler
- ✅ Unknown event type (logs + returns 200)
- ✅ Edge cases (missing data, API errors, DB errors)

### checkout.test.js (12 test)
- ✅ Input validation (tier, email)
- ✅ Payment link creation (pro/team)
- ✅ Payment link caching
- ✅ Error handling (Stripe API, network)
- ✅ Edge cases (case sensitivity, whitespace, special chars)

## Test Results

```
✅ tests 34
✅ pass  34
❌ fail  0
⏱  duration 35ms
```

## Mock Pattern

**Mock completo offline:**
- Stripe SDK (customers, subscriptions, paymentLinks, webhooks)
- Webhook signature generation + verification
- Database in-memory (Map-based)
- Express req/res objects

**Nessuna chiamata esterna:**
- No Stripe API reale
- No database reale
- Test veloci e deterministici

## Come Eseguire

```bash
cd packages/api

# Run tutti i test
npm test

# Watch mode
npm test:watch

# Output
▶ Checkout Route (12 test)
  ✔ Input Validation (7 test)
  ✔ Payment Link Creation (4 test)
  ✔ Caching (3 test)

▶ Webhook Handler (22 test)
  ✔ Signature Verification (4 test)
  ✔ Event Handlers (6 test)
  ✔ Edge Cases (5 test)
```

## Filosofia Applicata

> "Se non è testato, non funziona."

- **Happy path** + **Sad path** testati
- **Edge cases** coperti (null, empty, invalid, missing)
- **Mock intelligenti** - Solo dipendenze esterne
- **Report chiari** - describe/test pattern Node.js

## Success Criteria

- [x] Struttura test/ creata
- [x] Helper mock (Stripe + Express)
- [x] Test webhooks.ts (signature + handlers)
- [x] Test checkout.ts (validation + creation)
- [x] Script npm test funzionanti
- [x] Tutti i test passano (34/34)
- [x] Pattern coerente con CLI
- [x] Documentazione README

## Note Tecniche

**Node.js Test Runner:**
- Native `node:test` module (no deps)
- `describe/test/assert` pattern
- Mock con `t.mock.method()`
- Stesso stile della CLI

**Mock Webhook Signature:**
- HMAC SHA256 (crypto)
- Formato Stripe: `t=timestamp,v1=signature`
- Verifica valida/invalida simulata

**Mock Database:**
- Map in-memory
- CRUD operations complete
- Reset tra test (beforeEach)

---

*Completato: 17 Gennaio 2026*
*Cervella Tester*
*"Edge cases trovati. API protetta."*
