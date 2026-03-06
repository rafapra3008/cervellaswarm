# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-06 - Sessione 433
> **STATUS:** S433 Migliora Casa v2 IN CORSO. D5 LSP Avanzato PROSSIMO.

---

## SESSIONE 433 - Migliora Casa v2

### Cosa e successo
Ispezione completa del sistema + miglioramenti infrastruttura + Dependabot triage.

### Fix applicati S433
- **Status bar v2.0** -- context-monitor.py riscritto da zero (JSON nativo Claude Code)
  - Mostra: CTX:XX% + modello + costo + progetto
  - Fix Guardiana: sentinel _MISSING, from __future__ import annotations, __version__
  - File: `~/.claude/scripts/context-monitor.py`
- **2 .pyc orfani rimossi** (test_repo_mapper, test_symbol_extractor)
- **2 .pyc tracked rimossi da git** (backend_properties_api, greeting)
- **settings.json.backup rimosso** (stale, 4 Gen 2026)
- **Path test corretto** nel PROMPT_RIPRESA (packages/agent-hooks/tests/)
- **11/20 Dependabot PR mergiate** (5 Actions + 3 minor + 3 dev deps)
- **MCP connectors** Gmail + Calendar autenticati, Notion disabilitato
- **Thinking budget** impostato a High

### Dependabot: 9 major PR ancora aperte
- ALTO: @anthropic-ai/sdk 0.39->0.75, zod 3->4, express 4->5, stripe 17->20
- MEDIO: express-rate-limit 7->8, conf 13->15
- BASSO: open 10->11, ora 8->9, commander 12->14
- Strategia: sessione dedicata con test per batch

### Audit Guardiana S433
- context-monitor.py v2: **9.3/10** APPROVED (fix applicati)
- Audit finale S433: **9.5/10** APPROVED

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE D: L'Ecosistema -- 4/6 DONE
    D1: Syntax Highlighting   [####################] DONE! (9.5/10)
    D2: LSP Base (lu lsp)     [####################] DONE! (9.5/10)
    D3: Playground Online      [####################] DONE! (LIVE!)
    D4: "A Tour of LU"        [####################] DONE! (9.5/10)
    D5: LSP Avanzato           [....................] PROSSIMO
    D6: Guardiana Finale       [....................] TODO

  Migliora Casa (S431)        [####################] COMPLETATA!
  Backlog Fix (S432)          [####################] COMPLETATA!
  Migliora Casa v2 (S433)    [##################..] IN CORSO
```

---

## PROSSIMA SESSIONE: D5 LSP Avanzato

- **Hover:** tipo + documentazione al passaggio mouse
- **Completion:** keyword, ruoli, trust tiers
- **Go-to-definition:** click su tipo -> definizione
- **Base LSP:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py`
- **Subroadmap:** `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
- **Metodo:** Researcher -> Piano -> Guardiana audit piano -> Implementa -> Guardiana audit

### TODO Rafa
- Attivare 2FA GitHub (SCADUTO 6 Marzo!)
- Ruotare Bedzzle key su MyReception

### BACKLOG per sessione futura
- 9 Dependabot major PR (serve test suite per ogni batch)
- F5: centralizzare PROJECT_MAPPING (7 file duplicano lo stesso mapping)
- F6: test automatizzati per context-monitor.py

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test agent-hooks | **253** (packages/agent-hooks/tests/) |
| Test totali LU | **2856** |
| Fix S431+S432+S433 | **24 + 8** totali |
| Audit Guardiana | **5+** (2 S431 + 2 S432 + 1+ S433) |
| Dependabot mergiate | **11/20** |

---

## Lezioni Apprese (S433)

### Cosa ha funzionato bene
- **Guardiana in background** -- audit corre mentre si lavora, zero tempo perso
- **Researcher per status bar** -- scoperto JSON nativo di Claude Code che ignoravamo
- **Ops autonoma su Dependabot** -- 11 PR mergiate senza intervento manuale

### Cosa non ha funzionato
- **Niente di grave** -- sessione fluida

### Pattern candidato
- **"Ricerca PRIMA di riscrivere"** -- la Researcher ha scoperto dati JSON che non sapevamo esistessero, evitando reinvenzione

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
