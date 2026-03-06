# GitHub Release - Strategia Monorepo Multi-Package
**Data:** 2026-02-25
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti consultate:** 18 (GitHub, PyPI, blog ingegneristici, SDK Anthropic/OpenAI, google-cloud-python)

---

## CONTESTO PROGETTO

CervellaSwarm: monorepo con 9 package Python tutti v0.1.0 su PyPI.
Tag format GIA IMPLEMENTATO nei workflow: `{package-name}-v{version}` (es: `code-intelligence-v0.1.0`)
Prossimo step: F4.1c GitHub Release formale.

---

## DOMANDA 1: Tag Format - Cosa fa il settore?

### Risposta: Il settore usa ESATTAMENTE il formato gia implementato

Il formato `{package-name}-v{version}` e il GOLD STANDARD industriale:

| Player | Tag format | Esempio |
|--------|-----------|---------|
| google-cloud-python (googleapis) | `{package-name}-v{version}` | `google-cloud-kms-v3.11.0` |
| release-please (Google tool) | `{component}-v{version}` | default configurabile |
| Microsoft ISE | `{model/a}-v{version}` | per componente |
| semantic-release-monorepo | `{package-name}-{version}` | namespace-based |

**Conclusione:** La scelta fatta in S393 e CORRETTA e ALLINEATA ai big. Zero cambiamenti necessari.

**Dettaglio google-cloud-python:** Ogni package ha la sua release indipendente con tag come
`grafeas-v1.20.0`, `google-maps-places-v0.7.0`, `google-cloud-kms-v3.11.0`. Nessun umbrella tag.

---

## DOMANDA 2: Release Notes per Primo Release - Cosa includere?

### Pattern raccomandato (sintesi da Anthropic SDK, OpenAI Agents SDK, py-pkgs.org)

```markdown
## [Package Name] v0.1.0 - Initial Release

[Una frase che spiega COSA FA il package, scritta per chi non conosce il progetto]

### Install
pip install cervellaswarm-{package}==0.1.0

### What's included
- Feature 1: [breve descrizione]
- Feature 2: [breve descrizione]
- Feature N: ...

### CLI commands (se applicabile)
cervella-xxx --help

### Links
- PyPI: https://pypi.org/project/cervellaswarm-{package}/0.1.0/
- Documentation: ...
- Changelog: ...

---
Part of the CervellaSwarm suite.
```

**Key insight Anthropic SDK:** Minimal ma informativo. Niente verbose. Focus su:
1. Cosa fa (1 frase)
2. Come installarlo (copy-paste-ready)
3. Cosa e incluso (bullet list)
4. Link PyPI

**Key insight OpenAI Agents:** Include "What's Changed" con bullet list delle feature principali.

### Per un primo release (v0.1.0) specificamente:
- "Initial release" e sufficiente come titolo/nota
- Listare TUTTE le feature incluse (e' la prima versione, non c'e "what's new" - c'e' TUTTO)
- Includere requisiti: Python >= 3.10, dipendenze
- Includere un esempio di codice funzionante (3-5 righe)

---

## DOMANDA 3: Umbrella Release - Come funziona?

### Pattern consigliato: DUAL MODEL (per package + umbrella)

I grandi player adottano approcci diversi:

**Approccio A - Solo per-package (google-cloud-python, microsoft ISE):**
- Ogni package ha la sua release indipendente
- PRO: utenti installano solo quello che serve
- PRO: changelog pulito per package
- CON: nessuna "announcement" aggregata per il lancio

**Approccio B - Solo umbrella (azu/monorepo-github-releases):**
- Una release per tutti, versione sincronizzata
- PRO: semplice, buono per prodotti coesi
- CON: difficile se i package evolvono a ritmi diversi

**Approccio C - DUAL: umbrella per il LANCIO + per-package per gli aggiornamenti:**
- Tag speciale: `v0.1.0` (o `cervellaswarm-v0.1.0`) per il lancio iniziale
- Poi per ogni release futura: `{package}-v{version}` per package individuale
- PRO: lancio ha visibilita massima, futura manutenzione e' granulare
- USATO DA: ecosistemi che vogliono "moment of launch" chiaro

