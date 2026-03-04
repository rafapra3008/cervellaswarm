/**
 * A Tour of Lingua Universale
 * 24 interactive steps across 4 chapters.
 *
 * Each step has code that MUST pass check_source().
 * Reference: packages/lingua-universale/examples/*.lu
 */

/* eslint-disable max-len */

const LU_TOUR_VERSION = 1;

const LU_TOUR = {
  title: "A Tour of Lingua Universale",
  subtitle: "From zero to verified protocol in 90 minutes",
  version: LU_TOUR_VERSION,
  chapters: [

    // ================================================================
    // CHAPTER 1: TYPES
    // ================================================================
    {
      id: "types",
      title: "Chapter 1: Types",
      description: "The building blocks of Lingua Universale",
      steps: [
        {
          id: "types-1-hello",
          title: "Welcome to Lingua Universale",
          explanation: `**Lingua Universale** (LU) is a programming language designed for AI agent communication.

Unlike traditional languages built for deterministic machines, LU understands that AI agents have **uncertainty**, **trust levels**, and need **provable protocols**.

Let's start with the simplest concept: a **variant type**. A variant declares a set of possible values -- like an enum in other languages.

Press **Check** to validate this code.`,
          code: `# Your first LU code!\n# A variant type: a set of possible values.\n\ntype TaskStatus = Pending | Running | Done`,
          suggestedAction: "check",
          hint: "Variant types are like enums. Each value (Pending, Running, Done) is a distinct state.",
        },
        {
          id: "types-2-variants",
          title: "More Variant Types",
          explanation: `Variant types can have as many values as you need. They model **choices** and **states** in your domain.

Notice how each type name starts with an uppercase letter, and values are separated by \`|\`.

Try modifying the code -- add a new value to one of the types, then press **Check**.`,
          code: `# Multiple variant types in one program\n\ntype Priority = Critical | High | Normal | Low\n\ntype Role = Frontend | Backend | Researcher | Guardiana\n\ntype Verdict = Approved | NeedsRevision | Rejected`,
          suggestedAction: "check",
          hint: "Types are the vocabulary of your program. Define them before agents and protocols.",
        },
        {
          id: "types-3-records",
          title: "Record Types",
          explanation: `A **record type** groups related fields together -- like a struct or dataclass.

Fields are defined with **indentation** (4 spaces) under the type name. Each field has a name and a type.

Built-in types include \`String\`, \`Number\`, \`Boolean\`, and \`List[T]\`.`,
          code: `# A record type: fields with types\n\ntype DeploymentPlan =\n    target: String\n    version: String\n    rollback: Boolean\n\ntype TestResult =\n    passed: Number\n    failed: Number\n    duration: Number\n    log: List[String]`,
          suggestedAction: "check",
          hint: "Indentation matters! Use exactly 4 spaces for fields under a type.",
        },
        {
          id: "types-4-composed",
          title: "Composing Types",
          explanation: `Types can **reference other types**. A record field can use a variant type, and records can reference other records.

This is how you build a rich domain model: small types composed into larger ones.

In this example, \`Recipe\` uses \`Category\` (a variant) and \`List[String]\` (a built-in generic).`,
          code: `# Types referencing other types\n\ntype Category = Antipasto | Primo | Secondo | Dolce\n\ntype Recipe =\n    name: String\n    category: Category\n    ingredients: List[String]\n    servings: Number`,
          suggestedAction: "check",
          hint: "Variant types + record types = a complete domain model.",
        },
        {
          id: "types-5-confident",
          title: "Confident[T]: Uncertainty as a Type",
          explanation: `This is LU's **first pillar**: uncertainty as a first-class citizen.

In other languages, confidence is a string: \`"I'm 70% sure"\`. In LU, it's a **type**: \`Confident[T]\`.

The compiler knows that a \`Confident[Number]\` is different from a plain \`Number\`. It carries uncertainty information that can be checked and composed.

*"Not as a string. As a TYPE. The compiler knows what to do with it."*`,
          code: `# Confident[T]: uncertainty is a type, not a string\n\ntype AnalysisResult =\n    summary: String\n    score: Confident[Number]\n    details: List[String]\n\ntype Prediction =\n    value: Confident[String]\n    model: String\n    timestamp: Number`,
          suggestedAction: "check",
          hint: "Confident[T] wraps any type with uncertainty metadata. The AI's doubt becomes part of the program.",
        },
        {
          id: "types-6-optional",
          title: "Optional Fields",
          explanation: `Append \`?\` to a field type to make it **optional**. This means the field can be absent -- no null pointer surprises.

Optional fields are explicit in the type definition. You always know which fields might be missing.`,
          code: `# Optional fields: String? means "might be absent"\n\ntype UserProfile =\n    name: String\n    email: String\n    bio: String?\n    avatar: String?\n\ntype SearchResult =\n    query: String\n    results: List[String]\n    total: Number\n    nextPage: String?`,
          suggestedAction: "check",
          hint: "String? = maybe a String, maybe nothing. No surprises at runtime.",
        },
        {
          id: "types-exercise",
          title: "Exercise: Model a Library",
          explanation: `Your turn! Model a **library system** with LU types.

You need:
- A variant type for book genres (at least 3 genres)
- A record type for a Book with title, author, genre, and pages
- A record type for a Library with name and a list of books

Edit the code below and press **Check** to validate your design.`,
          code: `# Exercise: Model a library system\n# Define your types below!\n\ntype Genre = Fiction | NonFiction | Science\n\ntype Book =\n    title: String\n    author: String\n    genre: Genre\n    pages: Number\n\ntype Library =\n    name: String\n    books: List[String]`,
          suggestedAction: "check",
          hint: "There's no single right answer. Any valid type definitions that model the domain are correct!",
          isExercise: true,
          solution: `# One possible solution\n\ntype Genre = Fiction | NonFiction | Science | Poetry | History\n\ntype Book =\n    title: String\n    author: String\n    genre: Genre\n    pages: Number\n    rating: Confident[Number]\n    isbn: String?\n\ntype Library =\n    name: String\n    books: List[String]\n    city: String`,
        },
      ],
    },

    // ================================================================
    // CHAPTER 2: AGENTS
    // ================================================================
    {
      id: "agents",
      title: "Chapter 2: Agents",
      description: "AI team members with roles, trust, and contracts",
      steps: [
        {
          id: "agents-1-basic",
          title: "Your First Agent",
          explanation: `An **agent** is an AI team member with a specific role. In LU, agents are defined with their capabilities and constraints.

Every agent has:
- **role**: what kind of work they do (backend, frontend, guardiana, researcher...)
- **trust**: how much authority they have
- **accepts/produces**: what message types they handle`,
          code: `# Your first agent definition\n\ntype TaskStatus = Pending | Running | Done\n\nagent Worker:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult`,
          suggestedAction: "check",
          hint: "Agents are like job descriptions: role, trust level, and what they accept/produce.",
        },
        {
          id: "agents-2-trust",
          title: "Trust Tiers",
          explanation: `LU has three **trust tiers** that control what an agent can do:

- \`verified\`: highest trust -- can make final decisions, audit others
- \`trusted\`: mid-level -- can plan and coordinate
- \`standard\`: basic -- executes assigned tasks

Trust is LU's **second pillar**: trust composition. A \`standard\` agent cannot override a \`verified\` decision.`,
          code: `# Three trust tiers: verified > trusted > standard\n\ntype Priority = Critical | High | Normal\n\nagent Architect:\n    role: backend\n    trust: trusted\n    accepts: PlanRequest\n    produces: PlanProposal\n\nagent Builder:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n\nagent Guardian:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict`,
          suggestedAction: "check",
          hint: "Trust tiers prevent privilege escalation: a standard agent can't do what a verified agent does.",
        },
        {
          id: "agents-3-contracts",
          title: "Agent Contracts",
          explanation: `Agents can have **contracts**: preconditions (\`requires\`) and postconditions (\`ensures\`).

- \`requires\`: what must be true BEFORE the agent starts work
- \`ensures\`: what the agent guarantees AFTER completing work

These are not comments -- LU compiles them into runtime checks.`,
          code: `# Contracts: requires (preconditions) and ensures (postconditions)\n\nagent Analyst:\n    role: researcher\n    trust: standard\n    accepts: ResearchQuery\n    produces: ResearchReport\n    requires: task.well_defined\n    ensures: result.confidence >= 0.7\n\nagent Reviewer:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: result.submitted\n    ensures: verdict.justified`,
          suggestedAction: "check",
          hint: "requires = what the agent needs. ensures = what the agent promises. Both are enforced.",
        },
        {
          id: "agents-4-multi-requires",
          title: "Multiple Contracts",
          explanation: `An agent can have **multiple** \`requires\` and \`ensures\` clauses. Each one is a separate contract that must hold.

You can also combine conditions with \`and\` in a single clause.`,
          code: `# Multiple contract clauses\n\nagent Deployer:\n    role: backend\n    trust: trusted\n    accepts: TaskRequest\n    produces: TaskResult\n    requires:\n        code.submitted\n        tests.pass_()\n    ensures: result.tests_pass\n\nagent SecurityAuditor:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: code.submitted\n    ensures: verdict.justified and verdict.complete`,
          suggestedAction: "check",
          hint: "Multiple requires lines = ALL conditions must be met. 'and' combines conditions in one line.",
        },
        {
          id: "agents-5-team",
          title: "Building a Team",
          explanation: `A real AI team has multiple agents with different roles and trust levels working together.

Notice how the types, agents, and their contracts form a **complete specification** of who does what and under what conditions.

Press **Run** to see this team compiled into Python.`,
          code: `type Priority = Critical | High | Normal | Low\n\ntype DeploymentPlan =\n    target: String\n    version: String\n    priority: Priority\n\nagent Architect:\n    role: backend\n    trust: trusted\n    accepts: PlanRequest\n    produces: PlanProposal\n    requires: spec.approved\n    ensures: plan.complete\n\nagent Builder:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: plan.approved\n    ensures: result.tests_pass\n\nagent Guardian:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: code.submitted\n    ensures: verdict.justified`,
          suggestedAction: "run",
          hint: "Press Run to see the generated Python code. LU compiles to real, executable Python.",
        },
        {
          id: "agents-6-real-world",
          title: "Real-World Agents",
          explanation: `Agents model real roles in your organization. Here's a recipe management system where a \`RecipeManager\` handles data and a \`QualityChecker\` audits it.

The key insight: **the agent definition IS the specification**. No separate docs needed.`,
          code: `type Category = Antipasto | Primo | Secondo | Dolce\n\ntype Recipe =\n    name: String\n    category: Category\n    ingredients: List[String]\n    servings: Number\n    notes: String?\n\nagent RecipeManager:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: request.valid\n    ensures: result.done\n\nagent QualityChecker:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: data.submitted\n    ensures: verdict.justified`,
          suggestedAction: "check",
          hint: "Agent definitions are living documentation. They describe AND enforce behavior.",
        },
        {
          id: "agents-exercise",
          title: "Exercise: Design a Support Team",
          explanation: `Design a **customer support** team with LU agents.

You need at least:
- A \`SupportAgent\` (standard trust) that handles tickets
- A \`Escalator\` (trusted) that handles complex cases
- A \`Manager\` (verified) that audits resolutions

Define appropriate types for ticket status and contracts for each agent.`,
          code: `# Exercise: Design a customer support team\n\ntype TicketStatus = Open | InProgress | Resolved | Escalated\n\nagent SupportAgent:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: ticket.valid\n    ensures: result.done`,
          suggestedAction: "check",
          hint: "Add the Escalator and Manager agents. Think about what each role requires and ensures.",
          isExercise: true,
          solution: `# One possible solution\n\ntype TicketStatus = Open | InProgress | Resolved | Escalated\n\ntype TicketPriority = Urgent | High | Normal | Low\n\ntype Ticket =\n    id: String\n    status: TicketStatus\n    priority: TicketPriority\n    description: String\n    customer: String\n\nagent SupportAgent:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: ticket.valid\n    ensures: result.done\n\nagent Escalator:\n    role: backend\n    trust: trusted\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: ticket.escalated\n    ensures: result.resolution_complete\n\nagent Manager:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: resolution.submitted\n    ensures: verdict.justified`,
        },
      ],
    },

    // ================================================================
    // CHAPTER 3: PROTOCOLS
    // ================================================================
    {
      id: "protocols",
      title: "Chapter 3: Protocols",
      description: "Who talks to whom, in what order, with what guarantees",
      steps: [
        {
          id: "protocols-1-basic",
          title: "Your First Protocol",
          explanation: `A **protocol** defines how agents communicate: who sends what to whom, in what order.

Every protocol has:
- **roles**: the participants
- **actions**: what happens (asks, returns, tells)
- **properties**: guarantees about the protocol

This is LU's **third pillar**: protocols that prove themselves correct.`,
          code: `# A simple two-role protocol\n\ntype TaskStatus = Pending | Running | Done\n\nagent Worker:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n\nprotocol SimpleTask:\n    roles: boss, worker\n    boss asks worker to do task\n    worker returns result to boss\n    properties:\n        always terminates`,
          suggestedAction: "check",
          hint: "Protocols are sequences of messages between roles. 'asks' sends a request, 'returns' sends a response.",
        },
        {
          id: "protocols-2-actions",
          title: "Protocol Actions",
          explanation: `LU protocols support several **action verbs**:

- \`asks ... to do\`: request work from another agent
- \`returns ... to\`: send a result back
- \`tells ... revise\`: request a revision
- \`asks ... to verify\`: request verification/audit

Each action specifies **sender**, **receiver**, and **what** is being communicated.`,
          code: `type TaskStatus = Pending | Running | Done\n\nagent Worker:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n\nagent Guardian:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n\nprotocol DelegateTask:\n    roles: regina, worker, guardiana\n    regina asks worker to do task\n    worker returns result to regina\n    regina asks guardiana to verify\n    guardiana returns verdict to regina\n    properties:\n        always terminates\n        no deadlock`,
          suggestedAction: "check",
          hint: "Three roles, four actions. The protocol guarantees: always terminates, no deadlock.",
        },
        {
          id: "protocols-3-choice",
          title: "Choice: Branching Protocols",
          explanation: `Real protocols have **decisions**. The \`when ... decides\` block creates branches.

One role makes a decision, and the protocol follows different paths depending on the choice. Each branch is a complete sub-protocol.

This is like an if/else, but for multi-agent communication.`,
          code: `type TaskStatus = Pending | Running | Done\n\nagent Reviewer:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n\nprotocol CodeReview:\n    roles: dev, reviewer\n    dev returns code to reviewer\n    when reviewer decides:\n        approve:\n            reviewer returns verdict to dev\n        reject:\n            reviewer tells dev revise code\n            dev returns revised to reviewer\n            reviewer returns verdict to dev\n    properties:\n        always terminates\n        no deadlock`,
          suggestedAction: "check",
          hint: "'when X decides' creates branches. Each branch name (approve, reject) is followed by indented actions.",
        },
        {
          id: "protocols-4-properties",
          title: "Protocol Properties",
          explanation: `Properties are **guarantees** about your protocol. LU can verify them:

- \`always terminates\`: the protocol always reaches an end
- \`no deadlock\`: no agent gets stuck waiting forever
- \`all roles participate\`: every listed role sends at least one message
- \`X before Y\`: ordering constraints between agents
- \`X cannot send Y\`: exclusion constraints

These are not hopes -- they are **checked** by the compiler.`,
          code: `type Priority = Critical | High | Normal\n\nagent Architect:\n    role: backend\n    trust: trusted\n    accepts: PlanRequest\n    produces: PlanProposal\n\nagent Builder:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n\nagent Guardian:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n\nprotocol DeployPipeline:\n    roles: regina, architect, builder, guardian\n    regina asks architect to plan deployment\n    architect returns proposal to regina\n    regina asks builder to do implementation\n    builder returns result to regina\n    regina asks guardian to verify deployment\n    guardian returns verdict to regina\n    properties:\n        always terminates\n        no deadlock\n        all roles participate\n        architect before builder\n        builder before guardian\n        builder cannot send audit_verdict`,
          suggestedAction: "run",
          hint: "Press Run to see this protocol compiled. Notice how ordering and exclusion constraints are enforced.",
        },
        {
          id: "protocols-5-confidence",
          title: "Confidence in Protocols",
          explanation: `Protocols can require **minimum confidence** and **trust levels**:

- \`confidence >= high\`: results must have high confidence
- \`trust >= standard\`: all participants must have at least standard trust
- \`X before Y\`: enforce execution order

These properties combine LU's three pillars: uncertainty, trust, and provable protocols.`,
          code: `type AnalysisStatus = InProgress | Complete | NeedsReview\n\ntype AnalysisResult =\n    summary: String\n    score: Confident[Number]\n    status: AnalysisStatus\n\nagent Analyst:\n    role: researcher\n    trust: standard\n    accepts: ResearchQuery\n    produces: ResearchReport\n    requires: task.well_defined\n    ensures: result.confidence >= 0.7\n\nagent Reviewer:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: result.submitted\n    ensures: verdict.justified\n\nprotocol ConfidenceReview:\n    roles: analyst, reviewer, regina\n    analyst returns report to regina\n    regina asks reviewer to verify report\n    when reviewer decides:\n        approve:\n            reviewer returns verdict to regina\n        needs_revision:\n            reviewer tells analyst revise findings\n            analyst returns revised report to regina\n            reviewer returns verdict to regina\n    properties:\n        always terminates\n        no deadlock\n        confidence >= high\n        trust >= standard\n        analyst before reviewer`,
          suggestedAction: "check",
          hint: "Confidence + trust + ordering = a protocol that proves its own correctness.",
        },
        {
          id: "protocols-exercise",
          title: "Exercise: The Pizza Protocol",
          explanation: `Design a **pizza ordering protocol** with three roles:

- \`customer\`: orders pizza
- \`chef\`: makes the pizza
- \`manager\`: checks quality before delivery

Include a \`when\` branch where the manager can approve or send back to the chef. Add at least 3 properties.

This is like the real world: customer orders, chef cooks, manager quality-checks.`,
          code: `# Exercise: Design a pizza ordering protocol\n\ntype PizzaSize = Small | Medium | Large\n\ntype Pizza =\n    name: String\n    size: PizzaSize\n    toppings: List[String]\n\nagent Chef:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: order.valid\n    ensures: result.done\n\nprotocol PizzaOrder:\n    roles: customer, chef\n    customer asks chef to do make pizza\n    chef returns result to customer\n    properties:\n        always terminates`,
          suggestedAction: "check",
          hint: "Add a Manager agent (verified trust) and a quality check branch with 'when manager decides'.",
          isExercise: true,
          solution: `# One possible solution\n\ntype PizzaSize = Small | Medium | Large\n\ntype Pizza =\n    name: String\n    size: PizzaSize\n    toppings: List[String]\n\nagent Chef:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: order.valid\n    ensures: result.done\n\nagent QualityManager:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: pizza.ready\n    ensures: verdict.justified\n\nprotocol PizzaOrder:\n    roles: customer, chef, manager\n    customer asks chef to do make pizza\n    chef returns result to customer\n    customer asks manager to verify quality\n    when manager decides:\n        approve:\n            manager returns verdict to customer\n        redo:\n            manager tells chef revise pizza\n            chef returns revised to customer\n            manager returns verdict to customer\n    properties:\n        always terminates\n        no deadlock\n        chef before manager`,
        },
      ],
    },

    // ================================================================
    // CHAPTER 4: VERIFICATION
    // ================================================================
    {
      id: "verification",
      title: "Chapter 4: Putting It All Together",
      description: "Check, compile, run -- the full LU cycle",
      steps: [
        {
          id: "verify-1-check",
          title: "lu check: Validate Without Running",
          explanation: `The \`check\` command **validates** your code without executing it. It:

1. **Tokenizes**: breaks code into tokens
2. **Parses**: builds an abstract syntax tree (AST)
3. **Compiles**: generates Python source code

If any step fails, you get a clear error with the exact line and column.

Press **Check** to see the validation in action.`,
          code: `# A complete LU program -- check validates all of it\n\ntype Status = Active | Paused | Complete\n\ntype Project =\n    name: String\n    status: Status\n    confidence: Confident[Number]\n\nagent ProjectManager:\n    role: backend\n    trust: trusted\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: project.defined\n    ensures: plan.complete\n\nagent Developer:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: plan.approved\n    ensures: result.tests_pass\n\nprotocol Sprint:\n    roles: pm, dev\n    pm asks dev to do implement feature\n    dev returns result to pm\n    properties:\n        always terminates`,
          suggestedAction: "check",
          hint: "Check = parse + compile. No execution. Fast validation of your entire program.",
        },
        {
          id: "verify-2-errors",
          title: "Understanding Errors",
          explanation: `When something is wrong, LU gives you **clear, actionable errors** with:

- The exact line and column
- An error code (like \`LU-N001\`)
- A human-readable explanation
- Often a suggestion for how to fix it

This code has an intentional error. Press **Check** to see the error message, then fix it!`,
          code: `# This code has an error! Can you find and fix it?\n\ntype Color = Red | Green | Blue\n\nagent Painter\n    role: frontend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult`,
          suggestedAction: "check",
          hint: "Look at the agent definition. Something is missing after the agent name...",
          isExercise: true,
          solution: `# Fixed! The colon was missing after the agent name.\n\ntype Color = Red | Green | Blue\n\nagent Painter:\n    role: frontend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult`,
        },
        {
          id: "verify-3-run",
          title: "lu run: Execute Your Program",
          explanation: `The \`run\` command goes further than \`check\`: it **executes** the generated Python code.

After compilation, LU creates a Python module with:
- Classes for your types
- Agent descriptors with contract enforcement
- Protocol definitions with runtime checking

Press **Run** to see the full output: types, agents, protocols, and the generated Python source.`,
          code: `use python datetime\n\ntype Priority = Critical | High | Normal | Low\n\ntype DeploymentPlan =\n    target: String\n    version: String\n    priority: Priority\n    rollback: Boolean\n\ntype DeploymentResult =\n    success: Boolean\n    log: List[String]\n    duration: Number\n\nagent Architect:\n    role: backend\n    trust: trusted\n    accepts: PlanRequest\n    produces: PlanProposal\n    requires: spec.approved\n    ensures: plan.complete and plan.tested\n\nagent Builder:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: plan.approved\n    ensures: result.tests_pass\n\nagent Guardian:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires:\n        code.submitted\n        tests.pass_()\n    ensures: verdict.justified\n\nprotocol DeployPipeline:\n    roles: regina, architect, builder, guardian\n    regina asks architect to plan deployment\n    architect returns proposal to regina\n    when regina decides:\n        approve:\n            regina asks builder to do implementation\n            builder returns result to regina\n            regina asks guardian to verify deployment\n            guardian returns verdict to regina\n        reject:\n            regina tells architect revise plan\n            architect returns revised proposal to regina\n    properties:\n        always terminates\n        no deadlock\n        all roles participate\n        architect before builder\n        builder before guardian\n        builder cannot send audit_verdict`,
          suggestedAction: "run",
          hint: "Run = check + execute. Expand 'Generated Python' to see the compiled code.",
        },
        {
          id: "verify-4-finale",
          title: "The Big Picture",
          explanation: `You've learned the three pillars of Lingua Universale:

1. **Uncertainty as a type** -- \`Confident[T]\` makes AI doubt explicit
2. **Trust composition** -- \`verified > trusted > standard\` prevents privilege escalation
3. **Protocols that prove themselves** -- \`always terminates\`, \`no deadlock\`, ordering constraints

LU also supports **formal verification** via Lean 4 (the \`lu verify\` command). This mathematically proves that your protocols are correct -- not just tested, but *proven*.

Lean 4 verification runs locally (not in the browser), but every protocol you've written here CAN be formally verified.

**What's next?**
- Install LU: \`pip install cervellaswarm-lingua-universale\`
- Try the CLI: \`lu check myfile.lu\`
- Explore: \`lu repl\` for interactive experimentation
- Read the source: all 25 modules, ZERO external dependencies

*"Not faster. SAFER. With mathematical proofs, not hopes."*`,
          code: `# The complete picture: types + agents + protocols + properties\n# This is a real, verifiable LU program.\n\ntype Category = Antipasto | Primo | Secondo | Dolce\n\ntype Recipe =\n    name: String\n    category: Category\n    ingredients: List[String]\n    servings: Number\n    notes: String?\n\ntype SearchResult =\n    recipes: List[String]\n    total: Number\n\nagent RecipeManager:\n    role: backend\n    trust: standard\n    accepts: TaskRequest\n    produces: TaskResult\n    requires: request.valid\n    ensures: result.done\n\nagent QualityChecker:\n    role: guardiana\n    trust: verified\n    accepts: AuditRequest\n    produces: AuditVerdict\n    requires: data.submitted\n    ensures: verdict.justified\n\nprotocol AddRecipe:\n    roles: nonna, manager, checker\n    nonna asks manager to do save recipe\n    manager returns result to nonna\n    nonna asks checker to verify recipe data\n    checker returns verdict to nonna\n    properties:\n        always terminates\n        no deadlock\n        manager before checker`,
          suggestedAction: "run",
          hint: "This is La Nonna's recipe protocol -- a real-world domain modeled with verified guarantees.",
        },
      ],
    },
  ],
};

window.LU_TOUR = LU_TOUR;
window.LU_TOUR_VERSION = LU_TOUR_VERSION;
