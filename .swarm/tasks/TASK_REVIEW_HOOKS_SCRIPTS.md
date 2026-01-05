# Task: Review Completa Hooks e Scripts Sistema Swarm

**Assegnato a:** cervella-reviewer
**Priorita:** ALTA
**Stato:** ready

---

## Obiettivo

Fare una code review COMPLETA di tutto il sistema hooks e scripts dello Swarm.
Verificare qualita, sicurezza, best practices, e coerenza.

---

## File da Revieware

### HOOKS (~/.claude/hooks/)
1. `context_check.py` - AUTO-HANDOFF v4.3.0
2. `session_start_cervellaswarm.py` - Hook avvio sessione
3. `session_start_miracollo.py` - Hook avvio sessione
4. `session_start_contabilita.py` - Hook avvio sessione
5. `subagent_start.py` - Traccia inizio agenti
6. `subagent_stop.py` - Traccia fine agenti
7. Altri hooks presenti nella directory

### SCRIPTS (~/.local/bin/)
1. `spawn-workers` - Script spawning agenti
2. `swarm-status` - Status dei task
3. `swarm-review` - Review dei task
4. `swarm-health` - Health check sistema

### CONFIG
1. `~/.swarm/config` - Configurazione centralizzata
2. `~/.local/lib/swarm-common.sh` - Funzioni comuni

---

## Cosa Verificare

1. **Sicurezza**
   - Injection vulnerabilities
   - Path traversal
   - Secrets hardcodati

2. **Best Practices**
   - Error handling
   - Logging appropriato
   - Codice DRY (no duplicazioni)

3. **Coerenza**
   - Stile codice uniforme
   - Naming conventions
   - Struttura file

4. **Funzionalita**
   - Edge cases gestiti
   - Fallback appropriati
   - Documentazione inline

5. **Path e Configurazione**
   - Path hardcodati da rimuovere
   - Uso corretto di ~/.swarm/config

---

## Output Atteso

Report in formato:

```
## REVIEW HOOKS E SCRIPTS - [DATA]

### Rating Globale: X/10

### Problemi ALTI (da fixare subito)
- [lista]

### Problemi MEDI (da fixare presto)
- [lista]

### Problemi BASSI (nice to have)
- [lista]

### Punti di Forza
- [lista]

### Raccomandazioni
- [lista]
```

Salva il report in: `reports/review_hooks_scripts_YYYYMMDD.md`

---

## Note

- Questa e' una review di AUDIT, non di modifica
- Se trovi problemi critici, segnalali subito
- Focus su sicurezza e robustezza del sistema

---

*Creato: 5 Gennaio 2026 - Sessione 89*
*La Regina ha delegato questa review*
