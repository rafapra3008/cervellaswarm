# MAPPA - Il Linguaggio CervellaSwarm

> "Non fare le cose piu veloce. Farle piu sicure.
>  Con prove matematiche, non con speranze." - La Regina, S380

> "La domanda e la risposta nello STESSO linguaggio." - Rafa

**Creata:** 24 Febbraio 2026 - Sessione 394
**Aggiornata:** 11 Marzo 2026 - Sessione 441 (E.4 Voice Interface DONE!)
**Autrice:** Cervella Architect (su commissione della Regina)
**Fonti:** NORD.md + 3 report di ricerca (64+ fonti esterne) + analisi codebase
**Score target:** 9.5/10 per ogni step (audit Guardiana)

---

## DOVE SIAMO

```
LAYER 8: Voce (STT locale via faster-whisper)              OPERATIVO (S441!)
LAYER 7: Conversazione con Claude                        OPERATIVO
LAYER 6: Lingua Universale DSL parser + session checker   OPERATIVO
LAYER 5: Session Types + Confidence + Trust               OPERATIVO
LAYER 4: Lean 4 Bridge - verifica prove formali           OPERATIVO
LAYER 3: Code Generation certificata                      OPERATIVO (S395!)
LAYER 2: Agent Hooks + Quality Gates                      OPERATIVO
LAYER 1: CI/CD + PyPI + Fly.io                            OPERATIVO

Asset: 28 moduli, 3312 test, ~14000+ LOC, ZERO deps esterne (anthropic [nl], faster-whisper+sounddevice [voice] optional)
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

## FASE D: L'ECOSISTEMA -- COMPLETA! (S425-S435)

> Piano esecutivo: `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
> 6 step, media 9.5/10. "Come hanno fatto i big?" - Rafa, S425.
> Fonti: 46+ (Python/Rust/Go/Gleam/Zig/Roc).

```
D1 Syntax Highlighting + VS Code Extension    DONE (S426, 9.5/10)
D2 LSP Base (lu lsp, pygls, diagnostics)       DONE (S426, 9.5/10)
D3 Playground Online (Pyodide, GitHub Pages)   DONE (S429, LIVE!)
D4 "A Tour of LU" (24 step interattivi)        DONE (S430, 9.5/10)
D5 LSP Avanzato (Hover, Completion, Go-to-def) DONE (S434, 9.5/10)
D6 Guardiana Finale + Launch                   DONE (S435, 9.5/10)
```

---

## FASE E: PER TUTTI -- IntentBridge (S438+)

