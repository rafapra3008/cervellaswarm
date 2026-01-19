# Ricerca Reddit - Requisiti Posting Subreddit Tecnici

**Data:** 19 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Obiettivo:** Identificare requisiti per postare su subreddit tecnici in vista del lancio CervellaSwarm (26 Gennaio 2026)

---

## TL;DR - Raccomandazioni

| Subreddit | Priorità | Difficoltà | Requisiti Stimati | Raccomandazione |
|-----------|----------|------------|-------------------|-----------------|
| **r/SideProject** | ⭐⭐⭐ ALTA | ✅ FACILE | Nessun requisito specifico | **INIZIA QUI** - Ideale per CervellaSwarm |
| **r/ClaudeAI** | ⭐⭐⭐ ALTA | ✅ FACILE | No requisiti pubblici | **OTTIMO** - Target perfetto |
| **r/webdev** | ⭐⭐ MEDIA | ⚠️ MEDIA | ~100-1000 karma (stimato) | Possibile, dopo build karma |
| **r/programming** | ⭐ BASSA | 🔴 DIFFICILE | ~100-1000 karma + strict rules | Solo se molto rilevante |
| **r/LocalLLaMA** | ⭐ BASSA | ⚠️ MEDIA | ~100+ karma (stimato) | Marginal fit (usa Claude, non local) |

**Strategia Consigliata:**
1. **Settimana 1-2:** Build karma su r/ClaudeAI e r/webdev (commenti utili, non spam)
2. **Lancio (26 Gen):** Post su r/SideProject e r/ClaudeAI
3. **Post-lancio:** r/webdev se hai 100+ karma

---

## 1. r/programming

**Membri:** 5.8M
**Attività:** Altissima
**Self-Promotion:** Molto limitata (~10% del tuo contenuto totale)

### Requisiti (Stimati)
- **Karma:** 100-1000 (non pubblico, ma stimato per subreddit di questa dimensione)
- **Account Age:** Probabilmente 7-30 giorni
- **Karma Type:** Combinato (post + comment)

### Regole Chiave
1. **Self-Promotion Limitata:** Max ~10% del tuo contenuto totale
2. **Qualità Alta:** Contenuto deve essere tecnicamente rilevante
3. **No Landing Pages:** Il progetto deve essere utilizzabile, non solo marketing
4. **Contribuisci Prima:** Non usare Reddit come piattaforma pubblicitaria

### Best Practices
- "Be a Redditor with a website, not a website with a Reddit account"
- Segui la regola 80/20: 80% partecipazione, 20% promozione
- Aggiungi sempre un commento iniziale spiegando tecnicamente il progetto
- Usa linguaggio tecnico, non marketing

### Raccomandazione per CervellaSwarm
⚠️ **ATTENZIONE** - r/programming ha regole molto strict. CervellaSwarm è rilevante ma:
- Aspetta di avere karma solido (100+)
- Posiziona come "Show HN-style": "I built a multi-agent orchestration system with Claude"
- Focus su architettura tecnica, non marketing
- **Rischio ban alto se appare come pura self-promotion**

---

## 2. r/ClaudeAI

**Membri:** 386K
**Attività:** Molto alta ("crazy activity")
**Self-Promotion:** Permessa se rilevante e con disclosure

### Requisiti (Stimati)
- **Karma:** Nessun requisito pubblico dichiarato
- **Account Age:** Probabile minimo (7 giorni?)
- **Verificato:** Read rules before posting

### Regole Chiave (Ufficiali)

1. **Non Anthropic-Controlled**
   - Subreddit non gestito da Anthropic
   - Per problemi account → support.anthropic.com

2. **Self-Promotion Permessa MA:**
   - Full disclosure di cosa fai e perché
   - Dichiara tua associazione con il progetto
   - Privilegi posting dipendono da partecipazione utile

3. **Good Faith Discussion**
   - Diversità opinioni benvenuta
   - No personal attacks, no harassment

4. **Stay Relevant**
   - Deve essere rilevante a Claude
   - Post generici AI non accettati
   - Se menzioni competitor → confronto dettagliato con Claude

