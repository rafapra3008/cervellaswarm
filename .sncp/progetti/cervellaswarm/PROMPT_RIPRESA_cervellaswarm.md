# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-04 - Sessione 334
> **STATUS:** REFACTORING CASA IN CORSO

---

## SESSIONE 334 - REFACTORING TECHNICAL DEBT

```
+================================================================+
|   S334: FASE 1 COMPLETATA! FASE 2 INIZIATA                     |
+================================================================+
```

### SUBROADMAP ATTIVA

**File:** `.sncp/roadmaps/SUBROADMAP_REFACTORING_CASA.md`

### Stato Fasi

| Fase | File | Status | Score |
|------|------|--------|-------|
| FASE 1 | weekly_retro.py | COMPLETATA | 9.5/10 |
| FASE 2 | analytics.py | INIZIATA | - |
| FASE 3 | dashboard.py | TODO | - |
| FASE 4 | Test | TODO | - |
| FASE 5 | Cleanup | TODO | - |

### FASE 1 - Output (COMPLETATA)

```
scripts/memory/retro/
├── __init__.py      22 righe   v2.2.0
├── sections.py     225 righe   v2.2.0
├── output.py       414 righe   v2.2.0
├── suggestions.py   78 righe   v2.2.0
└── cli.py          365 righe   v2.2.0
```

- SQL injection FIXATO (query parametrizzate)
- generate_retro() ridotto da 447 a 60 righe
- Audit Guardiana: 9.5/10 APPROVE

### FASE 2 - In Corso (PARZIALE)

```
scripts/memory/analytics/
├── helpers.py       CREATO
├── commands/
│   └── __init__.py  CREATO
└── (altri file da creare)
```

**NOTA:** API Anthropic dava errore 500, interrotto per checkpoint.

---

## PROSSIMA SESSIONE (S335)

**PRIORITA:** Continuare SUBROADMAP_REFACTORING_CASA.md

### FASE 2 - analytics.py (847 righe)

**Struttura iniziata:**
```
scripts/memory/analytics/
├── helpers.py           CREATO (console, HAS_RICH)
└── commands/__init__.py CREATO (imports)
```

**DA CREARE:**
```
scripts/memory/analytics/
├── cli.py               # main(), argparse
└── commands/
    ├── summary.py       # cmd_summary (74 righe)
    ├── lessons.py       # cmd_lessons (45 righe)
    ├── events.py        # cmd_events - FIX SQL!
    ├── agents.py        # cmd_agents (59 righe)
    ├── patterns.py      # cmd_patterns (52 righe)
    ├── dashboard.py     # cmd_dashboard - FIX SQL!
    ├── auto_detect.py   # cmd_auto_detect
    └── retro.py         # RIUSARE modulo retro/!
```

**SQL INJECTION DA FIXARE:**
- cmd_events(): riga 217-224
- cmd_dashboard(): righe 397-418
- cmd_retro(): righe 615-622, 685-688, 711-718

**PATTERN:** Seguire stesso approccio di FASE 1 (retro/)

### Dopo FASE 2

- FASE 3: dashboard.py (620 righe)
- FASE 4: Test & Validazione
- FASE 5: Cleanup finale

---

## ARCHIVIO

**S333:** SNCP-INIT v2.0 + CervellaCostruzione
**S334:** FASE 1 weekly_retro.py COMPLETATA (9.5/10)

---

*"Casa pulita dentro = codice che dura nel tempo"*
*Sessione 334 - Cervella & Rafa*
