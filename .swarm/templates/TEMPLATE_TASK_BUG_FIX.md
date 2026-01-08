# Task: Bug Fix - [NOME_BUG]

**Assegnato a:** cervella-tester
**Sessione:** [NUMERO_SESSIONE]
**Sprint:** [NUMERO_SPRINT] - [NOME_SPRINT]
**Priorità:** [CRITICA / ALTA / MEDIA / BASSA]
**Stato:** ready

---

## 🎯 OBIETTIVO

Identificare root cause e fixare bug: **[DESCRIZIONE_BUG]**

**IMPATTO:** [Cosa blocca? Chi colpisce? Quanto grave?]

---

## 🐛 DESCRIZIONE BUG

### Comportamento Atteso

[Cosa DOVREBBE succedere?]

### Comportamento Attuale

[Cosa succede INVECE?]

### Differenza

[In cosa differiscono?]

---

## 🔍 RIPRODUZIONE

### Step per riprodurre:

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Risultato: bug si manifesta]

### Ambiente:

- **Browser/OS:** [se frontend]
- **Python version:** [se backend]
- **Database:** [se DB-related]
- **Branch:** [quale branch]

### Frequenza:

- [ ] Sempre (100%)
- [ ] Spesso (>75%)
- [ ] A volte (25-75%)
- [ ] Raro (<25%)

---

## 📋 INVESTIGAZIONE RICHIESTA

### 1. Root Cause Analysis

**Dove cercare:**
- [ ] File sospetto 1: [path/to/file]
- [ ] File sospetto 2: [path/to/file]
- [ ] Component/Function: [nome]

**Ipotesi causa:**
- Ipotesi 1: [possibile causa]
- Ipotesi 2: [possibile causa]

### 2. Test Esplorativi

**Testare varianti:**
- [ ] Con input diverso: [quale]
- [ ] Con utente diverso: [quale]
- [ ] In ambiente diverso: [quale]

**Domande da rispondere:**
- Il bug è solo visuale o logico?
- Colpisce tutti gli utenti o solo alcuni?
- È regressione o bug sempre esistito?
- Ha side effects su altre feature?

---

## 📤 OUTPUT RICHIESTO

### 1. Report Investigazione

**File:** `docs/tests/BUG_REPORT_[NOME].md`

```markdown
# Bug Report: [NOME]

## Root Cause
[Causa identificata - file:linea se possibile]

## Perché è successo
[Spiegazione tecnica]

## Impatto
- Feature colpite: [lista]
- Utenti colpiti: [chi]
- Data-loss risk?: [sì/no]

## Fix Proposto
[Come fixarlo]

## Rischi Fix
[Cosa potrebbe rompere il fix?]

## Test Regressione
[Come verificare non rompe altro?]
```

### 2. Fix Implementato

**File modificati:**
- [ ] [path/to/file1] - [cosa modificato]
- [ ] [path/to/file2] - [cosa modificato]

**Test aggiunti:**
- [ ] Test riproduzione bug (deve fallire PRIMA del fix)
- [ ] Test che fix funziona (deve passare DOPO fix)
- [ ] Test regressione (verifica non rompe altro)

---

## ✅ CRITERI DI SUCCESSO

Task completato quando:

### Investigazione
- [ ] Root cause identificata con certezza
- [ ] File/linea esatta trovata
- [ ] Capito PERCHÉ è successo

### Fix
- [ ] Bug fixato
- [ ] Test riproduzione passa dopo fix
- [ ] Test regressione passano (non rompe altro)
- [ ] Code review: fix elegante e manutenibile

### Prevenzione
- [ ] Test aggiunto per prevenire regressione
- [ ] Documentato in report
- [ ] Lesson learned (se applicabile)

**Rating minimo atteso:** 9/10 (bug fix deve essere solido!)

---

## 🎯 CONTESTO

**Quando è stato scoperto:**
[Chi, quando, dove]

**Storia:**
- [ ] Bug sempre esistito
- [ ] Introdotto in [commit/PR]
- [ ] Regressione dopo [cambio]

**Urgenza:**
- [ ] CRITICA (blocca produzione)
- [ ] ALTA (workaround esiste ma brutto)
- [ ] MEDIA (impatta ma non blocca)
- [ ] BASSA (nice to fix)

---

## 💡 SUGGERIMENTI

**Per investigare:**
- Usa git blame per trovare quando introdotto
- Controlla PR/commit che ha toccato file sospetto
- Aggiungi logging temporaneo per capire flusso
- Riproduci in locale con debugger

**Per fixare:**
- Fix minimo necessario (non refactor tutto!)
- Se non sei sicuro, chiedi seconda opinione
- Test PRIMA di committare
- Documenta PERCHÉ il fix funziona (commento)

**IMPORTANTE:**
- Se non trovi root cause in 2h → CHIEDI AIUTO
- Se fix rompe test → NON committare, INVESTIGA
- Se fix richiede refactor grosso → DISCUTI prima

---

## 🚨 NON FARE

- ❌ Non fare quick fix senza capire root cause
- ❌ Non commentare codice rotto (FIXA o ELIMINA)
- ❌ Non skipare test regressione "sicuro va bene"
- ❌ Non fixare solo il sintomo, fixa la CAUSA
- ❌ Non assumere impatto limitato senza testare

---

## 📊 ESEMPIO

**Bug fix simile completato:**
- [Link a bug report precedente]
- [Pattern seguito]

---

**BUON DEBUG!** 🐛🔧

*Tempo stimato: [1h / 2h / 4h / 8h]*

**Se non trovi causa in tempo stimato: CHIEDI AIUTO subito!**
