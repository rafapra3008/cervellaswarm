# RICERCA: Autenticazione Claude Code CLI

**Data:** 16 Gennaio 2026
**Researcher:** Cervella Researcher
**Versione:** 1.0.0

---

## Executive Summary

Claude Code supporta **3 metodi di autenticazione principali**:
1. **Subscription-based** (Claude Pro/Max) - OAuth con claude.ai
2. **Console-based** (Pay-per-use) - OAuth con console.anthropic.com
3. **API Key** (BYOK) - ANTHROPIC_API_KEY environment variable

**ATTENZIONE CRITICA:** Se ANTHROPIC_API_KEY è impostato, Claude Code usa **API billing** invece della subscription, anche se sei loggato con account Pro/Max!

---

## 1. METODI DI AUTENTICAZIONE

### A. Claude Pro/Max Subscription (Raccomandato per Individui)

**Come Funziona:**
- Sottoscrizione unificata: stesso account per claude.ai web + Claude Code CLI
- Login OAuth via credenziali claude.ai
- Gestione centralizzata dell'account

**Prezzi e Limiti:**
| Piano | Costo | Usage Limit (ogni 5 ore) | Modelli |
|-------|-------|--------------------------|---------|
| **Free** | $0 | NO ACCESS a Claude Code | - |
| **Pro** | $20/mese | ~45 messaggi web OR ~10-40 prompt CLI | Sonnet, Opus 4.5 |
| **Max 5x** | $100/mese | ~225 messaggi web OR ~50-200 prompt CLI | Sonnet, Opus 4.5 |
| **Max 20x** | $200/mese | ~900 messaggi web OR ~200-800 prompt CLI | Sonnet, Opus 4.5 |

**Nota Critica:** Usage è CONDIVISA tra web e CLI! Se usi 30 messaggi su claude.ai, ne hai ~15 rimasti per Claude Code.

**Best For:** Sviluppatori individuali, piccoli repository (< 1,000 righe di codice per Pro)

### B. Claude Console (Pay-per-use)

**Come Funziona:**
- Account console.anthropic.com
- OAuth flow per autenticazione
- Richiede billing attivo
- Workspace "Claude Code" creato automaticamente per tracking usage

**LIMITAZIONE IMPORTANTE:**
- Il workspace "Claude Code" è READ-ONLY per API keys
- Non puoi creare API keys in questo workspace
- È dedicato ESCLUSIVAMENTE all'uso di Claude Code CLI

**Best For:** Uso sporadico, progetti con budget specifico

### C. API Key (BYOK - Bring Your Own Key)

**Come Funziona:**
- Imposta environment variable `ANTHROPIC_API_KEY`
- Claude Code la rileva automaticamente
- Billing a consumo (pay-as-you-go) via API

**ATTENZIONE CRITICA:**
```bash
# Se questo è impostato, anche con account Pro/Max loggato:
export ANTHROPIC_API_KEY="sk-ant-..."

# Claude Code userà API BILLING invece della subscription!
```

**Conflitto Rilevato:**
- Durante setup, se API key è presente, Claude Code chiede quale metodo usare
- Comando `/status` mostra quale metodo è attivo
- Issue GitHub #9699, #9515 documentano problemi di conflict

**Best For:** Team con controllo granulare dei costi, integrazione CI/CD

### D. Team & Enterprise

**Claude for Teams/Enterprise:**
- Gestione centralizzata billing e utenti
- Membri del team si loggano con account claude.ai individuali
- Accesso condiviso a Claude web + Claude Code

**Cloud Provider Integration:**
- Amazon Bedrock
- Google Vertex AI
- Microsoft Foundry
- Integrazione con infrastruttura cloud esistente

---

## 2. FLUSSO PRIMO UTILIZZO

### Installazione

```bash
# Passo 1: Installa Claude Code
npm install -g claude-code  # (comando esatto da code.claude.com/docs)

# Passo 2: Avvia in un progetto
cd your-project
claude
```

### Prima Autenticazione

