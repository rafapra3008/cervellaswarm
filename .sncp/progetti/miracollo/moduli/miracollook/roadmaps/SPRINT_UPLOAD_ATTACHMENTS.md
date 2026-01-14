# SPRINT: Upload Attachments
> **Data:** 14 Gennaio 2026
> **Effort:** ~4h totali
> **Status:** READY TO START

---

## OBIETTIVO

Permettere agli utenti di allegare file quando compongono email.
Limite Gmail: 25MB totale.

---

## STEP-BY-STEP

### STEP 1: Backend - Modifiche (1.5h)

**File:** `backend/gmail/compose.py`

```
1.1 [ ] Aggiungere imports necessari
    - from email.mime.multipart import MIMEMultipart
    - from email.mime.base import MIMEBase
    - from email import encoders
    - import mimetypes

1.2 [ ] Modificare create_message()
    - Nuovo parametro: attachments: Optional[List[tuple]] = None
    - Se attachments: usa MIMEMultipart invece di MIMEText
    - Loop: crea MIMEBase per ogni file
    - encode_base64 + Content-Disposition header

1.3 [ ] Modificare endpoint /gmail/send
    - Accettare files: List[UploadFile] = File(None)
    - Processare file: read bytes, get MIME type
    - Validare totale < 25MB
    - Passare a create_message()
```

### STEP 2: Frontend Hook (1h)

**File:** `frontend/src/hooks/useAttachments.ts`

```
2.1 [ ] Creare hook useAttachments()
    - State: attachments con file + preview URL
    - addAttachments(files: FileList)
    - removeAttachment(index: number)
    - clearAttachments()
    - getTotalSize(): number
    - isOverLimit: boolean (>25MB)

2.2 [ ] Implementare preview
    - URL.createObjectURL() per ogni file
    - URL.revokeObjectURL() su remove/unmount
    - Cleanup in useEffect return
```

### STEP 3: Frontend Component (1h)

**File:** `frontend/src/components/Compose/AttachmentPicker.tsx`

```
3.1 [ ] Creare AttachmentPicker component
    - Input type="file" hidden + multiple
    - Button trigger "Attach Files"
    - Lista preview files
    - Remove button [x] per ogni file
    - Total size display

3.2 [ ] Preview visuale
    - Immagini: thumbnail 40x40
    - Altri file: icon generico + nome
    - File size in KB/MB

3.3 [ ] Validazione UI
    - Warning se > 20MB (yellow)
    - Error se > 25MB (red, block send)
```

### STEP 4: Integrare in ComposeModal (0.5h)

**File:** `frontend/src/components/Compose/ComposeModal.tsx`

```
4.1 [ ] Usare useAttachments hook
4.2 [ ] Rendere AttachmentPicker sotto body
4.3 [ ] Modificare handleSend:
    - Costruire FormData invece di JSON
    - Append files al FormData
    - NO Content-Type header (browser auto)
4.4 [ ] Cleanup attachments on close/send
```

---

## TEST PLAN

```
[ ] Invia email senza attachments (backward compat)
[ ] Invia email con 1 attachment PDF
[ ] Invia email con 1 attachment immagine (verifica preview)
[ ] Invia email con 3 attachments misti
[ ] Tenta invio con > 25MB (verifica block)
[ ] Remove attachment e invia (verifica cleanup)
[ ] Chiudi modal senza inviare (verifica cleanup memory)
```

---

## DIPENDENZE

- ComposeModal esistente funzionante
- Endpoint /gmail/send esistente
- create_message() in compose.py

---

## OUTPUT ATTESO

1. Backend accetta files nel send
2. Frontend mostra picker + preview
3. Invio funziona con attachments
4. Limite 25MB rispettato
5. Memory cleanup corretto

---

*Ricerca completa in: `studi/RICERCA_UPLOAD_ATTACHMENTS.md`*
