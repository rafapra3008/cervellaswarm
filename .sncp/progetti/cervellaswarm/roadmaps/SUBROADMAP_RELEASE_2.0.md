# SUBROADMAP: Release 2.0 - Comunicazione & Allineamento

> **"Il prodotto e' SOLIDO. La comunicazione NO."**
> **Score Target:** 9.5/10

**Creata:** 20 Gennaio 2026 - Sessione 299
**Aggiornata:** 20 Gennaio 2026 - Sessione 301 (Ricerca Completa + Findings)
**Basata su:** Analisi Researcher + Marketing + Ingegnera + Ricerca AIDER

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
- Architettura (17 agenti funzionano) ← CORRETTO: 17 non 16!
- API Fly.io (running, health OK)
- npm packages (gia 2.0.0-beta!)

**Cosa sistemiamo:**
- Sito web (pricing, testi, feature)
- Documentazione (README, FAQ)
- Coerenza ovunque

---

## SESSIONE 301 - RICERCA COMPLETA (20 Gen 2026)

### FAMIGLIA CONFERMATA: 17 MEMBRI

| Livello | Membri | Model | Ruolo |
|---------|--------|-------|-------|
| Regina | 1 | Opus | Coordina tutto |
| Guardiane | 3 | Opus | Verificano qualita |
| **Architect** | **1** | **Opus** | **NUOVO! Pianifica task complessi** |
| Worker | 12 | Sonnet | Specialisti |

**TOTALE: 5 Opus + 12 Sonnet = 17 membri!**

### COMPARAZIONE vs AIDER (Ricerca Researcher)

**PARITY RAGGIUNTA:**
- Tree-sitter (W2) = loro "repository map"
- Git Attribution (W1) = loro "auto-commit"
- Architect Pattern (W3-B) = loro "architect mode"

**5 DIFFERENZIATORI NOSTRI:**
1. **17 agent team** vs 1 AI solo
2. **3 Guardiane** verificano qualita (UNICO!)
3. **SNCP 2.0** memoria perfetta vs session-only
4. **Semantic Search API** impact analysis in 2s
5. **Task classification** routing automatico

**5 GAP (Roadmap futura):**
1. Multi-model support (P1) - loro 20+ providers
2. IDE file watching (P1)
3. Voice/image input (P3)
4. Prompt caching esplicito (P2)
5. 100+ languages (P2)

### SNCP 2.0 - COMPLETATO! (Sessione 299)

| Cosa | Status |
|------|--------|
| oggi.md deprecato | DONE |
| Template Handoff 6-sezioni | DONE |
| Hook aggiornati | DONE |
| Score | 9.5/10 |

### W5 DOGFOODING - STATO VERIFICATO (Sessione 301)

> **NOTA:** Report Ingegnera (19 Gen) era OUTDATED. Verificato 20 Gen - tutto INTEGRATO!

| Feature | Creata | Integrata | Come Usare |
|---------|--------|-----------|------------|
| W1 Git Flow | 100% | ✅ 100% | `spawn-workers --auto-commit` |
| W2 Tree-sitter | 100% | ✅ Auto | Auto-context per worker code-aware |
| W3-A Semantic Search | 100% | ✅ CLI | `semantic-search.sh find-symbol "X"` |
| W3-B Architect | 100% | ✅ Flag | `spawn-workers --architect "task"` |
| W4 CI/CD | 100% | ✅ Auto | GitHub Actions su push/PR |

**STRUMENTI VERIFICATI (20 Gen 2026):**
- `spawn-workers.sh v3.9.0` - Include --architect (v3.8.0)
- `semantic-search.sh v1.0.0` - CLI wrapper completo
- `impact_analyzer.py` - API disponibile
- Auto-context per 8 worker code-aware (v3.9.0)

### FILE RICERCA CREATI (Sessione 301)

- `.swarm/tasks/RICERCA_AIDER_VS_CERVELLASWARM.md` - Comparativa completa
- `.swarm/tasks/MARKETING_COMUNICAZIONE_V2.md` - Copy pronti all'uso

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
- Famiglia 17 agenti documentata (incluso Architect!)
- Ruoli chiari (1 Regina + 3 Guardiane + 1 Architect + 12 Worker)
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

**DAY 0: DECISIONI** ✅ COMPLETATO (Sessione 300)
- [x] Early Bird deciso ($149/anno Founding Members)
- [x] Pricing confermato (FREE/PRO $29/TEAM $49)
- [x] Stripe timing deciso (dopo 50 utenti beta)
- [x] v1.0.0 criteria definiti (dopo 100-200 utenti 30d)
- [x] Tagline scelto ("checks its own work")

**FASE 1: SITO WEB** - IN PROGRESS
- [ ] Pricing corretto ovunque ($29/$49)
- [ ] Feature W1-W6 visibili
- [ ] Tagline killer in hero ✅ FATTO (Sessione 300)
- [ ] Zero claim non verificabili
- [ ] **NUOVO:** Famiglia 17 membri documentata (non 16!)
- [ ] **NUOVO:** Self-Checking come feature #1

