# SUBROADMAP - Landing Page Professionale

> **Creata:** 18 Gennaio 2026 - Sessione 258
> **Obiettivo:** Da 6.5/10 → 9/10 (Show HN Ready)
> **Timeline:** 3-5 giorni
> **Analisi base:** `.sncp/progetti/cervellaswarm/ANALISI_LANDING_CRITICA.md`

---

## RECAP SITUAZIONE

```
+================================================+
|  LANDING PAGE ATTUALE                          |
|                                                |
|  Score: 6.5/10 (FUNZIONALE, non PROFESSIONALE) |
|  File: /landing/index.html                     |
|  Tech: Tailwind CSS, single file               |
|  Status: NON deployata                         |
+================================================+
```

### Cosa c'è di BUONO
- Value proposition forte ("16 Specialized AI Agents")
- Privacy-first messaging ("Your code stays local")
- Pricing trasparente con Free tier
- Design pulito, dark mode

### Cosa MANCA (critico)
- Demo visiva (video/GIF) - zero visuale del prodotto
- Trust signals (testimonial, social proof)
- CTA ottimizzati (confusi e generici)
- Footer links morti

### Cosa è DATATO
- Emoji come unico visual
- Early bird banner confuso
- Design senza micro-animazioni

---

## FASI LAVORO

### FASE 1: QUICK WINS (4 ore)
**Chi:** cervella-frontend
**Effort:** LOW | **Impact:** ALTO

- [ ] Fix footer links (remove "#" o add pagine)
- [ ] Ottimizza CTA copy ("Install CLI in 60 seconds")
- [ ] Mobile touch targets (44px minimum)
- [ ] Remove/fix early bird banner confuso
- [ ] Add micro-copy sotto CTA ("No signup required")

### FASE 2: CONTENUTI (1 giorno)
**Chi:** cervella-marketing + backend
**Effort:** MED | **Impact:** ALTO

- [ ] Aggiorna comparison table (dati corretti 2026)
- [ ] Expand feature descriptions (3-5 righe cadauna)
- [ ] Add FAQ preview (top 3 domande)
- [ ] Add "npm install" snippet visibile
- [ ] Verifica pricing allineato a Stripe

### FASE 3: DEMO VISIVA (2 giorni)
**Chi:** Da decidere
**Effort:** HIGH | **Impact:** ALTISSIMO

Opzioni:
- [ ] **A) GIF animata** - Screen recording + editing
- [ ] **B) Video 60s** - Più professionale ma più effort
- [ ] **C) Screenshot statici** - Minimo effort, ok per MVP

Contenuto demo:
- Regina che coordina task
- Worker che risponde
- Guardiana che valida
- Output finale

### FASE 4: POLISH DESIGN (1-2 giorni)
**Chi:** cervella-frontend
**Effort:** MED | **Impact:** MEDIO

- [ ] Animated gradient background
- [ ] Scroll-triggered fade-in cards
- [ ] Hover states con micro-interactions
- [ ] Replace emoji con icon set (Lucide/Heroicons)
- [ ] Glassmorphism sui box feature

### FASE 5: TRUST SIGNALS (quando disponibili)
**Chi:** cervella-marketing
**Effort:** MED | **Impact:** ALTO

- [ ] Counter utenti (se >100)
- [ ] Quote beta tester (se ci sono)
- [ ] "Listed on mcp-ai.org" badge
- [ ] "MCP Dev Summit 2026" mention (se accettato)

### FASE 6: DEPLOY (1 ora)
**Chi:** cervella-devops
**Effort:** LOW | **Impact:** CRITICO

- [ ] Deploy su Vercel/Netlify
- [ ] Configura cervellaswarm.com
- [ ] SSL certificato
- [ ] Test mobile

---

## DECISIONI DA PRENDERE

| Domanda | Opzioni | Note |
|---------|---------|------|
| Demo format? | GIF / Video / Screenshot | GIF = balance effort/impact |
| Early bird banner? | Keep / Remove | Crea confusione pricing |
| Emoji? | Keep some / Replace all | Keep 👸 come signature |
| Testimonial? | Wait real / Use internal | Aspettare HN feedback |

---

## TIMELINE PROPOSTA

```
GEN 18 (OGGI)
  └── Decisioni + Quick Wins

GEN 19
  └── FASE 1 completata
  └── FASE 2 iniziata

GEN 20
  └── FASE 2 completata
  └── FASE 3 iniziata (demo)

GEN 21-22
  └── FASE 3 completata
  └── FASE 4 (polish)

GEN 23
  └── FASE 6: DEPLOY
  └── Test finale

GEN 24-25
  └── Show HN LAUNCH!
```

---

## METRICS TARGET

| Metrica | Attuale | Target |
|---------|---------|--------|
| Score design | 6.5/10 | 9/10 |
| Mobile usability | OK | Ottimo |
| CTA clarity | Confuso | Chiaro |
| Trust signals | 0 | 3+ |
| Demo visiva | 0 | 1+ |

---

## FILE CORRELATI

| File | Cosa |
|------|------|
| `/landing/index.html` | Landing attuale |
| `ANALISI_LANDING_CRITICA.md` | Analisi completa |
| `docs/BOZZA_SHOW_HN.md` | Post HN |
| `docs/BOZZA_TWEET_LANCIO.md` | Tweet |

---

*"Il design impone rispetto. Quando guardano vedono che è una cosa seria."*
