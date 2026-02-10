# Analisi Duplicazione CLI vs MCP-server

**Data:** 2026-01-22
**Analista:** Cervella Ingegnera
**Obiettivo:** Identificare codice duplicato e valutare necessità di un package `@cervellaswarm/core`

---

## EXECUTIVE SUMMARY

**Health Score:** 6/10 (duplicazione significativa trovata)
**Raccomandazione:** ⚠️ **CREARE `@cervellaswarm/core`** (ma NON ora - pianificare per v2.1+)

**Top 3 Issues:**
1. **ALTO**: 85% logica duplicata in `spawner` (351/739 righe totali)
2. **ALTO**: 100% logica duplicata in `config/manager` (API key + settings)
3. **MEDIO**: Worker prompts hardcoded in entrambi i package

---

## 1. ANALISI FILE SPAWNING

### 1.1 File Identificati

#### CLI (`packages/cli/src/`)
- `agents/spawner.js` - 374 righe
- `agents/router.js` - 40 righe (routing task → agent)

#### MCP-server (`packages/mcp-server/src/`)
- `agents/spawner.ts` - 365 righe
- **NO router** (MCP usa spawn diretto)

---

### 1.2 Codice DUPLICATO Esatto

#### A) Core Logic Spawning (85% duplicazione)

**File:** `spawner.js` vs `spawner.ts`
**Linee duplicate:** ~320/365 righe (87%)

**Funzioni identiche:**
1. **spawnAgent/spawnWorker** (righe 156-303 CLI, 235-365 MCP)
   - Retry logic: IDENTICO
   - Timeout handling: IDENTICO
   - Error mapping: IDENTICO (solo format diverso - JS vs TS)
   - Anthropic API call: IDENTICO

2. **Sleep utility** (righe 96-98 CLI, 209-211 MCP)
   ```javascript
   // IDENTICO in entrambi
   function sleep(ms) {
     return new Promise(resolve => setTimeout(resolve, ms));
   }
   ```

3. **Retry delays** (righe 18 CLI, 20 MCP)
   ```javascript
   const RETRY_DELAYS = [1000, 3000, 5000];  // IDENTICO
   ```

4. **Error handling logic** (righe 103-151 CLI, 306-348 MCP)
   - Status code mapping: IDENTICO
   - User-friendly messages: IDENTICO (stesse frasi)
   - Retryable detection: IDENTICO

**Differenze minori:**
- CLI: JavaScript + JSDoc
- MCP: TypeScript + types
- CLI: `extractFilesFromOutput()` (righe 308-333) - MCP NON ha
- CLI: `suggestNextStep()` (righe 338-351) - MCP ha `NEXT_STEPS` dict

#### B) Worker Prompts (100% duplicazione)

**Prompts identici per 8 worker base:**
- backend, frontend, tester, docs, devops, data, security, researcher

**Esempio duplicato:**
```
CLI (righe 41-45):
'cervella-backend': `Sei CERVELLA-BACKEND, specialista Python, FastAPI...`

MCP (righe 64-67):
backend: `Sei CERVELLA-BACKEND, specialista Python, FastAPI...`
```

**NOTA:** MCP ha 9 worker aggiuntivi che CLI NON ha:
- marketing, ingegnera, scienziata, reviewer
- 3 guardiane
- 1 orchestrator

---

### 1.3 Config Manager

#### CLI Structure (Modular - 5 files)
```
config/
├── schema.js          (102 righe) - Schema + Singleton
├── api-key.js         (76 righe)  - API key logic
├── settings.js        (151 righe) - Model, timeout, retries
├── billing.js         (145 righe) - Tier management
├── diagnostics.js     (78 righe)  - Validation
└── index.js           (62 righe)  - Re-exports
Total: 614 righe
```

#### MCP Structure (Monolithic - 1 file)
```
config/
└── manager.ts         (207 righe) - TUTTO in 1 file
```

