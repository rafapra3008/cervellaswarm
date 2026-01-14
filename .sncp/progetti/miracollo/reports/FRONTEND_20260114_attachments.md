# OUTPUT: Attachments UI Implementation

**Data**: 20260114 | **Worker**: cervella-frontend
**Progetto**: Miracollo

---

## File Creati/Modificati

### CREATI
1. `/Users/rafapra/Developer/miracollook/frontend/src/hooks/useAttachments.ts`
   - Hook per gestire attachments (add, remove, clear)
   - Preview URL management con cleanup
   - Limite 25MB con isOverLimit flag
   - totalSize calculation

2. `/Users/rafapra/Developer/miracollook/frontend/src/components/Compose/AttachmentPicker.tsx`
   - UI componente per file picker
   - Lista attachments con preview thumbnails (immagini)
   - File icons per tipi non-immagine
   - Size display e warning/error messages
   - Warning giallo > 20MB, error rosso > 25MB
   - Remove button per ogni file

### MODIFICATI
3. `/Users/rafapra/Developer/miracollook/frontend/src/services/api.ts`
   - `sendEmail` ora supporta `files?: File[]`
   - Se files presenti, usa FormData invece di JSON
   - Content-Type automatico dal browser per multipart

4. `/Users/rafapra/Developer/miracollook/frontend/src/components/Compose/ComposeModal.tsx`
   - Import useAttachments e AttachmentPicker
   - AttachmentPicker inserito dopo textarea body
   - clearAttachments su close e su send success
   - Send button disabilitato se isOverLimit
   - Files passati a sendEmail.mutateAsync

---

## Design Choices

### Styling
- Consistente con classi miracollo-* esistenti
- Dark mode friendly
- bg-miracollo-bg-input, text-miracollo-text
- Hover states e transitions
- Warning giallo/rosso per size limits

### UX
- Hidden file input + styled button
- Thumbnails per immagini (URL.createObjectURL)
- Icons emoji per altri file types (📄, 📊, 🎥, etc)
- Total size display sempre visibile
- Remove button con hover danger state
- Disabled send se > 25MB

### Performance
- URL.createObjectURL per preview (no base64)
- Cleanup automatico su unmount (useEffect return)
- Cleanup su remove singolo
- Multiple files support

---

## Come Testare

### Frontend Test (senza backend)
1. `cd /Users/rafapra/Developer/miracollook/frontend`
2. `npm run dev`
3. Apri ComposeModal
4. Click "📎 Attach Files"
5. Seleziona files (anche multipli)
6. Verifica preview/icons
7. Verifica total size display
8. Verifica warning > 20MB
9. Verifica error e disabled send > 25MB
10. Verifica remove button funziona
11. Verifica cleanup su close modal

### Full Test (con backend)
**NOTA**: Il backend DEVE supportare FormData con `files` multipart!

Endpoint atteso: `POST /gmail/send`
- Se `files` presente → FormData multipart
- Se NO files → JSON normale

Backend deve parsare:
```python
files: List[UploadFile] = File(None)
```

---

## Note per Guardiana

### Verificare
- [ ] Backend pronto per FormData multipart
- [ ] Endpoint `/gmail/send` gestisce `files: List[UploadFile]`
- [ ] Attachment encoding/decoding corretto
- [ ] Email inviate con attachments arrivano corrette

### Se Backend NON Pronto
Backend deve aggiungere:
1. `from fastapi import File, UploadFile`
2. Modificare `/gmail/send` per accettare Form + files
3. Usare Gmail API per allegare files

---

## Status

**Frontend**: ✅ COMPLETATO
**Backend**: ⚠️ DA VERIFICARE

L'UI è pronta e funzionale. Backend deve supportare multipart/form-data.

---

*"I dettagli fanno SEMPRE la differenza."*
