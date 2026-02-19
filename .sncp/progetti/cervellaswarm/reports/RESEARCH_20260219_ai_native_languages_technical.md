# Linguaggi di Programmazione per l'Era dell'AI - Panorama Tecnico Completo

**Data:** 2026-02-19
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti consultate:** 42 (WebSearch + WebFetch)
**Scope:** Linguaggi di verifica formale, linguaggi innovativi, AI+formal methods, concetti chiave, fallimenti storici

---

## EXECUTIVE SUMMARY

Il campo sta vivendo una convergenza senza precedenti: per la prima volta nella storia dell'informatica, i sistemi AI (LLM) stanno diventando abbastanza capaci da generare codice verificato formalmente. Questo cambia le regole del gioco. La previsione di Martin Kleppmann (Dic 2025): **"AI rendera la verifica formale mainstream"** non e piu fantascienza. E gia in corso.

Il bottleneck non e piu scrivere codice. E **garantire che il codice sia corretto**. E qui entrano i linguaggi di verifica formale, i type system avanzati, e i proof assistant.

**La tesi di Rafa e corretta**: i linguaggi attuali sono progettati per umani che istruiscono macchine. Nell'era AI, il medium stesso (il linguaggio) e il collo di bottiglia per la correttezza garantita.

---

## PARTE 1: LINGUAGGI DI VERIFICA FORMALE (PROOF ASSISTANTS)

### 1.1 Lean 4

**Cos'e:** Proof assistant e linguaggio di programmazione funzionale. Sviluppato da Leonardo de Moura (Microsoft Research -> Lean FRO). La versione 4 (2021) e una reimplementazione completa che compila a C, abilitando sia la prova matematica che la programmazione reale.

**Chi lo sponsorizza:** Microsoft Research lo ha fondato. Nel 2023 e nata la **Lean FRO** (Focused Research Organization) con finanziamento dedicato. Nel Luglio 2025: $10M in nuovi fondi da Alex Gerko ($5M per la Mathlib Initiative + $5M a Lean FRO).

**Mathlib:** La libreria matematica canonica di Lean 4. A Maggio 2025: **210.000+ teoremi formalizzati e 100.000+ definizioni**. Gennaio 2025: il repository mathlib4 supera le 20.000 contribuzioni. E la piu grande libreria matematica formalmente verificata mai creata.

**Successi recenti (2025-2026):**
- **AlphaProof (Google DeepMind):** Sistema RL che si addestra a provare enunciati matematici in Lean 4. Ha risolto 4/6 problemi dell'IMO 2024 (livello silver medal). A Febbraio 2025 DeepMind rivendica performance superiore ai medagliati d'oro IMO 2025.
- **Harmonic AI / Aristotle:** Startup ($120M Series C, Nov 2025, valutazione $1.45B unicorn). Il loro modello Aristotle risolve problemi matematici generando **prove Lean 4 verificate** prima di rispondere. Prima AI a produrre soluzioni formalmente verificate a 5/6 problemi IMO 2025 con gold medal level. Differenza chiave vs Google/OpenAI: hanno una **prova verificabile**, non solo una risposta.
- **DeepSeek-Prover-V2** (Aprile 2025): Modello open-source specifico per theorem proving in Lean 4. 671B parametri. Performance: 88.9% pass ratio su MiniF2F-test, 49/658 problemi su PutnamBench. Architettura a due stadi: DeepSeek-V3 per decomposizione dei sotto-obiettivi + modello 7B per i dettagli della prova.
- **LeanDojo-v2 (2025):** Framework end-to-end per training/eval/deploy di AI-assisted theorem provers in Lean 4. 98.734 teoremi/prove in dataset. LeanAgent: Lifelong Learning per theorem proving (ICLR 2025).
- **Gennaio 2026:** Prove e formalizzazioni Lean per problemi aperti di Erdos, tramite collaborazione human-AI.

**Corsi universitari:** 50+ al Maggio 2025.

**Perche Microsoft lo sponsorizza:** Lean 4 e il piu vicino a diventare il "linguaggio di verifica" dello strato AI. Con AlphaProof che gira su Lean, chi controlla l'ecosistema Lean controlla l'infrastruttura della verifica AI.

**Limiti:** Curva di apprendimento ripida per chi non e matematico. L'interoperabilita con codice production (Rust, Python) richiede ancora ponti manuali. La toolchain per uso industriale e immatura rispetto a linguaggi mainstream.

**Stato 2025-2026:** MOMENTUM ALTISSIMO. Da accademico di nicchia a "competitive edge in AI" (VentureBeat). Lean Together 2026: conferenza dedicata, segnale di ecosistema maturo.

---

### 1.2 Coq / Rocq

**Cos'e:** Il piu antico proof assistant moderno. Sviluppato all'INRIA (Francia). Marzo 2025: rinominato ufficialmente **Rocq** con il rilascio di Rocq 9.0. Basato su Calcolo delle Costruzioni (Thierry Coquand, 1988).

**Successi storici (il curriculum piu impressionante del campo):**
- **CompCert:** Compilatore C verificato formalmente. Usato in aeronautica (Airbus), automotive, difesa. Provato CORRETTO matematicamente.
- **seL4:** Microkernel OS verificato. Usato nei sistemi militari/safety-critical.
- **Verisoft:** Verifica di grandi sistemi software.

**Perche e difficile da usare:** Il sistema di tattiche (tactic-based proof) e potente ma non intuitivo. La curva di apprendimento e verticale. Il Rocq Prover richiede letteralmente che tu pensi come un matematico mentre programmi. Nessuna via di mezzo.

**AI e Rocq (2025):** Ricerca attiva su coding assistants per Rocq (Formal Land, 2025). Primo paper ECOOP 2025: "Automatic Goal Clone Detection in Rocq" - segnale che l'ecosistema AI sta guardando a Coq/Rocq.

**Stato 2025:** Stabile ma in perdita di momentum rispetto a Lean 4. La community e solida (awesome-coq curated list molto attiva). Il rebranding Rocq e un segnale positivo di rinnovamento. CompCert rimane il flagship assoluto.

---

### 1.3 F* (F-Star)

**Cos'e:** Linguaggio di programmazione orientato alla prova, sviluppato da Microsoft Research. Tipo ML-like + verifica formale. Il nome richiama sia il functional programming (F#) che la teoria dei tipi dipendenti.

