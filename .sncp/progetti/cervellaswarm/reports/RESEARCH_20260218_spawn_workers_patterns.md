# Spawn Workers Patterns - Ricerca F2.4
**Data:** 2026-02-18
**Researcher:** Cervella Researcher
**Status:** COMPLETA
**Fonti:** 18 consultate (5 framework + 3 tool tmux/process + 4 pattern process + 3 web + 3 competitor + spawn-workers.sh esistente)

---

## Obiettivo

Ricercare come i principali framework multi-agent lanciano worker paralleli, con focus su:
- Modelli di esecuzione parallela (in-process vs subprocess vs terminal)
- Config-driven spawning (YAML/JSON team definition)
- Portabilita macOS + Linux
- Best practices per PID tracking, signal handling, cleanup

---

## 1. Come Lanciano i Worker i Framework Principali

### 1.1 CrewAI - Thread/Async via asyncio

**Meccanismo:** Tutto in-process. Zero subprocess separati.

- `kickoff()` = esecuzione sincrona sequenziale dentro lo stesso processo Python
- `kickoff_async()` = wrappa `kickoff()` in `asyncio.to_thread` (thread pool, non veri processi)
- `akickoff()` = vera async con `async/await` per ogni task (raccomandato per high-concurrency)
- Parallelismo tra crew: `asyncio.gather(crew1.akickoff(), crew2.akickoff())`
- Task paralleli dentro un crew: `task.async_execution = True` + `context` per dipendenze

**Config format (agents.yaml):**
```yaml
researcher:
  role: '{topic} Senior Data Researcher'
  goal: 'Uncover cutting-edge developments in {topic}'
  backstory: 'You are a seasoned researcher...'
```

**Differenziale CervellaSwarm vs CrewAI:**
- CrewAI: in-process threads, tutto condivide la stessa RAM e contesto
- CervellaSwarm: processi separati (tmux), isolamento totale del contesto per worker
- CervellaSwarm ha file-based state (.ready/.working/.done), CrewAI ha state LLM-driven

### 1.2 AutoGen - Sequential GroupChat, Async via Core API

**Meccanismo:** GroupChat e' sequenziale by design.

- GroupChat v0.2: un agente alla volta, round-robin o selector
- GroupChat v0.4 Core API: supporto parallelismo via `RoundRobinGroupChat` e `SelectorGroupChat`
- Parallelismo vero: `a_initiate_chats()` per task multipli su agenti dedicati concorrenti
- Problema aperto (Feb 2025): "calling two agents simultaneously within NestedChat has challenges"

**Pattern parallelo AutoGen:**
```python
await asyncio.gather(
    agent1.a_initiate_chat(task1),
    agent2.a_initiate_chat(task2)
)
```

**Differenziale CervellaSwarm:** AutoGen non ha health tracking, PID files, o tmux sessions. Tutto in-process.

### 1.3 LangGraph - Fan-out/Fan-in con Supersteps

**Meccanismo:** Graph-based routing, worker come nodi del grafo.

- Fan-out: nodo A con edge multipli -> nodi B, C, D (eseguiti in parallelo nel superstep)
- Superstep: unita di esecuzione che raggruppa nodi concorrenti, tutti devono finire prima del prossimo step
- Send API: dispatch dinamico di worker in parallelo, poi fan-in
- `max_concurrency`: parametro per limitare quanti nodi girano contemporaneamente
- Deferred nodes (2025): nodo eseguito solo dopo che tutti i branch paralleli completano

**Pattern fan-out LangGraph:**
```python
# Nodi paralleli automatici (stessa superstep)
graph.add_edge("router", "worker_a")
graph.add_edge("router", "worker_b")
graph.add_edge("worker_a", "collector")
graph.add_edge("worker_b", "collector")
```

**Differenziale CervellaSwarm:** LangGraph non ha tmux/subprocess. E' in-memory, zero persistenza file-based. Nessun mechanism di auto-sveglia Regina.

### 1.4 OpenAI Agents SDK - asyncio.gather + Handoff

**Meccanismo:** In-process async, handoff come tool call LLM.

