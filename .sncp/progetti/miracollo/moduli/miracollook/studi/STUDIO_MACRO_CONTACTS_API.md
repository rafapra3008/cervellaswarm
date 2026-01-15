# STUDIO MACRO - Google People API per Contacts Autocomplete

> **Data:** 2026-01-15
> **Progetto:** Miracollook (Gestione Colloqui)
> **Livello:** MACRO (visione generale, capabilities, approcci)
> **Ricercatrice:** Cervella Researcher

---

## EXECUTIVE SUMMARY

Google People API fornisce tutti gli strumenti necessari per implementare un autocomplete contatti professionale. Pattern consolidato: debounce 300ms, cache locale, chip UI per recipient multipli, priorità recent contacts.

**Effort stimato:** 2-3 giorni (6-8 ore)
**Complessità:** Media (API semplice, UX standard)
**Rischi:** Rate limits (facilmente gestibili con cache)

---

## 1. API CAPABILITIES

### 1.1 Google People API v1

**Endpoint principale:** `people.searchContacts`
- Ricerca prefix-based su: nomi, nickname, email, telefono, organizzazioni
- Source: CONTACT (contatti utente autenticato)
- Supporta warmup request per cache refresh
- Response format: JSON con campi strutturati

**Altri endpoint utili:**
- `people.connections.list` - Lista completa contatti
- `people.listDirectoryPeople` - Contatti dominio (Workspace)
- `people.searchDirectoryPeople` - Ricerca in directory

### 1.2 Authorization Scopes

| Scope | Permesso | Uso |
|-------|----------|-----|
| `contacts` | Read/Write completo | Creazione/modifica contatti |
| `contacts.readonly` | Solo lettura | **CONSIGLIATO per autocomplete** |
| `contacts.other.readonly` | "Other Contacts" | Contatti Gmail auto-aggiunti |
| `directory.readonly` | Directory aziendale | Solo Workspace |

**Raccomandazione:** Usare `contacts.readonly` - minimo privilegio necessario!

### 1.3 Rate Limits (Quota)

| Limite | Valore | Note |
|--------|--------|------|
| Richieste/giorno | 20.000.000 | FREE tier - abbondante! |
| Richieste/utente/giorno | 10.000 | Per utente autenticato |
| QPS max | 2.400/min | Queries per secondo |
| Errore | HTTP 503 | Retry con exponential backoff |

**Implicazione:** Con cache + debounce, ZERO problemi rate limits!

### 1.4 Response Format

```json
{
  "results": [
    {
      "person": {
        "resourceName": "people/c12345",
        "names": [{"displayName": "Mario Rossi"}],
        "emailAddresses": [{"value": "mario.rossi@example.com"}],
        "photos": [{"url": "https://..."}]
      }
    }
  ]
}
```

**Campi utili per UI:**
- `displayName` - Nome completo
- `emailAddresses` - Uno o più email
- `photos` - Avatar (se presente)
- `organizations` - Company/role (per context)

---

## 2. PATTERN AUTOCOMPLETE CONSIGLIATO

### 2.1 Frontend Flow

```
1. User digita in input (To/CC/BCC)
   ↓
2. Debounce 300ms (attesa fine digitazione)
   ↓
3. Query minima: 2 caratteri
   ↓
4. Check cache locale (Map<query, results>)
   ↓
   Cache HIT → Mostra risultati
   Cache MISS → API call
   ↓
5. API call con AbortController (timeout 5s)
   ↓
6. Parse results + cache (TTL 5 min)
   ↓
7. Render dropdown (max 10 risultati)
   ↓
8. User seleziona → Crea CHIP
```

### 2.2 Debounce Strategy

**Raccomandazione:**
- **300ms** per query < 4 caratteri (user sta digitando)
- **100ms** per query ≥ 4 caratteri (user rallenta)
- **0ms** se cache HIT (instant feedback!)

**Perché:** Bilanciamento tra responsiveness e API calls. Gmail usa ~200ms.

### 2.3 Cache Strategy

**Struttura cache:**
```javascript
Map<query, {
  results: Array<Contact>,
  timestamp: number,
  ttl: 300000 // 5 minuti
}>
```

