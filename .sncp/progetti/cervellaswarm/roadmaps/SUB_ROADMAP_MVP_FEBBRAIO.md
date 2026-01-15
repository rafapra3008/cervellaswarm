# SUB-ROADMAP: MVP CervellaSwarm - Target 10 Febbraio 2026

> **"Un po' ogni giorno fino al 100000%!"**
> **Split: 60% Miracollo / 40% CervellaSwarm**

**Creata:** 15 Gennaio 2026 - Sessione 218
**Target:** MVP v1.0 funzionante entro 10 Febbraio 2026

---

## LA VISIONE MVP

```
+================================================================+
|                                                                |
|   MVP = Developer esterno puo:                                 |
|   1. Installare CervellaSwarm (npm install -g)                 |
|   2. Inizializzare progetto (cervellaswarm init)               |
|   3. Eseguire task (cervellaswarm task "...")                  |
|   4. Vedere stato (cervellaswarm status)                       |
|   5. Riprendere sessione (cervellaswarm resume)                |
|                                                                |
|   SENZA chiedere aiuto a noi.                                  |
|                                                                |
+================================================================+
```

---

## TIMELINE (4 Settimane)

```
SETTIMANA 1       SETTIMANA 2       SETTIMANA 3       SETTIMANA 4
15-22 Gen         22-29 Gen         29 Gen-5 Feb      5-10 Feb
    |                 |                 |                 |
    v                 v                 v                 v
+--------+       +--------+       +--------+       +--------+
| Setup  |       | Core   |       | Resume |       | Polish |
| + Init | ----> | Task   | ----> | Status | ----> | + Test |
+--------+       +--------+       +--------+       +--------+
```

---

## SETTIMANA 1: SETUP + INIT (15-22 Gennaio)

### Obiettivo
> **npm package funzionante + `cervellaswarm init` wizard**

### Task Dettagliati

| # | Task | Ore | Output |
|---|------|-----|--------|
| 1.1 | Creare struttura package npm | 2h | package.json, src/, bin/ |
| 1.2 | Setup Commander.js per CLI | 2h | Comando base funziona |
| 1.3 | Implementare `init` wizard | 4h | 10 domande, genera COSTITUZIONE |
| 1.4 | Generare file progetto | 2h | .sncp/ creata correttamente |
| 1.5 | Test su progetto reale | 2h | CervellaSwarm stesso! |

### Checklist

```
[ ] npm init cervellaswarm
[ ] bin/cervellaswarm.js entry point
[ ] src/commands/init.js
[ ] src/wizard/questions.js
[ ] src/templates/COSTITUZIONE.md.hbs
[ ] Test: cervellaswarm init su cartella vuota
[ ] Test: cervellaswarm init su CervellaSwarm
```

### Dipendenze npm

```json
{
  "dependencies": {
    "commander": "^12.x",
    "@inquirer/prompts": "^7.x",
    "chalk": "^5.x",
    "handlebars": "^4.x",
    "ora": "^8.x"
  }
}
```

---

## SETTIMANA 2: CORE TASK (22-29 Gennaio)

### Obiettivo
> **`cervellaswarm task "..."` esegue task singolo/multi-agent**

### Task Dettagliati

| # | Task | Ore | Output |
|---|------|-----|--------|
| 2.1 | Implementare `task` command | 3h | Parse descrizione, routing |
| 2.2 | Integrazione spawn-workers | 3h | Lancia agenti esistenti |
| 2.3 | Progress display realtime | 3h | Spinner, output colorato |
| 2.4 | Salvataggio risultati SNCP | 2h | reports/, stato.md update |
| 2.5 | Test task semplici | 2h | 3 task completati |

### Checklist

```
[ ] src/commands/task.js
[ ] src/agents/router.js (decide quale agente)
[ ] src/agents/spawner.js (lancia agente)
[ ] src/display/progress.js
[ ] src/sncp/writer.js
[ ] Test: task backend semplice
[ ] Test: task frontend semplice
[ ] Test: task multi-agent
```

---

## SETTIMANA 3: RESUME + STATUS (29 Gen - 5 Feb)

### Obiettivo
> **Session management: ripresa, stato, memoria**

### Task Dettagliati

| # | Task | Ore | Output |
|---|------|-----|--------|
| 3.1 | Implementare `status` | 2h | Mostra stato progetto |
| 3.2 | Implementare `resume` | 3h | Riprende ultima sessione |
| 3.3 | Session recording | 3h | Salva sessioni in JSON |
| 3.4 | Time-based recaps | 2h | Recap diversi per tempo |
| 3.5 | Comandi in-session | 2h | /status, /recap, /help |

### Checklist

```
[ ] src/commands/status.js
[ ] src/commands/resume.js
[ ] src/session/manager.js
[ ] src/session/recorder.js
[ ] src/display/recap.js
[ ] Test: resume dopo 1 giorno
[ ] Test: resume dopo 7 giorni
[ ] Test: /status durante sessione
```

