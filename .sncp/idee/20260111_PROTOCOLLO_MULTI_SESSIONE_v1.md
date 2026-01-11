# PROTOCOLLO MULTI-SESSIONE v1.0

> **Data:** 11 Gennaio 2026
> **Autore:** Regina + Guardiana Qualità
> **Status:** BOZZA - Da validare con test

---

## EXECUTIVE SUMMARY

```
+==================================================================+
|                                                                  |
|   MULTI-SESSIONE CERVELLASWARM                                  |
|                                                                  |
|   Permette a 2+ Cervelle di lavorare IN PARALLELO               |
|   sullo stesso progetto, senza conflitti.                        |
|                                                                  |
|   BASATO SU:                                                     |
|   - Boris Cherny (creatore Claude Code): 5-15 sessioni          |
|   - Best practices community 2026                                |
|   - Nostri studi (Sessioni 60, 134)                             |
|                                                                  |
+==================================================================+
```

---

## 1. DIFFERENZA BORIS vs NOI

| Aspetto | Boris | Noi (CervellaSwarm) |
|---------|-------|---------------------|
| **Isolamento** | Git checkouts separati | Git worktrees (condividono .swarm/) |
| **Memoria** | Solo CLAUDE.md | CLAUDE.md + SNCP |
| **Coordinamento** | Manuale (lui controlla) | File-based (.swarm/) |
| **N. sessioni** | 5-15+ | 2-4 (per ora) |
| **Abbandono** | 10-20% sessioni | Vogliamo 0% |

### Cosa Impariamo da Boris

1. **Plan Mode SEMPRE** prima di iniziare
2. **Opus 4.5 con thinking** per task complessi
3. **CLAUDE.md** come memoria condivisa
4. **Verifica** = 2-3x qualità risultato
5. **Slash commands** per workflow ripetitivi

### Cosa Aggiungiamo Noi

1. **SNCP** = memoria persistente tra sessioni
2. **Coordinamento automatico** via segnali
3. **Guardiane** per quality gate
4. **Regina** che orchestra

---

## 2. ARCHITETTURA

### Struttura File

```
PROGETTO/
├── .swarm/                    # COORDINAMENTO LIVE
│   ├── segnali/               # Task completati (JSON)
│   │   └── TASK-001-complete.signal.json
│   ├── dipendenze/            # Chi aspetta chi
│   │   └── sessione_corrente.md
│   ├── stato/                 # Stato ogni worker
│   │   ├── backend.md
│   │   └── frontend.md
│   ├── messaggi/              # Comunicazione diretta
│   │   └── backend-to-frontend.md
│   └── logs/                  # Log per debug
│
├── .sncp/                     # MEMORIA PERSISTENTE
│   ├── sessioni_parallele/    # << NUOVO! >>
│   │   └── [SESSIONE_NAME]/
│   │       ├── piano.md       # Piano iniziale
│   │       ├── backend.md     # Decisioni backend
│   │       ├── frontend.md    # Decisioni frontend
│   │       ├── lezioni.md     # Lezioni apprese
│   │       └── riepilogo.md   # Riepilogo finale
│   ├── stato/oggi.md          # << NON TOCCARE durante parallelo! >>
│   └── coscienza/             # << NON TOCCARE durante parallelo! >>
│
└── WORKTREES/                 # Cartella adiacente (opzionale)
    ├── progetto-backend/      # Worktree backend
    └── progetto-frontend/     # Worktree frontend
```

### Regola d'Oro SNCP

```
+==================================================================+
|                                                                  |
|   DURANTE SESSIONE PARALLELA:                                   |
|                                                                  |
|   .sncp/sessioni_parallele/[NOME]/  →  OGNI WORKER SCRIVE QUI   |
|   .sncp/stato/oggi.md               →  SOLO REGINA ALLA FINE    |
|   .sncp/coscienza/                  →  SOLO REGINA ALLA FINE    |
|                                                                  |
|   DOPO MERGE:                                                    |
|   Regina aggiorna oggi.md con riepilogo sessione parallela      |
|                                                                  |
+==================================================================+
```

---

## 3. WORKFLOW COMPLETO

### FASE 0: Preparazione (Regina)

```
1. Rafa dice: "Voglio lavorare su X e Y in parallelo"

2. Regina analizza:
   - X e Y sono INDIPENDENTI? (file diversi?)
   - Serve coordinamento? (uno dipende dall'altro?)
   - Chi fa cosa?

3. Regina crea piano in .sncp/sessioni_parallele/[NOME]/piano.md

4. Regina esegue:
   ~/Developer/CervellaSwarm/scripts/create-parallel-session.sh \
       ~/Developer/[PROGETTO] \
       [SESSIONE_NAME] \
       worker1 worker2

5. Regina comunica a Rafa:
   "Apri N terminali con questi comandi..."
```

