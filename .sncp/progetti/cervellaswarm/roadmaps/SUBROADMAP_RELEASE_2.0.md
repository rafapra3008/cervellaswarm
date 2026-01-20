# SUBROADMAP: Release 2.0 - Comunicazione & Allineamento

> **"Il prodotto e' SOLIDO. La comunicazione NO."**
> **Score Target:** 9.5/10

**Creata:** 20 Gennaio 2026 - Sessione 299
**Basata su:** Analisi Researcher + Marketing + Ingegnera

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|   PROBLEMA: Abbiamo un prodotto 90% pronto                     |
|            ma comunicazione/versioni al 70%                    |
|                                                                |
|   SOLUZIONE: 4 fasi, 8 giorni, score 9.5                       |
|                                                                |
|   RISULTATO: v2.0.0-beta REALE su npm + sito allineato        |
|                                                                |
+================================================================+
```

**Cosa NON cambiamo:**
- Codice (gia solido, 241 test passano)
- Architettura (16 agenti funzionano)
- API Fly.io (running, health OK)

**Cosa sistemiamo:**
- npm packages (0.1.2 -> 2.0.0-beta)
- Sito web (pricing, testi, feature)
- Documentazione (README, FAQ)
- Coerenza ovunque

---

## STATO ATTUALE vs TARGET

| Area | Attuale | Target | Gap |
|------|---------|--------|-----|
| npm CLI | 0.1.2 | 2.0.0-beta | CRITICO |
| npm MCP | 0.2.3 | 2.0.0-beta | CRITICO |
| Sito pricing | Discrepante | Allineato | ALTO |
| Sito feature | Incomplete | W1-W6 visibili | ALTO |
| README | Basic | Differenziatori | MEDIO |
| Stripe | Test Mode | Test Mode (OK) | - |

---

## PIANO 4 FASI

### FASE 1: TECNICA - npm Publish (Day 1-2)

**Obiettivo:** Pubblicare v2.0.0-beta su npm

#### Day 1: Verifica e Preparazione

```bash
# 1. Verifica test passano
cd packages/cli && npm test
cd packages/mcp-server && npm run build && npm test

# 2. Verifica CHANGELOG aggiornato
# 3. Verifica README packages aggiornati
```

**Checklist:**
- [ ] CLI tests passano
- [ ] MCP Server tests passano
- [ ] CHANGELOG ha entry v2.0.0-beta
- [ ] README CLI ha feature W1-W6
- [ ] README MCP ha famiglia 16 agenti

#### Day 2: Pubblicazione

```bash
# CLI
cd packages/cli
npm publish --tag beta

# MCP Server
cd packages/mcp-server
npm run build
npm publish --tag beta

# Verifica
npm view cervellaswarm@beta version
npm view @cervellaswarm/mcp-server@beta version
```

**Checklist:**
- [ ] CLI 2.0.0-beta su npm
- [ ] MCP Server 2.0.0-beta su npm
- [ ] Installazione funziona: `npm i -g cervellaswarm@beta`

**Audit Guardiana:** Score target 9.5/10

---

### FASE 2: SITO WEB - Allineamento (Day 3-4)

**Obiettivo:** Sito riflette prodotto reale

#### Day 3: Fix Critici

**P1 - Pricing Homepage:**
- Attuale: "$20/mo 100 tasks"
- Corretto: "$20/mo 500 calls" (da ANALISI_BUSINESS_MODEL.md)
- File: `landing/index.html` o simile

**P2 - Early Bird:**
- Rimuovere "$99/year" se non validato con Rafa
- O documentare in pricing page

**P3 - Badge "Most Popular":**
- Cambiare in "RECOMMENDED" (onesto)

#### Day 4: Feature Enhancement

**Sezione "What Makes Us Different":**
Aggiungere differenziatori W1-W6:

```markdown
- Tree-sitter AST Parsing (semantic code search)
- Architect Pattern (Opus planning before coding)
- Git Worker Attribution (conventional commits)
- Self-Checking System (Guardiane audit 9.5+ score)
- SNCP Memory System (perfect context persistence)
```

**Tagline above fold:**
> "The only AI coding team that checks its own work"

**Checklist:**
- [ ] Pricing corretto
- [ ] Early Bird rimosso/validato
- [ ] Badge onesto
- [ ] Feature W1-W6 visibili
- [ ] Tagline killer in hero

**Audit Guardiana:** Score target 9.5/10

---

### FASE 3: DOCUMENTAZIONE - README & FAQ (Day 5-6)

**Obiettivo:** Documentazione completa e attrattiva

#### Day 5: README Enhancement

**packages/cli/README.md:**
- Sezione "Why CervellaSwarm?"
- Differenziatori unici
- Quick start migliorato
- Link a CHANGELOG per W1-W6

**packages/mcp-server/README.md:**
- Famiglia 16 agenti documentata
- Ruoli chiari (3 Guardiane + 12 Worker)
- Integrazione con Claude Desktop

#### Day 6: FAQ & Docs

**docs/FAQ.md:**
- "Why beta?" - Spiegazione onesta
- "What's unique?" - Differenziatori
- "Pricing?" - Chiarezza totale
- "Roadmap?" - Link a NORD.md

**Checklist:**
- [ ] README CLI professionale
- [ ] README MCP completo
- [ ] FAQ aggiornate
- [ ] Link interni funzionano

**Audit Guardiana:** Score target 9.5/10

---

### FASE 4: VERIFICA FINALE (Day 7-8)

**Obiettivo:** Tutto allineato, tutto REALE

#### Day 7: Cross-Check

| Verifica | Comando/Azione |
|----------|----------------|
| npm CLI | `npm view cervellaswarm@beta` |
| npm MCP | `npm view @cervellaswarm/mcp-server@beta` |
| Sito live | Check cervellaswarm.com |
| API health | `curl cervellaswarm-api.fly.dev/health` |
| Docs sync | verify-sync cervellaswarm |

#### Day 8: Audit Finale

**Guardiana Qualita:**
- Review npm packages
- Review sito web
- Review documentazione
- Score finale

**Checklist:**
- [ ] Tutto allineato
- [ ] Zero discrepanze
- [ ] Score 9.5/10

---

## TIMELINE

```
+------+------+------+------+------+------+------+------+
| D1   | D2   | D3   | D4   | D5   | D6   | D7   | D8   |
+------+------+------+------+------+------+------+------+
|Prep  |Publi |Fix   |Feat  |READ  |FAQ   |Cross |Audit |
|Test  |sh npm|Critic|ures  |ME    |Docs  |Check |Final |
+------+------+------+------+------+------+------+------+
        |             |             |             |
        v             v             v             v
     FASE 1        FASE 2        FASE 3        FASE 4
