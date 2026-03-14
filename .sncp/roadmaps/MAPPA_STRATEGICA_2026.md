# MAPPA STRATEGICA -- Da Qui alla Community

> **Data:** 14 Marzo 2026 (aggiornata con audit Guardiana Qualita 8.5 + Guardiana Ops 6.8)
> **Fonti:** 7 report (Ingegnera, Scienziata, Researcher x3, Guardiana Qualita, Guardiana Ops)
> **Regola:** Un passo alla volta. Fatto bene > fatto veloce.

---

## DOVE SIAMO (la verita)

| Area | Score | Dato |
|------|-------|------|
| Qualita tecnica | 9.5/10 | 3684 test, 31 moduli, zero deps |
| Distribuzione | 1/10 | 4 stelle GitHub, 3 Show HN con 1 punto |
| Utenti reali | ~0 | Download PyPI = mirror automatici |
| Revenue | $0 | Business model non aggiornato |
| Mercato | Enorme | $7.5B -> $199B entro 2034. Zero competitor diretti |
| Infra tecnica | 8.5/10 | Playground, CI/CD, PyPI, VS Code -- tutto funziona |
| Identita/vetrina | 2/10 | README, sito, description -- raccontano il prodotto SBAGLIATO |

**Il prodotto e pronto. La vetrina no.**

---

## L'IDENTITA (decisione)

```
Lingua Universale = il PRODOTTO (linguaggio verificato per AI)
CervellaSwarm     = l'ORGANIZZAZIONE (come PSF per Python)
```

---

## LA MAPPA

### FASE 0: IDENTITA (BLOCCANTE per lancio)

- [ ] Riscrivere README pubblico: LU in primo piano (pattern big players: portale, non manuale)
- [ ] Primo esempio = problema RISOLTO (prima/dopo, 4-6 righe)
- [ ] CTA singola dominante: playground (zero friction per visitatori HN)
- [ ] GitHub description: "A language for verified AI agent protocols"
- [ ] Aggiornare numeri: 31 moduli, 3684 test (badge stale)
- [ ] sync-to-public.sh dopo il rewrite
- [ ] Guardiana audit del nuovo README

### FASE 1: COMMUNITY FOUNDATION (BLOCCANTE per lancio)

