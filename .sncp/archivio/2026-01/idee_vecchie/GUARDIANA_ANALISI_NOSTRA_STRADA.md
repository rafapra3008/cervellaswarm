# Analisi Guardiana - LA NOSTRA STRADA

> **Data:** 9 Gennaio 2026
> **Sessione:** 134
> **Guardiana:** cervella-guardiana-qualita
> **Tipo:** Scambio idee strategico

---

## VERDETTO SINTETICO

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   LA STRADA E' SEMPLICE                                         ║
║                                                                  ║
║   1. Ottimizzare context (in corso)                             ║
║   2. Stabilizzare 2-3 worker (in corso)                         ║
║   3. NON aggiungere tool finche' non SERVONO davvero            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## ANALISI PUNTO PER PUNTO

### 1. GitButler vs Git Clones

**Raccomandazione: MANTENIAMO GIT CLONES**
- Funzionano
- Zero complessita' aggiunta
- Non dipendono da tool terzi
- GitButler e' overengineering per i nostri volumi

### 2. ccswitch vs Nostro Pattern

**Raccomandazione: MANTENIAMO IL NOSTRO**
- Gia' testato nella Sessione 133
- Path chiari in ~/Developer/
- Zero curve di apprendimento
- Se servono 10+ sessioni, valutiamo ccswitch. Non oggi.

### 3. Quante Sessioni Parallele?

**Raccomandazione: 2-3 PER ORA, MASSIMO 4**
- 2-3 = gestibili con watcher + SNCP
- 4+ = richiede automazione piu' sofisticata
- Scalare DOPO che 2-3 sono STABILI

### 4. Task Tool vs Sessioni Esterne

**Regola dei 5 Minuti RAFFINATA:**

```
TASK TOOL INTERNO quando:
- Task < 5 minuti
- Read/Grep/Analisi veloce
- Output piccolo (< 500 token)
- Non modifica file

SESSIONE ESTERNA quando:
- Task > 5 minuti
- Modifica codice
- Output grande
- Task che potrebbe "espandersi"

⚠️ ATTENZIONE: Se Regina compatta, subagent PERDE il lavoro!
```

---

## L'ARCHITETTURA FINALE

```
ARCHITETTURA IBRIDA SEMPLICE

1. REGINA (Opus) - Coordina, SNCP, decisioni
   - Context ottimizzato (target -60%)
   - Usa Task tool per query veloci
   - Spawna worker per lavoro vero

2. WORKER ESTERNI (Sonnet) - Eseguono
   - Git clones separati (pattern attuale)
   - Massimo 2-3 paralleli
   - Watcher per notifiche

3. GUARDIANE (Opus) - Verificano
   - Solo quando serve review qualita'
   - Non sempre attive

FLUSSO:
Regina -> Task tool (quick) oppure spawn-workers (lavoro)
Worker -> .done -> Watcher -> notifica -> Regina verifica
```

---

## COSA FARE SUBITO vs DOPO

### SUBITO (Sessione 134)
1. Finalizzare CLAUDE.md snello
2. Documentare regola "Task tool vs Spawn" CHIARA
3. NON aggiungere nuovi tool

### PROSSIME 2-3 SESSIONI
1. Testare CLAUDE.md snello su CervellaSwarm
2. Stabilizzare pattern 2-3 worker paralleli
3. Migliorare watcher se necessario

### DOPO (1+ settimana)
1. SE 2-3 worker sono stabili, valutare 4
2. SE serve scaling, valutare ccswitch
3. MAI GitButler (troppa complessita')

---

## SCORE COMPLESSITA' vs BENEFICIO

| Tool | Complessita' | Beneficio | Decisione |
|------|--------------|-----------|-----------|
| GitButler | 7/10 | 3/10 | NO |
| ccswitch | 4/10 | 2/10 | NON ORA |
| Nostro pattern | 2/10 | 8/10 | SI |

---

## DUBBI SOLLEVATI

1. **Watcher affidabile?** Testare di piu'
2. **SNCP troppo frammentato?** Rischio context consumato per leggere
3. **Stiamo overcomplicando?** Boris ha 5-10+ MA senza Regina

---

*"Semplicita' prima di tutto."*
