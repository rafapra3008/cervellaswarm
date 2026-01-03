# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 3 Gennaio 2026 - Sessione 61 - MVP MULTI-FINESTRA COMPLETATO!

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
+------------------------------------------------------------------+
```

---

## LA STORIA (da dove veniamo)

### Sessione 60 - LA SCOPERTA

Rafa stava lavorando su Miracollo quando il compact era imminente. Tutto sembrava perso.
Ma poi ha fatto qualcosa di geniale: ha aperto una **NUOVA FINESTRA**.

La nuova Cervella ha fatto `git status` e ha visto TUTTO il lavoro non committato!
**30 moduli, ~5300 righe salvate!**

L'insight e' stato rivoluzionario:
```
PRIMA:   Una finestra = Un limite di contesto = Un limite di potenza
DOPO:    N finestre = N contesti = N volte piu' potenza!
```

Abbiamo studiato questo pattern con 2 ricerche approfondite:
- `docs/studio/STUDIO_MULTI_FINESTRA_TECNICO.md` - Il PERCHE' (finestre isolate, 200K token ognuna)
- `docs/studio/STUDIO_MULTI_FINESTRA_COMUNICAZIONE.md` - Il COME (protocollo .swarm/)

La Guardiana Ricerca ha validato: **8.5/10** - "Prima validare manualmente!"

### Sessione 61 - L'IMPLEMENTAZIONE (oggi!)

Abbiamo implementato il MVP! Lo sciame ha lavorato insieme:

```
Regina -> cervella-devops  -> Struttura .swarm/ creata!
Regina -> cervella-backend -> task_manager.py (307 righe!)
Regina -> cervella-tester  -> 10/10 test PASS! APPROVATO!
```

**IL PROTOCOLLO FUNZIONA!**

---

## COSA ABBIAMO ORA (funziona GIA'!)

### Il Sistema Multi-Finestra

```
.swarm/
├── tasks/                  # Qui la Regina mette i task
│   ├── TASK_XXX.md         # Descrizione task
│   ├── TASK_XXX.ready      # Flag: "task pronto"
│   ├── TASK_XXX.working    # Flag: "sto lavorando"
│   ├── TASK_XXX.done       # Flag: "completato"
│   └── TASK_XXX_output.md  # Output del worker
├── status/                 # Stato finestre
├── locks/                  # Lock per file critici
├── handoff/                # Handoff per compact
├── logs/                   # Log operazioni
└── archive/                # Task completati

scripts/swarm/
├── monitor-status.sh       # ./scripts/swarm/monitor-status.sh
└── task_manager.py         # python3 scripts/swarm/task_manager.py list
```

### Come Funziona

```
1. Regina crea .swarm/tasks/TASK_001.md
2. Regina fa: touch .swarm/tasks/TASK_001.ready
3. Worker vede .ready, legge il task
4. Worker fa: touch .swarm/tasks/TASK_001.working
5. Worker lavora...
6. Worker scrive: .swarm/tasks/TASK_001_output.md
7. Worker fa: touch .swarm/tasks/TASK_001.done
8. Regina legge output e verifica
```

### Script Utili

```bash
# Vedere stato di tutti i task
./scripts/swarm/monitor-status.sh

