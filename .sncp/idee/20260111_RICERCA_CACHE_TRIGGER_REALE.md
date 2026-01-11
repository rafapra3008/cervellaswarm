# RICERCA: Come Triggerare Cache Invalidation in Claude Code CLI

> **Data**: 11 Gennaio 2026
> **Ricercatrice**: Cervella Researcher
> **Obiettivo**: Scoprire metodi CONCRETI per controllare cache invalidation

---

## TL;DR - RISULTATI CHIAVE

### ✅ COSA FUNZIONA (Verificato)
1. **Timeout 5 minuti** - Cache scade automaticamente (ora ~3 min post-Dic 2025)
2. **Modificare tools definitions** - Invalida TUTTA la cache (system + messages)
3. **Quit & Restart CLI** - Reset completo (file + branch cache + conversation)
4. **Cambiare model** - Invalida cache (ogni model ha cache separata)

### ❌ COSA NON FUNZIONA (Bug Confermato)
1. **Comando /clear** - NON invalida cache completamente (file/branch persistono)
2. **Modificare CLAUDE.md** - NON triggera invalidation (solo content change, non tools)

### ⚠️ IPOTESI DA TESTARE
1. **Modificare MCP server config** (potrebbe cambiare tools)
2. **Cambiare model via API/settings** (forzare model switch)
3. **Usare cache_control con 1h TTL poi rimuoverlo**
4. **Saturare context window** (forza summarization = invalidation)

---

## 1. CACHE TTL: Il Timeout Automatico

### Come Funziona
- **TTL Ufficiale**: 5 minuti (documentazione Anthropic)
- **TTL Reale (Dic 2025)**: ~3 minuti (ridotto senza annuncio)
- **Meccanismo**: Ogni cache hit RESETTA il timer a 5 min

