# RICERCA: Gmail Labels API - Studio MACRO

**Data**: 2026-01-15
**Worker**: cervella-researcher
**Progetto**: Miracollo > Miracollook
**Tipo**: Studio MACRO (visione generale)

---

## STATUS: ✅ COMPLETATO

**TL;DR:** Gmail Labels API supporta CRUD completo, colori predefiniti (~80), nesting via naming convention, sync bidirezionale con Gmail web. Limite 10.000 labels (raccomandato 500). Frontend Miracollook 80% fatto. Effort: 2-3 giorni per integrazione completa.

---

## OPZIONE MIGLIORE

**Approccio raccomandato:**
1. **V1 (2 giorni):** Flat list labels + color picker palette Google + manual refresh
2. **V2 (opzionale):** Tree view nested + auto-refresh polling 5min
3. **V3 (futuro):** Gmail Push Notifications real-time

**Rationale:** Start semplice, itera in base a feedback utenti reali.

---

## KEY FINDINGS

### API Capabilities
- ✅ CRUD completo (create, read, update, delete)
- ✅ Colori: SI (~80 predefiniti, no custom HEX)
- ✅ Nesting: SI (via `Parent/Child/Grandchild` naming)
- ✅ Sync Gmail web: Bidirezionale automatico
- ✅ System vs User labels: Gestiti correttamente

### Limiti
- Max 10.000 labels (tecnico)
- Raccomandato 500 (performance)
- Rate limit: 250 units/sec per-user
- Solo colori palette Google

### UX Patterns (da Big Players)
- Gmail: Multi-label, drag & drop, color badges
- Outlook: Folder-based + categories (approccio diverso)
- Mobile: Modal/bottom sheet (no drag & drop)

### Frontend Status
```
✅ types/label.ts
✅ hooks/useLabels.ts
✅ components/Labels/LabelPicker.tsx
✅ services/api.ts (6 metodi)
❌ Integrazione in EmailList
❌ Label badges inline
❌ Sidebar filtro
```

---

## EFFORT BREAKDOWN

| Fase | Effort | Priorità |
|------|--------|----------|
| **Fase 1: Base** | 1 giorno | MUST |
| - Integrare LabelPicker | 2h | |
| - Label badges inline | 2h | |
| - Backend proxy | 3h | |
| - Testing | 1h | |
| **Fase 2: Polish** | 1 giorno | SHOULD |
| - Sidebar filtro | 3h | |
| - Palette colori UI | 2h | |
| - Keyboard shortcuts | 2h | |
| - Mobile optimization | 1h | |
| **Fase 3: Advanced** | 1 giorno | NICE |
| - Nested tree view | 4h | |
| - Drag & drop | 3h | |
| - Bulk operations | 1h | |

**TOTALE MINIMO:** 2 giorni (Fase 1 + 2)
**TOTALE COMPLETO:** 3 giorni (tutte fasi)

---

## DECISIONI DA PRENDERE

1. **Nested labels UI:** Flat list (V1) o Tree view (V2)?
2. **Color picker:** Pre-select (V1) o full picker limitato (V2)?
3. **Real-time sync:** Manual (V1), Polling (V2), Push (V3)?
4. **Mobile UX:** Modal (standard) o Swipe gesture (innovativo)?

**Raccomandazione:** Tutte Opzione 1 per V1, iterare in V2 basato su feedback.

---

## NEXT STEPS

1. ✅ Studio MACRO completato
2. ⏭️ Consultare **cervella-marketing** per validare UX design
3. ⏭️ Frontend worker: integrare LabelPicker in EmailList
4. ⏭️ Backend worker: proxy endpoints Labels API
5. ⏭️ Testing: Guardiana Qualità verifica

---

## FILE CREATI

**Studio completo:** `.sncp/progetti/miracollo/moduli/miracollook/studi/STUDIO_MACRO_LABELS_API.md` (150 righe)

**Contenuto:**
- API Capabilities dettagliate
- Limiti & Performance
- Pattern UX (Gmail, Outlook)
- Considerazioni tecniche
- Effort stimato
- Decisioni da prendere
- 10+ fonti citate

---

## FONTI

**Gmail API:**
- [Manage Labels Guide](https://developers.google.com/workspace/gmail/api/guides/labels)
- [REST Resource: users.labels](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.labels)
- [Usage Limits](https://developers.google.com/workspace/gmail/api/reference/quota)

**UX Research:**
- [Gmail Drag & Drop Labels](https://cloud.googleblog.com/2009/07/drag-and-drop-and-organize-your-labels.html)
- [Outlook vs Gmail](https://office-watch.com/2021/how-gmail-labels-and-categories-work-with-outlook/)
- [PatternFly Label Guidelines](https://www.patternfly.org/components/label/design-guidelines/)

**Limiti:**
- [Gmail Limits & Quotas](https://hiverhq.com/blog/gmail-and-google-apps-limits-every-admin-should-know)

---

## COSTITUZIONE APPLIED

**Principio:** "Studiare prima di agire - i big players hanno già risolto questi problemi!"

**Come applicato:**
1. Studiato docs ufficiali Gmail API
2. Analizzato UX di Gmail web e Outlook
3. Ricercato best practices (PatternFly, design systems)
4. Valutato limiti tecnici (10.000 labels, rate limits)
5. Proposto approccio incrementale (V1 → V2 → V3)

**Risultato:** Raccomandazione basata su ricerca solida, non invenzione. Pronta per implementazione.

---

*"Nulla è complesso - solo non ancora studiato!"*
*Cervella Researcher - 15 Gennaio 2026*
