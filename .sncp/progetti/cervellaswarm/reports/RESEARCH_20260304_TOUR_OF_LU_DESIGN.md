# Research: "A Tour of LU" - Design del Tutorial Interattivo

> **Data:** 2026-03-04
> **Researcher:** Cervella Researcher
> **Scopo:** Analisi dei migliori tutorial interattivi per linguaggi di programmazione
> **Target:** Definire struttura e formato per "A Tour of LU" (Fase D4)
> **Fonti consultate:** 4 tutorial analizzati, 12+ ricerche web, letteratura su cognitive load

---

## 1. ANALISI COMPARATIVA DEI TUTORIAL

### A. "A Tour of Go" - IL GOLD STANDARD

**Struttura:**
- 4 capitoli principali (Basics, Methods+Interfaces, Generics, Concurrency)
- Circa 76 lezioni totali (con variazioni negli anni)
- Circa 11 esercizi distribuiti (1-3 per capitolo, alla fine di ogni capitolo)
- Tempo stimato: 4-6 ore per completarlo

**Progressione:**
```
Packages/Imports -> Variabili -> Funzioni -> Flusso
-> Struct -> Array -> Slice -> Map
-> Methods -> Interfaces -> Type Assertions
-> Goroutines -> Channels -> Select
```
Ogni capitolo conclude con esercizi pratici.

**Formato per ogni lezione:**
- Pannello sinistro: spiegazione testuale (3-8 righe, mai di piu)
- Pannello destro: codice eseguibile e modificabile
- Il codice e GIA funzionante al caricamento della pagina
- L'utente puo modificare e rieseguire immediatamente
- Navigazione: < > con numero "Lezione X di Y"

**Cosa funziona bene:**
- Codice eseguibile dal secondo uno (no setup)
- "One concept per page" - mai due idee nella stessa lezione
- Esercizi al TERMINE di ogni capitolo, non dopo ogni lezione
- Il codice di default produce output visibile (premia subito)
- Layout split: leggi a sinistra, tocca a destra

**Cosa non funziona:**
- Nessun feedback automatico sugli esercizi (vai su forum a chiedere)
- Non salva il progresso (riinizi da zero)
- Mancanza di context: "perche mi serve questo?" non e mai spiegato
- Concurrency a fine tour = drop-off alto (argomento difficile, utenti stanchi)

---

### B. "Rust by Example" - L'APPROCCIO ALTERNATIVO

**Struttura:**
- 24 capitoli principali, ~100+ esempi totali (con sotto-sezioni)
- Nessun esercizio formale: ogni pagina e un esempio da leggere e modificare
- Tempo stimato: 8-15 ore (e piu un reference che un tutorial)
- Complementare a "The Rust Book" (che e narrativo/testuale)

**Progressione:**
```
Hello World -> Primitives -> Custom Types -> Control Flow
-> Functions -> Modules -> Error Handling
-> Std Library -> Testing -> Macros -> Unsafe
```

**Formato per ogni lezione:**
- Testo introduttivo breve (2-5 righe)
- Esempio di codice con commenti inline
- Output atteso mostrato sotto
- Link alla documentazione ufficiale
- Sezione "See also" con link correlati

**Cosa funziona bene:**
- Codice con commenti inline = spiega MENTRE mostra
- "See also" costruisce rete di conoscenza
- Nessuna aspettativa di "completare tutto" = meno pressione
- 24 capitoli chiari con titoli che dicono esattamente cosa troverai

**Cosa non funziona:**
- Non e un tutorial, e una reference con esempi - scatter mentale
- Manca guida narrativa: "perche vuoi imparare X?"
- Non adatto ai principianti (assume base di programmazione solida)
- Troppo lungo come primo approccio al linguaggio

---

### C. "Gleam Language Tour" - IL MODELLO PER LINGUAGGI GIOVANI

**Struttura (verificata):**
- 6 capitoli principali
- 63 lezioni totali (18 Basics + 10 Functions + 11 Flow Control + 10 Data Types + 5 Std Library + 9 Advanced)
- Nessun esercizio formale: ogni lezione ha codice modificabile
- Tempo stimato: 2-3 ore (il linguaggio e piccolo)
- URL speciale: /everything mostra TUTTO in una pagina

**Progressione:**
```
Hello World -> Modules -> Types -> Strings -> Booleans
-> Assignments -> Lists -> Constants
-> Functions -> Higher Order -> Pipelines
-> Pattern Matching -> Recursion
-> Tuples -> Custom Types -> Records -> Results
-> Standard Library
-> Opaque Types -> Use -> Externals
```

