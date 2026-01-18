# Show HN Post - CervellaSwarm

> **Status:** PRONTO PER LANCIO
> **Data target:** Domenica 26 Gennaio 2026, 12:00 UTC (13:00 Italia)
> **Preparato:** Sessione 261 - 18 Gennaio 2026

---

## TITOLO

```
Show HN: CervellaSwarm – 16 AI agents + 3 quality guardians, coordinated via MCP
```

---

## LINK DA POSTARE

```
https://github.com/rafapra3008/CervellaSwarm
```

---

## PRIMO COMMENTO (postare entro 5 minuti dal post)

```
Hey HN! I'm Rafa, the founder of CervellaSwarm.

Two years ago, I was stuck. Working a job that didn't fit, living through some rough times in Brazil, then moving to Italy after COVID looking for a fresh start. I needed change - not just geographically, but mentally.

I went deep on personal development, habits, mindset. Then AI happened. I saw the opportunity and thought: "I can actually do this."

But working with AI agents was... chaotic. Context limits. Lost state. Switching between conversations. Repeating yourself 50 times. I kept thinking: "There has to be a better way."

So I built CervellaSwarm. 260+ work sessions later, it's real.

**What it is:**
- 16 specialized AI agents (1 orchestrator "Regina" + 3 quality/security/ops guardians + 12 workers)
- MCP-native (Model Context Protocol) - agents communicate like a real team
- Privacy-first: your code stays local, no cloud sync required
- CLI + MCP server ready to plug into Claude Desktop

**What makes it different:**
- Agents have *persistent memory* across sessions (SNCP system)
- They *coordinate* - backend talks to frontend, marketing validates UX before implementation
- Built by someone who actually uses it daily for 3 production projects

**Try it:**
```
npx cervellaswarm init
npx cervellaswarm task "add login page"
```

Free tier available. Apache-2.0 licensed.

**What I need from you:**
- Does this solve a real problem for you?
- What would make you actually use it vs regular Claude?
- Any dealbreakers in the architecture?

I don't know where all this energy and knowledge came from. What we're doing with AI feels "incredible, real, and magical at the same time." But it works. And I'd love your honest feedback.

GitHub: https://github.com/rafapra3008/CervellaSwarm
```

---

## TIMING

| Cosa | Quando |
|------|--------|
| **Post su HN** | Domenica 26 Gennaio, 12:00 UTC |
| **Ora Italia** | 13:00 |
| **Primo commento** | Entro 5 minuti dal post |
| **Monitoring** | Ogni 30 min per prime 2 ore |

---

## CHECKLIST PRE-LANCIO

### 48h Prima (24-25 Gennaio)
- [x] Test `npx cervellaswarm init` su macchina pulita (Sessione 262)
- [x] Verificare README GitHub sia chiaro (Sessione 262)
- [x] Preparare risposte FAQ comuni

### 24h Prima (25 Gennaio)
- [ ] Rileggere titolo e commento
- [ ] Verificare link GitHub funzioni
- [ ] Avvisare Rafa del timing

### Il Giorno (26 Gennaio)
- [ ] Post alle 12:00 UTC esatte
- [ ] Primo commento entro 5 min
- [ ] Monitoring attivo
- [ ] Rispondere ai commenti entro 1 ora

---

## FAQ PREPARATE (10 FAQ)

### FAQ 1: Different from Claude
**Q: How is this different from using Claude directly?**
A: Instead of one generic assistant losing context, you have 16 specialists that coordinate. The backend agent talks to frontend, marketing validates UX decisions, and 3 guardians verify quality before any output is accepted.
**TL;DR:** 16 specialists + 3 quality reviewers > 1 generic assistant.

### FAQ 2: API Key
**Q: Does it require Anthropic API key?**
A: Yes, for the workers (Sonnet-based). Free tier uses your own API key directly - no rate limiting beyond Anthropic's own limits, no middleman.
**TL;DR:** Your API key, your control, no hidden limits.

### FAQ 3: SNCP
**Q: What's SNCP?**
A: Sistema Nervoso Centrale Persistente - our persistent memory system. Agents remember context across sessions, so you don't start from zero every time.
**TL;DR:** Persistent memory = no more repeating yourself.

