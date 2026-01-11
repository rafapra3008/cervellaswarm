# TEMPLATE: Inizio Sessione Parallela

> **Versione:** 1.0
> **Data:** 11 Gennaio 2026
> **Uso:** Copia-incolla per iniziare sessioni parallele

---

## PARTE 1: COMANDO REGINA (Setup)

### Prima di tutto, Regina esegue:

```bash
# 1. Crea la sessione parallela
~/Developer/CervellaSwarm/scripts/create-parallel-session.sh \
    ~/Developer/[PROGETTO] \
    [NOME_SESSIONE] \
    [WORKER1] [WORKER2]

# Esempio per Miracollo:
~/Developer/CervellaSwarm/scripts/create-parallel-session.sh \
    ~/Developer/miracollogeminifocus \
    room-manager \
    backend frontend
```

### Poi Regina crea piano SNCP:

```bash
# Crea cartella sessione
mkdir -p ~/Developer/[PROGETTO]/.sncp/sessioni_parallele/[NOME_SESSIONE]

# Copia template
cp ~/Developer/CervellaSwarm/.sncp/sessioni_parallele/_TEMPLATE/*.md \
   ~/Developer/[PROGETTO]/.sncp/sessioni_parallele/[NOME_SESSIONE]/
```

---

## PARTE 2: COSA DICE REGINA A RAFA

```
Rafa, ho preparato la sessione parallela!

WORKTREES PRONTI:
- Worker 1: ~/Developer/[PROGETTO]-[WORKER1]
- Worker 2: ~/Developer/[PROGETTO]-[WORKER2]

APRI QUESTI TERMINALI:

Terminal 1:
cd ~/Developer/[PROGETTO]-[WORKER1] && claude

Terminal 2:
cd ~/Developer/[PROGETTO]-[WORKER2] && claude

In ogni terminale, copia-incolla il prompt che ti do sotto.
Io resto qui a coordinare.
```

---

## PARTE 3: PROMPT PER WORKER (COPIA-INCOLLA)

### Worker Backend

```
SESSIONE PARALLELA - BACKEND

Sei cervella-backend in una sessione PARALLELA.
Progetto: [PROGETTO]
Sessione: [NOME_SESSIONE]
Il tuo task: TASK-001

STEP 1 - Verifica dipendenze:
Esegui nel terminale: check-dependencies.sh TASK-001

STEP 2 - Se nessuna dipendenza, inizia. Altrimenti:
wait-for-dependencies.sh TASK-001

STEP 3 - Il tuo lavoro:
[DESCRIZIONE SPECIFICA DEL TASK BACKEND]

REGOLE:
- Modifica SOLO: backend/, api/, services/
- NON toccare: frontend/, .sncp/stato/oggi.md
- Decisioni importanti → scrivi in .sncp/sessioni_parallele/[SESSIONE]/backend.md

STEP 4 - Quando finisci:
git add -A && git commit -m "[TASK-001] [descrizione]"
create-signal.sh TASK-001 success "[descrizione]" [COMMIT_HASH]

STEP 5 - ASPETTA che la Regina faccia il merge.

INIZIA ORA.
```

### Worker Frontend

```
SESSIONE PARALLELA - FRONTEND

Sei cervella-frontend in una sessione PARALLELA.
Progetto: [PROGETTO]
Sessione: [NOME_SESSIONE]
Il tuo task: TASK-002

STEP 1 - Verifica dipendenze:
Esegui nel terminale: check-dependencies.sh TASK-002

STEP 2 - Se dipendi da TASK-001:
wait-for-dependencies.sh TASK-002
(Aspetterà automaticamente finché backend non finisce)

STEP 3 - Il tuo lavoro:
[DESCRIZIONE SPECIFICA DEL TASK FRONTEND]

REGOLE:
- Modifica SOLO: frontend/, css/, js/
- NON toccare: backend/, .sncp/stato/oggi.md
- Decisioni importanti → scrivi in .sncp/sessioni_parallele/[SESSIONE]/frontend.md

STEP 4 - Quando finisci:
git add -A && git commit -m "[TASK-002] [descrizione]"
create-signal.sh TASK-002 success "[descrizione]" [COMMIT_HASH]

STEP 5 - ASPETTA che la Regina faccia il merge.

INIZIA ORA.
```

---

## PARTE 4: QUANDO WORKER FINISCONO (Regina)

```bash
# 1. Verifica stato
~/Developer/CervellaSwarm/scripts/status-parallel-worktrees.sh ~/Developer/[PROGETTO]

# 2. Se tutti success, merge
~/Developer/CervellaSwarm/scripts/merge-parallel-worktrees.sh ~/Developer/[PROGETTO]

# 3. Verifica merge OK
cd ~/Developer/[PROGETTO]
git log --oneline -5
git status

# 4. Cleanup worktrees
~/Developer/CervellaSwarm/scripts/cleanup-parallel-worktrees.sh ~/Developer/[PROGETTO]

# 5. Commit finale
git add -A && git commit -m "Sessione parallela [NOME]: [DESCRIZIONE]"
```

---

## PARTE 5: AGGIORNA SNCP (Regina)

Dopo il merge, Regina aggiorna:

1. `.sncp/sessioni_parallele/[SESSIONE]/riepilogo.md` - cosa abbiamo fatto
2. `.sncp/stato/oggi.md` - aggiungi la sessione parallela
3. `PROMPT_RIPRESA.md` - se necessario

---

## ESEMPIO COMPLETO: Miracollo Room Manager

### Setup (Regina esegue):

```bash
~/Developer/CervellaSwarm/scripts/create-parallel-session.sh \
    ~/Developer/miracollogeminifocus \
    room-manager \
    backend frontend

mkdir -p ~/Developer/miracollogeminifocus/.sncp/sessioni_parallele/room-manager
```

### Comunicazione a Rafa:

```
Rafa, sessione parallela pronta!

Terminal 1:
cd ~/Developer/miracollogeminifocus-backend && claude

Terminal 2:
cd ~/Developer/miracollogeminifocus-frontend && claude

Copia-incolla i prompt che ti mando.
```

### Prompt Backend:

```
SESSIONE PARALLELA - BACKEND

Sei cervella-backend. Progetto: Miracollo PMS. Sessione: room-manager
Il tuo task: TASK-001 - Room Manager API

Verifica: check-dependencies.sh TASK-001

Il tuo lavoro:
- Crea/modifica backend/routers/room_manager.py
- Endpoint per gestione camere
- CRUD operations

Modifica SOLO: backend/
NON toccare: frontend/

Quando finisci:
git add -A && git commit -m "[TASK-001] Room Manager API"
create-signal.sh TASK-001 success "Room Manager API completata"

ASPETTA merge della Regina.
```

### Prompt Frontend:

```
SESSIONE PARALLELA - FRONTEND

Sei cervella-frontend. Progetto: Miracollo PMS. Sessione: room-manager
Il tuo task: TASK-002 - Room Manager UI

Verifica: check-dependencies.sh TASK-002
Se dipendi da backend: wait-for-dependencies.sh TASK-002

Il tuo lavoro:
- Crea/modifica frontend/js/room-manager.js
- Crea frontend/room-manager.html
- UI per gestione camere

Modifica SOLO: frontend/
NON toccare: backend/

Quando finisci:
git add -A && git commit -m "[TASK-002] Room Manager UI"
create-signal.sh TASK-002 success "Room Manager UI completata"

ASPETTA merge della Regina.
```

---

*Template creato: 11 Gennaio 2026*
*"Copia, incolla, lavora in parallelo!"*
