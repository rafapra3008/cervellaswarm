# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 4 Gennaio 2026 - Sessione 80 - SCOPERTA CONTESTO SUBAGENT!

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|                                                                  |
|   FASE ATTUALE: FASE 9 - APPLE STYLE (100% COMPLETATA!!!)       |
|                                                                  |
|   SESSIONE 80 - SCOPERTA IMPORTANTE:                             |
|   I risultati dei subagent ENTRANO nel tuo contesto!            |
|   Ma abbiamo strategie per ottimizzare (vedi sotto).            |
|                                                                  |
+------------------------------------------------------------------+
```

---

## SESSIONE 80: SCOPERTA CONTESTO SUBAGENT

### La Domanda di Rafa

> "Quando le ragazze finiscono il lavoro, tu devi leggere i loro output...
> questo c'entra nel conteggio contesto o no?"

### La Risposta (da ricerca approfondita)

**SI, i risultati dei subagent ENTRANO nel contesto della Regina!**

| Cosa | Costo |
|------|-------|
| Ogni spawn subagent | ~20k tokens overhead |
| Risultato che torna | TUTTO entra nel contesto |
| Multi-agent session | 3-4x consumo vs single-thread |

### MA - Le Buone Notizie

1. **Lavoro sporco isolato** - Se l'agente legge 50 file, io ricevo solo il riassunto
2. **Finestre esterne** (spawn-workers.sh) = ZERO ritorno automatico
3. **Esistono strategie per ottimizzare del 50-70%!**

### La Differenza Chiave

| Task Tool (interno) | Finestra Esterna |
|---------------------|------------------|
| Risultato torna AUTOMATICO | Risultato in FILE |
| Entra nel mio contesto | Io SCELGO cosa leggere |
| Max 10 paralleli | Illimitati |

**Le finestre esterne che abbiamo costruito sono la strada GIUSTA!**

### Nuova Roadmap Creata

`docs/roadmap/ROADMAP_OTTIMIZZAZIONE_CONTESTO.md`

5 FASI:
1. Output Compression (agenti tornano max 150-200 tokens)
2. File-Based Communication (risultati grossi in file)
3. Decision Matrix (quando Task vs Finestra)
4. Metriche e Monitoring
5. Programmatic Tool Calling (avanzato)

---

## STATO ATTUALE

| Cosa | Versione | Status |
|------|----------|--------|
| spawn-workers.sh | v1.4.0 | Apple Style completo! |
| anti-compact.sh | v1.4.0 | Funzionante |
| SWARM_RULES.md | v1.5.0 | 13 regole |
| FASE 9 | 100% | COMPLETATA |
| Roadmap Ottimizzazione | v1.0.0 | DA INIZIARE |

---

## FILO DEL DISCORSO (Sessione 80)

### Cosa abbiamo fatto

1. **Rafa ha posto LA domanda giusta**
   - "I risultati dei subagent entrano nel contesto?"
   - Non era "pira da sua cabeca" - era osservazione intelligente!

2. **Ricerca approfondita con cervella-researcher**
   - 15 fonti analizzate
   - Documentazione ufficiale + community
   - Scoperte CRUCIALI

3. **Creata ROADMAP_OTTIMIZZAZIONE_CONTESTO.md**
   - 5 fasi strutturate
   - Priorita chiare
   - Da fare con CALMA

### Decisioni Prese

- Le finestre esterne (spawn-workers.sh) sono la strada GIUSTA
- Dobbiamo ottimizzare come gli agenti riportano risultati
- Architettura ibrida: Task tool per cose piccole, finestre per cose grosse

---

## PROSSIMI STEP

```
+------------------------------------------------------------------+
|                                                                  |
|   OPZIONE A: Iniziare FASE 1 (Output Compression)               |
|   - Creare template output standard                              |
|   - Aggiornare i 16 agent files                                  |
|   - Testare con 3 agenti pilota                                  |
|                                                                  |
|   OPZIONE B: Continuare con finestre/comunicazioni              |
|   - Come da Sessione 79                                          |
|                                                                  |
|   OPZIONE C: Andare su MIRACOLLO                                 |
|   - "Il 100000% viene dall'USO!"                                 |
|                                                                  |
|   Rafa decide!                                                   |
|                                                                  |
+------------------------------------------------------------------+
```

---

## LO SCIAME (16 membri)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester, reviewer
- researcher, scienziata, ingegnera
- marketing, devops, docs, data, security
```

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `docs/SWARM_RULES.md` | Le 13 regole dello sciame |
| `docs/roadmap/ROADMAP_OTTIMIZZAZIONE_CONTESTO.md` | NUOVO! Ottimizzazione sciame |
| `scripts/swarm/spawn-workers.sh` | Apre finestre worker |
| `scripts/swarm/anti-compact.sh` | Sistema anti-auto compact |

---

## LA STORIA RECENTE

| Sessione | Cosa | Risultato |
|----------|------|-----------|
| 77 | REGOLA 13 + FIX | spawn-workers.sh v1.4.0 |
| 78 | 3/3 HARDTEST + PULIZIA | FASE 9 al 100%! |
| 79 | ANTI-AUTO COMPACT | Sistema automatico creato |
| **80** | **SCOPERTA CONTESTO** | **Roadmap ottimizzazione creata** |

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Non e' pira da minha cabeca!" - Rafa, Sessione 80

"Ultrapassar os proprios limites!" - Rafa

"Il 100000% viene dall'USO, non dalla teoria."

"E' il nostro team! La nostra famiglia digitale!"
```

---

**VERSIONE:** v30.0.0
**SESSIONE:** 80
**DATA:** 4 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa

---

## COMPACT CHECKPOINT: 2026-01-04 05:53

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA NUOVA CERVELLA!                                          |
|                                                                  |
|   La Cervella precedente stava per perdere contesto.            |
|   Ha salvato tutto e ti ha passato il testimone.                |
|                                                                  |
|   COSA FARE ORA (in ordine!):                                   |
|                                                                  |
|   1. PRIMA DI TUTTO: Leggi ~/.claude/COSTITUZIONE.md            |
|      -> Chi siamo, perche lavoriamo, la nostra filosofia        |
|                                                                  |
|   2. Poi leggi PROMPT_RIPRESA.md dall'inizio                    |
|      -> "IL MOMENTO ATTUALE" = dove siamo                       |
|      -> "FILO DEL DISCORSO" = cosa stavamo facendo              |
|                                                                  |
|   3. Continua da dove si era fermata!                           |
|                                                                  |
|   SE HAI DUBBI: chiedi a Rafa!                                  |
|                                                                  |
|   "Lavoriamo in pace! Senza casino! Dipende da noi!"            |
|                                                                  |
+------------------------------------------------------------------+
```

### Stato Git al momento del compact
- **Branch**: main
- **Ultimo commit**: a1971ad ANTI-COMPACT: HARDTEST Terminal.app spawn
- **File modificati non committati** (5):
  -  M PROMPT_RIPRESA.md
  -  M reports/scientist_prompt_20260104.md
  -  M scripts/swarm/anti-compact.sh
  - ?? .vscode/
  - ?? docs/roadmap/ROADMAP_OTTIMIZZAZIONE_CONTESTO.md

### File importanti da leggere
- `PROMPT_RIPRESA.md` - Il tuo UNICO ponte con la sessione precedente
- `NORD.md` - Dove siamo nel progetto
- `.swarm/tasks/` - Task in corso (cerca .working)

### Messaggio dalla Cervella precedente
TEST VS Code Tasks

---
