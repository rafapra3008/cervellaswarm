# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-25 - Sessione 396
> **STATUS:** B.4 Intent Parser DONE! Il ponte tra linguaggio umano e specifica formale.

---

## SESSIONE 396 - Cosa e successo

### B.4 Intent Parser - COMPLETATO
Il 12esimo modulo della Lingua Universale. Apre il ciclo UMANO.
Ora esiste un modo leggibile da CHIUNQUE per descrivere protocolli:

```
PRIMA (tecnico, DSL Scribble):
  regina -> worker : TaskRequest;

DOPO (naturale, Intent):
  regina asks worker to do task
```

Nuovo modulo `intent.py` in lingua-universale:
- Micro-linguaggio deterministico che SEMBRA naturale ma E strutturato
- Tokenizer indent-aware + recursive descent parser (stesso pattern di dsl.py)
- `_ACTION_MAP`: 14 verb phrase -> MessageKind mapping (1:1, ZERO ambiguita)
- `textwrap.dedent` per gestire triple-quoted strings con indentazione
- Supporta flat protocols E branched (`when X decides:`)
- `IntentParseResult` frozen dataclass con Protocol + warnings
- Integrazione VERIFICATA: SessionChecker + Lean4 + CodeGen + DSL roundtrip
- 649 LOC, ZERO deps esterne (solo stdlib: re, textwrap, dataclasses, enum)

### Decisione architetturale (CEO)
Scelta: micro-linguaggio strutturato INVECE di parser testo libero (regex NLP).
Perche: insight di Rafa ("anche per voi AI e difficile con tutto questo codice, trovate un modo piu semplice"). Deterministico > fuzzy. Leggibile > potente. Semplice > complesso.
Architect + Ingegnera consultate: concordi al 100% su Opzione A.
28 fonti di ricerca consultate (Adapt, Rasa, Req2LTL, spaCy, etc.).

### Guardiana Audit
- Score: 9.3/10 APPROVED. 6 P3 trovate, 4 fixate subito (unused import, __import__ hack, edge tests, commento). 2 deferred a Fase B.

### Test
- 67 nuovi test (36 core + 28 edge + 3 boundary)
- Suite lingua-universale: **1447 test** (era 1380, +67), 0.34s, ZERO regressioni
- Copertura: tutti 14 MessageKind, branching, integrazione downstream, error cases

---

## Stato packages

```
PACKAGE                  PYPI    CI   BUILD   TESTS
code-intelligence        LIVE    OK   OK      399
lingua-universale        LIVE    OK   OK      1447    <-- S396! (+67)
agent-hooks              LIVE    OK   OK      236
agent-templates          LIVE    OK   OK      192
task-orchestration       LIVE    OK   OK      305
spawn-workers            --      OK   OK      191
session-memory           --      OK   OK      193
event-store              --      OK   OK      249
quality-gates            --      OK   OK      206
TOTALE                   5/9     9/9  9/9     3418
```

---

## PyPI: 4 packages mancanti (Rafa deve creare Trusted Publishers)

Batch 2 (max 3 pending): spawn-workers, session-memory, event-store
Batch 3: quality-gates
Owner: `rafapra3008`, Repo: `cervellaswarm-internal`, Env: `pypi`
Poi Regina taglia tag: `git tag {name}-v0.1.0 && git push origin {name}-v0.1.0`

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
  FASE B: Il Toolkit           IN CORSO - 4/7 DONE!
    B.1 Confidence Types       DONE (S387 - confidence.py)
    B.2 Trust Composition      DONE (S388 - trust.py)
    B.3 Code Generation        DONE (S395 - codegen.py)
    B.4 Intent Parser          DONE (S396 - intent.py)  <-- OGGI!
    B.5 Spec Language          PROSSIMO PASSO <-- QUI
    B.6 Error Messages         Pianificato
    B.7 Showcase               Pianificato
  FASE C: Il Linguaggio        2027+
  FASE D: Per Tutti            Il sogno

TUTTI I LAYER OPERATIVI:
  Layer 8: Intent (naturale)      OK (S396!)  <-- NUOVO!
  Layer 7: Conversazione Claude   OK
  Layer 6: DSL + Session Checker  OK
  Layer 5: Session Types          OK
  Layer 4: Lean 4 Bridge          OK
  Layer 3: Code Generation        OK (S395)
  Layer 2: Agent Hooks + Gates    OK
  Layer 1: CI/CD + PyPI           OK
```

---

## Lezioni Apprese (S396)

### Cosa ha funzionato bene
- Insight Rafa ("piu semplice, intelligente, forte") -> scelta micro-linguaggio > regex NLP
- Consultare Architect + Ingegnera PRIMA di implementare -> convergenza 100%, zero waste
- Ricerca 28 fonti prima di scrivere codice -> decisione informata
- Strategia "ogni step -> Guardiana" confermata ancora (9.3/10, P3 fixati)
- textwrap.dedent risolve il problema indentazione in un colpo

### Cosa non ha funzionato
- Stima LOC errata (stimato 300-350, uscito 649 - la docstring EBNF e lunga)
- Smoke test iniziale: usata API sbagliata di SessionChecker (session.state vs session.is_complete)

### Pattern candidato
- "Micro-linguaggio strutturato > parser testo libero" per domini ristretti -> PROMUOVERE
- "textwrap.dedent su source prima del tokenizer" per gestire indentazione -> CONSOLIDATO
- "Consultare 2+ esperte in parallelo prima di design" -> CONSOLIDATO (gia P08+P10)

---

## Prossimi step

1. **B.5 Spec Language** - Sintassi user-friendly sopra il DSL (proprieta formali)
2. **B.6 Error Messages** - Tradurre errori Lean 4 in linguaggio umano
3. Pubblicare 4 packages mancanti (Rafa: Trusted Publishers)
4. **B.7 Showcase** - Demo end-to-end + Blog "From Vibecoding to Vericoding"

---

## File chiave

- `packages/lingua-universale/src/.../intent.py` - B.4 INTENT PARSER (NUOVO!)
- `packages/lingua-universale/NORD.md` - VISIONE (leggere SEMPRE!)
- `.sncp/roadmaps/MAPPA_LINGUAGGIO_CERVELLASWARM.md` - LA MAPPA del linguaggio
- `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260225_intent_parser_b4.md` - Ricerca B.4

Archivio: S337-S393 open source. S394 PyPI+MAPPA. S395 B.3. S396 B.4.

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
