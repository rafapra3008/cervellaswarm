# RICERCA DRAFTS - Miracollook Email Client

**Data:** 14 Gennaio 2026
**Ricercatrice:** Cervella-Researcher
**Obiettivo:** Implementare auto-save drafts per ComposeModal

---

## TL;DR - Executive Summary

**COSA SERVE:**
1. Backend: 3 endpoint Gmail API (create/update/list drafts)
2. Frontend: Hook autosave con debounce 1.5-2s
3. UX: Indicatore "Saving.../Saved at HH:MM"
4. Recovery: LocalStorage fallback + lista drafts

**TIMING:** ~3-4h implementazione | Alta priorità UX

---

## 1. GMAIL API DRAFTS - Endpoint e Formato

### Endpoint Disponibili

| Operazione | Endpoint | Metodo | Cosa fa |
|------------|----------|--------|---------|
| **Create** | `users.drafts.create` | POST | Crea draft con label DRAFT |
| **Update** | `users.drafts.update` | PUT | Sostituisce contenuto draft (distrugge vecchio) |
| **List** | `users.drafts.list` | GET | Lista tutti i drafts |
| **Get** | `users.drafts.get` | GET | Recupera draft specifico |
| **Send** | `users.drafts.send` | POST | Invia e elimina automaticamente |
| **Delete** | `users.drafts.delete` | DELETE | Elimina draft permanentemente |

### Struttura Draft Gmail

```json
{
  "id": "18d1234567890abc",
  "message": {
    "raw": "base64url_encoded_mime_message",
    "threadId": "18d1234567890abc"
  }
}
```

