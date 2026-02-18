# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-18 - Sessione 369
> **STATUS:** FASE 1 OPEN SOURCE COMPLETA! Package LIVE su PyPI. Prossimo: FASE 2 (Agent Framework)

---

## SESSIONE 369 - F1.4: PyPI Publication

### Contesto
Seconda sessione FASE 1. Obiettivo: pubblicare `cervellaswarm-code-intelligence` v0.1.0 su PyPI con Trusted Publishing. Primo package open source di CervellaSwarm.

### Cosa abbiamo fatto

**NORD.md aggiornato:**
- FASE 0: 100% COMPLETA (era ~75%)
- FASE 1: 100% COMPLETA (era TODO)
- Test suite: 1032 (era 968)

**Workflow GitHub Actions creati:**
- `publish-pypi.yml`: Trusted Publishing OIDC, TestPyPI + PyPI + GitHub Release
- `ci-code-intelligence.yml`: Python 3.10-3.13 matrix, build+install verify

**Fix durante CI:**
- `scipy>=1.10.0` aggiunto come dipendenza (networkx PageRank richiede scipy)
- Repository name fix: `cervellaswarm-internal` (non `cervellaswarm`) su PyPI config
- README: "3 dependencies" -> "4 dependencies"

**Risultato: PACKAGE LIVE SU PyPI!**
- URL: https://pypi.org/project/cervellaswarm-code-intelligence/
- `pip install cervellaswarm-code-intelligence` funziona
- Attestazioni digitali PEP 740 (Sigstore) automatiche
- GitHub Release creato

**Ricerca:** Report Trusted Publishing con 10 fonti (`.sncp/progetti/cervellaswarm/reports/RESEARCH_20260218_pypi_trusted_publishing.md`)

### Decisioni S369

| Decisione | Perche |
|-----------|--------|
| Tag `code-intelligence-v*` | Separato da CLI `v*` per monorepo |
| scipy come dipendenza | networkx PageRank richiede scipy per risultati non-uniformi |
| Trusted Publishing OIDC | Zero API tokens, sicurezza massima, best practice 2026 |
| Publish da repo privato | cervellaswarm-internal (non public) - workflow file deve matchare |
| Environment protection PyPI | Manual approval da rafapra3008 per publish produzione |

### Lezioni apprese S369
- **networkx PageRank**: richiede scipy (non solo numpy). Test passano localmente perche scipy gia installato
- **PyPI Trusted Publisher**: il repository name deve matchare ESATTAMENTE (cervellaswarm-internal, non cervellaswarm)
- **PyPI immutabile**: una volta pubblicata una versione, non si puo sovrascrivere. Fix = bump version

---

## PROSSIMI STEP
- **FASE 2: Agent Framework** - Hook system, agent templates, task orchestration
  - F2.1: Hook System pubblicabile
  - F2.2: Agent Definitions come templates
  - F2.3: Task Orchestration
  - F2.4: Spawn Workers portabile
- **Hero image:** Creare immagine/GIF pulita senza riferimenti interni
- **F3 nota:** MCP SNCP KNOWN_PROJECTS hardcoded -> rendere configurabile
- **Post lancio:** Reddit r/ClaudeAI, r/Python, Twitter/X (quando pronto con FASE 2)

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349-S360 | MAPPA MIGLIORAMENTI completata + SNCP 4.0 + POLISH |
| S361 | REGOLA ANTI-DOWNGRADE modelli |
| S362 | OPEN SOURCE STRATEGY! subroadmap 5 fasi |
| S363-S367 | **FASE 0 COMPLETA** (6/6 step, media 9.4/10) |
| S368 | **FASE 1: F1.1+F1.2+F1.3** (9.6+9.5+9.5/10) |
| S369 | **FASE 1: F1.4 PyPI LIVE!** Package sul mondo! |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S369*