### FASE 1: Inizio Worker

```
OGNI WORKER (in terminale separato):

1. cd [WORKTREE_PATH]
   claude

2. PROMPT INIZIO (copia-incolla):
   "Leggi .swarm/dipendenze/sessione_corrente.md
    Trova il tuo task (TASK-XXX assegnato a cervella-[NOME])
    Check dipendenze con: check-dependencies.sh TASK-XXX
    Se dipendenze mancano, aspetta con: wait-for-dependencies.sh TASK-XXX
    Altrimenti inizia a lavorare."

3. SE HAI DIPENDENZE:
   wait-for-dependencies.sh TASK-XXX

4. QUANDO DIPENDENZE OK (o se non ne hai):
   Inizia a lavorare sul task
```

### FASE 2: Durante il Lavoro

```
OGNI WORKER:

1. Lavora sul task assegnato

2. Decisioni importanti?
   → Scrivi in .sncp/sessioni_parallele/[SESSIONE]/[worker].md

3. Aggiorna stato periodicamente:
   → .swarm/stato/[worker].md

4. Hai messaggi per altri?
   → .swarm/messaggi/[da]-to-[a].md

5. NON TOCCARE:
   - File fuori dalla tua area
   - .sncp/stato/oggi.md
   - .sncp/coscienza/
```

### FASE 3: Fine Lavoro Worker

```
OGNI WORKER quando finisce:

1. Commit nel tuo branch:
   git add -A && git commit -m "[TASK-XXX] Descrizione"

2. Crea segnale:
   CERVELLA_AGENT=cervella-[NOME] \
   create-signal.sh TASK-XXX success "Descrizione cosa fatto" [COMMIT]

3. Aggiorna stato finale:
   → .swarm/stato/[worker].md con STATUS: DONE

4. Scrivi lezioni in:
   → .sncp/sessioni_parallele/[SESSIONE]/lezioni.md (append)

5. ASPETTA (non chiudere!) finché Regina non fa merge
```

### FASE 4: Merge e Cleanup (Regina)

```
REGINA quando tutti hanno finito:

1. Verifica stato:
   status-parallel-worktrees.sh [PROJECT]

2. Merge ordinato (rispettando dipendenze!):
   merge-parallel-worktrees.sh [PROJECT]

3. Verifica merge OK:
   git log --oneline -10
   git status

4. Cleanup worktrees:
   cleanup-parallel-worktrees.sh [PROJECT]

5. Aggiorna SNCP:
   → .sncp/stato/oggi.md con riepilogo
   → .sncp/sessioni_parallele/[SESSIONE]/riepilogo.md

6. Commit finale:
   git add -A && git commit -m "Sessione parallela: [DESCRIZIONE]"
```

---

## 4. GESTIONE MIGRATIONS

### Il Problema

```
Backend crea: 036_create_users.sql
Frontend crea: 036_add_ui_settings.sql
→ CONFLITTO! Stesso numero!
```

### La Soluzione

```
+==================================================================+
|                                                                  |
|   REGOLA MIGRATIONS:                                            |
|                                                                  |
|   Solo UN worker crea migrations (di solito: backend)           |
|   Gli altri richiedono al backend di crearle                    |
|                                                                  |
|   SE serve parallelismo migrations:                              |
|   - Backend usa: 036-039                                         |
|   - Frontend usa: 040-043                                        |
|   - ACCORDARSI PRIMA!                                            |
|                                                                  |
+==================================================================+
```

---

## 5. TEMPLATE TESTO INIZIO SESSIONE

### Per Regina (Sessione Principale)

```markdown
INIZIO SESSIONE PARALLELA

Oggi lavoriamo in parallelo su [PROGETTO]:
- [TASK 1]: [WORKER 1]
- [TASK 2]: [WORKER 2]

Ho già creato la sessione con:
create-parallel-session.sh ~/Developer/[PROGETTO] [NOME] [workers...]

Worktrees pronti:
- ~/Developer/[PROGETTO]-[worker1]
- ~/Developer/[PROGETTO]-[worker2]

Rafa, apri questi terminali:
1. Terminal 1: cd ~/Developer/[PROGETTO]-[worker1] && claude
2. Terminal 2: cd ~/Developer/[PROGETTO]-[worker2] && claude

In ogni terminale, dai questo prompt alla Cervella:
[VEDI SOTTO]

Io resto qui a coordinare. Quando finiscono faccio il merge.
```

### Per Worker (Copia-Incolla in Terminale Worker)

