# RICERCA: Gmail API Attachments per Miracollook

**Data ricerca:** 13 Gennaio 2026
**Researcher:** Cervella-Researcher
**Progetto:** Miracollook (Email Client per Hotel)
**Obiettivo:** Implementazione completa gestione attachments (view, download, upload)

---

## EXECUTIVE SUMMARY

### TL;DR

Gmail API fornisce endpoint dedicati per attachments con struttura ben definita:
- **Download**: `GET /users/me/messages/{messageId}/attachments/{attachmentId}`
- **Upload**: MIME multipart con base64 encoding
- **Limite dimensione**: 25MB email totale, 35MB con encoding (Google Drive auto per file più grandi)
- **Formato dati**: Base64 URL-safe encoding per tutti gli attachments

### Raccomandazione Implementazione

**APPROCCIO CONSIGLIATO:**
1. **Backend FastAPI** - Streaming per efficienza memoria
2. **Attachment metadata** - Lista dal message payload (no chiamate extra)
3. **Download on-demand** - Solo quando utente richiede
4. **Upload multipart** - Per compatibilità con Gmail API

---

## 1. GMAIL API - ATTACHMENTS

### 1.1 Endpoint Download Attachment

**API Endpoint:**
```
GET https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{messageId}/attachments/{id}
```

**Path Parameters:**

| Parameter | Type | Descrizione |
|-----------|------|-------------|
| `userId` | string | Email utente o "me" per autenticato |
| `messageId` | string | ID del messaggio contenente l'attachment |
| `id` | string | Attachment ID (dal message payload) |

**OAuth Scopes Richiesti:**

Uno di questi:
- `https://mail.google.com/` (full access)
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.readonly` (solo lettura)

**Response Body:**

```json
{
  "size": 12345,
  "data": "base64url_encoded_data..."
}
```

### 1.2 Struttura Message Payload - Parts

**Come Gmail organizza gli attachments:**

```json
{
  "id": "message_id",
  "payload": {
    "mimeType": "multipart/mixed",
    "parts": [
      {
        "mimeType": "text/plain",
        "body": { "data": "..." }
      },
      {
        "filename": "documento.pdf",
        "mimeType": "application/pdf",
        "body": {
          "attachmentId": "ANGjdJ8...",
          "size": 45678
        },
        "headers": [
          {
            "name": "Content-Disposition",
            "value": "attachment; filename=\"documento.pdf\""
          }
        ]
      }
    ]
  }
}
```

**Identificare Attachments vs Inline Images:**

| Tipo | Come Riconoscerlo |
|------|-------------------|
| **Attachment** | `headers[].Content-Disposition` contiene "attachment" |
| **Inline Image** | `headers[].Content-Disposition` contiene "inline" E `headers[].Content-ID` presente |
| **Regular Content** | Nessun `filename`, nessun `attachmentId` |

**Regola Chiave:**
- Se `body.attachmentId` esiste → serve chiamata separata per ottenere dati
- Se `body.data` esiste E nessun attachmentId → dati già nel payload

### 1.3 Upload Attachments (Sending Email)

**Metodi Upload:**

| Metodo | Dimensione | Quando Usare |
|--------|-----------|--------------|
| **Simple** | ≤ 5 MB | File piccoli, no metadata |
| **Multipart** | ≤ 25 MB | File + metadata in una request |
| **Resumable** | > 5 MB | File grandi, connessioni instabili |

**Per email hotel tipiche: MULTIPART è ideale**

**Formato Email con Attachment:**
```
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="boundary_string"

--boundary_string
Content-Type: text/plain; charset="UTF-8"

Testo email qui...

--boundary_string
Content-Type: application/pdf; name="fattura.pdf"
Content-Disposition: attachment; filename="fattura.pdf"
Content-Transfer-Encoding: base64