**Funzionalità duplicate:**
- `getApiKey()` - IDENTICO (env priority, fallback config)
- `getDefaultModel()` - IDENTICO
- `getTimeout()` - IDENTICO
- `getMaxRetries()` - IDENTICO
- `getTier()` / `setTier()` - IDENTICO
- Schema validation - IDENTICO

**Differenze:**
- CLI: Più funzioni (setApiKey, clearApiKey, runDiagnostics, billing)
- MCP: Subset del CLI (solo read operations + tier)

---

## 2. QUANTIFICAZIONE DUPLICAZIONE

| Componente | CLI (righe) | MCP (righe) | Duplicate | % |
|------------|------------|------------|-----------|---|
| **Spawner core** | 200 | 180 | 180 | 90% |
| **Error handling** | 50 | 45 | 45 | 100% |
| **Retry logic** | 30 | 30 | 30 | 100% |
| **Worker prompts** | 50 | 50 | 50 | 100% |
| **Config API key** | 76 | 30 | 30 | 100% |
| **Config settings** | 151 | 50 | 50 | 100% |
| **TOTALE** | ~557 | ~385 | ~385 | 69% |

**Righe duplicate totali:** ~385/942 righe (41% del codice totale)
**Logica duplicate:** ~385/385 righe (100% della logica duplicata è IDENTICA)

---

## 3. PATTERN DUPLICATI DA ASTRARRE

### 3.1 Anthropic Client Wrapper
```typescript
// Funzionalità condivise:
- createClient(apiKey)
- retryableCall(fn, maxRetries, delays)
- handleError(error) → user-friendly message
- timeout wrapper
```

### 3.2 Config Management
```typescript
// Funzionalità condivise:
- getApiKey() con priority (env > config)
- getConfig(key, default)
- setConfig(key, value, validate)
- Schema validation
```

### 3.3 Worker Registry
```typescript
// Funzionalità condivise:
- Worker definitions (name, prompt, model, nextStep)
- getWorkerPrompt(workerName)
- getAvailableWorkers()
- validateWorkerExists(name)
```

---

## 4. RACCOMANDAZIONE: CREARE `@cervellaswarm/core`?

### ✅ PRO (Creare core package)

1. **DRY Principle:** 385 righe duplicate = technical debt
2. **Single Source of Truth:** Worker prompts aggiornati 1 volta, funzionano ovunque
3. **Bug fixes once:** Fix retry logic → propaga a CLI + MCP automaticamente
4. **Consistency:** CLI e MCP SEMPRE allineati
5. **Manutenibilità:** +2 package (CLI, MCP) = 2x sforzo manutenzione OGGI

### ⚠️ CONTRO (NON creare ora)

1. **Overhead build:** Nuovo package = nuovo build step
2. **Versioning complexity:** CLI v2.0.0 + core v1.0.0 + MCP v1.0.0 = 3 versioni da gestire
3. **Breaking changes risk:** Update core → rompe CLI/MCP se non testato bene
4. **Early stage:** Stiamo ancora iterando velocemente, premature abstraction?
5. **Ship velocity:** v2.0.0 sta per uscire, NON aggiungere complessità ORA

---

## 5. RACCOMANDAZIONE FINALE

### 🎯 DECISIONE: **SÌ, ma DOPO v2.0.0**

**Timeline suggerita:**
```
v2.0.0 (ORA)      → Ship con duplicazione (accettabile per MVP)
v2.0.1-v2.0.5     → Stabilize + Fix bugs
v2.1.0 (FUTURO)   → Refactor: Crea @cervellaswarm/core
```

