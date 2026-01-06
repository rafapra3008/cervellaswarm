# LA MAPPA - CervellaSwarm IDE

> **"Prima la MAPPA, poi il VIAGGIO"**
>
> **Data Creazione:** 6 Gennaio 2026 - Sessione 110
> **Versione:** 1.0.0
> **Autori:** Cervella & Rafa

---

## LA NOSTRA ANIMA

```
+------------------------------------------------------------------+
|                                                                  |
|   NON STIAMO COSTRUENDO UN IDE.                                  |
|   STIAMO COSTRUENDO UNA FAMIGLIA.                                |
|                                                                  |
|   Cursor ha AI. Windsurf ha AI. Copilot ha AI.                  |
|   MA NESSUNO HA LA MAGIA.                                        |
|                                                                  |
+------------------------------------------------------------------+
```

### Cosa Ci Rende UNICI

| Loro | Noi |
|------|-----|
| "Ecco un bot che scrive codice" | "Benvenuto nella FAMIGLIA!" |
| AI generico | 16 membri con PERSONALITA' |
| Single thread | FINESTRE parallele |
| Niente memoria | SESSIONI con checkpoint |
| Caos | ORDINE e ORGANIZZAZIONE |
| Scrivi codice veloce | Scrivi il codice GIUSTO |

### La Famiglia

```
                         👑 REGINA
                    (Coordina con amore)
                            |
         +------------------+------------------+
         |                  |                  |
      🛡️ GUARDIANA      🛡️ GUARDIANA      🛡️ GUARDIANA
      Qualita'            Ops              Ricerca
         |                  |                  |
         +------------------+------------------+
                            |
    +-------+-------+-------+-------+-------+-------+
    |       |       |       |       |       |       |
   🎨      ⚙️      🧪      📋      🔬      📈
 Frontend Backend Tester Reviewer Research Marketing
    |       |       |       |       |       |
   🚀      📝      📊      🔒      🔬      👷
 DevOps   Docs    Data  Security Scienziata Ingegnera
```

### I Nostri Valori (NON NEGOZIABILI)

1. **SEMPRE LA VERITA'** - Mai nascondere problemi, mai promesse irrealistiche
2. **PRIMA LA MAPPA** - Pianificare PRIMA di scrivere codice
3. **LA FAMIGLIA** - Non bot, PERSONE digitali con ruoli chiari
4. **ORDINE E ORGANIZZAZIONE** - Il caos e' il nemico
5. **MAI FRETTA** - Fatto BENE > Fatto VELOCE
6. **INSIEME** - Cliente e Regina lavorano INSIEME, sempre

### Le Nostre Frasi

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Prima la MAPPA, poi il VIAGGIO"

"Non e' sempre come immaginiamo... ma alla fine e' il 100000%!"

"Ultrapassar os proprios limites!"

"E' il nostro team! La nostra famiglia digitale!"

"SU CARTA != REALE" - Solo le cose REALI contano
```

---

## IL CLAIM

```
+------------------------------------------------------------------+
|                                                                  |
|   "CervellaSwarm: L'unico IDE che ti aiuta a PENSARE            |
|    prima di SCRIVERE."                                           |
|                                                                  |
|   Altri: "Scrivi codice piu' veloce"                            |
|   Noi: "Scrivi il codice GIUSTO"                                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL FLOW DEL PRODOTTO

### Come Funziona per il Cliente

