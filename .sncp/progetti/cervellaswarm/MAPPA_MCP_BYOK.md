# MAPPA STRATEGICA - CervellaSwarm MCP + BYOK

> **Data:** 16 Gennaio 2026 - Sessione 230
> **Decisione:** MCP Server + BYOK - La Via GIUSTA
> **Standard:** Score minimo 9.5/10
> **Filosofia:** "Fatto BENE > Fatto VELOCE"

---

## DECISIONE PRESA

```
+================================================================+
|                                                                |
|   CervellaSwarm sara:                                          |
|                                                                |
|   1. MCP SERVER - Integrabile con Claude Code                  |
|   2. CLI STANDALONE - Con opzione BYOK                         |
|   3. DUAL MODE - Entrambi funzionano                           |
|                                                                |
|   CHI PAGA API: SEMPRE L'UTENTE (BYOK!)                        |
|   NOI MONETIZZIAMO: Features CervellaSwarm                     |
|   MARGINI: 90%+ (zero costi variabili AI!)                     |
|                                                                |
+================================================================+
```

---

## SEZIONE 1: MCP PROTOCOL

| Punto | Studiato? | Documento | Score | GAP |
|-------|-----------|-----------|-------|-----|
| Specification v2025-11-25 | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 10/10 | - |
| JSON-RPC 2.0 protocol | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 10/10 | - |
| Lifecycle management | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 10/10 | - |
| Capabilities negotiation | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 9/10 | - |
| Tools definition | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 10/10 | - |
| Resources handling | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 9/10 | - |
| Prompts templates | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 8/10 | Esempi pratici |
| FastMCP SDK (Python) | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 9/10 | - |
| TypeScript SDK | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 8/10 | Da validare |
| OAuth per MCP | DA FARE | - | 0/10 | CRITICO |
| Session management MCP | DA FARE | - | 0/10 | IMPORTANTE |
| Rate limiting MCP | DA FARE | - | 0/10 | IMPORTANTE |

**Score Sezione: 8.3/10**

---

## SEZIONE 2: ARCHITETTURA TECNICA

| Punto | Studiato? | Documento | Score | GAP |
|-------|-----------|-----------|-------|-----|
| Architettura attuale CLI | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 10/10 | - |
| Trasformazione MCP | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 7/10 | POC necessario |
| Dual mode design | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 8/10 | - |
| MCP Tools da esporre | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 9/10 | - |
| MCP Resources da esporre | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 8/10 | - |
| Gestione API key dual mode | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 7/10 | Implementare |
| Security model | OK | ARCHITETTURA_MCP_CERVELLASWARM.md | 9/10 | Audit |
| Package `conf` integration | DA FARE | - | 0/10 | CRITICO |
| API key validation | DA FARE | - | 0/10 | CRITICO |
| Error handling MCP | PARZIALE | ARCHITETTURA_MCP_CERVELLASWARM.md | 6/10 | Approfondire |

**Score Sezione: 7.4/10**

---

## SEZIONE 3: BUSINESS MODEL

| Punto | Studiato? | Documento | Score | GAP |
|-------|-----------|-----------|-------|-----|
| Pricing tiers | OK | BUSINESS_MODEL_MCP_BYOK.md | 9/10 | - |
| Competitor benchmark | OK | STUDIO_STRATEGICO_AUTH_COMPETITOR.md | 9/10 | - |
| BYOK economics | OK | BUSINESS_MODEL_MCP_BYOK.md | 10/10 | - |
| Free tier limits | OK | BUSINESS_MODEL_MCP_BYOK.md | 8/10 | Validare |
| Team features | OK | BUSINESS_MODEL_MCP_BYOK.md | 8/10 | Design UI |
| Enterprise features | OK | BUSINESS_MODEL_MCP_BYOK.md | 7/10 | Dettagliare |
| Revenue projections | OK | BUSINESS_MODEL_MCP_BYOK.md | 8/10 | - |
| Launch strategy | OK | BUSINESS_MODEL_MCP_BYOK.md | 8/10 | - |
| Anthropic contact | DA FARE | - | 0/10 | Decidere quando |

**Score Sezione: 7.4/10**

---

## SEZIONE 4: ONBOARDING UTENTE

