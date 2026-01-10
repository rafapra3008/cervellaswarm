# CervellaSwarm

> Sistema multi-agent: 16 Cervelle coordinate dalla Regina.

## Regole Context-Smart

- Task < 5 min → Task tool interno
- Task > 5 min → Git clone separato (preserva context)
- Scrivi su .sncp/ mentre lavori (non accumulare context)
- Output conciso, strutturato

## Memoria Esterna (SNCP)

| Dove | Cosa |
|------|------|
| `.sncp/idee/` | Ricerche, idee, analisi |
| `.sncp/memoria/decisioni/` | Decisioni prese con PERCHE |
| `.sncp/coscienza/` | Pensieri sessione corrente |
| `.sncp/stato/oggi.md` | Stato OGGI - aggiornare! |

## REGOLA SNCP OBBLIGATORIA

> **"SNCP funziona solo se lo VIVIAMO!"**

1. **INIZIO sessione:** Leggi `.sncp/stato/oggi.md`
2. **DURANTE sessione:** Scrivi pensieri in `.sncp/coscienza/`
3. **FINE sessione:** Aggiorna `.sncp/stato/oggi.md`

**MAI chiudere sessione senza aggiornare SNCP!**

## File Importanti

| File | Quando |
|------|--------|
| PROMPT_RIPRESA.md | Inizio sessione |
| NORD.md | Direzione progetto |
| .sncp/idee/LA_NOSTRA_STRADA_ROADMAP_FINALE.md | Roadmap context optimization |

## La Famiglia

16 agenti in `~/.claude/agents/`:
- 1 Regina (orchestrator) + 3 Guardiane (Opus)
- 12 Worker specializzati (Sonnet)

Dettagli: `docs/DNA_FAMIGLIA.md`

## Comandi Utili

```bash
spawn-workers --list          # Vedi agenti disponibili
spawn-workers --backend       # Lancia worker backend
./tests/run_all_tests.sh      # Esegui test suite
```

## Progetti Collegati

- Miracollo: ~/Developer/miracollogeminifocus
- Contabilita: ~/Developer/ContabilitaAntigravity
