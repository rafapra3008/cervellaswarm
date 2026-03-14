# HN Response Playbook

> Risposte preparate per domande prevedibili su Hacker News.
> Tone: tecnico, onesto, conciso. Mai difensivo. Mai hype.

---

## Q1: "How is this different from LangGraph/CrewAI/AutoGen?"

> LU doesn't replace any of those -- it's a different layer. LangGraph *executes* your agents. LU *verifies* their communication protocol before you execute anything.
>
> Think of it like TypeScript for JavaScript. You keep your framework, you add type-level guarantees. If your protocol says agent A sends before agent B, the session type makes the opposite impossible at runtime.

## Q2: "Why not just use types/interfaces in Python?"

> Python types check data shapes. Session types check *communication sequences* -- who sends what, to whom, in what order, under what contracts. They're a different formalism.
>
> Specifically, LU implements multiparty session types (Honda/Yoshida/Carbone, POPL 2008). The key guarantee: if your protocol type-checks, it cannot deadlock, messages cannot arrive out of order, and the conversation always terminates. Python's type system can't express this.

## Q3: "How is this different from Scribble?"

> Scribble is the academic tool from the MPST group (Imperial/Oxford). LU takes the same theoretical foundation and adds: a complete compiler, LSP server, linter, formatter, Python codegen, browser playground, NL interface, and Lean 4 verification bridge. Scribble is for researchers; LU is for developers.

## Q4: "Why Lean 4 and not Coq/Isabelle/TLA+?"

> Lean 4 has the best story for *generated* proofs. Its `by decide` tactic handles finite-state properties automatically, which is what most protocol properties reduce to. The user never writes Lean -- LU generates the proof and verifies it.
>
> That said, the Lean 4 bridge runs in simulation mode for some property combinations. We're honest about what's fully verified and what's pending full proof elaboration.

## Q5: "Zero dependencies -- really?"

> Yes, `dependencies = []` in pyproject.toml. The core compiler, parser, spec checker, linter, formatter, REPL, and CLI are all pure Python stdlib.
>
> Claude API (for NL mode), pygls (for LSP), and faster-whisper (for voice) are optional extras: `pip install cervellaswarm-lingua-universale[nl]`, `[lsp]`, `[voice]`.

## Q6: "What's the formal verification actually proving?"

> LU verifies 9 property kinds statically: `always_terminates`, `no_deadlock`, `no_deletion`, `role_exclusive`, `ordering`, `exclusion`, `confidence_min`, `trust_min`, `all_roles_participate`.
>
> For each property, the spec checker either returns PROVED (with evidence) or VIOLATED (with the specific step that fails). When Lean 4 is available, it generates a machine-checked proof.

## Q7: "This seems academic -- who would use this in production?"

> Fair question. Today, most AI agent failures come from hallucinations and costs, not protocol violations. But as agents get more autonomous (tool use, multi-agent pipelines, financial transactions), the *coordination* failure mode becomes critical.
>
> Our bet: session types for AI agents will matter the way HTTPS mattered for the web -- not immediately, but inevitably.

## Q8: "3684 tests for a DSL? That seems like a lot."

> We take testing seriously. The test suite runs in ~2.5 seconds, covers 98% of the codebase, and includes: parser edge cases, compiler correctness, runtime enforcement, linter rules, formatter idempotency, LSP protocol compliance, intent bridge multi-turn conversations, and all 20 stdlib protocols.
>
> Zero flaky tests. We run the full suite on every commit.

## Q9: "Why three languages (English/Italian/Portuguese)?"

> The author is Brazilian-Italian. The NL interface was designed for the "La Nonna" use case: a non-technical person describes a system in their native language, and the tool generates a formally verified protocol.
>
> It's also a proof of concept: the intent bridge is language-agnostic by design. Adding a new language is ~20 lines of translations, not a redesign.

## Q10: "What's the business model?"

> Open source, Apache 2.0, no strings. Right now we're focused on building a community, not monetizing.
>
> Long-term thinking: hosted playground for teams, enterprise compliance features, protocol registry. But that's months away. Today it's about whether the tool is useful.

---

*Regola: rispondi entro 2 ore da ogni commento. Mai difensivo. Se non sai, dillo.*
