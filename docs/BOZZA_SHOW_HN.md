# BOZZA POST SHOW HN - CervellaSwarm

> **Status:** BOZZA - Pronta per review Rafa
> **Data lancio:** Martedì 21 Gennaio 2026
> **Orario consigliato:** 8-10 AM Eastern Time (14:00-16:00 ora italiana)

---

## TITOLO (max 80 caratteri)

```
Show HN: CervellaSwarm – 16 AI agents that check each other's work
```

**Perché funziona:**
- Numero specifico (16) = tangibile, non vago
- "check each other's work" = USP chiaro in 4 parole
- Zero marketing speak
- Pattern provato (top CLI tools HN)

---

## URL

```
https://github.com/rafapra3008/CervellaSwarm
```

---

## PRIMO COMMENTO (CRITICO - postare IMMEDIATAMENTE dopo il post)

```markdown
Hi HN,

Rafa here, creator of CervellaSwarm.

**The Problem:**
I love AI coding assistants, but they have a fatal flaw: they don't check their own work.

I've watched Claude write beautiful code, then break it 10 minutes later trying to add a feature. Or confidently generate tests that don't actually run.

**The Solution:**
What if AI could check its OWN work BEFORE touching your codebase?

That's CervellaSwarm: a team of 16 specialized AI agents with a critical architectural difference:

→ 12 Workers do the work (frontend, backend, testing, research, docs, security, etc.)
→ 3 Guardians ONLY review and validate (quality, ops, specialized checks)
→ 1 Regina orchestrates everything

Workers propose changes. Guardians validate. Code merges only after passing QA.

**Why This Works:**
- Guardians use Claude Opus (stronger reasoning for QA)
- Workers use Sonnet (fast execution)
- Each Guardian has veto power
- Result: Code that's been reviewed by AI experts BEFORE it touches your repo

**Try It Now:**

CLI:
    npm install -g cervellaswarm
    cervellaswarm doctor

MCP Server (for Claude Desktop):
    npm install -g @cervellaswarm/mcp-server

**What I'd Love Feedback On:**
1. Is the "AI team that checks itself" concept compelling?
2. Would you trust AI QA more if it was specialized agents vs general assistant?
3. What's your biggest hesitation with multi-agent systems?

GitHub: https://github.com/rafapra3008/CervellaSwarm
Demo: [collaboration_flow image in README]

Thanks for checking it out! Happy to answer any questions.

- Rafa
```

---

## RISPOSTE PRE-PREPARATE

### Se chiedono "Why not just use one AI?"

```
Good question! Single AI = single perspective. Our tests show that specialized agents (backend expert, security expert, tester) catch different types of issues.

The key innovation isn't the number of agents, it's the SEPARATION between "doers" and "checkers". Workers never review their own work - Guardians do.

Think of it like pair programming, but with specialized roles.
```

### Se chiedono "Isn't this expensive (tokens)?"

```
Fair point. Multi-agent = more tokens. But consider the alternative:

Option A: Single AI writes code, you find bugs later, fix cycle
Option B: 16 agents, Guardians catch issues BEFORE merge

We've found the extra tokens upfront saves debugging time downstream. The Guardians use Opus (better at QA), Workers use Sonnet (faster, cheaper).

For teams already paying for AI assistants, the ROI is in fewer production bugs.
```

### Se chiedono "How is this different from [competitor]?"

```
Great question. Most multi-agent systems focus on collaboration - agents working together.

CervellaSwarm focuses on VALIDATION - dedicated QA agents whose only job is to find problems in other agents' work.

The 3 Guardians don't write code. They only review. That specialization is the key difference.
```

### Se sono critici/negativi

```
Appreciate the feedback. You raise a valid point about [X].

[Address with data/reasoning, not defensively]

Happy to discuss further if helpful.
```

---

## CHECKLIST PRE-LANCIO

### 2-3 giorni prima (18-19 Gennaio)
- [ ] README impeccabile con hero image
- [ ] `npm install -g cervellaswarm` funziona perfettamente
- [ ] `cervellaswarm doctor` mostra output pulito
- [ ] MCP server testato in Claude Desktop
- [ ] GIF/video demo pronto (opzionale ma consigliato)

### Giorno prima (20 Gennaio)
- [ ] Primo commento scritto e pronto (copy-paste)
- [ ] Risposte pre-preparate pronte
- [ ] Notifiche HN attive
- [ ] 6 ore libere per engagement

### Launch day (21 Gennaio)
- [ ] Postare 8-10 AM Eastern (14:00-16:00 IT)
- [ ] Account personale Rafa (non @cervellaswarm)
- [ ] Primo commento IMMEDIATO
- [ ] Refresh ogni 5-10 minuti per 6 ore
- [ ] Rispondere a OGNI commento (target: < 15 min)

---

## REGOLE ENGAGEMENT

**DA FARE:**
- Rispondere a OGNI commento
- Essere tecnico e onesto
- Ringraziare per feedback (anche negativo)
- Ammettere limitazioni quando vere

**DA NON FARE:**
- MAI chiedere upvotes
- MAI condividere link su Discord/Slack per "supporto"
- MAI essere difensivo
- MAI usare marketing speak ("revolutionary", "game-changing")

---

## MESSAGGI CHIAVE (da ripetere)

```
"The only AI coding team that checks its own work"

"Workers do the work. Guardians validate. Code merges only after QA."

"16 brains are better than one - especially when 3 of them are QA experts."

"Think of it like pair programming, but with specialized AI roles."
```

---

## NOTE

**Account da usare:** Account personale Rafa (più autentico)

**Timing:** Martedì 21 Gennaio 2026 è perfetto (early week, staff HN attivo)

**Aspettative realistiche:**
- Front page = great success
- 100+ upvotes = solid launch
- 50+ upvotes = good start
- Qualsiasi numero = learning experience

---

*Bozza creata: 18 Gennaio 2026 - Sessione 255*
*"The only AI coding team that checks its own work"*
