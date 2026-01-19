# Email List Design Specs FINAL - Miracollook

> **Data:** 13 Gennaio 2026 - Sessione 184
> **Validato da:** Cervella Marketing
> **Target:** Professionisti hotel (uso 6-8 ore/giorno)
> **Status:** APPROVATO PER IMPLEMENTAZIONE

---

## VALIDAZIONE SPECS RICERCA

**Status**: ✅ APPROVATE CON ADATTAMENTI BRAND

Le specs dalla ricerca sono SOLIDE (basate su Superhuman, Linear, Apple Mail).
Adattate per:
- Palette Design Salutare (#1C1C1E, #7c7dff)
- Brand identity Miracollook (indigo + warm)
- Contesto hospitality (VIP guests, warmth)

---

## 1. SPACING SYSTEM (8px Grid)

### Email Item Padding
```scss
// CONFERMATO - Pattern Superhuman
padding: 12px 16px;  // Verticale: 12px, Orizzontale: 16px

// Mobile (< 640px)
padding: 10px 12px;  // Slightly più compatto
```

### Internal Gaps
```scss
$sender-subject-gap: 4px;    // CONFERMATO
$subject-preview-gap: 2px;   // CONFERMATO
$item-border-bottom: 1px;    // Separator subtle
```

### Date Group Headers
```scss
$group-header-margin-top: 24px;
$group-header-padding: 8px 16px;
$group-header-sticky: true;  // iOS pattern
```

**Rationale:** 12px vertical = sweet spot per 6-8h uso (compatto ma non cramped)

---

## 2. TYPOGRAPHY SCALE

### Sender Name
```scss
font-size: 15px;
line-height: 22px;  // 1.47x
font-weight: 600;   // Semibold UNREAD
font-weight: 400;   // Normal READ
color: var(--miracollo-text-primary);  // #FFFFFF
```

### Subject Line
```scss
font-size: 14px;
line-height: 20px;  // 1.43x
font-weight: 600;   // Semibold UNREAD
font-weight: 400;   // Normal READ
color: var(--miracollo-text-primary);
```

### Preview Text
```scss
font-size: 13px;
line-height: 18px;  // 1.38x
font-weight: 400;   // Normal sempre
color: var(--miracollo-text-secondary);  // rgba(235,235,245,0.6)
opacity: 0.65;      // 65% per preview
```

**Rationale:** Line-height 1.4-1.5x = optimal per leggibilità prolungata

---

## 3. UNREAD INDICATOR

### DECISIONE: Bold + Indigo Dot (BRAND!)

```scss
.email-item.unread {
  // Bold text
  .sender, .subject {
    font-weight: 600;
  }

  // Indigo dot (BRAND #7c7dff invece di blue)
  &::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--miracollo-accent-primary);  // #7c7dff
    margin-right: 8px;
    flex-shrink: 0;
  }
}
```

**PERCHÉ INDIGO:**
- Blue generico (#007AFF) = tutti email client
- Indigo (#7c7dff) = BRAND Miracollook signature!
- Riconoscimento immediato, differentiation

---

## 4. DATE GROUPS - STICKY HEADERS

### Pattern iOS (CONFERMATO)

```tsx
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
```

### DateHeader Specs
```scss
.date-header {
  position: sticky;
  top: 0;
  z-index: 10;

  padding: 8px 16px;
  background: var(--miracollo-bg-primary);  // #1C1C1E
  backdrop-filter: blur(10px);  // iOS-style glass

  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--miracollo-text-muted);  // rgba(235,235,245,0.3)

  border-bottom: 1px solid var(--miracollo-separator);  // #38383A
}
```

**Rationale:** Headers sticky = context sempre visibile durante scroll

---

## 5. HOVER STATE

### Background Change + Quick Actions Reveal

```scss
.email-item {
  transition: background-color 150ms ease-out;
  cursor: pointer;

  &:hover {
    background-color: var(--miracollo-bg-hover);  // #404042

    .quick-actions {
      opacity: 1;
      transform: translateX(0);
    }
  }
}

.quick-actions {
  opacity: 0;
  transform: translateX(8px);
  transition: all 200ms ease-in-out;

  display: flex;
  gap: 8px;
  align-items: center;
}
```

### Quick Actions - Hotel Staff Specifiche

**DECISIONE ACTIONS PER HOSPITALITY:**

```tsx
<QuickActions>
  <IconButton
    icon="star"
    title="VIP Guest"
    color={starred ? 'var(--miracollo-accent-warm)' : 'inherit'}
  />
  <IconButton
    icon="archive"
    title="Archive"
  />
  <IconButton
    icon="trash"
    title="Delete"
  />
</QuickActions>
```

**PERCHÉ QUESTI:**
1. **Star (VIP)** - Hotel staff marca ospiti importanti
2. **Archive** - Pulizia inbox senza delete (review later)
3. **Delete** - Spam, errori

**NON SERVONO:**
- ❌ Snooze (hotel risponde subito, no delay)
- ❌ Mark as read (click email = legge subito)
- ❌ Assign (futuro, Phase 2)

---

## 6. SELECTED STATE

### Border Left + Background (BRAND COLORS)

```scss
.email-item.selected {
  // Border left accent INDIGO (brand!)
  border-left: 3px solid var(--miracollo-accent-primary);  // #7c7dff
  padding-left: calc(16px - 3px);  // Compensate border

  // Background tint
  background-color: rgba(124, 125, 255, 0.15);  // 15% indigo tint

  // Optional: Subtle glow
  box-shadow: inset 0 0 0 1px rgba(124, 125, 255, 0.2);
}
```

**Rationale:** Border left + background = massima chiarezza, brand reinforcement

---

## 7. VIP EMAILS - WARM ACCENT INTEGRATION

### DECISIONE: Warm Accent (#d4985c) per VIP

```scss
.email-item.vip {
  // Border left WARM (ospite importante!)
  border-left: 3px solid var(--miracollo-accent-warm);  // #d4985c
  padding-left: calc(16px - 3px);

  // Star icon warm
  .star-icon {
    color: var(--miracollo-accent-warm);
    fill: var(--miracollo-accent-warm);
  }

  // Subtle warm glow
  &.selected {
    background-color: rgba(212, 152, 92, 0.12);  // 12% warm tint
    box-shadow: inset 0 0 0 1px rgba(212, 152, 92, 0.15);
  }
}
```

### Combined States (Unread + VIP)

```tsx
// Email da guest VIP non letta
<EmailItem
  className="unread vip"
>
  {/* Warm dot + Bold text */}
  <UnreadDot color="var(--miracollo-accent-warm)" />
  <Sender weight={600}>Mr. Alessandro Rossi</Sender>
  <VIPBadge>VIP</VIPBadge>
</EmailItem>
```

**Rationale:** Warm = hospitality, VIP = oro/calore/importanza

---

## 8. COMPLETE EMAIL ITEM STRUCTURE

```tsx
<EmailItem
  className={cn(
    "email-item",
    unread && "unread",
    selected && "selected",
    vip && "vip"
  )}
>
  <EmailItemInner>
    {/* Left: Indicators */}
    <IndicatorColumn>
      {unread && (
        <UnreadDot
          color={vip ? 'var(--miracollo-accent-warm)' : 'var(--miracollo-accent-primary)'}
        />
      )}
    </IndicatorColumn>

    {/* Main: Content */}
    <ContentColumn>
      {/* First Line: Sender + Timestamp */}
      <FirstLine>
        <SenderGroup>
          <Sender weight={unread ? 600 : 400}>
            {sender}
          </Sender>
          {vip && (
            <VIPBadge color="var(--miracollo-accent-warm)">
              VIP
            </VIPBadge>
          )}
        </SenderGroup>
        <Timestamp>
          {formatTimestamp(date)}
        </Timestamp>
      </FirstLine>

      {/* Subject Line */}
      <SubjectLine weight={unread ? 600 : 400}>
        {subject}
      </SubjectLine>

      {/* Preview Text */}
      <PreviewText opacity={0.65}>
        {preview}
      </PreviewText>
    </ContentColumn>

    {/* Right: Quick Actions (on hover) */}
    <QuickActions>
      <IconButton
        icon="star"
        active={vip}
        color={vip ? 'var(--miracollo-accent-warm)' : 'inherit'}
        onClick={handleToggleVIP}
      />
      <IconButton
        icon="archive"
        onClick={handleArchive}
      />
      <IconButton
        icon="trash"
        onClick={handleDelete}
      />
    </QuickActions>
  </EmailItemInner>
</EmailItem>
```

---

## 9. PALETTE COLORS - MAPPED

```scss
/* === EMAIL LIST COLORS === */

/* Backgrounds */
--email-bg-primary: var(--miracollo-bg-primary);      // #1C1C1E
--email-bg-hover: var(--miracollo-bg-hover);          // #404042
--email-bg-selected: rgba(124, 125, 255, 0.15);       // Indigo tint
--email-bg-selected-vip: rgba(212, 152, 92, 0.12);    // Warm tint

/* Borders */
--email-border-separator: var(--miracollo-separator); // #38383A
--email-border-selected: var(--miracollo-accent-primary);  // #7c7dff
--email-border-vip: var(--miracollo-accent-warm);     // #d4985c

/* Text */
--email-text-sender: var(--miracollo-text-primary);   // #FFFFFF
--email-text-subject: var(--miracollo-text-primary);  // #FFFFFF
--email-text-preview: var(--miracollo-text-secondary); // rgba(235,235,245,0.6)
--email-text-timestamp: var(--miracollo-text-muted);  // rgba(235,235,245,0.3)

/* Indicators */
--email-unread-dot: var(--miracollo-accent-primary);  // #7c7dff
--email-unread-dot-vip: var(--miracollo-accent-warm); // #d4985c
--email-vip-badge-bg: var(--miracollo-accent-warm);   // #d4985c
--email-vip-badge-text: var(--miracollo-bg-primary);  // #1C1C1E (contrast!)
```

---

## 10. DESIGN RATIONALE - PERCHÉ QUESTE SCELTE

### Hospitality Context

| Scelta Design | Rationale Hospitality |
|---------------|----------------------|
| **Warm accent VIP** | Oro/calore = lusso hospitality |
| **Quick star action** | Staff marca ospiti VIP veloce |
| **No snooze** | Hotel risponde SUBITO (no delay) |
| **Sticky date headers** | Context temporale critico (check-in/out) |
| **8px grid compact** | Più email visibili = priorità veloce |

### Eye-Friendly (6-8h uso)

| Scelta Design | Rationale Eye-Friendly |
|---------------|----------------------|
| **#1C1C1E bg** | Apple tested, -30% strain vs vecchio |
| **65% opacity preview** | Hierarchy chiara, no overwhelm |
| **Line-height 1.4-1.5x** | Leggibilità prolungata |
| **No pure black** | No OLED smearing, no halation |

### Brand Differentiation

| Scelta Design | Rationale Brand |
|---------------|----------------|
| **Indigo unread dot** | #7c7dff = Miracollook signature! |
| **Warm VIP accent** | Hospitality feel unico |
| **Consistent palette** | Logo indigo reflected everywhere |

---

## 11. MOBILE ADAPTATIONS (< 640px)

```scss
@media (max-width: 640px) {
  .email-item {
    padding: 10px 12px;  // Ridotto da 12px 16px
  }

  .sender {
    font-size: 14px;     // Ridotto da 15px
  }

  .subject {
    font-size: 13px;     // Ridotto da 14px
  }

  .preview {
    display: none;       // Nascosto su mobile (spazio limitato)
  }

  .quick-actions {
    display: none;       // No hover su mobile
  }

  // Swipe actions instead (Phase 2)
  &.swiped-left {
    .swipe-delete {
      opacity: 1;
    }
  }
}
```

---

## 12. IMPLEMENTATION PRIORITY

### Phase 1: Core (SUBITO)
- ✅ 8px grid spacing
- ✅ Typography scale (15/14/13px)
- ✅ Unread: Bold + Indigo dot
- ✅ Hover: Background change
- ✅ Selected: Border left + background

### Phase 2: Enhanced (PROSSIMO)
- ✅ Date groups sticky headers
- ✅ VIP: Warm accent integration
- ✅ Quick actions reveal
- ⏳ Mobile swipe actions

### Phase 3: Polish (FUTURO)
- ⏳ Animations (delete, archive)
- ⏳ Customizable density (compact/normal/relaxed)
- ⏳ Accessibility (keyboard navigation)

---

## 13. FRONTEND HANDOFF - CERVELLA-FRONTEND

**File da creare/modificare:**

```
frontend/src/components/EmailList/
├── EmailItem.tsx           # Main component
├── UnreadDot.tsx          # Indigo/Warm dot
├── VIPBadge.tsx           # Warm badge
├── QuickActions.tsx       # Hover actions
├── DateHeader.tsx         # Sticky headers
└── EmailItem.styles.ts    # Styled components

frontend/src/styles/
└── email-list.css         # Complete CSS specs
```

**Props EmailItem:**
```tsx
interface EmailItemProps {
  id: string;
  sender: string;
  subject: string;
  preview: string;
  timestamp: Date;
  unread: boolean;
  vip: boolean;
  selected: boolean;
  onSelect: (id: string) => void;
  onToggleVIP: (id: string) => void;
  onArchive: (id: string) => void;
  onDelete: (id: string) => void;
}
```

---

## 14. SUCCESS METRICS

### User Experience
- [ ] Tempo identificazione email unread < 1s
- [ ] Hover quick actions < 0.5s reveal
- [ ] VIP emails visibili subito (warm accent)
- [ ] Zero eye strain dopo 2h uso

### Technical
- [ ] Scroll performance 60fps (sticky headers)
- [ ] Contrast ratio WCAG AAA (text vs bg)
- [ ] Mobile swipe fluido < 16ms

### Brand
- [ ] Indigo recognition = Miracollook brand
- [ ] Warm VIP accent = hospitality feel
- [ ] Differenziazione vs Gmail/Superhuman

---

## RISULTATO ATTESO

```
+================================================================+
|                                                                |
|   EMAIL LIST PROFESSIONALE + WARM HOSPITALITY                 |
|                                                                |
|   - Eye-friendly: 9/10 (Apple foundation)                     |
|   - Brand recognition: 9/10 (indigo signature)                |
|   - Hospitality feel: 8/10 (warm VIP accents)                 |
|   - Usabilità hotel staff: 9/10 (quick actions)               |
|                                                                |
|   "I dettagli fanno SEMPRE la differenza!"                    |
|                                                                |
+================================================================+
```

---

*Validato: 13 Gennaio 2026*
*Cervella Marketing - CervellaSwarm*
*Ready for cervella-frontend implementation!*