**FASE 2: DOCUMENTAZIONE**
- [ ] README professionali
- [ ] FAQ complete
- [ ] CHANGELOG visibile
- [ ] **NUOVO:** Architect Pattern documentato
- [ ] **NUOVO:** Differenziatori vs AIDER

**FASE 3: VERIFICA**
- [ ] Cross-check passato
- [ ] Audit Guardiana 9.5/10
- [ ] Pronto per v1.0.0 (dopo primi utenti)

**FASE 4: W5 DOGFOODING** ✅ COMPLETATO (Verificato Sessione 301)
- [x] Architect integrato in spawn-workers (--architect flag) ← v3.8.0!
- [x] Semantic Search CLI wrapper creato ← semantic-search.sh v1.0.0!
- [x] CLAUDE.md aggiornato con nuove feature ← Sessione 301!
- [x] Test REALE: semantic-search.sh PASSATO! ← Sessione 301!

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

## DECISIONI CON RAFA (Day 0) - Sessione 300

### DECISIONI PRESE

| # | Decisione | Scelta | Data |
|---|-----------|--------|------|
| 5 | **Tagline homepage** | "The only AI coding team that checks its own work" | 20 Gen 2026 |
| 4 | **v1.0.0 timing** | Dopo 100-200 utenti attivi 30 giorni (~15 Apr 2026) | 20 Gen 2026 |
| 3 | **Stripe Live** | Dopo 50 utenti beta, retention >30%, 0 critical bugs (~15 Feb 2026) | 20 Gen 2026 |
| 2 | **Pricing finale** | FREE $0 (3 agenti, 50 tasks) / PRO $29 (16 agenti, unlimited) / TEAM $49/user | 20 Gen 2026 |
| 1 | **Early Bird** | $149/anno per primi 200 "Founding Members" (-57% vs $348 annuale) | 20 Gen 2026 |

### PRICING STRUCTURE DETTAGLIATA (Decisione 2)

| Tier | Prezzo | Agenti | Tasks | Target |
|------|--------|--------|-------|--------|
| FREE | $0/mo | 3 | 50/mese | Studenti, hobby |
| PRO | $29/mo | 16 | UNLIMITED | Indie dev, freelance |
| TEAM | $49/user/mo | 16 | UNLIMITED | Team 3-10 |
| ENTERPRISE | Custom | Custom | UNLIMITED | Aziende |

**Unità:** TASKS (1 task = 1 spawn-workers)
**Naming:** Free/Pro/Team/Enterprise
**Valore:** $1.81/agente vs $20+ competitor

### EARLY BIRD DETTAGLIO (Decisione 1)

| Aspetto | Valore |
|---------|--------|
| Prezzo | $149/anno |
| Durata | **LIFETIME** - prezzo bloccato per sempre |
| Limite | Primi 200 utenti (no deadline temporale) |
| Sconto | -57% vs PRO annuale ($348) |
| Messaging | **"Founding Member"** (esclusivo, non discount) |

**Cosa include Founding Member:**
- Tutto PRO (16 agenti, unlimited tasks)
- Badge "Founding Member" sul profilo
- Priority feature requests
- Accesso anticipato nuove feature
- Prezzo $149 BLOCCATO per sempre (anche se PRO aumenta)

**Copy suggerito:**
> "Become a Founding Member: Lock in $149/year forever.
> After 200 members: $348/year. Your price never changes."

**TUTTE LE 5 DECISIONI COMPLETATE - Day 0 DONE!**

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
|   17 agenti funzionano. Nessuno lo sa.                         |
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

## MESSAGGI KILLER DA COMUNICARE (Marketing Sessione 301)

**Tagline principale:**
> "The only AI coding team that checks its own work"

**3 Differenziatori (comunicare SEMPRE):**
1. **Self-Checking System** - 3 Guardiane Opus verificano ogni output
2. **Semantic Code Understanding** - Tree-sitter, non grep
3. **Architect-First Workflow** - Piano → Codice → Verifica

**Copy user-centric:**
- "Capisce il tuo codice come un senior developer"
- "Impatto modifiche in 2 secondi"
- "Piano prima, codice dopo. Zero refactoring a meta strada"
- "Ricorda tutto, anche dopo settimane" (SNCP)

**Analogie per utenti:**
- Tree-sitter = "Google per codice, ma preciso"
- 17 Agenti = "Software house con ruoli"
- Guardiane = "Code review senior automatico"

---

*Subroadmap creata da: Regina + Researcher + Marketing + Ingegnera*
*Data: 20 Gennaio 2026 - Sessione 299*
*Aggiornata: 20 Gennaio 2026 - Sessione 301 (Ricerca Completa + Findings)*
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
