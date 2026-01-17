# Ricerca: Best Practices Comunicazione Multi-Agent

**Data:** 17 Gennaio 2026
**Researcher:** cervella-researcher
**Contesto:** Fase 7 Casa Pulita - Migliorare comunicazione interna famiglia CervellaSwarm

---

## 1. REGOLE SEGUITE SEMPRE - Pattern Enforcement

### Runtime Enforcement (AgentSpec Framework)
**Pattern chiave:** Regole definite con `Trigger → Predicate → Action`

```
Esempio:
- Trigger: "Agent sta per scrivere file"
- Predicate: "File > 500 righe?"
- Action: "BLOCCA + Richiedi chunking"
```

**Efficacia:** 90%+ di compliance in sistemi reali (paper AgentSpec 2025)

### Dual-Layer Verification
**Best practice:** Due livelli di controllo
1. **Preventivo:** Hook pre-azione (es. pre-commit hook)
2. **Runtime:** LLM self-reflection + external validator

**Applicabile a noi:**
- Pre-commit hook ✅ (già implementato Sessione 247)
- Self-reflection: Agent si chiede "Rispetto COSTITUZIONE?" prima di output

### Deterministic Controls > Probabilistic
**Principio:** "Non fidarsi SOLO dell'LLM per regole critiche"

```
SBAGLIATO: "Ricordati di non superare 150 righe"
CORRETTO: Hook che BLOCCA scrittura se > 150 righe
```

---

## 2. DECISIONI TRA AGENTI - Propagation Patterns

### Shared Memory Architecture
**Pattern dominante:** Dual-tier memory

```
Private Memory (per agent)
  ↓
Shared Memory (read/write protocols)
  ↓
Decision Log (audit trail)
```

**Applicazione CervellaSwarm:**
- Private: Context interno agente durante task
- Shared: `.sncp/progetti/{progetto}/stato.md`
- Log: `.swarm/tasks/TASK_XXX_OUTPUT.md`

### Stigmergy (Indirect Communication)
**Definizione:** Agenti comunicano modificando ambiente condiviso

**Esempio pratico per noi:**
```
Worker Backend scrive: docs/decisioni/API_DESIGN_CHOICE.md
  ↓
Guardiana Qualita legge documento
  ↓
Valida scelta SENZA dialogo diretto
```

**Vantaggi:** No dipendenze temporali, scalabile, audit naturale

### Consensus Mechanisms
**Quando serve:** Conflitti su stesso topic

**Pattern suggerito:**
1. Timestamp + Author su ogni decisione
2. Regina risolve conflitti ESPLICITI
3. "Last write wins" per decisioni minori

---

## 3. COMPLIANCE VERIFICATION

### Real-World Pattern: "Swiss-Cheese Layering"
**Strategia:** Multipli layer di verifica

```
Layer 1: Input Gating (cosa può chiedere Regina)
Layer 2: LLM Prompt (DNA + COSTITUZIONE nel context)
Layer 3: Output Detection (verifica post-generazione)
Layer 4: External Validation (hook scripts)
```

**Per noi:**
- Layer 1: Task file structure
- Layer 2: DNA injection (già fatto!)
- Layer 3: Agent self-check
- Layer 4: Pre-commit hooks ✅

### Automated Verification Tools
**Best practice:** Script periodici che verificano compliance

**Suggerimento implementazione:**
```bash
scripts/compliance_check.sh
  - Verifica naming conventions
  - Check limiti righe
  - Valida structure SNCP
  - Report violazioni
```

**Frequenza:** Daily (come sncp_daily)

---

## 4. MEMORIA CONDIVISA - Practical Patterns

### SRMT Pattern (Shared Recurrent Memory)
**Meccanismo:** "Pool and broadcast individual memories"

**Tradotto per noi:**
1. Ogni agent scrive `.swarm/agents/{agent_id}/memory.md`
2. Script aggrega in `.swarm/shared_memory.md`
3. Agents leggono shared PRIMA di task

**Vantaggio:** Zero perdita informazioni tra sessioni

### Memory Types Implementation

| Tipo | Scope | File | Retention |
|------|-------|------|-----------|
| **STM** | Sessione | oggi.md | 1 giorno |
| **MTM** | Progetto | stato.md | Fino archivio |
| **LTM** | Globale | COSTITUZIONE.md | Permanente |

### Access Control Pattern
**Collaborative Memory with Dynamic Access:**
- Ogni agente può LEGGERE shared memory
- Solo Regina può SCRIVERE decisioni strategiche
- Workers scrivono solo in task output
- Guardiane validano, non modificano

---

## RACCOMANDAZIONI IMPLEMENTABILI

### Priorità 1: Compliance Automation
```bash
# Già fatto (Sessione 247):
- pre-commit hook ✅

# Da implementare:
- compliance_check.sh (daily)
- Agent self-reflection prompt section
```

### Priorità 2: Decision Propagation
```
Pattern Stigmergy:
1. Creare docs/decisioni/ centralizzato
2. Workers scrivono decisioni in file markdown
3. README.md indice automatico
4. Guardiane leggono prima di validare
```

### Priorità 3: Shared Memory Upgrade
```
SRMT-inspired:
1. .swarm/shared_memory.md (aggregato automatico)
2. Script post-task: aggrega output in shared
3. Hook pre-task: inietta shared in context
```

---

## FONTI

**Frameworks & Research:**
- [AgentSpec: Runtime Enforcement for LLM Agents](https://arxiv.org/pdf/2503.18666)
- [Multi-Agent Reference Architecture - Memory](https://microsoft.github.io/multi-agent-reference-architecture/docs/memory/Memory.html)
- [SRMT: Shared Memory Multi-Agent](https://arxiv.org/html/2501.13200v1)

**Practical Experience:**
- [8 Rules for Managing 20 AI Agents](https://zachwills.net/i-managed-a-swarm-of-20-ai-agents-for-a-week-here-are-the-8-rules-i-learned/)
- [Swarm Multi-Agent Pattern](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)

**Industry Standards:**
- [Agent Communication Protocol (ACP)](https://onereach.ai/blog/power-of-multi-agent-ai-open-protocols/)
- [Best Practices for AI Agent Implementations 2026](https://onereach.ai/blog/best-practices-for-ai-agent-implementations/)

---

**TL;DR:**
- **Enforcement:** Deterministic hooks > prompt-only rules
- **Decisions:** Stigmergy (write to shared docs) > direct messaging
- **Compliance:** Multi-layer verification (4+ checkpoints)
- **Memory:** STM/MTM/LTM separation + aggregation scripts

**Next Step Suggerito:** Implementare compliance_check.sh + docs/decisioni/ structure