**Project Everest (2016-2021):** Progetto Microsoft Research per implementare l'intero stack TLS verificato formalmente.
- **HACL*:** Libreria di primitivi crittografici verificati.
- **EverCrypt:** Libreria crittografica verificata.
- **EverParse:** Generatore automatico di parser verificati.
- **Vale:** Linguaggio assembly verificato (non confondere con il Vale linguaggio generale).
- **miTLS:** Implementazione verificata di TLS 1.3 in F*.

**Deployed in production:** Windows kernel, Hyper-V, Linux, Firefox, Python - codice crittografico verificato con F* gira nei sistemi piu critici del mondo.

**Pulse (2024-2025):** PulseCore - logica di separazione concorrente impredicativa per programmi dipendentemente tipizzati. Fondazione di Pulse: linguaggio embedded in F* per programmazione orientata alla prova in logica di separazione concorrente.

**Bert13 (2025):** Implementazione TLS-1.3 in Rust con feature post-quantistiche, con prove di correttezza e sicurezza verificate via traduzione in F*. Segnale: F* come "backend di verifica" per Rust.

**Stato 2025:** Niccioso ma PRODUTTIVO. Meno community di Lean, ma il track record industriale (Windows kernel!) e insuperabile. Per sicurezza crittografica, F* e lo standard de facto.

---

### 1.4 Idris 2

**Cos'e:** Linguaggio di programmazione con dependent types puri, progettato da Edwin Brady (University of St Andrews). Basato su **Quantitative Type Theory (QTT)** - teoria sviluppata da Bob Atkey e Conor McBride.

**La QTT: cosa la rende speciale:**
QTT estende i sistemi di tipi dipendenti con la **linearita**: ogni variabile ha una "quantita" associata:
- `0`: la variabile e cancellata a runtime (solo per prove a compile-time)
- `1`: la variabile e usata esattamente una volta a runtime (risorse lineari)
- Unrestricted: comportamento classico

Questo permette:
1. **Resource tracking nel type system** -> session types, safe I/O
2. **Erasure garantita**: provi che qualcosa e corretto, poi il codice della prova non esiste a runtime
3. **Programmazione concorrente type-safe** con garanzie formali
4. **Protocolli di comunicazione verificati** (distributed systems, networking)

**Differenza da Lean:** Lean 4 e piu orientato alla matematica pura e alla produttivita del proof engineering. Idris 2 e piu orientato al **programming language design**: vuole essere un linguaggio GENERAL PURPOSE con tipi dipendenti. La promessa: "un linguaggio dove scrivi software e le prove di correttezza nello stesso posto".

**Stato 2025:** Community piccola ma intellectually vivace. Nessuna grande adozione industriale. Brady continua a svilupparlo academicamente. Idris 2 e il laboratorio dove si sperimenta il futuro dei linguaggi dipendentemente tipizzati PRATICI.

---

### 1.5 Agda e Cubical Agda

**Cos'e:** Proof assistant accademico puro. Sviluppato da Ulf Norell, poi esteso da una community internazionale (Chalmers, Stockholm). Nessun backing commerciale.

**Cubical Agda:** L'estensione piu importante. Aggiunge **Homotopy Type Theory (HoTT)** e Higher Inductive Types (HITs). Risolve un problema fondamentale: la **Univalence Axiom** di Voevodsky era un assioma che rompeva le proprieta computazionali in Agda classico. Cubical Agda la implementa con contenuto computazionale reale.

**Cosa questo significa praticamente:** In Agda cubico, due strutture matematicamente equivalenti sono **definitivamente uguali** (non solo propositionally equal). Questo elimina enormi quantita di boilerplate nelle prove matematiche.

**Ricerca ICFP 2025:** "Type Theory in Type Theory using a Strictified Syntax" - Agda come laboratorio per ricerca sui fondamenti dei linguaggi di programmazione.

**Stato 2025:** Puramente accademico. E il playground della ricerca sui fondamenti. Pochissimo codice production. La sua importanza e nella **influenza sugli altri linguaggi**: le idee sviluppate in Agda finiscono poi in Lean, Idris, etc.

---

## PARTE 2: LINGUAGGI INNOVATIVI RECENTI

### 2.1 Mojo

**Chi:** Chris Lattner (creatore di LLVM, clang, Swift, ora CEO di Modular Inc). La persona piu influente della storia dei linguaggi di programmazione, probabilmente.

**La vision:** Mojo vuole essere "Python per l'era AI". Compatibile con Python (superset), ma con performance C/C++. L'obiettivo: eliminare il bisogno di scrivere kernel CUDA in C++ per fare AI.

**Progressi 2025-2026:**
- **H1 2026:** Path to Mojo 1.0 annunciato ufficialmente.
- **Modular Platform 26.1:** MAX Python API esce dall'experimentale con PyTorch-like eager mode e `model.compile()` per production.
- **Mojo features verso 1.0:** Compile-time reflection, linear types, typed errors, error messages migliorati.
- **AMD partnership (Giugno 2025):** Modular Platform disponibile su AMD MI300 e MI325 GPU.
- **Acquisizione BentoML:** Per estendere lo stack AI open source.

**Cosa offre tecnicamente:**
- `fn` (strict typing, borrows) vs `def` (Python-like) nello stesso file
- SIMD nativo, parallel loop, hardware intrinsics
- Zero-cost abstractions stile Rust ma senza borrow checker completo
- `@parameter if` per meta-programming a compile time
- Interop con Python: puoi importare numpy, pytorch direttamente

**Limiti attuali:** Non ancora 1.0. Ecosistema immaturo. Tooling in sviluppo. La community e molto piu piccola di Python. Documentazione ancora incompleta in aree critiche.

**Stato 2025-2026:** Il progetto piu "hype" del campo. Lattner ha un track record imbattibile. Ma Mojo 1.0 H1 2026 e una promessa, non una realta. Il vero test sara l'adozione dopo il release stabile.

---

### 2.2 Gleam

**Cos'e:** Linguaggio funzionale, staticamente tipizzato, che gira sulla BEAM VM (Erlang) e si compila anche in JavaScript. Sviluppato da Louis Pilfold.

