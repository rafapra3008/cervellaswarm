# STUDIO MACRO - Gmail Labels API

> **Data**: 2026-01-15
> **Ricercatrice**: cervella-researcher
> **Livello**: MACRO (visione generale, capabilities, approcci)

---

## EXECUTIVE SUMMARY

Gmail Labels API supporta CRUD completo con colori predefiniti, nesting/hierarchy, sync bidirezionale con Gmail web. Limite **10.000 labels** (Google raccomanda 500 per performance). Pattern UX consolidato: multi-label, drag & drop, color-coding. Frontend già implementato (TypeScript + React Query). Effort stimato: **2-3 giorni** per integrare completamente.

---

## 1. API CAPABILITIES

### CRUD Operations

**Endpoints disponibili:**
```
GET    /gmail/v1/users/{userId}/labels          # List
POST   /gmail/v1/users/{userId}/labels          # Create
GET    /gmail/v1/users/{userId}/labels/{id}     # Get
PUT    /gmail/v1/users/{userId}/labels/{id}     # Update
PATCH  /gmail/v1/users/{userId}/labels/{id}     # Partial Update
DELETE /gmail/v1/users/{userId}/labels/{id}     # Delete
```

**Scope richiesto:** `https://www.googleapis.com/auth/gmail.labels`

### Label Object Structure

```json
{
  "id": "Label_123",
  "name": "Work/Projects/Miracollo",
  "type": "user",  // o "system"
  "messageListVisibility": "show",  // o "hide"
  "labelListVisibility": "labelShow",  // "labelShowIfUnread", "labelHide"
  "messagesTotal": 42,
  "messagesUnread": 3,
  "threadsTotal": 38,
  "threadsUnread": 2,
  "color": {
    "textColor": "#000000",
    "backgroundColor": "#4a86e8"
  }
}
```

### System vs User Labels

| Tipo | Esempi | Modificabile | Eliminabile |
|------|--------|--------------|-------------|
| **SYSTEM** | INBOX, SPAM, TRASH, SENT, DRAFT, STARRED | ❌ NO | ❌ NO |
| **USER** | Custom labels (Work, Personal, etc.) | ✅ SI | ✅ SI |

**IMPORTANTE:** Non puoi creare USER labels con nomi riservati (INBOX, etc.) → HTTP 400 error.

### Label Colors

**Supporto:** ✅ SI, ma SOLO colori predefiniti da Google (~80 opzioni)

**Esempi colori disponibili:**
- `#000000`, `#434343`, `#666666` (grigi)
- `#4a86e8` (blu), `#43d692` (verde), `#16a766` (verde scuro)
- `#fad165` (giallo), `#ffad47` (arancione), `#fb4c2f` (rosso)

**Struttura:**
```json
{
  "textColor": "#ffffff",
  "backgroundColor": "#4a86e8"
}
```

**Limitazione:** Non puoi usare colori custom HEX arbitrari. Solo dalla palette Google.

### Nesting (Sublabels)

**Supporto:** ✅ SI, via naming convention

**Come funziona:**
```
Parent/Child/Grandchild/GreatGrandChild
```

**Esempio:**
```
Work
Work/Projects
Work/Projects/Miracollo
Work/Projects/Miracollo/Sprint-2
```

**Regola:** Parent label deve esistere PRIMA di creare il child.

**API:** Non c'è campo `parentId`. Il nesting è gestito tramite `/` nel nome.

### Sync con Gmail Web

**Bidirezionale:** ✅ SI, completamente sincronizzato

- Labels creati in Miracollook → visibili in Gmail web
- Labels creati in Gmail web → disponibili via API
- Cambio colore/nome → sincronizzato istantaneamente
- Delete label → rimosso da tutte le email

**Comportamento su email:**
- Aggiungere label a messaggio → label associato al thread
- Label NON propagato automaticamente ad altri messaggi del thread
- Visibile in Gmail web con stesso colore/nome

---

## 2. LIMITI & PERFORMANCE

### Limiti Account

| Limite | Valore | Note |
|--------|--------|------|
| **Max labels totali** | 10.000 | Limite tecnico |
| **Raccomandato Google** | 500 | Per performance ottimale |
| **Workspace Enterprise** | 10.000 | Confermato |
| **Gmail Free** | 5.000 | Documentazione ufficiale |

**Performance warning:**
- > 500 labels → UI Gmail web rallenta
- > 1000 labels → sync più lento
- Nested labels contano nel totale

### Rate Limits API

