# RICERCA HANDOFFS IMPLEMENTATION - Claude Code CLI

> **Data:** 2 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **REGOLA 11:** PERCHÉ → RICERCA → VERIFICA PERCHÉ

---

## EXECUTIVE SUMMARY

### TL;DR - RISPOSTA AL PERCHÉ

**RISPONDE AL NOSTRO PERCHÉ?** ✅ **SÌ, MA CON LIMITAZIONI**

Claude Code CLI **NON** supporta handoffs automatici nativi. Però:

1. **Possiamo IMPLEMENTARLI NOI** usando hooks + prompt engineering
2. **Effort stimato:** 4-8 ore per implementazione base
3. **Pattern consigliato:** "Orchestrator with Explicit Handoffs"
4. **Limitazione chiave:** No nesting (subagent non può spawnare altri subagent)

---

## LIMITAZIONI TECNICHE CONFERMATE

### 1. NO Nested Subagents

> "Subagents cannot spawn their own subagents. Don't include Task in a subagent's tools array."
> - Documentazione ufficiale Anthropic

**Cosa significa:**
- ❌ Frontend NON può invocare direttamente Tester via Task tool
- ✅ Solo la Regina (main agent) può invocare subagent
- ✅ Serve pattern "back to orchestrator"

### 2. Context Isolation

> "Sub-agents start fresh with no conversation history"

- Ogni subagent parte con context VUOTO
- Passare info via prompt o file condivisi
- Possiamo usare swarm_memory.db per state

---

## OPZIONI IMPLEMENTAZIONE

### OPZIONE 1: Prompt Template (0 ore) ⭐

**Approccio:** Includere workflow chain nel prompt

```markdown
## TASK PER @cervella-frontend

### ⚡ WORKFLOW CHAIN
1. ✅ @cervella-backend (API creata)
2. → @cervella-frontend (TU - crea UI) ← SEI QUI
3. → @cervella-tester (testa integrazione)
4. → @cervella-reviewer (review finale)

**IMPORTANTE:** Nel risultato finale, scrivi:
"⚡ NEXT: @cervella-tester - testare integrazione"
```

**PRO:** Zero codice, funziona SUBITO
**CONTRO:** Manuale, agent può dimenticare

### OPZIONE 2: SubagentStop Hook (4-6 ore) ⭐

**Approccio:** Hook suggerisce prossimo agent

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

WORKFLOWS = {
    "full-stack": ["cervella-backend", "cervella-frontend", "cervella-tester", "cervella-reviewer"],
    "research-doc": ["cervella-researcher", "cervella-docs"],
}

def main():
    payload = json.loads(sys.stdin.read())
    agent_type = payload.get("tool_input", {}).get("subagent_type")

    # Carica workflow attivo da file
    workflow_file = Path.cwd() / ".active-workflow"
    if workflow_file.exists():
        workflow = workflow_file.read_text().strip()
        if workflow in WORKFLOWS:
            chain = WORKFLOWS[workflow]
            if agent_type in chain:
                idx = chain.index(agent_type)
                if idx < len(chain) - 1:
                    print(f"\n🔗 HANDOFF: Next → @{chain[idx+1]}\n")

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**PRO:** Automatico, tracciabile
**CONTRO:** Regina deve leggere e delegare

### OPZIONE 3: Queue System (6-8 ore)

**Approccio:** File .workflow-queue.json con task chain

```json
{
  "workflow_id": "sprint-3.2",
  "tasks": [
    {"agent": "cervella-backend", "description": "Create API", "completed": false},
    {"agent": "cervella-frontend", "description": "Build UI", "completed": false},
    {"agent": "cervella-tester", "description": "Test integration", "completed": false}
  ]
}
```

**PRO:** Workflow complessi, debuggabile
**CONTRO:** Setup richiesto

---

## PATTERN CONSIGLIATO (Anthropic)

> "In production, the most stable agents follow a simple rule: give each subagent one job, and let an orchestrator coordinate."

**Applicato a CervellaSwarm:**
- Regina coordina
- Worker eseguono ONE job
- Handoff esplicito via return message

---

## RACCOMANDAZIONE

### Fase 1 - SUBITO (0 ore)
Prompt template con sezione "⚡ WORKFLOW CHAIN"

### Fase 2 - SHORT TERM (4-6 ore)
SubagentStop hook per suggerimenti automatici

### Fase 3 - MEDIUM TERM (6-8 ore)
Queue system per workflow complessi (se serve)

---

## EFFORT TOTALE

| Feature | Ore |
|---------|-----|
| Prompt template | 0h |
| SubagentStop hook | 4-6h |
| Queue system | 6-8h |
| **MVP** | **4-6h** |

---

**Autrice:** Cervella Researcher 🔬
**Modalità:** "Noi Mode" - Creiamo NOI il sistema handoffs!
