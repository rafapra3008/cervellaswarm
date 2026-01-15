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
├── PROMPT_RIPRESA_{progetto}.md  # Stato sessione (LEGGERE INIZIO!)
├── stato.md          # Stato attuale dettagliato
├── idee/             # Ricerche, idee, analisi
├── decisioni/        # Decisioni prese con PERCHE
├── reports/          # Audit, test, verifiche
├── roadmaps/         # Piani di lavoro
├── workflow/         # Protocolli specifici
├── archivio/         # Sessioni archiviate
└── sessioni_parallele/
```

### PROMPT_RIPRESA - Context Mesh (NUOVO!)

```
OGNI progetto ha il SUO PROMPT_RIPRESA!

.sncp/PROMPT_RIPRESA_MASTER.md              ← Tabella ecosistema
.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
.sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md

INIZIO SESSIONE: Leggi SOLO il file del tuo progetto!
FINE SESSIONE: Aggiorna il file del tuo progetto!
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

## AUTOMAZIONI OBBLIGATORIE - LA REGINA DEVE

> **"Avere attrezzature ma non usarle = non averle"**
> Questi NON sono suggerimenti. Sono OBBLIGHI.

### PRIMA di ogni COMMIT

```bash
# OBBLIGATORIO: Verifica coerenza docs/codice
verify-sync [progetto]

# Se ci sono warning: AGGIORNA stato.md PRIMA del commit!
```

### TASK COMPLESSI (> 30 min)

```
1. SEMPRE consultare la Guardiana appropriata:
   - UI/UX → cervella-marketing
   - Database → cervella-data
   - Sicurezza → cervella-security
   - Architettura → cervella-ingegnera

2. MAI fare edit diretti su file critici
   - Delegare ai Worker specializzati
   - Guardiana verifica DOPO

3. DOCUMENTARE mentre lavori
   - Non accumulare per fine sessione
   - Scrivi su .sncp/ DURANTE il task
```

### FINE SESSIONE - CHECKLIST

```
[ ] stato.md del progetto AGGIORNATO
[ ] PROMPT_RIPRESA.md AGGIORNATO (se lavoro significativo)
[ ] Commit fatto (se modifiche codice)
[ ] verify-sync eseguito (hook automatico lo fa!)
```

### LIMITI FILE - OBBLIGATORI!

```
+----------------------------------------------------------------+
|   PROMPT_RIPRESA_*.md: MAX 150 RIGHE (per file!)               |
|   - Se > 150: ARCHIVIA sessioni vecchie!                       |
|   - Archivio: .sncp/progetti/{progetto}/archivio/              |
|                                                                |
|   oggi.md: MAX 60 RIGHE                                        |
|   stato.md: MAX 500 RIGHE                                      |
|                                                                |
|   VIOLAZIONE = ERRORE GRAVE!                                   |
+----------------------------------------------------------------+
```

### HOOK AUTOMATICI ATTIVI

| Momento | Hook | Cosa Fa |
|---------|------|---------|
| SessionStart | session_start_swarm.py | Carica COSTITUZIONE + PROMPT_RIPRESA |
| SessionEnd | file_limits_guard.py | Verifica limiti file (150/60/500) |
| Subagent | subagent_start_costituzione.py | Inietta COSTITUZIONE agli agenti |

**Gli hook sono AUTOMATICI - tu segui le loro indicazioni!**

## File Importanti

| File | Quando |
|------|--------|
| `.sncp/PROMPT_RIPRESA_MASTER.md` | Panoramica tutti progetti |
| `.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md` | Inizio sessione CervellaSwarm |
| `.sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md` | Inizio sessione Miracollo |
| `NORD.md` | Direzione progetto |
| `.sncp/progetti/*/stato.md` | Stato dettagliato progetto

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