- Handoff: un agente trasferisce controllo a un sub-agente tramite tool call
- Agent-as-tool: agente principale chiama sub-agenti come tool (non trasferisce controllo)
- Parallelismo: `asyncio.gather(agent1.run(), agent2.run())` per task indipendenti
- Guardrails: validazioni input/output girano in parallelo con l'esecuzione principale

**Differenziale CervellaSwarm:** SDK OpenAI richiede API key per ogni worker. CervellaSwarm usa Claude Max (unset ANTHROPIC_API_KEY) - zero costi aggiuntivi per worker.

### 1.5 Claude Code Task Tool - Ephemeral Subagents in-process

**Meccanismo:** Task tool spawna subagent come worker temporanei, tutto in-process dentro Claude Code.

- Ogni Task = contesto isolato 200K token
- Parallelismo: max 10 task simultanei, poi batch (attende completamento batch prima del prossimo)
- Subagents vs Task tool: stessa engine, subagents hanno config persistente in `.claude/agents/`
- Task tool deve essere in allowedTools per poter usarlo

**Differenziale CervellaSwarm:** Claude Code non ha persistenza file-based dello stato worker, no PID tracking, no health check, no tmux sessions monitorate. CervellaSwarm aggiunge tutte queste feature sopra.

---

## 2. Terminal Multiplexing per Agenti AI

### 2.1 tmux - Il Denominatore Comune (RACCOMANDATO)

**Disponibilita:** macOS (Homebrew: `brew install tmux`) + Linux (tutti i package manager). POSIX standard.

**Pattern programmatico:**
```bash
# Crea sessione detached
tmux new-session -d -s "swarm_worker_backend_$(date +%s)"

# Verifica esistenza
tmux has-session -t "$SESSION_NAME" 2>/dev/null

# Invia comando a sessione
tmux send-keys -t "$SESSION_NAME" "claude --command '...'" C-m

# Attendi segnale di completamento
tmux wait-for -S "worker_done"

# Elenca sessioni
tmux list-sessions

# Kill sessione
tmux kill-session -t "$SESSION_NAME"

# remain-on-exit: mantieni pane aperto dopo fine processo
tmux set-option -t "$SESSION_NAME" remain-on-exit on
```

**Tool Python per tmux:** `libtmux` (agent-conductor lo usa), `tmuxp` per session manager YAML.

**Limitations:** richiede che tmux sia installato. Non disponibile out-of-the-box su macOS senza Homebrew.

### 2.2 Analisi: Cosa fa gia spawn-workers.sh v4.1.0

Il nostro script esistente (665 righe) implementa gia:
- tmux headless come DEFAULT (v3.1.0+)
- Terminal.app via AppleScript come fallback (--window flag)
- PID tracking via .pid files in .swarm/status/
- Health tracking: timestamp start, worker name, session name
- remain-on-exit per catturare output dopo fine worker
- MAX_WORKERS limit (default 5)
- AUTO-SVEGLIA watcher-regina.sh

**Gap identificati nello script esistente:**
1. **Config file non supportato**: worker definiti hardcoded nello script (case statement)
2. **Nessun signal handling**: SIGINT/SIGTERM non propagato ai worker figli
3. **Cleanup incompleto**: tmux sessions rimangono dopo crash del parent
4. **Linux headless senza GUI**: funziona ma nessun test documentato
5. **Prompt hardcoded**: il prompt worker e' dentro lo script, non in file config separato
6. **No process group**: ogni worker e' sessione tmux indipendente, no group kill

### 2.3 Terminal.app (macOS) - AppleScript

**Pattern attuale (spawn_worker() in spawn-workers.sh):**
```applescript
tell application "Terminal"
    do script "$runner_script"
end tell
```

**Limitazioni:**
- Funziona SOLO su macOS
- Richiede accesso Accessibility
- Finestre rimangono aperte (side effect visivo)
- Non portable su Linux/CI

### 2.4 screen - Alternativa a tmux

**Pattern:**
```bash
screen -dmS "swarm_backend" bash -c "claude --command '...' > worker.log 2>&1"
screen -list  # elenca sessioni
screen -S "swarm_backend" -X quit  # kill sessione
```

