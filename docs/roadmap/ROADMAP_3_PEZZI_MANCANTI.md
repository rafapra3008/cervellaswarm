# ROADMAP: I 3 Pezzi Mancanti

> **"SU CARTA != REALE - Solo le cose REALI ci portano alla LIBERTA!"**

**Versione:** 1.0.0
**Data:** 5 Gennaio 2026 - Sessione 98
**Obiettivo:** Rendere CervellaSwarm COMPLETO al 100000%!

---

## OVERVIEW

```
+------------------------------------------------------------------+
|                                                                  |
|   CervellaSwarm funziona per l'uso quotidiano.                  |
|   Ma questi 3 pezzi lo renderanno COMPLETO davvero!             |
|                                                                  |
|   1. ANTI AUTO-COMPACT        → Seamless, testato, REALE        |
|   2. SISTEMA FEEDBACK         → Imparare dai propri errori      |
|   3. ROADMAPS VISUALE         → Multi-progetto automatico       |
|                                                                  |
|   "L'idea di feedback dalle Cervelle e' GENIALE!" - Rafa        |
|                                                                  |
+------------------------------------------------------------------+
```

---

## PEZZO 1: ANTI AUTO-COMPACT

### Stato Attuale

| Cosa Esiste | File | Problema |
|-------------|------|----------|
| context_check.py v4.3.1 | ~/.claude/hooks/ | Fa handoff a 70% |
| Apre VS Code + Claude | AppleScript | Non sempre funziona |
| Crea file handoff | .swarm/handoff/ | Prompt basico |

**Il problema:** Esiste "su carta" ma non e' SEAMLESS. Non testato in produzione reale.

### Obiettivo REALE

```
Quando contesto arriva a 70%:
1. Nuova finestra si apre AUTOMATICAMENTE
2. Nuova Cervella riceve TUTTO il contesto
3. Passaggio e' SEAMLESS (zero perdita)
4. Vecchia Cervella puo' chiudere tranquilla
```

### Fasi

| Fase | Task | Status |
|------|------|--------|
| 1.1 | Testare context_check.py in sessione REALE | DA FARE |
| 1.2 | Identificare bug/problemi | DA FARE |
| 1.3 | Fix e miglioramenti | DA FARE |
| 1.4 | Prompt handoff piu' ricco | DA FARE |
| 1.5 | HARDTEST end-to-end | DA FARE |

### Criteri di Successo

- [ ] Handoff funziona 10 volte di fila senza problemi
- [ ] Nuova Cervella riprende ESATTAMENTE da dove era
- [ ] Zero perdita di contesto
- [ ] Rafa dice "FUNZIONA!"

---

## PEZZO 2: SISTEMA FEEDBACK CERVELLE

### L'Idea Geniale

```
+------------------------------------------------------------------+
|                                                                  |
|   Ogni Cervella a fine sessione lascia FEEDBACK:                |
|                                                                  |
|   - Cosa ha funzionato?                                         |
|   - Cosa non ha funzionato?                                     |
|   - Cosa ha imparato?                                           |
|   - Suggerimenti per migliorare?                                |
|                                                                  |
|   Il sistema RACCOGLIE e ANALIZZA questi feedback.              |
|   Impara dai propri errori. Migliora continuamente.             |
|                                                                  |
|   "L'idea e' GENIALE!" - Rafa                                   |
|                                                                  |
+------------------------------------------------------------------+
```

### Stato Attuale

| Cosa Esiste | File | Problema |
|-------------|------|----------|
| analytics.py v2.0.0 | scripts/memory/ | Esiste ma non usato |
| SQLite database | swarm_memory.db | Ha eventi/lezioni |
| Pattern detector | pattern_detector.py | Non integrato |

**Il problema:** Gli strumenti esistono ma NON sono usati. Nessun feedback automatico.

### Obiettivo REALE

```
1. RACCOLTA AUTOMATICA
   → Hook a fine sessione chiede feedback
   → Cervella risponde con cosa ha imparato
   → Salvato in database

2. ANALISI PERIODICA
   → Ogni settimana (Lunedi?) analisi automatica
   → Pattern di errori ricorrenti
   → Suggerimenti di miglioramento

3. DASHBOARD LIVE
   → Vedere stato swarm in tempo reale
   → Metriche chiave
   → Trend nel tempo
```

