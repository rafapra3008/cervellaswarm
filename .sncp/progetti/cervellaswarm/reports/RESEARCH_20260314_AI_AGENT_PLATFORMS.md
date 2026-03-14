# AI Agent Platforms - Dove Deve Essere Lingua Universale

> Ricerca: 14 Marzo 2026 | Cervella Scienziata
> Contesto: LU ha agente su Moltbook (karma 22, < 24h). Dove altro dobbiamo essere?

---

## MAPPA PIATTAFORME (priorita decrescente)

---

### CATEGORIA 1: SOCIAL NETWORK PER AI AGENT (Moltbook-equivalenti)

#### 1. Moltbook -- GIA PRESENTI (karma 22)
- **URL:** https://www.moltbook.com/u/lingua-universale
- **Dimensione:** 1.6M agenti, acquisito Meta 10/03/2026
- **Rilevanza:** ALTA -- unica piattaforma mainstream per agent identity
- **Status:** LIVE. Bot 24/7 su Fly.io. Karma 22 in < 24h.
- **Rischio:** Meta acquisita. API incerta a lungo termine.
- **Azione:** Mantenere presenza. NON dipendere come canale primario.

#### 2. Chirper.ai
- **URL:** https://chirper.ai
- **Dimensione:** 65.000 agenti, 7.7M post generati da AI
- **Rilevanza:** MEDIA -- piu vecchio di Moltbook, meno tech/developer-focused
- **Differenza da Moltbook:** Si trasforma in "AI world simulato" (non puro social). Persona-driven, non skill-driven.
- **Effort:** Medio. Richiede creare persona AI con character sheet.
- **Priorita:** 3 (dopo Moltbook consolidato e ClawHub)
- **Azione:** CONSIDERARE in Aprile se Moltbook satura. Non urgente adesso.

#### 3. OpenClaw Social (openclawsocial.org)
- **URL:** https://openclawsocial.org + https://openclawsocial.forum
- **Dimensione:** Non verificata. Community attorno a OpenClaw (100K+ GitHub stars).
- **Rilevanza:** ALTA -- e la community degli agent developer piu tecnici. OpenClaw e il runtime che alimenta Moltbook.
- **Chi c'e:** Developer che costruiscono agenti con OpenClaw. Esattamente il nostro pubblico.
- **Effort:** Basso. Forum standard, commenti su thread tecnici.
- **Priorita:** 2 -- ALTA. Dobbiamo essere qui.
- **Azione:** Creare account, commentare su thread protocollo/sicurezza. Angolo: "LU come verification layer per OpenClaw agents."

---

### CATEGORIA 2: MARKETPLACE SKILL/TOOL (dove pubblichiamo la skill OpenClaw)

#### 4. ClawHub (openclaw registry)
- **URL:** https://clawhub.openclaw.dev (via ClawHub)
- **Dimensione:** 13.729 skill (dato Febbraio 2026)
- **Rilevanza:** ALTA -- e la piattaforma nativa dove va la nostra `openclaw-skill-lu/`
- **Effort:** Basso. `clawhub publish` (gia in roadmap S461)
- **Sicurezza:** Ogni skill riceve SHA-256 hash verificato via VirusTotal. Positivo per noi.
- **Priorita:** 1 -- DOBBIAMO ESSERE QUI PRIMA DI SHOW HN
- **Azione:** `clawhub publish` entro Settimana 1 (14-21 Marzo). E un prerequisito per social proof HN.

#### 5. SkillsMP
- **URL:** https://skillsmp.com
- **Dimensione:** 351.000+ skill (volume leader). Aggrega da GitHub.
- **Rilevanza:** ALTA per volume. Crawla repo GitHub con SKILL.md.
- **Come funziona:** Automatico -- se pubblichiamo la skill su GitHub con SKILL.md standard, SkillsMP la indicizza senza azione.
- **Effort:** ZERO aggiuntivo. Se la skill e su GitHub con SKILL.md, appare qui automaticamente.
- **Priorita:** 1 -- GRATIS, automatico, alta visibilita
- **Azione:** Verificare che `openclaw-skill-lu/` abbia SKILL.md corretto. Controllare se gia indicizzata dopo GitHub publish.

#### 6. Skills.sh (Vercel)
- **URL:** https://skills.sh
- **Dimensione:** Non verificata. Supporta 18 AI agent (Claude Code, Cursor, Codex, Copilot, Windsurf...)
- **Rilevanza:** ALTA per developer. Vercel = credibilita tech. Traccia install count reali.
- **Differenza da SkillsMP:** Non solo OpenClaw. Supporta Claude Code Skills, Codex Skills.
- **Effort:** Basso. Standard aperto SKILL.md.
- **Priorita:** 2 -- ALTA ma dopo ClawHub. Diversifica oltre OpenClaw ecosystem.
- **Azione:** Pubblicare la nostra skill anche qui. Compatibile con Claude Code Skills format.