5. **Value Addition**
   - Post devono aggiungere conoscenza/esperienza
   - No duplicati recenti
   - No agitazione gratuita

6. **Performance Reports**
   - Usa Megathread stickied per esperienze/performance

### Best Practices
- Fornisci **contesto** (use case, setup, challenges)
- Condividi **esempi specifici** quando chiedi aiuto
- Follow-up su soluzioni (cosa ha funzionato?)
- Contribuisci scoperte e prompt di successo

### Raccomandazione per CervellaSwarm
✅ **IDEALE** - r/ClaudeAI è perfetto per CervellaSwarm:
- Target audience esatto (utenti Claude avanzati)
- Self-promotion permessa con disclosure
- CervellaSwarm è 100% rilevante (sistema multi-agent per Claude)
- Community interessata a tool/automation

**Template Post Suggerito:**
```
Title: [I built] CervellaSwarm - Multi-Agent Orchestration for Claude Code

Body:
Hi r/ClaudeAI! Sono l'autore di CervellaSwarm, un sistema che estende
Claude Code con 16 agenti specializzati coordinati da una Regina.

**Cosa fa:**
- Orchestrazione multi-agent (1 Regina + 3 Guardiane + 12 Worker)
- Task delegation intelligente
- Memory management cross-session (SNCP system)

**Perché l'ho costruito:**
Claude Code è potente ma single-threaded. CervellaSwarm permette di
delegare task complessi ad agenti specializzati in contesti separati.

**Tech Stack:** Python, Claude API, bash automation

**Open Source:** [link GitHub]

Feedback benvenuto! Quali use case vi interesserebbero?

[Full disclosure: Sono il creator del progetto, lo condivido per feedback]
```

---

## 3. r/SideProject

**Membri:** 576K
**Attività:** Altissima ("huge community with crazy activity")
**Self-Promotion:** Esplicitamente benvenuta

### Requisiti (Ufficiali)
- **Karma:** ✅ NESSUN REQUISITO SPECIFICO
- **Account Age:** Account attivo (non fresh spam account)
- **Engagement:** Consigliato avere qualche interazione, non solo post promozionali

### Regole Chiave
1. **Self-Promotion Welcome** - Subreddit fatto per questo
2. **Constructive Feedback** - Focus su ricevere feedback costruttivo
3. **Show, Don't Tell** - Video/demo performano meglio

### Best Practices

**Formato Contenuto:**
- ✅ **Video demo** - Performa meglio su r/SideProject
- Mostra il prodotto in azione
- Rendi facile capire cosa fa

**Positioning:**
- Usa "I made this..." invece di "Our company..."
- Community più forgiving con indie makers
- Accetta feedback su bug/rough edges

**Account:**
- Evita account "pure advertising"
- Meglio avere qualche engagement altrove
- Non serve molto, ma almeno qualche commento

### Raccomandazione per CervellaSwarm
✅ **PERFETTO** - r/SideProject è IL posto migliore per lanciare:
- Zero barriere all'entry
- Community welcoming per side projects
- Target giusto (indie makers, developers)
- Self-promotion esplicitamente permessa

**Template Post Suggerito:**
```
Title: I built CervellaSwarm - 16 AI agents coordinating like a swarm 🐝

Body:
Hey r/SideProject! I made a multi-agent system that turns Claude Code
into a coordinated swarm of 16 specialized AI agents.

[VIDEO/GIF demo of task delegation]

**What it does:**
- 1 Queen orchestrates 16 specialized agents
- Automated task distribution
- Persistent memory across sessions

**Why I built it:**
I was frustrated with Claude Code's single-thread limitation. Wanted
to delegate complex tasks to specialist agents.

**Open Source:** [GitHub link]

This is my first multi-agent system. Feedback super welcome!

Tech stack: Python, Claude API, bash scripts
```

---

## 4. r/webdev

**Membri:** ~1M
**Attività:** Alta
**Self-Promotion:** Permessa con moderazione