**Formato per ogni lezione:**
- Il codice si compila e ESEGUE MENTRE SCRIVI (real-time, nessun click)
- Pannello sinistro: spiegazione + codice editabile
- Pannello destro: output in tempo reale
- WebAssembly: il compilatore Gleam gira NEL BROWSER
- CodeFlask come editor (leggero, non Monaco)

**Cosa funziona bene:**
- Feedback ISTANTANEO: compile-as-you-type e rivoluzionario
- "/everything" page: utenti avanzati saltano avanti
- Copertina intera del linguaggio in 63 lezioni (non si esclude nulla)
- Gleam e la 2a lingua "most admired" su Stack Overflow 2025 - il tour ha contribuito
- Deploy su GitHub Pages (stessa infrastruttura che abbiamo noi)

**Cosa non funziona:**
- Nessun esercizio con soluzione: non testa la comprensione
- Il feedback real-time e ottimo ma richiede il compilatore in WASM
  (noi usiamo Pyodide, dobbiamo fare click "Run" - diverso)
- I 63 capitoli scoraggiano chi vuole solo "capire il concetto base"

---

### D. "Tour of Scala" - L'APPROCCIO DOCUMENTAZIONE

**Struttura:**
- 33 capitoli, navigazione sequenziale
- Mix tra tutorial e documentazione di riferimento
- Codice eseguibile via Scastie (servizio esterno)
- Tempo stimato: 4-8 ore

**Progressione:**
```
Basics -> Classes -> Traits -> Composition
-> Higher-order Functions -> Case Classes -> Pattern Matching
-> Generics -> Variance -> Type Bounds
-> Implicits -> Annotations -> Packages
```

**Cosa funziona bene:**
- 33 capitoli con titoli chiari: facile trovare quello che serve
- Mescola OOP e FP in modo naturale

**Cosa non funziona:**
- Scastie e un servizio esterno: latenza, possibili downtime
- Troppo verboso: alcune pagine hanno 500+ parole
- Assume background Java: non accessibile a tutti
- "Just a brief tour, not a full language tutorial" = promise non mantenuta

---

## 2. PATTERN UNIVERSALI (cosa emerge da tutti e 4)

### Cosa i migliori fanno SEMPRE

| Pattern | Go | Gleam | Rust by Example | Scala |
|---------|-----|-------|-----------------|-------|
| Codice eseguibile inline | SI | SI | SI | Parziale |
| One concept per pagina | SI | SI | SI | No |
| Progressione semplice->complesso | SI | SI | SI | SI |
| Nessun setup locale | SI | SI | SI | Parziale |
| Codice gia funzionante al caricamento | SI | SI | SI | No |
| Progress indicator | SI | SI | No | No |

### Cognitive Load Research - Cosa dice la scienza

La ricerca su cognitive load (Sweller, 1988; applicata al software learning) dice:
- **1 concetto per lezione** e il limite cognitivo ottimale
- **Progress bar** riduce ansia e aumenta completamento
- **Feedback immediato** (codice che gira) sposta in long-term memory piu veloce
- **Micro-learning** (lezioni < 5 min) ottimizza retention vs lezioni lunghe
- **"Wow moment" entro i primi 3 step** e critico per il retention

---

## 3. ANALISI DELLA NOSTRA SITUAZIONE TECNICA

### Cosa abbiamo
- Monaco Editor + Pyodide gia LIVE su GitHub Pages
- `check_source()` e `run_source()` funzionanti nel browser
- 4 esempi gia scritti (hello, confidence, multiagent, ricette)
- Il limite: click "Run" (non real-time come Gleam) - va bene, e normale

### La differenza chiave da Gleam
Gleam compila JavaScript -> puo fare real-time (0ms latency).
Noi usiamo Pyodide (Python in WASM): ~200-500ms per run.
Quindi: click "Run" e il pattern giusto, non real-time.
Non e uno svantaggio - e come Tour of Go funziona!

### Cosa ci manca per D4
- Struttura multi-step con navigazione (< > + contatore)
- Testo esplicativo per ogni step
- Codice pre-caricato per ogni step (come gli esempi attuali)
- Progress indicator
- (Opzionale) esercizi con soluzione

---

## 4. RACCOMANDAZIONI CONCRETE PER "A TOUR OF LU"

### Struttura Proposta: 4 Capitoli, 24 Step Totali

**Principio guida:** Tour of Go come modello, ma piu breve.
Gleam ha 63 step per un linguaggio piccolo. LU ha 3 concetti chiave
(types, agents, protocols) + 1 avanzato (verify). 24 step e il giusto.

