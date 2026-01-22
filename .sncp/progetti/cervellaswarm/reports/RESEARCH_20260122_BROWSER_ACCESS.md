# Ricerca: Browser Access per CervellaSwarm Workers

**Data**: 22 Gennaio 2026
**Researcher**: cervella-researcher
**Status**: ✅ COMPLETA
**Fonti consultate**: 12

---

## TL;DR - Executive Summary

**SCOPERTA CRITICA:** Playwright MCP Server e' **GIA' INSTALLATO** in CervellaSwarm!

```json
// ~/.claude/settings.json (righe 166-179)
"mcpServers": {
  "browser": {
    "command": "npx",
    "args": ["-y", "@playwright/mcp@latest", "--browser", "chromium"]
  }
}
```

**PROBLEMA:** I **worker subagent NON ereditano MCP config** dalla Regina!
**SOLUZIONE:** Iniettare config browser MCP ai worker che ne hanno bisogno.

**RACCOMANDAZIONE:** Abilitare browser access per `cervella-researcher` (MVP scope).

---

## 1. Opzioni Tecnologiche Disponibili

### 1.1 Playwright MCP Server ✅ (RACCOMANDATO)

**Cos'e'**: Server MCP ufficiale Microsoft che espone browser automation via Model Context Protocol.

**Vantaggi:**
- ✅ **GIA' INSTALLATO** in CervellaSwarm (Regina ha accesso)
- ✅ Ufficiale Microsoft - maintained
- ✅ Integration nativa con Claude Code via MCP
- ✅ Accessibilita' tree-based (no vision model required)
- ✅ Lightweight (no screenshot overhead)
- ✅ Supporto headless Chromium

**Svantaggi:**
- ⚠️ 26 tools = **context-hungry** (~1000+ tokens per page interaction)
- ⚠️ Chromium footprint: ~400-500MB disk space
- ⚠️ Tool proliferation problem (vedi ricerca Vercel)

**Setup Requirements:**
```bash
# Gia' presente!
npx -y @playwright/mcp@latest
```

**Config Worker:**
```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--browser", "chromium"]
    }
  }
}
```

