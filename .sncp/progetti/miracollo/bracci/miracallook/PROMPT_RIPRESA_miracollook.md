# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 242
> **STATO:** Allotment funziona! Pronto per Design Salutare

---

## COS'E MIRACOLLOOK

Email client per hotel che CONOSCE i tuoi ospiti.
Porta :8002 dentro ecosistema Miracollo.

---

## SESSIONE 242 - COSA ABBIAMO FATTO

```
+================================================================+
|   MIGRAZIONE COMPLETATA: react-resizable-panels -> Allotment   |
|                                                                |
|   PROBLEMA: react-resizable-panels v4.4.1 bloccava i pannelli  |
|   SOLUZIONE: Allotment (libreria Microsoft, usata da VS Code)  |
|                                                                |
|   RISULTATO: Pannelli funzionano! Build OK!                    |
+================================================================+
```

### File Modificati
- `package.json` - Allotment invece di react-resizable-panels
- `ThreePanelResizable.tsx` - Riscritto con API Allotment
- `index.css` - CSS per handle resize (viola accent)
- `App.tsx` - Import aggiornato

### Commit
`68189a1` - Miracollook: Migrazione a Allotment per resizable panels

---

## PROSSIMA SESSIONE - Design Salutare

```
OBIETTIVO: Applicare palette Apple eye-friendly

COSA FARE:
1. Leggere PALETTE_DESIGN_SALUTARE_VALIDATA.md
2. Applicare colori passo passo
3. Verificare che pannelli NON si bloccano dopo ogni modifica
4. Se si blocca -> identificare quale CSS causa il problema

ATTENZIONE:
- In passato il design salutare bloccava i pannelli
- Ora con Allotment potrebbe funzionare
- Fare un cambio alla volta e testare!
```

---

## PALETTE DA APPLICARE

```css
/* Backgrounds */
--miracollo-bg: #1C1C1E;
--miracollo-bg-secondary: #2C2C2E;

/* Text */
--miracollo-text: #FFFFFF;
--miracollo-text-secondary: rgba(235, 235, 245, 0.6);

/* Accent */
--miracollo-accent: #7c7dff;
--miracollo-accent-warm: #d4985c;

/* Border */
--miracollo-border: #38383A;
```

---

## FILE CHIAVE

| File | Path | Stato |
|------|------|-------|
| ThreePanelResizable | `frontend/src/components/Layout/` | Allotment OK |
| Palette Design | `.sncp/.../PALETTE_DESIGN_SALUTARE_VALIDATA.md` | Da applicare |
| Studio Ricerca | `.sncp/.../studi/RICERCA_DESIGN_SALUTARE.md` | Completo |
| Tailwind Config | `frontend/tailwind.config.js` | Colori definiti |

---

## COMANDI

```bash
# Backend
cd ~/Developer/miracollogeminifocus/miracallook/backend
uvicorn main:app --port 8002 --reload

# Frontend
cd ~/Developer/miracollogeminifocus/miracallook/frontend
npm run dev
```

---

## STATO FASE 1 (80%)

```
FATTO:
[x] OAuth, Inbox, Send, Reply, Forward, Archive, Trash
[x] Search, AI Summary, Keyboard Shortcuts, Command Palette
[x] Mark Read/Unread, Drafts Auto-Save
[x] Upload Attachments, Thread View
[x] Resizable Panels (Allotment) <- SESSIONE 242!

DA FARE:
[ ] 1.6 Context Menu (5h)
[ ] 1.7 Bulk Actions (7-10gg)
[ ] 1.8 Labels Custom (2-3gg)
[ ] Design Salutare <- PROSSIMO!
```

---

*"Non e un email client. E l'Outlook che CONOSCE il tuo hotel."*
