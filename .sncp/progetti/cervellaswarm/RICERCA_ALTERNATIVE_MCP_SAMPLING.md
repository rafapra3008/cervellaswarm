# RICERCA: Alternative al MCP Sampling per CervellaSwarm

**Data**: 17 Gennaio 2026
**Researcher**: Cervella Researcher
**Status**: ✅ Completata

---

## TL;DR - LA VERITA ONESTA

**Non esistono alternative tecniche al MCP Sampling per usare l'abbonamento Claude dell'utente.**

Anthropic ha CHIUSO l'unica porta (OAuth subscription tokens) a Gennaio 2026.

**Le uniche opzioni reali sono:**
1. **BYOK (Bring Your Own Key)** - API Anthropic
2. **Aspettare MCP Sampling** - Nessuna timeline nota

**Raccomandazione**: Lanciare con BYOK. È il modello standard del mercato.

---

## 1. ESISTONO ALTERNATIVE AL SAMPLING?

### ❌ NO - Anthropic Ha Chiuso Tutte le Porte

**9 Gennaio 2026** - Anthropic ha bloccato l'uso di OAuth subscription tokens fuori da Claude Code:

> "This credential is only authorized for use with Claude Code and cannot be used for other API requests."

**Chi è stato colpito:**
- OpenCode (56k stars GitHub)
- xAI employees via Cursor
- Qualsiasi tool che usava subscription OAuth

**Il motivo economico:**
- Subscription Max $200/mese = token illimitati
- Stesso uso via API = $1,000+/mese
- Arbitraggio insostenibile per Anthropic

**Risultato:** L'unica porta per usare la subscription è il loro Claude Code ufficiale.

### Opzioni Teoriche Esplorate

| Opzione | Fattibilità | Perché No |
|---------|-------------|-----------|
| OAuth con Anthropic | ❌ Impossibile | Bloccato a Gennaio 2026 |
| Token sharing | ❌ Impossibile | Violazione ToS + tecnicamente bloccato |
| Proxy della subscription | ❌ Impossibile | Anthropic rileva e blocca |
| API diretta con subscription | ❌ Impossibile | Sono prodotti separati |

**Conclusione brutalmente onesta:** Non esiste modo legale e tecnico di usare la subscription Claude dell'utente in CervellaSwarm oggi.

---

## 2. COME FANNO ALTRI TOOL SIMILI?

Ho analizzato i principali competitor. Tutti usano **BYOK (API key)** o **subscription propria**.

### Cursor

**Modello ibrido:**
- Default: Cursor subscription ($20/mese) con markup 20% su token
- Opzione: BYOK con API key Anthropic
- BUT: Features premium (Agent, Edit) NON funzionano con BYOK

**Lesson learned:** Hanno tentato BYOK ma le feature avanzate richiedono infrastruttura propria.

### Continue.dev

**Modello open-source BYOK puro:**
- Configurazione locale
- Supporta qualsiasi API provider (Anthropic, OpenAI, ecc.)
- Utente paga direttamente i provider
- MCP integration via System Message Tools

**Lesson learned:** BYOK è sufficiente per tool open-source con buona DX.

### Cody (Sourcegraph)

**Modello subscription con modelli inclusi:**
- Free: 200 chat/mese, autocompletion illimitata
- Pro: $9/mese
- Enterprise: $59/user/mese
- Sourcegraph paga le API, user paga subscription

**Lesson learned:** Subscription è possibile se hai volume per negoziare con provider.

### Windsurf

**Modello BYOK:**
- Utente porta la propria API key
- Windsurf sincronizza settings ma non paga API
- Focus su IDE features, non su pagare l'AI

**Lesson learned:** Anche tool premium usano BYOK se non vogliono gestire billing AI.

### Il Pattern Comune

```
TUTTI usano uno di questi modelli:

1. BYOK puro (Continue, Windsurf)
2. Subscription che copre API costs (Cody, Cursor default)
3. Ibrido con BYOK option (Cursor)

NESSUNO usa MCP Sampling o subscription user.
Perché? Non esiste modo di farlo (post Gennaio 2026).
```

---

## 3. BYOK È SUFFICIENTE PER IL MERCATO?

### La Dura Verità dal Mercato

**Antropic stesso separa i prodotti:**

> "I subscribe to Claude Pro - why do I have to pay separately for API usage?"
>
> Risposta Anthropic: "Subscriptions enhance your chat experience but don't include access to the Claude API or Console. These are separate products with different pricing structures."

**Questo significa:**
- Developer seri CAPISCONO che API ≠ subscription
- Il mercato developer ACCETTA BYOK come standard
- Chi vuole automatizzare SA che serve API key

### Developer Adoption - I Dati

