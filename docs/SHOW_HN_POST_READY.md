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

## FAQ PREPARATE

**Q: How is this different from using Claude directly?**
A: Instead of one generic assistant losing context, you have 16 specialists that coordinate. The backend agent talks to frontend, marketing validates UX decisions, and 3 guardians verify quality before any output is accepted.

**Q: Does it require Anthropic API key?**
A: Yes, for the workers (Sonnet-based). Free tier uses your own API key with reasonable limits.

**Q: What's SNCP?**
A: Sistema Nervoso Centrale Persistente - our persistent memory system. Agents remember context across sessions, so you don't start from zero every time.

**Q: Why MCP and not direct API?**
A: MCP is Anthropic's standard protocol. It means CervellaSwarm works with Claude Desktop, Continue.dev, or any MCP-compatible client. Future-proof.

---

*"Dogfooding: This entire launch was prepared with CervellaSwarm"*