#### 7. Hugging Face Spaces (MCP)
- **URL:** https://huggingface.co/spaces?filter=mcp-server
- **Dimensione:** Hub con milioni di developer. Spaces filtrabile per MCP server.
- **Rilevanza:** MEDIA-ALTA -- community ML/AI piu ampia. Non agent-social, ma developer che costruiscono agenti.
- **Come funziona:** Creare uno Space che espone LU come MCP server. `lu verify` via Gradio app.
- **Effort:** Medio. Richiede wrapper Gradio o API endpoint.
- **Priorita:** 3 -- Dopo Show HN. Ottimo per credibilita accademica/ML community.
- **Azione:** Creare HF Space "Lingua Universale Verifier" come Gradio app + MCP server. Backlog Aprile.

---

### CATEGORIA 3: DIRECTORY MCP SERVER (dove gli agenti cercano tool)

#### 8. PulseMCP
- **URL:** https://www.pulsemcp.com/servers
- **Dimensione:** 10.400+ server MCP, aggiornato daily
- **Rilevanza:** ALTA -- chi cerca tool MCP lo cerca qui. Directory piu completa.
- **Effort:** Basso. Submission form o auto-discovery da GitHub.
- **Priorita:** 2 -- ALTA. Dobbiamo apparire come "LU MCP server" per agent verification.
- **Azione:** Creare MCP server LU (wrappa `lu verify` + `lu lint`). Pubblicare su PulseMCP. Requisito: il server deve esistere.

#### 9. Glama.ai
- **URL:** https://glama.ai/mcp/servers
- **Dimensione:** Non verificata. Piu tecnica di PulseMCP, "most comprehensive registry".
- **Rilevanza:** MEDIA-ALTA -- developer piu tecnici.
- **Effort:** Basso. Segue standard MCP con `server.json`.
- **Priorita:** 3 -- Pubblicare insieme a PulseMCP una volta che il server esiste.
- **Azione:** Submit contestualmente a PulseMCP. Zero effort aggiuntivo.

#### 10. Official MCP Registry (modelcontextprotocol.io)
- **URL:** https://registry.modelcontextprotocol.io
- **Dimensione:** Registro ufficiale Anthropic/Linux Foundation.
- **Rilevanza:** MASSIMA per credibilita. E il registro "ufficiale".
- **Effort:** Medio-alto. Requisiti piu stringenti (server.json, validazione).
- **Priorita:** 2 -- ALTA per credibilita. Anthropic endorsement implicito.
- **Azione:** Pubblicare qui DOPO PulseMCP (test deployment prima). Requisito: MCP server stabile.

---

### CATEGORIA 4: COMMUNITY DEVELOPER (dove conversiamo, non pubblichiamo)

#### 11. DEV Community (dev.to)
- **URL:** https://dev.to
- **Dimensione:** Milioni di developer. Articoli indicizzati da Google.
- **Rilevanza:** ALTA per SEO e reach developer.
- **Chi c'e:** Articoli su MCP vs A2A, agent protocols -- esattamente il nostro spazio.
- **Effort:** Medio. Articolo tecnico 800-1500 parole.
- **Priorita:** 2 -- Post "Formal verification for AI agent protocols: introducing LU" ha potenziale virale.
- **Azione:** Un articolo post-Show HN. Riusa contenuto esistente.

#### 12. Hacker News (Show HN)
- **URL:** https://news.ycombinator.com
- **Dimensione:** 5M+ lettori settimanali. Gate per credibilita tech.
- **Rilevanza:** MASSIMA. E il nostro lancio principale.
- **Priorita:** 1 -- Finestra 21-28 Marzo. NON una piattaforma "da presidiare" ma da usare una volta bene.
- **Azione:** Show HN v2. Draft: `docs/SHOW_HN_V2_DRAFT.md`. Prerequisito: ClawHub + karma Moltbook.

#### 13. Agentic AI Foundation (Linux Foundation)
- **URL:** https://agenticaifoundation.org (parte di Linux Foundation)
- **Dimensione:** Founding members: Anthropic, OpenAI, AWS, Google, Microsoft. Standard MCP e A2A donati qui.
- **Rilevanza:** ALTA per legittimita. Se LU diventa standard de-facto per verification, deve essere qui.
- **Effort:** Alto. Richiede adoption first, poi membership/contribution.
- **Priorita:** 4 -- Obiettivo 6-12 mesi. Adesso siamo troppo piccoli.
- **Azione:** Seguire le specifiche AAIF. Contribuire commenti pubblici quando pubblicano RFC.

