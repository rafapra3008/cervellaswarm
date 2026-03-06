# Claude Desktop - Aggiornamenti Febbraio 2026
**Data ricerca:** 2026-02-24
**Ricercatrice:** Cervella Researcher
**Fonti consultate:** 12 (Anthropic official, The Decoder, CNBC, VentureBeat, TechCrunch, Claude Docs)

---

## SINTESI ESECUTIVA (per CEO)

Anthropic ha fatto tre mosse distinte a febbraio 2026:
1. **Claude Code Desktop** aggiornato (20 feb) con preview live, code review automatica, gestione PR GitHub
2. **Cowork** lanciato su Windows (10 feb) - agente desktop per knowledge work NON-coding
3. **Claude Code Security** in preview (23 feb) - scansione vulnerabilita codebase

Questi sono prodotti DIVERSI che condividono lo stesso app Claude Desktop come contenitore.

---

## 1. COSA C'E' DI NUOVO (febbraio 2026)

### Claude Code Desktop - Update 20 febbraio 2026

**Preview Live dell'App**
- Claude avvia il dev server e mostra l'app in esecuzione DENTRO l'interfaccia desktop
- Vede l'UI, legge i console log, trova errori e itera in autonomia
- Zero switch al browser. Claude verifica da solo ogni modifica (auto-verify)
- Interazione diretta con l'app nel browser embedded: click, form, DOM inspection

**Code Review Automatica**
- Nuovo pulsante "Review code" nel diff view
- Claude esamina i diff locali e lascia commenti inline
- Segnala: compile errors, logic errors, security vulnerabilities, bug ovvi
- NON segnala: style, formatting, linter issues (solo high-signal)

**PR Management con GitHub**
- Monitora lo stato della PR direttamente nell'app desktop
- Auto-fix: corregge automaticamente i CI failure che trova
- Auto-merge: unisce la PR quando tutti i check passano (metodo: squash)
- Richiede GitHub CLI (`gh`) installato e autenticato

**Sessioni Parallele con Git Isolation**
- Piu sessioni parallele, ognuna con il suo Git worktree isolato
- Modifiche in una sessione non toccano le altre finche non si fa commit
- Stored in `<project-root>/.claude/worktrees/`

**Cross-Platform Session Sync**
- Inizia da CLI -> `/desktop` per portare la sessione nel Desktop
- Inizia da Desktop -> "Continue with Claude Code on the web" per continuare da browser o mobile
- Sessioni Remote: girano su cloud Anthropic, continuano anche a computer spento

---

### Cowork - Agente Desktop per Knowledge Work

**Cos'e Cowork**
Cowork porta le stesse capacita agentive di Claude Code a task NON-coding. Target: qualsiasi knowledge worker, non solo sviluppatori.

**Funzionalita chiave**
- Accesso diretto a file locali (legge, modifica, crea)
- Sub-agent coordination: divide task complessi in workstream paralleli
- Genera Excel con formule, PowerPoint, bozze da appunti sparsi
- Integrazione con Google Drive, Gmail, DocuSign, FactSet, Linear, Notion, Slack
- Plugin aziendali customizzabili (financial analysis, HR, engineering)
- "Claude in Chrome" per task che richiedono il browser

**Disponibilita**
- macOS: gennaio 2026 (research preview)
- Windows: 10 febbraio 2026 (full feature parity)
- Piani: Max, Team, Enterprise (lista d'attesa per altri)
- Cowork tab richiede Apple Silicon (M1+) su macOS - non disponibile su Intel Mac

**Impatto mercato**
CNBC riporta che il lancio di Cowork ha causato un selloff di $285B in azioni enterprise software (Microsoft, Salesforce, ecc.) - segnale che il mercato lo vede come sostituto di strumenti SaaS.

---

### Claude Code Security (23 febbraio 2026 - Limited Preview)
- Scansione automatica della codebase per vulnerabilita di sicurezza
- Suggerisce patch mirate per revisione umana
- Disponibile solo come research preview limitata

---

## 2. COSA SIGNIFICA "GOOD FOR DESIGN"

La frase viene da due cose distinte:

**a) Frontend Design Plugin (ufficiale Anthropic)**
- Plugin installabile in Claude Code Desktop
- Attivazione automatica quando chiedi di creare UI/frontend
- Capacita: tipografia non-generica, animazioni scroll-triggered, composizioni asimmetriche, gradienti/texture su layer multipli
- Prima definisce un framework estetico (brutalist, maximalist, retro-futuristic, luxury, playful) poi scrive il codice
- Goal: evitare "generic AI aesthetics"