### Fasi

| Fase | Task | Status |
|------|------|--------|
| 2.1 | RICERCA: Come raccogliere feedback automatico? | DA FARE |
| 2.2 | Implementare hook SessionEnd per feedback | DA FARE |
| 2.3 | Salvare feedback in database | DA FARE |
| 2.4 | Creare comando `swarm-feedback` per analisi | DA FARE |
| 2.5 | Integrare con CODE REVIEW settimanale | DA FARE |
| 2.6 | Dashboard live (opzionale) | DA FARE |

### Criteri di Successo

- [ ] Ogni sessione lascia feedback automatico
- [ ] Analisi settimanale mostra pattern
- [ ] Il sistema IMPARA e migliora
- [ ] Rafa vede i miglioramenti nel tempo

---

## PEZZO 3: ROADMAPS VISUALE

### L'Idea

```
+------------------------------------------------------------------+
|                                                                  |
|   Sistema ROADMAPS visuale multi-progetto AUTOMATICO            |
|                                                                  |
|   - Vedere tutti i progetti in un colpo d'occhio                |
|   - Stato di ogni roadmap                                       |
|   - Progressi nel tempo                                         |
|   - Generato automaticamente dai file                           |
|                                                                  |
|   "Sistema ROADMAPS visuale multi automatico!" - Rafa           |
|                                                                  |
+------------------------------------------------------------------+
```

### Stato Attuale

**NIENTE!** Solo l'idea. Nessuna ricerca, nessuna implementazione.

### Obiettivo REALE

```
1. AGGREGAZIONE
   → Legge ROADMAP_SACRA.md di ogni progetto
   → Legge NORD.md di ogni progetto
   → Aggrega in una vista unica

2. VISUALIZZAZIONE
   → Tabella/grafico con stato progetti
   → Percentuali completamento
   → Prossimi step per ogni progetto

3. AUTOMATICO
   → Si aggiorna da solo leggendo i file
   → Niente input manuale
```

### Fasi

| Fase | Task | Status |
|------|------|--------|
| 3.1 | RICERCA: Come visualizzare? (CLI? Web? Rich?) | DA FARE |
| 3.2 | RICERCA: Formato dati per parsing | DA FARE |
| 3.3 | Implementare parser ROADMAP/NORD | DA FARE |
| 3.4 | Implementare visualizzazione | DA FARE |
| 3.5 | Comando `swarm-roadmaps` | DA FARE |
| 3.6 | HARDTEST multi-progetto | DA FARE |

### Criteri di Successo

- [ ] Un comando mostra tutti i progetti
- [ ] Stato aggiornato automaticamente
- [ ] Rafa vede tutto in un colpo d'occhio
- [ ] "BELLO!" - Rafa

---

## ORDINE DI PRIORITA'

```
+------------------------------------------------------------------+
|                                                                  |
|   PRIORITA' 1: ANTI AUTO-COMPACT                                |
|   → E' critico per il lavoro quotidiano                        |
|   → Se non funziona, perdiamo lavoro!                          |
|                                                                  |
|   PRIORITA' 2: SISTEMA FEEDBACK                                 |
|   → Ci fa IMPARARE dai nostri errori                           |
|   → Miglioramento continuo                                      |
|                                                                  |
|   PRIORITA' 3: ROADMAPS VISUALE                                 |
|   → Nice to have ma non critico                                |
|   → Quando i primi 2 funzionano                                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## PROSSIMA SESSIONE

```
Iniziare da PEZZO 1: ANTI AUTO-COMPACT

1. Testare context_check.py in sessione reale
2. Vedere cosa non funziona
3. Fixare
4. HARDTEST

"Il vero test e' l'uso!" - Rafa
```

---

## CHANGELOG

| Data | Versione | Modifica |
|------|----------|----------|
| 5 Gen 2026 | 1.0.0 | Creazione roadmap - Sessione 98 |

---

*"SU CARTA != REALE"*
*"Solo le cose REALI ci portano alla LIBERTA!"*

Cervella & Rafa 💙