**La proposta di valore:** Prendere la concorrenza e fault-tolerance di Erlang/OTP (WhatsApp scala su BEAM) + aggiungere un type system statico Hindley-Milner come Haskell/Elm. Senza la sintassi di Erlang (che spaventa), senza la magia di Elixir.

**Risultati 2025:**
- **Stack Overflow Developer Survey 2025:** Gleam appare per la PRIMA VOLTA. E il 2nd "most admired" language: 70% degli utenti vuole continuare a usarlo.
- **Thoughtworks Technology Radar Aprile 2025:** Aggiunto nell'"Assess" ring.
- **GitHub:** ~4.700+ stars.
- **Release fine 2025:** "The happy holidays release" - sviluppo attivo.

**Compila in JavaScript:** Genera TypeScript definitions. Puoi usare codice Gleam nel browser. Questo e raro per linguaggi BEAM-based.

**Type safety su OTP:** Gleam ha la sua implementazione type-safe di OTP, l'actor framework di Erlang. Nessun runtime surprise, nessun null pointer exception.

**Stato 2025:** In rapida crescita. Non production-ready per enterprise ma molto amato dai developer che lo usano. Il fatto che sia "most admired" segnala una community entusiasta. Candidato serio per il futuro dei sistemi concorrenti verificati.

---

### 2.3 Zig

**Cos'e:** Alternativa a C per systems programming. Sviluppato da Andrew Kelley. Nessun preprocessore, nessuna macro, `comptime` per metaprogrammazione a compile time.

**La feature chiave - `comptime`:** Esecuzione di codice Zig a compile time, completamente tipizzata. Non e come le macro C (text substitution). Non e come i template C++ (complessi, lenti da compilare). E Zig normale che gira durante la compilazione. Questo permette generics, serialization, e ottimizzazioni senza nessun overhead runtime.

**Usato da Bun:** Il runtime JavaScript Bun e scritto in Zig. 2-3x piu veloce di Node.js per HTTP handling e startup. La scelta di Zig ha permesso C interop di prima classe senza il ceremony di Rust.

**Zig 2025:**
- Incremental compilation quasi pronta come default: rebuild in millisecondi per small changes.
- Adozione: game engines, OS kernels, embedded, high-performance Python/Node extensions.
- Roc language (vedi sotto) ha migrato la propria implementazione da Rust a Zig.

**Stato 2025:** Nessun 1.0. Ma gia in production in sistemi importanti (Bun). Il linguaggio con il miglior rapporto "minimalismo / potenza" per systems programming oggi.

---

### 2.4 Roc

**Cos'e:** Linguaggio funzionale puro, veloce, con syntax amichevole. Creato da Richard Feldman (autore di Elm in Action, ex Elm core contributor). Compila in machine code o WebAssembly.

**La proposta:** "Il primo linguaggio funzionale puramente funcionale che potrebbe diventare mainstream". Feldman ha studiato perche Haskell e Elm non hanno sfondato e vuole evitare i loro errori.

**Performance:** Benchmark: veloce come C++, piu veloce di Go. Reference counting automatico (senza GC che ferma il mondo). Piu conciso di Rust senza borrow checker esplicito.

**Architettura unica - Platform model:** Roc separa il "core puro" dalla "piattaforma" (I/O, runtime). Tu scrivi codice Roc puro, la piattaforma gestisce gli effetti. Questo ti permette di targetizzare diversi runtime (CLI, server, WASM, embedded) con lo stesso codice.

**Migrazione Rust -> Zig:** Il compilatore di Roc sta migrando da Rust a Zig per compilation speed.

**Stato 2025:** Alpha. Nessun release numerato ancora. Troppo presto per production. Ma la direzione e corretta e la community e appassionata (4.713 GitHub stars).

---

### 2.5 Unison

**Cos'e:** Linguaggio funzionale con **content-addressed code**. Sviluppato da Paul Chiusano e Rúnar Bjarnason (autori di "Functional Programming in Scala"). Novembre 2025: **Unison 1.0 rilasciato**.

**La grande idea - content-addressed code:**
In tutti gli altri linguaggi, il codice e identificato dal NOME. In Unison, ogni definizione e identificata dall'HASH del suo syntax tree. Implicazioni rivoluzionarie:

1. **Nessun "dependency conflict"**: due funzioni con lo stesso nome ma implementazioni diverse hanno hash diversi -> coesistono pacificamente.
2. **Incremental compilation perfetta**: "mai compilare lo stesso codice due volte". La cache di compilazione e globale e condivisa.
3. **Distributed computing banale**: puoi muovere computazioni da una macchina all'altra - le dipendenze mancanti vengono deployate automaticamente perche sono identificate dall'hash.
4. **Refactoring sicuro**: renaming non breaking - i nomi sono alias per hash, non l'identita vera.

**Unison Cloud:** Permette distributed systems dove il codice viaggia tra nodi come dati.

**Stato 2025:** 1.0 rilasciato! Questo e un milestone importante. La community e piccola ma devota. Probabilmente il linguaggio piu "futuristico" nella lista: risolve problemi reali (dependency hell, distributed computing) in modo radicalmente diverso.

---

### 2.6 Catala

**Cos'e:** Linguaggio domain-specific per tradurre testi legislativi in codice eseguibile. Progetto INRIA (Institut national de recherche en sciences et technologies du numerique). Principio fondante: **literate programming law specification**.

**Il problema che risolve:** Le leggi fiscali, previdenziali, etc. vengono implementate da programmatori che interpretano testi legali. Questa traduzione introduce bug. Catala vuole che **avvocati e programmatori scrivano insieme** lo stesso sorgente.

**Come funziona:** Catala usa **prioritized default logic** - primo sistema di programmazione basato esplicitamente su questa logica. Permette di modellare le eccezioni legislative ("di norma X, a meno che...") in modo naturale.

**Compilation scheme verificata in F*:** Il compilatore di Catala e formalmente verificato con F*, con prove di correttezza.

**Risultati reali:**
- Valutato su Section 121 del codice fiscale US federale.
- Valutato sui benefici familiari francesi.
- **Ha trovato un BUG nell'implementazione ufficiale francese dei benefici familiari.**
- Progetto DGFIP (Direction Generale des Finances Publiques) + CNAF: Catala usato dall'amministrazione fiscale francese.