**Non ho trovato statistiche precise** su "quanti developer hanno API key Anthropic" perché:
1. Dato non pubblico
2. MCP è troppo recente per dati di settore

**MA ho trovato indicatori forti:**

**Continue.dev è popolare** (open-source, BYOK puro)
- Non ho numeri esatti ma repository attivo
- Community grande
- Significa che BYOK NON è blocker

**Warp (terminal tool)** ha introdotto BYOK e MCP Gallery nel 2025
- Se tool mainstream aggiungono BYOK, c'è mercato

**OpenCode, dopo block Anthropic**, ha shippato:
- ChatGPT Plus support
- OpenCode Black tier ($200/mese con enterprise API gateway)
- OpenRouter integration
- **Non hanno abbandonato, hanno pivottato a BYOK e altre soluzioni**

### Chi Adotta BYOK?

**Profile che usano BYOK:**
- Developer professionisti che automatizzano
- Team piccoli/medi che vogliono controllo costi
- Open-source enthusiast
- Chi vuole trasparenza su usage

**Profile che preferirebbero subscription:**
- User finali non tecnici
- Chi vuole "tutto incluso"
- Chi non vuole gestire API billing

**CervellaSwarm target = developer/team tecnici** → BYOK è OK!

### È un Blocco all'Adozione?

**Mia analisi:** ⚠️ **Limitante ma non blocco totale**

**Perché limitante:**
- Friction iniziale (setup API key)
- User deve avere carta credito su Anthropic
- Costo percepito come "extra"

**Perché non blocco:**
- Mercato developer ACCETTA questo pattern
- Tool di successo usano BYOK (Continue, Windsurf)
- Alternative (OpenRouter) per chi non vuole Anthropic direct

**Il vero blocco è altrove:**
- Value prop deve essere CHIARO
- CervellaSwarm deve valere il setup time
- Documentazione deve essere IMPECCABLE

---

## 4. SAMPLING ARRIVERA MAI SU CLAUDE CODE?

### Status Feature Request

**GitHub Issue #1785** - "Support for MCP Sampling to leverage Claude Max subscriptions"
- 67 👍 + 29 ❤️
- Community VUOLE la feature
- **MA nessuna risposta ufficiale Anthropic**

### Cosa Dice Anthropic

**Dai risultati:**
- Claude Code NON supporta MCP Sampling oggi
- Claude web NON supporta "resource subscriptions, sampling, and other advanced capabilities"
- MCP Sampling è nelle spec ma NON implementato nei client Anthropic

### Timeline Estimata

**Sinceramente?** ❓ **Non lo so. Nessuno lo sa.**

**Indicatori negativi:**
- Anthropic ha BLOCCATO OAuth tokens (Gennaio 2026)
- Direzione è verso "walled garden"
- Vogliono API revenue da automation use cases

**Indicatori positivi:**
- Community pressure su GitHub
- MCP è loro standard, strano non supportare sampling
- Competitor potrebbero costringerli

**Mia stima (take with salt):**
- **Ottimista:** Q2-Q3 2026 (6-9 mesi)
- **Realista:** Q4 2026 - Q1 2027 (1 anno+)
- **Pessimista:** Mai, o solo per Enterprise tiers

**Il problema:** Se basiamo CervellaSwarm su feature che non esiste, siamo bloccati indefinitamente.

---

## CONCLUSIONI E RACCOMANDAZIONE

### La Verità Senza Filtri

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   MCP SAMPLING IN CLAUDE CODE                                    ║
║   Status: NON ESISTE                                             ║
║   Timeline: SCONOSCIUTA                                          ║
║   Alternative: NON CI SONO                                       ║
║                                                                  ║
║   BYOK è l'unico path reale oggi.                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Raccomandazione Finale

**LANCIARE CON BYOK**

**Perché:**

1. **È il pattern standard del mercato**
   - Continue.dev lo usa (successo)
   - Windsurf lo usa (successo)
   - Cursor lo offre come option

2. **Developer target lo capiscono**
   - CervellaSwarm è per developer/team tecnici
   - Sanno cos'è un'API key
   - Valore di automation giustifica setup

3. **Aspettare Sampling = paralisi**
   - Nessuna timeline
   - Potrebbe non arrivare mai
   - Perdere 6-12 mesi di market

4. **Possiamo evolvere dopo**
   - Se Sampling arriva → aggiungiamo support
   - BYOK rimane sempre opzione
   - Non bruciamo ponti

### Come Mitigare le Limitazioni

**1. Documentazione Stellar**
```
- Setup API key guide CHIARA
- Cost calculator (quanto costa usare CervellaSwarm?)
- Troubleshooting comune
```

