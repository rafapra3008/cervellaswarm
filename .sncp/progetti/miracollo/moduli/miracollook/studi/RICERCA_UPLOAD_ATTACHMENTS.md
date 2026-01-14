# Ricerca: Upload Attachments per Miracallook Email

**Data**: 13 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Status**: ✅ Completata

---

## TL;DR - Raccomandazione Rapida

**Approccio consigliato**: **Multipart/form-data** con FastAPI `UploadFile`

**Perché**:
- Standard HTTP nativo per file upload
- Memory-efficient per file grandi (fino a 25MB limite Gmail)
- FastAPI supporto nativo con `UploadFile`
- No overhead base64 encoding (+33% dimensione)
- Compatible con Gmail API (usa MIMEMultipart standard)

**Implementazione**:
1. Backend: `UploadFile` in FastAPI + MIMEMultipart + MIMEBase
2. Frontend: `<input type="file" multiple>` + FormData
3. Gmail API: MIMEMultipart con base64url encoding finale

---

## 1. Gmail API - Attachment Requirements

### 1.1 Struttura MIME

Gmail API richiede messaggi con attachments strutturati come **multipart MIME**.

**Componenti chiave**:
```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import base64
```

**Struttura messaggio**:
```
MIMEMultipart (container)
├── MIMEText (body del messaggio)
└── MIMEBase (attachment 1)
    └── headers: Content-Disposition, filename
    └── payload: file data base64-encoded
└── MIMEBase (attachment 2)
    └── ...
```

### 1.2 Encoding Process

**Step 1**: Costruisci MIME message con attachments
**Step 2**: Converti in bytes: `message.as_bytes()`
**Step 3**: Encode base64url: `base64.urlsafe_b64encode(...).decode()`
**Step 4**: Invia a Gmail API: `{"raw": encoded_message}`

### 1.3 Limiti Gmail

| Limite | Valore |
|--------|--------|
| Max attachment size (totale) | 25 MB |
| Max attachment singolo | 25 MB |
| Formati supportati | Tutti (Gmail usa MIME type detection) |

