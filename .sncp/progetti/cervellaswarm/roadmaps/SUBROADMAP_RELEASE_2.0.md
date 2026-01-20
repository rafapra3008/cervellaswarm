# SUBROADMAP: Release 2.0 - Comunicazione & Allineamento

> **"Il prodotto e' SOLIDO. La comunicazione NO."**
> **Score Target:** 9.5/10

**Creata:** 20 Gennaio 2026 - Sessione 299
**Aggiornata:** 20 Gennaio 2026 - Sessione 300 (Audit Guardiana)
**Basata su:** Analisi Researcher + Marketing + Ingegnera

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|   PROBLEMA: Abbiamo un prodotto 90% pronto                     |
|            ma comunicazione al 70%                             |
|                                                                |
|   SOLUZIONE: Day 0 + 3 fasi, 6 giorni, score 9.5              |
|                                                                |
|   RISULTATO: Sito allineato + docs professionali              |
|                                                                |
|   NOTE: npm 2.0.0-beta GIA PUBBLICATO (19 Gen 2026)           |
|                                                                |
+================================================================+
```

**GIA FATTO (Sessione 287):**
- npm CLI 2.0.0-beta pubblicato
- npm MCP Server 2.0.0-beta pubblicato
- CHANGELOG aggiornato

**Cosa NON cambiamo:**
- Codice (gia solido, 241 test passano)
- Architettura (16 agenti funzionano)
- API Fly.io (running, health OK)
- npm packages (gia 2.0.0-beta!)

**Cosa sistemiamo:**
- Sito web (pricing, testi, feature)
- Documentazione (README, FAQ)
- Coerenza ovunque

---

## STATO ATTUALE vs TARGET

| Area | Attuale | Target | Status |
|------|---------|--------|--------|
| npm CLI | 2.0.0-beta | 2.0.0-beta | DONE |
| npm MCP | 2.0.0-beta | 2.0.0-beta | DONE |
| Sito pricing | Discrepante | Allineato | ALTO |
| Sito feature | Incomplete | W1-W6 visibili | ALTO |
| README | Basic | Differenziatori | MEDIO |
| Stripe | Test Mode | Test Mode (OK) | - |

---

## PIANO: Day 0 + 3 FASI

### DAY 0: DECISIONI RAFA (Blocca tutto il resto)

**Obiettivo:** Prendere decisioni necessarie PRIMA di modificare sito/docs

**Decisioni richieste:**

| # | Decisione | Opzioni | Impatto |
|---|-----------|---------|---------|
| 1 | **Early Bird $99/year** | Tenere / Rimuovere | Pricing page, FAQ |
| 2 | **Pricing finale** | $20/500 calls conferma? | Homepage, checkout |
| 3 | **Stripe Live** | Quando attivare? | Post Show HN? |
| 4 | **v1.0.0 timing** | Dopo quanti utenti beta? | Roadmap |
| 5 | **Tagline homepage** | "16 AI Agents" vs "checks its own work" | Hero section |

**IMPORTANTE:** Senza queste decisioni, FASE 1 non puo iniziare!

---

### FASE 1: SITO WEB - Allineamento (Day 1-2)

**Obiettivo:** Sito riflette prodotto reale

#### Day 1: Fix Critici

**P1 - Pricing Homepage:**
- Attuale: "$20/mo 100 tasks"
- Corretto: "$20/mo 500 calls" (da ANALISI_BUSINESS_MODEL.md)
- File: `landing/index.html` o simile

**P2 - Early Bird:**
- Rimuovere "$99/year" se non validato con Rafa
- O documentare in pricing page

**P3 - Badge "Most Popular":**
- Cambiare in "RECOMMENDED" (onesto)

#### Day 2: Feature Enhancement

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

### FASE 2: DOCUMENTAZIONE - README & FAQ (Day 3-4)

**Obiettivo:** Documentazione completa e attrattiva

#### Day 3: README Enhancement

**packages/cli/README.md:**
- Sezione "Why CervellaSwarm?"
- Differenziatori unici
- Quick start migliorato
- Link a CHANGELOG per W1-W6

**packages/mcp-server/README.md:**
- Famiglia 16 agenti documentata
- Ruoli chiari (3 Guardiane + 12 Worker)
- Integrazione con Claude Desktop

#### Day 4: FAQ & Docs

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

### FASE 3: VERIFICA FINALE (Day 5-6)

**Obiettivo:** Tutto allineato, tutto REALE

#### Day 5: Cross-Check

| Verifica | Comando/Azione |
|----------|----------------|
| npm CLI | `npm view cervellaswarm@beta` |
| npm MCP | `npm view @cervellaswarm/mcp-server@beta` |
| Sito live | Check cervellaswarm.com |
| API health | `curl cervellaswarm-api.fly.dev/health` |
| Docs sync | verify-sync cervellaswarm |

#### Day 6: Audit Finale

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
+------+------+------+------+------+------+------+
| D0   | D1   | D2   | D3   | D4   | D5   | D6   |
+------+------+------+------+------+------+------+
|Decis |Fix   |Feat  |READ  |FAQ   |Cross |Audit |
|Rafa  |Critic|ures  |ME    |Docs  |Check |Final |
+------+------+------+------+------+------+------+
   |          |             |             |
   v          v             v             v
 DAY 0     FASE 1        FASE 2        FASE 3
```

