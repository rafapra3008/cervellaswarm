# SUBROADMAP - Famiglia Completa MCP

> **Creata:** 17 Gennaio 2026 - Sessione 252
> **Obiettivo:** Portare tutti i 16 agenti nel MCP Server pubblico

---

## IL SEGRETO

```
+================================================================+
|   LE GUARDIANE = IL NOSTRO DIFFERENZIATORE!                    |
|                                                                |
|   Nessun altro tool AI ha:                                     |
|   - Guardiane che VERIFICANO il lavoro                         |
|   - Sistema gerarchico Regina → Guardiane → Worker             |
|   - Qualità controllata a più livelli                          |
|                                                                |
|   QUESTO CI RENDE UNICI!                                       |
+================================================================+
```

---

## REGOLA D'ORO - COME USARE LE GUARDIANE

```
+================================================================+
|   QUANDO HAI DUBBI → CHIEDI ALLA GUARDIANA!                    |
+================================================================+
|                                                                |
|   Le Guardiane sbloccano SEMPRE:                               |
|                                                                |
|   - Confrontare codice       → "È fatto bene?"                 |
|   - Verificare opinioni      → "È la scelta giusta?"           |
|   - Validare idee            → "Ha senso?"                     |
|   - Controllare qualità      → "Standard 9.5 minimo!"          |
|                                                                |
|   STANDARD ALTO = 9.5 MINIMO                                   |
|                                                                |
+================================================================+
```

### Quando Usare Quale Guardiana

| Situazione | Guardiana | Cosa Chiede |
|------------|-----------|-------------|
| Dubbi su codice/qualità | guardiana-qualita | "Verifica questo codice" |
| Dubbi su ricerca/info | guardiana-ricerca | "Verifica questa ricerca" |
| Dubbi su deploy/ops | guardiana-ops | "Verifica questo deploy" |

### Esempio di Uso

```
PRIMA (senza Guardiana):
  "Faccio questo codice... spero sia giusto"
  → Errori, refactoring, tempo perso

DOPO (con Guardiana):
  "Guardiana, verifica questo approccio"
  → Feedback, correzioni, fatto BENE la prima volta

RISULTATO: Standard 9.5+ sempre!
```

---

## STATO ATTUALE

```
MCP Server v0.1.2 - 8 worker:
  [x] backend      Python, FastAPI, API, Database
  [x] frontend     React, CSS, Tailwind, UI/UX
  [x] tester       Testing, Debug, QA
  [x] docs         Documentation, README, Guides
  [x] devops       Deploy, CI/CD, Docker
  [x] data         SQL, Analytics, Database Design
  [x] security     Security Audit, Vulnerabilities
  [x] researcher   Research, Analysis, Best Practices
```

---

## DA AGGIUNGERE (8 membri)

### Worker Mancanti (4)

| Worker | Specialty | Priorità |
|--------|-----------|----------|
| marketing | UX strategy, positioning, copywriting | ALTA |
| ingegnera | Architecture, refactoring, tech debt | ALTA |
| scienziata | Market research, competitor analysis | MEDIA |
| reviewer | Code review, best practices | MEDIA |

### Guardiane (3) - IL SEGRETO!

| Guardiana | Ruolo | Priorità |
|-----------|-------|----------|
| guardiana-qualita | Verifica output, standard codice | CRITICA |
| guardiana-ricerca | Verifica qualità ricerche | ALTA |
| guardiana-ops | Supervisiona deploy, security | ALTA |

### Regina (1)

| Agente | Ruolo | Priorità |
|--------|-------|----------|
| orchestrator | Coordina tutti, delega task | CRITICA |

---

## FASI IMPLEMENTAZIONE

### FASE 1: Worker Mancanti
```
1. Aggiungere marketing al spawner
2. Aggiungere ingegnera al spawner
3. Aggiungere scienziata al spawner
4. Aggiungere reviewer al spawner
5. Test ogni worker
6. npm publish
```

### FASE 2: Guardiane
```
1. Definire come le Guardiane verificano
2. Implementare guardiana-qualita
3. Implementare guardiana-ricerca
4. Implementare guardiana-ops
5. Test sistema di verifica
6. npm publish
```

### FASE 3: Regina/Orchestrator
```
1. Definire logica orchestrazione
2. Implementare orchestrator
3. Test flusso completo
4. npm publish v1.0.0
```

---

## MARKETING ANGLE

```
PRIMA (ora):
  "8 specialized AI agents"

DOPO (famiglia completa):
  "16 AI agents with quality guardians"
  "The only AI team that checks its own work"
  "Built-in code review and quality assurance"
```

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| DNA Famiglia | `docs/DNA_FAMIGLIA.md` |
| MCP Server | `packages/mcp-server/` |
| Spawner | `packages/mcp-server/src/agents/spawner.ts` |

---

*"Le Guardiane = il nostro segreto!"*
*"Fatto BENE > Fatto VELOCE"*
