# Marketing Validation - Email List Design

> **Output cervella-marketing**
> **Data:** 13 Gennaio 2026
> **Target:** Professionisti hotel (6-8h uso/giorno)

---

## VALIDAZIONE SPECS

**Status**: ✅ APPROVATE CON ADATTAMENTI BRAND

Specs dalla ricerca sono SOLIDE (Superhuman, Linear, Apple Mail).
Adattate per Miracollook brand + hospitality context.

---

## DECISIONI CHIAVE

### 1. Unread Indicator
**DECISIONE:** Bold + Indigo Dot (#7c7dff)
- ❌ Blue generico (#007AFF) = tutti email client
- ✅ Indigo (#7c7dff) = BRAND Miracollook!
- Differenziazione immediata

### 2. VIP Emails
**DECISIONE:** Warm Accent (#d4985c) per VIP
- Border left warm oro
- Star icon warm
- Warm glow on selected
- **Rationale:** Oro/calore = hospitality luxury

### 3. Quick Actions Hotel Staff
**DECISIONE:** Star (VIP) + Archive + Delete
- Star = marca ospiti importanti
- Archive = pulizia inbox (review later)
- Delete = spam, errori
- ❌ NO Snooze (hotel risponde SUBITO)
- ❌ NO Mark as Read (click = legge)

### 4. Date Groups
**DECISIONE:** Sticky Headers (iOS pattern)
- Today/Yesterday/Last Week
- Context temporale critico (check-in/out)
- Visibile durante scroll

---

## PALETTE INTEGRATION

```css
/* Unread Normal */
--unread-dot: #7c7dff (indigo brand)

/* Unread VIP */
--unread-dot-vip: #d4985c (warm hospitality)

/* Selected Normal */
--border-selected: #7c7dff
--bg-selected: rgba(124,125,255,0.15)

/* Selected VIP */
--border-vip: #d4985c
--bg-selected-vip: rgba(212,152,92,0.12)
```

---

## SPECS VALIDATE

| Elemento | Valore | Status |
|----------|--------|--------|
| Padding item | 12px vertical, 16px horizontal | ✅ |
| Gap sender-subject | 4px | ✅ |
| Gap subject-preview | 2px | ✅ |
| Sender size | 15px semibold unread | ✅ |
| Subject size | 14px semibold unread | ✅ |
| Preview size | 13px 65% opacity | ✅ |
| Hover bg | rgba(255,255,255,0.05) | ✅ |
| Date headers | 11px uppercase sticky | ✅ |

---

## DESIGN RATIONALE

### Hospitality Context
- Warm VIP accent = oro/lusso hospitality
- Quick star action = staff marca ospiti veloce
- No snooze = hotel risponde SUBITO
- Sticky dates = context check-in/out

### Eye-Friendly (6-8h uso)
- #1C1C1E bg = Apple tested, -30% strain
- 65% opacity preview = hierarchy chiara
- Line-height 1.4-1.5x = leggibilità prolungata

### Brand Differentiation
- Indigo unread dot = Miracollook signature
- Warm VIP accent = hospitality feel unico
- Consistent palette = brand reinforcement

---

## NEXT: CERVELLA-FRONTEND

**File specs completo:**
`.sncp/progetti/miracollo/moduli/miracallook/EMAIL_LIST_SPECS_FINAL.md`

**Implementare:**
1. EmailItem.tsx component
2. UnreadDot.tsx (indigo/warm)
3. VIPBadge.tsx (warm badge)
4. QuickActions.tsx (hover reveal)
5. DateHeader.tsx (sticky)

**Props EmailItem:**
```tsx
{
  sender, subject, preview, timestamp,
  unread, vip, selected,
  onSelect, onToggleVIP, onArchive, onDelete
}
```

---

## RISULTATO ATTESO

- Eye-friendly: 9/10
- Brand recognition: 9/10
- Hospitality feel: 8/10
- Usabilità hotel staff: 9/10

**"I dettagli fanno SEMPRE la differenza!"**

---

*cervella-marketing - 13 Gennaio 2026*
