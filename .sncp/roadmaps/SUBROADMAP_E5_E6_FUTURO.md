# SUBROADMAP - E.5 La Nonna Demo + E.6 + Futuro

> **Creata:** 12 Marzo 2026 - Sessione 442
> **Autrice:** Cervella Regina (CEO)
> **Prerequisiti:** E.1-E.4 COMPLETE. E.5 step 1-3 DONE.
> **Score target:** 9.5/10 per ogni step (audit Guardiana)
> **Filosofia:** "Fatto BENE > Fatto VELOCE" | "Un progresso al giorno"

---

## DOVE SIAMO (S442)

```
+================================================================+
|   E.1 Script "La Nonna"           DONE (S438)                  |
|   E.2 IntentBridge Core           DONE (S440, 9.5/10)          |
|   E.3 NL Processing               DONE (S440, 9.5/10)          |
|   E.4 Voice Interface              DONE (S441, 9.5/10)          |
|   E.5 La Nonna Demo               DONE (S442-S443)              |
|   E.6 CervellaLang 1.0            IN PROGRESS                   |
|     T3.1 Grammar 1.0 RFC          DONE (S444)                   |
|     T3.3 lu init                   DONE (S444)                   |
|     T3.4 lu verify standalone      DONE (S444)                   |
|     T3.2 Standard Library          DONE (S445)                   |
|                                                                |
|   Asset: 29 moduli, 3436 test, ~14000+ LOC, ZERO deps core    |
+================================================================+
```

---

## FASE 1: E.5 COMPLETAMENTO (1-2 sessioni)

### T1.1: R20 - Demo Violazione Interattiva (P1)

**Cosa:** Atto 5 Scena 5.3 dello script. Quando l'utente chiede "e se qualcuno prova a cancellare?", il sistema mostra la violazione bloccata.

**Architettura:**
```
Dopo simulazione (SIMULATE phase):
  Sistema: "Vuoi provare a violare una regola?"
  Utente: "si" / "yes" / "sim"
  Sistema: genera scenario di violazione basato su properties del draft
    - no_deletion -> tentativo di cancellazione bloccato
    - role_exclusive -> tentativo da ruolo sbagliato bloccato
    - always_terminates -> ciclo infinito rilevato
  Sistema: mostra messaggio colorato VIOLATION + spiegazione
```

**Implementazione:**
- Nuovo metodo `_render_violation_demo()` in `_intent_bridge.py`
- Usa `SessionChecker` per simulare violazione reale (non finta)
- Output narrativo in lingua target (3 locales)
- Nuovo i18n keys: `violation_prompt`, `violation_blocked`, `violation_explain`

**Criterio completamento:**
- [x] Demo violazione funziona per no_deletion
- [x] Demo violazione funziona per role_exclusive
- [x] Output narrativo in 3 lingue
- [x] 11 test per violazione demo (7 positive, 2 negative, 2 unit)
- [ ] Guardiana audit 9.5/10 (in corso)

**Effort:** 0.5 sessione (DONE S442)

---

### T1.2: `lu demo` - Comando Demo Autonomo (P2)

**Cosa:** Comando CLI che esegue la demo completa SENZA input utente. Scripted.

**Perche:** Per video recording, per presentazioni, per chi vuole vedere il sistema in azione senza interagire.

**Architettura:**
```python
# In _cli.py:
def _cmd_demo(args):
    """Run the complete La Nonna demo autonomously."""
    from ._intent_bridge import ChatSession, DemoRunner
    runner = DemoRunner(lang=args.lang, speed=args.speed)
    runner.run()  # Typewriter effect, pauses, narration
```

```
CLI: lu demo [--lang it|pt|en] [--speed slow|normal|fast]
```

**Implementazione:**
- `DemoRunner` class: scripted ChatSession con input pre-programmati
- Typewriter effect per output (simula digitazione)
- Pausa tra atti per leggibilita
- Include tutti i 5 atti dello script La Nonna
- Atto 5.3: violation demo automatica
- Colori e formattazione terminale

**Criterio completamento:**
- [x] `lu demo` esegue demo completa senza input
- [x] `lu demo --lang it` demo in italiano (+ en, pt)
- [x] Typewriter effect per output (3 speed: slow/normal/fast)
- [x] Tutti 5 atti visibili
- [x] 15 test (7 parser + 8 execution/output)
- [ ] Guardiana audit 9.5/10 (IN PROGRESS)