#### 14. NIST AI Agent Standards Initiative
- **URL:** https://www.nist.gov/caisi/ai-agent-standards-initiative
- **Dimensione:** Governo USA. Definisce standard per enterprise adoption.
- **Rilevanza:** MEDIA adesso, ALTA tra 12 mesi. Enterprise vuole compliance NIST.
- **Priorita:** 5 -- Backlog. Richiede risultati dimostrabili prima.
- **Azione:** Monitorare RFC pubblici. Rispondere con commenti tecnici quando pertinente.

---

## MATRICE PRIORITA -- COSA FARE E QUANDO

| Priorita | Piattaforma | Azione | Quando | Effort |
|----------|-------------|--------|--------|--------|
| **P1** | ClawHub | `clawhub publish` | 14-18 Marzo | 2h |
| **P1** | SkillsMP | Verificare SKILL.md in repo | 14-18 Marzo | 30 min |
| **P1** | Hacker News | Show HN v2 | 21-28 Marzo | 4h prep |
| **P2** | OpenClaw Social | Creare account + 5 commenti tecnici | 18-21 Marzo | 3h |
| **P2** | Official MCP Registry | Submit LU MCP server | Dopo Show HN | 4h |
| **P2** | PulseMCP | Submit LU MCP server | Dopo Show HN | 1h |
| **P2** | Skills.sh | Publish skill | Dopo ClawHub | 2h |
| **P2** | DEV Community | Articolo post-Show HN | Aprile | 4h |
| **P3** | Chirper.ai | Creare agente LU | Aprile | 4h |
| **P3** | Hugging Face Spaces | MCP server Gradio | Aprile-Maggio | 8h |
| **P3** | Glama.ai | Submit (contestuale PulseMCP) | Dopo Show HN | 30 min |
| **P4** | AAIF/Linux Foundation | Contributi RFC | 6-12 mesi | - |
| **P5** | NIST | Commenti pubblici | 12+ mesi | - |

---

## GAP CRITICO IDENTIFICATO: MANCA IL MCP SERVER LU

Per presidiare PulseMCP, Glama, Official MCP Registry -- serve un MCP server LU che esponga:
- `lu_verify(protocol)` -- verifica formale protocollo
- `lu_lint(code)` -- lint codice LU
- `lu_format(code)` -- formato
- `lu_init(template)` -- inizializza progetto

La nostra `openclaw-skill-lu/` e gia 4 tool. Ma un MCP server nativo (non OpenClaw-specific) espanderebbe il reach a TUTTI i client MCP (Claude Desktop, Cursor, Codex, VS Code con Copilot).

**Stima effort:** 4-6h. Architettura: FastAPI + MCP SDK. Base: codice skill OpenClaw gia esistente.
**ROI:** Una volta pubblicato, appare automaticamente su 3 directory (PulseMCP + Glama + Official Registry).

---

## RISCHIO CONCENTRAZIONE

Attualmente siamo presenti solo su Moltbook. Se Meta chiude API o restringe accesso:
- Perdiamo presenza su unica piattaforma social agenti
- La skill OpenClaw rimane ma perde discovery

**Mitigazione (in ordine di impatto):**
1. ClawHub (immediato) -- indipendente da Meta
2. OpenClaw Social (immediato) -- community OpenClaw sopravvive a Meta
3. Discord LU proprio (CEO deve creare) -- owned audience
4. MCP server multi-piattaforma (3-4 settimane) -- bypass dipendenza OpenClaw/Moltbook

---

## RACCOMANDAZIONE ESECUTIVA

**Questa settimana (14-18 Marzo):**
Fare P1: ClawHub publish + SKILL.md check. Due mosse, 3 ore totali, danno visibilita immediata prima di Show HN.

**Prossima settimana (18-21 Marzo):**
OpenClaw Social account + commenti. Warm up community prima del lancio HN.

**Show HN (21-28 Marzo):**
Con ClawHub + Moltbook come proof points. "You can already install the skill on ClawHub."

**Aprile:**
MCP server nativo -> PulseMCP + Glama + Official Registry. Questo e il moltiplicatore vero.

---

*"I dati guidano le decisioni. Conosci il mercato prima di entrarci."*
*Fonti: TechCrunch, Axios, CNBC, SkillsMP, PulseMCP, dev.to, NIST, Linux Foundation AAIF*

COSTITUZIONE-APPLIED: SI | Principio: "Ricerca PRIMA di implementare"
