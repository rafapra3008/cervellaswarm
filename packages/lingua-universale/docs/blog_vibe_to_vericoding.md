# From Vibe Coding to Vericoding

Maria is 68 years old and has never written a line of code. Last Tuesday, she created a software protocol with 5 mathematically proven safety properties. It took her 2 minutes and 47 seconds. The only tool she used was Italian.

---

## The Problem with Vibe Coding

There is a term that has been circulating in AI developer circles: "vibe coding." The idea is appealing — describe what you want, and an AI writes the code for you. No boilerplate, no syntax errors, just intent translated into working software.

But there is a gap between "working software" and "correct software," and that gap is where things break in production.

When you vibe code, you get code that probably works for the cases you described. You get no guarantee about the cases you did not think to describe. You get no proof that two AI agents talking to each other will not deadlock. You get no mathematical certainty that a `no_deletion` rule actually prevents deletion.

You are trusting the vibe.

The broader AI landscape has a version of this same problem. As autonomous agents become more capable, the question of *what they are allowed to do* becomes critical. We have tools for specifying behavior. We have tools for verifying behavior. But they are separate tools, and neither of them is accessible to the person who needs the guarantee the most — the domain expert who is not a formal methods researcher.

Maria knows her recipe system. She knows that no one should be able to delete a recipe. She does not know what a session type is, and she should not have to.

---

## The Insight: Two Stages, One Tool

The approach in Lingua Universale is based on a pattern formalized in recent academic work, specifically the two-stage architecture from Req2LTL (ASE 2025). The insight is this: natural language is too ambiguous to verify directly, but natural language can be reliably mapped to a structured intermediate representation, and *that* representation can be verified formally.

This is the pipeline:

```
Natural Language (Italian, English, Portuguese)
    |
    v
[NL Processing] Claude interprets intent, asks clarifying questions
    |
    v
[IntentDraft] Structured micro-language — unambiguous, parseable
    |
    v
[B.4 Parser] Deterministic parse — zero ambiguity, 100% syntactic correctness
    |
    v
[B.5 Spec Checker] Formal property verification — 9 property kinds
    |
    v
[Lean 4 Bridge] Mathematical proofs generated
    |
    v
[Python Codegen] Certified code — session-typed, runtime-enforced
```

The NL layer is where humans speak. The micro-language layer is where machines verify. The user never sees the middle layers. They see what matters: *PROVED* or *VIOLATION DETECTED*.

---

## The Demo

![La Nonna Demo -- guided mode](../demo/demo_la_nonna.gif)
*The GIF shows guided mode (`lu demo`). The narrative below demonstrates NL mode (`lu chat --lang it`), where Maria types freely in Italian.*

Maria starts by typing:

> "Voglio un sistema per le ricette della nonna. Il cuoco chiede alla dispensa cosa c'e, la dispensa risponde, e il cuoco decide cosa cucinare."

The system responds in Italian, identifies two roles (Cuoco, Dispensa), and asks three clarifying questions. Maria answers: "Si, il cuoco aggiunge ricette. Ma nessuno puo cancellare per sbaglio! Sono sicurissima."

The system builds the protocol and shows it back to her in plain language:

```
protocol GestioneRicette
  roles: Cuoco, Dispensa

  Cuoco asks Dispensa for "ingredienti disponibili"
  Dispensa returns list of "ingrediente"
  when Cuoco decides:
    "cucinare":
      Cuoco sends "ricetta scelta" to Dispensa
    "aggiungere":
      Cuoco sends "nuova ricetta" to Dispensa

  requires always_terminates
  requires no_deadlock
  requires no_deletion
  requires role_exclusive("aggiungere", Cuoco)
  requires confidence >= high
```

Maria adds one more requirement: only the Cuoco should be able to add recipes, not the Dispensa. One sentence of Italian. The system adds `role_exclusive`.

Then the verification runs:

