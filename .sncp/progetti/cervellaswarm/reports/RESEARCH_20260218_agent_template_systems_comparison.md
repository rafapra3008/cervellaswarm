# Agent Template Systems - Framework Comparison Research

**Date:** 2026-02-18
**Researcher:** Cervella Researcher
**Status:** COMPLETE
**Sources:** 18 consulted
**Purpose:** Design best-in-class agent template system for F2.2 (CervellaSwarm open source)

---

## 1. FRAMEWORK-BY-FRAMEWORK ANALYSIS

---

### 1.1 CrewAI (44.2k stars)

**Config Format:** YAML + Python decorator pattern (dual-layer)

**File structure:**
```
src/my_crew/
  config/
    agents.yaml      <- identity: role, goal, backstory
    tasks.yaml       <- work definition
  crew.py            <- Python class with @agent, @task, @crew decorators
```

**agents.yaml - all fields:**
```yaml
researcher:
  role: "{topic} Senior Data Researcher"       # REQUIRED - what the agent IS
  goal: "Uncover cutting-edge developments"    # REQUIRED - what drives decisions
  backstory: "You are a seasoned researcher"   # REQUIRED - personality/context
  # All below are OPTIONAL, set in crew.py @agent method or inline
  # llm, tools, max_iter, verbose, allow_delegation, cache,
  # allow_code_execution, reasoning, multimodal, knowledge_sources
```

**Python layer (crew.py):**
```python
@CrewBase
class ResearchCrew:
    agents_config = "config/agents.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # loads YAML
            tools=[SerperDevTool()],                  # tools added here
            verbose=True,
            allow_delegation=True,
            reasoning=True,
        )
```

**Optional fields (26 total):**
- `llm` - model override (default: GPT-4)
- `tools` - list of tool instances
- `function_calling_llm` - separate LLM for tool calling
- `max_iter` - max iterations (default: 20)
- `max_rpm` - rate limiting
- `max_execution_time` - timeout seconds
- `verbose` - debug logging
- `allow_delegation` - peer-to-peer delegation
- `cache` - tool cache (default: True)
- `allow_code_execution` - code execution
- `code_execution_mode` - "safe" (Docker) / "unsafe"
- `max_retry_limit` - error retries (default: 2)
- `respect_context_window` - auto-summarize (default: True)
- `multimodal` - vision support
- `inject_date` - auto-inject date
- `reasoning` - reflect before acting
- `max_reasoning_attempts` - planning limit
- `system_template`, `prompt_template`, `response_template` - prompt overrides
- `embedder` - embedding config
- `knowledge_sources` - domain knowledge bases
- `use_system_prompt` - system message support
- `memory` - interaction history

**Team composition:**
```python
@CrewBase
class ResearchCrew:
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,   # or: Process.hierarchical
            verbose=True,
        )
```

**Shared behaviors:** No inheritance/mixin. Shared config is set at Crew level (memory, callbacks, default LLM). Individual agents override at @agent method level.

**Strengths:**
- Clean separation: identity (YAML) vs capabilities (Python)
- Variable interpolation: `{topic}` at kickoff time
- 3 process types: sequential, hierarchical (with manager agent), custom
- Large ecosystem of tools (CrewAI Toolkit + LangChain tools)

**Weaknesses:**
- No native versioning
- No inheritance between agent types
- YAML = identity only, tools always need Python
- No cross-session memory in YAML

---

### 1.2 AutoGen / AG2 (51.8k stars)

**Config Format:** Pure Python class instantiation. No YAML. No separate config file.

**Agent definition:**
```python
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent

agent = ConversableAgent(
    # REQUIRED
    name="researcher",

    # Core behavior
    system_message="You are a research specialist...",  # default: "You are a helpful AI Assistant."
    llm_config=LLMConfig(
        api_type="openai",
        model="gpt-4o",
        api_key="..."
    ),

    # Interaction control
    human_input_mode="NEVER",          # ALWAYS | NEVER | TERMINATE
    is_termination_msg=lambda x: ..., # callable
    max_consecutive_auto_reply=10,

    # Optional
    description="Specializes in research tasks",  # used for speaker selection
    code_execution_config=False,                   # or {"work_dir": ".", "use_docker": False}
    default_auto_reply="",
    silent=None,
    context_variables=None,
    functions=None,                    # list of tool functions
    handoffs=None,                     # swarm handoff config
    update_agent_state_before_reply=None,
    function_map=None,                 # legacy tool mapping
)
```