**Valutazione:** screen e' disponibile su piu sistemi di default, ma tmux e' piu moderno, ha API piu pulita, e il nostro codice usa gia tmux. Manteniamo tmux.

### 2.5 nohup + Background Process - Headless Puro

**Pattern:**
```bash
nohup claude --command '...' > worker.log 2>&1 &
echo $! > worker.pid  # salva PID
wait $!  # attendi completamento
```

**Vantaggi:** disponibile su qualsiasi Unix, zero dipendenze, funziona in CI/CD headless.
**Svantaggi:** non puoi riattaccarti, no session management, output solo su file.

**Raccomandazione:** nohup come fallback se tmux non disponibile.

---

## 3. Config-Driven Worker Spawning

### 3.1 Analisi Competitor

**CrewAI agents.yaml:**
```yaml
researcher:
  role: Senior Researcher
  goal: Find cutting-edge info
  backstory: You are experienced...
```
Mapping: nome chiave YAML -> istanza Agent Python. Kickoff automatico.

**agent-conductor (gaurav-yadav):**
- Usa markdown con YAML frontmatter per agent profiles
- libtmux per creare pane nel tmux
- CLI: `acd worker <session>` per spawn
- SQLite per persistenza stato
- Limitazione: local-only, Unix-only, richiede Python 3.11+ e uv

**CervellaSwarm agent-templates (F2.2 - nostro package):**
```yaml
# team.yaml
name: my-project
version: 1.0.0
agents:
  - name: backend
    type: worker
    specialty: backend
    role: worker
  - name: tester
    type: worker
    specialty: tester
    role: worker
entry_point: lead
process: hierarchical
```
**Questo e' gia il nostro differenziale!** Il nostro team.yaml e' pronto da usare per config-driven spawning.

### 3.2 Pattern Raccomandato: team.yaml -> Spawn

Il package F2.4 dovrebbe leggere il `team.yaml` e spawna i worker definiti:

```python
# cervellaswarm_spawn_workers/spawner.py
def spawn_team(team_yaml_path: str, tasks_dir: str) -> SpawnResult:
    team = load_team_yaml(team_yaml_path)
    workers = [a for a in team.agents if a.role == "worker"]
    return spawn_workers(workers, tasks_dir)
```

### 3.3 Context Passing ai Worker

**Metodi (dal migliore al peggiore):**

1. **File system** (nostro metodo attuale): prompt file in `.swarm/prompts/worker_X.txt`
   - Sicuro, persistente, debuggabile
   - Claude legge con `--append-system-prompt "$(cat file.txt)"`

2. **Env vars**: `WORKER_TYPE=backend TASK_ID=123 claude -p "..."`
   - Semplice per metadata piccola
   - NON per prompt grandi (limite OS ~32KB)

3. **Stdin**: `echo "$prompt" | claude -p --stdin`
   - Non supportato nativamente da claude CLI

4. **--system-prompt flag**: passato direttamente
   - Problema con caratteri speciali, escape issues
   - Usiamo gia `--append-system-prompt` via file = approccio corretto

### 3.4 Pool vs On-Demand

**Pool di worker (pre-spawn):**
- Vantaggi: pronti immediatamente, warm start
- Svantaggi: consumano risorse anche idle, difficile scalare

**On-demand spawn (nostro approccio attuale):**
- Vantaggi: zero overhead idle, semplice, naturale per Claude
- Svantaggi: cold start (pochi secondi per avviare Claude CLI)
- **Raccomandazione: mantieni on-demand**, aggiunge config-driven sopra

---

## 4. Best Practices CLI con Processi Paralleli

### 4.1 PID Tracking

**Pattern attuale (buono):**
```bash
echo $! > ".swarm/status/worker_${name}.pid"
```

**Pattern migliorato con process group:**
```bash
# Usa setsid per creare process group isolato
setsid claude --command "..." &
PGID=$!
echo $PGID > ".swarm/status/worker_${name}.pgid"

# Kill group intero (tutti i figli)
kill -- -$(cat ".swarm/status/worker_${name}.pgid")
```