[base64_encoded_file_data]
--boundary_string--
```

### 1.4 Limiti e Restrizioni

**Dimensioni:**

| Limite | Valore | Note |
|--------|--------|------|
| Max email totale | 25 MB | Include tutti gli attachments |
| Max con encoding | 35 MB | MIME base64 aumenta del ~33% |
| Max per upload API | 35 MB | Specifico Gmail API |
| File grandi | Auto Google Drive | Gmail converte automaticamente |

**MIME Encoding Impact:**
- File 10 MB → ~13.3 MB dopo base64 encoding
- Calcolare sempre overhead per validazione

**MIME Types Supportati:**
- Tutti i MIME types standard
- Email message: `message/rfc822`
- Verificare con `mimetypes.guess_type()` in Python

---

## 2. IMPLEMENTAZIONE PYTHON

### 2.1 Funzione: Lista Attachments da Message

```python
from typing import List, Dict, Optional
import base64

def extract_attachments_metadata(message: dict) -> List[Dict]:
    """
    Estrae metadata di tutti gli attachments da un messaggio Gmail.

    Args:
        message: Risposta Gmail API (message resource)

    Returns:
        Lista di dict con metadata attachments:
        [{
            'attachmentId': str,
            'filename': str,
            'mimeType': str,
            'size': int,
            'isInline': bool
        }]
    """
    attachments = []

    def parse_parts(parts, message_id):
        if not parts:
            return

        for part in parts:
            # Ricorsione per parti nested
            if part.get('parts'):
                parse_parts(part.get('parts'), message_id)

            filename = part.get('filename')
            mime_type = part.get('mimeType')
            body = part.get('body', {})
            attachment_id = body.get('attachmentId')

            # Solo se ha attachmentId (file esterno)
            if attachment_id and filename:
                # Determina se inline o attachment
                is_inline = False
                headers = part.get('headers', [])

                for header in headers:
                    if header.get('name') == 'Content-Disposition':
                        value = header.get('value', '')
                        is_inline = 'inline' in value.lower()
                        break

                attachments.append({
                    'attachmentId': attachment_id,
                    'filename': filename,
                    'mimeType': mime_type,
                    'size': body.get('size', 0),
                    'isInline': is_inline,
                    'messageId': message_id
                })

    # Avvia parsing
    payload = message.get('payload', {})
    parse_parts(payload.get('parts'), message.get('id'))

    return attachments
```

### 2.2 Funzione: Download Attachment

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

async def download_attachment(
    service,
    message_id: str,
    attachment_id: str
) -> bytes:
    """
    Scarica un attachment da Gmail API.

    Args:
        service: Gmail API service object
        message_id: ID del messaggio
        attachment_id: ID dell'attachment

    Returns:
        Bytes del file decodificato
    """
    try:
        attachment = service.users().messages().attachments().get(
            userId='me',
            messageId=message_id,
            id=attachment_id
        ).execute()

        # Decodifica base64 URL-safe
        data = attachment.get('data')
        if data:
            file_data = base64.urlsafe_b64decode(data)
            return file_data
        else:
            raise ValueError("No data in attachment response")

    except Exception as e:
        raise Exception(f"Error downloading attachment: {str(e)}")
```

### 2.3 Funzione: Send Email con Attachments

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os

