# Roadmap Design Salutare - Miracollook

> **Data:** 13 Gennaio 2026 - Sessione 184
> **Obiettivo:** Implementare palette eye-friendly
> **Effort stimato:** ~4 ore

---

## STEP 1: Audit CSS Attuale (30 min)

```
[ ] Leggere tailwind.config.js - colori attuali
[ ] Leggere index.css - eventuali hardcoded
[ ] Identificare componenti da aggiornare
[ ] Screenshot BEFORE
```

**Output:** Lista colori da cambiare

---

## STEP 2: Aggiornare Tailwind Config (1 ora)

```
[ ] Sostituire palette in tailwind.config.js
[ ] Mantenere nomi classi esistenti (no breaking changes)
[ ] Aggiungere nuovi colori (warm, hover states)
```

**Mapping:**
| Vecchio | Nuovo |
|---------|-------|
| miracollo-bg (#0a0e1a) | #1C1C1E |
| miracollo-bg-card (#1e2642) | #2C2C2E |
| miracollo-accent (#6366f1) | #7c7dff |
| miracollo-text-muted (#8b9cb5) | rgba(235,235,245,0.3) |
| miracollo-border (#475569) | #38383A |

---

## STEP 3: Applicare ai Componenti (1.5 ore)

**Priorita:**
1. Layout.tsx - background principale
2. Sidebar.tsx - navigation
3. EmailList.tsx - lista email
4. EmailDetail.tsx - dettaglio

```
[ ] Layout - bg-primary
[ ] Sidebar - accent, hover states
[ ] EmailList - cards, separators
[ ] EmailDetail - text hierarchy
```

---

## STEP 4: Test e Validazione (1 ora)

```
[ ] Avviare Docker (cd ~/Developer/miracollook && docker compose up)
[ ] Screenshot AFTER
[ ] Confronto BEFORE/AFTER
[ ] Check contrasti WCAG AAA
[ ] Validazione Guardiana Qualita
```

---

## CHECKPOINT

- [ ] Palette implementata
- [ ] Nessun breaking change
- [ ] Screenshot documentati
- [ ] SNCP aggiornato

---

*"I dettagli fanno SEMPRE la differenza!"*