### 4.2 Signal Handling (GAP CRITICO)

**Problema attuale:** Se spawn-workers.sh riceve SIGINT (Ctrl+C), le sessioni tmux rimangono orfane.

**Pattern corretto:**
```bash
WORKER_SESSIONS=()

cleanup() {
    echo "Cleanup: killing all worker sessions..."
    for session in "${WORKER_SESSIONS[@]}"; do
        tmux kill-session -t "$session" 2>/dev/null
        echo "Killed: $session"
    done
}

trap cleanup SIGINT SIGTERM EXIT

# Spawn worker
tmux new-session -d -s "$session_name" "..."
WORKER_SESSIONS+=("$session_name")
```

**Pattern Python (piu robusto):**
```python
import signal, subprocess, atexit

processes = []

def cleanup(signum=None, frame=None):
    for p in processes:
        p.terminate()
    # Se non terminano in 3s, kill
    for p in processes:
        try:
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            p.kill()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
atexit.register(cleanup)
```

### 4.3 Output Management

**Pattern attuale (buono):** ogni worker scrive su `.swarm/logs/worker_NAME_TIMESTAMP.log`

**Pattern migliorato:**
```bash
# Structured log con timestamp e worker name prefix
exec > >(while IFS= read -r line; do
    echo "[$(date +%H:%M:%S)] [${WORKER_NAME}] $line"
done | tee "${LOG_FILE}")
```

**Raccomandazione:** Mantieni log separati per worker. Aggiungi log aggregator opzionale per vedere tutto insieme.

### 4.4 Health Check

**Pattern attuale (buono):** heartbeat log ogni 60s

**Pattern migliorato con tmux check:**
```bash
is_worker_alive() {
    local session="$1"
    tmux has-session -t "$session" 2>/dev/null
}

check_all_workers() {
    for session in "${WORKER_SESSIONS[@]}"; do
        if ! is_worker_alive "$session"; then
            echo "DEAD: $session"
        fi
    done
}
```

---

## 5. Portabilita macOS + Linux

### 5.1 Matrice Disponibilita Tool

| Tool | macOS (default) | macOS (Homebrew) | Linux (Ubuntu) | Linux (Alpine) | CI/CD |
|------|----------------|-----------------|----------------|----------------|-------|
| tmux | NO | SI | SI | SI (apk add) | SI |
| screen | SI | - | SI | SI | SI |
| nohup | SI | - | SI | SI | SI |
| Terminal.app | SI | - | NO | NO | NO |
| AppleScript | SI | - | NO | NO | NO |
| osascript | SI | - | NO | NO | NO |

### 5.2 Strategia Portabilita

**Tier 1 (usare sempre):** nohup + background process (`&` + `$!`)
**Tier 2 (usare se disponibile):** tmux (migliore UX, session management)
**Tier 3 (solo macOS):** Terminal.app + AppleScript (mantenuto come --window legacy)

**Detection pattern:**
```bash
if command -v tmux &>/dev/null; then
    SPAWN_MODE="tmux"
elif command -v screen &>/dev/null; then
    SPAWN_MODE="screen"
else
    SPAWN_MODE="nohup"
fi
```

### 5.3 stat Command (macOS vs Linux)

**Problema noto in spawn-workers.sh:** stat differisce su macOS e Linux.

```bash
# macOS
stat -f %u "$file"   # owner UID
stat -f %Lp "$file"  # permissions

# Linux
stat -c %u "$file"   # owner UID
stat -c %a "$file"   # permissions
```

Lo script esistente gia gestisce questo con `$OSTYPE` check - BENE.

---

## 6. Differenziali Unici CervellaSwarm

### 6.1 Cosa NESSUN competitor fa

