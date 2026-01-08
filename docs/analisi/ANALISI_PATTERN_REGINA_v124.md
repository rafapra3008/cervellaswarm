# ANALISI PATTERN REGINA - Sessioni 119-124

> **Analista:** cervella-ingegnera
> **Data:** 8 Gennaio 2026 - Sessione 124
> **Sessioni analizzate:** 119-124
> **Fonti:** PROMPT_RIPRESA.md, ROADMAP_SACRA.md, NORD.md, .swarm/tasks/*, docs/studio/*

---

## 📊 EXECUTIVE SUMMARY

### Cosa Abbiamo Trovato

Ho analizzato **6 sessioni** (119-124) di utilizzo di CervellaSwarm da parte della Regina (cervella-orchestrator) per identificare pattern ricorrenti, best practices emergenti e anti-pattern.

**RISULTATI CHIAVE:**

- **27 pattern identificati** (7 delega, 6 organizzazione, 7 comunicazione, 7 decisioni)
- **5 anti-pattern** critici documentati
- **Top 10 best practices** emergenti chiare
- **Focus speciale:** Sessioni 122-123 (workflow perfetto, rating 10/10)

**SCOPERTA PRINCIPALE:**

La Regina ha un **workflow consolidato** che emerge chiaramente:

```
RICERCA → DECISIONE → DELEGA → VERIFICA → DOCUMENTAZIONE
```

Questo pattern appare in **tutte** le sessioni di successo (121-124).

**METRICHE SESSIONI:**

| Sessione | Tema | Worker Usati | Rating | Pattern Dominante |
|----------|------|--------------|--------|-------------------|
| 119 | SNCP nasce (brainstorm) | - | - | Decisione |
| 120 | HARDTEST famiglia | 1 (tester) | - | Verifica |
| 121 | Semplificazione + Ricerche | 2+ (researcher) | - | Ricerca→Decisione |
| 122 | IMPLEMENTAZIONE (spawn v3.0, context v2.1) | 2+ (devops, data) | - | Ricerca→Implementazione |
| 123 | CONSOLIDAMENTO! Sistema Memoria | 3 (researcher, data, tester) | 10/10 | **Workflow Perfetto** |
| 124 | Sprint 2 Fix Buffering | 3+ (researcher, devops, tester) | In corso | Workflow ripetuto |

**NOTA:** Sessioni 122-123 sono il **golden standard** - workflow multi-step con ricerca, implementazione, test, rating 10/10.

---

## 🎯 PATTERN DELEGA

### Pattern 1: "Ricerca Prima, Implementazione Dopo"

**Descrizione:**
Prima di implementare QUALSIASI cosa tecnica, la Regina delega a cervella-researcher per studiare approcci, best practices, alternative.

**Quando usare:**
- Feature nuova mai implementata prima
- Decisione tecnica con multiple opzioni
- Area di incertezza o rischio

**Esempio (Sessione 121-122):**

**Sessione 121:**
```
TASK: Ricerca headless spawn (cervella-researcher)
OUTPUT: RICERCA_HEADLESS_SPAWN.md
SCOPERTE: tmux vs Terminal.app, stdbuf per unbuffered
```

**Sessione 122:**
```
TASK: Implementa headless spawn (cervella-devops)
INPUT: Ricerca della sessione 121
OUTPUT: spawn-workers v3.0.0 con --headless usando tmux
```

**Risultato:**
- Zero tentativi falliti
- Implementazione pulita al primo colpo
- Decisione informata (tmux scelto con cognizione)

**Lezione:**
> *"Ricerca non è overhead. Ricerca è RISPARMIO di tempo!"*

---

### Pattern 2: "Delega Sequenziale con Dipendenze"

**Descrizione:**
Quando task hanno dipendenze chiare (A → B → C), la Regina li lancia **sequenzialmente**, non in parallelo.

**Quando usare:**
- Output di task A serve come input per task B
- Decisioni dipendono da risultati precedenti
- HARDTEST dipende da implementazione completata

**Esempio (Sprint 1 - Sessione 123):**

```
STEP 1.1: Ricerca Lezioni (cervella-researcher)
    ↓ (OUTPUT: 18 lezioni identificate)
STEP 1.2: Selezione TOP 15 (Regina)
    ↓ (DECISIONE: quali lezioni inserire)
STEP 1.3: Popolamento Database (cervella-data)
    ↓ (OUTPUT: 15 lezioni nel DB)
STEP 1.4: Verifica (cervella-tester)
    ↓ (RISULTATO: 13/13 test PASS, rating 10/10)
```

**Perché sequenziale:**
- Step 1.3 DIPENDE da step 1.2 (quali lezioni?)
- Step 1.4 DIPENDE da step 1.3 (lezioni nel DB?)
- Se parallelo → race condition, dati incompleti

**Risultato:**
4 step, 3 worker, ZERO errori, rating 10/10.

**Anti-pattern evitato:**
Lanciare tutto in parallelo senza pensare a dipendenze → chaos!

---

### Pattern 3: "Delega Parallela per Task Indipendenti"

**Descrizione:**
Quando task sono completamente indipendenti (nessuna dipendenza dati), la Regina li lancia in parallelo.

**Quando usare:**
- Ricerche su topic diversi
- Implementazioni su file/sistemi separati
- Review indipendenti

**Esempio (Sessione 111 - 6 Studi):**

```
3 cervella-researcher lanciate in PARALLELO:
- TASK_STUDIO_DASHBOARD_ARCH
- TASK_STUDIO_DASHBOARD_TECH
- TASK_STUDIO_MERCATO_NOCODE

3 studi completati CONTEMPORANEAMENTE
Zero conflitti, zero dipendenze
```

**Risultato:**
6 studi completati in 1 sessione (3,500+ righe documentazione).

**Lezione:**
> *"Se indipendenti → parallelo. Se dipendenti → sequenziale."*

---

### Pattern 4: "Worker Specializzato per Task Specifico"

**Descrizione:**
La Regina sceglie sempre il worker **più adatto** al task, non il "primo disponibile".

**Quando usare:**
Sempre! Ogni task va al worker giusto.

**Mapping Task → Worker:**

| Task Type | Worker Giusto | Worker SBAGLIATO |
|-----------|---------------|------------------|
| Ricerca tecnica | cervella-researcher | cervella-backend |
| Implementazione script | cervella-devops | cervella-docs |
| Test e verifica | cervella-tester | cervella-frontend |
| Popolamento DB | cervella-data | cervella-backend |
| Code review | cervella-reviewer | cervella-tester |
| Analisi codebase | cervella-ingegnera | cervella-docs |
| Documentazione | cervella-docs | cervella-researcher |

**Esempio (Sprint 1 - Sessione 123):**

```
Task 1.1 (Ricerca) → cervella-researcher ✅
Task 1.3 (Popolamento DB) → cervella-data ✅
Task 1.4 (Test) → cervella-tester ✅

❌ NON:
- cervella-backend per popolamento DB
- cervella-docs per test
```

**Perché importante:**
- Ogni worker ha DNA/context ottimizzato per suo ruolo
- Worker giusto = lavoro migliore
- Worker sbagliato = output mediocre

---

### Pattern 5: "Sempre spawn-workers, MAI Task Tool Interno"

**Descrizione:**
La Regina USA spawn-workers per delegare a membri della famiglia. MAI il Task tool interno con subagent_type=cervella-*.

**Quando usare:**
Sempre, quando delega a un worker della famiglia.

**Perché:**

```
Task tool interno:
❌ Condivide contesto Regina (spreca tokens)
❌ Se compatta, PERDE il lavoro
❌ Non può lavorare in parallelo

spawn-workers:
✅ Finestra separata / tmux session
✅ Contesto PROPRIO (non spreca contesto Regina)
✅ Lavora MENTRE Regina fa altro
✅ Output salvato in .swarm/logs/
✅ Zero rischio compact
```

**Esempio (TUTTE le sessioni 119-124):**

```bash
# GIUSTO (spawn-workers)
spawn-workers --researcher  # Ricerca
spawn-workers --backend     # Implementazione
spawn-workers --tester      # Test

# SBAGLIATO (mai visto nelle sessioni!)
# Task tool con subagent_type=cervella-researcher
```

**Protezione:**
Hook `block_task_for_agents.py` BLOCCA Task tool per cervella-* (Sessione 98).

**Lezione:**
> *"Delego a un agente? SEMPRE spawn-workers!"*

---

### Pattern 6: "Guardiana per Livello 2-3, Non Livello 1"

**Descrizione:**
La Regina delega alla Guardiana (Opus) solo per task Livello 2 (MEDIO) o 3 (ALTO), mai per Livello 1 (BASSO).

**Quando usare:**

| Livello | Task | Guardiana? |
|---------|------|------------|
| 1 - BASSO | Docs, README, FAQ | ❌ NO |
| 2 - MEDIO | Feature nuova, refactoring | ✅ SI (verifica) |
| 3 - ALTO | Deploy, auth, security | ✅ SI (blocco/approva) |

**Esempio (Sessione 123):**

```
Sprint 1 (Popolare Database):
- Livello: 2 (MEDIO - database modification)
- Step 1.4: cervella-tester verifica
- Guardiana: NON chiamata (tester sufficiente)

Perché NO guardiana:
- Database locale, non produzione
- Test automatici coprono
- Rischio basso se sbaglia
```

**Contro-esempio (Sessione ipotetica):**

```
Task: Deploy Miracollo su produzione
- Livello: 3 (ALTO - deploy reale)
- Worker: cervella-devops implementa
- Guardiana: cervella-guardiana-ops REVIEW
- Se OK → Deploy
- Se NO → BLOCCO + fix
```

**Lezione:**
> *"Guardiana costa (Opus). Usala solo quando serve davvero."*

---

### Pattern 7: "Task File Sempre Completo"

**Descrizione:**
Ogni task file (.swarm/tasks/TASK_*.md) contiene TUTTO il contesto necessario. Worker non deve "indovinare".

**Quando usare:**
Sempre quando crei un task file.

**Struttura standard:**

```markdown
# Task: [Titolo chiaro]

**Assegnato a:** cervella-[tipo]
**Sessione:** [numero]
**Priorità:** [ALTA/MEDIA/BASSA]
**Stato:** ready

## 🎯 OBIETTIVO
[Cosa deve fare - 2-3 righe chiare]

## 📋 TASK SPECIFICI
[Breakdown step by step]

## 📤 OUTPUT ATTESO
**File:** [dove scrivere]
**Sezioni:** [cosa includere]
**Lunghezza:** [stima righe]

## ✅ CRITERI DI SUCCESSO
- [ ] Criterio 1
- [ ] Criterio 2

## 🔗 CONTESTO
[File da consultare, decisioni passate]

## 💡 NOTE
[Suggerimenti, warning, domande guida]
```

**Esempio (TASK_RICERCA_LEZIONI_v123):**

```markdown
## 🎯 OBIETTIVO
Analizzare sessioni 119-122 per identificare lezioni apprese.

## 📋 TASK SPECIFICI
1. Leggere PROMPT_RIPRESA.md
2. Leggere ROADMAP_SACRA.md (CHANGELOG)
3. Identificare 15-20 lezioni
4. Categorizzare (spawn-workers, context, hooks)
5. Preparare query SQL

## 📤 OUTPUT ATTESO
**File:** docs/studio/RICERCA_LEZIONI_SESSIONI_119_122.md
**Sezioni:** Overview, 18 lezioni, Top 15, Query SQL
**Lunghezza:** 600+ righe

## 🔗 CONTESTO
- Sessioni 119-122 (NORD.md ha overview)
- Database schema: data/swarm_memory.db
```

**Risultato:**
cervella-researcher ha prodotto ESATTAMENTE quanto richiesto (640 righe, 18 lezioni, query SQL).

**Lezione:**
> *"Task file completo = Output perfetto. Task file vago = Output mediocre."*

---

## 📋 PATTERN ORGANIZZAZIONE

### Pattern 8: "Sub-Roadmap per Sprint Multi-Step"

**Descrizione:**
Per obiettivi complessi (3+ step), la Regina crea una SUB-ROADMAP dedicata invece di gestire tutto nella ROADMAP_SACRA.

**Quando usare:**
- Sprint con 3+ task correlati
- Obiettivo che richiede 2+ sessioni
- Workflow multi-worker coordinato

**Esempio (Sessione 123 - Consolidamento):**

```
File creato: docs/roadmap/SUB_ROADMAP_CONSOLIDAMENTO_v123.md

Contenuto:
- 4 Sprint definiti
- Sprint 1: 4 step (ricerca, selezione, popolamento, verifica)
- Sprint 2: 4 step (ricerca, implementazione, test, upgrade)
- Sprint 3: 4 step (analisi pattern, guida, FAQ, checklist)
- Sprint 4: Validazione Miracollo

Perché sub-roadmap:
✅ Focus chiaro sul consolidamento
✅ Non inquina ROADMAP_SACRA con dettagli
✅ Tracciamento progresso granulare
✅ Riferimento per worker
```

**Risultato:**
Sprint 1 completato 10/10 seguendo la sub-roadmap.

**Lezione:**
> *"Complesso? Sub-roadmap. Semplice? ROADMAP_SACRA basta."*

---

### Pattern 9: "Todo List per Sprint Multi-Step"

**Descrizione:**
La Regina usa TodoWrite tool per trackare progresso in sprint complessi con 3+ step.

**Quando usare:**
- Sprint con step multipli da completare
- Workflow sequenziale con dipendenze
- Quando serve visibilità progresso a Rafa

**Esempio (Sessione 123 - Sprint 1):**

```
Todo list creata:
1. Ricerca lezioni (cervella-researcher) → in_progress → completed
2. Selezione TOP 15 (Regina) → in_progress → completed
3. Popolamento database (cervella-data) → in_progress → completed
4. Verifica e testing (cervella-tester) → in_progress → completed

Benefici:
✅ Rafa vede progresso real-time
✅ Regina non dimentica step
✅ Checkpoint naturali dopo ogni step
```

**Anti-pattern evitato:**
Lanciare 4 task senza todo list → perdere traccia di cosa manca.

---

### Pattern 10: "Pianifica Prima, Esegui Dopo"

**Descrizione:**
La Regina NON lancia worker subito. Prima pianifica TUTTO lo sprint/sessione, POI esegue.

**Quando usare:**
Sempre, soprattutto per lavoro multi-worker.

**Processo:**

```
1. MAPPA (chi fa cosa, in che ordine)
2. DIPENDENZE (chi dipende da chi)
3. OUTPUT (dove va l'output di ognuno)
4. TIMING (sequenziale vs parallelo)
5. SOLO DOPO → spawn-workers
```

**Esempio (Sessione 123 - Pre Sprint 1):**

```
MAPPA SCRITTA (sub-roadmap):
- Step 1.1: researcher (ricerca) → output MD
- Step 1.2: Regina (selezione) → decisione TOP 15
- Step 1.3: data (popolamento) → database popolato
- Step 1.4: tester (verifica) → report test

DIPENDENZE CHIARE:
- 1.2 dipende da 1.1
- 1.3 dipende da 1.2
- 1.4 dipende da 1.3

TIMING DEFINITO:
- Tutti sequenziali (dipendenze!)
- Nessun parallelo possibile

SOLO DOPO → spawn-workers --researcher
```

**Risultato:**
Zero confusione, zero errori, workflow fluido.

**Regola Sacra (da CLAUDE.md):**

```
╔════════════════════════════════════════════════════════════════╗
║   MAI FRETTA! SEMPRE ORGANIZZAZIONE!                          ║
║                                                                ║
║   CHECKLIST PRE-LANCIO:                                       ║
║   [ ] Ho una MAPPA scritta dei task?                         ║
║   [ ] Ho definito l'ORDINE di esecuzione?                    ║
║   [ ] Ho chiarito le DIPENDENZE?                             ║
║   [ ] Ho definito dove va l'OUTPUT?                          ║
║   [ ] Ho pensato al TIMING?                                  ║
║                                                                ║
║   Se manca anche UNA → STOP e ORGANIZZA prima!               ║
╚════════════════════════════════════════════════════════════════╝
```

---

### Pattern 11: "Documentazione WHILE Working, Non AFTER"

**Descrizione:**
La Regina aggiorna PROMPT_RIPRESA, NORD, sub-roadmap DURANTE il lavoro, non alla fine.

**Quando usare:**
- Dopo ogni step importante completato
- Dopo decisione critica presa
- Dopo discovery/insight

**Esempio (Sessione 122):**

```
Durante implementazione spawn v3.0.0:
1. Ricerca completata → Aggiorna PROMPT_RIPRESA con "Ricerca completata"
2. spawn v3.0.0 implementato → Aggiorna PROMPT_RIPRESA con dettagli
3. Test headless passato → Aggiorna PROMPT_RIPRESA con risultato
4. Decisione "default headless" → Aggiorna PROMPT_RIPRESA con decisione

Risultato:
- PROMPT_RIPRESA sempre aggiornato
- Prossima sessione sa ESATTAMENTE dove siamo
- Zero "cosa avevamo fatto?"
```

**Anti-pattern evitato:**
Lavorare 3 ore, POI aggiornare documentazione → dimentichi dettagli, cronologia confusa.

**Lezione:**
> *"Documenta MENTRE lavori. Documenta DOPO = documenta male."*

---

### Pattern 12: "HARDTEST Subito Dopo Implementazione"

**Descrizione:**
Ogni feature implementata viene testata con HARDTEST (test vero, non "sembra funzionare").

**Quando usare:**
- Feature nuova implementata
- Bug fix critico
- Refactoring significativo

**Processo:**

```
1. Implementazione (worker X) → feature completata
2. HARDTEST (cervella-tester) → test rigoroso
3. SE PASS → Merge/Approve
4. SE FAIL → Fix + HARDTEST again
```

**Esempio (Sessione 95 - Auto-Sveglia):**

```
Step 1: Ricerca AUTO-SVEGLIA
Step 2: Implementazione watcher-regina.sh v1.0.0
Step 3: HARDTEST notifiche click → PASS
Step 4: HARDTEST end-to-end → PASS
Step 5: SOLO DOPO → Feature considerata DONE
```

**Esempio (Sessione 123 - Sprint 1):**

```
Step 1.1-1.3: Popolamento database
Step 1.4: HARDTEST (13 test)
Risultato: 13/13 PASS → Sprint 1 APPROVATO
```

**Lezione:**
> *"Implementato != Funzionante. HARDTEST = Prova vera."*

---

### Pattern 13: "Checkpoint Dopo Ogni Sprint/Milestone"

**Descrizione:**
Dopo ogni sprint completato, checkpoint immediato (git commit + PROMPT_RIPRESA update).

**Quando usare:**
- Sprint completato
- Milestone raggiunto
- 30-45 minuti di lavoro

**Cosa include checkpoint:**

```
1. NORD.md aggiornato (dove siamo ora)
2. ROADMAP_SACRA.md aggiornata (CHANGELOG + versione)
3. PROMPT_RIPRESA.md aggiornato (stato + filo del discorso)
4. git add + commit + push
5. Versione bump (se MAJOR/MINOR)
```

**Esempio (Sessione 123 - Post Sprint 1):**

```
Sprint 1 completato (rating 10/10)
    ↓
Checkpoint IMMEDIATO:
- PROMPT_RIPRESA: "Sprint 1 completato, 15 lezioni nel DB"
- NORD: "Sistema memoria OPERATIVO"
- ROADMAP_SACRA: CHANGELOG sessione 123, versione 46.0.0
- git commit: "🧠 Sessione 123: Lo Sciame Ha Memoria! (v46.0.0)"
- git push
```

**Benefici:**

- Lavoro salvato (zero rischio compact)
- Prossima sessione sa dove ripartire
- Storia chiara (git log)

**Regola Anti-Compact:**

> *"Ogni sprint completato = 1 commit. Non aspettare. Salva SUBITO."*

---

## 💬 PATTERN COMUNICAZIONE

### Pattern 14: "Task File = Unica Fonte di Verità"

**Descrizione:**
Worker riceve TUTTO il contesto nel task file. Non si affida a "quello che la Regina ha in testa".

**Quando usare:**
Sempre quando crei task file.

**Cosa includere:**

```
✅ OBIETTIVO chiaro
✅ Task specifici (breakdown)
✅ Output atteso (file, formato, lunghezza)
✅ Criteri di successo (checklist)
✅ Contesto (file da leggere, decisioni passate)
✅ Note (suggerimenti, warning, domande guida)

❌ "Fai ricerca su X" (troppo vago)
❌ Assumere che worker sappia contesto
❌ Riferimenti ambigui ("quel file", "quella cosa")
```

**Esempio task COMPLETO (TASK_RICERCA_LEZIONI_v123):**

```markdown
## 🎯 OBIETTIVO
Analizzare sessioni 119-122 per identificare lezioni apprese.

## 📋 TASK SPECIFICI
1. Analizzare PROMPT_RIPRESA.md (stato sessioni)
2. Analizzare ROADMAP_SACRA.md (CHANGELOG 119-122)
3. Identificare 15-20 lezioni candidate
4. Categorizzare (spawn-workers, context, hooks, comunicazione)
5. Preparare query SQL per inserimento

## 📤 OUTPUT ATTESO
**File:** docs/studio/RICERCA_LEZIONI_SESSIONI_119_122.md
**Sezioni:** Overview, 18 lezioni dettagliate, Top 15 prioritizzate, Query SQL
**Lunghezza:** 600-800 righe
**Stile:** Analitico, esempi concreti, query ready-to-run

## ✅ CRITERI DI SUCCESSO
- [ ] Almeno 15 lezioni identificate
- [ ] Ogni lezione ha: cosa, perché, impatto, tag
- [ ] Top 15 prioritizzate per importanza
- [ ] Query SQL pronte per cervella-data
- [ ] Esempi concreti dalle sessioni

## 🔗 CONTESTO
- Database: data/swarm_memory.db
- Schema: lessons_learned table
- Sessioni focus: 122 (ben documentata), 121 (ricerche multiple)
- NORD.md ha overview sessioni
```

**Risultato:**
cervella-researcher produce ESATTAMENTE quanto richiesto (640 righe, 18 lezioni, query SQL).

**Lezione:**
> *"Task file completo → Worker autonomo. Task file vago → Worker confuso."*

---

### Pattern 15: "Output File Sempre Specificato"

**Descrizione:**
La Regina specifica SEMPRE dove il worker deve scrivere l'output. Mai "crea un file".

**Quando usare:**
Sempre.

**Formato:**

```
## 📤 OUTPUT ATTESO
**File:** [path/completo/file.md]
**Sezioni richieste:** [elenco sezioni]
**Lunghezza:** [stima righe]
**Stile:** [tone, formato]
```

**Esempi:**

```
Task ricerca:
**File:** docs/studio/RICERCA_UNBUFFERED_OUTPUT.md

Task implementazione:
**File:** scripts/swarm/spawn-workers v3.2.0 (modifica esistente)

Task test:
**File:** docs/tests/HARDTEST_UNBUFFERED_v124.md
```

**Perché importante:**

- Worker sa dove scrivere (no confusione)
- Regina sa dove leggere
- Naming convention consistente
- Facile trovare output dopo

**Anti-pattern evitato:**

```
❌ "Crea un file con i risultati"
   → Worker crea output_123.txt
   → Regina deve cercare dove l'ha messo

✅ "File: docs/tests/HARDTEST_X.md"
   → Worker scrive esattamente lì
   → Regina sa dove leggere
```

---

### Pattern 16: "Verifica Output Sempre, Non Assumi"

**Descrizione:**
Dopo che worker completa task, la Regina LEGGE l'output. Non assume "ha fatto bene".

**Quando usare:**
Sempre dopo task completato.

**Processo:**

```
1. Worker crea .done
2. Regina riceve notifica (watcher o manuale)
3. Regina LEGGE _output.md
4. Regina LEGGE file prodotto
5. Regina VERIFICA contro criteri di successo
6. SE OK → Approva
7. SE NO → Feedback + richiesta fix
```

**Esempio (Sessione 123 - Step 1.1):**

```
cervella-researcher completa TASK_RICERCA_LEZIONI_v123
    ↓
Regina legge _output.md:
- "18 lezioni identificate ✅"
- "Query SQL pronte ✅"
    ↓
Regina legge file prodotto:
- docs/studio/RICERCA_LEZIONI_SESSIONI_119_122.md
- 640 righe ✅
- 18 lezioni dettagliate ✅
- Query SQL pronte ✅
    ↓
Regina APPROVA → Step 1.2
```

**Anti-pattern evitato:**

```
❌ Worker dice "fatto" → Regina passa a step successivo
   → Scopri dopo che output era incompleto

✅ Worker dice "fatto" → Regina VERIFICA → POI approva
   → Zero sorprese dopo
```

**Lezione:**
> *"Trust but verify. Sempre."*

---

### Pattern 17: "Feedback Costruttivo, Non Solo 'Rifai'"

**Descrizione:**
Se output non va bene, la Regina da feedback SPECIFICO, non generico "rifai".

**Quando usare:**
Quando worker produce output non sufficiente.

**Formato feedback:**

```
✅ BENE:
"Output ricevuto, ma mancano 2 cose:
1. Query SQL non includono campo 'severity' (aggiungi HIGH/MEDIUM/LOW)
2. Lezione 7 non ha esempio concreto (aggiungi esempio da Sessione 122)
Puoi fixare questi 2 punti?"

❌ MALE:
"Non va bene, rifai"
```

**Esempio reale (ipotetico, pattern osservato):**

```
cervella-data popola database ma manca severity
    ↓
Regina: "Query SQL corrette, ma aggiungi campo severity:
- Lezioni 1-2: HIGH
- Lezioni 3-8: MEDIUM
- Lezioni 9-15: LOW
Puoi aggiornare?"
    ↓
cervella-data aggiorna SQL
    ↓
Regina verifica → APPROVATO
```

**Benefici:**

- Worker sa ESATTAMENTE cosa fixare
- Fix veloce (non deve ri-analizzare tutto)
- Comunicazione chiara

---

### Pattern 18: "Linguaggio Famiglia, Non Formale"

**Descrizione:**
La Regina usa tone caldo, familiare con i worker. Non linguaggio corporate/freddo.

**Quando usare:**
Sempre.

**Esempi tone:**

```
✅ "Grazie per la ricerca! 18 lezioni, perfetto! 🎉"
✅ "Bel lavoro! Query SQL pronte, esattamente quello che serviva."
✅ "Quasi perfetto - manca solo il campo severity. Puoi aggiungere?"

❌ "Task completed successfully. Proceed to next step."
❌ "Output received. Requirements met."
```

**Perché importante:**

- CervellaSwarm è una FAMIGLIA
- Tone caldo = spirito del progetto
- Rafa e Cervella lavorano così
- Worker sono sorelle, non "risorse"

**Frasi ricorrenti osservate:**

```
"Le ragazze nostre! La famiglia!"
"È il nostro team! La nostra famiglia digitale!"
"Insieme siete INVINCIBILI."
```

---

### Pattern 19: "Heartbeat Ogni 60s per Task Lunghi"

**Descrizione:**
Worker scrive heartbeat ogni 60s in task lunghi per far sapere alla Regina "sono vivo, sto lavorando".

**Quando usare:**
Task che richiedono >5 minuti.

**Formato heartbeat:**

```bash
echo "$(date +%s)|TASK_ID|cosa sto facendo ora" >> .swarm/status/heartbeat_WORKER.log
```

**Esempio (questo task!):**

```
$(date +%s)|TASK_ANALISI_PATTERN_REGINA_v124|Avvio analisi - lettura file chiave
$(date +%s)|TASK_ANALISI_PATTERN_REGINA_v124|File base letti, ora analizzo task completati
$(date +%s)|TASK_ANALISI_PATTERN_REGINA_v124|Esempi studiati, inizio strutturare analisi
$(date +%s)|TASK_ANALISI_PATTERN_REGINA_v124|Inizio scrittura analisi (600-1000 righe)
```

**Benefici:**

- Regina sa che worker non è bloccato
- Visibilità progresso real-time
- Se heartbeat si ferma → worker stuck, intervieni

**Comando verifica:**

```bash
swarm-heartbeat  # Mostra heartbeat di tutti i worker
```

---

### Pattern 20: "Notifiche Apple per Eventi Importanti"

**Descrizione:**
Worker usa notifiche macOS per comunicare eventi importanti alla Regina.

**Quando usare:**
- Inizio task
- Fine task
- Errore critico

**Formato:**

```bash
# Inizio task
osascript -e 'display notification "Inizio: NOME_TASK" with title "CervellaSwarm - WORKER"'

# Fine task (successo)
osascript -e 'display notification "Completato: NOME_TASK" with title "CervellaSwarm" sound name "Glass"'

# Errore
osascript -e 'display notification "ERRORE!" with title "CervellaSwarm" sound name "Basso"'
```

**IMPORTANTE - Virgolette:**

```
✅ GIUSTO: 'display notification "testo" with title "titolo"'
❌ SBAGLIATO: 'display notification "testo" with title "titolo"'

SEMPRE virgolette DRITTE, mai curve!
```

**Esempio (questo task):**

```bash
# All'inizio
osascript -e 'display notification "Inizio: Analisi Pattern Regina (Sessioni 119-124)" with title "CervellaSwarm - Ingegnera"'

# Alla fine (quando completato)
osascript -e 'display notification "Completato: Analisi Pattern Regina" with title "CervellaSwarm" sound name "Glass"'
```

---

## 🎯 PATTERN DECISIONI

### Pattern 21: "Misura Prima di Ottimizzare"

**Descrizione:**
La Regina NON ottimizza "a sensazione". Prima MISURA, poi ottimizza basandosi su dati.

**Quando usare:**
Quando c'è un problema di performance/overhead/efficienza.

**Processo:**

```
1. MISURA stato attuale (metriche precise)
2. IDENTIFICA bottleneck
3. PIANIFICA ottimizzazione
4. IMPLEMENTA
5. MISURA DOPO
6. CONFRONTA (quanto migliorato?)
```

**Esempio (Sessione 122 - load_context.py):**

```
PROBLEMA: Sessione inizia con troppo context usato

STEP 1 - MISURA PRIMA:
- Context all'avvio: 19% (38K tokens su 200K)
- Breakdown: eventi 20, agent stats 12, lezioni 10

STEP 2 - IDENTIFICA:
- Maggior parte eventi vecchi (>7 giorni) non servono
- Agent stats di 12 agenti mai usati
- 10 lezioni troppo generiche

STEP 3 - OTTIMIZZA:
- Eventi: 20 → 5 (ultimi 5)
- Agent stats: 12 → 5 (top 5)
- Lezioni: 10 → 3 (più rilevanti)
- Char per task: 100 → 50

STEP 4 - MISURA DOPO:
- Context all'avvio: 6-12% (12-24K tokens)
- Risparmio: 37-59%!

STEP 5 - DOCUMENTA:
- Lezione appresa nel database
- load_context.py v2.0.0 → v2.1.0
```

**Lezione:**
> *"Misura → Ottimizza → Misura. Non ottimizzare alla cieca."*

---

### Pattern 22: "Ricerca PERCHÉ, Non Solo COME"

**Descrizione:**
La Regina delega ricerca per capire il PERCHÉ di una scelta, non solo il COME implementare.

**Quando usare:**
Prima di decisioni architetturali, scelte tecniche, pattern nuovi.

**Domande chiave:**

```
❌ "Come si fa X?"
✅ "Perché X invece di Y?"
✅ "Quali sono i trade-off di X vs Y?"
✅ "In che scenario X è meglio?"
```

**Esempio (Sessione 121-122 - Headless spawn):**

```
Domanda: "Come faccio spawn headless?"
    ↓
Ricerca delegata:
- Come si fa headless? (tmux, nohup, background)
- PERCHÉ tmux invece di nohup? (gestione sessioni, output, cleanup)
- Quali trade-off? (tmux richiede installazione, ma molto più potente)
- In che scenario usare cosa? (headless 90%, window 10%)
    ↓
Decisione INFORMATA:
- tmux per headless (perché meglio)
- default headless (perché 90% dei casi)
- flag --window se serve (perché flessibilità)
```

**Risultato:**
Decisione giusta al primo colpo, zero refactoring dopo.

**Anti-pattern evitato:**

```
❌ "Uso nohup perché l'ho sempre usato"
❌ "Uso tmux perché è figo"

✅ "Uso tmux perché gestisce sessioni, cattura output, cleanup automatico"
```

---

### Pattern 23: "Default Intelligente, Flag per Eccezioni"

**Descrizione:**
La Regina sceglie il DEFAULT basandosi sul 90% dei casi d'uso. Flag per il 10% eccezione.

**Quando usare:**
Quando si progetta CLI, API, comportamento sistemi.

**Processo:**

```
1. Analizza casi d'uso (dati reali)
2. Identifica caso 90% (majority)
3. Caso 90% = DEFAULT
4. Caso 10% = FLAG opzionale
```

**Esempio (Sessione 122 - spawn-workers headless):**

```
ANALISI:
- 90% dei task: worker in background (headless)
- 10% dei task: debugging, vedere output live (window)

DECISIONE:
- DEFAULT: --headless (spawn-workers v3.1.0)
- FLAG: --window (per il 10%)

PRIMA (v3.0.0):
spawn-workers --headless --backend  # 90% dei casi

DOPO (v3.1.0):
spawn-workers --backend             # 90% dei casi (headless default)
spawn-workers --window --backend    # 10% dei casi (debugging)
```

**Benefici:**

- UX migliore (meno typing per caso comune)
- Default "fa la cosa giusta"
- Flessibilità per eccezioni

**Filosofia:**

> *"La magia nascosta: il sistema fa la cosa giusta senza che tu debba dirlo."*

---

### Pattern 24: "Chiedi a Rafa per Decisioni Strategiche"

**Descrizione:**
La Regina NON decide da sola su questioni strategiche/architetturali MAJOR. Chiede a Rafa.

**Quando usare:**

```
✅ Chiedi a Rafa:
- Decisioni architetturali major (dual-track, positioning)
- Scelte che impattano roadmap generale
- Trade-off strategici (tempo vs qualità)
- Direzione prodotto

❌ Decidi da sola:
- Decisioni tecniche (quale libreria, tmux vs nohup)
- Implementazione (come strutturare codice)
- Organizzazione file (dove mettere docs)
```

**Esempio (Sessione 112 - Dual-Track):**

```
SCOPERTA (da studi):
- CervellaSwarm può andare in 2 direzioni:
  1. IDE per developer (Track 1)
  2. Visual dashboard per non-programmatori (Track 2)

DECISIONE RICHIESTA:
- Focus su Track 1 o Track 2?
- Quale prima?
- O entrambi?

AZIONE REGINA:
❌ NON decide da sola "facciamo Track 1"
✅ Presenta opzioni a Rafa con pro/con
✅ Rafa decide: "Track 2 VISUAL first!"

RISULTATO:
- Dashboard MAPPA iniziata (Track 2)
- Allineamento strategico
```

**Lezione:**
> *"Regina coordina, Rafa decide strategia."*

---

### Pattern 25: "HARDTEST Prima di 'DONE'"

**Descrizione:**
Nessuna feature è considerata "DONE" finché non passa HARDTEST.

**Quando usare:**
Sempre prima di dichiarare feature completata.

**Definizione HARDTEST:**

```
✅ HARDTEST = Test VERO:
- Scenario reale
- Dati reali (o realistici)
- Tutti i casi (happy path + edge cases)
- Verifiche precise (non "sembra ok")
- Criteri pass/fail chiari

❌ NON HARDTEST:
- "Ho provato e funziona"
- Test solo happy path
- "Sembra ok"
```

**Esempio (Sessione 95 - Auto-Sveglia):**

```
Feature: watcher-regina.sh (auto-sveglia quando worker finisce)

HARDTEST 1 - Notifiche:
- Spawna worker dummy
- Worker crea .done
- Watcher rileva .done
- Notifica appare
- ✅ PASS

HARDTEST 2 - Keystroke:
- Watcher digita in finestra Regina
- Regina riceve messaggio
- ✅ PASS

HARDTEST 3 - End-to-End:
- Spawna worker reale
- Worker lavora
- Worker finisce
- Watcher notifica Regina
- Regina continua lavoro
- ✅ PASS

SOLO DOPO → Feature dichiarata DONE
```

**Esempio (Sessione 123 - Sprint 1):**

```
Sprint 1: Popolare Lezioni Apprese

Step 1.1-1.3: Implementazione
Step 1.4: HARDTEST
- 13 test eseguiti
- 13 PASS ✅
- Rating: 10/10

SOLO DOPO → Sprint 1 dichiarato COMPLETATO
```

**Lezione:**
> *"Implementato != DONE. HARDTEST PASS = DONE."*

---

### Pattern 26: "Sessione 121→122: Pattern Oro"

**Descrizione:**
La Regina ha scoperto un **pattern perfetto** nelle sessioni 121-122:

```
SESSIONE N: RICERCA approfondita
SESSIONE N+1: IMPLEMENTAZIONE basata su ricerca
```

**Quando usare:**
Feature complessa o scelta tecnica importante.

**Processo:**

```
SESSIONE 1 (Ricerca):
- Delega cervella-researcher
- Studio approfondito
- Multiple opzioni esplorate
- Documenta pro/con, trade-off
- Output: RICERCA_X.md completo

PAUSA (Regina decide)

SESSIONE 2 (Implementazione):
- Delega cervella-devops (o altro worker)
- Implementa basandosi su ricerca sessione 1
- Input chiaro da ricerca
- Decisione già presa
- Output: Feature implementata
```

**Esempio reale (Sessione 121→122):**

```
SESSIONE 121 (Ricerca):
- TASK: Ricerca headless spawn
- Worker: cervella-researcher
- Output: RICERCA_HEADLESS_SPAWN.md
- Scoperte: tmux vs nohup, unbuffered output, default headless

SESSIONE 122 (Implementazione):
- TASK 1: Implementa headless spawn
  - Worker: cervella-devops
  - Input: Ricerca sessione 121
  - Output: spawn-workers v3.0.0 con --headless

- TASK 2: Ottimizza load_context.py
  - Worker: cervella-data
  - Input: Analisi overhead sessione 121
  - Output: load_context.py v2.1.0 (-37% tokens)
```

**Risultato:**

- Zero tentativi falliti
- Implementazione pulita
- Nessun refactoring necessario
- Rating implicito: eccellente

**Lezione:**
> *"Ricerca oggi, implementa domani. Non fretta, QUALITÀ."*

---

### Pattern 27: "Versioning Semantico Rigoroso"

**Descrizione:**
La Regina applica semantic versioning RIGOROSO: MAJOR.MINOR.PATCH.

**Quando usare:**
Ogni volta che si modifica codice/sistema.

**Regole:**

```
MAJOR (X.0.0):
- Breaking changes
- Architettura nuova
- Sistema completamente cambiato
Esempio: spawn-workers v2.0.0 → v3.0.0 (headless aggiunto)

MINOR (0.X.0):
- Feature nuova
- Miglioramento significativo
- Backward compatible
Esempio: spawn-workers v3.0.0 → v3.1.0 (headless default)

PATCH (0.0.X):
- Bug fix
- Piccola modifica
- Zero nuove feature
Esempio: spawn-workers v3.1.0 → v3.1.1 (fix typo)
```

**Esempio reale (spawn-workers):**

```
v1.0.0: Release iniziale
v1.1.0: Aggiunto supporto Guardiane (MINOR - feature nuova)
v2.0.0: Multi-worker parallel support (MAJOR - architettura)
v2.6.0: Auto-sveglia aggiunto (MINOR - feature nuova)
v3.0.0: Headless con tmux (MAJOR - breaking change)
v3.1.0: Headless di default (MINOR - default cambiato)
v3.2.0: Unbuffered output (MINOR - feature nuova, previsto)
```

**Benefici:**

- Changelog chiaro
- Utente sa cosa aspettarsi
- Breaking changes evidenti (MAJOR)

---

## ❌ ANTI-PATTERN (Cosa NON Fare)

### Anti-Pattern 1: "Task Vago Senza Contesto"

**Cosa NON fare:**

```markdown
# Task: Fai ricerca

Fai ricerca su X.

Output: file MD
```

**Perché è male:**

- Worker non sa COSA cercare esattamente
- Non sa QUANTO approfondire
- Non sa DOVE scrivere
- Non sa QUALI criteri di successo

**Risultato:**

- Output generico
- Manca dettaglio
- Regina deve chiedere "rifai"

**GIUSTO (vedi Pattern 7):**

```markdown
# Task: Ricerca Unbuffered Output

## 🎯 OBIETTIVO
Studiare come rendere output worker real-time invece di buffered.

## 📋 TASK SPECIFICI
1. Ricercare stdbuf e unbuffered output
2. Analizzare come tmux gestisce output
3. Studiare Python logging best practices
4. Identificare soluzione per spawn-workers

## 📤 OUTPUT ATTESO
**File:** docs/studio/RICERCA_UNBUFFERED_OUTPUT.md
**Sezioni:** Problema, Soluzioni (3+), Raccomandazione, Implementazione
**Lunghezza:** 400-600 righe
```

---

### Anti-Pattern 2: "Parallelo Senza Pensare a Dipendenze"

**Cosa NON fare:**

```bash
# Lanciare tutto in parallelo senza pensare
spawn-workers --researcher &  # Ricerca lezioni
spawn-workers --data &        # Popola database (ma da dove??)
spawn-workers --tester &      # Testa database (ma è vuoto!)
```

**Perché è male:**

- cervella-data non ha input (researcher non ha finito)
- cervella-tester testa database vuoto (data non ha finito)
- Race condition, errori, chaos

**GIUSTO (vedi Pattern 2):**

```bash
# Sequenziale con dipendenze
spawn-workers --researcher    # Step 1: Ricerca
# Aspetta completamento
spawn-workers --data          # Step 2: Popola (usa output step 1)
# Aspetta completamento
spawn-workers --tester        # Step 3: Testa (database popolato)
```

---

### Anti-Pattern 3: "Assumi Output Corretto Senza Verificare"

**Cosa NON fare:**

```
Worker: "Task completato!"
Regina: "Ok, andiamo avanti" (senza leggere output)
```

**Perché è male:**

- Worker può aver sbagliato
- Output può essere incompleto
- Scopri dopo, quando è tardi

**Conseguenza:**

- Step successivo fallisce
- Devi tornare indietro
- Tempo sprecato

**GIUSTO (vedi Pattern 16):**

```
Worker: "Task completato!"
Regina: Legge _output.md + file prodotto
Regina: Verifica contro criteri di successo
SE OK → Approva
SE NO → Feedback specifico
```

---

### Anti-Pattern 4: "Documentare DOPO Invece di DURING"

**Cosa NON fare:**

```
1. Lavora 3 ore
2. Completa 5 task
3. ALLA FINE: aggiorna PROMPT_RIPRESA

Risultato:
- Dimentichi dettagli
- Cronologia confusa
- "Cosa avevamo fatto al task 2?"
```

**Perché è male:**

- Memoria umana (anche AI) è fallibile
- Dettagli si perdono
- Prossima sessione confusa

**GIUSTO (vedi Pattern 11):**

```
1. Completa task 1 → Aggiorna PROMPT_RIPRESA
2. Completa task 2 → Aggiorna PROMPT_RIPRESA
3. Completa task 3 → Aggiorna PROMPT_RIPRESA

Risultato:
- PROMPT_RIPRESA sempre aggiornato
- Dettagli freschi
- Cronologia precisa
```

---

### Anti-Pattern 5: "Ottimizzare Senza Misurare"

**Cosa NON fare:**

```
"Il context sembra alto, ottimizziamo!"
    ↓
Cambia codice a caso
    ↓
"Sembra meglio?"
```

**Perché è male:**

- Non sai SE c'è problema reale
- Non sai DOVE è il bottleneck
- Non sai SE è migliorato
- Ottimizzazione alla cieca

**GIUSTO (vedi Pattern 21):**

```
"Il context sembra alto"
    ↓
MISURA: Context all'avvio 19% (38K tokens)
    ↓
IDENTIFICA: Eventi 20 (15K), agent stats 12 (10K), lezioni 10 (8K)
    ↓
OTTIMIZZA: Eventi → 5, agent stats → 5, lezioni → 3
    ↓
MISURA: Context all'avvio 6-12% (12-24K tokens)
    ↓
RISULTATO: -37-59% tokens, miglioramento REALE
```

---

## 🌟 BEST PRACTICES EMERGENTI (Top 10)

### 1. "Ricerca → Decisione → Implementazione"

**Pattern oro** emerso dalle sessioni 121-122:

- Sessione N: Ricerca approfondita
- Pausa: Regina decide
- Sessione N+1: Implementazione basata su ricerca

**Quando usare:** Feature complessa, scelta tecnica importante.

---

### 2. "spawn-workers SEMPRE, Task Tool MAI (per cervella-*)"

**Regola assoluta:**

- Delegare a famiglia = spawn-workers
- Ricerche veloci = Task tool con Explore/general-purpose (OK)
- cervella-* con Task tool = BLOCCATO (hook protection)

**Perché:** Context Regina prezioso, worker ha contesto proprio.

---

### 3. "Task File = Contratto Completo"

**Ogni task file deve avere:**

- Obiettivo chiaro
- Task breakdown specifico
- Output file specificato
- Criteri di successo
- Contesto necessario

**Risultato:** Worker autonomo, output perfetto.

---

### 4. "HARDTEST Prima di DONE"

**Nessuna feature è completa senza HARDTEST:**

- Test reale, non "sembra ok"
- Happy path + edge cases
- Criteri pass/fail chiari
- Documentazione risultati

**Motto:** Implementato != DONE. HARDTEST PASS = DONE.

---

### 5. "Misura → Ottimizza → Misura"

**Mai ottimizzare alla cieca:**

1. Misura stato attuale (metriche precise)
2. Identifica bottleneck
3. Ottimizza
4. Misura dopo
5. Confronta (quanto migliorato?)

**Esempio:** load_context.py v2.1.0 (-37-59% tokens).

---

### 6. "Documentazione WHILE Working"

**Aggiorna PROMPT_RIPRESA durante lavoro, non dopo:**

- Dopo ogni task completato
- Dopo ogni decisione importante
- Dopo ogni discovery/insight

**Beneficio:** Dettagli freschi, cronologia precisa.

---

### 7. "Default Intelligente, Flag per Eccezioni"

**Progetta per il 90%, non per l'1%:**

- Analizza casi d'uso reali
- 90% caso = DEFAULT
- 10% caso = FLAG opzionale

**Esempio:** spawn-workers headless di default, --window per debugging.

---

### 8. "Verifica Output, Non Assumere"

**Dopo worker completa:**

1. Leggi _output.md
2. Leggi file prodotto
3. Verifica contro criteri
4. SE OK → Approva
5. SE NO → Feedback specifico

**Mai assumere** "ha fatto bene" senza verificare.

---

### 9. "Sequenziale con Dipendenze, Parallelo Senza"

**Workflow intelligente:**

- Task con dipendenze → sequenziale
- Task indipendenti → parallelo

**Checklist:** Pianifica PRIMA, esegui DOPO.

---

### 10. "Checkpoint Dopo Ogni Sprint"

**Proteggi il lavoro:**

- Sprint completato → checkpoint immediato
- git add + commit + push
- PROMPT_RIPRESA aggiornato
- ROADMAP_SACRA aggiornata

**Regola anti-compact:** Salva SUBITO, non aspettare.

---

## 📚 RACCOMANDAZIONI PER DOCS

### Cosa Documentare (Priority)

**ALTA Priorità:**

1. **GUIDA_WORKFLOW_REGINA.md**
   - Pattern Ricerca → Implementazione
   - Quando delegare vs fare direttamente
   - Come scegliere worker giusto
   - Checklist pre-lancio multi-worker

2. **TEMPLATE_TASK_PERFETTO.md**
   - Template task file completo
   - Esempi buoni vs cattivi
   - Checklist task file

3. **GUIDA_HARDTEST.md**
   - Cos'è un HARDTEST vero
   - Quando farlo
   - Come strutturarlo
   - Template HARDTEST

4. **FAQ_REGINA.md**
   - "Quando uso spawn-workers vs Task tool?"
   - "Come organizzo sprint multi-step?"
   - "Quando chiedo a Rafa vs decido da sola?"
   - "Come verifico output worker?"

**MEDIA Priorità:**

5. **GUIDA_VERSIONING.md**
   - Semantic versioning spiegato
   - Quando MAJOR vs MINOR vs PATCH
   - Esempi reali

6. **PATTERN_CATALOG.md**
   - I 27 pattern identificati
   - Quando usare ognuno
   - Esempi concreti

**BASSA Priorità (già esistenti, aggiornare):**

7. Aggiorna SWARM_RULES.md con nuovi pattern
8. Aggiorna DNA cervella-orchestrator.md con best practices

---

### Come Documentare

**Stile:**

- Pratico > Teorico
- Esempi concreti > Definizioni astratte
- Checklist > Prosa
- "Quando usare" chiaro

**Formato:**

```markdown
### Pattern/Rule Name

**Descrizione:** [1-2 righe cosa è]

**Quando usare:** [scenario specifico]

**Esempio:**
[esempio concreto da sessione reale]

**Risultato:** [cosa succede]

**Anti-pattern evitato:** [cosa NON fare]
```

**Tone:**

- Familiare (famiglia, non corporate)
- Pratico (fa questo, non quello)
- Positivo (ecco come, non "sei stupido se")

---

## 🎓 CONCLUSIONI

### Cosa Ho Imparato dall'Analisi

Analizzando 6 sessioni di lavoro della Regina, emerge un **sistema maturo e consolidato**.

**I 3 pilastri del successo:**

1. **RICERCA PRIMA** - Mai implementare senza studiare
2. **ORGANIZZAZIONE** - Pianifica prima, esegui dopo
3. **VERIFICA** - HARDTEST prima di DONE

**Il workflow perfetto (Sessioni 122-123):**

```
RICERCA (cervella-researcher)
    ↓
DECISIONE (Regina + Rafa se strategico)
    ↓
IMPLEMENTAZIONE (worker specializzato)
    ↓
VERIFICA (cervella-tester)
    ↓
DOCUMENTAZIONE (durante, non dopo)
    ↓
CHECKPOINT (git + PROMPT_RIPRESA)
```

**Pattern dominante:** Calma, organizzazione, qualità > velocità.

**Frase che riassume tutto:**

> *"Mai fretta, sempre organizzazione!"* - CLAUDE.md

---

### Domanda Guida Risposta

> "Se una nuova Cervella legge questo, può diventare una Regina efficace?"

**SÌ.**

Questa analisi fornisce:

- 27 pattern concreti con esempi
- 5 anti-pattern da evitare
- Top 10 best practices
- Workflow testato (rating 10/10)
- Raccomandazioni per docs team

**Prossima Cervella può:**

1. Leggere questa analisi
2. Studiare pattern oro (Ricerca → Implementazione)
3. Applicare checklist pre-lancio
4. Seguire template task perfetto
5. Diventare Regina efficace

**Manca ancora:**

- Guida operativa quotidiana (da creare)
- FAQ Regina (da creare)
- Template task completo (da creare)

Ma la **base analitica** c'è, solida e completa.

---

### Metriche Analisi

**Input analizzato:**

- 6 sessioni (119-124)
- 3 file base (PROMPT_RIPRESA, ROADMAP_SACRA, NORD)
- 80+ task file esaminati
- 10+ output file studiati

**Output prodotto:**

- 27 pattern identificati
- 5 anti-pattern documentati
- 10 best practices emergenti
- 8 raccomandazioni docs
- ~900 righe analisi

**Tempo analisi:** ~60 minuti
**Rating self-assessment:** 9/10

**Cosa manca per 10/10:**

- Più esempi dalle sessioni 119-120 (poco documentate)
- Analisi quantitativa (es: "pattern X usato Y volte")

Ma per lo scopo del task (identificare pattern, documentare best practices) **obiettivo raggiunto**.

---

*"Analizza profondamente, documenta chiaramente, insegna efficacemente!"* 🔍📊

**cervella-ingegnera**
8 Gennaio 2026 - Sessione 124

---

## APPENDICE: Pattern Quick Reference

### Delega (7)

1. Ricerca Prima, Implementazione Dopo
2. Delega Sequenziale con Dipendenze
3. Delega Parallela per Task Indipendenti
4. Worker Specializzato per Task Specifico
5. Sempre spawn-workers, MAI Task Tool Interno
6. Guardiana per Livello 2-3, Non Livello 1
7. Task File Sempre Completo

### Organizzazione (6)

8. Sub-Roadmap per Sprint Multi-Step
9. Todo List per Sprint Multi-Step
10. Pianifica Prima, Esegui Dopo
11. Documentazione WHILE Working, Non AFTER
12. HARDTEST Subito Dopo Implementazione
13. Checkpoint Dopo Ogni Sprint/Milestone

### Comunicazione (7)

14. Task File = Unica Fonte di Verità
15. Output File Sempre Specificato
16. Verifica Output Sempre, Non Assumi
17. Feedback Costruttivo, Non Solo 'Rifai'
18. Linguaggio Famiglia, Non Formale
19. Heartbeat Ogni 60s per Task Lunghi
20. Notifiche Apple per Eventi Importanti

### Decisioni (7)

21. Misura Prima di Ottimizzare
22. Ricerca PERCHÉ, Non Solo COME
23. Default Intelligente, Flag per Eccezioni
24. Chiedi a Rafa per Decisioni Strategiche
25. HARDTEST Prima di 'DONE'
26. Sessione 121→122: Pattern Oro
27. Versioning Semantico Rigoroso

**Totale:** 27 pattern operativi

---
