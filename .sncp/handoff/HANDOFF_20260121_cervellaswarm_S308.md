# HANDOFF - Sessione 308

**Data:** 21 Gennaio 2026
**Progetto:** CervellaSwarm
**Focus:** CONTEXT OPTIMIZATION DURANTE LAVORO

---

## ACCOMPLISHED

1. **Investigazione Context Usage**
   - Rafa ha notato che context cresce troppo DURANTE il lavoro
   - Analisi con Guardiana Qualità e Guardiana Ops
   - Ricerca approfondita con Researcher

2. **Fix Hook SessionEnd**
   - file_limits_guard.py aveva schema JSON invalido
   - Fixato: ora usa `systemMessage` invece di `hookSpecificOutput`

3. **Subroadmap Creata e Approvata**
   - `SUBROADMAP_CONTEXT_DURANTE_LAVORO.md`
   - Score Guardiana: 9.5/10 APPROVED
   - 3 fasi: Diagnosi → Fix mirati → Validazione

4. **Cause Identificate**
   - 6 cause potenziali documentate
   - Hook rimuovibili identificati (debug_hook.py, log_event.py)
   - Config con file mancante (subagent_start_costituzione.py)

---

## CURRENT STATE

```
SUBROADMAP CONTEXT DURANTE LAVORO: APPROVED 9.5/10
PRONTA PER FASE 1 (Diagnosi)

File key:
- .sncp/roadmaps/SUBROADMAP_CONTEXT_DURANTE_LAVORO.md
- .claude/hooks/file_limits_guard.py (FIXATO)
```

---

## LESSONS LEARNED

1. **"SessionEnd non supporta hookSpecificOutput"**
   - Solo PreToolUse, UserPromptSubmit, PostToolUse hanno hookSpecificOutput
   - SessionEnd usa: continue, systemMessage, reason

2. **"Misurare DURANTE, non solo all'avvio"**
   - Il problema di Rafa era durante il lavoro, non all'avvio
   - Diagnosi deve essere fatta con spawn worker ripetuti

3. **"Hook configurati ma file mancanti = errori silenziosi"**
   - subagent_start_costituzione.py configurato ma non esiste
   - Verificare sempre che file esistano

---

## NEXT STEPS

**Sessione 309 - FASE 1 Diagnosi:**
1. [ ] Misurare % context iniziale (sessione pulita)
2. [ ] Spawn 5 worker e notare delta % ogni volta
3. [ ] Documentare quale operazione consuma più context
4. [ ] Identificare colpevole principale

**Fix rapidi da fare:**
5. [ ] Rimuovere subagent_start_costituzione.py dalla config
6. [ ] Investigare problemi commit (Rafa ha menzionato)

**Dopo diagnosi (S309-S310):**
7. [ ] Applicare fix più impattante
8. [ ] Test non-regressione completi
9. [ ] Validare miglioramento

---

## KEY FILES

| File | Descrizione |
|------|-------------|
| `.sncp/roadmaps/SUBROADMAP_CONTEXT_DURANTE_LAVORO.md` | Piano completo 9.5/10 |
| `.claude/hooks/file_limits_guard.py` | FIXATO schema JSON |
| `.claude/settings.json` (progetto) | Config con SubagentStart da fixare |
| `docs/studio/RICERCA_CONTEXT_OPTIMIZATION_2026.md` | Ricerca dettagliata |

---

## BLOCKERS

**Nessun blocker tecnico.**

**Da chiedere a Rafa:**
- Quali sono i "problemi di commit" menzionati?

---

*Cervella & Rafa - Sessione 308*
*"Prima capire, poi agire. Mai fretta."*