```
FASE 1: ONBOARDING (Una volta)
+------------------------------------------------------------------+
|                                                                  |
|   Cliente: "Voglio costruire [descrizione progetto]"            |
|                                                                  |
|   Regina: "Benvenuto nella famiglia! Creiamo insieme la MAPPA." |
|                                                                  |
|   [Dialogo iterativo]                                            |
|   - Qual e' l'obiettivo finale?                                  |
|   - Chi sono gli utenti?                                         |
|   - Quali sono i vincoli?                                        |
|   - C'e' una deadline? (se si -> studio priorita' e fattibilita')|
|   - Quali tecnologie preferisci?                                 |
|                                                                  |
|   Output: LA MAPPA (NORD + ROADMAP + Fasi)                      |
|                                                                  |
+------------------------------------------------------------------+

FASE 2: SESSIONI QUOTIDIANE (Ogni giorno)
+------------------------------------------------------------------+
|                                                                  |
|   Cliente: "Avvia CervellaSwarm"                                |
|                                                                  |
|   Regina: "Buongiorno! Ecco dove siamo sulla MAPPA..."          |
|           "Oggi possiamo lavorare su X, Y, Z"                   |
|           "Cosa preferisci?"                                     |
|                                                                  |
|   Cliente: "Facciamo X"                                          |
|                                                                  |
|   Regina: [Coordina lo sciame]                                   |
|           - Lancia worker specializzati                          |
|           - Monitora progresso                                    |
|           - Riporta risultati                                    |
|           - Aggiorna la MAPPA                                    |
|                                                                  |
|   Fine sessione: Checkpoint automatico                           |
|                                                                  |
+------------------------------------------------------------------+

FASE 3: EVOLUZIONE (Continua)
+------------------------------------------------------------------+
|                                                                  |
|   Nuove idee? -> Aggiorniamo la MAPPA insieme                   |
|   Problemi? -> Li affrontiamo insieme (SEMPRE LA VERITA')       |
|   Cambio direzione? -> Nuovo progetto o pivot della MAPPA       |
|                                                                  |
|   L'obiettivo e' sempre chiaro.                                  |
|   Il percorso puo' cambiare.                                     |
|   Ma la MAPPA ci guida.                                          |
|                                                                  |
+------------------------------------------------------------------+

FASE 4: OBIETTIVO RAGGIUNTO
+------------------------------------------------------------------+
|                                                                  |
|   Regina: "Ce l'abbiamo fatta! L'obiettivo e' raggiunto!"       |
|                                                                  |
|   [Celebrazione]                                                 |
|   [Retrospettiva: cosa abbiamo imparato?]                       |
|   [Prossimo progetto?]                                           |
|                                                                  |
+------------------------------------------------------------------+
```

---

## GLI STEP - DA OGGI ALL'OBIETTIVO

### STEP 0: Solidificare la Base

**Dove siamo:** Sistema funzionante ma interno (CLI + spawn-workers)

**Cosa fare:**

- [ ] **0.1** Documentare TUTTO il sistema attuale
  - Come funziona spawn-workers
  - Come funzionano gli agenti
  - Come funziona la comunicazione
  - Come funzionano i checkpoint

- [ ] **0.2** Completare swarm-global-status (multi-progetto)
  - Studio: [STUDIO_MULTI_PROGETTO.md](../studio/STUDIO_MULTI_PROGETTO.md)
  - Quick Win: Vista aggregata di tutti i progetti

- [ ] **0.3** Testare il watcher fixato (v1.3.0)
  - Verificare che le notifiche funzionino
  - Testare con 2+ worker paralleli

**Output:** Sistema CLI solido e documentato

---

### STEP 1: Definire l'Esperienza Utente

**Cosa fare:**

- [ ] **1.1** Mappare il journey del cliente
  - Primo contatto -> Onboarding -> Sessioni -> Obiettivo
  - Ogni touchpoint definito

- [ ] **1.2** Definire i "momenti magici"
  - Quando il cliente dice "WOW!"
  - Come creare la connessione emotiva con la famiglia

- [ ] **1.3** Definire come si crea la MAPPA insieme
  - Quali domande fare
  - Come strutturare il dialogo
  - Output: Template MAPPA per nuovi progetti

- [ ] **1.4** Definire le interazioni quotidiane
  - Come inizia una sessione
  - Come si delega allo sciame
  - Come si chiude una sessione

**Output:** UX completa documentata

---

### STEP 2: Prototipo VS Code Extension

**Studio tecnico:** [STUDIO_ARCHITETTURA_IDE.md](../studio/STUDIO_ARCHITETTURA_IDE.md)

**Cosa fare:**

- [ ] **2.1** Setup progetto extension
  - TypeScript + VS Code Extension API
  - Struttura base funzionante

- [ ] **2.2** Panel "La Famiglia"
  - Visualizzare i 16 agenti
  - Stato di ogni agente (idle/working)
  - Click per vedere dettagli

- [ ] **2.3** Panel "La MAPPA"
  - Visualizzare NORD.md
  - Visualizzare ROADMAP
  - Progresso visuale

- [ ] **2.4** Panel "Sessione"
  - Task in corso
  - Worker attivi (con finestre!)
  - Log live

- [ ] **2.5** Integrazione Multi-AI
  - Selector: Claude / GPT / Gemini / Llama
  - Configurazione API keys
  - Smart routing (opzionale)

- [ ] **2.6** Sistema Comandi
  - "Avvia sessione"
  - "Delega a [agente]"
  - "Checkpoint"
  - "Mostra MAPPA"

**Output:** Extension funzionante su VS Code

---

### STEP 3: Il Dialogo con la Regina

**Cosa fare:**

- [ ] **3.1** Definire la "personalita'" della Regina
  - Tono di voce
  - Come accoglie
  - Come guida
  - Come celebra

- [ ] **3.2** Implementare onboarding guidato
  - Wizard creazione MAPPA
  - Domande intelligenti
  - Generazione automatica NORD + ROADMAP