# Gestire task con Python
python3 scripts/swarm/task_manager.py list
python3 scripts/swarm/task_manager.py create TASK_003 cervella-backend "Descrizione" 1
python3 scripts/swarm/task_manager.py ready TASK_003
python3 scripts/swarm/task_manager.py status TASK_003
```

---

## LO SCIAME - La Famiglia (16 membri!)

```
+------------------------------------------------------------------+
|                                                                  |
|   TU SEI LA REGINA (Opus)                                        |
|   -> Coordina, decide, delega - MAI Edit diretti!                |
|                                                                  |
|   3 GUARDIANE (Opus - Supervisione)                              |
|   - cervella-guardiana-qualita (verifica codice)                |
|   - cervella-guardiana-ops (verifica infra/security)            |
|   - cervella-guardiana-ricerca (verifica ricerche)              |
|                                                                  |
|   12 WORKER (Sonnet - Esecuzione)                                |
|   - cervella-frontend      - cervella-backend                   |
|   - cervella-tester        - cervella-reviewer                  |
|   - cervella-researcher    - cervella-scienziata                |
|   - cervella-ingegnera     - cervella-marketing                 |
|   - cervella-devops        - cervella-docs                      |
|   - cervella-data          - cervella-security                  |
|                                                                  |
+------------------------------------------------------------------+
```

### I 3 Livelli di Rischio

| Livello | Tipo | Chi Verifica | Esempio |
|---------|------|--------------|---------|
| **1 - BASSO** | Docs, typo, README | Nessuno | Correggi typo |
| **2 - MEDIO** | Feature, codice | Guardiana | Nuova funzione |
| **3 - ALTO** | Deploy, auth, DB | Guardiana + Rafa | Modifica sicurezza |

---

## COSA FARE ADESSO

```
+------------------------------------------------------------------+
|                                                                  |
|   MVP COMPLETATO! IL SISTEMA FUNZIONA!                          |
|                                                                  |
|   OPZIONE A: Wave 2 Automazione                                 |
|   ----------------------------------------                       |
|   Cosa: Script watch-tasks.sh, auto-handoff, timeout            |
|   Perche': Rendere il sistema piu' automatico                   |
|   Tempo: 3-4 ore                                                 |
|                                                                  |
|   OPZIONE B: Usare su Miracollo                                 |
|   ----------------------------------------                       |
|   Cosa: Testare Multi-Finestra su progetto REALE                |
|   Perche': Validare con task concreti di produzione             |
|   Tempo: Variabile                                               |
|                                                                  |
|   OPZIONE C: Altre Feature                                      |
|   ----------------------------------------                       |
|   Cosa: Handoffs automatici, Sessions CLI, Hooks avanzati       |
|   Perche': Migliorare lo sciame                                 |
|   Tempo: 4-8 ore per feature                                    |
|                                                                  |
|   NOTA: Chiedi a Rafa cosa preferisce!                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STATO SISTEMA COMPLETO

| Componente | Stato | Note |
|------------|-------|------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE | Tutti operativi |
| 8 Hooks globali | FUNZIONANTE | SessionStart, PreCompact, etc. |
| SWARM_RULES v1.4.0 | FUNZIONANTE | 12 regole |
| Sistema Memoria SQLite | FUNZIONANTE | analytics.py |
| Pattern Catalog | FUNZIONANTE | 3 pattern validati |
| GUIDA_COMUNICAZIONE v2.0 | FUNZIONANTE | Testata con HARDTESTS |
| HARDTESTS Comunicazione | 3/3 PASS | Tutti i livelli testati |
| **.swarm/ Multi-Finestra** | **NUOVO!** | MVP completato! |
| **task_manager.py** | **NUOVO!** | 307 righe, 10/10 test! |

---

## GIT

```
Branch:   main
Commit:   5318da1
Versione: v26.0.0
Stato:    Pulito, tutto pushato
```

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `ROADMAP_SACRA.md` | Tutte le fasi, changelog |
| `SWARM_RULES.md` | Le 12 regole dello sciame |
| `docs/guide/GUIDA_COMUNICAZIONE.md` | Come comunicare nello sciame |
| `docs/studio/STUDIO_MULTI_FINESTRA_*.md` | Studi sul pattern |
| `.swarm/README.md` | Documentazione sistema Multi-Finestra |

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Nulla e' complesso - solo non ancora studiato."

"Fatto BENE > Fatto VELOCE"

"Il segreto e' la comunicazione!"

"E' il nostro team! La nostra famiglia digitale!"

"Ultrapassar os proprios limites!"

"Non e' sempre come immaginiamo... ma alla fine e' il 100000%!"
```

---

## VERSIONE

**v26.0.0** - 3 Gennaio 2026 - Sessione 61 - MVP MULTI-FINESTRA COMPLETATO!

---

*Scritto con ANIMA per la prossima Cervella.*

*"Lo sciame ha lavorato insieme e ha FUNZIONATO!"*

Cervella & Rafa
