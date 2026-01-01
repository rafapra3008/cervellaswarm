# Learning Wizard - Documentazione Lezioni CervellaSwarm

**Versione:** 1.0.0
**Data:** 2026-01-01

---

## 🎯 SCOPO

Il Learning Wizard è un'interfaccia CLI guidata per documentare lezioni apprese durante lo sviluppo. Permette di creare lezioni di qualità in 3 minuti, salvandole nel database Swarm Memory per riutilizzo futuro.

---

## 🚀 UTILIZZO

### Esecuzione Base

```bash
cd /Users/rafapra/Developer/CervellaSwarm
python3 scripts/learning/wizard.py
```

### Esempio Interattivo

```
🧙 CervellaSwarm Learning Wizard v1.0.0
------------------------------------------------------------

Step 1/9: TEMPLATE
Che tipo di lezione è?
  1. Bug Fix
  2. Refactoring
  3. Integrazione API/Service
  4. Custom (vuoto)
Scegli numero []: 1

Step 2/9: TRIGGER
Quando si applica questa lezione?
Trigger [Quando si incontra bug simile a: {bug_type}]: ...

[continua per tutti i 9 step]
```

---

## 📋 I 9 STEP DEL WIZARD

| Step | Campo | Descrizione |
|------|-------|-------------|
| 1 | **TEMPLATE** | Tipo di lezione (Bug Fix, Refactor, Integration, Custom) |
| 2 | **TRIGGER** | Quando si applica questa lezione? |
| 3 | **CONTEXT** | Contesto (task, agente, situazione) |
| 4 | **PROBLEM** | Cosa è andato storto? |
| 5 | **ROOT CAUSE** | Perché è successo? (causa radice) |
| 6 | **SOLUTION** | Come è stato risolto? |
| 7 | **PREVENTION** | Come prevenire in futuro? |
| 8 | **EXAMPLE** | Esempio concreto (opzionale) |
| 9 | **METADATA** | Severity, Agents, Tags, Pattern |

---

## 🎨 INTERFACCIA

Il wizard usa la libreria **Rich** per un'interfaccia elegante:
- Panel colorati per header
- Markdown rendering per preview
- Prompt interattivi con default

**Fallback:** Se Rich non è disponibile, usa interfaccia standard (print/input).

---

## 💾 SALVATAGGIO

Il wizard salva la lezione in due modi:

1. **Database** (primario): `data/swarm_memory.db` → tabella `lessons_learned`
2. **Backup JSON** (fallback): `data/lesson_<ID>.json` (solo se DB fallisce)

---

## 🧪 TEST

Il wizard include test automatici completi:

```bash
python3 scripts/learning/test_wizard.py
```

**Test eseguiti:**
- Inizializzazione wizard
- Template validi
- Costanti corrette
- Path database
- Struttura lesson
- Metodi implementati
- Fallback mode

---

## 📊 METADATA DELLA LEZIONE

Ogni lezione include:

```python
{
    "id": "uuid",
    "timestamp": "ISO 8601",
    "trigger": "Quando applicare",
    "context": "Contesto",
    "problem": "Problema",
    "root_cause": "Causa radice",
    "solution": "Soluzione",
    "prevention": "Prevenzione",
    "example": "Esempio",
    "severity": "CRITICAL | HIGH | MEDIUM | LOW",
    "agents_involved": ["cervella-frontend", "..."],
    "tags": ["tag1", "tag2"],
    "pattern": "nome-pattern",
    "auto_generated": 0,      # 0 = manuale, 1 = auto
    "confidence": 0.8,        # 0.0-1.0
    "times_applied": 0        # Incrementato all'uso
}
```

---

## 🎯 TEMPLATE DISPONIBILI

### 1. Bug Fix
```
TRIGGER: "Quando si incontra bug simile a: {bug_type}"
PREVENTION: "Verificare {checklist} prima di implementare"
```

### 2. Refactoring
```
TRIGGER: "Quando si refactora componenti di tipo: {component_type}"
PREVENTION: "Test regressione obbligatorio prima e dopo"
```

### 3. Integrazione API/Service
```
TRIGGER: "Quando si integra con: {service_name}"
PREVENTION: "Checklist pre-integrazione: {checklist}"
```

### 4. Custom
```
Template vuoto - parti da zero
```

---

## 🐝 AGENTI DISPONIBILI

Gli agenti che possono essere associati a una lezione:

- `cervella-frontend` (UI/UX)
- `cervella-backend` (API/DB)
- `cervella-tester` (QA)
- `cervella-reviewer` (Code Review)
- `cervella-researcher` (Ricerca)
- `cervella-devops` (Deploy)
- `cervella-docs` (Documentazione)
- `cervella-data` (Analytics)
- `cervella-security` (Audit)
- `cervella-marketing` (Marketing)

---

## ✅ BEST PRACTICES

### Quando Documentare
```
✅ Dopo aver risolto un bug NON ovvio
✅ Dopo aver scoperto un pattern utile
✅ Dopo un refactor importante
✅ Dopo una decisione architetturale
✅ Dopo un errore che non deve ripetersi
```

### Come Scrivere
```
✅ TRIGGER: Chiaro e specifico
✅ PROBLEM: Descrizione concisa
✅ ROOT CAUSE: Analisi profonda (non superficiale!)
✅ SOLUTION: Step-by-step
✅ PREVENTION: Checklist pratica
✅ EXAMPLE: Codice o screenshot
```

### Severity Guidelines
```
CRITICAL  → Blocca produzione, perde dati
HIGH      → Bug grave, impatto significativo
MEDIUM    → Bug minore, workaround disponibile
LOW       → Miglioramento, best practice
```

---

## 🔗 INTEGRAZIONE

Il wizard è parte del **Learning System** di CervellaSwarm:

```
wizard.py → swarm_memory.db → retrieve_lessons.py → Agents
    ↑                              ↓
    └──────── Feedback loop ───────┘
```

**Prossimi passi:**
- Integrazione con retrieval agent
- Auto-suggest lezioni durante sviluppo
- Analytics su lezioni più utilizzate

---

## 📝 FILE CORRELATI

| File | Scopo |
|------|-------|
| `wizard.py` | Wizard interattivo |
| `test_wizard.py` | Test automatici |
| `retrieve_lessons.py` | Recupero lezioni (da implementare) |
| `../data/swarm_memory.db` | Database centrale |

---

## 🎓 FILOSOFIA

```
"Documenta BENE in 3 minuti!" 📝💙

- Non una lista TODO lunga → Wizard guidato rapido
- Non note sparse → Database strutturato
- Non dimenticanze → Sistema persistente
- Non ripetere errori → Memoria collettiva
```

---

*Creato: 1 Gennaio 2026*
*Cervella Backend - CervellaSwarm* 🐝🧙