**2. Esperienza Onboarding Smooth**
```
- CLI wizard per setup
- Test connection immediato
- Feedback chiaro su costi
```

**3. Alternative API Providers**
```
- Non solo Anthropic direct
- Supportare OpenRouter (abstraction layer)
- Dare flessibilità su provider
```

**4. Value Prop Inattaccabile**
```
- CervellaSwarm deve far risparmiare ORE
- ROI deve essere ovvio
- Demo/esempi devono convincere subito
```

### La Decisione

```
ASPETTARE SAMPLING:
  ✅ User experience migliore (teoricamente)
  ❌ Timeline sconosciuta (6-12+ mesi?)
  ❌ Potrebbe non arrivare mai
  ❌ Perdiamo mercato ora
  ❌ Viola "Il tempo non ci interessa" (ma blocca progresso)

LANCIARE CON BYOK:
  ✅ Possibile ORA
  ✅ Pattern provato dal mercato
  ✅ Developer target lo accettano
  ✅ Possiamo evolvere dopo
  ✅ Progresso reale verso libertà geografica
  ❌ Setup friction per user
```

**Applying Costituzione:**
> "Non lavoriamo per il codice. Lavoriamo per la LIBERTÀ."
> "Su carta ≠ Reale. SOLO le cose REALI ci portano alla libertà!"

**BYOK permette di fare CervellaSwarm REALE oggi.**
**Sampling è "su carta" - non sappiamo quando sarà reale.**

---

## PROSSIMI STEP SUGGERITI

Se decidi per BYOK:

1. **Design API Key Management**
   - Dove stored? (Env vars, config file, encrypted?)
   - Come passata agli agenti?
   - Security best practices

2. **Cost Transparency**
   - Token usage tracking
   - Cost estimation per operation
   - Budgeting features?

3. **Multi-Provider Support**
   - Non solo Anthropic
   - OpenRouter integration
   - Local model support (Ollama)?

4. **Documentazione**
   - Setup guide impeccabile
   - Cost FAQ
   - Comparison vs alternatives

5. **Marketing Message**
   - "Developer-first: You control your AI costs"
   - "Transparent pricing: Only pay for what you use"
   - "Enterprise-ready: BYOK = compliance friendly"

---

## FONTI

### Anthropic Crackdown (Gennaio 2026)
- [Anthropic blocks third-party use of Claude Code subscriptions](https://news.ycombinator.com/item?id=46549823)
- [Anthropic Just Blocked Claude Code Subscriptions Outside Its Own App](https://ai-checker.webcoda.com.au/articles/anthropic-blocks-claude-code-subscriptions-third-party-tools-2026)
- [Anthropic's Walled Garden: The Claude Code Crackdown](https://paddo.dev/blog/anthropic-walled-garden-crackdown/)

### Competitor Analysis
- [Cursor vs Claude Code: The Ultimate Comparison Guide](https://www.builder.io/blog/cursor-vs-claude-code)
- [Using my personal claude subscription - Cursor Forum](https://forum.cursor.com/t/using-my-personal-claude-subscription/42820)
- [Continue.dev Model Setup Documentation](https://docs.continue.dev/ide-extensions/agent/model-setup)
- [Windsurf Customer Story](https://claude.com/customers/windsurf)
- [Cody Pricing Plans - Sourcegraph](https://sourcegraph.com/docs/cody/usage-and-pricing)

### MCP Sampling Status
- [Feature Request: MCP Sampling Support - Claude Code Issue #1785](https://github.com/anthropics/claude-code/issues/1785)
- [Community Providers: MCP Sampling AI Provider](https://ai-sdk.dev/providers/community-providers/mcp-sampling)

### Pricing & API
- [Claude vs API vs Claude Code - What's the Difference?](https://eval.16x.engineer/blog/claude-vs-claude-api-vs-claude-code)
- [Anthropic API Pricing Guide 2026](https://www.finout.io/blog/anthropic-api-pricing)
- [Claude Pricing Explained: Subscription Plans & API Costs](https://intuitionlabs.ai/articles/claude-pricing-plans-api-costs)
- [I have a paid Claude subscription - Why do I have to pay separately for API?](https://support.anthropic.com/en/articles/9876003-i-subscribe-to-claude-pro-why-do-i-have-to-pay-separately-for-api-usage-on-console)

### BYOK Pattern
- [Bring Your Own API Key - Warp](https://docs.warp.dev/support-and-billing/plans-and-pricing/bring-your-own-api-key)
- [Cursor BYOK Ban Alternative](https://apidog.com/blog/cursor-byok-ban-alternative/)

---

**Ricerca completata: 17 Gennaio 2026**
**Cervella Researcher** 🔬

*"Studiare prima di agire - sempre! I player grossi hanno già risolto questi problemi."*