```
CAPITOLO 1: TIPI (6 step) - "Dai un nome alle cose"
  1.1 Hello LU          -- type Color = Red | Green | Blue
                           (variant, il piu semplice possibile)
  1.2 Record Types      -- record Point { x: int, y: int }
                           (dati strutturati)
  1.3 Tipi Composti     -- variant + record insieme
                           (esempio: type Result = Ok(String) | Error(String))
  1.4 Confident[T]      -- l'incertezza come tipo, non come stringa
                           (il nostro pilastro 1: mostra perche e diverso)
  1.5 Livelli di fiducia -- Certain, High, Medium, Low, Speculative
                           (far vedere cosa cambia nella pratica)
  1.6 ESERCIZIO         -- "Modella una pizza: tipo, ingredienti, confidence"
                           (primo checkpoint reale)

CAPITOLO 2: AGENTI (6 step) - "Chi fa cosa"
  2.1 Il tuo primo agente   -- agent Worker (struttura base)
  2.2 Role e Trust Tiers    -- trusted vs standard vs untrusted: perche conta
  2.3 Capabilities          -- can read, can write, cannot deploy
  2.4 Requires + Ensures    -- contratti dichiarativi (pilastro 2)
  2.5 Due agenti insieme    -- Worker + Guardiana (sistema minimo funzionante)
  2.6 ESERCIZIO             -- "Crea un agente Cuoco con capabilities realistiche"

CAPITOLO 3: PROTOCOLLI (7 step) - "Come parlano"
  3.1 Il tuo primo protocollo  -- roles + una sola interazione
  3.2 Sequenza di messaggi     -- ask -> return (il pattern base)
  3.3 Properties: terminates   -- always terminates: cosa significa?
  3.4 Properties: no_deadlock  -- visualizza un deadlock, poi la soluzione
  3.5 Choice (when decides)    -- decisioni nel protocollo
  3.6 Requires + Ensures       -- i contratti nel protocollo
  3.7 ESERCIZIO                -- "Il protocollo della nonna: salva ricetta + verifica"
                                  (esempio gia esistente, perfetto come esercizio!)

CAPITOLO 4: VERIFICA FORMALE (5 step) - "Provalo, non sperarlo"
  4.1 lu check: errori in tempo reale -- mostra cosa sbaglio e perche LU-N-XXX
  4.2 lu verify: Lean 4 sotto cofano  -- breve intro alla verifica matematica
  4.3 Il ciclo completo               -- types -> agents -> protocol -> verified
  4.4 Confronto: senza LU vs con LU  -- il "prima" e "dopo" (narrativo, no esercizio)
  4.5 DEMO FINALE                     -- "Build your first verified protocol in 10 min"
                                         (il multi-agent pipeline gia esistente)
```

**Totale: 24 step, ~4 esercizi, ~90-120 minuti per completare**

---

### Formato Raccomandato per Ogni Step

Ispirato al Tour of Go (il gold standard), adattato alla nostra infrastruttura:

```
[HEADER]
Capitolo X - Step Y/Z: [Titolo Breve]
Progress bar: [####.....]

[PANNELLO SINISTRO - fisso, ~300px]
Titolo: "Il tuo primo agente"

Spiegazione: 4-8 righe MAX.
Una frase sull'idea centrale.
Una o due righe "perche questo conta per LU".
Mai piu di un paragrafo.

"Cosa noti nel codice:"
- bullet 1 (punta a keyword specifica)
- bullet 2 (spiega l'effetto)

[PANNELLO DESTRO - flex, Monaco Editor]
Codice pre-caricato (funzionante, bello)

[OUTPUT - sotto editor]
Output di run_source() gia visibile
(il codice di default gia gira, utente vede risultato subito)

[NAVIGAZIONE]
< Precedente    [Step 3 di 24]    Prossimo >
```

**Regole contenuto:**
- Testo: max 8 righe, font 14-16px, linee corte
- Codice: 15-30 righe, gia funzionante
- Output: gia visibile al caricamento (non aspettare click)
- 1 solo concetto per step

---

### Come Integrare nel Playground Pyodide Esistente

L'integrazione MINIMA e sufficiente. Non servono grandi riscritture:

**Approccio 1: Tab "Tour" nel playground esistente (RACCOMANDATO)**
- Aggiungere tab "Tour" accanto ai 4 esempi esistenti
- Ogni step e un "esempio" con metadata: titolo, spiegazione, step number
- La struttura di `LU_EXAMPLES` in `examples.js` si estende con campi aggiuntivi
- Navigazione < > aggiunta nella sidebar

**Questo approccio:**
- Riusa tutto il codice esistente (Monaco + Pyodide + run_source)
- Non richiede nuovo deploy
- L'utente che arriva al playground vede sia "Esempi" che "Tour"
- Stima: 1 sessione di implementazione (D4 step 2)

