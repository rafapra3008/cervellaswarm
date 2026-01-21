# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 21 Gennaio 2026 - Sessione 308
> **STATUS:** SUBROADMAP CONTEXT DURANTE LAVORO APPROVED 9.5/10

---

## SESSIONE 308 - CONTEXT OPTIMIZATION

```
+================================================================+
|   PROBLEMA IDENTIFICATO:                                        |
|   Context cresce troppo velocemente DURANTE il lavoro           |
|   (non all'avvio - quello è normale ~20%)                       |
|                                                                |
|   SUBROADMAP CREATA E APPROVATA: 9.5/10                        |
+================================================================+
```

---

## COSA FATTO SESSIONE 308

| Task | Status |
|------|--------|
| Investigazione context usage | COMPLETATA |
| Analisi hook con Guardiane | COMPLETATA |
| Fix hook SessionEnd (file_limits_guard.py) | FIXATO |
| Subroadmap context durante lavoro | CREATA 9.5/10 |
| Audit Guardiana Qualità | APPROVED |

### File Creati/Modificati

| File | Cosa |
|------|------|
| `.sncp/roadmaps/SUBROADMAP_CONTEXT_DURANTE_LAVORO.md` | Piano ottimizzazione |
| `.claude/hooks/file_limits_guard.py` | Fix schema JSON SessionEnd |
| `docs/studio/RICERCA_CONTEXT_OPTIMIZATION_2026.md` | Ricerca Researcher |

---

## DIAGNOSI PRELIMINARE

**Cause potenziali identificate:**
1. Subagent context accumulation
2. Tool results troppo grandi
3. Hook durante lavoro (debug_hook.py, log_event.py)
4. Agent prompt growth (architect 293 righe!)
5. Context base fisso (CLAUDE.md 336 righe)
6. MCP servers output

**Hook rimuovibili SICURI (Guardiana approved):**
- debug_hook.py
- log_event.py

**Hook con errore:**
- subagent_start_costituzione.py NON ESISTE ma configurato

---

## PROSSIMI STEP (Sessione 309)

**FASE 1 - Diagnosi (priorità):**
1. [ ] Misurare crescita context con spawn worker
2. [ ] Documentare delta % per ogni operazione
3. [ ] Identificare colpevole principale

**FASE 2 - Fix mirati:**
4. [ ] Rimuovere hook non essenziali (se causa)
5. [ ] Ridurre prompt agent (con cautela su architect)

**Problemi correlati:**
- [ ] Fix config SubagentStart (rimuovere file mancante)
- [ ] Investigare problemi commit (Rafa ha menzionato)

---

## METRICHE TARGET

| Metrica | Baseline | Target |
|---------|----------|--------|
| Context dopo 5 spawn | Da misurare | -30% |
| Durata sessione | ~45 min | 90+ min |

---

*"Prima capire, poi agire. Mai fretta."*
*Cervella & Rafa - Sessione 308*
