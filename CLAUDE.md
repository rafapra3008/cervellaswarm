# CervellaSwarm

> Sistema multi-agent: 16 Cervelle coordinate dalla Regina.
> "Lavoriamo in pace! Senza casino! Dipende da noi!"

## Regole Context-Smart

- Task < 5 min → Task tool interno
- Task > 5 min → Git clone separato (preserva context)
- Scrivi su .sncp/ mentre lavori (non accumulare context)
- Output conciso, strutturato

## Memoria Esterna (SNCP) - STRUTTURA PROGETTI

> **SNCP = Sistema Nervoso Centrale Progetti**
> Ogni progetto ha la sua cartella dedicata!

### Path per Progetto

| Progetto | Path SNCP |
|----------|-----------|
| **Miracollo** | `.sncp/progetti/miracollo/` |
| **CervellaSwarm** | `.sncp/progetti/cervellaswarm/` |
| **Contabilita** | `.sncp/progetti/contabilita/` |

### Struttura Ogni Progetto

```
.sncp/progetti/{progetto}/
├── stato.md          # Stato attuale (LEGGERE SEMPRE!)
├── idee/             # Ricerche, idee, analisi
├── decisioni/        # Decisioni prese con PERCHE
├── reports/          # Audit, test, verifiche
├── roadmaps/         # Piani di lavoro
├── workflow/         # Protocolli specifici
└── sessioni_parallele/
```

### File Globali (non di progetto)

| Dove | Cosa |
|------|------|
| `.sncp/stato/oggi.md` | Stato GENERALE (tutti i progetti) |
| `.sncp/coscienza/` | Pensieri sessione corrente |
| `.sncp/handoff/` | Handoff tra sessioni |
| `.sncp/memoria/decisioni/` | Decisioni GLOBALI |

## REGOLA SNCP OBBLIGATORIA

> **"SNCP funziona solo se lo VIVIAMO!"**

1. **INIZIO sessione:** Leggi `.sncp/progetti/{progetto}/stato.md`
2. **DURANTE sessione:** Scrivi in `.sncp/progetti/{progetto}/`
3. **FINE sessione:** Aggiorna `stato.md` del progetto

**MAI mescolare file di progetti diversi!**
**MAI cercare file Miracollo in miracollogeminifocus locale!**

## File Importanti

| File | Quando |
|------|--------|
| PROMPT_RIPRESA.md | Inizio sessione |
| NORD.md | Direzione progetto |
| `.sncp/progetti/miracollo/stato.md` | Stato Miracollo |
| `.sncp/progetti/miracollo/roadmaps/` | Roadmap Revenue

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