def create_message_with_attachments(
    sender: str,
    to: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    attachments: List[str] = None
) -> dict:
    """
    Crea messaggio Gmail con attachments.

    Args:
        sender: Email mittente
        to: Email destinatario (comma separated per multipli)
        subject: Oggetto email
        body_text: Corpo testo plain
        body_html: Corpo HTML (opzionale)
        attachments: Lista path file da allegare

    Returns:
        Dict pronto per Gmail API send
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Corpo email (plain + html se presente)
    if body_html:
        msg_alternative = MIMEMultipart('alternative')
        msg_alternative.attach(MIMEText(body_text, 'plain'))
        msg_alternative.attach(MIMEText(body_html, 'html'))
        message.attach(msg_alternative)
    else:
        message.attach(MIMEText(body_text, 'plain'))

    # Attachments
    if attachments:
        for filepath in attachments:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")

            # Detect MIME type
            content_type, _ = mimetypes.guess_type(filepath)
            if content_type is None:
                content_type = 'application/octet-stream'

            main_type, sub_type = content_type.split('/', 1)

            # Leggi e allega file
            with open(filepath, 'rb') as f:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(f.read())

            # Encode base64
            encoders.encode_base64(msg)

            # Header attachment
            filename = os.path.basename(filepath)
            msg.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename
            )

            message.attach(msg)

    # Encode per Gmail API
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {'raw': raw_message}


async def send_email_with_attachments(
    service,
    sender: str,
    to: str,
    subject: str,
    body: str,
    attachments: List[str] = None
) -> dict:
    """
    Invia email con attachments via Gmail API.

    Returns:
        Response Gmail API con message ID
    """
    message = create_message_with_attachments(
        sender=sender,
        to=to,
        subject=subject,
        body_text=body,
        attachments=attachments or []
    )

    try:
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        return sent_message

    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")
```

---

## 3. INTEGRAZIONE FASTAPI

### 3.1 Endpoint: Lista Attachments

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/emails", tags=["emails"])

class AttachmentMetadata(BaseModel):
    attachmentId: str
    filename: str
    mimeType: str
    size: int
    isInline: bool

@router.get("/{message_id}/attachments", response_model=List[AttachmentMetadata])
async def get_message_attachments(
    message_id: str,
    gmail_service = Depends(get_gmail_service)  # Tuo dependency
):
    """
    Ottiene lista attachments di un messaggio.

    NOTA: Questa è veloce - metadata già nel message payload!
    """
    try:
        # Fetch message (se non già in cache)
        message = gmail_service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'  # Serve 'full' per avere parts
        ).execute()

        # Estrai metadata
        attachments = extract_attachments_metadata(message)

        return attachments

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching attachments: {str(e)}"
        )
```

### 3.2 Endpoint: Download Attachment (STREAMING)

```python
from fastapi.responses import StreamingResponse
import io

@router.get("/{message_id}/attachments/{attachment_id}/download")
async def download_attachment_endpoint(
    message_id: str,
    attachment_id: str,
    gmail_service = Depends(get_gmail_service)
):
    """
    Download attachment con streaming per efficienza memoria.

    BEST PRACTICE:
    - Non carica tutto in memoria
    - Usa StreamingResponse per file grandi
    - Client riceve progressivamente
    """
    try:
        # Ottieni metadata per filename e MIME type
        message = gmail_service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        # Trova attachment nei parts
        attachment_info = None
        def find_attachment(parts):
            nonlocal attachment_info
            if not parts:
                return
            for part in parts:
                if part.get('parts'):
                    find_attachment(part.get('parts'))
                body = part.get('body', {})
                if body.get('attachmentId') == attachment_id:
                    attachment_info = {
                        'filename': part.get('filename', 'attachment'),
                        'mimeType': part.get('mimeType', 'application/octet-stream')
                    }
                    return

        find_attachment(message.get('payload', {}).get('parts'))

        if not attachment_info:
            raise HTTPException(status_code=404, detail="Attachment not found")

        # Download attachment
        file_data = await download_attachment(
            gmail_service,
            message_id,
            attachment_id
        )

        # Stream response
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=attachment_info['mimeType'],
            headers={
                'Content-Disposition': f'attachment; filename="{attachment_info["filename"]}"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading attachment: {str(e)}"
        )
```

### 3.3 Endpoint: Upload & Send Email

```python
from fastapi import UploadFile, File, Form
from typing import Optional
import tempfile
import os

@router.post("/send")
async def send_email_endpoint(
    to: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    gmail_service = Depends(get_gmail_service),
    current_user = Depends(get_current_user)
):
    """
    Invia email con attachments.

    BEST PRACTICE:
    - Usa UploadFile per async handling
    - Salva temporaneamente file su disco
    - Cleanup dopo invio
    - Valida dimensioni PRIMA di processare
    """
    temp_files = []

    try:
        # Valida dimensione totale
        total_size = 0
        if files:
            for file in files:
                file_content = await file.read()
                total_size += len(file_content)
                await file.seek(0)  # Reset per riutilizzo

        # Limite 20MB (lascia margine per encoding)
        MAX_SIZE = 20 * 1024 * 1024
        if total_size > MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Total attachments size ({total_size} bytes) exceeds 20MB limit"
            )

        # Salva files temporaneamente
        if files:
            for file in files:
                # Crea file temporaneo
                suffix = os.path.splitext(file.filename)[1]
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                )

                # Scrivi contenuto
                content = await file.read()
                temp_file.write(content)
                temp_file.close()

                temp_files.append(temp_file.name)

        # Invia email
        result = await send_email_with_attachments(
            service=gmail_service,
            sender=current_user.email,
            to=to,
            subject=subject,
            body=body,
            attachments=temp_files if temp_files else None
        )

        return {
            'success': True,
            'messageId': result['id'],
            'attachmentCount': len(temp_files)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending email: {str(e)}"
        )
    finally:
        # Cleanup files temporanei
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
```

---

## 4. STRUTTURA DATI FRONTEND

### 4.1 TypeScript Interfaces

```typescript
// Metadata attachment (dalla lista)
interface EmailAttachment {
  attachmentId: string;
  filename: string;
  mimeType: string;
  size: number;
  isInline: boolean;
  messageId: string;
}

// Attachment con preview
interface AttachmentWithPreview extends EmailAttachment {
  previewUrl?: string;  // Blob URL per preview locale
  downloadUrl: string;   // URL endpoint backend
  iconType: 'image' | 'pdf' | 'document' | 'archive' | 'other';
}

// Response lista attachments
interface AttachmentsResponse {
  attachments: EmailAttachment[];
  totalSize: number;
}
```

### 4.2 Helper Functions Frontend

```typescript
// Determina icona da mostrare
function getAttachmentIcon(mimeType: string): 'image' | 'pdf' | 'document' | 'archive' | 'other' {
  if (mimeType.startsWith('image/')) return 'image';
  if (mimeType === 'application/pdf') return 'pdf';
  if (mimeType.includes('word') || mimeType.includes('document')) return 'document';
  if (mimeType.includes('zip') || mimeType.includes('archive')) return 'archive';
  return 'other';
}

// Formatta dimensione file
function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Download attachment
async function downloadAttachment(
  messageId: string,
  attachmentId: string,
  filename: string
) {
  const url = `/api/emails/${messageId}/attachments/${attachmentId}/download`;

  const response = await fetch(url);
  const blob = await response.blob();

  // Trigger download browser
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = filename;
  link.click();

  // Cleanup
  window.URL.revokeObjectURL(link.href);
}

// Preview immagine
async function previewImage(
  messageId: string,
  attachmentId: string
): Promise<string> {
  const url = `/api/emails/${messageId}/attachments/${attachmentId}/download`;

  const response = await fetch(url);
  const blob = await response.blob();

  // Crea blob URL per <img>
  return window.URL.createObjectURL(blob);
}
```

---

## 5. BEST PRACTICES

### 5.1 Performance

**DO:**
- Cache attachment metadata nel message object
- Download on-demand (solo quando utente clicca)
- Usa StreamingResponse per file > 1MB
- Implementa lazy loading per email con molti attachments

**DON'T:**
- Pre-download tutti gli attachments
- Caricare intero file in memoria lato backend
- Fetch metadata con chiamate separate se già nel payload

### 5.2 Security

**Validazioni Necessarie:**

```python
# Backend validation
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
}

def validate_attachment(filename: str, mime_type: str, size: int):
    # Size limit
    if size > 20 * 1024 * 1024:  # 20MB
        raise ValueError("File too large")

    # MIME type whitelist
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"File type not allowed: {mime_type}")

    # Filename sanitization
    import re
    if not re.match(r'^[\w\-. ]+$', filename):
        raise ValueError("Invalid filename")
```

**Virus Scanning:**
- Per upload hotel, considera integrazione ClamAV
- Scansione async in background
- Flag email con attachments suspicious

### 5.3 UX Considerations

**Preview per Immagini:**
```python
# Endpoint thumbnails (opzionale)
@router.get("/{message_id}/attachments/{attachment_id}/thumbnail")
async def get_thumbnail(message_id: str, attachment_id: str):
    """
    Genera thumbnail 200x200 per preview veloce.
    Usa PIL/Pillow per resize.
    """
    file_data = await download_attachment(...)

    from PIL import Image
    import io

    img = Image.open(io.BytesIO(file_data))
    img.thumbnail((200, 200))

    thumb_io = io.BytesIO()
    img.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    return StreamingResponse(thumb_io, media_type='image/jpeg')
```

**Indicatori Progresso:**
- Mostra spinner durante download
- Progress bar per upload file grandi
- Timeout 30s per operazioni attachment

### 5.4 Caching Strategy

```python
# Redis cache per metadata
import redis
import json

cache = redis.Redis(host='localhost', port=6379, db=0)

async def get_attachments_cached(message_id: str):
    # Check cache
    cache_key = f"attachments:{message_id}"
    cached = cache.get(cache_key)

    if cached:
        return json.loads(cached)

    # Fetch da API
    attachments = extract_attachments_metadata(message)

    # Cache 1 hour
    cache.setex(cache_key, 3600, json.dumps(attachments))

    return attachments
```

---

## 6. TESTING

### 6.1 Test Cases Critici

```python
import pytest
from fastapi.testclient import TestClient

def test_download_attachment_success():
    """Test download attachment esistente"""
    response = client.get("/api/emails/msg123/attachments/att456/download")
    assert response.status_code == 200
    assert response.headers['content-disposition'].startswith('attachment')

def test_download_attachment_not_found():
    """Test attachment inesistente"""
    response = client.get("/api/emails/msg123/attachments/invalid/download")
    assert response.status_code == 404

def test_send_email_size_limit():
    """Test limite dimensione"""
    large_file = b'x' * (25 * 1024 * 1024)  # 25MB

    response = client.post(
        "/api/emails/send",
        data={'to': 'test@test.com', 'subject': 'Test', 'body': 'Test'},
        files={'files': ('large.bin', large_file)}
    )
    assert response.status_code == 413

def test_attachment_metadata_extraction():
    """Test parsing attachment da payload"""
    message = {
        'id': 'msg123',
        'payload': {
            'parts': [
                {
                    'filename': 'test.pdf',
                    'mimeType': 'application/pdf',
                    'body': {
                        'attachmentId': 'att123',
                        'size': 12345
                    },
                    'headers': [
                        {'name': 'Content-Disposition', 'value': 'attachment'}
                    ]
                }
            ]
        }
    }

    attachments = extract_attachments_metadata(message)
    assert len(attachments) == 1
    assert attachments[0]['filename'] == 'test.pdf'
    assert attachments[0]['isInline'] == False
```

---

## 7. DEPLOYMENT CONSIDERATIONS

### 7.1 Variabili Ambiente

```bash
# .env
MAX_ATTACHMENT_SIZE_MB=20
ENABLE_VIRUS_SCAN=false
THUMBNAIL_CACHE_TTL=3600
TEMP_FILE_DIR=/tmp/miracollook
```

### 7.2 Monitoring

**Metriche da tracciare:**
- Attachment download latency
- Upload success/failure rate
- Average attachment size
- Cache hit rate
- Virus scan detections

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

attachment_downloads = Counter(
    'attachment_downloads_total',
    'Total attachment downloads',
    ['status']
)

attachment_download_duration = Histogram(
    'attachment_download_duration_seconds',
    'Attachment download duration'
)
```

---

## 8. ROADMAP IMPLEMENTAZIONE

### Fase 1: MVP (1-2 giorni)
- [ ] Backend: Endpoint lista attachments
- [ ] Backend: Endpoint download singolo attachment
- [ ] Frontend: Mostra lista attachments in email view
- [ ] Frontend: Click per download

### Fase 2: Upload (1 giorno)
- [ ] Backend: Endpoint send con files
- [ ] Frontend: File picker in compose
- [ ] Validazione dimensioni
- [ ] Preview files prima invio

### Fase 3: Enhancements (opzionale)
- [ ] Thumbnail per immagini
- [ ] Preview PDF inline
- [ ] Drag & drop upload
- [ ] Progress indicators
- [ ] Virus scanning

---

## 9. CODICE COMPLETO ESEMPIO

### Backend Service Layer

```python
# services/gmail_attachments.py

from typing import List, Dict, Optional
import base64
import os
import tempfile
from googleapiclient.discovery import Resource

class GmailAttachmentService:
    """Service per gestione attachments Gmail API"""

    def __init__(self, gmail_service: Resource):
        self.service = gmail_service

    def get_message_attachments(self, message_id: str) -> List[Dict]:
        """Ottiene lista attachments da messaggio"""
        message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        return self._extract_attachments(message)

    def _extract_attachments(self, message: dict) -> List[Dict]:
        """Estrae metadata attachments da payload"""
        attachments = []

        def parse_parts(parts):
            if not parts:
                return

            for part in parts:
                if part.get('parts'):
                    parse_parts(part.get('parts'))

                filename = part.get('filename')
                body = part.get('body', {})
                attachment_id = body.get('attachmentId')

                if attachment_id and filename:
                    is_inline = self._is_inline_attachment(part)

                    attachments.append({
                        'attachmentId': attachment_id,
                        'filename': filename,
                        'mimeType': part.get('mimeType'),
                        'size': body.get('size', 0),
                        'isInline': is_inline,
                        'messageId': message.get('id')
                    })

        payload = message.get('payload', {})
        parse_parts(payload.get('parts'))

        return attachments

    def _is_inline_attachment(self, part: dict) -> bool:
        """Determina se attachment è inline"""
        headers = part.get('headers', [])
        for header in headers:
            if header.get('name') == 'Content-Disposition':
                return 'inline' in header.get('value', '').lower()
        return False

    def download_attachment(
        self,
        message_id: str,
        attachment_id: str
    ) -> bytes:
        """Download attachment data"""
        attachment = self.service.users().messages().attachments().get(
            userId='me',
            messageId=message_id,
            id=attachment_id
        ).execute()

        data = attachment.get('data')
        if not data:
            raise ValueError("No data in attachment")

        return base64.urlsafe_b64decode(data)

    def send_with_attachments(
        self,
        to: str,
        subject: str,
        body: str,
        sender: str,
        attachment_paths: Optional[List[str]] = None
    ) -> dict:
        """Invia email con attachments"""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        import mimetypes

        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        if attachment_paths:
            for filepath in attachment_paths:
                content_type, _ = mimetypes.guess_type(filepath)
                if not content_type:
                    content_type = 'application/octet-stream'

                main_type, sub_type = content_type.split('/', 1)

                with open(filepath, 'rb') as f:
                    msg = MIMEBase(main_type, sub_type)
                    msg.set_payload(f.read())

                encoders.encode_base64(msg)

                filename = os.path.basename(filepath)
                msg.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=filename
                )

                message.attach(msg)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        return self.service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
```

### Frontend Component (React + TypeScript)

```typescript
// components/AttachmentList.tsx

import React from 'react';

interface Attachment {
  attachmentId: string;
  filename: string;
  mimeType: string;
  size: number;
  isInline: boolean;
}

interface Props {
  messageId: string;
  attachments: Attachment[];
}

export const AttachmentList: React.FC<Props> = ({ messageId, attachments }) => {
  const downloadAttachment = async (att: Attachment) => {
    const url = `/api/emails/${messageId}/attachments/${att.attachmentId}/download`;

    try {
      const response = await fetch(url);
      const blob = await response.blob();

      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = att.filename;
      link.click();

      window.URL.revokeObjectURL(link.href);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Errore durante il download');
    }
  };

  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const getIcon = (mimeType: string): string => {
    if (mimeType.startsWith('image/')) return '🖼️';
    if (mimeType === 'application/pdf') return '📄';
    if (mimeType.includes('word')) return '📝';
    return '📎';
  };

  // Non mostrare inline images
  const displayAttachments = attachments.filter(att => !att.isInline);

  if (displayAttachments.length === 0) {
    return null;
  }

  return (
    <div className="attachments-list">
      <h4>Allegati ({displayAttachments.length})</h4>
      <ul>
        {displayAttachments.map(att => (
          <li key={att.attachmentId} className="attachment-item">
            <span className="icon">{getIcon(att.mimeType)}</span>
            <span className="filename">{att.filename}</span>
            <span className="size">{formatSize(att.size)}</span>
            <button onClick={() => downloadAttachment(att)}>
              Download
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};
```

---

## RACCOMANDAZIONE FINALE

### Implementazione Suggerita per Miracollook

**STACK:**
- Backend: FastAPI + funzioni Python custom (no librerie extra)
- Gmail API: Chiamate dirette con `google-api-python-client`
- Storage: Temporaneo su disco per upload, no persistenza attachments
- Frontend: React component dedicato per attachments view

**PRIORITA:**
1. **SUBITO**: Lista + download attachments
2. **DOPO**: Upload in compose
3. **OPZIONALE**: Preview, thumbnails

**VANTAGGI APPROCCIO:**
- Zero dipendenze extra
- Pieno controllo logica business
- Streaming efficiente memoria
- Facile testing

**STIMA EFFORT:**
- Lista/Download: 4-6 ore
- Upload: 3-4 ore
- Testing: 2 ore
- **TOTALE: 1-2 giorni development**

---

## FONTI DOCUMENTAZIONE

### Documentazione Ufficiale
- [Gmail API Attachments Reference](https://developers.google.com/gmail/api/reference/rest/v1/users.messages.attachments/get)
- [Gmail API Uploading Attachments](https://developers.google.com/gmail/api/guides/uploads)
- [Gmail API Sending Email](https://developers.google.com/gmail/api/guides/sending)

### Tutorial e Guide
- [How to Use Gmail API in Python - The Python Code](https://thepythoncode.com/article/use-gmail-api-in-python)
- [Gmail API Send Email with Attachments - Learn Data Analysis](https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-with-attachments-in-python/)
- [Gmail API MIME Types Structure](https://www.ehfeng.com/gmail-api-mime-types/)

### Best Practices FastAPI
- [FastAPI File Upload Documentation](https://fastapi.tiangolo.com/tutorial/request-files/)
- [Streaming File Downloads FastAPI](https://python.plainenglish.io/streaming-file-uploads-and-downloads-with-fastapi-a-practical-guide-ee5be38fdd66)
- [FastAPI File Uploads Best Practices](https://davidmuraya.com/blog/fastapi-file-uploads/)

### Limiti e Specifiche
- [Gmail Attachment Size Limit 2026](https://emailanalytics.com/gmail-attachment-size-limit/)
- [Gmail API Upload Methods](https://developers.google.com/gmail/api/guides/uploads)

---

**Fine Ricerca**

Report completo salvato in: `.sncp/progetti/miracollo/moduli/miracallook/studi/RICERCA_GMAIL_ATTACHMENTS.md`

Pronta per implementazione! 🔬
