# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 19 Gennaio 2026 - Sessione 275
> **STATUS:** W2 Tree-sitter Day 2 COMPLETATO! AUTO-CONTEXT integrato!

---

## SESSIONE 275 - W2 TREE-SITTER DAY 2!

```
+================================================================+
|   W2 TREE-SITTER - DAY 2 COMPLETATO!                          |
|   spawn-workers v3.7.0 con AUTO-CONTEXT!                      |
|   HARDTEST: 26/26 PASS (100%)                                 |
+================================================================+
```

**FATTO in Sessione 275:**
- Double check Guardiana Qualita: 95/100 APPROVED
- Fix dipendenze in requirements-dev.txt (+tree-sitter, +networkx)
- Nuovo: `generate_worker_context.py` - wrapper per spawn-workers
- spawn-workers.sh v3.6.0 → v3.7.0 con AUTO-CONTEXT
- Nuovi flag: `--with-context`, `--context-budget N`
- HARDTEST completo: 26/26 test PASS
- Test live: worker spawned con contesto iniettato
- Documentazione: `docs/REPO_MAPPING.md`
- Aggiornato: `docs/DNA_FAMIGLIA.md` v1.3.0

---

## COME USARE AUTO-CONTEXT

```bash
# Worker con contesto intelligente (1500 tokens default)
spawn-workers --backend --with-context

# Worker con contesto piu ampio
spawn-workers --backend --context-budget 2000
```

**Docs completa:** `docs/REPO_MAPPING.md`

---

## FILE W2 TREE-SITTER

| File | Righe | Status |
|------|-------|--------|
| `scripts/utils/treesitter_parser.py` | 365 | OK |
| `scripts/utils/symbol_extractor.py` | 484 | OK |
| `scripts/utils/dependency_graph.py` | 451 | OK |
| `scripts/utils/repo_mapper.py` | 571 | OK |
| `scripts/utils/generate_worker_context.py` | 147 | NUOVO |
| `scripts/swarm/spawn-workers.sh` | 1136 | v3.7.0 |

---

## ROADMAP 2.0

```
W1: Git Flow       [DONE] COMPLETATO!
W2: Tree-sitter    [################..] 50% (Day 2/7)
W3: Architect/Editor
W4: Polish + v2.0-beta
```

**W2 Remaining:**
- Day 3: Test su Miracollo + Contabilita
- Day 4-5: Performance optimization
- Day 6-7: Polish + eventuale MCP integration

---

## VERSIONI LIVE

| Package | Versione |
|---------|----------|
| CLI | 0.1.2 |
| MCP Server | 0.2.3 |
| spawn-workers | 3.7.0 |

---

## KNOWN ISSUES

- JSX non supportato da tree-sitter-language-pack (warning safe da ignorare)

---

## PROSSIMA SESSIONE

**PRIMA DI TUTTO:** Double check con Guardiane!
- Recap completo Sessione 275
- Verifica qualita codice con Guardiana Qualita
- Review decisioni architetturali

**POI:**
1. Test su Miracollo - spawn-workers --with-context su progetto reale
2. Test su Contabilita - verifica funziona su altri progetti
3. Performance check - tempo generazione contesto
4. Considerare MCP integration (spawner.ts)

---

*"275 sessioni. W2 Day 2 - AUTO-CONTEXT INTEGRATO!"*