### Raccomandazione per CervellaSwarm

**STRATEGIA RACCOMANDATA:** Approccio C, con queste specifiche:

1. **Tag umbrella per il lancio:** `cervellaswarm-v0.1.0` (una sola volta, per il Show HN moment)
   - Release titled "CervellaSwarm Suite v0.1.0 - Initial Launch"
   - Lista tutti e 9 i package con descrizione 1-liner
   - Link a ogni package su PyPI
   - E' la "landing page" del progetto su GitHub Releases

2. **Per ogni release futura di ogni package:** `{package-name}-v{version}`
   - Gia implementato nei workflow esistenti
   - GitHub Release automatica via softprops/action-gh-release

---

## DOMANDA 4: Esempi Concreti da Grandi Progetti

### google-cloud-python
- Repository: `googleapis/google-cloud-python`
- Struttura: 200+ package nello stesso repo
- Tag: `{package-name}-v{version}` (ESATTO come CervellaSwarm)
- Release: automatizzate via release-please
- Ogni release ha: changelog estratto automaticamente da CHANGELOG.md

### release-please (Google)
- Config per Python monorepo (`release-please-config.json`):
  ```json
  {
    "release-type": "python",
    "packages": {
      "packages/code-intelligence": {"package-name": "cervellaswarm-code-intelligence"},
      "packages/lingua-universale": {"package-name": "cervellaswarm-lingua-universale"}
    }
  }
  ```
- Legge CHANGELOG.md per generare release notes automaticamente
- PRO: zero effort manuale dopo il setup
- CON: richiede conventional commits (feat:, fix:, etc.)

### Anthropic Claude Agent SDK
- Release notes: minimal, focus su installation + what changed
- NO badges nelle release notes (li mettono nel README)
- Format: flat text con sezioni H3

### OpenAI Agents Python
- Release notes: include contributor credits
- Include "Full Changelog" link (compare tra tag)
- Include esempi di codice per feature principali

---

## DOMANDA 5: Massimizzare Visibilita

### Badge da includere nel README (shields.io)

```markdown
[![PyPI version](https://img.shields.io/pypi/v/cervellaswarm-lingua-universale.svg)](https://pypi.org/project/cervellaswarm-lingua-universale/)
[![Python](https://img.shields.io/pypi/pyversions/cervellaswarm-lingua-universale.svg)](https://pypi.org/project/cervellaswarm-lingua-universale/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/rafapra3008/cervellaswarm/actions/workflows/ci-lingua-universale.yml/badge.svg)](https://github.com/rafapra3008/cervellaswarm/actions)
```

