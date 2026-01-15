# STUDIO MACRO - Settings UI Pattern per Email Client

> **Data:** 2026-01-15
> **Tipo:** Strategic Research - MACRO
> **Livello:** Visione generale pattern UX, categorie settings, architettura
> **Autrice:** Cervella Researcher

---

## TL;DR

**RACCOMANDAZIONE:** Settings drawer laterale (come Outlook) con auto-save per toggle/switch, explicit save per dati sensibili. 7 categorie principali. Storage: localStorage per UI preferences, database per business data (firme hotel, templates). Effort: **8-12 ore**.

---

## 1. CATEGORIE SETTINGS PROPOSTE

### 1.1 Categorie Standard Email Client

| Categoria | Sottocategorie | Priorita | Note |
|-----------|----------------|----------|------|
| **Account** | Profile, Avatar, Password | ALTA | OAuth-only (Google), minimal |
| **Appearance** | Theme (light/dark), Density (compact/comfortable), Fonts, Language | ALTA | Auto-save |
| **Notifications** | Desktop, Sound, Email types (new email, replies, etc) | MEDIA | Per-category control |
| **Signature** | Default signature, Per-account signature | ALTA | Rich text editor |
| **Privacy** | Read receipts, Tracking pixels, External images | MEDIA | Explicit save |
| **Keyboard** | Shortcuts customization, Quick actions | BASSA | Advanced users |
| **Advanced** | Auto-archive rules, Filters, Storage management | BASSA | Future |

### 1.2 Categorie SPECIFICHE Hotel (Miracollook)

| Categoria | Sottocategorie | Priorita | Note |
|-----------|----------------|----------|------|
| **Hotel Settings** | Default signature hotel, Quick reply templates, Staff assignment | CRITICA | Database-backed |
| **Team Settings** | Shared inbox rules, Assignment rules, SLA tracking | FUTURA | Fase 3+ |
| **PMS Integration** | Auto-tag guests, Guest context display, Booking integration | FUTURA | Fase 2 completa |

---

## 2. PATTERN UX CONSIGLIATO

### 2.1 Pattern BIG PLAYERS Analizzati

| Email Client | Pattern | Pro | Contro |
|--------------|---------|-----|--------|
| **Gmail** | Quick Settings Panel + Full Settings Page | Quick access, scalabile | Due interfacce da mantenere |
| **Outlook** | Settings Drawer (laterale) | Contesto mantenuto, fluido | Limita spazio per settings complessi |
| **Superhuman** | Command Palette (Cmd+K) per settings rapidi | Veloce per power users | Curva apprendimento |
| **Front/Missive** | Full page settings con sidebar nav | Spazio illimitato, chiaro | Perde contesto inbox |

### 2.2 RACCOMANDAZIONE per Miracollook

```
PATTERN SCELTO: Settings Drawer (Outlook-like)

PERCHE:
- Utenti receptionist: context switching costoso
- Devono poter modificare firma senza lasciare inbox
- Spazio sufficiente per 7 categorie
- Mobile-friendly (full screen su mobile)
```

### 2.3 Struttura UI Proposta

```
┌─────────────────────────────────────────────────────┐
│  Miracollook                    [Settings Icon]  [X] │  ← Header
├─────────────────────────────────────────────────────┤
│                                                      │
│  INBOX PRINCIPALE                    ┌──────────────┤  ← Drawer slide-in
│  - Email 1                           │  SETTINGS    │
│  - Email 2                           │              │
│  - Email 3                           │  [Search]    │
│  ...                                 │              │
│                                      │  Account     │
│                                      │  Appearance ◄│  ← Active
│                                      │  Notifications│
│                                      │  Signature   │
│                                      │  Privacy     │
│                                      │  Keyboard    │
│                                      │  Hotel       │
│                                      │              │
│                                      │  ┌─────────┐ │
│                                      │  │ Theme   │ │
│                                      │  ├─────────┤ │
│                                      │  │ ○ Light │ │
│                                      │  │ ● Dark  │ │
│                                      │  │ ○ Auto  │ │
│                                      │  └─────────┘ │
│                                      │              │
│                                      │  [Close]     │
└──────────────────────────────────────┴──────────────┘
```

