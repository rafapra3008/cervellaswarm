# BUSINESS MODEL - CervellaSwarm

> **Data:** 9 Gennaio 2026 - Sessione 139
> **Status:** PROPOSTA (da validare con Rafa)

---

## BENCHMARK COMPETITOR

| Competitor | Free | Pro | Teams | Enterprise |
|------------|------|-----|-------|------------|
| **Copilot** | $0 (limited) | $10/mo | - | $19/user |
| **Cursor** | $0 (2000 comp) | $20/mo | $40/user | Custom |
| **Windsurf** | $0 (25 credits) | $15/mo | $30/user | $60/user |

**Insight:** $10-20/mo è lo standard per Pro.

---

## I NOSTRI COSTI (Anthropic API)

| Modello | Input | Output | Uso Tipico |
|---------|-------|--------|------------|
| Haiku | $1/MTok | $5/MTok | Tasks leggeri |
| Sonnet | $3/MTok | $15/MTok | Tasks normali |
| Opus | $5/MTok | $25/MTok | Guardiane, complex |

### Costo Per Utente Stimato

| Profilo | Uso/Mese | Costo API |
|---------|----------|-----------|
| Light | 500K tok | ~$5-10 |
| Medium | 2M tok | ~$20-40 |
| Heavy | 5M tok | ~$50-100 |
| Power | 10M+ tok | ~$100-200 |

---

## PROPOSTA PRICING

### Opzione A: Usage-Based (Come Costo API)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   FREE TIER                                                    │
│   ├── 100K tokens/mese (Haiku only)                           │
│   ├── 2 agenti base                                            │
│   └── CLI only, no web                                         │
│                                                                 │
│   PRO - $25/mese                                               │
│   ├── 2M tokens/mese (Sonnet)                                  │
│   ├── 16 agenti                                                │
│   ├── Web dashboard                                            │
│   └── SNCP full                                                │
│                                                                 │
│   TEAMS - $50/user/mese                                        │
│   ├── 5M tokens/user                                           │
│   ├── Team collaboration                                       │
│   ├── Shared SNCP                                              │
│   └── Priority support                                         │
│                                                                 │
│   ENTERPRISE - Custom                                          │
│   ├── Unlimited (volume pricing)                               │
│   ├── SSO, audit logs                                          │
│   ├── Dedicated support                                        │
│   └── On-prem option                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Pro:** Trasparente, scalabile
**Contro:** Utenti odiano "limits"

---

### Opzione B: Flat Rate (Semplice)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   FREE TRIAL - 14 giorni                                       │
│   ├── Full access                                              │
│   └── No credit card                                           │
│                                                                 │
│   PRO - $29/mese (flat)                                        │
│   ├── Unlimited* use                                           │
│   ├── 16 agenti                                                │
│   ├── Web dashboard                                            │
│   └── *Fair use policy                                         │
│                                                                 │
│   TEAMS - $49/user/mese                                        │
│   ├── Everything in Pro                                        │
│   ├── Team features                                            │
│   └── Priority support                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Pro:** Semplice, predictable
**Contro:** Rischio abuse, margin squeeze

---

### Opzione C: IBRIDO (RACCOMANDATO)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   FREE - Per Sempre                                            │
│   ├── BYOK (Bring Your Own Key)                               │
│   ├── CLI full, 16 agenti                                      │
│   ├── Web dashboard (read-only)                                │
│   └── Community support                                        │
│                                                                 │
│   PRO - $29/mese                                               │
│   ├── Inclusi 3M tokens Sonnet                                 │
│   ├── Web dashboard full                                       │
│   ├── SNCP cloud backup                                        │
│   ├── Email support                                            │
│   └── Overage: $10/1M tokens                                   │
│                                                                 │
│   TEAMS - $49/user/mese                                        │
│   ├── 5M tokens/user inclusi                                   │
│   ├── Team workspace                                           │
│   ├── Shared SNCP                                              │
│   ├── Admin console                                            │
│   └── Priority support                                         │
│                                                                 │
│   ENTERPRISE - Custom                                          │
│   ├── Volume pricing                                           │
│   ├── SSO/SAML                                                 │
│   ├── Audit logs                                               │
│   ├── SLA                                                      │
│   └── Dedicated success manager                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Perche IBRIDO:**
1. **FREE BYOK** - Attira dev che hanno già API key
2. **PRO $29** - Tra Cursor ($20) e valore premium
3. **TEAMS $49** - Competitivo con Cursor Teams ($40)
4. **Token inclusi** - Semplice ma con safety net

---

## ANALISI MARGINI

### PRO $29/mese

| Scenario | Token Use | Costo API | Margine |
|----------|-----------|-----------|---------|
| Light | 1M | ~$8 | $21 (72%) |
| Medium | 3M | ~$24 | $5 (17%) |
| Heavy | 5M | ~$40 | -$11 (loss!) |

**Insight:** Heavy users = loss. Serve:
- Fair use policy
- Overage pricing
- O tier più alto

### Con Overage $10/1M

| Scenario | Token Use | Costo | Revenue | Margine |
|----------|-----------|-------|---------|---------|
| Light | 1M | $8 | $29 | $21 |
| Medium | 3M | $24 | $29 | $5 |
| Heavy | 5M | $40 | $49* | $9 |

*$29 + $20 overage (2M extra)

**Meglio!** Overage protegge margini.

---

## POSITIONING VS COMPETITOR

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Copilot $10  ──────── Windsurf $15 ──────── Cursor $20      │
│        ↑                                           ↑           │
│   "Assistant"                                  "Editor"        │
│                                                                 │
│                    CervellaSwarm $29                           │
│                          ↑                                      │
│                    "AI TEAM"                                    │
│                                                                 │
│   Giustificazione prezzo premium:                              │
│   - 16 agenti vs 1-4                                           │
│   - Memoria persistente                                        │
│   - Quality gates                                              │
│   - IDE agnostic                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PROPOSTA FINALE

### Tier Structure

| Tier | Prezzo | Token | Target |
|------|--------|-------|--------|
| **Free (BYOK)** | $0 | Your API | Hobbyst, try-before-buy |
| **Pro** | $29/mo | 3M | Individual devs |
| **Teams** | $49/user | 5M/user | Small teams |
| **Enterprise** | Custom | Custom | Large orgs |

### Overage
- $10 per 1M tokens extra
- Notifica a 80% usage
- Hard cap opzionale

### Free Trial
- 14 giorni Pro
- No credit card
- Full access

---

## DOMANDE APERTE

1. **BYOK Free** - Troppo generoso? O ottimo per adoption?
2. **$29 vs $25** - $29 è psicologico ($30-1), $25 è più accessibile
3. **Overage** - $10/1M è giusto? Troppo? Poco?
4. **Enterprise** - Quando iniziare a offrire?

---

## NEXT STEPS

1. Validare con Rafa
2. Creare landing page con pricing
3. Setup Stripe/billing
4. Definire fair use policy

---

*"Premium price = premium value. Non competiamo su prezzo."*

*Proposta: 9 Gennaio 2026*