**Effort:** 1 sessione (DONE S442)

---

### T1.3: Video Recording (P1)

**Cosa:** Screen recording di `lu demo --lang it` per YouTube/social.

**Tool:** VHS (https://github.com/charmbracelet/vhs) - tape files per registrare terminali, produce GIF/MP4. Raccomandato dalla ricerca (18 fonti, report `RESEARCH_20260312_demo_launch_strategy.md`).
- Scriptabile, riproducibile, CI-friendly
- Tema: "Catppuccin Frappe" o "Dracula" (alta leggibilita)
- TypingSpeed 0.05, pausa 3-4 sec prima/dopo VIOLAZIONE RILEVATA (il climax!)

**Output:** Video 2:47 (come script). GIF per README. MP4 per YouTube.

**Criterio completamento:**
- [x] VHS installato (`/opt/homebrew/bin/vhs`)
- [x] VHS tape file `demo/demo_la_nonna.tape` (full MP4) + `demo/demo_la_nonna_short.tape` (GIF 3x speed)
- [x] GIF per README (3.3MB < 5MB target, 5x speed, optimized with gifsicle)
- [x] MP4 per YouTube (4.4MB, slow speed, full quality)
- [x] Il momento VIOLAZIONE RILEVATA e nel demo output (verificato)

**Effort:** 0.5 sessione (dopo T1.2)

---

### T1.4: Blog Post "From Vibe Coding to Vericoding" (P1)

**Cosa:** Blog post tecnico con story-telling. Hook -> Problema -> Soluzione -> Demo -> CTA.

**Struttura (da ricerca 18 fonti, pattern Gleam/Rust/Elm):**
```
1. HOOK: Maria, la scena (NON feature list) - pattern Czaplicki
2. PROBLEMA: "Vibe coding" = AI scrive codice senza garanzie
3. INSIGHT: Session types + NL = il pezzo mancante (citare Req2LTL ASE 2025)
4. DEMO: La Nonna (con GIF inline, momento VIOLAZIONE RILEVATA)
5. COME FUNZIONA: pipeline diagram (NL -> IntentDraft -> verify -> codice)
6. RISULTATI: 3274 test, 28 moduli, 9 proprieta
7. CTA doppio (come Gleam): pip install + GitHub star
```

**Claim candidato:** "Certified Communication" o "The first language where AI agents
describe their own verified behavior in natural language."

**Tono:** Prima persona, autentico, specifico > generico. Evitare "revolutionary".

**Criterio completamento:**
- [x] Blog post scritto (183 righe, ~1000 parole)
- [x] GIF demo inline (reference to demo_la_nonna.gif)
- [x] Adatto per Show HN / Reddit / dev.to
- [x] Review da Cervella Marketing (scritto da Marketing agent)
- [ ] Cervella Docs review finale (pending)

**Effort:** DONE S442

---

### T1.5: Test Persona Non-Tecnica (P2)

**Cosa:** Far usare `lu chat --lang it` a una persona NON tecnica e raccogliere feedback.

**Output:**
- Script di test (cosa chiedere, come osservare)
- Template feedback form
- Report risultati con azioni

**Criterio completamento:**
- [ ] Script test preparato
- [ ] Almeno 1 persona non-tecnica testa il sistema
- [ ] Report feedback con azioni

**Effort:** 0.5 sessione (dipende da disponibilita tester)

---

### T1.6: Guardiana Finale E.5 (P1)

**Criterio completamento:**
- [x] Audit completo tutti i file E.5
- [x] Score 9.5/10
- [x] ZERO P1/P2 aperti
- [x] P3 tutti fixati (il diamante!)

**Effort:** DONE S443 (round 1: 9.3/10 S442+, round 2: 9.5/10 S443)

---

## FASE 2: INFRASTRUTTURA & QUALITA (1-2 sessioni)

### T2.1: PyPI v0.3.1 Publish (P1) -- DONE!

**LIVE su PyPI dal 13 Marzo 2026!** `pip install cervellaswarm-lingua-universale==0.3.1`

**Cosa include (v0.3.1):**
- E.5 complete: IntentBridge, NL mode, Voice, violation demo, lu demo
- E.6 T3.1-T3.4: Grammar RFC, stdlib 20 protocols, lu init --template, lu verify
- 2 new PropertyKind: NO_DELETION, ROLE_EXCLUSIVE (9 total)
- P1 FIX: stdlib moved inside package for wheel inclusion
- CHANGELOG completo, README aggiornato (3436 test, 29 moduli, 10 CLI)
- 3436 test

**Criterio completamento:**
- [x] Rafa approva GitHub environment (auto-approved via API S446)
- [x] CHANGELOG v0.3.1 scritto (S446)
- [x] Version bump 0.3.0 -> 0.3.1 (pyproject.toml + __init__.py)
- [x] stdlib in wheel (spostata in src/, verificato con zipfile)
- [x] .gitignore aggiornato per nuovo path
- [x] README aggiornato (12 stale refs fixate, +Standard Library sezione)
- [x] Wheel build test: `cervellaswarm_lingua_universale-0.3.1-py3-none-any.whl` OK
- [x] `pip install cervellaswarm-lingua-universale==0.3.1` funziona (clean venv verified)
- [x] Test installazione pulita: 20 templates, lu init --template, lu verify OK
- [x] Guardiana audit (S446)
- [x] GitHub Release creata automaticamente
- [x] Sync to public repo (103 files, 14/14 security checks)

---

### T2.2: CI Smoke Test per Pipeline Verifica (P2)

**Cosa:** Test CI che verifica la pipeline completa: intent -> parse -> spec -> verify -> codegen -> simulate.

**Perche:** BUG 1 (S442) era nascosto per 4 sessioni. Un smoke test CI l'avrebbe trovato subito.

**Implementazione:**
```python
# tests/test_pipeline_smoke.py
def test_full_pipeline_e2e():
    """Smoke test: intent -> parse -> check -> codegen -> simulate."""
    session = ChatSession(lang="en", input_fn=..., output_fn=...)
    result = session.run()
    assert result.property_report.results  # NOT empty!
    assert all(r.verdict == PropertyVerdict.PROVED for r in result.property_report.results)
    assert result.generated_code  # NOT empty string
```

**Criterio completamento:**
- [x] Pipeline smoke test: 3 classi, 6 test
- [x] Copre 3 scenari (flat, branched, con 4 properties)
- [x] Eseguito in < 0.1 secondi
- [ ] Integrazione in CI workflow (se necessario, gia nella suite pytest)

**Effort:** DONE S442 (15 min)

---

### T2.3: Playground + IntentBridge Integration (P3)

**Cosa:** Aggiungere tab "Chat" al playground online (Pyodide).

**Perche:** Il playground e GIA live. Aggiungere IntentBridge permette a chiunque di provare senza installare.

**Sfida:** Il guided mode funziona bene in Pyodide. NL mode no (serve anthropic API). Voice mode no (serve browser mic API).

**Criterio completamento:**
- [ ] Tab "Chat" nel playground con guided mode
- [ ] Funziona senza backend (tutto client-side Pyodide)
- [ ] 3 lingue selezionabili

**Effort:** 1-2 sessioni

---

### T2.4: Property Templates Library (P3)

**Cosa:** Libreria di property set pre-configurati per scenari comuni.

```python
PROPERTY_TEMPLATES = {
    "data_safe": ["always_terminates", "no_deadlock", "no_deletion"],
    "strict_roles": ["always_terminates", "no_deadlock", "all_roles_participate", "role_exclusive"],
    "high_trust": ["always_terminates", "no_deadlock", "trust_min high", "confidence_min high"],
}
```

**Perche:** Nella guided mode, l'utente sceglie un template invece di selezionare proprieta una a una.

**Criterio completamento:**
- [ ] 5+ template pre-configurati
- [ ] Integrazione in ChatSession (fase PROPERTIES)
- [ ] i18n per nomi/descrizioni template
- [ ] 10+ test

**Effort:** 0.5 sessione

---

### T2.5: Dependabot PR Cleanup (P3)

**Cosa:** Risolvere 3 PR Dependabot aperte (#19, #14, #11).

**Effort:** 0.5 sessione

---

## FASE 3: E.6 CERVELLAANG 1.0 -- VISIONE (3-5 sessioni)

> "La meta finale. Il primo linguaggio di programmazione per AI con verifica formale."

### T3.1: Grammatica 1.0 RFC (P1)

**Cosa:** Documento RFC che definisce la grammatica EBNF finale, frozen.

**Include:**
- Tutti i keyword attuali + nuovi (`chat`, `voice`, `template` come soft/reserved)
- Regole di compatibilita (1.x additive only, 2.0 breaking with migration)
- Processo di estensione (new PropertyKind, new MessageKind, soft keywords)
- Versionamento Go-style annotations `(* [LU 1.0] *)`

**Criterio completamento:**
- [x] RFC scritto con grammatica EBNF completa (64 produzioni, 9 sezioni)
- [x] Review da Ingegnera (gap analysis) + Researcher (best practices 18 fonti)
- [ ] Feedback community (se presente)
- [x] Guardiana verifica (9.3/10 -> 7/7 findings fixati -> 9.5+)

**P0 Fix (prerequisito):**
- [x] Parser AST allineato 9/9 PropertyKind (`NoDeletionProp`, `RoleExclusiveProp`)
- [x] Grammar export (GBNF + Lark) aggiornato
- [x] 8 nuovi test (7 positivi + 1 negativo)
- [x] Docstrings e CHANGELOG aggiornati (62->64 produzioni, 7->9 property)

**RFC:** `.sncp/progetti/cervellaswarm/reports/RFC_T3_1_GRAMMAR_1_0.md`
**Effort:** DONE S444 (0.5 sessione)

---

### T3.2: Standard Library - 20 Protocolli Verificati (P2)

**Cosa:** Libreria di protocolli pre-costruiti e verificati formalmente.

**Categorie:**
```
Comunicazione:
  - request_response (base)
  - pub_sub (publish/subscribe)
  - pipeline (catena di processamento)
  - scatter_gather (fan-out + collect)

Data:
  - crud_safe (CRUD con no_deletion opzionale)
  - data_pipeline (ETL con verifiche)
  - cache_invalidation (consistency garantita)

Business:
  - order_fulfillment (e-commerce)
  - approval_workflow (multi-level approval)
  - auction (bidding protocol)

AI/ML:
  - rag_pipeline (retrieval + generation)
  - agent_delegation (task assignment con trust)
  - consensus (voting protocol)
```

**Criterio completamento:**
- [x] 20 protocolli scritti in .lu (5 categorie)
- [x] TUTTI verificati formalmente (PROVED)
- [x] Documentazione per ogni protocollo (SPDX header + README)
- [x] Test per ogni protocollo (72 test in 5 file)
- [x] Tutte 9 PropertyKind coperte
- [x] `lu init --template` per usare stdlib come base
- [ ] Navigabili nel playground (futuro T2.3)

**Effort:** DONE S445 (1 sessione!)

---

### T3.3: `lu init` - Project Scaffolding (P2)

**Cosa:** Comando per creare un nuovo progetto LU con struttura standard.

```bash
lu init my-protocol
# Creates:
#   my-protocol/
#     my-protocol.lu       # protocol skeleton (parses + verifies PROVED)
#     my-protocol_test.lu   # verification test
#     README.md             # quick start guide
```

**Design:** deno-init style. Non-interactive, one-shot. ZERO deps (pathlib + textwrap).

**Opzioni:**
- `--minimal` -- solo il .lu file
- `--force` -- sovrascrive directory non-vuota

**Criterio completamento:**
- [x] `lu init` crea 3 file (protocol + test + README)
- [x] `--minimal` crea solo .lu
- [x] `--force` sovrascrive senza perdere file esistenti
- [x] File generati parsano E verificano (PROVED)
- [x] Nome validato (no digit-leading, no special chars)
- [x] PascalCase conversion per hyphens/underscores
- [x] 23 test (7 template + 12 core + 4 CLI)
- [x] Guardiana audit 9.3/10 -> 7/7 findings fixati

**Effort:** DONE S444 (0.3 sessione)

---

### T3.4: `lu verify` - Verifica Standalone (P2)

**Cosa:** Comando per verificare un file .lu dalla CLI senza passare per la chat.

```bash
lu verify protocol.lu
# Output:
#   Verifying protocol.lu...
#   [1/3] always_terminates  ... PROVED
#   [2/3] no_deadlock        ... PROVED
#   [3/3] no_deletion        ... PROVED
#   All 3 properties PROVED.
```

**Implementazione (S444):**
- `verify_source()`: 2-layer (static property checking + Lean 4 bridge)
- `_protocol_node_to_runtime()`: AST → Protocol con ChoiceNode → ProtocolChoice
- `_ast_properties_to_spec()`: 9/9 PropertyKind mapping
- `_safe_check_properties()`: graceful per-property fallback with SKIPPED verdict
- `_action_to_kind_map()`: shared DRY helper (was duplicated)
- `_cmd_verify()`: colored output (GREEN PROVED, RED VIOLATED, YELLOW SKIPPED)
- 12 test: 11 property + 1 ChoiceNode

**Criterio completamento:**
- [x] `lu verify` mostra verdetti per-property colorati
- [x] 9/9 PropertyKind supportati (PROVED/VIOLATED/SKIPPED)
- [x] ChoiceNode branches inclusi nella verifica
- [x] 12 test nuovi (tutti passed)
- [x] Guardiana audit 9.3/10 → 7/7 findings fixati

**Effort:** DONE S444 (0.5 sessione)

---

### T3.5: VS Code Marketplace Publish (P2)

**Cosa:** Pubblicare l'estensione VS Code su Marketplace.

**Blocco:** Publisher account (serve Rafa).

**Effort:** 0.5 sessione (dopo account creato)

---

### T3.6: Community Seeding (P3)

**Cosa:** Raggiungere i primi 100 developer.

**Canali:**
- Show HN (gia fatto S404, ma nuova demo con La Nonna)
- Reddit r/ProgrammingLanguages, r/Python
- Dev.to post
- Twitter/X thread
- Conference lightning talks (PyCon, Strange Loop)

**Criterio completamento:**
- [ ] 100+ GitHub stars
- [ ] 50+ pip installs/settimana
- [ ] 10+ issue/PR dalla community
- [ ] 5+ blog post/tweet che menzionano LU

---

## FASE 4: LU COME LINGUAGGIO NATIVO PER AI (lungo termine)

> **Visione di Rafa (S442):** "Un giorno le AI sviluppano CON Lingua Universale."
> Come Python e diventato il linguaggio dell'AI/ML, LU diventa lo standard
> per la comunicazione verificata tra agenti AI.

### T4.1: AI Agent Framework Integration (PRIORITA ALTA)

**Cosa:** Plugin per LangChain, CrewAI, AutoGen, Claude Agent SDK che usa LU per coordinare agenti.

**Perche:** Il nostro campo vergine. AI agent coordination con garanzie formali. Le AI usano LU come "contratto" per comunicare tra loro, come protobuf per gRPC ma verificato formalmente.

**Milestone:** Un agente Claude che parla LU nativamente per coordinare altri agenti.

---

### T4.2: LU come Protocollo AI-to-AI

**Cosa:** Definire LU come standard di comunicazione tra AI agents con verifica formale integrata.

**Perche:** Oggi gli agenti AI comunicano in JSON/testo senza garanzie. LU aggiunge: ordine dei messaggi garantito, nessun deadlock, proprietà verificate matematicamente. L'AI non solo AIUTA a scrivere LU -- l'AI PARLA LU.

---

### T4.3: Multi-Backend Verifica (Lean4 + Z3 + Coq)

**Cosa:** Supportare piu backend di verifica formale, non solo Lean4.

**Perche:** Z3 e piu accessibile (pip installabile). Coq ha community accademica forte.

---

### T4.4: TypeScript Runtime

**Cosa:** Runtime checker in TypeScript per protocolli LU.

**Perche:** JavaScript/TypeScript e il linguaggio piu usato. Sblocca web frontend + AI agents in JS.

---

### T4.5: Protocol Composition

**Cosa:** Combinare protocolli: `protocol AB = A >> B` (sequenza), `A || B` (parallelo).

**Perche:** Pattern fondamentale dei session types. Differenziatore accademico. Permette AI agents di comporre protocolli complessi da primitivi verificati.

---

### T4.6: Real-Time Monitor Dashboard

**Cosa:** Dashboard web che mostra protocolli in esecuzione, violazioni, metriche.

**Perche:** Da "tool CLI" a "piattaforma di monitoraggio". Revenue enterprise.

---

## BACKLOG (non prioritizzato)

| ID | Task | Priority |
|----|------|----------|
| B1 | Refactoring `_lsp.create_server()` 136 righe | P3 |
| B2 | Dependabot PR #19, #14, #11 | P3 |
| B3 | NORD.md aggiornamento E.5 completamento | P2 (dopo E.5 done) |
| B4 | Memory cleanup (session-history.md troppo lungo) | P3 |
| B5 | `lu lint` - linter per file .lu | P3 |
| B6 | `lu fmt` - formatter per file .lu | P3 |
| B7 | Test coverage report (attuale: stimato 95%+) | P3 |
| B8 | Documentation site (Sphinx/MkDocs) | P3 |

---

## DIPENDENZE

```
FASE 1 (E.5 completamento)
   |
   +-- T1.1 R20 Violation Demo ← NESSUNA dipendenza
   +-- T1.2 lu demo ← dipende da T1.1
   +-- T1.3 Video ← dipende da T1.2
   +-- T1.4 Blog ← dipende da T1.3
   +-- T1.5 Test persona ← dipende da T1.2
   +-- T1.6 Guardiana finale ← dipende da T1.1-T1.5
   |
FASE 2 (Infrastruttura)
   |
   +-- T2.1 PyPI ← blocco: Rafa (parallelo a Fase 1)
   +-- T2.2 CI Smoke ← dopo T1.1
   +-- T2.3 Playground Chat ← dopo T1.6
   +-- T2.4 Property Templates ← dopo T1.1
   +-- T2.5 Dependabot ← parallelo
   |
FASE 3 (E.6 CervellaLang 1.0)
   |
   +-- T3.1 RFC ← dopo Fase 1 + 2
   +-- T3.2 Standard Library ← dopo T3.1
   +-- T3.3 lu init ← dopo T3.1
   +-- T3.4 lu verify ← parallelo a T3.2
   +-- T3.5 VS Code ← blocco: Rafa
   +-- T3.6 Community ← dopo T3.1 + Blog
   |
FASE 4 (Futuro)
   +-- Tutto ← dopo E.6 base completa
```

---

## EFFORT STIMATO

```
FASE 1: 2-3 sessioni (E.5 completamento)
FASE 2: 2-3 sessioni (infrastruttura)
FASE 3: 3-5 sessioni (E.6 CervellaLang 1.0)
FASE 4: lungo termine (iterativo)

TOTALE fino a E.6 base: 7-11 sessioni
```

---

## METRICHE TARGET

| Metrica | Attuale | Target E.5 | Target E.6 |
|---------|---------|------------|------------|
| Test LU | 3436 | 3400+ | 3600+ |
| Moduli LU | 29 | 29 | 32+ |
| PropertyKind | 9 | 9 | 9+ |
| Protocolli standard lib | 20 | 0 | 20+ |
| CLI commands | 10 (check, run, verify, compile, init, repl, lsp, chat, demo, version) | 10 (attuale) | 12+ (+lint, +fmt) |
| GitHub stars | ~10 | ~10 | 100+ |
| pip installs/settimana | ~5 | ~10 | 50+ |
| Lingue supportate | 3 | 3 | 3 |
| Guardiana media | 9.5/10 | 9.5/10 | 9.5/10 |

---

## PRIORITA SESSIONE CORRENTE (S446)

```
FASE 1-2: SOSTANZIALMENTE DONE
  T1.5 Test persona non-tecnica  ← dipende da tester reale
  T2.1 PyPI v0.3.1               ← DONE! LIVE su PyPI (13 Mar 2026)
  T2.5 Dependabot PR Cleanup     ← CI failures su tutte le PR, investigation needed

FASE 3 (E.6): T3.1-T3.4 DONE
  T3.1 Grammar 1.0 RFC           ← DONE S444
  T3.2 Standard Library 20 prot  ← DONE S445 (20 protocolli, 72 test)
  T3.3 lu init (+--template)     ← DONE S444+S445
  T3.4 lu verify                 ← DONE S444
  T3.5 VS Code Marketplace       ← PROSSIMO (blocco: Rafa publisher)
  T3.6 Community Seeding          ← PROSSIMO (aggiornare con stdlib)

S446 FINDINGS:
  P1 FIX: stdlib was outside src/ → not in wheel! Moved + verified.
  P3 FIX: README 12 stale references (test counts, module counts, grammar rules)
  P3 FIX: .gitignore negation pattern for new stdlib path
  RESEARCH: Nested choice support (Researcher in background)
```

---

> "La nonna non sa cosa sono i session types.
>  Ma sa che le sue ricette sono AL SICURO."

> "Se nessuno l'ha fatto prima, e perche aspettavano noi."
> "Ultrapassar os proprios limites!"

*Cervella Regina - CervellaSwarm S442*