**Scenario A: Account Pro/Max**
1. Claude Code chiede di autenticarti
2. Usa comando `/login`
3. Redirect a claude.ai
4. OAuth flow: autorizza l'app
5. Torna al terminale, autenticato
6. Credenziali salvate localmente

**Scenario B: Console Account**
1. Comando `/login`
2. Redirect a console.anthropic.com
3. OAuth flow
4. Workspace "Claude Code" creato automaticamente
5. Credenziali salvate

**Scenario C: API Key già presente**
1. Claude Code rileva `ANTHROPIC_API_KEY`
2. Chiede conferma: usare API key o login subscription?
3. Scegli metodo desiderato
4. Se scegli subscription, API key viene ignorata

### Comandi Utili Post-Login

```bash
# Verifica status autenticazione
/status

# Verifica quale metodo è attivo
/status  # mostra se usa subscription o API key

# Logout (per switch account)
/logout

# Switch tra modelli (Pro/Max)
/model  # scegli Sonnet o Opus 4.5

# Riprendi conversazione
/resume

# Aggiorna Claude Code
claude update
```

### Troubleshooting Setup

Se login non funziona:
1. `/logout`
2. `claude update`
3. Riavvia terminale completamente
4. `claude` e re-login
5. Seleziona account corretto

---

## 3. ACCOUNT TYPES & REQUIREMENTS

### Requisiti Minimi per Claude Code

| Account Type | Può Usare Claude Code? | Metodo Auth |
|--------------|------------------------|-------------|
| **Free** | NO | N/A |
| **Pro ($20)** | SÌ | OAuth claude.ai |
| **Max 5x ($100)** | SÌ | OAuth claude.ai |
| **Max 20x ($200)** | SÌ | OAuth claude.ai |
| **Console** | SÌ | OAuth console + billing attivo |
| **API Key** | SÌ | Environment variable |
| **Teams** | SÌ | OAuth claude.ai (individuale) |
| **Enterprise** | SÌ | OAuth + cloud integration |

### Differenze Chiave

**Claude.ai Account (Pro/Max):**
- Subscription mensile fissa
- Usage limits con reset ogni 5 ore
- Nessun costo aggiuntivo oltre subscription
- Accesso sia web che CLI

**Console Account:**
- Pay-per-use (API pricing)
- Nessun limite fisso, paghi ciò che usi
- Richiede billing method attivo
- Workspace Claude Code dedicato

**API Key:**
- Massima flessibilità
- Adatto per automazione/CI
- Pay-per-token
- Compatibile con SDK Anthropic esistenti

---

## 4. BYOK (BRING YOUR OWN KEY)

### Supporto Ufficiale

**Risposta:** SÌ, Claude Code supporta BYOK via `ANTHROPIC_API_KEY`.

### Come Funziona

**Setup:**
```bash
# In ~/.zshrc o ~/.bash_profile
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Verifica
echo $ANTHROPIC_API_KEY

# Claude Code la rileva automaticamente
claude
```

**Priority Behavior:**
- Se `ANTHROPIC_API_KEY` è impostato → usa API billing
- Se non impostato + loggato → usa subscription
- Se entrambi presenti → chiede quale usare

### Costi BYOK vs Subscription

**Scenario Esempio:**
- Pro Plan: $20/mese, ~10-40 prompt CLI ogni 5 ore
- API Key: ~$0.003 per prompt (varia con lunghezza input/output)

**Quando BYOK conviene:**
- Uso sporadico (< 100 prompt/mese)
- Automazione CI/CD
- Controllo granulare costi per cliente/progetto

**Quando Subscription conviene:**
- Uso quotidiano intenso
- Sviluppo attivo
- Prevedibilità costi mensili

### Eventi Recenti (Gennaio 2026)

**Anthropic Enforcement:**
- Gennaio 2026: Anthropic ha bloccato app terze che spoof Claude Code
- "Tightened safeguards against spoofing"
- Terze parti NON possono più usare subscription Pro per API calls
- Obiettivo: proteggere revenue model, spingere high-volume verso API commerciale

**Impatto:**
- Tool come Cursor, Windsurf NON possono usare Claude Code subscriptions
- Claude Code subscription è SOLO per CLI ufficiale
- Third-party devono usare API keys dirette (BYOK)

