# Show HN Strategy - Ricerca Completa
**Data:** 2026-02-25
**Ricercatore:** Cervella Researcher
**Status:** COMPLETA
**Fonti:** 22 consultate

---

## 1. Stato del Mercato Show HN nel 2025-2026

### Performance media per categoria
La ricerca statistica di Sturdy Statistics (post con 134 punti su HN) rivela:
- **Weekend (sabato/domenica)**: 11.08-11.75% "breakout rate" (post che superano 30 voti)
- **Giorni feriali**: 9.45-9.90% breakout rate
- **Il weekend e 20-30% piu efficace** dei giorni feriali
- Post Show HN hanno distribuzione bimodale: piu facile superare i 10 punti della media, ma superare 100 ha le stesse probabilita dei post normali

### Tendenza AI su HN nel 2025
DATO CRITICO: AI-related Show HN posts **underperformano le aspettative** nel 2025.
- "AI Automation" e l'unico sub-topic AI che performa meglio della sua prevalenza
- La maggior parte degli AI project Show HN si trova nel "quadrant of death" (alto volume, bassa performance relativa)
- Ragione: l'AI ha prodotto piu contenuto ma piu superficiale, il rumore rende piu difficile scoprire contenuto genuino
- Q3 2025 ha visto sentiment piu negativo verso AI su HN

**Implicazione per CervellaSwarm:** Il progetto deve differenziarsi chiaramente dall'orda di "yet another AI framework". La verifica formale e il type system sono il differenziatore principale.

---

## 2. Top Show HN 2025 - Cosa ha funzionato

### Post di successo 2025 (con punti)

| Punti | Progetto | Pattern |
|-------|----------|---------|
| 3237 | Open-source laptop costruito da zero | Hardware + storia personale |
| 1581 | Sviluppatore ex-Meta, gioco indie su Steam | Storia personale autentica |
| 1539 | Airline pilot, visualizzazione voli interattiva | Expertise unica + visuale |
| 1289 | Tetris giocabile dentro un PDF | Trucco tecnico sorprendente |
| 1278 | Sintetizzatore costruito per la figlia | Storia emotiva + tecnica |
| 1094 | Term.everything: GUI apps nel terminale | Tool pratico + demo immediata |
| 756 | Nue framework (lightweight) | Posizionamento anti-bloat |
| 652 | Dia: text-to-speech open-weights | Open-weights + qualita reale |
| 616 | Browser MCP per Cursor/Claude | Integrazioni specifiche |
| 524 | Real-time AI voice chat ~500ms latency | Numero concreto specifico |
| 461 | BadSeek: backdoor di language models | Security research originale |
| 449 | Scripton IDE con visualizzazioni | Developer tool specifico |

### Pattern comuni nei successi
1. **Storia personale**: "I built this because..." risuona piu di qualsiasi pitch
2. **Demo immediata**: si puo provare subito, senza email, senza signup
3. **Numero concreto**: "500ms", "3791 tests", "zero dependencies"
4. **Differenziatore tecnico specifico**: non "migliore", ma "diverso in questo modo preciso"
5. **Open source**: sempre un vantaggio su HN

---

## 3. Struttura Ideale di un Show HN Post

### Titolo - Le Regole

**Formato base:**
```
Show HN: [Cosa hai costruito] – [differenziatore in una frase]
```

**Esempi di titoli che funzionano (pattern analizzato):**
- "Show HN: PromptTools – open-source tools for evaluating LLMs and vector DBs"
- "Show HN: Redbean – single-file web server"
- "Show HN: Browser MCP – automate your browser from Cursor/Claude"

**Regole per il titolo:**
- Specifico e diretto, zero marketing language
- NIENTE superlative: no "fastest", "best", "revolutionary"
- NIENTE "first ever" a meno che non sia verificabile e clamoroso
- Include il differenziatore tecnico nel titolo stesso
- Max 80-100 caratteri
- "Show HN:" e obbligatorio come prefisso

**Titoli da evitare (pattern di fallimento):**
- "Show HN: CervellaSwarm - The AI Agent Framework" (troppo generico)
- "Show HN: The Future of AI Development" (marketing speak)
- "Show HN: First AI type system ever" (claim troppo forte)

### Corpo del Post (primo commento dell'autore)

Struttura raccomandata in 7 punti:

```
1. Chi siete (1-2 frasi, umane)
2. Una frase: cosa fa il progetto
3. Il problema (perche esiste questo problema?)
4. La vostra storia: perche lo avete costruito
5. La soluzione tecnica (specifici, con dettagli)
6. Il differenziatore (cosa lo rende diverso dai competitor)
7. Invito al feedback: cosa volete imparare dalla community
```

**Tone:** Conversazionale, builder-to-builder. Mai corporate. Mai "leverage", "synergy", "paradigm shift".

**Lunghezza ideale:** 300-500 parole per il primo commento. Abbastanza per dare contesto, non tanto da sembrare un comunicato stampa.

---

## 4. Timing Ottimale

### Dati quantitativi (da Myriade.ai analysis)

| Finestra | Breakout Rate |
|----------|---------------|
| Domenica 0-2 UTC | 15.7% (PICCO ASSOLUTO) |
| Domenica 11-16 UTC | 12-14% |
| Sabato 14-20 UTC | 12-14% |
| Lunedi-Venerdi 11-13 UTC | 10-11% |
| 3-7 UTC qualsiasi giorno | 8.2% (EVITARE) |

**Raccomandazione timing per CervellaSwarm:**
- **Prima scelta:** Domenica tra le 12:00 e 14:00 UTC (8-10 AM EST)
- **Seconda scelta:** Sabato 14:00-16:00 UTC
- **Evitare assolutamente:** Lunedi-Mercoledi ore di punta (troppa concorrenza)

**Nota importante:** C'e un trade-off. Weekend = meno concorrenza = piu facile arrivare in front page. Ore di punta feriale = piu traffico totale ma piu difficile emergere. Per un lancio, weekend e la scelta piu sicura.

### Doppio lancio (strategia avanzata)
Se il primo post non performa, si puo contattare `hn@ycombinator.com` richiedendo il "second-chance pool" - HN lo usa per boostrare post borderline che meritavano piu attenzione.

---

## 5. Errori Comuni - Cosa fa DOWNVOTARE

### Errori fatali (da evitare assolutamente)
1. **Vote rings**: condividere il link diretto a persone chiedendo upvote. HN lo rileva e annulla i voti. Le upvote devono venire da persone che trovano il post organicamente o tramite link al sito principale (non al post HN)
2. **Claims non verificabili**: "world's first", "revolutionary", "nobody has done this before" - la community HN verifica e attacca
3. **Marketing language**: "leverage", "cutting-edge", "game-changing" = downvote immediato
4. **Demo dietro signup/email**: viola le linee guida Show HN ufficiali
5. **Titolo editato dopo il post**: penalizzazione algoritmica
6. **Risposta difensiva alle critiche**: se qualcuno critica, ringraziare prima di difendersi

### Errori medi (riducono performance)
- Post corpo troppo lungo o troppo corto
- Nessuna demo interattiva (solo README/docs)
- Non rispondere ai commenti nelle prime 2-3 ore
- Troppi link interni (sembra spam)
- README con solo feature list, nessuna storia

### Claim pericolosi per CervellaSwarm
Questi claim verranno ATTACCATI se non supportati precisamente:
- "first session type system for AI agents" -> serve citazione accademica che confermo lo stato dell'arte
- "formally verified" -> HN ha molti ricercatori PL, chiederanno dettagli tecnici profondi su Lean 4
- "production ready" -> senza utenti reali, evitare
- "9/9 packages on PyPI" -> OK, e verificabile

---

## 6. Demo Interattiva vs Documentazione

### La risposta netta: DEMO VINCE SEMPRE

Dati dalla ricerca:
- "Show HN is for something you've made that **other people can play with**" (regola ufficiale)
- Projects con demo immediata hanno probabilita di non-upvote del 30% vs 50% per progetti senza demo
- Successi analizzati: TUTTI avevano qualcosa di provabile

### Opzioni demo per CervellaSwarm
1. **pip install + esempio in 3 righe** (minimo accettabile)
2. **Notebook interattivo su Google Colab/Binder** (buono)
3. **Repl.it/Codespaces con codice pre-caricato** (ottimo)
4. **Web playground in-browser** (ideale, ma costa sviluppo)

**Raccomandazione:** Per il lancio attuale, puntare su un Jupyter notebook su Binder o un Colab notebook che mostri la lingua universale in azione. Non serve un sito web elaborato.

---

## 7. Blog Post Separato - Serve o No?

### Pattern dei progetti di successo

Show HN ufficialmente NON accetta blog post, landing page o material di solo lettura. Il post deve linkare a qualcosa di provabile.