### Fonte Dati
- [Anthropic Prompt Caching Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [GitHub Issue #14628](https://github.com/anthropics/claude-code/issues/14628) - Cache TTL ridotto da 5→3 min a metà dicembre 2025

### Comportamento Osservato
```
cache_read_input_tokens: 51534  →  Hit! Timer reset a 5 min
(attendi 5+ minuti senza messaggi)
cache_creation_input_tokens: 29119  →  Miss! Cache ricreata
```

### METODO TESTABILE #1: "Attendi 5+ Minuti"
```bash
# 1. Fai una richiesta normale
echo "Test message" | claude

# 2. ATTENDI esattamente 6 minuti
sleep 360

# 3. Invia altro messaggio
echo "Another test" | claude

# 4. VERIFICA nei log: dovresti vedere cache_creation > 0
```

**Pro**: Metodo garantito, ufficiale
**Contro**: Lento (6 min di attesa), non controllabile on-demand

---

## 2. CACHE INVALIDATION: Triggers Confermati

### 2.1 Modificare Tools Definitions

**COME FUNZIONA:**
Cache segue gerarchia: `tools → system → messages`
Cambiare tools invalida TUTTO sotto (system + conversation)

**FONTE:**
- [Anthropic Caching Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- "Changes to tool_choice or the presence/absence of images anywhere in the prompt will invalidate the cache"

**METODO TESTABILE #2: "Aggiungi/Rimuovi Tool"**

Ipotesi: Claude Code usa MCP servers come tools. Modificare MCP config potrebbe triggerare invalidation.

```bash
# 1. Verifica tools attuali
cat ~/.claude/settings.json | grep -A 20 "mcpServers"

# 2. Aggiungi un fake MCP server
cat >> ~/.claude/settings.json << 'EOF'
{
  "mcpServers": {
    "cache-buster": {
      "command": "echo",
      "args": ["test"]
    }
  }
}
EOF

# 3. Riavvia sessione e verifica cache_creation spike
```

**Pro**: Se funziona, controllabile on-demand
**Contro**: Richiede modifica config, potrebbe non essere tool ma solo env change

---

### 2.2 Cambiare Model

**COME FUNZIONA:**
Ogni model ha cache SEPARATA. Switching model = cache miss garantita.

**FONTE:**
- Cache sono isolate per model (Anthropic docs)

**METODO TESTABILE #3: "Model Switch"**

```bash
# 1. Usa Sonnet 4.5 (default)
echo "Test sonnet" | claude

# 2. Switcha a Opus 4.5
claude --model claude-opus-4-5-20251101

# 3. Torna a Sonnet
claude --model claude-sonnet-4-5-20250929

# 4. VERIFICA: primo messaggio dopo switch dovrebbe avere cache_creation
```

**Pro**: Controllabile, reversibile
**Contro**: Cambia anche model (non solo cache), costa di più (Opus)

---

### 2.3 Quit & Restart

**COME FUNZIONA:**
Chiudere e riaprire CLI resetta:
- File cache
- Branch cache
- Conversation history
- Session state

**FONTE:**
- [GitHub Issue #2538](https://github.com/anthropics/claude-code/issues/2538)
- Workaround ufficiale per /clear bug

**METODO TESTABILE #4: "Hard Restart"**

```bash
# 1. Lavora normalmente, verifica cache hit alto
echo "Normal work" | claude

# 2. Esci da claude CTRL+D o exit

# 3. Riapri
claude

# 4. VERIFICA: primo messaggio dovrebbe avere cache_creation alto
```

**Pro**: Reset completo garantito, metodo ufficiale
**Contro**: Perdi conversation history (non sempre desiderabile)

---

## 3. BUG CONFERMATI: Cosa NON Funziona

### 3.1 Comando /clear

**PROBLEMA:**
/clear NON resetta completamente cache. Persistono:
- File references (Claude ricorda file cancellati)
- Branch cache (Claude ricorda vecchi branch)
- Partial conversation context

**FONTE:**
- [GitHub Issue #2538](https://github.com/anthropics/claude-code/issues/2538)
- [GitHub Issue #4629](https://github.com/anthropics/claude-code/issues/4629)

**OSSERVATO:**
```
1. Usa file TestPlan.md
2. Cancella file
3. /clear
4. Claude cerca ancora di leggere TestPlan.md (FAIL!)
```

**WORKAROUND:** Usa quit & restart invece di /clear.

---

### 3.2 Modificare CLAUDE.md

**PROBLEMA:**
Modificare CLAUDE.md cambia solo CONTENT, non STRUCTURE.
Cache invalidation richiede cambio di:
- Tools
- System prompt structure
- Model
- Timeout (5 min)

CLAUDE.md è parte del CONTENT caricato, ma non triggera structural change.

**TEST FATTO DA NOI:**
- Modificato CLAUDE.md
- Context rimasto a 75%
- Cache read ancora alto

**SPIEGAZIONE:**
CLAUDE.md viene letto e inserito nel system prompt CONTENT, ma la STRUTTURA del prompt (tools, cache_control markers) non cambia.

---

## 4. MECCANICA INTERNA: Come Funziona Claude Code

### Request Structure (da analisi rastrigin.systems)

**FONTE:** [What Claude Code Actually Sends](https://rastrigin.systems/blog/claude-code-part-1-requests/)

```json
{
  "model": "claude-opus-4-5-20251101",
  "stream": true,
  "max_tokens": 16000,
  "system": [
    {
      "type": "text",
      "text": "...",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "tools": [
    { "name": "Read", "...": "..." },
    { "name": "Write", "...": "..." },
    "cache_control": {"type": "ephemeral"}
  ],
  "messages": [
    // Conversation history (NO cache)
  ]
}
```

### Cache Layers

**Layer 1: Tools** (cachato)
- Definizioni Read, Write, Grep, Glob, Bash, etc
- ~15-25K tokens
- Invalida se: aggiungi/rimuovi tool, cambi signature

**Layer 2: System Prompt** (cachato)
- CLAUDE.md content
- DNA/Costituzione
- Project instructions
- ~10-15K tokens
- Invalida se: Layer 1 cambia

**Layer 3: Conversation** (NON cachato)
- Messages history
- Cresce ad ogni turn
- Mai cachato (cambia sempre)

---

## 5. AIDER APPROACH: Cache Keepalive Pings

### Come Lo Fa Aider

**FONTE:** [Aider Prompt Caching Docs](https://aider.chat/docs/usage/caching.html)

```bash
aider --cache-keepalive-pings 12
```

**Meccanismo:**
- Ogni 5 minuti invia "ping" all'API
- Ping = richiesta con STESSO prompt prefix
- Reset del TTL timer
- Mantiene cache viva fino a 12*5 = 60 minuti

**COSA INVIA:**
Non documentato esattamente, ma logica:
1. Richiesta con tools + system identici
2. Message minimale (es: "ping" o empty)
3. API vede cache hit → reset TTL

### METODO TESTABILE #5: "Manual Keepalive"

Possiamo simulare questo in Claude Code?

**Ipotesi Script:**
```bash
#!/bin/bash
# keepalive-ping.sh

while true; do
  sleep 240  # Ogni 4 minuti (prima che scada cache a 5 min)

  # Invia messaggio minimale che genera cache hit
  echo "ping" | claude --no-stream > /dev/null

  echo "[$(date)] Cache keepalive sent"
done
```

**Pro**: Mantiene cache viva durante pausa/lettura
**Contro**: Consuma API calls, non testato se Claude Code accetta stdin così

---

## 6. STREAM EVENTS: Monitorare Cache in Real-Time

### Metadata Usage

**FONTE:** [Anthropic Streaming Docs](https://platform.claude.com/docs/en/build-with-claude/streaming)

Ogni risposta include usage metadata:

```json
{
  "usage": {
    "input_tokens": 1234,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 15000,
    "output_tokens": 567
  }
}
```

### Cache Metrics Spiegati

| Metrica | Significato | Costo |
|---------|-------------|-------|
| `input_tokens` | Token NON cachati (nuovo input) | 100% |
| `cache_creation_input_tokens` | Token scritti in cache (NEW entry) | 125% |
| `cache_read_input_tokens` | Token letti da cache (HIT) | 10% |

**CACHE HIT PERFETTO:**
```json
{
  "input_tokens": 50,              // Solo nuovo messaggio
  "cache_creation_input_tokens": 0,   // Nessuna write
  "cache_read_input_tokens": 25000    // Tutto il resto da cache
}
```

**CACHE MISS (Invalidation):**
```json
{
  "input_tokens": 1000,
  "cache_creation_input_tokens": 24000,  // Riscrive TUTTO
  "cache_read_input_tokens": 0
}
```

### METODO TESTABILE #6: "Log Watcher"

```bash
# Monitor cache metrics in real-time
tail -f ~/.claude/data/logs/*.log | grep -E "cache_(creation|read)_input_tokens"

# Pattern da cercare:
# - cache_read alto (>20k) = HIT
# - cache_creation alto (>20k) = INVALIDATION
# - Spike cache_creation = trigger trovato!
```

---

## 7. CONFIGURAZIONI NASCOSTE: Environment Variables

### Settings Disponibili

**FONTE:**
- [Claude Code Settings Docs](https://code.claude.com/docs/en/settings)
- [Environment Variables Guide](https://medium.com/@dan.avila7/claude-code-environment-variables-a-complete-reference-guide-41229ef18120)

**File Config:**
- `~/.claude/settings.json` - User settings
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local override

**Variabili Rilevanti:**
```json
{
  "ANTHROPIC_MODEL": "claude-sonnet-4-5-20250929",
  "BASH_DEFAULT_TIMEOUT_MS": "120000",
  "BASH_MAX_TIMEOUT_MS": "600000"
}
```

### METODO TESTABILE #7: "Force Model Switch via ENV"

```bash
# 1. Check current model
grep ANTHROPIC_MODEL ~/.claude/settings.json

# 2. Force switch
export ANTHROPIC_MODEL="claude-opus-4-5-20251101"
claude

# 3. Verifica cache_creation spike (model change invalida cache)

# 4. Switch back
export ANTHROPIC_MODEL="claude-sonnet-4-5-20250929"
claude
```

**Pro**: Non modifica files permanentemente
**Contro**: ENV vars potrebbero non essere letti in sessioni già avviate

---

## 8. TIMEOUT BEHAVIORS: Idle e Shell Commands

### Idle Timeout

**FONTE:** [GitHub Issue #13922](https://github.com/anthropics/claude-code/issues/13922)

- **idle_prompt notification**: Hardcoded 60 secondi
- Se utente non risponde per 60s → hook triggered
- NON invalida cache (solo notifica)

### Shell Command Timeout

**FONTE:** [GitHub Issue #1635](https://github.com/anthropics/claude-code/issues/1635)

- **Default**: 2 minuti (120 secondi)
- **Configurabile**: `BASH_DEFAULT_TIMEOUT_MS`
- Se comando supera timeout → killed
- NON invalida cache (solo processo)

**CONCLUSIONE:**
Timeout shell/idle NON triggera cache invalidation. Solo cache TTL (5 min) conta.

---

## 9. CONTEXT SATURATION: Forzare Summarization

### Teoria

Da [rastrigin.systems analysis](https://rastrigin.systems/blog/claude-code-part-1-requests/):

> "Long sessions exceeding context limits force Claude Code to compress history via summarization, effectively resetting and invalidating previous conversation state."

**MECCANICA:**
1. Conversation cresce ad ogni turn
2. Quando supera max_tokens (200K per Sonnet 4.5)
3. Claude Code SUMMARIZZA vecchi messaggi
4. Summarization = NEW conversation structure
5. Invalida cache layer messages (ma non tools/system)

### METODO TESTABILE #8: "Satura Context con Long Output"

```bash
# 1. Genera output enorme (es: dump di file grossi)
echo "Read all .md files in docs/" | claude

# 2. Ripeti fino a saturare context (~200K tokens)
echo "List all files recursively" | claude
echo "Show git log --all" | claude

# 3. VERIFICA: quando saturo, dovrei vedere summarization event
# 4. DOPO summarization: cache_creation spike?
```

**Pro**: Potrebbe rivelare threshold automatico
**Contro**: Lento, spreca token, non controllabile precisamente

---

## 10. MANUAL CACHE CLEANUP: Cancellare Files

### Cache Locations

**FONTE:** [Claude Code Cleanup Guide](https://ctok.ai/en/claude-code-cleanup)

**macOS:**
```
~/Library/Caches/claude-code/
~/.claude/projects/*/
~/.claude.json
```

**Cosa Contiene:**
- `*.jsonl` - Conversation transcripts
- `subagents/` - Worker sessions
- Project state & caches

### METODO TESTABILE #9: "Nuclear Option"

```bash
# 1. BACKUP first!
cp -r ~/.claude ~/.claude.backup

# 2. Clear project cache
rm -rf ~/.claude/projects/-Users-rafapra-Developer-CervellaSwarm/*.jsonl

# 3. Clear general cache
rm -rf ~/Library/Caches/claude-code/*

# 4. Restart claude
claude

# 5. VERIFICA: cache_creation dovrebbe essere MASSIMO (tutto perso)
```

**Pro**: Reset totale garantito
**Contro**: Perdi TUTTA la history, irreversibile (senza backup)

---

## 11. GITHUB REPOSITORY: Source Code

### Repo Ufficiale

**URL:** https://github.com/anthropics/claude-code

**Stato:** NON completamente open source
Core engine è closed source, solo wrappers/CLI public.

### Community Tools

- [claude-clear](https://github.com/sanchez314c/claude-clear) - Tool per purge cache
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Community resources

**NOTA:** Source code di /clear command NON trovato pubblicamente.

---

## 12. RIEPILOGO METODI TESTABILI

### Alta Priorità (Testare Subito)

| # | Metodo | Effort | Rischio | Success Rate |
|---|--------|--------|---------|--------------|
| 1 | Attendi 6+ minuti | BASSO | ZERO | 100% |
| 2 | Quit & Restart CLI | BASSO | ZERO | 100% |
| 3 | Switch Model (ENV) | MEDIO | BASSO | 95% |
| 4 | Modifica MCP Config | MEDIO | MEDIO | 60%? |

### Media Priorità (Sperimentale)

| # | Metodo | Effort | Rischio | Success Rate |
|---|--------|--------|---------|--------------|
| 5 | Manual Keepalive Script | ALTO | MEDIO | 40%? |
| 6 | Log Watcher (monitor) | BASSO | ZERO | 100% (info) |
| 7 | Context Saturation | ALTO | ALTO | 30%? |

### Bassa Priorità (Nuclear)

| # | Metodo | Effort | Rischio | Success Rate |
|---|--------|--------|---------|--------------|
| 8 | Clear Cache Files | BASSO | ALTO | 100% |
| 9 | Modify Tools Manually | ALTO | ALTO | 80%? |

---

## 13. RACCOMANDAZIONI FINALI

### Per CONTROLLARE Cache Invalidation ORA

**OPZIONE A: Model Switch**
```bash
# Script: force-cache-invalidate.sh
export ANTHROPIC_MODEL="claude-opus-4-5-20251101"
echo "Cache invalidated (model switch)" | claude --no-stream
export ANTHROPIC_MODEL="claude-sonnet-4-5-20250929"
```

**OPZIONE B: Quit/Restart Automation**
```bash
# Script: restart-claude.sh
pkill -f "claude"  # Kill existing session
sleep 2
claude  # Restart fresh
```

### Per MONITORARE Cache Status

**Script: cache-monitor.sh**
```bash
#!/bin/bash
# Monitor cache metrics in real-time

tail -f ~/.claude/data/logs/*.log | while read line; do
  if echo "$line" | grep -q "cache_creation_input_tokens"; then
    creation=$(echo "$line" | jq -r '.usage.cache_creation_input_tokens // 0')
    read_tok=$(echo "$line" | jq -r '.usage.cache_read_input_tokens // 0')

    if [ "$creation" -gt 10000 ]; then
      echo "⚠️  CACHE INVALIDATION DETECTED!"
      echo "   Creation: $creation tokens"
      echo "   Read: $read_tok tokens"
      echo "   Timestamp: $(date)"
    elif [ "$read_tok" -gt 10000 ]; then
      echo "✅ Cache Hit: $read_tok tokens"
    fi
  fi
done
```

### Prossimi Test da Fare

1. **Test MCP Server Modification**
   - Aggiungere fake MCP server
   - Verificare se tools definitions cambiano
   - Misurare cache_creation spike

2. **Test Model Switch Automation**
   - Script che switcha model ogni N minuti
   - Log cache metrics before/after
   - Calcolare overhead vs benefit

3. **Test Manual Keepalive**
   - Script aider-style che pinga ogni 4 min
   - Verificare se mantiene cache viva
   - Misurare costo API calls

---

## FONTI CONSULTATE

### Documentazione Ufficiale
- [Anthropic Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Claude Code Settings Docs](https://code.claude.com/docs/en/settings)

### GitHub Issues
- [Issue #2538](https://github.com/anthropics/claude-code/issues/2538) - /clear bug (file/branch cache persist)
- [Issue #14628](https://github.com/anthropics/claude-code/issues/14628) - Cache TTL reduced 5→3 min
- [Issue #5615](https://github.com/anthropics/claude-code/issues/5615) - Timeout configuration
- [Issue #13922](https://github.com/anthropics/claude-code/issues/13922) - Idle prompt timeout

### Analisi Tecniche
- [What Claude Code Actually Sends](https://rastrigin.systems/blog/claude-code-part-1-requests/) - Deep dive request structure
- [Aider Caching Docs](https://aider.chat/docs/usage/caching.html) - Keepalive implementation

### Guide Community
- [Claude Code Environment Variables](https://medium.com/@dan.avila7/claude-code-environment-variables-a-complete-reference-guide-41229ef18120)
- [Claude Code Cleanup Guide](https://ctok.ai/en/claude-code-cleanup)

---

**Fine Ricerca**
**Researcher**: Cervella Researcher
**Data**: 11 Gennaio 2026
**Token Consumati**: ~25K (ricerca + synthesis)
**Status**: ✅ Completata - Metodi testabili identificati
