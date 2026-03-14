# ClawHub Publish - Research Report
**Date:** 2026-03-14
**Status:** COMPLETA
**Fonti:** 14 consultate (npm, docs.openclaw.ai, docs.claw.so, advenboost.com, github.com/openclaw/clawhub, gist, vpn07.com, digitalocean, medium, libraries.io, ququ123.top, lobehub, skillsmp.com, github topics)

---

## Sintesi Esecutiva

1. `clawhub publish` E UN COMANDO REALE - e un pacchetto npm standalone, NON pip
2. Il processo e CLI-based, non web-based (nessun form di submission)
3. Il nostro SKILL.md ha un bug critico: usa `metadata.openclaw` invece di `metadata.clawdbot`
4. SkillsMP auto-indicizza da GitHub: serve aggiungere topic `skill-md` o `skillsmp`
5. Entrambi i canali (ClawHub + SkillsMP) sono raggiungibili oggi

---

## 1. ClawHub - Risposta alle Domande

### E un comando reale?

SI. `clawhub` e un pacchetto npm standalone (v0.8.0, rilasciato gen 2026).

```bash
npm install -g clawhub
# oppure
npm i -g clawhub
```

Non e pip. Non richiede openclaw installato. Standalone CLI.

### Processo di pubblicazione

**Step 1: Installa clawhub CLI**
```bash
npm install -g clawhub
```

**Step 2: Login (GitHub OAuth)**
```bash
clawhub login
# Apre browser su https://clawhub.ai/cli/auth
# Token salvato in ~/Library/Application Support/clawhub/config.json (macOS)
# Alternativa headless: clawhub login --token clh_...
```

Prerequisito: account GitHub con almeno 1 settimana di vita.

**Step 3: Pubblica la skill**
```bash
clawhub publish ./openclaw-skill-lu/ \
  --slug lingua-universale \
  --name "Lingua Universale Protocol Verification" \
  --version 0.1.0 \
  --changelog "Initial release: 4 MCP tools for formal protocol verification"
```

**Step 4: Verifica live**
```bash
clawhub search "protocol verification"
clawhub search "lingua universale"
```

### E web-based o CLI?

CLI-based. Non esiste form web di submission documentata.
La registry ha UI web su clawhub.ai per browsing, ma il publish avviene via CLI.

---

## 2. Formato SKILL.md - Gap Critico Identificato

### BUG nel nostro SKILL.md

Il nostro SKILL.md usa `metadata.openclaw` nella riga 5:
```yaml
metadata: {"openclaw":{"emoji":"🔬","requires":{"bins":["uvx"],"env":[]}}}
```

**ClawHub ignora `metadata.openclaw`. Richiede `metadata.clawdbot`.**

Fonte: checklist 13 punti pubblicato da contributor esperto (6 iterazioni):
> "Using `metadata.openclaw` instead of `metadata.clawdbot` → ClawHub ignores this"

### SKILL.md Formato Corretto per ClawHub

```yaml
---
name: lingua-universale
version: 0.1.0
description: Verify agent-to-agent communication against session type protocols. Mathematical proofs, not trust.
author: CervellaSwarm
homepage: https://github.com/rafapra3008/cervellaswarm
tags: [protocol-verification, session-types, mcp, ai-agents, formal-methods]
user-invocable: true
metadata:
  clawdbot:
    emoji: "🔬"
    requires:
      bins:
        - uvx
      env: []
---

# Lingua Universale - Protocol Verification Skill

[... corpo del file come ora ...]
```

### Campi Richiesti

| Campo | Tipo | Status nel nostro SKILL.md |
|-------|------|---------------------------|
| `name` | string, kebab-case | OK (`lingua-universale`) |
| `description` | string | OK |
| `version` | semver | MANCANTE (necessario per publish) |
| `metadata.clawdbot` | object | BUG (usiamo `metadata.openclaw`) |
| `user-invocable` | bool | OK (`true`) |
| `author` | string | MANCANTE (raccomandato) |
| `homepage` | string | MANCANTE (raccomandato) |
| `tags` | list | MANCANTE (raccomandato) |

---

## 3. SkillsMP - Auto-Indicizzazione

### Come funziona

SkillsMP (skillsmp.com) auto-scrapa GitHub. Nessuna submission manuale richiesta.

**Processo per essere indicizzati:**
1. Repo deve essere pubblico su GitHub
2. Aggiungere topic `skill-md` al repo (Settings > Topics su GitHub)
3. Opzionalmente aggiungere topic `skillsmp`
4. SkillsMP scraper sincronizza periodicamente

**Filtro qualita:** repo con meno di 2 stelle vengono filtrati.
Il nostro repo pubblico (rafapra3008/cervellaswarm) deve avere abbastanza stelle.

**Nota importante:** SkillsMP indicherizza il repo intero, non skill specifiche.
Cerchera SKILL.md ricorsivamente nella directory del repo.
Il nostro SKILL.md e in `openclaw-skill-lu/SKILL.md` - verrebbe trovato.

### Alternativa: CLI submission

Esiste anche `agent-skills-cli` (Karanjot786) che ha comando `skills submit-repo`:
```bash
skills submit-repo rafapra3008/cervellaswarm
```
Ma e un tool community, non ufficiale.

