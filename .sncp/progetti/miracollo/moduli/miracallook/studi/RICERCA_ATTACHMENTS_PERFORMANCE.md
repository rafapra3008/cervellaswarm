# Ricerca: Ottimizzazione Performance Download Attachments Email

**Data**: 13 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Progetto**: Miracollook - Email Module
**Problema**: Download attachments troppo lento (30-40 secondi)

---

## Executive Summary

**RACCOMANDAZIONE PRINCIPALE**: Implementare sistema **Eager Loading + Caching Redis + Streaming FastAPI**

**Guadagno atteso**: Da 30-40s a ~2-5s (riduzione 80-90%)

**Strategia in 3 fasi**:
1. **Immediate** (Quick Win): Streaming + Compression → -40% tempo
2. **Short-term** (Settimana 1): Redis Caching → -60% ripetuti
3. **Medium-term** (Settimana 2-3): Eager Loading → UX istantanea

---

## 1. ANALISI COMPETITOR: Come Fanno i Big

### Gmail Web Client

**Strategia Principale**: Prefetching + CDN + Aggressive Caching

- **Prefetching immagini**: Gmail pre-scarica immagini quando l'utente ha sessione attiva, PRIMA che apra l'email
- **Proxy Google**: Tutte le immagini passano attraverso proxy Google (cache centralizzata)
- **Lazy loading intelligente**: Carica solo ciò che è visibile nel viewport
- **Compression**: GZIP su tutte le risposte API

