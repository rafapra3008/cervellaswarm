# Decisione da Prendere: BYOK vs Bundled Claude

> Data: 2026-01-09 - Sessione 143
> Status: DA DECIDERE

## La Domanda

Come gestiamo il costo Claude API per gli utenti?

## Opzione A: BYOK (Bring Your Own Key)

**Come funziona:**
- Utente crea account Anthropic
- Utente mette la sua API key
- Utente paga direttamente Anthropic per usage
- Noi vendiamo solo il software ($20/mese)

**Pro:**
- Noi non abbiamo costi API
- Margine 100% sul subscription
- Semplice da implementare (già fatto!)
- Utente ha controllo totale sui costi
- Privacy: noi non vediamo i loro prompt

**Contro:**
- Friction onboarding (utente deve creare account Anthropic)
- Utente paga 2 volte (noi + Anthropic)
- Costo totale utente: $20 + ~$10-50 API = $30-70/mese
- Competitor come Cursor includono tutto

---

## Opzione B: Bundled (Noi Paghiamo Claude)

**Come funziona:**
- Utente paga solo noi ($20/mese)
- Noi paghiamo Anthropic per il loro usage
- Margine = $20 - costo API

**Pro:**
- Onboarding semplice (1 account)
- Prezzo tutto incluso
- Come fanno Cursor, Copilot
- Migliore UX

**Contro:**
- Rischio margine negativo (heavy users)
- Serve rate limiting / fair use policy
- Complessità billing
- Serve capitale per coprire costi API iniziali
- Se Anthropic alza prezzi, siamo fregati

---

## Opzione C: Hybrid

**Come funziona:**
- Free tier: BYOK (utente paga sua API)
- Pro tier: Bundled con limits (es. 1000 task/mese)
- Heavy users: BYOK o Enterprise custom

**Pro:**
- Free tier a costo zero per noi
- Pro tier con margine controllato
- Flessibilità

**Contro:**
- Complessità gestione
- Messaging confuso

---

## Dati da Considerare

### Costo API Anthropic (stima per task)
- Task semplice (Sonnet): ~$0.01-0.05
- Task complesso (Opus): ~$0.10-0.50
- Media stimata: ~$0.05/task

### Break-even Bundled
- Se utente fa 400 task/mese → costo API ~$20 → margine $0
- Se utente fa 200 task/mese → costo API ~$10 → margine $10
- Se utente fa 100 task/mese → costo API ~$5 → margine $15

### Competitor
- Cursor: Bundled con credits ($20 = X premium requests)
- Copilot: Bundled con limits ($10 = unlimited + caps)
- Windsurf: Credits system

---

## Raccomandazione Preliminare

**Per MVP: BYOK**

Perché:
1. Già implementato e funzionante
2. Zero rischio finanziario
3. Possiamo validare prodotto senza preoccuparci di margini
4. Pivot a Bundled dopo se necessario

**Post-PMF: Considera Hybrid o Bundled**

Quando:
1. Abbiamo dati su usage medio
2. Abbiamo capitale per coprire costi
3. Utenti chiedono "tutto incluso"

---

## Prossimi Step

- [ ] Ricerca dettagliata costi API Anthropic
- [ ] Calcolo break-even per vari scenari usage
- [ ] User interviews: preferiscono BYOK o tutto incluso?
- [ ] Decisione finale pre-launch

---

*Decisione critica per il business model - da prendere con dati*
