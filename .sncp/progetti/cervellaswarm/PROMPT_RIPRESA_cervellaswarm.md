# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 234
> **FASE ATTUALE:** MCP Server configurato - PRONTO PER TEST!

---

## AZIONE IMMEDIATA - TEST MCP

```
+================================================================+
|   TESTA SUBITO!                                                |
|                                                                |
|   Sessione 234 ha configurato settings.json                    |
|   ORA devi testare che i tools MCP funzionino REALI           |
|                                                                |
|   COMANDO TEST:                                                |
|   > Chiedi a Claude: "usa check_status di cervellaswarm"      |
|   > Oppure: "list_workers di cervellaswarm"                   |
|                                                                |
|   Se FUNZIONA: continua con Resources SNCP                    |
|   Se NON funziona: debug (vedi sezione troubleshooting)       |
+================================================================+
```

---

## COSA È STATO FATTO (Sessione 234)

| Cosa | Status |
|------|--------|
| Verifica MCP compilato | OK (dist/index.js esiste) |
| Test avvio server | OK ("v0.1.0 started") |
| Config settings.json | FATTO |
| Permessi mcp__cervellaswarm__* | FATTO |

**File modificato:** `~/.claude/settings.json`

---

## ROADMAP AGGIORNATA

```
FASE 0: Fondamenta           [####################] FATTO!
FASE 1: POC MCP              [####################] FATTO!
FASE 2: MCP Completo         [####................] IN CORSO
  - settings.json            [####################] FATTO
  - Test REALE               [....................] DA TESTARE ORA
  - Resources SNCP           [....................] PROSSIMO
  - Più tools                [....................]
FASE 3: Polish & Launch      [....................]
```

---

## SE IL TEST FALLISCE

```
1. Verifica che il server si avvii:
   node /Users/rafapra/Developer/CervellaSwarm/packages/mcp-server/dist/index.js

2. Controlla errori in Console (stderr)

3. Verifica JSON valido:
   cat ~/.claude/settings.json | jq .

4. Path corretto nel settings.json:
   /Users/rafapra/Developer/CervellaSwarm/packages/mcp-server/dist/index.js
```

---

## PROSSIMI STEP (dopo test OK)

```
[ ] Aggiungere Resources SNCP (stato.md, sessioni)
[ ] Aggiungere più tools (coordinate_workers, etc)
[ ] Unit test per spawner
[ ] Test end-to-end completo
```

---

## TL;DR

**Sessione 234:** Configurato settings.json per MCP.

**ORA:** Riavvia Claude Code e testa `check_status`.

*"SU CARTA != REALE - Testiamo!"*
