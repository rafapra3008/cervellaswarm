# Lingua Universale Standard Library

20 verified protocols across 5 categories. Every protocol parses, compiles,
and verifies with `lu verify`.

## Categories

### Communication (5)

| Protocol | File | Roles | Key Properties |
|----------|------|-------|----------------|
| **RequestResponse** | `communication/request_response.lu` | client, server | always terminates, no deadlock |
| **PingPong** | `communication/ping_pong.lu` | checker, service | always terminates, no deadlock |
| **PubSub** | `communication/pub_sub.lu` | publisher, broker, subscriber | all roles participate |
| **ScatterGather** | `communication/scatter_gather.lu` | coordinator, worker, aggregator | all roles participate |
| **Pipeline** | `communication/pipeline.lu` | source, processor, transformer, sink | ordering (source before processor before transformer before sink) |

### Data (3)

| Protocol | File | Roles | Key Properties |
|----------|------|-------|----------------|
| **CrudSafe** | `data/crud_safe.lu` | client, store, auditor | **no deletion**, all roles participate |
| **DataSync** | `data/data_sync.lu` | primary, replica, monitor | ordering (primary before replica) |
| **CacheInvalidation** | `data/cache_invalidation.lu` | writer, cache, reader | choice (hit/miss), all roles participate |

### Business (4)

| Protocol | File | Roles | Key Properties |
|----------|------|-------|----------------|
| **TwoBuyer** | `business/two_buyer.lu` | buyer1, buyer2, seller | MPST canonical (Honda/Yoshida POPL 2008) |
| **ApprovalWorkflow** | `business/approval_workflow.lu` | requester, approver, notifier | **role exclusive** (only approver decides) |
| **Auction** | `business/auction.lu` | auctioneer, bidder, recorder | choice (sold/unsold) |
| **SagaOrder** | `business/saga_order.lu` | coordinator, payment, inventory | distributed transaction, ordering |

### AI/ML (5)

| Protocol | File | Roles | Key Properties |
|----------|------|-------|----------------|
| **RagPipeline** | `ai_ml/rag_pipeline.lu` | user, retriever, generator | ordering (retriever before generator) |
| **AgentDelegation** | `ai_ml/agent_delegation.lu` | supervisor, worker, validator | trust >= standard, ordering |
| **ToolCalling** | `ai_ml/tool_calling.lu` | agent, registry, executor | ordering (registry before executor) |
| **HumanInLoop** | `ai_ml/human_in_loop.lu` | agent, human, logger | **role exclusive** (only human decides) |
| **Consensus** | `ai_ml/consensus.lu` | proposer, validator, aggregator | all roles participate, ordering, **confidence >= medium** |

### Security (3)

| Protocol | File | Roles | Key Properties |
|----------|------|-------|----------------|
| **AuthHandshake** | `security/auth_handshake.lu` | client, auth, resource | ordering (auth before resource), **exclusion** (client cannot send token) |
| **MutualTls** | `security/mutual_tls.lu` | client, server | all roles participate, ordering (client before server) |
| **RateLimitedApi** | `security/rate_limited_api.lu` | client, limiter, backend | **role exclusive** (only limiter throttles) |

## Usage

```bash
# Verify any protocol
lu verify stdlib/communication/request_response.lu

# Check syntax
lu check stdlib/ai_ml/rag_pipeline.lu

# Use as template for your own protocol
cp stdlib/business/approval_workflow.lu my_workflow.lu
```

## Property Coverage (all 9 PropertyKind)

| Property | Protocols |
|----------|-----------|
| `always terminates` | All 20 (structural guarantee for finite protocols) |
| `no deadlock` | All 20 (structural guarantee for finite protocols) |
| `all roles participate` | 15 protocols |
| `no deletion` | CrudSafe |
| `role exclusive` | ApprovalWorkflow, HumanInLoop, RateLimitedApi |
| `ordering` | Pipeline, DataSync, SagaOrder, RagPipeline, AgentDelegation, ToolCalling, Consensus, AuthHandshake, TwoBuyer, MutualTls |
| `exclusion` | AuthHandshake (client cannot send token) |
| `confidence >= level` | Consensus (confidence >= medium) |
| `trust >= tier` | AgentDelegation (trust >= standard) |

## Academic References

- **TwoBuyer**: Honda, Yoshida, Carbone - POPL 2008 (foundational MPST)
- **Auction**: Honda/Yoshida electronic auction (MPST literature)
- **AuthHandshake**: Scribble Project OAuth 2.0 (Imperial College London)
- **ScatterGather**: DMst ECOOP 2023 (dynamic task delegation)
- **SagaOrder**: Microservices saga pattern (distributed transactions)
