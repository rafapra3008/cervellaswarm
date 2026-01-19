# MIRACOLLOOK SIDEBAR - DESIGN SPECS COMPLETE

> **Status**: DESIGN SPECS FINALI - READY FOR IMPLEMENTATION
> **Data**: 13 Gennaio 2026
> **Designer**: Cervella Marketing
> **Riferimento**: Miracollo PMS Sidebar (style.css)

---

## OBIETTIVO

Trasformare la sidebar attuale di Miracollook da semplice lista testuale a sidebar **professionale e premium** come Miracollo PMS, mantenendo coerenza visiva nel design system.

---

## 1. LAYOUT & STRUTTURA

### Dimensioni Sidebar

```
Width: 200px (fixed)
Height: 100vh (full screen)
Position: fixed, left: 0, top: 0
Z-index: 100
```

### Struttura Verticale (3 sezioni)

```
┌────────────────────────┐
│  HEADER                │ ← Logo + Version (60px height)
├────────────────────────┤
│  COMPOSE BUTTON        │ ← 16px padding top/bottom
├────────────────────────┤
│                        │
│  NAV MENU              │ ← Flex: 1 (occupa spazio)
│  (scrollable)          │   Categories con icone
│                        │
│                        │
├────────────────────────┤
│  FOOTER                │ ← Status/Info (optional)
└────────────────────────┘
```

---

## 2. HEADER SECTION

### Logo + Version

**Layout:**
```
Padding: 20px 16px
Border-bottom: 1px solid #2d3654
Display: flex
Align-items: center
Justify-content: space-between
```

**Logo Text:**
```
Font: Outfit
Font-size: 18px (1.125rem)
Font-weight: 600 (semibold)
Gradient: linear-gradient(135deg, #6366f1, #8b5cf6)
-webkit-background-clip: text
-webkit-text-fill-color: transparent
```

**Version Badge (optional):**
```
Font: JetBrains Mono
Font-size: 11px (0.7rem)
Color: #64748b
Background: #151a2e
Padding: 4px 8px
Border-radius: 6px
```

**Tailwind Classes:**
```tsx
<div className="px-4 py-5 border-b border-miracollo-border flex items-center justify-between">
  <h1 className="text-lg font-semibold font-outfit bg-gradient-to-br from-miracollo-accent to-miracollo-accent-secondary bg-clip-text text-transparent">
    MiracOllook
  </h1>
  <span className="font-jetbrains text-[11px] text-miracollo-text-muted bg-miracollo-bg-input px-2 py-1 rounded-md">
    v1.0
  </span>
</div>
```

---

## 3. COMPOSE BUTTON

### Design

**Container:**
```
Padding: 16px
```

**Button:**
```
Width: 100%
Height: 44px
Background: linear-gradient(135deg, #6366f1, #8b5cf6)
Border-radius: 8px
Box-shadow: 0 0 20px rgba(99, 102, 241, 0.3)
Font-weight: 600
Color: #ffffff
Transition: all 0.15s ease
```

**Hover State:**
```
Transform: translateY(-2px)
Box-shadow: 0 0 30px rgba(99, 102, 241, 0.4)
```

**Icon:**
- Heroicon: `PencilSquareIcon` (outline)
- Size: 20px (w-5 h-5)
- Position: Prima del testo

**Shortcut Badge:**
```
Font-size: 11px
Opacity: 0.7
Margin-left: auto
```

**Tailwind Classes:**
```tsx
<button className="btn-gradient w-full h-11 px-4 rounded-miracollo-sm font-semibold text-white flex items-center justify-center gap-2 transition-fast hover:-translate-y-0.5">
  <PencilSquareIcon className="w-5 h-5" />
  <span>Compose</span>
  <span className="text-[11px] opacity-70 ml-auto">(C)</span>
</button>
```

---

## 4. NAV MENU - CATEGORIES

### Container

```
Flex: 1 (espande per occupare spazio disponibile)
Padding: 12px 8px
Overflow-y: auto (scroll se necessario)
Display: flex
Flex-direction: column
Gap: 2px (tra items)
```

### Category Items

**Anatomia Item:**
```
Display: flex
Align-items: center
Gap: 12px (tra icona e label)
Padding: 14px 16px (vertical | horizontal)
Border-radius: 8px
Transition: all 0.15s ease
Font-size: 14px (0.875rem)
Font-weight: 500
```

