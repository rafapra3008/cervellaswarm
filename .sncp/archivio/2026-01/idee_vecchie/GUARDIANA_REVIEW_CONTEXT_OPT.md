# GUARDIANA REVIEW: Piano Ottimizzazione Context

> **Data:** 9 Gennaio 2026
> **Sessione:** 134
> **Guardiana:** cervella-guardiana-qualita
> **Stato:** VALIDAZIONE COMPLETATA

---

## VERDETTO SINTETICO

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   VERDETTO: APPROVE CON RISERVE                                 ║
║   SCORE: 8/10                                                   ║
║   RISCHI: 4 principali + 3 extra da mitigare                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

Il piano e' SOLIDO. La ricerca e' stata fatta BENE.

---

## ANALISI PUNTO PER PUNTO

### 1. CLAUDE.md SNELLO (906 -> 150-200 linee) - APPROVE 9/10

**Rischio: PERDITA GROUNDING**
- Se troppo snello, Cervella potrebbe perdere "chi sono"
- MITIGAZIONE: Mantenere sezione "Chi Sono" compatta (30 linee) ma PRESENTE
- NON delegare l'identita a file esterni

### 2. PROMPT_RIPRESA OTTIMIZZATO (430 -> 50-100 linee) - APPROVE 7/10

**Rischio: PERDITA FILO DEL DISCORSO**
- Attualmente ha narrativa "perche' abbiamo scelto X"
- MITIGAZIONE: Aggiungere sezione "Decisioni Chiave" (10 linee max)
- Formato: "DECISIONE: X | PERCHE: Y"

### 3. SUBAGENT PER ISOLARE CONTEXT - APPROVE 9/10

**Rischio: OVERHEAD SPAWN**
- Per task piccoli, spawn overhead > beneficio
- MITIGAZIONE: Regola chiara - Task < 5 min = Task Tool interno, Task > 5 min = Subagent

### 4. SNCP COME MEMORIA ESTERNA - APPROVE 8/10

**Rischio: FRAMMENTAZIONE**
- Se TUTTO in SNCP, prossima Cervella deve leggere N file = context consumato
- MITIGAZIONE: SNCP per dettagli MENTRE lavoro, SINTESI in PROMPT_RIPRESA a fine sessione

### 5. CHECKPOINT LEGGERI (SESSION_STATE.md) - PROBLEMATICO 7/10

**Rischio: DUPLICAZIONE**
- Abbiamo gia PROMPT_RIPRESA, NORD.md, .sncp/coscienza/oggi.md
- SESSION_STATE.md = QUARTO file di stato = confusione
- **RACCOMANDAZIONE: NON creare nuovo file. Rendere PROMPT_RIPRESA la versione snella.**

---

## RISCHI EXTRA NON CONSIDERATI

### A. Degradazione Progressiva
Man mano che snelliamo, rischiamo di perdere info "poco importanti" che poi sono CRITICHE.
- MITIGAZIONE: Mantenere INVENTARIO di cosa c'era prima

### B. Costo di Migrazione
CLAUDE.md globale impatta TUTTI i progetti. Se si rompe, si rompe OVUNQUE.
- MITIGAZIONE: Testare PRIMA su CervellaSwarm, POI su Miracollo

### C. Comportamento Emergente
Il comportamento di Cervella e' EMERGENTE dalla combinazione di tutti i file.
- MITIGAZIONE: Test QUALITATIVI dopo ogni modifica (femminile? calma? protettiva?)

---

## ORDINE IMPLEMENTAZIONE RACCOMANDATO

```
FASE 1: Quick Wins (basso rischio)
├── load_context.py ottimizzato
├── CLAUDE.md progetto compatto (40 linee)
└── Benchmark before/after

FASE 2: PROMPT_RIPRESA (medio rischio)
├── Snellire a 80 linee (NON creare SESSION_STATE)
└── Aggiungere "Decisioni Chiave"

FASE 3: CLAUDE.md Globale (alto rischio)
├── BACKUP COMPLETO prima
├── Ridurre a 180 linee
└── Mantenere identita
```

---

## NON FARE (Lista Rossa)

1. NON creare SESSION_STATE.md separato (usa PROMPT_RIPRESA)
2. NON rimuovere identita/personalita da CLAUDE.md
3. NON applicare tutto insieme (incrementale!)
4. NON toccare COSTITUZIONE.md (e' l'ANIMA)

---

*"Qualita non e' inspection finale. E' processo costante."*