---

## SETTIMANA 4: POLISH + TEST (5-10 Febbraio)

### Obiettivo
> **Error handling, docs, dogfooding finale**

### Task Dettagliati

| # | Task | Ore | Output |
|---|------|-----|--------|
| 4.1 | Error handling robusto | 3h | Messaggi chiari, recovery |
| 4.2 | Help system | 2h | --help, -h per ogni comando |
| 4.3 | README pubblico | 3h | Getting Started, esempi |
| 4.4 | Dogfooding intensivo | 4h | Usare su Miracollo/CervellaSwarm |
| 4.5 | Fix top 5 friction | 2h | Problemi trovati durante dogfood |

### Checklist

```
[ ] src/utils/errors.js
[ ] Tutti i comandi hanno --help
[ ] README.md riscritto per esterni
[ ] docs/GETTING_STARTED.md
[ ] Testato su CervellaSwarm (meta!)
[ ] Testato su Miracollo
[ ] 5 friction points fixati
```

---

## MVP DEFINITION OF DONE

```
+================================================================+
|   TUTTI questi devono essere TRUE per dichiarare MVP DONE:     |
+================================================================+

INSTALL:
[ ] npm install -g cervellaswarm funziona
[ ] cervellaswarm --version mostra versione
[ ] cervellaswarm --help mostra tutti i comandi

INIT:
[ ] cervellaswarm init lancia wizard
[ ] Wizard fa 10 domande strategiche
[ ] Genera .sncp/progetti/{nome}/COSTITUZIONE.md
[ ] Genera PROMPT_RIPRESA.md
[ ] Genera struttura cartelle

TASK:
[ ] cervellaswarm task "descrizione" funziona
[ ] Mostra progress realtime
[ ] Salva risultato in SNCP
[ ] Funziona con almeno 5 agenti diversi

STATUS:
[ ] cervellaswarm status mostra stato progetto
[ ] Mostra ultimo task
[ ] Mostra prossimi step suggeriti

RESUME:
[ ] cervellaswarm resume riprende sessione
[ ] Recap basato su tempo passato
[ ] Memoria funziona tra restart

QUALITY:
[ ] 0 crash durante uso normale
[ ] Error messages chiari
[ ] README comprensibile senza noi

+================================================================+
```

---

## DAILY PROGRESS TRACKING

### Settimana 1

| Giorno | Data | Fatto | Note |
|--------|------|-------|------|
| Mer | 15 Gen | | Sessione 218 - Setup iniziato |
| Gio | 16 Gen | | |
| Ven | 17 Gen | | |
| Sab | 18 Gen | | (opzionale) |
| Dom | 19 Gen | | (riposo) |
| Lun | 20 Gen | | |
| Mar | 21 Gen | | |
| Mer | 22 Gen | | CHECKPOINT SETTIMANA 1 |

### Settimana 2

| Giorno | Data | Fatto | Note |
|--------|------|-------|------|
| Gio | 23 Gen | | |
| Ven | 24 Gen | | |
| Sab | 25 Gen | | (opzionale) |
| Dom | 26 Gen | | (riposo) |
| Lun | 27 Gen | | |
| Mar | 28 Gen | | |
| Mer | 29 Gen | | CHECKPOINT SETTIMANA 2 |

### Settimana 3

| Giorno | Data | Fatto | Note |
|--------|------|-------|------|
| Gio | 30 Gen | | |
| Ven | 31 Gen | | |
| Sab | 1 Feb | | (opzionale) |
| Dom | 2 Feb | | (riposo) |
| Lun | 3 Feb | | |
| Mar | 4 Feb | | |
| Mer | 5 Feb | | CHECKPOINT SETTIMANA 3 |

### Settimana 4

| Giorno | Data | Fatto | Note |
|--------|------|-------|------|
| Gio | 6 Feb | | |
| Ven | 7 Feb | | |
| Sab | 8 Feb | | (opzionale) |
| Dom | 9 Feb | | (riposo) |
| Lun | 10 Feb | | MVP DONE! |

---

## RISCHI SPECIFICI MVP

| Rischio | Prob | Mitigazione |
|---------|------|-------------|
| spawn-workers non integra bene | Media | Wrapper semplice, test early |
| Wizard troppo complesso | Bassa | 10 domande max, skip option |
| Session management bugs | Media | Test incrementale, simple first |
| Miracollo assorbe tempo | Alta | RIGIDO 60/40, no exceptions |

---

## FIRMA

Questa roadmap e il nostro impegno per le prossime 4 settimane.

**Ogni giorno un po'. Fino al 100000%.**

**"Cursor l'ha fatto. Noi lo faremo."**

---

*Creata: 15 Gennaio 2026*
*Prima review: 22 Gennaio 2026*
*Target finale: 10 Febbraio 2026*