**Pattern raccomandato (tre livelli):**
1. **GitHub repo** come home base (il README e la vostra landing page)
2. **Show HN post** che linka al GitHub (NON a un blog post)
3. **Blog post tecnico** come contenuto supplementare da condividere *nei commenti* se rilevante

**Il blog post aiuta DOPO il lancio**, non come sostituto. Nei commenti puoi linkare: "ho scritto un deep-dive tecnico su X qui: [link]"

**Per CervellaSwarm:** Il README di `lingua-universale` o un README generale di progetto e sufficiente come destinazione. Un blog post "From Vibecoding to Vericoding" puo essere condiviso come commento aggiuntivo, non come link principale.

---

## 8. Analisi Competitor Rilevanti su HN

### Progetti simili che hanno postato su HN (2025-2026)

**Show HN: AIP - open protocol for verifying what AI agents are allowed to do**
- Punti: ~1 (pochissimi)
- Perche ha fallito: troppo astratto, nessuna demo, problema non percepito come urgente

**Show HN: An AI agent that audits your entire Python codebase**
- Progetto pyscn-bot
- Demo automatica (PR review), problema concreto e immediato

**Show HN: Formal Verification for Machine Learning Models Using Lean 4** (Marzo 2025)
- Trovato ma punti non accessibili (rate limiting HN)
- La verifica formale per AI e un topic caldo ma di nicchia su HN

**Trend rilevante:** L'articolo di Martin Kleppmann "AI will make formal verification go mainstream" (Dicembre 2025) ha avuto forte engagement su HN. Il termine "vericoding" (LLM che genera codice formalmente verificato) e emerso a Settembre 2025. CervellaSwarm puo cavalcare questa narrativa.

---

## 9. Frasi che Funzionano vs Frasi da Evitare

### FUNZIONANO su HN
- "We built X to solve Y, here's how it works technically"
- "After N months/sessions of work, we're sharing..."
- "We found that [specific observation]. Here's our approach."
- "The core insight is [specific technical insight]"
- "Zero dependencies. Pure stdlib."
- "[X] tests, [Y]% coverage"
- "We were inspired by [academic paper/known concept]"
- "Here's what we got wrong and had to fix"
- "Try it in one command: pip install X"

### DA EVITARE su HN
- "Revolutionary approach to..."
- "We're the first to..."
- "Unlike all other solutions..."
- "This changes everything"
- "Enterprise-grade"
- "Powered by AI" (ovvio nel 2026)
- "Scalable solution"
- "Game-changing"
- Qualsiasi acronimo non spiegato

---

## 10. Raccomandazioni Concrete per CervellaSwarm

### Candidati titolo Show HN (in ordine di forza)

**Opzione A - Focus su verifica formale (angolo piu unico):**
```
Show HN: CervellaSwarm – session types for AI agents with Lean 4 formal proofs
```

**Opzione B - Focus sul problema pratico (piu accessibile):**
```
Show HN: CervellaSwarm – type-check your multi-agent protocols before they deadlock
```

**Opzione C - Focus sul differenziatore vericoding (cavalca trend):**
```
Show HN: cervellaswarm-lingua-universale – formally verified protocols for AI agent swarms
```

**Opzione D - Angolo pragmatico (piu largo):**
```
Show HN: CervellaSwarm – 9 Python packages for building AI agent teams (with formal verification)
```

**Raccomandazione:** Opzione B o C. Opzione B e piu accessibile, C e piu tecnico e preciso. A/B test mentale: quale title faresti click tu stesso come dev?

### Struttura primo commento raccomandata

```
Hi HN,

We've been building CervellaSwarm for about two years – a Python toolkit
for multi-agent AI systems. Today we're sharing what we think is the most
interesting part: cervellaswarm-lingua-universale.

THE PROBLEM: When you have 17 AI agents talking to each other, how do you
know the communication protocols are correct? You mostly don't. You run it,
it deadlocks, you debug it, you fix it. Repeat.

OUR APPROACH: Session types from programming language theory (originally
from Honda et al. 1993). We implemented them in Python + Lean 4 so your
protocols are checked mathematically before runtime. If your protocol can
deadlock, the type checker rejects it.

WHAT IT IS:
- Pure Python, zero dependencies
- 13 modules, 1820 tests, 98% coverage
- Lean 4 bridge: generate formal proofs of your protocols
- DSL inspired by Scribble notation
- Works today with Claude, GPT-4, any LLM-based agent

WHAT MAKES IT DIFFERENT from LangGraph, AutoGen, CrewAI:
Those frameworks coordinate agents. We prove your coordination is correct.
"Vibecoding to vericoding" – not just running agents but verifying them.

Try it:
  pip install cervellaswarm-lingua-universale
  [3-line example]

We have 8 other packages in the suite (code-intelligence, session-memory,
quality-gates, etc.) but lingua-universale is the most academically novel.

What we're most curious about from HN: is formal verification a concern
you have when building multi-agent systems? We're deciding whether to push
harder on the Lean 4 direction for Fase C.
```