---

## 5. LIMITI E USAGE

### Reset Schedule

**Tutti i piani subscription:**
- Limite sessione reset ogni **5 ore**
- Contatore riavvia automaticamente
- Monitora con `/status`

### Usage Condivisa

**CRITICO:** Usage è condivisa tra:
- Claude.ai web
- Claude mobile app
- Claude desktop app
- Claude Code CLI

**Esempio:**
- Pro plan: 45 messaggi ogni 5 ore TOTALI
- Se usi 30 su web → rimangono 15 per CLI
- Se usi 20 su CLI → rimangono 25 per web

### Recent Confusion (Gennaio 2026)

**The Register Article:**
- Dicembre 2025: Anthropic raddoppiò limiti come regalo
- 31 Dicembre 2025: ritorno a limiti normali
- Utenti si lamentarono pensando fosse nerf
- Era solo fine del periodo promozionale

### Superamento Limiti

**Opzione API Continuation:**
Quando raggiungi limite subscription:
1. Claude Code offre continuare con API credits
2. **Richiede consenso esplicito**
3. Puoi rifiutare e aspettare reset (5 ore)
4. Se accetti, passa temporaneamente a API billing

**Best Practice:**
- Monitora usage regolarmente (`/status`)
- Pianifica task grandi per inizio finestra 5-ore
- Considera Max 5x/20x se limiti troppo stretti

---

## 6. DOCUMENTAZIONE UFFICIALE

### Link Principali

| Risorsa | URL |
|---------|-----|
| **Setup Guide** | https://code.claude.com/docs/en/setup |
| **Quickstart** | https://code.claude.com/docs/en/quickstart |
| **Pro/Max Guide** | https://support.claude.com/en/articles/11145838 |
| **Usage Limits** | https://support.claude.com/en/articles/8324991 |
| **Free Account** | https://support.claude.com/en/articles/8602283 |
| **API Key Env Vars** | https://support.claude.com/en/articles/12304248 |
| **Pricing** | https://claude.ai/pricing |

### Community Resources

- **ClaudeLog:** https://claudelog.com/faqs/claude-code-release-notes/
- **Shipyard Cheatsheet:** https://shipyard.build/blog/claude-code-cheat-sheet/
- **DevHints:** https://devhints.io/claude-code

### GitHub Issues Rilevanti

- **#9699:** ANTHROPIC_API_KEY conflict prompts auth
- **#9515:** Conflict warning when env var set

---

## 7. RACCOMANDAZIONI

### Per il Nostro Uso (CervellaSwarm)

**Scenario Attuale:**
- Rafa ha account Pro/Max
- Uso quotidiano intenso
- Multiple sessioni simultanee (Regina + Workers)

**Opzione A: Subscription Max 20x ($200/mese)**
- PRO: Costi fissi prevedibili, no surprise billing
- PRO: 200-800 prompt CLI ogni 5 ore
- PRO: Switch facile Sonnet/Opus 4.5
- CON: Usage condivisa web+CLI
- CON: Limiti potrebbero essere stretti per sciame

**Opzione B: API Key (BYOK)**
- PRO: No limiti fissi
- PRO: Pay solo ciò che usi
- PRO: Perfetto per CI/CD e automazione
- PRO: Ogni worker può avere session separata
- CON: Costi variabili
- CON: Richiede monitoring attivo spesa

**Opzione C: Hybrid (Pro per Regina, API per Workers)**
- PRO: Regina usa subscription (interactive)
- PRO: Workers usano API keys (batch/automation)
- PRO: Best of both worlds
- CON: Gestione più complessa
- CON: Due sistemi billing da monitorare

### Decisione Suggerita

**RACCOMANDAZIONE: Opzione C (Hybrid)**

**Rationale:**
1. Regina (uso interattivo): Max 20x subscription
   - Conversazioni con Rafa
   - Decision making
   - Coordinamento sciame

2. Workers (automazione): API Keys separate
   - Background tasks
   - Parallel processing
   - No impatto su usage Regina

