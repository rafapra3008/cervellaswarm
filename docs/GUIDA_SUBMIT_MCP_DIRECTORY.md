# Guida Submit MCP Directory

> **Status:** DA FARE - Requisiti da completare prima del submit
> **Directory disponibili:** Anthropic Official + mcp.so

---

## DIRECTORY 1: Anthropic Official (Connectors)

**URL:** https://claude.com/connectors
**Form:** https://forms.gle/tyiAZvch1kDADKoP9
**Guida:** https://support.claude.com/en/articles/12922490-remote-mcp-server-submission-guide

### Requisiti per Submission

| Requisito | Status | Note |
|-----------|--------|------|
| Tool annotations | **MANCANTE** | readOnlyHint/destructiveHint su ogni tool |
| Documentazione | OK | README completo |
| Test credentials | N/A | Non richiede account |
| Esempi (min 3) | OK | Quick Start ha esempi |
| Contact info | OK | GitHub issues |

### BLOCCANTE: Tool Annotations Mancanti

Il nostro MCP server (`packages/mcp-server/src/index.ts`) NON ha le annotations richieste.

**Cosa serve aggiungere:**

```typescript
// Esempio per spawn_worker:
server.tool(
  "spawn_worker",
  {
    description: "Spawn a CervellaSwarm worker...",
    // AGGIUNGERE:
    annotations: {
      readOnlyHint: false,    // Può modificare file
      destructiveHint: false  // Non è distruttivo
    }
  },
  // ... resto
);

// Esempio per list_workers (read-only):
server.tool(
  "list_workers",
  {
    description: "List all available...",
    annotations: {
      readOnlyHint: true,     // Solo lettura
      destructiveHint: false
    }
  },
  // ...
);
```

**Azione richiesta:** Aggiungere annotations a tutti e 4 i tools prima del submit.

### Informazioni per il Form

```
Server Name: CervellaSwarm
Description: Multi-agent orchestration system with 16 specialized AI agents
             for development. Backend, Frontend, Testing, Security, DevOps,
             and more - coordinated by a Queen orchestrator with Guardian QA agents.

npm Package: @cervellaswarm/mcp-server
GitHub: https://github.com/rafapra3008/CervellaSwarm
Documentation: https://github.com/rafapra3008/CervellaSwarm/blob/main/docs/GETTING_STARTED.md

Tools:
1. spawn_worker - Execute tasks with specialized AI agents
2. list_workers - List all 16 available agents
3. check_status - Verify configuration
4. check_usage - Check quota and usage

Examples:
1. npm install -g @cervellaswarm/mcp-server
2. Use spawn_worker with worker="backend" task="Create REST API"
3. Use list_workers to see all 16 agents

Contact: GitHub Issues (https://github.com/rafapra3008/CervellaSwarm/issues)
```

---

## DIRECTORY 2: mcp.so (Community)

**URL:** https://mcp.so
**Submit:** GitHub Issue nel loro repo

### Come Submittere

1. Vai su mcp.so
2. Clicca "Submit" nel navbar
3. Crea GitHub issue con:

```markdown
### Server Name
CervellaSwarm

### Description
Multi-agent orchestration system - 16 specialized AI agents for development.
Not one assistant - a TEAM. Backend, Frontend, Testing, Security, DevOps, Docs, and more.

### Installation
npm install -g @cervellaswarm/mcp-server

### GitHub Repository
https://github.com/rafapra3008/CervellaSwarm

### Category
Development Tools / Multi-Agent

### Features
- 16 specialized agents
- Guardian QA layer (3 agents validate all work)
- SNCP persistent memory
- Works with Claude Code and Claude Desktop
```

### Status: PRONTO per Submit
mcp.so NON richiede tool annotations. Possiamo submittere subito.

---

## PIANO D'AZIONE

### Step 1: Fix Tool Annotations (BLOCCANTE per Anthropic)
- Modificare `packages/mcp-server/src/index.ts`
- Aggiungere readOnlyHint/destructiveHint a tutti i tools
- Testare che funzioni ancora
- Pubblicare nuova versione npm

### Step 2: Submit mcp.so (SUBITO)
- Non richiede annotations
- Submit via GitHub issue
- Puo essere fatto ORA

### Step 3: Submit Anthropic (DOPO fix)
- Compilare form: https://forms.gle/tyiAZvch1kDADKoP9
- Review time: 24-48h
- Fare PRIMA del lancio Show HN

---

## Note

- Tool annotations sono OBBLIGATORIE per Anthropic (30% rejection rate senza)
- mcp.so è community-driven, meno strict
- Entrambe le directory portano visibilità

---

## Fonti

- [Remote MCP Server Submission Guide](https://support.claude.com/en/articles/12922490-remote-mcp-server-submission-guide)
- [Local MCP Server Submission Guide](https://support.claude.com/en/articles/12922832-local-mcp-server-submission-guide)
- [Anthropic Connectors Directory FAQ](https://support.claude.com/en/articles/11596036-anthropic-connectors-directory-faq)
- [mcp.so](https://mcp.so/)

---

*Guida creata: Sessione 256*