**State: Normal (inactive):**
```
Background: transparent
Color: #94a3b8 (text-secondary)
```

**State: Hover:**
```
Background: #232942 (bg-hover)
Color: #f8fafc (text-primary)
Cursor: pointer
```

**State: Active (selected):**
```
Background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.1))
Color: #f8fafc (text-primary)
Border-left: 3px solid #6366f1
```

**Badge Count:**
```
Font-size: 11px
Color: #64748b (text-muted)
Margin-left: auto
Font: JetBrains Mono
```

**Tailwind Classes (Normal):**
```tsx
<button className="flex items-center gap-3 px-4 py-3.5 rounded-miracollo-sm text-miracollo-text-secondary hover:bg-miracollo-bg-hover hover:text-miracollo-text transition-fast cursor-pointer w-full text-left">
  {/* Icon */}
  {/* Label */}
  {/* Count badge */}
</button>
```

**Tailwind Classes (Active):**
```tsx
<button className="flex items-center gap-3 px-4 py-3.5 rounded-miracollo-sm bg-gradient-to-br from-miracollo-accent/20 to-miracollo-accent-secondary/10 text-miracollo-text border-l-[3px] border-miracollo-accent w-full text-left">
  {/* Icon */}
  {/* Label */}
  {/* Count badge */}
</button>
```

---

## 5. ICONE - HEROICONS + COLORI

### Mapping Categorie → Icone + Colori

| Categoria | Heroicon | Variante | Colore HEX | Nome CSS |
|-----------|----------|----------|------------|----------|
| **All** | `InboxIcon` | outline | #6366f1 | accent-primary |
| **VIP** | `StarIcon` | solid | #f59e0b | warning (gold) |
| **Check-in** | `CalendarDaysIcon` | outline | #3b82f6 | info (blue) |
| **Team** | `UsersIcon` | outline | #8b5cf6 | accent-secondary (purple) |
| **Fornitori** | `TruckIcon` | outline | #f97316 | orange |
| **Newsletter** | `NewspaperIcon` | outline | #64748b | text-muted (gray) |
| **System** | `Cog6ToothIcon` | outline | #6b7280 | gray |
| **Other** | `EnvelopeIcon` | outline | #94a3b8 | text-secondary |

### Note Icone

1. **Dimensione**: 20px (w-5 h-5)
2. **Import** da `@heroicons/react/24/outline` (o `/solid` per StarIcon)
3. **Color inline style**: `style={{ color: '#f59e0b' }}`

**Esempio implementazione:**
```tsx
import { InboxIcon, StarIcon, CalendarDaysIcon, UsersIcon, TruckIcon, NewspaperIcon, Cog6ToothIcon, EnvelopeIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolid } from '@heroicons/react/24/solid';

const categoryIcons: Record<EmailCategory, { Icon: any, color: string }> = {
  all: { Icon: InboxIcon, color: '#6366f1' },
  vip: { Icon: StarSolid, color: '#f59e0b' },
  checkin: { Icon: CalendarDaysIcon, color: '#3b82f6' },
  team: { Icon: UsersIcon, color: '#8b5cf6' },
  fornitori: { Icon: TruckIcon, color: '#f97316' },
  newsletter: { Icon: NewspaperIcon, color: '#64748b' },
  system: { Icon: Cog6ToothIcon, color: '#6b7280' },
  other: { Icon: EnvelopeIcon, color: '#94a3b8' },
};

// Uso:
const { Icon, color } = categoryIcons[category];
<Icon className="w-5 h-5" style={{ color }} />
```

---

## 6. SEPARATOR "CATEGORIES"

**Dopo "All" e prima delle altre categorie:**

```
Margin-top: 16px
Padding: 8px 16px
Text: "CATEGORIES"
Font-size: 11px (0.7rem)
Font-weight: 600
Text-transform: uppercase
Letter-spacing: 0.05em (tracking-wider)
Color: #64748b (text-muted)
```

**Tailwind:**
```tsx
<div className="text-[11px] font-semibold uppercase tracking-wider text-miracollo-text-muted px-4 py-2 mt-4">
  Categories
</div>
```

