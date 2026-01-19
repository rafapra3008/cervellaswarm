# MAPPA VERITA - MIRACOLLOOK

> **QUESTO FILE RIFLETTE IL CODICE REALE**
> **Aggiornato: 19 Gennaio 2026 - Sessione 268**
> **"SU CARTA" != "REALE" - Questo file e REALE**

---

## STATO REALE - DAL CODICE

```
+================================================================+
|                                                                |
|   CODICE: 100% | ROBUSTEZZA: 6.5/10 → 9.5                      |
|                                                                |
|   Frontend: 8.5/10 | ~4,800 righe | 41 file (+LabelPicker)    |
|   Backend:  8.5/10 | ~3,100 righe | 34 endpoint               |
|                                                                |
+================================================================+
```

---

## FEATURE - VERIFICA DAL CODICE

### IMPLEMENTATE (dal codice)

| Feature | Frontend | Backend | File Chiave |
|---------|----------|---------|-------------|
| **Resizable Panels** | ThreePanelResizable.tsx (131L) | - | Allotment v1.20.5 |
| **Context Menu** | EmailContextMenu.tsx (280L) | - | Portal + keyboard nav |
| **Thread View** | ThreadView.tsx (299L) | GET /thread/{id} | Collapsible messages |
| **Mark Read/Unread** | useEmailHandlers.ts | POST /mark-read, /mark-unread | actions.py L150, L194 |
| **Drafts** | useDraft.ts (212L) | 6 endpoint CRUD | drafts.py (305L) |
| **Upload Attachments** | AttachmentPicker.tsx (176L) | POST /send-with-attachments | 25MB limit |
| **Search** | SearchBar | GET /search | search.py (89L) |
| **AI Summary** | - | GET /ai/* | ai.py (198L) + Claude |
| **Keyboard Shortcuts** | useKeyboardShortcuts.ts | - | j/k/e/r/c/f/s |
| **Command Palette** | CommandPalette | - | CMDK v1.1.1 |
| **Design Salutare** | CSS con colori corretti | - | #778DA9, #E0DED0, #EBEBF5 |

### IMPLEMENTATE (Sessione 267-268)

| Feature | Frontend | Backend | Note |
|---------|----------|---------|------|
| **Bulk Actions** | useBulkActions.ts | POST /batch-modify | Gmail batchModify nativo! |
| **Labels CRUD** | api.ts (6 metodi) | labels.py (6 endpoint) | CRUD completo + assign! |
| **Add Label UI** | LabelPicker.tsx + BulkActionsBar | +add_label/remove_label | Sessione 268! |

### DA IMPLEMENTARE (Robustezza - SUBROADMAP)

| Fase | Feature | Effort | Score |
|------|---------|--------|-------|
| 0 | Dependency audit + Split api.py | 2h | prep |
| 1 | Token encryption + Gitignore | 3-4h | 7.5/10 |
| 2 | Auto-start + Backup + Health | 1-2h | 8.0/10 |
| 3 | Rate limiting + Retry | 2-3h | 8.5/10 |
| 4 | Testing pytest 80% | 4-5 giorni | 9.0/10 |
| 5-6 | Monitoring + Frontend env | 8-10h | 9.5/10 |

**SUBROADMAP:** `docs/roadmap/SUBROADMAP_MIRACOLLOOK_ROBUSTEZZA.md`

### DA IMPLEMENTARE (Post-Robustezza)

| Feature | Effort Stimato | Note |
|---------|----------------|------|
| Contacts Autocomplete | 6h full | Google People API |
| Settings Page | 8h full | Preferenze utente |

---

## ARCHITETTURA REALE

### Frontend (React 19 + Vite 7)

```
miracallook/frontend/src/
├── components/           # 15 componenti
│   ├── EmailList/       (EmailList, EmailListItem, BundleItem)
│   ├── EmailDetail/     (EmailDetail)
│   ├── Thread/          (ThreadView)
│   ├── Compose/         (ComposeModal, AttachmentPicker)
│   ├── BulkActions/     (BulkActionsBar)
│   ├── EmailContextMenu/(EmailContextMenu)
│   ├── Layout/          (ThreePanelResizable)
│   └── ...
├── hooks/               # 9 custom hooks
│   ├── useEmails.ts
│   ├── useDraft.ts (212L)
│   ├── useBulkActions.ts
│   └── ...
├── services/api.ts      # Axios client
└── types/               # TypeScript types
```

**Dipendenze chiave:**
- React 19.2.0
- Vite 7.2.4
- TypeScript 5.9.3
- Tailwind 4.1.18
- Allotment 1.20.5 (resizable)
- CMDK 1.1.1 (command palette)
- React Hotkeys Hook 5.2.1

### Backend (FastAPI + SQLite)

```
miracallook/backend/
├── gmail/               # 9 moduli (refactored 16 Gen!)
│   ├── api.py (81L)     # Router aggregator
│   ├── inbox.py (106L)  # List inbox
│   ├── message.py (225L)# Get message/thread
│   ├── actions.py (235L)# Archive, trash, read
│   ├── compose.py (412L)# Send, attachments
│   ├── drafts.py (305L) # CRUD drafts
│   ├── search.py (89L)  # Search
│   └── ai.py (198L)     # Claude AI
├── auth/google.py       # OAuth
├── db/                  # SQLite + SQLAlchemy
└── main.py (98L)        # FastAPI app
```

**27 endpoint attivi:**
- Inbox/Listing: 5
- Message/Thread: 4
- Actions: 5
- Compose: 4
- Drafts: 6
- Search: 1
- AI: 2

---

## METRICHE REALI

| Metrica | Frontend | Backend |
|---------|----------|---------|
| Righe totali | ~4,600 | ~2,600 |
| File | 40 | ~15 |
| File > 300 righe | 2 | 1 |
| Health Score | 8.5/10 | 8/10 |

### File da tenere d'occhio

| File | Righe | Azione |
|------|-------|--------|
| ComposeModal.tsx | 432 | Split consigliato |
| App.tsx | 319 | OK ma context API migliorerebbe |
| compose.py | 412 | OK sotto soglia |

---

## PROSSIMI STEP REALI

```
PRIORITA 1 - ROBUSTEZZA (da SUBROADMAP):
[ ] FASE 0.1: Dependency audit (pip-audit)
[ ] FASE 0.2: Split api.py (1391 righe!)
[ ] FASE 1.1: Token encryption
[ ] FASE 1.2: Gitignore root

PRIORITA 2 - Continuare SUBROADMAP:
[ ] FASE 2: Auto-start + Backup + Health
[ ] FASE 3: Rate limiting + Retry
[ ] FASE 4: Testing 80%+

PRIORITA 3 - Post-Robustezza:
[ ] PMS Integration (Guest Identification)
[ ] Contacts Autocomplete
[ ] Settings Page
```

**CODICE FEATURE COMPLETE!** Ora focus su ROBUSTEZZA.

---

## CONFRONTO DOCS vs CODICE

| Documento | Diceva | Codice dice | Azione |
|-----------|--------|-------------|--------|
| NORD | FASE 1 = 80% | 92% | AGGIORNARE |
| PROMPT_RIPRESA | FASE 1 = 85% | 92% | AGGIORNARE |
| ROADMAP_MASTER | FASE 1 = 75% | 92% | AGGIORNARE |
| NORD | Context Menu DA FARE | FATTO | AGGIORNARE |
| NORD | Resizable DA FARE | FATTO | AGGIORNARE |

---

## COMANDI

```bash
# Backend
cd ~/Developer/miracollogeminifocus/miracallook/backend
source venv/bin/activate
uvicorn main:app --port 8002 --reload

# Frontend
cd ~/Developer/miracollogeminifocus/miracallook/frontend
npm run dev
```

---

*"La VERITA dal codice. Non dai documenti."*
*Generato: 19 Gennaio 2026*
