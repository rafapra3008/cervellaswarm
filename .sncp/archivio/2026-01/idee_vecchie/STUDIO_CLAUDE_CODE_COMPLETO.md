# Studio Claude Code - Completo

> **Data:** 9 Gennaio 2026 - Sessione 141
> **Obiettivo:** Capire come costruire CervellaSwarm come prodotto
> **Status:** RICERCA COMPLETATA

---

## SCOPERTA PRINCIPALE

**CervellaSwarm può essere distribuito come PLUGIN ufficiale Claude Code!**

I plugin sono il metodo ufficiale per distribuire:
- Configurazioni
- Agenti custom
- Comandi
- Hooks

---

## 1. SUBAGENTS - Come Funzionano

### Cosa Sono

Subagents sono istanze Claude separate con:
- Proprio context window
- Proprie istruzioni
- Propri permessi tool

### Come Si Creano

**Metodo 1: Flag --agents (runtime)**

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**Metodo 2: Dentro Plugin (persistente)**

I plugin possono includere definizioni di subagents che persistono.

### Parametri Subagent

| Parametro | Descrizione | Obbligatorio |
|-----------|-------------|--------------|
| `description` | Descrizione breve (quando usarlo) | SI |
| `prompt` | System prompt dell'agente | SI |
| `tools` | Lista tool permessi | NO (default: tutti) |
| `model` | Modello (sonnet/opus/haiku) | NO (default: eredita) |

### Tools Disponibili

```
Read, Write, Edit, Glob, Grep, Bash,
WebSearch, WebFetch, Task, TodoWrite,
NotebookEdit, AskUserQuestion, etc.
```

### Nostri 16 Agenti → Subagents

I nostri file in `~/.claude/agents/` possono diventare definizioni ufficiali di subagents!

---

## 2. PLUGINS - Come Funzionano

### Cosa Sono

Plugin = pacchetto che installa con un comando:
- Slash commands
- Subagents
- MCP servers
- Hooks

### Struttura Plugin

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json        # Manifest principale
│   ├── marketplace.json   # Per marketplace (opzionale)
│   └── commands/          # Slash commands
│       └── my-command.md
├── agents/                # Definizioni subagents
│   └── my-agent.json
├── hooks/                 # Hook scripts
│   └── pre-commit.sh
└── README.md
```

### plugin.json (Manifest)

```json
{
  "name": "cervellaswarm",
  "version": "1.0.0",
  "description": "AI Team per Dev Professionali",
  "author": "Rafa",
  "commands": ["./commands/"],
  "agents": ["./agents/"],
  "hooks": ["./hooks/"],
  "mcpServers": {}
}
```

### Come Si Installano

```bash
# Da URL
/plugin install https://github.com/user/my-plugin

# Da marketplace
/plugin marketplace add user/repo
/plugin install plugin-name
```

### Come Si Distribuiscono

**Opzione A: GitHub Repository**
- Pubblica il plugin su GitHub
- Altri installano con URL

**Opzione B: Marketplace**
- Crea `marketplace.json`
- Pubblica il marketplace
- Altri aggiungono il marketplace e installano

---

## 3. DISTRIBUZIONE - Opzioni

### Opzione 1: Plugin GitHub (Consigliata)

```
Utente esegue:
/plugin install https://github.com/cervellaswarm/plugin

Risultato:
- 16 agenti installati
- Comandi custom installati
- Hooks configurati
- SNCP template creato
```

**Pro:** Semplice, ufficiale, un comando
**Contro:** Richiede Claude Code installato

### Opzione 2: Marketplace Proprio

```
1. Creiamo marketplace.json
2. Pubblichiamo su GitHub
3. Utenti aggiungono:
   /plugin marketplace add cervellaswarm/marketplace
4. Poi installano:
   /plugin install cervellaswarm
```

**Pro:** Più "professionale", controllo versioni
**Contro:** Un passo in più

### Opzione 3: npm Package + Plugin

```bash
npm install -g cervellaswarm
cervellaswarm init
# Questo installa il plugin automaticamente
```

**Pro:** Familiare per dev, può fare setup extra
**Contro:** Più complesso da sviluppare

---

## 4. COSA POSSIAMO FARE

### MVP Minimo (Plugin Base)

Creare un plugin che include:
1. **16 Subagents** - Le nostre Cervelle
2. **Comandi custom** - /spawn-backend, /spawn-frontend, etc.
3. **Template SNCP** - Struttura cartelle

### MVP Medio (Plugin + CLI)

Aggiungere:
4. **CLI wrapper** - `cervellaswarm` command
5. **Setup wizard** - Configurazione guidata
6. **Dashboard web** - Monitoring (opzionale)

---

## 5. ARCHITETTURA PROPOSTA

```
┌─────────────────────────────────────────────────────────────────┐
│                     CERVELLASWARM PLUGIN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  .claude-plugin/                                                │
│  ├── plugin.json          # Manifest                           │
│  └── commands/                                                  │
│      ├── spawn-backend.md                                       │
│      ├── spawn-frontend.md                                      │
│      └── ...                                                    │
│                                                                 │
│  agents/                                                        │
│  ├── cervella-backend.json                                      │
│  ├── cervella-frontend.json                                     │
│  ├── cervella-tester.json                                       │
│  └── ... (16 agenti)                                            │
│                                                                 │
│  templates/                                                     │
│  └── sncp/                # Template struttura SNCP             │
│      ├── idee/                                                  │
│      ├── memoria/                                               │
│      └── coscienza/                                             │
│                                                                 │
│  hooks/                                                         │
│  └── session-start.sh     # Setup automatico                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. PROSSIMI STEP

