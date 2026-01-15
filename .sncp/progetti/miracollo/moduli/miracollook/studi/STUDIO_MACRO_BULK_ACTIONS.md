# STUDIO MACRO - Bulk Actions per Email Client

> **Data:** 15 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Livello:** MACRO (visione generale, pattern, best practices)
> **Progetto:** Miracollook - Email Client per Hotel

---

## Executive Summary

**OBIETTIVO:** Capire come i big players (Gmail, Outlook, Superhuman) implementano bulk actions per progettare una soluzione fluida e veloce per Miracollook.

**KEY FINDING:** Bulk actions è una feature CRITICA per hotel (inbox cleanup 2-3 volte/giorno). Pattern consolidato: checkbox + toolbar dinamica + keyboard shortcuts.

**RACCOMANDAZIONE:** Implementare con approccio progressivo: MVP (select + 3 azioni base) → Advanced (shift+click, cmd+A, undo).

---

## 1. COME FANNO I BIG PLAYERS

### Gmail (Industry Standard)

**Selection Pattern:**
- Checkbox singola per email (list view)
- Checkbox master in header (select all in page)
- Link "Select all X in [category]" per andare oltre pagina corrente
- Shift+Click per selezionare range
- Ctrl/Cmd+Click per selezione individuale non consecutiva

**Toolbar Dinamica:**
- Appare quando ≥1 email selezionata
- Mostra counter: "3 selected" chiaro e prominente
- Azioni disponibili: Archive, Delete, Mark Read/Unread, Move, Label, Snooze
- Nasconde toolbar normale (search, compose) per focus

**Mobile:**
- Long press su email → checkboxes appaiono
- Tap su altre email per aggiungere
- NO select all in bulk (limitazione UX mobile)

