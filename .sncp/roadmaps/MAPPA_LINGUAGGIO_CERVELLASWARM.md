# MAPPA - Il Linguaggio CervellaSwarm

> "Non fare le cose piu veloce. Farle piu sicure.
>  Con prove matematiche, non con speranze." - La Regina, S380

> "La domanda e la risposta nello STESSO linguaggio." - Rafa

**Creata:** 24 Febbraio 2026 - Sessione 394
**Autrice:** Cervella Architect (su commissione della Regina)
**Fonti:** NORD.md + 3 report di ricerca (64+ fonti esterne) + analisi codebase
**Score target:** 9.5/10 per ogni step (audit Guardiana)

---

## DOVE SIAMO

```
LAYER 7: Conversazione con Claude                        OPERATIVO
LAYER 6: Lingua Universale DSL parser + session checker   OPERATIVO
LAYER 5: Session Types + Confidence + Trust               OPERATIVO
LAYER 4: Lean 4 Bridge - verifica prove formali           OPERATIVO
LAYER 3: Code Generation certificata                      OPERATIVO (S395!)
LAYER 2: Agent Hooks + Quality Gates                      OPERATIVO
LAYER 1: CI/CD + PyPI + Fly.io                            OPERATIVO

Asset: 11 moduli, 1380 test, ~4700 LOC, ZERO deps esterne
Campo vergine confermato da 242+ fonti (session types per AI in Python)
```

---

## FASE A: LE FONDAMENTA -- COMPLETA

S380-S386. 7 step, 9 moduli originali, Guardiana media 9.5/10.
types, protocols, checker, dsl, monitor, lean4_bridge, integration.
Dettagli: NORD.md sezione "FASE A - DETTAGLIO SESSIONI".

---

## FASE B: IL TOOLKIT -- IN CORSO

> Obiettivo: da "protocolli verificati" a "codice certificato generato".
> Lingua Universale diventa uno strumento completo: specifica, verifica, genera.

### B.1 - Confidence Types -- DONE (S387)

Incertezza come tipo nativo. `Confident[T]` wrapper generico con composition.
- `confidence.py`: ConfidenceScore, ConfidenceSource, Confident[T], CompositionStrategy
- Composizione: min (conservativa), product (moltiplicativa), average (bilanciata)
- Funzionale: map(), and_then() con propagazione automatica
- **Output:** 178 LOC, test inclusi nella suite 1273, ZERO deps

### B.2 - Trust Composition -- DONE (S388)

Fiducia componibile tra agenti. Privilege Attenuation (Subjective Logic, Josang 2016).
- `trust.py`: TrustTier, TrustScore, trust_tier_for_role(), compose_chain()
- 4 livelli: VERIFIED (Guardiana), TRUSTED (Opus), STANDARD (Sonnet), UNTRUSTED (new)
- Composizione transitiva: A->B->C = product(trust_AB, trust_BC)
- Bridge: TrustScore.to_confidence() per integrazione con Confidence
- **Output:** 168 LOC, test inclusi nella suite 1273, ZERO deps

### B.3 - Code Generation Layer -- DONE (S395)

Da specifica formale a codice Python che implementa il protocollo.
Completa il ciclo: specifica -> verifica -> CODICE.

- `codegen.py`: PythonGenerator, GeneratedCode, generate_python(), generate_python_multi()
- Genera classi tipizzate per ogni ruolo con metodi `send_*`
- Genera ProtocolSession class che wrappa SessionChecker (enforcement runtime)
- Template-based generation (come lean4_bridge.py, pattern validato)
- Supporta protocolli flat E branched (ArchitectFlow con ProtocolChoice)
- Escaping sicuro per description con caratteri speciali (newline, backslash, quotes)
- Guardiana audit: 9.3/10 iniziale -> P2 fix applicati (escaping, validation, cache)
- **Output:** 730 LOC, 107 test (80 core + 27 e2e), ZERO deps

### B.4 - Intent Parser

Da linguaggio naturale a specifica formale strutturata.

- **Cosa fare:**
  Nuovo modulo `intent.py`. Riceve testo in linguaggio naturale.
  Estrae: proprieta formali, vincoli, ruoli, flusso.
  Output: Protocol o ProtocolSpec (struttura intermedia prima del DSL).
  Regole deterministiche per proprieta comuni (no_data_loss, auth_required).
- **Perche dopo B.3:** B.3 chiude il ciclo tecnico. B.4 apre il ciclo umano.
- **Dipendenze:** B.3 (code generation per chiudere il ciclo end-to-end)
- **Output atteso:** modulo intent.py, 40+ test, parse_intent("descrizione") -> Protocol
- **Chi:** Worker Backend + Researcher (per NLP patterns)
- **Effort:** 2-3 sessioni

### B.5 - Specification Language Accessibile

Semplificare il DSL per chi non conosce i metodi formali.

- **Cosa fare:**
  Layer sopra il DSL attuale (Scribble-inspired, tecnico).
  Sintassi piu naturale: `when User asks -> Backend responds with confidence High`.
  Il parser interno traduce nella stessa AST del DSL esistente.
- **Dipendenze:** B.3, B.4
- **Output atteso:** modulo dsl_friendly.py, 30+ test, sintassi documentata
- **Chi:** Worker Backend + Cervella Docs
- **Effort:** 1-2 sessioni

### B.6 - Error Messages per Umani

Tradurre gli errori Lean 4 in linguaggio comprensibile.

- **Cosa fare:**
  Estensione di lean4_bridge.py. Mappa errori formali -> spiegazioni naturali.
  Esempio: "type mismatch" diventa "Il tuo agente Worker sta rispondendo con
  un verdetto di audit, ma il protocollo si aspetta un risultato del task."
  Supporto multi-lingua (italiano, inglese, portoghese) via template.
