# RICERCA: Email List Design Best Practices

> "I dettagli fanno SEMPRE la differenza!"
> Ricerca condotta: 13 Gennaio 2026
> Per: Miracollook Email Client

---

## Executive Summary

**TL;DR:** I migliori email client usano:
- **Spacing:** 8px base grid, 12-16px padding verticale per item
- **Typography:** 14-16px body, line-height 1.4-1.6x, sender più bold
- **Unread:** Combinazione bold text + dot/background change
- **Grouping:** Headers sticky con "Today/Yesterday/Last Week"
- **Hover:** Background subtle change (5-10% opacity) + quick actions reveal
- **Selected:** Border left accent + background change

---

## 1. SPACING - Design Specifications

### Grid System Foundation

**Base Grid: 8px**
- Tutti i valori di spacing sono multipli di 8px (8, 16, 24, 32)
- Uso opzionale del mezzo step (4px) per micro-adjustments
- Principio: "Ogni spazio tra elementi divisibile per 4"

**Email List Item Padding**
```css
/* Pattern Comune */
padding: 12px 16px; /* Verticale: 12px, Orizzontale: 16px */

/* Alternative osservate */
padding: 16px;      /* Superhuman: Padding uniforme */
padding: 8px 16px;  /* Più compatto */
```

**Gap tra Elementi**
- Gap tra sender e subject: **4px**
- Gap tra subject e preview text: **2-4px**
- Gap tra email items: **0px** (border separator invece)
- Gap tra date groups: **16-24px**

**Internal ≤ External Rule**
- Padding interno item: 12-16px
- Margin tra gruppi: 16-24px (sempre ≥ padding interno)

### Squish Pattern per List Items

**"Squished Inset"** - Riduzione padding verticale del 50%
```
Normal:   padding: 16px
Squished: padding: 8px 16px (top/bottom ridotto)
```

Usato da: Linear, Gmail (vista compatta)

