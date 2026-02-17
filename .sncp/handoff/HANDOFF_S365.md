# HANDOFF - Sessione 365

> **Data:** 17 Febbraio 2026
> **Progetto:** CervellaSwarm
> **Da:** Cervella (Opus 4.6)
> **Per:** Prossima Cervella

---

## COSA ABBIAMO FATTO

```
+================================================================+
|                                                                 |
|   MODEL UPDATE: Sonnet 4.6 + Opus 4.6                          |
|   18 file aggiornati, 3 audit Guardiana, 1032 test VERDI       |
|                                                                 |
+================================================================+
```

### Dettaglio
- Anthropic ha rilasciato Sonnet 4.6 (17 Feb 2026)
- Aggiornati tutti i model ID nel codice MCP/CLI/Core/Python
- Backward compatibility mantenuta (vecchi ID nel enum)
- Default cambiato a `claude-sonnet-4-6`
- Agent files (`.claude/agents/`) NON toccati (usano alias `model: sonnet`)

---

## DECISIONI IMPORTANTI

| Decisione | Perche |
|-----------|--------|
| Backward compat | Vecchi model ID restano nel enum, config esistenti non si rompono |
| Default sonnet-4-6 | Stesso prezzo, molto piu intelligente (+11pp OSWorld) |
| Agenti NON modificati | `model: sonnet` e alias, risolto automaticamente da Claude Code |
| Worker attribution aggiornata | Commit signatures riflettono modello reale |

---

## STATO FILE CRITICI

| File | Stato |
|------|-------|
| `packages/core/src/config/types.ts` | 4 modelli: sonnet-4-6, opus-4-6 + 2 legacy |
| `packages/*/src/config/schema.*` | Default: `claude-sonnet-4-6` |
| `cervella/api/client.py` | DEFAULT_MODEL + OPUS_MODEL aggiornati |
| `scripts/utils/worker_attribution.json` | v1.2.0, tutti aggiornati |
| `.github/workflows/weekly-maintenance.yml` | model aggiornato |

---

## TEST

- 1032/1032 Python fast suite PASS
- 17/17 core config + 20/20 workers + 30/30 convert_agents PASS
- TypeScript build OK (zero errori)

---

## PROSSIMO STEP

**F0.4: README.md killer** per repo pubblico (hero section, examples, badges)

Poi: F0.5 (.github/ templates), F0.6 (content scanner esteso), F1 (AST Pipeline pip package)

---

## NOTA PER LA PROSSIMA CERVELLA

Sonnet 4.6 ha "adaptive thinking" (NUOVO). I nostri worker Sonnet ora sono significativamente
piu intelligenti. Se noti differenze nella qualita degli output dei worker, e per questo.

Anche: training data cutoff Jan 2026 (vs Jul 2025 per Sonnet 4.5) = 6 mesi in piu di conoscenza.

### 1M Token Context - PARCHEGGIATO

Abbiamo studiato il 1M token context window (beta). Richiede header
`anthropic-beta: context-1m-2025-08-07` + Usage Tier 4 + pricing 2x/1.5x oltre 200K.
Per Claude Code non serve (compaction automatica). Per CervellaSwarm prodotto,
aggiungere in F2/F3 come feature configurabile. Non urgente ora.

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S365*