| Limite | Valore |
|--------|--------|
| **Quota giornaliera** | 1.000.000.000 units |
| **Per-user rate** | 250 units/sec (moving average) |
| **labels.list** | 1 unit |
| **labels.create** | 5 units |
| **labels.update** | 5 units |
| **labels.delete** | 5 units |

**Error:** HTTP 429 "User-rate limit exceeded" se superato.

**Best Practice:** Cache labels client-side (staleTime 5 min), invalidare solo su mutations.

---

## 3. PATTERN UX CONSIGLIATO

### Come Fanno i BIG

#### **Gmail Web**
- **Multi-label:** Check email → drag to label (espande sidebar con tutti i labels)
- **Color-coding:** Label colorati con badge nella lista email
- **Nested labels:** Expandable tree nella sidebar sinistra
- **Quick actions:** Right-click → Add/Remove labels
- **Mobile:** "Move to" button (no drag & drop su mobile)

#### **Outlook**
- **Folders:** Sistema folder-based (un folder alla volta)
- **Categories:** Simili a labels, ma secondari rispetto a folders
- **Color tags:** Multiple categories per email con colori
- **Approccio ibrido:** Folder primario + categories come tag

#### **Differenza filosofica:**
- Gmail: **Tag-based** (many-to-many)
- Outlook: **Folder-based** (one-to-many + categories)

### Componenti UI Essenziali

**1. LabelPicker Component** (✅ GIÀ FATTO!)
```tsx
<LabelPicker
  messageId={email.id}
  currentLabels={email.labelIds}
  onLabelsChange={handleChange}
/>
```

**Features:**
- Dropdown con search
- Multi-select con checkbox
- Color badge preview
- "Create new label" inline

**2. LabelBadge Component**
```tsx
<LabelBadge
  label={label}
  removable={true}
  onClick={() => filterByLabel(label.id)}
  onRemove={() => removeLabel(label.id)}
/>
```

**3. LabelSidebar (Filter View)**
```tsx
<LabelSidebar
  labels={userLabels}
  selectedLabelId={activeLabelId}
  onLabelClick={filterByLabel}
  onLabelCreate={createLabel}
/>
```

### UX Best Practices

**Drag & Drop:**
- Visual affordance (drag handle o hover state)
- Ghost image durante drag
- Drop zone highlighting
- Multi-selection support (drag multiple emails)

**Accessibility:**
- Keyboard navigation (Tab, Enter, Space)
- Aria labels ("Select labels for message")
- Color + icon (non solo colore per indicare stato)
- Screen reader friendly

**Performance:**
- Virtualizzazione se > 100 labels
- Debounce su search
- Optimistic updates (UI immediato, API async)
- Cache labels (no refetch ad ogni render)

**Mobile:**
- No drag & drop (usa modal/bottom sheet)
- Touch-friendly tap targets (min 44x44px)
- Swipe gestures per quick actions

---

## 4. CONSIDERAZIONI TECNICHE

### Frontend (Miracollook)

**Status attuale:** ✅ 80% FATTO
```
✅ types/label.ts
✅ hooks/useLabels.ts (React Query)
✅ components/Labels/LabelPicker.tsx
✅ services/api.ts (6 metodi Labels)
```

**Da fare:**
1. Integrare LabelPicker in EmailList toolbar
2. Mostrare label badges nella lista email
3. Sidebar filtro per label (opzionale)
4. Gestione colori (palette Google)
5. Nested labels tree view (opzionale v2)

**Pattern seguito:**
- React Query per caching (staleTime 5 min) ✅
- Optimistic updates su mutations ✅
- TypeScript strict ✅
- Tailwind CSS ✅

### Backend (API Proxy)

**Endpoint da implementare:**
```python
# Label CRUD
GET    /api/gmail/labels
POST   /api/gmail/labels
PUT    /api/gmail/labels/{label_id}
DELETE /api/gmail/labels/{label_id}

# Assign labels to messages
POST   /api/gmail/messages/{message_id}/labels
DELETE /api/gmail/messages/{message_id}/labels
```

**Considerazioni:**
- Gestire refresh token Gmail
- Error handling 429 (rate limit)
- Cache labels in Redis? (opzionale)
- Validare colori contro palette Google
- Impedire nomi riservati (INBOX, etc.)

### Sync & Real-time

**Problema:** Come sapere se labels cambiano in Gmail web?

**Opzioni:**
1. **Polling periodico** (ogni 5 min)
   - Pro: Semplice
   - Contro: Latenza, consuma quota API

2. **Gmail Push Notifications** (Pub/Sub)
   - Pro: Real-time
   - Contro: Setup complesso (Google Cloud Pub/Sub)

3. **Invalidazione manuale** (user-triggered)
   - Pro: Zero latenza, no API waste
   - Contro: UX meno fluida