### Timeline raccomandata per il lancio

1. **Oggi (Pre-lancio):**
   - Creare Jupyter notebook demo su Google Colab (link pubblico, zero signup)
   - Verificare che `pip install cervellaswarm-lingua-universale` funzioni con esempio 3 righe
   - Scrivere e rivedere il testo del primo commento

2. **GitHub Release (F4.1c):**
   - Fare release formale GitHub prima del Show HN
   - Aggiungere link "Try on Colab" nel README principale

3. **Lancio (F4.1d):**
   - **Domenica mattina, 12:00-14:00 UTC**
   - Postare su HN
   - Nelle prime 2 ore: rispondere a OGNI commento (anche "nice work" merita risposta)
   - Condividere su LinkedIn/Twitter *il link al repo GitHub*, non il link HN diretto

4. **Post-lancio:**
   - Se < 10 punti dopo 2 ore: contattare `hn@ycombinator.com` per second-chance pool
   - Se discussione tecnica: condividere link al blog post "From Vibecoding to Vericoding" nei commenti
   - Monitorare GitHub stars e Issues come segnale di engagement reale

---

## Fonti Consultate

1. [Show HN Official Guidelines](https://news.ycombinator.com/showhn.html)
2. [State of Show HN 2025 - Sturdy Statistics](https://blog.sturdystatistics.com/posts/show_hn/)
3. [State of Show HN: 2025 HN Discussion](https://news.ycombinator.com/item?id=47039478)
4. [Best of Show HN All Time](https://bestofshowhn.com/)
5. [Best of Show HN 2025](https://bestofshowhn.com/2025)
6. [When is it the best time to post on Show HN - Myriade.ai](https://www.myriade.ai/blogs/when-is-it-the-best-time-to-post-on-show-hn)
7. [How to launch a dev tool on Hacker News - Markepear](https://www.markepear.dev/blog/dev-tool-hacker-news-launch)
8. [How to crush your HN launch - DEV Community](https://dev.to/dfarrell/how-to-crush-your-hacker-news-launch-10jk)
9. [How to post on HN without getting flagged - DEV Community](https://dev.to/developuls/how-to-post-on-hacker-news-without-getting-flagged-or-ignored-2eaf)
10. [My Show HN reached front page - Indie Hackers](https://www.indiehackers.com/post/my-show-hn-reached-hacker-news-front-page-here-is-how-you-can-do-it-44c73fbdc6)
11. [How to do a successful HN launch - Lucas Costa](https://lucasfcosta.com/2023/08/21/hn-launch.html)
12. [Best time to post on HN - Simon Hartcher](https://simonhartcher.com/posts/2025-09-10-best-times-to-post-on-hacker-news-according-to-claude/)
13. [Show HN: AIP - agent intent protocol](https://news.ycombinator.com/item?id=47050216)
14. [Show HN: Formal Verification + Lean 4 ML Models](https://news.ycombinator.com/item?id=43454861)
15. [Show HN: Formal Verification via Spectral Geometry Lean 4](https://news.ycombinator.com/item?id=46535363)
16. [Show HN: We proved you can't train hallucinations out of AI](https://news.ycombinator.com/item?id=47061492)
17. [Prediction: AI will make formal verification go mainstream - Kleppmann](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html)
18. [Lean 4: How the theorem prover works - VentureBeat](https://venturebeat.com/ai/lean4-how-the-theorem-prover-works-and-why-its-the-new-competitive-edge-in)
19. [Lean 4 HN discussion](https://news.ycombinator.com/item?id=47047027)
20. [VericoCoding Benchmark arXiv](https://www.arxiv.org/pdf/2509.22908)
21. [Best of Show HN 100 AI Startups](https://bestofshowhn.com/search?q=%5Bai%5D)
22. [Beyond the Front Page - personal guide to HN](https://hsu.cy/2025/09/how-to-read-hn/)
