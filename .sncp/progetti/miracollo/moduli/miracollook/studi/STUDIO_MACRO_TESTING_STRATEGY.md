# STUDIO MACRO: TESTING STRATEGY MIRACOLLOOK

> **Data:** 15 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Livello:** MACRO (strategia generale, tools, coverage targets)
> **Progetto:** Miracollook (Backend Python/FastAPI + Frontend React/TypeScript)

---

## EXECUTIVE SUMMARY

Testing strategy per Miracollook basata su best practices 2026 dei big players.

**Stack:**
- Backend: Python + FastAPI
- Frontend: React + TypeScript + Vite
- API Esterna: Gmail API

**Raccomandazione:**
- Backend: pytest + VCR.py (Gmail mock)
- Frontend: Vitest + RTL + MSW
- E2E: Playwright (solo critical paths)
- Coverage target: 70% (pragmatico, non dogmatico)

---

## 1. BACKEND TESTING STRATEGY (Python/FastAPI)

### 1.1 Tool Selection

**pytest > unittest**
- Standard de facto per FastAPI (docs ufficiali lo usano)
- Fixtures native + async support
- pytest-cov per coverage
- pytest-asyncio per async endpoints
- Ecosystem maturo (2026)

**VCR.py per Gmail API**
- Record/replay reale API Gmail (cassette YAML)
- Zero setup dopo prima run
- Redact secrets (auth headers)
- Test deterministici + veloci
- pytest-recording per integrazione pytest

### 1.2 Test Structure

```
backend/tests/
├── conftest.py              # Fixtures condivise
├── unit/
│   ├── test_services.py     # Business logic
│   └── test_utils.py        # Helper functions
├── integration/
│   ├── test_api_endpoints.py
│   └── test_database.py
└── fixtures/
    └── cassettes/           # VCR Gmail responses
```

### 1.3 Coverage Target

**70% realistico**
- Unit tests: business logic core (80% coverage)
- Integration: API endpoints (60% coverage)
- Happy paths + edge cases critici
- NO 100% dogmatico (pragmatic approach)

**Cosa testare PRIMA:**
1. Gmail API integration (VCR)
2. Email parsing/formatting
3. Auth/token refresh
4. Attachment handling
5. Error handling

**Cosa testare DOPO:**
- Edge cases non critici
- Validator input (FastAPI fa già)
- Utils semplici

### 1.4 Gmail API Mocking

**VCR.py Pattern:**
```python
# conftest.py
@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization", "x-goog-api-key"],
        "record_mode": "once"
    }

# test_gmail_service.py
@pytest.mark.vcr
def test_fetch_emails(gmail_service):
    emails = gmail_service.fetch_inbox(limit=10)
    assert len(emails) == 10
    # Prima run: chiama Gmail API reale, salva cassette
    # Run successive: replay da cassette, veloce!
```

**Vantaggi:**
- Test con dati REALI (no mock manuale)
- Veloce dopo prima run
- Cassette committabili (secrets redacted)
- Zero coupling con implementazione

---

## 2. FRONTEND TESTING STRATEGY (React/TypeScript)

### 2.1 Tool Selection

**Vitest > Jest (2026)**
- Velocità: 10-20x più veloce in watch mode
- Zero config con Vite (già usi Vite!)
- ESM/TypeScript native
- 95% compatibile con Jest API
- Memoria: 800MB vs 1.2GB (Jest)
- CI cost reduction

**React Testing Library (RTL)**
- Standard de facto React (2026)
- Test user behavior, non implementazione
- Accessibility-first
- Ottimo con Vitest

**MSW (Mock Service Worker)**
- Industry standard API mocking
- Network-level intercept (Service Worker)
- Reusabile: test + Storybook + dev
- NO stub fetch/axios
- Raccomandata da RTL docs

### 2.2 Test Structure

```
frontend/tests/
├── setup.ts                 # Vitest config
├── mocks/
│   └── handlers.ts          # MSW handlers (API Gmail mock)
├── components/
│   ├── EmailList.test.tsx
│   ├── EmailViewer.test.tsx
│   └── Compose.test.tsx
└── integration/
    └── email-flow.test.tsx
```

### 2.3 Coverage Target

**70% realistico**
- Component tests: 75% coverage
- Integration tests: 50% coverage
- Critical user flows completi
- NO 100% (pragmatic)

**Cosa testare PRIMA:**
1. EmailList rendering + interactions
2. EmailViewer display + mark read
3. Compose + send
4. Attachment upload/display
5. Error states

**Cosa testare DOPO:**
- Edge cases UI non critici
- Styling tests (visual regression separato)
- Utils semplici

### 2.4 API Mocking (MSW)

**Pattern:**
```typescript
// mocks/handlers.ts
export const handlers = [
  rest.get('/api/gmail/messages', (req, res, ctx) => {
    return res(ctx.json({ messages: mockEmails }))
  }),
  rest.post('/api/gmail/send', (req, res, ctx) => {
    return res(ctx.status(200))
  })
]

// test
test('renders email list', async () => {
  render(<EmailList />)
  const emails = await screen.findAllByRole('listitem')
  expect(emails).toHaveLength(10)
})
```