### FAQ 4: MCP
**Q: Why MCP and not direct API?**
A: MCP is Anthropic's standard protocol. It means CervellaSwarm works with Claude Desktop, Continue.dev, or any MCP-compatible client. Future-proof.
**TL;DR:** Industry standard protocol = works everywhere, future-proof.

### FAQ 5: Privacy
**Q: What about privacy? Where does my code go?**
A: Your code stays 100% local. Here's exactly what happens:
- **LOCAL (never leaves your machine):** All source files, SNCP memory/state, Agent coordination logic
- **SENT TO ANTHROPIC API:** Task prompts, Code snippets relevant to current task, Uses YOUR API key directly
- **WHAT ANTHROPIC DOES:** Zero data retention for API usage, No training on API data
**TL;DR:** We never see your code. Anthropic processes but doesn't retain it. Your API key, your control.

### FAQ 6: Pricing
**Q: What does this cost? Real numbers please.**
A: No hidden fees. Here's the real math:
- **FREE TIER:** Uses YOUR Anthropic API key directly. Typical cost per task: $0.01-0.05. Full-time dev monthly: ~$20-50 in API calls. No middleman markup.
- **COMPARISON:** CervellaSwarm $0 + API (~$20-50/mo) | Cursor Pro $20/mo + usage | GitHub Copilot $10/mo
**TL;DR:** Free to start. ~$30/month typical for daily use. Cheaper than Cursor, more agents than Copilot.

### FAQ 7: Security
**Q: What about security? Can agents run arbitrary code?**
A: Honest answer: AI agents have risks. Here's how we handle them:
- **PROTECTIONS:** No arbitrary shell commands without approval, File operations require permission, Guardian validation before accepting outputs, MCP tools sandboxed
- **KNOWN RISKS (transparent):** Prompt injection mitigated by Guardian review, Tool poisoning mitigated by pinned versions
- **AUDIT WELCOME:** Apache-2.0 = full source transparency. Found something? Open an issue.
**TL;DR:** Defense in depth. Guardians verify. You approve. Not bulletproof (nothing is), but responsible design.

### FAQ 8: Multi-provider
**Q: Does it only work with Claude? What about GPT-4 or local models?**
A: Honest answer: Claude-only today. Here's why and what's coming:
- **CURRENT:** Regina (Opus), Workers (Sonnet). Why: Best reasoning for multi-agent coordination.
- **ROADMAP 2026:** OpenAI GPT-4/o1 in development, Ollama for local models planned
- **ARCHITECTURE:** Model-agnostic by design. Swapping providers requires adapter changes, not rewrites.
**TL;DR:** Claude-first because it works best. Multi-provider coming. No permanent lock-in.

### FAQ 9: Git Integration
**Q: How does it handle Git? Aider has great Git integration.**
A: Aider's Git integration is excellent - we respect that. Here's where we are:
- **TODAY:** Context-aware commits, Guardiana reviews before push, SNCP tracks repo state
- **COMING v2.0:** Auto-commit per worker with attribution, Conventional Commits, /undo command
- **HONEST COMPARISON:** Aider wins on Git depth. We win on coordination + quality checks. Different tools, different strengths.
**TL;DR:** Good Git support today, great Git support coming. We're learning from Aider.

### FAQ 10: Production-ready
**Q: Is this production-ready or just an experiment?**
A: Honest answer: Beta. Here's the full picture:
- **REAL USAGE:** 260+ work sessions, 3 production projects daily, 134 tests passing, This launch prepared WITH CervellaSwarm
- **KNOWN LIMITATIONS:** CLI UX can improve, No VSCode extension yet, No team collaboration features yet
- **WHO SHOULD USE IT NOW:** Solo developers, early adopters comfortable with CLI
- **COMMITMENT:** 2 years in, not stopping. Actively developed. Daily dogfooding = bugs get fixed.
**TL;DR:** Real tool, real usage, real limitations. Beta quality. Actively developed.

---

*"Dogfooding: This entire launch was prepared with CervellaSwarm"*
