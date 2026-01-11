# ROADMAP - Il Prodotto Vero

> **Data:** 9 Gennaio 2026
> **Versione:** 1.0
> **Principio:** Prima COSTRUIRE, poi VENDERE

---

## PANORAMICA

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   FASE A: STUDIARE         [................] 0%                ║
║   FASE B: DECIDERE         [................] 0%                ║
║   FASE C: COSTRUIRE MVP    [................] 0%                ║
║   FASE D: VALIDARE         [................] 0%                ║
║   FASE E: GO TO MARKET     [................] 0%                ║
║                                                                  ║
║   (Le fasi precedenti: Ricerca + Decisioni + Landing = PRONTE)  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## FASE A: STUDIARE

**Obiettivo:** Capire cosa possiamo costruire e come

### A.1 - Studio Claude Code

| Punto | Domanda | Come Rispondere |
|-------|---------|-----------------|
| A.1.1 | Come funziona il sistema agenti? | Documentazione Anthropic |
| A.1.2 | Come si configurano agenti custom? | Test pratici |
| A.1.3 | Quali sono i limiti del Task tool? | Test pratici |
| A.1.4 | Come funziona CLAUDE.md? | Documentazione + test |
| A.1.5 | Si può distribuire una configurazione? | Ricerca |

**Output:** Documento `STUDIO_CLAUDE_CODE.md`

### A.2 - Studio Distribuzione

| Punto | Domanda | Come Rispondere |
|-------|---------|-----------------|
| A.2.1 | Come si crea una CLI npm? | Ricerca + esempi |
| A.2.2 | Come si crea estensione VSCode? | Documentazione VSCode |
| A.2.3 | Esistono progetti simili open source? | GitHub search |
| A.2.4 | Come altri hanno risolto questo problema? | Ricerca |

**Output:** Documento `STUDIO_DISTRIBUZIONE.md`

### A.3 - Studio Mercato Reale

| Punto | Domanda | Come Rispondere |
|-------|---------|-----------------|
| A.3.1 | Chi userebbe questo prodotto? | Riflessione |
| A.3.2 | Quanto pagherebbero? | Benchmark competitor |
| A.3.3 | Quali problemi risolve VERAMENTE? | Lista concreta |
| A.3.4 | Perché NOI e non Cursor/Copilot? | Differenziatori reali |

**Output:** Documento `STUDIO_MERCATO_REALE.md`

---

## FASE B: DECIDERE

**Obiettivo:** Scegliere cosa costruire, con chiarezza cristallina

### B.1 - Decisione Architettura

| Opzione | Descrizione | Pro | Contro |
|---------|-------------|-----|--------|
| A | CLI standalone | Semplice | Richiede Claude Code |
| B | Estensione VSCode | Marketplace | Lock-in |
| C | Web + CLI | Team features | Complesso |
| D | Solo config files | Semplicissimo | Non è prodotto |

**Decisione da prendere:** Quale opzione?

### B.2 - Decisione MVP

| Domanda | Risposta (da decidere) |
|---------|------------------------|
| Cosa INCLUDE il MVP? | ??? |
| Cosa ESCLUDE il MVP? | ??? |
| Quanto tempo per MVP? | ??? |
| Chi testa il MVP? | ??? |

### B.3 - Decisione Nome/Brand

| Domanda | Risposta (da decidere) |
|---------|------------------------|
| Nome finale? | CervellaSwarm? Altro? |
| Dominio? | cervellaswarm.com? Altro? |
| Logo? | Da creare |

**Output:** Documento `DECISIONI_PRODOTTO_FINALE.md`

---

## FASE C: COSTRUIRE MVP

**Obiettivo:** Creare qualcosa che FUNZIONA

### C.1 - Setup Progetto

| Punto | Task |
|-------|------|
| C.1.1 | Creare repository pulito (o usare esistente) |
| C.1.2 | Setup struttura base |
| C.1.3 | README iniziale |
| C.1.4 | .gitignore appropriato |

### C.2 - Core Funzionalità