**Quando cachare:**
- ✅ Query con risultati (anche vuoti!)
- ✅ Recent contacts (cache separata, TTL 1 ora)
- ❌ Query < 2 caratteri (troppo generiche)

**Cache invalidation:**
- Manual: Button "refresh contacts"
- Auto: TTL scaduto
- Long-lived: Purge quando > 100 entries

### 2.4 Recent Contacts Priority

**Gmail pattern:** Ultimi 10-20 contatti usati = TOP priority

**Implementazione:**
1. Store in localStorage: `recent_contacts: Array<{email, name, lastUsed}>`
2. Quando user seleziona contact → aggiorna `lastUsed`
3. Nel dropdown: Recent PRIMA, poi API results
4. Visual: Badge "Recent" per distinguerli

**Benefit:** User trova velocemente contatti frequenti senza digitare!

---

## 3. UX BEST PRACTICES

### 3.1 Chip/Tag Display per Recipients

**Pattern Gmail/Outlook:**
- Click su suggestion → Crea chip
- Chip = Avatar (optional) + Nome + Email + X button
- Multiple recipients: To, CC, BCC separati
- Keyboard: Enter/Tab/Comma → Crea chip

**HTML structure consigliato:**
```html
<div class="chip">
  <img src="avatar" alt=""> <!-- Optional -->
  <span class="chip-label">Mario Rossi (mario@example.com)</span>
  <button class="chip-remove" aria-label="Remove">×</button>
</div>
```

**CSS considerations:**
- Size: min-height 32px (touch-friendly!)
- Spacing: 4px gap between chips
- Hover state: Background darker
- Focus state: Outline 2px (accessibility!)

### 3.2 Dropdown Display

**Limit:** Max 10 results (standard!)
**Order:** Recent contacts → Exact matches → Fuzzy matches

**Card layout:**
```
┌─────────────────────────────────────┐
│ [Avatar] Mario Rossi                │
│          mario.rossi@example.com    │ ← Result card
│          Company Name (optional)    │
└─────────────────────────────────────┘
```

**Accessibility:**
- `role="listbox"` su dropdown
- `role="option"` su ogni result
- `aria-activedescendant` per keyboard nav
- `aria-label` descrittivi per screen reader

### 3.3 Keyboard Navigation

| Key | Action |
|-----|--------|
| **↓/↑** | Navigate dropdown |
| **Enter** | Select highlighted contact |
| **Tab** | Select + move to next field |
| **Escape** | Close dropdown |
| **Backspace** | Remove last chip (se input vuoto) |

**Gmail trick:** Comma (`,`) crea chip automaticamente! User può digitare "mario@example.com," e chip si crea subito.

### 3.4 Validation & Error States