---

## 7. FOOTER SECTION (OPTIONAL)

### Status Indicator

**Se vogliamo mostrare status utente/connessione:**

```
Padding: 16px
Border-top: 1px solid #2d3654
Display: flex
Align-items: center
Gap: 8px
```

**Status Dot:**
```
Width: 8px
Height: 8px
Border-radius: 50%
Background: #10b981 (green - connesso)
```

**Status Text:**
```
Font-size: 12px (0.75rem)
Color: #64748b (text-muted)
```

**Tailwind:**
```tsx
<div className="p-4 border-t border-miracollo-border flex items-center gap-2">
  <div className="w-2 h-2 rounded-full bg-miracollo-success"></div>
  <span className="text-xs text-miracollo-text-muted">Connected</span>
</div>
```

**ALTERNATIVA - Keyboard Shortcuts Hint (come ora):**
```tsx
<div className="p-4 border-t border-miracollo-border text-xs text-miracollo-text-secondary space-y-2">
  <div>
    Press <kbd className="px-1 py-0.5 bg-miracollo-bg-secondary rounded text-miracollo-text-muted">?</kbd> for shortcuts
  </div>
  <div>
    Press <kbd className="px-1 py-0.5 bg-miracollo-bg-secondary rounded text-miracollo-text-muted">⌘K</kbd> for commands
  </div>
</div>
```

---

## 8. COLORI - PALETTE COMPLETA

### Background

| Token | HEX | Uso |
|-------|-----|-----|
| `miracollo-bg` | #0a0e1a | Background principale sidebar |
| `miracollo-bg-secondary` | #111827 | Background alternativo |
| `miracollo-bg-card` | #1a1f35 | Card/Panel |
| `miracollo-bg-hover` | #232942 | Hover state item |
| `miracollo-bg-input` | #151a2e | Input field, badge version |

### Text

| Token | HEX | Uso |
|-------|-----|-----|
| `miracollo-text` | #f8fafc | Testo primario (active) |
| `miracollo-text-secondary` | #94a3b8 | Testo item normale |
| `miracollo-text-muted` | #64748b | Badge count, separator |

### Accent

| Token | HEX | Uso |
|-------|-----|-----|
| `miracollo-accent` | #6366f1 | Accent principale (Compose, border active) |
| `miracollo-accent-secondary` | #8b5cf6 | Gradient stop, purple |
| `miracollo-success` | #10b981 | Status green |
| `miracollo-warning` | #f59e0b | VIP gold |
| `miracollo-danger` | #ef4444 | Errori (se serve) |
| `miracollo-info` | #3b82f6 | Check-in blue |

### Border

| Token | HEX | Uso |
|-------|-----|-----|
| `miracollo-border` | #2d3654 | Border header, footer |

---

## 9. TYPOGRAPHY

### Font Families

```
Logo/Headings: 'Outfit', system-ui, sans-serif
Body/Labels: 'Inter', system-ui, sans-serif
Data/Badges: 'JetBrains Mono', monospace
```

**Nota:** Fonts già importati in `index.css`

### Font Sizes

| Elemento | Size | Tailwind |
|----------|------|----------|
| Logo | 18px | text-lg |
| Nav item label | 14px | text-sm |
| Badge count | 11px | text-[11px] |
| Separator | 11px | text-[11px] |
| Footer hint | 12px | text-xs |
| Version badge | 11px | text-[11px] |

### Font Weights

| Elemento | Weight | Tailwind |
|----------|--------|----------|
| Logo | 600 | font-semibold |
| Nav item label | 500 | font-medium |
| Compose button | 600 | font-semibold |
| Separator | 600 | font-semibold |

---

## 10. SPACING & PADDING

| Elemento | Padding/Margin |
|----------|----------------|
| Sidebar header | px-4 py-5 |
| Compose container | p-4 |
| Compose button | px-4 h-11 |
| Nav menu container | p-3 (12px all) |
| Nav item | px-4 py-3.5 |
| Gap icona-label | gap-3 (12px) |
| Gap tra items | gap-0.5 (2px) - via parent flex |
| Separator | px-4 py-2 mt-4 |
| Footer | p-4 |

---

## 11. BORDER RADIUS