> "Un mondo dove OGNI persona puo creare software parlando nella sua lingua."
> La barriera tra "avere un'idea" e "realizzarla" diventa ZERO.
> Piano esecutivo: `.sncp/roadmaps/SUBROADMAP_FASE_E_INTENTBRIDGE.md`
> Ricerca: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260306_FASE_E_INTENTBRIDGE.md` (18 fonti)

### E.1 - "La Nonna" Script

- Dialogo parola per parola della demo definitiva.
- Guida TUTTE le decisioni architetturali. Si scrive PRIMA del codice.
- **Output:** screenplay + requisiti tecnici estratti

### E.2 - IntentBridge Core (CLI chat)

- Pipeline: conversazione guidata -> B.4 intent -> spec -> check -> codegen.
- Comando CLI: `lu chat` (interactive mode).
- Multi-lingua dal giorno 1 (it/pt/en).
- Pattern two-stage validato da Req2LTL: LLM -> IR strutturato -> deterministico (88% vs 43%).
- **Output:** `_intent_bridge.py`, 100+ test, ZERO deps

### E.3 - NL Processing (LLM Integration) -- DONE (S440, 9.5/10)

- LLM (Claude) traduce NL libero -> IntentDraft strutturato via tool_use.
- Disambiguazione intelligente: se input vago, LLM chiede chiarimenti (NLClarificationNeeded).
- anthropic come optional dependency (`pip install ...[nl]`).
- 2 audit Guardiana, 13 findings tutti fixati.
- **Output:** `_nl_processor.py` (~450 LOC), 68 test, CLI `lu chat --mode nl`

### E.4 - Voice Interface -- DONE (S441, 9.5/10)

- STT locale (faster-whisper) -> NL -> pipeline IntentBridge.
- Voice-first per non-tecnici ("la nonna").
- Push-to-talk con ENTER, modello "small" default, lazy loading.
- Ricerca: 24 fonti (Whisper, Deepgram, Vosk, Claude voice, etc.)
- Guardiana: 9.5/10, 6 P3 tutti fixati.
- **Output:** `_voice.py` (~290 LOC), 70 test, CLI `lu chat --voice`, `[voice]` optional dep

### E.5 - "La Nonna" Demo Finale -- IN PROGRESS (S442)

- La demo definitiva. Persona non-tecnica descrive, sistema crea, con PROVA matematica.
- S442: 2 bug critici fixati (verifica formale era ROTTA), 2 nuove proprieta (NO_DELETION, ROLE_EXCLUSIVE), property explanations i18n
- S442: R20 violation demo DONE (Guardiana 9.5+), `lu demo` command DONE (Guardiana 9.5/10, 5 P3 fixati)
- Prossimi: video VHS, blog post, test persona non-tecnica
- **Piano dettagliato:** `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`
- **Output:** demo funzionante, video, blog post

### E.6 - CervellaLang 1.0

- Grammatica frozen 1.0. Standard library 20+ protocolli (poi 100+). Community.
- RFC grammatica, `lu init` + `lu verify`, VS Code Marketplace.
- **Piano dettagliato:** `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` (Fase 3)
- **Output:** CervellaLang 1.0, community attiva, "vericoding" riconosciuto

---

## MAPPA DELLE DIPENDENZE

```
FASE A (DONE) --> B.1-B.7 (DONE) --> C (DONE) --> D (DONE, Ecosistema)
                                                       |
                                                      E.1 (La Nonna Script)
                                                       |
                                                      E.2 (IntentBridge Core)
                                                       |
                                                      E.3 (NL Processing)
                                                       |
                                                      E.4 (Voice)
                                                       |
                                                      E.5 (La Nonna Demo)
                                                       |
                                                      E.6 (CervellaLang 1.0)
```

---

## METRICHE DI SUCCESSO

| Fase | Metrica | Target | Status |
|------|---------|--------|--------|
| B.7 | PyPI packages LIVE | 9/9 | DONE |
| B.7 | Show HN post | Top 10 del giorno | DONE (S404) |
| C | Grammatica + Compilatore + LSP | 25 moduli, 2909 test | DONE |
| D | Ecosistema (VS Code, Playground, Tour) | 6/6 step, 9.5/10 | DONE |
| E.1 | Script "La Nonna" | Screenplay completo | DONE (S438) |
| E.2 | `lu chat` funziona end-to-end | 3 lingue, 100+ test | DONE (S440: 3 protocolli, narrativa, 202 test, 9.5/10) |
| E.3 | NL -> codice verificato | 80%+ accuracy | DONE (S440: ClaudeNLProcessor + disambiguation, 68 test, 9.5/10) |
| E.4 | `lu chat --voice` | 3 lingue, < 3s | DONE (S441: faster-whisper + sounddevice, 70 test, 9.5/10) |
| E.5 | Demo "la nonna" | Video 3 minuti | IN PROGRESS (S442: T1.1+T1.2 DONE, T1.3 video in progress) |
| E.6 | Community | 1000+ developer | TODO |

---

> "Se nessuno l'ha fatto prima, e perche aspettavano noi."
> "Fatto BENE > Fatto VELOCE."
> "Ultrapassar os proprios limites!"

*Cervella Architect - CervellaSwarm S394*
*La bibbia del linguaggio. Da qui parte tutto.*