```

**Durata totale:** 8 giorni (1 progresso al giorno)

---

## DEFINITION OF DONE

**FASE 1: TECNICA**
- [ ] npm CLI 2.0.0-beta pubblicato
- [ ] npm MCP 2.0.0-beta pubblicato
- [ ] Installazione funziona globalmente

**FASE 2: SITO WEB**
- [ ] Pricing corretto ovunque
- [ ] Feature W1-W6 visibili
- [ ] Tagline killer in hero
- [ ] Zero claim non verificabili

**FASE 3: DOCUMENTAZIONE**
- [ ] README professionali
- [ ] FAQ complete
- [ ] CHANGELOG visibile

**FASE 4: VERIFICA**
- [ ] Cross-check passato
- [ ] Audit Guardiana 9.5/10
- [ ] Pronto per v1.0.0 (dopo primi utenti)

---

## METRICHE SUCCESSO

| Metrica | Prima | Dopo | Come Misurare |
|---------|-------|------|---------------|
| npm version gap | 2.0 vs 0.1 | 0 | npm view |
| Sito discrepanze | 3+ | 0 | Manual review |
| Feature visibili | 30% | 100% | Checklist W1-W6 |
| README quality | Basic | Pro | Guardiana audit |
| Overall score | 7/10 | 9.5/10 | Guardiana finale |

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| npm publish fallisce | Bassa | Alto | Test locale prima |
| Breaking changes | Media | Alto | CHANGELOG chiaro |
| Sito deploy issues | Bassa | Medio | Cloudflare rollback |
| Rafa non approva pricing | Media | Medio | Chiedi PRIMA di cambiare |

---

## DECISIONI DA PRENDERE CON RAFA

1. **Early Bird $99/year** - Teniamo o rimuoviamo?
2. **Pricing finale** - $20/500 calls confermato?
3. **Stripe Live** - Quando attivare? (dopo Show HN?)
4. **v1.0.0 timing** - Dopo quanti utenti beta?

---

## NOTA IMPORTANTE

```
+================================================================+
|                                                                |
|   IL CODICE E' PRONTO. LA COMUNICAZIONE NO.                   |
|                                                                |
|   Non stiamo "creando" nulla di nuovo.                         |
|   Stiamo COMUNICANDO quello che abbiamo GIA'.                  |
|                                                                |
|   Feature W1-W6 esistono. Nessuno lo sa.                       |
|   16 agenti funzionano. Nessuno lo sa.                         |
|   Score 9.6/10 media. Nessuno lo sa.                           |
|                                                                |
|   ORA LO SAPRANNO.                                             |
|                                                                |
+================================================================+
```

---

## MANTRA

> "Il prodotto parla da solo... se qualcuno glielo fa dire."

> "Marketing non e' vendere. E' raccontare la verita' in modo che la gente la capisca."

> "Un progresso al giorno = Release 2.0 in 8 giorni."

---

*Subroadmap creata da: Regina + Researcher + Marketing + Ingegnera*
*Data: 20 Gennaio 2026 - Sessione 299*
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