**Fonte:** [UI Spacing Guidelines](https://medium.com/dwarves-design/the-principle-of-spacing-part-2-e3cf31b909fa), [Design Systems Spacing](https://www.designsystems.com/space-grids-and-layouts/)

---

## 2. TYPOGRAPHY - Font Size & Line Height

### Sender Name
```
Font Size:   14-16px
Font Weight: 600 (semibold) unread, 400 (normal) read
Line Height: 20-24px (1.4-1.5x)
Color:       Near-black (#1a1a1a light) / Near-white (#f0f0f0 dark)
```

### Subject Line
```
Font Size:   14-15px
Font Weight: 600 unread, 400 read
Line Height: 20-22px
Color:       Same as sender (primary text)
Truncation:  Single line, ellipsis
```

### Preview Text (Pre-header)
```
Font Size:   12-13px (più piccolo di subject)
Font Weight: 400 (normal sempre)
Line Height: 18-20px
Color:       Secondary (#666 light, #999 dark)
Opacity:     60-70%
Truncation:  Single line, ellipsis
```

### Best Practices
- **Sender più grande del subject** (pattern Outlook 2013/2016)
- **Line Height: 1.4-1.6x** font size (prevent crowding)
- **Preview text 11-12px** (trovato in 51% dei top email clients)

**Fonte:** [Smashing Magazine Typography](https://www.smashingmagazine.com/2015/08/typographic-patterns-in-html-newsletter-email-design/), [Email Typography Best Practices](https://www.emailmavlers.com/blog/email-typography-guide/)

---

## 3. RAGGRUPPAMENTO PER DATA

### Pattern Standard

**Categorie comuni:**
- Today
- Yesterday
- Last Week
- Last Month
- Older

**Implementazione:**

#### Outlook Pattern
```
┌─────────────────────────────────┐
│ TODAY                           │ ← Header sticky
├─────────────────────────────────┤
│ Email 1                         │
│ Email 2                         │
├─────────────────────────────────┤
│ YESTERDAY                       │ ← Header sticky
├─────────────────────────────────┤
│ Email 3                         │
```

- Headers **sticky** durante scroll
- Default abilitato (Show In Groups)
- Text: UPPERCASE, 11-12px, bold, muted color

#### Gmail Multiple Inboxes Pattern
```
┌─────────────────────────────────┐
│ [TODAY]                         │ ← Inline, non-sticky
│ Email 1                         │
│ Email 2                         │
│                                 │
│ [YESTERDAY]                     │
│ Email 3                         │
```

- Headers **inline** (non-sticky)
- Separator line sopra/sotto
- Minimalista

#### iOS Mail Pattern (Sticky Headers)
```swift
// Lista con section headers sticky
List {
    Section(header: Text("Today")) {
        EmailRow()
    }
    Section(header: Text("Yesterday")) {
        EmailRow()
    }
}
```

- Headers **sticky** (Plain Header style)
- Font più piccolo, muted
- Background sfumato per distinguere

### Date Format Patterns

| Client | Format Today | Format Yesterday | Format Week | Format Old |
|--------|-------------|------------------|-------------|------------|
| Superhuman | 10:30 AM | Yesterday | Mon, Jan 8 | Jan 1, 2026 |
| Gmail | 10:30 AM | Yesterday | Mon | 1/1/26 |
| Apple Mail | 10:30 AM | Yesterday | Mon 10:30 AM | Jan 1 |
| Outlook | 10:30 AM | Yesterday | Mon 1/8 | 1/1/2026 |

**Raccomandazione:** Usa formato relativo (Today/Yesterday) + formato assoluto da "Last Week" in poi.

**Fonte:** [Outlook Date Grouping](https://www.lingfordconsulting.com.au/ms-outlook/outlook-emails-show-in-groups-by-date), [iOS List Headers](https://medium.com/@deannaritchie/choosing-the-right-header-style-for-lists-in-ios-63f96c33c079)

---

## 4. STATI VISIVI - Unread, VIP, Important

### Unread Indicators

**Pattern 1: Bold + Dot (Most Common)**
```css
/* Email Item Unread */
.email-item.unread {
  font-weight: 600; /* Bold */
}

.email-item.unread::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #007AFF; /* Blue dot */
  margin-right: 8px;
}
```
Usato da: Apple Mail, iOS Mail, Outlook (blue dot variant)

**Pattern 2: Background Change**
```css
.email-item.unread {
  background-color: rgba(0, 122, 255, 0.05); /* 5% blue tint */
  font-weight: 600;
}
```
Usato da: Gmail (subtle), Superhuman

**Pattern 3: Bold + Border Left**
```css
.email-item.unread {
  border-left: 3px solid #007AFF;
  font-weight: 600;
  padding-left: 13px; /* Compensate border */
}
```
Usato da: Missive, alcuni email clients

**Raccomandazione:** Combina Bold + Dot (massima visibilità)

### VIP / Priority Indicators

**Star Icon** (Gmail pattern)
```css
.star-indicator {
  width: 16px;
  height: 16px;
  color: #fbbc04; /* Yellow star */
  margin-right: 8px;
}
```

**Color-coded Priority** (Outlook/ClearContext)
```
High Priority:   Red exclamation mark
Important:       Yellow flag
VIP Contact:     Color-coded background (light red)
```

**Position:**
- Left side (before sender)
- Right side (after timestamp)

**Raccomandazione:** Star left side + color accent

**Fonte:** [Unread Indicators Patterns](https://www.myshyft.com/blog/unread-message-indicators/), [Email Priority Design](https://www.clearcontext.com/user_guide/contacts.html)

---

## 5. HOVER STATES - Interaction Patterns

### Background Change (Baseline)

```css
.email-item {
  transition: background-color 150ms ease-out;
}

.email-item:hover {
  background-color: rgba(0, 0, 0, 0.03); /* Light mode */
  background-color: rgba(255, 255, 255, 0.05); /* Dark mode */
  cursor: pointer;
}
```

**Timing:** 150-200ms delay prevent accidental hovers

### Quick Actions Reveal

**Pattern Superhuman/Linear:**
```
┌───────────────────────────────────────────────┐
│ Sender Name                  [Archive] [Star] │ ← Icons appear on hover
│ Subject Line                                  │
│ Preview text...                               │
└───────────────────────────────────────────────┘
```

```css
.quick-actions {
  opacity: 0;
  transition: opacity 200ms ease-in-out;
}

.email-item:hover .quick-actions {
  opacity: 1;
}
```

**Actions comuni:**
- Archive
- Star/Favorite
- Mark as read
- Delete
- Snooze

**Position:** Right side, aligned with first line (sender)

### Synchronized Hover (Baymard Research)

Se ci sono più elementi cliccabili nello stesso item:
- Evidenzia TUTTI gli elementi che portano allo stesso path
- Es: Hover su sender → underline anche subject

```css
.email-item:hover .sender,
.email-item:hover .subject {
  text-decoration: underline;
}
```

**Fonte:** [Baymard Hover UX](https://baymard.com/blog/list-items-hover-and-hit-area), [Button States NN/G](https://www.nngroup.com/articles/button-states-communicate-interaction/)

---

## 6. SELECTED STATE - Highlight Pattern

### Pattern Raccomandato (Multi-Indicator)

```css
.email-item.selected {
  /* Border Left Accent */
  border-left: 3px solid #007AFF;
  padding-left: 13px; /* Adjust for border */

  /* Background Change */
  background-color: rgba(0, 122, 255, 0.08);

  /* Optional: Subtle shadow */
  box-shadow: inset 0 0 0 1px rgba(0, 122, 255, 0.2);
}
```

### Alternatives Osservate

**Gmail Pattern:**
```css
.selected {
  background: #c2dbff; /* Light blue */
}
```

**Linear Pattern:**
```css
.selected {
  background: rgba(99, 102, 241, 0.1); /* Indigo tint */
  border-left: 2px solid #6366f1;
}
```

**Apple Mail Pattern:**
```css
.selected {
  background: #0A84FF; /* System blue */
  color: white; /* Inverted text */
}
```

### Best Practices

- **Non usare solo background** (low contrast in some themes)
- **Border left + background** = massima chiarezza
- **Maintain text legibility** (contrast ratio ≥ 4.5:1)
- **Consistent con system design language**

**Fonte:** [Design System States](https://designsystem.emarsys.net/style/style-rules/states), [UI Highlight Patterns](https://www.chameleon.io/blog/new-design-patterns-highlighting-elements)

---

## 7. DARK MODE SPECIFICATIONS

### Superhuman Dark Mode Principles

**Color Palette:**
```
5 Shades of Gray:
- Nearest surface:  #2a2a2a (lighter)
- Main surface:     #1a1a1a
- Far surface:      #0f0f0f (darker)
- Background:       #010101 (avoid pure black #000)

Text:
- Primary:   rgba(255, 255, 255, 0.9)  /* 90% white */
- Secondary: rgba(255, 255, 255, 0.65) /* 65% white */
- Tertiary:  rgba(255, 255, 255, 0.4)  /* 40% white */
```

**Layering Rule:**
> "The closer the layer is to the user (e.g., modals), the lighter the surface area."

**Why Avoid Pure Black:**
- OLED smearing on dark backgrounds
- Breaks depth perception via shadows
- Causes halation with light text

**Contrast Management:**
- Evita contrasti eccessivi (white on pure black)
- Text opacity 90% invece di 100% (riduce halation)
- Accent colors: preserve hue, reduce lightness, increase saturation

### Dark Mode Hover States

```css
.email-item:hover {
  background: rgba(255, 255, 255, 0.05); /* 5% white overlay */
}

.email-item.selected {
  background: rgba(0, 122, 255, 0.15); /* More visible in dark */
  border-left: 3px solid #0A84FF; /* Brighter blue */
}
```

**Fonte:** [Superhuman Dark Theme Design](https://blog.superhuman.com/how-to-design-delightful-dark-themes/)

---

## 8. COMPETITOR ANALYSIS - Interface Patterns

### Superhuman

**Filosofia:** Minimalismo + Velocità
- **Spacing:** Calibrato, no clutter
- **Typography:** Relentlessly refined, font flourishes
- **Dark Mode:** 5 shades of gray, layered depth
- **Keyboard-first:** UI supporta navigazione veloce

**Visual Details:**
- Padding item: ~16px uniform
- No visual noise (minimal borders)
- Bold sender + subject unread
- Clean icons, consistent sizing

**Strengths:** Attenzione ossessiva ai dettagli tipografici

**Fonte:** [Superhuman Review](https://afit.co/superhuman-email-review), [Dark Mode Article](https://blog.superhuman.com/how-to-design-delightful-dark-themes/)

---

### Missive

**Filosofia:** Collaboration + Clean Interface
- **Layout:** 3-panel familiar (inbox | list | preview)
- **Spacing:** Function over form
- **Themes:** Light, dark, mixed
- **Collaboration:** Team features integrate into list UI

**Visual Details:**
- Three-pane layout standard
- Conversation threading visible in list
- Clean, fast filtering
- Quick access to features

**Strengths:** Structure and logic, operational efficiency

**Weaknesses:** Feature richness può overwhelm new users

**Fonte:** [Missive Review](https://efficient.app/apps/missive), [HeroThemes Review](https://herothemes.com/blog/missive-review/)

---

### Apple Mail

**Filosofia:** Native System Integration
- **Spacing:** System standard (Apple HIG)
- **Typography:** San Francisco font
- **Grouping:** Organize by Conversation toggle
- **Date Groups:** Today/Yesterday visible but toggleable

**Visual Details:**
- Column layout customizable
- Conversation grouping issues reported (false positives)
- VIP mailbox separate
- Categories on iPad (Primary, Transactions, etc.)

**Strengths:** Deep system integration, familiar

**Weaknesses:** Conversation grouping sometimes inaccurate

**Fonte:** [Apple Mail Support](https://support.apple.com/guide/mail/use-column-layout-mlhlc18e666f/mac), [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/patterns)

---

### Gmail

**Filosofia:** Conversation-Centric
- **Grouping:** Auto-group replies (max 100 emails/thread)
- **Layout Types:** Default, Important first, Unread first, Priority
- **Unread Indicator:** Blue dot (less obvious per alcuni utenti)
- **Date Grouping:** Via Multiple Inboxes feature

**Visual Details:**
- Conversation breaks on subject change
- Unread handling: flag boolean in mailbox index
- Preview pane marks as read (no toggle)
- Tabs: Primary, Social, Promotions

**Strengths:** Conversation threading maturo

**Weaknesses:** Unread in preview pane, blue dot not intuitive

**Fonte:** [Gmail Conversation View](https://support.google.com/mail/answer/5900), [Gmail Threading](https://groups.google.com/g/gmail-users/)

---

### Linear

**Filosofia:** Structured Minimalism
- **Spacing:** 8pt base scale, 4pt half-step
- **Layout:** Sidebar + tabs + headers + panels
- **List Modes:** List, board, timeline, split, fullscreen
- **Visual Hierarchy:** Reduced noise, increased density

**Visual Details:**
- 8px grid system rigoroso
- List view per sprint planning
- Multiple display modes
- Filters and options in headers

**Strengths:** Structured layouts, visual alignment impeccabile

**Applicabilità Email:** Design patterns trasferibili (list + filters)

**Fonte:** [Linear UI Redesign](https://linear.app/now/how-we-redesigned-the-linear-ui), [Linear Design Trend](https://blog.logrocket.com/ux-design/linear-design/)

---

## 9. RACCOMANDAZIONI PER MIRACOLLOOK

### Spacing System

```scss
// Base Grid
$spacing-base: 8px;
$spacing-half: 4px;

// Email List Item
$item-padding-vertical: 12px;   // (1.5 * base)
$item-padding-horizontal: 16px; // (2 * base)
$item-gap: 0px;                 // Use border separator

// Date Group Headers
$group-header-margin-top: 24px;    // (3 * base)
$group-header-margin-bottom: 8px;  // (1 * base)
$group-header-padding: 8px 16px;

// Internal Element Gaps
$sender-subject-gap: 4px;
$subject-preview-gap: 2px;
```

### Typography Scale

```scss
// Sender Name
$sender-font-size: 15px;
$sender-line-height: 22px; // (1.47x)
$sender-weight-unread: 600;
$sender-weight-read: 400;

// Subject Line
$subject-font-size: 14px;
$subject-line-height: 20px; // (1.43x)
$subject-weight-unread: 600;
$subject-weight-read: 400;

// Preview Text
$preview-font-size: 13px;
$preview-line-height: 18px; // (1.38x)
$preview-weight: 400;
$preview-opacity: 0.65;
```

### Color System (Dark Mode Ready)

```scss
// Light Mode
$bg-primary: #ffffff;
$bg-hover: rgba(0, 0, 0, 0.03);
$bg-selected: rgba(0, 122, 255, 0.08);
$text-primary: #1a1a1a;
$text-secondary: rgba(0, 0, 0, 0.65);
$accent: #007AFF;

// Dark Mode
$bg-primary-dark: #1a1a1a;
$bg-hover-dark: rgba(255, 255, 255, 0.05);
$bg-selected-dark: rgba(0, 122, 255, 0.15);
$text-primary-dark: rgba(255, 255, 255, 0.9);
$text-secondary-dark: rgba(255, 255, 255, 0.65);
$accent-dark: #0A84FF;
```

### Email Item Component Structure

```tsx
<EmailItem className={`${unread ? 'unread' : ''} ${selected ? 'selected' : ''}`}>
  <EmailItemInner>
    {/* Left Side: Indicators */}
    <IndicatorColumn>
      {unread && <UnreadDot />}
      {starred && <StarIcon />}
    </IndicatorColumn>

    {/* Main Content */}
    <ContentColumn>
      <FirstLine>
        <Sender weight={unread ? 600 : 400}>{sender}</Sender>
        <Timestamp>{timestamp}</Timestamp>
      </FirstLine>

      <SubjectLine weight={unread ? 600 : 400}>
        {subject}
      </SubjectLine>

      <PreviewText opacity={0.65}>
        {preview}
      </PreviewText>
    </ContentColumn>

    {/* Right Side: Quick Actions (on hover) */}
    <QuickActions className="on-hover">
      <IconButton icon="archive" />
      <IconButton icon="star" />
      <IconButton icon="trash" />
    </QuickActions>
  </EmailItemInner>
</EmailItem>
```

### Date Grouping Pattern

**Raccomandazione: Sticky Headers (iOS Pattern)**

```tsx
<EmailList>
  <DateGroup sticky>
    <DateHeader>TODAY</DateHeader>
    <EmailItem />
    <EmailItem />
  </DateGroup>

  <DateGroup sticky>
    <DateHeader>YESTERDAY</DateHeader>
    <EmailItem />
  </DateGroup>

  <DateGroup sticky>
    <DateHeader>LAST WEEK</DateHeader>
    <EmailItem />
  </DateGroup>
</EmailList>
```

**Specs DateHeader:**
```scss
.date-header {
  position: sticky;
  top: 0;
  z-index: 10;

  padding: 8px 16px;
  background: $bg-primary;
  backdrop-filter: blur(10px); // iOS-style

  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: $text-secondary;

  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
```

### States - Complete CSS

```scss
.email-item {
  padding: $item-padding-vertical $item-padding-horizontal;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  transition: background-color 150ms ease-out;
  cursor: pointer;

  // Hover State
  &:hover {
    background-color: $bg-hover;

    .quick-actions {
      opacity: 1;
    }
  }

  // Selected State
  &.selected {
    background-color: $bg-selected;
    border-left: 3px solid $accent;
    padding-left: calc($item-padding-horizontal - 3px);
  }

  // Unread State
  &.unread {
    .sender,
    .subject {
      font-weight: 600;
    }
  }

  // Dark Mode
  @media (prefers-color-scheme: dark) {
    background-color: $bg-primary-dark;
    border-color: rgba(255, 255, 255, 0.1);

    &:hover {
      background-color: $bg-hover-dark;
    }

    &.selected {
      background-color: $bg-selected-dark;
      border-left-color: $accent-dark;
    }
  }
}
```

---

## 10. PRIORITÀ IMPLEMENTAZIONE

### Phase 1: Foundation (Must Have)
1. **8px Grid System** - Base spacing scale
2. **Typography Scale** - Sender/Subject/Preview font sizes
3. **Email Item Padding** - 12px vertical, 16px horizontal
4. **Unread Indicator** - Bold + Dot pattern
5. **Hover State** - Background change

### Phase 2: Enhanced UX (Should Have)
1. **Date Grouping** - Today/Yesterday/Last Week headers
2. **Sticky Headers** - Durante scroll
3. **Selected State** - Border + Background
4. **Quick Actions** - Reveal on hover (Archive, Star, Delete)
5. **Dark Mode** - Color palette completo

### Phase 3: Polish (Nice to Have)
1. **VIP Indicators** - Star + color coding
2. **Priority Flags** - High/Low importance
3. **Synchronized Hover** - Multiple clickable areas
4. **Animations** - Micro-interactions (delete, archive)
5. **Customizable Density** - Compact/Normal/Relaxed view

---

## FONTI & REFERENZE

### Design Guidelines
- [Superhuman Dark Mode Design](https://blog.superhuman.com/how-to-design-delightful-dark-themes/)
- [Apple Human Interface Guidelines - Patterns](https://developer.apple.com/design/human-interface-guidelines/patterns)
- [Linear UI Redesign Article](https://linear.app/now/how-we-redesigned-the-linear-ui)

### Spacing & Typography
- [Smashing Magazine - Email Typography](https://www.smashingmagazine.com/2015/08/typographic-patterns-in-html-newsletter-email-design/)
- [UI Spacing Guide - Medium](https://medium.com/dwarves-design/the-principle-of-spacing-part-2-e3cf31b909fa)
- [Design Systems - Spacing](https://www.designsystems.com/space-grids-and-layouts/)
- [Email Typography Best Practices](https://www.emailmavlers.com/blog/email-typography-guide/)

### UX Patterns
- [Baymard Institute - Hover UX](https://baymard.com/blog/list-items-hover-and-hit-area)
- [Nielsen Norman Group - Button States](https://www.nngroup.com/articles/button-states-communicate-interaction/)
- [Unread Message Indicators](https://www.myshyft.com/blog/unread-message-indicators/)

### Email Client Reviews
- [Superhuman Review - Efficient App](https://efficient.app/apps/superhuman)
- [Missive Review - HeroThemes](https://herothemes.com/blog/missive-review/)
- [Gmail Conversation View - Google Support](https://support.google.com/mail/answer/5900)
- [Apple Mail Support](https://support.apple.com/guide/mail/use-column-layout-mlhlc18e666f/mac)

### iOS Design
- [iOS List Headers - Medium](https://medium.com/@deannaritchie/choosing-the-right-header-style-for-lists-in-ios-63f96c33c079)
- [SwiftUI Sticky Headers](https://medium.com/evangelist-apps/create-a-list-in-swiftui-with-sticky-section-headers-373bab2f9e96)

---

## CONCLUSIONI

### Pattern Vincenti

1. **8px Grid + Squish Pattern** = Spacing consistente e professionale
2. **Bold + Dot per Unread** = Massima visibilità senza overwhelm
3. **Sticky Date Headers** = Context sempre visibile
4. **Border Left + Background per Selected** = Chiarezza immediata
5. **Dark Mode con 5 Shades** = Depth perception + low eye strain

### Design Philosophy da Adottare

> "Minimalismo strutturato: ogni pixel ha uno scopo."

- **Superhuman:** Attenzione ossessiva ai dettagli tipografici
- **Linear:** Structured layouts con visual hierarchy chiara
- **Missive:** Functionality senza sacrificare estetica
- **iOS Mail:** Native patterns = familiarity immediata

### Differenziatore Miracollook

**Mentre i competitor fanno A o B, Miracollook fa A+B+C:**
- Spacing Superhuman-level + Date grouping Gmail + Quick actions Linear
- Dark mode scientificamente bilanciato (no pure black)
- Typography hierarchy con line-height ottimizzato per leggibilità
- States multipli combinati (unread + VIP + priority in una vista)

**"I dettagli fanno SEMPRE la differenza."**

---

*Ricerca completata: 13 Gennaio 2026*
*Cervella Researcher - CervellaSwarm*