3. Fallback: Se API costa troppo, Max 20x può servire anche workers
   - 200-800 prompt ogni 5 ore potrebbero bastare
   - Monitora primo mese

**Prossimi Step:**
1. Verifica account attuale Rafa (Pro o Max?)
2. Setup ANTHROPIC_API_KEY per testing worker isolation
3. Monitor usage 1 settimana per baseline
4. Decide definitivo basato su dati reali

---

## 8. FAQ CRITICHE

### Q: Posso usare stesso account per più processi Claude Code paralleli?

**A:** SÌ, ma condividono usage limit. Con subscription, tutti i processi contano verso stesso pool (es. 200-800 prompt/5h per Max 20x totali, non per processo).

Con API key separata per processo, nessun limite condiviso (paghi tutto).

### Q: Se sono loggato Pro ma imposto ANTHROPIC_API_KEY, cosa succede?

**A:** Claude Code usa API key e API billing. Subscription è ignorata finché API key è settata. `/status` mostra quale metodo è attivo.

### Q: Posso switch tra subscription e API key senza logout?

**A:** NO. Devi:
1. `/logout` se loggato
2. Unset `ANTHROPIC_API_KEY` se presente
3. Riavvia terminale
4. `claude` e scegli nuovo metodo

### Q: Free account può usare API key per accedere Claude Code?

**A:** SÌ! Free account non può usare subscription per CLI, ma se ha API key Anthropic può settare `ANTHROPIC_API_KEY` e usare Claude Code con API billing.

### Q: Usage limit è per user o per macchina?

**A:** Per USER (account). Se login stesso account Pro su 3 laptop, tutti e 3 condividono stesso pool usage.

### Q: Workspace "Claude Code" in Console può creare API keys?

**A:** NO. Workspace "Claude Code" è read-only per keys. Se serve API key, crea altro workspace type in Console.

---

## FONTI

Questa ricerca è basata su documentazione ufficiale Anthropic e fonti verificate:

### Documentazione Ufficiale
- [Set up Claude Code - Claude Code Docs](https://code.claude.com/docs/en/setup)
- [Using Claude Code with your Pro or Max plan | Claude Help Center](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [About Claude's Pro Plan Usage | Claude Help Center](https://support.claude.com/en/articles/8324991-about-claude-s-pro-plan-usage)
- [About Free Claude Usage | Claude Help Center](https://support.claude.com/en/articles/8602283-about-free-claude-usage)
- [Managing API Key Environment Variables in Claude Code | Claude Help Center](https://support.claude.com/en/articles/12304248-managing-api-key-environment-variables-in-claude-code)

### Guide e Tutorial
- [Claude Code for the Rest of Us: Setup Guide & Use Cases](https://www.whytryai.com/p/claude-code-beginner-guide)
- [The Ultimate Claude Code Beginner Guide: Build Your First AI App (2026)](https://futurebrainy.com/blog/the-ultimate-claude-code-beginner-guide-build-your-first-ai-app-2026/)
- [Getting Started with Claude Code: A No-BS Quick Guide](https://fuszti.com/claude-code-setup-guide-2025/)
- [Shipyard | Claude Code CLI Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)

### News & Analysis
- [Anthropic cracks down on unauthorized Claude usage | VentureBeat](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses)
- [Claude devs complain about surprise usage limits • The Register](https://www.theregister.com/2026/01/05/claude_devs_usage_limits/)
- [Claude, Claude API, and Claude Code: What's the Difference?](https://eval.16x.engineer/blog/claude-vs-claude-api-vs-claude-code)

### Community Resources
- [ClaudeLog - Claude Code Pricing](https://claudelog.com/claude-code-pricing/)
- [GitHub Issue #9699 - ANTHROPIC_API_KEY conflict](https://github.com/anthropics/claude-code/issues/9699)
- [GitHub Issue #9515 - API key warning](https://github.com/anthropics/claude-code/issues/9515)

---

**Fine Ricerca**
**Total Time:** ~20 minuti
**Confidence Level:** Alta (fonti ufficiali + verificate)
**Next Action:** Condividere con Regina per decisione setup CervellaSwarm