---

## 4. Piani di Azione - Step Esatti

### Piano A: ClawHub (OGGI)

```bash
# 1. Installa clawhub CLI
npm install -g clawhub

# 2. Fix SKILL.md (vedere sezione 2 sopra)
# Cambia metadata.openclaw -> metadata.clawdbot
# Aggiungi version, author, homepage, tags

# 3. Login
clawhub login

# 4. Publish
clawhub publish /Users/rafapra/Developer/CervellaSwarm/openclaw-skill-lu/ \
  --slug lingua-universale \
  --name "Lingua Universale Protocol Verification" \
  --version 0.1.0 \
  --changelog "4 MCP tools: formal protocol verification for AI agent communication"

# 5. Verifica
clawhub search "protocol verification"
```

### Piano B: SkillsMP (OGGI, 2 min)

```bash
# Sul repo pubblico rafapra3008/cervellaswarm su GitHub:
# Settings > Topics > Aggiungere: skill-md, skillsmp, mcp, protocol-verification
```

SkillsMP truvera automaticamente `openclaw-skill-lu/SKILL.md`.

### Piano C: PR su awesome-openclaw-skills (BONUS)

Il repo VoltAgent/awesome-openclaw-skills (curated list) accetta PR.
Aggiungere `lingua-universale` in categoria Security o AI/ML.
Visibilita extra per Show HN.

---

## 5. Comandi ClawHub Completi (Referenza)

```bash
# Auth
clawhub login                    # browser OAuth
clawhub login --token clh_...    # headless
clawhub logout
clawhub whoami

# Discovery
clawhub search "protocol verification"
clawhub explore
clawhub inspect lingua-universale

# Install/manage
clawhub install <slug>
clawhub update --all
clawhub list

# Publish
clawhub publish <path>           # minimal
clawhub publish <path> --slug <slug> --name <name> --version <version> --changelog <text>
clawhub sync                     # pubblica tutti i nuovi/modificati in workspace
clawhub sync --all --no-input --force

# Admin (owner)
clawhub delete <slug>
clawhub skill rename <old> <new>
```

---

## 6. Note Tecniche

### Sicurezza: ClawHub Security Scan
ClawHub esegue security scan 2-layer (regex + LLM Claude) prima di pubblicare.
Il nostro skill e SAFE: nessun exec di user input, solo parsing di testo .lu.

### MCP server = Skill
Confermato: "Every skill on ClawHub is an MCP server."
Il nostro `lu_mcp_server.py` con FastMCP e il formato esatto atteso.

### uvx compatibility
Il nostro install via `uvx openclaw-skill-lingua-universale` e il pattern standard su ClawHub.
Il file `requires.bins: [uvx]` nel SKILL.md e corretto.

### token config path (macOS)
Config token in: `~/Library/Application Support/clawhub/config.json`
Override: env var `CLAWHUB_CONFIG_PATH`

---

## 7. Warning: Piattaforme Ibride Rilevate

La ricerca ha trovato CMDOP.com (menzionato nel contesto originale).
CMDOP e una piattaforma diversa (workflow automation), NON la stessa cosa di ClawHub.
`clawhub` npm package != CMDOP. Non confondere.

LobeHub.com mostra anche skill pages (es: `lobehub.com/skills/openclaw-skills-clawhud`).
LobeHub auto-indicizza da ClawHub, non serve submission separata.

---

## Raccomandazione

**Ordine di esecuzione:**

1. **SUBITO (5 min):** Fix SKILL.md - cambia `metadata.openclaw` -> `metadata.clawdbot`, aggiungi `version`, `author`, `homepage`, `tags`

2. **SUBITO (2 min):** Aggiungere topic `skill-md` e `skillsmp` al repo GitHub pubblico (rafapra3008/cervellaswarm)

3. **OGGI (10 min):** `npm install -g clawhub` + `clawhub login` + `clawhub publish`

4. **BONUS:** PR su VoltAgent/awesome-openclaw-skills

Il prerequisito tecnico critico e solo il fix di `metadata.clawdbot`.
Tutto il resto del nostro SKILL.md e corretto (struttura, contenuto, tools descritti).

---

## Appendice: Fix Preciso SKILL.md

Cambiare frontmatter da:
```yaml
---
name: lingua-universale
description: Verify agent-to-agent communication against session type protocols. Mathematical proofs, not trust.
user-invocable: true
metadata: {"openclaw":{"emoji":"🔬","requires":{"bins":["uvx"],"env":[]}}}
---
```

A:
```yaml
---
name: lingua-universale
version: 0.1.0
description: Verify agent-to-agent communication against session type protocols. Mathematical proofs, not trust.
author: CervellaSwarm
homepage: https://github.com/rafapra3008/cervellaswarm
tags: [protocol-verification, session-types, mcp, ai-agents, formal-methods]
user-invocable: true
metadata:
  clawdbot:
    emoji: "🔬"
    requires:
      bins:
        - uvx
      env: []
---
```

Nessun cambiamento al corpo del file (tutto il markdown dopo il frontmatter rimane identico).
