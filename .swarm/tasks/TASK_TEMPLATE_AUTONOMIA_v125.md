# Task: Template Task + Workflow Autonomia Regina

**Assegnato a:** cervella-docs
**Sessione:** 125 (8 Gennaio 2026)
**Priorità:** ALTA ⚡
**Obiettivo:** Rendere Regina AUTONOMA nella delegazione

---

## 🎯 OBIETTIVO

Creare **template task pronti** e documentare **workflow autonomia** per Regina.

**SCOPO:** Regina deve poter delegare SENZA azioni manuali da Rafa!

---

## 📋 PROBLEMA DA RISOLVERE

**Attualmente:**
```
Rafa chiede feature X
→ Regina crea file .swarm/tasks/TASK_X.md manualmente
→ Regina fa `touch .ready` manualmente
→ Regina lancia `spawn-workers --backend` con Bash
→ Worker lavora
```

**DOVREBBE ESSERE:**
```
Rafa chiede feature X
→ Regina dice: "Delego a backend per X"
→ SISTEMA fa tutto automatico (task + .ready + spawn)
→ Worker lavora
→ Regina verifica output
```

**ZERO azioni manuali!** ✅

---

## 📤 OUTPUT RICHIESTO

### 1. Template Task (in `.swarm/templates/`)

**Creare 8 template pronti all'uso:**

**File:** `.swarm/templates/TEMPLATE_RICERCA_TECNICA.md`
```markdown
# Task: [NOME RICERCA]

**Assegnato a:** cervella-researcher
**Priorità:** [ALTA/MEDIA/BASSA]

## 🎯 OBIETTIVO
[Cosa ricercare]

## 📋 DOMANDE DA RISPONDERE
1. [Domanda 1]
2. [Domanda 2]
3. [Domanda 3]

## 📤 OUTPUT
**File:** `docs/studio/RICERCA_[NOME].md`

**Struttura:**
- Executive Summary
- Ricerca dettagliata
- Raccomandazioni
- Prossimi step

## ✅ CRITERI DI SUCCESSO
- [ ] Tutte le domande risposte
- [ ] Fonti citate
- [ ] Raccomandazioni chiare
```

**Altri 7 template:**
- `TEMPLATE_IMPLEMENTAZIONE_FEATURE.md` (backend/frontend)
- `TEMPLATE_BUG_FIX.md` (tester)
- `TEMPLATE_CODE_REVIEW.md` (reviewer)
- `TEMPLATE_DOCUMENTAZIONE.md` (docs)
- `TEMPLATE_HARDTEST.md` (tester)
- `TEMPLATE_DEPLOY.md` (devops)
- `TEMPLATE_ANALISI_CODEBASE.md` (ingegnera)

**Ogni template:**
- Campo [PLACEHOLDER] chiari da sostituire
- Struttura completa
- Criteri successo
- Output path definito

---

### 2. Workflow Autonomia Regina

**File:** `docs/guide/WORKFLOW_AUTONOMIA_REGINA.md`

**Contenuto:**

```markdown
# WORKFLOW AUTONOMIA REGINA

> Come delegare senza azioni manuali da Rafa

## 🎯 PRINCIPIO

Regina coordina. Worker lavorano. Sistema gestisce file.
ZERO comandi manuali da Rafa!

## 📋 WORKFLOW DELEGAZIONE

### Step 1: Regina Decide

Rafa chiede: "Voglio ricerca su unbuffered output"

Regina pensa:
- Chi? → cervella-researcher
- Cosa? → Ricerca tecnica
- Template? → TEMPLATE_RICERCA_TECNICA.md

### Step 2: Regina Usa Template

```bash
# Regina copia template
cp .swarm/templates/TEMPLATE_RICERCA_TECNICA.md \
   .swarm/tasks/TASK_RICERCA_UNBUFFERED_v125.md

# Regina sostituisce placeholder
sed -i '' 's/\[NOME RICERCA\]/Unbuffered Output/g' \
   .swarm/tasks/TASK_RICERCA_UNBUFFERED_v125.md
```

### Step 3: Sistema Lancia Worker

```bash
# Regina marca ready e spawna
touch .swarm/tasks/TASK_RICERCA_UNBUFFERED_v125.ready
spawn-workers --researcher
```

### Step 4: Watcher Sveglia Regina

Worker finisce → crea .done → watcher sveglia → Regina verifica!

## 🛠️ TOOL PER REGINA

### Funzione: delega()

**Cosa fa:**
1. Copia template giusto
2. Sostituisce placeholder
3. Marca .ready
4. Lancia spawn-workers
5. Informa Rafa

**Esempio uso:**
```bash
delega --researcher "Ricerca unbuffered output"
→ SISTEMA fa tutto!
```

## 📊 CHECKLIST AUTONOMIA

Prima di delegare:
- [ ] Ho scelto worker giusto?
- [ ] Ho template per questo tipo task?
- [ ] Ho specificato output path?
- [ ] Ho criteri successo chiari?

Dopo delegazione:
- [ ] Worker spawned con successo?
- [ ] Task marcato .working?
- [ ] Watcher attivo?

Quando worker finisce:
- [ ] File .done creato?
- [ ] Output file esiste?
- [ ] Verifico qualità output
- [ ] Informo Rafa risultato
```

---

## ✅ CRITERI DI SUCCESSO

1. **8 template creati** in `.swarm/templates/`
2. **Ogni template** ha placeholder chiari
3. **Workflow autonomia** documentato step-by-step
4. **Checklist** per Regina seguire
5. **Esempi concreti** per ogni tipo task

---

## 🎯 CONTESTO

**Problema:** Attualmente Regina deve fare troppi step manuali.

**Soluzione:** Template + workflow chiaro = autonomia!

**Obiettivo finale:**
```
Rafa: "Voglio X"
Regina: "Delego!" [sistema fa tutto]
Worker: [lavora]
Regina: "Fatto! Ecco risultato"
```

**ZERO friction!** ✅

---

## 💡 NOTE IMPORTANTI

- Template devono essere **COMPLETI** ma **FLESSIBILI**
- Placeholder **CHIARI**: [NOME], [PRIORITA], etc.
- Output path **DEFINITO**: docs/studio/, docs/tests/, etc.
- Workflow deve funzionare per **QUALSIASI progetto**

---

## 🚀 ISPIRAZIONE

Guarda come funzionano OGGI i task:
- `.swarm/tasks/TASK_GUIDA_BEST_PRACTICES_v124.md` (docs)
- `.swarm/tasks/TASK_REVIEW_SPRINT3_DOCS_v124.md` (guardiana)
- `.swarm/tasks/TASK_WORKFLOW_REGINA_v124.md` (docs)

**Usa questi come base per template!**

---

**BUON LAVORO, CERVELLA-DOCS!** 📝

Crea template e workflow che renderanno Regina INVINCIBILE! 👸