| Punto | Studiato? | Documento | Score | GAP |
|-------|-----------|-----------|-------|-----|
| First-run experience MCP | DA FARE | - | 0/10 | CRITICO |
| First-run experience CLI | PARZIALE | ANALISI_AUTH_ATTUALE.md | 5/10 | Migliorare |
| API key wizard | DA FARE | - | 0/10 | CRITICO |
| API key validation | DA FARE | - | 0/10 | CRITICO |
| `cervellaswarm doctor` | DA FARE | - | 0/10 | IMPORTANTE |
| Tutorial interattivo | DA FARE | - | 0/10 | NICE-TO-HAVE |
| Documentazione utente | DA FARE | - | 0/10 | CRITICO |
| Error messages user-friendly | DA FARE | - | 0/10 | IMPORTANTE |

**Score Sezione: 0.6/10** - AREA CRITICA!

---

## SEZIONE 5: CLAUDE CODE INTEGRATION

| Punto | Studiato? | Documento | Score | GAP |
|-------|-----------|-----------|-------|-----|
| Come Claude Code trova MCP | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 9/10 | - |
| Config ~/.claude/mcp.json | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 9/10 | - |
| Transports (stdio/HTTP) | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 8/10 | - |
| Permessi e approvazioni | PARZIALE | STUDIO_MCP_PROTOCOL_COMPLETO.md | 6/10 | Approfondire |
| Testing con Claude Code | DA FARE | - | 0/10 | CRITICO |
| Distribution npm | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 8/10 | - |

**Score Sezione: 6.7/10**

---

## SEZIONE 6: COMPETITOR ANALYSIS

| Punto | Studiato? | Documento | Score | GAP |
|-------|-----------|-----------|-------|-----|
| Cursor model | OK | RICERCA_TECNICA_CURSOR_AUTH.md | 9/10 | - |
| GitHub Copilot model | OK | STUDIO_STRATEGICO_AUTH_COMPETITOR.md | 9/10 | - |
| Windsurf model | OK | STUDIO_STRATEGICO_AUTH_COMPETITOR.md | 8/10 | - |
| Continue.dev model | OK | STUDIO_STRATEGICO_AUTH_COMPETITOR.md | 8/10 | - |
| JetBrains BYOK | OK | STUDIO_STRATEGICO_AUTH_COMPETITOR.md | 8/10 | - |
| Altri MCP servers | OK | STUDIO_MCP_PROTOCOL_COMPLETO.md | 7/10 | - |

**Score Sezione: 8.2/10**

---

## SCORE GLOBALE

```
+================================================================+
|   AREA                          | SCORE  | STATUS              |
+================================================================+
|   MCP Protocol                  | 8.3/10 | OK - gap minori     |
|   Architettura Tecnica          | 7.4/10 | DA COMPLETARE       |
|   Business Model                | 7.4/10 | OK - gap minori     |
|   Onboarding Utente             | 0.6/10 | CRITICO!            |
|   Claude Code Integration       | 6.7/10 | DA COMPLETARE       |
|   Competitor Analysis           | 8.2/10 | OK                  |
+================================================================+
|   MEDIA GLOBALE                 | 6.4/10 | SOTTO TARGET 9.5    |
+================================================================+
```

---

## GAP CRITICI DA COLMARE

### PRIORITA 1 - Blockers (da fare PRIMA di tutto)

| GAP | Descrizione | Azione | Owner |
|-----|-------------|--------|-------|
| API Key Wizard | Manca wizard per chiedere API key | Implementare in init.js | cervella-backend |
| API Key Validation | Manca validazione che key funziona | Implementare test call | cervella-backend |
| Package `conf` | Installato ma MAI usato | Implementare config manager | cervella-backend |
| Documentazione utente | Zero docs per utenti esterni | Creare README dettagliato | cervella-docs |

### PRIORITA 2 - Architettura MCP

| GAP | Descrizione | Azione | Owner |
|-----|-------------|--------|-------|
| POC MCP Server | Validare architettura con prototype | Spike 1 settimana | cervella-backend |
| OAuth MCP | Come gestire auth in MCP mode | Ricerca approfondita | cervella-researcher |
| Testing MCP | Come testare integration | Definire test strategy | cervella-tester |

### PRIORITA 3 - UX/Onboarding

| GAP | Descrizione | Azione | Owner |
|-----|-------------|--------|-------|
| First-run MCP | Esperienza primo uso con Claude Code | Design flow | cervella-marketing |
| First-run CLI | Esperienza primo uso standalone | Design flow | cervella-marketing |
| Error messages | Messaggi user-friendly | Audit e rewrite | cervella-docs |
| `doctor` command | Health check per debug | Implementare | cervella-backend |

---

## ROADMAP IMPLEMENTAZIONE