**NOTA IMPORTANTE:**
- Draft DEVE avere solo label `DRAFT` (nessun'altra)
- Il messaggio è in formato MIME base64url encoded
- Update DISTRUGGE il draft precedente (non è un patch)
- Invio automaticamente elimina draft e crea nuovo messaggio con label SENT

**FONTE:** [Gmail API Drafts Guide](https://developers.google.com/workspace/gmail/api/guides/drafts)

---

## 2. BEST PRACTICES UX - Auto-Save Drafts

### Quando Salvare?

| Trigger | Quando | Raccomandazione |
|---------|--------|-----------------|
| **Keystroke** | Ogni battitura | ❌ NO - troppo frequente |
| **Timer fisso** | Es. ogni 20s | ⚠️ Possibile - rischio perdita dati |
| **Debounce** | User smette di scrivere | ✅ **CONSIGLIATO** |
| **Focus lost** | User esce dal campo | ✅ Backup aggiuntivo |
| **Window beforeunload** | Browser chiude | ✅ Salvataggio emergenza |

**PATTERN VINCENTE:**
- **Debounce 1.5-2s** dopo ultima battitura
- **Salva su blur** dei campi principali
- **Salva su beforeunload** come fallback

### Timing Debounce Consigliato

```
TROVATO:
- Gmail autosave: ~ogni 1-2 minuti (feedback utenti variabile)
- Industry standard: 1.5-2 secondi per UX forms
- Bilanciamento: troppo corto = carico server | troppo lungo = rischio perdita

RACCOMANDAZIONE: 2000ms (2 secondi)
```

**FONTE:** [Auto-Save Implementation Guide](https://www.dhiwise.com/post/implementing-auto-save-on-forms)

### Feedback Visuale

**PATTERN STANDARD:**
```
[Status Indicator]
┌─────────────────────┐
│ ○ Draft             │  Idle - nessun cambiamento
│ ⟳ Saving...         │  In corso (spinner animato)
│ ✓ Saved at 14:35    │  Completato con timestamp
│ ⚠ Failed to save    │  Errore (retry button)
└─────────────────────┘
```

**ELEMENTI CHIAVE:**
1. **Visibilità bassa** - Non disturbare UX
2. **Timestamp** - Rassicura l'utente
3. **Animazione** - Durante salvataggio
4. **Errore chiaro** - Con possibilità di retry

**FONTE:** [Saving and Feedback - GitLab Design System](https://design.gitlab.com/usability/saving-and-feedback)

### Draft Recovery

**STRATEGIE:**
1. **Server-side** (Gmail API) - Drafts persistiti su Gmail
2. **LocalStorage** - Fallback browser (recovery crash)
3. **Modal warning** - "You have unsaved draft" on exit

**PATTERN RECOVERY:**
```
User apre Compose Modal:
1. Check localStorage per draft temporaneo
2. Se esiste: "Restore draft from [timestamp]?"
3. Se accetta: carica da localStorage
4. Se rifiuta: elimina localStorage

User riapre app dopo crash:
1. Check Gmail API drafts list
2. Mostra modal: "You have X unsaved drafts"
3. Lista cliccabile per recupero
```

---

## 3. CODEBASE MIRACOLLOOK - Cosa Già Esiste

### Backend

#### File Esistenti

```
backend/gmail/
├── compose.py       ✅ /send, /reply, /forward
├── utils.py         ✅ create_message(), create_reply_message()
├── messages.py      ✅ /inbox, /message/{id}
├── actions.py       ✅ /archive, /trash, /star
├── api.py           ✅ Router principale
└── [altri moduli]
```

**MANCANO:**
- ❌ `/drafts/create` - Crea draft
- ❌ `/drafts/update` - Aggiorna draft esistente
- ❌ `/drafts/list` - Lista drafts
- ❌ `/drafts/{id}` - Ottieni draft specifico
- ❌ `/drafts/{id}/send` - Invia draft

**RIUTILIZZABILE:**
- ✅ `get_gmail_service()` - Servizio autenticato
- ✅ `create_message()` - Già formatta MIME
- ✅ Error handling patterns - HTTP 401/429/500

### Frontend

#### ComposeModal Esistente

```tsx
// File: frontend/src/components/Compose/ComposeModal.tsx
// Status: BASIC - solo invio immediato

Stato attuale:
✅ Form completo (to, cc, bcc, subject, body)
✅ Keyboard shortcuts (Cmd+Enter to send)
✅ Error/Success feedback
✅ useSendEmail hook

Mancano:
❌ Stato draft (draft_id)
❌ Auto-save logic
❌ Debounce handler
❌ Save indicator
❌ Draft recovery on open
❌ LocalStorage fallback
```

#### Hook Disponibili

```
frontend/src/hooks/
├── useEmails.ts     ✅ useSendEmail (mutation)
└── [da creare: useDraft.ts]
```

---

## 4. PIANO IMPLEMENTAZIONE - Step by Step

### FASE 1: Backend Drafts API (2h)

**File:** `backend/gmail/drafts.py` (NUOVO)

```python
"""
Miracollook - Gmail Drafts
Endpoint per gestione bozze email
"""

@router.post("/drafts/create")
async def create_draft(
    to: str,
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    html: bool = False
):
    """Crea nuovo draft"""
    # 1. Usa create_message() da utils
    # 2. service.users().drafts().create()
    # 3. Return draft_id

@router.put("/drafts/{draft_id}")
async def update_draft(draft_id: str, ...):
    """Aggiorna draft esistente"""
    # 1. service.users().drafts().update(id=draft_id)
    # 2. Return updated draft_id

@router.get("/drafts")
async def list_drafts():
    """Lista tutti drafts utente"""
    # service.users().drafts().list()

@router.get("/drafts/{draft_id}")
async def get_draft(draft_id: str):
    """Ottieni draft specifico"""
    # service.users().drafts().get()

@router.post("/drafts/{draft_id}/send")
async def send_draft(draft_id: str):
    """Invia draft (elimina automaticamente)"""
    # service.users().drafts().send()
```

**Registrazione:** Aggiungere a `backend/gmail/api.py`:
```python
from . import drafts
router.include_router(drafts.router, tags=["Drafts"])
```

---

### FASE 2: Frontend Hook Auto-Save (1h)

**File:** `frontend/src/hooks/useDraft.ts` (NUOVO)

```typescript
import { useCallback, useEffect, useRef } from 'react';
import { useMutation } from '@tanstack/react-query';
import { debounce } from 'lodash';

interface DraftData {
  to: string;
  subject: string;
  body: string;
  cc?: string;
  bcc?: string;
}

export const useDraft = () => {
  const draftIdRef = useRef<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  // Mutation per create/update
  const saveDraft = useMutation({
    mutationFn: async (data: DraftData) => {
      if (draftIdRef.current) {
        // Update esistente
        return api.put(`/drafts/${draftIdRef.current}`, data);
      } else {
        // Crea nuovo
        const result = await api.post('/drafts/create', data);
        draftIdRef.current = result.data.draft_id;
        return result;
      }
    },
    onMutate: () => setSaveStatus('saving'),
    onSuccess: () => {
      setSaveStatus('saved');
      setLastSaved(new Date());
    },
    onError: () => setSaveStatus('error')
  });

  // Debounced save (2 secondi)
  const debouncedSave = useRef(
    debounce((data: DraftData) => {
      saveDraft.mutate(data);
    }, 2000)
  ).current;

  // Auto-save function
  const autoSave = useCallback((data: DraftData) => {
    debouncedSave(data);
  }, [debouncedSave]);

  // Cleanup
  useEffect(() => {
    return () => debouncedSave.cancel();
  }, [debouncedSave]);

  // LocalStorage fallback
  const saveToLocalStorage = useCallback((data: DraftData) => {
    localStorage.setItem('draft_temp', JSON.stringify({
      ...data,
      timestamp: new Date().toISOString()
    }));
  }, []);

  const loadFromLocalStorage = useCallback(() => {
    const stored = localStorage.getItem('draft_temp');
    if (stored) {
      return JSON.parse(stored);
    }
    return null;
  }, []);

  return {
    autoSave,
    saveStatus,
    lastSaved,
    draftId: draftIdRef.current,
    saveToLocalStorage,
    loadFromLocalStorage
  };
};
```

---

### FASE 3: Integrazione ComposeModal (1h)

**Modifiche a:** `frontend/src/components/Compose/ComposeModal.tsx`

```typescript
import { useDraft } from '../../hooks/useDraft';

export const ComposeModal = ({ isOpen, onClose }: ComposeModalProps) => {
  const { autoSave, saveStatus, lastSaved } = useDraft();

  // Trigger autosave su ogni change
  useEffect(() => {
    if (to || subject || body) {
      autoSave({ to, subject, body, cc, bcc });
    }
  }, [to, subject, body, cc, bcc]);

  // Recovery on open
  useEffect(() => {
    if (isOpen) {
      const draft = loadFromLocalStorage();
      if (draft) {
        // Show modal: "Restore draft?"
      }
    }
  }, [isOpen]);

  // Save on beforeunload
  useEffect(() => {
    const handleBeforeUnload = () => {
      saveToLocalStorage({ to, subject, body, cc, bcc });
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [to, subject, body]);

  return (
    // ... existing UI
    <div className="draft-status">
      {saveStatus === 'saving' && '⟳ Saving...'}
      {saveStatus === 'saved' && `✓ Saved at ${format(lastSaved, 'HH:mm')}`}
      {saveStatus === 'error' && '⚠ Failed to save'}
    </div>
  );
};
```

---

## 5. CONSIDERAZIONI TECNICHE

### Rate Limiting Gmail API

**ATTENZIONE:**
- Gmail API ha rate limits (non documentati esattamente)
- Utenti riportano problemi con autosave troppo frequente
- **Soluzione:** Debounce 2s è sicuro

### Operational Transform (Advanced)

Gmail usa **Operational Transform** per evitare conflitti:
- Invia solo **delta** (insert/delete operations)
- Non l'intero contenuto ogni volta
- **Per MVP:** Non necessario - Gmail API accetta full message

**FONTE:** [Hashnode - Gmail Drafts Implementation](https://hashnode.com/post/how-to-implement-an-auto-save-draft-feature-like-gmail-using-backend-technologies-ciibz8efv00ksj3xt8bzofemm)

### Gestione Errori

| Errore | Causa | Soluzione |
|--------|-------|-----------|
| 401 | Token scaduto | Redirect a /auth/login |
| 429 | Rate limit | Retry con exponential backoff |
| 404 | Draft cancellato | Crea nuovo draft |
| 500 | Gmail API down | LocalStorage fallback |

### Testing

**SCENARI:**
1. ✅ User scrive → autosave → vede "Saved"
2. ✅ User chiude modal → draft persiste
3. ✅ User riapre modal → draft recuperato
4. ✅ Browser crash → recovery da localStorage
5. ✅ Network error → mostra warning, salva local
6. ✅ Invio riuscito → draft eliminato

---

## 6. RACCOMANDAZIONI FINALI

### DO ✅

1. **Debounce 2s** - Bilanciamento perfetto
2. **LocalStorage fallback** - Sicurezza extra
3. **Timestamp visibile** - Rassicura utente
4. **Silent autosave** - Non disturbare UX
5. **Recovery modal** - "Restore draft?" chiaro
6. **Cleanup localStorage** - Dopo invio/cancellazione

### DON'T ❌

1. ❌ Autosave < 1s - Troppo frequente
2. ❌ Bloccare UI durante save - Deve essere async
3. ❌ Salvare campo vuoto - Spreco risorse
4. ❌ Multiple drafts stessa email - Confonde utente
5. ❌ Mancanza feedback errore - User deve sapere

### Pattern Consigliato: HYBRID

```
┌──────────────────────────────────────┐
│ PRIMARY: Gmail API Drafts            │
│ - Server-side persistence            │
│ - Sync across devices                │
│ - Debounce 2s                        │
│                                      │
│ FALLBACK: LocalStorage               │
│ - Crash recovery                     │
│ - Network offline                    │
│ - Instant save on beforeunload       │
└──────────────────────────────────────┘
```

---

## 7. FONTI

**Gmail API:**
- [Working with Drafts | Gmail API](https://developers.google.com/workspace/gmail/api/guides/drafts)
- [users.drafts.create | Gmail API](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.drafts/create)
- [users.drafts.update | Gmail API](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.drafts/update)

**UX Best Practices:**
- [UX: Autosave or explicit save action](https://www.damianwajer.com/blog/autosave/)
- [Saving and Feedback | GitLab Design System](https://design.gitlab.com/usability/saving-and-feedback)
- [Design to save people from themselves](https://brianlovin.com/writing/design-to-save-people-from-themselves)

**Implementation Patterns:**
- [A Guide to Implementing Auto-Save Functionality](https://www.dhiwise.com/post/implementing-auto-save-on-forms)
- [How to implement auto save draft like Gmail](https://hashnode.com/post/how-to-implement-an-auto-save-draft-feature-like-gmail-using-backend-technologies-ciibz8efv00ksj3xt8bzofemm)

**React Debounce:**
- [How to debounce and throttle in React](https://www.developerway.com/posts/debouncing-in-react)
- [Using Lodash debounce with React and TypeScript](https://carlrippon.com/using-lodash-debounce-with-react-and-ts/)
- [React Debounce: Syntax, Usage, and Examples](https://mimo.org/glossary/react/debounce)

---

## PROSSIMI STEP

### IMMEDIATI (oggi)
1. Creare `backend/gmail/drafts.py` con 5 endpoint
2. Testare endpoint con Postman/curl
3. Creare `frontend/src/hooks/useDraft.ts`

### BREVE TERMINE (domani)
4. Integrare in ComposeModal
5. Aggiungere UI feedback (Saving/Saved)
6. Implementare recovery modal

### MIGLIORAMENTI FUTURI
7. Draft list sidebar (inbox-style)
8. Draft preview (quick view)
9. Metrics (quanti drafts salvati, success rate)

---

**NOTA FINALE:**

Drafts sono BASIC FEATURE per email client moderno. Utenti si aspettano autosave - mancanza = frustrazione alta. Implementazione relativamente semplice (3-4h) con alto ROI UX.

**Priorità:** 🔴 ALTA - Feature richiesta frequentemente

---

*Ricerca completata da Cervella-Researcher*
*14 Gennaio 2026, ore 07:30*
