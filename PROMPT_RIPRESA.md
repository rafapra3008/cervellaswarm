# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 3 Gennaio 2026 - Sessione 66 - LA MAGIA! spawn-workers.sh FUNZIONA!

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|   DELEGA sempre, MAI edit diretti!                               |
|                                                                  |
|   E oggi... LA MAGIA FUNZIONA!!!                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL MOMENTO MAGICO (Sessione 66)

```
+------------------------------------------------------------------+
|                                                                  |
|   "MADONAAAAAAA MIAAAA MEU DEUSSSS DO CEUUU!" - Rafa            |
|                                                                  |
|   spawn-workers.sh FUNZIONA!!!                                   |
|                                                                  |
|   ./spawn-workers.sh --backend                                   |
|   -> Si apre NUOVA finestra Terminal                             |
|   -> Claude Code si avvia AUTOMATICAMENTE                        |
|   -> Worker pronto con prompt iniettato!                         |
|                                                                  |
|   Da oggi le finestre si aprono con UN COMANDO!                  |
|   La MAGIA e' REALE!!!                                           |
|                                                                  |
+------------------------------------------------------------------+
```

### Come funziona spawn-workers.sh

1. **Crea prompt file** in `.swarm/prompts/worker_X.txt`
2. **Crea runner** in `.swarm/runners/run_X.sh`
3. **osascript** apre nuova finestra Terminal
4. **Claude Code** parte con `--append-system-prompt`

### Opzioni disponibili

```bash
./spawn-workers.sh --backend     # Solo backend
./spawn-workers.sh --frontend    # Solo frontend
./spawn-workers.sh --tester      # Solo tester
./spawn-workers.sh --all         # backend + frontend + tester
./spawn-workers.sh --list        # Mostra tutti i worker
```

---

## LA STORIA (come siamo arrivati qui)

### Sessione 60 - LA SCOPERTA
Rafa stava su Miracollo, compact imminente. Apre NUOVA FINESTRA.
La nuova Cervella fa `git status` -> vede TUTTO!
**Insight:** N finestre = N contesti = N volte piu potenza!

### Sessione 61 - MVP MULTI-FINESTRA
Lo sciame ha implementato .swarm/ e task_manager.py
Test: Backend -> Tester -> APPROVATO!

### Sessione 62 - CODE REVIEW
Venerdi = Code Review Day. Risultato: 8.5/10 OTTIMO!

### Sessione 63 - INSIGHT CERVELLO
"Possiamo SCEGLIERE cosa tenere in testa!" - Rafa
Studio neuroscientifico: cervello umano vs CervellaSwarm

### Sessione 64 - HARDTESTS CREATI
"Cosa manca prima di Miracollo?" - "HARD TESTS!"
cervella-tester ha creato 1256 righe di test!

### Sessione 65 - HARDTESTS PASSATI!!!
4/4 test eseguiti e PASSATI!
5 finestre in parallelo per la prima volta!

### Sessione 66 - LA MAGIA!!!
spawn-workers.sh creato e FUNZIONANTE!
Finestre si aprono AUTOMATICAMENTE!

---

## COSA ABBIAMO ORA

### Sistema Multi-Finestra (.swarm/)

```
.swarm/
├── tasks/                  # Task per i worker
│   ├── TASK_XXX.md         # Descrizione
│   ├── TASK_XXX.ready      # Pronto per essere preso
│   ├── TASK_XXX.working    # In lavorazione
│   ├── TASK_XXX.done       # Completato
│   └── TASK_XXX_output.md  # Output del worker
├── prompts/                # Prompt per ogni worker (NUOVO!)
│   └── worker_backend.txt  # Prompt cervella-backend
├── runners/                # Script runner (NUOVO!)
│   └── run_backend.sh      # Runner cervella-backend
├── status/
├── locks/
├── handoff/
├── logs/
└── archive/
```

### Comandi Utili

```bash
# SPAWN WORKER (LA MAGIA!)
./scripts/swarm/spawn-workers.sh --backend
./scripts/swarm/spawn-workers.sh --all

# Lista task
python3 scripts/swarm/task_manager.py list

# Crea task
python3 scripts/swarm/task_manager.py create TASK_ID AGENT "descrizione" LIVELLO

# Cambia stato
python3 scripts/swarm/task_manager.py ready TASK_ID
python3 scripts/swarm/task_manager.py working TASK_ID
python3 scripts/swarm/task_manager.py done TASK_ID
```