**Dimensioni:**
- Desktop: drawer 400px wide (fisso)
- Tablet: drawer 350px wide
- Mobile: full screen overlay

---

## 3. SAVE BEHAVIOR - Pattern Ibrido

### 3.1 Best Practices 2026

| Tipo Setting | Save Method | Rationale | Feedback |
|--------------|-------------|-----------|----------|
| **Toggle/Switch** | Auto-save immediato | User expectation, basso rischio | Toast "Saved" 2s |
| **Dropdown/Radio** | Auto-save immediato | Singola scelta, deterministico | Toast "Saved" 2s |
| **Text Input** | Explicit save (bottone) | Dati sensibili, editing complesso | Button highlight |
| **Rich Editor** | Auto-save + Explicit | Draft auto-saved, publish explicit | "Saved 2s ago" |

### 3.2 Regole Miracollook

```javascript
// PSEUDO-CODE PATTERN

// Auto-save settings (UI preferences)
function onToggleChange(setting, value) {
  localStorage.setItem(setting, value);
  showToast("Saved");
}

// Explicit save settings (business data)
function onSignatureEdit(content) {
  setDraft(content);
  // Auto-save draft ogni 2s
  debounce(() => saveDraftToLocalStorage(content), 2000);
}

function onSignatureSave() {
  // Explicit save al server
  await api.updateSignature(draft);
  showToast("Signature saved");
}
```

### 3.3 REGOLA CRITICA

> **MAI mixare auto-save e explicit save NELLA STESSA SEZIONE!**
>
> Confonde utente. Se una sezione ha explicit save, TUTTI i campi in quella sezione devono essere explicit.