**b) Preview Live = feedback visivo immediato**
- Claude vede l'app in esecuzione, fa screenshot, clicca elementi
- Puoi selezionare elementi visivi nel preview e dare feedback direttamente
- Ciclo design-iterate molto piu veloce rispetto al CLI

**c) File attachment per design mockup**
- Desktop supporta attach di immagini e PDF
- Puoi condividere screenshot di bug, design mockup, reference documents
- CLI NON ha questa feature

In sintesi: "good for design" = la combinazione di plugin Frontend Design + preview visual + file attachment rende il Desktop il tool giusto per lavoro UI/frontend.

---

## 3. DESKTOP vs CLI - DIFFERENZE CHIAVE

### Quando usare Claude Code Desktop
- Lavoro UI/frontend (preview live, design feedback visivo)
- Code review prima del PR (diff view + commenti inline)
- Gestione PR GitHub (auto-fix CI, auto-merge)
- Sessioni parallele su task diversi
- Attach immagini e PDF al contesto
- Plugin e Connectors con UI grafica
- Utenti nuovi o che preferiscono interfaccia visuale

### Quando usare Claude Code CLI
- Scripting e automazione (`--print`, Agent SDK)
- Third-party providers: AWS Bedrock, Google Vertex, Azure Foundry (Desktop NON supporta)
- Agent teams e orchestrazione multi-agent (`subagents`)
- Linux (Desktop NON supporta Linux)
- Automation batch senza interfaccia
- Integrazione con pipeline CI/CD esistenti
- Massimo controllo con flag (`--dangerously-skip-permissions`, `dontAsk` mode)

### Condiviso tra Desktop e CLI
- Stessa engine Claude Code sotto
- CLAUDE.md e CLAUDE.local.md letti da entrambi
- MCP servers (configurati in `~/.claude.json` o `.mcp.json`)
- Hook e Skills definiti in settings
- Settings in `~/.claude.json` e `~/.claude/settings.json`
- Modelli disponibili: Sonnet, Opus, Haiku

**ATTENZIONE CRITICA:**
```
MCP servers configurati per il Claude Desktop CHAT APP
(in claude_desktop_config.json) sono SEPARATI da Claude Code!
Per usare MCP in Claude Code: configurare in ~/.claude.json o .mcp.json
```

---

## 4. DESKTOP + CLI: LAVORANO INSIEME?

SI, sono complementari e si integrano bene:

1. **Session continuity**: `/desktop` dalla CLI porta la sessione nel Desktop (macOS e Windows)
2. **Shared config**: stesse CLAUDE.md, MCP servers, hooks, settings
3. **Possono girare in parallelo** sullo stesso progetto
4. **Session history separata** ma project memory condivisa
5. **Continue in Web/Mobile**: dal Desktop puoi spostare la sessione al cloud

Il CLI rimane necessario per automazione, scripting, third-party providers, e Linux.

---

## 5. MCP SUPPORT - DOMANDA CHIAVE PER CERVELLASWARM

### Claude Desktop CHAT APP (tab Chat)
- Configura MCP in `~/Library/Application Support/Claude/claude_desktop_config.json`
- Supporta: stdio locale, Streamable HTTP
- Node.js, Python, binary MCP servers
- Desktop Extensions: installazione one-click da Settings > Extensions (come browser extensions)
- 593+ MCP servers disponibili nell'ecosistema

### Claude Code Desktop (tab Code)
- Configura MCP in `~/.claude.json` o `.mcp.json` nel progetto
- Connectors UI: Google Calendar, Slack, GitHub, Linear, Notion (MCP con setup grafico)
- Per MCP custom: aggiungere manualmente nei settings files
- Connectors = MCP servers con setup flow grafico

### Possiamo connettere il nostro MCP server CervellaSwarm?

**SI, in entrambi i modi:**

