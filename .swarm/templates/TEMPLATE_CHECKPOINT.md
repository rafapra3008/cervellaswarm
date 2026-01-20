# TEMPLATE CHECKPOINT - Copia e Incolla per Fine Sessione

> **Come usare:** Copia il blocco sotto e incollalo a Cervella a fine sessione.
> Sostituisci {N} con numero sessione e {progetto} con nome progetto.

---

```
CHECKPOINT SESSIONE {N}!

1. LIMITI RIGHE:
   - PROMPT_RIPRESA_{progetto}.md (max 150)
   - stato.md (max 500)
   - Handoff: nessun limite (ma conciso)

2. NORD.md aggiornato? → {Progetto}/NORD.md (sempre in ROOT!)

3. PROMPT_RIPRESA aggiornato?
   → .sncp/progetti/{progetto}/PROMPT_RIPRESA_{progetto}.md

4. HANDOFF creato? (SNCP 2.0)
   → .sncp/handoff/HANDOFF_YYYYMMDD_{progetto}_S{N}.md
   → Template: .swarm/templates/TEMPLATE_SESSION_HANDOFF.md
   → 6 sezioni: ACCOMPLISHED, CURRENT STATE, LESSONS LEARNED,
                NEXT STEPS, KEY FILES, BLOCKERS

5. Commit + push (origin)

REGOLA GIT (solo CervellaSwarm):
- origin = TUTTO (incluso .sncp/)
- public = SOLO packages/, docs pubbliche
- MAI commit .sncp/ su public!

PATH SNCP (tutti i progetti):
- CervellaSwarm/.sncp/progetti/cervellaswarm/
- CervellaSwarm/.sncp/progetti/miracollo/
- CervellaSwarm/.sncp/progetti/contabilita/
```

---

## Versione Compatta (se preferisci)

```
CHECKPOINT {N}! Progetto: {progetto}
→ PROMPT_RIPRESA aggiornato?
→ HANDOFF creato? (.sncp/handoff/HANDOFF_YYYYMMDD_{progetto}_S{N}.md)
→ Commit + push
```

---

*SNCP 2.0 - Aggiornato Sessione 298*
