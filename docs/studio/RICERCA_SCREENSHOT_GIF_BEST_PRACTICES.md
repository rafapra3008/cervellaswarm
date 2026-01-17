# Best Practices Screenshot/GIF per Launch CervellaSwarm su Hacker News

**Data ricerca:** 17 Gennaio 2026
**Obiettivo:** Show HN Martedi 21 Gennaio
**Target:** Developer che cercano AI coding tools

---

## TL;DR - Le Regole d'Oro

```
FORMAT:      GIF animate (non video) per README/Show HN
DURATA:      Max 6 secondi (ideale 3-4 secondi)
DIMENSIONI:  1200x630 per header, 1270x760 per gallery
FILE SIZE:   < 3MB (ideale < 1MB)
FRAME RATE:  15-24fps (ottimale 15fps @ 540p)
TOOL:        VHS (Charmbracelet) - scriptabile e ripetibile
MOMENTI:     "Delegating work" non "typing fast"
```

---

## 1. GIF vs Video - La Scelta

### Usa GIF quando (il nostro caso!)

- Launch su Show HN / Product Hunt
- Demo veloce e comprensibile a colpo d'occhio
- Embedding in README GitHub
- Condivisione social
- File size piccolo e caricamento immediato

### Usa Video quando

- Tutorial dettagliati > 15 secondi
- Necessita seeking/pause
- Spiegazioni complesse

**Decisione:** GIF per Show HN, eventualmente video su YouTube per deep dive.

---

## 2. Specifiche Tecniche

### Dimensioni Ottimali

| Piattaforma | Dimensioni | Note |
|-------------|-----------|------|
| **Product Hunt Header** | 1200x630 | JPG/PNG/GIF |
| **Product Hunt Gallery** | 1270x760 | 2+ immagini richieste |
| **GitHub README** | 1200x600 | Max width leggibile |
| **Show HN inline** | 800-1200px wide | Responsive |

### File Size & Optimization

**Target:**
- Ideale: < 1MB
- Max accettabile: 3MB
- Email/mobile: < 200KB

**Ottimizzazione (dopo creazione):**
```bash
# Gifsicle compression
gifsicle --lossy=80 --colors=256 input.gif -o output.gif

# Oppure online
https://gifcompressor.com
https://ezgif.com/optimize
```

### Frame Rate & Durata

| Tipo Demo | Durata | FPS | Note |
|-----------|--------|-----|------|
| **Quick feature** | 3-4 sec | 15 | Perfetto per Show HN |
| **Tutorial** | 4-6 sec | 15-24 | Max consigliato |
| **Email** | 2-3 sec | 12 | Ultra compressed |

**Limite massimo:** 6 secondi (15 secondi hard limit tecnico)

---

## 3. Tool Consigliato: VHS (Charmbracelet)

**Perche VHS e non altri?**
- Scriptabile (.tape files) = ripetibile
- Output GIF, MP4, WebM
- Dimensioni ottime (22KB-223KB se ottimizzato)
- Golden files per integration testing
- Publish gratuito su vhs.charm.sh

### Esempio .tape file

```tape
# Setup
Set Width 1200
Set Height 600
Set FontSize 46

# Demo
Type "cervella spawn-workers --list"
Sleep 500ms
Enter
Sleep 2s

Type "cervella spawn-workers --researcher"
Sleep 500ms
Enter
Sleep 3s

# Output
Output demo.gif
```

### Pubblicazione

```bash
vhs publish demo.gif
# Ti da link per condivisione browser/HTML/Markdown
```

**Alternativa:** asciinema + agg (se preferisci cast interattivi)

---

## 4. Cosa Mostrare nei Demo - AI Coding Tools

### Cosa Funziona (da esempi Aider, Claude Code, Cursor)

**1. Delegating Work (non typing fast!)**
```
❌ "Guarda che veloce scrivo codice"
✅ "Guarda come delego task complessi"
```

**2. Context Awareness**
- AI che mappa codebase
- Capisce architettura esistente
- Trova file corretti automaticamente

**3. Workflow Reale**
- Problema reale, non toy example
- Come un dev senior userebbe il tool
- "Un'ora di lavoro da un paragrafo di istruzioni"

**4. Git Integration**
- Commit intelligenti
- Diff chiari
- Rollback facili

**5. Voice/Multi-Modal (se applicabile)**
- Screenshot to code
- Voice commands
- Natural language → action

### Esempi Concreti per CervellaSwarm

**Demo 1: Spawn & Delegate (3-4 sec)**
```
1. cervella spawn-workers --list
   → Mostra 16 agenti disponibili

2. cervella spawn-workers --researcher
   → Worker spawna, esegue task

3. Output salvato in .swarm/tasks/
   → Risultato pronto
```

**Demo 2: Multi-Agent Coordination (4-5 sec)**
```
1. Task complesso ricevuto
2. Regina mappa task → 3 worker
3. Worker lavorano in parallelo
4. Output merge automatico
5. Regina verifica qualita
```

