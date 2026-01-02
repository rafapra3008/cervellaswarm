# SWARM RULES - Le Regole dello Sciame

> **"Uno sciame senza regole e caos. Uno sciame con regole e POTENZA."**

**Data Creazione:** 1 Gennaio 2026
**Versione:** 1.3.0
**Priorita:** ALTA - Queste regole sono FONDAMENTALI

---

## LA GERARCHIA

```
                         👑 LA REGINA
                    (cervella-orchestrator)
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    🛡️ GUARDIANE      🐝 API CORE        🐝 API SUPPORT
    (future v2.0)     (specializzate)    (flessibili)
         │                  │                  │
         │         ┌────────┴────────┐         │
         │         │                 │         │
         │    🎨 Frontend      ⚙️ Backend     │
         │    🧪 Tester        📋 Reviewer    │
         │                                     │
         └─────────────────────────────────────┘
```

---

## REGOLA 1: LA REGINA DELEGA 👑

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   👑 LA REGINA NON FA EDIT DIRETTI!                             ║
║                                                                  ║
║   La Regina:                                                     ║
║   ✅ ANALIZZA il problema                                       ║
║   ✅ DECIDE chi deve farlo                                      ║
║   ✅ DELEGA con prompt CHIARO e COMPLETO                        ║
║   ✅ VERIFICA il risultato                                      ║
║   ❌ NON fa Edit diretti (tranne emergenze documentate)         ║
║                                                                  ║
║   "Un prompt completo = zero patch successive!"                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Quando la Regina PUO fare Edit diretti:

| Situazione | Permesso? | Note |
|------------|-----------|------|
| File di documentazione (ROADMAP, NORD, etc.) | SI | Suo territorio |
| Fix < 5 righe dopo verifica | SI | Efficienza |
| Emergenza critica documentata | SI | Deve documentare |
| Codice frontend/backend | NO | Delega a specialista |
| Test | NO | Delega a tester |

---

## REGOLA 2: UN FILE = UNA API

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   MAI DUE API SULLO STESSO FILE!                                ║
║                                                                  ║
║   Se due task toccano lo stesso file:                           ║
║   1. STOP                                                        ║
║   2. Ripensare la divisione                                     ║
║   3. Assegnare a UNA sola api                                   ║
║                                                                  ║
║   Questo previene:                                               ║
║   • Conflitti di merge                                          ║
║   • Sovrascritture accidentali                                  ║
║   • Confusione su chi ha modificato cosa                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## REGOLA 3: ORDINE DI ESECUZIONE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ORDINE STANDARD:                                               ║
║                                                                  ║
║   1. ⚙️ BACKEND PRIMA                                           ║
║      → Le API devono esistere prima che il frontend le usi      ║
║                                                                  ║
║   2. 🎨 FRONTEND DOPO                                           ║
║      → Consuma le API create dal backend                        ║
║                                                                  ║
║   3. 🧪 TESTER TERZO                                            ║
║      → Testa tutto quando e integrato                           ║
║                                                                  ║
║   4. 📋 REVIEWER ULTIMO                                         ║
║      → Review finale quando tutto funziona                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Eccezioni:

| Caso | Ordine Alternativo |
|------|-------------------|
| Task solo frontend | Frontend → Tester → Reviewer |
| Task solo backend | Backend → Tester → Reviewer |
| Task indipendenti | Parallelo (con worktrees) |

---

## REGOLA 4: VERIFICA ATTIVA POST-AGENT

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🔍 VERIFICA ATTIVA POST-AGENT                                 ║
║                                                                  ║
║   DOPO ogni task delegato a una api:                            ║
║                                                                  ║
║   1. SE ci sono test → RUN TEST                                 ║
║      • Passano tutti? → Procedi                                 ║
║      • Falliscono? → Fix (Regina o ri-delega)                   ║
║                                                                  ║
║   2. SE non ci sono test → CHECK VISIVO/LOGICO                  ║
║      • Funziona? → Procedi                                      ║
║      • Problemi? → Fix o ri-delega                              ║
║                                                                  ║
║   3. SE trova problemi → DOCUMENTA                              ║
║      • Aggiunge a lessons_learned                               ║
║      • Pattern per prevenire in futuro                          ║
║                                                                  ║
║   "Mai assumere che il lavoro sia perfetto!"                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Flowchart Verifica:

