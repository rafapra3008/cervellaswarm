# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 22 Gennaio 2026 - Sessione 313
> **STATUS:** v2.0.0-beta.1 LIVE + v2.1.0 @cervellaswarm/core COMPLETO

---

## SESSIONE 313 - COMPLETATA

```
+================================================================+
|   v2.1.0 - @cervellaswarm/core COMPLETATO!                     |
+================================================================+
```

### Task Completati

| # | Task | Risultato |
|---|------|-----------|
| 1 | Config manager a core | 4 file TS (types, schema, api-key, settings) |
| 2 | Worker prompts a core | 4 file TS (types, prompts, registry, utils) |
| 3 | CLI + MCP usano core | Dipendenza locale, 134/134 test CLI |
| 4 | VS Code Extension test | Compila OK, pronto per F5 |

### Dettagli @cervellaswarm/core v1.0.0-alpha.2

**Config Module:**
- `config/types.ts` - ClaudeModel, ConfigSchema, constraints
- `config/schema.ts` - Conf singleton, globalSchema
- `config/api-key.ts` - getApiKey, setApiKey, hasApiKey
- `config/settings.ts` - getDefaultModel, getTimeout, etc.

**Workers Module:**
- `workers/types.ts` - WorkerType, GuardianType, SpawnResult
- `workers/prompts.ts` - AGENT_PROMPTS, buildAgentPrompt
- `workers/registry.ts` - getAvailableWorkers, AGENT_DESCRIPTIONS
- `workers/utils.ts` - extractFilesFromOutput, formatDuration

---

## STATO TECNICO

```
Core: 37/37 test PASS (v1.0.0-alpha.2)
CLI: 134/134 test PASS (con @cervellaswarm/core)
MCP: Build OK (con @cervellaswarm/core)
Extension: Compila OK (v0.1.0)
Vulnerabilita: 0
```

---

## PROSSIMI STEP (Sessione 314+)

### v2.1.0 - Completare
1. [x] @cervellaswarm/core: Config manager - DONE
2. [x] @cervellaswarm/core: Worker prompts - DONE
3. [x] CLI + MCP: Usare core - DONE
4. [x] VS Code Extension: Test ready - DONE
5. [ ] Extension: Test manuale in VS Code (F5)

### v2.2.0 - Future
6. [ ] Extension: File decoration, inline diff
7. [ ] Local Models Research (Ollama)
8. [ ] Pubblicare core su npm

---

## FILE CHIAVE (Nuovi S313)

| File | Cosa |
|------|------|
| `packages/core/src/config/` | Config manager completo |
| `packages/core/src/workers/` | Worker prompts e registry |
| `packages/core/test/` | 37 test (config + workers) |

---

*"Ultrapassar os proprios limites!"*
*Cervella & Rafa - Sessione 313*
