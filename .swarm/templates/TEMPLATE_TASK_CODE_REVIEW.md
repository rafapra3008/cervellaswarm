# Task: Code Review - [NOME_FEATURE/PR]

**Assegnato a:** cervella-reviewer
**Sessione:** [NUMERO_SESSIONE]
**Sprint:** [NUMERO_SPRINT] - [NOME_SPRINT]
**Priorità:** [ALTA/MEDIA/BASSA]
**Stato:** ready

---

## 🎯 OBIETTIVO

Code review per: **[Feature/PR/Sprint name]**

**SCOPO:** [Verificare qualità prima di merge / Audit generale / Review pre-deploy]

---

## 📋 FILE DA REVIEWARE

### Backend (se applicabile)
- [ ] `[path]/routes/[file].py`
- [ ] `[path]/models/[file].py`
- [ ] `[path]/services/[file].py`
- [ ] `[path]/tests/test_[file].py`

### Frontend (se applicabile)
- [ ] `src/components/[path]/[file].tsx`
- [ ] `src/api/[file].ts`
- [ ] `src/types/[file].ts`
- [ ] `src/styles/[file].css`

### Altri
- [ ] [File 1]
- [ ] [File 2]

**Totale:** [~N] file, [~N] righe

---

## 🔍 CRITERI DI REVIEW

### 1. QUALITÀ CODICE (30%)

**Leggibilità:**
- [ ] Nomi variabili/funzioni chiari
- [ ] Nessun magic number
- [ ] Commenti dove necessario
- [ ] Struttura logica

**Manutenibilità:**
- [ ] Funzioni < 50 righe
- [ ] Nessuna duplicazione codice
- [ ] Single Responsibility Principle
- [ ] DRY (Don't Repeat Yourself)

**Best Practices:**
- [ ] Segue style guide progetto
- [ ] Pattern consistenti
- [ ] Nessun anti-pattern

---

### 2. FUNZIONALITÀ (25%)

- [ ] Implementa spec completamente
- [ ] Edge cases gestiti
- [ ] Error handling robusto
- [ ] Logging appropriato

**Domande:**
- Il codice fa quello che deve fare?
- Ci sono casi non gestiti?
- Comportamento su input inaspettato?

---

### 3. SECURITY (20%)

- [ ] Input validati
- [ ] Output sanitizzati
- [ ] Nessun SQL injection
- [ ] Nessun XSS
- [ ] Autenticazione/autorizzazione corretta
- [ ] Nessun secret hardcodato
- [ ] Nessun sensitive data nei log

**CRITICO:** Qualsiasi issue security → rating automaticamente < 5/10

---

### 4. PERFORMANCE (15%)

- [ ] Nessuna query N+1
- [ ] Index DB appropriati
- [ ] Nessun loop inutile
- [ ] Caching dove necessario
- [ ] Lazy loading se applicabile

**Red flags:**
- Loop dentro loop
- Query in loop
- Loading tutto in memoria

---

### 5. TEST (10%)

- [ ] Test presenti
- [ ] Coverage >= 80%
- [ ] Test significativi (non solo happy path)
- [ ] Test edge cases
- [ ] Test nomi chiari

---

## 📤 OUTPUT RICHIESTO

**File:** `docs/review/CODE_REVIEW_[NOME]_v[SESSIONE].md`

```markdown
# Code Review: [NOME]

**Reviewer:** cervella-reviewer
**Data:** [DATA]
**File reviewati:** [N] file, [N] righe

---

## EXECUTIVE SUMMARY

[Sintesi 2-3 paragrafi: codice pronto per merge?]

**Rating Generale:** X/10

**Raccomandazione:**
- [ ] ✅ APPROVE - Merge immediato
- [ ] ⚠️ APPROVE con note - Merge ok, fix minori dopo
- [ ] ⚠️ REQUEST CHANGES - Fix necessari prima merge
- [ ] ❌ REJECT - Refactor significativo necessario

---

## BREAKDOWN RATING

| Criterio | Rating | Note |
|----------|--------|------|
| Qualità Codice | X/10 | [note] |
| Funzionalità | X/10 | [note] |
| Security | X/10 | [note] |
| Performance | X/10 | [note] |
| Test | X/10 | [note] |

---

## ISSUES TROVATI

### 🔴 CRITICAL (blocca merge)
1. [Issue critico 1 - file:linea]
2. [Issue critico 2 - file:linea]

### 🟠 HIGH (fix prima di merge)
1. [Issue importante 1 - file:linea]
2. [Issue importante 2 - file:linea]

### 🟡 MEDIUM (fix consigliato)
1. [Issue medio 1 - file:linea]
2. [Issue medio 2 - file:linea]

### 🟢 LOW (nice to have)
1. [Suggestion 1 - file:linea]
2. [Suggestion 2 - file:linea]

---

## PUNTI DI FORZA

[Cosa è fatto BENE? 3-5 bullet points]

---

## RACCOMANDAZIONI

[Come migliorare? Prossimi step?]

---

## PROSSIMI STEP

1. [Step 1]
2. [Step 2]
```

---

## ✅ CRITERI DI SUCCESSO

Review completata quando:

- [ ] Tutti i file reviewati
- [ ] Ogni issue documentato con file:linea
- [ ] Rating onesto (non generoso!)
- [ ] Raccomandazione chiara (merge sì/no)
- [ ] Fix proposti concreti (non vaghi)

**Rating minimo per review:** 8/10 (review deve essere approfondita!)

---

## 🎯 CONTESTO

**Cosa revieware:**
[Feature implementata / Bug fix / Refactor / etc.]

**Priorità review:**
- [ ] Security (deploy produzione)
- [ ] Qualità (codebase sano)
- [ ] Performance (app veloce)
- [ ] General (tutto importante)

**Urgenza:**
[Blocca deploy? Nice to have? Audit programmato?]

---

## 💡 SUGGERIMENTI

**Review efficace:**
- Inizia da test (capire cosa deve fare)
- Poi business logic
- Poi edge cases
- Poi performance/security

**Sii costruttivo:**
- "Considera usare X invece di Y perché..."
- "Questo potrebbe causare X, suggerisco Y"
- "Bel pattern qui! Applica anche a Z?"

**Sii pratico:**
- Issue CRITICAL solo se veramente blocca
- Non nitpick su style (linter fa quello)
- Se incerto, CHIEDI all'autore

---

## 🚨 RED FLAGS AUTOMATICI

Se trovi questi → rating < 5/10 automaticamente:

- ❌ SQL injection possibile
- ❌ XSS possibile
- ❌ Secret hardcodato
- ❌ Nessun test
- ❌ Query N+1 massive
- ❌ Codice duplicato >50 righe
- ❌ Funzioni >200 righe

---

## 📊 ESEMPIO

**Review simile:**
- `docs/review/REVIEW_SPRINT3_DOCS_v124.md` (rating 9.5/10)

**Usa come riferimento per struttura e profondità!**

---

**BUONA REVIEW!** 📋👁️

*Tempo stimato: [1h / 2h / 4h]*

**Sii onesto ma costruttivo. La qualità dipende da te!**
