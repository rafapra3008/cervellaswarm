# Esempio d'Uso - Learning Wizard

**Data:** 2026-01-01

---

## 🎯 SCENARIO

Hai appena risolto un bug critico in cui un modal non si chiudeva correttamente perché mancava la gestione dell'evento ESC. Vuoi documentare questa lezione per non ripetere l'errore.

---

## 🚀 ESECUZIONE

```bash
cd ~/Developer/CervellaSwarm
python3 scripts/learning/wizard.py
```

---

## 📝 INTERAZIONE STEP-BY-STEP

### Step 1/9: TEMPLATE

```
Che tipo di lezione è?
  1. Bug Fix
  2. Refactoring
  3. Integrazione API/Service
  4. Custom (vuoto)
Scegli numero []: 1
```

**→ Scelgo: `1`** (Bug Fix)

---

### Step 2/9: TRIGGER

```
Quando si applica questa lezione?
Trigger [Quando si incontra bug simile a: {bug_type}]:
```

**→ Inserisco:** `Quando si crea un modal che deve chiudersi con ESC`

---

### Step 3/9: CONTEXT

```
Descrivi il contesto (task, agente, situazione)
Context []:
```

**→ Inserisco:** `Modal di conferma eliminazione in Miracollo PMS, sviluppato da cervella-frontend`

---

### Step 4/9: PROBLEM

```
Cosa è andato storto?
Problem []:
```

**→ Inserisco:** `Il modal non si chiudeva premendo ESC, solo cliccando X o sfondo`

---

### Step 5/9: ROOT CAUSE

```
Perché è successo? (causa radice)
Root Cause []:
```

**→ Inserisco:** `Mancava event listener per keydown ESC nel componente Modal`

---

### Step 6/9: SOLUTION

```
Come è stato risolto?
Solution []:
```

**→ Inserisco:** `Aggiunto useEffect con event listener per ESC key che chiama onClose`

---

### Step 7/9: PREVENTION

```
Come prevenire in futuro?
Prevention [Verificare {checklist} prima di implementare]:
```

**→ Inserisco:** `Checklist modal: (1) ESC close, (2) click fuori close, (3) X button, (4) focus trap`

---

### Step 8/9: EXAMPLE

```
Esempio concreto (opzionale)
Example []:
```

**→ Inserisco:**
```javascript
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') onClose();
  };
  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, [onClose]);
```

---

### Step 9/9: METADATA

#### Severity

```
Severity?
  1. CRITICAL
  2. HIGH
  3. MEDIUM
  4. LOW
Scegli numero []:
```

**→ Scelgo: `2`** (HIGH - impatta UX)

#### Agents

```
Quali agenti devono conoscere questa lezione?
(inserisci numeri separati da virgola, es: 1,3,5)
  1. cervella-frontend
  2. cervella-backend
  3. cervella-tester
  4. cervella-reviewer
  5. cervella-researcher
  6. cervella-devops
  7. cervella-docs
  8. cervella-data
  9. cervella-security
  10. cervella-marketing
Scegli numeri []:
```

**→ Inserisco: `1,3,4`** (Frontend, Tester, Reviewer)

#### Tags

```
Tags (separati da virgola) []:
```

**→ Inserisco:** `modal, keyboard, accessibility, ux`

#### Pattern

```
Pattern name (identificativo breve) []:
```

**→ Inserisco:** `modal-esc-close`

---

## 📋 PREVIEW

```markdown
============================================================
📋 ANTEPRIMA LEZIONE
============================================================

**TRIGGER:** Quando si crea un modal che deve chiudersi con ESC

**CONTEXT:** Modal di conferma eliminazione in Miracollo PMS, sviluppato da cervella-frontend

**PROBLEM:** Il modal non si chiudeva premendo ESC, solo cliccando X o sfondo

**ROOT CAUSE:** Mancava event listener per keydown ESC nel componente Modal

**SOLUTION:** Aggiunto useEffect con event listener per ESC key che chiama onClose

**PREVENTION:** Checklist modal: (1) ESC close, (2) click fuori close, (3) X button, (4) focus trap

**EXAMPLE:**
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') onClose();
  };
  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, [onClose]);

**SEVERITY:** HIGH
**AGENTS:** cervella-frontend, cervella-tester, cervella-reviewer
**TAGS:** modal, keyboard, accessibility, ux
**PATTERN:** modal-esc-close
```

---

## ✅ CONFERMA

```
Salvare questa lezione? [Y/n]:
```

**→ Premo: `Y`** (o ENTER)

---

## 🎉 RISULTATO

```
✅ Lezione salvata con ID: 3f7e9a21-4b2c-4d8f-9c1e-5a3b8d7f2e9c

🎉 Lezione documentata con successo!
   ID: 3f7e9a21-4b2c-4d8f-9c1e-5a3b8d7f2e9c
   Pattern: modal-esc-close
```

---

## 💾 DOVE È SALVATA?

La lezione è ora nel database `data/swarm_memory.db`:

```sql
SELECT * FROM lessons_learned WHERE pattern = 'modal-esc-close';
```

E può essere recuperata automaticamente dagli agenti quando lavorano su modal simili!

---

## 🔄 PROSSIMI UTILIZZI

Quando `cervella-frontend` crea un nuovo modal, il sistema:

1. Rileva pattern simile ("modal" in contesto)
2. Recupera lezione `modal-esc-close`
3. Suggerisce la checklist PRIMA di implementare
4. Evita il bug PRIMA che accada!

**Questo è il potere del Learning System!** 🧠💙

---

*Cervella Backend - CervellaSwarm* 🐝