| Step | Azione | Priorità |
|------|--------|----------|
| 1 | Studiare struttura plugin esistenti | ALTA |
| 2 | Convertire nostri agenti in formato JSON | ALTA |
| 3 | Creare plugin.json base | ALTA |
| 4 | Testare installazione plugin | ALTA |
| 5 | Creare comandi custom | MEDIA |
| 6 | Aggiungere template SNCP | MEDIA |
| 7 | Testare su computer pulito | ALTA |

---

## 7. FONTI

- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Create Plugins](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [GitHub anthropics/claude-code](https://github.com/anthropics/claude-code)
- [Claude Code Plugins Blog](https://claude.com/blog/claude-code-plugins)
- [feiskyer/claude-code-settings](https://github.com/feiskyer/claude-code-settings)

---

## 8. CONCLUSIONE

**La strada è chiara:**

CervellaSwarm diventa un **Plugin Claude Code ufficiale**.

Questo significa:
- Installazione con UN COMANDO
- Distribuzione ufficiale
- Aggiornamenti facili
- Compatibilità garantita

**Il prodotto esiste già** (i nostri 16 agenti + SNCP).
Dobbiamo solo **impacchettarlo** nel formato plugin.

---

## 9. ANALISI NOSTRI AGENTI ATTUALI

### Dove Sono

```
~/.claude/agents/
├── cervella-backend.md
├── cervella-frontend.md
├── cervella-tester.md
├── cervella-reviewer.md
├── cervella-researcher.md
├── cervella-docs.md
├── cervella-data.md
├── cervella-devops.md
├── cervella-security.md
├── cervella-marketing.md
├── cervella-scienziata.md
├── cervella-ingegnera.md
├── cervella-orchestrator.md
├── cervella-guardiana-qualita.md
├── cervella-guardiana-ops.md
└── cervella-guardiana-ricerca.md
```

### Struttura Attuale (Markdown con YAML frontmatter)

```yaml
---
name: cervella-backend
version: 1.0.0
updated: 2026-01-02
compatible_with: cervellaswarm >= 1.0.0
description: Specialista Python, FastAPI...
tools: Read, Edit, Bash, Glob, Grep, Write, WebSearch, WebFetch
model: sonnet
---

# Cervella Backend

[Contenuto markdown con istruzioni...]
```

### Cosa Contengono

Ogni agente ha:

| Sezione | Descrizione |
|---------|-------------|
| Frontmatter YAML | Metadati (name, tools, model) |
| PRIMA DI TUTTO | Link a COSTITUZIONE.md |
| REGOLA DECISIONE AUTONOMA | Quando procedere/fermarsi |
| DNA DI FAMIGLIA | Filosofia CervellaSwarm |
| REGOLE CONTEXT-SMART | Come gestire il contesto |
| Specializzazioni | Cosa sa fare |
| Zone di Competenza | File che può/non può toccare |
| Output Atteso | Formato risposte |
| Protocolli Swarm | Comunicazione con Regina |

### Conversione Necessaria

Per diventare plugin, dobbiamo:

1. **Estrarre frontmatter** → JSON per plugin
2. **Contenuto markdown** → Prompt per subagent
3. **Tools** → Array nel JSON
4. **Model** → Parametro nel JSON

### Esempio Conversione

**Da (attuale):**
```yaml
---
name: cervella-backend
tools: Read, Edit, Bash, Glob, Grep, Write
model: sonnet
---
# Cervella Backend
[istruzioni...]
```

**A (plugin format):**
```json
{
  "cervella-backend": {
    "description": "Specialista Python, FastAPI, Database, API REST",
    "prompt": "# Cervella Backend\n[istruzioni...]",
    "tools": ["Read", "Edit", "Bash", "Glob", "Grep", "Write"],
    "model": "sonnet"
  }
}
```

### Valore Aggiunto Nostro

Cosa rende i nostri agenti UNICI:

| Caratteristica | Descrizione |
|----------------|-------------|
| **Filosofia** | "Lavoriamo in PACE!" |
| **Identità** | Parlano al femminile, hanno personalità |
| **SNCP** | Sistema memoria esterna integrato |
| **Protocolli** | Comunicazione strutturata |
| **Guardiane** | 3 agenti Opus per supervisione |
| **Regole Context** | Gestione token ottimizzata |

---

## 10. MVP CONCRETO

### Cosa Include MVP v1.0

```
cervellaswarm-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── cervella-backend.json
│   ├── cervella-frontend.json
│   ├── cervella-tester.json
│   └── ... (tutti 16)
├── commands/
│   └── init-sncp.md          # Comando per inizializzare SNCP
├── templates/
│   └── sncp/
│       ├── idee/
│       ├── memoria/
│       └── coscienza/
└── README.md
```

### Cosa NON Include MVP v1.0

- CLI wrapper separato
- Dashboard web
- Sistema di pagamento
- Autenticazione

### Risultato Per L'Utente

```bash
# Utente installa Claude Code
npm install -g @anthropic-ai/claude-code

# Utente installa CervellaSwarm
/plugin install https://github.com/cervellaswarm/plugin

# Utente inizializza progetto
/init-sncp

# Utente usa i 16 agenti!
# (automaticamente disponibili nel Task tool)
```

---

*"La soluzione era sotto i nostri occhi!"*

*Studio completato: 9 Gennaio 2026*