**Fonte:** [Damian Wajer - Autosave UX](https://www.damianwajer.com/blog/autosave/)

---

## 4. STORAGE STRATEGY

### 4.1 LocalStorage vs Database

| Tipo Data | Storage | Sync | Max Size | Use Case |
|-----------|---------|------|----------|----------|
| **UI Preferences** | localStorage | No | 5MB | Theme, density, sidebar collapse |
| **Notifications** | localStorage + DB | Si | N/A | Local + server-side logic |
| **Signature** | Database | Si | N/A | Cross-device, business critical |
| **Templates** | Database | Si | N/A | Hotel-wide shared |
| **Keyboard Shortcuts** | localStorage | No | 5MB | Per-device customization |

### 4.2 Hybrid Approach (RACCOMANDATO)

```
PATTERN: localStorage First, Database Backup

FLOW:
1. User cambia setting UI (theme)
   → Salva in localStorage (instant)
   → API call asincrona al DB (background)

2. User cambia business data (signature)
   → Salva SOLO in DB (authoritative)
   → Invalida localStorage cache

3. User login nuovo device
   → Carica settings dal DB
   → Popola localStorage
   → Override con preferences locali (se esistenti)
```

**Vantaggi:**
- Performance: localStorage instant
- Persistence: DB cross-device
- Offline: fallback a localStorage

**Fonte:** [SitePoint - Client-side Storage](https://www.sitepoint.com/client-side-storage-options-comparison/)

### 4.3 Schema Database Proposto

```sql
-- Minimal schema per Settings

CREATE TABLE user_preferences (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  key VARCHAR(100) NOT NULL,      -- "theme", "density", "notifications.desktop"
  value JSONB NOT NULL,            -- Flexible: string, bool, object
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, key)
);

CREATE INDEX idx_user_prefs ON user_preferences(user_id);

-- Hotel-specific settings
CREATE TABLE hotel_email_settings (
  id SERIAL PRIMARY KEY,
  hotel_id INT NOT NULL REFERENCES hotels(id),
  default_signature TEXT,          -- HTML
  quick_reply_templates JSONB,     -- Array di {name, body}
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(hotel_id)
);
```

---

## 5. FEATURES DETTAGLIATE

### 5.1 Account Settings

```
- Display name (read-only, da Google)
- Email address (read-only, OAuth)
- Avatar (Google profile pic + upload custom)
- Logout
```

### 5.2 Appearance Settings

```
THEME:
○ Light
● Dark
○ Auto (system)

DENSITY:
○ Compact (piu email visibili)
● Comfortable (spacing maggiore)
○ Spacious (max readability)

FONT SIZE:
[Slider: Small ──●── Large]

LANGUAGE:
[Dropdown: English, Italiano, etc]
```

### 5.3 Notifications Settings

```
DESKTOP NOTIFICATIONS:
[Toggle ON/OFF]

SOUND:
[Toggle ON/OFF]
[Dropdown: Sound 1, Sound 2, ...]

NOTIFY ME FOR:
☑ New emails in inbox
☑ Replies to my emails
☐ Calendar reminders
☑ @mentions in shared inbox

QUIET HOURS:
[Toggle ON/OFF]
From: [22:00] To: [08:00]
```

**Pattern Superhuman:** Granular per-category control
**Fonte:** [Superhuman Shortcuts](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts)

### 5.4 Signature Settings (CRITICO per Hotel)

```
DEFAULT SIGNATURE:
┌────────────────────────────┐
│ [Rich Text Editor]         │  ← TinyMCE o Tiptap
│                            │
│ Best regards,              │
│ {name}                     │  ← Variables: {name}, {hotel}, {phone}
│ {hotel}                    │
│ {email} | {phone}          │
└────────────────────────────┘

[Save Signature]

HOTEL SIGNATURE TEMPLATES:
- Check-in confirmation
- Check-out thank you
- Booking request
[+ Add Template]
```

**Fonti:**
- [Email Signature Marketing Hotels](https://www.rocketseed.com/email-signature-marketing-for-hotels/)
- [Hotel Email Signatures](https://www.bybrand.io/blog/hospitality/)

### 5.5 Privacy Settings

```
READ RECEIPTS:
[Toggle ON/OFF] - Send read receipts when I open emails

TRACKING PIXELS:
[Toggle ON/OFF] - Block tracking pixels in incoming emails

EXTERNAL IMAGES:
○ Always load
● Ask before loading
○ Never load

DATA SHARING:
[Toggle ON/OFF] - Share usage data to improve Miracollook
```

### 5.6 Keyboard Shortcuts (Advanced)

```
SHORTCUTS ENABLED:
[Toggle ON/OFF]

CUSTOMIZE SHORTCUTS:
Archive               [E]           [Edit]
Reply                 [R]           [Edit]
Reply All             [A]           [Edit]
Forward               [F]           [Edit]
Compose               [C]           [Edit]
Search                [/]           [Edit]
Command Palette       [Cmd+K]       [Edit]

[Reset to Defaults]
```

**Pattern Superhuman:** Cmd+K command palette dominante
**Fonte:** [Superhuman Keyboard Shortcuts](https://nickgray.net/superhuman/)

### 5.7 Hotel Settings (UNICO per Miracollook)

```
DEFAULT HOTEL SIGNATURE:
[Rich Text Editor con template hotel]

QUICK REPLY TEMPLATES:
1. "Room available - [Date]"       [Edit] [Delete]
2. "Booking confirmed"             [Edit] [Delete]
3. "Check-in instructions"         [Edit] [Delete]
[+ Add Template]

STAFF ASSIGNMENT:
When email from booking.com arrives:
→ Assign to: [Dropdown: Reception, Manager, ...]

AUTO-TAG RULES:
booking.com → [Tag: Booking]
airbnb.com  → [Tag: Booking]
@guest      → [Tag: Guest]
```

---

## 6. RESET TO DEFAULTS

```
OGNI sezione settings DEVE avere:

[Reset to Defaults]
↓
Modal conferma:
"Reset all [Category] settings to default?"
[Cancel] [Reset]
↓
Toast: "Settings reset"
```

**Fonte:** [Modal UX Best Practices](https://www.eleken.co/blog-posts/modal-ux)

---

## 7. MOBILE CONSIDERATIONS

### 7.1 Responsive Breakpoints

```
Desktop (>1024px): Drawer 400px laterale
Tablet (768-1023px): Drawer 350px laterale
Mobile (<768px): Full screen overlay con header + back button
```

### 7.2 Touch Optimizations

```
- Toggle switch: min 44px height (touch target)
- Spacing tra opzioni: min 16px
- Scroll smooth con momentum
- Swipe-to-close drawer (mobile)
```

---

## 8. ACCESSIBILITY (WCAG 2.1 AA)

```
REQUIREMENTS:
- Keyboard navigation completa (Tab, Enter, Esc)
- Focus visible su tutti elementi interattivi
- aria-label su tutti toggle/switch
- Color contrast 4.5:1 (text) 3:1 (UI)
- Screen reader: announce "Saved" toast
- Skip to content link
```

**Fonte:** Settings devono essere accessibili come inbox!

---

## 9. EFFORT STIMATO

### 9.1 Breakdown Task

| Task | Ore | Note |
|------|-----|------|
| **Backend API** | 2h | GET/PUT /api/settings/{category} |
| **DB Schema** | 1h | user_preferences + hotel_email_settings |
| **Settings Drawer Component** | 2h | Drawer + routing categorie |
| **7 Categorie UI** | 3h | ~25min/categoria (UI only) |
| **Save Logic** | 1h | Auto-save + explicit + feedback |
| **Rich Text Editor** | 1h | Tiptap integration per signature |
| **Mobile Responsive** | 1h | Breakpoints + touch optimization |
| **Testing** | 1h | Manual testing tutte categorie |
| **TOTALE** | **12h** | ~1.5 giorni |

### 9.2 Split Fasi

```
FASE 1 (MVP - 6h):
- Backend API base
- Drawer component
- Appearance + Signature (2 categorie core)

FASE 2 (Standard - 4h):
- Account + Notifications + Privacy
- Mobile responsive

FASE 3 (Advanced - 2h):
- Keyboard shortcuts
- Hotel settings

FASE 4 (Futuro):
- Team settings (shared inbox)
- Advanced filters/rules
```

---

## 10. DECISIONI ARCHITETTURA

### 10.1 Tech Stack Proposto

```
FRONTEND:
- Component: SettingsDrawer.tsx (React 19)
- Routing: /settings/:category (React Router)
- State: Zustand store per settings cache
- Editor: Tiptap (rich text signature)
- UI: Tailwind v4 custom components

BACKEND:
- GET /api/settings/{category}
- PUT /api/settings/{category}
- GET /api/hotels/{id}/email-settings
- PUT /api/hotels/{id}/email-settings

STORAGE:
- localStorage: UI preferences (instant)
- PostgreSQL: Business data + backup preferences
- Redis: Cache settings per session (optional)
```

### 10.2 API Design

```json
// GET /api/settings/appearance
{
  "theme": "dark",
  "density": "comfortable",
  "fontSize": 16,
  "language": "it"
}

// PUT /api/settings/appearance
// Body: same structure
// Response: { "success": true, "updated_at": "2026-01-15T10:30:00Z" }

// GET /api/hotels/123/email-settings
{
  "default_signature": "<p>Best regards,<br>{name}</p>",
  "quick_reply_templates": [
    {"name": "Room available", "body": "We have a room..."}
  ]
}
```

---

## 11. COMPETITOR COMPARISON

| Feature | Gmail | Outlook | Superhuman | Miracollook |
|---------|-------|---------|------------|-------------|
| Quick Settings Panel | ✅ | ❌ | ❌ | ❌ (non serve) |
| Settings Drawer | ❌ | ✅ | ❌ | ✅ (scelto) |
| Full Settings Page | ✅ | ✅ | ✅ | ❌ (troppo) |
| Auto-save | Partial | ✅ | ✅ | ✅ (hybrid) |
| Signature Editor | Basic | ✅ | ✅ | ✅ (rich) |
| Templates | ❌ | ✅ | ❌ | ✅ (hotel) |
| Command Palette | ❌ | ❌ | ✅ | ✅ (gia fatto) |
| Mobile Full Screen | ✅ | ✅ | ✅ | ✅ |
| Hotel-specific | ❌ | ❌ | ❌ | ✅ (UNICO!) |

---

## 12. NEXT STEPS

```
QUANDO IMPLEMENTARE:
- DOPO: Bulk Actions, Labels, Contacts (Sprint 3)
- PRIMA: PMS Integration (Fase 2)

RATIONALE:
Settings NON sono blocker per usabilita core.
Users possono usare defaults fino a Sprint 4.

PRIORITA: MEDIA (non urgente, ma necessario per professionalità)
```

---

## FONTI

### UX Patterns & Best Practices
- [CSS-Tricks - Email Settings UI Patterns](https://css-tricks.com/ui-pattern-ideas-email-settings/)
- [Eleken - Modal UX Best Practices](https://www.eleken.co/blog-posts/modal-ux)
- [Damian Wajer - Autosave vs Explicit Save](https://www.damianwajer.com/blog/autosave/)
- [Primer Style - Saving Patterns](https://primer.style/ui-patterns/saving/)

### Email Client Analysis
- [Superhuman Keyboard Shortcuts](https://nickgray.net/superhuman/)
- [Superhuman Help - Speed Up With Shortcuts](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts)
- [Mailbird - Privacy Email Settings 2026](https://www.getmailbird.com/privacy-email-settings-configuration-guide/)

### Storage & Technical
- [SitePoint - Client-side Storage Options](https://www.sitepoint.com/client-side-storage-options-comparison/)
- [RxDB - localStorage Guide](https://rxdb.info/articles/localstorage.html)
- [Dev.to - Web Storage Guide](https://dev.to/austinwdigital/a-guide-to-web-storage-localstorage-sessions-cookies-more-1fbm)

### Hotel Email Signatures
- [Rocketseed - Email Signature Marketing Hotels](https://www.rocketseed.com/email-signature-marketing-for-hotels/)
- [Bybrand - Hotel Email Signatures](https://www.bybrand.io/blog/hospitality/)
- [Email Signature Rescue - Hotel Templates](https://emailsignaturerescue.com/email-signatures/industries/hotels)

### Modern Email Trends 2026
- [Top Business Software - Email Clients 2026](https://topbusinesssoftware.com/categories/email-clients/)
- [Mailbird - Best Email Clients macOS 2026](https://www.getmailbird.com/best-email-client-alternatives-macos/)

---

## COSTITUZIONE-APPLIED

**COSTITUZIONE-APPLIED:** SI

**Principio usato:** RICERCA PRIMA DI IMPLEMENTARE (Pilastro #1 Formula Magica)

**Come applicato:**
1. RICERCATO big players (Gmail, Outlook, Superhuman) per pattern consolidati
2. ANALIZZATO storage strategies (localStorage vs DB) con fonti tecniche
3. IDENTIFICATO best practices UX (auto-save vs explicit) da esperti 2026
4. PROPOSTO architettura MACRO basata su ricerca, non invenzione
5. STIMATO effort realisticamente (8-12h) senza fretta

**Visione MACRO mantenuta:** Nessun dettaglio implementativo, solo pattern e decisioni strategiche. Marketing/Ingegnera valideranno prima di implementare.

*"Non inventare! Studiare come fanno i big!"* ✅

---

*Studio creato: 15 Gennaio 2026 - Sessione 224*
*Researcher: Cervella Researcher*
*"I dettagli fanno SEMPRE la differenza!"*