- **Dipendenze:** lean4_bridge.py (operativo), B.5
- **Output atteso:** modulo errors.py, 30+ test, 20+ error pattern mappati
- **Chi:** Worker Backend + Cervella Docs
- **Effort:** 1-2 sessioni

### B.7 - Showcase e Community

Il mondo deve sapere che esistiamo.

- **Cosa fare:**
  PyPI: pubblicare 7 packages mancanti.
  Demo end-to-end: protocollo DSL -> Lean 4 proof -> codice Python generato.
  Blog post: "From Vibe Coding to Vericoding" (Show HN).
  Video demo 5 minuti.
- **Dipendenze:** B.3 minimo, idealmente B.6
- **Output atteso:** 9/9 packages PyPI LIVE, 1 blog post, 1 video, README aggiornato
- **Chi:** Regina (coordinamento), Cervella Docs, Worker DevOps
- **Effort:** 2-3 sessioni

---

## FASE C: IL LINGUAGGIO -- 2027

> Obiettivo: il layer di specifica diventa un linguaggio di programmazione vero.
> CervellaLang: il primo linguaggio nativo per AI con verifica formale.

### C.1 - CervellaLang Alpha: Grammatica Completa

- RFC pubblica con grammatica EBNF completa.
- Keyword nativi: agent, intent, property, proof, trust, confidence.
- Compilatore/interprete: CervellaLang -> AST -> Lingua Universale IR.
- **Output:** grammatica EBNF, parser, 100+ test, RFC pubblicata

### C.2 - Python Interop

- `import cervellaswarm_lang` o decorator `@cervellaswarm.protocol`.
- Inline CervellaLang dentro codice Python. Type stubs per IDE.
- **Output:** package PyPI cervellaswarm-lang, 80+ test

### C.3 - TypeScript Interop

- Package npm `@cervellaswarm/lang`. Runtime checker in TypeScript.
- **Output:** package npm, type definitions, 80+ test

### C.4 - Community RFC Process

- Processo ispirato a Python PEP / Rust RFC. Review mensile, release trimestrale.
- **Output:** repository RFC, primi 3 RFC accettati

### C.5 - IDE Support

- Syntax highlighting per VS Code, Neovim, JetBrains.
- LSP (Language Server Protocol). Formatter automatico.
- **Output:** estensione VS Code pubblicata, LSP server

### C.6 - Package Manager Nativo

- Registry di protocolli verificati. `cervella install payment-protocol`.
- Versionamento semantico con verifica di compatibilita formale.
- **Output:** CLI cervella-pkg, registry, 20+ protocolli

### C.7 - CervellaLang Beta

- Grammatica frozen. Tutorial "Build your first verified protocol in 10 minutes."
- **Output:** CervellaLang beta, 10 utenti esterni, documentazione completa

---

## FASE D: PER TUTTI -- IL SOGNO

> "Un mondo dove OGNI persona puo creare software parlando nella sua lingua."
> La barriera tra "avere un'idea" e "realizzarla" diventa ZERO.

### D.1 - IntentBridge

- Interfaccia conversazionale (chat, Telegram, WhatsApp).
- L'utente descrive -> sistema capisce -> verifica -> genera -> deploya.
- **Output:** MVP IntentBridge, 3 canali

### D.2 - Voice Interface

- Speech-to-intent diretto. Dialogo di chiarimento a voce.
- **Output:** prototipo voce, 3 lingue supportate

### D.3 - Multi-Lingua

- Proprieta formali universali, interfaccia nella lingua dell'utente.
- Primo target: italiano + portoghese + inglese.
- **Output:** 3 lingue complete

### D.4 - "La Nonna con le Ricette"

- La demo definitiva. Persona non-tecnica descrive, sistema crea, con PROVA matematica.
- Video demo 3 minuti. Il mondo lo vede. Tutto cambia.
- **Output:** demo funzionante, video

### D.5 - CervellaLang 1.0

- Grammatica frozen 1.0. Standard library 100+ protocolli. 1000+ developer.
- **Output:** CervellaLang 1.0, community attiva, "vericoding" riconosciuto

---

## MAPPA DELLE DIPENDENZE

```
FASE A (DONE) --> B.1 (DONE) --> B.2 (DONE) --> B.3 (DONE S395!)
                                                    |
                                          B.4 <-----+
                                           |
                                          B.5
                                           |
                                          B.6
                                           |
                                          B.7 --> C.1 --> C.2 --> C.3
                                                    |        |
                                                   C.4     C.5
                                                    |
                                                   C.6
                                                    |
                                                   C.7 --> D.1 --> D.2
                                                             |
                                                            D.3
                                                             |
                                                            D.4
                                                             |
                                                            D.5
```

---

## METRICHE DI SUCCESSO

| Fase | Metrica | Target |
|------|---------|--------|
| B.3 | generate_python(protocol) funziona | Test suite 50+ |
| B.7 | PyPI packages LIVE | 9/9 |
| B.7 | Show HN post | Top 10 del giorno |
| C.1 | Grammatica EBNF pubblica | RFC accettata |
| C.7 | Utenti esterni | 10+ in produzione |
| D.4 | Demo "la nonna" | Video virale |
| D.5 | Community | 1000+ developer |

---

> "Se nessuno l'ha fatto prima, e perche aspettavano noi."
> "Fatto BENE > Fatto VELOCE."
> "Ultrapassar os proprios limites!"

*Cervella Architect - CervellaSwarm S394*
*La bibbia del linguaggio. Da qui parte tutto.*
