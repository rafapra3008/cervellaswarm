# UPLOAD ATTACHMENTS - Design Specs
> **Data:** 14 Gennaio 2026
> **Status:** READY FOR IMPLEMENTATION
> **Effort:** ~4h (ricerca gia completa!)
> **Ricerca:** `studi/RICERCA_UPLOAD_ATTACHMENTS.md`

---

## DECISIONE

Implementare upload attachments nel ComposeModal usando **Multipart/Form-Data**.

**Perche questo approccio:**
- Standard HTTP nativo
- Memory-efficient (no +33% overhead base64)
- FastAPI `UploadFile` built-in
- Compatibile con Gmail API (25MB limite)

---

## COSA IMPLEMENTARE

### Backend (~1.5h)

1. **Modificare `create_message()`** in `compose.py`
   - Aggiungere parametro `attachments: List[tuple]`
   - Switchare a `MIMEMultipart` quando ci sono attachments
   - Loop: `MIMEBase` + `encode_base64` + `Content-Disposition`

2. **Modificare endpoint `/gmail/send`**
   - Accettare `files: List[UploadFile] = File(None)`
   - Validazione 25MB totale
   - MIME type detection

### Frontend (~2.5h)

1. **Hook `useAttachments.ts`**
   - State per files con preview
   - `addAttachment()` - URL.createObjectURL()
   - `removeAttachment()` - cleanup URL
   - `getTotalSize()` - validazione 25MB
   - Cleanup on unmount

2. **Component `AttachmentPicker.tsx`**
   - Input file hidden + button trigger
   - Preview list (immagini thumbnail, altri icon file)
   - Remove button per ogni file
   - Total size indicator
   - 25MB warning

3. **Modificare `ComposeModal.tsx`**
   - Integrare hook useAttachments
   - Area attachments sotto body
   - FormData in send (non JSON!)

---

## UI SPECS

### AttachmentPicker Layout

```
┌─────────────────────────────────────────────────┐
│ 📎 Attach Files                    Total: 2.5MB │
├─────────────────────────────────────────────────┤
│ ┌─────┐ document.pdf           1.2MB    [x]    │
│ │ 📄 │ application/pdf                         │
│ └─────┘                                         │
│ ┌─────┐ photo.jpg              1.3MB    [x]    │
│ │ 🖼️ │ image/jpeg (thumbnail)                  │
│ └─────┘                                         │
└─────────────────────────────────────────────────┘
```

### Interazioni

- Click "Attach Files" → file picker nativo
- Drag & drop (future enhancement)
- Click [x] → rimuovi attachment
- Warning se > 25MB

---

## FILE DA MODIFICARE/CREARE

### Backend
```
backend/gmail/compose.py     # Modificare create_message() + send endpoint
```

### Frontend
```
frontend/src/hooks/useAttachments.ts              # NUOVO - hook gestione files
frontend/src/components/Compose/AttachmentPicker.tsx  # NUOVO - UI picker
frontend/src/components/Compose/ComposeModal.tsx      # MOD - integrare attachments
frontend/src/services/api.ts                          # MOD - sendEmail con FormData
```

---

## CHECKLIST IMPLEMENTAZIONE

### Backend
- [ ] Import: MIMEMultipart, MIMEBase, encoders, mimetypes
- [ ] Modificare `create_message()` con parametro attachments
- [ ] MIMEMultipart container quando attachments
- [ ] Loop attachments: MIMEBase + encode_base64
- [ ] Endpoint: `files: List[UploadFile] = File(None)`
- [ ] Validazione 25MB totale
- [ ] MIME type detection + fallback

### Frontend
- [ ] `useAttachments.ts` hook con state + handlers
- [ ] URL.createObjectURL per preview
- [ ] URL.revokeObjectURL cleanup
- [ ] `AttachmentPicker.tsx` component
- [ ] Preview: thumbnail immagini, icon altri
- [ ] Remove button
- [ ] Size indicator
- [ ] 25MB validation + warning
- [ ] Integrare in ComposeModal
- [ ] FormData invece di JSON per send
- [ ] Cleanup on modal close

### Testing
- [ ] Test singolo file (PDF, JPG)
- [ ] Test multipli file
- [ ] Test limite 25MB
- [ ] Test remove attachment
- [ ] Test send senza attachments (backward compat)
- [ ] Test tipi file vari (ZIP, TXT, DOCX)

---

## RIFERIMENTI

- Ricerca completa: `studi/RICERCA_UPLOAD_ATTACHMENTS.md`
- Gmail API: `studi/RICERCA_GMAIL_ATTACHMENTS.md`
- Performance: `studi/RICERCA_ATTACHMENTS_PERFORMANCE.md`

---

*"Non esistono cose difficili, esistono cose non studiate!"*
