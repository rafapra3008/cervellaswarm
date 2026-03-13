// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 CervellaSwarm Contributors

/**
 * Lingua Universale Playground - Preloaded Examples
 * Preloaded examples: 4 tutorials + 3 standard library protocols.
 */

const LU_EXAMPLES = [
  {
    id: "hello",
    label: "Hello World",
    description: "Basic agent + protocol structure",
    code: `type TaskStatus = Pending | Running | Done

agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: task.well_defined
    ensures: result.done

protocol DelegateTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
    properties:
        always terminates
        no deadlock
`,
  },

  {
    id: "confidence",
    label: "Confidence Types",
    description: "Confidence levels + when/decides branching",
    code: `type AnalysisStatus = InProgress | Complete | NeedsReview

type AnalysisResult =
    summary: String
    score: Confident[Number]
    details: List[String]
    status: AnalysisStatus

agent Analyst:
    role: researcher
    trust: standard
    accepts: ResearchQuery
    produces: ResearchReport
    requires: task.well_defined
    ensures: result.confidence >= 0.7

agent Reviewer:
    role: guardiana
    trust: verified
    accepts: AuditRequest
    produces: AuditVerdict
    requires: result.submitted
    ensures: verdict.justified

protocol ConfidenceReview:
    roles: analyst, reviewer, regina

    analyst returns report to regina
    regina asks reviewer to verify report
    when reviewer decides:
        approve:
            reviewer returns verdict to regina
        needs_revision:
            reviewer tells analyst revise findings
            analyst returns revised report to regina
            reviewer returns verdict to regina

    properties:
        always terminates
        no deadlock
        confidence >= high
        trust >= standard
        analyst before reviewer
`,
  },

  {
    id: "multiagent",
    label: "Multi-Agent",
    description: "Full deploy pipeline with Architect, Builder, Guardian",
    code: `use python datetime

type Priority = Critical | High | Normal | Low

type DeploymentPlan =
    target: String
    version: String
    priority: Priority
    rollback: Boolean

type DeploymentResult =
    success: Boolean
    log: List[String]
    duration: Number

agent Architect:
    role: backend
    trust: trusted
    accepts: PlanRequest
    produces: PlanProposal
    requires: spec.approved
    ensures: plan.complete and plan.tested

agent Builder:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: plan.approved
    ensures: result.tests_pass

agent Guardian:
    role: guardiana
    trust: verified
    accepts: AuditRequest
    produces: AuditVerdict
    requires:
        code.submitted
        tests.pass_()
    ensures: verdict.justified

protocol DeployPipeline:
    roles: regina, architect, builder, guardian

    regina asks architect to plan deployment
    architect returns proposal to regina

    when regina decides:
        approve:
            regina asks builder to do implementation
            builder returns result to regina
            regina asks guardian to verify deployment
            guardian returns verdict to regina
        reject:
            regina tells architect revise plan
            architect returns revised proposal to regina

    properties:
        always terminates
        no deadlock
        all roles participate
        architect before builder
        builder before guardian
        builder cannot send audit_verdict
`,
  },

  {
    id: "ricette",
    label: "La Nonna",
    description: "Recipe manager - real-world domain modeling",
    code: `type Category = Antipasto | Primo | Secondo | Dolce | Contorno

type Recipe =
    name: String
    category: Category
    ingredients: List[String]
    steps: List[String]
    servings: Number
    notes: String?

type SearchResult =
    recipes: List[String]
    total: Number

agent RecipeManager:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: request.valid
    ensures: result.done

agent QualityChecker:
    role: guardiana
    trust: verified
    accepts: AuditRequest
    produces: AuditVerdict
    requires: data.submitted
    ensures: verdict.justified

protocol AddRecipe:
    roles: nonna, manager, checker

    nonna asks manager to do save recipe
    manager returns result to nonna
    nonna asks checker to verify recipe data
    checker returns verdict to nonna

    properties:
        always terminates
        no deadlock
        manager before checker
`,
  },

  // ============================================================
  // Standard Library Examples
  // ============================================================

  {
    id: "rag_pipeline",
    label: "RAG Pipeline",
    description: "Stdlib: Retrieval-Augmented Generation (AI/ML)",
    code: `type RelevanceScore = High | Medium | Low

type Query =
    text: String
    max_results: Number
    language: String

type RetrievedDocument =
    content: String
    source: String
    relevance: RelevanceScore
    score: Number

type GeneratedAnswer =
    text: String
    sources: List[String]
    confidence: Number

agent QueryUser:
    role: user
    trust: standard
    accepts: GeneratedAnswer
    produces: Query
    requires: query.valid
    ensures: answer.received

agent DocumentRetriever:
    role: retriever
    trust: trusted
    accepts: Query
    produces: RetrievedDocument
    requires: index.available
    ensures: documents.relevant

agent AnswerGenerator:
    role: generator
    trust: trusted
    accepts: RetrievedDocument
    produces: GeneratedAnswer
    requires: context.provided
    ensures: answer.grounded

protocol RagPipeline:
    roles: user, retriever, generator

    user asks retriever to search documents
    retriever sends context to generator
    generator returns answer to user

    properties:
        always terminates
        no deadlock
        all roles participate
        retriever before generator
`,
  },

  {
    id: "auth_handshake",
    label: "Auth Handshake",
    description: "Stdlib: OAuth-inspired authentication (Security)",
    code: `type AuthMethod = Password | OAuth | ApiKey | Certificate

type AuthRequest =
    client_id: String
    method: AuthMethod
    credentials: String

type AuthToken =
    token: String
    expires_in: Number
    scope: String

type ResourceResponse =
    data: String
    status: String
    request_id: String

agent AuthClient:
    role: client
    trust: standard
    accepts: ResourceResponse
    produces: AuthRequest
    requires: credentials.valid
    ensures: token.received

agent AuthenticationServer:
    role: auth
    trust: verified
    accepts: AuthRequest
    produces: AuthToken
    requires: credentials.verified
    ensures: token.signed

agent ProtectedResource:
    role: resource
    trust: trusted
    accepts: AuthToken
    produces: ResourceResponse
    requires: token.valid
    ensures: response.authorized

protocol AuthHandshake:
    roles: client, auth, resource

    client asks auth to authenticate

    when auth decides:
        granted:
            auth returns token to client
            client asks resource to access protected data
            resource returns response to client

        denied:
            auth returns rejection to client

    properties:
        always terminates
        no deadlock
        auth before resource
        client cannot send token
`,
  },

  {
    id: "consensus",
    label: "Consensus",
    description: "Stdlib: Multi-agent voting protocol (AI/ML)",
    code: `type VoteValue = Agree | Disagree | Abstain

type Proposal =
    id: String
    description: String
    category: String
    deadline: String

type Vote =
    proposal_id: String
    value: VoteValue
    confidence: Number
    rationale: String

type ConsensusResult =
    proposal_id: String
    outcome: String
    votes_for: Number
    votes_against: Number
    quorum_reached: Boolean

agent ProposerAgent:
    role: proposer
    trust: standard
    accepts: ConsensusResult
    produces: Proposal
    requires: proposal.valid
    ensures: proposal.submitted

agent ValidatorAgent:
    role: validator
    trust: trusted
    accepts: Proposal
    produces: Vote
    requires: proposal.reviewed
    ensures: vote.cast

agent VoteAggregator:
    role: aggregator
    trust: verified
    accepts: Vote
    produces: ConsensusResult
    requires: votes.collected
    ensures: result.final

protocol Consensus:
    roles: proposer, validator, aggregator

    proposer sends proposal to validator
    validator returns vote to aggregator
    aggregator returns decision to proposer

    properties:
        always terminates
        no deadlock
        all roles participate
        confidence >= medium
        proposer before validator
        validator before aggregator
`,
  },
];

// Expose to global scope for index.html
window.LU_EXAMPLES = LU_EXAMPLES;
