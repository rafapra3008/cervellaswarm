# Show HN - Draft

> Preparato: S401 (2026-02-25). Da revisionare prima di submit.

---

## TITLE

```
Show HN: Lingua Universale – session types and Lean 4 proofs for AI agent protocols
```

**Length:** 83 characters (under 100 limit)
**Why this title:**
- Names the package directly (`Lingua Universale`)
- Two technical differentiators: `session types` + `Lean 4 proofs`
- `AI agent protocols` = the problem space
- No superlatives. No "first". No marketing language.

---

## URL

```
https://github.com/rafapra3008/cervellaswarm
```

**Why GitHub, not blog:** Show HN rules require something people can try. The repo has pip install, README, Colab link, and 9 packages.

---

## FIRST COMMENT (author post)

```
Hi HN,

We've been building CervellaSwarm for about three months -- a set of Python
packages for multi-agent AI systems. Today we're sharing what we think is
the most interesting part: cervellaswarm-lingua-universale, a session type
system for AI agent communication.

THE PROBLEM: When multiple AI agents collaborate (a planner, a coder, a
reviewer), they communicate via dictionaries and strings. No framework we
could find -- AutoGen, CrewAI, LangGraph, OpenAI Agents SDK, Google A2A --
answers a basic question: did this agent send the right message, to the
right recipient, at the right point in the protocol?

OUR APPROACH: Session types from programming language theory (Honda 1993;
multiparty extension by Honda, Yoshida & Carbone, POPL 2008). We
implemented them in Python so you can define a protocol, bind agents to
roles, and get violations caught at runtime -- not after the deployment
fails.

The library also generates Lean 4 code with theorems that prove structural
properties of your protocol (all senders/receivers are valid roles, no
self-loops, non-empty branches). The proofs use `by decide` -- decidable,
machine-checkable, zero manual proof writing.

WHAT IT IS:
- Pure Python, zero dependencies, pip install and go
- 13 modules: types, protocols, checker, DSL, monitor, Lean 4 bridge,
  codegen, intent parser, spec language, confidence types, trust model,
  error messages, agent integration
- 1,820 tests, 98% coverage
- DSL inspired by Scribble notation: `sender -> receiver : MessageKind;`
- Lean 4 verification is optional (runtime checking works without it)

Try it in 30 seconds:

    pip install cervellaswarm-lingua-universale

    from cervellaswarm_lingua_universale import Protocol, ProtocolStep, MessageKind, SessionChecker, TaskResult, TaskStatus
    protocol = Protocol(name="Review", roles=("dev", "reviewer"), elements=(
        ProtocolStep(sender="dev", receiver="reviewer", message_kind=MessageKind.TASK_RESULT),))
    checker = SessionChecker(protocol)
    checker.send("dev", "reviewer", TaskResult(task_id="1", status=TaskStatus.OK, summary="Done"))

Or try the interactive Colab notebook (2 min, zero setup):
https://colab.research.google.com/github/rafapra3008/cervellaswarm/blob/main/docs/blog/from-vibecoding-to-vericoding-demo.ipynb

To our knowledge, session types haven't been applied to AI agent
communication before -- we searched 242 sources across academic papers,
frameworks, and protocols. If we missed prior work, we'd genuinely like
to know.

lingua-universale is one of 9 CervellaSwarm packages on PyPI (the others
cover code intelligence, agent hooks, task orchestration, session memory,
and more). All Apache 2.0.

What we're most curious about: do you see formal verification as relevant
to multi-agent systems? We're deciding how far to push the Lean 4
direction.
```

**Word count:** ~350 (within 300-500 recommended range)

---

## CLAIM VERIFICATION CHECKLIST

| Claim | Source | Verified |
|-------|--------|----------|
| "about three months" | Dec 2025 - Feb 2026 (S1-S401) | YES |
| "session type system for AI agent communication" | types.py + protocols.py + checker.py | YES |
| "No framework we could find" answers protocol correctness | 242 sources research (S375, S380) | YES |
| "Honda 1993; Honda, Yoshida & Carbone 2008" | Binary session types (1993) + MPST (2008) | YES |
| "Scribble/MPST" | DSL inspired by Scribble notation (dsl.py) | YES |
| "Pure Python, zero dependencies" | pyproject.toml has no runtime deps | YES |
| "13 modules" | types, protocols, checker, dsl, monitor, lean4_bridge, integration, confidence, trust, codegen, intent, spec, errors = 13 | YES |
| "1,820 tests, 98% coverage" | MEMORY.md, test suite | YES |
| "by decide" proofs | lean4_bridge.py generates `by decide` tactics | YES |
| "242 sources" | Research across S375-S386 | YES |
| "9 CervellaSwarm packages on PyPI" | All 9 published S399 | YES |
| "All Apache 2.0" | All pyproject.toml files | YES |
| "To our knowledge" qualifier | Hedged correctly, invites correction | SAFE |

---

## RESPONSE STRATEGY (first 2 hours)

**If asked "what makes this different from X?"**
- AutoGen/CrewAI/LangGraph: "Those coordinate agents. We prove the coordination is correct. They're complementary -- you could use lingua-universale inside any of them."
- Google A2A / MCP: "Those define message formats. We define and enforce message sequences."

**If asked about "first" claim:**
- "We searched 242 sources and couldn't find prior work applying session types to AI agents in Python. Happy to be corrected -- we'd love to study it."

**If asked about production readiness:**
- "It's v0.1.0 -- the API will evolve. We use it daily to coordinate 17 agents, but we're honest that it hasn't been tested outside our setup yet."

**If asked about Lean 4 proofs:**
- "The proofs cover structural properties (valid roles, no self-loops, non-empty). They don't prove behavioral properties like liveness of arbitrary protocols. That's Fase C."

**If asked "these are runtime checks, not real session types" (PL researchers):**
- "You're right that classical session types are static. In Python, without dependent types or a compiler plugin, runtime is where we can enforce. We think of it as session types at the enforcement layer that fits -- similar to how contracts/DbC work in dynamic languages. The Lean 4 bridge is our path toward static: prove properties offline, then the runtime checker handles dynamic inputs."

**If asked "why not just a state machine?":**
- "A state machine enforces sequences but doesn't type the messages or bind roles. You can be in the right state and still send the wrong payload to the wrong agent. Session types give you both: the sequence AND the who-sends-what-to-whom typing."

**If asked "who is 'we'?":**
- "A developer and a multi-agent system that helped build itself. The irony isn't lost on us."

**If someone shares a deep technical critique:**
- Thank them. Ask follow-up questions. This is exactly the audience we want.

**Blog post link (share in comments if discussion gets technical):**
- "I wrote a longer piece about the 'vibecoding to vericoding' framing: [link to blog post]"

---

## TIMING

**Target:** Sunday, 12:00-14:00 UTC (8-10 AM EST)
**Rationale:** Weekend breakout rate 20-30% higher. Sunday 11-16 UTC is sweet spot per research.

---

## PRE-SUBMIT CHECKLIST

- [ ] `pip install cervellaswarm-lingua-universale` works in fresh env
- [ ] Colab notebook "Run All" works (test in incognito)
- [ ] GitHub README has Colab badge link
- [ ] All 9 packages installable from PyPI
- [ ] First comment ready (copy-paste, no edits under pressure)
- [ ] Response strategy reviewed
- [ ] Blog post link ready for comments
