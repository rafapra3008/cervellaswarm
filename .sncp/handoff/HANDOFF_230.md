# HANDOFF - Sessione 230

> **Data:** 16 Gennaio 2026
> **Progetto:** CervellaSwarm
> **Prossima Cervella:** Leggi questo PRIMA di iniziare!

---

## DECISIONE STRATEGICA PRESA!

```
+================================================================+
|   SESSIONE 230: CAMBIO DIREZIONE FONDAMENTALE                  |
|                                                                |
|   PRIMA: Stavamo per fare npm publish v0.1.0                   |
|   ORA: "Chiudere il porto e sistemare la nave"                 |
|                                                                |
|   DECISIONE: MCP Server + CLI Standalone + BYOK                |
|   STANDARD: Score minimo 9.5/10                                |
|   APPROVATO: Rafa ha approvato la MAPPA!                       |
+================================================================+
```

---

## PERCHE QUESTO CAMBIO

1. **Domanda iniziale:** Come gestire auth/login per utenti?
2. **Scoperta:** Anthropic ha bloccato subscription per terze parti (9 Gen 2026)
3. **Ricerca:** 8 documenti, 8000+ righe di studio
4. **Soluzione:** MCP (Model Context Protocol) e la via LEGITTIMA

---

## COSA ABBIAMO DECISO

```
CervellaSwarm sara:
1. MCP SERVER - Integrabile con Claude Code
2. CLI STANDALONE - Con opzione BYOK
3. DUAL MODE - Entrambi funzionano

CHI PAGA API: SEMPRE l'utente (BYOK!)
NOI MONETIZZIAMO: Features CervellaSwarm
MARGINI: 90%+ (profittabili DAY 1!)
```

---

## DOCUMENTI CREATI (8!)

| File | Contenuto |
|------|-----------|
| `idee/STUDIO_MCP_PROTOCOL_COMPLETO.md` | MCP protocol in dettaglio (1850 righe) |
| `idee/ARCHITETTURA_MCP_CERVELLASWARM.md` | Design architetturale (2021 righe) |
| `idee/BUSINESS_MODEL_MCP_BYOK.md` | Pricing e strategia (1200 righe) |
| `idee/RICERCA_TECNICA_CURSOR_AUTH.md` | Come fa Cursor |
| `idee/STUDIO_STRATEGICO_AUTH_COMPETITOR.md` | Tutti i competitor |
| `idee/RICERCA_AUTH_CLAUDE_CODE.md` | Auth Claude Code ufficiale |
| `idee/RICERCA_INTEGRAZIONE_CLAUDE_CODE.md` | Perche MCP |
| `idee/ANALISI_AUTH_ATTUALE.md` | Gap codice attuale |

---

## MAPPA APPROVATA

**File:** `MAPPA_MCP_BYOK.md` (nella root progetti/cervellaswarm/)

**Score attuale:** 6.4/10
**Target:** 9.5/10
**Area critica:** Onboarding (0.6/10)

---

## COSA DEVI FARE - FASE 0

```
PRIORITA 1 - Blockers:
[ ] Config manager con `conf` (package gia installato!)
[ ] API key wizard durante init
[ ] API key validation (test call)
[ ] `cervellaswarm doctor` command
[ ] README utente dettagliato

DOVE:
- packages/cli/src/config/manager.js (NUOVO)
- packages/cli/src/commands/init.js (MODIFICARE)
- packages/cli/src/commands/doctor.js (NUOVO)
```

---

## ROADMAP COMPLETA

```
FASE 0: Fondamenta (1-2 settimane) <- SEI QUI
FASE 1: POC MCP Server (2 settimane)
FASE 2: MCP Completo (4 settimane)
FASE 3: Polish & Launch (2 settimane)
```

---

## PRICING DECISO

```
Free:  50 calls/mese, 3 progetti
Pro:   $20/mo, 500 calls, unlimited progetti
Team:  $35/user/mo, 1K calls, shared SNCP
```

---

## LEZIONI SESSIONE

1. **"Chiudere il porto e sistemare la nave"** - Prima fare bene, poi pubblicare
2. **MCP e la via legittima** - Non workaround, ma standard ufficiale
3. **BYOK = margini 90%+** - Utente paga API, noi monetizziamo features
4. **Score 9.5 minimo** - Non accettiamo meno

---

## FILE CHIAVE

- **MAPPA:** `.sncp/progetti/cervellaswarm/MAPPA_MCP_BYOK.md`
- **PROMPT_RIPRESA:** `.sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md`
- **Ricerche:** `.sncp/progetti/cervellaswarm/idee/`

---

*"Fatto BENE > Fatto VELOCE"*
*"IL TEMPO NON CI INTERESSA"*

---

**Buon lavoro!**