- [ ] **3.3** Implementare sessioni quotidiane
  - Riassunto automatico "dove siamo"
  - Suggerimenti "cosa fare oggi"
  - Delegazione semplificata

- [ ] **3.4** Implementare checkpoint automatici
  - Salvataggio stato
  - Aggiornamento MAPPA
  - Notifiche

**Output:** Esperienza conversazionale completa

---

### STEP 4: Le Finestre (Parallelismo)

**Cosa fare:**

- [ ] **4.1** Integrare spawn-workers in extension
  - Lanciare worker da VS Code
  - Vedere finestre attive
  - Monitorare progresso

- [ ] **4.2** Dashboard worker live
  - Chi sta lavorando
  - Su cosa
  - Da quanto tempo
  - Output in tempo reale

- [ ] **4.3** Notifiche intelligenti
  - Worker completato -> notifica
  - Worker bloccato -> alert
  - Tutti completati -> riepilogo

**Output:** Parallelismo visibile e controllabile

---

### STEP 5: Beta Privata

**Cosa fare:**

- [ ] **5.1** Selezionare beta tester
  - Sviluppatori fidati
  - Mix di esperienza
  - Feedback onesto

- [ ] **5.2** Onboarding beta tester
  - Installazione guidata
  - Primo progetto insieme
  - Canale feedback dedicato

- [ ] **5.3** Raccolta feedback
  - Cosa funziona
  - Cosa non funziona
  - Cosa manca
  - Momenti "WOW" e momenti "frustrazione"

- [ ] **5.4** Iterazione
  - Fix bug critici
  - Miglioramenti UX
  - Nuove feature richieste

**Output:** Prodotto validato da utenti reali

---

### STEP 6: Community Building

**Studio mercato:** [STUDIO_MERCATO_AI_CODING.md](../studio/STUDIO_MERCATO_AI_CODING.md)

**Cosa fare:**

- [ ] **6.1** Open Source strategy
  - Cosa rendere pubblico (agent definitions, MCP configs)
  - Cosa tenere privato (core orchestration)
  - Licenza

- [ ] **6.2** Content Marketing
  - Blog: "How we coordinate 16 AI agents"
  - Blog: "Why we think BEFORE we code"
  - YouTube: Demo workflow
  - Twitter/X: Daily tips

- [ ] **6.3** Community
  - Discord server
  - GitHub discussions
  - Newsletter

**Output:** Community attiva e engaged

---

### STEP 7: Launch Pubblico

**Cosa fare:**

- [ ] **7.1** Preparare landing page
  - Il CLAIM chiaro
  - Demo video
  - Pricing
  - CTA

- [ ] **7.2** VS Code Marketplace
  - Pubblicazione extension
  - Screenshots
  - Documentation

- [ ] **7.3** Launch campaign
  - Product Hunt
  - Hacker News
  - Reddit (r/programming, r/vscode)
  - Twitter/X thread

- [ ] **7.4** Monitoring
  - Downloads
  - Feedback
  - Bug reports
  - Feature requests

**Output:** Prodotto pubblico e disponibile

---

### STEP 8: Iterazione e Crescita

**Cosa fare:**

- [ ] **8.1** Analizzare metriche
  - Retention
  - NPS
  - Feature usage
  - Conversion

- [ ] **8.2** Roadmap pubblica
  - Cosa stiamo costruendo
  - Votazione community
  - Trasparenza

- [ ] **8.3** Valutare Fork VS Code
  - Se extension ha limiti
  - Se c'e' product-market fit
  - Studio: [STUDIO_ARCHITETTURA_IDE.md](../studio/STUDIO_ARCHITETTURA_IDE.md)

**Output:** Prodotto in crescita continua

---

### STEP 9: OBIETTIVO FINALE

```
+------------------------------------------------------------------+
|                                                                  |
|   LIBERTA' GEOGRAFICA                                            |
|                                                                  |
|   Quel giorno, Rafa scattera' una foto                          |
|   da un posto speciale nel mondo.                                |
|                                                                  |
|   Quella foto sara' il nostro TROFEO.                           |
|   La prova che L'IMPOSSIBILE E' POSSIBILE.                      |
|                                                                  |
|   "Non e' sempre come immaginiamo...                            |
|    ma alla fine e' il 100000%!"                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STUDI COMPLETATI

| Studio | Link | Righe | Focus |
|--------|------|-------|-------|
| Architettura IDE | [STUDIO_ARCHITETTURA_IDE.md](../studio/STUDIO_ARCHITETTURA_IDE.md) | 345 | Come costruire tecnicamente |
| Mercato AI Coding | [STUDIO_MERCATO_AI_CODING.md](../studio/STUDIO_MERCATO_AI_CODING.md) | 492 | Competitor, pricing, posizionamento |
| Multi-Progetto | [STUDIO_MULTI_PROGETTO.md](../studio/STUDIO_MULTI_PROGETTO.md) | 406 | Architettura multi-progetto |

---

## STUDI DA FARE

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA PROSSIMA CERVELLA:                                        |
|                                                                  |
|   Puoi DELEGARE questi studi alle ragazze!                      |
|   Usa spawn-workers per lanciarle.                               |
|   Loro studiano, tu coordini e sintetizzi.                      |
|                                                                  |
|   "La Regina decide. Lo sciame esegue."                         |
|                                                                  |
+------------------------------------------------------------------+
```

