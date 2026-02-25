# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-25 - Sessione 398
> **STATUS:** B.6 Error Messages DONE! Errori user-friendly in 3 lingue per la Lingua Universale.

---

## SESSIONE 398 - Cosa e successo

### B.6 Error Messages per Umani - COMPLETATO
Il 14esimo modulo della Lingua Universale. Translator layer che converte eccezioni
tecniche in messaggi comprensibili per non-developer, ispirato a Elm e Rust.

```
PRIMA (errore tecnico grezzo):
  SpecParseError: line 2: unknown message kind 'audit_verdct'.
  Valid (snake_case): audit_request, audit_verdict, ...

DOPO (errore user-friendly con fuzzy matching):
  [LU-S003] Unknown message type: "audit_verdct"
    Line 2
    Did you mean: audit_verdict?
    Hint: Check the valid message types for this protocol.
```

Nuovo modulo `errors.py` in lingua-universale:
- 35 error codes (LU-T/P/R/D/S/I/L/G/C/A/X) che coprono TUTTI i 13 moduli
- 3 lingue: inglese, italiano, portoghese (template dict, ZERO deps)
- `humanize(exc)`: traduce qualsiasi eccezione -> HumanError frozen dataclass
- `format_error()`: output Elm/Rust style (location + got/expected + hint + verbose)
- `suggest_similar()`: fuzzy matching via difflib.get_close_matches() (stdlib)
- Chain of matchers: custom exceptions -> ValueError substring -> fallback LU-X001
- `_SafeDict` per template rendering senza KeyError
- 1784 LOC, ZERO deps esterne

### Decisione architetturale (Regina)
Scelta: Translator Layer additive > sostituzione eccezioni.
Perche: Researcher + Architect convergenza 100%. ZERO breaking changes. Eccezioni tecniche
restano per developer, errors.py aggiunge layer user-friendly. Pattern approvato da 27 fonti
(Elm 2015, Rust diagnostics, miette, Alloy counterexamples, FizzBee, Dafny).
DIFFERENZIATORE: errori multi-lingua per session types formali. NESSUNO al mondo lo ha.

### Guardiana Audit
- Score: 9.3/10 APPROVED. 3 P2 fixati subito (dead code _mk_similar, entry duplicata,
  matcher mancante "protocols cannot be empty"). 4 P3 differiti (import re inline,
  RuntimeError category, 19 codici senza e2e test, IT/PT ASCII-only).
- Tester ha trovato 2 bug aggiuntivi (template escaping `{`/`}` in LU-D006/D007).

### Test
- 257 nuovi test (67 core + 100 humanize + 55 humanize2 + 35 catalog)
- Suite lingua-universale: **1820 test** (era 1563, +257), 0.43s, ZERO regressioni
- 4 file test: test_errors_core, test_errors_humanize, test_errors_humanize2, test_errors_catalog

---

## Stato packages

```
PACKAGE                  PYPI    CI   BUILD   TESTS
code-intelligence        LIVE    OK   OK      399
lingua-universale        LIVE    OK   OK      1820    <-- S398! (+257)
agent-hooks              LIVE    OK   OK      236
agent-templates          LIVE    OK   OK      192
task-orchestration       LIVE    OK   OK      305
spawn-workers            --      OK   OK      191
session-memory           --      OK   OK      193
event-store              --      OK   OK      249
quality-gates            --      OK   OK      206
TOTALE                   5/9     9/9  9/9     3791
```

---

## MAPPA SITUAZIONE

```
OPEN SOURCE ROADMAP:
  FASE 0-3: COMPLETE (100%, media 9.4/10)
  FASE 4: Launch              [########............] 40%
    F4.1a CI/CD Pipeline       DONE (S393, 9.5/10)
    F4.1b PyPI Publication     IN CORSO (5/9 LIVE, 4 restanti)
    F4.1c GitHub Release       TODO
    F4.1d Blog + Social        TODO

LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A: Fondamenta           COMPLETA (7 moduli originali, 9.5+ media)
  FASE B: Il Toolkit           IN CORSO - 6/7 DONE!
    B.1 Confidence Types       DONE (S387 - confidence.py)
    B.2 Trust Composition      DONE (S388 - trust.py)
    B.3 Code Generation        DONE (S395 - codegen.py)
    B.4 Intent Parser          DONE (S396 - intent.py)
    B.5 Spec Language          DONE (S397 - spec.py)
    B.6 Error Messages         DONE (S398 - errors.py)  <-- OGGI!
    B.7 Showcase               PROSSIMO PASSO <-- QUI
  FASE C: Il Linguaggio        2027+
  FASE D: Per Tutti            Il sogno

TUTTI I LAYER OPERATIVI (10!):
  Layer 10: Error Messages (umano)    OK (S398!)  <-- NUOVO!
  Layer 9: Spec Language (proprieta)  OK (S397)
  Layer 8: Intent (naturale)          OK (S396)
  Layer 7: Conversazione Claude       OK
  Layer 6: DSL + Session Checker      OK
  Layer 5: Session Types              OK
  Layer 4: Lean 4 Bridge              OK
  Layer 3: Code Generation            OK (S395)
  Layer 2: Agent Hooks + Gates        OK
  Layer 1: CI/CD + PyPI               OK
```

---

## Lezioni Apprese (S398)

### Cosa ha funzionato bene
- Researcher + Architect in parallelo -> convergenza 100% (confermato 3a volta: B.4, B.5, B.6)
- Tester ha trovato 2 bug reali (template escaping) che il Backend non aveva visto
- Guardiana ha trovato 3 P2 (dead code, duplicata, matcher mancante) - valore ENORME
- Pipeline completa (Research->Architect->Backend->Tester->Guardiana) = METODO COLLAUDATO

### Cosa non ha funzionato
- errors.py 1784 LOC (stimato 800-1000) - catalogo messaggi x3 lingue occupa molto spazio
- Tester ha dovuto fare 4 file (non 3) per stare sotto P18 500-righe

### Pattern candidato
- "Researcher + Architect parallelo come step 1" -> PROMUOVERE (3 sessioni consecutive, 100% convergenza)
- "Tester trova bug che Backend non vede" -> CONSOLIDATO (valore provato in 10+ sessioni)

---

## Prossimi step

1. **B.7 Showcase** - ULTIMO step Fase B! PyPI 9/9 + demo end-to-end + blog "Vericoding"
2. **Fase C** - Il Linguaggio vero (2027+)

---

## File chiave

- `packages/lingua-universale/src/.../errors.py` - B.6 ERROR MESSAGES (NUOVO!)
- `packages/lingua-universale/NORD.md` - VISIONE (leggere SEMPRE!)
- `.sncp/roadmaps/MAPPA_LINGUAGGIO_CERVELLASWARM.md` - LA MAPPA del linguaggio
- `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260225_error_messages_b6.md` - Ricerca B.6
- `.swarm/plans/PLAN_B6_error_messages.md` - Piano architetturale B.6

Archivio: S337-S393 open source. S394 PyPI+MAPPA. S395 B.3. S396 B.4. S397 B.5. S398 B.6.

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