**Per Claude Desktop Chat tab:**
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "python3",
      "args": ["/path/to/cervellaswarm/mcp_server.py"]
    }
  }
}
```

**Per Claude Code Desktop (tab Code):**
```json
// ~/.claude.json o CervellaSwarm/.mcp.json
{
  "mcpServers": {
    "cervellaswarm": {
      "command": "python3",
      "args": ["/path/to/cervellaswarm/mcp_server.py"]
    }
  }
}
```

Entrambi richiedono restart dell'app dopo la configurazione.

---

## 6. IMPLICAZIONI STRATEGICHE PER CERVELLASWARM

### Opportunita

1. **Cowork e un segnale fortissimo**: Anthropic sta portando l'AI agentiva ai knowledge worker NON-tecnici. Questo e esattamente il mercato che CervellaSwarm puo servire.

2. **Desktop Extensions (one-click install)**: il meccanismo di distribuzione one-click per MCP servers e disponibile. CervellaSwarm potrebbe diventare un Desktop Extension ufficiale.

3. **MCP e lo standard**: supportato da Anthropic, OpenAI, Google, Microsoft. 593+ servers. Il nostro approccio MCP-first e allineato con la direzione del mercato.

4. **Il CLI resta il cuore per team tecnici**: agent teams, multi-agent orchestration, automation - tutto solo CLI. CervellaSwarm CLI resta differenziato per questo segmento.

### Rischi/Attenzioni

1. **Cowork fa parte di cio che CervellaSwarm propone**: confrontarsi con questa concorrenza diretta nella proposta di valore.

2. **CONFIGURAZIONI MCP SEPARATE**: Chat tab e Code tab hanno config file diversi! Da documentare bene per i nostri utenti.

3. **Desktop NON supporta Linux**: il nostro target developer su Linux deve usare CLI.

4. **Desktop NON supporta third-party providers**: chi usa AWS/GCP usa CLI. Non blocca noi (siamo Anthropic-native).

---

## RACCOMANDAZIONI

1. **PRIORITA ALTA**: documentare la configurazione MCP per CervellaSwarm in entrambi i contesti (Chat tab e Code tab). Confusione garantita senza guida chiara.

2. **MONITORARE**: Desktop Extensions marketplace - valutare submission di CervellaSwarm come extension ufficiale.

3. **POSIZIONAMENTO**: enfatizzare che CervellaSwarm aggiunge al Desktop/Code quello che Anthropic NON fornisce out-of-box: memoria persistente cross-sessione, orchestrazione swarm, protocol verification (Lingua Universale).

4. **NON CAMBIARE**: la scelta CLI-first per team tecnici e ancora la scelta giusta. Il Desktop e ottimo per individui, CLI resta il backbone per team/automation.

---

## FONTI

- [Claude.com - Preview, review, and merge with Claude Code](https://claude.com/blog/preview-review-and-merge-with-claude-code) - UFFICIALE
- [Claude.com - Introducing Cowork](https://claude.com/blog/cowork-research-preview) - UFFICIALE
- [Claude Code Docs - Use Claude Code Desktop](https://code.claude.com/docs/en/desktop) - UFFICIALE
- [Claude.com - Frontend Design Plugin](https://claude.com/plugins/frontend-design) - UFFICIALE
- [The Decoder - Claude Code desktop features](https://the-decoder.com/anthropic-updates-claude-code-with-desktop-features-that-automate-more-of-the-dev-workflow/)
- [CNBC - Anthropic Cowork office worker](https://www.cnbc.com/2026/02/24/anthropic-claude-cowork-office-worker.html)
- [VentureBeat - Cowork on Windows](https://venturebeat.com/technology/anthropics-claude-cowork-finally-lands-on-windows-and-it-wants-to-automate)
- [TechCrunch - Cowork agentic plugins](https://techcrunch.com/2026/01/30/anthropic-brings-agentic-plugins-to-cowork/)
- [support.claude.com - Getting started with local MCP servers](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [modelcontextprotocol.io - Connect local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
- [blockchain.news - Claude Code Desktop Update 2026](https://blockchain.news/ainews/claude-code-desktop-update-latest-2026-features-for-app-preview-code-review-ci-failures-and-pr-automation)
- [winbuzzer.com - Claude Code Security](https://winbuzzer.com/2026/02/23/anthropic-launches-claude-code-security-desktop-automation-xcxwbn/)
