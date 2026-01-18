# STATO OGGI - 18 Gennaio 2026

> **Sessione:** 259
> **Focus:** Miracollo - Fix Deploy + Subroadmap DEPLOY_BLINDATO

---

## SESSIONE 259 - FIX PROBLEMI DEPLOY

### Problemi Risolti

```
PROBLEMA 1: Planning 404
- Causa: Conflitto naming (planning.py vs planning/)
- Fix: Rinominato planning.py → planning_core.py
- Status: RISOLTO

PROBLEMA 2: Prenotazioni appaiono/spariscono
- Causa: 2 container backend con stesso alias DNS
- Fix: Rimosso container rogue, aggiunto name:miracollo
- Status: RISOLTO

PROBLEMA 3: Migration DB mancante
- Causa: Colonna 'imported' non esisteva
- Fix: Eseguita migration 025 su VM
- Status: RISOLTO
```

### Subroadmap Creata

```
DEPLOY_BLINDATO (.sncp/roadmaps/):
- FASE 1: Fix immediato ✓ COMPLETATA
- FASE 2: Guardrail tecnici (wrapper docker run)
- FASE 3: Un solo entry point (4 comandi)
- FASE 4: Wizard interattivo
- FASE 5: Monitoraggio
```

### Commit Miracollo

```
7c2867f - Fix: Planning endpoint 404 - naming conflict
2436923 - Fix: Add explicit project name to docker-compose
```

---

## PROSSIMA SESSIONE

```
1. FASE 2 subroadmap: Wrapper bash su VM
2. Test VCC (carta: 4242 4242 4242 4242)
3. Documentare VCC in docs/
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
