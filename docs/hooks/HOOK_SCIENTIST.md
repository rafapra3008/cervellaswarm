# 🔬 Hook: La Scienziata (SessionStart)

**File:** `~/.claude/hooks/session_start_scientist.py`
**Versione:** 1.0.0
**Data:** 1 Gennaio 2026

---

## 🎯 SCOPO

Hook che si attiva automaticamente a ogni SessionStart per:
1. Rilevare il progetto attivo
2. Determinare il dominio di ricerca (tech, competitors)
3. Generare un prompt per cervella-researcher
4. Salvare il prompt in `reports/scientist_prompt_[DATE].md`

La Regina può poi invocare cervella-researcher per eseguire la ricerca.

---

## 🏗️ COME FUNZIONA

```
SessionStart Hook
       ↓
session_start_scientist.py
       ↓
1. Riceve JSON con cwd
2. Rileva progetto da cwd
3. Determina dominio (tech, domain, competitors)
4. Genera prompt per cervella-researcher
5. Salva prompt in reports/scientist_prompt_[DATE].md
       ↓
La Regina invoca cervella-researcher (quando vuole)
       ↓
cervella-researcher esegue ricerca
       ↓
Scrive report in reports/DAILY_RESEARCH_[DATE].md
```

---

## 📊 PROGETTI SUPPORTATI

| Progetto | Emoji | Tech | Competitors |
|----------|-------|------|-------------|
| **CervellaSwarm** | 🐝 | Python, Claude Code, Multi-agent, SQLite | LangGraph, CrewAI, AutoGPT |
| **Miracollo PMS** | 🏨 | React, Vite, TailwindCSS, FastAPI, SQLite | Lodgify, Guesty, Hostaway |
| **Contabilità** | 💰 | FastAPI, SQLite, Jinja2, HTMX | YNAB, Mint, Spendee |
| **Libertaio** | 💡 | React, TailwindCSS, FastAPI, SQLite | (da definire) |

**Progetti sconosciuti:** Hook logga ma non genera prompt (evita errori).

---

## 📝 OUTPUT

### File generato: `reports/scientist_prompt_[DATE].md`

Contiene:
- Progetto e emoji
- Tecnologie usate
- Dominio applicativo
- Competitor da monitorare
- Missione (cosa cercare)
- Output atteso (formato report)
- Configurazione ricerca

### Esempio (CervellaSwarm):

```markdown
# 🔬 SCIENTIST PROMPT - 2026-01-01

## Progetto: CervellaSwarm 🐝

### Dominio di Ricerca

**Tecnologie usate:**
- Python
- Claude Code
- Multi-agent
- SQLite

**Dominio applicativo:**
- AI Orchestration
- Agent Systems
- Automation

**Competitor da monitorare:**
- LangGraph
- CrewAI
- AutoGPT

---

## 🎯 MISSIONE

Cerca e analizza:
1. Novità Tecnologie (ultimi 30 giorni)
2. Competitor Updates
3. Trend del Dominio
4. Opportunità

---

## 📝 OUTPUT ATTESO

Scrivi il report in: `reports/DAILY_RESEARCH_20260101.md`

[struttura report...]
```

---

## 🧪 TEST

```bash
# Test con CervellaSwarm
echo '{"session_id": "test", "cwd": "/Users/rafapra/Developer/CervellaSwarm"}' | \
  ~/.claude/hooks/session_start_scientist.py

# Output:
# [2026-01-01 18:56:04] 🔬 La Scienziata ATTIVATA
#   Progetto: 🐝 CervellaSwarm
#   Prompt salvato: /Users/rafapra/Developer/CervellaSwarm/reports/scientist_prompt_20260101.md

# Test con progetto sconosciuto
echo '{"session_id": "test", "cwd": "/Users/rafapra/Developer/unknown"}' | \
  ~/.claude/hooks/session_start_scientist.py

# Output:
# [2026-01-01 18:56:18] 🔬 La Scienziata ATTIVATA
#   Progetto: 📁 Unknown
#   Prompt salvato: (non generato - progetto sconosciuto)
#   ⚠️ Progetto sconosciuto - dominio non definito
```

---

## 🔧 CONFIGURAZIONE

Per aggiungere un nuovo progetto, modificare `PROJECT_DOMAINS` in `session_start_scientist.py`:

```python
"nome-folder-progetto": {
    "name": "Nome Progetto",
    "emoji": "🎨",
    "tech": ["Tech1", "Tech2"],
    "domain": ["Dominio1", "Dominio2"],
    "competitors": ["Competitor1", "Competitor2"]
}
```

---

## 🐝 INTEGRAZIONE CON SWARM

La Regina (cervella-orchestrator) può invocare cervella-researcher così:

```markdown
Sono la Regina. Delego a cervella-researcher:

Leggi il prompt in reports/scientist_prompt_20260101.md
ed esegui la ricerca come indicato.

Scrivi il report in reports/DAILY_RESEARCH_20260101.md
```

---

## 📊 LOG

Il hook logga in console (stderr) per debug:
```
[2026-01-01 18:56:04] 🔬 La Scienziata ATTIVATA
  Progetto: 🐝 CervellaSwarm
  Prompt salvato: /path/to/reports/scientist_prompt_20260101.md
```

**Non logga nel database** (la Regina può farlo se necessario).

---

## ✅ COMPLETATO

- [x] Hook creato e funzionante
- [x] Test con progetti conosciuti
- [x] Test con progetti sconosciuti
- [x] Documentazione completa
- [x] Gestione errori graceful
- [x] Directory reports/ creata automaticamente

---

*Creato: 1 Gennaio 2026*
*Cervella Backend 🐍*