**Fonte**: [Gmail API Sending Guide](https://developers.google.com/workspace/gmail/api/guides/sending)

---

## 2. Backend Python - Implementazione

### 2.1 Modifiche a `create_message()` Esistente

**File**: `miracallook/backend/gmail/api.py`

**Funzione attuale** (linee 44-72):
```python
def create_message(to: str, subject: str, body: str,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None,
                   html: bool = False) -> dict:
    message = MIMEText(body, 'html' if html else 'plain')
    message['to'] = to
    message['subject'] = subject
    # ...
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}
```

**Problema**: Usa `MIMEText` (single-part), incompatibile con attachments.

**Soluzione**: Switchare a `MIMEMultipart` quando ci sono attachments.

### 2.2 Nuova Implementazione con Attachments

```python
def create_message(to: str, subject: str, body: str,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None,
                   html: bool = False,
                   attachments: Optional[List[tuple]] = None) -> dict:
    """
    Crea messaggio MIME per invio email.

    Args:
        to: Destinatario principale
        subject: Oggetto email
        body: Corpo email
        cc: Lista CC (opzionale)
        bcc: Lista BCC (opzionale)
        html: Se True, body è HTML, altrimenti plain text
        attachments: Lista di tuple (filename: str, file_data: bytes, mime_type: str)

    Returns:
        dict: Messaggio pronto per Gmail API
    """
    # Se ci sono attachments, usa MIMEMultipart
    if attachments:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject

        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)

        # Aggiungi body come prima parte
        body_part = MIMEText(body, 'html' if html else 'plain')
        message.attach(body_part)

        # Aggiungi attachments
        for filename, file_data, mime_type in attachments:
            # Determina main_type e sub_type
            main_type, sub_type = mime_type.split('/', 1)

            # Crea attachment part
            attachment_part = MIMEBase(main_type, sub_type)
            attachment_part.set_payload(file_data)

            # Encode in base64
            encoders.encode_base64(attachment_part)

            # Aggiungi header Content-Disposition
            attachment_part.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename
            )

            message.attach(attachment_part)

    else:
        # Senza attachments, mantieni comportamento originale
        message = MIMEText(body, 'html' if html else 'plain')
        message['to'] = to
        message['subject'] = subject

        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)

    # Encoding finale per Gmail API
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}
```

### 2.3 FastAPI Endpoint con File Upload

**Nuovo endpoint**: `/gmail/send` con supporto attachments

**Opzione A: Multipart/form-data (CONSIGLIATA)**

```python
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
import mimetypes

@router.post("/send")
async def send_email(
    to: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    cc: Optional[str] = Form(None),  # Comma-separated
    bcc: Optional[str] = Form(None),  # Comma-separated
    html: bool = Form(False),
    files: List[UploadFile] = File(None)  # Multiple files
):
    """
    Invia email con attachments.

    IMPORTANTE: Usa multipart/form-data!

    Frontend esempio:
    const formData = new FormData();
    formData.append('to', 'email@example.com');
    formData.append('subject', 'Test');
    formData.append('body', 'Hello');
    files.forEach(file => formData.append('files', file));

    fetch('/gmail/send', {
        method: 'POST',
        body: formData  // NO Content-Type header! Browser lo setta auto
    });
    """
    service = get_gmail_service()

    # Converti cc/bcc da stringa a lista
    cc_list = [x.strip() for x in cc.split(',')] if cc else None
    bcc_list = [x.strip() for x in bcc.split(',')] if bcc else None

    # Processa attachments
    attachments_data = []
    if files:
        total_size = 0

        for upload_file in files:
            # Leggi file data
            file_data = await upload_file.read()
            file_size = len(file_data)
            total_size += file_size

            # Check dimensione
            if total_size > 25 * 1024 * 1024:  # 25MB
                raise HTTPException(
                    status_code=413,
                    detail="Attachments totali superano 25MB (limite Gmail)"
                )

            # Determina MIME type
            mime_type = upload_file.content_type
            if not mime_type or mime_type == 'application/octet-stream':
                # Fallback: guess da filename
                guessed_type, _ = mimetypes.guess_type(upload_file.filename)
                mime_type = guessed_type or 'application/octet-stream'

            attachments_data.append((
                upload_file.filename,
                file_data,
                mime_type
            ))

            logger.info(f"Attachment: {upload_file.filename} ({file_size} bytes, {mime_type})")

    try:
        # Crea messaggio con attachments
        message = create_message(
            to=to,
            subject=subject,
            body=body,
            cc=cc_list,
            bcc=bcc_list,
            html=html,
            attachments=attachments_data if attachments_data else None
        )

        # Invia
        sent = service.users().messages().send(userId="me", body=message).execute()

        logger.info(f"Email inviata: {sent['id']} a {to} con {len(attachments_data)} attachments")

        return {
            "status": "sent",
            "message_id": sent['id'],
            "thread_id": sent['threadId'],
            "to": to,
            "subject": subject,
            "attachments_count": len(attachments_data),
            "total_size_bytes": sum(len(a[1]) for a in attachments_data)
        }

    except HttpError as error:
        logger.error(f"Errore invio email: {error}")
        # ... (gestione errori come prima)
```

**Opzione B: Base64 in JSON (NON CONSIGLIATA)**

```python
from pydantic import BaseModel
from typing import List, Optional

class Attachment(BaseModel):
    filename: str
    data_base64: str  # File encoded in base64
    mime_type: str

class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    html: bool = False
    attachments: Optional[List[Attachment]] = None

@router.post("/send-json")
async def send_email_json(request: SendEmailRequest):
    """
    Invia email con attachments encodati in base64.

    ⚠️ SCONSIGLIATO per file > 5MB (overhead +33% dimensione)
    """
    service = get_gmail_service()

    # Decodifica attachments da base64
    attachments_data = []
    if request.attachments:
        for att in request.attachments:
            try:
                file_data = base64.b64decode(att.data_base64)
                attachments_data.append((att.filename, file_data, att.mime_type))
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Errore decodifica attachment {att.filename}: {str(e)}"
                )

    # ... (resto come sopra)
```

---

## 3. Frontend React - Implementazione

### 3.1 Component: File Upload con Preview

```typescript
import React, { useState } from 'react';

interface AttachmentPreview {
  file: File;
  preview: string;  // URL.createObjectURL()
}

export const EmailComposer: React.FC = () => {
  const [to, setTo] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [attachments, setAttachments] = useState<AttachmentPreview[]>([]);
  const [sending, setSending] = useState(false);

  // Handler: selezione file
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    // Crea preview per ogni file
    const newAttachments: AttachmentPreview[] = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];

      // Check dimensione (25MB totale limite Gmail)
      const currentTotalSize = attachments.reduce((sum, a) => sum + a.file.size, 0);
      if (currentTotalSize + file.size > 25 * 1024 * 1024) {
        alert('Dimensione totale attachments supera 25MB');
        return;
      }

      // Crea preview URL
      const previewUrl = URL.createObjectURL(file);

      newAttachments.push({
        file,
        preview: previewUrl
      });
    }

    setAttachments(prev => [...prev, ...newAttachments]);
  };

  // Handler: rimuovi attachment
  const handleRemoveAttachment = (index: number) => {
    setAttachments(prev => {
      // Revoca URL object per evitare memory leak
      URL.revokeObjectURL(prev[index].preview);
      return prev.filter((_, i) => i !== index);
    });
  };

  // Handler: invio email
  const handleSendEmail = async () => {
    setSending(true);

    try {
      // Costruisci FormData (multipart/form-data)
      const formData = new FormData();
      formData.append('to', to);
      formData.append('subject', subject);
      formData.append('body', body);
      formData.append('html', 'false');

      // Aggiungi attachments
      attachments.forEach(att => {
        formData.append('files', att.file);
      });

      const response = await fetch('/gmail/send', {
        method: 'POST',
        body: formData
        // NON settare Content-Type! Browser lo fa automaticamente
      });

      if (!response.ok) {
        throw new Error(`Errore: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Email inviata:', result);

      // Reset form
      setTo('');
      setSubject('');
      setBody('');

      // Cleanup previews
      attachments.forEach(att => URL.revokeObjectURL(att.preview));
      setAttachments([]);

      alert('Email inviata con successo!');

    } catch (error) {
      console.error('Errore invio:', error);
      alert('Errore invio email');
    } finally {
      setSending(false);
    }
  };

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      attachments.forEach(att => URL.revokeObjectURL(att.preview));
    };
  }, []);

  return (
    <div className="email-composer">
      {/* Form fields */}
      <input
        type="text"
        placeholder="To"
        value={to}
        onChange={(e) => setTo(e.target.value)}
      />

      <input
        type="text"
        placeholder="Subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
      />

      <textarea
        placeholder="Message body"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows={10}
      />

      {/* File upload */}
      <div className="attachments-section">
        <label htmlFor="file-input" className="attach-button">
          📎 Attach Files
        </label>
        <input
          id="file-input"
          type="file"
          multiple
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />

        {/* Preview attachments */}
        {attachments.length > 0 && (
          <div className="attachments-preview">
            <h4>Attachments ({attachments.length})</h4>
            {attachments.map((att, index) => (
              <div key={index} className="attachment-item">
                {/* Preview immagine se applicabile */}
                {att.file.type.startsWith('image/') ? (
                  <img
                    src={att.preview}
                    alt={att.file.name}
                    style={{ width: 50, height: 50, objectFit: 'cover' }}
                  />
                ) : (
                  <div className="file-icon">📄</div>
                )}

                <div className="file-info">
                  <div className="file-name">{att.file.name}</div>
                  <div className="file-size">
                    {(att.file.size / 1024).toFixed(1)} KB
                  </div>
                </div>

                <button
                  onClick={() => handleRemoveAttachment(index)}
                  className="remove-button"
                >
                  ✕
                </button>
              </div>
            ))}

            <div className="total-size">
              Total: {(attachments.reduce((sum, a) => sum + a.file.size, 0) / 1024 / 1024).toFixed(2)} MB
            </div>
          </div>
        )}
      </div>

      {/* Send button */}
      <button
        onClick={handleSendEmail}
        disabled={sending || !to || !subject}
      >
        {sending ? 'Sending...' : 'Send Email'}
      </button>
    </div>
  );
};
```

### 3.2 CSS per Preview

```css
.email-composer {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.email-composer input,
.email-composer textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.attachments-section {
  margin: 20px 0;
}

.attach-button {
  display: inline-block;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.attach-button:hover {
  background: #0056b3;
}

.attachments-preview {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: white;
  border-radius: 4px;
  margin-bottom: 8px;
}

.file-icon {
  font-size: 24px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e9ecef;
  border-radius: 4px;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  font-size: 14px;
}

.file-size {
  font-size: 12px;
  color: #6c757d;
}

.remove-button {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 14px;
}

.remove-button:hover {
  background: #c82333;
}

.total-size {
  margin-top: 10px;
  font-size: 12px;
  color: #6c757d;
  text-align: right;
}
```

---

## 4. Confronto Approcci

### Multipart/Form-Data vs Base64 JSON

| Criterio | Multipart/Form-Data | Base64 JSON |
|----------|---------------------|-------------|
| **Dimensione dati** | Originale (es. 10MB) | +33% overhead (es. 13.3MB) |
| **Memory usage** | Stream (low) | Tutto in RAM (alto) |
| **Compatibilità** | Standard HTTP | Richiede encoding/decoding |
| **Complessità frontend** | `FormData` nativo | Manuale base64 encoding |
| **FastAPI support** | `UploadFile` built-in | Custom logic |
| **Limite pratico** | 25MB (limite Gmail) | ~5MB (JSON parsing) |
| **Performance** | ✅ Ottima | ⚠️ Degrada con file grandi |
| **Best practice** | ✅ Consigliato | ❌ Sconsigliato |

**Verdict**: **Multipart/Form-Data vince su tutti i fronti.**

---

## 5. Checklist Implementazione

### Backend (api.py)

- [ ] Modificare `create_message()` per accettare parametro `attachments`
- [ ] Aggiungere logica `MIMEMultipart` quando attachments presenti
- [ ] Loop attachments: `MIMEBase` + `encode_base64` + `Content-Disposition`
- [ ] Modificare endpoint `/send` per accettare `files: List[UploadFile]`
- [ ] Validazione dimensione totale (25MB)
- [ ] MIME type detection con fallback
- [ ] Import necessari:
  ```python
  from email.mime.multipart import MIMEMultipart
  from email.mime.base import MIMEBase
  from email import encoders
  import mimetypes
  ```

### Frontend (EmailComposer)

- [ ] State per attachments: `useState<AttachmentPreview[]>([])`
- [ ] Input file con `multiple` attribute
- [ ] Handler `handleFileSelect`: `URL.createObjectURL()` per preview
- [ ] Handler `handleRemoveAttachment`: cleanup con `URL.revokeObjectURL()`
- [ ] Validazione dimensione totale (25MB)
- [ ] Preview rendering: immagini vs icona file generica
- [ ] FormData construction in `handleSendEmail`
- [ ] Cleanup on unmount: `useEffect` return function
- [ ] Error handling: 413 (file too large), 400 (invalid file)

### Testing

- [ ] Test file singolo (PDF, JPG, TXT)
- [ ] Test multipli file (3-4 file piccoli)
- [ ] Test limite dimensione (tentare 26MB)
- [ ] Test MIME types: immagine, PDF, ZIP, TXT
- [ ] Test remove attachment (verifica memory cleanup)
- [ ] Test invio senza attachments (backward compatibility)
- [ ] Test error cases: network error, Gmail API rate limit

---

## 6. Fonti e Riferimenti

### Documentazione Ufficiale

- [Gmail API - Sending Messages](https://developers.google.com/workspace/gmail/api/guides/sending)
- [Python email.mime Documentation](https://docs.python.org/3/library/email.mime.html)
- [FastAPI Request Files](https://fastapi.tiangolo.com/tutorial/request-files/)

### Tutorial e Guide

- [Learn Data Analysis - Gmail API Attachments](https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-with-attachments-in-python/)
- [Mailtrap - Python Send Email Gmail 2026](https://mailtrap.io/blog/python-send-email-gmail/)
- [BezKoder - React Multiple Image Upload](https://www.bezkoder.com/multiple-image-upload-react-js/)
- [Uploadcare - React File Upload](https://uploadcare.com/blog/how-to-upload-file-in-react/)

### FastAPI Discussioni

- [FastAPI GitHub - UploadFile with payload](https://github.com/fastapi/fastapi/discussions/8435)
- [FastAPI File Upload Best Practices](https://dev.to/spaceofmiah/api-file-upload-done-right-fastapi-1kd1)

---

## 7. Conclusioni

### Raccomandazione Finale

**Implementare upload attachments con approccio Multipart/Form-Data**:

1. **Backend**: Modificare `create_message()` + endpoint `/send` con `UploadFile`
2. **Frontend**: Component React con preview e `FormData`
3. **Validazione**: 25MB limite, MIME type detection
4. **Testing**: Suite completa con vari formati file

**Stima effort**:
- Backend: ~2-3 ore (modify funzione + endpoint + testing)
- Frontend: ~3-4 ore (component + preview + styling + testing)
- **Totale**: ~6 ore per implementazione completa

**Rischi**:
- ⚠️ MIME type detection potrebbe fallire per formati strani (fallback a `application/octet-stream`)
- ⚠️ Memory leak se non cleanup `URL.createObjectURL()` (mitigato con `useEffect`)
- ⚠️ Rate limiting Gmail API se troppi invii con attachments grandi

**Opportunità**:
- ✅ Feature parity con Gmail web client
- ✅ Drag & drop future enhancement possibile
- ✅ Progress bar upload possibile (FastAPI streaming)

---

**Fine Ricerca**
*"Non esistono cose difficili, esistono cose non studiate!"* 🔬