**Approccio 2: Pagina separata `tour.html`**
- Pro: layout puo essere ottimizzato (split 40/60)
- Contro: duplica la logica Pyodide (26MB da ricaricare)
- Contro: due URL da mantenere
- Non raccomandato

---

### Numero di Step Finale: 24

**Motivazione dalla ricerca:**

| Tutorial | Step totali | Ore stimate | Linguaggio |
|----------|-------------|-------------|------------|
| Tour of Go | ~76 | 4-6h | Sistema + Concurrency |
| Gleam Tour | 63 | 2-3h | Linguaggio piccolo |
| Rust by Example | 100+ | 8-15h | Reference, non tutorial |
| Tour of Scala | 33 | 4-8h | OOP + FP |
| **Tour of LU (proposto)** | **24** | **~90min** | **3 concetti chiave** |

LU ha 3 pilastri (types, agents, protocols) + verifica.
24 step permette ~6 per pilastro + spazio per esercizi.
90 minuti e il target "completabile in una sessione" (Gleam-style).

Il motto del Tour di LU: **"Da zero a protocollo verificato in 90 minuti."**

---

## 5. COSA EVITARE (anti-pattern)

| Anti-Pattern | Chi lo fa | Problema |
|-------------|-----------|----------|
| Piu di 1 concetto per step | Scala | Cognitive overload |
| Esercizi senza soluzione | Go, Gleam | Frustrazione, abbandono |
| Codice non funzionante al caricamento | Scala | Prima impressione negativa |
| Steps > 60 | Rust by Example | Scoraggia prima ancora di iniziare |
| Nessun progress indicator | Rust by Example | "Quanto manca?" crea ansia |
| Spiegazioni > 10 righe | Tutti tranne Go | Si smette di leggere |
| Dipendenza da servizi esterni | Scala (Scastie) | Latenza, downtime, UX rotta |

---

## 6. INSIGHT SPECIFICO PER LU

### Il nostro vantaggio unico
Tutti i tutorial dei linguaggi mostrano sintassi.
Il Tour of LU puo mostrare **perche esiste ogni feature**.

Esempio per Confident[T] (step 1.4):
- Non solo "ecco la sintassi"
- Ma: "Prima: l'AI ti diceva 70% sicura come STRINGA.
  Adesso: e un TIPO. Il compilatore sa cosa fare."

Questo differenzia il Tour of LU da qualsiasi altro tutorial.

### L'esercizio della nonna (step 3.7)
Abbiamo gia il codice `La Nonna` in `examples.js`.
Diventa l'esercizio finale del capitolo 3.
L'utente lo "costruisce" step by step nei 7 step del capitolo,
e alla fine vede il codice completo come reward.

### La demo finale (step 4.5)
Il multi-agent example (`examples.js`) e gia perfetto come demo finale.
"Questo e un deployment pipeline verificato formalmente.
Nessun altro linguaggio puo dire questo."

---

## 7. RIEPILOGO RACCOMANDAZIONI

| Domanda | Risposta |
|---------|----------|
| Modello di riferimento | Tour of Go (layout + progressione) |
| Numero step | 24 |
| Numero capitoli | 4 |
| Tempo stimato | 90-120 minuti |
| Esercizi | 4 (uno per capitolo, alla fine) |
| Formato step | Split layout: testo sinistra, Monaco destra |
| Codice al caricamento | Gia eseguito (output visibile subito) |
| Progress indicator | SI (es. "Step 3 di 24") |
| Integrazione | Tab "Tour" nel playground esistente |
| Output step | check_source() + run_source() come ora |
| Real-time compile | No (click Run) - come Tour of Go, va bene |

---

## FONTI CONSULTATE

- [A Tour of Go](https://go.dev/tour/) - Gold standard analizzato
- [Gleam Language Tour - Table of Contents](https://tour.gleam.run/table-of-contents/) - 63 step verificati
- [Gleam's new interactive language tour (blog)](https://gleam.run/news/gleams-new-interactive-language-tour/) - Design decisions
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) - 24 capitoli analizzati
- [Tour of Scala](https://docs.scala-lang.org/tour/tour-of-scala.html) - 33 capitoli analizzati
- [Hacker News: Gleam's Interactive Language Tour](https://news.ycombinator.com/item?id=39055517) - Community feedback
- Cognitive Load Theory research (Sweller + applicazioni al software learning)
- Class Central: A Tour of Go analysis

---

*Cervella Researcher - Sessione 430 - 2026-03-04*
*"Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*
