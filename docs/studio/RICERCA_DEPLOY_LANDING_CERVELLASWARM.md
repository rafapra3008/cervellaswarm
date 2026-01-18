# RICERCA: Opzioni Deploy Landing Page CervellaSwarm

> **Ricercatrice:** Cervella Researcher
> **Data:** 18 Gennaio 2026
> **Contesto:** Landing page statica per SHOW HN (24-25 Gennaio)
> **Versione:** 1.0

---

## EXECUTIVE SUMMARY

**Raccomandazione:** Cloudflare Pages
**Motivazione:** Gratuito, illimitato, performance eccellenti, zero configurazione, GitHub integration nativa
**Alternativa:** Vercel (se servono feature premium future)
**Costo mensile stimato:** $0 (con Cloudflare Pages)

**TL;DR per Rafa:**
```
Cloudflare Pages = scelta OVVIA
- FREE per sempre (non "free trial")
- UNLIMITED bandwidth (non 100GB come Vercel)
- CDN globale 300+ edge locations
- Deploy automatico da GitHub
- SSL automatico
- Custom domain gratis
- Zero configurazione
- Performance top-tier

È quello che usano i big player.
```

---

## CONTESTO PROGETTO

### Caratteristiche Landing Page

| Caratteristica | Dettaglio |
|----------------|-----------|
| **Tipo** | Statica pura (HTML/CSS/JS) |
| **Pagine** | 4 (index, how-it-works, faq, getting-started) |
| **Asset** | 1 immagine OG (58KB), Tailwind CDN |
| **Dominio** | cervellaswarm.com (da configurare) |
| **Backend** | Separato su Fly.io (cervellaswarm-api.fly.dev) |
| **Target traffico** | ~10k visite/mese iniziali (SHOW HN) |
| **Pubblico** | Dev professionisti |

### Requisiti Non-Negoziabili

- ✅ SSL/HTTPS automatico
- ✅ Custom domain support
- ✅ Deploy automatico da GitHub
- ✅ Performance globale (CDN)
- ✅ Zero downtime
- ✅ Costi prevedibili

### Requisiti Nice-to-Have

- 🎯 Analytics privacy-friendly
- 🎯 Preview deployments (per PR)
- 🎯 Rollback facile
- 🎯 Edge locations globali

---

## ANALISI OPZIONI

### 1. CLOUDFLARE PAGES ⭐⭐⭐⭐⭐

**Status:** RACCOMANDAZIONE PRIMARIA

#### Pricing

| Caratteristica | Free Tier | Limite |
|----------------|-----------|--------|
| **Bandwidth** | UNLIMITED | ∞ |
| **Requests** | UNLIMITED | ∞ |
| **Build minutes** | 500/mese | OK per noi |
| **Custom domains** | 100/progetto | OK |
| **Sites** | UNLIMITED | ∞ |
| **Costo mensile** | **$0** | - |

**Overage:** NON esistono overage su Free - tutto unlimited!

#### Performance

- **CDN:** 300+ edge locations globali
- **Latency:** Best-in-class (dati 2026)
- **Cold starts:** N/A (static)
- **DDoS protection:** Incluso (industry-leading)
- **Uptime:** 99.99%+ (rete Cloudflare)

#### Features

| Feature | Supporto | Note |
|---------|----------|------|
| SSL/HTTPS | ✅ Automatico | Let's Encrypt, auto-renewal |
| Custom Domain | ✅ Gratis | Illimitati |
| GitHub Integration | ✅ Nativo | Push → deploy automatico |
| Preview Deployments | ✅ | Per ogni PR |
| Rollback | ✅ | 1-click |
| CI/CD | ✅ | GitHub Actions o nativo |
| Analytics | ✅ | Web Analytics gratis |
| Edge Functions | ✅ | Se serve in futuro |

#### Setup Complexity

**Difficoltà:** 1/10 (triviale)

```bash
# Procedura
1. Connetti repo GitHub a Cloudflare Pages
2. Cloudflare auto-detecta static site
3. Push → deploy automatico
4. Configura custom domain (DNS CNAME)
5. Done!

Tempo stimato: 10 minuti
```

#### Pro

