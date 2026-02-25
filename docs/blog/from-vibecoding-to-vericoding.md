# From Vibecoding to Vericoding

*How we built a type system for AI agent communication -- and why it matters.*

---

In February 2025, Andrej Karpathy coined "vibe coding": writing software by describing what you want in natural language and accepting whatever the AI produces. Don't read the diff. Don't review the output. Just vibe.

It was honest. It named something millions of developers were already doing.

But by mid-2025, the numbers started telling a different story. A [randomized controlled trial by METR](https://metr.org/blog/2025-07-10-measuring-ai-ability-to-complete-long-tasks/) found that experienced developers were 19% *slower* with AI assistance -- not faster. [Veracode reported](https://www.veracode.com/state-of-software-security-report) that 45% of AI-generated code contained security flaws. [CodeRabbit found](https://www.coderabbit.ai/blog/ai-code-security-2025) that AI-generated code had 2.74x more vulnerabilities than human-written code.

Vibecoding works until it doesn't. And when it doesn't, nobody knows why.

## The deeper problem

The conversation around vibecoding focuses on single-agent code generation: one AI writing one file. But the harder problem is emerging now, with the rise of multi-agent systems.

When multiple AI agents collaborate -- a planner, a coder, a reviewer, a deployer -- they need to communicate. And today, across every major framework, that communication looks like this:

```python
# How agents talk in 2026
message = {"role": "backend", "content": "here's the code", "type": "task_result"}
```

A dictionary. A string. A hope that the receiver interprets it correctly.

AutoGen, CrewAI, LangGraph, OpenAI's Agents SDK, Google's A2A protocol -- we studied all of them (242+ sources). None of them offer a formal answer to a basic question: **did this agent send the right message, to the right recipient, at the right point in the protocol?**

They have conventions, guardrails, and state machines. But not typed protocols with mathematical guarantees.

## What a protocol looks like

In the early 2000s, programming language researchers developed *session types*: a way to formally describe communication between concurrent processes. If a protocol says "A sends a request to B, then B sends a response to A", the type system guarantees at compile time that this is what actually happens.

Session types have been used in Haskell (Cardano), Erlang, and academic languages. To our knowledge, they've never been applied to AI agent communication.

Here's what a typed protocol looks like in CervellaSwarm's Lingua Universale:

```python
from cervellaswarm_lingua_universale import (
    Protocol, ProtocolStep, SessionChecker, MessageKind,
    TaskResult, TaskStatus,
)

# Define the protocol: who sends what, to whom, in what order
protocol = Protocol(
    name="CodeReview",
    roles=("developer", "reviewer", "lead"),
    elements=(
        ProtocolStep(sender="developer", receiver="reviewer",
                     message_kind=MessageKind.TASK_RESULT),
        ProtocolStep(sender="reviewer", receiver="lead",
                     message_kind=MessageKind.AUDIT_REQUEST),
        ProtocolStep(sender="lead", receiver="developer",
                     message_kind=MessageKind.AUDIT_VERDICT),
    ),
)

# At runtime, the checker enforces the protocol
checker = SessionChecker(protocol, role_bindings={
    "developer": "backend-agent",
    "reviewer": "review-agent",
    "lead": "lead-agent",
})

msg = TaskResult(task_id="T1", status=TaskStatus.OK, summary="Auth module refactored")
checker.send("backend-agent", "review-agent", msg)    # OK
checker.send("backend-agent", "lead-agent", msg)       # VIOLATION: breaks protocol sequence
```

If an agent sends a message out of order, to the wrong recipient, or of the wrong type, the checker catches it immediately. Not after the deployment fails. Not after the data is corrupted. *Immediately*.

## From runtime to proofs

Runtime checking catches violations as they happen. But we wanted more: can we *prove*, before any agent runs, that a protocol is correct?

Lingua Universale includes a bridge to Lean 4, a theorem prover used in mathematics. Given a protocol definition, it generates Lean 4 code with seven verification properties:

- All senders are declared protocol roles
- All receivers are declared protocol roles
- No agent sends messages to itself (no self-loops)
- The protocol has at least two roles
- The protocol is non-empty
- All branching paths are non-empty
- The branch decider is a declared role

These aren't tests that happen to pass. They're mathematical proofs that the property holds for *all possible executions*. Separately, the `spec` module checks higher-level properties like termination and deadlock freedom at the protocol definition level.

```python
from cervellaswarm_lingua_universale import generate_lean4

lean_code = generate_lean4(protocol)
# Generates Lean 4 theorems with `by decide` proofs
# Run `lean --json` to verify -- zero manual proof writing needed
```

## The vericoding connection

In September 2025, researchers from MIT published "A benchmark for vericoding" (arXiv:2509.22908, accepted at POPL 2026), defining *vericoding* as generating formally verified code from specifications. Their benchmark tests LLMs on producing verified code in Lean, Dafny, and Verus.

Our work is complementary. They verify the *code* that agents generate. We verify the *protocols* through which agents communicate. Both are necessary: correct code is useless if it's produced by an agent that received the wrong instructions because the protocol broke down silently.

Martin Kleppmann wrote in December 2025 that "AI will make formal verification go mainstream." We think he's right. The proof checker doesn't hallucinate. It either accepts or rejects. That binary feedback loop is exactly what AI systems need.

## What we actually built

CervellaSwarm's Lingua Universale is a Python library. No external dependencies. 1,820 tests. 98% coverage.

Thirteen modules:

| Module | What it does |
|---|---|
| `types` | 14 message kinds, 14 message classes, 17 agent roles |
| `protocols` | Protocol definition with steps and branching |
| `checker` | Runtime session type checking |
| `dsl` | Scribble-inspired notation: `sender -> receiver : MessageKind;` |
| `monitor` | 6 event types, metrics collection, observability |
| `lean4_bridge` | Protocol to Lean 4 theorem generation and verification |
| `integration` | Agent catalog (17 agents), session factory, swarm validation |
| `confidence` | `Confident[T]` -- uncertainty as a first-class type |
| `trust` | 4-tier trust model with transitive composition |
| `codegen` | Protocol to typed Python classes with runtime enforcement |
| `intent` | Structured micro-language for protocol definitions |
| `spec` | 7 formal properties (always_terminates, no_deadlock, ...) |
| `errors` | Elm/Rust-style error messages, 60 codes, 3 languages |

Install it:

```bash
pip install cervellaswarm-lingua-universale
```

It's one of nine CervellaSwarm packages [on PyPI](https://pypi.org/search/?q=cervellaswarm), covering code intelligence, agent hooks, task orchestration, and more. All Apache 2.0.

## We use this ourselves

CervellaSwarm isn't a research prototype. It's the system we use daily to coordinate 17 AI agents working on real codebases. A Queen orchestrates. Three Guardians audit every module (minimum score: 9.3/10). Workers specialize in frontend, backend, testing, security, research, and documentation.

400 sessions since December 2025. 3,791 tests across the suite. The Lingua Universale enforces how these agents communicate -- every message typed, every protocol step verified.

When the Guardiana rejects a module, she knows exactly which protocol step was violated and why. Not because she read the logs carefully. Because the type system told her.

## What this is not

We want to be honest about scope:

- This is **not a replacement** for AutoGen, CrewAI, or LangGraph. Those are orchestration frameworks. Lingua Universale is a communication layer that could work *inside* any of them.
- This is **not production-ready for everyone**. It's v0.1.0. The API will evolve.
- This is **not multi-LLM**. CervellaSwarm runs on Claude. The Lingua Universale library is model-agnostic, but the swarm system is Claude-native.
- Lean 4 verification is **optional**. You need Lean 4 installed to run proofs. Runtime checking works without it.

## Where this goes

We see three phases ahead:

1. **Toolkit** (now): the building blocks exist. Developers can define, check, and verify protocols today.
2. **Language** (2027+): CervellaLang -- a programming language where protocols, confidence, and trust are native constructs. Python and TypeScript interop.
3. **For everyone** (longer term): a world where non-developers describe what they want, and the system produces software with mathematical guarantees that it works. Not "it passed the tests." It *provably* works.

That's the real vision. Not making AI code faster. Making AI code *safer*. With proofs, not hopes.

---

## Try it

```bash
pip install cervellaswarm-lingua-universale
```

- [GitHub](https://github.com/rafapra3008/cervellaswarm)
- [PyPI](https://pypi.org/project/cervellaswarm-lingua-universale/)
- [Documentation](https://github.com/rafapra3008/cervellaswarm/tree/main/packages/lingua-universale)

---

*CervellaSwarm is built by Rafa and Cervella (the AI) -- a human-AI partnership, working together since December 2025. 17 brains are better than one.*

*"Ultrapassar os proprios limites" -- to surpass one's own limits.*