**Demo 3: SNCP Memory (3 sec)**
```
1. Sessione nuova, context vuoto
2. Read PROMPT_RIPRESA
3. Agente "ricorda tutto"
4. Continua lavoro senza re-spiegare
```

---

## 5. Errori Comuni da Evitare

### Da discussioni Hacker News

**1. GIF Troppo Lunghi**
- Limite Google Slides: 1000 frame
- Attenzione frame rate alto + durata lunga
- **Fix:** Max 6 secondi @ 15fps = 90 frame

**2. File Troppo Pesanti**
- GIF unoptimized = 1.2MB+
- **Fix:** Compress con gifsicle/gifcompressor

**3. Testo Illegibile**
- Font troppo piccolo
- Colori bassi contrasto
- **Fix:** FontSize 40-46px, high contrast theme

**4. Strobing/Quick Cuts**
- Product Hunt rifiuta GIF con strobing
- Troppi cut confondono
- **Fix:** Transizioni smooth, pause strategiche

**5. Troppo Tecnico Troppo Presto**
- Dev vogliono capire COSA, non COME (subito)
- **Fix:** Prima "what it does", poi "how it works"

**6. Mancanza One-Click Demo**
- "Offering a one-click demo" aumenta upvote
- **Fix:** Link a playground/quickstart chiaro

---

## 6. Strategia Screenshot Show HN

### Set Minimo Necessario

**1. Hero GIF (1200x600, < 1MB)**
- Prima cosa che vedono
- "Wow factor" immediato
- Mostra value proposition in 3 secondi

**2. Gallery Screenshots (1270x760)**
- Feature 1: Spawn workers
- Feature 2: Task coordination
- Feature 3: SNCP memory context

**3. Architecture Diagram (statico)**
- Come funziona sistema
- 16 agenti + Regina
- Input → Processing → Output

### Ordine Racconto

```
1. PROBLEMA
   → "AI coding tools perdono contesto ogni sessione"

2. SOLUZIONE
   → "CervellaSwarm: 16 specialist agents + external memory"

3. DEMO
   → GIF mostra spawn worker che risolve task

4. RISULTATO
   → Output salvato, contesto preservato, zero re-explain

5. CALL TO ACTION
   → "Try it: npm install -g cervellaswarm"
```

---

## 7. Best Practices da Successful Show HN

### Da "How to do successful HN launch"

**Timing:**
- Martedi-Giovedi mattina (US time)
- 8-10am EST ideale
- Evita weekend/holidays

**Titolo:**
```
✅ "Show HN: CervellaSwarm – 16 AI Agents that Don't Forget Context"
❌ "Show HN: My New AI Tool"
```

**Engagement:**
- Rispondi OGNI commento
- Discussione interessante = piu upvote
- Sii umile, accetta feedback

**Demo Access:**
- One-click install
- Quick start < 2 minuti
- Fallback video se install problemi

**Visual Content:**
- Post con immagini performano meglio
- GIF > screenshot statico
- Ma screenshot statico > niente

---

## 8. Checklist Pre-Launch

### GIF/Screenshot

- [ ] Hero GIF < 1MB, 3-4 secondi, mostra value prop
- [ ] 2-3 gallery screenshot features chiave
- [ ] Architecture diagram (optional ma consigliato)
- [ ] Tutti i file verificati su mobile/desktop
- [ ] Compressione ottimizzata (gifsicle)
- [ ] Testo leggibile anche su mobile

### README GitHub

- [ ] GIF hero in cima (subito dopo titolo)
- [ ] One-liner value proposition
- [ ] Quick install command visibile
- [ ] Screenshots features embedded
- [ ] Link a demo/playground se disponibile

### Product Hunt (se facciamo)

- [ ] Header image 1200x630
- [ ] Gallery 2+ immagini 1270x760
- [ ] Thumbnail logo 240x240
- [ ] NO strobing effects
- [ ] Tutti GIF < 3MB

### Show HN Post

- [ ] Titolo chiaro "Show HN: CervellaSwarm – [value prop]"
- [ ] Link al repo GitHub
- [ ] README con GIF visibili
- [ ] Rafa pronto a rispondere commenti
- [ ] Quick start funzionante e testato

---

## 9. Tools & Resources

### Recording

- **VHS** (consigliato): https://github.com/charmbracelet/vhs
- **asciinema + agg**: https://docs.asciinema.org/getting-started/
- **Terminalizer**: https://www.terminalizer.com/

### Optimization

- **Gifsicle**: https://www.lcdf.org/gifsicle/
- **Online compressor**: https://gifcompressor.com
- **ezgif optimizer**: https://ezgif.com/optimize

### Hosting

- **VHS publish**: vhs.charm.sh (gratis)
- **GitHub**: Direttamente nel repo
- **ImgBB / Imgur**: Backup hosting