**Durata totale:** Day 0 + 6 giorni (1 progresso al giorno)

**Nota:** npm publish GIA FATTO (Sessione 287) - risparmiati 2 giorni!

---

## DEFINITION OF DONE

**DAY 0: DECISIONI**
- [ ] Early Bird deciso
- [ ] Pricing confermato
- [ ] Stripe timing deciso
- [ ] v1.0.0 criteria definiti
- [ ] Tagline scelto

**FASE 1: SITO WEB**
- [ ] Pricing corretto ovunque
- [ ] Feature W1-W6 visibili
- [ ] Tagline killer in hero
- [ ] Zero claim non verificabili

**FASE 2: DOCUMENTAZIONE**
- [ ] README professionali
- [ ] FAQ complete
- [ ] CHANGELOG visibile

**FASE 3: VERIFICA**
- [ ] Cross-check passato
- [ ] Audit Guardiana 9.5/10
- [ ] Pronto per v1.0.0 (dopo primi utenti)

**GIA COMPLETATO (Sessione 287):**
- [x] npm CLI 2.0.0-beta pubblicato
- [x] npm MCP 2.0.0-beta pubblicato
- [x] Installazione funziona globalmente

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
| ~~npm publish fallisce~~ | ~~Bassa~~ | ~~Alto~~ | ~~GIA FATTO!~~ |
| Breaking changes | Media | Alto | CHANGELOG chiaro |
| Sito deploy issues | Bassa | Medio | Cloudflare rollback |
| Rafa non approva pricing | Media | Medio | Day 0 decisioni PRIMA |
| Stripe non pronto per Live | Media | Alto | Test webhook prima di annunciare |
| Early Bird crea confusione | Alta | Medio | Decidere SI/NO prima di toccare FAQ |
| Feature W1-W6 non comprensibili | Media | Medio | Copy chiaro, user testing |

---

## DECISIONI DA PRENDERE CON RAFA (Day 0)

1. **Early Bird $99/year** - Teniamo o rimuoviamo?
2. **Pricing finale** - $20/500 calls confermato?
3. **Stripe Live** - Quando attivare? (dopo Show HN?)
4. **v1.0.0 timing** - Dopo quanti utenti beta?
5. **Tagline homepage** - "16 AI Agents" (attuale) vs "The only AI team that checks its own work" (differenziante)?

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

> "Un progresso al giorno = Release 2.0 in 6 giorni."

---

*Subroadmap creata da: Regina + Researcher + Marketing + Ingegnera*
*Data: 20 Gennaio 2026 - Sessione 299*
*Aggiornata: 20 Gennaio 2026 - Sessione 300 (Audit Guardiana)*
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
