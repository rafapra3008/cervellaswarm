# MAPPA - Il Linguaggio CervellaSwarm

> "Non fare le cose piu veloce. Farle piu sicure.
>  Con prove matematiche, non con speranze." - La Regina, S380

> "La domanda e la risposta nello STESSO linguaggio." - Rafa

**Creata:** 24 Febbraio 2026 - Sessione 394
**Aggiornata:** 6 Marzo 2026 - Sessione 437 (FASE D COMPLETA! PyPI v0.3.0)
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

Asset: 25 moduli, 2909 test, ~12000+ LOC, ZERO deps esterne
Campo vergine confermato da 242+ fonti (session types per AI in Python)
```

---

## FASE A: LE FONDAMENTA -- COMPLETA

S380-S386. 7 step, 9 moduli originali, Guardiana media 9.5/10.
types, protocols, checker, dsl, monitor, lean4_bridge, integration.
Dettagli: NORD.md sezione "FASE A - DETTAGLIO SESSIONI".

---

## FASE B: IL TOOLKIT -- COMPLETA

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

### B.4 - Intent Parser -- DONE (S396)

Micro-linguaggio strutturato: sembra naturale, e deterministico.
Scelta architetturale: micro-linguaggio > parser NLP (insight Rafa + Architect + Ingegnera).

- `intent.py`: IntentParseResult, IntentParseError, parse_intent(), parse_intent_protocol()
- Tokenizer indent-aware + recursive descent (stesso pattern di dsl.py)
- `_ACTION_MAP`: 14 verb phrase -> MessageKind (deterministic, ZERO ambiguita)
- Supporta flat protocols E branched (`when X decides:`)
- Integrazione verificata: SessionChecker + Lean4 + CodeGen + DSL roundtrip
- Guardiana audit: 9.3/10, 6 P3 (4 fixati subito)
- Ricerca: 28 fonti (Adapt, Rasa, Req2LTL, spaCy, LUIS, etc.)
- **Output:** 649 LOC, 67 test (36 core + 31 edge), ZERO deps

### B.5 - Specification Language -- DONE (S397)

Mini-DSL per esprimere proprieta formali sui protocolli. Dual verification: statico + runtime.
Scelta architetturale: micro-DSL strutturato (come B.4) > builder/decorator/inline DSL.

- `spec.py`: SpecParseError, PropertyKind (7 tipi), PropertySpec, ProtocolSpec, PropertyReport
- Parser indent-aware + recursive descent (stesso pattern intent.py/dsl.py)
- `check_properties()`: statico contro Protocol (PROVED/VIOLATED)
- `check_session()`: runtime contro session log (SATISFIED/VIOLATED)
- 7 proprieta: always_terminates, no_deadlock, ordering, exclusion, confidence_min, trust_min, all_roles_participate
- DIFFERENZIATORE: `confidence >= high` come proprieta formale (NESSUNO al mondo lo ha!)
- Guardiana audit: 9.3/10 APPROVED, 2 P2 fixati (inner import + O(n) scan), 7 P3 (4 fixati, 3 deferred)
- Ricerca: 27 fonti (Dwyer 1999, DECLARE, TLA+, FizzBee, NL2LTL, Alloy, etc.)
- **Output:** 1242 LOC, 116 test (47 core + 43 parse + 23 session + 3 regression), ZERO deps

### B.6 - Error Messages per Umani -- DONE (S398)

Translator layer: errori tecnici -> messaggi user-friendly stile Elm/Rust.
- `errors.py`: humanize(), format_error(), render_snippet(), suggest_similar(), _SafeDict
- 72 error codes (LU-T/P/R/D/S/I/L/G/C/A/X/N), 3 locales (en, it, pt)
- Fuzzy matching via difflib.get_close_matches() (stdlib, ZERO deps)
- Guardiana 9.3/10 APPROVED, 5 bug trovati e fixati (2 Tester + 3 Guardiana)
- Ricerca: 27 fonti (Elm 2015, Rust diagnostics, miette, Alloy, FizzBee, Dafny)
- **Output:** ~2200 LOC, 293 test (257 + 36 C3.3), ZERO deps, 74 error codes (72 + LU-N013 + LU-N014)
- C3.3 (S422): +12 codici LU-N per pipeline C1 (tokenizer+parser), render_snippet() Rust-style
- C3.5 (S424): +2 codici LU-N013 (invalid trust tier) + LU-N014 (invalid confidence level)

### B.7 - Showcase e Community -- DONE (S398-S404)

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

## FASE C: IL LINGUAGGIO -- COMPLETA! (S407-S425)

> **NOTA (S425):** Fase C COMPLETATA! Piano esecutivo:
> `.sncp/roadmaps/SUBROADMAP_FASE_C_LINGUAGGIO.md` (C1 Grammatica, C2 Compilatore, C3 L'Esperienza).
> 25 moduli, 2909 test, 74 error codes, 5 file .lu, ZERO deps. Media 9.45/10.
> I sub-step C.1-C.7 sotto sono la visione originale S394; il piano esecutivo reale e nella SUBROADMAP.

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

## FASE D: L'ECOSISTEMA (rinominata da "Per Tutti", S425)

> **NOTA (S425):** Fase D ridefinita come "L'Ecosistema" dopo ricerca su come i linguaggi
> di successo crescono (46+ fonti, Python/Rust/Go/Gleam).
> Piano esecutivo: `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
> (D1 Syntax Highlighting, D2 LSP, D3 Playground, D4 Tutorial, D5 LSP Avanzato, D6 Launch)
>
> La visione "Per Tutti" (IntentBridge, voce, multi-lingua) diventa FASE E.

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
                                          B.4 (DONE S396!) <--+
                                           |
                                          B.5 (DONE S397!)
                                           |
                                          B.6 (DONE S398!)
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
