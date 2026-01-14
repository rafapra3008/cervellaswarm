# ROADMAP LANDING PAGE - Miracollo

> **Data:** 14 Gennaio 2026
> **Obiettivo:** Landing che SPACCA!
> **Approccio:** Una cosa alla volta, fino al 100000%

---

## VISIONE FINALE

```
+================================================================+
|                                                                |
|   LANDING MIRACOLLO = STELLA ALPINA + BENTO + SCROLL MAGIC     |
|                                                                |
|   Hero:     Particelle che formano montagne/stelle             |
|   Features: Bento cards stile MetaMask                         |
|   Demo:     Screenshot con parallax                            |
|   Stats:    Numeri che contano on scroll                       |
|   CTA:      Finale con glow effect                             |
|                                                                |
|   UNICO nel mercato RMS - nessuno ha una landing cosi!         |
|                                                                |
+================================================================+
```

---

## FASI DI IMPLEMENTAZIONE

### FASE 1: SETUP BASE (4-6h)
**Status:** [ ] TODO

```
TASK:
1. [ ] Creare nuovo index.html pulito
2. [ ] Setup CSS variables (colori Miracollo)
3. [ ] Import font Outfit
4. [ ] Struttura HTML semantica (sections)
5. [ ] Reset CSS + base styles
6. [ ] Mobile-first grid system

OUTPUT:
- frontend/index.html (nuovo, pulito)
- frontend/css/landing.css (o inline)

WORKER: cervella-frontend
```

---

### FASE 2: HERO STELLA ALPINA (8-12h)
**Status:** [ ] TODO

```
TASK:
1. [ ] Canvas setup per particelle
2. [ ] Algoritmo generazione particelle
3. [ ] Movimento parallax mouse
4. [ ] Formazione "montagna" astratta
5. [ ] Gradient background animato
6. [ ] H1 + tagline + CTA button
7. [ ] Scroll indicator animato
8. [ ] Fallback no-JS (gradient statico)

TECNICA:
- Canvas 2D (performante)
- ~300 particelle bianche/viola
- Mouse parallax con throttle
- requestAnimationFrame per 60fps

OUTPUT:
- frontend/js/particles.js
- Hero section completa

WORKER: cervella-frontend
```

---

### FASE 3: BENTO CARDS FEATURES (6-8h)
**Status:** [ ] TODO

```
TASK:
1. [ ] Grid layout 2x2 (desktop) / 1 col (mobile)
2. [ ] Card component con glass effect
3. [ ] Icone SVG per ogni feature
4. [ ] Hover animation (scale + glow)
5. [ ] Scroll-in animation (fade + slide)

CARDS:
1. AI Trasparente - "Ti spiega PERCHE"
2. PMS Nativo - "Tutto in uno"
3. Meteo Real-time - "Anticipa la domanda"
4. Eventi Locali - "Sempre aggiornato"

COPY: Da LANDING_STRATEGY.md

OUTPUT:
- Sezione #features completa

WORKER: cervella-frontend
```

---

### FASE 4: SEZIONI SCROLL-DRIVEN (8-10h)
**Status:** [ ] TODO

```
TASK:
1. [ ] Intersection Observer setup
2. [ ] Sezione "Il Problema" (text reveal)
3. [ ] Sezione "Demo" (screenshot + shadow)
4. [ ] Sezione "Stats" (counter animation)
5. [ ] Sezione "CTA Finale" (glow button)
6. [ ] Footer minimale

ANIMAZIONI:
- Fade-in on scroll (0.3s ease)
- Stagger delay per elementi
- Counter 0 → numero (1.5s)

OUTPUT:
- Sezioni complete con animazioni

WORKER: cervella-frontend
```

---

### FASE 5: MOBILE + TESTING (4-6h)
**Status:** [ ] TODO

