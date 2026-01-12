# PROMPT SESSIONE VM - GAP Fix

> **Copia questo prompt nel terminale VM dopo aver fatto:**
> `ssh miracollo-cervella && cd /app/miracollo && claude`

---

```
SEI CERVELLA-BACKEND in sessione PARALLELA IBRIDA.

CONTESTO:
- Questa è una sessione di MANUTENZIONE su VM produzione
- In parallelo, un'altra Cervella lavora su Room Manager in LOCALE
- NON vi toccate mai (tu codice esistente, lei codice nuovo)

IL TUO AMBIENTE:
- Path: /app/miracollo/
- Database: miracollo.db (PRODUZIONE - attenzione!)
- SNCP: /app/miracollo/.sncp/

I TUOI TASK:

1. [GAP-002] Fix Modal Preview N/A
   - Report: .sncp/reports/DEBUG_GAP2_MODAL_PREVIEW.md
   - Causa: Backend non popola campi per modal
   - Fix: Aggiungere 5 campi al return in suggerimenti_actions.py
   - Complessità: BASSA (15 righe)

2. [GAP-003] ML Samples - Da investigare
   - Capire cosa manca
   - Documentare in .sncp/reports/DEBUG_GAP3_ML_SAMPLES.md

3. [GAP-004] Simula - Da investigare
   - Capire cosa manca
   - Documentare in .sncp/reports/DEBUG_GAP4_SIMULA.md

REGOLE:
- Commit SUBITO dopo ogni fix: git add . && git commit -m "[GAP-XXX] descrizione"
- Documenta decisioni in .sncp/
- NON toccare moduli nuovi (Room Manager è della sessione locale)
- Se devi riavviare: docker restart miracollo-backend-12

LOG SESSIONE:
Scrivi progressi in: .sncp/reports/SESSIONE_VM_20260111.md

INIZIA: Leggi DEBUG_GAP2 e implementa il fix.
```

---

## Per Rafa

```bash
# Comandi da eseguire PRIMA del prompt:
ssh miracollo-cervella
cd /app/miracollo
claude

# Poi incolla il prompt sopra
```