### Testing

- **Mobile preview**: Usa browser dev tools
- **File size check**: `ls -lh demo.gif`
- **Frame count**: `gifsicle --info demo.gif`

---

## 10. Template VHS per CervellaSwarm

### demo_spawn.tape

```tape
# Cervella Demo: Spawn Worker

Set Shell "bash"
Set Width 1200
Set Height 600
Set FontSize 42
Set Theme "Dracula"

# Intro
Type "# CervellaSwarm: 16 AI Agents that Remember Everything"
Sleep 1s
Enter
Sleep 500ms

# Show available workers
Type "cervella spawn-workers --list"
Sleep 500ms
Enter
Sleep 2s

# Spawn researcher
Type "cervella spawn-workers --researcher"
Sleep 500ms
Enter
Sleep 2s

# Show output
Type "cat .swarm/tasks/TASK_001_OUTPUT.md"
Sleep 500ms
Enter
Sleep 2s

Output demo_spawn.gif
```

### demo_memory.tape

```tape
# Cervella Demo: Context Memory

Set Shell "bash"
Set Width 1200
Set Height 600
Set FontSize 42
Set Theme "Dracula"

# Intro
Type "# New session, zero context in memory"
Sleep 1s
Enter
Sleep 500ms

# Read PROMPT_RIPRESA
Type "cervella read-memory miracollo"
Sleep 500ms
Enter
Sleep 2s

# Agent remembers everything
Type "# Agent knows: last 3 sprints, decisions, next steps"
Sleep 2s
Enter

Output demo_memory.gif
```

---

## Fonti & Riferimenti

**Show HN Best Practices:**
- [How to do a successful Hacker News launch](https://lucasfcosta.com/2023/08/21/hn-launch.html)
- [My Show HN reached front page](https://www.indiehackers.com/post/my-show-hn-reached-hacker-news-front-page-here-is-how-you-can-do-it-44c73fbdc6)
- [Best of Show HN - CLI Tools](https://bestofshowhn.com/search?q=cli)

**Terminal Recording:**
- [VHS - CLI Home Video Recorder](https://github.com/charmbracelet/vhs)
- [How to capture terminal to GIFs](https://news.ycombinator.com/item?id=25234750)
- [asciinema Getting Started](https://docs.asciinema.org/getting-started/)
- [Terminal Recorders Comprehensive Guide](https://intoli.com/blog/terminal-recorders/)

**GIF Optimization:**
- [Animated GIF Best Practices](https://www.svgator.com/blog/animated-gif-best-practices-to-optimize-gifs-like-pros/)
- [GIF Frame Rate & Duration Best Practices](https://fastmakergif.com/blog/gif-frame-rate-duration-best-practices)
- [How To Optimize GIFs on Command Line](https://www.digitalocean.com/community/tutorials/how-to-make-and-optimize-gifs-on-the-command-line)

**Product Hunt Guidelines:**
- [Product Hunt Gallery Images](https://www.producthunt.com/launch/preparing-for-launch)
- [Ultimate Product Hunt Launch Guide](https://www.scalenut.com/blogs/master-your-product-hunt-launch-a-guide-to-becoming-1)

**AI Coding Tools Examples:**
- [Aider - AI Pair Programming](https://github.com/Aider-AI/aider)
- [How I use Claude Code](https://www.builder.io/blog/claude-code)
- [Ask HN: Best AI Code Assistant?](https://news.ycombinator.com/item?id=41819039)

---

## Prossimi Step Consigliati

1. **Installare VHS**
   ```bash
   brew install vhs
   ```

2. **Creare 3 .tape files**
   - demo_spawn.tape (spawn worker)
   - demo_memory.tape (SNCP context)
   - demo_coordination.tape (multi-agent)

3. **Generare GIF**
   ```bash
   vhs demo_spawn.tape
   vhs demo_memory.tape
   vhs demo_coordination.tape
   ```

4. **Ottimizzare**
   ```bash
   gifsicle --lossy=80 --colors=256 demo_spawn.gif -o demo_spawn_opt.gif
   ```

5. **Testare**
   - Verificare leggibilita mobile
   - Check file size < 1MB
   - Preview su GitHub README mock

6. **Pubblicare**
   ```bash
   vhs publish demo_spawn_opt.gif
   ```

---

**Raccomandazione finale:**

Per Show HN Martedi 21:
- **1 Hero GIF** (spawn + execute task) - 3-4 secondi
- **2 Screenshot** (architecture + features) - statici
- **README chiaro** con quick install in cima

Meno e meglio. Un GIF perfetto > tre GIF mediocri.

Focus su "delegating work to specialized agents" piu che su technical details.
Developer vogliono vedere VALUE, non implementation.

---

**Status:** Ricerca completata
**File verificato:** 2026-01-17
**Next:** Creare .tape files e generare GIF