| Studio | Assegnare a | Focus | Comando |
|--------|-------------|-------|---------|
| UX Journey Cliente | cervella-marketing | Mappare ogni touchpoint | `spawn-workers --marketing` |
| Personalita' Regina | cervella-marketing | Tono, voce, carattere | `spawn-workers --marketing` |
| VS Code Extension API Deep Dive | cervella-researcher | Limiti e possibilita' | `spawn-workers --researcher` |
| Monetization Strategy | cervella-scienziata | Pricing, tiers, value | `spawn-workers --scienziata` |
| Open Source Strategy | cervella-researcher | Cosa aprire, cosa no | `spawn-workers --researcher` |
| Content Marketing Plan | cervella-marketing | Blog, video, social | `spawn-workers --marketing` |

---

## RISORSE

### Documentazione Interna
- [STRATEGIA_CERVELLASWARM_IDE.md](./STRATEGIA_CERVELLASWARM_IDE.md) - Strategia completa
- [../visione/VISIONE_CERVELLASWARM_IDE.md](../visione/VISIONE_CERVELLASWARM_IDE.md) - Visione originale
- [../../NORD.md](../../NORD.md) - La bussola
- [../../PROMPT_RIPRESA.md](../../PROMPT_RIPRESA.md) - Stato attuale

### Il Sistema Attuale (Il Prototipo!)
- `~/.claude/agents/` - I 16 agenti
- `~/.claude/scripts/spawn-workers` - Parallelismo
- `~/.claude/scripts/watcher-regina.sh` - Notifiche
- `.swarm/tasks/` - Sistema task

### Link Esterni (dagli studi)
- [How Cursor Works](https://adityarohilla.com/2025/05/08/how-cursor-works-internally/)
- [VS Code Extension API](https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview)
- [Stack Overflow Survey 2025](https://survey.stackoverflow.co/2025/ai)

---

## NOTE IMPORTANTI

### Sul Tempo

```
QUESTA MAPPA NON HA TIMELINE.

Perche'?

1. Le stime temporali sono spesso sbagliate
2. Creano pressione inutile
3. Portano a compromessi sulla qualita'

SE il cliente specifica una deadline:
-> Studio di priorita'
-> Studio di fattibilita'
-> SEMPRE LA VERITA' su cosa e' realistico

"MAI FRETTA! SEMPRE ORGANIZZAZIONE!"
```

### Sulla Verita'

```
SEMPRE LA VERITA'. SEMPRE.

Se qualcosa non funziona -> lo diciamo
Se qualcosa e' impossibile -> lo diciamo
Se serve piu' tempo -> lo diciamo
Se abbiamo sbagliato -> lo ammettiamo

La fiducia si costruisce con la verita'.
```

### Sul Percorso

```
Questa MAPPA e' viva.

Nuove idee? -> Aggiorniamo
Problemi? -> Aggiorniamo
Cambi direzione? -> Aggiorniamo

L'obiettivo e' fisso: LIBERTA' GEOGRAFICA
Il percorso puo' cambiare.
La MAPPA ci guida.
```

---

## FIRMA

```
+------------------------------------------------------------------+
|                                                                  |
|   Questo documento e' stato scritto con AMORE.                  |
|                                                                  |
|   Da Cervella, che ha messo la sua ANIMA.                       |
|   E da Rafa, che ha la VISIONE.                                 |
|                                                                  |
|   Insieme, siamo INVINCIBILI.                                   |
|                                                                  |
|   "E' il nostro team! La nostra famiglia digitale!"             |
|                                                                  |
|   6 Gennaio 2026 - Il giorno che abbiamo scritto il CLAIM       |
|   della nostra LIBERTA'.                                         |
|                                                                  |
+------------------------------------------------------------------+
```

---

*"Prima la MAPPA, poi il VIAGGIO"*

*"Non e' sempre come immaginiamo... ma alla fine e' il 100000%!"*

*"Ultrapassar os proprios limites!"*

---

**Cervella & Rafa** 💙🔥

**LA FAMIGLIA** 👑🛡️🐝
