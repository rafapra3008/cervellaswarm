# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 236
> **FASE ATTUALE:** MCP Config CORRETTA - Test dopo riavvio!

---

## AZIONE IMMEDIATA

```
+================================================================+
|   RIAVVIA CLAUDE CODE E TESTA!                                 |
|                                                                |
|   Sessione 236 ha scoperto il VERO problema:                   |
|   - settings.json NON è dove Claude legge MCP                  |
|   - Claude legge da ~/.claude.json o .mcp.json                 |
|   - Creato .mcp.json nel project root (fix corretto!)          |
|                                                                |
|   DOPO RIAVVIO:                                                |
|   1. Terminale: claude mcp list                                |
|      → Deve mostrare cervellaswarm connesso                    |
|   2. In Claude: "usa check_status di cervellaswarm"            |
+================================================================+
```

---

## COSA È CAMBIATO (Sessione 235 → 236)

| Sessione | Cosa pensavamo | Realtà |
|----------|----------------|--------|
| 235 | Config in settings.json | NON letto per MCP |
| 236 | Studiato docs ufficiali | MCP va in .mcp.json |

**File creato:** `/Users/rafapra/Developer/CervellaSwarm/.mcp.json`

---

## ROADMAP

```
FASE 0: Fondamenta           [####################] FATTO!
FASE 1: POC MCP              [####################] FATTO!
FASE 2: MCP Completo         [##########..........] IN CORSO
  - Server funziona          [####################] OK
  - Config .mcp.json         [####################] FATTO (Sessione 236!)
  - Test REALE post-restart  [....................] PROSSIMO
  - Resources SNCP           [....................] DOPO
FASE 3: Polish & Launch      [....................]
```

---

## CLEANUP PENDING

Config in `settings.json` (normale + insiders) può restare o essere rimossa.
Non interferisce, ma è inutile ora.

---

## TL;DR

**Sessione 236:** Scoperto che MCP config va in `.mcp.json`, non in `settings.json`. Fix applicato.

**ORA:** Riavvia → `claude mcp list` → test tool.

*"Studiare = Risolvere!"*