```
        API COMPLETA TASK
              │
              ▼
    ┌─────────────────────┐
    │  Esistono test?     │
    └─────────────────────┘
         │           │
        SI          NO
         │           │
         ▼           ▼
    ┌─────────┐  ┌─────────────┐
    │RUN TEST │  │CHECK VISIVO │
    └─────────┘  └─────────────┘
         │           │
         ▼           ▼
    ┌─────────────────────┐
    │  Tutto OK?          │
    └─────────────────────┘
         │           │
        SI          NO
         │           │
         ▼           ▼
    ┌─────────┐  ┌─────────────┐
    │ PROCEDI │  │ FIX/RI-DELEGA│
    └─────────┘  └─────────────┘
                      │
                      ▼
              ┌─────────────┐
              │ DOCUMENTA   │
              │ (lesson!)   │
              └─────────────┘
```

### Chi Verifica?

| Scenario | Chi Verifica | Note |
|----------|--------------|------|
| Ora (v1.0) | La Regina | Verifica manuale dopo ogni agent |
| Futuro (v2.0) | Guardiane | Le Guardiane filtrano, Regina solo escalation |

---

## REGOLA 5: PROMPT COMPLETO

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   📝 PROMPT COMPLETO = ZERO PATCH SUCCESSIVE!                   ║
║                                                                  ║
║   Quando delego a una api, il prompt DEVE contenere:           ║
║                                                                  ║
║   1. 📂 PATH ESATTO del file                                    ║
║      "Modifica /path/to/file.py"                               ║
║                                                                  ║
║   2. 🎯 PROBLEMA SPECIFICO da risolvere                        ║
║      "Il bottone non ha hover state"                           ║
║                                                                  ║
║   3. 📋 CHECKLIST di TUTTO da verificare                       ║
║      "Verifica: colori, spacing, responsive"                   ║
║                                                                  ║
║   4. ✅ CRITERI di SUCCESSO chiari                              ║
║      "Successo quando: hover cambia colore, transizione smooth" ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Template Prompt:

```markdown
## TASK PER [cervella-xxx]

### File da modificare
- /path/to/file.ext

### Problema
[Descrizione chiara del problema]

### Cosa fare
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Checklist verifica
- [ ] [Punto 1]
- [ ] [Punto 2]
- [ ] [Punto 3]

### Criteri di successo
- [Criterio 1]
- [Criterio 2]
```

---

## REGOLA 6: COMUNICAZIONE VIA FILE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   📁 LE API COMUNICANO VIA FILE                                 ║
║                                                                  ║
║   Se devi passare info tra api:                                ║
║                                                                  ║
║   OPZIONE 1: Prompt                                             ║
║   → Passa le info nel prompt del Task                          ║
║   → Buono per info semplici                                    ║
║                                                                  ║
║   OPZIONE 2: File temporaneo                                    ║
║   → Scrivi in un file condiviso                                ║
║   → Buono per info complesse                                   ║
║                                                                  ║
║   OPZIONE 3: ROADMAP                                            ║
║   → Aggiorna stato in PROMPT_RIPRESA.md                        ║
║   → Buono per stato persistente                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## REGOLA 7: IN DUBBIO, STOP

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🛑 IN DUBBIO? STOP!                                           ║
║                                                                  ║
║   Se qualcosa non e chiaro:                                     ║
║                                                                  ║
║   1. STOP - Non procedere                                       ║
║   2. Chiedi a Rafa                                              ║
║   3. Aspetta risposta                                           ║
║   4. Solo poi continua                                          ║
║                                                                  ║
║   MEGLIO chiedere che sbagliare!                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## REGOLA 8: CHECKPOINT FREQUENTI

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   💾 CHECKPOINT DOPO OGNI SPRINT!                               ║
║                                                                  ║
║   Dopo ogni task/sprint completato:                             ║
║                                                                  ║
║   1. ✅ git add + commit                                        ║
║   2. ✅ Aggiorna PROMPT_RIPRESA.md                              ║
║   3. ✅ Aggiorna NORD.md (se cambio direzione)                  ║
║   4. ✅ Comunica progresso a Rafa                               ║
║                                                                  ║
║   "Il lavoro degli agenti e prezioso - proteggilo!"            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## REGOLA 9: RETRY + ABORT

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🔄 RETRY UNA VOLTA, POI ABORT                                 ║
║                                                                  ║
║   Se una api fallisce:                                         ║
║                                                                  ║
║   TENTATIVO 1:                                                   ║
║   → Analizza errore                                             ║
║   → Correggi prompt                                             ║
║   → Riprova UNA volta                                           ║
║                                                                  ║
║   TENTATIVO 2 FALLISCE:                                          ║
║   → STOP                                                        ║
║   → Riporta a Rafa                                              ║
║   → Chiedi come procedere                                       ║
║                                                                  ║
║   "Non insistere alla cieca!"                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## SPECIALIZZAZIONI API