**Raccomandazione:** Start con #3 (manual), poi #1 (polling 5 min), poi #2 (push) se necessario.

---

## 5. EFFORT STIMATO

### Fase 1: Integrazione Base (1 giorno)
- [ ] Integrare LabelPicker in EmailList (2h)
- [ ] Mostrare label badges inline (2h)
- [ ] Backend proxy endpoints (3h)
- [ ] Testing manuale (1h)

### Fase 2: Polish UX (1 giorno)
- [ ] Sidebar filtro per label (3h)
- [ ] Gestione palette colori Google (2h)
- [ ] Keyboard shortcuts (L = add label) (2h)
- [ ] Mobile optimization (1h)

### Fase 3: Advanced (opzionale, 1 giorno)
- [ ] Nested labels tree view (4h)
- [ ] Drag & drop email → label (3h)
- [ ] Bulk operations (select multiple + label) (1h)

**TOTALE MINIMO:** 2 giorni (Fase 1 + Fase 2)
**TOTALE COMPLETO:** 3 giorni (tutte le fasi)

---

## 6. DECISIONI DA PRENDERE

### A. Nested Labels UI

**Opzione 1:** Flat list (più semplice)
```
✓ Work
✓ Work/Projects
✓ Work/Projects/Miracollo
```

**Opzione 2:** Tree view (più complesso, migliore UX)
```
▾ Work
  ▾ Projects
    ✓ Miracollo
```

**Raccomandazione:** Start con Opzione 1 (V1), poi Opzione 2 (V2).

### B. Label Colors

**Opzione 1:** Pre-select dalla palette Google (semplice)
**Opzione 2:** Color picker limitato a palette Google (migliore UX)

**Raccomandazione:** Opzione 1 per V1.

### C. Real-time Sync

**Opzione 1:** Manual refresh button
**Opzione 2:** Auto-refresh ogni 5 min
**Opzione 3:** Gmail Push Notifications

**Raccomandazione:** Opzione 1 per V1, Opzione 2 per V2.

### D. Mobile Experience

**Opzione 1:** Modal/bottom sheet per label picker
**Opzione 2:** Swipe gesture (swipe left → show labels)

**Raccomandazione:** Opzione 1 (standard pattern).

---

## 7. RISKS & MITIGATIONS

| Risk | Probabilità | Impact | Mitigation |
|------|-------------|--------|------------|
| Rate limit 429 | Media | Alto | Client-side caching, debounce |
| Colori custom non supportati | Alta | Basso | Documentare palette Google |
| Nested labels complessi | Bassa | Medio | Flat view per V1 |
| Sync lag Gmail web | Media | Medio | Manual refresh button |

---

## FONTI

### Gmail API Documentation
- [Manage Labels Guide](https://developers.google.com/workspace/gmail/api/guides/labels)
- [REST Resource: users.labels](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.labels)
- [Method: users.labels.create](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.labels/create)
- [Usage Limits & Quotas](https://developers.google.com/workspace/gmail/api/reference/quota)

### UX Research
- [Gmail Drag and Drop Labels](https://cloud.googleblog.com/2009/07/drag-and-drop-and-organize-your-labels.html)
- [Outlook vs Gmail Labels](https://office-watch.com/2021/how-gmail-labels-and-categories-work-with-outlook/)
- [Gmail vs Outlook Comparison](https://www.getinboxzero.com/blog/post/gmail-vs-outlook)
- [Labels vs Folders Guide](https://hiverhq.com/blog/labels-vs-folders-guide)

### Best Practices
- [PatternFly Label Design Guidelines](https://www.patternfly.org/components/label/design-guidelines/)
- [Gmail Limits & Quotas](https://hiverhq.com/blog/gmail-and-google-apps-limits-every-admin-should-know)

---

## CONCLUSIONE

**Gmail Labels API è maturo e completo.** CRUD operations, colori predefiniti, nesting, sync bidirezionale. Frontend Miracollook ha già 80% del lavoro fatto. Effort stimato **2-3 giorni** per integrare completamente con UX polish.

**Raccomandazione:** PROCEDI con Fase 1 (integrazione base) + Fase 2 (polish UX). Fase 3 (advanced features) posticipabile a V2.

**Next Step:** Consultare cervella-marketing per validare UX design prima di implementare.

---

**COSTITUZIONE-APPLIED:** SI
**Principio usato:** "Studiare prima di agire - i big players hanno già risolto questi problemi!" → Ho studiato Gmail web, Outlook, API docs, UX patterns. Raccomandazione basata su ricerca, non invenzione.