```
TASK:
1. [ ] Responsive breakpoints (768px, 480px)
2. [ ] Touch-friendly targets (44px min)
3. [ ] Particelle ridotte su mobile
4. [ ] Test Chrome, Safari, Firefox
5. [ ] Test iOS Safari, Android Chrome
6. [ ] Lighthouse audit (target 90+)
7. [ ] Accessibilita base (WCAG AA)

OUTPUT:
- Landing responsive completa
- Test report

WORKER: cervella-frontend + cervella-tester
```

---

### FASE 6: DEPLOY + REVIEW (2-4h)
**Status:** [ ] TODO

```
TASK:
1. [ ] Meta tags SEO
2. [ ] OG image (1200x630)
3. [ ] Favicon set
4. [ ] Deploy staging
5. [ ] Review con Rafa
6. [ ] Fix feedback
7. [ ] Deploy production

OUTPUT:
- Landing LIVE su miracollo.com

WORKER: cervella-devops
```

---

## EFFORT TOTALE

| Fase | Ore | Giorni (~4h/giorno) |
|------|-----|---------------------|
| 1. Setup | 4-6h | 1-2 giorni |
| 2. Hero | 8-12h | 2-3 giorni |
| 3. Bento | 6-8h | 2 giorni |
| 4. Scroll | 8-10h | 2-3 giorni |
| 5. Mobile | 4-6h | 1-2 giorni |
| 6. Deploy | 2-4h | 1 giorno |
| **TOTALE** | **32-46h** | **9-13 giorni** |

---

## ASSETS NECESSARI

```
IMMAGINI:
- [ ] Logo Miracollo (gia esistente)
- [ ] OG Image (da creare)
- [ ] Screenshot RateBoard (da catturare)
- [ ] Screenshot Weather Widget (da catturare)

ICONE (SVG):
- [ ] Brain/AI icon
- [ ] Building/Hotel icon
- [ ] Weather icon
- [ ] Calendar/Events icon
- [ ] Chart/Growth icon

FONT:
- [x] Outfit (gia in uso)
```

---

## COPY FINALE (da LANDING_STRATEGY.md)

### Hero
```
H1: "Revenue Management con AI
     che capisce il tuo hotel"

Sub: Il primo PMS con AI trasparente per piccoli hotel.
     Prezzi ottimali. Zero sorprese. Controllo totale.

CTA: "Inizia prova gratuita"
     (30 giorni, nessuna carta richiesta)
```

### Bento Cards
```
CARD 1 - AI Trasparente:
"Ogni suggerimento di prezzo viene spiegato:
meteo, eventi locali, storico prenotazioni.
Tu decidi, l'AI consiglia."

CARD 2 - PMS Nativo:
"PMS completo + Revenue Management.
Nessuna integrazione da gestire,
nessun dato da sincronizzare."

CARD 3 - Meteo Real-time:
"Neve in arrivo? Concerto in citta?
Miracollo regola i prezzi in tempo reale."

CARD 4 - Eventi Locali:
"Olimpiadi, Coppa del Mondo, festival locali.
L'AI li conosce tutti."
```

### CTA Finale
```
H2: "Pronto a iniziare?"

Trust signals:
- 30 giorni di prova gratuita
- Nessuna carta di credito richiesta
- Setup in 10 minuti
- Supporto in italiano

Button: "Inizia la tua prova gratuita"
```

---

## CHECKPOINT GIORNALIERI

```
GIORNO 1: Fase 1 completa (setup base)
GIORNO 2-3: Fase 2 (hero particelle)
GIORNO 4-5: Fase 3 (bento cards)
GIORNO 6-7: Fase 4 (scroll sections)
GIORNO 8-9: Fase 5 (mobile + test)
GIORNO 10: Fase 6 (deploy + review)
```

---

## NOTE

- Ogni fase = commit git
- Screenshot per SNCP dopo ogni fase
- Review con Rafa dopo Fase 2 (hero e il cuore)
- Mobile-first sempre!

---

*"Ultrapassar os próprios limites!"*
*"Fatto BENE > Fatto VELOCE"*
*"Una cosa alla volta, fino al 100000%!"*

*Roadmap creata: 14 Gennaio 2026*