| Feature | CrewAI | AutoGen | LangGraph | OpenAI SDK | agent-conductor | CervellaSwarm |
|---------|--------|---------|-----------|------------|-----------------|---------------|
| File-based state (.ready/.working/.done) | NO | NO | NO | NO | NO | SI |
| Atomic race protection (open `x` mode) | NO | NO | NO | NO | NO | SI |
| team.yaml config-driven spawn | YAML (agents.yaml) | NO | NO | NO | markdown | SI (unico con team composition) |
| tmux headless + Terminal.app fallback | NO | NO | NO | NO | pane tmux | SI |
| Auto-watcher (sveglia Regina) | NO | NO | NO | NO | NO | SI |
| Claude Max (zero API cost) | NO | NO | NO | NO | NO | SI (unset ANTHROPIC_API_KEY) |
| PID + session tracking | NO | NO | NO | NO | parziale | SI |
| Heartbeat logging ogni 60s | NO | NO | NO | NO | NO | SI |
| Output validation post-task | NO | NO | NO | NO | NO | SI (Reflection Pattern) |
| Auto-context codebase (tree-sitter) | NO | NO | NO | NO | NO | SI |
| Process portability (tmux+nohup fallback) | NO | NO | NO | NO | NO | **DA AGGIUNGERE in F2.4** |
| Signal handling cleanup | NO | parziale | NO | NO | NO | **DA AGGIUNGERE in F2.4** |

### 6.2 Gap da Chiudere in F2.4

**P1 (critici per portabilita):**
1. **nohup fallback**: se tmux non disponibile, usa nohup + `$!` PID tracking
2. **Signal handling**: trap SIGINT/SIGTERM per kill tutte le sessioni tmux alla chiusura
3. **Config-driven spawn da team.yaml**: leggi agents da file invece di hardcoded case statement

**P2 (miglioramenti importanti):**
4. **Process group management**: `setsid` + `kill -- -$PGID` per kill robusto
5. **Worker status command**: `spawn-workers --status` per vedere chi e' vivo
6. **Graceful shutdown**: SIGTERM prima, poi SIGKILL dopo timeout

**P3 (nice to have):**
7. **Screen fallback**: se tmux non disponibile ma screen si
8. **Aggregated log view**: `spawn-workers --logs` per vedere tutti i worker live

---

## 7. Raccomandazione per il Package F2.4

### 7.1 Nome Package

`cervellaswarm-spawn-workers` v0.1.0

### 7.2 Architettura Raccomandata

```
packages/spawn-workers/
├── src/cervellaswarm_spawn_workers/
│   ├── __init__.py
│   ├── spawner.py          # Core: spawn_worker(), spawn_team()
│   ├── team_loader.py      # Legge team.yaml, valida schema
│   ├── process_manager.py  # PID tracking, health check, cleanup
│   ├── backend.py          # Backends: tmux, nohup, screen (auto-detect)
│   └── cli.py              # Entry points CLI
├── tests/
└── pyproject.toml
```

### 7.3 CLI Entry Points Raccomandati

```bash
cervella-spawn --team team.yaml           # Spawna dal team.yaml
cervella-spawn --worker backend           # Spawna singolo worker
cervella-spawn --all                      # Spawna tutti i worker del team
cervella-spawn --status                   # Mostra worker vivi/morti
cervella-spawn --kill                     # Kill tutti i worker
cervella-spawn --logs                     # Mostra log aggregati (tail -f)
```

### 7.4 Config Schema (team.yaml esteso per spawn)

```yaml
# Aggiunge sezione spawn al team.yaml esistente
name: my-project
spawn:
  backend: tmux   # tmux | nohup | screen (auto-detect se omesso)
  max_workers: 5
  tasks_dir: .swarm/tasks
  logs_dir: .swarm/logs
agents:
  - name: backend
    type: worker
    specialty: backend
    role: worker
    # Nuovo campo per spawn:
    spawn_on_start: true  # spawna automaticamente con --all
```

### 7.5 Backend Detection (auto-detect + fallback)

```python
def detect_backend() -> str:
    """Auto-detect migliore backend disponibile."""
    import shutil
    if shutil.which("tmux"):
        return "tmux"
    elif shutil.which("screen"):
        return "screen"
    else:
        return "nohup"  # sempre disponibile su Unix
```

### 7.6 Signal Handling (da implementare)