| Elemento | Radius | Tailwind |
|----------|--------|----------|
| Compose button | 8px | rounded-miracollo-sm |
| Nav items | 8px | rounded-miracollo-sm |
| Version badge | 6px | rounded-md |
| Status dot | 50% | rounded-full |

---

## 12. TRANSITIONS & ANIMATIONS

### Hover Transitions

```css
transition: all 0.15s ease;
```

**Tailwind:** `transition-fast` (definito in config)

### Compose Button Hover

```css
transform: translateY(-2px);
box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
```

**Tailwind:** `hover:-translate-y-0.5`

---

## 13. SHADOWS

### Compose Button

**Normal:**
```
box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
```

**Hover:**
```
box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
```

**Tailwind:** Già incluso in classe `.btn-gradient`

---

## 14. STATI INTERATTIVI - RECAP

### Nav Item States

| Stato | Background | Text Color | Border | Cursor |
|-------|------------|------------|--------|--------|
| **Normal** | transparent | #94a3b8 | none | default |
| **Hover** | #232942 | #f8fafc | none | pointer |
| **Active** | gradient (#6366f1/20 → #8b5cf6/10) | #f8fafc | 3px left #6366f1 | default |

### Compose Button States

| Stato | Transform | Shadow |
|-------|-----------|--------|
| **Normal** | none | 0 0 20px rgba(99,102,241,0.3) |
| **Hover** | translateY(-2px) | 0 0 30px rgba(99,102,241,0.4) |
| **Active (click)** | translateY(0) | 0 0 15px rgba(99,102,241,0.2) |

---

## 15. SCROLLBAR STYLING (NAV MENU)

```css
/* Già definito in index.css - applica a tutta app */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #111827;
}

::-webkit-scrollbar-thumb {
  background: #2d3654;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #3d4664;
}
```

---

## 16. ACCESSIBILITY

### Keyboard Navigation

- Tutti gli item devono essere `<button>` (già sono)
- Focus ring visibile: `*:focus-visible { outline: 2px solid #6366f1; outline-offset: 2px; }` (già in index.css)

### Aria Labels

```tsx
<button aria-label="Compose new email" aria-keyshortcuts="c">
  ...
</button>

<button aria-label={`${getCategoryLabel(category)} - ${count} emails`} aria-current={active ? 'page' : undefined}>
  ...
</button>
```

---

## 17. RESPONSIVE (FUTURE - Desktop First)

**Current:** Fixed 200px sidebar, desktop only

**Future P3:**
- Mobile: Sidebar collapsible/offcanvas
- Breakpoint: < 768px
- Toggle button in header

---

## 18. ESEMPIO CODICE COMPLETO

### SidebarNew.tsx (Struttura proposta)

```tsx
import {
  InboxIcon,
  CalendarDaysIcon,
  UsersIcon,
  TruckIcon,
  NewspaperIcon,
  Cog6ToothIcon,
  EnvelopeIcon,
  PencilSquareIcon
} from '@heroicons/react/24/outline';
import { StarIcon } from '@heroicons/react/24/solid';
import type { EmailCategory } from '../../types/email';
import { getCategoryLabel } from '../../utils/categorize';

interface SidebarProps {
  onCompose: () => void;
  selectedCategory: EmailCategory;
  onSelectCategory: (category: EmailCategory) => void;
  categoryCounts: Record<EmailCategory, number>;
}

const categoryConfig: Record<EmailCategory, { Icon: any, color: string }> = {
  all: { Icon: InboxIcon, color: '#6366f1' },
  vip: { Icon: StarIcon, color: '#f59e0b' },
  checkin: { Icon: CalendarDaysIcon, color: '#3b82f6' },
  team: { Icon: UsersIcon, color: '#8b5cf6' },
  fornitori: { Icon: TruckIcon, color: '#f97316' },
  newsletter: { Icon: NewspaperIcon, color: '#64748b' },
  system: { Icon: Cog6ToothIcon, color: '#6b7280' },
  other: { Icon: EnvelopeIcon, color: '#94a3b8' },
};

export const SidebarNew = ({
  onCompose,
  selectedCategory,
  onSelectCategory,
  categoryCounts,
}: SidebarProps) => {
  const categories: EmailCategory[] = [
    'all',
    'vip',
    'checkin',
    'team',
    'fornitori',
    'newsletter',
    'system',
    'other',
  ];

  const renderItem = (category: EmailCategory) => {
    const { Icon, color } = categoryConfig[category];
    const isActive = selectedCategory === category;
    const count = categoryCounts[category];

    return (
      <button
        key={category}
        onClick={() => onSelectCategory(category)}
        aria-label={`${getCategoryLabel(category)} - ${count} emails`}
        aria-current={isActive ? 'page' : undefined}
        className={`
          flex items-center gap-3 px-4 py-3.5 rounded-miracollo-sm
          transition-fast cursor-pointer w-full text-left
          ${isActive
            ? 'bg-gradient-to-br from-miracollo-accent/20 to-miracollo-accent-secondary/10 text-miracollo-text border-l-[3px] border-miracollo-accent'
            : 'text-miracollo-text-secondary hover:bg-miracollo-bg-hover hover:text-miracollo-text'
          }
        `}
      >
        <Icon className="w-5 h-5" style={{ color }} />
        <span className="font-medium flex-1">{getCategoryLabel(category)}</span>
        {count > 0 && (
          <span className="text-[11px] text-miracollo-text-muted font-jetbrains">
            {count}
          </span>
        )}
      </button>
    );
  };

  return (
    <div className="h-full bg-miracollo-bg flex flex-col w-[200px] fixed left-0 top-0 z-[100] border-r border-miracollo-border">
      {/* Header */}
      <div className="px-4 py-5 border-b border-miracollo-border flex items-center justify-between">
        <h1 className="text-lg font-semibold font-outfit bg-gradient-to-br from-miracollo-accent to-miracollo-accent-secondary bg-clip-text text-transparent">
          MiracOllook
        </h1>
        <span className="font-jetbrains text-[11px] text-miracollo-text-muted bg-miracollo-bg-input px-2 py-1 rounded-md">
          v1.0
        </span>
      </div>

      {/* Compose Button */}
      <div className="p-4">
        <button
          onClick={onCompose}
          aria-label="Compose new email"
          aria-keyshortcuts="c"
          className="btn-gradient w-full h-11 px-4 rounded-miracollo-sm font-semibold text-white flex items-center justify-center gap-2 transition-fast hover:-translate-y-0.5"
        >
          <PencilSquareIcon className="w-5 h-5" />
          <span>Compose</span>
          <span className="text-[11px] opacity-70 ml-auto">(C)</span>
        </button>
      </div>

      {/* Categories */}
      <nav className="flex-1 px-3 py-3 overflow-y-auto flex flex-col gap-0.5">
        {/* All */}
        {renderItem('all')}

        {/* Separator */}
        <div className="text-[11px] font-semibold uppercase tracking-wider text-miracollo-text-muted px-4 py-2 mt-4">
          Categories
        </div>

        {/* Other Categories */}
        {categories.slice(1).map(renderItem)}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-miracollo-border text-xs text-miracollo-text-secondary space-y-2">
        <div>
          Press <kbd className="px-1 py-0.5 bg-miracollo-bg-secondary rounded text-miracollo-text-muted">?</kbd> for shortcuts
        </div>
        <div>
          Press <kbd className="px-1 py-0.5 bg-miracollo-bg-secondary rounded text-miracollo-text-muted">⌘K</kbd> for commands
        </div>
      </div>
    </div>
  );
};
```

---

## 19. CHECKLIST IMPLEMENTAZIONE

### Step 1: Setup Icone
- [ ] Installa `@heroicons/react` (probabilmente già installato)
- [ ] Verifica import in package.json

### Step 2: Crea categoryConfig
- [ ] File `utils/categoryConfig.ts` con mapping icone/colori
- [ ] Export const con Record<EmailCategory, ...>

### Step 3: Update Sidebar Component
- [ ] Rename `Sidebar.tsx` → `SidebarOld.tsx` (backup)
- [ ] Crea `SidebarNew.tsx` con nuovo design
- [ ] Usa Heroicons invece emoji
- [ ] Applica colori inline style per icone

### Step 4: Verifica Tailwind Config
- [ ] Tutti i token esistono (già OK!)
- [ ] `.btn-gradient` classe globale (già in index.css)
- [ ] `transition-fast` funziona

### Step 5: Test Stati
- [ ] Hover funziona su items
- [ ] Active state mostra border sinistra
- [ ] Compose button hover lift effect
- [ ] Scroll nav menu se categorie molte

### Step 6: Accessibility
- [ ] Aggiungere aria-labels
- [ ] Test keyboard navigation (Tab, Enter, Space)
- [ ] Focus ring visibile

### Step 7: Polish
- [ ] Spacing perfetto (usa inspector)
- [ ] Colori icone corretti
- [ ] Version badge posizionato bene
- [ ] Footer hint leggibile

---

## 20. METRICHE SUCCESSO

**Design è COMPLETO quando:**

- [ ] Sidebar visivamente identica a Miracollo PMS (sidebar structure)
- [ ] Icone colorate per OGNI categoria
- [ ] Hover states smooth (150ms)
- [ ] Active state mostra gradient + border
- [ ] Compose button ha glow effect
- [ ] Logo ha gradient text
- [ ] Version badge visibile ma discreto
- [ ] Nessuna emoji, solo Heroicons professionali
- [ ] Mobile: sidebar fixed, no responsive (P3 future)

---

## 21. DECISIONI DESIGN

### Perché 200px invece 260px?
- Miracollook ha meno voci menu (8 vs 15+ di Miracollo)
- Più spazio per email list (critico in email client)
- Coerenza con layout ThreePanel esistente

### Perché Heroicons outline (non solid)?
- Più leggere visivamente
- Coerenza Miracollo PMS (usa outline)
- Eccezione: StarIcon VIP usa solid (più impatto)

### Perché versione badge?
- Professional look (SaaS standard)
- Allineato con Miracollo PMS
- Opzionale: può essere rimosso

### Perché footer hints invece status?
- Utenti già vedono stato connessione Gmail altrove
- Keyboard hints più utili per power users
- Coerenza con UX attuale

---

## 22. VANTAGGIO COMPETITIVO

**Questa sidebar rende MiracOllook:**

✅ **Professionale** - Design che impone rispetto
✅ **Coerente** - Stessa visual language di Miracollo
✅ **Usabile** - Icone colorate = riconoscimento veloce
✅ **Scalabile** - Facile aggiungere categorie
✅ **Accessibile** - Keyboard + screen reader ready

---

## 23. NOTE IMPLEMENTAZIONE

### File da Modificare

```
miracallook/frontend/src/
├── components/
│   └── Sidebar/
│       ├── SidebarOld.tsx     (backup)
│       └── Sidebar.tsx         (nuovo design)
├── utils/
│   └── categoryConfig.ts       (NUOVO - icone mapping)
└── index.css                   (già OK!)
```

### Dependencies Check

```bash
# Verifica Heroicons installato
grep "@heroicons/react" package.json

# Se non c'è:
npm install @heroicons/react
```

### Test Visual

**Checklist visuale:**
1. Apri app in browser
2. Sidebar width esatto 200px (inspector)
3. Logo gradient visibile
4. Compose button glow al hover
5. Ogni icona colore corretto
6. Active item: gradient bg + border left
7. Separator "CATEGORIES" uppercase
8. Footer hints leggibili

---

## CONCLUSIONE

```
+================================================================+
|                                                                |
|   SIDEBAR DESIGN: COMPLETO E IMPLEMENTABILE                   |
|                                                                |
|   SPECS INCLUDE:                                               |
|   ✓ Layout struttura completa                                 |
|   ✓ Colori esatti (hex)                                       |
|   ✓ Icone Heroicons + colori                                  |
|   ✓ Typography (font, size, weight)                           |
|   ✓ Spacing (padding, margin, gap)                            |
|   ✓ Stati interattivi (normal, hover, active)                 |
|   ✓ Codice esempio completo                                   |
|   ✓ Checklist implementazione                                 |
|                                                                |
|   READY FOR: cervella-frontend                                |
|                                                                |
|   "Il design impone rispetto!"                                |
|                                                                |
+================================================================+
```

---

**Design by:** Cervella Marketing
**Data:** 13 Gennaio 2026
**Sessione:** 181
**Next:** Pass to cervella-frontend for implementation

*"Ogni pixel deve contare!"*