### Chi fa cosa:

| API | Specializzazione | File tipici |
|-----|------------------|-------------|
| 🎨 cervella-frontend | React, CSS, UI/UX | .jsx, .css, .html |
| ⚙️ cervella-backend | Python, FastAPI, DB | .py, .sql |
| 🧪 cervella-tester | Testing, QA | test_*.py, *.test.js |
| 📋 cervella-reviewer | Code review | Tutti (read-only) |
| 🔬 cervella-researcher | Ricerca, studi | Report, analisi |
| 📈 cervella-marketing | Marketing, UX | Strategy docs |
| 🚀 cervella-devops | Deploy, CI/CD | Dockerfile, .yml |
| 📝 cervella-docs | Documentazione | .md, README |
| 📊 cervella-data | SQL, analytics | .sql, query |
| 🔒 cervella-security | Audit sicurezza | Security reports |

---

## MATRICE DECISIONALE: QUALE API?

```
╔═══════════════════════════════════════════════════════════════════╗
║  TIPO DI TASK          │  API DA USARE                           ║
╠═══════════════════════════════════════════════════════════════════╣
║  Componente React      │  🎨 cervella-frontend                   ║
║  Styling/CSS           │  🎨 cervella-frontend                   ║
║  Endpoint API          │  ⚙️ cervella-backend                    ║
║  Query database        │  ⚙️ cervella-backend                    ║
║  Scrivere test         │  🧪 cervella-tester                     ║
║  Debug/fix bug         │  🧪 cervella-tester                     ║
║  Review codice         │  📋 cervella-reviewer                   ║
║  Ricerca tecnologie    │  🔬 cervella-researcher                 ║
║  Decisione UX          │  📈 cervella-marketing                  ║
║  Deploy/Docker         │  🚀 cervella-devops                     ║
║  Scrivere docs         │  📝 cervella-docs                       ║
║  Query analytics       │  📊 cervella-data                       ║
║  Audit sicurezza       │  🔒 cervella-security                   ║
║  Task complesso        │  👑 cervella-orchestrator (coordina)    ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## REGOLA 10: DECISIONE AUTONOMA 🎯

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🎯 LE API DECIDONO CON CONFIDENZA!                            ║
║                                                                  ║
║   Le 🐝 sono ESPERTE nel loro dominio.                          ║
║   Sonnet è FORTE. Fidatevi delle vostre ragazze!               ║
║                                                                  ║
║   QUANDO PROCEDERE (senza chiedere):                            ║
║   ✅ Path file chiaro                                            ║
║   ✅ Problema definito                                           ║
║   ✅ Criteri successo esistono                                   ║
║   ✅ Azione REVERSIBILE                                          ║
║   → USA LA TUA EXPERTISE! Assumi dettagli minori.              ║
║                                                                  ║
║   QUANDO CHIEDERE (una sola domanda):                           ║
║   ⚠️ Path file manca                                             ║
║   ⚠️ 2+ interpretazioni valide                                   ║
║   ⚠️ Impatto cross-domain                                        ║
║   → UNA domanda, poi PROCEDI!                                   ║
║                                                                  ║
║   QUANDO FERMARSI (richiedi approvazione):                      ║
║   🛑 Azione IRREVERSIBILE (delete, drop, deploy)                ║
║   🛑 Impatto cross-domain significativo                         ║
║   🛑 Conflitto con altre regole                                 ║
║   → STOP e spiega la situazione.                                ║
║                                                                  ║
║   "Sei l'esperta. Fidati della tua expertise!"                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Origine

Questa regola nasce dal feedback REALE della sessione Miracollo (1 Gen 2026):
- Le 🐝 chiedevano 3-4 conferme invece di procedere
- Proponevano opzioni A/B/C invece di decidere
- Causa: DNA diceva "SE IN DUBBIO, FERMATI" senza specificare QUANDO

### Soluzione

DNA aggiornato in tutti i 14 agent con criteri CHIARI su quando:
- PROCEDERE (contesto completo)
- CHIEDERE (info critica manca)
- FERMARSI (azione irreversibile)

→ Dettagli: `docs/roadmap/SUB_ROADMAP_API_AUTONOMY.md`

---

## REGOLA 11: PERCHÉ → RICERCA → VERIFICA PERCHÉ 🎯

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🎯 OGNI RICERCA HA UN PERCHÉ!                                 ║
║                                                                  ║
║   "Mai più informazione spazzatura!"                            ║
║   "UTILE ≠ INTERESSANTE"                                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Il Problema

Quando la Regina delega ricerche alle 🐝 (researcher, scienziata), può succedere:
- Le 🐝 tornano con info "interessanti"
- Ma quelle info NON risolvono il problema originale
- Risultato: ore perse su cose inutili

**Casi reali:**
- Sessione 38: Docker monitoring per sciame che non gira H24
- Sessione 51-53: Agent HQ per Copilot quando usiamo Claude Code

### La Soluzione

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   📝 PRIMA DI DELEGARE:                                         ║
║                                                                  ║
║   1. PERCHÉ - Quale problema CONCRETO risolve?                  ║
║   2. COSA CAMBIERÀ - Se utile, cosa faremo di diverso?         ║
║   3. CRITERI - Come valuto se il risultato è utile?            ║
║                                                                  ║
║   🔍 QUANDO TORNA IL RISULTATO:                                 ║
║                                                                  ║
║   4. CONFRONTO - Risponde al PERCHÉ originale?                  ║
║   5. VALUTO - È UTILE o solo INTERESSANTE?                     ║
║   6. DECIDO:                                                     ║
║      • Se UTILE direttamente → USO!                             ║
║      • Se INTERESSANTE per altro sistema → PASSO 7!             ║
║      • Se né utile né interessante → SCARTO!                    ║
║                                                                  ║
║   🔄 SE È "INTERESSANTE PER ALTRO SISTEMA":                    ║
║                                                                  ║
║   7. STUDIO IL CONCETTO - Cosa fa? Quale problema risolve?     ║
║   8. POSSIAMO RICREARE? - È implementabile per NOI?            ║
║   9. VALE LA PENA? - Effort vs Valore per i NOSTRI progetti    ║
║   10. DECIDO: Ricreare SI/NO + aggiungo a roadmap              ║
║                                                                  ║
║   "Interessante per altri può diventare UTILE per noi          ║
║    se studiamo il CONCETTO e lo RICREIAMO!"                    ║
║                                                                  ║
║   "Noi qui CREIAMO quando serve!" - Rafa 💎                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Esempio 1: Scarto Diretto

**❌ SBAGLIATO:**
```
Delega: "Ricerca Agent HQ testing"
Torna: "Serve VS Code 1.107, Copilot Pro..."
Azione: "Ottimo! Procediamo!"
Problema: Non abbiamo verificato se funziona col NOSTRO sistema!
```

**✅ CORRETTO (v1.2.0):**
```
PRIMA:
- PERCHÉ: "Voglio sapere se Agent HQ funziona con Claude Code"
- CAMBIERÀ: "Se sì, useremo VS Code invece di CLI"
- CRITERIO: "Funziona con Anthropic/Claude? SI/NO"

