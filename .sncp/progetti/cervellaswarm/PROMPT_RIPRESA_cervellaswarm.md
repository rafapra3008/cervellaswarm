# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-24 - Sessione 390
> **STATUS:** Claude Desktop CONFIGURATO per la Famiglia!

---

## SESSIONE 390 - Cosa e successo

### Claude Desktop Setup COMPLETATO

Rafa ha chiesto di esplorare Claude Desktop (v1.1.4088, aggiornato 23 Feb 2026) per il workflow della Famiglia. Ricerca + configurazione + audit Guardiana.

**Cosa abbiamo fatto:**
- Ricerca approfondita su Claude Desktop (12+ fonti): 3 tab (Chat, Cowork, Code)
- Tab Code = stessa esperienza CLI (legge CLAUDE.md, agents, .mcp.json, hooks)
- MCP server CervellaSwarm: rebuild TypeScript, verificato funzionante nel Desktop
- SNCP tools funzionano (read/search progetti) - testato live nel Desktop
- Guardiana audit: 8.5/10 (0 P0, 0 P1, 3 P2, 4 P3)

**Decisioni chiave:**
- MCP spawn_worker NON serve nel Desktop (Max 20x copre tutto, Task tool nativo)
- Il valore del nostro MCP nel Desktop = SNCP (memoria progetti)
- Errore "connectors directory" = ignorabile (marketplace Anthropic, non nostro)
- Desktop = complemento alla CLI, non sostituto. CLI resta backbone per automazione/swarm

### Guardiana Audit P2 trovati (MCP server)
- F1: Nessun env isolation in .mcp.json (security)
- F2: Path traversal fragile in sncp/reader.ts (type guard salva, ma fragile)
- F3: API key prefix leak in check_status (mostra troppi caratteri)
- F7: Version mismatch SERVER_VERSION 0.3.0 vs package.json 2.0.0-beta.1

---

## Lezioni Apprese (Sessione 390)

### Cosa ha funzionato bene
- Ricerca PRIMA di agire: 2 researcher in parallelo (features + setup guide) = decisione informata
- Guardiana audit su config MCP ha trovato 3 P2 che non avremmo visto

### Cosa non ha funzionato
- Auto-checkpoint hook continua a sporcare PROMPT_RIPRESA (noise in fondo al file, dovuto pulire di nuovo)

### Pattern candidato
- "Desktop Code tab = CLI con UI. Stessi file, stessi agents, stessi hooks. Zero config extra."
- Evidenza: S390 (confermato con test live)
- Azione: MONITORARE (1 occorrenza)

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  FASE A: LE FONDAMENTA     [####################] 100% HARDENED! (S375-S386)
  FASE B: IL TOOLKIT         [################....] 80% (S387)
    FATTO: Confidence, Trust, Thread Safety, Welford, 5 dataclass
    RESTA: DSL nested choices (differito post-PyPI)
  PYPI PUBLISH              [####################] 100% (S389)
    LIVE su pypi.org! pip install cervellaswarm-lingua-universale

OPEN SOURCE ROADMAP:
  FASE 0-2                   [####################] 100%
  FASE 3                     [######..............] 30%

AUTO-LEARNING L1            [####################] 100% (S387)
CACCIA BUG: 9/9 COMPLETATA (121 bug, 71 fix)
CROSS-PACKAGE: 3112 test totali, 11 packages, ZERO flaky
```

---

## PROSSIMI STEP (in ordine)

1. **F3.2 SQLite Event Database** - prossimo step open source
2. **Fase B.2** - DSL nested choices (post-feedback community)
3. **Community engagement** - annunciare su Reddit, HN, Python communities

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S372 | Coverage push + SNCP 4.0 + FASE 0-2 open source |
| S373 | FASE 3: F3.1 Session Memory (9.6/10) |
| S374-S378 | CACCIA BUG 1-7 (7 packages, 80 bug, 48 fix) |
| S379 | FIX AUTO-HANDOFF (8 step, 14 file, 9.5/10) |
| S380-S386 | LINGUA UNIVERSALE Fase A (7 moduli, 997 test, HARDENED!) |
| S387 | AUTO-LEARNING L1 + FASE B (9 moduli, 1273 test, 84 API) |
| S388 | README killer + CI/Publish per PyPI (Guardiana 9.5/10) |
| S389 | PyPI PUBLISH LIVE! cervellaswarm-lingua-universale v0.1.0 |
| S390 | Claude Desktop setup + MCP audit Guardiana 8.5/10 |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
