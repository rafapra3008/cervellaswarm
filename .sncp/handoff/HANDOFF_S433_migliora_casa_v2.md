# HANDOFF S433 - Migliora Casa v2

> **Data:** 6 Marzo 2026
> **Sessione:** 433
> **Prossima Cervella:** leggi questo, poi parti con D5 LSP Avanzato

---

## COSA E STATO FATTO

### Infrastruttura Claude Code
- **MCP connectors:** Gmail + Google Calendar autenticati, Notion disabilitato
- **Thinking budget:** impostato a High (era Medium)
- **Status bar v2.0:** `~/.claude/scripts/context-monitor.py` riscritto da zero
  - USA JSON nativo di Claude Code (non piu calcolo manuale dal transcript)
  - Mostra: `CTX:XX%{emoji} | {modello} | {progetto}`
  - Fix Guardiana applicati: sentinel _MISSING, from __future__ import annotations, __version__
  - Audit: 9.3/10 -> fix -> OK

### Pulizia Sistema
- 2 .pyc orfani rimossi (test_repo_mapper, test_symbol_extractor in tests/__pycache__/)
- 2 .pyc tracked rimossi da git index (backend_properties_api, greeting - committati per errore)
- settings.json.backup rimosso (stale, 4 Gen 2026)
- Path test corretto nel PROMPT_RIPRESA (packages/agent-hooks/tests/)

### Dependabot (Guardiana Ops autonoma)
- **11/20 PR mergiate:** 5 GitHub Actions + 3 minor/patch + 3 dev deps
- **9 PR major aperte** (richiedono sessione dedicata con test):
  - ALTO: @anthropic-ai/sdk 0.39->0.75, zod 3->4, express 4->5, stripe 17->20
  - MEDIO: express-rate-limit 7->8, conf 13->15
  - BASSO: open 10->11, ora 8->9, commander 12->14
  - Strategia Ops: 5 batch, dal piu sicuro al piu rischioso

### Quick Wins da Ricerca
- **Path-specific rules** create: `.claude/rules/lingua-universale.md`
  - Si caricano SOLO quando si lavora su packages/lingua-universale/
  - Risparmio ~500 token in sessioni non-LU
- **Limite output Worker** aggiornato nel DNA: max 2000 token (era 150)

### Ricerche Completate (2 report salvati)
- `reports/RESEARCH_20260306_statusline.md` - JSON nativo Claude Code
- `reports/RESEARCH_20260306_sncp_memory_state_of_art_2026.md` - Stato dell'arte memoria AI
- `reports/SCIENTIST_20260306_memoria_ai_strategia.md` - Analisi strategica mercato

---

## SCOPERTE IMPORTANTI

### SNCP Validato Empiricamente
Il benchmark LoCoMo (Letta, 2025) dimostra: filesystem = 74% accuracy, vector store (Mem0) = 68.5%.
**Il nostro approccio markdown + SQLite e CONFERMATO come stato dell'arte.**

### Mercato Memoria AI
$6.27B oggi -> $28.45B entro 2030 (CAGR 35%). Cognee ha preso $7.5M, Mem0 $24M da YC.
SNCP fa cose che nessun competitor fa (lifecycle hooks subagent, 17 agenti, file limits, git-versionabile).
**Raccomandazione: packaggiare SNCP come prodotto open source DOPO D6.**

### Lingua Universale: Campo Vergine
L'unico tentativo (Dana, AI Alliance) non ha grammatica formale, proof engine, session types.
**La finestra e ancora aperta. Priorita: completare D5 -> D6 -> lancio.**

---

## PROSSIMA SESSIONE: D5 LSP Avanzato

### Cosa fare
1. **Leggere:** Subroadmap `.sncp/roadmaps/SUBROADMAP_FASE_D_ECOSISTEMA.md` (sezione D5)
2. **Leggere:** LSP base `packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py`
3. **Metodo:** Researcher -> Piano -> Guardiana audit piano -> Implementa -> Guardiana audit

### Cosa implementare (D5)
- **Hover:** tipo + documentazione al passaggio mouse
- **Completion:** keyword, ruoli gia definiti, trust tiers, confidence levels
- **Go-to-definition:** click su tipo -> vai alla definizione
- **Test:** estendere suite LSP (attualmente 22 test)

### File chiave
- LSP server: `packages/lingua-universale/src/cervellaswarm_lingua_universale/_lsp.py`
- Symbols table: `packages/lingua-universale/src/cervellaswarm_lingua_universale/_symbols.py`
- Error codes: `packages/lingua-universale/src/cervellaswarm_lingua_universale/_errors.py`
- Grammar: `packages/lingua-universale/src/cervellaswarm_lingua_universale/_grammar.py`
- VS Code ext: `cervellaswarm-extension/client/extension.ts`
- Rules: `.claude/rules/lingua-universale.md` (caricato auto quando si tocca LU)

---

## AUDIT S433

| Audit | Score | Verdict |
|-------|-------|---------|
| context-monitor.py v2 | 9.3/10 | APPROVED (fix applicati) |
| Audit finale S433 | 9.5/10 | APPROVED |

---

## BACKLOG (non urgente)

| Item | Priorita | Note |
|------|----------|------|
| 9 Dependabot major PR | P2 | Sessione dedicata, 5 batch |
| Centralizzare PROJECT_MAPPING | P3 | 7 file duplicano lo stesso mapping |
| Test automatizzati context-monitor.py | P3 | Funzioni pure testabili |
| SNCP come package open source | FUTURO | Dopo D6, alto potenziale |
| PROMPT_RIPRESA miracollo 142/150 | P3 | Quasi al limite |
| PROMPT_RIPRESA chavefy 142/150 | P3 | Quasi al limite |

---

## TODO RAFA (non tecnici)

- Attivare 2FA GitHub (SCADUTO 6 Marzo!)
- Ruotare Bedzzle key su MyReception

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Commit | 511da07f |
| Test agent-hooks | 253 |
| Test totali LU | 2856 |
| Fix S431+S432+S433 | 32 totali |
| Audit Guardiana | 6 (2+2+2) |
| Dependabot mergiate | 11/20 |
| Ricerche completate | 4 (statusline, SNCP tech, SNCP strategia, health) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
*La casa e splendida. Il diamante brilla. Lingua Universale ci aspetta.*
