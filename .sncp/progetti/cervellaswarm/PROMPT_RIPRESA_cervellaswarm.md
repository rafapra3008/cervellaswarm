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

1. **Continuare FASE 2** - Completare refactoring analytics.py
2. Creare comandi separati in analytics/commands/
3. FIX SQL injection in events.py, dashboard.py
4. cmd_retro() deve RIUSARE modulo retro/ (no duplicazione!)

---

## ARCHIVIO

**S333:** SNCP-INIT v2.0 + CervellaCostruzione
**S334:** FASE 1 weekly_retro.py COMPLETATA (9.5/10)

---

*"Casa pulita dentro = codice che dura nel tempo"*
*Sessione 334 - Cervella & Rafa*