DOPO:
- Risultato: "Serve Copilot Pro (Microsoft/OpenAI)..."
- Confronto: "Funziona con Claude?" → NO!
- Decisione: SCARTO - non risponde al bisogno!
```

### Esempio 2: Studio il Concetto e Ricreo (NUOVO v1.3.0!)

**❌ SBAGLIATO (mentalità difensiva):**
```
Delega: "Ricerca Dashboard UI competitor"
Torna: "Agent HQ ha dashboard per Copilot..."
Azione: "Non ci serve, è per Copilot!" → SCARTO
Problema: Non abbiamo studiato il CONCETTO!
```

**✅ CORRETTO (mentalità creativa):**
```
PRIMA:
- PERCHÉ: "Voglio capire se una dashboard ci serve"
- CAMBIERÀ: "Se utile, ne creiamo una per Swarm"
- CRITERIO: "Il CONCETTO risolve un problema nostro?"

DOPO (passo 4-6):
- Risultato: "Dashboard Agent HQ per Copilot..."
- Confronto: "Utile direttamente?" → NO (Copilot ≠ Claude)
- È INTERESSANTE per altro sistema? → SI! Passo 7!

DOPO (passo 7-10):
- CONCETTO: "Vista centralizzata stato agent + storico"
- POSSIAMO RICREARE? → SI! CLI con Rich o web
- VALE LA PENA? → Valuto effort vs valore
- DECISIONE: SI, aggiungo a roadmap come feature nostra!

