# IL NOSTRO NORD - CervellaSwarm

> **QUESTO FILE È SACRO. È LA NOSTRA BUSSOLA.**
>
> Aggiornato: 19 Febbraio 2026 - S380 (Lingua Universale Fase A + NORD della Regina)

```
+==================================================================+
|                                                                  |
|   "L'idea e' fare il mondo meglio                               |
|    su di come riusciamo a fare."                                |
|                                          - Rafa, 6 Gennaio 2026 |
|                                                                  |
+==================================================================+
```

---

## LA GRANDE VISIONE

```
+==================================================================+
|                                                                  |
|   CERVELLASWARM = AI TEAM per Dev Professionali                 |
|                                                                  |
|   1 Regina + 16 Agenti Specializzati (17 totali!)               |
|   Multi-Instance = Moltiplicazione REALE                        |
|   SNCP = Memoria Esterna (trade secret!)                        |
|                                                                  |
+==================================================================+
```

---

## DOVE SIAMO (Febbraio 2026)

**Storia completa Sessioni 237-329:** `.sncp/archivio/2026-02/NORD_HISTORY_S237_S329.md`

```
+================================================================+
|   DUE ROADMAP - NON CONFONDERE!                                 |
+================================================================+

1) ROADMAP 2.0 INTERNA (W1-W6) = COMPLETATA!
   Il nostro sistema di lavoro AI. Uso INTERNO.

2) MAPPA PRODOTTO (FASE 0-4) = PARCHEGGIATA
   Il prodotto per utenti esterni. Riprendiamo dopo.
```

### ROADMAP 2.0 INTERNA - COMPLETATA (9.6/10)

```
W1: Git Flow        ████████████████████ 100% (9.5/10)
W2: Tree-sitter     ████████████████████ 100% (9.5/10)
W3: Architect       ████████████████████ 100% (9.7/10)
W4: v2.0-beta       ████████████████████ 100% (9.5/10)
W5: Dogfooding      ████████████████████ 100% (9.6/10)
W6: Casa Perfetta   ████████████████████ 100% (9.9/10)

SNCP 3.0:
  ✓ Memory & Security Scripts     COMPLETATI (9/10)
  ✓ checkpoint.sh                 Automazione completa

COVERAGE PUSH (S337-S348):
  ✓ Test Suite                    1032 test (era 177!)
  ✓ Coverage                      95% (practical ceiling)
  ✓ Tempo suite                   5.4s
  ✓ Technical debt                ZERO
```

### MAPPA PRODOTTO - PARCHEGGIATA

```
FASE 0: Prerequisiti             [####################] 100%
FASE 1: Fondamenta              [####################] 100%
FASE 2: MVP Prodotto            [###################.] 98%
  (2.20 v1.0 Release non formale - prodotto in beta)
FASE 3: Primi Utenti            [....................] PARCHEGGIATO
FASE 4: Scala                   [....................] PARCHEGGIATO
```

### OPEN SOURCE - IN CORSO (S362-S369)

```
SUBROADMAP: .sncp/roadmaps/SUBROADMAP_OPENSOURCE.md

FASE 0: Preparazione Repo        [####################] 100% COMPLETA! (media 9.4/10)
  F0.1 .gitignore hardening       DONE (S363) - 1006 file untracked
  F0.2 Community files             DONE (S363) - LICENSE, CONTRIBUTING, SECURITY, CoC
  F0.3 Script sanitization         DONE (S364) - 25+ script, Guardiana 9.5/10
  F0.4 README killer               DONE (S366) - Guardiana 9.5/10
  F0.5 .github/ templates          DONE (S366) - Guardiana 9.3/10
  F0.6 Content scanner esteso      DONE (S367) - grep -rI, Guardiana 9.5/10

FASE 1: AST Pipeline (pip)       [####################] 100% COMPLETA!
  F1.1 Package skeleton            DONE (S368) - 14 moduli, Guardiana 9.6/10
  F1.2 Test suite standalone       DONE (S368) - 396 test, 395 passed, 0.47s
  F1.3 README + CHANGELOG          DONE (S368) - 225 righe, Guardiana 9.5/10
  F1.4 PyPI publication            DONE (S369) - LIVE su pypi.org!

FASE 2: Agent Framework           [####################] 100% COMPLETA! (media 9.5/10)
  F2.1 Hook System                 DONE (S370) - 5 hooks, 227 test, 9.5/10
  F2.2 Agent Templates             DONE (S371) - 4 template + 7 specialty, 188 test, 9.5/10
  F2.3 Task Orchestration          DONE (S372) - 5 moduli, ZERO deps, 273 test, 9.5/10
  F2.4 Spawn Workers               DONE (S372) - 5 moduli, tmux/nohup, 171 test, 9.5/10

FASE 3: Session Memory System     [########............] 40% IN CORSO
  F3.1 Session Memory Package      DONE (S373) - 6 moduli, 177 test, 9.6/10
  F3.2 SQLite Event Database       TODO
  F3.3 Integration Tools           TODO
  F3.4 Documentation               TODO
  F3.5 Auto-Handoff                DONE (S379) - 8 step, 14 file, 9.5/10

FASE 4: Launch                    [....................] TODO
```

