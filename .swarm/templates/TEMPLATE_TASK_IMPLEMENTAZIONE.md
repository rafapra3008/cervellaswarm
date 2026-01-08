# Task: Implementazione Feature - [NOME_FEATURE]

**Assegnato a:** [cervella-backend / cervella-frontend]
**Sessione:** [NUMERO_SESSIONE]
**Sprint:** [NUMERO_SPRINT] - [NOME_SPRINT]
**Priorità:** [ALTA/MEDIA/BASSA]
**Stato:** ready

---

## 🎯 OBIETTIVO

Implementare feature: **[NOME_FEATURE]**

**SCOPO:** [Cosa deve fare questa feature? Quale problema risolve?]

---

## 📋 SPECIFICHE

### Funzionalità Richiesta

**Cosa deve fare:**
1. [Funzionalità 1]
2. [Funzionalità 2]
3. [Funzionalità 3]

**Input:**
- [Input 1: tipo, formato]
- [Input 2: tipo, formato]

**Output:**
- [Output 1: tipo, formato]
- [Output 2: tipo, formato]

**Casi d'uso:**
1. [Caso d'uso principale]
2. [Caso d'uso secondario]
3. [Edge case importante]

---

## 🏗️ ARCHITETTURA

### Backend (se backend task)

**Endpoint:**
```
[METHOD] /api/[path]
```

**Request body:**
```json
{
  "field1": "tipo",
  "field2": "tipo"
}
```

**Response:**
```json
{
  "field1": "tipo",
  "field2": "tipo"
}
```

**Database:**
- [ ] Nuova tabella necessaria?
- [ ] Modifica tabella esistente?
- [ ] Nome tabella: [nome]
- [ ] Campi: [lista campi]

**Business Logic:**
[Descrizione logica principale]

---

### Frontend (se frontend task)

**Component:**
- Path: `src/components/[path]/[ComponentName].tsx`
- Tipo: [Pagina / Component / Modal / Form / etc.]

**Props:**
```typescript
interface [ComponentName]Props {
  prop1: tipo;
  prop2: tipo;
}
```

**State necessario:**
- [State 1: scopo]
- [State 2: scopo]

**API calls:**
- [Endpoint 1: quando chiamare]
- [Endpoint 2: quando chiamare]

**UI/UX:**
- [Descrizione UI]
- [Responsive?]
- [Loading states?]
- [Error handling?]

---

## 🔒 REQUISITI NON FUNZIONALI

**Security:**
- [ ] Autenticazione richiesta?
- [ ] Autorizzazione (ruoli)?
- [ ] Validazione input (XSS, injection)?
- [ ] Sanitizzazione output?

**Performance:**
- [ ] Query ottimizzate?
- [ ] Caching necessario?
- [ ] Paginazione se lista?

**Error Handling:**
- [ ] Try/catch implementato?
- [ ] Error messages user-friendly?
- [ ] Logging errori?

---

## 📤 OUTPUT RICHIESTO

### File da creare/modificare:

**Backend:**
- [ ] `[path]/routes/[file].py` - Endpoint
- [ ] `[path]/models/[file].py` - Model (se nuovo)
- [ ] `[path]/services/[file].py` - Business logic
- [ ] `[path]/tests/test_[file].py` - Test

**Frontend:**
- [ ] `src/components/[path]/[Component].tsx` - Component
- [ ] `src/components/[path]/[Component].css` - Styles (se necessario)
- [ ] `src/api/[file].ts` - API calls (se nuove)
- [ ] `src/types/[file].ts` - Types (se nuovi)

### Test richiesti:

- [ ] Unit test (logica business)
- [ ] Integration test (endpoint completo)
- [ ] E2E test (se critico)

**Coverage minima:** 80%

---

## ✅ CRITERI DI SUCCESSO

Task completato quando:

### Funzionalità
- [ ] Feature implementata secondo spec
- [ ] Tutti i casi d'uso funzionanti
- [ ] Edge cases gestiti

### Qualità
- [ ] Test scritti e passano
- [ ] Coverage >= 80%
- [ ] Nessun warning/error

### Sicurezza
- [ ] Input validati
- [ ] Autenticazione/autorizzazione ok
- [ ] Nessuna vulnerabilità nota

### Documentazione
- [ ] Docstring/commenti presenti
- [ ] README aggiornato (se necessario)
- [ ] API documentata (se backend)

**Rating minimo atteso:** 8/10

---

## 🎯 CONTESTO

**Perché questa feature?**
[Contesto business, richiesta utente, etc.]

**Dipendenze:**
- [ ] Dipende da: [task/feature precedente]
- [ ] Blocca: [task/feature successiva]

**Riferimenti:**
- Design: [link Figma / screenshot]
- Spec tecnica: [link doc]
- Issue: [link issue tracker]

---

## 💡 SUGGERIMENTI

- Inizia con il caso d'uso più semplice
- Test PRIMA di implementare (TDD se possibile)
- Commit frequenti con messaggi chiari
- Se blocchi, CHIEDI! Non inventare
- Se spec poco chiara, CHIEDI chiarimenti!

---

## 🚨 NON FARE

- ❌ Non bypassare validazione "tanto è interno"
- ❌ Non skipare test "lo testo dopo"
- ❌ Non hardcodare valori "è veloce"
- ❌ Non ignorare error handling "non succede mai"
- ❌ Non fare over-engineering "potrebbe servire"

---

## 📊 ESEMPIO

**Task simile completato:**
- [Link a task esempio simile]
- [Pattern da seguire]

---

**BUONA IMPLEMENTAZIONE!** 💻

*Tempo stimato: [2h / 4h / 8h / 16h]*

**Se superi tempo stimato del 50%: FERMA e chiedi aiuto!**
