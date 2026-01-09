# DECISIONE: Strategia Pricing

> **Data:** 9 Gennaio 2026 - Sessione 139
> **Status:** DECISO (basato su ricerca + intuizione Rafa)

---

## LA STRATEGIA: Aggressiva + Premium

### Tier Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   FREE (BYOK)                                                  │
│   ├── Porta tua API key Anthropic                              │
│   ├── CLI full, 16 agenti                                      │
│   ├── SNCP full                                                │
│   └── Entry point zero attrito                                 │
│                                                                 │
│   ESSENTIALS - $19/mese                                        │
│   ├── Token inclusi (hosted)                                   │
│   ├── Web dashboard                                            │
│   ├── 100 task/mese                                            │
│   └── Email support                                            │
│                                                                 │
│   PROFESSIONAL - $39/mese                                      │
│   ├── Unlimited tasks                                          │
│   ├── Team features                                            │
│   ├── Priority support                                         │
│   └── Custom agents                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PERCHE QUESTA STRUTTURA

### $19 (non $29)
- **Sotto Cursor** ($20) - psicologicamente "meno"
- **Sopra budget** ($10) - non troppo economico
- **Charm pricing** - $19 < $20 percepito come molto meno
- **Low friction** - "non ci penso due volte"

### $39 (non $49)
- **Decoy effect** - fa sembrare $19 super accessibile
- **Premium tier** - per chi vuole di più
- **Margin buffer** - copre heavy users

### BYOK Free
- **Zero attrito** - prova senza rischio
- **Dev-friendly** - già hanno API key
- **Conversion funnel** - provano → amano → pagano

---

## STRATEGIE AGGRESSIVE (Lancio)

### 1. Early Bird
```
Primi 500 utenti: $99/anno = $8.25/mese
(invece di $228/anno)

Crea urgency + early advocates
```

### 2. Primo Mese $9.99
```
Trial upgrade: $9.99 primo mese
Poi $19/mese

Abbassa barriera entry
```

### 3. Referral
```
Invita 3 amici → 1 mese gratis
Loro ottengono primo mese $9.99

Word-of-mouth growth
```

---

## POSITIONING

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Copilot $10      Windsurf $15      Cursor $20                │
│       ↑                ↑                 ↑                      │
│   "Assistant"     "Cheaper"         "Editor"                   │
│                                                                 │
│                  CervellaSwarm $19                              │
│                        ↑                                        │
│              "AI TEAM at fair price"                           │
│                                                                 │
│   Non siamo il più economico.                                  │
│   Non siamo il più caro.                                       │
│   Siamo il MIGLIOR VALORE.                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## MESSAGGIO MARKETING

> "16 specialisti. $19/mese. Meno di Cursor, più di tutto."

> "Why pay for one assistant when you can have a team?"

> "Cursor gives you an editor. We give you a team."

---

## NOTA RAFA

> "Facciamo qualcosa aggressiva per iniziare.. fare loro provare
> e dopo che vedono che la cosa è fantastica facciamo pacchetti"

**Esatto!** BYOK free + Early Bird + $19 = aggressivo ma non "barato".

---

## RISCHI E MITIGAZIONI

| Rischio | Mitigazione |
|---------|-------------|
| Heavy users | Overage $10/1M tokens extra |
| Perception "cheap" | Messaging "best value" non "cheapest" |
| API costs | Volume discount Anthropic |
| Churn | Onboarding + SNCP lock-in positivo |

---

*"Non il più economico. Non il più caro. Il miglior valore."*

*Decisione presa: 9 Gennaio 2026*