**Vantaggi:**
- Mock network-level (realismo)
- Reusabile in Storybook
- No coupling con fetch/axios
- Testing Library recommended

---

## 3. E2E TESTING (Playwright)

### 3.1 Playwright > Cypress (2026)

**Perché Playwright:**
- Cross-browser: Chrome, Firefox, Safari (WebKit)
- Performance: 90min → 14min (case study healthcare)
- Parallel native: 15 workers (no external service)
- Multi-language (Python, Java, C#)
- Flakiness: 6.5% → 1.8%
- CI cost reduction

**Quando Cypress:**
- Team JS-only
- Real-time feedback UI critico
- Progetti small/medium
- Chrome-only ok

**Per Miracollook: Playlist > Cypress**
- Need Safari/Firefox testing (hotel multi-browser)
- CI scalability importante
- Cross-language team (Python backend)

### 3.2 E2E Scope (LIMITATO!)

**Solo critical paths:**
1. Login + auth flow
2. Inbox → Read email → Reply
3. Compose + Send
4. Attachment upload

**NO E2E per:**
- Edge cases (unit/integration)
- Styling
- Ogni variazione UI

**Effort: 5-7% test suite totale**

---

## 4. TEST PYRAMID & COVERAGE

### 4.1 Distribution

```
        E2E (5%)      ← Playwright, critical paths only
       /        \
      /          \
 Integration (25%)  ← pytest integration + Vitest integration
    /            \
   /              \
Unit Tests (70%)   ← pytest unit + Vitest component tests
```

**Rationale:**
- Unit: cheap, fast, stable (70-80% suite)
- Integration: best speed-to-confidence ratio
- E2E: expensive, slow, flaky (5-7% suite)

### 4.2 Coverage Targets

| Layer | Target | Rationale |
|-------|--------|-----------|
| **Unit** | 70-80% | Core business logic + components |
| **Integration** | 50-60% | API + database + UI flows |
| **E2E** | Critical paths | Login, send, reply, attach |

**NOT 100%!** Pragmatic approach:
- Focus su high-value code
- Skip trivial utils
- Skip auto-generated (validators)
- Cost/benefit analysis

### 4.3 Metrics

**Track:**
- Coverage % per layer
- Test execution time
- Flakiness rate (target < 2%)
- Bug escape rate (prod bugs non caught)

**Adjust pyramid se:**
- E2E troppo lento → più integration
- Bug escape alto → più E2E critical
- CI troppo lento → ridurre E2E

---

## 5. MOCKING APPROACH

### 5.1 Gmail API (Backend)

**VCR.py cassettes:**
- Prima run: record da Gmail reale
- Successive: replay da YAML
- Cassettes committate (secrets redacted)
- Update quando API cambia

**Fixture realistic:**
```
fixtures/cassettes/
├── gmail_inbox_10_messages.yaml
├── gmail_send_success.yaml
├── gmail_attachment_download.yaml
└── gmail_thread_view.yaml
```

### 5.2 API Calls (Frontend)

**MSW handlers:**
- Mock all `/api/gmail/*` endpoints
- Response format = backend reale
- Error scenarios mockabili
- Reusabile in Storybook

**Fixture realistic:**
```typescript
const mockEmails = [
  { id: '1', subject: 'Booking Naturae', from: 'guest@...', ... },
  // ... 9 more realistic emails
]
```

### 5.3 Best Practices

**DO:**
- Mock external services (Gmail)
- Use realistic data
- Test error scenarios
- Commit fixtures

**DON'T:**
- Mock everything (no over-mocking)
- Use fake data (mock REALISTIC)
- Skip error tests
- Ignore cassette updates

---

## 6. BEST PRACTICES 2026

### 6.1 Test First or After?

**Hybrid approach (pragmatico):**
- TDD per business logic core (Gmail parsing, formatting)
- Test dopo per UI (component rendering)
- Integration dopo feature completa

**Rationale:**
- TDD ottimo per algoritmi/logic
- Test-after ok per UI (design evolve)
- Balance dogma vs pragmatismo

### 6.2 CI/CD Integration

**Pipeline:**
1. Unit tests (fast) → ogni commit
2. Integration tests → ogni PR
3. E2E tests → pre-deploy only

**Parallelization:**
- pytest: pytest-xdist (multi-worker)
- Vitest: built-in parallel
- Playwright: native 15 workers

**Fail-fast:**
- Unit fail → block commit
- Integration fail → block merge
- E2E fail → block deploy

### 6.3 Test Data

**Realistic > Fake:**
- Use VCR for real Gmail data
- Mock emails based on real booking scenarios
- Test edge cases with real data patterns

**Privacy:**
- Redact PII in cassettes
- Use test accounts (no prod data)
- Sanitize fixtures before commit

---

## 7. EFFORT ESTIMATO (0% → 70%)

### 7.1 Backend (Python/FastAPI)

| Task | Effort | Note |
|------|--------|------|
| Setup pytest + fixtures | 2h | conftest.py, test DB |
| VCR.py integration | 3h | Cassette Gmail API |
| Unit tests core services | 8h | Gmail, parsing, formatting |
| Integration tests API | 6h | Endpoints + DB |
| Error handling tests | 4h | Edge cases |
| **TOTALE BACKEND** | **23h** | ~3 giorni |

### 7.2 Frontend (React/TypeScript)

| Task | Effort | Note |
|------|--------|------|
| Setup Vitest + RTL | 2h | Config + first test |
| MSW integration | 2h | Handlers mock API |
| Component tests | 10h | EmailList, Viewer, Compose |
| Integration tests | 5h | User flows |
| Error states tests | 3h | Loading, errors, empty |
| **TOTALE FRONTEND** | **22h** | ~3 giorni |

### 7.3 E2E (Playwright)

| Task | Effort | Note |
|------|--------|------|
| Setup Playwright | 2h | Config + first test |
| Critical paths | 6h | 4 flows completi |
| CI integration | 2h | Parallel + artifacts |
| **TOTALE E2E** | **10h** | ~1.5 giorni |

### 7.4 TOTALE

**55 ore → ~7 giorni lavorativi**
- Backend: 3 giorni
- Frontend: 3 giorni
- E2E: 1.5 giorni

**Approccio incrementale:**
- Week 1: Setup + unit tests (30h)
- Week 2: Integration + E2E (25h)

---

## 8. RACCOMANDAZIONE FINALE

### 8.1 Stack Definitivo

**Backend:**
- pytest + pytest-asyncio + pytest-cov
- VCR.py (Gmail mock)
- SQLite in-memory (test DB)

**Frontend:**
- Vitest (velocità + Vite integration)
- React Testing Library
- MSW (API mock)

**E2E:**
- Playwright (cross-browser + performance)
- Solo critical paths (5% suite)

### 8.2 Priorità

**FASE 1 (High Priority):**
1. Gmail API mocking (VCR) - critical!
2. Backend unit tests core logic
3. Frontend component tests core UI

**FASE 2 (Medium Priority):**
4. Integration tests API
5. Integration tests user flows
6. Error handling tests

**FASE 3 (Optional):**
7. E2E critical paths
8. Edge cases non critici
9. Coverage refinement

### 8.3 Success Metrics

**Target 6 mesi:**
- Coverage: 70%+ (backend + frontend)
- Test execution: < 5 min (unit + integration)
- E2E execution: < 15 min
- Flakiness: < 2%
- CI cost: reasonable (Playwright parallel)

---

## SOURCES

**Backend Testing:**
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing FastAPI with Pytest - Medium](https://medium.com/@gnetkov/testing-fastapi-application-with-pytest-57080960fd62)
- [FastAPI Testing Best Practices - FrugalTesting](https://www.frugaltesting.com/blog/what-is-fastapi-testing-tools-frameworks-and-best-practices)
- [Pytest FastAPI Tutorial - Pytest with Eric](https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/)

**VCR.py:**
- [Test APIs with VCR.py - Brian Hicks](https://www.brianthicks.com/post/2014/12/01/test-apis-properly-with-vcr-py/)
- [pytest-recording VCR - Simon Willison](https://til.simonwillison.net/pytest/pytest-recording-vcr)
- [Python REST API Testing - Pytest With Eric](https://pytest-with-eric.com/pytest-best-practices/python-rest-api-unit-testing/)

**Frontend Testing:**
- [Vitest vs Jest 2025 - Medium](https://medium.com/@ruverd/jest-vs-vitest-which-test-runner-should-you-use-in-2025-5c85e4f2bda9)
- [Vitest vs Jest Comparison - Better Stack](https://betterstack.com/community/guides/scaling-nodejs/vitest-vs-jest/)
- [Vitest Official Comparisons](https://vitest.dev/guide/comparisons)

**MSW:**
- [MSW Official Docs](https://mswjs.io/)
- [React Testing Library Example](https://testing-library.com/docs/react-testing-library/example-intro/)
- [MSW Guide - Callstack](https://www.callstack.com/blog/guide-to-mock-service-worker-msw)

**E2E Testing:**
- [Playwright vs Cypress 2026 - Medium](https://devin-rosario.medium.com/playwright-vs-cypress-the-2026-enterprise-testing-guide-ade8b56d3478)
- [Playwright vs Cypress Comparison - TestMu](https://www.testmu.ai/blog/cypress-vs-playwright/)
- [E2E Testing Showdown - FrugalTesting](https://www.frugaltesting.com/blog/playwright-vs-cypress-the-ultimate-2025-e2e-testing-showdown)

**Test Pyramid:**
- [Testing Pyramid Guide - VirtuosoQA](https://www.virtuosoqa.com/post/what-is-the-testing-pyramid)
- [Test Pyramid Strategy - Lead With Skills](https://www.leadwithskills.com/blogs/test-pyramid-strategy-unit-integration-e2e-balance)
- [Testing Pyramid Best Practices - CircleCI](https://circleci.com/blog/testing-pyramid/)

---

*"Nulla è complesso - solo non ancora studiato!"*
*"Fatto BENE > Fatto VELOCE"*
*"70% pragmatico > 100% dogmatico"*