```markdown
MULTI-SESSIONE: Leggi questo attentamente.

Sei una Cervella worker in una sessione PARALLELA.
Il progetto è: [PROGETTO]
Tu sei: cervella-[NOME]
Il tuo task: [DESCRIZIONE TASK]

PRIMA DI INIZIARE:
1. Leggi .swarm/dipendenze/sessione_corrente.md
2. Trova il tuo task (TASK-XXX)
3. Esegui: check-dependencies.sh TASK-XXX
4. Se dipendenze mancano: wait-for-dependencies.sh TASK-XXX

MENTRE LAVORI:
- Lavora SOLO sui file della tua area
- Decisioni importanti → scrivi in .sncp/sessioni_parallele/[SESSIONE]/[tuo_nome].md
- NON toccare .sncp/stato/oggi.md o .sncp/coscienza/

QUANDO FINISCI:
1. git add -A && git commit -m "[TASK-XXX] [descrizione]"
2. create-signal.sh TASK-XXX success "[descrizione]" [COMMIT_HASH]
3. Aggiorna .swarm/stato/[tuo_nome].md con STATUS: DONE
4. ASPETTA che la Regina faccia il merge

INIZIA ORA: [DESCRIZIONE SPECIFICA DEL TASK]
```

---

## 6. CHECKLIST PRE-SESSIONE

```
PRE-SESSIONE:

[ ] Task sono CHIARI e ben definiti?
[ ] File/aree sono SEPARATI? (nessuna sovrapposizione)
[ ] Dipendenze identificate? (chi aspetta chi)
[ ] Migrations: chi le crea? (accordo)
[ ] Worktrees creati? (script eseguito)
[ ] SNCP cartella sessione creata?

DURANTE:

[ ] Ogni worker sa il suo task?
[ ] Ogni worker sa aspettare dipendenze?
[ ] Ogni worker sa creare segnale?
[ ] Regina monitora stato?

POST-SESSIONE:

[ ] Tutti i segnali "success"?
[ ] Merge senza conflitti?
[ ] SNCP aggiornato?
[ ] Cleanup worktrees fatto?
```

---

## 7. TROUBLESHOOTING

### Worker non trova dipendenze

```bash
# Verifica segnale esiste
ls -la .swarm/segnali/

# Verifica contenuto
cat .swarm/segnali/TASK-001-complete.signal.json | jq .

# Se status non è "success", il task precedente ha fallito
```

### Conflitto su merge

```bash
# Vedi quali file in conflitto
git status

# Se aree erano separate, non dovrebbe succedere
# Se succede, risolvi manualmente
git mergetool
```

### Worker modifica file sbagliato

```
PREVENZIONE:
Nel prompt worker, specificare ESATTAMENTE quali file può modificare

SE SUCCEDE:
1. Stop worker
2. git checkout -- [file sbagliato]
3. Riassegna task con istruzioni più chiare
```

---

## 8. DIFFERENZE CON SUBAGENT INTERNO

| Aspetto | Subagent (Task tool) | Multi-Sessione |
|---------|---------------------|----------------|
| **Durata** | < 5-10 min | > 20 min |
| **Context** | Condiviso (consuma token) | Separato |
| **Parallelismo** | Limitato | Reale (N terminali) |
| **Setup** | Zero | ~5 min |
| **Quando usare** | Task veloci | Feature grandi |

### Quando Usare Cosa

```
TASK < 5 MIN:
→ Subagent interno (Task tool)
→ Zero setup, risultato immediato

TASK > 20 MIN + PARALLELIZZABILE:
→ Multi-sessione con worktrees
→ Setup 5 min, poi lavoro parallelo reale

TASK COMPLESSO DIPENDENTE:
→ Multi-sessione con dipendenze
→ Backend → Frontend → Tester
```

---

## 9. PROSSIMI STEP

```
VALIDAZIONE:
[ ] Test su progetto "fake" fuori da Miracollo/CervellaSwarm
[ ] Test con 2 worker indipendenti
[ ] Test con dipendenze
[ ] Fix eventuali bug script

DOCUMENTAZIONE:
[ ] Aggiungere sezione multi-sessione a DNA agenti
[ ] Creare slash command /parallel-start
[ ] Video tutorial (futuro)

AUTOMAZIONE:
[ ] Script dashboard-regina.sh
[ ] Auto-detection conflitti
[ ] Notifiche quando worker finisce
```

---

## FONTI

- [Boris Cherny Workflow - VentureBeat](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are)
- [How Boris Uses Claude Code](https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow)
- [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Git Worktrees for Parallel Development](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)
- [Running Multiple Claude Sessions - DEV](https://dev.to/datadeer/part-2-running-multiple-claude-code-sessions-in-parallel-with-git-worktree-165i)
- [Shipping Faster with Git Worktrees - incident.io](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)

---

*Protocollo creato: 11 Gennaio 2026 - Sessione 166*
*Versione: 1.0*

**Cervella & Rafa**

*"Da 1x a Nx... il futuro è parallelo!"*