```
✅ UNLIMITED bandwidth (vs 100GB Vercel)
✅ UNLIMITED requests
✅ FREE per sempre (non trial)
✅ Performance ECCELLENTI (300+ edge locations)
✅ Zero configurazione
✅ DDoS protection incluso
✅ Web Analytics privacy-first incluso
✅ Preview deployments automatici
✅ Rollback 1-click
✅ SSL automatico + renewal
✅ Nessun vendor lock-in (static files)
✅ Usato da big player (Shopify, Discord, etc)
```

#### Contro

```
❌ Build speed non sempre consistente (vs Vercel)
   → Non critico per noi (build ogni deploy, non runtime)
❌ Dashboard meno "sexy" di Vercel
   → Non rilevante per noi
```

#### Affidabilità

- **Uptime storico:** 99.99%+ (Cloudflare network)
- **Incident history:** Rarissimi, risolti velocemente
- **SLA:** No SLA formale su free (ma performance eccellenti)

#### Fonti

- [Cloudflare Pages Free Tier](https://www.freetiers.com/directory/cloudflare-pages)
- [Cloudflare Pages Limits](https://developers.cloudflare.com/pages/platform/limits/)
- [Cloudflare Pages Custom Domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [GitHub Integration Docs](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Performance Comparison](https://dev.to/dataformathub/cloudflare-vs-vercel-vs-netlify-the-truth-about-edge-performance-2026-50h0)

---

### 2. VERCEL ⭐⭐⭐⭐

**Status:** ALTERNATIVA PREMIUM

#### Pricing

| Caratteristica | Hobby (Free) | Pro ($20/mese) |
|----------------|--------------|----------------|
| **Bandwidth** | 100 GB/mese | 1 TB/mese |
| **Bandwidth overage** | Upgrade richiesto | $0.15/GB |
| **Build minutes** | Unlimited | Unlimited |
| **Custom domains** | Unlimited | Unlimited |
| **Sites** | Unlimited | Unlimited |
| **Team members** | 1 | Unlimited |
| **Costo mensile** | **$0** | **$20** |

**Nota:** Hobby tier NON permette overage - DEVI upgradare se superi 100GB.

#### Performance

- **CDN:** Edge Network globale
- **Latency:** Eccellente (leggermente dietro Cloudflare)
- **Build speed:** MOLTO consistente (vs Cloudflare)
- **Uptime:** 99.99%

#### Features

| Feature | Supporto | Note |
|---------|----------|------|
| SSL/HTTPS | ✅ Automatico | Let's Encrypt |
| Custom Domain | ✅ Gratis | Illimitati |
| GitHub Integration | ✅ Nativo | Best-in-class |
| Preview Deployments | ✅ | Per ogni PR |
| Rollback | ✅ | 1-click |
| CI/CD | ✅ | Nativo eccellente |
| Analytics | ⚠️ | Premium feature ($10/mese extra) |
| Edge Functions | ✅ | Se serve in futuro |

#### Setup Complexity

**Difficoltà:** 1/10 (triviale)

```bash
# Procedura
1. Import GitHub repo su Vercel
2. Auto-detect settings
3. Deploy automatico
4. Custom domain setup
5. Done!

Tempo stimato: 5 minuti
```

#### Pro

```
✅ Developer Experience ECCELLENTE
✅ Build speed CONSISTENTE
✅ Dashboard bellissima e intuitiva
✅ Preview deployments top-tier
✅ GitHub integration impeccabile
✅ Analytics (a pagamento ma buoni)
✅ Documentazione superba
✅ Usato da Next.js team (loro prodotto)
```

#### Contro

```
❌ FREE tier: 100GB bandwidth (vs UNLIMITED Cloudflare)
   → ~100k visite/mese max
   → Se SHOW HN virale, rischio upgrade forzato
❌ NO overage su Hobby - upgrade forzato
   → $20/mese se superi 100GB
❌ Analytics NON incluso (vs Cloudflare free)
❌ Vendor lock-in moderato (feature Next.js-specific)
```

#### Affidabilità

- **Uptime storico:** 99.99%
- **Incident history:** Rari
- **SLA:** No SLA su Hobby tier

#### Quando Scegliere Vercel

```
SE hai bisogno di:
- Next.js features avanzate (non il nostro caso)
- Build speed GARANTITA consistente
- Analytics premium
- Team collaboration da subito

Altrimenti: Cloudflare è superiore per static.
```

#### Fonti

- [Vercel Pricing](https://vercel.com/pricing)
- [Vercel Limits](https://vercel.com/docs/limits)
- [Vercel Pricing Breakdown](https://flexprice.io/blog/vercel-pricing-breakdown)
- [Vercel Free Guide 2026](https://freerdps.com/blog/is-vercel-hosting-free/)

---

### 3. NETLIFY ⭐⭐⭐

**Status:** TERZA OPZIONE

#### Pricing

| Caratteristica | Free Tier | Pro ($19/mese) |
|----------------|-----------|----------------|
| **Bandwidth** | 100 GB/mese | 400 GB/mese |
| **Build minutes** | 300/mese | 1000/mese |
| **Custom domains** | Unlimited | Unlimited |
| **Sites** | Unlimited | Unlimited |
| **Team members** | 1 | 5 |
| **Costo mensile** | **$0** | **$19** |

**Nota CRITICA:** Se superi limiti free, TUTTO il tuo account viene PAUSATO fino al mese successivo!

#### Performance

- **CDN:** Global CDN, multiple edge locations
- **Latency:** Buona (dietro Cloudflare e Vercel)
- **Uptime:** 99.9%

#### Features

| Feature | Supporto | Note |
|---------|----------|------|
| SSL/HTTPS | ✅ Automatico | Let's Encrypt |
| Custom Domain | ✅ Gratis | Illimitati |
| GitHub Integration | ✅ Nativo | Buono |
| Preview Deployments | ✅ | Per ogni PR |
| Rollback | ✅ | 1-click |
| CI/CD | ✅ | Buono |
| Analytics | ⚠️ | Premium ($9/mese) |
| Forms | ✅ | Se serve |

#### Setup Complexity

**Difficoltà:** 2/10 (facile)

```bash
# Procedura
1. Connetti GitHub a Netlify
2. Seleziona repo
3. Configure build settings
4. Deploy
5. Custom domain

Tempo stimato: 10 minuti
```

#### Pro

```
✅ Forms handling built-in (se serve)
✅ Split testing incluso
✅ Deployment previews
✅ Free tier generoso
```

#### Contro

```
❌ 100GB bandwidth (vs UNLIMITED Cloudflare)
❌ PAUSA account se superi limiti (CRITICO!)
   → Se SHOW HN virale: sito DOWN fino a mese prossimo!
❌ Build minutes limitati (300/mese)
❌ Performance inferiori a Cloudflare/Vercel
❌ Pricing model recente non chiaro (crediti)
```

#### Affidabilità

- **Uptime storico:** 99.9% (lower than competitors)
- **Incident history:** Alcuni problemi documentati

#### Perché NON Netlify

```
RISCHIO PAUSA ACCOUNT su free tier = DEALBREAKER

Se SHOW HN va virale:
→ Superi 100GB
→ Account PAUSATO
→ Sito DOWN
→ Opportunità PERSA

Non accettabile per lancio pubblico.
```

#### Fonti

- [Netlify Pricing](https://www.netlify.com/pricing/)
- [Netlify Free Tier Limits](https://www.freetiers.com/directory/netlify)
- [Netlify Pricing Guide](https://flexprice.io/blog/complete-guide-to-netlify-pricing-and-plans)
- [Leaving Netlify Free Tier](https://conorsheehan1.github.io/blog/2024/03/07/leaving-netlify-free-tier.html)

---

### 4. GITHUB PAGES ⭐⭐

**Status:** OPZIONE BASE

#### Pricing

| Caratteristica | Free Tier |
|----------------|-----------|
| **Bandwidth** | 100 GB/mese (soft limit) |
| **Storage** | 1 GB |
| **Build minutes** | 2000/mese (Actions) |
| **Costo mensile** | **$0** |

#### Performance

- **CDN:** Fastly CDN
- **Latency:** Accettabile
- **Edge locations:** Limitato vs Cloudflare
- **Uptime:** 99.9%

#### Features

| Feature | Supporto | Note |
|---------|----------|------|
| SSL/HTTPS | ✅ Automatico | Let's Encrypt |
| Custom Domain | ✅ Gratis | Con limitazioni DNS |
| GitHub Integration | ✅ Nativo | Ovviamente |
| Preview Deployments | ❌ | Solo branch gh-pages |
| Rollback | ⚠️ | Via git revert |
| CI/CD | ✅ | GitHub Actions |
| Analytics | ❌ | - |

#### Setup Complexity

**Difficoltà:** 3/10 (medio)

```bash
# Procedura
1. Enable GitHub Pages su repo
2. Configure gh-pages branch
3. Setup GitHub Actions per build
4. Custom domain CNAME
5. Attendi propagazione DNS

Tempo stimato: 20 minuti
```

#### Pro

```
✅ Gratis
✅ Zero vendor lock-in (è GitHub)
✅ Semplice per progetti open source
```

#### Contro

```
❌ Performance inferiori (Fastly vs Cloudflare)
❌ NO preview deployments (solo 1 branch)
❌ DNS configuration limitata (dominio < 64 caratteri)
❌ SSL provisioning può richiedere 24h
❌ NO analytics
❌ NO edge functions
❌ Esperienza developer inferiore
```

#### Affidabilità

- **Uptime storico:** 99.9%
- **Incident history:** Stabile ma basic

#### Perché NON GitHub Pages

```
Limitazioni tecniche vs alternative moderne:
- NO preview deployments
- Performance inferiori
- Feature set minimale
- DNS quirks

Cloudflare fa tutto meglio, gratis.
```

#### Fonti

- [GitHub Pages Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub Pages HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [GitHub Pages Limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)

---

### 5. FLY.IO (Static) ⭐⭐⭐

**Status:** OPZIONE CONSOLIDAMENTO (già usiamo per API)

#### Pricing

| Caratteristica | Free Tier | Costo |
|----------------|-----------|-------|
| **VMs** | 3x shared-cpu-1x (256MB) | Gratis |
| **Additional VMs** | Oltre 3 | $1.94/mese ciascuna |
| **Bandwidth** | 100GB/mese | Gratis |
| **Bandwidth overage** | Oltre 100GB | $0.02/GB |
| **Storage (Tigris)** | 5GB | Gratis |
| **Storage extra** | Oltre 5GB | $0.15/GB/mese |
| **Costo mensile stimato** | | **~$2-5/mese** |

#### Performance

- **CDN:** Global edge network (30+ regions)
- **Latency:** Eccellente
- **Uptime:** 99.99%
- **Note:** VA configurato CDN esterno per large assets

#### Features

| Feature | Supporto | Note |
|---------|----------|------|
| SSL/HTTPS | ✅ Automatico | Certificati automatici |
| Custom Domain | ✅ Gratis | - |
| GitHub Integration | ⚠️ | Via GitHub Actions |
| Preview Deployments | ❌ | Manuale |
| Rollback | ✅ | Via CLI |
| CI/CD | ⚠️ | Configurazione manuale |
| Analytics | ❌ | - |
| Static + Tigris | ✅ | Hosting statico su S3-like |

#### Setup Complexity

**Difficoltà:** 5/10 (medio-alto)

```bash
# Procedura
1. Install flyctl
2. Create Fly app
3. Configure fly.toml
4. Setup Tigris bucket (o nginx container)
5. Configure GitHub Actions deployment
6. Custom domain DNS
7. Test e deploy

Tempo stimato: 45-60 minuti
```

#### Pro

```
✅ Consolidamento: API + Landing su stessa piattaforma
✅ Controllo totale (VMs, container, etc)
✅ Edge network eccellente
✅ Uptime elevato
✅ Già familiari con Fly.io
```

#### Contro

```
❌ Costo mensile ($2-5 vs $0 Cloudflare)
❌ Complessità setup (nginx/container vs static hosting)
❌ Bandwidth 100GB (non unlimited)
❌ NO preview deployments automatici
❌ Configurazione manuale CI/CD
❌ Overkill per sito statico
❌ Costi imprevedibili se traffico alto
```

#### Affidabilità

- **Uptime storico:** 99.99%
- **Incident history:** Rari

#### Quando Scegliere Fly.io

```
SE consolidamento è priorità CRITICA:
→ Fly.io API + Landing stesso account
→ Semplifica billing
→ Semplifica gestione

ALTRIMENTI:
→ Cloudflare Pages è SUPERIORE per static
→ $0 vs $2-5/mese
→ Zero configurazione
→ Feature migliori
```

#### Fonti

- [Fly.io Pricing](https://fly.io/pricing/)
- [Fly.io Static Sites](https://brianli.com/hosting-static-sites-on-fly-io/)
- [Fly.io Pricing Calculator](https://fly.io/calculator)
- [Fly.io Alternatives Comparison](https://northflank.com/blog/flyio-alternatives)

---