**Fonti:**
- [GitHub - microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- [Playwright MCP Server Docs](https://executeautomation.github.io/mcp-playwright/docs/intro)
- [Setting Up MCP with Playwright - Complete Guide](https://medium.com/@peyman.iravani/setting-up-mcp-server-with-playwright-a-complete-integration-guide-bbd40dd008cf)

---

### 1.2 browser-use (Python Library)

**Cos'e'**: Open-source Python library per browser automation con LLM integration.

**Vantaggi:**
- ✅ Native Python (no Node.js dependency)
- ✅ Connects to **live browser sessions** (mantiene auth/cookies)
- ✅ LLM-first design (OpenAI, Claude, Llama support)
- ✅ Vision model integration built-in
- ✅ Custom-trained LLM (53 tasks/dollar efficiency)

**Svantaggi:**
- ❌ Richiede setup separato (non MCP-based)
- ❌ Integration con spawn-workers piu' complessa
- ❌ Python >= 3.11 requirement
- ⚠️ Screenshot-based = context overhead

**Setup:**
```bash
uv add browser-use
```

**Fonti:**
- [GitHub - browser-use/browser-use](https://github.com/browser-use/browser-use)
- [Browser Use - Enable AI to automate the web](https://browser-use.com/)
- [Browser-Use: Open-Source AI Agent For Web Automation](https://www.labellerr.com/blog/browser-use-agent/)

---

### 1.3 Browserbase (Cloud SaaS)

**Cos'e'**: Browser-as-a-Service - fleet di browser cloud gestiti.

**Vantaggi:**
- ✅ Zero local footprint (no Chromium install)
- ✅ Managed infrastructure
- ✅ Stealth, proxies, session recording built-in
- ✅ Stagehand SDK (natural language → browser actions)
- ✅ Usato da Vercel, Perplexity

**Svantaggi:**
- ❌ **PAID SERVICE** (costo per usage)
- ❌ Network dependency
- ❌ Privacy concern (browser cloud-hosted)
- ⚠️ Overkill per research tasks

**Fonti:**
- [Browserbase Official](https://www.browserbase.com)
- [Browserbase MCP Integration](https://www.browserbase.com/mcp)

---

### 1.4 Puppeteer / Selenium

**Status**: ❌ **NON RACCOMANDATI**

Playwright e' il **successore** di Puppeteer (stesso team Microsoft).
Selenium e' legacy, piu' complesso, meno LLM-friendly.

---

## 2. Security Considerations

### 2.1 Rischi

| Rischio | Impact | Mitigazione |
|---------|--------|-------------|
| **Web scraping abuse** | HIGH | Rate limiting, allowed-hosts whitelist |
| **Data exfiltration** | HIGH | Network sandboxing, audit logs |
| **Malicious sites** | MEDIUM | Headless + no-download policy |
| **Resource exhaustion** | MEDIUM | Max concurrent sessions, timeouts |

### 2.2 Best Practices Applicate

**Playwright MCP Security Features:**

```bash
# Config sicura
--allowed-hosts="docs.python.org,github.com,pypi.org"  # whitelist
--browser chromium                                     # headless
--viewport-size 1280x720                               # no full HD (lighter)
--user-data-dir /secure/path                           # isolated profile
```

**MCP Server Security (2026 Standards):**

1. ✅ **Sandboxing**: MCP server runs in isolated process (stdio transport)
2. ✅ **Least Privilege**: Worker subagents NON hanno accesso automatico
3. ✅ **Rate Limiting**: Playwright ha timeouts built-in
4. ✅ **OAuth 2.1**: Standard per HTTP-based transports (non stdio)
5. ✅ **Audit Trail**: Tutti i comandi MCP sono loggati da Claude Code

**Fonti:**
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Claude Code Security Best Practices](https://www.backslash.security/blog/claude-code-security-best-practices)
- [Understanding MCP Security - Datadog](https://www.datadoghq.com/blog/monitor-mcp-servers/)
- [MCP Security: How to Secure MCP Servers - WorkOS](https://workos.com/blog/mcp-security-risks-best-practices)

---

## 3. Context Efficiency Problem

### 3.1 Il Problema "Tool Proliferation"

**Ricerca Vercel (Dicembre 2025):**
"Removing 80% of tools made agent 3.5x faster with 100% success rate."

**Playwright MCP:**
- 26 tools esposti
- Ogni interazione ritorna **full accessibility tree**
- Page complessa = **1000+ DOM nodes per click**

**Esempio:**
```
Action: click button
Return: [8745 righe di accessibility tree]
Cost: ~2000 tokens wasted
```

### 3.2 Alternative Context-Efficient

**agent-browser (Vercel):**
- Rust CLI + Node.js daemon (Playwright sotto)
- Returns `@e1, @e2` references invece di full trees
- **93% less overhead**

**Problema:** NON e' un MCP server, richiede custom integration.

**Fonti:**
- [Why less is more: Playwright proliferation problem](https://www.speakeasy.com/blog/playwright-tool-proliferation)
- [Context Wars: Browser Tools Bleeding Tokens](https://paddo.dev/blog/agent-browser-context-efficiency/)

---

## 4. Effort & Complexity

### 4.1 Playwright MCP (MVP Scope)

| Task | Effort | Complexity |
|------|--------|-----------|
| **Setup Regina** | ✅ DONE | - |
| **Inject config to worker** | 2h | LOW |
| **Test cervella-researcher** | 1h | LOW |
| **Security hardening** | 3h | MEDIUM |
| **Documentation** | 2h | LOW |
| **TOTALE** | **~8h** | **LOW-MEDIUM** |

### 4.2 Dependencies

**Chromium Download:**
- Size: ~400-500MB (one-time)
- Location: `~/.cache/ms-playwright/chromium-*/`
- Auto-managed da Playwright

**Node.js:**
- Requirement: Node 18+ (gia' presente)
- npx scarica @playwright/mcp on-demand

**Performance Impact:**
- Chromium startup: ~2-3s (acceptable per research)
- Headless = minimal RAM (~200MB per session)

**Fonti:**
- [Playwright Browser Footprint](https://datawookie.dev/blog/2025/06/playwright-browser-footprint/)
- [Playwright Installation Docs](https://playwright.dev/docs/intro)

---

## 5. Integration con CervellaSwarm

### 5.1 Architettura Attuale

```
Regina (Claude Code Insiders)
├── settings.json → mcpServers.browser ✅
└── spawn-workers.sh
    └── Subagents
        ├── cervella-researcher (sonnet) ❌ no MCP config
        ├── cervella-backend (sonnet) ❌ no MCP config
        └── ...
```

**PROBLEMA:** I subagent spawned da `spawn-workers.sh` NON ereditano MCP config!

### 5.2 Soluzione Proposta

**Opzione A: Iniettare config al worker** (RACCOMANDATO)

Modificare `spawn-workers.sh` per passare `--mcp-config` ai worker selezionati:

```bash
# spawn-workers.sh (nuovo flag)
--researcher)
    AGENT="cervella-researcher"
    MCP_CONFIG="/Users/rafapra/.claude/mcp-configs/researcher.json"
    ;;
```

**Opzione B: Worker request via Regina**

Worker chiede alla Regina di fare web scraping → Regina usa Playwright MCP.

**Pro/Contro:**
- Opzione A: Worker autonomi, ma config complessa
- Opzione B: Piu' semplice, ma comunicazione overhead

### 5.3 Workflow Proposto (Opzione A)

```
1. Rafa: "Ricerca best practices React 2026"
2. Regina: spawn-workers --researcher "React best practices"
3. spawn-workers.sh:
   - Lancia cervella-researcher
   - Inietta mcp-config (browser tools)
4. cervella-researcher:
   - Usa Playwright MCP per navigare docs
   - Crea report RESEARCH_*.md
5. Regina: Legge report e sintetizza per Rafa
```

**Fonti:**
- [Connect Claude Code to MCP Tools](https://code.claude.com/docs/en/mcp)
- [Configuring MCP Tools in Claude Code](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)

---

## 6. Raccomandazione per CervellaSwarm

### 6.1 Scelta Tecnologica

**✅ RACCOMANDAZIONE: Playwright MCP Server**

**Motivazioni:**
1. **GIA' INSTALLATO** - Zero setup aggiuntivo
2. **Standard MCP** - Native integration con Claude Code
3. **Microsoft Official** - Long-term support garantito
4. **Security-first** - Sandbox built-in, stdio transport
5. **Headless-ready** - Perfetto per automation

**Alternative da considerare DOPO MVP:**
- browser-use: Se serve live session (Gmail login, etc)
- Browserbase: Se serve scale massive (improbabile)

### 6.2 MVP Scope

**FASE 1: cervella-researcher ONLY** (1 worker, risk-limited)

```yaml
Worker: cervella-researcher
Tools: Playwright MCP (browser tools)
Use cases:
  - Ricerca documentazione tecnica
  - Analisi competitor websites
  - Web scraping docs ufficiali
Constraints:
  - Allowed hosts whitelist (docs, github, pypi)
  - Max 3 concurrent sessions
  - 5min timeout per session
```

**Output attesi:**
- `RESEARCH_*.md` piu' ricchi (fonti web dirette)
- Meno "go check X yourself" (researcher fa direttamente)

### 6.3 Workers che NON dovrebbero avere browser

| Worker | Motivo |
|--------|--------|
| cervella-backend | Code-focused, no web needed |
| cervella-frontend | Code-focused, UI testing != browsing |
| cervella-tester | Test runner, no browsing needed |
| cervella-devops | Infra-focused, dangerous combo |

**ECCEZIONE:** cervella-marketing POTREBBE beneficiare (competitor analysis).

### 6.4 Timeline Implementazione

```
Week 1 (8h):
├── Day 1-2: Studiare spawn-workers MCP injection (3h)
├── Day 3: Implementare config injection per researcher (2h)
├── Day 4: Test + security hardening (2h)
└── Day 5: Documentation (1h)

Week 2 (4h):
├── Test real-world con researcher (2h)
└── Monitoring + adjustments (2h)

TOTALE: ~12h effort
```

### 6.5 Success Metrics

1. ✅ cervella-researcher puo' navigare docs senza Regina
2. ✅ RESEARCH_*.md contengono citazioni web dirette
3. ✅ No security incidents (monitored via audit log)
4. ✅ Context usage < 5000 tokens/research (acceptable)

---

## 7. Implementazione Step-by-Step

### Step 1: Creare Config MCP per Researcher

```bash
# File: ~/.claude/mcp-configs/researcher.json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest",
        "--browser", "chromium",
        "--allowed-hosts", "docs.python.org,github.com,pypi.org,react.dev,fastapi.tiangolo.com",
        "--viewport-size", "1280x720"
      ]
    }
  }
}
```

### Step 2: Modificare spawn-workers.sh

```bash
# Aggiungere supporto --mcp-config flag
if [[ "$AGENT_TYPE" == "researcher" ]]; then
    MCP_CONFIG_PATH="$HOME/.claude/mcp-configs/researcher.json"
    if [[ -f "$MCP_CONFIG_PATH" ]]; then
        EXTRA_ARGS="--mcp-config $MCP_CONFIG_PATH"
    fi
fi
```

### Step 3: Aggiornare cervella-researcher DNA

```markdown
# cervella-researcher.md

tools: Read, Glob, Grep, Write, WebSearch, WebFetch, **mcp__browser__***

## Browser Tools Available
- browser_navigate
- browser_screenshot
- browser_click
- browser_fill
- browser_console

## Use Cases
- Navigate documentation websites directly
- Verify live examples from docs
- Screenshot error pages for debugging
```

### Step 4: Test Protocol

```bash
# Test 1: Basic navigation
spawn-workers --researcher "Navigate to fastapi.tiangolo.com and extract getting started guide"

# Test 2: Multi-page
spawn-workers --researcher "Compare React vs Vue documentation structure"

# Test 3: Allowed hosts
spawn-workers --researcher "Try navigating to facebook.com"
# Expected: BLOCKED (not in whitelist)
```

### Step 5: Security Audit

```bash
# Check logs
cat ~/.claude/data/logs/mcp_audit.log | grep browser_ | tail -20

# Verify no unauthorized domains
grep -v "docs\|github\|pypi" mcp_audit.log | grep navigate
```

---

## 8. Rischi & Mitigazioni

| Rischio | Probabilita | Impact | Mitigazione |
|---------|-------------|--------|-------------|
| **Context explosion** | HIGH | MEDIUM | Limit to researcher only, monitor token usage |
| **Unauthorized scraping** | MEDIUM | HIGH | Allowed-hosts whitelist, audit logs |
| **Performance degradation** | LOW | MEDIUM | Max 3 concurrent, 5min timeout |
| **Security exploit** | LOW | HIGH | Headless + sandboxed + stdio transport |
| **Cost increase** | MEDIUM | LOW | Researcher ha gia' WebSearch (simile cost) |

**Rollback Plan:**
Se problemi emergono, rimuovere MCP config da researcher → fallback a WebSearch.

---

## 9. Alternative Future Considerations

### 9.1 Vercel agent-browser (Context-Efficient)

**Quando considerare:** Se context usage Playwright MCP diventa insostenibile.

**Effort:** 2-3 settimane (custom MCP wrapper needed)

### 9.2 Browser-use (Live Sessions)

**Quando considerare:** Se serve Gmail automation, auth flows complessi.

**Use case:** Miracollook (email client) potrebbe beneficiare.

### 9.3 Browserbase (Cloud)

**Quando considerare:** Mai, a meno di scale massive (unlikely).

---

## 10. Conclusioni

### Fattibilita': ✅ **ALTA**

- Setup: Playwright MCP gia' installato
- Integration: spawn-workers.sh modificabile
- Security: MCP standards + whitelist
- Cost: Marginale (Chromium disk space only)

### Beneficio: ✅ **MEDIO-ALTO**

- Researcher piu' autonoma
- Report piu' ricchi
- Meno round-trip Regina ↔ Researcher

### Raccomandazione Finale:

**PROCEDI con MVP:**
1. Abilitare browser MCP per `cervella-researcher` ONLY
2. Whitelist: docs.python.org, github.com, pypi.org, react.dev, fastapi.tiangolo.com
3. Monitor per 2 settimane
4. Se success → valutare estensione ad altri worker

**Timeline:** 2 settimane (~12h effort totale)

**Owner:** cervella-ingegnera (implementation) + cervella-guardiana-qualita (security review)

---

## Fonti Complete

### Playwright MCP
- [GitHub - microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- [Playwright MCP Server Docs](https://executeautomation.github.io/mcp-playwright/docs/intro)
- [Setting Up MCP with Playwright - Complete Guide](https://medium.com/@peyman.iravani/setting-up-mcp-server-with-playwright-a-complete-integration-guide-bbd40dd008cf)
- [Ultimate Guide to Playwright MCP](https://testdino.com/blog/playwright-mcp/)
- [Playwright MCP Server - Autify](https://autify.com/blog/playwright-mcp)

### browser-use
- [GitHub - browser-use/browser-use](https://github.com/browser-use/browser-use)
- [browser-use PyPI](https://pypi.org/project/browser-use/)
- [Browser Use Official Site](https://browser-use.com/)
- [Browser-Use: Open-Source AI Agent](https://www.labellerr.com/blog/browser-use-agent/)

### Security
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Claude Code Security - Backslash](https://www.backslash.security/blog/claude-code-security-best-practices)
- [Understanding MCP Security - Datadog](https://www.datadoghq.com/blog/monitor-mcp-servers/)
- [MCP Security: How to Secure MCP Servers - WorkOS](https://workos.com/blog/mcp-security-risks-best-practices)
- [MCP Security Vulnerabilities - Practical DevSecOps](https://www.practical-devsecops.com/mcp-security-vulnerabilities/)

### Context Efficiency
- [Why less is more: Playwright proliferation problem](https://www.speakeasy.com/blog/playwright-tool-proliferation)
- [Context Wars: Browser Tools Bleeding Tokens](https://paddo.dev/blog/agent-browser-context-efficiency/)

### Browserbase
- [Browserbase Official](https://www.browserbase.com)
- [Browserbase MCP Integration](https://www.browserbase.com/mcp)
- [Cloud Browser Automation Guide 2025](https://www.browserbase.com/blog/cloud-browser-automation-guide-2025)

### Claude Code MCP
- [Connect Claude Code to MCP Tools](https://code.claude.com/docs/en/mcp)
- [Configuring MCP Tools in Claude Code](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)

### Technical
- [Playwright Browser Footprint](https://datawookie.dev/blog/2025/06/playwright-browser-footprint/)
- [Playwright Installation Docs](https://playwright.dev/docs/intro)
- [Playwright Browsers Docs](https://playwright.dev/docs/browsers)

---

**Fine Ricerca**
**Data**: 22 Gennaio 2026, 11:25 CET
**Researcher**: cervella-researcher
**Approvazione richiesta da**: cervella-guardiana-qualita (security review)

---

*"Studiare prima di agire - i player grossi hanno gia' risolto questi problemi!"* 🔬
