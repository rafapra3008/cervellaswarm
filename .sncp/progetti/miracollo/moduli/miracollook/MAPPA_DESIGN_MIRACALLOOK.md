# MAPPA DESIGN MIRACALLOOK

> **Creato:** 12 Gennaio 2026 - Sessione 175
> **Basato su:** 4 ricerche parallele (researcher, marketing, ingegnera, explorer)
> **Filosofia:** "Design impone rispetto!"

---

## PROBLEMA ATTUALE

```
+================================================================+
|                                                                |
|   UI Health: 6/10                                              |
|                                                                |
|   PROBLEMI PRINCIPALI:                                         |
|   1. ThreePanel layout rotto (parent non coordina children)    |
|   2. Proporzioni colonne sbagliate                             |
|   3. Dark mode inconsistente                                   |
|   4. Guest Sidebar non visibile                                |
|   5. Spacing non uniforme                                      |
|   6. Font generici (non brand Miracollo)                       |
|                                                                |
+================================================================+
```

---

## DESIGN SYSTEM MIRACOLLO (da seguire)

### Colori
```css
/* BACKGROUND */
--bg-primary: #0a0e1a
--bg-secondary: #111827
--bg-card: #1a1f35
--bg-card-hover: #232942

/* TEXT */
--text-primary: #f8fafc
--text-secondary: #94a3b8
--text-muted: #64748b

/* ACCENT */
--accent-primary: #6366f1 (indigo)
--accent-secondary: #8b5cf6 (viola)
--accent-success: #10b981 (verde)
--accent-warning: #f59e0b (giallo)
--accent-danger: #ef4444 (rosso)
--accent-info: #3b82f6 (blu)

/* BORDER */
--border-color: #2d3654
--border-radius: 12px
--border-radius-sm: 8px
```

### Fonts
```css
/* Headings */
font-family: 'Outfit', -apple-system, sans-serif;

/* Data/Numbers */
font-family: 'JetBrains Mono', monospace;

/* Body (alternative) */
font-family: 'Inter', -apple-system, sans-serif;
```

### Spacing (8px grid)
```
4px  - extra small
8px  - small
12px - medium
16px - standard
24px - large
32px - extra large
```

### Effects
```css
/* Shadows */
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
--shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);

/* Transitions */
--transition-fast: 0.15s ease;
--transition-normal: 0.25s ease;

/* Hover */
transform: translateY(-2px);
```

---

## PROPORZIONI LAYOUT

```
+--------+------------+------------------+------------+
| SIDEBAR|   LISTA    |     DETTAGLIO    |   GUEST    |
| 200px  |   320px    |      flex-1      |   280px    |
| fixed  |   fixed    |     (min 400)    | conditional|
+--------+------------+------------------+------------+

TOTALE: ~1200px+ desktop
MOBILE: Stack verticale
```

---

## ROADMAP IMPLEMENTAZIONE

### FASE 1: FIX LAYOUT (30 min) - CRITICO!
```
[x] Fix ThreePanel.tsx - parent controlla widths
[x] Sidebar: w-[200px] fixed
[x] EmailList: w-[320px] fixed
[x] EmailDetail: flex-1 min-w-[400px]
[x] GuestSidebar: w-[280px] conditional
[x] Overflow scroll corretti
```

### FASE 2: COLORI MIRACOLLO (30 min)
```
[ ] Aggiorna tailwind.config.js con design tokens
[ ] Background: bg-[#0a0e1a] invece di bg-gray-900
[ ] Accent: indigo-500 (#6366f1)
[ ] Border: border-[#2d3654]
[ ] Text hierarchy corretta
```

### FASE 3: TYPOGRAPHY (20 min)
```
[ ] Import Google Fonts (Outfit, JetBrains Mono)
[ ] Headings: Outfit
[ ] Data/numbers: JetBrains Mono
[ ] Body: Inter o system
[ ] Size hierarchy corretta
```

### FASE 4: COMPONENTI POLISH (45 min)
```
[ ] EmailListItem: hover effect, selected state
[ ] Sidebar: nav-item active style
[ ] Buttons: gradient + glow
[ ] Cards: border + shadow
[ ] Badges: status colors
```

### FASE 5: GUEST SIDEBAR PREMIUM (30 min)
```
[ ] Glassmorphism effect
[ ] Avatar con gradient
[ ] Booking info cards
[ ] VIP badge gold
[ ] Action buttons styled
```

### FASE 6: ANIMATIONS (20 min)
```
[ ] Hover transitions (0.15s)
[ ] Selected transitions
[ ] Bundle collapse animation
[ ] Modal fade in
```

### FASE 7: RESPONSIVE (30 min)
```
[ ] Breakpoint 1200px: collapse guest sidebar
[ ] Breakpoint 768px: hide email list, full detail
[ ] Breakpoint 480px: mobile stack
```

---

## CHECKLIST QUALITA

### Must Have
- [ ] Layout non si rompe
- [ ] Tutte le colonne visibili
- [ ] Guest Sidebar appare quando serve
- [ ] Dark mode consistente
- [ ] Text leggibile (contrast ratio)

### Nice to Have
- [ ] Glassmorphism effects
- [ ] Smooth animations
- [ ] Keyboard shortcuts visual feedback
- [ ] Loading states

### Future
- [ ] Light mode toggle
- [ ] Density options (compact/comfortable)
- [ ] Custom themes

---

## PRIORITA

```
P0 (OGGI):
- FASE 1: Fix layout
- FASE 2: Colori base

P1 (PROSSIMA SESSIONE):
- FASE 3: Typography
- FASE 4: Components polish

P2 (FUTURO):
- FASE 5-7: Premium features
```

---

## FILE DA MODIFICARE

| File | Cosa |
|------|------|
| `tailwind.config.js` | Design tokens, colors, fonts |
| `src/index.css` | Global styles, font imports |
| `ThreePanel.tsx` | Layout fix |
| `Sidebar.tsx` | Width + styling |
| `EmailList.tsx` | Width + styling |
| `EmailDetail.tsx` | Flex + styling |
| `GuestSidebar.tsx` | Width + premium styling |
| `EmailListItem.tsx` | Hover/selected states |

---

## RIFERIMENTI

| Doc | Path |
|-----|------|
| Design Patterns Email | `studi/DESIGN_PATTERNS_EMAIL.md` |
| UX Strategy | `studi/UX_STRATEGY_MIRACALLOOK.md` |
| Analisi Codebase | `studi/ANALISI_CODEBASE_UI.md` |
| Design Miracollo | (explorer output) |

---

*"Design impone rispetto!" - Ogni pixel conta!*
*"Una cosa alla volta, fatta BENE!" - La Formula Magica*