| Punto | Task | Dipende da |
|-------|------|-----------|
| C.2.1 | Installazione base | Decisione B.1 |
| C.2.2 | Configurazione agenti | C.2.1 |
| C.2.3 | Primo test funzionante | C.2.2 |
| C.2.4 | Iterazione e fix | C.2.3 |

### C.3 - Documentazione Base

| Punto | Task |
|-------|------|
| C.3.1 | README con istruzioni installazione |
| C.3.2 | Guida "Quick Start" |
| C.3.3 | Troubleshooting base |

### C.4 - Test Interno

| Punto | Task |
|-------|------|
| C.4.1 | Test su computer Rafa (pulito) |
| C.4.2 | Fix problemi trovati |
| C.4.3 | Test di nuovo |
| C.4.4 | Documentare processo |

**Output:** MVP funzionante

---

## FASE D: VALIDARE

**Obiettivo:** Confermare che funziona per ALTRI

### D.1 - Test Esterni

| Punto | Task |
|-------|------|
| D.1.1 | Trovare 2-3 tester (amici dev) |
| D.1.2 | Dare istruzioni installazione |
| D.1.3 | Osservare (senza aiutare) |
| D.1.4 | Raccogliere feedback |

### D.2 - Iterazione

| Punto | Task |
|-------|------|
| D.2.1 | Analizzare feedback |
| D.2.2 | Prioritizzare fix |
| D.2.3 | Implementare miglioramenti |
| D.2.4 | Testare di nuovo |

### D.3 - Documentazione Finale

| Punto | Task |
|-------|------|
| D.3.1 | Aggiornare README |
| D.3.2 | Aggiungere FAQ da feedback |
| D.3.3 | Video tutorial (opzionale) |

**Output:** Prodotto validato

---

## FASE E: GO TO MARKET

**Obiettivo:** Ora possiamo vendere perché ESISTE

### E.1 - Preparazione

| Punto | Task |
|-------|------|
| E.1.1 | Aggiornare landing page con prodotto REALE |
| E.1.2 | Screenshot/GIF del prodotto vero |
| E.1.3 | Setup email (Resend) |
| E.1.4 | Setup payment (Stripe) |

### E.2 - Lancio Soft

| Punto | Task |
|-------|------|
| E.2.1 | Early bird a primi 10-50 utenti |
| E.2.2 | Raccogliere feedback |
| E.2.3 | Iterare |

### E.3 - Lancio Pubblico

| Punto | Task |
|-------|------|
| E.3.1 | Annuncio pubblico |
| E.3.2 | Social media |
| E.3.3 | Community building |

---

## COSA È IN PAUSA (ma pronto)

| Cosa | Dove | Quando Riprende |
|------|------|-----------------|
| Landing page | `landing/` | Fase E |
| Marketing plan | `.sncp/idee/MARKETING_VENDITA_MASTER.md` | Fase E |
| Video script | `.sncp/idee/ricerche_prodotto/TEASER_SCRIPT_STORYBOARD.md` | Fase E |
| Ricerche competitor | `.sncp/idee/ricerche_prodotto/` | Già usate |
| Decisioni pricing | `.sncp/memoria/decisioni/PRICING_STRATEGIA.md` | Fase E |

---

## METRICHE SUCCESSO

| Fase | Come Sappiamo che è Fatto |
|------|---------------------------|
| A | 3 documenti studio completati |
| B | Decisioni chiare documentate |
| C | MVP che si installa e funziona |
| D | 2-3 persone lo usano senza aiuto |
| E | Primi pagamenti ricevuti |

---

## PRINCIPI GUIDA

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   1. PRIMA funziona, POI bello                                  ║
║   2. PRIMA provare, POI promettere                              ║
║   3. PRIMA costruire, POI vendere                               ║
║   4. Una cosa alla volta, fatta BENE                            ║
║   5. Se non funziona su altro computer, non è prodotto          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## PROSSIMA AZIONE CONCRETA

**Iniziare da FASE A.1.1:**
> "Come funziona il sistema agenti di Claude Code?"

Ricerca documentazione Anthropic, test pratici, capire i limiti.

---

*"Dobbiamo vedere la cosa vera... averla... provarla...
installarla su altri computer... avere fiducia"*

*- Rafa, 9 Gennaio 2026*