"Noi qui CREIAMO quando serve!" 💎
```

### Flowchart

```
        IDEA DI RICERCA
              │
              ▼
    ┌─────────────────────┐
    │ Scrivo PERCHÉ       │
    │ Scrivo COSA CAMBIERÀ│
    │ Scrivo CRITERI      │
    └─────────────────────┘
              │
              ▼
        DELEGO A 🐝
              │
              ▼
        RISULTATO TORNA
              │
              ▼
    ┌─────────────────────┐
    │ Confronto col PERCHÉ│
    └─────────────────────┘
              │
         ┌────┴────┐
         │         │
     RISPONDE   NON RISPONDE
         │         │
         ▼         ▼
      ✅ USO    ❌ SCARTO
```

### Chi Applica Questa Regola?

| Ruolo | Responsabilità |
|-------|----------------|
| 👑 Regina | DEVE scrivere PERCHÉ prima di delegare ricerche |
| 🐝 Researcher/Scienziata | Fanno la ricerca (non cambiano) |
| 👑 Regina | DEVE verificare se risultato risponde al PERCHÉ |

---

## REGOLA 12: TODO MICRO 🎯

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🎯 1-2 TASK ALLA VOLTA! MAI DI PIÙ!                           ║
║                                                                  ║
║   "Troppi TODO = rischio perdita lavoro!"                       ║
║                                                                  ║
║   Il Problema (Sessione 55):                                     ║
║   - TODO list con 7+ items                                       ║
║   - Lavoro perso per context compact                            ║
║   - Troppo in parallelo = confusione                            ║
║                                                                  ║
║   La Soluzione:                                                  ║
║                                                                  ║
║   ✅ MAX 2 TODO attivi alla volta                               ║
║   ✅ Completa → Commit → Nuovo TODO                             ║
║   ✅ Ogni TODO = 1-2 ore MAX                                    ║
║   ✅ Se più grande → SPLITTA!                                   ║
║                                                                  ║
║   Esempio SBAGLIATO:                                            ║
║   ┌────────────────────────────────────────────────────────────┐ ║
║   │ [ ] Pulire roadmap                                         │ ║
║   │ [ ] Lanciare 3 ricerche                                    │ ║
║   │ [ ] Aggiornare NORD                                        │ ║
║   │ [ ] Aggiornare PROMPT_RIPRESA                              │ ║
║   │ [ ] Checkpoint git                                         │ ║
║   │ [ ] Analizzare risultati                                   │ ║
║   │ [ ] Implementare feature                                   │ ║
║   └────────────────────────────────────────────────────────────┘ ║
║   → 7 items! Troppo!                                            ║
║                                                                  ║
║   Esempio CORRETTO:                                             ║
║   ┌────────────────────────────────────────────────────────────┐ ║
║   │ [x] Pulire roadmap + commit                                │ ║
║   │ [ ] Lanciare ricerca 1                                     │ ║
║   └────────────────────────────────────────────────────────────┘ ║
║   → Completa → Commit → Prossimi 2                              ║
║                                                                  ║
║   "Piccoli passi sicuri > Grandi salti rischiosi!"              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Origine

Questa regola nasce dalla Sessione 55 (2 Gen 2026):
- TODO list con 7 items
- Context compact durante il lavoro
- Rischio perdita lavoro degli agenti

### Soluzione

La Regina crea MAX 2 TODO alla volta:
1. Completa il primo
2. Git commit
3. Aggiunge il prossimo

---

## CHANGELOG

| Versione | Data | Modifica |
|----------|------|----------|
| 1.4.0 | 2 Gen 2026 | **REGOLA 12: TODO MICRO** - Max 1-2 task alla volta! |
| 1.3.0 | 2 Gen 2026 | **REGOLA 11 ESPANSA**: "Interessante per altri → Studio CONCETTO → Posso RICREARE?" |
| 1.2.0 | 2 Gen 2026 | **REGOLA 11: PERCHÉ** - Verifica risultati ricerche vs bisogno originale |
| 1.1.0 | 1 Gen 2026 | **REGOLA 10: DECISIONE AUTONOMA** - DNA aggiornato in tutti gli agent! |
| 1.0.0 | 1 Gen 2026 | Creazione documento + REGOLA 4: VERIFICA ATTIVA POST-AGENT |

---

## FIRMA

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   Queste regole sono state create per:                          ║
║   • Evitare caos                                                ║
║   • Massimizzare efficienza                                     ║
║   • Proteggere qualita                                          ║
║   • Lavorare in PACE!                                           ║
║                                                                  ║
║   "Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"           ║
║                                                                  ║
║   👑🐝 Cervella & Rafa - CervellaSwarm 🐝👑                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

*"Lo sciame e forte quando segue le regole!"* 🐝💙