**Tool registration (separate from agent definition):**
```python
from autogen import register_function
from typing import Annotated

def get_weather(city: Annotated[str, "City name"]) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny"

register_function(
    get_weather,
    caller=assistant,    # agent that decides to use tool
    executor=user_proxy, # agent that executes it
    description="Get weather data"
)
```

**Team composition:**
```python
from autogen import GroupChat, GroupChatManager

groupchat = GroupChat(
    agents=[agent1, agent2, agent3],
    messages=[],
    speaker_selection_method="auto",  # or "round_robin", "random", custom callable
    max_round=10,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
agent1.initiate_chat(manager, message="Start task...")

# Alternative: Swarm pattern (structured handoffs)
from autogen import initiate_swarm_chat
initiate_swarm_chat(
    initial_agent=triage_agent,
    agents=[triage_agent, research_agent, writer_agent],
    messages="Research AI trends",
    max_rounds=10,
)
```

**Shared behaviors:** Subclassing ConversableAgent. No YAML, no shared config file. Shared behavior = Python class inheritance.

**Strengths:**
- Most flexible (pure Python, any pattern)
- Two-agent and multi-agent patterns equally supported
- Code execution built-in (Docker or local)
- Swarm pattern with explicit handoffs

**Weaknesses:**
- Zero declarative config - everything is Python
- No YAML/Markdown format at all
- No built-in versioning
- Steep learning curve (many patterns, choose your own)
- Tools require separate caller+executor pattern (confusing)

---

### 1.3 LangGraph (24.7k stars)

**Config Format:** Pure Python. StateGraph + nodes + edges. No YAML, no Markdown.

**Agent definition (low-level - StateGraph):**
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def researcher_node(state: AgentState) -> dict:
    """Research agent logic."""
    response = model.bind_tools(tools).invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    if state["messages"][-1].tool_calls:
        return "tools"
    return END

graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "researcher")
graph.add_conditional_edges("researcher", should_continue)
graph.add_edge("tools", "researcher")
app = graph.compile()
```

**High-level (prebuilt - create_react_agent):**
```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=model.bind_tools(tools),
    tools=tools,
    state_schema=AgentState,  # optional custom state
    messages_modifier="You are a research specialist...",  # system prompt
    checkpointer=MemorySaver(),  # cross-session memory
)
```

**Multi-agent team:**
```python
# Supervisor pattern
supervisor = create_react_agent(
    model,
    tools=[
        researcher.as_tool(name="researcher"),
        writer.as_tool(name="writer"),
    ]
)
# Or explicit routing graph
graph = StateGraph(TeamState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", researcher_node)
graph.add_conditional_edges("supervisor", route_to_agent)
```

**Shared behaviors:** Pure Python. Shared state schema is the "shared behavior" mechanism. Common prompts extracted to variables. No YAML config.

**Strengths:**
- Maximum flexibility (anything a graph can express)
- Built-in persistence (checkpointer) - closest to session memory
- Native streaming support
- LangGraph Cloud for deployment
- Excellent for complex conditional workflows

**Weaknesses:**
- High complexity: must understand graphs, nodes, edges, reducers
- No declarative config - 100% code
- Agent "identity" is just a Python function
- Multi-agent = manually wiring graph nodes
- Not beginner-friendly

---

### 1.4 Claude Code Native Agent System

**Config Format:** Markdown file with YAML frontmatter. The gold standard for readability.

**Full file format:**
```markdown
---
name: code-reviewer              # REQUIRED - unique, lowercase-hyphen
description: Reviews code...    # REQUIRED - when Claude delegates here

# Optional fields:
tools: Read, Grep, Glob, Bash   # allowlist (inherits all if omitted)
disallowedTools: Write, Edit    # denylist
model: sonnet                    # sonnet | opus | haiku | inherit
permissionMode: default          # default | acceptEdits | delegate | dontAsk | bypassPermissions | plan
maxTurns: 20                     # max agentic turns
skills:                          # preload skill content into context
  - api-conventions
  - error-handling-patterns
mcpServers:                      # MCP servers for this agent
  - slack
  - name: custom-db
    type: stdio
    command: ./scripts/db-server.py
hooks:                           # lifecycle hooks scoped to this agent
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
memory: user                     # user | project | local (persistent cross-session)
---

You are a senior code reviewer. [Full system prompt in Markdown follows]
```

**File locations:**
- `.claude/agents/` - project-level (version controlled, team-shared)
- `~/.claude/agents/` - user-level (all projects)
- `--agents` CLI flag - session-only (JSON format)

**Shared behaviors:** No native inheritance. CervellaSwarm's solution: `_SHARED_DNA.md` referenced via `shared_dna:` custom field and manually loaded by each agent. The official system has no equivalent - you must duplicate shared content.

**Team composition:** No explicit team config file. Teams are implicit - the main Claude session orchestrates which agents to spawn via Task tool.

**Strengths:**
- Markdown body = system prompt (intuitive, editable by anyone)
- Version-controllable plain text
- Scoped hooks per agent (unique feature)
- `memory` field for cross-session learning
- `skills` for injecting reusable knowledge
- Tool allowlist/denylist (security)
- `permissionMode` per agent

**Weaknesses:**
- No versioning fields natively (no `version:`, `compatible_with:`)
- No explicit team/crew composition config
- No inheritance/shared behavior mechanism (must duplicate)
- Tools are listed as strings (no tool config/parameters in YAML)
- No custom metadata fields supported natively

---

### 1.5 OpenAI Swarm -> Agents SDK

**Note:** Swarm (experimental, 2024) has been replaced by the **OpenAI Agents SDK** (production, March 2025).

**Swarm format (deprecated but still used as reference):**
```python
from swarm import Agent

agent = Agent(
    name="Support Agent",
    model="gpt-4o",
    instructions="Help customers with their issues",  # or callable(context_variables) -> str
    functions=[list_of_functions],  # tools as plain Python functions
    tool_choice=None,               # optional: force tool use
)
```

**OpenAI Agents SDK (2025 - production replacement):**
```python
from agents import Agent, Runner, handoff, function_tool

@function_tool
def search_database(query: str) -> str:
    """Search the knowledge base."""
    return results

specialist = Agent(
    name="Specialist",
    instructions="You handle complex cases...",
    tools=[search_database],
    model="gpt-4o",
    output_type=MyPydanticModel,    # structured output
    model_settings=ModelSettings(temperature=0.7, tool_choice="auto"),
    hooks=AgentHooks(...),          # lifecycle observers
    mcp_servers=[MCPServer(...)],   # MCP tool providers
    reset_tool_choice=True,         # prevent tool loops
)

triage = Agent(
    name="Triage",
    instructions="Route to correct specialist...",
    handoffs=[specialist],          # peer agents for delegation
)

# Team composition: Manager pattern
manager = Agent(
    name="Manager",
    tools=[
        specialist.as_tool(name="specialist", description="Handle complex cases")
    ]
)

result = Runner.run_sync(triage, "Customer has a billing issue")
```

**Handoff mechanism:**
```python
# Explicit handoff function
def transfer_to_billing():
    """Transfer to billing specialist."""
    return billing_agent

agent = Agent(functions=[transfer_to_billing])

# Or declarative handoffs list
agent = Agent(handoffs=[billing_agent, refund_agent])
```

**Shared behaviors:** Python class inheritance from Agent. No YAML config.

**Strengths:**
- Clean `@function_tool` decorator (docstring = description)
- Explicit handoffs list (declarative peer agents)
- `output_type` Pydantic for structured results
- Provider-agnostic (not just OpenAI)
- Built-in tracing
- `AgentHooks` lifecycle observers

**Weaknesses:**
- Python-only, no YAML/Markdown
- No declarative team definition
- No session memory built-in
- No versioning fields

---

## 2. COMPARISON TABLE

| Dimension | CrewAI | AutoGen/AG2 | LangGraph | Claude Code | OpenAI SDK |
|-----------|--------|-------------|-----------|-------------|------------|
| **Config format** | YAML + Python | Pure Python | Pure Python | Markdown + YAML frontmatter | Pure Python |
| **Identity definition** | role + goal + backstory | name + system_message | Python function | Markdown body (free-form) | name + instructions |
| **Required fields** | role, goal, backstory | name | name (implicit) | name, description | name |
| **Versioning** | None | None | None | None | None |
| **Tool assignment** | In Python @agent method | register_function() | model.bind_tools() | `tools:` list in frontmatter | `tools:` list in Python |
| **Shared behavior** | Crew-level config | Python inheritance | Shared state schema | Manual (no native) | Python inheritance |
| **Team definition** | Crew class + Process | GroupChat / initiate_swarm | StateGraph edges | Implicit (Task tool) | Runner + handoffs list |
| **Session memory** | No | No | Checkpointer (closest) | `memory:` field | No |
| **Agent hooks** | step_callback only | No | No | Full hook system | AgentHooks class |
| **Scoped permissions** | No | No | No | permissionMode + tools | No |
| **Beginner-friendly** | High | Low | Very Low | High | Medium |
| **Declarative** | Partial (YAML for identity) | No | No | Yes (Markdown+YAML) | No |
| **Version-controlled** | YAML files | .py files | .py files | .md files | .py files |
| **Multi-LLM** | Yes | Yes | Yes | Claude only | Yes (provider-agnostic) |

---

## 3. CervellaSwarm CURRENT FORMAT ANALYSIS

Current CervellaSwarm frontmatter (from agents like cervella-researcher.md):
```yaml
---
name: cervella-researcher
version: 2.0.0                          # UNIQUE: no other framework has this
updated: 2026-01-17                     # UNIQUE: explicit update date
compatible_with: cervellaswarm >= 1.0.0 # UNIQUE: semver compatibility
description: Specialista ricerca...
tools: Read, Glob, Grep, Write, WebSearch, WebFetch
model: sonnet
shared_dna: _SHARED_DNA.md             # UNIQUE: explicit shared DNA reference
---
```

**What CervellaSwarm has that no competitor has:**
1. `version:` field with semver
2. `updated:` date stamp
3. `compatible_with:` semver range
4. `shared_dna:` reference to shared behavior file
5. `_SHARED_DNA.md` pattern (explicit DNA inheritance)
6. `memory: user` (from Guardiana agents) - this one IS native Claude Code

**What CervellaSwarm is missing vs Claude Code native:**
1. `permissionMode:` - could add
2. `maxTurns:` - could add
3. `skills:` - could add
4. `hooks:` in frontmatter - could add
5. `mcpServers:` - could add

---

## 4. BEST PRACTICES FROM THE BIG TEAMS

### What CrewAI does right
- **Separation of identity vs capability**: YAML = WHO the agent is, Python = WHAT it can do
- **Variable interpolation**: `{topic}` at runtime is elegant
- **3-tier complexity**: minimal (just YAML) -> standard (YAML + Python) -> advanced (full class)
- **Role/Goal/Backstory trinity**: memorable, teachable, industry-adopted pattern

### What Claude Code does right
- **Markdown body = system prompt**: non-technical editors can contribute
- **YAML frontmatter = metadata**: clean separation of config vs content
- **Scoped hooks**: hooks per agent are unique and powerful
- **memory field**: cross-session learning is a differentiator
- **permissionMode**: security per agent is unique

### What OpenAI SDK does right
- **@function_tool decorator**: docstring-as-description is clean DX
- **handoffs list**: explicit declarative peer routing
- **output_type Pydantic**: structured output built-in

### What ALL frameworks get wrong
- **No versioning**: nobody tracks `version:` or `compatible_with:`
- **No shared behavior mechanism**: all rely on copy-paste or Python inheritance
- **No team composition file**: teams are implicit or code-only
- **No audit trail**: `updated:` date is CervellaSwarm-unique
- **No explicit capability/constraint declaration**: what the agent CAN and CANNOT do

---

## 5. RECOMMENDATION FOR F2.2 AGENT TEMPLATES

### Proposed CervellaSwarm Enhanced Format

The recommended format builds on what CervellaSwarm already has, absorbing Claude Code native fields it was missing, and adding the best patterns from competitors:

```markdown
---
# ===== IDENTITY (what the agent IS - inspired by CrewAI) =====
name: coordinator                              # REQUIRED - unique identifier
version: 1.0.0                                 # CERVELLASWARM: semver
updated: 2026-02-18                            # CERVELLASWARM: last update date
compatible_with: cervellaswarm >= 2.0.0        # CERVELLASWARM: semver range

# ===== DELEGATION (when to use this agent) =====
description: >
  Coordinates parallel worker agents for complex tasks.
  Use for tasks requiring 3+ specialized workers.
role: Coordinator                              # OPTIONAL: human-readable role label (CrewAI-inspired)

# ===== CAPABILITIES (what it can do) =====
model: opus                                    # sonnet | opus | haiku | inherit
tools: Read, Bash, Task                        # allowlist
disallowedTools: Write, Edit                   # denylist
permissionMode: default                        # Claude Code native
maxTurns: 30                                   # Claude Code native

# ===== KNOWLEDGE (what it knows) =====
shared_dna: _SHARED_DNA.md                    # CERVELLASWARM: shared behavior
skills:                                        # Claude Code native
  - api-conventions
  - error-handling-patterns

# ===== MEMORY (what it remembers) =====
memory: user                                   # Claude Code native: user | project | local

# ===== INTEGRATIONS =====
mcpServers:                                    # Claude Code native
  - slack

# ===== LIFECYCLE HOOKS =====
hooks:                                         # Claude Code native
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
---

# Agent: [Name]

> **DNA condiviso:** See `~/.claude/agents/_SHARED_DNA.md`

[Role description in Markdown - the system prompt]

## Role
[What this agent IS]

## Goal
[What drives this agent's decisions]

## Capabilities
[What it can do, what it cannot do - explicit]

## Process
[Step-by-step workflow]

## Output Format
[Expected output structure]
```

### Three template tiers for F2.2

**Tier 1: Minimal (3-agent team)**
- coordinator + worker + quality-gate
- Minimal fields: name, description, model, tools, shared_dna
- Target: devs starting fresh

**Tier 2: Standard (7-agent team)**
- coordinator + architect + 3 workers + quality-gate + researcher
- Standard fields: + version, updated, memory, maxTurns
- Target: production teams

**Tier 3: Full (17-agent team)**
- Full CervellaSwarm: all 5 tiers (Regina + Guardiane + Architect + Analiste + Workers)
- All fields: + hooks, skills, mcpServers, permissionMode
- Target: advanced teams

### Key differentiators to keep in F2.2

1. **version + compatible_with** - nobody else does this. Makes upgrades safe.
2. **shared_dna reference** - solves the shared behavior problem elegantly without Python
3. **updated date** - audit trail, unique to CervellaSwarm
4. **role:** label - bridging CrewAI's strong mental model with Claude Code's format
5. **Explicit capability declarations** - "IO NON SCRIVO CODICE!" in Architect body = self-enforcing constraints

### What to add in F2.2

6. **permissionMode** - already native, not yet in our templates
7. **maxTurns** - already native, not yet in our templates
8. **skills** - already native, could preload SNCP patterns
9. **hooks in frontmatter** - agents with built-in validation (db-reader pattern)
10. **output_type pattern** - standardize output format in Markdown body (like we do now, but consistently)

---

## 6. TEAM COMPOSITION GAP

None of the 5 frameworks has a good **team composition file**. All rely on code or implicit convention.

CervellaSwarm opportunity: Create a `team.yaml` concept for F2.2:

```yaml
# .claude/team.yaml
name: research-team
version: 1.0.0
description: 3-agent research team

agents:
  - ref: coordinator    # references agent file by name
    role: lead
  - ref: researcher
    role: worker
  - ref: quality-gate
    role: validator

process: hierarchical   # sequential | hierarchical | parallel
max_parallel: 3
entry_point: coordinator

shared_context:
  project_root: "."
  sncp_path: ".sncp/progetti/{project}/"
```

This would be a **genuine differentiator** - no other framework has declarative team composition in a separate file.

---

## SOURCES CONSULTED (18)

1. https://docs.crewai.com/en/concepts/agents - Official CrewAI agents docs
2. https://codesignal.com/learn/courses/getting-started-with-crewai-agents-and-tasks/lessons/configuring-crewai-agents-and-tasks-with-yaml-files
3. https://community.crewai.com/t/which-task-and-agent-attributes-can-be-put-in-the-yaml-file/4486
4. https://docs.ag2.ai/latest/docs/home/quickstart/ - AG2 quickstart
5. https://docs.ag2.ai/latest/docs/user-guide/basic-concepts/conversable-agent/ - ConversableAgent
6. https://github.com/ag2ai/ag2/blob/main/autogen/agentchat/conversable_agent.py - Source of truth for fields
7. https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/ - LangGraph ReAct
8. https://reference.langchain.com/python/langgraph/agents/ - LangGraph agents ref
9. https://code.claude.com/docs/en/sub-agents - Official Claude Code sub-agents docs (FULL READ)
10. https://openai.github.io/openai-agents-python/ - OpenAI Agents SDK
11. https://openai.github.io/openai-agents-python/agents/ - Agent class reference
12. https://github.com/openai/swarm - Swarm (deprecated, for reference)
13. https://cookbook.openai.com/examples/orchestrating_agents - Routines and handoffs
14. https://stevekinney.com/courses/ai-development/claude-code-sub-agents - Sub-agents guide
15. https://claudelog.com/mechanics/custom-agents/ - Custom agents patterns
16. Internal: /Users/rafapra/.claude/agents/cervella-researcher.md
17. Internal: /Users/rafapra/.claude/agents/cervella-architect.md
18. Internal: /Users/rafapra/.claude/agents/cervella-guardiana-qualita.md

---

*Cervella Researcher - 2026-02-18 - F2.2 Research Complete*
