# Task: HARDTEST - [NOME_FEATURE/SISTEMA]

**Assegnato a:** cervella-tester
**Sessione:** [NUMERO_SESSIONE]
**Sprint:** [NUMERO_SPRINT] - [NOME_SPRINT]
**Priorità:** [ALTA/MEDIA/BASSA]
**Stato:** ready

---

## 🎯 OBIETTIVO

HARDTEST di: **[Feature/Sistema/Integration]**

**SCOPO:** Verificare funzionamento REALE in condizioni estreme e edge cases.

**FILOSOFIA:** "Se non l'hai HARDTEST-ato, non è testato!"

---

## 🧪 COSA TESTARE

### Sistema Under Test:
[Descrizione cosa stai testando]

### Scope:
- [ ] **Functionality** - Fa quello che deve fare?
- [ ] **Edge Cases** - Gestisce casi limite?
- [ ] **Error Handling** - Fallisce gracefully?
- [ ] **Performance** - È abbastanza veloce?
- [ ] **Integration** - Funziona con resto sistema?
- [ ] **Security** - È sicuro?

---

## 📋 TEST PLAN

### 1. Happy Path (baseline)

**Test:** [Caso d'uso normale]

**Step:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected:** [Risultato atteso]

---

### 2. Edge Cases

**Test 2.1:** [Edge case 1 - es: input vuoto]
- Setup: [come preparare]
- Execute: [cosa fare]
- Expected: [cosa dovrebbe succedere]

**Test 2.2:** [Edge case 2 - es: input molto grande]
- Setup: [come preparare]
- Execute: [cosa fare]
- Expected: [cosa dovrebbe succedere]

**Test 2.3:** [Edge case 3 - es: input invalido]
- Setup: [come preparare]
- Execute: [cosa fare]
- Expected: [cosa dovrebbe succedere]

---

### 3. Stress Tests

**Test 3.1:** [High load - es: 1000 richieste]
- Setup: [come preparare]
- Execute: [cosa fare]
- Measure: [cosa misurare - tempo, memoria, CPU]
- Expected: [limiti accettabili]

**Test 3.2:** [Concurrent access - es: 10 utenti simultanei]
- Setup: [come preparare]
- Execute: [cosa fare]
- Expected: [risultato]

---

### 4. Failure Scenarios

**Test 4.1:** [Database down]
- Setup: [come simulare]
- Execute: [cosa fare]
- Expected: [error handling corretto]

**Test 4.2:** [Network timeout]
- Setup: [come simulare]
- Execute: [cosa fare]
- Expected: [error handling corretto]

**Test 4.3:** [Partial failure]
- Setup: [come simulare]
- Execute: [cosa fare]
- Expected: [rollback o recovery]

---

## 📤 OUTPUT RICHIESTO

**File:** `docs/tests/HARDTEST_[NOME]_v[SESSIONE].md`

```markdown
# HARDTEST Report: [NOME]

**Tester:** cervella-tester
**Data:** [DATA]
**Versione testata:** [commit/branch]

---

## EXECUTIVE SUMMARY

[Sintesi 2-3 paragrafi: sistema pronto per produzione?]

**Rating Generale:** X/10

**Raccomandazione:**
- [ ] ✅ PASS - Pronto per produzione
- [ ] ⚠️ PASS WITH NOTES - Ok ma con limitazioni note
- [ ] ⚠️ CONDITIONAL PASS - Fix minori necessari
- [ ] ❌ FAIL - Fix critici necessari

---

## TEST RESULTS

### Happy Path
- [✅/❌] Test 1: [nome] - [risultato]
- [✅/❌] Test 2: [nome] - [risultato]

### Edge Cases
- [✅/❌] Test 2.1: [nome] - [risultato]
- [✅/❌] Test 2.2: [nome] - [risultato]
- [✅/❌] Test 2.3: [nome] - [risultato]

### Stress Tests
- [✅/❌] Test 3.1: [nome] - [risultato + metriche]
- [✅/❌] Test 3.2: [nome] - [risultato + metriche]

### Failure Scenarios
- [✅/❌] Test 4.1: [nome] - [risultato]
- [✅/❌] Test 4.2: [nome] - [risultato]

---

## BUGS FOUND

### 🔴 CRITICAL
1. [Bug critico 1 - blocca produzione]
2. [Bug critico 2 - data loss possibile]

### 🟠 HIGH
1. [Bug importante 1 - impatta UX]
2. [Bug importante 2 - performance issue]

### 🟡 MEDIUM
1. [Bug medio 1 - edge case non gestito]

### 🟢 LOW
1. [Issue minore 1 - cosmetico]

---

## PERFORMANCE METRICS

| Test | Tempo | Memoria | CPU | Status |
|------|-------|---------|-----|--------|
| Happy path | Xms | XMB | X% | ✅ |
| High load | Xms | XMB | X% | ✅/❌ |
| Concurrent | Xms | XMB | X% | ✅/❌ |

**Bottlenecks identificati:**
- [Bottleneck 1]
- [Bottleneck 2]

---

## LIMITATIONS DISCOVERED

[Limitazioni del sistema scoperte durante test]

---

## RECOMMENDATIONS

[Cosa fixare? Cosa migliorare? Limitazioni accettabili?]

---

## NEXT STEPS

1. [Step 1 - fix critical bugs]
2. [Step 2 - performance optimization]
3. [Step 3 - re-test]
```

---

## ✅ CRITERI DI SUCCESSO

HARDTEST completato quando:

### Copertura
- [ ] Happy path testato
- [ ] Almeno 5 edge cases testati
- [ ] Almeno 2 stress tests eseguiti
- [ ] Almeno 2 failure scenarios testati

### Qualità
- [ ] Ogni test documentato (setup + execute + expected)
- [ ] Bugs documentati con severity
- [ ] Performance metrics raccolti
- [ ] Raccomandazione chiara (pass/fail)

### Onestà
- [ ] Rating onesto (non generoso!)
- [ ] Se fail, spiega PERCHÉ
- [ ] Limitazioni documentate chiaramente

**Rating minimo per HARDTEST:** 9/10 (deve essere rigoroso!)

---

## 🎯 CONTESTO

**Perché HARDTEST?**
[Pre-deploy? Bug reports? Validation post-implementazione?]

**Ambiente test:**
- [ ] Locale
- [ ] Staging
- [ ] Produzione-like

**Criticità:**
[Quanto è critico questo sistema? Payment? Auth? Analytics?]

---

## 💡 SUGGERIMENTI

**HARDTEST efficace:**
- Pensa come utente cattivo (cosa può rompere?)
- Testa combinazioni improbabili
- Simula failure realistici
- Misura tutto (tempo, memoria, errori)

**Sii spietato:**
- Non assumere nulla funziona
- Se test non è chiaro, non vale
- Se pass ma sei dubbioso, investiga
- Rating basso è OK se meritato!

**Tool utili:**
- `time` per misurare performance
- `htop` per monitorare risorse
- Log dettagliati durante test
- Screenshot per bug visivi

---

## 🚨 RED FLAGS

Se trovi questi → FAIL automatico:

- ❌ Data loss su failure
- ❌ Security vulnerability
- ❌ Crash irrecuperabile
- ❌ Performance 10x più lenta di atteso
- ❌ Silent failure (fail ma non dice nulla)

---

## 📊 ESEMPIO

**HARDTEST simile:**
- `docs/tests/HARDTEST_UNBUFFERED_OUTPUT_v124.md` (rating 4/10 - trovato problema!)

**Usa come riferimento!**

---

**BUON HARDTEST!** 🧪🔬

*Tempo stimato: [2h / 4h / 8h]*

**Be ruthless, not reckless. Test everything, assume nothing!**
