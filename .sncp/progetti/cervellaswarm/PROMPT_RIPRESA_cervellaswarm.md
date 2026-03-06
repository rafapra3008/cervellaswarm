# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-06 - Sessione 433
> **STATUS:** S433 Migliora Casa v2 COMPLETATA. D5 LSP Avanzato PROSSIMO.

---

## SESSIONE 433 - Migliora Casa v2 (COMPLETATA)

### Cosa e successo
Ispezione sistema + status bar v2 + pulizia + 11 Dependabot + ricerca SNCP + quick wins.
Handoff completo: `.sncp/handoff/HANDOFF_S433_migliora_casa_v2.md`

### Cambiamenti chiave
- **Status bar v2.0** -- context-monitor.py riscritto (JSON nativo Claude Code)
- **11/20 Dependabot PR mergiate** (Ops autonoma, 9 major aperte per sessione dedicata)
- **Path-specific rules** per lingua-universale (`.claude/rules/`)
- **Limite output Worker** aggiornato nel DNA (max 2000 token)
- **Pulizia:** .pyc orfani, .pyc tracked, settings.json.backup

### Ricerca SNCP: risultato strategico
- **SNCP validato empiricamente** (filesystem 74% > vector store 68.5%, benchmark LoCoMo)
- **Mercato memoria AI:** $6.27B -> $28.45B (2030)
- **Raccomandazione:** SNCP come package open source DOPO completamento D6
- Report: `reports/RESEARCH_20260306_sncp_memory_state_of_art_2026.md`

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

  Migliora Casa (S431-S433)  [####################] COMPLETATA!
```

---

## PROSSIMA SESSIONE: D5 LSP Avanzato

- **Hover:** tipo + documentazione al passaggio mouse
- **Completion:** keyword, ruoli, trust tiers
- **Go-to-definition:** click su tipo -> definizione
- **Base LSP:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py`
- **Subroadmap:** `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md`
- **Rules auto:** `.claude/rules/lingua-universale.md` (caricato automaticamente)
- **Metodo:** Researcher -> Piano -> Guardiana audit piano -> Implementa -> Guardiana audit

### TODO Rafa
- Attivare 2FA GitHub (SCADUTO 6 Marzo!)
- Ruotare Bedzzle key su MyReception

### BACKLOG
- 9 Dependabot major PR (sessione dedicata con test)
- Centralizzare PROJECT_MAPPING (7 file)
- Test automatizzati context-monitor.py
- SNCP come package open source (dopo D6)

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test agent-hooks | **253** (packages/agent-hooks/tests/) |
| Test totali LU | **2856** |
| Fix S431-S433 | **32** totali |
| Audit Guardiana | **6** (2+2+2) |
| Dependabot mergiate | **11/20** |

---

## Lezioni Apprese (S433)

### Cosa ha funzionato bene
- **Ricerca PRIMA di riscrivere** -- scoperto JSON nativo Claude Code che ignoravamo
- **Ops autonoma** -- 11 Dependabot PR gestite senza intervento
- **Guardiana in background** -- audit mentre si lavora, zero tempo perso

### Pattern candidato
- **"Ricerca PRIMA di riscrivere"** -- Evidenza: S433 (context-monitor)

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
