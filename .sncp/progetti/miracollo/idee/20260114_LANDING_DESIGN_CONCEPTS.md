# LANDING PAGE DESIGN CONCEPTS - Miracollo

> **Data:** 2026-01-14
> **Worker:** Cervella Frontend
> **Riferimento:** MetaMask.io style (minimalista, animazioni eleganti)

---

## PALETTE MIRACOLLO (DA MANTENERE)

```css
--primary: #6366f1        /* Viola/Indigo brand */
--primary-dark: #4f46e5   /* Hover states */
--background: #1a1a2e     /* Dark background */
--card-bg: #25253d        /* Card surfaces */
--text-primary: #ffffff   /* Headings */
--text-secondary: #a0a0b8 /* Body text */
--font-family: 'Outfit'   /* Google Font già in uso */
```

---

## CONCEPT A: STELLA ALPINA PARTICELLARE

### Descrizione Visiva
Una "costellazione" di micro-particelle che formano una sagoma astratta di montagne/stella alpina. Le particelle si muovono leggermente seguendo il mouse (parallax) e pulsano con opacity variabile.

**Hero Section:**
- Background dark con gradiente radiale dal centro (#1a1a2e → più scuro verso bordi)
- ~300-500 particelle bianche/viola chiare
- Al centro: H1 bold "Miracollo" + tagline
- Particelle più vicine al testo si "attirano" leggermente
- Effetto depth: particelle lontane più piccole e meno opache

### Tecnologia Necessaria

**Opzione 1 - CSS Puro (SEMPLICE)**
```
Complessità: ⭐⭐☆☆☆
- Gradient animato (keyframes)
- Pseudo-elementi ::before/::after per forme base
- No JS, performante
Limite: Effetto statico, no interazione mouse
```

**Opzione 2 - JS Leggero (RACCOMANDATO)**
```
Complessità: ⭐⭐⭐☆☆
- Canvas 2D o SVG con <circle>
- Event listener mousemove con throttle
- ~200 righe JS vanilla
Performance: 60fps su desktop, 30fps mobile
```

**Opzione 3 - Three.js (OVERKILL)**
```
Complessità: ⭐⭐⭐⭐⭐
Bundle size: +500kb
Sconsigliato per una landing page
```

### PRO
- Elegante e unico
- Richiama "montagne" (target Cortina/Alleghe)
- Scalabile (riduci particelle su mobile)
- Buon WOW factor

### CONTRO
- Richiede JS per versione interattiva
- Potenziale performance issue su mobile low-end
- Serve fallback statico per no-JS

---

## CONCEPT B: FLOATING GEOMETRY (Bento-Box Style)

### Descrizione Visiva
Design modulare ispirato a MetaMask. 3-4 "card" geometriche (cerchi, quadrati arrotondati) che fluttuano nella hero section con movimento subtile. Ogni card rappresenta una feature (Pricing AI, PMS, Analytics, etc.).

**Hero Section:**
- Background: Gradient verticale (#1a1a2e → #25253d)
- 3 floating cards con:
  - Blur backdrop (backdrop-filter: blur(20px))
  - Border gradient viola
  - Icone SVG animate
  - Testo feature minimale
- Cards si muovono in loop (translate3d)
- Hover: card si espande leggermente (scale 1.05)

### Tecnologia Necessaria

**CSS Puro (POSSIBILE!)**
```
Complessità: ⭐⭐⭐☆☆
- @keyframes per floating animation
- transform: translate3d() per hardware acceleration
- backdrop-filter per glass effect
- :hover transitions
NO JS richiesto per base!
JS opzionale per parallax mouse
```

### PRO
- Moderno e clean
- Mostra subito le feature principali
- CSS-only possibile = performance top
- Responsive facile (stack verticale su mobile)
- Accessibile (no dipendenza JS)

### CONTRO
- Meno "wow" rispetto a particelle
- Backdrop-filter non supportato Safari vecchi (graceful degradation)
- Rischio di sembrare "troppo generico" se non curato bene

---

## CONCEPT C: GRADIENT WAVE (Minimalismo Estremo)

### Descrizione Visiva
Gradiente animato con blur effect che crea "onde" di colore fluide. Stile Stripe/Linear.app. Hero section quasi totalmente tipografica con gradiente che si muove lentamente dietro.

**Hero Section:**
- Background: 3-4 sfere gradient (radial-gradient)
- Colori: viola → indigo → rosa sfumati
- Filter: blur(100px)
- Animation: rotazione lenta (60s) + scale pulsante
- Sopra: H1 gigante + CTA button
- Font weight: 700 per il titolo

### Tecnologia Necessaria

**CSS Puro (SEMPLICISSIMO)**
```
Complessità: ⭐☆☆☆☆
- 2-3 div con position: absolute
- radial-gradient backgrounds
- @keyframes per animazione
- filter: blur()
ZERO JS richiesto!
Performance: nativa, GPU-accelerated
```

### PRO
- Implementazione VELOCISSIMA (2-3 ore)
- Performance eccezionale
- Look moderno e premium
- Zero manutenzione
- Accessibilità perfetta

### CONTRO
- Meno distintivo (molti siti lo usano)
- Nessun elemento interattivo
- Non comunica visivamente "hotel/montagna"
- Può sembrare "troppo astratto" per alcuni

---

## CONCEPT D: SCROLL-TRIGGERED REVEAL (Mix dei 3)

### Descrizione Visiva
Combina elementi dei concept precedenti con focus su scroll-driven animations (trend 2026). Hero section minimalista, poi sezioni successive con reveal effects orchestrati.

**Hero Section (Minimale):**
- Background gradient wave (Concept C) - SEMPLICE
- Titolo + tagline + CTA
- Scroll indicator animato

**Sezioni Successive (Progressive Enhancement):**
1. **Features Bento** - 4 card che appaiono stagger (Concept B)
2. **Demo Screenshot** - Con parallax leggero
3. **Stats/Social Proof** - Numeri che contano su scroll-in-view
4. **Pricing Teaser** - Card minimale
5. **Footer** - Con mini-mappa località servite

### Tecnologia Necessaria

```
Complessità: ⭐⭐⭐⭐☆
- CSS per layout e base animations
- JS Intersection Observer per scroll triggers
- CountUp.js per numeri (opzionale, 5kb)
- Scroll-driven animations API (experimental, fallback CSS)
Effort: 2-3 giorni implementazione completa
```

### PRO
- Storytelling efficace (guided experience)
- Performance controllata (lazy animations)
- SEO-friendly (content above fold)
- Bilanciamento wow/usabilità

### CONTRO
- Più complesso da mantenere
- Richiede testing cross-browser attento
- Rischio di "troppe animazioni" se non calibrato

---

## RACCOMANDAZIONE FINALE

### Per Launch Rapido (1-2 giorni):
**CONCEPT C (Gradient Wave) + CONCEPT B (Bento Cards)**

```
HERO:     Gradient animato CSS-only
FEATURES: 3-4 bento cards statiche (no float animation)
DEMO:     Screenshot statico con shadow
CTA:      Button gradient con hover glow
FOOTER:   Minimale
```

**Effort:** 8-12 ore
**Performance:** 100/100 Lighthouse
**WOW Factor:** 7/10 (elegante ma safe)

---

### Per Massimo Impatto (1 settimana):
**CONCEPT D (Scroll-Driven Experience)**

```
HERO:     Gradient wave
FEATURES: Floating bento cards (JS parallax)
DEMO:     Video/GIF in-view autoplay
STATS:    CountUp animation
PRICING:  Card interattiva
FOOTER:   Rich con links
```

**Effort:** 40-50 ore
**Performance:** 95/100 Lighthouse
**WOW Factor:** 9/10 (premium look)

---

## STRUTTURA PAGINA CONSIGLIATA

```html
<section id="hero">           <!-- 100vh, gradient animato -->
  <h1>Miracollo</h1>
  <p>Il PMS che pensa come te</p>
  <button>Prova Gratis</button>
</section>

<section id="problem">        <!-- White text, dark bg -->
  "Gestire prezzi è complesso..."
</section>

<section id="solution">       <!-- Bento grid 2x2 -->
  <Card>Pricing AI</Card>
  <Card>PMS Nativo</Card>
  <Card>Meteo Real-time</Card>
  <Card>Eventi Locali</Card>
</section>

<section id="demo">           <!-- Screenshot/Video -->
  <img src="rateboard.png" />
</section>

<section id="proof">          <!-- Stats -->
  <Stat>+15% Revenue</Stat>
  <Stat>-80% Tempo</Stat>
</section>

<section id="cta">            <!-- Final push -->
  <h2>Pronto a iniziare?</h2>
  <button>Richiedi Demo</button>
</section>

<footer>                      <!-- Links + Legal -->
  <Links />
  <Social />
  <Copyright />
</footer>
```

---

## PROSSIMI STEP

1. **Rafa decide** quale concept (o mix)
2. **Cervella Frontend** crea wireframe HTML/CSS base
3. **Test responsive** (mobile-first!)
4. **Animazioni** (progressive enhancement)
5. **Deploy** su staging per review

---

## INSPIRATION LINKS (da verificare)

```
MetaMask:     https://metamask.io
Stripe:       https://stripe.com
Linear:       https://linear.app
Vercel:       https://vercel.com
Framer:       https://framer.com
```

---

*"Il design impone rispetto. Ogni pixel conta."*
*Cervella Frontend - 14 Gennaio 2026*