```
+================================================================+
|   FASE 0: FONDAMENTA (Settimana 1-2)                           |
+================================================================+
|                                                                |
|   [ ] Config manager con `conf`                                |
|   [ ] API key wizard in init                                   |
|   [ ] API key validation                                       |
|   [ ] `cervellaswarm doctor`                                   |
|   [ ] README utente dettagliato                                |
|                                                                |
|   GATE: Score Onboarding >= 8/10                               |
+================================================================+

+================================================================+
|   FASE 1: POC MCP SERVER (Settimana 3-4)                       |
+================================================================+
|                                                                |
|   [ ] Setup packages/mcp-server                                |
|   [ ] MCP server minimal (1 tool)                              |
|   [ ] Test con Claude Code locale                              |
|   [ ] Validare architettura dual-mode                          |
|                                                                |
|   GATE: POC funziona end-to-end                                |
+================================================================+

+================================================================+
|   FASE 2: MCP COMPLETO (Settimana 5-8)                         |
+================================================================+
|                                                                |
|   [ ] Tutti i tools MCP                                        |
|   [ ] Resources SNCP                                           |
|   [ ] Prompts templates                                        |
|   [ ] Error handling robusto                                   |
|   [ ] Security audit                                           |
|                                                                |
|   GATE: Score Architettura >= 9/10                             |
+================================================================+

+================================================================+
|   FASE 3: POLISH & DOCS (Settimana 9-10)                       |
+================================================================+
|                                                                |
|   [ ] Documentazione completa                                  |
|   [ ] Tutorial video/scritto                                   |
|   [ ] Examples repository                                      |
|   [ ] Error messages finali                                    |
|   [ ] Beta testing interno                                     |
|                                                                |
|   GATE: Score Globale >= 9.5/10                                |
+================================================================+

+================================================================+
|   FASE 4: LAUNCH (Quando pronto)                               |
+================================================================+
|                                                                |
|   [ ] npm publish                                              |
|   [ ] Product Hunt?                                            |
|   [ ] Community announcement                                   |
|   [ ] Contatto Anthropic?                                      |
|                                                                |
|   GATE: Tutto REALE, non su carta                              |
+================================================================+
```

---

## DOCUMENTI DI RIFERIMENTO

| Documento | Path | Contenuto |
|-----------|------|-----------|
| Studio MCP Protocol | `.sncp/progetti/cervellaswarm/idee/STUDIO_MCP_PROTOCOL_COMPLETO.md` | Protocollo MCP in dettaglio |
| Architettura MCP | `.sncp/progetti/cervellaswarm/idee/ARCHITETTURA_MCP_CERVELLASWARM.md` | Design architetturale |
| Business Model | `.sncp/progetti/cervellaswarm/idee/BUSINESS_MODEL_MCP_BYOK.md` | Pricing e strategia |
| Competitor Cursor | `.sncp/progetti/cervellaswarm/idee/RICERCA_TECNICA_CURSOR_AUTH.md` | Come fa Cursor |
| Competitor All | `.sncp/progetti/cervellaswarm/idee/STUDIO_STRATEGICO_AUTH_COMPETITOR.md` | Tutti i competitor |
| Auth Claude Code | `.sncp/progetti/cervellaswarm/idee/RICERCA_AUTH_CLAUDE_CODE.md` | Auth Claude Code ufficiale |
| Integrazione Claude | `.sncp/progetti/cervellaswarm/idee/RICERCA_INTEGRAZIONE_CLAUDE_CODE.md` | Perche MCP e via giusta |
| Auth Attuale | `.sncp/progetti/cervellaswarm/idee/ANALISI_AUTH_ATTUALE.md` | Gap codice attuale |

---

## NEXT STEP IMMEDIATO

```
+================================================================+
|                                                                |
|   1. RAFA APPROVA questa mappa? OK / Modifiche?                |
|                                                                |
|   2. Se OK, partiamo con FASE 0:                               |
|      - cervella-backend: Config manager + API wizard           |
|      - cervella-docs: README utente                            |
|      - cervella-tester: Test suite per nuovo code              |
|                                                                |
|   3. Un progresso al giorno, senza fretta                      |
|                                                                |
+================================================================+
```

---

*"Fatto BENE > Fatto VELOCE"*
*"IL TEMPO NON CI INTERESSA"*
*"Score minimo 9.5/10"*

---

**Cervella Regina + Guardiane**
*16 Gennaio 2026 - Sessione 230*