### Requisiti (Stimati)
- **Karma:** 100-1000 (non pubblico, stimato per dimensione)
- **Account Age:** Probabile 7-30 giorni
- **Type:** Mid-to-large subreddit rules

### Regole Generali (Non Specifiche Trovate)
- Subreddit requirements non pubblicamente dichiarati
- Tipico mid-size subreddit: 10-100 karma minimo
- Large subreddit: 100-1000+ karma + account age

### Best Practices
- Contribuisci prima di promuovere
- Focus su aspetti tecnici web development
- Evita puro marketing

### Raccomandazione per CervellaSwarm
⚠️ **POSSIBILE** - r/webdev è rilevante se:
- Enfasi su web development automation
- Hai già 100+ karma
- Posizioni come "tool for web developers"

**Angolo per r/webdev:**
"Multi-agent system to automate web development workflows - frontend, backend, testing agents working together"

---

## 5. r/LocalLLaMA

**Membri:** 603K
**Attività:** Alta
**Focus:** Local LLMs (Llama, ecc.)

### Requisiti (Stimati)
- **Karma:** 100+ (stimato)
- **Account Age:** Probabile 7+ giorni
- **Rilevanza:** Progetti AI/LLM

### Fit per CervellaSwarm
⚠️ **MARGINAL** - r/LocalLLaMA è focused su local models:
- CervellaSwarm usa Claude (API-based, non local)
- Community potrebbe essere meno interessata
- Meglio altri subreddit

### Se Decidessi di Postare
- Enfatizza architettura multi-agent (universale)
- Menziona compatibilità futura con local models
- Focus su orchestration pattern, non Claude-specific

---

## Requisiti Generali Reddit 2026

### Karma Requirements by Subreddit Size

| Dimensione | Karma Tipico | Account Age |
|------------|--------------|-------------|
| Small/casual | 0 karma | Nessuno |
| Mid-size | 10-100 karma | 7-30 giorni |
| Large/popular | 100-1000+ karma | 7-30 giorni |
| Premium/specialized | 1000-10000 karma | 30+ giorni |

### Perché Requisiti Sono Nascosti
- **Anti-spam:** Difficile per bot/spammer "farm" karma
- **AutoMod:** Ti dice requisiti se post rimosso
- **Strategia:** Subreddit non dichiarano pubblicamente threshold esatti

### Come Trovare Requisiti Specifici
1. **Sidebar/Rules:** Desktop → sidebar, Mobile → Community Info
2. **Tentativo Post:** AutoMod ti dice se mancano requisiti
3. **Partecipa:** Commenti utili → build karma naturalmente

---

## Strategia Consigliata - Timeline Lancio

### Fase 1: Pre-Lancio (Ora - 25 Gennaio)

**Obiettivo:** Build karma iniziale

1. **Crea account Reddit** (se non hai)
2. **Partecipa su r/ClaudeAI:**
   - Rispondi domande su Claude Code
   - Condividi esperienze utili
   - Target: 50+ comment karma
3. **Partecipa su r/webdev:**
   - Commenti su thread rilevanti
   - Condividi knowledge
   - Target: 50+ comment karma

**Tempo richiesto:** 30-60 min/giorno per 5-7 giorni

### Fase 2: Lancio (26 Gennaio)

**Mattina (EU time):**
1. **Post su r/SideProject** (zero requisiti)
   - Video demo
   - "I made this" positioning
   - Link GitHub

**Pomeriggio/Sera:**
2. **Post su r/ClaudeAI** (se hai 50+ karma)
   - Technical deep dive
   - Full disclosure
   - Focus su use cases Claude

### Fase 3: Post-Lancio (27-30 Gennaio)

**Se hai 100+ karma:**
3. **Post su r/webdev**
   - Angolo automation per web dev
   - Link a post r/SideProject per traction

**Solo se molto confident:**
4. **r/programming** (rischio ban)
   - Aspetta feedback positivi da altri sub
   - Technical angle only
   - "Show HN" style

---

## Best Practices Universali Reddit

### Content Creation

1. **Video/GIF > Testo**
   - Demo visuale performa meglio
   - Facile da capire subito
   - Più engagement

