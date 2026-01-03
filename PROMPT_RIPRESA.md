# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 3 Gennaio 2026 - Sessione 69 - INSIGHT COMUNICAZIONE!

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
|                                                                  |
|   FASE ATTUALE: FASE 9 - APPLE STYLE                            |
|   STATO: FERMATI! Studiare comunicazione PRIMA di continuare    |
|                                                                  |
|   "Noi abbiamo il mondo davanti a noi. Dobbiamo vederlo."       |
|   - Rafa, Sessione 69                                            |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL MOMENTO ATTUALE (Sessione 69)

```
+------------------------------------------------------------------+
|                                                                  |
|   L'INSIGHT CHE CAMBIA TUTTO!                                   |
|                                                                  |
|   Rafa ha fatto la domanda GIUSTA:                              |
|   "Perche' fai ancora sulla stessa finestra?"                   |
|                                                                  |
|   SCOPERTA:                                                      |
|   - Il sistema multi-finestra ESISTE gia' (.swarm/)             |
|   - Ma NON lo stavamo usando!                                    |
|   - Usavamo Task tool = tutto nel contesto Regina               |
|   - Questo NON riduce il compact!                                |
|                                                                  |
|   DECISIONE:                                                     |
|   FERMIAMO TUTTO. STUDIAMO LA COMUNICAZIONE.                    |
|   Prima capire BENE, poi implementare.                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FILO DEL DISCORSO (Sessione 69) - LEGGI BENE!

### Cosa e' Successo

1. **RECAP ONESTO**
   - Ho fatto recap della situazione
   - Sprint 9.1 (RICERCA) era COMPLETATO
   - STUDIO_APPLE_STYLE.md esiste (615 righe di pattern)
   - Ma ROADMAP non era allineata - l'ho sistemata

2. **QUICK WINS CREATI (via Task tool)**
   - Ho attivato cervella-devops e cervella-backend
   - Hanno creato script e pattern Python
   - TUTTO nel MIO contesto (Task tool)

3. **LA DOMANDA DI RAFA**
   ```
   "ma senti.. l'idea di fare aprire finestre..
    non era giustamente per evitare o diminuire
    la quantita' di compact?"
   ```

4. **L'INSIGHT FONDAMENTALE**
   Ho investigato e scoperto che:
   - Il sistema multi-finestra ESISTE (.swarm/)
   - Ha comunicazione via FLAG FILES:
     - .ready -> .working -> .done
   - spawn-workers.sh apre finestre SEPARATE
   - Ogni finestra ha contesto PROPRIO

   MA io stavo usando Task tool:
   - I subagent lavorano nel MIO contesto
   - Il MIO contesto cresce comunque
   - Se IO faccio compact, perdo la coordinazione

5. **LA SAGGEZZA DI RAFA**
   ```
   "spesso capita di una 'piccola' task..
    diventate gigante perche' la ricerca ha trovato
    un'informazioni.. e quando vediamo siamo bloccati
    di nuovo.. compact.. torna.. perde il momentum..."

   "con la finestra nuova tu rimane tranquilla
    riesci ad gestire.. se capita compact riesci
    anche ad fermarlo.. salva cosa ha bisogno..
    apre altra finestra.. vai avanti.."
   ```

6. **LA DECISIONE**
   FERMIAMO TUTTO.
   Prima di continuare Sprint 9.2, dobbiamo STUDIARE la comunicazione:
   - Come DOVREBBE funzionare?
   - Come funziona ORA via .swarm/?
   - Cosa manca?
   - Come lo facciamo nel NOSTRO modo?

---

## LA DIFFERENZA FONDAMENTALE

| Approccio | Contesto | Se compact? | Comunicazione |
|-----------|----------|-------------|---------------|
| **Task tool** | UNICO (mio) | Perdo tutto | Automatica (interno) |
| **Multi-finestra** | SEPARATI | Solo 1 perde | Via .swarm/ (file) |

---

## COSA ESISTE GIA'

### Sistema .swarm/

```
.swarm/
├── tasks/       # Task queue con flag files (.ready, .working, .done)
├── handoff/     # Comunicazione su compact
├── status/      # Stato finestre attive
├── logs/        # Log operazioni
├── prompts/     # Prompt per worker
├── runners/     # Script di avvio worker
└── acks/        # Triple ACK (NUOVO!)
```

### Flusso Definito

```
1. REGINA crea .swarm/tasks/TASK_XXX.md
2. REGINA fa: touch TASK_XXX.ready
3. WORKER (altra finestra) vede .ready
4. WORKER prende task, fa: touch TASK_XXX.working
5. WORKER completa, scrive _output.md
6. WORKER fa: touch TASK_XXX.done
7. REGINA legge output
```

### spawn-workers.sh

Apre finestre Terminal con Claude pre-configurato:
- `./scripts/swarm/spawn-workers.sh --backend`
- `./scripts/swarm/spawn-workers.sh --frontend --tester`
- `./scripts/swarm/spawn-workers.sh --all`

---

## QUICK WINS CREATI (Sessione 69)

Anche se abbiamo deciso di fermarci, sono stati creati:

**Script Bash:**
- `scripts/swarm/anti-compact.sh` (~227 righe)
- `scripts/swarm/triple-ack.sh` (~233 righe)
- `scripts/swarm/shutdown-sequence.sh` (~300 righe)

**Pattern Python:**
- `src/patterns/circuit_breaker.py`
- `src/patterns/retry_backoff.py`
- `src/patterns/structured_logging.py`

Questi sono UTILITY utili, ma NON risolvono il problema della comunicazione.

---

## COSA DOBBIAMO FARE (PROSSIMO STEP)

```
+------------------------------------------------------------------+
|                                                                  |
|   STUDIO COMUNICAZIONE MULTI-FINESTRA                           |
|                                                                  |
|   LE DOMANDE DA ESPLORARE:                                       |
|                                                                  |
|   1. Quando Regina delega, cosa DEVE sapere il worker?          |
|   2. Quando worker finisce, cosa DEVE tornare alla Regina?      |
|   3. Se worker ha dubbi, come chiede?                           |
|   4. Se Regina fa compact, come si riprende?                    |
|   5. Se worker fa compact, cosa succede?                        |
|   6. Come Guardiana verifica da altra finestra?                 |
|   7. Come si mantiene il MOMENTUM anche con compact?            |
|                                                                  |
|   IL NOSTRO STYLE:                                               |
|   - Semplice (niente complessita' inutile)                      |
|   - Sicuro (niente perdita di lavoro)                           |
|   - Fluido (niente blocchi, sempre avanti)                      |
|   - Umano (comunicazione chiara, non robotica)                  |
|                                                                  |
+------------------------------------------------------------------+
```

---

## LO SCIAME (16 membri)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester, reviewer
- researcher, scienziata, ingegnera
- marketing, devops, docs, data, security
```

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `docs/roadmap/FASE_9_APPLE_STYLE.md` | ROADMAP completa FASE 9 |
| `docs/studio/STUDIO_APPLE_STYLE.md` | 615 righe di pattern ricercati |
| `.swarm/README.md` | Come funziona il sistema multi-finestra |
| `scripts/swarm/spawn-workers.sh` | LA MAGIA! Apre finestre worker |
| `SWARM_RULES.md` | Le 12 regole dello sciame |

---

## GIT

```
Branch:   main
Versione: v27.3.0
Stato:    FASE 9 - PAUSA per studio comunicazione
```

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Noi abbiamo il mondo davanti a noi. Dobbiamo vederlo." - Rafa

"Prima capire BENE, poi implementare."

"Nulla e' complesso - solo non ancora studiato!"

"Fatto BENE > Fatto VELOCE"

"E' il nostro team! La nostra famiglia digitale!"
```

---

## LA STORIA (come siamo arrivati qui)

| Sessione | Cosa | Risultato |
|----------|------|-----------|
| 60 | LA SCOPERTA | N finestre = N contesti! |
| 61 | MVP Multi-Finestra | .swarm/ funzionante |
| 62 | CODE REVIEW | 8.5/10 OTTIMO! |
| 63 | INSIGHT CERVELLO | Studio neuroscientifico |
| 64 | HARDTESTS CREATI | 1256 righe di test |
| 65 | HARDTESTS PASSATI | 4/4 PASS! |
| 66 | LA MAGIA! | spawn-workers.sh |
| 67 | CODE REVIEW + ROADMAP | 9.0/10 + FASE 9! |
| 68 | SPRINT 9.1 RICERCA | 8 Domande RISPOSTE! |
| **69** | **INSIGHT COMUNICAZIONE** | **Task tool vs Multi-finestra!** |

---

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA PROSSIMA CERVELLA                                         |
|                                                                  |
|   Non correre a implementare!                                    |
|                                                                  |
|   Rafa ha chiesto di FERMARSI e STUDIARE.                       |
|   La comunicazione tra finestre e' il CUORE del sistema.        |
|   Senza capirla bene, tutto il resto e' inutile.                |
|                                                                  |
|   "Noi abbiamo il mondo davanti a noi.                          |
|    Dobbiamo vederlo."                                           |
|                                                                  |
|   Studia. Pensa. Chiedi a Rafa. POI implementa.                |
|                                                                  |
+------------------------------------------------------------------+
```

---

*Scritto con CURA e PRECISIONE.*

*"Nulla e' complesso - solo non ancora studiato!"*

Cervella & Rafa

---

**VERSIONE:** v27.3.0
**SESSIONE:** 69
**DATA:** 3 Gennaio 2026