```python
import signal, atexit

class SpawnManager:
    def __init__(self):
        self.sessions = []  # tmux session names
        self.pids = []      # nohup PIDs
        signal.signal(signal.SIGINT, self._cleanup)
        signal.signal(signal.SIGTERM, self._cleanup)
        atexit.register(self._cleanup)

    def _cleanup(self, *args):
        for session in self.sessions:
            subprocess.run(["tmux", "kill-session", "-t", session],
                          capture_output=True)
        for pid in self.pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
```

---

## 8. Sintesi Finale

**Trovati (ricerca completa):**
- CrewAI: in-process asyncio.gather - zero subprocess, zero file state
- AutoGen: sequential GroupChat, Core API per async - zero file state
- LangGraph: graph supersteps - deterministico ma zero persistenza
- OpenAI SDK: asyncio.gather + handoff tool call - in-process
- Claude Code Task tool: ephemeral subagents max 10 paralleli
- agent-conductor: tmux panes via libtmux, SQLite, local-only

**Differenziali confermati CervellaSwarm (unici nel mercato):**
1. File-based state machine (.ready/.working/.done) con race protection
2. Claude Max support (zero API cost per worker)
3. team.yaml come config format che gia abbiamo (F2.2)
4. Auto-watcher per svegliare la Regina al completamento

**Da aggiungere in F2.4:**
1. Config-driven spawn da team.yaml (leggere agents, spawnarli)
2. nohup fallback se tmux non disponibile (Linux portabilita)
3. Signal handling SIGINT/SIGTERM per cleanup pulito
4. `cervella-spawn --status` per health check worker

**Pattern consigliato per CLI:**
```bash
# Auto-detect backend, spawn da config
cervella-spawn --team .cervella/team.yaml

# Override backend
cervella-spawn --team team.yaml --backend nohup

# Gestione lifecycle
cervella-spawn --status
cervella-spawn --kill
```

---

## Fonti Consultate

- [CrewAI Kickoff Async Docs](https://docs.crewai.com/en/learn/kickoff-async)
- [CrewAI Agents Config YAML](https://docs.crewai.com/en/concepts/agents)
- [AutoGen Parallel Agent Execution Issue](https://github.com/microsoft/autogen/issues/5359)
- [AutoGen GroupChat Research Pattern](https://autogenhub.github.io/autogen/docs/notebooks/agentchat_groupchat_research/)
- [LangGraph Fan-out Best Practices](https://forum.langchain.com/t/best-practices-for-parallel-nodes-fanouts/1900)
- [LangGraph Branching Docs](https://www.baihezi.com/mirrors/langgraph/how-tos/branching/index.html)
- [OpenAI Agents SDK Multi-Agent](https://openai.github.io/openai-agents-python/multi_agent/)
- [OpenAI Swarm GitHub](https://github.com/openai/swarm)
- [Claude Code Subagents Docs](https://platform.claude.com/docs/en/agent-sdk/subagents)
- [Claude Code Task Tool Guide](https://cuong.io/blog/2025/06/24-claude-code-subagent-deep-dive)
- [agent-conductor GitHub](https://github.com/gaurav-yadav/agent-conductor)
- [tmux Programmatic Session Creation](https://www.geeksforgeeks.org/linux-unix/how-to-create-tmux-session-with-a-script/)
- [nohup vs tmux vs screen Comparison](https://gist.github.com/MangaD/632e8f5a6649c9b2e30e2e5d3926447b)
- [Bash Signal Propagation to Children](https://veithen.io/2014/11/16/sigterm-propagation.html)
- [Kill Process Group Baeldung](https://www.baeldung.com/linux/kill-members-process-group)
- [Python subprocess Popen Patterns](https://docs.python.org/3/library/subprocess.html)
- [Python asyncio Subprocess](https://docs.python.org/3/library/asyncio-subprocess.html)
- [Sub-Agent Spawning Patterns](https://agentic-patterns.com/patterns/sub-agent-spawning/)

---

*Report salvato: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260218_spawn_workers_patterns.md`*
*Sessione: S372 - F2.4 prep*