```
  [1/5] always_terminates    ... PROVATO
  [2/5] no_deadlock          ... PROVATO
  [3/5] no_deletion          ... PROVATO
  [4/5] role_exclusive       ... PROVATO
  [5/5] confidence >= high   ... VERIFICATO

  TUTTE LE PROPRIETA VERIFICATE
  5/5 provate matematicamente
  Il tuo sistema e GARANTITO sicuro.
```

Python code is generated automatically. A simulation runs. Everything works.

Then Maria asks: "E se la dispensa prova a cancellare una ricetta?"

```
  [Dispensa] tenta: cancellare "Insalata Caprese"

  VIOLAZIONE RILEVATA!
    Proprieta: no_deletion
    Messaggio: "La cancellazione non e permessa in questo protocollo."
    Azione bloccata.
```

This is the moment that matters. The mathematical proof was not decorative. It was operational. The runtime enforcer is derived from the same specification that was verified. The Dispensa role *cannot* delete, not because we trust it, but because the protocol structure makes it impossible.

The session ends:

> "Non e magia. E matematica."

---

## How It Works

Lingua Universale is built on session types, a formalism from Honda et al. (1998) that describes communication protocols as types. If two processes follow the same session type, they cannot deadlock, messages cannot arrive in the wrong order, and the conversation terminates.

Session types have been a research area for nearly 30 years. What has been missing is the human layer — a way for people who are not type theorists to specify and benefit from this kind of guarantee.

The `_intent_bridge.py` module (the IntentBridge) translates between natural language and the Lingua Universale micro-language. It is a multi-turn conversational system that uses Claude for NL interpretation with a `tool_use` schema for structured extraction. If the intent is ambiguous, it raises `NLClarificationNeeded` and asks the user a targeted question. Once the intent is confirmed, it becomes an `IntentDraft` — a frozen intermediate representation that feeds the deterministic B.4 parser.

The nine `PropertyKind` values currently supported include `NO_DELETION`, `ROLE_EXCLUSIVE`, `ALWAYS_TERMINATES`, `NO_DEADLOCK`, `CONFIDENCE_MIN`, and four others. Each can be checked at spec time (B.5) and enforced at runtime by the `SessionChecker`.

The system supports three languages: Italian, English, and Portuguese. Voice input is optional via `faster-whisper` (local STT, no cloud dependency).

---

## Where It Stands

This is alpha software. Here is what is real:

- 3438 tests, 0 regressions across 29 modules
- 9 property kinds with formal verification via Lean 4
- 20 verified standard library protocols across 5 categories (AI/ML, Business, Communication, Data, Security)
- The complete pipeline from NL to certified Python works end-to-end
- The La Nonna demo runs exactly as described above
- `lu init --template rag_pipeline` scaffolds from stdlib in seconds
- Zero core dependencies (Claude and voice are optional extras)

Here is what is not yet ready:

- The Lean 4 integration runs in simulation mode for some property combinations pending full proof elaboration
- Voice input requires local installation of `faster-whisper`
- Production hardening for protocols with more than ~10 roles is ongoing

We are calling this approach **Vericoding** — the complement to vibe coding. Not because AI-assisted development is wrong, but because AI-assisted development with mathematical proofs attached is a different category of claim.

---

## Try It

```bash
pip install cervellaswarm-lingua-universale==0.3.1
lu chat --lang en
```

Or in Italian:

```bash
lu chat --lang it
```

With voice input:

```bash
pip install "cervellaswarm-lingua-universale[voice]"
lu chat --lang it --voice
```

The source, all 29 modules and 3438 tests, is at [github.com/rafapra3008/cervellaswarm](https://github.com/rafapra3008/cervellaswarm). The live playground is at [rafapra3008.github.io/cervellaswarm](https://rafapra3008.github.io/cervellaswarm/).

If you are working on AI agents, autonomous systems, or just want a language where the proof comes with the code — we want to hear what you think.

---

*Lingua Universale v0.3.1 — CervellaSwarm, March 2026*