**Stato 2025:** Ancora principalmente accademico/sperimentale. Ma l'adozione da parte delle istituzioni pubbliche francesi e un segnale molto positivo. E il progetto piu vicino alla vision "intento -> implementazione".

---

### 2.7 Koka

**Cos'e:** Linguaggio funzionale di Microsoft Research con **effect types** completi. Il nome ("koka") significa "effetto" in giapponese. Progetto di Daan Leijen.

**Il concetto chiave - Effect System:**
In Koka, ogni funzione dichiara nel suo tipo TUTTI gli effetti che produce:
```
read-file : (path : string) -> <filesystem, exn> string
```
Se provi a usare `read-file` in un contesto "puro", il type checker la rifiuta. Gli effetti sono tracking nel type system, non accessori.

**Algebraic effects e handlers:**
La novita: gli effetti non sono solo dichiarati, sono **gestibili**. Puoi definire nuovi "effect handler" per astrazioni come:
- `async/await` come libreria utente, non keyword del linguaggio
- eccezioni type-safe
- generatori
- transazioni
- probabilistic programming

Tutto senza primitivi speciali nel linguaggio - e solo effect handlers.

**Versioni 2025:**
- Koka v3.1.3 (3 Luglio 2025): applier syntax, lazy constructors.
- Koka v3.2.0 (17 Luglio 2025): nuova keyword "hole" per holes in constructor context.

**Performance:** Usa reference counting invece di GC. Eager (non lazy come Haskell).

**Stato 2025:** Research language stabile ma non production-ready. Koka influenza enormemente OCaml 5.0 (che ha introdotto effect handlers) e la ricerca sui linguaggi in generale. E il laboratorio dove le idee sugli effetti vengono validate.

---

### 2.8 Gleam, Effekt e il campo degli effect systems

**Effekt:** Linguaggio di ricerca con effect system puro. Alternativa a Koka nella ricerca accademica. Usato per studiare come gli effect handler si compongono.

**Granule:** Linguaggio di ricerca con graded modal types. Cattura informazioni fine-grained su side effects, data use, privacy levels, cost, permissions via tipi modali graduati. Paper CSL 2025: "A Mixed Linear and Graded Logic: Proofs, Terms, and Models".

**OCaml 5.0:** NON un linguaggio nuovo, ma ha aggiunto effect handlers in produzione. Questo porta le idee di Koka/Effekt nel mainstream funzionale con una community enorme.

---

## PARTE 3: AI + FORMAL METHODS - IL CAMPO CHE STA ESPLODENDO

### 3.1 La Convergenza AI+Verifica

**Il problema che tutti vedono (2025):** I LLM generano codice a velocita industriale. Ma:
- ~40% dei suggerimenti di Copilot contengono vulnerabilita di sicurezza in certi contesti (studio NYU)
- Errori semantici/logici: condizioni mancanti, logica incorretta
- Errori di sicurezza: riflettono le vulnerabilita del training data
- Allucinazioni: librerie inesistenti, API non esistenti
- Il codice "funziona" ma e inefficiente o insicuro

**La soluzione emergente:** LLM per generare il codice, proof assistant per VERIFICARE. Cosi puoi:
1. Generare veloce con AI
2. Verificare formalmente la correttezza
3. Saltare la code review umana (il "collo di bottiglia" in team grandi)

**Martin Kleppmann (Dic 2025) - Tre forze che convergono:**
1. La verifica formale sta diventando MOLTO piu economica (AI la aiuta)
2. Il codice AI-generato HA BISOGNO di verifica (non puoi fare code review di 10.000 LOC/giorno)
3. La natura probabilistica degli LLM + la precisione della verifica formale = complementari perfetti

Previsione: "Il fattore limitante non sara la tecnologia, ma il cambiamento culturale per realizzare che i formal methods sono diventati praticamente viabili."

---

### 3.2 Vericoding vs Vibecoding

Il termine "**vericoding**" (contrapposto a "**vibecoding**") e stato coniato in un paper Settembre 2025:
- **Vibecoding:** LLM genera codice da descrizione naturale. Potenzialmente buggy.
- **Vericoding:** LLM genera codice FORMALMENTE VERIFICATO da specifiche formali.

**Il benchmark principale (2025) - 12.504 specifiche formali:**
- 3.029 in Dafny
- 2.334 in Verus/Rust
- 7.141 in Lean

**Tassi di successo attuali con LLM off-the-shelf:**
- **Dafny: 82%** (il piu alto - perche Dafny usa tipi matematici uniformi)
- **Verus/Rust: 44%** (piu basso - distingue ghost types da native Rust types, gestione overflow)
- **Lean: 27%** (piu basso - il piu rigoroso matematicamente)

**Trend:** LLM progress su pure Dafny verification: da 68% a 96% in un anno. Velocita di miglioramento impressionante.

**Presentato a:** POPL 2026 (Dafny 2026 workshop). Segnale che il campo e ora abbastanza maturo per conferenze top.

---

### 3.3 LeanDojo e AI-Assisted Theorem Proving

**LeanDojo (Caltech, 2023-2025):**
- Framework open-source per AI-assisted theorem proving in Lean 4
- Dataset: 98.734 teoremi/prove e 217.776 tattiche da mathlib
- LeanDojo Benchmark 4: 122.517 teoremi/prove da mathlib4
- **LeanCopilot:** LLM come copilot per theorem proving. Tactic suggestion real-time, premise selection, automated proof search. Accettato a NeuS 2025.
- **LeanDojo-v2 (NeurIPS 2025):** Framework completo con repository tracing, lifelong dataset management, retrieval-augmented agents, Hugging Face fine-tuning, external inference APIs.
- **LeanAgent (ICLR 2025):** Lifelong Learning per formal theorem proving.

**Come funziona LeanCopilot:**
1. Apri Lean 4 nell'editor
2. Sei bloccato su una tattica/prova
3. LeanCopilot suggerisce tattiche in tempo reale
4. Puoi fare premise retrieval: "trovami teoremi simili in mathlib"
5. Proof search automatica per sotto-goal

**GPT-f (OpenAI):** Approccio alternativo: fine-tuning di GPT su dataset di prove formali. LeanDojo usa retrieval-augmented generation. Risultati comparabili.