- [ ] Creare Discord (5 canali: #announcements, #general, #help, #show-and-tell, #dev)
- [ ] **Seed Discord con 10-15 persone PRIMA del lancio** (amici, colleghi, contatti AI)
- [ ] Link Discord nel README + playground + primo commento HN
- [ ] Preparare 5-10 risposte tipo per HN ("Why not just use LangGraph?" -> "LU doesn't replace it, it makes it safe")
- [ ] Aggiungere citazione paper Vericoding (arXiv 2509.22908, POPL 2026) nel blog
- [ ] Lista 20-30 persone da contattare con DM personale
- [ ] Commentare/chiudere Dependabot major PR (8 branch aperti = impressione "non mantenuto")

### FASE 2: LANCIO (quando FASE 0-1 sono completate)

- [ ] Show HN con nuovo posizionamento (mercoledi 18:00 CET = 9 AM Pacific)
- [ ] Cross-post: r/ProgrammingLanguages, r/MachineLearning
- [ ] Twitter/X: tag ricercatori (Yoshida, community MPST)
- [ ] Rispondere a OGNI commento HN in tempo reale
- [ ] **NON linkare cervellaswarm.com** (racconta storia vecchia, da aggiornare dopo)

**Piano B (se HN < 10 punti):** Focus su r/ProgrammingLanguages e dev.to come canali primari. Abbandonare HN come canale di lancio -- 4 fallimenti = pattern.

### VALIDAZIONE PMF (2 settimane dopo il lancio)

**Gate check:** Se dopo 2 settimane dal lancio NON abbiamo:
- Almeno 20 stelle GitHub
- Almeno 5 persone nel Discord
- Almeno 1 issue aperta da un esterno

-> FERMARSI e riconsiderare: il problema e il messaggio, il canale, o il prodotto stesso?

### FASE 3: POST-LANCIO (settimane 1-4)

- [ ] Tutorial dev.to: "How I added protocol verification to LangGraph in 20 lines"
  (base: dogfood_runner_live.py, ~2000 parole, 7 min lettura)
- [ ] Integration tutorial: LU + CrewAI
- [ ] Documentation site (MkDocs o Starlight)
- [ ] Documentare il nuovo business model per LU come linguaggio (hosted playground SaaS, enterprise compliance). Il piano BYOK/Sampling di Gennaio 2026 e OBSOLETO.
- [ ] `load_protocol()` public API (gap dal dogfooding, abilita integrazione)

### FASE 4: CRESCITA (mesi 2-6)

- [ ] 50+ stelle, 10+ Discord members = prima milestone
- [ ] Integration plugins per LangGraph/CrewAI/AutoGen
- [ ] Contattare The Pragmatic Engineer newsletter
- [ ] Talk/video su session types per AI
- [ ] GitHub Discussions (dopo 200+ Discord members)
- [ ] CONTRIBUTING.md con guida specifica LU

### FASE 5: MONETIZZAZIONE (mesi 6-12, dopo 500+ stelle)

- [ ] Hosted playground SaaS ($0 individui, $49-99/team)
- [ ] Enterprise: compliance, audit trail, custom stdlib
- [ ] Protocol Registry ("npm per protocolli verificati")

---

## REGOLA D'ORO

```
Nessuna FEATURE PER UTENTI NUOVI finche non abbiamo:
  - 50+ stelle GitHub
  - 10+ persone nel Discord
  - 1 utente esterno che ha scritto qualcosa in LU

Eccezioni: feature che ABILITANO la distribuzione
  - load_protocol() API
  - Integration stubs per LangGraph/CrewAI
  - Bug fix, aggiornamenti dipendenze

Ogni sessione = distribuzione PRIMA, codice SOLO se serve per la distribuzione.
```

---

## METRICHE DA MONITORARE

| Metrica | Oggi | Pessimistico 3m | Realistico 3m | Ottimistico 3m |
|---------|------|-----------------|----------------|-----------------|
| GitHub stars | 4 | 15 | 50 | 150 |
| Discord members | 0 | 5 | 20 | 50 |
| Issues da esterni | 0 | 1 | 5 | 15 |
| Tutorial/blog esterni | 0 | 0 | 2 | 5 |
| Download PyPI organici | ~0 | 20/mese | 100/mese | 300/mese |

---

## POSIZIONAMENTO (come comunicare)

**NON dire:** "Formal verification con Lean 4 e session types"
**DIRE:** "Un type checker per le conversazioni tra i tuoi agenti AI"

**NON dire:** "Competitor di LangGraph/CrewAI"
**DIRE:** "LU non sostituisce il tuo framework, lo rende sicuro. Come TypeScript per JavaScript."

**La storia che funziona:** La Nonna -- una persona non tecnica costruisce un protocollo verificato in 2 minuti parlando italiano.

**Riferimento accademico:** Vericoding (Bursuc, Tegmark et al., arXiv 2509.22908, POPL 2026). Noi applichiamo il paradigma vericoding specificamente a protocolli di comunicazione tra agenti AI.

---

## DOCUMENTI DA AGGIORNARE

- [ ] **NORD.md**: allineare all'identita LU-first, correggere "API Fly.io: ONLINE" (e parzialmente DOWN), reconciliare target
- [ ] **cervellaswarm.com**: aggiornare o non linkare (racconta "17 AI Agents", non LU)

---

## REPORT DI RIFERIMENTO

| Report | Path |
|--------|------|
| Analisi completa (Ingegnera) | `.sncp/progetti/cervellaswarm/reports/ENGINEER_20260314_ANALISI_COMPLETA.md` |
| Analisi strategica (Scienziata) | `.sncp/progetti/cervellaswarm/reports/SCIENTIST_20260314.md` |
| DSL launch patterns (Researcher) | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_DSL_LAUNCH_SUCCESS_PATTERNS.md` |
| Community strategy (Researcher) | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_COMMUNITY_STRATEGY.md` |
| README patterns (Researcher) | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_DSL_README_PATTERNS.md` |

---

*"Il debito tecnico si paga con interessi. Il debito di distribuzione si paga con l'irrilevanza."*

*"Ultrapassar os proprios limites!"*
