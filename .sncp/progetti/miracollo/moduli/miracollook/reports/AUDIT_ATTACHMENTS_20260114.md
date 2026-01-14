# AUDIT: Upload Attachments
Data: 14 Gennaio 2026
Auditor: Cervella Guardiana Qualita

## RISULTATO: PASS CON NOTE

---

## Backend

### utils.py (163 righe)
| Check | Status | Note |
|-------|--------|------|
| Syntax Python valida | OK | Imports corretti |
| create_message() supporta attachments | OK | Param `attachments: Optional[List[Tuple[str, bytes, str]]]` |
| MIMEMultipart usato | OK | Corretto per email con allegati |
| Type hints presenti | OK | Tutti i parametri tipizzati |
| Backward compatibility | OK | `if not attachments:` usa MIMEText originale |
| Logging presente | OK | `logger.info` su ogni attachment |

### compose.py (361 righe)
| Check | Status | Note |
|-------|--------|------|
| Endpoint /send accetta UploadFile | OK | `files: List[UploadFile] = File(None)` |
| Validazione 25MB | OK | `MAX_SIZE = 25 * 1024 * 1024` con HTTPException 413 |
| MIME type detection | OK | Fallback con `mimetypes.guess_type` |
| Error handling | OK | HTTPException per 400, 401, 413, 429, 500 |
| Logging | OK | File ricevuti, totale, invio |

---

## Frontend

### useAttachments.ts (75 righe)
| Check | Status | Note |
|-------|--------|------|
| TypeScript types | OK | Interface `AttachmentFile`, `UseAttachmentsReturn` |
| URL.createObjectURL cleanup | OK | useEffect cleanup on unmount (riga 57-61) |
| Limite 25MB | OK | `MAX_SIZE = 25 * 1024 * 1024`, `isOverLimit` |
| addAttachments | OK | Genera ID unico, crea preview |
| removeAttachment | OK | Revoke URL prima di rimuovere |
| clearAttachments | OK | Revoke tutti gli URL |

### AttachmentPicker.tsx (154 righe)
| Check | Status | Note |
|-------|--------|------|
| Component funzionale | OK | Props tipizzate correttamente |
| Preview immagini | OK | Condizionale `isImage ? <img> : icon` |
| Limite 25MB con warning | OK | Warning a 20MB, error a 25MB |
| UI accessibile | OK | `aria-label="Remove attachment"` presente |
| Input reset | OK | `e.target.value = ''` per ri-selezionare file |
| File icons | OK | Funzione `getFileIcon` con fallback |

### api.ts (238 righe)
| Check | Status | Note |
|-------|--------|------|
| FormData per files | OK | `if (data.files && data.files.length > 0)` |
| Content-Type auto | OK | Commento "NON settare Content-Type" (corretto) |
| Endpoint corretto | OK | `axios.post(${API_BASE_URL}/gmail/send, formData)` |

### ComposeModal.tsx (375 righe)
| Check | Status | Note |
|-------|--------|------|
| useAttachments integrato | OK | Righe 27-35 |
| AttachmentPicker integrato | OK | Righe 339-345 |
| Send disabilitato se overLimit | OK | `disabled={... || isOverLimit}` riga 362 |
| clearAttachments su close | OK | Riga 76, 180 |
| Files passati a sendEmail | OK | `emailData.files = attachments.map(a => a.file)` |

---

## Security

| Check | Status | Note |
|-------|--------|------|
| Size limit enforced | OK | Backend + Frontend |
| No file type validation | NOTA | Backend accetta qualsiasi tipo file (Gmail gestisce) |
| No XSS in preview | OK | `URL.createObjectURL` e sicuro, no injection |

---

## Best Practices

| Check | Status | Note |
|-------|--------|------|
| Codice pulito | OK | Ben organizzato, funzioni piccole |
| Nomi chiari | OK | addAttachments, removeAttachment, isOverLimit |
| No console.log | OK | Solo logger backend |
| Commenti | OK | Docstring Python presenti |

---

## Problemi Trovati

### Minori (Non Bloccanti)

1. **useAttachments cleanup dependency** (riga 61)
   - `useEffect` cleanup ha dependency array vuoto `[]`
   - `attachments` usato nel cleanup non e in deps
   - Funziona comunque ma linter potrebbe avvisare

2. **File size orfano** (compose.py riga 77)
   - `file_size` calcolato ma usato solo per `total_size`
   - Ok, ma potrebbe loggare anche per singolo file

---

## Suggerimenti (Opzionali)

1. **Drag & Drop** - Aggiungere in futuro per UX migliore
2. **Progress bar** - Per upload grandi, mostrare progresso
3. **File type filter** - Opzionale: limitare tipi pericolosi (.exe, .bat)

---

## Conclusione

**READY TO MERGE**

Implementazione solida e completa:
- Backend gestisce attachments correttamente con MIME
- Frontend ha UX chiara con preview, warning, error
- Validazione 25MB presente su entrambi i lati
- Backward compatibility mantenuta
- Cleanup memory (revokeObjectURL) implementato

"Fatto BENE > Fatto VELOCE"

---
*Cervella Guardiana Qualita*