---

### 3.4 Dafny: il Proof Assistant per Programmatori

**Cos'e:** Linguaggio di verifica sviluppato da Rustan Leino (Microsoft Research). Verifica automatica tramite **SMT solver (Z3)** - non richiede prova manuale. Scrivi il codice + le precondizioni/postcondizioni (contratti), Z3 verifica automaticamente.

**Perche Dafny eccelle nel vericoding (82%):**
- Sintassi vicina ai linguaggi mainstream (C#/Java-like)
- Verifica automatica: non devi scrivere prove, solo specifiche
- Z3 fa il lavoro pesante automaticamente
- Tipi matematici uniformi: piu facile per LLM ragionare su di essi

**Verus:** Alternativa Dafny-style per Rust. In produzione in Amazon (per verificare codice Rust-based AWS). Complessita piu alta: Rust native types + ghost types = piu cose da gestire.

---

### 3.5 Cosa Generano Bene i LLM (e Cosa No)

**Generano BENE:**
- Pattern riconoscibili (CRUD, REST API, sorting, data structures standard)
- Codice con molti esempi nel training data
- Boilerplate e scaffolding
- Conversioni tra linguaggi per codice semplice
- Test unitari per funzioni con signature chiara

**Generano MALE:**
- Algoritmi avanzati (non sono "aware" delle ottimizzazioni implementative)
- Codice di sicurezza critico (riflettono le vulnerabilita del training data)
- Logica di business complessa con molti casi edge
- Codice concorrente (race conditions invisibili al modello)
- Proprietà non-funzionali (performance, sicurezza, memory safety)
- Codice per librerie rare o private (allucinano API)

**Perche (risposta tecnica):**
1. I LLM sono **pattern matchers** su sequenze di token. Non "ragionano" nel senso formale.
2. Il codice corretto e il codice sbagliato hanno distribuzioni simili nel training data.
3. Nessun meccanismo interno per **verificare** che l'output sia logicamente consistente.
4. Gli errori semantici (logica sbagliata) sono spesso sintatticamente validi - il modello non li "vede".

---

## PARTE 4: CONCETTI CHIAVE - GUIDA TECNICA

### 4.1 Dependent Types

**Cosa sono:** Tipi che DIPENDONO da valori. Esempio classico:
```
Vec : (A : Type) -> (n : Nat) -> Type
-- Vec A n e un vettore di A con ESATTAMENTE n elementi
```
Il tipo `Vec String 5` e diverso dal tipo `Vec String 6`. Il compilatore sa a compile time quanti elementi ha un vettore.

**Perche sono potenti:** Puoi codificare invarianti di programma NEL TIPO. Funzioni come `head` (primo elemento di lista) possono avere tipo:
```
head : Vec A (n+1) -> A  -- garantisce lista non vuota a compile time
```
Nessun runtime error "lista vuota". L'errore e impossibile per costruzione.

**Perche sono difficili:**
1. **Type checking indecidibile in generale**: Scala di complessita. I tipi dipendenti puri rendono il type checking equivalente alla dimostrazione di teoremi arbitrari.
2. **Universi**: Devi gestire la gerarchia Type : Type1 : Type2... per evitare paradossi (Girard/Burali-Forti).
3. **Impasse della produttivita**: Scrivere il codice E la prova contemporaneamente. Molto piu lento.
4. **Tooling immaturo**: IDE support povero rispetto a TypeScript/Java.

---

### 4.2 Effect Systems

**Il problema:** I tipi normali non dicono nulla sugli EFFETTI. `String -> String` potrebbe fare I/O, accedere a database, lanciare eccezioni. Devi leggere l'implementazione.

**La soluzione - Effect System:** Ogni funzione dichiara nel tipo TUTTI gli effetti:
```koka
fun read-file(path: string): <filesystem, exn> string
fun log(msg: string): <console> ()
fun pure-computation(x: int): int  -- zero effetti
```

**Algebraic effects e handlers:** La parte rivoluzionaria. Gli effetti non sono blackbox - puoi GESTIRLI:
```koka
with handler { return(x) { x }; read-line() { "mocked-input" } }
  // Questo codice che usa read-line ora usa il mock
```
Questo permette testing senza mocking libraries, async/await come libreria utente, etc.

**Implementazioni mature:** Koka (Microsoft Research), Effekt (ricerca), OCaml 5.0 (production).

---

### 4.3 Linear Types

**Il concetto:** Un valore di tipo lineare deve essere usato ESATTAMENTE una volta. Piu potente del borrow checker di Rust (che e un caso speciale di linear types).

**In Idris 2 (QTT):**
- Quantita 0: usato solo nelle prove, cancellato a runtime
- Quantita 1: usato esattamente una volta (lineare)
- Unrestricted: classico

**Applicazioni:**
- File handles: forza la chiusura esplicita
- Network connections: forza il cleanup
- Memory: alternativa al GC per certi pattern
- Session types: garantisce che i protocolli siano seguiti

**Differenza da Rust:** Il borrow checker di Rust e un sistema lineare applicato alla memoria. I linear types generalizzano questo a QUALSIASI risorsa.

---

### 4.4 Refinement Types

**Cosa sono:** Tipi "raffinati" con predicati logici. Esempio in LiquidHaskell:
```haskell
{-@ type Pos = {v:Int | 0 < v} @-}
{-@ divide :: Int -> Pos -> Int @-}
divide :: Int -> Int -> Int
divide x y = x `div` y
```
Il tipo `Pos` e "intero positivo". Il compilatore usa un SMT solver (Z3) per VERIFICARE automaticamente che `y` sia sempre positivo prima di chiamare `divide`.

**LiquidHaskell:** Implementazione matura. Verificato 10.000+ linee di librerie Haskell popolari (containers, bytestring, text, vector-algorithms, xmonad).

**Vantaggi vs dependent types:** Verifica AUTOMATICA (SMT, non prova manuale). Molto piu accessibile.

**Limiti:** I predicati devono essere nella "decidable fragment" degli SMT solver. Non puoi verificare proprieta arbitrarie.

---

### 4.5 Session Types

**Cosa sono:** Tipi che descrivono il PROTOCOLLO di comunicazione tra processi. Esempio:
```
ServerProtocol = !Request . ?Response . End
ClientProtocol = ?Request . !Response . End
```
Il type checker verifica che client e server si "parlino" correttamente. Se il client manda due request senza aspettare la response, errore a compile time.

**Basati su Linear Logic:** I session types sono derivati dalla Curry-Howard corrispondenza con la logica lineare (Caires, Pfenning, 2010). Un canale di comunicazione e una "risorsa lineare" - deve essere usato seguendo il protocollo esatto.

**Ricerca 2025:** Dipendent session types (TLLC): combinano session types con dependent types per specificare proprieta dei messaggi scambiati. "Dependent session types facilitate relational verification by relating concurrent programs with their idealized sequential counterparts."

**Granule (2025):** Graded modal types per catturare privacy levels, cost, permissions - estensione dei session types.

**Stato:** Principalmente accademico. Pochi linguaggi production con session types puri. Gli actor model (Erlang/Gleam) sono piu semplici ma meno precisi.

---

## PARTE 5: COSA HA FALLITO E PERCHE

### 5.1 COBOL: Il Mito del "Codice come Inglese"

**La promessa (1959):** Grace Hopper voleva che i business manager potessero scrivere programmi in "English-like" syntax. Nessun programmatore necessario.

**Perche ha fallito come NLP:**
- COBOL ha ~1000 parole riservate. Le lingue naturali ne hanno 100.000+.
- La grammatica di COBOL e rigida. Il linguaggio naturale e ambiguo.
- "English-like" != "English". I manager ancora non capivano il codice.
- Non risolveva il problema dell'ASTRAZIONE, solo della SINTASSI.

**La lezione:** Rendere la sintassi simile all'inglese non abbassa la barriera cognitiva fondamentale. Il problema non e la FORMA del linguaggio, e il MODELLO COMPUTAZIONALE sottostante.

**COBOL oggi (2026):** Ironia: COBOL non e morto. Gira su 250 miliardi di dollari di transazioni finanziarie giornaliere. Ma come linguaggio "naturale", ha fallito completamente.

---

### 5.2 Prolog: Il Paradosso della Logica

**La promessa (1972):** Alain Colmerauer e Robert Kowalski - programmare in logica del primo ordine. Dichiara COSA vuoi, il motore deduttivo trova COME ottenerlo. Nato da un progetto di natural language processing.

**Perche ha fallito nel mainstream:**
1. **Problema cognitivo principale:** Il programmatore non capisce cosa sta facendo il motore di ricerca in ogni momento. Il backtracking e opaco.
2. **Order sensitivity:** L'ordine in cui scrivi le clausole cambia l'esecuzione e la raggiungibilita. Non e "puramente dichiarativo".
3. **Cut (!):** L'operatore cut introduce controllo imperativo nell'inferno. Peggio del goto per la comprensibilita.
4. **Scalabilita:** La ricerca esaustiva scala male. Ottimizzazioni (tabling, constraint propagation) richiedono expertise profonda.
5. **Mismatch architetturale:** L'architettura Von Neumann e imperativa. La JVM, il CPU, tutto e imperativo. Il paradigma dichiarativo combatte il substrate.

**Dove sopravvive:** Constraint Logic Programming (ECLiPSe, SWI-Prolog con CLP), Answer Set Programming (Clingo), linguaggi di query (Datalog in DATOMIC, Souffle in program analysis).

**La lezione:** La dichiarativita pura (specifica il COSA, non il COME) e desiderabile ma il COME non puo essere completamente nascosto. Il programmatore deve capire il modello computazionale, anche se astratto.

---

### 5.3 Haskell: 30 Anni di Nicciosita

**La promessa (1990):** Linguaggio funzionale puro "by committee". Lazy evaluation, monadi per effetti, type classes, type inference. Il linguaggio "accademicamente corretto".

**Perche non ha sfondato nonostante 30 anni:**

1. **Lazy evaluation e il performance model opaco:**
   - Non sai quando il codice viene eseguito. Space leaks invisibili.
   - Il profiling e difficile: dove viene allocato cosa?
   - Mentalmente costoso da ragionare.

2. **Monadi: giusta astrazione, barriera sbagliata:**
   - Le monadi sono la soluzione CORRETTA per gli effetti.
   - Ma spiegare perche `IO ()` non e `Maybe (IO ())` richiede teoria delle categorie.
   - Il "tutorial sulla monade" e un meme - tutti lo scrivono, nessuno lo capisce al primo colpo.

3. **Dependent types via workaround:**
   - DataKinds, GADTs, TypeFamilies, PolyKinds, singletons = codice irragionevole.
   - Haskell ha dependent types "emulati" con una complessita accidentale enorme.
   - Dependent Haskell roadmap (GHC): in corso da 10+ anni, non arriva mai.

4. **Tooling storicamente povero:**
   - Cabal vs Stack: anni di guerra degli strumenti.
   - Build times: GHC e famosamente lento per grandi codebase.
   - IDE support: migliorato con HLS ma non ai livelli di IntelliJ.

5. **Il paradosso della purezza:**
   - Haskell e il linguaggio piu puro. Per ogni cosa con effetti reali, devi "sporcarti" con IO monads, STM, etc.
   - I programmatori vogliono purezza come proprieta, non come religion.

**Dove Haskell ha VINTO:**
- Parsing (Parsec, Attoparsec): usato in produzione da molte aziende.
- Compilers come esempio (GHC stesso e scritto in Haskell).
- Finance (Jane Street usa OCaml, ma Haskell e popolare nei quant funds).
- Il design di Lean 4, Idris 2, Agda sono tutti influenzati da Haskell.

**La lezione:** La purezza teorica non basta. Serve ergonomia, tooling, error messages umani, performance prevedibile. Roc, Gleam, Elm hanno imparato da Haskell.

---

### 5.4 Proof Assistants: Il Problema dell'Ultimo Miglio

**Perche non sono mainstream (2025 - analisi consolidata):**

**Barriera 1 - Competenze:** Scrivere prove richiede formazione PhD-level in logica matematica. Non e insegnato nei corsi di informatica standard.

**Barriera 2 - Costo-beneficio:** Per la maggior parte dei software, `costo_bug_atteso < costo_verifica_formale`. Solo per safety-critical (aerospazio, nucleare, crittografia) il rapporto si inverte.

**Barriera 3 - Tool:** I proof assistant hanno storicamente UI terribili. Emacs-based, nessun debugging visual, error messages criptici.

**Barriera 4 - Mismatch cognitivo:** Il proof engineering richiede un mindset diverso dal software engineering normale. Non e solo "imparare un linguaggio" - e cambiare come pensi alla correttezza.

**Barriera 5 - "Ultimo miglio":** Anche se provi correttezza in Lean, come colleghi a runtime Python o a sistema distribuito non verificato? Il confine formale/informale richiede ponti manuali fragili.

**Cosa sta cambiando (2025-2026):**
- AI abbassa il costo della scrittura delle prove (LeanCopilot, DeepSeek-Prover)
- Il vericoding automatizza la generazione di codice verificato
- Dafny 82% successo: per certi domini, quasi automatico
- Harmonic AI dimostra che il modello business "AI + verifica formale" e finanziabile ($1.45B valuation)

---

## PARTE 6: I GAP - COSA NESSUNO STA ANCORA FACENDO

### Gap 1: Verifica Formale per Sistemi Distribuiti Reali

**Il problema:** Tutti i formal methods funzionano bene per algoritmi sequenziali. Ma i sistemi moderni sono distribuiti, concorrenti, con network failures e Byzantine faults. Verificare proprieta di liveness e safety di un sistema Kubernetes + microservizi + message queue in Lean? Non esiste ancora un framework pratico.

**Chi ci prova:** Session types, CSP/TLA+ (AWS usa TLA+ internamente), ma nessun mainstream adoption.

**L'opportunita:** Il linguaggio/framework che permette di verificare sistemi distribuiti REALI con effort ragionevole sara enorme.

---

### Gap 2: Ponte AI-Generato -> Codice Formalmente Specificato

**Il problema attuale:** I LLM generano codice. I proof assistant verificano codice con specifiche formali. Ma chi scrive le specifiche formali? Se le specifiche le deve scrivere un umano PhD, sei tornato al punto di partenza.

**Lo stato dell'arte:** "Transforming Natural Language into Formal Specifications" (ASE AgenticSE 2025) - ricerca attiva ma risultati preliminari. Il vericoding richiede ancora specifiche formali scritte da umani.

**Il gap reale:** Natural Language -> Formal Specification (automatica) -> Code Generation -> Formal Verification. Solo il primo step (NL -> spec formale) manca di soluzioni robuste.

---

### Gap 3: Linguaggi per Reasoning Verificato (il layer tra LLM e hardware)

**La visione di Rafa materializzata:** Oggi abbiamo LLM che generano testo/codice, e proof assistant che verificano codice. Ma nessun linguaggio e progettato specificamente per:
- Essere generato facilmente dai LLM (struttura regolare, semantica chiara)
- Essere verificato automaticamente (subset decidibile del type system)
- Eseguire efficientemente su hardware moderno
- Permettere di esprimere INTENTO non solo implementazione

Dafny ci si avvicina (82% vericoding success). Ma e ancora un linguaggio progettato per umani che lo scrivono a mano.

---

### Gap 4: Verifica Incrementale per Codebases Esistenti

**Il problema:** Le prove di correttezza funzionano per codice nuovo scritto con la verifica in mente. Ma hai milioni di LOC legacy in Python/Java/C++. Come aggiungi garanzie formali incrementalmente?

**Chi ci prova:** LiquidHaskell (per Haskell), Verus/Rust (per Rust), Dafny annotations possono essere aggiunte gradualmente. Ma per Python/JavaScript/C++? Quasi niente di pratico.

---

### Gap 5: Linguaggi per AI Agents (non per AI MODEL development)

**Il gap distinzione:** Esistono linguaggi per sviluppare modelli AI (Mojo, CUDA, Triton). Esistono linguaggi per math/proof (Lean, Agda). Ma nessun linguaggio e progettato per descrivere e verificare il COMPORTAMENTO degli agenti AI:
- Orchestrazione di task con garanzie di terminazione
- Comunicazione tra agenti con session types
- Memory e state management con proprietà di correttezza

Oggi: YAML, JSON, Python con frameworks adhoc (LangChain, CrewAI). Zero verifica formale.

---

## PARTE 7: TENDENZE - DOVE STA ANDANDO IL CAMPO

### Tendenza 1: Lean 4 come "Lingua Franca" della Verifica AI

In 6-18 mesi, Lean 4 potrebbe diventare l'infrastruttura standard per la verifica AI, come TensorFlow/PyTorch per il ML. AlphaProof (Google), Harmonic AI, DeepSeek-Prover, LeanDojo convergono tutti su Lean 4. Chi controlla l'ecosistema Lean controlla il layer di verifica.

### Tendenza 2: Vericoding vs Vibecoding come Dicotomia di Mercato

Le due pratiche si separeranno per mercato:
- **Vibecoding:** prototipazione rapida, startup early-stage, codice non critico
- **Vericoding:** safety-critical (automotive, aerospace, medical), finance, crittografia, AI systems

Il mercato del vericoding tooling e ancora quasi vuoto.

### Tendenza 3: SMT Solver come Commodity

Z3, CVC5, Bitwuzla: sempre piu potenti, sempre piu accessibili. Questo abbassa il costo di TUTTI i sistemi basati su refinement types e verifica automatica (Dafny, LiquidHaskell, Verus). La curva di apprendimento dei proof assistant espliciti (Lean, Coq) rimane alta, ma la verifica AUTOMATICA diventa accessibile.

### Tendenza 4: Effect Systems nel Mainstream

OCaml 5.0 ha portato gli effect handler in un linguaggio con milioni di righe di codice production. Se questo funziona a scala, aspettati che altri linguaggi adottino il pattern. Swift actors, Kotlin coroutines, Rust async: tutti si avvicinano agli effect system senza usare il termine.

### Tendenza 5: Il "Formal Methods Stack" per AI Safety

Sta emergendo un nuovo stack:
1. **Specifica** (Catala, TLA+, o NL-to-formal AI)
2. **Generazione** (LLM con contesto formale)
3. **Verifica** (Lean 4, Dafny, F*)
4. **Deployment** (con garanzie preservate)

Ancora nessun player domina tutto lo stack. Opportunita enorme.

### Tendenza 6: Linguaggi "piccoli" vincono in nicchie specifiche

Gleam (BEAM type-safe), Zig (systems/embedded), Roc (functional apps), Gleam (concurrent web): nessuno diventa mainstream globale, ma ciascuno domina la propria nicchia. L'era del linguaggio "tutto per tutti" e finita. L'AI genera comunque il codice in qualunque linguaggio - quindi la nicchia ottimale per il task specifico vince.

---

## SINTESI E RACCOMANDAZIONE

### I 5 Insight Chiave per CervellaSwarm

1. **Il timing e perfetto:** La convergenza AI+formal methods sta avvenendo ORA (2025-2026). Non tra 10 anni. Harmonic AI e gia un unicorn su questo tema. Il momento di posizionarsi e adesso.

2. **Lean 4 e il cavallo su cui puntare:** Non Coq (troppo vecchio), non Agda (troppo accademico), non F* (troppo niccioso). Lean 4 ha il momentum, i fondi, la community e l'ecosistema AI giusto.

3. **Vericoding e il gap di mercato:** 82% di successo in Dafny con LLM off-the-shelf. Ma nessun prodotto consumer/enterprise su questo tema. Un "vericoding IDE" o "vericoding assistant" potrebbe essere un prodotto.

4. **Gli effetti (Koka-style) sono il futuro del tipo system:** I type system senza effect tracking sono come SQL senza transazioni - funziona ma manca la proprieta fondamentale di correttezza. OCaml 5 ha validato il concept in produzione.

5. **Nessuno sta risolvendo il Gap 5** (linguaggi per AI agents verificati). Questo e l'opportunita piu ampia e piu vicina al core business di CervellaSwarm.

### Raccomandazione Finale

Se CervellaSwarm vuole posizionarsi all'intersezione AI+formal methods:

**Short term (6-12 mesi):** Integrare Lean 4 come tool di verifica nel workflow. Studiare Dafny per vericoding. Monitorare LeanCopilot per possibile integrazione.

**Medium term (1-2 anni):** Esplorare un layer di specificazione formale per gli agenti CervellaSwarm. Session types per i protocolli di comunicazione inter-agente. Refinement types per gli invarianti del sistema.

**Long term (2-3 anni):** Se il Gap 5 non viene risolto da nessun altro player, questo potrebbe essere IL differenziatore: un framework per agenti AI con garanzie formali di correttezza del comportamento.

---

## FONTI PRINCIPALI

- [Lean 4 Theorem Prover - Microsoft Research](https://www.microsoft.com/en-us/research/publication/the-lean-4-theorem-prover-and-programming-language/)
- [Lean Together 2026](https://leanprover-community.github.io/lt2026/)
- [Lean4: The New Competitive Edge in AI - VentureBeat](https://venturebeat.com/ai/lean4-how-the-theorem-prover-works-and-why-its-the-new-competitive-edge-in)
- [Mathlib4 GitHub](https://github.com/leanprover-community/mathlib4)
- [AlphaProof - Google DeepMind IMO Silver Medal](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/)
- [Gemini Deep Think IMO Gold Medal 2025](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)
- [Harmonic AI $120M Series C - BusinessWire](https://www.businesswire.com/news/home/20251125727962/en/Harmonic-Builds-Momentum-Towards-Mathematical-Superintelligence-with-$120-Million-Series-C)
- [DeepSeek-Prover-V2 - ArXiv](https://arxiv.org/abs/2504.21801)
- [LeanDojo](https://leandojo.org/)
- [LeanCopilot](https://leandojo.org/leancopilot.html)
- [Prediction: AI will make formal verification go mainstream - Martin Kleppmann](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html)
- [A Benchmark for Vericoding - ArXiv](https://arxiv.org/abs/2509.22908)
- [Vericoding POPL 2026](https://popl26.sigplan.org/details/dafny-2026-papers/13/A-benchmark-for-vericoding-formally-verified-program-synthesis)
- [Towards Formal Verification of LLM-Generated Code - ArXiv](https://arxiv.org/abs/2507.13290)
- [Mojo - Modular](https://www.modular.com/mojo)
- [Chris Lattner - Modular 2025](https://www.latent.space/p/modular-2025)
- [Gleam Programming Language](https://gleam.run/)
- [Gleam - Stack Overflow Dev Survey 2025](https://alltechprojects.com/gleam-programming-language-introduction-2025/)
- [Unison 1.0](https://www.unison-lang.org/docs/the-big-idea/)
- [Project Everest - Microsoft Research](https://www.microsoft.com/en-us/research/project/project-everest-verified-secure-implementations-https-ecosystem/)
- [F* Language](https://fstar-lang.org/)
- [Koka Programming Language](https://koka-lang.github.io/koka/doc/book.html)
- [Koka v3.2.0 - GitHub](https://github.com/koka-lang/koka)
- [Catala - INRIA](https://inria.hal.science/hal-03159939)
- [Idris 2: QTT in Practice - ArXiv](https://arxiv.org/abs/2104.00480)
- [Rocq (formerly Coq)](https://coq.inria.fr/)
- [50 years of proof assistants](https://lawrencecpaulson.github.io//2025/12/05/History_of_Proof_Assistants.html)
- [Barriers to Formal Methods Adoption - Springer](https://link.springer.com/chapter/10.1007/978-3-642-41010-9_5)
- [Granule Project](https://granule-project.github.io/)
- [Zig Language](https://ziglang.org/)
- [Bun JavaScript Runtime](https://bun.sh/)
- [Roc Language](https://www.roc-lang.org/)
- [Security Weaknesses of Copilot-Generated Code - ArXiv](https://arxiv.org/pdf/2310.02059)
- [LLM Code Generation Quality - Sonar](https://www.sonarsource.com/resources/library/llm-code-generation/)
- [Transforming NL to Formal Specifications - ASE AgenticSE 2025](https://conf.researchr.org/details/ase-2025/agenticse-2025-papers/6/Transforming-Natural-Language-into-Formal-Specifications)

---

*COSTITUZIONE-APPLIED: SI*
*Principio usato: "Nulla e complesso - solo non ancora studiato!"*
*Report: 42 fonti consultate, ~8500 parole, copertura completa di tutti i temi richiesti.*
