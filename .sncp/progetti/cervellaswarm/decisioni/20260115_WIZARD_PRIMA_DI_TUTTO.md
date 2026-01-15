# DECISIONE: Wizard PRIMA di tutto

**Data:** 15 Gennaio 2026
**Sessione:** 218
**Decisore:** Rafa (con supporto Regina)
**Stato:** APPROVATA

---

## LA DOMANDA

> "Wizard PRIMA (8 settimane, differenziale massimo) o MVP base PRIMA (3 settimane)?"

---

## LE OPZIONI VALUTATE

### Opzione A: Wizard Completo PRIMA

```
8 settimane di implementazione:
- 10 domande strategiche
- Session management robusto
- 3-Layer onboarding
- Time-based recaps
- /status, /recap sempre disponibili
- TUTTO come da WIZARD STUDY

POI: task execution, altri comandi
```

**Pro:**
- Il wizard È il differenziale - fatto BENE
- "Definisci progetto UNA VOLTA" = il nostro USP
- Nessun competitor ha questo
- Qualità massima dal giorno 1

**Contro:**
- 8 settimane prima di avere qualcosa di "completo"
- Rischio di over-engineering

### Opzione B: MVP Base PRIMA

```
3 settimane:
- Wizard semplice (5 domande)
- Task execution base
- Status base

POI: migliorare wizard
```

**Pro:**
- Al mercato veloce
- Feedback prima

**Contro:**
- Wizard mediocre = perde differenziale
- Rischio di "buono abbastanza" che non diventa mai ottimo
- First impression conta

---

## LA DECISIONE

```
+================================================================+
|                                                                |
|   DECISIONE: OPZIONE A - WIZARD COMPLETO PRIMA                 |
|                                                                |
|   "Il Wizard NON è una feature. È IL PRODOTTO."                |
|                                                                |
+================================================================+
```

---

## PERCHÉ QUESTA DECISIONE

### 1. Il Wizard È Il Differenziale

```
Cosa ci distingue da Cursor, Copilot, tutti gli altri?

NON è:
❌ Avere più agenti
❌ Essere più veloce
❌ Costare meno

È:
✓ "Definisci il progetto UNA VOLTA. Mai più rispiegare."
✓ Session management che RICORDA
✓ Time-based recaps intelligenti
✓ Costituzione del progetto

Se facciamo wizard mediocre, perdiamo TUTTO il vantaggio.
```

### 2. Prima Impressione Conta

```
Utente prova CervellaSwarm per la prima volta.
La PRIMA cosa che vede è: cervellaswarm init

Se il wizard è:
- Mediocre → "Meh, come tutti gli altri"
- Eccellente → "WOW! Questo è diverso!"

Non c'è seconda occasione per prima impressione.
```

### 3. La Ricerca È Già Fatta

```
WIZARD STUDY = 1526 righe di ricerca
- Best practices da npm init, Rails, Gemini CLI
- 10 domande strategiche definite
- Flusso prima/seconda/terza sessione
- Meccanismo ripresa robusto

La ricerca è FATTA. Ora serve solo IMPLEMENTARE.
Non stiamo inventando - stiamo eseguendo un piano chiaro.
```

### 4. Filosofia "Fatto BENE > Fatto VELOCE"

```
Dalla COSTITUZIONE:

> "Non abbiamo fretta. Vogliamo la PERFEZIONE."
> "Una feature perfetta > Dieci feature mediocri"

Il wizard perfetto È quella feature perfetta.
```

---

## PIANO DI IMPLEMENTAZIONE

```
SETTIMANA 1-2: Foundation
─────────────────────────
- Package npm skeleton
- CLI base con Commander.js
- 10 domande wizard (da WIZARD STUDY)
- Genera COSTITUZIONE.md progetto

SETTIMANA 3-4: Session Management
─────────────────────────────────
- Salvataggio sessioni JSON
- Project auto-detection (cwd based)
- Resume flow base

SETTIMANA 5-6: Re-engagement
────────────────────────────
- Time-based recaps (0h, 1d, 3d, 7d+)
- /status, /recap, /help commands
- Progress dashboard ASCII

SETTIMANA 7-8: Polish
─────────────────────
- Error handling robusto
- Help system completo
- Test su progetti REALI (CervellaSwarm, Miracollo)
- Documentazione

RISULTATO: Wizard PERFETTO come da WIZARD STUDY
```

---

## COSA NON FACCIAMO (per ora)

```
RIMANDATO A DOPO WIZARD:
- cervellaswarm task (esecuzione task)
- Integrazione spawn-workers
- Multi-agent coordination

PERCHÉ:
Il wizard deve essere PERFETTO prima.
Gli utenti devono poter:
1. Inizializzare progetto (wizard)
2. Avere memoria che funziona (session)
3. Riprendere senza ri-spiegare (resume)

SOLO POI aggiungiamo task execution.
```

---

## METRICHE DI SUCCESSO WIZARD

```
WIZARD È "PERFETTO" QUANDO:

[ ] Completamento: >80% utenti finisce wizard
[ ] Tempo: <7 minuti per completare
[ ] Ri-spiegazione: <5% utenti rispiegano progetto
[ ] Ripresa: <30 secondi per riprendere contesto
[ ] NPS: >50 sul wizard specificamente
```

---

## RISCHI E MITIGAZIONI

| Rischio | Prob | Mitigazione |
|---------|------|-------------|
| Over-engineering wizard | Media | Seguire WIZARD STUDY, non inventare |
| 8 settimane sembrano lunghe | Bassa | Split 60/40, ogni giorno un po' |
| Task execution ritarda | Media | È OK - wizard è priorità |

---

## DOCUMENTI CORRELATI

- ricerche/WIZARD_INIZIALE_STUDIO.md - La "bibbia" del wizard
- PRODOTTO_VISIONE_DEFINITIVA.md - Visione prodotto
- SUB_ROADMAP_MVP_FEBBRAIO.md - Timeline dettagliata

---

## CITAZIONE CHIAVE

> **Rafa:** "Il wizard NON è una feature. È IL PRODOTTO."

---

## FIRMA

**Decisione proposta da:** Rafa
**Validata da:** Regina (Cervella)
**Data:** 15 Gennaio 2026

---

*"Definisci il progetto UNA VOLTA. Mai più rispiegare."*
*Questo è il nostro differenziale. Questo è quello che costruiamo.*
