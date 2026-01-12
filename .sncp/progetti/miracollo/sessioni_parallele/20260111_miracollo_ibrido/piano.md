# Piano Sessione Parallela Ibrida - Miracollo

> **Data:** 11 Gennaio 2026
> **Sessione:** 168 - Prima sessione parallela IBRIDA
> **Creato da:** Regina

---

## OBIETTIVO

Prima prova di sessione parallela con workflow ibrido:
- **Sessione VM**: Fix GAP esistenti su produzione
- **Sessione Locale**: Sviluppo modulo Room Manager nuovo

---

## SESSIONI

### SESSIONE 1: VM - Manutenzione GAP

```
TERMINALE: ssh miracollo-cervella
WORKER: cervella-backend
AMBIENTE: VM Produzione
PATH: /app/miracollo/

TASK:
1. [GAP-002] Fix Modal Preview N/A (causa trovata, 15 righe)
2. [GAP-003] ML Samples (da investigare)
3. [GAP-004] Simula (da investigare)

FILE CHE TOCCA:
- backend/services/suggerimenti_actions.py
- (altri file GAP esistenti)

NON TOCCA:
- Nessun modulo nuovo
- Nessuna struttura nuova
```

### SESSIONE 2: Locale - Room Manager

```
TERMINALE: Locale MacBook
WORKER: cervella-backend + cervella-frontend
AMBIENTE: Locale (worktree)
PATH: ~/Developer/miracollo-worktrees/room-manager/

TASK:
1. Design API Room Manager
2. Creare struttura backend/routers/room_manager/
3. Creare struttura frontend/pages/RoomManager/
4. Implementare CRUD base camere

FILE CHE TOCCA:
- SOLO cartella room_manager/ (NUOVA)
- SOLO cartella RoomManager/ (NUOVA)

NON TOCCA:
- Codice esistente
- main.py, App.jsx (collegamenti DOPO, in deploy)
```

---

## DIPENDENZE

```
SESSIONE 1 (VM) ←→ SESSIONE 2 (Locale)

INDIPENDENTI! Zero conflitti possibili.

- VM lavora su codice ESISTENTE
- Locale lavora su codice NUOVO
- Mai si toccano
```

---

## WORKFLOW

```
1. Rafa apre 2 terminali

2. TERMINALE 1 (VM):
   ssh miracollo-cervella
   cd /app/miracollo
   claude
   [incolla prompt sessione VM]

3. TERMINALE 2 (Locale):
   cd ~/Developer/CervellaSwarm
   [prima: setup worktree]
   claude
   [incolla prompt sessione locale]

4. Regina monitora da qui (questo terminale)

5. Quando finiscono:
   - Sessione VM: commit + push
   - Sessione Locale: commit + push
   - Regina: verifica, poi deploy Room Manager su Lab
```

---

## SNCP

Ogni sessione scrive nel proprio file:
- `sessione_vm.md` - Log sessione VM
- `sessione_locale.md` - Log sessione locale

Regina consolida in `riepilogo.md` alla fine.

---

## CHECKLIST PRE-START

```
[ ] VM accessibile (ssh miracollo-cervella)
[ ] Worktree locale creato
[ ] Entrambi i terminali aperti
[ ] Prompt copiati e pronti
```

---

*Piano creato da Regina - Sessione 168*