2. **"I made this" > "Our product"**
   - Indie maker positioning
   - Community più forgiving
   - Autentico

3. **Technical Details**
   - Spiega COME funziona
   - Menziona tech stack
   - Confronta con alternative

4. **Primo Commento**
   - Sempre primo a commentare il tuo post
   - Aggiungi contesto tecnico
   - "I'm the author, AMA"

### Engagement Strategy

**Regola 80/20:**
- 80% partecipazione normale
- 20% self-promotion

**Build Karma:**
- Commenta su post altrui (utile)
- Rispondi domande
- Condividi knowledge genuino

**Timing:**
- US East Coast: 9am-12pm EST (pomeriggio EU)
- Evita weekend (meno attività)
- Martedì-Giovedì migliori giorni

### Red Flags da Evitare

❌ **Account nuovo + solo self-promotion**
❌ **Marketing language invece di tecnico**
❌ **Link a Twitter/X come primary link**
❌ **"Best", "Amazing", "Revolutionary" hype**
❌ **No video/demo, solo testo**
❌ **Cross-posting identico su tutti i sub**

✅ **Account con history**
✅ **Linguaggio tecnico, umile**
✅ **GitHub/demo come primary**
✅ **"I built", "Feedback welcome"**
✅ **Video demo showing value**
✅ **Customized per ogni subreddit**

---

## Raccomandazione Finale

### Per Lancio CervellaSwarm (26 Gennaio 2026)

**STRATEGIA A TRE LIVELLI:**

#### Tier 1: SAFE BETS (Alta Priorità)
1. ✅ **r/SideProject** - Zero barriere, perfect fit
2. ✅ **r/ClaudeAI** - Target audience perfetto

**Azione:** Post sicuri su entrambi il 26 Gennaio

#### Tier 2: BUILD KARMA FIRST (Media Priorità)
3. ⚠️ **r/webdev** - Serve 100+ karma
4. ⚠️ **r/opensource** - Se enfatizzi open source

**Azione:** Partecipa questa settimana, posta dopo lancio iniziale

#### Tier 3: ADVANCED (Bassa Priorità)
5. 🔴 **r/programming** - Alto rischio ban, serve >500 karma
6. 🔴 **r/LocalLLaMA** - Marginal fit

**Azione:** Solo se hai traction da altri sub + karma solido

### Next Steps Immediate

**Oggi (19 Gen):**
- [ ] Verifica di avere account Reddit attivo
- [ ] Check karma attuale

**20-25 Gennaio:**
- [ ] Partecipa r/ClaudeAI (target 50 karma)
- [ ] Partecipa r/webdev (target 50 karma)
- [ ] Prepara video demo CervellaSwarm
- [ ] Scrivi 3 versioni post (SideProject, ClaudeAI, webdev)

**26 Gennaio (Lancio):**
- [ ] Post r/SideProject (mattina EU)
- [ ] Post r/ClaudeAI (pomeriggio EU)
- [ ] Monitor feedback, rispondere attivamente

**27-30 Gennaio:**
- [ ] Post r/webdev (se karma OK)
- [ ] Crosspost su altri sub se traction buona

---

## Conclusioni

**Status:** ✅ RICERCA COMPLETATA

**TL;DR per la Regina:**
- r/SideProject e r/ClaudeAI sono **safe bets** per il lancio
- r/webdev e r/programming richiedono **karma building** (5-7 giorni)
- **Strategia consigliata:** Inizia partecipazione ora, lancia su 2 sub principali il 26 Gen

**File Creati:**
- Questo documento: `.sncp/progetti/cervellaswarm/RICERCA_REDDIT_REQUISITI.md`

**Fonti Principali:**
- Search Engine Journal (Reddit Karma 2025)
- Postiz (Reddit Karma Requirements Guide)
- MediaFast (r/SideProject Marketing)
- GummySearch (Subreddit Stats)
- ClaudeLog (r/ClaudeAI Info)

---

*Ricerca completata da Cervella Researcher - 19 Gennaio 2026*
*"Non reinventiamo la ruota - studiamo chi l'ha già fatta!"* 🔬
