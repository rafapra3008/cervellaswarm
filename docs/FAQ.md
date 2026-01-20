# Frequently Asked Questions

## General

### What is CervellaSwarm?

CervellaSwarm is a multi-agent AI system with 17 specialized agents coordinated by a central "Regina" (Queen) agent. It includes 3 Guardian agents that verify the quality of every output, ensuring consistent high-quality results.

The system is designed for complex software development tasks that benefit from specialized expertise: frontend, backend, testing, infrastructure, data analysis, security, and more.

### Why "Swarm"?

Because it's a coordinated swarm of agents collaborating on tasks, not a single AI. Each agent has specific expertise and responsibilities. The Regina coordinates task distribution, while Guardians verify quality before delivery.

This mirrors how real development teams work: specialized roles, coordination, and quality control.

### Why beta?

The code is solid - 241 tests pass, the architecture is proven in production across three real projects (Miracollo PMS, Miracollook, ContabilitaAntigravity).

We're in beta to gather feedback from real-world users before declaring v1.0 stability. We want to understand how developers use CervellaSwarm in different contexts, what workflows work best, and what needs improvement.

Beta means: the foundation is strong, we're refining the experience.

---

## What Makes Us Different

### Self-Checking System

Every output goes through 3 Guardian agents (Opus-powered) that verify:
- Code quality
- Security best practices
- Infrastructure correctness

Target score: 9.5/10. If quality is below threshold, work is revised automatically.

No other AI coding tool has this level of built-in quality assurance.

### Semantic Code Search

Built-in tree-sitter AST parsing for semantic code analysis. Find symbol definitions, function callers, and references in 2 seconds across large codebases.

Not grep. Not regex. Actual code understanding.

```bash
semantic-search.sh find-symbol "MyClass"
semantic-search.sh find-callers "my_function"
```

### Architect-First Workflow

Complex tasks go to the Architect agent first. It analyzes requirements, maps dependencies, creates a detailed plan, then delegates to specialized workers.

Plans before code. Structure before implementation.

This prevents the "rewrite everything halfway through" problem common with AI coding tools.

### SNCP Memory System

Persistent memory across sessions. The system remembers:
- Project architecture decisions
- Past discussions and why certain choices were made
- Current state and next steps

You don't re-explain your project every session. The context persists.

---

## Technical

### What models does it use?

**Opus-powered (5 agents):**
- Regina (coordinator)
- 3 Guardians (quality, operations, security)
- 1 Architect

**Sonnet-powered (12 agents):**
- Workers: backend, frontend, tester, docs, researcher, devops, data, security, marketing, ingegnera, scienziata, reviewer

This balances power (Opus for complex decisions) with efficiency (Sonnet for specialized execution).

### Does my code leave my machine?

Your code is sent to Anthropic's API for processing (standard Claude API). Nothing is stored on CervellaSwarm servers - we don't run servers.

All processing happens via Anthropic's Claude API with your API key. Same privacy model as using Claude directly.

### What languages are supported?

All languages supported by Claude: Python, JavaScript/TypeScript, Go, Rust, Java, C/C++, PHP, Ruby, Swift, Kotlin, and more.

Semantic search (tree-sitter) supports: Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby.

---

## Pricing

### What's the pricing?

**FREE Tier:**
- $0/month
- 3 agents (Regina + 2 workers)
- 50 tasks/month
- Bring Your Own Key (BYOK) - use your Anthropic API key

**PRO Tier:**
- $29/month
- 17 agents (full swarm)
- Unlimited tasks
- Includes API costs

**TEAM Tier:**
- $49/user/month
- 17 agents per user
- Unlimited tasks
- Shared memory/context across team
- Includes API costs

### What's Founding Member?

Special offer for the first 200 users: $149/year (one-time, locks in price forever).

That's $12.42/month vs $29/month PRO pricing - a 57% lifetime discount.

Founding Members get:
- PRO features forever at founding price
- Priority support
- Input on roadmap priorities
- Recognition in project credits

### How do API costs work?

**FREE tier:** You pay Anthropic directly with your API key.

**PRO/TEAM tiers:** API costs included in subscription. We handle the Anthropic billing.

PRO pricing is designed to cover typical developer usage patterns with comfortable margin.

---

## Roadmap

### Where's the roadmap?

See `NORD.md` in the project root for current direction and priorities.

Current focus areas:
- Web dashboard for task monitoring
- VS Code extension
- Enhanced collaboration features
- Performance optimizations

### When will v1.0 ship?

When we have 100-200 active users with 30+ days of real-world usage.

We prioritize stability over speed. v1.0 means: production-ready, API stable, documentation complete, edge cases handled.

Estimated timeline: Q2 2026, but we ship when it's ready, not when the calendar says so.

### Can I request features?

Yes. Open an issue on GitHub or email features@cervellaswarm.dev

We prioritize features based on:
1. Impact on existing workflows
2. Number of users requesting it
3. Alignment with core vision
4. Implementation complexity

Founding Members get priority consideration for feature requests.

---

## Getting Started

### How do I install it?

```bash
git clone https://github.com/cervellaswarm/cervellaswarm.git
cd cervellaswarm
./scripts/setup/install.sh
```

See `docs/INSTALLATION.md` for detailed setup instructions.

### Do I need to know how to code?

You need basic command-line familiarity. The agents do the coding, but you need to:
- Understand what you're asking for
- Review agent output
- Make architectural decisions

CervellaSwarm amplifies developer productivity. It's not a replacement for development knowledge.

### What's the learning curve?

**Day 1:** Spawn workers, delegate simple tasks, see results.

**Week 1:** Understand agent specializations, use Guardians for quality checks, leverage SNCP memory.

**Month 1:** Architect complex features, coordinate multi-agent workflows, customize agent behavior.

Most developers are productive within the first day. Mastery takes a few weeks.

---

## Troubleshooting

### Agent isn't responding

Check:
1. Is your API key valid? (`echo $ANTHROPIC_API_KEY`)
2. Are you within rate limits? (Anthropic has rate limits per tier)
3. Check `.swarm/status/{agent}.json` for error messages

### Quality score is low

Guardian found issues. Check:
1. `.swarm/output/TASK_XXX_QUALITY_REPORT.md` for specific problems
2. Agent will auto-revise if issues are fixable
3. You can override with `--skip-quality-check` (not recommended)

### Worker stuck on task

Check heartbeat: `.swarm/status/{agent}.json` has timestamp.

If no heartbeat for 5+ minutes:
```bash
scripts/swarm/kill-worker.sh {agent-name}
scripts/swarm/spawn-worker.sh {agent-name}
```

### Where are logs?

- Task outputs: `.swarm/tasks/`
- Agent status: `.swarm/status/`
- System logs: `.swarm/logs/`

All paths relative to project root.

---

## Philosophy

### Why do you use emojis in docs?

We don't. Emojis are disabled project-wide for professional documentation.

The only exception: internal DNA files for agent personalities (not user-facing).

### Why "Cervella"?

Italian for "brain." The founder (Rafa) is Italian. Each agent is a specialized brain working together.

### What's the long-term vision?

Enable developers to build complex software faster without sacrificing quality.

Not by replacing developers - by giving them a team of specialized AI agents that handle implementation details while they focus on architecture and decisions.

The goal: geographic freedom for developers. Work from anywhere, build anything, maintain quality.

---

For more questions, see:
- Technical docs: `docs/`
- GitHub issues: https://github.com/cervellaswarm/cervellaswarm/issues
- Discord community: (link coming soon)