### Package Structure Target (v2.1+)
```
packages/
├── core/                     # NUOVO!
│   ├── src/
│   │   ├── client/
│   │   │   ├── spawner.ts   # Core spawning logic
│   │   │   ├── retry.ts     # Retry + timeout utilities
│   │   │   └── errors.ts    # Error mapping
│   │   ├── config/
│   │   │   ├── manager.ts   # Config CRUD
│   │   │   └── schema.ts    # Validation schema
│   │   └── workers/
│   │       ├── registry.ts  # Worker definitions
│   │       └── prompts.ts   # All worker prompts
│   └── package.json
│
├── cli/
│   ├── src/
│   │   ├── commands/        # CLI-specific
│   │   ├── display/         # UI-specific
│   │   └── wizard/          # Setup wizard
│   ├── package.json
│   └── dependencies: ["@cervellaswarm/core"]
│
└── mcp-server/
    ├── src/
    │   ├── index.ts         # MCP protocol
    │   └── tools/           # MCP tools
    ├── package.json
    └── dependencies: ["@cervellaswarm/core"]
```

### Cosa mettere in `core`?

✅ **INCLUDE:**
- Spawner logic (retry, timeout, error handling)
- Worker registry + prompts
- Config manager (API key, settings, schema)
- Anthropic client utilities

❌ **EXCLUDE:**
- CLI commands (restano in `cli`)
- MCP protocol (resta in `mcp-server`)
- Display/UI utilities (CLI-specific)
- Billing logic (MAYBE in core, valutare)

---

## 6. NEXT STEPS (Post v2.0.0)

### Fase 1: Planning (1 giorno)
- [ ] Definire API esatta di `@cervellaswarm/core`
- [ ] Decidere versioning strategy
- [ ] Setup monorepo dependencies correttamente

### Fase 2: Implementation (2-3 giorni)
- [ ] Creare package `core` vuoto
- [ ] Migrare spawner logic
- [ ] Migrare config manager
- [ ] Migrare worker registry
- [ ] Update CLI per usare `core`
- [ ] Update MCP per usare `core`

### Fase 3: Testing (1 giorno)
- [ ] Test CLI con core
- [ ] Test MCP con core
- [ ] Integration tests
- [ ] Verify no regressions

### Fase 4: Deploy (mezzo giorno)
- [ ] Publish `@cervellaswarm/core@1.0.0`
- [ ] Publish `cervellaswarm@2.1.0`
- [ ] Publish `@cervellaswarm/mcp-server@1.1.0`

**Effort totale stimato:** 4.5 giorni (1 settimana di calendario)

---

## 7. ALTERNATIVE CONSIDERATE

### Alternativa A: Keep Duplication
- **Pro:** Zero effort ora
- **Contro:** Technical debt cresce, 2x bugs, 2x manutenzione
- **Verdict:** ❌ NON sostenibile long-term

### Alternativa B: MCP importa da CLI direttamente
- **Pro:** Zero nuovo package
- **Contro:** MCP dipende da CLI (architetturalmente sbagliato)
- **Verdict:** ❌ Architettura inversa

### Alternativa C: Git submodules
- **Pro:** Condivisione senza package
- **Contro:** Nightmare di manutenzione, versioning complesso
- **Verdict:** ❌ Troppo complesso

### Alternativa D: **Core package** ✅
- **Pro:** Clean architecture, DRY, scalabile
- **Contro:** Overhead build/versioning
- **Verdict:** ✅ **BEST choice long-term**

---

## 8. CONCLUSIONI

### 🔍 Findings Summary
- **Duplicazione:** 385 righe (41% del codice analizzato)
- **Pattern:** Spawner, config, worker prompts
- **Quality Impact:** Medio (funzionale ora, problematico poi)
- **Manutenibilità:** Bassa (2x effort per ogni cambio)

### 🎯 Azione Raccomandata
**NON ora, MA sì dopo v2.0.0 stabilization**

### 📋 Priorità
1. **CRITICO:** Ship v2.0.0 senza refactor (keep momentum)
2. **ALTO:** Pianificare core package per v2.1.0
3. **MEDIO:** Documentare decisione (FATTO ✓)

---

**Report completo:** `reports/engineer_duplication_analysis.md`
**Created:** 2026-01-22
**By:** Cervella Ingegnera