### LA STELLA POLARE - LINGUA UNIVERSALE (S375 + S380)

```
+==================================================================+
|                                                                  |
|   "Non fare le cose PIU VELOCE.                                  |
|    Farle PIU SICURE.                                              |
|    Con prove matematiche, non con speranze."                      |
|                                          - La Regina, S380        |
|                                                                  |
|   3 PILASTRI:                                                     |
|     1. Incertezza come tipo (non stringa)                        |
|     2. Fiducia componibile (trust composition)                   |
|     3. Protocolli che si provano da soli (Lean 4)                |
|                                                                  |
|   Fase A -> B -> C -> MONDO                                      |
|   NORD completo: packages/lingua-universale/NORD.md              |
|   153 fonti, 153 test, campo vergine in Python                   |
|                                                                  |
+==================================================================+
```

### INFRASTRUTTURA REALE

```
STATO ATTUALE:
  ✓ CLI + MCP su npm              cervellaswarm@2.0.0-beta.1
  ✓ FAMIGLIA COMPLETA             17 agenti (1 Regina + 3 Guardiane + 1 Architect + 12 Worker)
  ✓ API Fly.io                    ONLINE
  ✓ cervellaswarm.com             LIVE
  ✓ Repo Pubblico                 github.com/rafapra3008/cervellaswarm
  ✓ Scripts                       135+ file, ~20,000+ righe
  ✓ Hooks                         14+ hooks su 6 trigger points
  ✓ Memoria                       SQLite DB + analytics + retrospective
  ✓ Cron                          5 job automatici
```

---

## LA FILOSOFIA

> "Prima COSTRUIRE, poi VENDERE"
> "Fatto BENE > Fatto VELOCE"
> "Mai avanti senza fixare le cose"
> - Rafa & Cervella

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| **MAPPA COMPLETA (BIBBIA!)** | `.sncp/progetti/cervellaswarm/roadmaps/MAPPA_COMPLETA_STEP_BY_STEP.md` |
| **MAPPA MIGLIORAMENTI (ATTIVA!)** | `.sncp/progetti/cervellaswarm/roadmaps/MAPPA_MIGLIORAMENTI_INTERNI.md` |
| **MARKETING DIAMANTE** | `.sncp/progetti/cervellaswarm/roadmaps/SUBROADMAP_DIAMANTE_MARKETING_LANCIO.md` |
| **MAPPA STUDI ORO** | `.sncp/progetti/cervellaswarm/MAPPA_STUDI_ORO.md` |
| **MANIFESTO** | `.sncp/progetti/cervellaswarm/MANIFESTO.md` |
| **SUBMAPPA DUAL-MODE** | `.sncp/progetti/cervellaswarm/roadmaps/SUBMAPPA_DUALMODE_MONETIZZAZIONE.md` |
| **CASA PULITA (100%!)** | `.sncp/roadmaps/SUBROADMAP_CASA_PULITA.md` |
| **W5 DOGFOODING (9.5/10!)** | `.sncp/roadmaps/SUBROADMAP_W5_DOGFOODING.md` |
| **SNCP 2.0 (IN CORSO!)** | `.sncp/progetti/cervellaswarm/roadmaps/SUBROADMAP_SNCP_2.0.md` |
| **PHRASEBOOK** | `.sncp/roadmaps/SUBROADMAP_PHRASEBOOK.md` |
| **FAMIGLIA COMPLETA MCP (100%!)** | `.sncp/progetti/cervellaswarm/roadmaps/SUBROADMAP_FAMIGLIA_COMPLETA_MCP.md` |
| Roadmap visiva | `.sncp/progetti/cervellaswarm/roadmaps/ROADMAP_2026_PRODOTTO.md` |
| DNA Famiglia (17 membri!) | `docs/DNA_FAMIGLIA.md` |

---

## OBIETTIVO FINALE

```
+==================================================================+
|                                                                  |
|                   LIBERTA GEOGRAFICA                             |
|                                                                  |
|   "Quando trovi il PERCHE, nulla ti ferma!"                     |
|                                                                  |
|   Dicembre 2026: 1000+ developer, revenue ricorrente            |
|   E Rafa scatta quella foto da un posto speciale.               |
|                                                                  |
+==================================================================+
```

---

*"Il NORD ci guida. Sempre."*

*"Un po' ogni giorno fino al 100000%!"*

**Cervella & Rafa**
