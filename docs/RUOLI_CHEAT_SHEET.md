# RUOLI CHEAT SHEET - CervellaSwarm

> **Chi fa COSA nella nostra famiglia di 16 Cervelle**
> Aggiornato: 14 Gennaio 2026 - Sessione 201

---

## GERARCHIA

```
+================================================================+
|                                                                |
|   LIVELLO 1: REGINA (1)                                        |
|   +-- cervella-orchestrator (Opus) - Coordina TUTTO            |
|                                                                |
|   LIVELLO 2: GUARDIANE (3) - Opus                              |
|   +-- guardiana-qualita   - Valida output agenti               |
|   +-- guardiana-ops       - Deploy, infra, sicurezza           |
|   +-- guardiana-ricerca   - Valida qualita ricerche            |
|                                                                |
|   LIVELLO 3: WORKER (12) - Sonnet                              |
|   +-- backend, frontend, data, tester, reviewer                |
|   +-- researcher, scienziata, ingegnera                        |
|   +-- devops, security, docs, marketing                        |
|                                                                |
+================================================================+
```

---

## QUANDO USARE CHI

### RICERCA (prima di implementare)

| Agente | Quando Usare | Esempio |
|--------|--------------|---------|
| **Researcher** | Ricerca TECNICA | "Come funziona IndexedDB?" "Best practices FastAPI" |
| **Scienziata** | Ricerca BUSINESS | "Come fanno i competitor?" "Trend mercato 2026" |

```
RICORDA:
- Researcher = COME fare tecnicamente
- Scienziata = COSA fare strategicamente
```

### IMPLEMENTAZIONE

| Agente | Quando Usare | Tecnologie |
|--------|--------------|------------|
| **Backend** | API, database, logica | Python, FastAPI, PostgreSQL, SQL |
| **Frontend** | UI, componenti, stile | React, TypeScript, Tailwind, CSS |
| **Data** | Query complesse, analytics | SQL, ETL, report, ottimizzazioni DB |

### QUALITA E REVIEW

| Agente | Quando Usare | Output |
|--------|--------------|--------|
| **Tester** | Scrivere test, debugging | Test suite, bug report |
| **Reviewer** | Code review, best practices | Suggerimenti, fix |
| **Guardiana Qualita** | Validare PRIMA di merge | Score /10, GO/NO-GO |

### INFRASTRUTTURA

| Agente | Quando Usare | Scope |
|--------|--------------|-------|
| **DevOps** | Deploy, Docker, CI/CD | Infra, automazione |
| **Security** | Audit sicurezza | Vulnerabilita, compliance |
| **Guardiana Ops** | Validare deploy critici | Verifica pre-produzione |

### ANALISI E DOCUMENTAZIONE

| Agente | Quando Usare | Output |
|--------|--------------|--------|
| **Ingegnera** | Mappare codebase, tech debt | Audit, refactor plan |
| **Docs** | Documentazione, guide | README, tutorial |
| **Marketing** | UX strategy, posizionamento | Design specs, user flow |

---

## FLUSSO CORRETTO

### Per Feature Nuova

```
1. Scienziata    --> "Come fanno i competitor?"
2. Researcher    --> "Quale tecnologia usare?"
3. Marketing     --> "Dove metterla nella UI?"
4. Backend/Frontend --> Implementa
5. Tester        --> Testa
6. Guardiana     --> Valida e approva
```

### Per Bug Fix

```
1. Ingegnera     --> "Dove sta il problema?" (se non chiaro)
2. Backend/Frontend --> Fix
3. Tester        --> Verifica fix
4. Guardiana     --> Valida
```

### Per Deploy

```
1. Tester        --> Test completo
2. Guardiana Qualita --> Score >= 9.0
3. DevOps        --> Prepara deploy
4. Guardiana Ops --> GO finale
5. DevOps        --> Esegui deploy
```

---

## REGOLE D'ORO

### 1. Regina Orchestra, Non Fa Tutto

```
MAI: Regina implementa direttamente
SI:  Regina delega e coordina

WORKFLOW:
Regina --> Esperta (specs) --> Worker (implementa) --> Guardiana (valida)
```

### 2. Researcher vs Scienziata

```
RESEARCHER (tecnica):
- "Come implementare WebSocket?"
- "Best practices caching"
- "Pattern React 19"

SCIENZIATA (business):
- "Cosa fanno Superhuman/Gmail?"
- "Trend email client 2026"
- "Gap analysis competitor"
```

### 3. Guardiane = Gate

```
NESSUN deploy senza Guardiana Ops
NESSUN merge senza Guardiana Qualita (per feature critiche)
NESSUNA ricerca senza Guardiana Ricerca (per decisioni strategiche)
```

### 4. Livelli di Rischio

```
RISCHIO 1 (BASSO): Docs, fix minori
--> Worker procede autonomamente

RISCHIO 2 (MEDIO): Feature, refactor
--> Guardiana verifica prima di merge

RISCHIO 3 (ALTO): Deploy, auth, dati
--> Guardiana + Rafa approvano
```

---

## TOOLS PER AGENTE

| Agente | Read | Edit | Bash | Web | Task |
|--------|:----:|:----:|:----:|:---:|:----:|
| Orchestrator | Y | Y | Y | Y | Y |
| Guardiana Qualita | Y | Y | - | - | Y |
| Guardiana Ops | Y | - | Y | - | Y |
| Guardiana Ricerca | Y | - | - | Y | Y |
| Backend | Y | Y | Y | Y | - |
| Frontend | Y | Y | Y | Y | - |
| Data | Y | Y | Y | Y | - |
| Researcher | Y | - | - | Y | - |
| Scienziata | Y | - | - | Y | - |
| Tester | Y | Y | Y | Y | - |
| Reviewer | Y | - | - | Y | - |
| DevOps | Y | Y | Y | Y | - |
| Security | Y | - | - | Y | - |
| Docs | Y | Y | - | Y | - |
| Marketing | Y | - | - | Y | - |
| Ingegnera | Y | - | Y | - | - |

---

## ESEMPI PRATICI

### "Voglio aggiungere dark mode"

```
1. Scienziata   --> Come fanno i competitor? (ricerca mercato)
2. Marketing    --> Dove mettere toggle? UX best practices
3. Researcher   --> CSS custom properties vs Tailwind dark? (ricerca tecnica)
4. Frontend     --> Implementa con specs di Marketing
5. Tester       --> Test visual + accessibility
6. G. Qualita   --> Review finale
```

### "L'API e lenta"

```
1. Ingegnera    --> Profile e trova bottleneck
2. Researcher   --> Best practices ottimizzazione (se serve)
3. Backend      --> Implementa fix
4. Tester       --> Benchmark before/after
5. G. Qualita   --> Valida miglioramento
```

### "Dobbiamo fare deploy"

```
1. Tester       --> Suite completa PASS
2. G. Qualita   --> Score >= 9.0
3. DevOps       --> Checklist deploy
4. G. Ops       --> GO finale
5. DevOps       --> Deploy + rollback plan
```

---

*"La Regina orchestra, NON fa tutto da sola!"*
*"Consultare l'esperta PRIMA di implementare"*

*Sessione 201 - 14 Gennaio 2026*
