# Mappa Implementazione Completa

> **Data:** 9 Gennaio 2026
> **Sessione:** 134
> **Obiettivo:** Capire TUTTO quello che serve per implementare LA NOSTRA STRADA

---

## LA DOMANDA DI RAFA

```
"Abbiamo ricercato.. definito.. ora manca implementare tutto!"
"Come faremmo per noi e tutti i progetti?"
"Git clones non li abbiamo neanche provati.. non so come funziona"
```

---

## MAPPA COMPLETA: COSA SERVE

### 1. CONTEXT OPTIMIZATION

| Cosa | Stato | Serve |
|------|-------|-------|
| Template CLAUDE.md progetto snello | DA FARE | Creare template 40 linee |
| Template CLAUDE.md globale snello | DA FARE | Creare template 180 linee |
| Template PROMPT_RIPRESA snello | DA FARE | Creare formato 80 linee |
| Benchmark script | DA FARE | Script per misurare token |
| Guida migrazione | DA FARE | Come passare da vecchio a nuovo |

### 2. MULTI-SESSIONE (Git Clones)

| Cosa | Stato | Serve |
|------|-------|-------|
| Capire come funziona | DA FARE | Spiegazione per Rafa |
| Script crea-clones | PARZIALE | Esiste ma mai usato da Rafa |
| Workflow documentato | DA FARE | Step by step pratico |
| Test pratico | DA FARE | Rafa deve provare |

**NOTA:** Nella sessione 133 abbiamo creato:
- `~/Developer/CervellaSwarm-regina-A`
- `~/Developer/CervellaSwarm-regina-B`

Ma Rafa non ha mai interagito direttamente con loro!

### 3. PER LA FAMIGLIA (16 membri)

| Cosa | Stato | Serve |
|------|-------|-------|
| DNA aggiornato con regola 5 min | DA FARE | Ogni agente deve sapere |
| DNA con istruzioni SNCP | DA FARE | Come usare memoria esterna |
| DNA con context awareness | DA FARE | Non sprecare token |
| Verifica coerenza DNA | DA FARE | Tutti allineati |

**I 16 membri:**
- Regina (orchestrator)
- 3 Guardiane (qualita, ops, ricerca)
- 12 Worker (frontend, backend, tester, reviewer, researcher, scienziata, ingegnera, marketing, devops, docs, data, security)

### 4. HOOKS E TRIGGERS

| Cosa | Stato | Serve |
|------|-------|-------|
| Hook startup (context leggero) | DA VERIFICARE | Carica solo essenziale |
| Hook checkpoint | DA FARE | Salva automatico a 70-80% |
| Hook chiusura | DA FARE | PROMPT_RIPRESA snello |
| Trigger "spawn-workers" | ESISTE | Ma va documentato meglio |
| Trigger "checkpoint" | ESISTE | Ma va snellito |

### 5. PER OGNI PROGETTO

| Cosa | Stato | Serve |
|------|-------|-------|
| CLAUDE.md progetto snello | DA FARE per ogni progetto | CervellaSwarm, Miracollo, Contabilita |
| .sncp/ configurato | PARZIALE | CervellaSwarm ok, altri? |
| PROMPT_RIPRESA snello | DA FARE per ogni progetto | Migrare formato |
| Git clones setup | DA FARE per ogni progetto | Se servono |

### 6. GLOBALE (~/.claude/)

| Cosa | Stato | Serve |
|------|-------|-------|
| CLAUDE.md snello | DA FARE | Da 527 a ~180 linee |
| COSTITUZIONE.md | NON TOCCARE | Resta com'e |
| Agents DNA aggiornati | DA FARE | Tutti i 16 membri |
| Settings ottimizzati | DA VERIFICARE | MCP, permissions, ecc |

---

## DIPENDENZE: COSA PRIMA DI COSA

```
LIVELLO 0 (prerequisiti):
├── Capire git clones (Rafa deve capire)
├── Decidere se servono davvero
└── Template pronti

LIVELLO 1 (fondamenta):
├── CLAUDE.md progetto CervellaSwarm snello
├── Benchmark before/after
└── Test che funziona

LIVELLO 2 (espansione):
├── CLAUDE.md globale snello
├── PROMPT_RIPRESA snello template
└── DNA famiglia aggiornati

LIVELLO 3 (automazione):
├── Hooks checkpoint
├── Script git clones (se servono)
└── Watcher migliorato

LIVELLO 4 (rollout):
├── Applicare a Miracollo
├── Applicare a Contabilita
└── Documentazione finale
```

---

## DOMANDE APERTE

1. **Git clones servono davvero?**
   - Nella sessione 133 li abbiamo testati MA
   - Rafa non li ha mai usati
   - Forse il Task tool interno basta per il 90% dei casi?

2. **Quanti progetti toccare?**
   - CervellaSwarm (test)
   - Miracollo (produzione)
   - Contabilita (secondario)
   - Tutti insieme o uno alla volta?

3. **DNA famiglia: aggiornare tutti o solo alcuni?**
   - 16 membri sono tanti
   - Forse iniziare con i piu usati?

4. **Hooks: quali servono DAVVERO?**
   - Startup hook gia esiste
   - Checkpoint automatico serve?
   - O basta trigger manuale?

---

## STIMA EFFORT

| Blocco | Complessita | Sessioni stimate |
|--------|-------------|------------------|
| Template + benchmark | Bassa | 1 sessione |
| CLAUDE.md snello test | Media | 1-2 sessioni |
| DNA famiglia | Alta | 2-3 sessioni |
| Hooks/automazione | Media | 1-2 sessioni |
| Rollout altri progetti | Media | 2-3 sessioni |
| **TOTALE** | - | **7-11 sessioni** |

---

## COSA MANCA ANCORA

1. **Decisione su git clones** - Li usiamo o no?
2. **Priorita** - Cosa prima?
3. **Chi fa cosa** - Regina coordina, ma chi implementa?
4. **Test plan** - Come verifichiamo che funziona?

---

*Questa mappa serve per capire la PORTATA del lavoro*
