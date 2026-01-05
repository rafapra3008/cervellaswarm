# Task: Code Review Completo Sistema Swarm

**Assegnato a:** cervella-reviewer
**Stato:** ready
**Priorità:** alta

## Obiettivo

Fare CODE REVIEW COMPLETO del sistema CervellaSwarm (Beehive).

## File da Analizzare

1. **Script Globali:**
   - ~/.local/bin/spawn-workers (script principale v1.9.0)
   - ~/.local/bin/swarm-status (visibilità v1.0.0)
   - ~/.local/bin/swarm-review (workflow Guardiane v1.0.0)

2. **Struttura .swarm/ in CervellaSwarm:**
   - /Users/rafapra/Developer/CervellaSwarm/.swarm/

3. **Agent Files (i più importanti):**
   - ~/.claude/agents/cervella-orchestrator.md
   - ~/.claude/agents/cervella-backend.md
   - ~/.claude/agents/cervella-guardiana-qualita.md

## Cosa Verificare

1. **Qualità Codice:** Bash best practices, error handling, edge cases, leggibilità
2. **Sicurezza:** Path hardcodati, gestione permessi, input sanitization
3. **Architettura:** Coerenza tra script, pattern comuni, scalabilità
4. **Documentazione:** Help message, commenti, README

## Output Richiesto

Salva report in: /Users/rafapra/Developer/CervellaSwarm/reports/code_review_swarm_20260105.md

Con struttura:
- PUNTI DI FORZA
- PROBLEMI TROVATI (severità: CRITICO/ALTO/MEDIO/BASSO)
- SUGGERIMENTI MIGLIORAMENTO
- RATING FINALE (1-10)