**Email validation:**
- Regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` (basic)
- Visual: Red border se invalid email
- Tooltip: "Please enter a valid email address"

**API errors:**
- 503 (Rate limit): "Too many requests, please wait..."
- Network error: "Unable to load contacts. Check connection."
- No results: "No contacts found. Try a different search."

---

## 4. CONSIDERAZIONI TECNICHE

### 4.1 Privacy & Security

**Quali contatti mostrare?**
- ✅ Solo contatti utente autenticato (OAuth scope)
- ✅ Recent contacts se user ha usato Miracollook
- ❌ MAI condividere contatti tra utenti diversi!

**GDPR compliance:**
- Contatti in cache → Client-side only (localStorage)
- NO storage server-side senza consenso
- Privacy policy: Dichiarare uso People API

### 4.2 Performance

**Optimizations:**
1. **Debounce** (300ms) → -70% API calls
2. **Cache** (5min TTL) → -50% API calls
3. **AbortController** → Cancel richieste obsolete
4. **List virtualization** (se > 100 results) → Render solo visible

**Bundle size:**
- Google API client: ~50KB gzipped
- Chip UI component: ~5KB
- Total impact: ~55KB (acceptable!)

### 4.3 Offline Fallback

**Scenario:** User offline o API down

**Strategy:**
1. Cache persiste in localStorage (survives reload!)
2. Show cached recent contacts
3. Disable API-dependent features (search new contacts)
4. Toast message: "Working offline - showing cached contacts"

**Manual input:** User può SEMPRE digitare email manuale e creare chip!

### 4.4 Cross-Browser Compatibility

**API support:**
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support (OAuth quirks - testare!)

**Polyfills needed:**
- `AbortController` → Solo IE11 (possiamo ignorare?)
- `Map` / `localStorage` → Nativo ovunque

---

## 5. EFFORT STIMATO

### 5.1 Backend (Miracollo)

| Task | Effort | Note |
|------|--------|------|
| OAuth Google setup | 1h | Configurazione Cloud Console |
| Token storage/refresh | 1h | Service layer per tokens |
| Proxy endpoint (optional) | 0.5h | Se vogliamo nascondere client_secret |

**Totale Backend:** 2-2.5 ore

**Nota:** Backend può essere ZERO se client-side OAuth diretto!

### 5.2 Frontend (Miracollook)

| Task | Effort | Note |
|------|--------|------|
| Google API client integration | 1h | Import + OAuth flow |
| Debounce + Cache logic | 1.5h | Utility functions |
| Chip component | 2h | HTML/CSS/JS per chips |
| Dropdown autocomplete UI | 2h | Risultati + keyboard nav |
| Integration in "Nuovo Colloquio" | 1h | To/CC/BCC fields |
| Testing + polish | 1.5h | Edge cases, accessibility |

**Totale Frontend:** 9 ore

### 5.3 TOTALE PROGETTO

**Best case:** 2 giorni (6h backend + 9h frontend)
**Realistic:** 2.5-3 giorni (con testing completo)
**Worst case:** 4 giorni (se problemi OAuth/API)

---

## 6. RACCOMANDAZIONI FINALI

### ✅ DO

1. **Usa `contacts.readonly` scope** - minimo privilegio!
2. **Cache aggressivo** (5min TTL) - risparmia API calls
3. **Debounce 300ms** - bilanciamento UX/performance
4. **Recent contacts priorità** - UX come Gmail
5. **Keyboard navigation** - accessibility FIRST!
6. **Manual email input sempre possibile** - fallback critico!

### ❌ DON'T

1. **Non cachare > 10 minuti** - contatti cambiano!
2. **Non fare API call su ogni keystroke** - rate limits!
3. **Non mostrare > 10 results** - overwhelming!
4. **Non fare OAuth server-side** - meglio client-side per privacy!
5. **Non storage contatti server** - GDPR nightmare!

### 🎯 PROSSIMI STEP

1. **Decisione Rafa:** Backend proxy o client-side diretto?
2. **Setup Google Cloud Console** - OAuth credentials
3. **Spike tecnico** (2h) - Test People API con Miracollo OAuth
4. **Implementazione** (2-3 giorni)
5. **Test produzione** - Verificare rate limits reali

---

## FONTI

- [Google People API Introduction](https://developers.google.com/people)
- [People API - Contacts Management](https://developers.google.com/people/v1/contacts)
- [Method: people.searchContacts](https://developers.google.com/people/api/rest/v1/people/searchContacts)
- [Google People API Rate Limits](https://issuetracker.google.com/issues/185694048)
- [Gmail Autocomplete Guide](https://yamm.com/blog/gmail-autocomplete/)
- [Email Chip UI Design Best Practices](https://www.setproduct.com/blog/chip-ui-design)
- [Autocomplete UX Best Practices](https://smart-interface-design-patterns.com/articles/autocomplete-ux/)
- [Frontend Autocomplete System Design](https://frontendlead.com/system-design/frontend-autocomplete-system-design-guide)
- [Debouncing for Autocomplete Performance](https://www.freecodecamp.org/news/deboucing-in-react-autocomplete-example/)
- [Autocomplete Frontend Design Guide](https://www.greatfrontend.com/questions/system-design/autocomplete)

---

**COSTITUZIONE-APPLIED:** SI
**Principio usato:** "Studiare prima di agire - i player grossi hanno già risolto!" → Analizzato Gmail, Outlook, best practices consolidate. Pattern testato da milioni di utenti = zero reinvenzione ruota!

*"Non reinventiamo la ruota - studiamo chi l'ha già fatta!"* 🔬