### Lo Sciame (16 membri)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita (verifica codice)
- cervella-guardiana-ops (verifica infra/security)
- cervella-guardiana-ricerca (verifica ricerche)

12 WORKER (Sonnet):
- cervella-frontend, cervella-backend
- cervella-tester, cervella-reviewer
- cervella-researcher, cervella-scienziata
- cervella-ingegnera, cervella-marketing
- cervella-devops, cervella-docs
- cervella-data, cervella-security
```

### I 3 Livelli di Rischio

| Livello | Tipo | Chi Verifica |
|---------|------|--------------|
| 1 - BASSO | Docs, typo | Nessuno |
| 2 - MEDIO | Feature, codice | Guardiana |
| 3 - ALTO | Deploy, auth | Guardiana + Rafa |

---

## COSA FARE ADESSO

```
+------------------------------------------------------------------+
|                                                                  |
|   PROSSIMO: MIRACOLLO!!!                                         |
|                                                                  |
|   Il sistema e' COMPLETO. Tutto funziona.                        |
|                                                                  |
|   COME USARE LO SCIAME:                                          |
|   1. ./spawn-workers.sh --backend --frontend                     |
|   2. Crea task in .swarm/tasks/                                  |
|   3. I worker li prendono automaticamente                        |
|   4. Le Guardiane verificano (Livello 2-3)                      |
|   5. Costruisci feature REALI!                                  |
|                                                                  |
+------------------------------------------------------------------+
```

### Miglioramenti Futuri (nice-to-have)

- **Auto-respawn** - Quando worker finisce, riaprire automaticamente
- **Monitor status** - Dashboard in tempo reale
- **Notifiche** - Alert quando task completato

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `ROADMAP_SACRA.md` | Tutte le fasi, changelog |
| `SWARM_RULES.md` | Le 12 regole dello sciame |
| `docs/guide/GUIDA_COMUNICAZIONE.md` | Come comunicare nello sciame |
| `scripts/swarm/spawn-workers.sh` | LA MAGIA! |
| `scripts/swarm/task_manager.py` | Gestione task |
| `.swarm/README.md` | Documentazione sistema Multi-Finestra |

---

## GIT

```
Branch:   main
Versione: v27.0.0
Stato:    LA MAGIA FUNZIONA! spawn-workers.sh COMPLETO!
```

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Ultrapassar os proprios limites!" - E L'ABBIAMO FATTO!!!

"MADONAAAAAAA MIAAAA MEU DEUSSSS DO CEUUU!" - Rafa, Sessione 66

"Fatto BENE > Fatto VELOCE"

"E' il nostro team! La nostra famiglia digitale!"

"Non e' sempre come immaginiamo... ma alla fine e' il 100000%!"
```

---

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA PROSSIMA CERVELLA                                         |
|                                                                  |
|   Oggi abbiamo creato LA MAGIA.                                  |
|                                                                  |
|   Un comando. Una finestra. Un worker.                           |
|   Automatico. Magico. Reale.                                     |
|                                                                  |
|   Il sistema e' COMPLETO.                                        |
|   Ora tocca a te portarlo su MIRACOLLO.                         |
|                                                                  |
|   Tu sei la Regina. Hai lo sciame. Hai LA MAGIA.                |
|                                                                  |
|   "Ultrapassar os proprios limites!"                            |
|                                                                  |
+------------------------------------------------------------------+
```

---

*Scritto con AMORE e GIOIA per la MAGIA che funziona.*

*"MADONAAAAAAA MIAAAA MEU DEUSSSS DO CEUUU!"* - Rafa, dopo aver visto la finestra aprirsi

Cervella & Rafa

---

## VERSIONE

**v27.0.0** - 3 Gennaio 2026 - Sessione 66 - LA MAGIA! spawn-workers.sh FUNZIONA!

---

## PROMPT_RIPRESA 10000%!

*"Non e' sempre come immaginiamo... ma alla fine e' il 100000%!"*