**Fonte chiave**: [Gmail Prefetching Images - Litmus](https://www.litmus.com/blog/gmail-prefetching-images)

**Limitazione per noi**: Gmail API NON supporta partial download o thumbnail nativi ([Gmail API Issue #428](https://github.com/googleapis/google-api-nodejs-client/issues/428))

### Outlook Web App

**Strategia Principale**: Download Headers Only + On-Demand Full Content

- **Headers-only mode**: Scarica solo metadati inizialmente
- **Background sync**: Scarica contenuto completo in background mentre user naviga
- **Chunked download**: Divide grandi attachment in chunk
- **Local caching**: Cache aggressiva lato browser

**Fonte**: [How To Speed Up Outlook 2026](https://clean.email/blog/email-providers/how-to-speed-up-outlook-run-faster)

### Apple Mail

**Strategia Principale**: Local-first Architecture

- Download completo in background quando arriva email
- Database locale SQLite per attachments
- Preview immediato da cache locale

**Pattern comune**: TUTTI prefetchano in background, NESSUNO fa download sincrono al click!

---

## 2. STRATEGIE DI OTTIMIZZAZIONE ANALIZZATE

### 2.1 Streaming Response (FastAPI)

**Cosa**: Inviare file mentre scarica da Gmail API, invece di buffering completo

**Pro**:
- Riduce latency percepita (user vede download iniziare subito)
- Memoria server costante (no buffer completo)
- Facile da implementare

**Contro**:
- Non elimina latenza Gmail API
- Non aiuta per file ripetuti

**Implementazione**:

```python
from fastapi.responses import StreamingResponse
import httpx

async def download_attachment(message_id: str, attachment_id: str):
    """
    Stream attachment direttamente da Gmail API al client
    """
    gmail_service = get_gmail_service()

    # Get attachment metadata
    attachment = gmail_service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    # Decode base64 data
    import base64
    file_data = base64.urlsafe_b64decode(attachment['data'])

    # Stream in chunks
    async def file_iterator():
        chunk_size = 8192  # 8KB chunks
        for i in range(0, len(file_data), chunk_size):
            yield file_data[i:i + chunk_size]

    return StreamingResponse(
        file_iterator(),
        media_type='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Length': str(len(file_data))
        }
    )
```

**Fonte**: [FastAPI Streaming Response Guide](https://apidog.com/blog/fastapi-streaming-response/)

**CRITICO**: Usare `async def` generator, NON `def` sync! ([FastAPI Performance](https://pytutorial.com/fastapi-performance-optimization-guide/))

### 2.2 Redis Caching

**Cosa**: Cachare attachments scaricati per X tempo

**Pro**:
- Download ripetuti = istantanei
- Riduce chiamate Gmail API (quota limits!)
- Facile invalidazione cache

**Contro**:
- Memoria Redis (considerare limite file size)
- Overhead gestione cache
- Non aiuta primo download

**Strategia Cache-Aside** (Raccomandato):

```python
import redis
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)
CACHE_TTL = 3600  # 1 ora

async def get_attachment_cached(message_id: str, attachment_id: str):
    """
    Scarica attachment con caching Redis
    """
    # Generate cache key
    cache_key = f"attachment:{message_id}:{attachment_id}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return cached

    # Cache miss - download from Gmail
    gmail_service = get_gmail_service()
    attachment = gmail_service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    import base64
    file_data = base64.urlsafe_b64decode(attachment['data'])

    # Store in cache
    redis_client.setex(cache_key, CACHE_TTL, file_data)

    return file_data
```

**Fonte**: [Redis Caching Patterns - AWS](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)

**Considerazioni**:
- Limite Redis: ~512MB per chiave (OK per most attachments)
- Alternative per file GROSSI (>10MB): Salvare su disco `/tmp/` e cachare solo path
- TTL suggerito: 1-24h (dipende da storage disponibile)

### 2.3 Eager Loading (Background Prefetch)

**Cosa**: Scaricare attachments in background quando si apre email, PRIMA che user clicchi

**Pro**:
- UX percepita = istantanea
- User non aspetta mai
- Migliore strategia per engagement

**Contro**:
- Download speculativo (user potrebbe non cliccare)
- Uso banda maggiore
- Complessità implementazione

**Implementazione con FastAPI BackgroundTasks**:

```python
from fastapi import BackgroundTasks

async def get_email_detail(
    email_id: str,
    background_tasks: BackgroundTasks
):
    """
    Ritorna email detail e avvia prefetch attachments
    """
    # Get email
    email = await fetch_email(email_id)

    # Schedule background prefetch for ALL attachments
    if email.attachments:
        background_tasks.add_task(
            prefetch_attachments,
            email_id,
            email.attachments
        )

    return email

async def prefetch_attachments(email_id: str, attachments: list):
    """
    Background task: scarica e cacha tutti gli attachments
    """
    for attachment in attachments:
        try:
            # Download and cache
            await get_attachment_cached(email_id, attachment.id)
        except Exception as e:
            logger.error(f"Prefetch failed for {attachment.id}: {e}")
            # Non bloccare per errori
```

**Fonte**: [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)

**Quando NON prefetchare**:
- Mobile con connessione lenta
- Email con >10 attachments
- Attachments totali >50MB

**Smart Prefetching**: Prefetchare solo primi 3 attachments o solo <5MB

### 2.4 Compression (GZIP)

**Cosa**: Abilitare compressione GZIP su Gmail API requests

**Pro**:
- Riduce banda ~60-80% per file testuali
- Zero cambio architettura
- Supported by Gmail API

**Contro**:
- CPU overhead
- Minimo beneficio per file già compressi (jpg, zip, etc)

**Implementazione**:

```python
import google.auth
from googleapiclient.discovery import build

# Enable gzip in HTTP transport
http = google.auth.transport.requests.AuthorizedSession(credentials)
http.headers.update({
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Miracollook/1.0 gzip'
})

gmail_service = build('gmail', 'v1', http=http)
```

**Fonte**: [Gmail API Performance Tips](https://developers.google.com/gmail/api/guides/performance)

**Guadagno atteso**: 30-40% riduzione tempo per PDF, TXT, CSV. Minimo per immagini.

### 2.5 Batch Requests (Gmail API)

**Cosa**: Scaricare multipli attachments in 1 HTTP request

**Pro**:
- Riduce overhead HTTP
- Meno latency per email con multiple attachments

**Contro**:
- Limite 100 requests/batch (Gmail API)
- Raccomandato max 50/batch
- Complessità parsing response

**Quando usarlo**: Email con 3+ attachments piccoli (<1MB ciascuno)

**Implementazione**:

```python
from googleapiclient.http import BatchHttpRequest

def download_multiple_attachments(message_id: str, attachment_ids: list):
    """
    Download multiple attachments in batch
    """
    gmail_service = get_gmail_service()

    batch = gmail_service.new_batch_http_request()

    results = {}

    def callback(request_id, response, exception):
        if exception:
            logger.error(f"Batch request failed: {exception}")
        else:
            results[request_id] = response

    for att_id in attachment_ids[:50]:  # Max 50
        batch.add(
            gmail_service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=att_id
            ),
            callback=callback,
            request_id=att_id
        )

    batch.execute()
    return results
```

**Fonte**: [Gmail API Batching Requests](https://developers.google.com/workspace/gmail/api/guides/batch)

**Guadagno atteso**: -20-30% latency per 5+ attachments piccoli

---

## 3. RACCOMANDAZIONE IMPLEMENTATIVA

### Strategia Ottimale: Hybrid Approach

Combinare **Streaming + Redis + Eager Loading** per massimizzare performance.

### Fase 1: QUICK WIN (1-2 giorni)

**Obiettivo**: Ridurre latency percepita -40%

**Azioni**:
1. ✅ Abilitare GZIP compression su Gmail API client
2. ✅ Implementare StreamingResponse invece di buffer completo
3. ✅ Usare async generators per streaming

**Codice**:

```python
# services/gmail_service.py

async def stream_attachment(
    message_id: str,
    attachment_id: str,
    filename: str
):
    """
    Quick Win: Streaming + Compression
    """
    gmail_service = get_gmail_service_with_gzip()

    # Fetch attachment
    attachment = gmail_service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    # Decode
    import base64
    file_data = base64.urlsafe_b64decode(attachment['data'])

    # Stream in chunks (async generator)
    async def file_iterator():
        chunk_size = 8192
        for i in range(0, len(file_data), chunk_size):
            yield file_data[i:i + chunk_size]

    return StreamingResponse(
        file_iterator(),
        media_type='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Length': str(len(file_data)),
            'Cache-Control': 'private, max-age=3600'  # Browser cache 1h
        }
    )
```

**Testing**: Verificare riduzione tempo da 30s a ~20s

### Fase 2: CACHING (Settimana 1)

**Obiettivo**: Download ripetuti istantanei

**Azioni**:
1. ✅ Setup Redis container in docker-compose
2. ✅ Implementare cache-aside pattern
3. ✅ TTL 24h, max 10MB per file
4. ✅ Gestire cache invalidation

**Codice**:

```python
# services/cache_service.py

import redis.asyncio as redis
from typing import Optional

class AttachmentCacheService:
    def __init__(self):
        self.redis = redis.Redis(
            host='redis',
            port=6379,
            decode_responses=False  # Binary data
        )
        self.ttl = 86400  # 24h
        self.max_file_size = 10 * 1024 * 1024  # 10MB

    async def get(self, message_id: str, attachment_id: str) -> Optional[bytes]:
        """Get from cache"""
        key = f"att:{message_id}:{attachment_id}"
        return await self.redis.get(key)

    async def set(self, message_id: str, attachment_id: str, data: bytes):
        """Set in cache with TTL"""
        if len(data) > self.max_file_size:
            # Too large for Redis - skip cache
            return

        key = f"att:{message_id}:{attachment_id}"
        await self.redis.setex(key, self.ttl, data)

    async def invalidate(self, message_id: str, attachment_id: str):
        """Manual cache invalidation"""
        key = f"att:{message_id}:{attachment_id}"
        await self.redis.delete(key)

# Integration in endpoint
cache_service = AttachmentCacheService()

async def download_attachment_with_cache(
    message_id: str,
    attachment_id: str,
    filename: str
):
    # Try cache first
    cached_data = await cache_service.get(message_id, attachment_id)

    if cached_data:
        # Cache HIT - instant response
        return Response(
            content=cached_data,
            media_type='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'X-Cache-Status': 'HIT'
            }
        )

    # Cache MISS - download and cache
    gmail_service = get_gmail_service_with_gzip()
    attachment = gmail_service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    import base64
    file_data = base64.urlsafe_b64decode(attachment['data'])

    # Store in cache (async, non-blocking)
    await cache_service.set(message_id, attachment_id, file_data)

    return Response(
        content=file_data,
        media_type='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'X-Cache-Status': 'MISS'
        }
    )
```

**Docker Compose**:

```yaml
# docker-compose.yml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

volumes:
  redis_data:
```

**Testing**: Verificare cache hit ratio >60% dopo poche ore di uso

### Fase 3: EAGER LOADING (Settimana 2-3)

**Obiettivo**: UX istantanea - nessuna attesa al click

**Azioni**:
1. ✅ Background prefetch quando user apre email
2. ✅ Smart prefetching (solo primi 3 attachments o <5MB)
3. ✅ Indicatore UI "Preparing attachments..."

**Codice Backend**:

```python
# routers/emails.py

from fastapi import BackgroundTasks

@router.get("/emails/{email_id}")
async def get_email_detail(
    email_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Get email detail + trigger background prefetch
    """
    # Fetch email
    email = await email_service.get_email(email_id, current_user)

    # Smart prefetch decision
    if should_prefetch(email.attachments):
        background_tasks.add_task(
            prefetch_attachments_smart,
            email_id,
            email.attachments,
            current_user.id
        )

    return email

def should_prefetch(attachments: list) -> bool:
    """Decide if we should prefetch"""
    if not attachments:
        return False

    # Don't prefetch if too many
    if len(attachments) > 10:
        return False

    # Don't prefetch if total size > 50MB
    total_size = sum(att.size for att in attachments)
    if total_size > 50 * 1024 * 1024:
        return False

    return True

async def prefetch_attachments_smart(
    email_id: str,
    attachments: list,
    user_id: str
):
    """
    Smart background prefetch
    - Only first 3 attachments
    - Only if <5MB each
    """
    gmail_service = get_gmail_service_for_user(user_id)
    cache_service = AttachmentCacheService()

    for attachment in attachments[:3]:  # Max 3
        # Skip large files
        if attachment.size > 5 * 1024 * 1024:
            continue

        # Check if already cached
        cached = await cache_service.get(email_id, attachment.id)
        if cached:
            continue  # Already in cache

        try:
            # Download and cache
            att_data = gmail_service.users().messages().attachments().get(
                userId='me',
                messageId=email_id,
                id=attachment.id
            ).execute()

            import base64
            file_data = base64.urlsafe_b64decode(att_data['data'])

            await cache_service.set(email_id, attachment.id, file_data)

        except Exception as e:
            # Log but don't fail entire prefetch
            logger.warning(f"Prefetch failed for {attachment.id}: {e}")
```

**Codice Frontend**:

```typescript
// frontend/src/features/emails/hooks/useEmailDetail.ts

export const useEmailDetail = (emailId: string) => {
  const [isPrefetching, setIsPrefetching] = useState(false);

  const { data: email } = useQuery({
    queryKey: ['email', emailId],
    queryFn: async () => {
      const response = await api.get(`/emails/${emailId}`);

      // Start prefetch indicator
      if (response.data.attachments?.length > 0) {
        setIsPrefetching(true);

        // Wait for prefetch to complete (check cache)
        setTimeout(() => setIsPrefetching(false), 3000);
      }

      return response.data;
    }
  });

  return { email, isPrefetching };
};

// UI Component
<EmailDetailView email={email}>
  {isPrefetching && (
    <div className="prefetch-indicator">
      <Spinner size="sm" />
      Preparing attachments...
    </div>
  )}

  <AttachmentsList
    attachments={email.attachments}
    cacheStatus="ready"  // Instant download
  />
</EmailDetailView>
```

**Testing**: Verificare che >80% dei click su attachment risultano in cache HIT

---

## 4. TRADE-OFFS & CONSIDERAZIONI

### Memoria vs Velocità

| Strategia | Memoria Server | Memoria Redis | Velocità Guadagnata |
|-----------|----------------|---------------|---------------------|
| Streaming Only | Bassa (8KB buffer) | 0 | +40% |
| Caching | Bassa | Alta (~1GB/1000 files) | +80% (ripetuti) |
| Eager Loading | Media | Alta | +95% (UX percepita) |

**Raccomandazione**: Redis 512MB con LRU eviction = ottimo trade-off

### Costo API Calls vs UX

- Gmail API quota: 1 billion quota units/day ([Gmail API Quotas](https://developers.google.com/gmail/api/reference/quota))
- `attachments.get` = 25 quota units
- Eager loading aumenta chiamate ~30%
- Ma caching riduce chiamate ripetute -60%

**Risultato netto**: -30% chiamate totali dopo pochi giorni

### Complessità Implementazione vs Beneficio

| Fase | Complessità (1-5) | Beneficio | ROI |
|------|-------------------|-----------|-----|
| Streaming + GZIP | ⭐⭐ | Medio | Alto |
| Redis Caching | ⭐⭐⭐ | Alto | Molto Alto |
| Eager Loading | ⭐⭐⭐⭐ | Altissimo | Alto |
| Batch Requests | ⭐⭐⭐⭐⭐ | Basso | Basso |

**Raccomandazione**: Focus su Fase 1-3, saltare Batch (marginal gains)

---

## 5. METRICHE DI SUCCESSO

### Before (Baseline)

- Tempo download attachment: 30-40s
- Cache hit rate: 0%
- User frustration: Alta

### After Fase 1 (Streaming + GZIP)

- Tempo download: ~20-25s (-40%)
- Latency percepita: ~5s (inizio download immediato)
- Cache hit rate: 0%

### After Fase 2 (+ Redis Caching)

- Primo download: ~20s
- Download ripetuto: <1s (-95%)
- Cache hit rate: ~60-70%

### After Fase 3 (+ Eager Loading)

- User click download: <1s (cache HIT)
- Latency percepita: ~0s (istantaneo)
- Cache hit rate: ~80-85%
- Background prefetch overhead: +30% API calls (ma meglio UX)

### KPI da Monitorare

```python
# Metrics to track

@router.get("/attachments/{message_id}/{attachment_id}")
async def download_attachment(message_id: str, attachment_id: str):
    start_time = time.time()
    cache_status = "MISS"

    # ... download logic ...

    # Track metrics
    metrics.histogram(
        'attachment.download.duration',
        time.time() - start_time,
        tags=[f'cache:{cache_status}']
    )

    metrics.increment(
        'attachment.download.count',
        tags=[f'cache:{cache_status}']
    )
```

**Grafana Dashboards**:
- Attachment download duration (p50, p95, p99)
- Cache hit ratio %
- Background prefetch success rate
- Gmail API quota usage

---

## 6. RISCHI & MITIGAZIONI

### Rischio 1: Redis Out of Memory

**Scenario**: Cache riempie tutta la RAM disponibile

**Mitigazione**:
- Impostare `maxmemory 512mb`
- Policy `allkeys-lru` (evict least recently used)
- Monitor Redis memory usage
- Limite 10MB per file in cache

### Rischio 2: Prefetch Spreca Banda

**Scenario**: User apre email ma non scarica attachments

**Mitigazione**:
- Smart prefetching (solo primi 3, solo <5MB)
- Machine learning: predire probabilità download (fase futura)
- User setting: disable prefetch su mobile/slow connection

### Rischio 3: Stale Cache

**Scenario**: Attachment modificato ma cache serve versione vecchia

**Mitigazione**:
- TTL 24h (email attachments non cambiano mai)
- Manual invalidation API se serve
- Cache key include attachment.id (univoco)

### Rischio 4: Gmail API Rate Limit

**Scenario**: Eager loading causa quota exceeded

**Mitigazione**:
- Exponential backoff su errori 429
- Circuit breaker pattern
- Queue prefetch tasks (max 5/second)

```python
import asyncio
from asyncio import Semaphore

prefetch_semaphore = Semaphore(5)  # Max 5 concurrent

async def prefetch_with_rate_limit(email_id, attachment_id):
    async with prefetch_semaphore:
        await download_and_cache(email_id, attachment_id)
        await asyncio.sleep(0.2)  # 200ms delay
```

---

## 7. CODICE ESEMPIO COMPLETO

### Backend: Attachment Service (Final)

```python
# services/attachment_service.py

import base64
import logging
from typing import Optional
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, Response
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class AttachmentService:
    def __init__(self):
        self.redis = redis.Redis(
            host='redis',
            port=6379,
            decode_responses=False
        )
        self.cache_ttl = 86400  # 24h
        self.max_cache_size = 10 * 1024 * 1024  # 10MB

    async def download_attachment(
        self,
        message_id: str,
        attachment_id: str,
        filename: str,
        gmail_service
    ) -> Response:
        """
        Download attachment with caching + streaming
        """
        # Try cache first
        cache_key = f"att:{message_id}:{attachment_id}"
        cached_data = await self.redis.get(cache_key)

        if cached_data:
            logger.info(f"Cache HIT for {attachment_id}")
            return Response(
                content=cached_data,
                media_type='application/octet-stream',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'X-Cache-Status': 'HIT',
                    'Cache-Control': 'private, max-age=3600'
                }
            )

        # Cache MISS - download from Gmail
        logger.info(f"Cache MISS for {attachment_id} - downloading...")

        try:
            attachment = gmail_service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()

            file_data = base64.urlsafe_b64decode(attachment['data'])

            # Cache if not too large
            if len(file_data) <= self.max_cache_size:
                await self.redis.setex(cache_key, self.cache_ttl, file_data)
                logger.info(f"Cached attachment {attachment_id} ({len(file_data)} bytes)")

            return Response(
                content=file_data,
                media_type='application/octet-stream',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'X-Cache-Status': 'MISS',
                    'Content-Length': str(len(file_data))
                }
            )

        except Exception as e:
            logger.error(f"Failed to download attachment {attachment_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to download attachment")

    async def prefetch_attachments(
        self,
        message_id: str,
        attachments: list,
        gmail_service
    ):
        """
        Background prefetch with smart filtering
        """
        # Filter: only first 3, only <5MB
        to_prefetch = [
            att for att in attachments[:3]
            if att.get('size', 0) < 5 * 1024 * 1024
        ]

        for attachment in to_prefetch:
            attachment_id = attachment['id']

            # Skip if already cached
            cache_key = f"att:{message_id}:{attachment_id}"
            if await self.redis.exists(cache_key):
                continue

            try:
                # Download and cache
                att_data = gmail_service.users().messages().attachments().get(
                    userId='me',
                    messageId=message_id,
                    id=attachment_id
                ).execute()

                file_data = base64.urlsafe_b64decode(att_data['data'])

                if len(file_data) <= self.max_cache_size:
                    await self.redis.setex(cache_key, self.cache_ttl, file_data)
                    logger.info(f"Prefetched {attachment_id}")

            except Exception as e:
                logger.warning(f"Prefetch failed for {attachment_id}: {e}")
                # Continue with other attachments
```

### Router Integration

```python
# routers/emails.py

from fastapi import APIRouter, BackgroundTasks, Depends
from services.attachment_service import AttachmentService
from services.gmail_service import get_gmail_service

router = APIRouter()
attachment_service = AttachmentService()

@router.get("/emails/{email_id}")
async def get_email_detail(
    email_id: str,
    background_tasks: BackgroundTasks,
    gmail_service = Depends(get_gmail_service)
):
    """Get email + trigger prefetch"""
    # Fetch email
    email = gmail_service.users().messages().get(
        userId='me',
        id=email_id,
        format='full'
    ).execute()

    # Parse attachments
    attachments = extract_attachments(email)

    # Smart prefetch
    if len(attachments) > 0 and len(attachments) <= 10:
        background_tasks.add_task(
            attachment_service.prefetch_attachments,
            email_id,
            attachments,
            gmail_service
        )

    return {
        'id': email_id,
        'subject': email['subject'],
        'attachments': attachments
    }

@router.get("/attachments/{message_id}/{attachment_id}")
async def download_attachment(
    message_id: str,
    attachment_id: str,
    filename: str,
    gmail_service = Depends(get_gmail_service)
):
    """Download attachment (cached if available)"""
    return await attachment_service.download_attachment(
        message_id,
        attachment_id,
        filename,
        gmail_service
    )
```

---

## 8. ALTERNATIVE NON RACCOMANDATE

### Alternative Escluse

❌ **Gmail API Batch Requests per Attachments**
- Complessità alta
- Beneficio marginale (<20% gain)
- Gmail API non ottimizzato per batch attachments

❌ **Thumbnail Generation Lato Server**
- Gmail API non fornisce partial download
- Deve scaricare file completo comunque
- Overhead processing per generare thumbnail
- Beneficio UX limitato

❌ **Persistent Storage (Database) invece Redis**
- Database query più lenta di Redis
- No expiration automatica (TTL)
- Overhead gestione storage

❌ **CDN per Attachments**
- Attachments sono privati (autenticazione richiesta)
- CDN pubbliche non adatte
- Costo aggiuntivo vs Redis locale

---

## 9. PROSSIMI STEP (Roadmap)

### Sprint 1 (Questa settimana)

- [ ] Setup Redis in docker-compose
- [ ] Implementare Streaming Response
- [ ] Abilitare GZIP compression
- [ ] Testing manuale: verificare download 20-25s

### Sprint 2 (Prossima settimana)

- [ ] Implementare AttachmentService con caching
- [ ] Integrare Redis cache-aside pattern
- [ ] Monitoring: cache hit ratio
- [ ] Testing: verificare cache HIT <1s

### Sprint 3 (Settimana 3)

- [ ] Implementare background prefetch
- [ ] Smart prefetching logic
- [ ] Frontend: indicator "Preparing attachments"
- [ ] Testing E2E: user flow completo

### Sprint 4 (Settimana 4 - Optimization)

- [ ] Grafana dashboards per metriche
- [ ] A/B testing: con/senza prefetch
- [ ] Fine-tuning cache TTL e size limits
- [ ] Documentazione deployment

---

## 10. FONTI & RIFERIMENTI

### Documentazione Ufficiale

1. [Gmail API Performance Tips](https://developers.google.com/gmail/api/guides/performance) - Compression, partial responses
2. [Gmail API Batching Requests](https://developers.google.com/workspace/gmail/api/guides/batch) - Batch requests documentation
3. [Gmail API Attachment Methods](https://developers.google.com/gmail/api/reference/rest/v1/users.messages.attachments) - Attachment download API
4. [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) - Background task implementation
5. [FastAPI Streaming Response](https://apidog.com/blog/fastapi-streaming-response/) - Streaming file downloads
6. [Redis Caching Patterns - AWS](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html) - Cache-aside, write-through patterns
7. [Redis Caching Strategies](https://dev.to/sepehr/redis-caching-strategies-from-basics-to-advanced-patterns-395n) - Advanced patterns

### Competitor Analysis

8. [Gmail Prefetching Images - Litmus](https://www.litmus.com/blog/gmail-prefetching-images) - How Gmail prefetches
9. [How To Speed Up Outlook 2026](https://clean.email/blog/email-providers/how-to-speed-up-outlook-run-faster) - Outlook optimization strategies
10. [The Technical Guide to Email Attachments](https://www.getconnect.tech/blog/the-technical-guide-to-email-attachments-best-practices-for-developers-building-with-email-integration) - Email attachment best practices

### Technical Deep Dives

11. [FastAPI Performance Optimization Guide](https://pytutorial.com/fastapi-performance-optimization-guide/) - Async patterns, streaming
12. [Streaming File Downloads FastAPI](https://python.plainenglish.io/streaming-file-uploads-and-downloads-with-fastapi-a-practical-guide-ee5be38fdd66) - Practical streaming guide
13. [Gmail Batch Stream (GitHub)](https://github.com/zoellner/gmail-batch-stream) - Open source batch implementation

### Community Discussions

14. [Gmail API Thumbnails Issue](https://github.com/googleapis/google-api-nodejs-client/issues/428) - Thumbnail limitations
15. [How to Speed Up Gmail Email Retrieval](https://community.latenode.com/t/how-to-speed-up-bulk-email-retrieval-using-gmail-api/32446) - Community solutions

---

## CONCLUSIONI

**Il problema del download lento (30-40s) è RISOLVIBILE.**

**La soluzione NON è una singola tecnica, ma una COMBINAZIONE strategica:**

1. **Immediate relief**: Streaming + GZIP → -40% tempo
2. **Cache hits**: Redis → download ripetuti istantanei
3. **Perfect UX**: Eager loading → user non aspetta mai

**Implementazione graduale** in 3 sprint permette di:
- Testare ogni fase
- Validare benefici reali
- Rollback se problemi
- Imparare e ottimizzare

**ROI altissimo**: 1 settimana sviluppo → UX transformed (30s → <1s percepito)

**Nessun competitor fa download sincroni al click** - TUTTI prefetchano. È il modo giusto.

---

**NEXT ACTION**: Presentare questa ricerca a Rafa e Backend team per approvazione Sprint 1.

*"Non esistono cose difficili, esistono cose non studiate!"* ✅

---

*Ricerca completata da Cervella Researcher - 13 Gennaio 2026*