**Fonti:** [Mailbird Guide](https://www.getmailbird.com/how-to-select-multiple-emails-in-gmail/), [Clean.email](https://clean.email/blog/email-providers/how-to-select-all-in-gmail)

### Superhuman (Speed Focused)

**Selection Pattern:**
- Cmd+A (Mac) / Ctrl+A (Win) = "Select All From Here"
- Cmd+Shift+A / Ctrl+Shift+A = Select everything in split
- Add to selection via keyboard shortcuts
- Clear selection rapida

**Bulk Actions:**
- Hit E (archive) su selezione multipla → tutte archiviate
- "Get Me To Zero": bulk archive per timeframe (1 day → 1 month)
- Split Inbox nativa → bulk per categoria

**Filosofia:** Keyboard-first, ZERO mouse needed per power users.

**Fonti:** [Superhuman Mass Archive](https://help.superhuman.com/hc/en-us/articles/38458328563603-Mass-Archive), [Superhuman Shortcuts PDF](https://download.superhuman.com/Superhuman%20Keyboard%20Shortcuts.pdf)

### Outlook (Enterprise Standard)

**Selection Pattern:**
- Ctrl+A / Cmd+A per select all
- Shift+Click per range
- Ctrl/Cmd+Click per individuali

**Quick Steps (Killer Feature):**
- Bulk action customizzabili con shortcut Ctrl+Shift+5-9
- Esempio: "Move to folder X + Mark read" in 1 keystroke
- Pre-configured: Move to, Team Email, Done, Reply & Delete

**Toolbar:**
- Move to folder: Ctrl+Shift+V (instant move con dialog)
- Delete: Delete key | Permanent Delete: Shift+Delete

**Fonti:** [Email Sorters](https://emailsorters.com/blog/select-multiple-outlook-emails/), [Microsoft Support](https://support.microsoft.com/en-us/office/keyboard-shortcuts-for-outlook-3cdeb221-7ae5-4c1d-8c1d-9e63216c1efd)

---

## 2. UI PATTERN CONSIGLIATO

### Componenti Fondamentali

**1. Bulk Selector (Split Button)**
- Posizione: Leftmost in toolbar principale
- Combina: Checkbox master + dropdown menu
- Stati: None (⬜), Some (➖), All (✅)

**2. Selection Counter**
- Formato: "X selected" o "X of Y selected"
- Posizione: Prominente, vicino a toolbar azioni
- Cross-page: "23 selected (across multiple pages)" se pagination attiva

**3. Contextual Toolbar**
- Appare bottom/top quando ≥1 selezionata
- Actions: Archive, Delete, Mark Read/Unread, Move, Label, Assign (PMS!)
- Hide normale toolbar per evitare confusion

**Fonti:** [PatternFly Bulk Selection](https://www.patternfly.org/patterns/bulk-selection/), [Eleken Blog - 8 Guidelines](https://www.eleken.co/blog-posts/bulk-actions-ux)

### Keyboard Shortcuts Essenziali

```
Cmd/Ctrl + A          Select all in current view
Cmd/Ctrl + Shift + A  Select all in category/folder
Shift + Click         Select range (first → last)
Cmd/Ctrl + Click      Toggle individual selection
X                     Select/deselect email (vim-like)
E                     Archive selected
#                     Delete selected
!                     Mark as spam
Z                     Undo last action
```

---

## 3. API PATTERN - Backend Design

### Approccio Batch API

**Endpoint consigliato:**
```
POST /api/emails/bulk-action
Body: {
  "action": "archive" | "delete" | "mark_read" | "move" | "label",
  "email_ids": [123, 456, 789],
  "params": { "folder_id": 5 } // per move/label
}
```

### Error Handling - Partial Failure

**Pattern RFC 7807 (Problem Details):**
- HTTP 207 Multi-Status per operazioni miste
- Response body:
```json
{
  "status": "partial_success",
  "succeeded": [123, 456],
  "failed": [
    {
      "id": 789,
      "error": "Email not found",
      "code": "EMAIL_NOT_FOUND"
    }
  ],
  "summary": "2 of 3 succeeded"
}
```

**Alternativa AWS-style:**
- HTTP 200 OK sempre
- Client controlla campo `failed` in response

**Fonti:** [Adidas API Guidelines](https://adidas.gitbook.io/api-guidelines/rest-api-guidelines/execution/batch-operations), [Baeldung Best Practices](https://www.baeldung.com/rest-api-error-handling-best-practices)

### Optimistic UI + Undo

**Pattern:**
1. User seleziona 10 email → Click "Archive"
2. UI aggiorna IMMEDIATAMENTE (optimistic)
3. Mostra toast: "10 archived" con UNDO button (5s timeout)
4. API call async in background
5. Se fail → revert UI + show error
6. Undo button → POST /api/emails/bulk-undo con operation_id

**Fonti:** [Medium - Optimistic UI](https://medium.com/@kyledeguzmanx/what-are-optimistic-updates-483662c3e171), [React useOptimistic](https://react.dev/reference/react/useOptimistic)

---

## 4. CONSIDERAZIONI TECNICHE

### Performance

**Challenge:** Bulk su 1000+ email può bloccare UI
**Soluzione:**
- Pagination nel request (batches di 50)
- Loading indicator per operazioni lunghe
- Background job per bulk MASSIVE (>500)

### Database

**Transazioni:**
- Batch operations in SQL transaction
- Rollback se partial failure (or commit partial con 207)

**Indici necessari:**
- `(hotel_id, mailbox_id, read)` per bulk mark read
- `(hotel_id, mailbox_id, archived)` per bulk archive

---

## 5. EFFORT STIMATO

### MVP (2-3 giorni)
- ✅ Checkbox per email list
- ✅ Checkbox master in header
- ✅ Toolbar dinamica con counter
- ✅ 3 azioni: Archive, Delete, Mark Read
- ✅ API batch endpoint

### Advanced (3-4 giorni)
- ✅ Shift+Click per range selection
- ✅ Cmd+A select all in view
- ✅ Keyboard shortcuts (E, #, X)
- ✅ Optimistic UI + Undo toast
- ✅ Error handling con partial failure UI

### Deluxe (2-3 giorni)
- ✅ Cross-page selection (select all in category)
- ✅ Custom bulk actions (Outlook-style Quick Steps)
- ✅ PMS-integrated actions (Link to Booking, Assign to VIP)
- ✅ Mobile long-press support

**TOTALE:** 7-10 giorni per implementazione completa.

---

## 6. RACCOMANDAZIONE FINALE

**PATTERN CONSIGLIATO:** Ibrido Gmail + Superhuman
- Gmail pattern (checkbox + toolbar) per familiarità
- Superhuman shortcuts per velocità power users
- Outlook Quick Steps per hotel-specific workflows

**PRIORITÀ IMPLEMENTAZIONE:**
1. MVP con 3 azioni base (archive/delete/read) → subito usabile
2. Keyboard shortcuts → differenziatore per reception veloce
3. Optimistic UI + undo → professionalità percezione

**DIFFERENZIATORE MIRACOLLOOK:**
- Bulk actions PMS-aware: "Archive + Create booking note" in 1 action
- AI suggestion: "10 emails da stesso ospite → bulk link to booking?"

---

*Studio completato - Ready for implementation planning!*