**Note sui badge:**
- Badge nelle release notes GitHub: NON raccomandati (testo e' piu leggibile)
- Badge nel README: SI, sempre (aggiornamento dinamico automatico)
- PyPI badge usa shields.io: `https://img.shields.io/pypi/v/{package-name}`

### GitHub Release - Elementi che massimizzano visibilita

1. **Attach binary artifacts:** I workflow gia fanno `files: dist/*` (wheel + sdist). Corretto.
2. **Tag "Latest Release":** GitHub lo applica automaticamente all'ultima release non-prerelease.
3. **Description chiara nella release:** Prime 160 char vengono usate come preview in Google/GitHub search.
4. **Link "Full Changelog":** Aggiungere `**Full Changelog**: https://github.com/.../compare/...v0.0.0...code-intelligence-v0.1.0`

### GitHub Release vs PyPI - Strategia coordinata

| Cosa | GitHub Release | PyPI |
|------|---------------|------|
| Target audience | Sviluppatori che explorano | Chi cerca e installa |
| Tone | Narrativo + tecnico | Tecnico sintetico |
| Code examples | Si, utile | Nel README del package |
| Changelog | Link al CHANGELOG.md | Nel pypi page description |
| Install instructions | Obbligatorio | Gia nel README |

---

## DOMANDA 6: CHANGELOG Aggregato vs Per-Package

### Risposta: PER-PACKAGE e lo standard

**Perche per-package:**
- google-cloud-python: ogni package ha `CHANGELOG.md` proprio
- release-please: genera per-package per default
- Keep a Changelog: formato standard, per-package
- Permette versioning indipendente (package A a v0.2.0, package B ancora a v0.1.0)

**CHANGELOG aggregato (opzionale, solo per marketing):**
- Un file `CHANGELOG.md` in root che lista i "milestone" del progetto
- Non sostituisce i per-package, li complementa
- Esempio: "2026-02-25: CervellaSwarm v0.1.0 Suite - tutti 9 package pubblicati su PyPI"

**Struttura raccomandata per CervellaSwarm:**
```
packages/
  code-intelligence/CHANGELOG.md      <- GIA ESISTENTE
  lingua-universale/CHANGELOG.md      <- GIA ESISTENTE
  ...
CHANGELOG.md                          <- DA AGGIUNGERE (aggregato milestone)
```

Il CHANGELOG root serve per la "umbrella release" e per il blog post.

---

## STRATEGIA RACCOMANDATA PER F4.1c

### Step 1: Umbrella Release manuale (lancio)

**Tag:** `cervellaswarm-v0.1.0`
**Workflow:** Nuovo file `.github/workflows/release-umbrella.yml` oppure manuale via GitHub UI

**Titolo release:** `CervellaSwarm Suite v0.1.0 - Initial Launch`

**Body template:**

```markdown
# CervellaSwarm Suite v0.1.0

**The first open-source toolkit for formal multi-agent AI systems.**

9 packages. 3,791 tests. Zero compromises.

---

## Packages

| Package | PyPI | Description |
|---------|------|-------------|
| `cervellaswarm-lingua-universale` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-lingua-universale.svg)](https://pypi.org/project/cervellaswarm-lingua-universale/) | Session types & formal protocols for AI agents |
| `cervellaswarm-code-intelligence` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-code-intelligence.svg)](https://pypi.org/project/cervellaswarm-code-intelligence/) | AST-based code analysis & semantic search |
| `cervellaswarm-agent-hooks` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-agent-hooks.svg)](https://pypi.org/project/cervellaswarm-agent-hooks/) | Lifecycle hooks for Claude Code agents |
| `cervellaswarm-agent-templates` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-agent-templates.svg)](https://pypi.org/project/cervellaswarm-agent-templates/) | Standardized agent templates with team.yaml |
| `cervellaswarm-task-orchestration` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-task-orchestration.svg)](https://pypi.org/project/cervellaswarm-task-orchestration/) | Deterministic task routing, zero deps |
| `cervellaswarm-spawn-workers` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-spawn-workers.svg)](https://pypi.org/project/cervellaswarm-spawn-workers/) | Background worker management for agents |
| `cervellaswarm-session-memory` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-session-memory.svg)](https://pypi.org/project/cervellaswarm-session-memory/) | Cross-session persistent memory for AI |
| `cervellaswarm-event-store` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-event-store.svg)](https://pypi.org/project/cervellaswarm-event-store/) | Immutable append-only event log |
| `cervellaswarm-quality-gates` | [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-quality-gates.svg)](https://pypi.org/project/cervellaswarm-quality-gates/) | Content scoring & validation rules |

## Quick Start

pip install cervellaswarm-lingua-universale

## What makes this different

- **Lingua Universale**: the first session-type system for AI agents in Python
- **Formal verification**: Lean 4 bridge for protocol correctness proofs
- **Deterministic routing**: rule-based task classification (no LLM for orchestration)
- **Production-tested**: 3,791 tests, 95%+ coverage, Apache 2.0

## Full Changelog

See individual package CHANGELOGs:
- [lingua-universale/CHANGELOG.md](packages/lingua-universale/CHANGELOG.md)
- [code-intelligence/CHANGELOG.md](packages/code-intelligence/CHANGELOG.md)
- ...

---
Built by CervellaSwarm. "Ultrapassar os proprios limites!"
```

### Step 2: Per-Package Releases (trigger automatico)

I workflow esistenti sono GIA CORRETTI. Basta pushare i tag:

```bash
git tag code-intelligence-v0.1.0
git tag lingua-universale-v0.1.0
# ... per tutti e 9 ...
git push origin --tags
```

Ogni workflow crea automaticamente la GitHub Release con:
- Install instruction
- Link CHANGELOG
- Link PyPI
- Artifacts allegati (wheel + sdist)

**NOTA:** I workflow attuali hanno un body minimale. Puo' essere arricchito con:
- Un esempio di codice (3 righe)
- Badge PyPI dinamico
- "What's included" bullet list (solo per v0.1.0)

---

## MIGLIORIE AI WORKFLOW ESISTENTI (opzionali)

Il body attuale nei workflow e' sufficiente per il lancio. Migliorie opzionali per arricchire:

### Aggiungere al body delle release per-package:

```yaml
body: |
  ## cervellaswarm-{package} ${{ steps.version.outputs.version }}

  [![PyPI](https://img.shields.io/pypi/v/cervellaswarm-{package}.svg)](https://pypi.org/project/cervellaswarm-{package}/)
  [![Python](https://img.shields.io/pypi/pyversions/cervellaswarm-{package}.svg)](...)

  **[Una frase descrittiva]**

  ### Install
  pip install cervellaswarm-{package}==${{ steps.version.outputs.version }}

  ### What's included in v0.1.0
  - [Feature 1]
  - [Feature 2]

  ### Changelog
  See [CHANGELOG.md](https://github.com/.../packages/{package}/CHANGELOG.md)

  ### Links
  - [PyPI](https://pypi.org/project/cervellaswarm-{package}/${{ steps.version.outputs.version }}/)
  - [Documentation](...)

  ---
  Part of [CervellaSwarm Suite](https://github.com/rafapra3008/cervellaswarm).

  **Full Changelog**: https://github.com/rafapra3008/cervellaswarm/commits/{tag}
```

---

## SINTESI RACCOMANDAZIONI

1. **Tag format:** GIA CORRETTO. `{package-name}-v{version}` e' il gold standard (google-cloud-python usa lo stesso).

2. **Umbrella release:** CREA `cervellaswarm-v0.1.0` una sola volta per il lancio. Manuale o nuovo workflow. E' la "landing page" per Show HN / blog.

3. **Per-package releases:** I workflow esistenti sono FUNZIONALI. Basta pushare i 9 tag.

4. **Release notes per-package:** Arricchire il body con: badge PyPI, esempio codice, "What's included" per v0.1.0.

5. **Badge:** Shields.io in README. Non nelle release notes (non renderizzano in preview).

6. **CHANGELOG:** Per-package (gia esiste). Aggiungere `CHANGELOG.md` root per milestone aggregati.

7. **Ordine operativo:**
   a. Push umbrella tag `cervellaswarm-v0.1.0` (manuale, body ricco)
   b. Push i 9 tag per-package (automatico via workflow)
   c. Verifica che tutte le 10 release appaiano in GitHub Releases
   d. La umbrella release e' quella "pinned" per il blog/Show HN

---

## APPENDICE: Checklist Pre-Release

- [ ] Tutti i 9 tag per-package pushati
- [ ] Tutti i 9 workflow completati con successo
- [ ] Umbrella release `cervellaswarm-v0.1.0` creata
- [ ] Badge shields.io aggiunti al README principale
- [ ] CHANGELOG.md root aggiunto
- [ ] Link tra umbrella release e per-package funzionanti
- [ ] Artifacts (wheel + sdist) allegati a ogni release

---

*Report generato da Cervella Researcher - Sessione 400*
*Fonti: googleapis/google-cloud-python, googleapis/release-please, Anthropic SDK Python, OpenAI Agents Python, Microsoft ISE Blog, shields.io, capjamesg.github.io, py-pkgs.org*
